"""Structural verification for the B-PLT-TPL-01 story set (read-only)."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "_work" / "msr"
STORY_DIR = ROOT / "04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-TPL Service template and repositories"
LEGACY = ROOT / "04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB E1 044 Database migrations versioned with parameterized schema names v1.md"

META_ROWS = ["Story key", "Work type", "Suggested owner", "Service", "Service epic", "Wave", "Business epic", "Release",
             "Legacy key", "Legacy disposition", "Build status", "Patterns applied", "Parallel lane", "Ready to start",
             "Depends on (build)", "Contract dependencies", "Integration dependencies", "External dependencies",
             "PRD reference", "Status"]
SECTIONS = ["Story", "Business rationale", "Preconditions", "Flow", "Exception paths", "INVEST check", "Acceptance criteria",
            "Business rules", "State transitions", "Authority", "Data", "Contract", "Solution plan", "Validation and messages",
            "Screens and states", "Test cases", "Guardrails", "Traceability", "Out of scope"]
FILES = {
    "RWB-PLT-E1044-APP": "RWB PLT E1044 APP Database migrations versioned with parameterized schema names v1.md",
    "RWB-PLT-E1044-APP-2": "RWB PLT E1044 APP-2 Database migrations versioned with parameterized schema names v1.md",
    "RWB-PLT-E1044-CON": "RWB PLT E1044 CON Database migrations versioned with parameterized schema names - contract v1.md",
    "RWB-PLT-E1044-OPS": "RWB PLT E1044 OPS Database migrations versioned with parameterized schema names - deployment v1.md",
    "RWB-PLT-N004-OPS": "RWB PLT N004 OPS Service pipeline template and Helm chart - deployment v1.md",
    "RWB-PLT-NF01-OPS": "RWB PLT NF01 OPS Repository and pipeline baseline - deployment v1.md",
    "RWB-PLT-NF03-OPS": "RWB PLT NF03 OPS Environment baseline - deployment v1.md",
    "RWB-PLT-NF04-OPS": "RWB PLT NF04 OPS Secrets and configuration baseline - deployment v1.md",
}
FRAG_KEYS = ["id", "epic", "service", "wt", "lane", "ready", "owner", "business_epic", "wave", "release", "legacy",
             "disposition", "H", "C", "I", "X", "acs", "tcs", "reqs", "ops_provided", "ops_consumed",
             "events_published", "events_consumed", "workflows", "prd_ref", "gaps", "assumptions", "file"]


def text(p):
    return p.read_text(encoding="utf-8")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def section(t, n):
    m = re.search(rf"(?ms)^### {n}\. .*?(?=^### {n + 1}\. |\Z)", t)
    return m.group(0) if m else ""


def legacy_part(start, end):
    t = text(LEGACY)
    m = re.search(rf"(?ms)^## {start}\..*?(?=^## {end}\. |\Z)", t)
    return m.group(0) if m else ""


def main():
    fails = []
    frags = {}
    for sid, name in FILES.items():
        p = STORY_DIR / name
        if not p.exists():
            fails.append(f"{sid}: file missing")
            continue
        t = text(p)
        first = t.splitlines()[0]
        if not re.match(rf"^# {re.escape(sid)} ", first):
            fails.append(f"{sid}: bad title line {first!r}")
        head = t.split("### 1.", 1)[0]
        rows = [r.strip() for r in re.findall(r"(?m)^\|\s*([^|]+?)\s*\|", head)]
        got = [r for r in rows if r in META_ROWS]
        if got != META_ROWS:
            fails.append(f"{sid}: metadata rows {got}")
        heads = re.findall(r"(?m)^### (\d+)\. (.+?)\s*$", t)
        if [h[1] for h in heads[:19]] != SECTIONS or [int(h[0]) for h in heads[:19]] != list(range(1, 20)):
            fails.append(f"{sid}: section headings {heads[:19]}")
        for line in t.splitlines():
            if re.match(r"^\s*Scenario:\s*AC\d+", line) and not re.search(r"\((legacy RWB-E1-044 AC\d+|new, D-RCV-60)\)", line):
                fails.append(f"{sid}: AC tag missing {line.strip()[:90]}")
        for m in re.findall(r"(?i)\bjira\b|atlassian\.net", t):
            fails.append(f"{sid}: banned tracker word")
        if re.search(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", t):
            fails.append(f"{sid}: email address")
        if "T3 Code / OpenCode / DeepSeek v4.1 Flash" not in t:
            fails.append(f"{sid}: tool line missing")
        if "D-RCV-60" not in t:
            fails.append(f"{sid}: D-RCV-60 missing")
        s12 = section(t, 12)
        for sub in range(1, 10):
            if f"{12}.{sub}" not in s12:
                fails.append(f"{sid}: 12.{sub} heading missing")
        # fragment
        f = WORK / "fragments" / f"{sid}.json"
        if not f.exists():
            fails.append(f"{sid}: fragment missing")
        else:
            frag = json.loads(text(f))
            frags[sid] = frag
            if sorted(frag) != sorted(FRAG_KEYS):
                fails.append(f"{sid}: fragment keys {sorted(set(FRAG_KEYS) ^ set(frag))}")
            if frag.get("id") != sid:
                fails.append(f"{sid}: fragment id {frag.get('id')}")
            if frag.get("file") != f"04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-TPL Service template and repositories/{name}":
                fails.append(f"{sid}: fragment file path {frag.get('file')}")
            scen = set(re.findall(r"(?m)^\s*Scenario:\s*(AC\d+)", t))
            facs = {a["id"] for a in frag.get("acs", [])}
            if scen != facs:
                fails.append(f"{sid}: fragment acs {facs} vs scenarios {scen}")
            for tc in frag.get("tcs", []):
                if tc not in t:
                    fails.append(f"{sid}: fragment tc {tc} not in file")
            for g in frag.get("gaps", []):
                if g not in t:
                    fails.append(f"{sid}: gap {g} not cited")
            for a in frag.get("assumptions", []):
                if a not in t:
                    fails.append(f"{sid}: assumption {a} not cited")

    # preserved APP word-for-word check (section by section; AC tags and the
    # one level-mapping line after the legacy TC table are the only additions)
    app = STORY_DIR / FILES["RWB-PLT-E1044-APP"]
    if app.exists():
        ta = text(app)
        ta_untagged = norm(re.sub(r"\(legacy RWB-E1-044 AC\d+\)", "", ta))
        for n in list(range(1, 12)) + [14, 15, 18]:
            block = legacy_part(n, n + 1)
            if not block:
                fails.append(f"APP: legacy section {n} not found")
                continue
            body = block.split("\n", 1)[1] if "\n" in block else ""
            hay = ta_untagged if n == 7 else norm(ta)
            if norm(body) not in hay:
                fails.append(f"APP: legacy section {n} not verbatim")
        for n in (16, 19):
            block = legacy_part(n, n + 1)
            body = block.split("\n", 1)[1] if block and "\n" in block else ""
            if not block or norm(body) not in norm(ta):
                fails.append(f"APP: legacy section {n} not verbatim")
        for n in (12, 13):
            block = legacy_part(n, n + 1)
            body = block.split("\n", 1)[1] if block and "\n" in block else ""
            if body and norm(body) not in norm(ta):
                fails.append(f"APP: as-built legacy section {n} not verbatim")
        if "As built (monolith)" not in text(app):
            fails.append("APP: As built (monolith) heading missing")

    # citation check against the merged registers
    ids = set()
    for kind in ("gaps", "assumptions"):
        p = WORK / kind / "B-PLT-TPL-01.jsonl"
        if p.exists():
            for line in text(p).splitlines():
                if line.strip():
                    ids.add(json.loads(line)["id"])
    cite = re.compile(r"\b(?:CG|ASM)-B-PLT-TPL-01-[A-Za-z0-9]+-\d+\b")
    for sid, name in FILES.items():
        p = STORY_DIR / name
        if not p.exists():
            continue
        for c in set(cite.findall(text(p))):
            if c not in ids:
                fails.append(f"{sid}: cites {c} with no row")
        f = WORK / "fragments" / f"{sid}.json"
        if f.exists():
            frag = json.loads(text(f))
            for c in frag.get("gaps", []) + frag.get("assumptions", []):
                if c not in ids:
                    fails.append(f"{sid}: fragment cites {c} with no row")
    print(f"fragments={len(frags)} rows={len(ids)}")
    for x in fails:
        print("FAIL", x)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
