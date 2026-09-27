#!/usr/bin/env python3
"""
Prepare the WebClients checkout for an offline inbox-desktop build:
drop private registries and plugins from .yarnrc.yml, and trim the
workspace list to applications/inbox-desktop (the other apps pull in
packages from Proton's private registries).

Run from the root of the WebClients checkout.
"""

import json
import re
from pathlib import Path

YARNRC_PATTERNS = [
    r"^plugins:\n([ \t]+.*\n)*",
    r"^npmPublishRegistry:.*\n",
    r"^npmScopes:\n([ \t]+.*\n)*",
    r"^npmPreapprovedPackages:\n([ \t]+.*\n)*",
    r"^npmMinimalAgeGate:.*\n",
]


def trim_yarnrc(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for pattern in YARNRC_PATTERNS:
        text = re.sub(pattern, "", text, flags=re.MULTILINE)
    path.write_text(text, encoding="utf-8")


def trim_workspaces(path: Path) -> None:
    pkg = json.loads(path.read_text(encoding="utf-8"))
    pkg["workspaces"] = [
        w for w in pkg["workspaces"]
        if not w.startswith("applications/") and not w.startswith("tests")
    ] + ["applications/inbox-desktop"]
    path.write_text(json.dumps(pkg, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    trim_yarnrc(Path(".yarnrc.yml"))
    trim_workspaces(Path("package.json"))
