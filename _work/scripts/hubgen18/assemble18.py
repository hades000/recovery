"""Assemble Project Hub v18: the v17 viewer, re-pointed at the D-RCV-60 document set.

Reads: 14 Story Updates/Recovery Workbench Project Hub v17.html (never edited),
       _work/data/hub18_payload.json, _work/data/hub18_blobs.json, Decision Log v11.
Writes: 14 Story Updates/Recovery Workbench Project Hub v18.html (new file).
"""
import base64
import datetime
import gzip
import io
import json
import os
import re

import openpyxl

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14'
SRC = os.path.join(ROOT, '14 Story Updates', 'Recovery Workbench Project Hub v17.html')
OUT = os.path.join(ROOT, '14 Story Updates', 'Recovery Workbench Project Hub v18.html')
DATA = os.path.join(ROOT, '_work', 'data')
DECLOG = os.path.join(ROOT, '01 Decisions and governance', 'Recovery Workbench Decision Log v11.xlsx')
SVCDIR = os.path.join(ROOT, '04 User stories', 'Recovery Workbench Service Story Files v1')

# ------------------------------------------------------------------ payload clean-up
M = json.load(io.open(os.path.join(DATA, 'hub18_payload.json'), encoding='utf-8'))
blobs = json.load(io.open(os.path.join(DATA, 'hub18_blobs.json'), encoding='utf-8'))

subs = {(d['folder'], d['sub']) for d in M['docs'] if d.get('sub')}
sub_fam = {}
for folder, sub in subs:
    m = re.match(r'^(.*?)\s+v(\d+)$', sub)
    if m:
        sub_fam[(folder, m.group(1))] = int(m.group(2))


def stale(d):
    """A top-level file whose family continues as a newer versioned folder."""
    if d.get('sub'):
        return False
    m = re.match(r'^(.*?)\s+v(\d+)$', d['name'])
    return bool(m) and sub_fam.get((d['folder'], m.group(1)), -1) > int(m.group(2))


def drop(d):
    if stale(d):
        return True
    # the two registers are kept as Markdown text; the workbook is the same rows
    return d['ext'] == 'xlsx' and re.search(r'(Gap|Assumptions) Register', d['name']) is not None


keep = [i for i, d in enumerate(M['docs']) if not drop(d)]
dropped = [M['docs'][i]['file'] for i in range(len(M['docs'])) if i not in set(keep)]
remap = {old: new for new, old in enumerate(keep)}
M['docs'] = [M['docs'][i] for i in keep]
for code in list(M['ids']):
    v = M['ids'][code]
    v['u'] = [[remap[a], b] for a, b in v['u'] if a in remap]
    if v['d'][0] in remap:
        v['d'] = [remap[v['d'][0]], v['d'][1]]
    elif v['u']:
        v['d'] = list(v['u'][0])
    else:
        del M['ids'][code]
stale_files = {M_f for M_f in M['files']
               if re.match(r'^(.*?)\s+v(\d+)\.\w+$', M_f) and
               sub_fam.get((M['fmeta'][M_f]['folder'], re.match(r'^(.*?)\s+v(\d+)\.\w+$', M_f).group(1)), -1)
               > int(re.match(r'^(.*?)\s+v(\d+)\.\w+$', M_f).group(2))}
for f in stale_files:
    del M['files'][f]
    del M['fmeta'][f]
old_ids = sorted(M['files'].items(), key=lambda kv: kv[1])
blobs = [blobs[i] for _, i in old_ids]
M['files'] = {k: n for n, (k, _) in enumerate(old_ids)}
for d in M['docs']:
    d.pop('sub', None)
print('docs kept', len(M['docs']), 'dropped', dropped, 'stale files', sorted(stale_files))

# service, platform and integration epics, from the story-file folder names
SEPICS = []
for n in sorted(os.listdir(SVCDIR)):
    m = re.match(r'^(RWB-(?:SVC|PLT|ITG)-[A-Z0-9]+)\s+(.*)$', n)
    if m and os.path.isdir(os.path.join(SVCDIR, n)):
        SEPICS.append({'id': m.group(1), 'label': m.group(2)})


def sepic_order(e):
    m = re.match(r'RWB-SVC-([PS])(\d+)', e['id'])
    if m:
        return (0 if m.group(1) == 'P' else 1, int(m.group(2)), '')
    plt = ['TPL', 'DB', 'LIB', 'EDGE', 'EVT', 'WF', 'OBS']
    if e['id'].startswith('RWB-PLT-'):
        k = e['id'][8:]
        return (2, plt.index(k) if k in plt else 99, k)
    return (3, 0, e['id'])


SEPICS.sort(key=sepic_order)
print('service epics', len(SEPICS))


def fmt_date(v):
    if isinstance(v, datetime.datetime):
        v = v.date()
    if isinstance(v, datetime.date):
        return v.strftime('%d %B %Y'), v.isoformat()
    return str(v or '').strip(), ''


def load_dec():
    wb = openpyxl.load_workbook(DECLOG, data_only=True)
    s = lambda x: str(x or '').strip()  # noqa: E731
    op, tk = [], []
    for r in wb['Open decisions'].iter_rows(min_row=6, values_only=True):
        if not r or not r[0] or s(r[0]) == 'ID':
            continue
        by, iso = fmt_date(r[6])
        op.append({'id': s(r[0]), 'dec': s(r[1]), 'q': s(r[2]), 'opts': s(r[3]), 'rec': s(r[4]),
                   'owner': s(r[5]), 'by': by, 'iso': iso, 'blocks': s(r[7]), 'late': s(r[8])})
    for r in wb['Decisions taken'].iter_rows(min_row=5, values_only=True):
        if not r or not r[0] or s(r[0]) == 'ID':
            continue
        by, iso = fmt_date(r[2])
        tk.append({'id': s(r[0]), 'dec': s(r[1]), 'by': by, 'iso': iso, 'who': s(r[3]), 'means': s(r[4])})
    return {'open': op, 'taken': tk, 'file': os.path.basename(DECLOG), 'folder': '01 Decisions and governance'}


DEC = load_dec()
print('decisions open', len(DEC['open']), 'taken', len(DEC['taken']))

# ------------------------------------------------------------------ html
src = io.open(SRC, encoding='utf-8-sig').read()
p0 = src.index('<script type="application/octet-stream" id="payload">')
main_js = src.index('<script>', src.index('<script type="application/octet-stream" id="f%d">' %
                                          (len(re.findall(r'id="f\d+"', src)) - 1)))
head, tail = src[:p0], src[main_js:]

raw = json.dumps(M, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
pay = base64.b64encode(gzip.compress(raw, 9)).decode('ascii')
parts = [head, '<script type="application/octet-stream" id="payload">', pay, '</script>\n']
for i, b in enumerate(blobs):
    parts.append('<script type="application/octet-stream" id="f%d">%s</script>\n' % (i, b))
out = ''.join(parts)


def rep(old, new, text=None):
    global tail
    n = tail.count(old)
    assert n == 1, (n, old[:90])
    tail = tail.replace(old, new)


def rep_head(old, new):
    global out
    n = out.count(old)
    assert n == 1, (n, old[:90])
    out = out.replace(old, new)


def replace_const(name, obj):
    global tail
    key = 'const ' + name + '='
    i = tail.index(key) + len(key)
    dec = json.JSONDecoder()
    _, end = dec.raw_decode(tail, i)
    tail = tail[:i] + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + tail[end:]


replace_const('DEC', DEC)

# ---- header, title, CSS
rep_head('<title>Recovery Workbench project hub v17</title>',
         '<title>Recovery Workbench project hub v18</title>')
rep_head('<div class="brand">Recovery Workbench <span style="font-weight:400;color:var(--soft)">v17</span> D-RCV-36: Temporal and Drools adoption</div>',
         '<div class="brand">Recovery Workbench <span style="font-weight:400;color:var(--soft)">v18</span> D-RCV-60: 19-service realignment</div>')
rep_head('.kSTORY,.kREQ,.kFEAT{color:var(--k3);background:var(--k3b)}',
         '.kSTORY,.kREQ,.kFEAT,.kNSTORY,.kSEPIC,.kFR{color:var(--k3);background:var(--k3b)}')

# ---- code pattern (new story keys, epics, gaps, assumptions, PRD requirements)
NEWRX = ("RWB-(?:P10|P[1-9]|S[1-9]|PLT|ITG|ACE|AD|DM|TE)-(?=[A-Z]*\\\\d)[A-Z0-9]{3,7}-[A-Z]{2,3}(?:-\\\\d+)?|"
         "RWB-(?:SVC-(?:P10|P[1-9]|S[1-9])|PLT-[A-Z]{2,4}|ITG-(?:W[1-4]|NFR))|GAP-\\\\d{4}|ASM-\\\\d{4}|"
         "FR-(?:P10|P[1-9]|S[1-9])-\\\\d{3}|")
rep("const IDRX=new RegExp('\\\\b(", "const IDRX=new RegExp('\\\\b(" + NEWRX)
rep("const ORDER=['REQ',", "const ORDER=['NSTORY','SEPIC','FR','GAP','ASM','REQ',")

# ---- stories: new keys, attributes and service-epic groups
rep("""function buildStories(){
  const rx=/^(RWB-[A-Z]{1,3}\\d?-\\d{3})\\s+(.*)$/;""",
    """const SKEY=/^(RWB-[A-Z0-9]+(?:-[A-Z0-9]+){1,3})\\s+(.*)$/;
function buildStories(){
  const rx=SKEY;""")
rep("""      const ea=attr(s.t,'Epic').match(/E\\d/);
      STORIES.push({k:m[1], t:m[2], d:di, s:si, src:d.name,
        ep:ea?ea[0]:('E'+((m[1].match(/RWB-E(\\d)/)||[])[1]||'')),
        mod:attr(s.t,'Module'), pri:attr(s.t,'Priority'), st:attr(s.t,'Status'),
        rel:attr(s.t,'Epic')});""",
    """      const be=(attr(s.t,'Business epic').match(/EP0?(\\d)/)||[])[1];
      const ea=attr(s.t,'Epic').match(/E\\d/);
      STORIES.push({k:m[1], t:m[2], d:di, s:si, src:d.name,
        ep:be?('E'+be):(ea?ea[0]:('E'+((m[1].match(/RWB-E(\\d)/)||[])[1]||''))),
        mod:attr(s.t,'Service')||attr(s.t,'Module'), pri:attr(s.t,'Work type')||attr(s.t,'Priority'),
        st:attr(s.t,'Status'), rel:attr(s.t,'Release')||attr(s.t,'Epic'),
        sep:attr(s.t,'Service epic'), wave:attr(s.t,'Wave'), lane:attr(s.t,'Parallel lane'),
        ready:attr(s.t,'Ready to start'), leg:attr(s.t,'Legacy key'), own:attr(s.t,'Suggested owner')});""")
rep("""  STORIES.sort((a,b)=>((IMPL_ORDER[a.k]||9999)-(IMPL_ORDER[b.k]||9999))||a.k.localeCompare(b.k,undefined,{numeric:true}));""",
    """  const wv=s=>parseInt(s.wave,10)||9, rd=s=>/day\\s*1/i.test(s.ready)?0:1;
  STORIES.sort((a,b)=>(wv(a)-wv(b))||(rd(a)-rd(b))||a.lane.localeCompare(b.lane,undefined,{numeric:true})||a.k.localeCompare(b.k,undefined,{numeric:true}));""")
rep("""const FAM=[['RWB-ACE','ACE team stories','The ACE team contract that unblocks the recovery read path'],
           ['RWB-AD','Administration stories','Roles, access, reference data and the admin screens'],
           ['RWB-DM','Data migration stories','Moving the live book onto the Workbench'],
           ['RWB-TE','Technical enabler stories','Scaffolding the squads need before feature work']];""",
    """const FAM=[];
const SEPICS=""" + json.dumps(SEPICS, ensure_ascii=False) + """;
const GKIND={svc:'Service epics (19 services)',plt:'Platform epics',itg:'Integration epics',epic:'Business epics (EP01 to EP08)',other:'Other stories'};""")
rep("""function buildGroups(){
  GROUPS=EPICS.map(x=>({
    id:x.e, label:'Epic '+x.e.slice(1), note:x.theme, rel:x.rel, gets:x.gets,
    kind:'epic', items:STORIES.filter(s=>s.ep===x.e&&!isFam(s))}));""",
    """function buildGroups(){
  GROUPS=[];
  SEPICS.forEach(x=>{
    const items=STORIES.filter(s=>s.sep===x.id);
    if(!items.length) return;
    const w=Math.min(...items.map(s=>parseInt(s.wave,10)||9));
    GROUPS.push({id:x.id, label:x.id.replace(/^RWB-/,''), note:x.label, rel:w<9?'Wave '+w:'', gets:'',
      kind:x.id.startsWith('RWB-SVC')?'svc':x.id.startsWith('RWB-PLT')?'plt':'itg', items:items});
  });
  const known=new Set(SEPICS.map(x=>x.id));
  const rest=STORIES.filter(s=>!known.has(s.sep));
  EPICS.forEach(x=>GROUPS.push({
    id:x.e, label:'Epic '+x.e.slice(1), note:x.theme, rel:x.rel, gets:x.gets,
    kind:'epic', items:STORIES.filter(s=>s.ep===x.e)}));
  if(rest.length) GROUPS.push({id:'__other',label:'Other stories',note:'No service epic named',rel:'',kind:'other',items:rest});""")

# sidebar headings per group kind
rep("""  h+=`<div class="grp">Epics</div>`;
  let wroteFam=false;
  GROUPS.forEach(g=>{
    if(g.kind==='fam' && !wroteFam){ h+=`<div class="grp">Other backlog</div>`; wroteFam=true; }
    const items=f?g.items.filter(s=>(s.k+' '+s.t+' '+s.mod).toLowerCase().includes(f)):g.items;""",
    """  let lastKind='';
  GROUPS.forEach(g=>{
    const items=f?g.items.filter(s=>(s.k+' '+s.t+' '+s.mod+' '+(s.leg||'')+' '+(s.lane||'')).toLowerCase().includes(f)):g.items;
    if(f&&!items.length) return;
    if(g.kind!==lastKind){ h+=`<div class="grp">${esc(GKIND[g.kind]||'Stories')}</div>`; lastKind=g.kind; }""")
rep("""    if(f&&!items.length) return;
    const open=f?true:""", """    const open=f?true:""")
rep("""placeholder="Filter stories by key, title or module\"""",
    """placeholder="Filter by key, title, service, legacy key or lane\"""")

# group page rows
rep("""        <div class="m">${g.kind==='fam'?esc(s.ep)+' · ':''}${esc(s.pri)}${s.st?' · '+esc(s.st):''}</div></div>`;""",
    """        <div class="m">${g.kind==='epic'?esc(s.sep)+' · ':''}${s.wave?'Wave '+esc(s.wave)+' · ':''}${s.lane?esc(s.lane)+' · ':''}${esc(s.pri)}${s.ready?' · '+esc(s.ready):''}${s.leg?' · from '+esc(s.leg):''}</div></div>`;""")
rep("""    h+=`<p class="lede">In build order. Pick a story on the left, or from the list below. Everything a story needs sits on its own page.</p>`;""",
    """    h+=`<p class="lede">In build order: wave, then Day-1 stories, then parallel lane. Pick a story on the left, or from the list below. Everything a story needs sits on its own page.</p>`;""")

# story text ends at the next story heading or a heading at the story's own level
rep("""    if(/^RWB-[A-Z]{1,3}\\d?-\\d{3}\\s/.test(d.secs[k].h.trim())) break;""",
    """    if(SKEY.test(d.secs[k].h.trim())||(d.secs[k].l||9)<=(d.secs[si].l||1)) break;""")

# story page header
rep("""    <p class="lede">${esc(st.mod||'')}${st.rel?' · '+esc(st.rel):''}${st.pri?' · '+esc(st.pri):''}${st.st?' · '+esc(st.st):''}""",
    """    <p class="lede">${esc(st.mod||'')}${st.sep?' · '+idHtml(st.sep):''}${st.wave?' · Wave '+esc(st.wave):''}${st.lane?' · lane '+esc(st.lane):''}${st.ready?' · '+esc(st.ready):''}${st.rel?' · '+esc(st.rel):''}${st.pri?' · '+esc(st.pri):''}${st.st?' · '+esc(st.st):''}${st.leg?' · legacy '+idHtml(st.leg):''}""")

# tabs
rep("""`<button role="tab" data-t="__work">Stories by epic<span class="n">${STORIES.length}</span></button>`""",
    """`<button role="tab" data-t="__work">Stories by service epic<span class="n">${STORIES.length}</span></button>`""")

# home page
rep("""      <b>Version 17, 16 November 2026:</b> Temporal and Drools adoption, developer action plans, simple acceptance criteria and build order. Source data is read from 30
      <code>recovery.v_ace_*</code> views; there are no inbound loads in the Workbench.</p>""",
    """      <b>Version 18, 23 November 2026:</b> rebuilt from the D-RCV-60 document set. The backlog is realigned to
      19 services (P1 to P10, S1 to S9), 7 platform epics and 5 integration epics; every story is a service story with
      its own wave, parallel lane and Day-1 flag. Release dates are tentative and copied unchanged from the source documents.</p>""")
rep("""   <p>The <b>Stories by epic</b> tab lists the epics, and each epic opens its stories.""",
    """   <p>The <b>Stories by service epic</b> tab lists the 31 service, platform and integration epics, and then the eight
      business epics (EP01 to EP08) as a second view of the same stories. Each epic opens its stories.""")
rep("""   <h2>What changed in this version</h2>
   <p>The eight inbound load stories (E1-003, 004, 005, 006, 009, 010, 012 and 051) and the EFS load story E2-023 are gone.""",
    """   <h2>What changed in version 18</h2>
   <p>Every document is the current version on disk after the D-RCV-60 microservice realignment: User Stories Epic 1 v10,
      Epic 2 v8, Epics 3 to 8 v4, Technical Enablers v8, Administration v4, Data Migration v4, ACE Team Stories v2,
      the Service Epics v1 and Service Story Catalog v1, the 20 PRDs, FSD by Module v7, TSD by Module v6,
      API Specification v5, Physical Schema v7, Decision Log v11, and the Gap Register and Assumptions Register in
      folder 23. A story key now names its service and work type, for example
      <code>RWB-P1-E1001-APP</code>; the old key it came from is shown as <b>legacy</b> on the story page. New code families are
      clickable: service stories, service epics, PRD requirements (FR-), gaps (GAP-) and assumptions (ASM-).</p>
   <p>The table, column and endpoint boxes are still read from the v17 schema extract (one recovery schema). The
      per-service schemas are in Physical Schema v7 in the Documents tab. Some story files are too large to embed and are
      listed on the Original files tab; get them from the SharePoint folder.</p>
   <h2>Carried from version 17</h2>
   <p>The eight inbound load stories (E1-003, 004, 005, 006, 009, 010, 012 and 051) and the EFS load story E2-023 are gone.""")

# original files: name the files kept out of the hub
rep("""      Click to download and open in Word, PowerPoint, Excel or the browser.</p>`+""",
    """      Click to download and open in Word, PowerPoint, Excel or the browser.</p>`+
    ((M.notembedded||[]).length&&!folder?`<div class="note"><b>Not embedded, too large for one file:</b> `+
      M.notembedded.map(x=>esc(x.folder+' / '+x.file)+' ('+(x.size/1048576).toFixed(1)+' MB)').join('; ')+
      `. Their text is in the Documents tab and the stories tab; download the file from the SharePoint folder.</div>`:'')+""")

out = out + tail
io.open(OUT, 'w', encoding='utf-8').write(out)
print('written', OUT, round(os.path.getsize(OUT) / 1048576, 1), 'MB')
