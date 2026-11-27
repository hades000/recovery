import csv, collections, os, re, zipfile
import openpyxl, docx
from w9lib import STAGE, LOGFILE
from docdiff2 import lines
x = lambda p: openpyxl.load_workbook(STAGE + '/' + p)
cat = x('04 User stories/Recovery Workbench Service Story Catalog v3.xlsx')
dm = x('11 Delivery and operations/Recovery Workbench Dependency Map v7.xlsx')
d = [r for r in cat['Dependencies'].iter_rows(min_row=2, max_col=3, values_only=True) if r[0]]
body = [r for r in dm['Story dependencies v5'].iter_rows(min_row=5, values_only=True) if r[0] and str(r[0]).startswith('RWB-')]
print('catalog deps', len(d), 'unique', len({(a, b) for a, b, c in d}), 'map rows', len(body), 'same', {(a, b, c) for a, b, c in d} == {(r[0], r[7], r[13]) for r in body})
bs = dm['By service and class']
print('by service All', [c.value for c in bs[26]][3:], 'wave all', [c.value for c in bs[35]][2:7], collections.Counter(c for a, b, c in d))
rm = dm['Read me']
for r in range(1, rm.max_row + 1):
    v = rm.cell(r, 1).value
    if v and re.search(r'rows|Day 1', str(v)) and r not in (16, 17, 18, 19, 20, 21, 23):
        print('  rm', r, str(v)[:200], '|', rm.cell(r, 2).value)
print('later-wave C', sum(1 for r in body if r[13] == 'C' and r[15] == 'Later wave'))
cp = x('05 Technical architecture/Recovery Workbench Service Catalog v2.xlsx')
om = x('22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v3.xlsx')
dl = x('01 Decisions and governance/Recovery Workbench Decision Log v13.xlsx')
for wb in (cat, dm, cp, om, dl):
    bad = [(ws.title, c.coordinate) for ws in wb for row in ws.iter_rows() for c in row if isinstance(c.value, str) and ('�' in c.value and 'W9' in c.value)]
    assert not bad, bad
# logged "after" text present
rows = list(csv.DictReader(open(LOGFILE, encoding='utf-8-sig')))
print('log rows', len(rows), 'ids unique', len({r['edit_id'] for r in rows}), collections.Counter(r['action'] for r in rows))
print(collections.Counter(os.path.basename(r['file'])[:70] for r in rows if r['action'] != 'REQUEST'))
for p in ['01 Decisions and governance/Recovery Workbench Decision Log v13.xlsx', '22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v3.xlsx',
          '04 User stories/Recovery Workbench Service Story Catalog v3.xlsx', '05 Technical architecture/Recovery Workbench Service Catalog v2.xlsx',
          '11 Delivery and operations/Recovery Workbench Dependency Map v7.xlsx', '09 Testing and quality/Recovery Workbench Definition of Ready and Done v5.docx',
          '11 Delivery and operations/Recovery Workbench Story Build Order v5.docx']:
    z = zipfile.ZipFile(STAGE + '/' + p)
    assert z.testzip() is None
    if p.endswith('docx'):
        docx.Document(STAGE + '/' + p)
    ver = [l for l in (lines(STAGE + '/' + p) if p.endswith('docx') else
                       [' | '.join(str(v) for v in r if v is not None) for ws in openpyxl.load_workbook(STAGE + '/' + p) if ws.title == 'Read me' for r in ws.iter_rows(values_only=True)])
           if '27 November 2026' in l and ('P1 developer readiness' in l)]
    print('OK', p.split('/')[-1], '| version row:', ver[:1])
md = open(STAGE + '/05 Technical architecture/Recovery Workbench Service Catalog v2.md', encoding='utf-8').read()
print('md version rows', md.count('D-RCV-60 P1 developer readiness'))
