#!/usr/bin/env python3
"""Render every .excalidraw in the Epic 1 folder to .png (4 at a time)."""

from __future__ import annotations

import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
RENDER = HERE / "render" / "render_excalidraw.py"
PROJECT = Path(r"C:\Users\SahilMore\.claude\skills\excalidraw-diagram\references")


def render(path: Path) -> tuple[str, int, str]:
    cmd = ["uv", "run", "--project", str(PROJECT), "python", str(RENDER),
           str(path), "--scale", "1", "--width", "3200"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return path.name, result.returncode, (result.stderr or "")[-400:]


def main() -> int:
    files = sorted(OUT.glob("*.excalidraw"))
    only = sys.argv[1:]
    if only:
        files = [f for f in files if any(o in f.name for o in only)]
    print(f"{len(files)} file(s)")
    failed = 0
    with ThreadPoolExecutor(max_workers=4) as pool:
        for name, code, err in pool.map(render, files):
            status = "OK" if code == 0 else "FAIL"
            if code:
                failed += 1
            print(f"{status} {name}")
            if err.strip():
                print("   " + err.strip().replace("\n", "\n   "))
    print(f"\n{len(files) - failed} rendered, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
