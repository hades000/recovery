"""RWB-TE-011 round-5 remediation evidence (read only; prints names and counts, never values).
Usage: python -I te011_round5_check.py <repo-root> <E1-001 is_personal_union_v4.tsv>
Prints: described objects (SG5-01); API schemas whose properties share a name with a personal field or an
x-personal-data property, and whether the schema is described (SG5-01, DG5-01); ACE schema copy tables
and (table, column) pairs that only the unambiguous-name rule reaches (SG5-01); SQL files, column-less
INSERTs and COPY blocks in the scan roots (SG5-03); fixture positions in today's test roots that carry an
unambiguous personal name with a non-SYN- literal (zero-finding baseline, states 1 and 2); INSERT
statements of the PS v6 copy by table (SG5-04)."""
import re, sys, os, collections, yaml
repo, tsv = sys.argv[1], sys.argv[2]
P = lambda *a: os.path.join(repo, *a)
ps = open(P("infra/postgres/schema/03-recovery-physical-schema-v6.sql"), encoding="utf-8").read()

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

F = {}
for l in ps.splitlines():
    if l.startswith("INSERT INTO sys_fields"):
        cols = [c.strip() for c in l[l.index("(") + 1:l.index(")")].split(",")]
        d = dict(zip(cols, split_values(l[l.index("VALUES") + 6:].strip().rstrip(";").strip()[1:-1])))
        F[d["field_id"]] = d
U = {l.split("\t")[0] for l in open(tsv, encoding="utf-8") if not l.startswith("#")}
PS6 = {f for f, d in F.items() if d["is_personal"] == "true"}

def snake(s): return re.sub(r"(?<!^)([A-Z])", r"_\1", s).lower()

api = yaml.safe_load(open(P("api/recovery-api-v4.yaml"), encoding="utf-8"))["components"]["schemas"]
api_props = {s: (v.get("properties") or {}) for s, v in api.items() if isinstance(v, dict)}
api_marked = {(snake(s), snake(p)) for s, pr in api_props.items() for p, pv in pr.items()
              if isinstance(pv, dict) and pv.get("x-personal-data") is True}
api_marked_names = {f for _, f in api_marked}
print("API v4: schemas", len(api_props), "| x-personal-data properties", sorted(api_marked))

for label, M in (("PS v6 (state 1)", PS6), ("protective union (state 2)", U)):
    keys = {(F[f]["object_name"], F[f]["field_name"]) for f in M} | api_marked
    for f in M:
        m = re.fullmatch(r"[a-z_]+\.([a-z0-9_]+)\.([a-z0-9_]+)", F[f]["source_field"] or "")
        if m: keys.add((m.group(1), m.group(2)))
    described = ({d["object_name"] for d in F.values()}
                 | {re.fullmatch(r"[a-z_]+\.([a-z0-9_]+)\.[a-z0-9_]+", d["source_field"]).group(1)
                    for d in F.values() if re.fullmatch(r"[a-z_]+\.[a-z0-9_]+\.[a-z0-9_]+", d["source_field"] or "")}
                 | {o for o, _ in api_marked})
    byname = collections.defaultdict(lambda: [0, 0])
    for fid, d in F.items(): byname[d["field_name"]][0 if fid in M else 1] += 1
    pn = {n for n, (p, q) in byname.items() if p} | api_marked_names
    unamb = {n for n in pn if not byname[n][1]}
    print("\n==", label, "| keys", len(keys), "| described objects", len(described),
          "| personal names", len(pn), "| unambiguous", len(unamb))
    print("  six seed tables described:", all(t in described for t in
          ["sys_fields", "sys_objects", "data_product", "lov_value", "role", "permission"]))
    # API schemas: properties whose snake name is a personal name
    rows = []
    for s, pr in sorted(api_props.items()):
        for p, pv in pr.items():
            n = snake(p)
            if n in pn:
                marked = isinstance(pv, dict) and pv.get("x-personal-data") is True
                rows.append((s, p, "marked" if marked else "unmarked",
                             "described" if snake(s) in described else "undescribed",
                             "key" if (snake(s), n) in keys else "no key",
                             "unambiguous" if n in unamb else "ambiguous",
                             "x-personal-data name" if n in api_marked_names else ""))
    esc = [r for r in rows if r[3] == "described" and r[4] == "no key"]
    print("  API properties with a personal name:", len(rows),
          "| on undescribed schemas (now reached by the name rule):", sum(r[3] == "undescribed" for r in rows),
          "| on described schemas with no key (stay non-findings):", len(esc))
    for r in rows:
        if r[6] or label.startswith("PS"): print("   ", *r)
    # ACE schema copy
    ace = open(P("infra/postgres/schema/01-ace-schema-v1.sql"), encoding="utf-8").read()
    tabs = {}
    for m in re.finditer(r"CREATE TABLE\s+(?:public\.)?(\w+)\s*\((.*?)\n\);", ace, re.S):
        tabs[m.group(1)] = [c.split()[0].strip('"') for c in m.group(2).split("\n")
                            if c.strip() and not re.match(r"\s*(CONSTRAINT|PRIMARY|UNIQUE|FOREIGN|CHECK|--)", c)]
    und = [t for t in tabs if t not in described]
    pairs = sorted((t, c) for t in und for c in tabs[t] if c in unamb)
    amb_pairs = sorted((t, c) for t in und for c in tabs[t] if c in pn and c not in unamb)
    print("  ACE schema copy: tables", len(tabs), "| undescribed", len(und),
          "| undescribed (table, column) pairs with an unambiguous personal name (finding under SG5-01 fix):",
          len(pairs), pairs, "| with an ambiguous personal name (notice):", len(amb_pairs))
    for n in ("summary", "file_name", "address", "first_name"):
        print("  name", n, "personal on", byname[n][0], "rows, non-personal on", byname[n][1],
              "->", "unambiguous" if n in unamb else ("ambiguous" if n in pn else "not personal"))

    # today's test roots: fixture positions with an unambiguous personal name and a non-SYN- literal
    roots = ["backend/src/test", "frontend/e2e", "frontend/src/test", "frontend/src/modules/recovery/__tests__",
             "infra"]
    hits, nfiles = [], 0
    variants = {}
    for n in unamb:
        camel = re.sub(r"_([a-z0-9])", lambda m: m.group(1).upper(), n)
        for v in (n, camel): variants[v] = n
    pat = re.compile(r"""(?:\b(set)([A-Z]\w*)\s*\(\s*["'`]|\.(\w+)\s*\(\s*["'`]|["']?(\w+)["']?\s*:\s*["'`]|\b(\w+)\s*=\s*["'`])(?!SYN-)""")
    for r in roots:
        for dp, dn, fn in os.walk(P(r)):
            dn[:] = [d for d in dn if d not in ("node_modules", "build", "dist", "coverage")]
            if os.path.relpath(dp, repo).replace("\\", "/").startswith("infra/postgres/schema"): continue
            for f in fn:
                if not re.search(r"\.(java|ts|tsx|json|sql|js|yaml|yml)$", f) and not f.endswith(".test.tsx"):
                    if not (dp.replace("\\", "/").endswith("frontend/src") and ".test." in f): continue
                nfiles += 1
                for i, l in enumerate(open(os.path.join(dp, f), encoding="utf-8", errors="replace"), 1):
                    for m in pat.finditer(l):
                        name = (m.group(2) and m.group(2)[0].lower() + m.group(2)[1:]) or m.group(3) or m.group(4) or m.group(5)
                        if name in variants:
                            hits.append((os.path.relpath(os.path.join(dp, f), repo).replace("\\", "/") + ":" + str(i), variants[name]))
    print("  test roots: files", nfiles, "| positions with an unambiguous personal name and a non-SYN- literal:", hits)

# SG5-03: SQL files, column-less INSERT and COPY in scan roots (migrations, tests, infra except schema copies)
sqlf, colless, copy = [], [], []
for r in ["backend/src/main/resources/db/modulemigration/recovery", "backend/src/test", "frontend", "infra"]:
    for dp, dn, fn in os.walk(P(r)):
        dn[:] = [d for d in dn if d not in ("node_modules", "build", "dist", "coverage")]
        if os.path.relpath(dp, repo).replace("\\", "/").startswith("infra/postgres/schema"): continue
        for f in fn:
            if f.endswith(".sql"):
                p = os.path.join(dp, f); sqlf.append(os.path.relpath(p, repo).replace("\\", "/"))
                t = open(p, encoding="utf-8").read()
                colless += re.findall(r"(?i)\bINSERT\s+INTO\s+[\w.\"${}]+\s+(?:VALUES|SELECT)\b", t)
                copy += re.findall(r"(?im)^\s*(?:COPY|\\copy)\s+[\w.\"${}]+.*\bFROM\b", t)
print("\nscan roots: .sql files", sqlf, "| column-less INSERT", len(colless), "| COPY/\\copy FROM", len(copy))
ins = collections.Counter(re.match(r"INSERT INTO (\S+)", l).group(1) for l in ps.splitlines() if l.startswith("INSERT"))
print("PS v6 copy INSERT statements by table:", dict(ins), "| total", sum(ins.values()))
print("PS v6 copy: column-less INSERT", len(re.findall(r"(?m)^INSERT INTO \S+ (?:VALUES|SELECT)", ps)),
      "| COPY", len(re.findall(r"(?im)^\s*COPY\s", ps)),
      "| foreign keys referencing sys_fields", len(re.findall(r"REFERENCES\s+(?:\w+\.)?sys_fields\b", ps)))

# Per-pair description (SG5-01 rule as specified): a position is resolved only when the dictionary
# describes that field on that object (a sys_fields row, a source_field column, or an x-personal-data
# property). Check the seed tables of the PS v6 copy and the API properties on described schemas.
dpairs = {(d["object_name"], d["field_name"]) for d in F.values()} | api_marked
for d in F.values():
    m = re.fullmatch(r"[a-z_]+\.([a-z0-9_]+)\.([a-z0-9_]+)", d["source_field"] or "")
    if m: dpairs.add((m.group(1), m.group(2)))
for label, M in (("PS v6 (state 1)", PS6), ("protective union (state 2)", U)):
    byname = collections.defaultdict(lambda: [0, 0])
    for fid, d in F.items(): byname[d["field_name"]][0 if fid in M else 1] += 1
    pn = {n for n, (p, q) in byname.items() if p} | api_marked_names
    unamb = {n for n in pn if not byname[n][1]}
    cols = collections.defaultdict(set)
    for l in ps.splitlines():
        m = re.match(r"INSERT INTO (\S+)\s*\(([^)]*)\)", l)
        if m: cols[m.group(1)].update(c.strip() for c in m.group(2).split(","))
    und = sorted((t, c) for t, cs in cols.items() for c in cs if (t, c) not in dpairs)
    print("\n==", label, "| PS v6 seed INSERT columns not described on their table:", len(und),
          "| of which unambiguous personal names (would be findings):", [p for p in und if p[1] in unamb],
          "| ambiguous personal names (notices):", [p for p in und if p[1] in pn and p[1] not in unamb])
    rows = [(s, p) for s, pr in api_props.items() for p in pr if snake(p) in pn]
    desc_obj = {o for o, _ in dpairs}
    nk = [(s, p) for s, p in rows if snake(s) in desc_obj and (snake(s), snake(p)) not in dpairs]
    print("  API properties with a personal name on a described schema but no dictionary row for that pair:",
          len(nk), "| unambiguous:", sum(snake(p) in unamb for s, p in nk))
