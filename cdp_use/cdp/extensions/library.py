# This file is auto-generated by the CDP protocol generator.
# Do not edit this file manually as your changes will be overwritten.
# Generated from Chrome DevTools Protocol specifications.

"""CDP Extensions Domain Library"""

from typing import Any, Dict, Optional, cast

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...client import CDPClient
    from .commands import ClearStorageItemsParameters
    from .commands import GetStorageItemsParameters
    from .commands import GetStorageItemsReturns
    from .commands import LoadUnpackedParameters
    from .commands import LoadUnpackedReturns
    from .commands import RemoveStorageItemsParameters
    from .commands import SetStorageItemsParameters
    from .commands import UninstallParameters

class ExtensionsClient:
    """Client for Extensions domain commands."""

    def __init__(self, client: 'CDPClient'):
        self._client = client

    async def loadUnpacked(
        self,
        params: "LoadUnpackedParameters",
        session_id: Optional[str] = None,
    ) -> "LoadUnpackedReturns":
        """Installs an unpacked extension from the filesystem similar to
--load-extension CLI flags. Returns extension ID once the extension
has been installed. Available if the client is connected using the
--remote-debugging-pipe flag and the --enable-unsafe-extension-debugging
flag is set."""
        return cast("LoadUnpackedReturns", await self._client.send_raw(
            method="Extensions.loadUnpacked",
            params=params,
            session_id=session_id,
        ))

    async def uninstall(
        self,
        params: "UninstallParameters",
        session_id: Optional[str] = None,
    ) -> "Dict[str, Any]":
        """Uninstalls an unpacked extension (others not supported) from the profile.
Available if the client is connected using the --remote-debugging-pipe flag
and the --enable-unsafe-extension-debugging."""
        return cast("Dict[str, Any]", await self._client.send_raw(
            method="Extensions.uninstall",
            params=params,
            session_id=session_id,
        ))

    async def getStorageItems(
        self,
        params: "GetStorageItemsParameters",
        session_id: Optional[str] = None,
    ) -> "GetStorageItemsReturns":
        """Gets data from extension storage in the given `storageArea`. If `keys` is
specified, these are used to filter the result."""
        return cast("GetStorageItemsReturns", await self._client.send_raw(
            method="Extensions.getStorageItems",
            params=params,
            session_id=session_id,
        ))

    async def removeStorageItems(
        self,
        params: "RemoveStorageItemsParameters",
        session_id: Optional[str] = None,
    ) -> "Dict[str, Any]":
        """Removes `keys` from extension storage in the given `storageArea`."""
        return cast("Dict[str, Any]", await self._client.send_raw(
            method="Extensions.removeStorageItems",
            params=params,
            session_id=session_id,
        ))

    async def clearStorageItems(
        self,
        params: "ClearStorageItemsParameters",
        session_id: Optional[str] = None,
    ) -> "Dict[str, Any]":
        """Clears extension storage in the given `storageArea`."""
        return cast("Dict[str, Any]", await self._client.send_raw(
            method="Extensions.clearStorageItems",
            params=params,
            session_id=session_id,
        ))

    async def setStorageItems(
        self,
        params: "SetStorageItemsParameters",
        session_id: Optional[str] = None,
    ) -> "Dict[str, Any]":
        """Sets `values` in extension storage in the given `storageArea`. The provided `values`
will be merged with existing values in the storage area."""
        return cast("Dict[str, Any]", await self._client.send_raw(
            method="Extensions.setStorageItems",
            params=params,
            session_id=session_id,
        ))


