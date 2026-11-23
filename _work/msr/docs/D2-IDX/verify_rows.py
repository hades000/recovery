import io, re

def rows(path):
    out = {}
    for line in io.open(path, encoding='utf-8').read().splitlines():
        if line.startswith('| ') and line.count('|') == 6:
            c = [x.strip() for x in line.strip().strip('|').split('|')]
            if re.match(r'^\d+$', c[0]):
                out[c[0]] = c
    return out

a = rows('12 Project communication/Recovery Workbench Document Index v13.md')
b = rows('12 Project communication/Recovery Workbench Document Index v14.md')
print('v13 rows', len(a), 'v14 rows', len(b))
missing = [k for k in a if k not in b]
print('missing source rows:', missing)
changed_text = [k for k in a if k in b and a[k][1:4] != b[k][1:4]]
print('rows with changed document/what/standard:', changed_text)
new = [k for k in b if k not in a]
print('new rows:', new)
print('duplicate numbers in v14:', [k for k in b if list(b).count(k) > 1][:5])
# sources files changed count
fch = [k for k in a if k in b and a[k][4] != b[k][4]]
print('files changed on', len(fch), 'rows')
print('unchanged files rows', len(a) - len(fch))
