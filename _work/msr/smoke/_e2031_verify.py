import json, re, os

base = r"04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P10 rwb-agent (Agent)"
files = {
 "APP": ("RWB P10 E2031 APP Agent monitoring dashboard v2 [E3d] v1.md", "RWB-P10-E2031-APP"),
 "CON": ("RWB P10 E2031 CON Agent monitoring dashboard v2 [E3d] - contract v1.md", "RWB-P10-E2031-CON"),
 "OPS": ("RWB P10 E2031 OPS Agent monitoring dashboard v2 [E3d] - deployment v1.md", "RWB-P10-E2031-OPS"),
}
meta = ["Story key","Work type","Suggested owner","Service","Service epic","Wave","Business epic","Release",
        "Legacy key","Legacy disposition","Build status","Patterns applied","Parallel lane","Ready to start",
        "Depends on (build)","Contract dependencies","Integration dependencies","External dependencies",
        "PRD reference","Status"]
sections = ["1. Story","2. Business rationale","3. Preconditions","4. Flow","5. Exception paths","6. INVEST check",
            "7. Acceptance criteria","8. Business rules","9. State transitions","10. Authority","11. Data","12. Contract",
            "13. Solution plan","14. Validation and messages","15. Screens and states","16. Test cases",
            "17. Guardrails","18. Traceability","19. Out of scope"]
bad_words = ["jira","atlassian","co-authored","@","todo","tbd","xxx"]

gap_ids = set()
for line in open(r"_work/msr/gaps/B-P10-02-E2031.part.jsonl", encoding="utf-8"):
    if line.strip():
        gap_ids.add(json.loads(line)["id"])
asm_ids = set()
for line in open(r"_work/msr/assumptions/B-P10-02-E2031.part.jsonl", encoding="utf-8"):
    if line.strip():
        asm_ids.add(json.loads(line)["id"])

for tag, (name, key) in files.items():
    p = os.path.join(base, name)
    lines = open(p, encoding="utf-8").read().split("\n")
    print("==", tag, "lines", len(lines))
    print("  title:", lines[0])
    print("  hdr2:", lines[2], "|", lines[3])
    rows = []
    for l in lines:
        m = re.match(r"^\| ([^|]+?) \|", l)
        if m and m.group(1).strip() in meta:
            rows.append(m.group(1).strip())
    print("  meta rows:", len(rows), "in order:", rows == meta)
    if rows != meta:
        print("   got:", rows)
    h3 = [x for x in re.findall(r"(?m)^### (.+)$", "\n".join(lines))]
    print("  sections ok:", h3 == sections, len(h3))
    t = "\n".join(lines)
    cg = set(re.findall(r"CG-B-P10-02-E2031-\d", t))
    missing_cg = [c for c in cg if c not in gap_ids]
    asm = set(re.findall(r"ASM-B-P10-02-E2031-\d+", t))
    missing_asm = [a for a in asm if a not in asm_ids]
    print("  cg cited:", sorted(cg), "missing:", missing_cg)
    print("  asm cited:", sorted(asm, key=lambda s: int(s.rsplit('-',1)[1])), "missing:", missing_asm)
    print("  monolith base:", t.count("/api/recovery/v1"))
    print("  release tentative:", "| Release | 31 December 2026 (tentative) |" in t)
    low = t.lower()
    print("  bad words:", [w for w in bad_words if w in low])
    # scenario tags
    sc = re.findall(r"(?m)^\s*Scenario: .*$", t)
    print("  scenarios:", len(sc), "untagged:", [s for s in sc if not (s.rstrip().endswith("(new, D-RCV-60)") or "(legacy RWB-E2-031 AC" in s)])
    print("  change log D-RCV-60/date/tool:", ("D-RCV-60" in t), ("22 November 2026" in t), ("Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash." in t))
    print("  level column:", "| TC ID | Covers | Level | Data |" in t)
