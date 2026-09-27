#!/usr/bin/env python3
"""
Add a <release> entry to the metainfo if it isn't there yet.

Usage: add-metainfo-release.py <metainfo.xml> <version> <YYYY-MM-DD>
"""

import sys


def main(path: str, version: str, date: str) -> None:
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if f'version="{version}"' in text:
        return

    entry = (f'        <release version="{version}" date="{date}">\n'
             f'            <description/>\n'
             f'        </release>\n')
    updated = text.replace("    <releases>\n", "    <releases>\n" + entry, 1)
    if updated == text:
        sys.exit("could not find <releases> in metainfo")

    with open(path, "w", encoding="utf-8") as f:
        f.write(updated)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(f"Usage: {sys.argv[0]} <metainfo.xml> <version> <date>")
    main(sys.argv[1], sys.argv[2], sys.argv[3])
