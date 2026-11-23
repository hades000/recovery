import base64, json, re, zlib, html
from pathlib import Path

ROOT = Path('.').resolve()
SRC = ROOT / '12 Project communication' / 'Recovery Workbench Project Hub v14.html'
DST = ROOT / '12 Project communication' / 'Recovery Workbench Project Hub v15.html'
SCRATCH = ROOT / '_work' / 'msr' / 'docs' / 'D2-HUB'

src = SRC.read_text(encoding='utf-8')

# ---------------------------------------------------------------- payload
m = re.search(r'<script type="application/octet-stream" id="payload">([^<]*)</script>', src)
assert m, 'payload script not found'
raw = base64.b64decode(m.group(1))
payload_txt = zlib.decompress(raw, 16 + zlib.MAX_WBITS).decode('utf-8')
M = json.loads(payload_txt)
print('docs', len(M['docs']), 'ids', len(M['ids']), 'files', len(M['files']))

# ---------------------------------------------------------------- current files on disk
disk = []
for p in ROOT.iterdir():
    if p.is_dir() and re.match(r'^\d\d ', p.name):
        for f in p.rglob('*'):
            if f.is_file():
                disk.append(f.relative_to(ROOT).as_posix())

VER = re.compile(r'^(.*?)\s+v(\d+)$')

def fam(basename):
    stem, ext = (basename.rsplit('.', 1) + [''])[:2] if '.' in basename else (basename, '')
    stem2 = basename[:-(len(ext) + 1)] if ext else basename
    mm = VER.match(stem2)
    if mm:
        return mm.group(1), int(mm.group(2)), ('(.' + ext + ')' if ext else '')
    # folder names carry vN too:  "Recovery Workbench API Specification v5"
    return stem2, 0, ('(.' + ext + ')' if ext else '')

# ---------------------------------------------------------------- map each embedded doc to the current file
newer = {}
for d in M['docs']:
    folder = d['folder']
    base = d['file'].rsplit('/', 1)[-1].strip()   # zip members: use the member name
    fstem, fver, fext = fam(base)
    best = None
    for rel in disk:
        if not rel.startswith(folder + '/'):
            continue
        b = rel.rsplit('/', 1)[-1]
        cstem, cver, cext = fam(b)
        if cstem == fstem and cver > fver:
            key = (cver, 1 if cext == fext else 0)
            if best is None or key > best[0]:
                best = (key, rel)
    if best:
        newer[d['file']] = best[1]
        d['nf'] = best[1]

print('mapped to a newer file:', len(newer))

# ---------------------------------------------------------------- the new files from the run (edit logs)
setfiles = []
seen = set()
for lg in sorted((ROOT / '_work' / 'msr' / 'editlog').glob('*.md')):
    if lg.stem in ('SMOKE',) or lg.stem.startswith('A6'):
        continue
    t = lg.read_text(encoding='utf-8')
    if '## Files written' not in t:
        continue
    blk = t.split('## Files written', 1)[1].split('\n## ', 1)[0]
    for mm in re.finditer(r'(?m)^\s*[-*]\s+`([^`]+\.(?:md|docx|xlsx|pptx|yaml|sql|json|html|svg|excalidraw|zip|txt))`', blk):
        p = mm.group(1).replace('\\', '/').strip()
        if p.startswith('_work/') or p in ('rows_readme.json', 'v3_dump.txt', 'src_dump.json', 'v2_dump.txt'):
            continue
        if not (ROOT / p).exists():
            continue
        if p in seen:
            for x in setfiles:
                if x['file'] == p and lg.stem not in x['wp'].split(', '):
                    x['wp'] = x['wp'] + ', ' + lg.stem
            continue
        seen.add(p)
        setfiles.append({'file': p, 'wp': lg.stem})
setfiles.append({'file': '12 Project communication/Recovery Workbench Project Hub v15.html', 'wp': 'D2-HUB'})
setfiles.sort(key=lambda x: x['file'].lower())
M['setfiles'] = setfiles
M['setlabel'] = 'Document set v15'
print('setfiles', len(setfiles))

# ---------------------------------------------------------------- re-encode payload
new_payload = json.dumps(M, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
print('payload bytes', len(new_payload))
co = zlib.compressobj(9, zlib.DEFLATED, 16 + zlib.MAX_WBITS)
blob = base64.b64encode(co.compress(new_payload) + co.flush()).decode('ascii')
out = src[:m.start(1)] + blob + src[m.end(1):]

# ---------------------------------------------------------------- shell patches
def rep(old, new, count=1):
    global out
    assert out.count(old) == count, (out.count(old), old[:80])
    out = out.replace(old, new, count)

rep('<title>Recovery Workbench project hub</title>',
    '<title>Recovery Workbench project hub. Document set v15</title>')

css_add = """
.dochead{display:flex;gap:6px 16px;flex-wrap:wrap;align-items:center;padding:6px 16px;border-bottom:1px solid var(--line);background:var(--tint);font-size:11.5px;color:var(--soft)}
.dochead .dhset{margin-left:auto;font-weight:700;color:var(--accent);background:var(--accent-soft);border-radius:10px;padding:2px 9px;font-size:11px;letter-spacing:.02em}
.setpill{font-size:10.5px;font-weight:700;color:var(--accent);background:var(--accent-soft);border-radius:10px;padding:2px 8px;margin-left:8px;letter-spacing:.02em}
@media (max-width:620px){.dochead{font-size:11px}.dochead .dhset{display:none}}
"""
rep('@media (min-width:901px){#menu{display:none}}\n</style>',
    '@media (min-width:901px){#menu{display:none}}' + css_add + '</style>')

rep('main{display:grid;grid-template-columns:326px 1fr;height:calc(100% - 86px)}',
    'main{display:grid;grid-template-columns:326px 1fr;height:calc(100% - 116px)}')
rep('.side{position:fixed;left:0;top:86px;', '.side{position:fixed;left:0;top:116px;')

rep('<header>\n <div class="top">',
    '<header>\n <div class="dochead"><span>SCB Collections and Recovery. Henka Group, 22 November 2026.</span>'
    '<span>(C) Siam Commercial Bank and Henka Pte Ltd</span><span class="dhset">Document set v15</span></div>\n <div class="top">')

rep('<div class="brand">Recovery Workbench</div>',
    '<div class="brand">Recovery Workbench<span class="setpill">Document set v15</span></div>')

rep("+`<button role=\"tab\" data-t=\"__terms\">Terms<span class=\"n\">${TERMS.terms.length}</span></button>`;",
    "+`<button role=\"tab\" data-t=\"__set\">Set v15<span class=\"n\">${M.setfiles.length}</span></button>`"
    "+`<button role=\"tab\" data-t=\"__terms\">Terms<span class=\"n\">${TERMS.terms.length}</span></button>`;")

rep("  if(t==='__files'){ sideFiles(); bodyFiles(); return; }",
    "  if(t==='__files'){ sideFiles(); bodyFiles(); return; }\n"
    "  if(t==='__set'){ sideSet(); bodySet(); return; }")

rep("  M.folders=[...new Set(M.docs.map(d=>d.folder))].sort();",
    "  M.folders=[...new Set(M.docs.map(d=>d.folder))].sort();\n"
    "  M.setfolders=[...new Set(M.setfiles.map(x=>x.file.includes('/')?x.file.slice(0,x.file.lastIndexOf('/')):'(root)'))].sort();")

# --- new tab functions, inserted before the documents block
set_js = r"""
/* ---------- document set v15 ---------- */
function setFolder(file){ return file.includes('/')?file.slice(0,file.lastIndexOf('/')):'(root)'; }
function setGroups(){
  const by={};
  M.setfiles.forEach(x=>{(by[setFolder(x.file)]=by[setFolder(x.file)]||[]).push(x);});
  return by;
}
function shortFolder(f){
  return f.replace('04 User stories/Recovery Workbench Service Story Files v1/','Stories: ')
          .replace('05 Technical architecture/Recovery Workbench API Specification v5/asyncapi','API v5 / asyncapi')
          .replace('05 Technical architecture/Recovery Workbench API Specification v5','API Specification v5')
          .replace('05 Technical architecture/Recovery Workbench Technical Specifications by Module v6','TSD by Module v6')
          .replace('03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7','FSD by Module v7')
          .replace('06 Data/Recovery Workbench Physical Schema v7','Physical Schema v7');
}
function sideSet(sel){
  const by=setGroups();
  let h=`<div class="grp">Document set v15</div>
    <a href="#" data-s="*" class="${!sel||sel==='*'?'on':''}">Every new file<span class="ex">${M.setfiles.length} files</span></a>
    <div class="grp">By folder</div>`;
  h+=Object.keys(by).sort().map(f=>`<a href="#" data-s="${esc(f)}" class="${sel===f?'on':''}">${esc(shortFolder(f))}
      <span class="ex">${by[f].length} file${by[f].length===1?'':'s'}</span></a>`).join('');
  const side=document.querySelector('.side'); side.innerHTML=h;
  side.querySelectorAll('a[data-s]').forEach(a=>a.onclick=ev=>{ev.preventDefault();sideSet(a.dataset.s);bodySet(a.dataset.s);});
}
function bodySet(sel){
  const by=setGroups();
  const all=!sel||sel==='*';
  const folders=all?Object.keys(by).sort():[sel];
  let h=`<h1>Document set v15</h1>
   <p class="lede">${M.setfiles.length} new and next-version files, in ${Object.keys(by).length} folders, written by the
     D-RCV-60 microservice realignment. The text in the Documents tab is the set as it was embedded at the previous version;
     this tab names the file that replaces each one, and every document page also shows its Set v15 file.</p>
   <div class="note"><table><thead><tr><th style="width:74px">Version</th><th style="width:140px">Date</th><th>Change log</th></tr></thead><tbody>
    <tr><td data-l="Version">v15</td><td data-l="Date">22 November 2026</td>
        <td data-l="Change log">D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash</td></tr>
   </tbody></table></div>`;
  folders.forEach(f=>{
    const rows=by[f].slice().sort((a,b)=>a.file.localeCompare(b.file,undefined,{numeric:true}));
    h+=`<h2>${esc(f)} <span class="chip">${rows.length}</span></h2>
      <table><thead><tr><th>File</th><th style="width:120px">Written by</th></tr></thead><tbody>`+
      rows.map(x=>`<tr><td data-l="File">${esc(x.file.split('/').pop())}</td><td data-l="Written by">${esc(x.wp)}</td></tr>`).join('')+
      `</tbody></table>`;
  });
  const b=document.querySelector('.body'); b.innerHTML=h; b.scrollTop=0;
  if(innerWidth<=900) document.querySelector('.side').classList.remove('open');
}

/* ---------- documents ---------- */"""
rep("/* ---------- documents ---------- */", set_js, 1)

# --- document page and cards show the Set v15 file
rep("""    <p class="lede">${esc(d.folder)} / ${esc(d.file)} · ${d.secs.length} section${d.secs.length===1?'':'s'}</p>`+""",
    """    <p class="lede">${esc(d.folder)} / ${esc(d.file)} · ${d.secs.length} section${d.secs.length===1?'':'s'}</p>`+
    (d.nf?`<p class="lede"><b>Document set v15:</b> ${esc(d.nf)}
      <button class="dl" data-set="${esc(setFolder(d.nf))}" style="margin:0 0 0 8px">See that folder in Set v15</button></p>`:``)+""")

rep("""  b.scrollTop=0; wireFile();
  if(anchor!=null){const el=document.getElementById('s'+anchor); if(el) el.scrollIntoView();}""",
    """  b.scrollTop=0; wireFile();
  b.querySelectorAll('.dl[data-set]').forEach(x=>x.onclick=()=>{go('__set');sideSet(x.dataset.set);bodySet(x.dataset.set);});
  if(anchor!=null){const el=document.getElementById('s'+anchor); if(el) el.scrollIntoView();}""")

rep("""       <div class="m">${esc(d.inzip?d.file:d.file)} · ${d.secs.length} section${d.secs.length===1?'':'s'}</div></div>`).join('')+`</div>`;""",
    """       <div class="m">${esc(d.inzip?d.file:d.file)} · ${d.secs.length} section${d.secs.length===1?'':'s'}</div>
       ${d.nf?`<div class="m"><b>Set v15:</b> ${esc(d.nf.split('/').pop())}</div>`:``}</div>`).join('')+`</div>`;""")

rep("""    <p class="lede">${ds.length} document${ds.length===1?'':'s'}. The text is here and searchable; the original file downloads from the page.</p>""",
    """    <p class="lede">${ds.length} document${ds.length===1?'':'s'}. The text is here and searchable; the original file downloads from the page.
      Where the microservice realignment wrote a new version, the Set v15 file is named on the card and on the document page.</p>""")

# --- home page: the label, what changed, change-log row
rep("""   <h1>Recovery Workbench, for the squads</h1>
   <p class="lede">Everything the build needs, in one file. No network, no sign-in.</p>""",
    """   <h1>Recovery Workbench, for the squads</h1>
   <p class="lede">Everything the build needs, in one file. No network, no sign-in. Document set v15.</p>
   <h2>What this version is</h2>
   <p>This is the v15 of the project hub, and the label for the whole set is <b>Document set v15</b>. It keeps every story,
      document, code, number and date of the previous hub, and adds the links to the files the D-RCV-60 microservice
      realignment wrote: 19 services (P1 to P10, S1 to S9) with their own schema, login, REST base, topic and task queue,
      the reissued requirements, architecture and test documents, and the service story files. The
      <b>Set v15</b> tab lists every new file by folder, and each document page names its Set v15 file.</p>
   <table><thead><tr><th style="width:74px">Version</th><th style="width:140px">Date</th><th>Change log</th></tr></thead><tbody>
    <tr><td data-l="Version">v15</td><td data-l="Date">22 November 2026</td>
        <td data-l="Change log">D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash</td></tr>
   </tbody></table>""")

rep("""    <tr><td data-l="Tab">Original files</td><td data-l="What it holds">The Word, PowerPoint, Excel and PDF files themselves, to download.</td></tr>""",
    """    <tr><td data-l="Tab">Original files</td><td data-l="What it holds">The Word, PowerPoint, Excel and PDF files themselves, to download.</td></tr>
    <tr><td data-l="Tab">Set v15</td><td data-l="What it holds">Every new and next-version file written by the D-RCV-60 realignment, by folder.</td></tr>""")

# --- epic plan: state that the dates are tentative (rule 10)
rep("""    <p class="lede">Each epic closes at a month end. Click a count to work in that epic.</p>""",
    """    <p class="lede">Each epic closes at a month end. Click a count to work in that epic.
      Every release date is tentative and is copied unchanged from the source documents.</p>""")

DST.write_text(out, encoding='utf-8')
print('written', DST, DST.stat().st_size)

# sanity: payload round trip
chk = re.search(r'<script type="application/octet-stream" id="payload">([^<]*)</script>', out)
Mj = json.loads(zlib.decompress(base64.b64decode(chk.group(1)), 16 + zlib.MAX_WBITS).decode('utf-8'))
print('roundtrip docs', len(Mj['docs']), 'setfiles', len(Mj['setfiles']))
print('scripts', out.count('<script'))
