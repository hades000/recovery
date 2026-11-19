import csv
import io
from collections import Counter, defaultdict

REMOVED = {
    'loan_account', 'account_payment', 'party', 'contact_point', 'collateral', 'account_collateral',
    'collections_history', 'party_product', 'valuation', 'score',
    'load_run', 'dq_exception', 'dq_rule', 'source_field_map', 'source_code_map',
    'interface_run', 'interface_signoff', 'tracker_inventory', 'tracker_row',
}
REMOVE_STORIES = {'RWB-E1-003', 'RWB-E1-004', 'RWB-E1-005', 'RWB-E1-006', 'RWB-E1-009',
                  'RWB-E1-010', 'RWB-E1-012', 'RWB-E1-051', 'RWB-E2-023', 'RWB-DM-001', 'RWB-DM-002'}
REWRITE = {
    # E1
    'RWB-E1-001', 'RWB-E1-002', 'RWB-E1-007', 'RWB-E1-011', 'RWB-E1-015', 'RWB-E1-016',
    'RWB-E1-018', 'RWB-E1-023', 'RWB-E1-037', 'RWB-E1-052', 'RWB-E1-056', 'RWB-E1-064', 'RWB-E1-065',
    # TE
    'RWB-TE-001', 'RWB-TE-004', 'RWB-TE-007',
    # E2
    'RWB-E2-001', 'RWB-E2-003', 'RWB-E2-007', 'RWB-E2-008', 'RWB-E2-010', 'RWB-E2-034',
    # E3-8
    'RWB-E4-002', 'RWB-E4-006', 'RWB-E3-010', 'RWB-E3-017', 'RWB-E4-046', 'RWB-E4-050',
    # AD
    'RWB-AD-018', 'RWB-AD-019',
    # DM
    'RWB-DM-005', 'RWB-DM-006', 'RWB-DM-011', 'RWB-DM-013',
}
MINOR_NAMED = {'RWB-E1-013', 'RWB-E1-017', 'RWB-E1-020', 'RWB-E1-028', 'RWB-E1-032', 'RWB-E1-043',
               'RWB-E1-044', 'RWB-E1-045', 'RWB-E1-055', 'RWB-E1-059', 'RWB-TE-011', 'RWB-AD-004'}

rows = list(csv.DictReader(io.open(r'_work\data\stories.csv', encoding='utf-8')))
counts = defaultdict(Counter)
dispo = []
for r in rows:
    fam, key, title, ents = r['family'], r['key'], r['title'], r['entities']
    names = {e.strip() for e in ents.split(',') if e.strip()}
    if key in REMOVE_STORIES:
        d = 'Remove'
    elif key in REWRITE:
        d = 'Rewrite'
    elif key in MINOR_NAMED or (names & REMOVED):
        d = 'Minor'
    else:
        d = 'No impact'
    counts[fam][d] += 1
    dispo.append((fam, key, d, title, ents))

for fam in ['E1', 'TE', 'E2', 'E38', 'AD', 'DM']:
    c = counts[fam]
    print(fam, dict(c), 'total', sum(c.values()))
print('all', dict(Counter(d[2] for d in dispo)))

with io.open(r'_work\data\story_disposition.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['family', 'key', 'disposition', 'title', 'entities'])
    for row in sorted(dispo, key=lambda x: (x[0], x[1])):
        w.writerow(row)
