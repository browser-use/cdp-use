"""
CDP Protocol Version Configuration

Pin the protocol to a specific Chromium release tag so that the generated
types exactly match the browser version being targeted.

The protocol JSON files are fetched directly from the Chromium and V8
source repositories at the given tag.  Googlesource returns base64-encoded
content when `?format=TEXT` is appended — the downloader handles decoding.

To update:
  1. Find the Chromium tag at https://chromium.googlesource.com/chromium/src/+refs
  2. Look up the V8 sub-module commit for that tag:
       https://chromium.googlesource.com/chromium/src/+/<tag>/v8?format=TEXT
     (the response is the commit hash)
  3. Update CHROMIUM_TAG and V8_COMMIT below.
  4. Run `uv run python -m cdp_use.generator` to regenerate.
"""

# ── Chromium TAG  ──
CHROMIUM_TAG = "144.0.7559.109"
V8_COMMIT = "d75d178c137447df1a3e8830eae86b0bd72b9ac6"

# Browser protocol (from Blink / Chromium source)
BROWSER_PROTOCOL_FILE = (
    f"https://chromium.googlesource.com/chromium/src/+/refs/tags/{CHROMIUM_TAG}"
    f"/third_party/blink/public/devtools_protocol/browser_protocol-1.3.json?format=TEXT"
)

# JS protocol (from V8 source, pinned to the commit embedded in this Chromium tag)
JS_PROTOCOL_FILE = (
    f"https://chromium.googlesource.com/v8/v8/+/{V8_COMMIT}"
    f"/include/js_protocol-1.3.json?format=TEXT"
)

# Legacy alias used by generate.py log messages
CDP_VERSION = f"chromium-{CHROMIUM_TAG}"
