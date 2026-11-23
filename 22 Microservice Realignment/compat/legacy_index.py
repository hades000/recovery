"""Parse the 7 legacy story masters (+ E1/E2 story files) into _work/msr/plan/legacy_index.json."""
import hashlib, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import STORIES, WORK, LEGACY_RE, sha256, write_json, append_jsonl

MASTERS = [  # file, group, expected count
    ("Recovery Workbench User Stories Epic 1 v9.md", "E1", 72),
    ("Recovery Workbench User Stories Epic 2 v7.md", "E2", 41),
    ("Recovery Workbench User Stories Epics 3 to 8 v3.md", "E3-8", 181),
    ("Recovery Workbench Technical Enabler Stories v7.md", "TE", 12),
    ("Recovery Workbench Administration Stories v3.md", "AD", 22),
    ("Recovery Workbench Data Migration Stories v3.md", "DM", 14),
    ("Recovery Workbench ACE Team Stories v1.md", "ACE", 1),
]
STORY_DIRS = {"E1": "Recovery Workbench User Stories Epic 1 Story Files v7", "E2": "Recovery Workbench User Stories Epic 2 Story Files v5"}
HEAD = re.compile(r"^#{1,2} (RWB-(?:E[1-8]|TE|AD|DM|ACE)-\d{3})\b[ \t]*(.*)$", re.M)
META = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(.*?)\s*\|\s*$", re.M)
SEC_NUM = re.compile(r"^### (\d+)\. (.+)$", re.M)
SEC_BOLD = re.compile(r"^\*\*([A-Z][^*\n]{1,60}?)\.?\*\*", re.M)
BE = {"E1": "EP01", "TE": "EP01-TE", "ACE": "EP01", "E2": "EP02", "E3": "EP03", "E4": "EP04", "E5": "EP05",
      "E6": "EP06", "E7": "EP07", "E8": "EP08", "AD": "EP08", "DM": "EP08"}
NF = {  # Non feature tasks (no master; titles from the realignment plan, gaps raised in split_plan)
    "NF-01": "Repository and pipeline baseline", "NF-02": "Shared library baseline", "NF-03": "Environment baseline",
    "NF-04": "Secrets and configuration baseline", "NF-05": "Quality gates baseline",
    "NF-06": "Create the 19 rwb_* schemas and logins", "NF-07": "Airflow edge integration", "NF-08": "Temporal platform baseline"}

def _meta(block):
    out = {}
    for k, v in META.findall(block.split("\n### ", 1)[0].split("**Story", 1)[0]):
        if k not in ("Item", "---") and not set(k) <= set("-: "):
            out.setdefault(k, v)
    return out

def _sections(block):
    hits = [(m.start(), m.group(2).strip()) for m in SEC_NUM.finditer(block)]
    if not hits:
        hits = [(m.start(), m.group(1).strip()) for m in SEC_BOLD.finditer(block)]
    secs = {}
    for i, (pos, name) in enumerate(hits):
        end = hits[i + 1][0] if i + 1 < len(hits) else len(block)
        secs[name] = block[pos:end]
    return secs

def _uniq(xs):
    seen = []
    for x in xs:
        if x not in seen:
            seen.append(x)
    return seen

def parse_master(path, group):
    text = Path(path).read_text(encoding="utf-8")
    heads = list(HEAD.finditer(text)); rows = []
    for i, m in enumerate(heads):
        block = text[m.start(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        meta = _meta(block); key = m.group(1)
        epic_row = meta.get("Epic", "")
        rel = re.search(r"release\s+(.+)$", epic_row)
        mod = re.match(r"\s*(P10|P[1-9]|S[1-9])\b", meta.get("Module", ""))
        pfx = key.split("-")[1]
        em = re.match(r"\s*(E[1-8])\b", epic_row)
        be = BE.get(pfx if pfx in ("TE", "ACE", "AD", "DM") else (em.group(1) if em else pfx), "EP08")
        deps_txt = meta.get("Depends on", "")
        rows.append({
            "key": key, "title": m.group(2).strip(), "group": group, "master": str(Path(path).name),
            "meta": meta, "module": mod.group(1) if mod else None, "release": rel.group(1).strip() if rel else "",
            "business_epic": be,
            "deps": _uniq(f"RWB-{a}-{b}" for a, b in LEGACY_RE.findall(deps_txt) if f"RWB-{a}-{b}" != key),
            "feat_deps": _uniq(re.findall(r"FEAT-[A-Z]+-\d+", deps_txt)),
            "reqs": _uniq(re.findall(r"REQ-[A-Z]+-\d{3}", block)),
            "acs": _uniq(re.findall(r"Scenario:\s*(AC\d+)", block)),
            "tcs": _uniq(re.findall(r"\bTC-[A-Z0-9]+-\d{3}-\d{2}\b", block)),
            "msgs": _uniq(re.findall(r"\bMSG-[A-Z0-9]+-\d{3}\b", block)),
            "sections": {k: len(v) for k, v in _sections(block).items()},
            "status": meta.get("Status", ""),
            "chars": len(block),
            "sha256": hashlib.sha256(block.encode("utf-8")).hexdigest(),
            "story_file": None, "story_file_sha256": None,
        })
    return rows

def attach_story_files(rows):
    for grp, folder in STORY_DIRS.items():
        d = STORIES / folder
        files = {f.name: f for f in d.glob("*.md")} if d.exists() else {}
        for r in rows:
            if r["group"] != grp:
                continue
            k = r["key"].replace("RWB-", "RWB ").replace("-", " ")  # RWB E1 018
            hit = next((f for n, f in sorted(files.items()) if n.startswith(k + " ")), None)
            if hit:
                r["story_file"] = str(hit.relative_to(STORIES.parent)); r["story_file_sha256"] = sha256(hit)

def main():
    rows, counts = [], {}
    for fname, grp, exp in MASTERS:
        part = parse_master(STORIES / fname, grp); rows += part; counts[grp] = (len(part), exp)
        if len(part) != exp:
            append_jsonl(WORK / "assumptions" / "A4.jsonl", {"id": f"ASM-A4-{grp}", "text": f"{fname} has {len(part)} story headings, plan expected {exp}; the parsed count is used.", "why": "count differs", "read": fname, "confidence": "High"})
    for k, t in NF.items():
        rows.append({"key": k, "title": t, "group": "NF", "master": None, "meta": {}, "module": None, "release": "",
                     "business_epic": "NF", "deps": [], "feat_deps": [], "reqs": [], "acs": [], "tcs": [], "msgs": [],
                     "sections": {}, "status": "", "chars": 0, "sha256": None, "story_file": None, "story_file_sha256": None})
    attach_story_files(rows)
    write_json(WORK / "plan" / "legacy_index.json", rows)
    hashes = {fname: sha256(STORIES / fname) for fname, _, _ in MASTERS}
    hashes.update({r["story_file"]: r["story_file_sha256"] for r in rows if r["story_file"]})
    write_json(WORK / "plan" / "legacy_hashes.json", hashes)
    print("A4 OK", {g: c[0] for g, c in counts.items()}, "total", len(rows))

if __name__ == "__main__":
    main()
