"""RWB-TE-011 round-4 remediation evidence (read only; no values printed).
Usage: python -I te011_round4_check.py <repo-root> <E1-001 is_personal_union_v4.tsv>
Prints: INSERT count and pattern scan of the Physical Schema v6 copy; statements that write sys_fields;
name ambiguity of the protective union; personal (object, field) pairs on dictionary/reference seed
tables; source_field keys; personal names used by today's log calls."""
import re, sys, os, collections
repo, tsv = sys.argv[1], sys.argv[2]
ps = open(os.path.join(repo, "infra/postgres/schema/03-recovery-physical-schema-v6.sql"), encoding="utf-8").read()

def split_values(v):
    out, cur, q, i = [], "", False, 0
    while i < len(v):
        c = v[i]
        if q:
            if c == "'" and i + 1 < len(v) and v[i + 1] == "'": cur += "'"; i += 2; continue
            if c == "'": q = False; i += 1; continue
            cur += c
        elif c == "'": q = True
        elif c == ",": out.append(cur.strip()); cur = ""
        else: cur += c
        i += 1
    out.append(cur.strip()); return out

lines = ps.splitlines()
ins = [l for l in lines if l.startswith("INSERT")]
per_table = collections.Counter(re.match(r"INSERT INTO (\S+)", l).group(1) for l in ins)
print("PS v6 copy: INSERT statements", len(ins), "| by table", dict(per_table))

# pattern scan (SPEC-TE011-009 shapes, any check digit, so a superset)
print("  pattern scan: 13-digit", len(re.findall(r"(?<!\d)\d{13}(?!\d)", ps)),
      "| dashed ID", len(re.findall(r"(?<!\d)\d-\d{4}-\d{5}-\d{2}-\d(?!\d)", ps)),
      "| Thai mobile", len(re.findall(r"(?<![\d+])(?:0[689]\d[- ]?\d{3}[- ]?\d{4}|\+?66[- ]?[689]\d[- ]?\d{3}[- ]?\d{4})(?!\d)", ps)),
      "| e-mail", len(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+", ps)))
# statements that write sys_fields (outside string literals)
def strip_literals_and_comments(t):
    """One quote-aware pass: blanks string literals, -- and /* */ comments; keeps statement ends."""
    out, i, n = [], 0, len(t)
    while i < n:
        if t.startswith("--", i):
            j = t.find("\n", i); i = n if j < 0 else j
        elif t.startswith("/*", i):
            j = t.find("*/", i + 2); i = n if j < 0 else j + 2; out.append(" ")
        elif t[i] == "'":
            j = i + 1
            while j < n:
                if t[j] == "'" and j + 1 < n and t[j + 1] == "'": j += 2; continue
                if t[j] == "'": break
                j += 1
            out.append("''"); i = j + 1
        else:
            out.append(t[i]); i += 1
    return "".join(out)
nostr = strip_literals_and_comments(ps)
stmts = [" ".join(x.split()) for x in nostr.split(";")]
ins_st = [x for x in stmts if x.startswith("INSERT")]
print("  INSERT statements (quote-aware split)", len(ins_st), "| multi-row VALUES:",
      [(re.match(r"INSERT INTO (\S+)", x).group(1), x.split("VALUES", 1)[1].count("(")) for x in ins_st if "VALUES" in x and re.search(r"\)\s*,\s*\(", x.split("VALUES", 1)[1])],
      "| INSERT ... SELECT:", sum(1 for x in ins_st if "VALUES" not in x))
writes = collections.Counter()
for st in nostr.split(";"):
    s = " ".join(st.split())
    if re.search(r"\bsys_fields\b", s):
        m = re.match(r"(INSERT INTO|UPDATE|DELETE FROM|TRUNCATE|COPY|MERGE INTO|ALTER TABLE|DROP TABLE|CREATE TABLE|COMMENT ON (?:TABLE|COLUMN)|CREATE (?:OR REPLACE )?VIEW|CREATE (?:UNIQUE )?INDEX)\s*(\S*)", s.lstrip("-\n "))
        writes[(m.group(1) if m else s[:30])] += 1
print("  statements naming sys_fields, by kind:", dict(writes))

F = {}
for l in ins:
    if l.startswith("INSERT INTO sys_fields"):
        cols = [c.strip() for c in l[l.index("(") + 1:l.index(")")].split(",")]
        d = dict(zip(cols, split_values(l[l.index("VALUES") + 6:].strip().rstrip(";").strip()[1:-1])))
        F[d["field_id"]] = d
U = {l.split("\t")[0] for l in open(tsv, encoding="utf-8") if not l.startswith("#")}
print("dictionary rows", len(F), "| PS v6 is_personal=true", sum(d["is_personal"] == "true" for d in F.values()), "| protective union", len(U))
byname = collections.defaultdict(lambda: [0, 0])
for fid, d in F.items(): byname[d["field_name"]][0 if fid in U else 1] += 1
pn = {n for n, (p, q) in byname.items() if p}
amb = {n for n in pn if byname[n][1]}
print("union: personal field names", len(pn), "| also non-personal on another object (ambiguous)", len(amb))
seed = [f for f, d in F.items() if d["is_personal"] == "true"]
print("  PS v6 18 marked names ambiguous:", sorted({F[f]["field_name"] for f in seed} & amb))
for n in ["field_name", "description", "source_system", "owner_role", "status", "comments"]:
    print("  name", n, "personal on", byname[n][0], "objects, not personal on", byname[n][1])
seedt = {"sys_fields", "sys_objects", "data_product", "lov_value", "role", "permission"}
print("personal (object, field) pairs on dictionary/reference seed tables:", sorted((F[f]["object_name"], F[f]["field_name"]) for f in U if F[f]["object_name"] in seedt))
sf = [F[f]["source_field"] for f in U if re.fullmatch(r"[a-z_]+\.[a-z0-9_]+\.[a-z0-9_]+", F[f]["source_field"] or "")]
print("union fields with source_field <schema>.<table>.<column>:", len(sf), "| differing column name example:",
      [(F[f]["object_name"] + "." + F[f]["field_name"], F[f]["source_field"]) for f in seed if F[f]["source_field"].endswith(".surname")])
# today's log calls: identifiers used vs union names
def snake(s): return re.sub(r"(?<!^)([A-Z])", r"_\1", s).lower()
src = os.path.join(repo, "backend/src/main/java")
for dp, _, fn in os.walk(src):
    for f in fn:
        for i, l in enumerate(open(os.path.join(dp, f), encoding="utf-8"), 1):
            if re.search(r"\b(log|logger|LOG|LOGGER)\.(trace|debug|info|warn|error)\(|System\.(out|err)\.", l):
                args = re.sub(r'"[^"]*"', "", l.split("(", 1)[1])
                ids = {snake(re.sub(r"^get", "", t)) for t in re.findall(r"[A-Za-z_]\w*", args)}
                print("log call", os.path.relpath(os.path.join(dp, f), repo).replace("\\", "/") + ":" + str(i), "| personal names used:", sorted(ids & pn))
