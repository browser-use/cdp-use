# This file is auto-generated by the CDP protocol generator.
# Do not edit this file manually as your changes will be overwritten.
# Generated from Chrome DevTools Protocol specifications.

"""CDP FileSystem Domain Library"""

from typing import Optional, cast

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...client import CDPClient
    from .commands import GetDirectoryParameters
    from .commands import GetDirectoryReturns

class FileSystemClient:
    """Client for FileSystem domain commands."""

    def __init__(self, client: 'CDPClient'):
        self._client = client

    async def getDirectory(
        self,
        params: "GetDirectoryParameters",
        session_id: Optional[str] = None,
    ) -> "GetDirectoryReturns":
        return cast("GetDirectoryReturns", await self._client.send_raw(
            method="FileSystem.getDirectory",
            params=params,
            session_id=session_id,
        ))


