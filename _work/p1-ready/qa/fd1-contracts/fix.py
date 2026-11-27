"""Restore the original row order of the P3 operation table; compare operation lists with the specs."""
import glob
import os

import openpyxl
import yaml

from ed import API, STAGE

MD = os.path.join(STAGE, '05 Technical architecture/Recovery Workbench Service Contract Catalog v3.md')
raw = open(MD, 'rb').read()
EOL = '\r\n' if b'\r\n' in raw else '\n'
lines = raw.decode('utf-8').split(EOL)
a = next(i for i, l in enumerate(lines) if l.startswith('## 6.3 '))
b = next(i for i, l in enumerate(lines) if l.startswith('## 6.4 '))
moved = [i for i in range(a, b) if lines[i].startswith(('| GET /cases/closure-dates |', '| GET /cases/retention-exclusions |'))]
assert len(moved) == 2
rows = {lines[i].split('|')[1].strip(): lines[i] for i in moved}
for i in reversed(moved):
    del lines[i]
h = next(i for i in range(a, b) if lines[i].startswith('**REST operations owned'))
end = next(i for i in range(h, b) if lines[i].startswith('| Operation |'))
while lines[end].startswith('|'):
    end += 1
lines[end:end] = [rows['GET /cases/retention-exclusions'], rows['GET /cases/closure-dates']]
open(MD, 'wb').write(EOL.join(lines).encode('utf-8'))

M = ('get', 'put', 'post', 'patch', 'delete')
ops = set()
for f in glob.glob(os.path.join(STAGE, API, '*.yaml')):
    d = yaml.safe_load(open(f, encoding='utf-8'))
    code = d.get('x-service', {}).get('code', 'PLT')
    for p, v in (d.get('paths') or {}).items():
        ops |= {(m.upper() + ' ' + p, code) for m in v if m in M}
wb = openpyxl.load_workbook(os.path.join(STAGE, '05 Technical architecture/Recovery Workbench Service Contract Catalog v3.xlsx'))
sheet = {(r[0], r[1]) for r in wb['REST operations'].iter_rows(min_row=2, values_only=True) if r[0]}
print('spec', len(ops), 'sheet', len(sheet))
print('missing in sheet', sorted(ops - sheet))
print('extra in sheet', sorted(sheet - ops))
