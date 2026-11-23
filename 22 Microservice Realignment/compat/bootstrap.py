import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, R22, R23, WORK, CHECKS, SUBDIRS, write_json, sha256

TOP_SKIP = {"_work", "22 Microservice Realignment", "23 Document Gaps", ".opencode", ".git"}
ANY_SKIP = {".git", "node_modules", "target", "build", "dist", ".gradle", "rwb-wt", "temp"}

def baseline():
    """sha256 of every file that exists before the run. Check C01 proves none of them changed."""
    out = {}
    for p in ROOT.rglob("*"):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in TOP_SKIP or ANY_SKIP & set(rel.parts) or not p.is_file():
            continue
        try:
            out[rel.as_posix()] = sha256(p)
        except OSError:
            pass
    write_json(WORK / "plan" / "baseline.json", out)
    return len(out)

def main():
    for d in [R22, R23, CHECKS, CHECKS / "reports", R22 / "compat" / "tests"] + [WORK / s for s in SUBDIRS]:
        d.mkdir(parents=True, exist_ok=True)
    if not (WORK / "status.json").exists():
        write_json(WORK / "status.json", {})
    n = baseline() if not (WORK / "plan" / "baseline.json").exists() else "kept"
    print("BOOTSTRAP OK", WORK, "baseline files:", n)

if __name__ == "__main__":
    main()
