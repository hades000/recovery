"""Dependency changes between each v2 story header and its staged v3 header."""
import glob, os, re, json, collections
import openpyxl
from w9lib import SET, STAGE

ID = re.compile(r'RWB-(?:[A-Z0-9]+-)+(?:APP|CON|DB|OPS|ITG|INF|UI|LIB|DEL)\b')
KIND = {'Depends on (build)': 'H', 'Contract dependencies': 'C', 'Integration dependencies': 'I',
        'External dependencies': 'E', 'Ready to start': 'R'}
US = '04 User stories'


def header(path):
    out = {}
    for line in open(path, encoding='utf-8').read().split('\n')[:60]:
        m = re.match(r'\|\s*(Story key|Story ID|Key|Depends on \(build\)|Contract dependencies|Integration dependencies|External dependencies|Ready to start)\s*\|(.*)\|', line)
        if m and m.group(1) not in out:
            out[m.group(1)] = m.group(2).strip()
    return out


wb = openpyxl.load_workbook(os.path.join(STAGE, US, 'Recovery Workbench Service Story Catalog v3.xlsx'))
stories = {}
cols = [c.value for c in wb['Stories'][1]]
for row in wb['Stories'].iter_rows(min_row=2, values_only=True):
    if row[0]:
        stories[row[0]] = dict(zip(cols, row))
bytitle = {}
for key, s in stories.items():
    if s['File']:
        bytitle[os.path.basename(str(s['File']).replace('\\', '/')).replace(' v2.md', '')] = key
cat = {}
for a, b, c in wb['Dependencies'].iter_rows(min_row=2, values_only=True):
    if a:
        cat[(a, b)] = c

changes = {}
unmatched = []
new_root = os.path.join(STAGE, US, 'Recovery Workbench Service Story Files v3')
old_root = os.path.join(SET, US, 'Recovery Workbench Service Story Files v2')
for path in glob.glob(os.path.join(new_root, '*', '*.md')):
    name = os.path.basename(path)[:-len(' v3.md')]
    folder = os.path.basename(os.path.dirname(path))
    old = os.path.join(old_root, folder, name + ' v2.md')
    key = bytitle.get(name)
    if key is None:
        m = re.match(r'RWB (\S+) (\S+) (APP|CON|DB|OPS|ITG|INF|UI|LIB|DEL) ', name)
        key = 'RWB-%s-%s-%s' % m.groups() if m else None
    if key not in stories or not os.path.exists(old):
        unmatched.append(name)
        continue
    h0, h1 = header(old), header(path)
    sets = []
    for h in (h0, h1):
        d = {}
        for field in ('Depends on (build)', 'Contract dependencies', 'Integration dependencies'):
            for t in ID.findall(h.get(field, '')):
                if t != key:
                    d.setdefault(t, KIND[field])
        sets.append(d)
    a, b = sets
    add = {t: k for t, k in b.items() if t not in a}
    rem = {t: k for t, k in a.items() if t not in b}
    move = {t: (a[t], b[t]) for t in a if t in b and a[t] != b[t]}
    changes[key] = dict(add=add, rem=rem, move=move, ready0=h0.get('Ready to start'), ready1=h1.get('Ready to start'),
                        folder=folder, new=b)

if __name__ == '__main__':
    print('staged story files', len(changes), 'unmatched', len(unmatched), unmatched[:5])
    n = collections.Counter()
    for key in sorted(changes):
        c = changes[key]
        add = {t: k for t, k in c['add'].items() if (key, t) not in cat}
        rem = {t: k for t, k in c['rem'].items() if (key, t) in cat}
        move = {t: v for t, v in c['move'].items() if (key, t) in cat and cat[(key, t)] != v[1]}
        if add or rem or move:
            n['stories'] += 1
            n['add'] += len(add)
            n['rem'] += len(rem)
            n['move'] += len(move)
            bad = [t for t in add if t not in stories]
            print(key, '+', {t[4:]: k for t, k in add.items()}, '-', {t[4:]: k for t, k in rem.items()},
                  '~', {t[4:]: (cat[(key, t)], v) for t, v in move.items()}, 'UNKNOWN %s' % bad if bad else '')
    print(n)
