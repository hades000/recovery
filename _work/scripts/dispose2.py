import csv
import io
import re
import openpyxl

sources = [
    ('E1', r'04 User stories\Recovery Workbench User Stories Epic 1 v7.xlsx'),
    ('E2', r'04 User stories\Recovery Workbench User Stories Epic 2 v5.xlsx'),
    ('E38', r'04 User stories\Recovery Workbench User Stories Epics 3 to 8 v2.xlsx'),
    ('TE', r'04 User stories\Recovery Workbench Technical Enabler Stories v5.xlsx'),
    ('AD', r'04 User stories\Recovery Workbench Administration Stories v2.xlsx'),
    ('DM', r'04 User stories\Recovery Workbench Data Migration Stories v2.xlsx'),
]
PAT = re.compile(r'(JOB-\d\d|INT-\d\d|tracker|load_run|load run|dq_exception|dq_rule|source_field_map|source_code_map|interface_run|interface_signoff|file load|daily load|load(ed)? from|extract load|ALS load|EFS load|CCMS load|SVAF load|AMIS load|RPS load|WIN load|GL load|COLLINS load)', re.I)
out = {}
for fam, path in sources:
    wb = openpyxl.load_workbook(path, data_only=True)
    if 'Acceptance criteria' not in wb.sheetnames:
        continue
    ws = wb['Acceptance criteria']
    for row in ws.iter_rows(min_row=5, values_only=True):
        if row[0] and str(row[0]).startswith('RWB-'):
            hits = sorted({m.group(0).lower() for m in PAT.finditer(str(row[2] or ''))})
            out[str(row[0])] = (fam, hits)

csvrows = list(csv.DictReader(io.open(r'_work\data\story_disposition.csv', encoding='utf-8')))
up = []
for r in csvrows:
    fam, hits = out.get(r['key'], (r['family'], []))
    if r['disposition'] == 'No impact' and hits:
        r['disposition'] = 'Minor'
        r['entities'] = (r['entities'] + ' || load words: ' + ','.join(hits)).strip(' |')
    up.append(r)
with io.open(r'_work\data\story_disposition.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['family', 'key', 'disposition', 'title', 'entities'])
    for r in up:
        w.writerow([r['family'], r['key'], r['disposition'], r['title'], r['entities']])

from collections import Counter, defaultdict
c = defaultdict(Counter)
for r in up:
    c[r['family']][r['disposition']] += 1
for fam in ['E1', 'TE', 'E2', 'E38', 'AD', 'DM']:
    print(fam, dict(c[fam]), sum(c[fam].values()))
print('all', dict(Counter(r['disposition'] for r in up)))
