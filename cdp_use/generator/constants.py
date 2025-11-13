"""
CDP Protocol Version Configuration

Change CDP_VERSION to pin a specific version of the Chrome DevTools Protocol.

Examples:
  - Latest master: "refs/heads/master"
  - Specific commit: "4b0c3f2e8c5d6a7b9e1f2a3c4d5e6f7a8b9c0d1e"
  - Tagged version: "refs/tags/v1.3"  (when available)

To find commits: https://github.com/ChromeDevTools/devtools-protocol/commits/master
"""

CDP_VERSION = "refs/heads/master"  # Change this to pin a specific version

JS_PROTOCOL_FILE = f"https://raw.githubusercontent.com/ChromeDevTools/devtools-protocol/{CDP_VERSION}/json/js_protocol.json"

BROWSER_PROTOCOL_FILE = f"https://raw.githubusercontent.com/ChromeDevTools/devtools-protocol/{CDP_VERSION}/json/browser_protocol.json"
