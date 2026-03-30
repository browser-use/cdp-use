# ABOUTME: Tests for three specific fixes in recorder.py and client.py.
# ABOUTME: Covers try/finally task_done, double-start guard, and _recorder back-ref clearing.

import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

from cdp_use.recorder import Recorder


def make_fake_client():
    """Return a minimal fake client that stubs the CDP calls Recorder needs."""
    client = MagicMock()
    client._recorder = None
    client.send.Page.enable = AsyncMock()
    client.send.Page.startScreencast = AsyncMock()
    client.send.Page.stopScreencast = AsyncMock()
    client.send.Page.screencastFrameAck = AsyncMock()
    # register.Page.screencastFrame just stores the callback; capture it for tests
    client.register.Page.screencastFrame = MagicMock()
    return client


# ---------------------------------------------------------------------------
# Fix 1: try/finally ensures task_done() is called even when frame processing
# raises, so queue.join() doesn't hang.
# ---------------------------------------------------------------------------

def test_task_done_called_after_frame_processing_exception():
    async def run():
        client = make_fake_client()
        recorder = Recorder(client, "/tmp/test_frames")

        await recorder.start()

        # Grab the on_frame callback that was registered
        on_frame = client.register.Page.screencastFrame.call_args[0][0]

        # Push a malformed event — missing "data" key — so base64.b64decode raises
        on_frame({"sessionId": "abc"}, "abc")

        # queue.join() must complete; if task_done() wasn't called it would hang
        await asyncio.wait_for(recorder._queue.join(), timeout=2.0)

        recorder._running = False
        recorder._worker_task.cancel()
        try:
            await recorder._worker_task
        except (asyncio.CancelledError, KeyError):
            pass

    asyncio.run(run())


# ---------------------------------------------------------------------------
# Fix 2: Calling start_recording() twice raises RuntimeError.
# ---------------------------------------------------------------------------

def test_start_recording_twice_raises():
    async def run():
        from cdp_use.client import CDPClient

        client = CDPClient("ws://fake")
        # Simulate a recorder already being active
        client._recorder = object()

        with pytest.raises(RuntimeError, match="Recording already in progress"):
            await client.start_recording("/tmp/out")

    asyncio.run(run())


# ---------------------------------------------------------------------------
# Fix 3: After recorder.stop(), client._recorder is cleared to None.
# ---------------------------------------------------------------------------

def test_recorder_stop_clears_client_back_ref():
    async def run():
        client = make_fake_client()
        recorder = Recorder(client, "/tmp/test_frames")

        await recorder.start()

        # Point the client back-ref at this recorder (as start_recording() does)
        client._recorder = recorder

        await recorder.stop()

        assert client._recorder is None

    asyncio.run(run())
