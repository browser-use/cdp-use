import os
import base64
import asyncio
from typing import Any


class Recorder:
    """
    Records browser frames using CDP screencast and saves them as JPEG images.
    """

    def __init__(self, client: Any, output_dir: str):
        self.client = client
        self.output_dir = output_dir
        self.frame_count = 0
        self._running = False
        self._queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()
        self._worker_task: asyncio.Task | None = None

    async def start(self) -> None:
        """
        Start recording frames.
        """
        os.makedirs(self.output_dir, exist_ok=True)
        self._running = True

        async def worker():
            while self._running or not self._queue.empty():
                event = await self._queue.get()

                self.frame_count += 1

                # Decode base64 frame into binary image
                image_data = base64.b64decode(event["data"])

                filename = os.path.join(
                    self.output_dir, f"frame_{self.frame_count:04d}.jpg"
                )

                with open(filename, "wb") as f:
                    f.write(image_data)

                print(f"Saved {filename}")

                # Acknowledge frame so Chrome continues sending frames
                await self.client.send.Page.screencastFrameAck({
                    "sessionId": event["sessionId"]
                })

                self._queue.task_done()

        def on_frame(event: dict, session_id: str) -> None:
            if self._running:
                self._queue.put_nowait(event)

        self.client.register.Page.screencastFrame(on_frame)

        self._worker_task = asyncio.create_task(worker())

        await self.client.send.Page.enable()

        await self.client.send.Page.startScreencast({
            "format": "jpeg",
            "quality": 50,
            "everyNthFrame": 1
        })

    async def stop(self) -> None:
        """
        Stop recording and finalize frame saving.
        """
        self._running = False

        await self.client.send.Page.stopScreencast()

        await self._queue.join()

        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass

        print(f"Recording saved to {self.output_dir}")