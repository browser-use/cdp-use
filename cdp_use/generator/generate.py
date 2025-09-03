#!/usr/bin/env python3
"""
CDP Protocol Downloader and Generator

Downloads the latest Chrome DevTools Protocol specifications and generates
type-safe Python bindings.
"""

import tempfile
from pathlib import Path
from urllib.request import urlretrieve

from .constants import BROWSER_PROTOCOL_FILE, CDP_VERSION, JS_PROTOCOL_FILE
from .generator import CDPGenerator


def download_protocol_files() -> tuple[str, str]:
    """Download the protocol files from the official repository."""
    temp_dir = Path(tempfile.mkdtemp())

    print(
        f"Downloading Chrome DevTools Protocol specifications (version: {CDP_VERSION})..."
    )

    # Download JavaScript protocol
    js_protocol_path = temp_dir / "js_protocol.json"
    print(f"  Downloading JS protocol from {JS_PROTOCOL_FILE}")
    urlretrieve(JS_PROTOCOL_FILE, js_protocol_path)

    # Download Browser protocol
    browser_protocol_path = temp_dir / "browser_protocol.json"
    print(f"  Downloading Browser protocol from {BROWSER_PROTOCOL_FILE}")
    urlretrieve(BROWSER_PROTOCOL_FILE, browser_protocol_path)

    print("✅ Protocol files downloaded successfully")

    return str(js_protocol_path), str(browser_protocol_path)


def main():
    """Main entry point for the generator."""
    try:
        # Download protocol files
        js_file, browser_file = download_protocol_files()

        # Discover any custom protocol JSON files placed under cdp_use/custom_protocols/
        project_root = Path(__file__).resolve().parents[2]
        custom_dir = project_root / "cdp_use" / "custom_protocols"
        custom_protocol_files: list[str] = []
        if custom_dir.exists() and custom_dir.is_dir():
            for path in sorted(custom_dir.glob("*.json")):
                print(f"  Including custom protocol: {path}")
                custom_protocol_files.append(str(path))

        # Create generator and run it, appending any custom protocol files
        generator = CDPGenerator()
        generator.generate_all(
            protocol_files=[js_file, browser_file, *custom_protocol_files]
        )

        print("🎉 CDP type-safe client generation completed!")
        print("")
        print("📖 Usage:")
        print("   from cdp_use.client import CDPClient")
        print("   # cdp.send.Target.getTargets() - fully type safe!")

    except Exception as e:
        print(f"❌ Error during generation: {e}")
        raise


if __name__ == "__main__":
    main()
