import re, glob, io

want = ['REQ-DRI-', 'REQ-ACA-', 'REQ-CWC-', 'REQ-RDF-', 'REQ-DCM-']
lines = []
for p in sorted(glob.glob(r'_work/msr/extract/Recovery Workbench Functional Specifications by Module v6/*.md')):
    t = io.open(p, encoding='utf-8').read()
    name = p.split('\\')[-1]
    for ln in t.split('\n'):
        s = ln.strip()
        if not s.startswith('|'):
            continue
        for w in want:
            if w in s:
                lines.append('[%s] %s' % (name, s))
                break
io.open(r'_work/msr/docs/B-REQ-PRD-PLT/req_rows.txt', 'w', encoding='utf-8').write('\n'.join(lines))
print(len(lines))
for l in lines:
    print(l[:400])
