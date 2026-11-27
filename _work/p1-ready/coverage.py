"""Coverage of review findings by P1 story edit logs. Usage: python -I coverage.py [agent ...]"""
import csv, glob, os, re, sys, collections
REV = r'C:\Users\SahilMore\Downloads\RWB Story Review P1\stories'
LOG = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\p1-ready\editlog'
agents = sys.argv[1:] or [os.path.basename(p)[:-4] for p in glob.glob(os.path.join(LOG, 'S*-stories.csv'))]
refs = collections.defaultdict(set)
for a in agents:
    p = os.path.join(LOG, a + '.csv')
    if not os.path.exists(p): continue
    for r in csv.DictReader(open(p, encoding='utf-8-sig')):
        for k, n in re.findall(r'(RWB-P1-[A-Z0-9]+-[A-Z]+)#(\d+)', r.get('finding_refs', '') or ''):
            refs[k].add(n)
for d in sorted(glob.glob(os.path.join(REV, 'RWB-P1-*'))):
    k = os.path.basename(d)
    if not k.endswith(('-APP', '-CON', '-OPS', '-DB')): continue
    f = glob.glob(os.path.join(d, '*findings.csv'))
    n = len(list(csv.DictReader(open(f[0], encoding='utf-8-sig')))) if f else 0
    c = len(refs.get(k, ()))
    if k in refs or not sys.argv[1:]:
        print(f'{k:22} findings {n:3} covered {c:3} {"SHALLOW" if n and c < 0.6 * n else ""}')
