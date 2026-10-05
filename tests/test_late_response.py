import asyncio
import importlib
import json
import unittest

from cdp_use.client import CDPClient

importlib.import_module('websockets.exceptions')


class FakeWebSocket:
    def __init__(self) -> None:
        self.inbox: asyncio.Queue[str] = asyncio.Queue()

    async def send(self, raw: str) -> None:
        pass

    async def recv(self) -> str:
        return await self.inbox.get()

    async def close(self) -> None:
        pass


class TestLateResponses(unittest.IsolatedAsyncioTestCase):
    async def test_cancelled_request_late_response_is_not_logged_as_duplicate(self) -> None:
        client = CDPClient("ws://127.0.0.1:9/devtools/browser/test")
        client.ws = FakeWebSocket()
        reader = asyncio.create_task(client._handle_messages())

        try:
            with self.assertRaises(TimeoutError):
                await asyncio.wait_for(
                    client.send_raw("Page.navigate", {"url": "about:blank"}),
                    timeout=0.01,
                )

            self.assertEqual(list(client.pending_requests), [1])

            with self.assertLogs("cdp_use.client", level="DEBUG") as logs:
                await client.ws.inbox.put(json.dumps({"id": 1, "result": {}}))
                await asyncio.wait_for(self._wait_until_no_pending_requests(client), timeout=1.0)

            self.assertEqual(
                logs.output,
                ["DEBUG:cdp_use.client:Received response for cancelled request 1 - ignoring"],
            )
            self.assertEqual(client.pending_requests, {})
        finally:
            reader.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await reader

    async def _wait_until_no_pending_requests(self, client: CDPClient) -> None:
        while client.pending_requests:
            await asyncio.sleep(0)


if __name__ == "__main__":
    unittest.main()
