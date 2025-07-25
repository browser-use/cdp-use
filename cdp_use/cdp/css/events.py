# This file is auto-generated by the CDP protocol generator.
# Do not edit this file manually as your changes will be overwritten.
# Generated from Chrome DevTools Protocol specifications.

"""CDP CSS Domain Events"""

from typing_extensions import TypedDict

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..dom.types import NodeId
    from .types import CSSStyleSheetHeader
    from .types import FontFace
    from .types import StyleSheetId

"""Fires whenever a web font is updated.  A non-empty font parameter indicates a successfully loaded
web font."""
class FontsUpdatedEvent(TypedDict, total=False):
    font: "FontFace"
    """The web font that has loaded."""



"""Fires whenever a MediaQuery result changes (for example, after a browser window has been
resized.) The current implementation considers only viewport-dependent media features."""
class MediaQueryResultChangedEvent(TypedDict):
    pass



"""Fired whenever an active document stylesheet is added."""
class StyleSheetAddedEvent(TypedDict):
    header: "CSSStyleSheetHeader"
    """Added stylesheet metainfo."""



"""Fired whenever a stylesheet is changed as a result of the client operation."""
class StyleSheetChangedEvent(TypedDict):
    styleSheetId: "StyleSheetId"



"""Fired whenever an active document stylesheet is removed."""
class StyleSheetRemovedEvent(TypedDict):
    styleSheetId: "StyleSheetId"
    """Identifier of the removed stylesheet."""



class ComputedStyleUpdatedEvent(TypedDict):
    nodeId: "NodeId"
    """The node id that has updated computed styles."""
