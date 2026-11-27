import csv, pickle
csv.field_size_limit(10 ** 9)
LOG = 'editlog/TR-tests.csv'
rows = list(csv.reader(open(LOG, encoding='utf-8-sig')))
n = max(int(r[0].rsplit('-', 1)[1]) for r in rows[1:] if r and r[0].startswith('TR-tests-'))
MAP = pickle.load(open('qa/tr-tests/map.pkl', 'rb'))
TC = '09 Testing and quality/Recovery Workbench Test Cases v9.xlsx'
S = '04 User stories/Recovery Workbench Service Story Files v3'
req = [
 ('REQUEST', '05 Technical architecture/Recovery Workbench Technical Specifications by Module v7/Recovery Workbench TSD P1 Recovery data engine v6.md', 'Requirement trace test column',
  'It cites legacy test case IDs whose rwb-source-data case moved: ' + ', '.join('%s to %s' % (k, MAP[k]) for k in ['TC-E1-001-01', 'TC-E1-069-02', 'TC-E1-011-01', 'TC-E1-013-01', 'TC-E1-015-01', 'TC-E1-016-01', 'TC-E1-017-01', 'TC-E1-064-01']) + '. Repoint where the P1 case is meant. TSD P3 v5 (TC-E2-001-01) and TSD P6 v3 (TC-E2-021-01) need the same check.'),
 ('REQUEST', S + ' (rwb-source-data)', 'Section 16 prose that still says legacy',
  'Only test case ID tokens were changed. Reword the sentences that now call a TC-P1 ID legacy or say version 9 uses the legacy IDs: ACE001 DB, E1016 APP and CON, E1018 APP, E1064 APP, E1065 APP, E1066 CON and OPS, E1067 CON, E1069 DB, E2001 APP, E2007 APP, E2010 CON and OPS, E2021 APP, E2022 APP.'),
 ('REQUEST', S + ' (other services)', 'References that meant the rwb-source-data case',
  'RWB-ITG-E1065-ITG line 378 (TC-E1-065-03 test migration) is now %s; RWB-P5-E1016-APP row TC-E1-016-12 says run by RWB-P1-E1016-APP, whose case is now %s.' % (MAP['TC-E1-065-03'], MAP['TC-E1-016-12'])),
 ('REQUEST', TC, 'Restored version 8 rows with superseded behaviour',
  'Legacy rows are restored to version 8 text. Several describe behaviour later removed (data lake and Power BI under DP-17, case list in P1 under RD-P1-024), for example TC-E1-013-03, TC-E1-013-07, TC-E1-002-11, TC-E1-011-05. Each citing service restates its own case when it is made developer ready (NEW-GAP-W2-tests-7).'),
 ('REQUEST', '23 Document Gaps (registers)', 'NEW-GAP-W2-tests-7 scope',
  '134 IDs (246 section 16 citations in non-rwb-source-data service stories) that version 9 had given to rwb-source-data cases are now free and have no row, as in version 8; add them to NEW-GAP-W2-tests-7. Gap, assumption and cross-document change register entries that cite a moved ID are history; the mapping is in _work/p1-ready/qa/tr-tests/id-map.csv.'),
]
out = []
for a, f, sec, text in req:
    n += 1
    out.append(['TR-tests-%04d' % n, a, f, 'v9', 'v9', sec, '', text, '', '', 'NEW-GAP-W2-tests-7' if 'W2-tests-7' in text else '', 'claude-sonnet-5-5', 'TR-tests'])
with open(LOG, 'a', encoding='utf-8', newline='') as fh:
    csv.writer(fh, quoting=csv.QUOTE_ALL).writerows(out)
import openpyxl
wb = openpyxl.load_workbook('stage/' + TC, read_only=True)
tc = {r[0]: r for r in list(wb['Story test cases'].iter_rows(values_only=True))[4:] if r and r[0]}
C1, C2, _ = pickle.load(open('qa/tr-tests/sets.pkl', 'rb'))
with open('qa/tr-tests/id-map.csv', 'w', encoding='utf-8', newline='') as fh:
    w = csv.writer(fh, quoting=csv.QUOTE_ALL)
    w.writerow(['old_id', 'new_p1_id', 'p1_story', 'p1_status', 'old_id_now'])
    for k in sorted(MAP):
        v = MAP[k]
        now = 'v8 row restored' if k in C1 else ('row of ' + str(tc[k][15]) if k in tc else 'no row')
        w.writerow([k, v, tc[v][15], tc[v][12], now])
all_ = list(csv.reader(open(LOG, encoding='utf-8-sig')))[1:]
ids = [r[0] for r in all_]
import collections
print('log rows', len(all_), 'unique', len(set(ids)), 'bad width', sum(len(r) != 13 for r in all_), collections.Counter(r[1] for r in all_))
print('p1 story citation edits', sum(r[1] == 'EDIT' and r[2].startswith('04 ') for r in all_), 'trace', sum(r[5].startswith('Criterion trace') for r in all_), 'rtm req', sum(r[5].startswith('RTM ') for r in all_), 'backfill', sum(r[2] == 'tc-backfill.csv' for r in all_))
