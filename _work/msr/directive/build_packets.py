"""Build one model-pass packet per story from needs_wording.jsonl (D-RCV-60 directive run)."""
import json, sys, re, pickle
from pathlib import Path
from collections import defaultdict
ROOT, S = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
sys.path.insert(0, str(ROOT / "22 Microservice Realignment/checks"))
import rwbsrc
hdr, rows = pickle.load(open(S / "rul3.pkl", "rb"))
by_r = {r["Ruling ID"]: r for r in rows}
idx = rwbsrc.Sources(ROOT, ROOT / "_work/msr/pipeline/all-stories-2026-11-26/_cache").story_index()
applied = {json.loads(l)["file"]: json.loads(l) for l in open(S / "apply-v4/3-applied/apply_result.jsonl", encoding="utf-8")}
items = defaultdict(list); nostory = []
for l in open(S / "apply-v4/2-fixes/needs_wording.jsonl", encoding="utf-8"):
    x = json.loads(l); r = by_r[x["ruling"]]
    it = {k: r.get(k) for k in ("Ruling ID", "Kind", "Item ID", "Severity", "Check", "Title", "Detail", "Evidence",
                                "Owner role", "Proposed fix", "Notes")}
    it = {k: v for k, v in it.items() if v}
    sts = [s for s in (x["story"] or "").split("; ") if s]
    if not sts:
        nostory.append(it)
    for s in sts:
        items[s].append(it)
def bump(name):
    m = re.search(r" v(\d+)\.md$", name)
    return name[:m.start()] + f" v{int(m.group(1)) + 1}.md"
pk = S / "mp/packets"; pk.mkdir(parents=True, exist_ok=True)
man = []
for s, its in sorted(items.items()):
    p = idx.get(s)
    if not p:
        print("no file for", s); continue
    rel = Path(p).resolve().relative_to(ROOT).as_posix()
    a = applied.get(rel)
    if a and a["status"] == "APPLIED":
        src = S / "apply-v4/3-applied" / Path(rel).parent / a["to"]
    else:
        src = ROOT / rel
    out = S / "mp/out" / Path(rel).parent / bump(Path(src).name)
    d = {"story": s, "project_file": rel, "input_file": str(src), "output_file": str(out),
         "disposition_file": str(S / "mp/disp" / f"{s}.jsonl"), "items": its}
    (pk / f"{s}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    man.append((s, Path(src).stat().st_size, len(its)))
(S / "mp/nostory.json").write_text(json.dumps(nostory, ensure_ascii=False, indent=1), encoding="utf-8")
(S / "mp/manifest.json").write_text(json.dumps(man), encoding="utf-8")
print(len(man), "packets;", len(nostory), "no-story items")
