"""ERD v4: add Graphviz diagrams (as in v3) to the page built by build_erd_v4.py, then print the PDF.

Pipeline: runpy build_erd_v4.py (writes the base html and gives the model)
          -> DOT per tab -> @viz-js/viz (Graphviz wasm, node) -> SVG
          -> replace entity cards with figures, add legend, notation and print CSS
          -> headless Edge --print-to-pdf.
argv[1] = folder holding node_modules/@viz-js/viz (scratchpad).
"""
import html, json, os, re, runpy, subprocess, sys, tempfile, collections

ROOT = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
OUT = os.path.join(ROOT, r"06 Data\Recovery Workbench Entity Relationship Diagram v4.html")
PDF = os.path.join(ROOT, r"06 Data\Recovery Workbench Entity Relationship Diagram v4.pdf")
NODEDIR = sys.argv[1]
E = lambda s: html.escape(str(s), quote=True)
STD = {"is_active", "state", "version", "created_at", "created_by", "updated_at", "updated_by"}

g = runpy.run_path(os.path.join(ROOT, r"_work\scripts\build_erd_v4.py"))
entities, rels, dps, tabs, views = g["entities"], g["rels"], g["dps"], g["tabs"], g["views"]
by_dp = g["by_dp"]
dp_of = lambda n: entities[n]["dp"]

PUR, PURT, INK, MUT = "#604a7b", "#4e297f", "#1f1f1f", "#595959"
ACE_B, ACE_T, ACE_F = "#a35a00", "#8a4b00", "#fff4e3"
EXT_F = "#eeeaf6"
FONT = "Arial"


def chunks(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]


def field_label(f):
    marks = []
    if f.get("fk"):
        marks.append("(FK)")
    if f.get("bk"):
        marks.append("(BK)")
    if f.get("ak"):
        marks.append("(%s)" % f["ak"])
    if f.get("sb"):
        marks.append("(T2)")
    return E(f["name"] + (" " + " ".join(marks) if marks else ""))


def rows_html(lines, color=INK, size=11, italic=False):
    out = []
    for ln in lines:
        t = '<FONT POINT-SIZE="%d" COLOR="%s">%s</FONT>' % (size, color, ln)
        if italic:
            t = "<I>%s</I>" % t
        out.append('<TR><TD ALIGN="LEFT">%s</TD></TR>' % t)
    return "".join(out)


def box(title, title_color, top, rest, border, fill="#ffffff", dashed=False, title_size=13, bold=True):
    style = ' STYLE="dashed"' if dashed else ""
    inner = top + ("<HR/>" + rest if rest else "")
    t = E(title)
    if bold:
        t = "<B>%s</B>" % t
    return ('<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="0">'
            '<TR><TD ALIGN="LEFT"><FONT POINT-SIZE="%d" COLOR="%s">%s</FONT></TD></TR>'
            '<TR><TD><TABLE BORDER="1" COLOR="%s" BGCOLOR="%s"%s CELLBORDER="0" CELLSPACING="0" CELLPADDING="1">%s</TABLE></TD></TR>'
            '</TABLE>>' % (title_size, title_color, t, border, fill, style, inner))


def full_node(name):
    e = entities[name]
    fl = [f for f in e["fields"] if f["name"] not in STD]
    if e["kind"] == "view":
        tag = ["ACE view, read only, Tier %d" % e["tier"]]
        tag += [", ".join("public." + t for t in c) for c in chunks(e["ace"], 2)]
        top = rows_html([E(x) for x in tag], ACE_T, 10, italic=True)
        rest = rows_html([field_label(f) for f in fl])
        return box(name, ACE_T, top, rest, ACE_B, ACE_F, dashed=e["tier"] == 2)
    pk = [f for f in fl if f["pk"]]
    other = [f for f in fl if not f["pk"]]
    top = rows_html([field_label(f) for f in pk])
    if e["kind"] == "ext":
        top = rows_html(["<I>extension, 1:1 by ACE business key</I>"], PURT, 10) + top
        return box(name, PURT, top, rows_html([field_label(f) for f in other]), PUR, EXT_F)
    return box(name, PURT, top, rows_html([field_label(f) for f in other]), PUR)


def stub_node(name):
    e = entities[name]
    dpn = "%s %s" % (e["dp"], dps[e["dp"]]["name"])
    if e["kind"] == "view":
        keys = [f["name"] for f in e["fields"] if f.get("bk")] or [e["fields"][0]["name"]]
        top = rows_html([E(k + " (BK)") for k in keys])
        rest = rows_html([E("ACE view, Tier %d" % e["tier"]), E(dpn)], ACE_T, 10)
        return box(name, ACE_T, top, rest, ACE_B, ACE_F, dashed=e["tier"] == 2, title_size=12)
    pk = [f["name"] for f in e["fields"] if f["pk"]]
    top = rows_html([E(k) for k in pk], MUT)
    rest = rows_html([E(dpn)], MUT, 10)
    return ('<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="0">'
            '<TR><TD ALIGN="LEFT"><FONT POINT-SIZE="12" COLOR="%s"><B>%s</B></FONT></TD></TR>'
            '<TR><TD><TABLE BORDER="1" COLOR="#8c8c8c" STYLE="dashed" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1">%s%s</TABLE></TD></TR>'
            '</TABLE>>' % (MUT, E(name), top, rest))


def edge(r, label=None):
    a = ['dir=both', 'arrowtail=dot', 'arrowhead=%s' % ("none" if r["mand"] else "odiamond"), 'arrowsize=0.55']
    if r["logical"]:
        a += ['color="%s"' % ACE_B, 'style=dashed', 'penwidth=1.3', 'class="bk"', 'fontcolor="%s"' % ACE_T]
        lab = label if label is not None else r["col"] + " (BK)"
    else:
        a += ['color="%s"' % PUR, 'style=dashed', 'fontcolor="%s"' % MUT]
        lab = label if label is not None else r["col"]
    a.append('label="%s"' % lab)
    return '"%s" -> "%s" [%s];' % (r["child"], r["parent"], ", ".join(a))


HEAD = ('digraph G { graph [overlap=false, splines=true, sep="+14", esep="+6", pad=0.2, outputorder=edgesfirst]; '
        'node [shape=plaintext, fontname="%s", fontsize=11, fontcolor="%s", margin=0]; '
        'edge [fontname="%s", fontsize=10, arrowsize=0.55]; ' % (FONT, INK, FONT))


def dp_dot(d):
    members = by_dp[d]
    out = [HEAD]
    for n in members:
        out.append('"%s" [label=%s];' % (n, full_node(n)))
    stubs = []
    rr = [r for r in rels if r["child"] in members]
    for r in rr:
        if r["parent"] not in members and r["parent"] not in stubs:
            stubs.append(r["parent"])
    for n in stubs:
        out.append('"%s" [label=%s];' % (n, stub_node(n)))
    for r in rr:
        out.append(edge(r))
    out.append("}")
    return "\n".join(out), rr


def ace_dot():
    out = [HEAD.replace("digraph G { graph [", "digraph G { graph [rankdir=TB, ranksep=0.9, nodesep=0.15, newrank=true, ")]
    lrels = [r for r in rels if r["logical"]]
    for tier in (1, 2):
        out.append('subgraph cluster_t%d { label="%s"; labeljust=l; fontname="%s"; fontsize=13; fontcolor="%s"; color="%s"; style="%s";'
                   % (tier, "Tier 1 - ACE tables that exist today (Section A, 16 views)" if tier == 1 else
                      "Tier 2 - ACE additions in RWB-ACE-001 (Section B, 14 views)", FONT, ACE_T, ACE_B,
                      "solid" if tier == 1 else "dashed"))
        for v in views:
            if views[v]["tier"] != tier:
                continue
            e = entities[v]
            keys = [f["name"] + " (BK)" for f in e["fields"] if f.get("bk") and any(r["parent"] == v for r in lrels)]
            top = rows_html([E(", ".join("public." + t for t in c)) for c in chunks(e["ace"], 2)], ACE_T, 10, italic=True)
            rest = rows_html([E(k) for k in keys] + [E("%s, %d fields" % (e["dp"], len(e["fields"])))], INK, 10)
            out.append('"%s" [label=%s];' % (v, box(v, ACE_T, top, rest, ACE_B, ACE_F, dashed=tier == 2, title_size=12)))
        out.append("}")
    kids = []
    for r in lrels:
        if r["child"] not in kids:
            kids.append(r["child"])
    out.append('subgraph cluster_wb { label="Recovery schema - Workbench tables that link to ACE by business key"; labeljust=l; fontname="%s"; fontsize=13; fontcolor="%s"; color="%s";' % (FONT, PURT, PUR))
    for k in kids:
        e = entities[k]
        cols = [r["col"] + " (BK)" for r in lrels if r["child"] == k]
        top = rows_html([E(c) for c in cols])
        rest = rows_html([E("%s %s" % (e["dp"], dps[e["dp"]]["name"]))], MUT, 10)
        out.append('"%s" [label=%s];' % (k, box(k, PURT, top, rest, PUR, EXT_F if e["kind"] == "ext" else "#ffffff", title_size=12)))
    out.append("}")
    for r in lrels:
        out.append(edge(r))
    # keep Tier 2 below Tier 1: one invisible edge from a Tier 1 view to each Tier 2 view
    t1 = [v for v in views if views[v]["tier"] == 1]
    t2 = [v for v in views if views[v]["tier"] == 2]
    for i, v in enumerate(t2):
        out.append('"%s" -> "%s" [style=invis];' % (t1[i % len(t1)], v))
    out.append("}")
    return "\n".join(out)


def overview_dot():
    out = [HEAD]
    for d in tabs:
        wb = [n for n in by_dp[d] if entities[n]["kind"] != "view"]
        vw = [n for n in by_dp[d] if entities[n]["kind"] == "view"]
        shaded = d == "DP03"
        tc, fc, fill = ("#ffffff", "#ffffff", "#403152") if shaded else (PURT, INK, "#ffffff")
        if wb:
            lines = "".join('<TR><TD ALIGN="LEFT"><FONT POINT-SIZE="11" COLOR="%s">%s</FONT></TD></TR>'
                            % (fc, E(n + (" (ext)" if entities[n]["kind"] == "ext" else ""))) for n in wb)
            lab = ('<<TABLE BORDER="1" COLOR="%s" BGCOLOR="%s" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1">'
                   '<TR><TD ALIGN="LEFT"><FONT POINT-SIZE="13" COLOR="%s"><B>%s %s</B></FONT></TD></TR>%s</TABLE>>'
                   % (PUR, fill, tc, d, E(dps[d]["name"]), lines))
            out.append('"%s" [label=%s];' % (d, lab))
        if vw:
            lines = "".join('<TR><TD ALIGN="LEFT"><FONT POINT-SIZE="11" COLOR="%s">%s</FONT></TD></TR>'
                            % (INK, E("%s (T%d)" % (n, entities[n]["tier"]))) for n in vw)
            dashed = ' STYLE="dashed"' if all(entities[n]["tier"] == 2 for n in vw) else ""
            lab = ('<<TABLE BORDER="1" COLOR="%s" BGCOLOR="%s"%s CELLBORDER="0" CELLSPACING="0" CELLPADDING="1">'
                   '<TR><TD ALIGN="LEFT"><FONT POINT-SIZE="12" COLOR="%s"><B>ACE views - %s</B></FONT></TD></TR>%s</TABLE>>'
                   % (ACE_B, ACE_F, dashed, ACE_T, d, lines))
            out.append('"ACE_%s" [label=%s];' % (d, lab))
    node_of = lambda n: ("ACE_" + dp_of(n)) if entities[n]["kind"] == "view" else dp_of(n)
    agg = collections.OrderedDict()
    for r in rels:
        a, b = node_of(r["child"]), node_of(r["parent"])
        if a == b:
            continue
        k = (a, b, r["logical"])
        d = agg.setdefault(k, {"n": 0, "mand": False})
        d["n"] += 1
        d["mand"] = d["mand"] or r["mand"]
    for (a, b, lg), d in agg.items():
        out.append(edge({"child": a, "parent": b, "mand": True, "logical": lg, "col": ""}, label=str(d["n"])))
    out.append("}")
    return "\n".join(out), agg


# ---------- render through Graphviz wasm ----------
jobs = collections.OrderedDict()
ov_dot, ov_agg = overview_dot()
jobs["overview"] = {"dot": ov_dot, "engine": "neato"}
dp_rr = {}
for d in tabs:
    dot, rr = dp_dot(d)
    dp_rr[d] = rr
    jobs[d.lower()] = {"dot": dot, "engine": "neato" if len(by_dp[d]) > 1 else "dot"}
jobs["ace"] = {"dot": ace_dot(), "engine": "dot"}

tmp = tempfile.mkdtemp()
jin, jout = os.path.join(tmp, "in.json"), os.path.join(tmp, "out.json")
json.dump(jobs, open(jin, "w", encoding="utf-8"))
js = r"""
const fs=require('fs');const {instance}=require('@viz-js/viz');
instance().then(viz=>{const jobs=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));const out={};
for(const k in jobs){const r=viz.render(jobs[k].dot,{format:'svg',engine:jobs[k].engine});
if(r.status!=='success'){console.error(k,JSON.stringify(r.errors));process.exit(1)}out[k]=r.output;
for(const e of r.errors) if(e.level==='error') console.error(k,e.message);}
fs.writeFileSync(process.argv[3],JSON.stringify(out));});
"""
jsf = os.path.join(NODEDIR, "erd_render_tmp.js")
open(jsf, "w").write(js)
subprocess.run(["node", jsf, jin, jout], check=True, cwd=NODEDIR)
os.remove(jsf)
svgs = json.load(open(jout, encoding="utf-8"))


def clean(svg):
    svg = svg[svg.index("<svg"):]
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    # logical links: longer dash so they read as business-key lines, not FK constraints
    svg = re.sub(r'(<g id="edge\d+" class="edge bk">.*?</g>)',
                 lambda m: m.group(1).replace('stroke-dasharray="5,2"', 'stroke-dasharray="9,4"'), svg, flags=re.S)
    svg = re.sub(r"\n\s*\n", "\n", svg)
    return svg


svgs = {k: clean(v) for k, v in svgs.items()}
assert sum(s.count('class="edge bk"') for k, s in svgs.items() if k.startswith("dp") or k in ("ops", "agt", "rpt")) == \
    sum(1 for d in tabs for r in dp_rr[d] if r["logical"])

LEGEND = ('<div class="legend"><span><i style="border:1px solid #604a7b;background:#fff"></i>Workbench table</span>'
          '<span><i style="border:1px solid #604a7b;background:#eeeaf6"></i>Extension table, 1:1 by ACE business key</span>'
          '<span><i style="border:1px solid #a35a00;background:#fff4e3"></i>ACE view, Tier 1 (ACE table today)</span>'
          '<span><i style="border:1px dashed #a35a00;background:#fff4e3"></i>ACE view, Tier 2 (RWB-ACE-001)</span>'
          '<span><i style="border:1px dashed #8c8c8c;background:#fff"></i>Entity of another data product</span>'
          '<span><i class="ln" style="border-top:2px dashed #604a7b"></i>Foreign key</span>'
          '<span><i class="ln" style="border-top:2px dashed #a35a00"></i>Logical link: business key, no foreign key</span></div>')

page = open(OUT, encoding="utf-8").read()

# overview: keep the boundary picture, add the data-product reference diagram after it
n_cross_fk = sum(d["n"] for (a, b, lg), d in ov_agg.items() if not lg)
n_cross_bk = sum(d["n"] for (a, b, lg), d in ov_agg.items() if lg)
ov_block = ('<h3>Data products, their ACE views and the references between them</h3>'
            '<p>Each purple box is a data product with its Workbench and extension tables; DP03 Case and ownership is shaded. '
            'Each amber box holds the ACE views of that data product, marked T1 or T2. A line joins two boxes with the number of references between them; '
            'the dot is at the referring end. Purple dashed lines are foreign keys inside the recovery schema (%d across products). '
            'Amber long-dashed lines are logical links by ACE business key with no foreign key (%d across products, 18 in all).</p>'
            '<div class="fig">%s</div>%s' % (n_cross_fk, n_cross_bk, svgs["overview"], LEGEND))
anchor = "<h3>Data products</h3>"
assert page.count(anchor) == 1
page = page.replace(anchor, ov_block + anchor, 1)

for d in tabs:
    sid = d.lower()
    m = re.search(r'(<section class="tab" id="%s">.*?)<h3>Objects</h3><div class="cards">.*?</div></div><h3>References</h3>' % sid, page, flags=re.S)
    assert m, d
    fig = ('<div class="fig">%s</div>%s<p class="muted">References from other data products to these entities are on the tabs of those products, '
           'on the overview and on the ACE views tab.</p><h3>References</h3>' % (svgs[sid], LEGEND))
    page = page[:m.start()] + m.group(1) + fig + page[m.end():]

m = re.search(r'<h3>View boxes</h3>.*?</div></section>', page, flags=re.S)
page = page[:m.start()] + ('<h3>Diagram</h3><p class="muted">The 30 views in two tiers, the ACE tables each reads, and the 18 logical links from the recovery schema. '
                           'No line carries a foreign key: ACE cascades deletes on account, so integrity is checked by the read model and reconciliation rule REC-05. '
                           'The fields of each view are on its data product tab.</p><div class="fig">%s</div>%s</section>' % (svgs["ace"], LEGEND)) + page[m.end():]
assert 'class="cards"' not in page

# notation, matched to the diagrams
m = re.search(r'(<section class="tab" id="notation">).*?</section>', page, flags=re.S)
NOT = [("Square-cornered box", "An independent entity. Its key does not depend on any other entity. Every Workbench entity in this model is independent"),
       ("Name above the box", "The entity name as it is held in the recovery schema of the ACE database, or the view name"),
       ("Line inside the box", "Above the line is the primary key. Below it are the other attributes. The seven standard record columns (is_active, state, version, created_at, created_by, updated_at, updated_by) are not shown"),
       ("(FK)", "A foreign key inside the recovery schema"),
       ("(BK)", "A business key of an ACE record, varchar(255). It replaces a UUID foreign key into a removed source copy, or keys an extension table. No foreign key constraint into ACE"),
       ("(AK1)", "An alternate key: unique on its own or together with the other AK1 attributes of the entity"),
       ("(T2)", "A column on a Tier 1 view that RWB-ACE-001 adds to an existing ACE table"),
       ("Purple box on lilac", "A Workbench extension table: 1:1 with an ACE record, keyed by its business key, holding Workbench decisions and never a copy"),
       ("Amber box, solid border", "External and ACE-owned: a Tier 1 recovery.v_ace_* view over ACE tables that exist today. Read only; the italic line names the ACE tables it reads"),
       ("Amber box, dashed border", "External and ACE-owned: a Tier 2 view over a table the ACE team adds in RWB-ACE-001 (Section B, V0003)"),
       ("Dashed grey box", "A Workbench entity from another data product, shown with its key only"),
       ("Purple short-dashed line", "A non-identifying relationship with a foreign key constraint. The label is the foreign key attribute"),
       ("Amber long-dashed line", "A logical relationship by business key, with no foreign key. Integrity is checked by the read model and reconciliation rule REC-05. The label is the business-key column"),
       ("Filled dot", "The child end of the relationship: zero, one or more child records (zero or one for an extension table)"),
       ("Open diamond", "At the parent end: the reference is optional, so a child may have no parent"),
       ("No diamond", "At the parent end: the reference is mandatory, so every child has exactly one parent"),
       ("Number on a line (overview)", "The number of references between the two boxes")]
page = page[:m.start()] + ('<section class="tab" id="notation"><h2>IDEF1X notation and legend</h2><p>The diagrams use the IDEF1X notation for entities, keys and relationships, with an amber notation for the ACE boundary.</p>'
                           '<div class="tw"><table style="min-width:760px"><thead><tr><th>Symbol</th><th>Meaning</th></tr></thead><tbody>%s</tbody></table></div>%s</section>'
                           % ("".join('<tr><td>%s</td><td>%s</td></tr>' % (E(a), E(b)) for a, b in NOT), LEGEND)) + page[m.end():]

# style: legend lines, fixed white figure ground, print as in v3 (A3 landscape, one diagram a page)
CSS = """
.fig{background:#FFFFFF}
.legend i.ln{width:26px;height:0;border:0;vertical-align:3px}
.foot{display:none}
@media print{
 @page{size:A3 landscape;margin:12mm}
 html,body{background:#fff;color:#1F1F1F}
 header,nav,.grid,.tw,.filter,section.tab>p,section.tab>h3,section.tab>p.muted{display:none!important}
 section.tab#all{display:none!important}
 section.tab#notation .tw{display:block!important}
 section.tab{page-break-before:always;break-before:page}
 section.tab#overview{page-break-before:auto;break-before:auto}
 main{max-width:none;padding:0}
 h2{margin:0 0 6px}
 .fig{border:0;padding:0;overflow:visible}
 .fig svg{width:auto;height:auto;max-width:100%;max-height:236mm}
 .legend{margin:4px 0 0}
 .foot{display:block;position:fixed;bottom:0;left:0;font-size:11px;color:#595959}
}
"""
page = page.replace("</style>", CSS + "</style>", 1)
page = page.replace("</main>", '</main><div class="foot">(C) Siam Commercial Bank and Henka Pte Ltd. Recovery Workbench Entity Relationship Diagram v4, 15 November 2026.</div>', 1)
page = page.replace(".fig svg{display:block;max-width:none}", ".fig svg{display:block;max-width:none;height:auto}")
open(OUT, "w", encoding="utf-8", newline="\n").write(page)
print("html", len(page), "svgs", len(svgs), "svg tags", page.count("<svg"), "bk edges drawn",
      sum(s.count('class="edge bk"') for s in svgs.values()))

# ---------- PDF ----------
edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
url = "file:///" + OUT.replace("\\", "/").replace(" ", "%20")
prof = tempfile.mkdtemp()
subprocess.run([edge_exe, "--headless", "--disable-gpu", "--no-pdf-header-footer", "--user-data-dir=" + prof,
                "--virtual-time-budget=5000", "--print-to-pdf=" + PDF, url], check=True, timeout=180)
print("pdf", os.path.getsize(PDF))
