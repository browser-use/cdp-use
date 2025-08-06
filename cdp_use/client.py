import asyncio
import json
import logging
import re
import time
from typing import TYPE_CHECKING, Any, Dict, Optional

import websockets

if TYPE_CHECKING:
    from cdp_use.cdp.library import CDPLibrary
    from cdp_use.cdp.registration_library import CDPRegistrationLibrary
    from cdp_use.cdp.registry import EventRegistry

# Set up logging
logger = logging.getLogger(__name__)

# Custom formatter for websocket messages
class WebSocketLogFilter(logging.Filter):
    def __init__(self):
        super().__init__()
        self.ping_times = {}  # Track ping send times by ping data
        self.ping_timeout_tasks = {}  # Track timeout tasks
        
    def filter(self, record):
        # Only process websocket client messages
        if record.name != 'websockets.client':
            return True
            
        # Change the logger name
        record.name = 'cdp_use.client'
        
        # Process the message
        msg = record.getMessage()
        
        # Handle PING/PONG sequences
        if '> PING' in msg:
            # Extract ping data (e.g., "9d 20 7c 5c")
            match = re.search(r'> PING ([a-f0-9 ]+) \[binary', msg)
            if match:
                ping_data = match.group(1)
                self.ping_times[ping_data] = time.time()
                
                # Schedule timeout warning
                async def check_timeout():
                    await asyncio.sleep(3)
                    if ping_data in self.ping_times:
                        # Still waiting for PONG after 3 seconds
                        del self.ping_times[ping_data]
                        timeout_logger = logging.getLogger('cdp_use.client')
                        timeout_logger.warning('⚠️ PING not answered by browser... (>3s and no PONG received)')
                
                # Try to schedule the timeout check
                try:
                    loop = asyncio.get_event_loop()
                    self.ping_timeout_tasks[ping_data] = loop.create_task(check_timeout())
                except RuntimeError:
                    # No event loop available, skip timeout check
                    pass
                    
            return False  # Suppress the PING message
            
        elif '< PONG' in msg:
            # Extract pong data
            match = re.search(r'< PONG ([a-f0-9 ]+) \[binary', msg)
            if match:
                pong_data = match.group(1)
                if pong_data in self.ping_times:
                    # Calculate round-trip time
                    elapsed = (time.time() - self.ping_times[pong_data]) * 1000
                    del self.ping_times[pong_data]
                    
                    # Cancel timeout task if exists
                    if pong_data in self.ping_timeout_tasks:
                        self.ping_timeout_tasks[pong_data].cancel()
                        del self.ping_timeout_tasks[pong_data]
                    
                    # Update message to show consolidated PING status
                    record.msg = f'✔ PING ({elapsed:.1f}ms)'
                    record.args = ()
                    return True
            return False  # Suppress if we can't match it
            
        elif '% sent keepalive ping' in msg or '% received keepalive pong' in msg:
            # Suppress keepalive status messages
            return False
            
        # Handle HTTP handshake messages (websockets library uses > for outgoing, < for incoming)
        elif '> GET ' in msg or '> Host:' in msg or '> Upgrade:' in msg or '> Connection:' in msg or '> Sec-WebSocket' in msg or '> User-Agent:' in msg:
            # Outgoing HTTP request headers (we send to server)
            # Keep as is - these are correct
            record.msg = msg
            record.args = ()
            return True
            
        elif '< HTTP/' in msg or '< Upgrade:' in msg or '< Connection:' in msg or '< Sec-WebSocket' in msg:
            # Incoming HTTP response headers (server sends to us)
            # Keep as is - these are correct
            record.msg = msg
            record.args = ()
            return True
            
        elif '= connection is' in msg:
            # Connection state messages - make them more subtle
            if 'CONNECTING' in msg:
                record.msg = '🔗 Connecting...'
            elif 'OPEN' in msg:
                record.msg = '✅ Connected'
            elif 'CLOSING' in msg or 'CLOSED' in msg:
                record.msg = '🔌 Disconnected'
            else:
                # Keep original message but clean it up
                msg = msg.replace('= ', '')
                record.msg = msg
            record.args = ()
            return True
            
        # Process CDP messages
        # websockets library uses > for outgoing (we send), < for incoming (we receive)
        # We want to show: ← for what we send to browser, → for what browser sends to us
        elif '> TEXT' in msg or '< TEXT' in msg:
            # Parse the message to extract JSON and size
            
            # Extract direction, JSON content, and size
            # > TEXT means we're sending to browser
            # < TEXT means we're receiving from browser
            is_outgoing = '> TEXT' in msg
            
            # Extract JSON content and size from message
            match = re.search(r'[<>] TEXT [\'"]?(.*?)[\'"]? \[(\d+) bytes\]', msg)
            if match:
                json_str = match.group(1)
                size_bytes = int(match.group(2))
                
                try:
                    # Parse JSON to extract method, id, params/result
                    data = json.loads(json_str)
                    
                    # Format size (only show if > 5kb)
                    size_str = ''
                    if size_bytes > 5120:  # 5kb = 5120 bytes
                        size_kb = size_bytes / 1024
                        size_str = f' [{size_kb:.0f}kb]'
                    
                    if is_outgoing:
                        # We're sending to browser (outgoing request)
                        if 'method' in data and 'id' in data:
                            method = data['method']
                            params = data.get('params', {})
                            msg_id = data['id']
                            # Format params without quotes
                            params_str = str(params).replace("'", "").replace('"', '')
                            record.msg = f'🌎 ← #{msg_id}: {method}({params_str}){size_str}'
                        else:
                            # Fallback for non-standard messages
                            json_clean = str(data).replace("'", "").replace('"', '')
                            record.msg = f'🌎 ← {json_clean}{size_str}'
                    else:
                        # Browser is sending to us (incoming response/event)
                        if 'id' in data and 'result' in data:
                            msg_id = data['id']
                            result = data.get('result', {})
                            # Format result without quotes, truncate if needed
                            result_str = str(result).replace("'", "").replace('"', '')
                            if len(result_str) > 100:
                                result_str = result_str[:100] + '...'
                            record.msg = f'🌎 → #{msg_id}: ↳ {result_str}{size_str}'
                        elif 'id' in data and 'error' in data:
                            msg_id = data['id']
                            error = data.get('error', {})
                            error_str = str(error).replace("'", "").replace('"', '')
                            record.msg = f'🌎 → #{msg_id}: ❌ {error_str}{size_str}'
                        elif 'method' in data:
                            # Event from browser
                            method = data['method']
                            params = data.get('params', {})
                            params_str = str(params).replace("'", "").replace('"', '')
                            if len(params_str) > 100:
                                params_str = params_str[:100] + '...'
                            record.msg = f'🌎 → Event: {method}({params_str}){size_str}'
                        else:
                            # Fallback
                            json_clean = str(data).replace("'", "").replace('"', '')
                            record.msg = f'🌎 → {json_clean}{size_str}'
                    
                    record.args = ()
                    return True
                except (json.JSONDecodeError, KeyError):
                    # If we can't parse JSON, just clean up the message
                    pass
            
        # Handle EOF messages - suppress individual EOF messages
        elif '> EOF' in msg or '< EOF' in msg:
            # Suppress EOF messages - they're not useful
            return False
            
        # Handle other connection-related messages
        elif 'x half-closing TCP connection' in msg:
            record.msg = '👋 Closing our half of the TCP connection'
            record.args = ()
            return True
            
        # Handle connection closed with EOF
        elif 'WebSocket connection closed' in msg and 'EOF' in msg:
            record.msg = '❌ CDP connection closed (EOF)'
            record.args = ()
            return True
            
        # Fallback - translate all arrow directions consistently
        # websockets uses: > for outgoing (we send), < for incoming (we receive)
        # We want: ← for outgoing, → for incoming
        
        # First handle any remaining > or < prefixes
        if msg.startswith('>'):
            msg = '←' + msg[1:]
        elif msg.startswith('<'):
            msg = '→' + msg[1:]
        
        # Clean up any quotes
        msg = re.sub(r"['\"]", '', msg)
        
        # Update the message
        record.msg = msg
        record.args = ()
        
        return True

# Configure websockets logger
ws_logger = logging.getLogger('websockets.client')
ws_logger.addFilter(WebSocketLogFilter())


class CDPClient:
    def __init__(self, url: str):
        self.url = url
        self.ws: Optional[websockets.ClientConnection] = None
        self.msg_id: int = 0
        self.pending_requests: Dict[int, asyncio.Future] = {}
        self._message_handler_task = None
        # self.event_handlers: Dict[str, Callable] = {}

        # Initialize the type-safe CDP library
        from cdp_use.cdp.library import CDPLibrary
        from cdp_use.cdp.registration_library import CDPRegistrationLibrary
        from cdp_use.cdp.registry import EventRegistry

        self.send: "CDPLibrary" = CDPLibrary(self)
        self._event_registry: "EventRegistry" = EventRegistry()
        self.register: "CDPRegistrationLibrary" = CDPRegistrationLibrary(
            self._event_registry
        )

    async def __aenter__(self):
        """Async context manager entry"""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.stop()

    # def on_event(self, method: str, handler: Callable):
    #     """Register an event handler for CDP events"""
    #     self.event_handlers[method] = handler

    async def start(self):
        """Start the WebSocket connection and message handler task"""
        if self.ws is not None:
            raise RuntimeError("Client is already started")

        logger.info(f"Connecting to {self.url}")
        self.ws = await websockets.connect(
            self.url,
            max_size=100 * 1024 * 1024,  # 100MB limit instead of default 1MB
        )
        self._message_handler_task = asyncio.create_task(self._handle_messages())

    async def stop(self):
        """Stop the message handler and close the WebSocket connection"""
        # Cancel the message handler task
        if self._message_handler_task:
            self._message_handler_task.cancel()
            try:
                await self._message_handler_task
            except asyncio.CancelledError:
                pass
            self._message_handler_task = None

        # Cancel all pending requests
        for future in self.pending_requests.values():
            if not future.done():
                future.set_exception(ConnectionError("Client is stopping"))
        self.pending_requests.clear()

        # Close the websocket connection
        if self.ws:
            await self.ws.close()
            self.ws = None

    async def _handle_messages(self):
        """Continuously handle incoming messages"""
        try:
            while True:
                if not self.ws:
                    break

                raw = await self.ws.recv()
                data = json.loads(raw)

                # Handle response messages (with id)
                if "id" in data and data["id"] in self.pending_requests:
                    future = self.pending_requests.pop(data["id"])
                    if "error" in data:
                        logger.error(
                            f"CDP Error for request {data['id']}: {data['error']}"
                        )
                        future.set_exception(RuntimeError(data["error"]))
                    else:
                        future.set_result(data["result"])

                # Handle event messages (without id, but with method)
                elif "method" in data:
                    method = data["method"]
                    params = data.get("params", {})
                    session_id = data.get("sessionId")

                    # logger.debug(f"Received event: {method} (session: {session_id})")

                    # Call registered event handler if available
                    handled = self._event_registry.handle_event(
                        method, params, session_id
                    )
                    if not handled:
                        # logger.debug(f"No handler registered for event: {method}")
                        pass

                # Handle unexpected messages
                else:
                    logger.warning(f"Received unexpected message: {data}")

        except websockets.exceptions.ConnectionClosed as e:
            logger.warning(f"WebSocket connection closed: {e}")
            # Connection closed, resolve all pending futures with an exception
            for future in self.pending_requests.values():
                if not future.done():
                    future.set_exception(ConnectionError("WebSocket connection closed"))
            self.pending_requests.clear()
        except Exception as e:
            logger.error(f"Error in message handler: {e}")
            # Handle other exceptions
            for future in self.pending_requests.values():
                if not future.done():
                    future.set_exception(e)
            self.pending_requests.clear()

    async def send_raw(
        self,
        method: str,
        params: Optional[Any] = None,
        session_id: Optional[str] = None,
    ) -> dict[str, Any]:
        if not self.ws:
            raise RuntimeError(
                "Client is not started. Call start() first or use as async context manager."
            )

        self.msg_id += 1
        msg = {
            "id": int(self.msg_id),
            "method": method,
            "params": params or {},
        }

        if session_id:
            msg["sessionId"] = session_id

        # Create a future for this request
        future = asyncio.Future()
        self.pending_requests[self.msg_id] = future

        # logger.debug(f"Sending: {method} (id: {self.msg_id}, session: {session_id})")
        await self.ws.send(json.dumps(msg))

        # Wait for the response
        return await future
