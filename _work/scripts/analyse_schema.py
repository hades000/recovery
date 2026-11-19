import io
import re

p = r'06 Data\Recovery Workbench Physical Schema v4.sql'
txt = io.open(p, encoding='utf-8').read()
print('chars', len(txt), 'lines', txt.count('\n'))
tables = re.findall(r'CREATE TABLE (?:IF NOT EXISTS )?(?:recovery\.)?([a-z0-9_]+)', txt, re.I)
print('tables', len(tables))
print(', '.join(tables))
print()
fks = re.findall(r'REFERENCES\s+([a-z0-9_.]+)\s*\(([a-z0-9_]+)\)', txt, re.I)
print('FK count', len(fks))
from collections import Counter
c = Counter(t for t, _ in fks)
for k, v in c.most_common():
    print(v, k)
