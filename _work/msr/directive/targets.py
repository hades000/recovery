"""Normalise the free-text cross-document targets into one list of target documents (D-RCV-60).

Each Cross-document disposition (merged: Haiku, then Sonnet and Opus corrections) has a free-text `target`. Rules
map the text to a canonical key: STORY:<key> for another story, a project file (latest version) for a known
document, API:<service>.yaml for an API spec file, or OTHER:<text> for the light model check.

Usage: python -I targets.py [--model-check]   writes mp/targets/targets.json, by_target.jsonl, unknown.json
Library: normalise(text) -> list of keys; FILES: key -> ROOT-relative file of the latest version.
"""
import argparse, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

D = Path(__file__).resolve().parent
ROOT = D.parents[2]
MP = D / "mp"
sys.path.insert(0, str(D))


def latest(folder, stem):
    """Latest ' vN' file in ROOT/folder whose name starts with stem (prefers .md, then .xlsx, then .docx)."""
    best = None
    for p in (ROOT / folder).glob(f"{stem} v*"):
        m = re.match(re.escape(stem) + r" v(\d+)(\.\w+)?$", p.name)
        if not m:
            continue
        rank = (int(m.group(1)), {".md": 3, ".xlsx": 2, ".docx": 1}.get((m.group(2) or "").lower(), 0))
        if best is None or rank > best[0]:
            best = (rank, p)
    return best[1].relative_to(ROOT).as_posix() if best else None


DOCS = [  # (key, regex on the target text, folder, file stem)
    ("Temporal Catalog", r"temporal (workflow and activity )?catalog|activity catalog|temporal workflow", "05 Technical architecture",
     "Recovery Workbench Temporal Workflow and Activity Catalog"),
    ("Kafka Catalog", r"kafka (topic and event )?catalog|event catalog", "05 Technical architecture",
     "Recovery Workbench Kafka Topic and Event Catalog"),
    ("RTM", r"\brtm\b|requirements traceability matrix|traceability matrix", "09 Testing and quality",
     "Recovery Workbench Requirements Traceability Matrix"),
    ("Error and Message Standard", r"error and message standard|message standard", "07 Screens and experience",
     "Recovery Workbench Error and Message Standard"),
    ("Users Roles and Permissions", r"users,? roles|roles and permissions", "02 Business architecture and process",
     "Recovery Workbench Users Roles and Permissions"),
    ("Test Cases", r"\btest cases v\d|test cases workbook|test cases\b(?! for)", "09 Testing and quality",
     "Recovery Workbench Test Cases"),
    ("LDM", r"\bldm\b|logical data model", "06 Data", "Recovery Workbench Logical Data Model and Data Dictionary"),
    ("Data Classification", r"data classification", "06 Data", "Recovery Workbench Data Classification and Personal Data Inventory"),
    ("Ownership Map", r"ownership map", "22 Microservice Realignment", "Recovery Workbench Microservice Ownership Map"),
    ("Service Contract Catalog", r"service contract catalog|contract catalog", "05 Technical architecture",
     "Recovery Workbench Service Contract Catalog"),
    ("Service Template Specification", r"service template spec", "05 Technical architecture",
     "Recovery Workbench Service Template Specification"),
    ("Dependency Map", r"dependency map", "11 Delivery and operations", "Recovery Workbench Dependency Map"),
    ("Service Story Catalog", r"service story catalog|story catalog", "04 User stories", "Recovery Workbench Service Story Catalog"),
    ("Reference Data", r"reference data v\d|reference data workbook|\blov\b", "06 Data", "Recovery Workbench Reference Data and Lists of Values"),
    ("Decision Log", r"decision log", "01 Decisions and governance", "Recovery Workbench Decision Log"),
    ("Change Register", r"change register", "22 Microservice Realignment", "Recovery Workbench Microservice Change Register"),
    ("Architecture v5", r"architecture v5|arch v5", "22 Microservice Realignment", "Recovery Workbench Architecture v5 Text Extract"),
    ("Physical Schema", r"physical schema", "06 Data", "Recovery Workbench Physical Schema"),
    ("Event and Messaging Design", r"event and messaging", "05 Technical architecture", "Recovery Workbench Event and Messaging Design"),
    ("Business Rules and Routing Logic", r"business rules and routing|routing logic", "02 Business architecture and process",
     "Recovery Workbench Business Rules and Routing Logic"),
    ("Epic design record", r"epic design", "04 User stories", "(none)"),
    ("Definition of Ready and Done", r"definition of ready", "09 Testing and quality", "Recovery Workbench Definition of Ready and Done"),
]
FILES = {}


def resolve_files():
    for key, _, folder, stem in DOCS:
        f = latest(folder, stem)
        if f is None:  # search the whole tree once for the stem
            hits = sorted(p for p in ROOT.glob(f"[0-9]*/**/{stem} v*") if "_work" not in p.parts)
            f = hits[-1].relative_to(ROOT).as_posix() if hits else None
        FILES[key] = f
    api = ROOT / "05 Technical architecture/Recovery Workbench API Specification v5"
    for p in api.glob("*.yaml"):
        FILES[f"API:{p.name}"] = p.relative_to(ROOT).as_posix()
    FILES["parameter-catalog.csv"] = "parameter-catalog.csv"
    for p in (ROOT / "03 Requirements and specifications/PRD").glob("*.md"):
        m = re.match(r"Recovery Workbench PRD (\S+)", p.name)
        if m:
            k = f"PRD {m.group(1)}"
            if k not in FILES or p.name > Path(FILES[k]).name:
                FILES[k] = p.relative_to(ROOT).as_posix()


STORY = re.compile(r"\bRWB-[A-Z0-9]+-[A-Z0-9]+-[A-Z]+\b")


def normalise(text):
    t = (text or "").strip()
    if not t:
        return ["OTHER:(no target)"]
    keys = []
    for part in re.split(r";\s*|,\s+(?=[A-Z0-9])", t):
        p = part.strip()
        if not p:
            continue
        found = []
        found += [f"STORY:{k}" for k in STORY.findall(p)]
        found += [f"API:{m}" for m in re.findall(r"\b(rwb-[a-z-]+\.yaml|gateway-bff\.yaml|index\.yaml)\b", p)]
        if re.search(r"parameter[- ]catalog", p, re.I):
            found.append("parameter-catalog.csv")
        m = re.search(r"\bPRD (P\d+|S\d+|PLT)\b", p)
        if m:
            found.append(f"PRD {m.group(1)}")
        for key, rx, _, _ in DOCS:
            if re.search(rx, p, re.I):
                found.append(key)
        if not found and re.search(r"api spec", p, re.I):
            found.append("API:(service not named)")
        keys += found or ["OTHER:" + " ".join(p.split())[:120]]
    out = []
    for k in keys:
        if k not in out:
            out.append(k)
    return out


def collect():
    import esc
    stories = [s for s, _ in json.loads((MP / "stories.json").read_text())]
    rows = []
    for s in stories:
        if not esc.haiku_complete(s):
            continue
        final = esc.opus_done(s)  # a target document is ready when every story citing it is reviewed
        for r, d in esc.merged_dispositions(s).items():
            if d["status"] == "Cross-document":
                rows.append(dict(d, story=s, final=final, keys=normalise(d.get("target", ""))))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    resolve_files()
    rows = collect()
    by = defaultdict(list)
    for r in rows:
        for k in r["keys"]:
            by[k].append(r)
    out = MP / "targets"
    out.mkdir(parents=True, exist_ok=True)
    with (out / "by_target.jsonl").open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    summary = [{"key": k, "file": FILES.get(k) or (k[6:] if k.startswith("STORY:") else None), "items": len(v),
                "stories": len({x["story"] for x in v})} for k, v in sorted(by.items(), key=lambda x: -len(x[1]))]
    (out / "targets.json").write_text(json.dumps(summary, ensure_ascii=False, indent=0), encoding="utf-8")
    unk = [s for s in summary if s["key"].startswith("OTHER:")]
    (out / "unknown.json").write_text(json.dumps(unk, ensure_ascii=False, indent=0), encoding="utf-8")
    kinds = Counter("story" if s["key"].startswith("STORY:") else "other" if s["key"].startswith("OTHER:") else
                    "document" for s in summary)
    items = Counter("story" if s["key"].startswith("STORY:") else "other" if s["key"].startswith("OTHER:") else
                    "document" for r in rows for s in [{"key": r["keys"][0]}])
    print(f"{len(rows)} cross-document items; {len(summary)} targets {dict(kinds)}; first target kind {dict(items)}")
    for s in summary[:25]:
        print(s["items"], s["key"], "->", s["file"])


if __name__ == "__main__":
    main()
