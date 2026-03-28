import asyncio
from cdp_use.client import CDPClient


async def main():
    ws_url = "ws://localhost:9222/devtools/page/XXXX"

    async with CDPClient(ws_url) as client:
        # Start recording browser session
        recorder = await client.start_recording("recording_output")

        try:
            # Perform actions while recording
            await client.send.Page.navigate({"url": "https://youtube.com"})
            await asyncio.sleep(5)
        finally:
            # Ensure recording is properly stopped
            await recorder.stop()


asyncio.run(main())