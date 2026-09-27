#!/usr/bin/env python3
"""
Drop sources the inbox-desktop build doesn't need from generated-sources.json:
Playwright browsers, and Electron zips, headers and cache symlinks for
versions other than the one inbox-desktop pins.

Usage: prune-generated-sources.py <generated-sources.json> <inbox-desktop/package.json>
"""

import json
import re
import sys


def main(sources_path: str, package_json_path: str) -> None:
    with open(package_json_path, encoding="utf-8") as f:
        pkg = json.load(f)
    electron = pkg["devDependencies"]["electron"].lstrip("^~")

    with open(sources_path, encoding="utf-8") as f:
        sources = json.load(f)

    electron_re = re.compile(
        r"electron/releases/download/v([\d.]+)/"
        r"|electronjs\.org/headers/v([\d.]+)/"
        r"|node-gyp/([\d.]+)"
        r"|electron-v([\d.]+)-linux"
        r"|SHASUMS256\.txt-([\d.]+)"
    )

    def keep(entry: dict) -> bool:
        url = entry.get("url", "")
        dest = entry.get("dest", "")
        if "cdn.playwright.dev" in url or "ms-playwright" in dest:
            return False
        for m in electron_re.finditer(json.dumps(entry)):
            if next(v for v in m.groups() if v) != electron:
                return False
        return True

    pruned = [e for e in sources if keep(e)]

    with open(sources_path, "w", encoding="utf-8") as f:
        json.dump(pruned, f, indent=4)
        f.write("\n")

    print(f"Electron {electron}: kept {len(pruned)} of {len(sources)} sources.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(f"Usage: {sys.argv[0]} <generated-sources.json> <package.json>")
    main(sys.argv[1], sys.argv[2])
