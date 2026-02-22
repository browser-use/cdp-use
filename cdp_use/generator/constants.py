"""
CDP Protocol Version Configuration

Pin the protocol to a specific Chromium revision so that the generated
types exactly match the browser version being targeted.

The full (unfrozen) protocol JSON files are fetched from the
ChromeDevTools/devtools-protocol GitHub repository, which auto-syncs
from Chromium source. Tags use the format v0.0.<Cr-Commit-Position>.

To update:
  1. Find the Chromium tag at https://chromium.googlesource.com/chromium/src/+refs
  2. Get the commit metadata (format=JSON) to find the Cr-Branched-From
     position: refs/heads/main@{#XXXXXXX}
  3. Find the nearest devtools-protocol tag at:
       https://api.github.com/repos/ChromeDevTools/devtools-protocol/git/matching-refs/tags/v0.0.XXXX
  4. Update CHROMIUM_TAG and DEVTOOLS_PROTOCOL_TAG below.
  5. Run `uv run python -m cdp_use.generator` to regenerate.
"""

# ── Chromium 144.0.7559.109 ──
# Branch point: refs/heads/main@{#1552494}
# Nearest devtools-protocol tag: v0.0.1551306
CHROMIUM_TAG = "144.0.7559.109"
DEVTOOLS_PROTOCOL_TAG = "v0.0.1551306"

# Full protocol JSON files from ChromeDevTools/devtools-protocol
BROWSER_PROTOCOL_FILE = (
    f"https://raw.githubusercontent.com/ChromeDevTools/devtools-protocol"
    f"/{DEVTOOLS_PROTOCOL_TAG}/json/browser_protocol.json"
)

JS_PROTOCOL_FILE = (
    f"https://raw.githubusercontent.com/ChromeDevTools/devtools-protocol"
    f"/{DEVTOOLS_PROTOCOL_TAG}/json/js_protocol.json"
)

# Used by generate.py log messages
CDP_VERSION = f"chromium-{CHROMIUM_TAG} ({DEVTOOLS_PROTOCOL_TAG})"
