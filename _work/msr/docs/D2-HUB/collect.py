import re, json
from pathlib import Path

ROOT = Path('.').resolve()
logs = sorted(Path('_work/msr/editlog').glob('*.md'))
files = {}
for lg in logs:
    if lg.name.startswith('SMOKE') or lg.name.startswith('A6'):
        continue
    t = lg.read_text(encoding='utf-8')
    if '## Files written' not in t:
        continue
    blk = t.split('## Files written', 1)[1].split('\n## ', 1)[0]
    for m in re.finditer(r'(?m)^\s*[-*]\s+`([^`]+\.(?:md|docx|xlsx|pptx|yaml|sql|json|html|svg|excalidraw|zip|txt))`', blk):
        p = m.group(1).replace('\\', '/').strip()
        if p.startswith('_work/'):
            continue
        files.setdefault(p, set()).add(lg.stem)

print('files', len(files))
byfolder = {}
for p in files:
    f = p.rsplit('/', 1)[0] if '/' in p else '(root)'
    byfolder.setdefault(f, []).append(p)
for f in sorted(byfolder):
    print(f, len(byfolder[f]))
missing = [p for p in files if not (Path(p)).exists()]
print('missing on disk', len(missing))
for p in missing[:20]:
    print(' M', p)
json.dump({p: sorted(v) for p, v in files.items()}, open(r'_work\msr\docs\D2-HUB\setfiles.json', 'w'), indent=1)
