# This file is auto-generated by the CDP protocol generator.
# Do not edit this file manually as your changes will be overwritten.
# Generated from Chrome DevTools Protocol specifications.

"""CDP Accessibility Domain Events"""

from typing import List
from typing_extensions import TypedDict

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .types import AXNode

"""The loadComplete event mirrors the load complete event sent by the browser to assistive
technology when the web page has finished loading."""
class LoadCompleteEvent(TypedDict):
    root: "AXNode"
    """New document root node."""



"""The nodesUpdated event is sent every time a previously requested node has changed the in tree."""
class NodesUpdatedEvent(TypedDict):
    nodes: "List[AXNode]"
    """Updated node data."""
