import io
import re

p = r'06 Data\Recovery Workbench Physical Schema v4.sql'
txt = io.open(p, encoding='utf-8').read()

for tbl in ['sys_objects', 'data_product', 'sys_fields', 'lov_value', 'job_catalog', 'interface_config']:
    ins = re.findall(r'INSERT INTO %s \((.*?)\)\s*VALUES' % tbl, txt)
    print(tbl, 'insert statements:', len(ins))
    if ins:
        print('  columns:', ins[0])

# count total inserted rows per table via INSERT ... VALUES (...),(...);
m = re.findall(r'INSERT INTO (\w+) \((.*?)\)\s*VALUES\s*(.*?);\s*\n', txt, re.S)
from collections import Counter
c = Counter()
for tbl, cols, vals in m:
    c[tbl] += vals.count('),(') + 1
for k, v in sorted(c.items()):
    print('rows', v, k)
