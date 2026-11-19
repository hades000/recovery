import io, os, re, csv, sys

BASE = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
FILES = [("AD", os.path.join(BASE, r"04 User stories\Recovery Workbench Administration Stories v3.md")),
         ("DM", os.path.join(BASE, r"04 User stories\Recovery Workbench Data Migration Stories v3.md"))]

objs = set()
for r in csv.DictReader(open(os.path.join(BASE, r"_work/data/v5_objects.csv"), encoding="utf-16")):
    objs.add(r["object_name"])
field_ids = set()
field_of = {}
for r in csv.DictReader(open(os.path.join(BASE, r"_work/data/v5_fields.csv"), encoding="utf-16")):
    field_ids.add(r["field_id"])
    field_of[(r["object_name"], r["field_name"])] = r["field_id"]

BANNED = ["SY-DATALOAD", "load_run", "dq_exception", "tracker", "Tracker", "loan_account",
          "account_payment", "contact_point ", "collateral_id", "party_id", "primary_customer_id",
          "JOB-01", "JOB-09", "LoadCompleted", "LoadRefused", "value_token", "id_no_token"]

bad = 0
for tag, path in FILES:
    doc = io.open(path, encoding="ascii").read()
    print("=" * 70)
    print(tag, os.path.basename(path), len(doc), "chars")
    print("non-ascii:", sum(1 for b in io.open(path, "rb").read() if b > 127))

    for b in BANNED:
        hits = [i + 1 for i, l in enumerate(doc.split("\n")) if b in l]
        if hits:
            bad += 1
            print(" BANNED %-16s lines %s" % (b, hits[:8]))

    blocks = re.split(r"(?m)^(?=## RWB-)", doc)
    blocks = [b for b in blocks if b.startswith("## RWB-")]
    print("stories:", len(blocks))

    acs_all = set()
    tcs_all = set()
    ent_checked = 0
    for b in blocks:
        key, title = re.match(r"## (RWB-\w+-\d+) (.*)", b).groups()
        # data table entities
        dsec = re.search(r"(?ms)^\*\*Data\*\*\n(.*?)(?=^\*\*Endpoints|\Z)", b)
        if dsec:
            for ln in dsec.group(1).split("\n"):
                m = re.match(r"^\| ([a-z_0-9]+) \| .* \| (DF-[A-Z0-9]*-[0-9]+(?: to DF-[A-Z0-9]*-[0-9]+)?(?:, DF-[A-Z0-9]*-[0-9]+)*) \|$", ln)
                if not m:
                    continue
                ent, ids = m.group(1), m.group(2)
                ent_checked += 1
                if ent not in objs:
                    bad += 1
                    print("  MISSING ENTITY", key, ent)
                for part in ids.split(", "):
                    mm = re.match(r"(DF-[A-Z0-9]*-\d+) to (DF-[A-Z0-9]*-\d+)", part)
                    if mm:
                        a, c = mm.groups()
                        for x in (a, c):
                            if x not in field_ids:
                                bad += 1
                                print("  MISSING FIELD ID", key, x)
                        # range must belong to the entity
                        if (ent, "x") and not any(
                            v.startswith(mm.group(1).rsplit("-", 1)[0]) and
                            int(v.rsplit("-", 1)[1]) >= int(a.rsplit("-", 1)[1]) and
                            int(v.rsplit("-", 1)[1]) <= int(c.rsplit("-", 1)[1]) for (e, f), v in field_of.items() if e == ent):
                            bad += 1
                            print("  RANGE NOT IN ENTITY", key, ent, part)
                    else:
                        if part not in field_ids:
                            bad += 1
                            print("  MISSING FIELD ID", key, part)
                        elif not any(v == part and e == ent for (e, f), v in field_of.items()):
                            bad += 1
                            print("  FIELD NOT IN ENTITY", key, ent, part)

        # gherkin
        g = re.search(r"(?ms)```gherkin\n(.*?)```", b)
        if g:
            sc = re.findall(r"(?m)^  Scenario: (AC\d+) (.*)$", g.group(1))
            body = re.split(r"(?m)^  Scenario: ", g.group(1))[1:]
            for (code, name), chunk in zip(sc, body):
                acs_all.add((key, code))
                if chunk.count("\n    When ") != 1:
                    bad += 1
                    print("  GHERKIN WHEN COUNT", key, code, chunk.count("\n    When "))
                if "\n    Given " not in chunk or "\n    Then " not in chunk:
                    bad += 1
                    print("  GHERKIN MISSING STEP", key, code)
        else:
            if "Removed" not in b[:200]:
                bad += 1
                print("  NO GHERKIN", key)

        # test cases
        tsec = re.search(r"(?ms)^\*\*Test cases\*\*\n(.*?)(?=^\*\*Guardrails)", b)
        if tsec:
            for ln in tsec.group(1).split("\n"):
                m = re.match(r"^\| (TC-\w+-\d+-\d+) \| ([^|]+?) \|", ln)
                if m:
                    tcs_all.add((key, m.group(1), m.group(2).strip()))

    # tc <-> ac cross-check
    for key, tc, covers in sorted(tcs_all):
        if covers.startswith("AC"):
            code = covers.split(",")[0].strip()
            if (key, code) not in acs_all:
                bad += 1
                print("  TC COVERS UNKNOWN AC", tc, covers)
    covered = {(k, c.split(",")[0].strip()) for k, t, c in tcs_all if c.startswith("AC")}
    for key, code in sorted(acs_all):
        if (key, code) not in covered:
            bad += 1
            print("  AC WITHOUT TC", key, code)
    print("entities checked:", ent_checked, " ACs:", len(acs_all), " TCs:", len(tcs_all))

print("=" * 70)
print("DEFECTS:", bad)
