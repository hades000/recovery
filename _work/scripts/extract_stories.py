import csv
import io
import re
import openpyxl

REMOVED = {
    'loan_account', 'account_payment', 'party', 'contact_point', 'collateral', 'account_collateral',
    'collections_history', 'party_product', 'valuation', 'score',
    'load_run', 'dq_exception', 'dq_rule', 'source_field_map', 'source_code_map',
    'interface_run', 'interface_signoff', 'tracker_inventory', 'tracker_row',
}
LOAD_WORDS = re.compile(r'\b(load|feed|file drop|extract|tracker|source system|COLLINS|SVAF|CCMS|AMIS|RPS|WIN|GL|EFS)\b', re.I)

sources = [
    ('E1', r'04 User stories\Recovery Workbench User Stories Epic 1 v7.xlsx'),
    ('E2', r'04 User stories\Recovery Workbench User Stories Epic 2 v5.xlsx'),
    ('E38', r'04 User stories\Recovery Workbench User Stories Epics 3 to 8 v2.xlsx'),
    ('TE', r'04 User stories\Recovery Workbench Technical Enabler Stories v5.xlsx'),
    ('AD', r'04 User stories\Recovery Workbench Administration Stories v2.xlsx'),
    ('DM', r'04 User stories\Recovery Workbench Data Migration Stories v2.xlsx'),
]

out = []
for fam, path in sources:
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb['Stories']
    # header row is 4
    hdr = [str(c.value).strip() if c.value else '' for c in ws[4]]
    idx = {h: i for i, h in enumerate(hdr)}
    for row in ws.iter_rows(min_row=5, values_only=True):
        key = row[idx['Key']]
        if not key or not str(key).startswith('RWB-'):
            continue
        ents = str(row[idx['Entities']] or '')
        title = str(row[idx['Title']] or '')
        out.append((fam, key, title, ents))

with io.open(r'_work\data\stories.csv', 'w', encoding='utf-8', newline='',) as f:
    w = csv.writer(f)
    w.writerow(['family', 'key', 'title', 'entities'])
    w.writerows(out)

from collections import Counter
print(Counter(o[0] for o in out))
hits = 0
for fam, key, title, ents in out:
    names = {e.strip() for e in ents.split(',') if e.strip()}
    inter = names & REMOVED
    if inter:
        hits += 1
print('stories referencing removed tables:', hits)
for fam, key, title, ents in out:
    names = {e.strip() for e in ents.split(',') if e.strip()}
    inter = names & REMOVED
    if inter:
        print(key, '|', title[:60], '|', ','.join(sorted(inter)))
