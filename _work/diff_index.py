import re
ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication'
row_re = re.compile(r'^\| (\d+) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|$')

def load(p):
    d = {}
    for line in open(p, encoding='utf-8').read().split('\n'):
        m = row_re.match(line)
        if m:
            d[int(m.group(1))] = m.groups()[1:]
    return d

a = load(ROOT + r'\Recovery Workbench Document Index v11.md')
b = load(ROOT + r'\Recovery Workbench Document Index v12.md')
print('v11 rows', len(a), 'v12 rows', len(b), 'new ids', sorted(set(b) - set(a)), 'lost', sorted(set(a) - set(b)))
dc = [i for i in a if a[i][0] != b[i][0]]
ds = [i for i in a if a[i][2] != b[i][2]]
dw = [i for i in a if a[i][1] != b[i][1]]
print('doc name changes', dc)
print('standard changes', ds)
print('description changes', dw)
