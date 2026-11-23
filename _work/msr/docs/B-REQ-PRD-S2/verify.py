import io, json, os, re

ROOT = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
WP = "B-REQ-PRD-S2"
PRD = os.path.join(ROOT, "03 Requirements and specifications", "PRD",
                   "Recovery Workbench PRD S2 rwb-treatment v1.md")
t = io.open(PRD, encoding="utf-8").read()
lines = t.splitlines()
fails, notes = [], []

# 1 header
if "SCB Collections and Recovery. Henka Group, 22 November 2026." not in "\n".join(lines[:6]):
    fails.append("R8.1 header line 1 missing in the first six lines")
if "(C) Siam Commercial Bank and Henka Pte Ltd" not in "\n".join(lines[:6]):
    fails.append("R8.1 header line 2 missing in the first six lines")
if "D-RCV-60 microservice realignment" not in t or "T3 Code / OpenCode / DeepSeek v4.1 Flash" not in t:
    fails.append("change-log row missing")

# 2 ids
def ids(prefix, n, width=3):
    return [f"{prefix}-S2-{i:0{width}d}" for i in range(1, n + 1)]

caps = sorted(set(re.findall(r"\bCAP-S2-\d{3}\b", t)))
frs = sorted(set(re.findall(r"\bFR-S2-\d{3}\b", t)))
nfrs = sorted(set(re.findall(r"\bNFR-S2-\d{3}\b", t)))
acs = sorted(set(re.findall(r"\bAC-S2-\d{3}\b", t)))
oqs = sorted(set(re.findall(r"\bOQ-S2-\d{2}\b", t)))
rols = sorted(set(re.findall(r"\bROL-S2-\d{2}\b", t)))
jrns = sorted(set(re.findall(r"\bJRN-S2-\d{2}\b", t)))
notes.append(f"CAP {len(caps)}: {caps[0]}..{caps[-1]}")
notes.append(f"FR {len(frs)}: {frs[0]}..{frs[-1]}")
notes.append(f"NFR {len(nfrs)}: {nfrs[0]}..{nfrs[-1]}")
notes.append(f"AC {len(acs)}: {acs[0]}..{acs[-1]}")
notes.append(f"OQ {len(oqs)}: {len(oqs)}; ROL {len(rols)}: {len(rols)}; JRN {len(jrns)}: {len(jrns)}")
if caps != ids("CAP", 19): fails.append(f"CAP ids not contiguous 001-019: {caps}")
if frs != ids("FR", 42): fails.append(f"FR ids not contiguous 001-042: {frs}")
if nfrs != ids("NFR", 32): fails.append(f"NFR ids not contiguous 001-032: {nfrs}")
if acs != ids("AC", 24): fails.append(f"AC ids not contiguous 001-024: {acs}")

# 3 registers
gids, aids = set(), set()
for kind, s in (("gaps", gids), ("assumptions", aids)):
    for p in os.listdir(os.path.join(ROOT, "_work", "msr", kind)):
        if not p.endswith(".jsonl"):
            continue
        for line in io.open(os.path.join(ROOT, "_work", "msr", kind, p), encoding="utf-8"):
            line = line.strip()
            if line:
                s.add(json.loads(line)["id"])
cite = re.compile(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b")
missing = sorted({c for c in cite.findall(t) if c not in gids | aids})
if missing:
    fails.append(f"cited ids without a register row: {missing}")
mine_g = [i for i in gids if i.startswith(f"CG-{WP}-")]
mine_a = [i for i in aids if i.startswith(f"ASM-{WP}-")]
notes.append(f"own gap rows {len(mine_g)}; own assumption rows {len(mine_a)}")
# every own id cited?
uncited = sorted(i for i in mine_g + mine_a if i not in t)
if uncited:
    fails.append(f"register rows not cited in the PRD: {uncited}")

# 4 FR table rows
fr_rows = re.findall(r"(?m)^\| (FR-S2-\d{3}) \|(.+)$", t)
if len(fr_rows) != 42:
    fails.append(f"FR table rows {len(fr_rows)} != 42")
cap_in_fr = set()
for fid, row in fr_rows:
    cells = [c.strip() for c in row.split("|")]
    if len(cells) < 6:
        fails.append(f"{fid}: fewer than six columns: {cells}")
        continue
    cap_cell, br_cell, fsd_cell, prio, rel = cells[1], cells[2], cells[3], cells[4], cells[5]
    if not re.fullmatch(r"CAP-S2-\d{3}", cap_cell):
        fails.append(f"{fid}: CAP cell '{cap_cell}'")
    else:
        cap_in_fr.add(cap_cell)
    if not re.search(r"REQ-S2-0\d{2}", br_cell):
        fails.append(f"{fid}: no REQ-S2 requirement in the BR cell")
    if not re.search(r"REQ-S2-0\d{2}", fsd_cell):
        fails.append(f"{fid}: no FSD REQ in the FSD cell")
    if prio not in ("Must", "Should", "Could"):
        fails.append(f"{fid}: priority '{prio}'")
    if rel not in ("2", "3", "4"):
        fails.append(f"{fid}: release '{rel}'")
no_fr = [c for c in caps if c not in cap_in_fr]
if no_fr:
    fails.append(f"capabilities with no functional requirement: {no_fr}")
frs_in_table = {f for f, _ in fr_rows}
if frs_in_table != set(frs):
    fails.append(f"FR ids in text but not in the table (or the reverse): {sorted(frs ^ frs_in_table)}")

# 5 AC rows cover existing FR/NFR only
ac_rows = re.findall(r"(?m)^\| (AC-S2-\d{3}) \|([^|]+)\|", t)
if len(ac_rows) != 24:
    fails.append(f"AC table rows {len(ac_rows)} != 24")
for aid, covers in ac_rows:
    for ref in re.findall(r"(?:FR|NFR)-S2-\d{3}", covers):
        if ref not in set(frs) | set(nfrs):
            fails.append(f"{aid}: covers unknown {ref}")
covered_fr = set()
for aid, covers in ac_rows:
    covered_fr.update(re.findall(r"FR-S2-\d{3}", covers))
# ranges such as "FR-S2-007 to FR-S2-012" and "FR-S2-032 to FR-S2-035"
for a, b in re.findall(r"FR-S2-(\d{3}) to FR-S2-(\d{3})", t):
    for i in range(int(a), int(b) + 1):
        covered_fr.add(f"FR-S2-{i:03d}")
uncovered = sorted(set(frs) - covered_fr)
if uncovered:
    fails.append(f"functional requirements with no acceptance criterion: {uncovered}")

# 6 tentative dates
for d in ("31 December 2026", "31 January 2027"):
    occ = [m.start() for m in re.finditer(re.escape(d), t)]
    bad = [i for i in occ if "(tentative)" not in t[i:i + 60]]
    if bad:
        fails.append(f"{d} appears without (tentative) at {len(bad)} place(s)")

# 7 service naming
if "/api/recovery/treatment/v1" not in t: fails.append("REST base missing")
if "rwb.treatment.events.v1" not in t: fails.append("topic missing")
if "rwb-treatment" not in t: fails.append("task queue missing")
if "rwb_treatment" not in t: fails.append("schema missing")
if re.search(r"/api/recovery/v1/", t): fails.append("old monolith API base present")
if re.search(r"(?i)\bjira\b|atlassian", t): fails.append("issue tracker reference present")
for bad in ("rwb.treatments.events", "rwb_treatment.events", "/api/recovery/treatments/"):
    if bad in t: fails.append(f"suspect service name: {bad}")

# 8 no design leakage words that would be a class/endpoint design
for bad in ("(class ", "CREATE TABLE", "ALTER TABLE", "@RestController", "Spring Boot", "public class"):
    if bad in t:
        fails.append(f"solution design wording present: {bad}")

# 9 section headings present in order
heads = [h for h in re.findall(r"(?m)^# (.+)$", t) if re.match(r"^\d+\. ", h)]
want = ["1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.", "11.", "12.", "13."]
if [h.split(".")[0] + "." for h in heads] != want:
    fails.append(f"section headings: {heads}")

print("\n".join(notes))
print("FAILS:", len(fails))
for f in fails:
    print(" -", f)
