# This file is auto-generated by the CDP protocol generator.
# Do not edit this file manually as your changes will be overwritten.
# Generated from Chrome DevTools Protocol specifications.

"""CDP Event Registration Library"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .registry import EventRegistry

class CDPRegistrationLibrary:
    """Main CDP registration library with domain-specific registration interfaces."""

    def __init__(self, registry: 'EventRegistry'):
        self._registry = registry

        # Console domain registration
        from .console.registration import ConsoleRegistration
        self.Console = ConsoleRegistration(registry)

        # Debugger domain registration
        from .debugger.registration import DebuggerRegistration
        self.Debugger = DebuggerRegistration(registry)

        # HeapProfiler domain registration
        from .heapprofiler.registration import HeapProfilerRegistration
        self.HeapProfiler = HeapProfilerRegistration(registry)

        # Profiler domain registration
        from .profiler.registration import ProfilerRegistration
        self.Profiler = ProfilerRegistration(registry)

        # Runtime domain registration
        from .runtime.registration import RuntimeRegistration
        self.Runtime = RuntimeRegistration(registry)

        # Accessibility domain registration
        from .accessibility.registration import AccessibilityRegistration
        self.Accessibility = AccessibilityRegistration(registry)

        # Animation domain registration
        from .animation.registration import AnimationRegistration
        self.Animation = AnimationRegistration(registry)

        # Audits domain registration
        from .audits.registration import AuditsRegistration
        self.Audits = AuditsRegistration(registry)

        # Autofill domain registration
        from .autofill.registration import AutofillRegistration
        self.Autofill = AutofillRegistration(registry)

        # BackgroundService domain registration
        from .backgroundservice.registration import BackgroundServiceRegistration
        self.BackgroundService = BackgroundServiceRegistration(registry)

        # Browser domain registration
        from .browser.registration import BrowserRegistration
        self.Browser = BrowserRegistration(registry)

        # CSS domain registration
        from .css.registration import CSSRegistration
        self.CSS = CSSRegistration(registry)

        # Cast domain registration
        from .cast.registration import CastRegistration
        self.Cast = CastRegistration(registry)

        # DOM domain registration
        from .dom.registration import DOMRegistration
        self.DOM = DOMRegistration(registry)

        # DOMStorage domain registration
        from .domstorage.registration import DOMStorageRegistration
        self.DOMStorage = DOMStorageRegistration(registry)

        # Emulation domain registration
        from .emulation.registration import EmulationRegistration
        self.Emulation = EmulationRegistration(registry)

        # Input domain registration
        from .input.registration import InputRegistration
        self.Input = InputRegistration(registry)

        # Inspector domain registration
        from .inspector.registration import InspectorRegistration
        self.Inspector = InspectorRegistration(registry)

        # LayerTree domain registration
        from .layertree.registration import LayerTreeRegistration
        self.LayerTree = LayerTreeRegistration(registry)

        # Log domain registration
        from .log.registration import LogRegistration
        self.Log = LogRegistration(registry)

        # Network domain registration
        from .network.registration import NetworkRegistration
        self.Network = NetworkRegistration(registry)

        # Overlay domain registration
        from .overlay.registration import OverlayRegistration
        self.Overlay = OverlayRegistration(registry)

        # Page domain registration
        from .page.registration import PageRegistration
        self.Page = PageRegistration(registry)

        # Performance domain registration
        from .performance.registration import PerformanceRegistration
        self.Performance = PerformanceRegistration(registry)

        # PerformanceTimeline domain registration
        from .performancetimeline.registration import PerformanceTimelineRegistration
        self.PerformanceTimeline = PerformanceTimelineRegistration(registry)

        # Security domain registration
        from .security.registration import SecurityRegistration
        self.Security = SecurityRegistration(registry)

        # ServiceWorker domain registration
        from .serviceworker.registration import ServiceWorkerRegistration
        self.ServiceWorker = ServiceWorkerRegistration(registry)

        # Storage domain registration
        from .storage.registration import StorageRegistration
        self.Storage = StorageRegistration(registry)

        # Target domain registration
        from .target.registration import TargetRegistration
        self.Target = TargetRegistration(registry)

        # Tethering domain registration
        from .tethering.registration import TetheringRegistration
        self.Tethering = TetheringRegistration(registry)

        # Tracing domain registration
        from .tracing.registration import TracingRegistration
        self.Tracing = TracingRegistration(registry)

        # Fetch domain registration
        from .fetch.registration import FetchRegistration
        self.Fetch = FetchRegistration(registry)

        # WebAudio domain registration
        from .webaudio.registration import WebAudioRegistration
        self.WebAudio = WebAudioRegistration(registry)

        # WebAuthn domain registration
        from .webauthn.registration import WebAuthnRegistration
        self.WebAuthn = WebAuthnRegistration(registry)

        # Media domain registration
        from .media.registration import MediaRegistration
        self.Media = MediaRegistration(registry)

        # DeviceAccess domain registration
        from .deviceaccess.registration import DeviceAccessRegistration
        self.DeviceAccess = DeviceAccessRegistration(registry)

        # Preload domain registration
        from .preload.registration import PreloadRegistration
        self.Preload = PreloadRegistration(registry)

        # FedCm domain registration
        from .fedcm.registration import FedCmRegistration
        self.FedCm = FedCmRegistration(registry)

        # BluetoothEmulation domain registration
        from .bluetoothemulation.registration import BluetoothEmulationRegistration
        self.BluetoothEmulation = BluetoothEmulationRegistration(registry)

