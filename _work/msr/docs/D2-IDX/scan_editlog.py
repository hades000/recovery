import re, glob, os, json

EXT = r'(?:md|docx|pptx|xlsx|zip|yaml|sql|svg|html|csv|excalidraw|json|py|txt|png|pdf)'
rows = {}
for p in sorted(glob.glob('_work/msr/editlog/*.md')):
    t = open(p, encoding='utf-8', errors='replace').read()
    wp = os.path.basename(p)[:-3]
    m = re.search(r'^#+\s*Files written\s*$(.*?)(?=^#+ |\Z)', t, re.S | re.M)
    if not m:
        m = re.search(r'Files written[:\s]*(.*?)(?=\n## |\Z)', t, re.S)
    sec = m.group(1) if m else ''
    paths = []
    for line in sec.splitlines():
        s = line.strip()
        if not s.startswith(('-', '*')):
            continue
        s = s.lstrip('-* ').strip()
        bt = re.findall(r'`([^`]+)`', s)
        cand = bt if bt else [s]
        for c in cand:
            c = c.strip().rstrip(',;.')
            if re.search(r'\.' + EXT + r'$', c) and ' / ' not in c:
                paths.append(c)
    out = [x for x in paths if not x.startswith('_work/')]
    rows[wp] = out

json.dump(rows, open('_work/msr/docs/D2-IDX/editlog_files.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
allw = list(rows)
zero = [w for w in allw if not rows[w]]
print('editlogs', len(allw), 'zero', len(zero), zero[:40])
