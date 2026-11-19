"""Count tables, columns, sys_objects and sys_fields seed rows in Physical Schema v6.
Usage: python -I count_v6.py <path-to-sql>"""
import re, sys, collections, json

src = open(sys.argv[1], encoding="utf-8").read()
lines = src.splitlines()

STD = {"is_active", "state", "version", "created_at", "created_by", "updated_at", "updated_by"}

# 1. Tables and columns from CREATE TABLE blocks
tables = collections.OrderedDict()
for m in re.finditer(r"^CREATE TABLE (\w+) \((.*?)^\);", src, re.S | re.M):
    name, body = m.group(1), m.group(2)
    cols = []
    for ln in body.splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("CONSTRAINT") or ln.startswith("--"):
            continue
        cm = re.match(r"(\w+)\s+([a-z]+(?:\s+precision)?(?:\(\d+(?:,\d+)?\))?(?:\[\])?)", ln)
        if cm:
            cols.append((cm.group(1), cm.group(2)))
    tables[name] = cols

# 2. Seed rows
def parse_values(stmt):
    # split VALUES (...) into tokens honoring quotes
    v = stmt[stmt.index("VALUES") + 6:].strip().rstrip(";").strip()
    assert v.startswith("(") and v.endswith(")"), v[:80]
    v = v[1:-1]
    out, cur, q, i = [], "", False, 0
    while i < len(v):
        c = v[i]
        if q:
            if c == "'" and i + 1 < len(v) and v[i + 1] == "'":
                cur += "'"; i += 2; continue
            if c == "'":
                q = False; i += 1; continue
            cur += c
        else:
            if c == "'":
                q = True
            elif c == ",":
                out.append(cur.strip()); cur = ""
            else:
                cur += c
        i += 1
    out.append(cur.strip())
    return out

objs, fields = [], []
for ln in lines:
    if ln.startswith("INSERT INTO sys_objects"):
        cols = [c.strip() for c in ln[ln.index("(") + 1:ln.index(")")].split(",")]
        objs.append(dict(zip(cols, parse_values(ln))))
    elif ln.startswith("INSERT INTO sys_fields"):
        cols = [c.strip() for c in ln[ln.index("(") + 1:ln.index(")")].split(",")]
        fields.append(dict(zip(cols, parse_values(ln))))

views = re.findall(r"^CREATE OR REPLACE VIEW recovery\.(v_ace_\w+)", src, re.M)

obj_names = [o["object_name"] for o in objs]
dup_objs = [k for k, n in collections.Counter(obj_names).items() if n > 1]
fid = [f["field_id"] for f in fields]
dup_fids = [k for k, n in collections.Counter(fid).items() if n > 1]
dup_obj_field = [k for k, n in collections.Counter((f["object_name"], f["field_name"]) for f in fields).items() if n > 1]

print("CREATE TABLE count:", len(tables))
total_cols = sum(len(c) for c in tables.values())
bus_cols = sum(len([x for x in c if x[0] not in STD]) for c in tables.values())
print("columns total:", total_cols, " excluding 7 standard columns:", bus_cols)
print("v_ace_* views:", len(views), len(set(views)))
print("sys_objects INSERT rows:", len(objs), " distinct object_name:", len(set(obj_names)), " duplicates:", dup_objs)
print("sys_fields INSERT rows:", len(fields), " distinct field_id:", len(set(fid)), " duplicate field_id:", dup_fids[:20], len(dup_fids))
print("duplicate (object,field) pairs:", dup_obj_field[:20], len(dup_obj_field))

# object classification
tbl_set, view_set = set(tables), set(views)
obj_set = set(obj_names)
print("objects that are tables:", len(obj_set & tbl_set), " views:", len(obj_set & view_set),
      " neither:", sorted(obj_set - tbl_set - view_set))
print("tables with no sys_objects row:", sorted(tbl_set - obj_set))
print("views with no sys_objects row:", sorted(view_set - obj_set))

# product vs no product
nullp = [o for o in objs if o.get("data_product") in ("NULL", "", None)]
print("objects with NULL data_product:", len(nullp), collections.Counter(o["subject_area"] for o in nullp))
print("objects per subject_area:", dict(collections.Counter(o["subject_area"] for o in objs)))
print("objects per data_product:", dict(sorted(collections.Counter(o["data_product"] for o in objs).items())))

# fields per table vs columns (excluding standard)
fields_by_obj = collections.defaultdict(list)
for f in fields:
    fields_by_obj[f["object_name"]].append(f)
tf = sum(len(fields_by_obj[t]) for t in tables)
vf = sum(len(fields_by_obj[v]) for v in views)
print("sys_fields rows on tables:", tf, " on v_ace views:", vf, " on other objects:",
      len(fields) - tf - vf)

mism = []
for t, cols in tables.items():
    colmap = {c: ty for c, ty in cols if c not in STD}
    fmap = {f["field_name"]: f["physical_type"] for f in fields_by_obj[t]}
    for c in colmap:
        if c not in fmap:
            mism.append((t, c, "column without field"))
        elif fmap[c].lower() != colmap[c].lower():
            mism.append((t, c, f"type {colmap[c]} vs field {fmap[c]}"))
    for c in fmap:
        if c not in colmap:
            mism.append((t, c, "field without column"))
print("column/field mismatches (tables):", len(mism))
for m in mism[:60]:
    print("  ", m)

if len(sys.argv) > 2:
    for t in sys.argv[2:]:
        print(t, [c for c, _ in tables.get(t, [])], len(fields_by_obj[t]))
