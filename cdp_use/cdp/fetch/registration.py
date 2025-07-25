# This file is auto-generated by the CDP protocol generator.
# Do not edit this file manually as your changes will be overwritten.
# Generated from Chrome DevTools Protocol specifications.

"""CDP Fetch Domain Event Registration"""

from typing import Callable, Optional

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..registry import EventRegistry
    from .events import AuthRequiredEvent, RequestPausedEvent

class FetchRegistration:
    """Event registration interface for Fetch domain."""

    def __init__(self, registry: 'EventRegistry'):
        self._registry = registry
        self._domain = "Fetch"

    def requestPaused(
        self,
        callback: Callable[['RequestPausedEvent', Optional[str]], None],
    ) -> None:
        """
        Register a callback for requestPaused events.
        
        Issued when the domain is enabled and the request URL matches the
specified filter. The request is paused until the client responds
with one of continueRequest, failRequest or fulfillRequest.
The stage of the request can be determined by presence of responseErrorReason
and responseStatusCode -- the request is at the response stage if either
of these fields is present and in the request stage otherwise.
Redirect responses and subsequent requests are reported similarly to regular
responses and requests. Redirect responses may be distinguished by the value
of `responseStatusCode` (which is one of 301, 302, 303, 307, 308) along with
presence of the `location` header. Requests resulting from a redirect will
have `redirectedRequestId` field set.
        
        Args:
            callback: Function to call when event occurs.
                     Receives (event_data, session_id) as parameters.
        """
        self._registry.register("Fetch.requestPaused", callback)

    def authRequired(
        self,
        callback: Callable[['AuthRequiredEvent', Optional[str]], None],
    ) -> None:
        """
        Register a callback for authRequired events.
        
        Issued when the domain is enabled with handleAuthRequests set to true.
The request is paused until client responds with continueWithAuth.
        
        Args:
            callback: Function to call when event occurs.
                     Receives (event_data, session_id) as parameters.
        """
        self._registry.register("Fetch.authRequired", callback)

