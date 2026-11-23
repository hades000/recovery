import json, re
from pathlib import Path

wp = Path('_work/msr/wp/B2-P7-004.md')
t = wp.read_text(encoding='utf-8')
blk = t.split('Write only:', 1)[1].split('\nDo', 1)[0]
allowed = [l[2:].split(' (')[0].strip() for l in blk.splitlines() if l.startswith('- ')]
log = Path('_work/msr/editlog/B2-P7-004.md').read_text(encoding='utf-8')
pat = re.compile(r"(?m)^\s*[-*]\s+`?([^`\n]+?\.(?:md|json|jsonl|xlsx|docx|pptx|yaml|sql|svg|excalidraw))`?\s*$")
ms = pat.findall(log)
print('log refs', len(ms))
for m in ms:
    ok = any(m.replace('\\', '/').startswith(a.rstrip('/')) for a in allowed)
    print('ok ' if ok else 'BAD', m)

# story checks
p = Path('04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2035 APP Next action on the case v1.md')
s = p.read_text(encoding='utf-8')
ids = set()
for k in ('gaps', 'assumptions'):
    for line in Path('_work/msr/%s/B2-P7-004.jsonl' % k).read_text(encoding='utf-8').splitlines():
        if line.strip():
            ids.add(json.loads(line)['id'])
cite = set(re.findall(r'\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b', s))
print('cites', len(cite), 'missing', sorted(cite - ids))
print('AC lines', len(re.findall(r'(?m)^\s*Scenario: AC\d+', s)))
print('bytes', p.stat().st_size)
frag = json.loads(Path('_work/msr/fragments/RWB-P7-E2035-APP.json').read_text(encoding='utf-8'))
print('frag ids exist', frag['file'] == str(p.as_posix()).replace('04 User stories', '04 User stories'))
print('frag file ok', Path(frag['file']).exists())
