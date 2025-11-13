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
        if record.name != "websockets.client":
            return True

        # Change the logger name
        record.name = "cdp_use.client"

        # Process the message
        msg = record.getMessage()

        # === SPECIAL CASES (suppress or consolidate) ===

        # Handle PING/PONG sequences
        if "> PING" in msg:
            match = re.search(r"> PING ([a-f0-9 ]+) \[binary", msg)
            if match:
                ping_data = match.group(1)
                self.ping_times[ping_data] = time.time()

                # Schedule timeout warning
                async def check_timeout():
                    await asyncio.sleep(3)
                    if ping_data in self.ping_times:
                        del self.ping_times[ping_data]
                        timeout_logger = logging.getLogger("cdp_use.client")
                        timeout_logger.warning(
                            "⚠️ PING not answered by browser... (>3s and no PONG received)"
                        )

                try:
                    loop = asyncio.get_event_loop()
                    self.ping_timeout_tasks[ping_data] = loop.create_task(
                        check_timeout()
                    )
                except RuntimeError:
                    pass

            return False  # Suppress the PING message

        elif "< PONG" in msg:
            match = re.search(r"< PONG ([a-f0-9 ]+) \[binary", msg)
            if match:
                pong_data = match.group(1)
                if pong_data in self.ping_times:
                    elapsed = (time.time() - self.ping_times[pong_data]) * 1000
                    del self.ping_times[pong_data]

                    if pong_data in self.ping_timeout_tasks:
                        self.ping_timeout_tasks[pong_data].cancel()
                        del self.ping_timeout_tasks[pong_data]

                    record.msg = f"✔ PING ({elapsed:.1f}ms)"
                    record.args = ()
                    return True
            return False

        # Suppress keepalive and EOF messages
        elif (
            "% sent keepalive ping" in msg
            or "% received keepalive pong" in msg
            or "> EOF" in msg
            or "< EOF" in msg
        ):
            return False

        # Connection state messages
        elif "= connection is" in msg:
            if "CONNECTING" in msg:
                record.msg = "🔗 Connecting..."
            elif "OPEN" in msg:
                record.msg = "✅ Connected"
            elif "CLOSING" in msg or "CLOSED" in msg:
                record.msg = "🔌 Disconnected"
            else:
                msg = msg.replace("= ", "")
                record.msg = msg
            record.args = ()
            return True

        elif "x half-closing TCP connection" in msg:
            record.msg = "👋 Closing our half of the TCP connection"
            record.args = ()
            return True

        # === GENERIC PROCESSING ===

        # Parse CDP messages - be flexible with regex matching
        if "TEXT" in msg:
            # Determine direction
            is_outgoing = ">" in msg[:10]  # Check start of message for direction

            # Extract and handle size
            size_match = re.search(r"\[(\d+) bytes\]", msg)
            if size_match:
                size_bytes = int(size_match.group(1))
                # Only show size if > 5kb
                size_str = f" [{size_bytes // 1024}kb]" if size_bytes > 5120 else ""
                # Remove size from message for cleaner parsing
                msg_clean = msg[: msg.rfind("[")].strip() if "[" in msg else msg
            else:
                size_str = ""
                msg_clean = msg

            # Extract id (flexible)
            id_match = re.search(r'(?:"id":|id:)\s*(\d+)', msg_clean)
            msg_id = id_match.group(1) if id_match else None

            # Extract method (flexible)
            method_match = re.search(
                r'(?:"method":|method:)\s*"?([A-Za-z.]+)', msg_clean
            )
            method = method_match.group(1) if method_match else None

            # Remove quotes from entire message for cleaner output
            msg_clean = msg_clean.replace('"', "")

            # Build formatted message based on what we found
            if is_outgoing and msg_id and method:
                # Outgoing request
                params_match = re.search(r"(?:params:)\s*({[^}]*})", msg_clean)
                params_str = params_match.group(1) if params_match else ""

                if params_str == "{}" or not params_str:
                    record.msg = f"🌎 ← #{msg_id}: {method}(){size_str}"
                else:
                    record.msg = f"🌎 ← #{msg_id}: {method}({params_str}){size_str}"
                record.args = ()
                return True

            elif not is_outgoing and msg_id:
                # Incoming response
                if "result:" in msg_clean:
                    # Extract whatever comes after result:
                    result_match = re.search(r"result:\s*({.*})", msg_clean)
                    if result_match:
                        result_str = result_match.group(1)

                        # Clean up common artifacts
                        result_str = re.sub(r"},?sessionId:[^}]*}?$", "}", result_str)

                        # Suppress empty results
                        if result_str == "{}":
                            return False

                        # Truncate if too long
                        if len(result_str) > 200:
                            result_str = result_str[:200] + "..."

                        record.msg = f"🌎 → #{msg_id}: ↳ {result_str}{size_str}"
                        record.args = ()
                        return True

                elif "error:" in msg_clean:
                    error_match = re.search(r"error:\s*({[^}]*})", msg_clean)
                    error_str = error_match.group(1) if error_match else "error"
                    record.msg = f"🌎 → #{msg_id}: ❌ {error_str}{size_str}"
                    record.args = ()
                    return True

            elif not is_outgoing and method:
                # Event
                params_match = re.search(r"params:\s*({.*})", msg_clean)
                params_str = params_match.group(1) if params_match else ""

                # Clean up common artifacts
                params_str = re.sub(r"},?sessionId:[^}]*}?$", "}", params_str)

                # Truncate if too long
                if len(params_str) > 200:
                    params_str = params_str[:200] + "..."

                if params_str == "{}" or not params_str:
                    record.msg = f"🌎 → Event: {method}(){size_str}"
                else:
                    record.msg = f"🌎 → Event: {method}({params_str}){size_str}"
                record.args = ()
                return True

        # === GENERIC ARROW REPLACEMENT ===
        # Replace all arrows: > becomes ←, < becomes →
        # Add emoji for TEXT messages
        if " TEXT " in msg:
            msg = re.sub(r"^>", "🌎 ←", msg)
            msg = re.sub(r"^<", "🌎 →", msg)
            msg = msg.replace(" TEXT ", " ")
        else:
            msg = re.sub(r"^>", "←", msg)
            msg = re.sub(r"^<", "→", msg)

        # Remove all quotes
        msg = re.sub(r"['\"]", "", msg)

        record.msg = msg
        record.args = ()
        return True


# Configure websockets logger
ws_logger = logging.getLogger("websockets.client")
ws_logger.addFilter(WebSocketLogFilter())


class CDPClient:
    def __init__(
        self,
        url: str,
        additional_headers: Optional[Dict[str, str]] = None,
        max_ws_frame_size: int = 100 * 1024 * 1024,  # Default 100MB
    ):
        self.url = url
        self.additional_headers = additional_headers
        self.max_ws_frame_size = max_ws_frame_size
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

        logger.info(
            f"Connecting to {self.url} (max frame size: {self.max_ws_frame_size / 1024 / 1024:.0f}MB)"
        )
        connect_kwargs = {
            "max_size": self.max_ws_frame_size,
        }
        if self.additional_headers:
            connect_kwargs["additional_headers"] = self.additional_headers
        self.ws = await websockets.connect(self.url, **connect_kwargs)
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
                    # Check if future is already done to avoid InvalidStateError
                    if not future.done():
                        if "error" in data:
                            logger.debug(
                                f"CDP Error for request {data['id']}: {data['error']}"
                            )
                            future.set_exception(RuntimeError(data["error"]))
                        else:
                            future.set_result(data["result"])
                    else:
                        logger.warning(
                            f"Received duplicate response for request {data['id']} - ignoring"
                        )

                # Handle event messages (without id, but with method)
                elif "method" in data:
                    method = data["method"]
                    params = data.get("params", {})
                    session_id = data.get("sessionId")

                    # logger.debug(f"Received event: {method} (session: {session_id})")

                    # Call registered event handler if available
                    handled = await self._event_registry.handle_event(
                        method, params, session_id
                    )
                    if not handled:
                        # logger.debug(f"No handler registered for event: {method}")
                        pass

                # Handle unexpected messages
                else:
                    logger.warning(f"Received unexpected message: {data}")

        except websockets.exceptions.ConnectionClosed as e:
            logger.debug(f"WebSocket connection closed: {e}")
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
