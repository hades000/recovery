"""Assemble the v16 hub: current payload, current resources, same viewer."""
import base64
import gzip
import io
import json
import os
import re
import sys

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14'
SRC = os.path.join(ROOT, '14 Story Updates', 'Recovery Workbench Project Hub v15.html')
OUT = os.path.join(ROOT, '14 Story Updates', 'Recovery Workbench Project Hub v16.html')
DATA = os.path.join(ROOT, '_work', 'data')


def replace_json_const(html, name, obj):
    key = 'const ' + name + '='
    idx = html.index(key)
    start = idx + len(key)
    assert html[start] == '{', (name, html[start:start + 20])
    depth, i, in_str, esc = 0, start, False, False
    while i < len(html):
        ch = html[i]
        if in_str:
            if esc:
                esc = False
            elif ch == '\\':
                esc = True
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    break
        i += 1
    end = i
    return html[:idx] + key + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + html[end + 1:]


def replace_body_start(html):
    start = html.index('function bodyStart(){')
    end = html.index('\nfunction bodyPlan', start)
    new = r'''function bodyStart(){
  const n=k=>Object.values(M.ids).filter(v=>v.k===k).length;
  document.querySelector('.body').innerHTML=`
   <h1>Recovery Workbench, for the squads</h1>
   <p class="lede">Everything the build needs, in one file. No network, no sign-in.
      <b>Version 16, 15 November 2026:</b> the ACE re-base. Source data is read from 30
      <code>recovery.v_ace_*</code> views; there are no inbound loads in the Workbench.</p>
   <h2>Start from a story</h2>
   <p>The <b>Stories by epic</b> tab lists the epics, and each epic opens its stories. Pick one and the whole story
      opens on the right: the attributes, every section, and then the full wording of every code it names.
      The developer action plan is section 13 of every story: what to build, in what order, and how you know it is done.</p>
   <h2>What changed in this version</h2>
   <p>The eight inbound load stories (E1-003, 004, 005, 006, 009, 010, 012 and 051) and the EFS load story E2-023 are gone.
      ACE ingests the source data. Their basic "file arrived" and "row loaded" acceptance criteria, which confused
      developers about what the Workbench builds, are gone with them. What remains in section 7 of a story is the
      behaviour the developer must build; access and delivery checks live in the test plan and the pipeline.</p>
   <h2>A code opens where you are standing</h2>
   <p>Any coloured code in a story is clickable. It opens a box under that line carrying the rule itself and the whole
      section it was written in. Nothing else has to be opened to read it. Use
      <b>Open every reference on this page</b> at the top of a story to expand all of them at once.</p>
   <h2>Click any underlined word, not just the codes</h2>
   <p>A story names things without explaining them. On this page each of those opens where it stands.</p>
   <table><thead><tr><th style="width:200px">What you click</th><th>What opens</th></tr></thead><tbody>
    <tr><td data-l="What you click">A table or view name such as <span class="rx" data-k="table" data-v="v_ace_account">v_ace_account</span></td>
        <td data-l="What opens">What the object is for, every column with its type and meaning, its foreign keys, its indexes and any trigger. Read from Physical Schema v5.</td></tr>
    <tr><td data-l="What you click">A column name such as <span class="rx" data-k="column" data-v="days_past_due">days_past_due</span></td>
        <td data-l="What opens">What the column means, its type, and every table or view that holds it, each one clickable.</td></tr>
    <tr><td data-l="What you click">A count such as <span class="rx num" data-k="set" data-v="tables92">92 tables</span> or <span class="rx num" data-k="set" data-v="fields1366">1,366 fields</span></td>
        <td data-l="What opens">The actual list behind the number, so you never have to go looking for which ones they are.</td></tr>
    <tr><td data-l="What you click">An endpoint such as <span class="rx" data-k="endpoint" data-v="GET /api/recovery/v1/cases">GET /cases</span></td>
        <td data-l="What opens">Its full path, what it does, the permission it needs, the epic it is built in and the responses it returns.</td></tr>
    <tr><td data-l="What you click">A document named in the text, such as Recovery Workbench Physical Schema v5.sql</td>
        <td data-l="What opens">Which folder it is in, a button to open it here, and a button to download the original file.</td></tr>
    <tr><td data-l="What you click">The actor on a flow step, such as <span class="rx" data-k="actor" data-v="Pipeline">Pipeline</span></td>
        <td data-l="What opens">Whether it is a person or automation, and who does it.</td></tr>
   </tbody></table>
   <h2>What the codes mean</h2>
   <table><thead><tr><th style="width:120px">Prefix</th><th>Meaning</th><th style="width:80px">Count</th></tr></thead><tbody>
   ${ORDER.filter(k=>M.kinds[k]&&n(k)).map(k=>`<tr><td data-l="Prefix"><code class="id k${k.replace(/-/g,'')}">${esc(k)}</code></td>
      <td data-l="Meaning">${esc(M.kinds[k])}</td><td data-l="Count">${n(k)}</td></tr>`).join('')}
   </tbody></table>
   <h2>The rest of the tabs</h2>
   <table><thead><tr><th style="width:190px">Tab</th><th>What it holds</th></tr></thead><tbody>
    <tr><td data-l="Tab">Epic plan</td><td data-l="What it holds">The eight epics, what each one delivers and when it releases.</td></tr>
    <tr><td data-l="Tab">Documents</td><td data-l="What it holds">Every document in the set, by folder, with its text searchable.</td></tr>
    <tr><td data-l="Tab">Codes</td><td data-l="What it holds">Every requirement, rule, field and message as a list, by family.</td></tr>
    <tr><td data-l="Tab">Original files</td><td data-l="What it holds">The Word, PowerPoint, Excel and PDF files themselves, to download.</td></tr>
   </tbody></table>
   <p class="lede" style="margin-top:16px">Search box at the top, or press <b>/</b>, runs across every document.
      Typing a code takes you straight to it.</p>`;
  document.querySelector('.body').scrollTop=0;
}
'''
    return html[:start] + new + html[end:]


def main():
    payload = json.load(io.open(os.path.join(DATA, 'hub_payload.json'), encoding='utf-8'))
    res = json.load(io.open(os.path.join(DATA, 'hub_res.json'), encoding='utf-8'))
    misc = json.load(io.open(os.path.join(DATA, 'hub_misc.json'), encoding='utf-8'))
    blobs = json.load(io.open(os.path.join(DATA, 'hub_blobs.json'), encoding='utf-8'))

    html = io.open(SRC, encoding='utf-8').read()

    html = html.replace('<title>Recovery Workbench project hub</title>',
                        '<title>Recovery Workbench project hub v16</title>')
    html = html.replace('<div class="brand">Recovery Workbench</div>',
                        '<div class="brand">Recovery Workbench <span style="font-weight:400;color:var(--soft)">v16</span></div>')
    html = html.replace("src:'Physical Schema v4'", "src:'Physical Schema v5'")
    html = html.replace("src:'API Specification v2'", "src:'API Specification v3'")

    for name, obj in [('TH', misc['TH']), ('RES', res), ('NOTES', misc['NOTES']),
                      ('TERMS', misc['TERMS']), ('DEC', misc['DEC']), ('SIMPLE', misc['SIMPLE'])]:
        html = replace_json_const(html, name, obj)

    # counts that the viewer links to their lists
    old_setrx = re.search(r'const SETRX=\[.*?\n\];', html, re.S)
    if not old_setrx:
        raise SystemExit('SETRX not found')
    new_setrx = r'''const SETRX=[
  [/\b92 tables\b/g,'tables92'],[/\b88 (?:Workbench )?tables\b/g,'tables92'],
  [/\b1,366 (?:fields|sys_fields rows)\b/g,'fields1366'],[/\b1366\b(?= fields)/g,'fields1366'],
  [/\b122 (?:sys_objects rows|objects|entities)\b/g,'objects122'],
  [/\b30 (?:read-only )?(?:ACE )?views\b/g,'views30'],
  [/\b14 data[_ ]products?\b/g,'products14'],[/\bDP01 to DP14\b/g,'products14'],
  [/\b7 standard columns\b/g,'standard7'],[/\bseven standard columns\b/g,'standard7'],
  [/\b\d+ foreign keys\b/g,'fk'],[/\b\d+ indexes\b/g,'idx'],
  [/\bappend-only triggers\b/g,'trig']
];'''
    html = html[:old_setrx.start()] + new_setrx + html[old_setrx.end():]

    html = html.replace(
        "const ORDER=['REQ','BR'",
        "const ORDER=['REQ','D-RCV','BR'")
    html = html.replace(
        "const FAM=[['RWB-AD'",
        "const FAM=[['RWB-ACE','ACE team stories','The ACE team contract that unblocks the recovery read path'],\n           ['RWB-AD'")
    html = html.replace('.kDL,.kDT,.kDEV{', '.kDL,.kDT,.kDEV,.kDRCV{')

    html = html.replace(
        "      const m=rx.exec(s.h.trim());\n      if(!m) return;\n      const ea=attr(s.t,'Epic').match(/E\\d/);",
        "      const m=rx.exec(s.h.trim());\n      if(!m) return;\n      const sk=attr(s.t,'Story key');\n      if(sk && sk!==m[1]) return;\n      if(!sk && !attr(s.t,'Module')) return;\n      if(/^removed/i.test(attr(s.t,'Status'))) return;\n      const ea=attr(s.t,'Epic').match(/E\\d/);")

    html = html.replace("h=h.replace(/\\*\\*([^*]+)\\*\\*/g,'<b>$1</b>');",
                        "h=h.replace(/\\*\\*(.+?)\\*\\*/g,'<b>$1</b>');")
    html = html.replace(
        '`<button class="dl" id="openall">Open every reference on this page</button>`+',
        '`<button class="dl" id="openall">Open every reference on this page</button>`+\n    `<button class="dl" id="jump-plan">Developer actions (section 13)</button>`+')
    html = html.replace(
        "  document.getElementById('openall').onclick=()=>{\n    b.querySelectorAll('code.id').forEach(c=>{ if(!c.closest('.def')) inlineDef(c,true); });};",
        "  document.getElementById('openall').onclick=()=>{\n    b.querySelectorAll('code.id').forEach(c=>{ if(!c.closest('.def')) inlineDef(c,true); });};\n  const jp=document.getElementById('jump-plan');\n  if(jp) jp.onclick=()=>{const h=Array.from(b.querySelectorAll('h3')).find(x=>/Solution plan/i.test(x.textContent)); if(h) h.scrollIntoView({block:'start'});};")

    html = replace_body_start(html)

    # payload
    raw = json.dumps(payload, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    b64 = base64.b64encode(gzip.compress(raw, 9, mtime=0)).decode('ascii')
    html = re.sub(r'(<script type="application/octet-stream" id="payload">).*?(</script>)',
                  lambda m: m.group(1) + b64 + m.group(2), html, count=1, flags=re.S)

    # file blobs: replace the whole contiguous run
    first = html.index('<script type="application/octet-stream" id="f0">')
    last_start = html.rindex('<script type="application/octet-stream" id="f')
    last_end = html.index('</script>', last_start) + len('</script>')
    block = '\n'.join('<script type="application/octet-stream" id="f%d">%s</script>' % (i, b)
                      for i, b in enumerate(blobs))
    html = html[:first] + block + html[last_end:]

    io.open(OUT, 'w', encoding='utf-8', newline='\n').write(html)
    print('wrote', OUT, round(os.path.getsize(OUT) / 1048576, 2), 'MB')
    print('payload b64 MB', round(len(b64) / 1048576, 2), 'blobs', len(blobs))


if __name__ == '__main__':
    main()
