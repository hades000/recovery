"""Validate the B-P2-01 deliverables against the WP and the legacy stories."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WP = json.loads("[]")
WP_PATH = ROOT / "_work/msr/wp/B-P2-01.md"

# --- parse the WP story lines ------------------------------------------------
lines = []
for raw in WP_PATH.read_text(encoding="utf-8").splitlines():
    s = raw.strip()
    if s.startswith('{"id"'):
        lines.append(json.loads(s))

META = ["Story key", "Work type", "Suggested owner", "Service", "Service epic", "Wave", "Business epic",
        "Release", "Legacy key", "Legacy disposition", "Build status", "Patterns applied", "Parallel lane",
        "Ready to start", "Depends on (build)", "Contract dependencies", "Integration dependencies",
        "External dependencies", "PRD reference", "Status"]
SECTIONS = ["Story", "Business rationale", "Preconditions", "Flow", "Exception paths", "INVEST check",
            "Acceptance criteria", "Business rules", "State transitions", "Authority", "Data", "Contract",
            "Solution plan", "Validation and messages", "Screens and states", "Test cases", "Guardrails",
            "Traceability", "Out of scope"]
OWNERS = {"CON": "TechX (suggested; any team may pick up this story)",
          "APP": "TechX (suggested; any team may pick up this story)",
          "DB": "ACE team (suggested; any team may pick up this story)",
          "INF": "SCB IT infrastructure (suggested; any team may pick up this story)",
          "OPS": "DevOps team (suggested; any team may pick up this story)",
          "ITG": "TechX (suggested; any team may pick up this story)"}


def read(p):
    return Path(p).read_text(encoding="utf-8-sig")


def meta_of(text):
    head = text.split("### 1.", 1)[0]
    rows = {}
    for m in re.finditer(r"^\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*$", head, re.M):
        rows[m.group(1)] = m.group(2)
    return rows, [m.group(1) for m in re.finditer(r"^\|\s*([^|]+?)\s*\|", head, re.M)]


def sections(text):
    return [(m.group(1), m.group(2)) for m in re.finditer(r"^### (\d+)\. (.+?)\s*$", text, re.M)]


def scenarios(text):
    """Return {ACn: [lines of body]} from the gherkin block."""
    out, cur = {}, None
    for line in text.splitlines():
        m = re.match(r"^\s*Scenario:\s*(AC\d+)\b", line)
        if m:
            cur = m.group(1)
            out[cur] = []
            continue
        if cur is not None:
            if re.match(r"^\s*```", line):
                cur = None
                continue
            if re.match(r"^\s*(Scenario:|Background:)", line):
                cur = None
                continue
            out[cur].append(line.strip())
    return out


def legacy_scenarios(text):
    out, cur = {}, None
    for line in text.splitlines():
        m = re.match(r"^\s*Scenario:\s*(AC\d+)\b", line)
        if m:
            cur = m.group(1)
            out[cur] = []
            continue
        if cur is not None:
            if re.match(r"^\s*```", line):
                cur = None
                continue
            out[cur].append(line.strip())
    return {k: [x for x in v if x] for k, v in out.items()}


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


problems = []
for x in lines:
    p = ROOT / x["file"]
    if not p.exists():
        problems.append((x["id"], "MISSING FILE"))
        continue
    t = read(p)
    rows, order = meta_of(t)
    # metadata
    if not re.match(r"^# " + re.escape(x["id"]) + r" ", t):
        problems.append((x["id"], "title line"))
    for k in META:
        if k not in rows:
            problems.append((x["id"], f"metadata row missing: {k}"))
    if [r for r in order if r in META] != META:
        problems.append((x["id"], "metadata row order"))
    exp = {
        "Story key": x["id"],
        "Work type": f"{x['wt']}",
        "Suggested owner": OWNERS[x["wt"]],
        "Service": x["service"],
        "Service epic": x["epic"],
        "Wave": str(x["wave"]),
        "Business epic": x["business_epic"],
        "Release": f"{x['release']} (tentative)",
        "Legacy key": x["legacy"],
        "Legacy disposition": x["disposition"],
        "Build status": x["build_status"],
        "Parallel lane": x["lane"],
        "Ready to start": x["ready"],
    }
    for k, v in exp.items():
        got = rows.get(k, "")
        if not got.startswith(v):
            problems.append((x["id"], f"metadata {k}: '{got}' != '{v}'"))
    # dependency and pattern rows must copy the WP JSON exactly
    def deps(key):
        v = x.get(key) or []
        return ", ".join(v) if v else "None"
    if rows.get("Patterns applied", "") != ", ".join(x["patterns"]):
        problems.append((x["id"], f"Patterns applied: '{rows.get('Patterns applied')}'"))
    for k, key in (("Depends on (build)", "H"), ("Contract dependencies", "C"),
                   ("Integration dependencies", "I"), ("External dependencies", "X")):
        if rows.get(k, "") != deps(key):
            problems.append((x["id"], f"{k}: '{rows.get(k)}' != '{deps(key)}'"))
    if rows.get("PRD reference", "") != "Pending (C1)":
        problems.append((x["id"], "PRD reference"))
    if rows.get("Status", "") != "Draft (realignment v1)":
        problems.append((x["id"], "Status row"))
    if "D-RCV-60" not in t:
        problems.append((x["id"], "no D-RCV-60 change-log row"))
    if "T3 Code / OpenCode / DeepSeek v4.1 Flash" not in t:
        problems.append((x["id"], "no tool line"))
    # sections
    heads = sections(t)
    if [h[0] for h in heads[:19]] != [str(i) for i in range(1, 20)] or [h[1] for h in heads[:19]] != SECTIONS:
        problems.append((x["id"], "19 sections"))
    # contract tables
    for n in range(1, 10):
        if f"12.{n}" not in t:
            problems.append((x["id"], f"missing table 12.{n}"))
    # ACs
    got = scenarios(t)
    leg = legacy_scenarios(read(ROOT / x["source"]))
    for ac in x["acs"]:
        if ac not in got:
            problems.append((x["id"], f"{ac} missing"))
            continue
        if ac not in leg:
            problems.append((x["id"], f"{ac} not in legacy"))
            continue
        g = [norm(z) for z in got[ac] if z]
        l = [norm(z) for z in leg[ac] if z]
        j = 0
        ok = True
        for line in g:
            if j < len(l) and line == l[j]:
                j += 1
            elif re.match(r"^Given the [a-z0-9-]+ contract mock returns ", line) or re.match(r"^Given package ", line):
                continue
            else:
                ok = False
                problems.append((x["id"], f"{ac}: line not in legacy or out of order: {line[:90]}"))
                break
        if ok and j != len(l):
            problems.append((x["id"], f"{ac}: legacy lines missing ({len(l)-j})"))
    # scenario tag
    for m in re.finditer(r"(?m)^\s*Scenario:\s*(AC\d+)(.*)$", t):
        if not re.search(rf"\((legacy {re.escape(x['legacy'])} {m.group(1)}|new, D-RCV-60)\)", m.group(2)):
            problems.append((x["id"], f"{m.group(1)} origin tag missing"))
    # test cases (rule 5: only the TCs of the ACs the story owns)
    if x["acs"]:
        for tc in x["tcs_legacy"]:
            if tc not in t:
                problems.append((x["id"], f"legacy TC missing: {tc}"))
    else:
        for tc in x["tcs_legacy"]:
            if re.search(rf"\b{re.escape(tc)}\b", t):
                problems.append((x["id"], f"legacy TC on a story that owns no AC: {tc}"))
    if not re.search(r"^\|\s*TC ID\s*\|\s*Covers\s*\|\s*Level\s*\|\s*Data\s*\|", t, re.M):
        problems.append((x["id"], "section 16 table lacks the Level column"))

print(f"stories checked: {len(lines)}")
print(f"problems: {len(problems)}")
for a, b in problems[:200]:
    print(" -", a, "|", b)
