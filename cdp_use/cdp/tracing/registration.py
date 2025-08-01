# This file is auto-generated by the CDP protocol generator.
# Do not edit this file manually as your changes will be overwritten.
# Generated from Chrome DevTools Protocol specifications.

"""CDP Tracing Domain Event Registration"""

from typing import Callable, Optional

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..registry import EventRegistry
    from .events import BufferUsageEvent, DataCollectedEvent, TracingCompleteEvent

class TracingRegistration:
    """Event registration interface for Tracing domain."""

    def __init__(self, registry: 'EventRegistry'):
        self._registry = registry
        self._domain = "Tracing"

    def bufferUsage(
        self,
        callback: Callable[['BufferUsageEvent', Optional[str]], None],
    ) -> None:
        """
        Register a callback for bufferUsage events.
        
        Args:
            callback: Function to call when event occurs.
                     Receives (event_data, session_id) as parameters.
        """
        self._registry.register("Tracing.bufferUsage", callback)

    def dataCollected(
        self,
        callback: Callable[['DataCollectedEvent', Optional[str]], None],
    ) -> None:
        """
        Register a callback for dataCollected events.
        
        Contains a bucket of collected trace events. When tracing is stopped collected events will be
sent as a sequence of dataCollected events followed by tracingComplete event.
        
        Args:
            callback: Function to call when event occurs.
                     Receives (event_data, session_id) as parameters.
        """
        self._registry.register("Tracing.dataCollected", callback)

    def tracingComplete(
        self,
        callback: Callable[['TracingCompleteEvent', Optional[str]], None],
    ) -> None:
        """
        Register a callback for tracingComplete events.
        
        Signals that tracing is stopped and there is no trace buffers pending flush, all data were
delivered via dataCollected events.
        
        Args:
            callback: Function to call when event occurs.
                     Receives (event_data, session_id) as parameters.
        """
        self._registry.register("Tracing.tracingComplete", callback)

