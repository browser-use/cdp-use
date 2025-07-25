# This file is auto-generated by the CDP protocol generator.
# Do not edit this file manually as your changes will be overwritten.
# Generated from Chrome DevTools Protocol specifications.

"""CDP DOM Domain Event Registration"""

from typing import Callable, Optional

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..registry import EventRegistry
    from .events import (
    AttributeModifiedEvent,
    AttributeRemovedEvent,
    CharacterDataModifiedEvent,
    ChildNodeCountUpdatedEvent,
    ChildNodeInsertedEvent,
    ChildNodeRemovedEvent,
    DistributedNodesUpdatedEvent,
    DocumentUpdatedEvent,
    InlineStyleInvalidatedEvent,
    PseudoElementAddedEvent,
    PseudoElementRemovedEvent,
    ScrollableFlagUpdatedEvent,
    SetChildNodesEvent,
    ShadowRootPoppedEvent,
    ShadowRootPushedEvent,
    TopLayerElementsUpdatedEvent
)

class DOMRegistration:
    """Event registration interface for DOM domain."""

    def __init__(self, registry: 'EventRegistry'):
        self._registry = registry
        self._domain = "DOM"

    def attributeModified(
        self,
        callback: Callable[['AttributeModifiedEvent', Optional[str]], None],
    ) -> None:
        """
        Register a callback for attributeModified events.
        
        Fired when `Element`'s attribute is modified.
        
        Args:
            callback: Function to call when event occurs.
                     Receives (event_data, session_id) as parameters.
        """
        self._registry.register("DOM.attributeModified", callback)

    def attributeRemoved(
        self,
        callback: Callable[['AttributeRemovedEvent', Optional[str]], None],
    ) -> None:
        """
        Register a callback for attributeRemoved events.
        
        Fired when `Element`'s attribute is removed.
        
        Args:
            callback: Function to call when event occurs.
                     Receives (event_data, session_id) as parameters.
        """
        self._registry.register("DOM.attributeRemoved", callback)

    def characterDataModified(
        self,
        callback: Callable[['CharacterDataModifiedEvent', Optional[str]], None],
    ) -> None:
        """
        Register a callback for characterDataModified events.
        
        Mirrors `DOMCharacterDataModified` event.
        
        Args:
            callback: Function to call when event occurs.
                     Receives (event_data, session_id) as parameters.
        """
        self._registry.register("DOM.characterDataModified", callback)

    def childNodeCountUpdated(
        self,
        callback: Callable[['ChildNodeCountUpdatedEvent', Optional[str]], None],
    ) -> None:
        """
        Register a callback for childNodeCountUpdated events.
        
        Fired when `Container`'s child node count has changed.
        
        Args:
            callback: Function to call when event occurs.
                     Receives (event_data, session_id) as parameters.
        """
        self._registry.register("DOM.childNodeCountUpdated", callback)

    def childNodeInserted(
        self,
        callback: Callable[['ChildNodeInsertedEvent', Optional[str]], None],
    ) -> None:
        """
        Register a callback for childNodeInserted events.
        
        Mirrors `DOMNodeInserted` event.
        
        Args:
            callback: Function to call when event occurs.
                     Receives (event_data, session_id) as parameters.
        """
        self._registry.register("DOM.childNodeInserted", callback)

    def childNodeRemoved(
        self,
        callback: Callable[['ChildNodeRemovedEvent', Optional[str]], None],
    ) -> None:
        """
        Register a callback for childNodeRemoved events.
        
        Mirrors `DOMNodeRemoved` event.
        
        Args:
            callback: Function to call when event occurs.
                     Receives (event_data, session_id) as parameters.
        """
        self._registry.register("DOM.childNodeRemoved", callback)

    def distributedNodesUpdated(
        self,
        callback: Callable[['DistributedNodesUpdatedEvent', Optional[str]], None],
    ) -> None:
        """
        Register a callback for distributedNodesUpdated events.
        
        Called when distribution is changed.
        
        Args:
            callback: Function to call when event occurs.
                     Receives (event_data, session_id) as parameters.
        """
        self._registry.register("DOM.distributedNodesUpdated", callback)

    def documentUpdated(
        self,
        callback: Callable[['DocumentUpdatedEvent', Optional[str]], None],
    ) -> None:
        """
        Register a callback for documentUpdated events.
        
        Fired when `Document` has been totally updated. Node ids are no longer valid.
        
        Args:
            callback: Function to call when event occurs.
                     Receives (event_data, session_id) as parameters.
        """
        self._registry.register("DOM.documentUpdated", callback)

    def inlineStyleInvalidated(
        self,
        callback: Callable[['InlineStyleInvalidatedEvent', Optional[str]], None],
    ) -> None:
        """
        Register a callback for inlineStyleInvalidated events.
        
        Fired when `Element`'s inline style is modified via a CSS property modification.
        
        Args:
            callback: Function to call when event occurs.
                     Receives (event_data, session_id) as parameters.
        """
        self._registry.register("DOM.inlineStyleInvalidated", callback)

    def pseudoElementAdded(
        self,
        callback: Callable[['PseudoElementAddedEvent', Optional[str]], None],
    ) -> None:
        """
        Register a callback for pseudoElementAdded events.
        
        Called when a pseudo element is added to an element.
        
        Args:
            callback: Function to call when event occurs.
                     Receives (event_data, session_id) as parameters.
        """
        self._registry.register("DOM.pseudoElementAdded", callback)

    def topLayerElementsUpdated(
        self,
        callback: Callable[['TopLayerElementsUpdatedEvent', Optional[str]], None],
    ) -> None:
        """
        Register a callback for topLayerElementsUpdated events.
        
        Called when top layer elements are changed.
        
        Args:
            callback: Function to call when event occurs.
                     Receives (event_data, session_id) as parameters.
        """
        self._registry.register("DOM.topLayerElementsUpdated", callback)

    def scrollableFlagUpdated(
        self,
        callback: Callable[['ScrollableFlagUpdatedEvent', Optional[str]], None],
    ) -> None:
        """
        Register a callback for scrollableFlagUpdated events.
        
        Fired when a node's scrollability state changes.
        
        Args:
            callback: Function to call when event occurs.
                     Receives (event_data, session_id) as parameters.
        """
        self._registry.register("DOM.scrollableFlagUpdated", callback)

    def pseudoElementRemoved(
        self,
        callback: Callable[['PseudoElementRemovedEvent', Optional[str]], None],
    ) -> None:
        """
        Register a callback for pseudoElementRemoved events.
        
        Called when a pseudo element is removed from an element.
        
        Args:
            callback: Function to call when event occurs.
                     Receives (event_data, session_id) as parameters.
        """
        self._registry.register("DOM.pseudoElementRemoved", callback)

    def setChildNodes(
        self,
        callback: Callable[['SetChildNodesEvent', Optional[str]], None],
    ) -> None:
        """
        Register a callback for setChildNodes events.
        
        Fired when backend wants to provide client with the missing DOM structure. This happens upon
most of the calls requesting node ids.
        
        Args:
            callback: Function to call when event occurs.
                     Receives (event_data, session_id) as parameters.
        """
        self._registry.register("DOM.setChildNodes", callback)

    def shadowRootPopped(
        self,
        callback: Callable[['ShadowRootPoppedEvent', Optional[str]], None],
    ) -> None:
        """
        Register a callback for shadowRootPopped events.
        
        Called when shadow root is popped from the element.
        
        Args:
            callback: Function to call when event occurs.
                     Receives (event_data, session_id) as parameters.
        """
        self._registry.register("DOM.shadowRootPopped", callback)

    def shadowRootPushed(
        self,
        callback: Callable[['ShadowRootPushedEvent', Optional[str]], None],
    ) -> None:
        """
        Register a callback for shadowRootPushed events.
        
        Called when shadow root is pushed into the element.
        
        Args:
            callback: Function to call when event occurs.
                     Receives (event_data, session_id) as parameters.
        """
        self._registry.register("DOM.shadowRootPushed", callback)

