"""Split the per-story packets into small chunk files for the Haiku model pass (D-RCV-60 directive run).
Each story gets: out/<story>.md (pre-copied next version), chunks/<story>/cNN.md (<=10 items, compact),
and the worker writes disp/<story>/cNN.jsonl per chunk."""
import json, sys, re, shutil
from pathlib import Path
S, MP = Path(sys.argv[1]), Path(sys.argv[2])
CH = 10
def clip(s, n):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    return s if len(s) <= n else s[:n] + " ..."
def sections(it):
    t = " ".join(str(it.get(k, "")) for k in ("Title", "Detail", "Evidence", "Proposed fix"))
    sec = sorted(set(re.findall(r"§\s?(\d+(?:\.\d+)?)", t)), key=lambda x: [int(p) for p in x.split(".")])
    if not sec:
        sec = {"Missing AC": ["7", "16"], "AC review": ["7"]}.get(it["Kind"], [])
    return ", ".join(sec) or "find it"
batches = []
for p in sorted((S / "mp/packets").glob("*.json")):
    d = json.loads(p.read_text(encoding="utf-8"))
    st = d["story"]
    out = MP / "out" / f"{st}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(d["input_file"], out)
    its = d["items"]
    n = (len(its) + CH - 1) // CH
    cd = MP / "chunks" / st; cd.mkdir(parents=True, exist_ok=True)
    (MP / "disp" / st).mkdir(parents=True, exist_ok=True)
    for c in range(n):
        part = its[c * CH:(c + 1) * CH]
        L = [f"# {st} chunk c{c+1:02d} of {n}", "", f"Story file to edit: `{out.relative_to(MP.parents[3]).as_posix()}`",
             f"Disposition file to write: `{(MP / 'disp' / st / f'c{c+1:02d}.jsonl').relative_to(MP.parents[3]).as_posix()}`", ""]
        for i, it in enumerate(part, 1):
            L += [f"## {i}. {it['Item ID']} ({it['Kind']}; ruling {it['Ruling ID']}; sections: {sections(it)})",
                  f"- Title: {clip(it.get('Title'), 300)}",
                  f"- Detail: {clip(it.get('Detail'), 600)}"]
            if it.get("Evidence"): L.append(f"- Evidence: {clip(it.get('Evidence'), 300)}")
            if it.get("Proposed fix"): L.append(f"- Proposed fix: {clip(it.get('Proposed fix'), 600)}")
            if it.get("Owner role"): L.append(f"- Owner role: {clip(it.get('Owner role'), 80)}")
            L.append("")
        (cd / f"c{c+1:02d}.md").write_text("\n".join(L), encoding="utf-8")
    meta = {"story": st, "project_file": d["project_file"], "input_file": d["input_file"],
            "output_name": Path(d["output_file"]).name, "out": str(out), "chunks": n, "items": len(its)}
    (cd / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    batches.append((st, n))
(MP / "stories.json").write_text(json.dumps(batches), encoding="utf-8")
print(len(batches), "stories;", sum(n for _, n in batches), "chunks")
