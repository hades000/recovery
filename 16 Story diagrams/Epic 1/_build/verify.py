#!/usr/bin/env python3
"""Final checks for the Epic 1 story maps.

1. File counts (72 .excalidraw + 72 .png).
2. JSON sanity: unique ids, every container and binding resolves.
3. Spot-check five maps against sections 11-13 of their story file.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
ROOT = HERE.parents[2]
STORIES = ROOT / "04 User stories" / "Recovery Workbench User Stories Epic 1 Story Files v6"
SPECS = HERE / "specs"

problems: list[str] = []


def check_files() -> None:
    drawings = sorted(OUT.glob("*.excalidraw"))
    pngs = sorted(OUT.glob("*.png"))
    print(f"excalidraw: {len(drawings)}   png: {len(pngs)}")
    if len(drawings) != 72:
        problems.append(f"expected 72 .excalidraw, found {len(drawings)}")
    if len(pngs) != 72:
        problems.append(f"expected 72 .png, found {len(pngs)}")
    for path in drawings:
        if not path.with_suffix(".png").exists():
            problems.append(f"no png for {path.name}")


def check_json() -> None:
    for path in sorted(OUT.glob("*.excalidraw")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("type") != "excalidraw":
            problems.append(f"{path.name}: type is not excalidraw")
        els = data["elements"]
        ids = [e["id"] for e in els]
        if len(ids) != len(set(ids)):
            problems.append(f"{path.name}: duplicate ids")
        known = set(ids)
        for el in els:
            for ref in el.get("boundElements") or []:
                if ref["id"] not in known:
                    problems.append(f"{path.name}: {el['id']} -> {ref['id']}")
            for field in ("startBinding", "endBinding"):
                b = el.get(field)
                if b and b["elementId"] not in known:
                    problems.append(f"{path.name}: {el['id']} {field} broken")
            if el["type"] == "text" and el["containerId"]:
                if el["containerId"] not in known:
                    problems.append(f"{path.name}: {el['id']} container gone")


def section(text: str, number: int) -> str:
    start = text.find(f"## {number}.")
    end = text.find(f"## {number + 1}.")
    if start < 0:
        return ""
    return text[start:end if end > start else len(text)]


def clean(name: str) -> str:
    name = re.sub(r"\s*\(.*?\)\s*$", "", name)
    name = name.split(" ")[0]
    return name.strip(".,;:")


def check_spot() -> None:
    for key in ("RWB-E1-002", "RWB-E1-018", "RWB-E1-024", "RWB-E1-052",
                "RWB-TE-006"):
        spec = json.loads((SPECS / f"{key}.json").read_text(encoding="utf-8"))
        story = STORIES / f"{spec['file_stem']} v1.md"
        if not story.exists():
            problems.append(f"{key}: story file not found: {story.name}")
            continue
        body = "\n".join(section(story.read_text(encoding="utf-8"), n)
                         for n in (11, 12, 13))
        names = []
        for item in spec["ace"]:
            names.append(("view", item["view"]))
        for item in spec["writes"]:
            names.append(("table", item["t"]))
        missing = []
        for kind, name in names:
            probe = clean(name)
            if not probe or "*" in probe or probe.lower() in (
                    "recovery", "task", "blobs", "job"):
                continue
            parts = probe.split(".") if "." in probe else [probe]
            if not all(part in body for part in parts):
                missing.append(f"{kind} {probe}")
        if missing:
            problems.append(f"{key}: not in sections 11-13: {', '.join(missing)}")
        else:
            print(f"{key}: every view and table found in sections 11-13")


def main() -> int:
    check_files()
    check_json()
    check_spot()
    if problems:
        print("\nPROBLEMS")
        for p in problems:
            print("  " + p)
        return 1
    print("\nall checks pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
