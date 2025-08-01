# This file is auto-generated by the CDP protocol generator.
# Do not edit this file manually as your changes will be overwritten.
# Generated from Chrome DevTools Protocol specifications.

"""CDP Browser Domain Commands"""

from typing import List
from typing_extensions import NotRequired, TypedDict

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..target.types import TargetID
    from .types import Bounds
    from .types import BrowserCommandId
    from .types import BrowserContextID
    from .types import Histogram
    from .types import PermissionDescriptor
    from .types import PermissionSetting
    from .types import PermissionType
    from .types import PrivacySandboxAPI
    from .types import WindowID

class SetPermissionParameters(TypedDict):
    permission: "PermissionDescriptor"
    """Descriptor of permission to override."""
    setting: "PermissionSetting"
    """Setting of the permission."""
    origin: "NotRequired[str]"
    """Origin the permission applies to, all origins if not specified."""
    browserContextId: "NotRequired[BrowserContextID]"
    """Context to override. When omitted, default browser context is used."""





class GrantPermissionsParameters(TypedDict):
    permissions: "List[PermissionType]"
    origin: "NotRequired[str]"
    """Origin the permission applies to, all origins if not specified."""
    browserContextId: "NotRequired[BrowserContextID]"
    """BrowserContext to override permissions. When omitted, default browser context is used."""





class ResetPermissionsParameters(TypedDict, total=False):
    browserContextId: "BrowserContextID"
    """BrowserContext to reset permissions. When omitted, default browser context is used."""





class SetDownloadBehaviorParameters(TypedDict):
    behavior: "str"
    """Whether to allow all or deny all download requests, or use default Chrome behavior if
available (otherwise deny). |allowAndName| allows download and names files according to
their download guids."""
    browserContextId: "NotRequired[BrowserContextID]"
    """BrowserContext to set download behavior. When omitted, default browser context is used."""
    downloadPath: "NotRequired[str]"
    """The default path to save downloaded files to. This is required if behavior is set to 'allow'
or 'allowAndName'."""
    eventsEnabled: "NotRequired[bool]"
    """Whether to emit download events (defaults to false)."""





class CancelDownloadParameters(TypedDict):
    guid: "str"
    """Global unique identifier of the download."""
    browserContextId: "NotRequired[BrowserContextID]"
    """BrowserContext to perform the action in. When omitted, default browser context is used."""





class GetVersionReturns(TypedDict):
    protocolVersion: "str"
    """Protocol version."""
    product: "str"
    """Product name."""
    revision: "str"
    """Product revision."""
    userAgent: "str"
    """User-Agent."""
    jsVersion: "str"
    """V8 version."""



class GetBrowserCommandLineReturns(TypedDict):
    arguments: "List[str]"
    """Commandline parameters"""



class GetHistogramsParameters(TypedDict, total=False):
    query: "str"
    """Requested substring in name. Only histograms which have query as a
substring in their name are extracted. An empty or absent query returns
all histograms."""
    delta: "bool"
    """If true, retrieve delta since last delta call."""


class GetHistogramsReturns(TypedDict):
    histograms: "List[Histogram]"
    """Histograms."""



class GetHistogramParameters(TypedDict):
    name: "str"
    """Requested histogram name."""
    delta: "NotRequired[bool]"
    """If true, retrieve delta since last delta call."""


class GetHistogramReturns(TypedDict):
    histogram: "Histogram"
    """Histogram."""



class GetWindowBoundsParameters(TypedDict):
    windowId: "WindowID"
    """Browser window id."""


class GetWindowBoundsReturns(TypedDict):
    bounds: "Bounds"
    """Bounds information of the window. When window state is 'minimized', the restored window
position and size are returned."""



class GetWindowForTargetParameters(TypedDict, total=False):
    targetId: "TargetID"
    """Devtools agent host id. If called as a part of the session, associated targetId is used."""


class GetWindowForTargetReturns(TypedDict):
    windowId: "WindowID"
    """Browser window id."""
    bounds: "Bounds"
    """Bounds information of the window. When window state is 'minimized', the restored window
position and size are returned."""



class SetWindowBoundsParameters(TypedDict):
    windowId: "WindowID"
    """Browser window id."""
    bounds: "Bounds"
    """New window bounds. The 'minimized', 'maximized' and 'fullscreen' states cannot be combined
with 'left', 'top', 'width' or 'height'. Leaves unspecified fields unchanged."""





class SetContentsSizeParameters(TypedDict):
    windowId: "WindowID"
    """Browser window id."""
    width: "NotRequired[int]"
    """The window contents width in DIP. Assumes current width if omitted.
Must be specified if 'height' is omitted."""
    height: "NotRequired[int]"
    """The window contents height in DIP. Assumes current height if omitted.
Must be specified if 'width' is omitted."""





class SetDockTileParameters(TypedDict, total=False):
    badgeLabel: "str"
    image: "str"
    """Png encoded image. (Encoded as a base64 string when passed over JSON)"""





class ExecuteBrowserCommandParameters(TypedDict):
    commandId: "BrowserCommandId"





class AddPrivacySandboxEnrollmentOverrideParameters(TypedDict):
    url: "str"





class AddPrivacySandboxCoordinatorKeyConfigParameters(TypedDict):
    api: "PrivacySandboxAPI"
    coordinatorOrigin: "str"
    keyConfig: "str"
    browserContextId: "NotRequired[BrowserContextID]"
    """BrowserContext to perform the action in. When omitted, default browser
context is used."""


