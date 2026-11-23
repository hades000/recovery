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
changed = {k for k in a if a[k][4] != b[k][4]}
new = {k for k in b if k not in a}

t = io.open('12 Project communication/Recovery Workbench Document Index v14.md', encoding='utf-8').read()
sec = t.split('### Every new and next version', 1)[1].split('### Run material', 1)[0]
listed = re.findall(r'^\| (\d+) \|', sec, re.M)
print('listed', len(listed), 'changed+new', len(changed | new))
print('in table but not changed/new:', sorted(set(listed) - (changed | new)))
print('changed/new but not in table:', sorted((changed | new) - set(listed)))
