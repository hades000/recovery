# Build Recovery Workbench Entity Relationship Diagram v4
# Reads Physical Schema v5.sql, LDM v7.xlsx, CDM v6.xlsx, the ACE view SQL and the v3 page style.
import html
import os
import re
import collections
import openpyxl

ROOT = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
SQL = os.path.join(ROOT, r"06 Data\Recovery Workbench Physical Schema v5.sql")
VIEWSQL = os.path.join(ROOT, r"15 ACE DB Alignment\Recovery Workbench ACE Source Views v1.sql")
LDM = os.path.join(ROOT, r"06 Data\Recovery Workbench Logical Data Model and Data Dictionary v7.xlsx")
CDM = os.path.join(ROOT, r"06 Data\Recovery Workbench Conceptual Data Model v6.xlsx")
V3 = os.path.join(ROOT, r"06 Data\Recovery Workbench Entity Relationship Diagram v3.html")
OUT = os.path.join(ROOT, r"06 Data\Recovery Workbench Entity Relationship Diagram v4.html")

E = html.escape

# ---------- schema v5 tables ----------
sql = open(SQL, encoding="utf-8").read()
tables = collections.OrderedDict()
for m in re.finditer(r"CREATE TABLE (\w+) \((.*?)\n\);", sql, flags=re.S):
    name, body = m.group(1), m.group(2)
    cols, pk, uks = [], [], []
    for ln in body.split("\n"):
        ln = ln.strip().rstrip(",")
        if not ln or ln.startswith("--"):
            continue
        cm = re.match(r"CONSTRAINT \w+ UNIQUE \(([^)]*)\)", ln)
        if cm:
            uks.append([c.strip() for c in cm.group(1).split(",")])
            continue
        cm = re.match(r"(?:CONSTRAINT \w+ )?PRIMARY KEY \(([^)]*)\)", ln)
        if cm:
            pk = [c.strip() for c in cm.group(1).split(",")]
            continue
        if ln.startswith("CONSTRAINT"):
            continue
        cm = re.match(r"(\w+) (.+)$", ln)
        rest = cm.group(2)
        cols.append(cm.group(1))
        if "PRIMARY KEY" in rest:
            pk = [cm.group(1)]
    tables[name] = {"cols": cols, "pk": pk, "uks": uks}
assert len(tables) == 92, len(tables)

# ---------- views ----------
vsql = open(VIEWSQL, encoding="utf-8").read()
secB = vsql.index("-- Section B")
views = collections.OrderedDict()
for m in re.finditer(r"CREATE OR REPLACE VIEW recovery\.(v_ace_\w+)\s*\nAS\n(.*?);\n", vsql, flags=re.S):
    body = m.group(2)
    src = []
    for t in re.findall(r"public\.(\w+)", body):
        if t not in src:
            src.append(t)
    views[m.group(1)] = {"tier": 1 if m.start() < secB else 2, "ace": src,
                         "fields": re.findall(r"AS\s+(\w+)\s*(?:,|\n)", body)}
assert len(views) == 30, len(views)

# ---------- LDM ----------
wb = openpyxl.load_workbook(LDM, read_only=True, data_only=True)
ent_rows = [r for r in list(wb["Entities"].iter_rows(values_only=True))[4:] if r[0]]
ldm_ent = collections.OrderedDict()
for r in ent_rows:
    ldm_ent[r[0]] = {"biz": r[1], "dp": r[3], "what": r[4], "sor": r[5], "ace": r[6], "n": r[7]}
fld_rows = [r for r in list(wb["Fields"].iter_rows(values_only=True))[4:] if r[1]]
ldm_fields = collections.defaultdict(list)
for r in fld_rows:
    ldm_fields[r[1]].append({"name": r[2], "key": r[9], "ref": r[10], "personal": r[13]})
assert len(ent_rows) == 122, len(ent_rows)
assert len(fld_rows) == 1366, len(fld_rows)

# ---------- CDM ----------
wc = openpyxl.load_workbook(CDM, read_only=True, data_only=True)
dp_rows = [r for r in list(wc["Data products"].iter_rows(values_only=True))[3:]
           if r[0] and str(r[0]).startswith("DP")]
dps = collections.OrderedDict()
for r in dp_rows:
    dps[r[0]] = {"name": r[1], "what": r[2], "sor": r[3], "how": r[4], "fresh": r[5]}
cent = [r for r in list(wc["Entities"].iter_rows(values_only=True))[4:] if r[0]]
cdm_view = {r[0]: {"subject": r[1], "dp": r[2].split(" ")[0], "what": r[3], "sor": r[4], "n": r[6]}
            for r in cent if str(r[0]).startswith("v_ace_")}
assert len(cdm_view) == 30
dps["OPS"] = {"name": "Loads and operations",
              "what": "The freshness stamp, reconciliation, outbound interfaces, jobs, feature flags, the outbox and idempotency records that run the Workbench. No inbound load: the ACE batch record is read through v_ace_batch_status",
              "sor": "Recovery Workbench; ACE for the batch record",
              "how": "Held in the Workbench; the ACE batch business date is read through recovery.v_ace_batch_status",
              "fresh": "As it changes; batch status at each ACE batch"}
dps["AGT"] = {"name": "Agent runtime",
              "what": "Agent policies, prompts, runs, labeled samples, evaluations, feedback and alerts",
              "sor": "Recovery Workbench", "how": "Held in the Workbench", "fresh": "As it changes"}
dps["RPT"] = {"name": "Reporting",
              "what": "Measure definitions and the snapshots published to Power BI",
              "sor": "Recovery Workbench", "how": "Held in the Workbench", "fresh": "Daily"}

# ---------- relationships ----------
rel_rows = [r for r in list(wb["Relationships"].iter_rows(values_only=True))[4:] if r[0]]
rels = []
for r in rel_rows:
    child, col, parent, card, mand, note = r
    logical = bool(note and "business key" in note)
    rels.append({"child": child, "col": col, "parent": parent, "mand": mand == "Yes",
                 "logical": logical, "card": card,
                 "kind": "Business key, no foreign key" if logical else "Foreign key"})
ext_map = {"Party extension": "party_ext", "Contact point extension": "contact_point_ext",
           "Account extension": "account_ext", "Valuation extension": "valuation_ext"}
crel = [r for r in list(wc["Relationships"].iter_rows(values_only=True))[4:] if r[0]]
for r in crel:
    if r[0] in ext_map:
        child = ext_map[r[0]]
        card = {"Many to one": "N:1", "Many to zero or one": "N:0..1", "One to one": "1:1"}.get(r[2], r[2])
        rels.append({"child": child, "col": "person_key" if child == "party_ext" else
                     "contact_key" if child == "contact_point_ext" else
                     "account_key" if child == "account_ext" else "valuation_key",
                     "parent": r[1], "mand": True, "logical": True, "card": card,
                     "kind": "Business key, no foreign key (1:1 extension)"})
assert len(rels) == 104, len(rels)

# ---------- entity records ----------
entities = collections.OrderedDict()
for name, t in tables.items():
    e = ldm_ent[name]
    uks = {}
    for i, u in enumerate(t["uks"]):
        for c in u:
            uks.setdefault(c, "AK%d" % (i + 1))
    fields = []
    for c in t["cols"]:
        fields.append({"name": c, "pk": c in t["pk"], "ak": uks.get(c),
                       "fk": any(r["child"] == name and r["col"] == c and not r["logical"] for r in rels),
                       "bk": any(r["child"] == name and r["col"] == c and r["logical"] for r in rels)})
    kind = "ext" if name.endswith("_ext") else "table"
    entities[name] = {"kind": kind, "dp": e["dp"], "biz": e["biz"], "what": e["what"],
                      "fields": fields, "n": len(fields)}
SECTION_B_COLS = {
    "v_ace_account": ["business_unit", "principal_outstanding", "interest_outstanding",
                      "fees_outstanding", "daily_bucket", "settlement_booked_date",
                      "settlement_booked_amount"],
    "v_ace_customer": ["party_type", "id_type", "segment"],
    "v_ace_efs_action": ["contact_result", "action_contact_status"],
}
for vname, v in views.items():
    c = cdm_view[vname]
    fields = []
    for f in ldm_fields[vname]:
        fields.append({"name": f["name"], "pk": False, "ak": None, "fk": False,
                       "bk": f["name"] in ("account_key", "person_key", "contact_key",
                                           "asset_key", "payment_code", "valuation_key")})
    for col in SECTION_B_COLS.get(vname, []):
        fields.append({"name": col, "pk": False, "ak": None, "fk": False, "bk": False, "sb": True})
    entities[vname] = {"kind": "view", "dp": c["dp"], "biz": vname, "what": c["what"],
                       "fields": fields, "n": len(fields), "tier": v["tier"], "ace": v["ace"]}
assert len(entities) == 122

n_tab = sum(1 for e in entities.values() if e["kind"] == "table")
n_ext = sum(1 for e in entities.values() if e["kind"] == "ext")
n_view = sum(1 for e in entities.values() if e["kind"] == "view")
assert (n_tab, n_ext, n_view) == (88, 4, 30)

order = [r[0] for r in ent_rows if not str(r[0]).startswith("v_ace_")] + list(views)
tabs = ["DP01", "DP02", "DP03", "DP04", "DP05", "DP06", "DP07", "DP08", "DP09",
        "DP10", "DP11", "DP12", "DP13", "DP14", "OPS", "AGT", "RPT"]
by_dp = collections.OrderedDict((d, []) for d in tabs)
for name in order:
    by_dp[entities[name]["dp"]].append(name)


def dp_of(name):
    return entities[name]["dp"]


def prod_card(entity):
    cls = "ent " + ("view" if entity["kind"] == "view" else "ext" if entity["kind"] == "ext" else "table")
    if entity["kind"] == "view":
        tag = "ACE view, read only - Tier %d" % entity["tier"]
    elif entity["kind"] == "ext":
        tag = "Workbench extension, 1:1 by business key"
    else:
        tag = "Workbench table"
    rows = []
    for f in entity["fields"]:
        marks = []
        if f["pk"]:
            marks.append("PK")
        if f["ak"]:
            marks.append(f["ak"])
        if f["fk"]:
            marks.append("FK")
        if f["bk"]:
            marks.append("BK")
        if f.get("sb"):
            marks.append("B")
        rows.append('<tr><td class="code">%s</td><td class="key">%s</td></tr>' % (E(f["name"]), E(", ".join(marks))))
    return ('<div class="%s"><header><b class="code">%s</b><span class="tag">%s</span></header>'
            '<table><tbody>%s</tbody></table></div>' % (cls, E(entity["biz"]), E(tag), "".join(rows)))


# ---------- product references ----------
pairs = collections.OrderedDict()
internal = 0
for r in rels:
    a, b = dp_of(r["child"]), dp_of(r["parent"])
    if a == b:
        internal += 1
        continue
    k = tuple(sorted((a, b)))
    d = pairs.setdefault(k, {"n": 0, "mand": 0, "logical": 0})
    d["n"] += 1
    d["mand"] += 1 if r["mand"] else 0
    d["logical"] += 1 if r["logical"] else 0

# ---------- style, from v3 ----------
v3 = open(V3, encoding="utf-8").read()
style = re.search(r"<style>(.*?)</style>", v3, flags=re.S).group(1)
extra = """
.ent{border:1px solid var(--rule);background:var(--surface);margin:0}
.ent>header{display:block;padding:7px 10px;background:var(--pale);border-bottom:1px solid var(--rule)}
.ent>header b{color:var(--title);font-size:14px}
.ent table{min-width:0;font-size:12px;width:100%}
.ent td{padding:3px 10px;border-bottom:1px solid var(--rule)}
.ent tr:last-child td{border-bottom:0}
.ent.view{border-style:dashed;border-color:#8A76AD;background:var(--pale)}
.ent.view>header{background:transparent}
.ent.ext{border-left:4px solid var(--orange)}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:12px;margin:8px 0 16px}
.tag{display:block;font-size:10px;letter-spacing:.03em;text-transform:uppercase;color:var(--muted);margin-top:2px}
.key{color:var(--title);font-weight:700;font-size:11px;white-space:nowrap;width:64px}
.badgeview{border:2px dashed #8A76AD;background:var(--pale);padding:8px 10px;margin:6px 0}
.badgeview b{color:var(--title)}
@media print{
 :root{--bg:#FFFFFF;--ink:#1F1F1F;--muted:#595959;--title:#4E297F;--head:#DCD3EB;--pale:#EEEAF6;--rule:#C8C8C8;--surface:#FFFFFF}
 header{padding-top:10px}
 nav{display:none}
 section.tab{display:block!important;page-break-before:always}
 section.tab#overview{page-break-before:auto}
 .tw{max-height:none;overflow:visible}
 .cards{display:block}
 .ent{margin:0 0 10px;page-break-inside:auto}
 .filter{display:none}
 table{font-size:11px}
}
"""
style = style.replace("--surface:#FFFFFF}", "--surface:#FFFFFF;--ext:#FF9900}") + extra

# ---------- overview figure ----------
HW = 1020
HH = 512
sv = []
sv.append('<svg viewBox="0 0 %d %d" width="100%%" xmlns="http://www.w3.org/2000/svg" font-family="Aptos, Segoe UI, Arial" role="img" aria-label="The ACE boundary: ACE tables and additions, 30 read-only views, the recovery schema">' % (HW, HH))
sv.append('<rect width="%d" height="%d" fill="var(--surface)"/>' % (HW, HH))
sv.append('<defs><marker id="a" markerWidth="9" markerHeight="9" refX="7" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="#604A7B"/></marker></defs>')


def wrap(text, width):
    out, line = [], ""
    for word in text.split():
        if not line:
            line = word
        elif len(line) + 1 + len(word) <= width:
            line += " " + word
        else:
            out.append(line)
            line = word
    if line:
        out.append(line)
    return out


def panel(x, y, w, h, title, blocks, fill="#FFFFFF", stroke="#604A7B", dash=None):
    d = ' stroke-dasharray="6,4"' if dash else ""
    sv.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s" stroke="%s"%s/>' % (x, y, w, h, fill, stroke, d))
    sv.append('<text x="%d" y="%d" font-size="12.5" font-weight="bold" fill="#4E297F">%s</text>' % (x + 10, y + 19, E(title)))
    yy = y + 38
    for kind, text in blocks:
        if kind == "gap":
            yy += 6
            continue
        if kind == "h":
            sv.append('<text x="%d" y="%d" font-size="11" font-weight="bold" fill="#1F1F1F">%s</text>' % (x + 10, yy, E(text)))
            yy += 15
            continue
        for ln in wrap(text, 46):
            sv.append('<text x="%d" y="%d" font-size="10.5" fill="#1F1F1F">%s</text>' % (x + 10, yy, E(ln)))
            yy += 14.2


sv.append('<text x="8" y="18" font-size="11" fill="#595959">ACE holds the data, the Workbench holds the case, and a read-only view joins them.</text>')
panel(8, 30, 300, 446, "ACE database (ACE team)", [
    ("p", "Owned by ACE. The Workbench never writes here and never holds a copy."),
    ("gap", ""),
    ("h", "Tier 1 - in ACE today (22 tables)"),
    ("p", "account, payment, customer, phone, email, address, ca_relation, aa_relation, collateral, asset, efs_action, efs_action_code, efs_assignment, bucket_log_snapshot, product, branch, bot_holiday, ace_case, cfsc_mg_ssme_tdr_case, tdr_calculation, ai_recommended_plan, iam_user"),
    ("gap", ""),
    ("h", "Tier 2 - RWB-ACE-001 (14 tables)"),
    ("p", "ace_batch_run, valuation, collateral_detail, npa_asset, npa_sale, lawsuit, hearing, pod_receipt, gl_write_off, collins_score, party_product, credit_decision, esign_request, iam_group"),
    ("gap", ""),
    ("h", "12 new columns"),
    ("p", "account 7, customer 3, efs_action 2, exposed by CREATE OR REPLACE in V0003."),
], fill="#EEEAF6")

panel(336, 30, 306, 446, "recovery.v_ace_* (30 views)", [
    ("p", "Read only. One view per ACE object family. Owned by ace_view_owner."),
    ("gap", ""),
    ("h", "Section A - 16 views (V0002)"),
    ("p", "v_ace_account, v_ace_payment, v_ace_customer, v_ace_contact, v_ace_ca_relation, v_ace_aa_relation, v_ace_collateral, v_ace_asset, v_ace_efs_action, v_ace_efs_action_code, v_ace_efs_assignment, v_ace_bucket_log, v_ace_product, v_ace_branch, v_ace_holiday, v_ace_plan"),
    ("gap", ""),
    ("h", "Section B - 14 views (V0003)"),
    ("p", "v_ace_batch_status, v_ace_valuation, v_ace_collateral_detail, v_ace_npa_asset, v_ace_npa_sale, v_ace_lawsuit, v_ace_hearing, v_ace_pod, v_ace_write_off, v_ace_score, v_ace_party_product, v_ace_credit_decision, v_ace_esign, v_ace_iam_group"),
], stroke="#8A76AD", dash="6,4")

panel(672, 30, 340, 446, "Recovery schema (Workbench)", [
    ("h", "Tier 3 - 4 extension tables, 1:1"),
    ("p", "party_ext, contact_point_ext, account_ext, valuation_ext. Keyed by the ACE business key; no copy of ACE data."),
    ("gap", ""),
    ("h", "Tier 4 - 88 Workbench tables"),
    ("p", "Case, workflow, treatment, legal, partner, debt sale, documents, decision log, reference, outbox, flags and agents."),
    ("gap", ""),
    ("h", "Links into ACE"),
    ("p", "account_key, person_key, asset_key, payment_code, contact_key, valuation_key."),
    ("gap", ""),
    ("h", "No foreign key into ACE"),
    ("p", "ACE cascades deletes on account, and a cascade would delete case history."),
])

sv.append('<line x1="310" y1="250" x2="332" y2="250" stroke="#604A7B" stroke-width="2" marker-end="url(#a)"/>')
sv.append('<line x1="644" y1="250" x2="666" y2="250" stroke="#604A7B" stroke-width="2" marker-end="url(#a)"/>')
sv.append('<path d="M 980 479 C 980 490, 120 490, 120 479" fill="none" stroke="#C0392B" stroke-width="1.5" stroke-dasharray="4,3"/>')
sv.append('<text x="550" y="507" font-size="10.5" fill="#C0392B" text-anchor="middle">no write, and no foreign key into ACE</text>')
sv.append('<text x="316" y="240" font-size="9.5" fill="#595959" text-anchor="middle">SELECT</text>')
sv.append('<text x="650" y="240" font-size="9.5" fill="#595959" text-anchor="middle">SELECT</text>')
sv.append('</svg>')
overview_svg = "".join(sv)

# ---------- page ----------
nav = ['<button data-t="overview" aria-selected="false">Overview</button>']
for d in tabs:
    nav.append('<button data-t="%s" aria-selected="false">%s</button>' % (d.lower(), d))
nav.append('<button data-t="ace" aria-selected="false">ACE views</button>')
nav.append('<button data-t="all" aria-selected="false">Relationships</button>')
nav.append('<button data-t="notation" aria-selected="false">Notation</button>')

sections = []
# overview
grid = ('<div class="grid"><div class="box"><b>Objects</b>122</div>'
        '<div class="box"><b>Workbench tables</b>88</div>'
        '<div class="box"><b>Extension tables</b>4</div>'
        '<div class="box"><b>ACE views, read only</b>30</div>'
        '<div class="box"><b>References</b>104</div>'
        '<div class="box"><b>Business-key links</b>18</div></div>')
rows = []
for (a, b), d in sorted(pairs.items(), key=lambda kv: (-kv[1]["n"], kv[0])):
    rows.append('<tr><td class="code">%s</td><td class="code">%s</td><td class="num">%d</td><td class="num">%d</td><td class="num">%d</td></tr>'
                % (a, b, d["n"], d["mand"], d["logical"]))
pair_table = ('<div class="tw"><table><thead><tr><th>Data product</th><th>Refers to</th><th>References</th>'
              '<th>Mandatory</th><th>Business key</th></tr></thead><tbody>%s</tbody></table></div>' % "".join(rows))
prod_rows = []
for d in tabs:
    ents = by_dp[d]
    nt = sum(1 for x in ents if entities[x]["kind"] == "table")
    ne = sum(1 for x in ents if entities[x]["kind"] == "ext")
    nv = sum(1 for x in ents if entities[x]["kind"] == "view")
    prod_rows.append('<tr><td class="code">%s</td><td>%s</td><td class="num">%d</td><td class="num">%d</td>'
                     '<td class="num">%d</td><td class="num">%d</td><td>%s</td></tr>'
                     % (d, E(dps[d]["name"]), len(ents), nt, ne, nv, E(dps[d]["sor"])))
prod_table = ('<div class="tw"><table><thead><tr><th>ID</th><th>Data product</th><th>Objects</th><th>Tables</th>'
              '<th>Extension</th><th>Views</th><th>System of record</th></tr></thead><tbody>%s</tbody></table></div>'
              % "".join(prod_rows))
sections.append("""<section class="tab" id="overview"><h2>The ACE boundary and the references between data products</h2>
<p>122 objects: 88 Workbench tables, 4 extension tables and 30 ACE source views, with 104 references. The 14 data products hold 97 of them; OPS, AGT and RPT hold the other 25. The views are external and read only, and their boxes are dashed. The 18 business-key links carry no foreign key into ACE; the other 86 references are ordinary foreign keys inside the recovery schema.</p>
%s<div class="fig">%s</div>
<h3>Data products</h3>%s
<h3>References between data products</h3><p class="muted">%d references cross a data product boundary and %d stay inside one. Each row reads from the first data product to the second, and is ordered by count.</p>%s
</section>""" % (grid, overview_svg, prod_table, sum(d["n"] for d in pairs.values()), internal, pair_table))

# data product tabs
for d in tabs:
    ents = by_dp[d]
    cards = "".join(prod_card(entities[x]) for x in ents)
    r = [x for x in rels if dp_of(x["child"]) == d or dp_of(x["parent"]) == d]
    rrows = "".join('<tr><td class="code">%s</td><td class="code">%s</td><td class="code">%s</td><td>%s</td><td>%s</td></tr>'
                    % (E(x["child"]), E(x["col"]), E(x["parent"]),
                       E("Mandatory" if x["mand"] else "Optional"), E(x["kind"])) for x in r)
    rt = ('<div class="tw"><table><thead><tr><th>Entity</th><th>Field</th><th>Refers to</th><th>Reference</th>'
          '<th>Kind</th></tr></thead><tbody>%s</tbody></table></div>' % rrows) if r else "<p>No references.</p>"
    sections.append("""<section class="tab" id="%s"><h2>%s %s</h2><p>%s</p>
<div class="grid"><div class="box"><b>System of record</b>%s</div><div class="box"><b>How it reaches the Workbench</b>%s</div><div class="box"><b>Freshness</b>%s</div><div class="box"><b>Objects</b>%d</div></div>
<h3>Objects</h3><div class="cards">%s</div><h3>References</h3>%s</section>""" %
               (d.lower(), d, E(dps[d]["name"]), E(dps[d]["what"]), E(dps[d]["sor"]),
                E(dps[d]["how"]), E(dps[d]["fresh"]), len(ents), cards, rt))

# ACE views tab
vrows = "".join('<tr><td class="code">%s</td><td>%d</td><td class="code">%s</td><td class="code">%s</td><td>%s</td></tr>'
                % (E(v), views[v]["tier"], E(", ".join("public." + t for t in views[v]["ace"])),
                   E(cdm_view[v]["dp"]), E(cdm_view[v]["what"])) for v in views)
vcards = "".join(prod_card(entities[v]) for v in views)
sections.append("""<section class="tab" id="ace"><h2>The 30 ACE source views</h2>
<p>These are the only way the recovery module reads ACE. Each is a SELECT-only view over one ACE object family, owned by <span class="code">ace_view_owner</span>; the recovery service identity holds SELECT on the views and on nothing else in <span class="code">public</span>. They have no primary key and no foreign key, and the Workbench links to them by business key. Section A ships with RWB-E1-069; Section B ships the week RWB-ACE-001 lands.</p>
<div class="tw"><table><thead><tr><th>View</th><th>Tier</th><th>ACE objects read</th><th>Data product</th><th>What it gives the Workbench</th></tr></thead><tbody>%s</tbody></table></div>
<h3>View boxes</h3><p class="muted">Every view box is dashed: it is external to the recovery schema and read only. The fields are the view columns named for the Workbench, not the ACE column names. A field marked B is one of the 12 Tier 2 columns that V0003 adds to an existing view through CREATE OR REPLACE VIEW: seven on v_ace_account, three on v_ace_customer and two on v_ace_efs_action.</p>
<div class="cards">%s</div></section>""" % (vrows, vcards))

# relationships tab
allrows = "".join('<tr data-g="%s"><td class="code">%s</td><td class="code">%s</td><td class="code">%s</td><td>%s</td><td>%s</td><td class="code">%s</td></tr>'
                  % (dp_of(x["child"]), E(x["child"]), E(x["col"]), E(x["parent"]),
                     E(("Mandatory, " if x["mand"] else "Optional, ") + x["card"]), E(x["kind"]),
                     E(dp_of(x["child"]) + " to " + dp_of(x["parent"]))) for x in rels)
sections.append("""<section class="tab" id="all"><h2>All 104 references</h2>
<div class="filter"><input data-filter="allrels" placeholder="Filter by entity, field or data product"><select data-filtersel="allrels"><option value="">All data products</option>%s</select></div>
<div class="tw"><table id="allrels"><colgroup><col style="width:24%%"><col style="width:18%%"><col style="width:18%%"><col style="width:12%%"><col style="width:16%%"><col style="width:12%%"></colgroup><thead><tr><th>Entity</th><th>Field</th><th>Refers to</th><th>Reference</th><th>Kind</th><th>Data products</th></tr></thead><tbody>%s</tbody></table></div>
<p class="muted">18 references are business-key links with no foreign key. 14 of them replace a UUID foreign key into a source copy; 4 join an extension table to its ACE view. The remaining 86 are foreign keys inside the recovery schema.</p></section>"""
                % ("".join('<option value="%s">%s</option>' % (d, d) for d in tabs), allrows))

# notation
sections.append("""<section class="tab" id="notation"><h2>Notation and legend</h2><p>The page uses the IDEF1X key notation for entities and keys, and adds a notation for the ACE boundary.</p><div class="tw"><table><thead><tr><th>Symbol</th><th>Meaning</th></tr></thead><tbody>
<tr><td>Square-cornered box</td><td>A Workbench table. Its key does not depend on any other entity</td></tr>
<tr><td>Name above the box</td><td>The entity name as it is held in the physical schema</td></tr>
<tr><td>Line inside the box</td><td>Above the line is the primary key. Below it are the other attributes</td></tr>
<tr><td>(PK)</td><td>The primary key of the entity</td></tr>
<tr><td>(AK1)</td><td>An alternate key: unique on its own or together with the other AK1 attributes</td></tr>
<tr><td>(FK)</td><td>A foreign key inside the recovery schema</td></tr>
<tr><td>(BK)</td><td>A business key. The column holds an ACE business key and carries no foreign key</td></tr>
<tr><td>Dashed box with an ACE view name</td><td>An ACE source view. External to the recovery schema, read only, no primary key and no foreign key</td></tr>
<tr><td>Orange left edge</td><td>A Workbench extension table, 1:1 with an ACE record and keyed by its business key</td></tr>
<tr><td>Dashed grey box</td><td>An entity outside the recovery schema, shown with its key and its fields</td></tr>
<tr><td>Label on a reference</td><td>The kind: foreign key, business key, or business key on a 1:1 extension</td></tr>
</tbody></table></div>
<p class="muted">A view box lists the view columns as the Workbench names them. The ACE name appears only in the view definition and the STTM. A blue-purple view box is never written and never the parent of a foreign key.</p></section>""")

page = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Recovery Workbench Entity Relationship Diagram</title><style>%s</style></head><body>
<header><div class="in"><div class="lab">COLLECTIONS AND RECOVERY TRANSFORMATION</div><h1>Recovery Workbench Entity Relationship Diagram</h1><div class="meta">SCB Collections and Recovery. Henka Group, 15 November 2026. Version 4. 122 objects: 88 Workbench tables, 4 extension tables and 30 ACE views. D-RCV-35 and ADR-010.</div></div></header>
<nav><div class="in">%s</div></nav><main>%s</main><script>
const B=[...document.querySelectorAll('nav button')],S=[...document.querySelectorAll('section.tab')];
function show(id,deep){B.forEach(b=>b.setAttribute('aria-selected',b.dataset.t===id));S.forEach(s=>s.classList.toggle('on',s.id===id));
if(deep){try{history.replaceState(null,'','#'+id)}catch(e){}}}
B.forEach(b=>b.addEventListener('click',()=>{show(b.dataset.t,true);window.scrollTo(0,0)}));
const h=(location.hash||'').slice(1);show(S.some(s=>s.id===h)?h:S[0].id,false);window.scrollTo(0,0);
document.querySelectorAll('[data-filter]').forEach(inp=>{const t=document.getElementById(inp.dataset.filter);
const sel=document.querySelector('[data-filtersel="'+inp.dataset.filter+'"]');
function run(){const q=inp.value.toLowerCase(),v=sel?sel.value:'';
t.querySelectorAll('tbody tr').forEach(r=>{const tx=r.textContent.toLowerCase();
r.style.display=(!q||tx.includes(q))&&(!v||r.dataset.g===v)?'':'none'})}
inp.addEventListener('input',run);if(sel)sel.addEventListener('change',run)});
</script></body></html>""" % (style, "".join(nav), "".join(sections))

open(OUT, "w", encoding="utf-8", newline="\n").write(page)
print("written", OUT, len(page), "chars")
print("tables %d ext %d views %d rels %d (logical %d) pairs %d internal %d" % (
    n_tab, n_ext, n_view, len(rels), sum(1 for r in rels if r["logical"]), len(pairs), internal))
print("ascii", all(ord(c) < 128 for c in page))
