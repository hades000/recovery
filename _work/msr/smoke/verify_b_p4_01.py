"""Cross-file verifier for WP B-P4-01 (D-RCV-60). Read-only; prints findings, exits 1 on any.

Run: python -I "_work/msr/smoke/verify_b_p4_01.py"
"""
import json, re, sys
from pathlib import Path

WORK = Path(__file__).resolve().parents[1]
ROOT = WORK.parents[1]
WP = "B-P4-01"

META_ROWS = ["Story key", "Work type", "Suggested owner", "Service", "Service epic", "Wave", "Business epic", "Release",
             "Legacy key", "Legacy disposition", "Build status", "Patterns applied", "Parallel lane", "Ready to start",
             "Depends on (build)", "Contract dependencies", "Integration dependencies", "External dependencies",
             "PRD reference", "Status"]
SECTIONS = ["Story", "Business rationale", "Preconditions", "Flow", "Exception paths", "INVEST check", "Acceptance criteria",
            "Business rules", "State transitions", "Authority", "Data", "Contract", "Solution plan", "Validation and messages",
            "Screens and states", "Test cases", "Guardrails", "Traceability", "Out of scope"]
SHORTS = {"source-data", "integration", "case", "access", "document", "comms", "decision", "payment", "reporting",
          "agent", "valuation", "treatment", "guarantee", "litigation", "asset", "debtsale", "writeoff", "deviation", "partner"}
OWNER = {"TechX": "TechX (suggested; any team may pick up this story)",
         "ACE": "ACE team (suggested; any team may pick up this story)",
         "INFRA": "SCB IT infrastructure (suggested; any team may pick up this story)",
         "DEVOPS": "DevOps team (suggested; any team may pick up this story)",
         "QA": "QA team (suggested; any team may pick up this story)"}
WT_NAME = {"CON": "Contract", "APP": "App development", "DB": "ACE DB", "INF": "Infrastructure",
           "OPS": "DevOps", "ITG": "Integration"}
LEGACY_FILES = {
    "RWB-E1-022": "04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB E1 022 Sign on with SSO MFA and the first roles v1.md",
    "RWB-E1-037": "04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB E1 037 Role to permission matrix as data and PDPA field masking by role v1.md",
    "RWB-E1-039": "04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB E1 039 Access log into the decision log and break glass admin v1.md",
    "RWB-E2-019": "04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5/RWB E2 019 Partner identities through the external gateway v1.md",
    "RWB-AD-001": "04 User stories/Recovery Workbench Administration Stories v3.md",
}

fails, warns = [], []


def add(msg):
    fails.append(msg)


def warn(msg):
    warns.append(msg)


plan = json.loads((WORK / "plan" / "split_plan.json").read_text(encoding="utf-8"))
slices = {s["id"]: s for s in plan["slices"]}
mine = [s for s in plan["slices"] if s["id"].startswith(("RWB-P4-E1022-", "RWB-P4-E1037-", "RWB-P4-E1039-", "RWB-P4-E2019-", "RWB-P4-AD001-"))]
mine = sorted(mine, key=lambda s: s["id"])


def read(p):
    return Path(p).read_text(encoding="utf-8", errors="replace")


def legacy_acs(path):
    """Scenario bodies per AC id from a legacy file."""
    t = read(path)
    out = {}
    for m in re.finditer(r"Scenario: (AC\d+)[^\n]*\n(.*?)(?=\n\s*Scenario:|\n```|\Z)", t, re.S):
        body = [l.strip() for l in m.group(2).strip("\n").splitlines() if l.strip()]
        out[m.group(1)] = body
    return out


def new_acs(text):
    out = {}
    for m in re.finditer(r"Scenario: (AC\d+) ([^\n]*)\n(.*?)(?=\n\s*Scenario:|\n```|\Z)", text, re.S):
        tag = re.search(r"\((legacy RWB-[A-Z0-9-]+ (AC\d+)|new, D-RCV-60)\)\s*$", m.group(2))
        body = [l.strip() for l in m.group(3).strip("\n").splitlines() if l.strip()]
        out[m.group(1)] = {"title": m.group(2), "tag": tag.group(0) if tag else None, "body": body}
    return out


def parse_meta(text):
    head = text.split("### 1.", 1)[0]
    rows = {}
    for line in head.splitlines():
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 2 and cells[0] in META_ROWS:
                rows[cells[0]] = cells[1]
    return rows


def table_rows(text, start_pat, end_pat=None):
    m = re.search(start_pat, text)
    if not m:
        return []
    rest = text[m.end():]
    if end_pat:
        rest = rest.split(end_pat, 1)[0]
    out = []
    for line in rest.splitlines():
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and not set("".join(cells)) <= set("-: "):
                out.append(cells)
    return out


stories = []
for s in mine:
    p = ROOT / s["file"]
    if not p.exists():
        add(f"{s['id']}: story file missing: {s['file']}")
        continue
    stories.append(s)
    t = read(p)
    frag_p = WORK / "fragments" / f"{s['id']}.json"
    if not frag_p.exists():
        add(f"{s['id']}: fragment missing")
        frag = {}
    else:
        try:
            frag = json.loads(frag_p.read_text(encoding="utf-8"))
        except Exception as e:
            add(f"{s['id']}: fragment not valid JSON: {e}")
            frag = {}

    # 1 title
    first = t.splitlines()[0] if t.splitlines() else ""
    if first != f"# {s['id']} {s['title']}":
        add(f"{s['id']}: title line is {first!r}")
    # 2 header + change log
    head6 = "\n".join(t.splitlines()[:6])
    if "SCB Collections and Recovery. Henka Group," not in head6:
        add(f"{s['id']}: header line missing in the first six lines")
    if "D-RCV-60" not in head6 or "T3 Code / OpenCode / DeepSeek v4.1 Flash" not in head6:
        add(f"{s['id']}: change log with D-RCV-60 and the tool line missing in the first six lines")
    # 3 metadata
    meta = parse_meta(t)
    got = [r for r in META_ROWS if r in meta]
    if got != META_ROWS:
        add(f"{s['id']}: metadata rows missing or out of order: {[r for r in META_ROWS if r not in meta]}")
    exp = {
        "Story key": s["id"],
        "Work type": f"{s['wt']} ({WT_NAME[s['wt']]})",
        "Suggested owner": OWNER[s["owner"]],
        "Service": "rwb-access",
        "Service epic": s["epic"],
        "Wave": str(s["wave"]),
        "Business epic": s["business_epic"],
        "Release": s["release"] + " (tentative)",
        "Legacy key": s["legacy"],
        "Legacy disposition": s["disposition"],
        "Build status": s["build_status"],
        "Patterns applied": ", ".join(s["patterns"]),
        "Parallel lane": s["lane"],
        "Ready to start": s["ready"],
        "Depends on (build)": ", ".join(s["H"]) if s["H"] else "None",
        "Contract dependencies": ", ".join(s["C"]) if s["C"] else "None",
        "Integration dependencies": ", ".join(s["I"]) if s["I"] else "None",
        "External dependencies": ", ".join(s["X"]) if s["X"] else "None",
        "PRD reference": "Pending (C1)",
        "Status": "Draft (realignment v1)",
    }
    for k, v in exp.items():
        if meta.get(k) != v:
            add(f"{s['id']}: metadata {k} = {meta.get(k)!r}, expected {v!r}")
    # 4 sections
    heads = re.findall(r"^### (\d+)\. (.+?)\s*$", t, re.M)
    if [h[1] for h in heads[:19]] != SECTIONS or [int(h[0]) for h in heads[:19]] != list(range(1, 20)):
        add(f"{s['id']}: the 19 section headings are not complete and in order")
    # 5 contract sub-tables
    subs = re.findall(r"^#### (12\.\d) (.+?)\s*$", t, re.M)
    if [x[0] for x in subs] != [f"12.{i}" for i in range(1, 10)]:
        add(f"{s['id']}: section 12 sub-tables are {[x[0] for x in subs]}, expected 12.1-12.9")
    # 6 ACs
    nac = new_acs(t)
    for aid, a in nac.items():
        if not a["tag"]:
            add(f"{s['id']}: {aid} has no origin tag")
    line_tags = [l for l in t.splitlines() if re.match(r"^\s*Scenario:\s*AC\d+", l)]
    for l in line_tags:
        if not re.search(r"\((legacy RWB-[A-Z0-9-]+ AC\d+|new, D-RCV-60)\)\s*$", l):
            add(f"{s['id']}: scenario line without a trailing origin tag: {l.strip()[:70]}")
    owned = s.get("acs") or []
    legacy_owned = [a for a in owned if f"AC{a[2:]}" in owned] if owned else []
    if owned:
        missing = [a for a in owned if a not in nac]
        extra = [a for a in nac if a not in owned]
        if missing:
            add(f"{s['id']}: legacy ACs owned but not written: {missing}")
        for a in owned:
            tg = nac.get(a, {}).get("tag") or ""
            if f"(legacy {s['legacy']} {a})" not in tg:
                add(f"{s['id']}: {a} tag is {tg!r}, expected (legacy {s['legacy']} {a})")
        if extra:
            warn(f"{s['id']}: extra scenarios beyond the owned set: {extra}")
    else:
        for aid, a in nac.items():
            if a["tag"] != "(new, D-RCV-60)":
                add(f"{s['id']}: {aid} must be tagged (new, D-RCV-60), is {a['tag']!r}")
    # 7 verbatim legacy AC bodies
    if owned:
        leg = legacy_acs(ROOT / LEGACY_FILES[s["legacy"]])
        for a in owned:
            lb, nb = leg.get(a), nac.get(a, {}).get("body", [])
            if lb is None:
                add(f"{s['id']}: legacy {s['legacy']} {a} not found in the legacy file")
                continue
            if "AD-001" in s["legacy"]:
                continue
            lset = list(lb)
            nset = list(nb)
            # one or more legacy Givens may be replaced by a mocked boundary Given
            if [x for x in nset if "contract mock returns" in x]:
                nset = [x for x in nset if "contract mock returns" not in x]
                kept, i = [], 0
                for line in lset:
                    if i < len(nset) and line == nset[i]:
                        kept.append(line)
                        i += 1
                    elif line.lower().startswith("given"):
                        continue
                    else:
                        kept.append(line)
                if i != len(nset):
                    add(f"{s['id']}: {a} is not verbatim; unmatched new line: {nset[i][:110]}")
                    continue
                lset = kept
            if lset != nset:
                diff = [x for x in lset if x not in nset] + [x for x in nset if x not in lset]
                add(f"{s['id']}: {a} is not verbatim; first difference: {diff[0][:110] if diff else 'order'}")
    # 8 TCs
    tc_rows = table_rows(t, r"### 16\. Test cases", r"### 17\.")
    tcs = [r[0] for r in tc_rows if r and re.match(r"^TC-", r[0])]
    for r in tc_rows:
        if len(r) >= 4 and r[0].startswith("TC-"):
            if "," in r[0]:
                add(f"{s['id']}: TC id cell holds a list, not one id: {r[0][:60]}")
            if r[2] not in {"Unit", "Component", "Contract", "Integration", "End to end", "NFR"}:
                add(f"{s['id']}: {r[0]} Level {r[2]!r} is not one of the six")
    if len(tc_rows) < 2 or not tcs:
        add(f"{s['id']}: section 16 has no test-case rows")
    if tcs and sorted(tcs) != sorted(frag.get("tcs") or []):
        add(f"{s['id']}: fragment tcs do not match section 16: {sorted(set(tcs) ^ set(frag.get('tcs') or []))[:6]}")
    if owned:
        for tc in s["tcs_legacy"]:
            if tc not in t:
                warn(f"{s['id']}: legacy TC {tc} not named anywhere in the file")
    # 9 fragment identity
    for k in ["id", "epic", "service", "wt", "lane", "ready", "owner", "business_epic", "wave", "release",
              "legacy", "disposition", "H", "C", "I", "X", "acs", "tcs", "reqs", "ops_provided", "ops_consumed",
              "events_published", "events_consumed", "workflows", "prd_ref", "gaps", "assumptions", "file"]:
        if k not in frag:
            add(f"{s['id']}: fragment key {k} missing")
    if frag:
        if list(frag.keys()) != ["id", "epic", "service", "wt", "lane", "ready", "owner", "business_epic", "wave",
                                 "release", "legacy", "disposition", "H", "C", "I", "X", "acs", "tcs", "reqs",
                                 "ops_provided", "ops_consumed", "events_published", "events_consumed", "workflows",
                                 "prd_ref", "gaps", "assumptions", "file"]:
            warn(f"{s['id']}: fragment key order differs from the WP order")
        for k in ["epic", "wt", "lane", "ready", "owner", "business_epic", "wave", "release", "legacy", "disposition"]:
            if frag.get(k) != s.get(k):
                add(f"{s['id']}: fragment {k} = {frag.get(k)!r}, plan says {s.get(k)!r}")
        for k in ["H", "C", "I", "X"]:
            if frag.get(k) != s.get(k):
                add(f"{s['id']}: fragment {k} does not match the plan")
        if owned:
            if (frag.get("acs") and [a.get("id") for a in frag["acs"]]) != owned:
                add(f"{s['id']}: fragment acs {[a.get('id') for a in frag.get('acs', [])]} != owned {owned}")
        else:
            if not frag.get("acs"):
                add(f"{s['id']}: fragment acs is empty; the new criteria of this story are missing")
            for a in frag.get("acs") or []:
                if a.get("origin") != "new, D-RCV-60":
                    add(f"{s['id']}: fragment {a.get('id')} origin {a.get('origin')!r}, expected new, D-RCV-60")
        for a in frag.get("acs") or []:
            if owned and a.get("id") not in owned:
                continue
            first = (a.get("text_first_line") or "").strip()
            if first and first not in t:
                add(f"{s['id']}: fragment AC first line not in the file: {first[:70]}")
        if frag.get("file") != s["file"]:
            add(f"{s['id']}: fragment file path differs from the plan")
        if frag.get("prd_ref") != "Pending (C1)":
            add(f"{s['id']}: fragment prd_ref is {frag.get('prd_ref')!r}")
    # 10 patterns
    for dp in s["patterns"]:
        if not re.search(rf"\b{dp.replace('DP', 'DP-')}\b", t):
            add(f"{s['id']}: pattern {dp} not applied in the file")
    # 11 forbidden and naming
    low = t.lower()
    if re.search(r"\bjira\b|atlassian\.net", low):
        add(f"{s['id']}: refers to the issue tracker")
    if re.search(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", t):
        add(f"{s['id']}: contains an email address")
    if "Co-Authored-By" in t or "Generated with" in t:
        add(f"{s['id']}: wrong tool attribution")
    for rx in [r"\brwb\.([a-z-]+)\.events\.v1\b", r"/api/recovery/([a-z-]+)/v1\b", r"\bqueue rwb-([a-z-]+)\b"]:
        for m in re.finditer(rx, t):
            if m.group(1) not in SHORTS:
                add(f"{s['id']}: unknown service short {m.group(1)!r} in {m.group(0)}")
    if re.search(r"/api/recovery/v1/", t) and "As built (monolith)" not in t:
        add(f"{s['id']}: monolith API base outside an as-built section")
    # 12 no legacy sections copied wholesale
    if "As built (monolith)" in t:
        add(f"{s['id']}: has an As built (monolith) heading but preserved=false")

# registers
rows_gap = [json.loads(l) for l in (WORK / "gaps" / f"{WP}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
rows_asm = [json.loads(l) for l in (WORK / "assumptions" / f"{WP}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
ids = {r["id"] for r in rows_gap} | {r["id"] for r in rows_asm}
for kind in ("gaps", "assumptions"):
    for p in (WORK / kind).glob("*.jsonl"):
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                ids.add(json.loads(line)["id"])
own_ids = {r["id"] for r in rows_gap} | {r["id"] for r in rows_asm}
if len({r["id"] for r in rows_gap}) != len(rows_gap):
    add("duplicate gap ids")
if len({r["id"] for r in rows_asm}) != len(rows_asm):
    add("duplicate assumption ids")
for r in rows_gap:
    for k in ["id", "title", "description", "type", "severity", "source", "area", "wp"]:
        if not str(r.get(k) or "").strip():
            add(f"gap {r.get('id')}: empty {k}")
    if r.get("type") not in {"Missing", "Conflict", "Ambiguous", "Outdated", "ID collision"}:
        add(f"gap {r.get('id')}: type {r.get('type')!r}")
    if r.get("severity") not in {"P1", "P2", "P3"}:
        add(f"gap {r.get('id')}: severity {r.get('severity')!r}")
    if r.get("wp") != WP:
        add(f"gap {r.get('id')}: wp {r.get('wp')!r}")
    if not str(r.get("id", "")).startswith(f"CG-{WP}-"):
        add(f"gap {r.get('id')}: id prefix")
for r in rows_asm:
    for k in ["id", "text", "why", "gap", "applied_in", "confidence", "confirm", "impact", "wp"]:
        if not str(r.get(k) or "").strip():
            add(f"asm {r.get('id')}: empty {k}")
    if r.get("confidence") not in {"High", "Medium", "Low"}:
        add(f"asm {r.get('id')}: confidence {r.get('confidence')!r}")
    if not str(r.get("id", "")).startswith(f"ASM-{WP}-"):
        add(f"asm {r.get('id')}: id prefix")

# citations resolve, per file
cite = re.compile(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b")
for s in stories:
    t = read(ROOT / s["file"])
    for c in sorted(set(cite.findall(t))):
        if c not in ids:
            add(f"{s['id']}: cites {c} with no register row")
    fp = WORK / "fragments" / f"{s['id']}.json"
    if fp.exists():
        fg = json.loads(fp.read_text(encoding="utf-8"))
        for c in (fg.get("gaps") or []) + (fg.get("assumptions") or []):
            if c not in own_ids:
                add(f"{s['id']}: fragment names {c} with no row in the WP registers")

# every legacy AC of the five keys is owned by exactly one slice here
for leg in LEGACY_FILES:
    owned = {}
    for s in mine:
        for a in s.get("acs") or []:
            if s["legacy"] == leg:
                owned[a] = owned.get(a, 0) + 1
    for a, n in owned.items():
        if n > 1:
            add(f"{leg}: {a} owned by {n} slices")

print(f"stories={len(stories)} gaps={len(rows_gap)} assumptions={len(rows_asm)}")
for w in warns:
    print("WARN", w)
for f in fails:
    print("FAIL", f)
print("RESULT", "FAIL" if fails else "PASS", f"({len(fails)} failures, {len(warns)} warnings)")
sys.exit(1 if fails else 0)
