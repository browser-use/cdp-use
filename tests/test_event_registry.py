import asyncio
import unittest

from cdp_use.cdp.registry import EventRegistry


class TestEventRegistry(unittest.IsolatedAsyncioTestCase):
    async def test_registering_two_handlers_for_same_event_calls_both(self) -> None:
        registry = EventRegistry()
        calls: list[str] = []

        registry.register(
            "Network.responseReceived",
            lambda params, session_id=None: calls.append("first"),
        )
        registry.register(
            "Network.responseReceived",
            lambda params, session_id=None: calls.append("second"),
        )

        handled = await registry.handle_event(
            "Network.responseReceived",
            {"requestId": "1"},
            None,
        )

        self.assertTrue(handled)
        self.assertEqual(calls, ["first", "second"])

    async def test_async_handlers_are_awaited_in_registration_order(self) -> None:
        registry = EventRegistry()
        calls: list[str] = []

        async def first(params, session_id=None):
            await asyncio.sleep(0)
            calls.append("first")

        async def second(params, session_id=None):
            await asyncio.sleep(0)
            calls.append("second")

        registry.register("Network.responseReceived", first)
        registry.register("Network.responseReceived", second)

        handled = await registry.handle_event(
            "Network.responseReceived",
            {"requestId": "1"},
            None,
        )

        self.assertTrue(handled)
        self.assertEqual(calls, ["first", "second"])

    async def test_failing_handler_does_not_suppress_later_handlers(self) -> None:
        registry = EventRegistry()
        calls: list[str] = []

        def failing(params, session_id=None):
            calls.append("failing")
            raise RuntimeError("boom")

        def later(params, session_id=None):
            calls.append("later")

        registry.register("Network.responseReceived", failing)
        registry.register("Network.responseReceived", later)

        with self.assertLogs("cdp_use.cdp.registry", level="ERROR") as logs:
            handled = await registry.handle_event(
                "Network.responseReceived",
                {"requestId": "1"},
                None,
            )

        self.assertFalse(handled)
        self.assertEqual(calls, ["failing", "later"])
        self.assertEqual(
            logs.output,
            ["ERROR:cdp_use.cdp.registry:Error in event handler for Network.responseReceived: boom"],
        )

    async def test_unregister_removes_all_handlers_for_method(self) -> None:
        registry = EventRegistry()
        calls: list[str] = []

        registry.register(
            "Network.responseReceived",
            lambda params, session_id=None: calls.append("first"),
        )
        registry.register(
            "Network.responseReceived",
            lambda params, session_id=None: calls.append("second"),
        )

        registry.unregister("Network.responseReceived")

        handled = await registry.handle_event(
            "Network.responseReceived",
            {"requestId": "1"},
            None,
        )

        self.assertFalse(handled)
        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
