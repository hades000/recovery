import re, shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import WS, F17, F18

def copy_tree(src, dst):
    shutil.copytree(src, dst, dirs_exist_ok=True)

def copy_latest_md(src, dst):
    """Copy *.md, keeping only the highest -vN of each family."""
    dst.mkdir(parents=True, exist_ok=True)
    best = {}
    for p in Path(src).glob("*.md"):
        m = re.match(r"^(.*?)-v(\d+)\.md$", p.name)
        fam, v = (m.group(1), int(m.group(2))) if m else (p.stem, 0)
        if fam not in best or v > best[fam][0]:
            best[fam] = (v, p)
    for _, p in best.values():
        shutil.copy2(p, dst / p.name)

def main():
    copy_tree(F18 / "aisdlc" / ".github", WS / ".github")
    copy_tree(F17 / "requirement" / "legacy", WS / "requirement" / "legacy")
    copy_latest_md(F17 / "docs" / "brds", WS / "docs" / "brds")
    copy_latest_md(F17 / "docs" / "prds", WS / "docs" / "prds")
    (WS / ".claude-commands").mkdir(parents=True, exist_ok=True)
    for n in ["brd-builder.md", "prd-builder.md", "backlog-builder.md"]:
        shutil.copy2(F18 / ".claude" / "commands" / n, WS / ".claude-commands" / n)
    for d in ["docs/increments", "output", "requirement/legacy/_converted"]:
        (WS / d).mkdir(parents=True, exist_ok=True)
    tm = WS / "requirement" / "Traceability_Matrix.md"
    if not tm.exists():
        tm.write_text("# Traceability Matrix (realignment workspace)\n\n| Source | ID | Target |\n|---|---|---|\n", encoding="utf-8")
    print("WORKSPACE OK", WS)

if __name__ == "__main__":
    main()
