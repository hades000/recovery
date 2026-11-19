"""Compare sys_fields.is_personal in Physical Schema v6 with the Personal data column of the
PDPA Inventory v4 (Fields tab), and measure the Story v7 section 13 seed values against the
data_product column widths.
Usage: python -I pdpa_v4_vs_ps_v6.py <ps-v6.sql> <inventory-v4.md> <story-v7.md>"""
import re, sys, collections

ps, inv, story = (open(p, encoding="utf-8").read() for p in sys.argv[1:4])

def parse_values(stmt):
    v = stmt[stmt.index("VALUES") + 6:].strip().rstrip(";").strip()[1:-1]
    out, cur, q, i = [], "", False, 0
    while i < len(v):
        c = v[i]
        if q:
            if c == "'" and i + 1 < len(v) and v[i + 1] == "'":
                cur += "'"; i += 2; continue
            if c == "'":
                q = False; i += 1; continue
            cur += c
        elif c == "'":
            q = True
        elif c == ",":
            out.append(cur.strip()); cur = ""
        else:
            cur += c
        i += 1
    out.append(cur.strip())
    return out

ps_fields = {}
for ln in ps.splitlines():
    if ln.startswith("INSERT INTO sys_fields"):
        cols = [c.strip() for c in ln[ln.index("(") + 1:ln.index(")")].split(",")]
        d = dict(zip(cols, parse_values(ln)))
        ps_fields[d["field_id"]] = d

# Inventory v4 Fields tab: lines starting "| DF-" before the "## Summary" heading
fields_part = inv.split("## Summary")[0]
inv_rows = {}
for ln in fields_part.splitlines():
    if ln.startswith("| DF-"):
        c = [x.strip() for x in ln.strip().strip("|").split("|")]
        inv_rows[c[0]] = {"entity": c[1], "field": c[2], "category": c[3], "class": c[4], "personal": c[5]}

print("PS v6 sys_fields rows:", len(ps_fields), " is_personal=true:",
      sum(1 for f in ps_fields.values() if f["is_personal"].lower() == "true"))
print("Inventory v4 Fields rows:", len(inv_rows), " Personal=Yes:",
      sum(1 for r in inv_rows.values() if r["personal"] == "Yes"))
print("Inventory categories:", dict(collections.Counter(r["category"] for r in inv_rows.values())))
both = set(ps_fields) & set(inv_rows)
print("field IDs in both:", len(both), " PS v6 only:", len(set(ps_fields) - set(inv_rows)),
      " inventory only:", len(set(inv_rows) - set(ps_fields)))

def ps_true(fid): return ps_fields[fid]["is_personal"].lower() == "true"

a = sorted(f for f in both if inv_rows[f]["category"] in ("Direct identifier", "Sensitive") and not ps_true(f))
print("\n(A) inventory Direct identifier or Sensitive, PS v6 is_personal=false:", len(a))
for f in a:
    print("  ", f, ps_fields[f]["object_name"], ps_fields[f]["field_name"], "|", inv_rows[f]["category"])
b = sorted(f for f in both if ps_true(f) and inv_rows[f]["personal"] == "No")
print("\n(B) PS v6 is_personal=true, inventory Personal data=No:", len(b))
for f in b:
    print("  ", f, ps_fields[f]["object_name"], ps_fields[f]["field_name"], "|", inv_rows[f]["category"])
c = sorted(f for f in both if inv_rows[f]["personal"] == "Yes" and not ps_true(f))
print("\n(C) inventory Personal data=Yes, PS v6 is_personal=false:", len(c))
print("    by category:", dict(collections.Counter(inv_rows[f]["category"] for f in c)))
u = sorted(f for f in ps_fields if ps_true(f) or (f in inv_rows and inv_rows[f]["personal"] == "Yes"))
print("\n(U) union (PS v6 true or inventory Yes):", len(u))
p = sorted(f for f in ps_fields if ps_true(f) or (f in inv_rows and inv_rows[f]["category"] in ("Direct identifier", "Sensitive")))
print("(P) PS v6 true or inventory Direct identifier/Sensitive:", len(p))

# Story v7 section 13 seed lengths
widths = {"name": 80, "definition": 400, "sor": 120, "cycle": 10, "expected": 20}
print("\nStory v7 section 13 seed lengths (name<=80, definition<=400, system_of_record<=120, refresh_cycle<=10, expected_by<=20):")
for ln in story.splitlines():
    m = re.match(r"^\| (DP\d\d) \|", ln)
    if m:
        c = [x.strip() for x in ln.strip().strip("|").split("|")]
        vals = dict(name=c[1], definition=c[2], sor=c[3], cycle=c[4], expected=c[5])
        over = [k for k in widths if len(vals[k]) > widths[k]]
        print("  ", c[0], {k: len(v) for k, v in vals.items()}, "OVER:" + ",".join(over) if over else "")

if len(sys.argv) > 4:
    with open(sys.argv[4], "w", encoding="utf-8") as fh:
        fh.write("# field_id of every sys_fields row seeded is_personal=true under ASM-E1001-14 (protective union)\n")
        fh.write("# source: PS v6 is_personal=true OR PDPA Inventory v4 Personal data=Yes; count %d\n" % len(u))
        for f in u:
            src_ = "PSv6+INVv4" if (ps_true(f) and f in inv_rows and inv_rows[f]["personal"] == "Yes") else ("PSv6" if ps_true(f) else "INVv4")
            fh.write("%s\t%s\t%s\t%s\n" % (f, ps_fields[f]["object_name"], ps_fields[f]["field_name"], src_))
