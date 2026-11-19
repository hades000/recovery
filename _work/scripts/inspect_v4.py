import io, re
p = r'06 Data\Recovery Workbench Physical Schema v4.sql'
t = io.open(p, encoding='utf-8-sig').read()
lines = t.split('\n')
print('lines', len(lines))
# show section banners
for i, ln in enumerate(lines, 1):
    if ln.startswith('-- ') and len(ln) < 120 and not ln.startswith('-- Recovery case'):
        if i < 2600 or i > 4100:
            print(i, ln)
