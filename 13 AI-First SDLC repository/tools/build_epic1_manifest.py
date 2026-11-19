#!/usr/bin/env python3
"""Build the Epic 1 story manifest and module groups for the batch spec run."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT / "13 AI-First SDLC repository"
BUILD = REPO / "requirement" / "legacy" / "11-delivery-and-operations" / \
    "recovery-workbench-build-sequence-epic-1-and-epic-2-v4-xlsx.md"
STORY_DIR = REPO / "requirement" / "legacy" / "04-user-stories" / \
    "recovery-workbench-user-stories-epic-1-story-files-v5_extracted"
OUT_MD = REPO / "output" / "EPIC1-STORY-MANIFEST.md"
OUT_JSON = REPO / "output" / "EPIC1-STORY-MANIFEST.json"

GROUPS = {
    "P1a": ["RWB-E1-001", "RWB-E1-003", "RWB-E1-005", "RWB-E1-064", "RWB-E1-065",
            "RWB-TE-004", "RWB-E1-010", "RWB-E1-017", "RWB-E1-014", "RWB-E1-012"],
    "P1b": ["RWB-E1-016", "RWB-E1-066", "RWB-E1-002", "RWB-E1-067", "RWB-E1-068",
            "RWB-E1-006", "RWB-E1-011", "RWB-E1-015", "RWB-E1-004", "RWB-E1-009"],
    "P2": ["RWB-TE-001", "RWB-TE-002", "RWB-TE-003", "RWB-TE-011", "RWB-E1-007",
           "RWB-E1-051", "RWB-E1-047", "RWB-E1-056", "RWB-TE-006"],
    "P3a": ["RWB-E1-044", "RWB-E1-042", "RWB-TE-005", "RWB-E1-043", "RWB-E1-029",
            "RWB-TE-007", "RWB-E1-019", "RWB-E1-045", "RWB-E1-018"],
    "P3b": ["RWB-E1-020", "RWB-E1-023", "RWB-E1-028", "RWB-E1-031", "RWB-E1-021",
            "RWB-E1-030", "RWB-E1-035", "RWB-E1-048"],
    "P4": ["RWB-E1-038", "RWB-E1-022", "RWB-E1-037", "RWB-E1-039"],
    "P5a": ["RWB-TE-012", "RWB-E1-025", "RWB-E1-024", "RWB-E1-049", "RWB-E1-041",
            "RWB-E1-050", "RWB-E1-026"],
    "P5b": ["RWB-E1-053", "RWB-E1-057", "RWB-E1-032", "RWB-E1-033", "RWB-E1-040",
            "RWB-E1-054"],
    "P6": ["RWB-E1-046", "RWB-E1-034", "RWB-E1-052", "RWB-E1-055"],
    "P7": ["RWB-E1-008", "RWB-E1-027", "RWB-TE-008"],
    "P9": ["RWB-E1-013"],
    "P10": ["RWB-E1-058", "RWB-TE-013", "RWB-E1-062", "RWB-E1-059", "RWB-E1-060",
            "RWB-E1-061", "RWB-E1-063"],
}


def parse_build() -> dict[str, dict]:
    stories: dict[str, dict] = {}
    for line in BUILD.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 11 or not re.fullmatch(r"\d+", cells[0]):
            continue
        if cells[9] != "E1":
            continue
        stories[cells[1]] = {
            "order": int(cells[0]),
            "key": cells[1],
            "title": cells[2],
            "module": cells[3],
            "type": cells[4],
            "priority": cells[5],
            "depends_on": cells[6],
            "window": cells[7],
            "critical_path": cells[10],
        }
    return stories


def story_file(key: str) -> str:
    prefix = key.replace("RWB-", "RWB ").replace("-", " ")
    for p in STORY_DIR.glob("*.md"):
        if p.name.startswith(prefix):
            return p.relative_to(REPO).as_posix()
    return ""


def main() -> None:
    build = parse_build()
    groups = []
    used = set()
    for gid, keys in GROUPS.items():
        items = []
        for key in keys:
            if key not in build:
                items.append({"key": key, "title": "MISSING FROM BUILD SEQUENCE", "module": gid,
                              "type": "", "priority": "", "depends_on": "", "window": "",
                              "critical_path": "", "story_file": "", "output_dir": ""})
                continue
            b = build[key]
            sf = story_file(key)
            b = dict(b)
            order = b.pop("order")
            b["story_file"] = sf
            b["output_dir"] = f"output/INC-{order:03d}-epic-1-{key}/specify"
            b["group"] = gid
            items.append(b)
            used.add(key)
        groups.append({"id": gid, "stories": items})
    missing = sorted(set(build) - used)
    extra = sorted(used - set(build))
    manifest = {"groups": groups, "missing_from_groups": missing, "extra_in_groups": extra,
                "build_count": len(build), "grouped_count": len(used)}
    OUT_JSON.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = ["# Epic 1 story manifest", "",
             f"Build-sequence E1 items: **{len(build)}** · Grouped: **{len(used)}** · "
             f"Missing: **{len(missing)}** · Extra: **{len(extra)}**", "",
             "| Group | Key | Title | Module | Type | Priority | Story file | Output |",
             "|---|---|---|---|---|---|---|---|"]
    for group in groups:
        for s in group["stories"]:
            sf = f"`{s['story_file']}`" if s["story_file"] else "**MISSING**"
            lines.append(f"| {group['id']} | {s['key']} | {s['title']} | {s['module']} | "
                         f"{s['type']} | {s['priority']} | {sf} | `{s['output_dir']}` |")
    if missing:
        lines += ["", "## Not in any group", ""] + [f"- {m}" for m in missing]
    if extra:
        lines += ["", "## Extra keys", ""] + [f"- {m}" for m in extra]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Build E1 items: {len(build)}; grouped: {len(used)}; missing: {len(missing)}; extra: {len(extra)}")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
