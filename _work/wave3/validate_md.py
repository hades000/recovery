import re, csv, collections, sys

BASE = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
MD = BASE + r"\04 User stories\Recovery Workbench User Stories Epic 2 v6.md"
doc = open(MD, encoding="ascii").read()

parts = re.split(r"(?m)^(?=## RWB-E2-\d+ )", doc)
parts = [p for p in parts if p.startswith("## RWB-E2-")]
print("stories:", len(parts))

total_ac = total_tc = 0
rows = []
for p in parts:
    key = re.match(r"## (RWB-E2-\d+)", p).group(1)
    acs = re.findall(r"(?m)^  Scenario: (AC\d+) (.*)$", p)
    tcsec = re.search(r"(?ms)### 16\. Test cases(.*?)(?=### 17\.)", p)
    tcs = re.findall(r"(?m)^\| (TC-E2-\d{3}-\d{2}) \|", tcsec.group(1)) if tcsec else []
    data = re.search(r"(?ms)### 11\. Data(.*?)(?=### 12\.)", p)
    ents = []
    if data:
        for ln in data.group(1).split("\n"):
            mm = re.match(r"\| (DF-[\w\-]+(?: to DF-[\w\-]+)?|Standard column) \| ([a-z_0-9]+) \| ([a-z_0-9]+) \|", ln)
            if mm:
                e = mm.group(2)
                if e not in ents:
                    ents.append(e)
    total_ac += len(acs)
    total_tc += len(tcs)
    rows.append((key, len(acs), len(tcs), ",".join(ents)))
    print(f"{key}  AC={len(acs)}  TC={len(tcs)}")
print("TOTAL AC", total_ac, "TC", total_tc)

# header claims
for ln in doc.split("\n")[:12]:
    if ln.startswith("| Stories") or ln.startswith("| Acceptance") or ln.startswith("| Test cases") or ln.startswith("| Modules"):
        print(ln)

# entity existence
objs = set()
with open(BASE + r"\_work\data\v5_objects.csv", encoding="utf-16") as f:
    for r in csv.DictReader(f):
        objs.add(r["object_name"])
bad = []
for key, a, t, ents in rows:
    for e in ents.split(","):
        if e and e not in objs:
            bad.append((key, e))
print("entities not in v5:", bad)

# forbidden tokens in table rows / prose
forbidden = ["loan_account", "account_payment", "party_product", "contact_point |", "| collateral |", "| valuation |",
             "| party |", "collections_history", "load_run", "dq_exception", "JOB-01", "JOB-09", "tracker",
             "interface_run", "interface_signoff", "primary_customer_id", "account_payment_id"]
for f in forbidden:
    hits = [(i + 1, l.strip()[:110]) for i, l in enumerate(doc.split("\n")) if f in l]
    if hits:
        print("FORBIDDEN", f, len(hits), hits[:3])

# gherkin one When per scenario
prob = []
for p in parts:
    key = re.match(r"## (RWB-E2-\d+)", p).group(1)
    g = re.search(r"(?ms)```gherkin(.*?)```", p)
    if not g:
        prob.append((key, "no gherkin")); continue
    scen = re.split(r"(?m)^  Scenario: ", g.group(1))[1:]
    for s in scen:
        name = s.split("\n")[0]
        n = len(re.findall(r"(?m)^\s+When ", s))
        if n != 1:
            prob.append((key, name, n))
print("one-When problems:", prob)

# non ascii
print("nonascii:", sum(1 for ch in doc if ord(ch) > 127))
