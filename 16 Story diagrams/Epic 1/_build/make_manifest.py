#!/usr/bin/env python3
"""Write the review manifest: 71 story PNGs in 8 groups, for the eye check."""

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent
NAMES = [
    p.name for p in sorted(OUT.glob("*.png")) if not p.name.startswith("00 ")
]
GROUP = 9
lines = []
for i, name in enumerate(NAMES):
    lines.append(f"{i // GROUP + 1}\t{i % GROUP + 1:02d}\t{name}")
(Path(__file__).resolve().parent / "inspect_manifest.txt").write_text(
    "\n".join(lines) + "\n", encoding="utf-8")
print(len(NAMES), "files, size", GROUP)
for g in range(1, 9):
    n = len([l for l in lines if l.startswith(f"{g}\t")])
    print("group", g, n)
