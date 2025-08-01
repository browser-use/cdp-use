# This file is auto-generated by the CDP protocol generator.
# Do not edit this file manually as your changes will be overwritten.
# Generated from Chrome DevTools Protocol specifications.

"""CDP Cast Domain Library"""

from typing import Any, Dict, Optional, cast

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...client import CDPClient
    from .commands import EnableParameters
    from .commands import SetSinkToUseParameters
    from .commands import StartDesktopMirroringParameters
    from .commands import StartTabMirroringParameters
    from .commands import StopCastingParameters

class CastClient:
    """Client for Cast domain commands."""

    def __init__(self, client: 'CDPClient'):
        self._client = client

    async def enable(
        self,
        params: Optional["EnableParameters"] = None,
        session_id: Optional[str] = None,
    ) -> "Dict[str, Any]":
        """Starts observing for sinks that can be used for tab mirroring, and if set,
sinks compatible with |presentationUrl| as well. When sinks are found, a
|sinksUpdated| event is fired.
Also starts observing for issue messages. When an issue is added or removed,
an |issueUpdated| event is fired."""
        return cast("Dict[str, Any]", await self._client.send_raw(
            method="Cast.enable",
            params=params,
            session_id=session_id,
        ))

    async def disable(
        self,
        params: None = None,
        session_id: Optional[str] = None,
    ) -> "Dict[str, Any]":
        """Stops observing for sinks and issues."""
        return cast("Dict[str, Any]", await self._client.send_raw(
            method="Cast.disable",
            params=params,
            session_id=session_id,
        ))

    async def setSinkToUse(
        self,
        params: "SetSinkToUseParameters",
        session_id: Optional[str] = None,
    ) -> "Dict[str, Any]":
        """Sets a sink to be used when the web page requests the browser to choose a
sink via Presentation API, Remote Playback API, or Cast SDK."""
        return cast("Dict[str, Any]", await self._client.send_raw(
            method="Cast.setSinkToUse",
            params=params,
            session_id=session_id,
        ))

    async def startDesktopMirroring(
        self,
        params: "StartDesktopMirroringParameters",
        session_id: Optional[str] = None,
    ) -> "Dict[str, Any]":
        """Starts mirroring the desktop to the sink."""
        return cast("Dict[str, Any]", await self._client.send_raw(
            method="Cast.startDesktopMirroring",
            params=params,
            session_id=session_id,
        ))

    async def startTabMirroring(
        self,
        params: "StartTabMirroringParameters",
        session_id: Optional[str] = None,
    ) -> "Dict[str, Any]":
        """Starts mirroring the tab to the sink."""
        return cast("Dict[str, Any]", await self._client.send_raw(
            method="Cast.startTabMirroring",
            params=params,
            session_id=session_id,
        ))

    async def stopCasting(
        self,
        params: "StopCastingParameters",
        session_id: Optional[str] = None,
    ) -> "Dict[str, Any]":
        """Stops the active Cast session on the sink."""
        return cast("Dict[str, Any]", await self._client.send_raw(
            method="Cast.stopCasting",
            params=params,
            session_id=session_id,
        ))


