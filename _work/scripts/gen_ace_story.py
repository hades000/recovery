# -*- coding: utf-8 -*-
"""Generate RWB-ACE-001 (md and xlsx) from the frozen gap list."""
import csv
import io
import re
from collections import OrderedDict
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

FIELDS = [f for f in csv.DictReader(io.open(r'_work\data\fields.csv', encoding='utf-8'))
          if f['Disposition'] == 'ACE new']
probe = io.open(r'_work\sql\ace_tier2_probe.sql', encoding='utf-8').read()

# parse table columns
tables = OrderedDict()
for m in re.finditer(r'CREATE TABLE public\.([a-z_]+) \((.*?)\n\);', probe, re.S):
    name = m.group(1)
    cols = []
    for line in m.group(2).split('\n'):
        line = line.strip().rstrip(',')
        if not line or line.lower().startswith('constraint'):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        col, typ = parts[0], parts[1]
        cols.append((col, typ,
                     'NO' if 'not null' in line else 'YES',
                     'PK' if 'primary key' in line else ('FK' if 'references' in line else '')))
    tables[name] = cols
alter = [(m.group(1), m.group(2), m.group(3)) for m in
         re.finditer(r'ALTER TABLE public\.([a-z_]+)\s+ADD COLUMN ([a-z_]+) ([a-z0-9_(),]+);', probe)]

FREQ = {'ALS': 'Daily, end of day', 'SCBPDM': 'Daily, end of day', 'EFS': 'Daily, end of day',
        'CCMS': 'Weekly', 'SVAF': 'Weekly', 'AMIS': 'Monthly', 'RPS': 'Weekly', 'LIT': 'Daily, end of day',
        'WIN': 'Weekly', 'GL': 'Monthly', 'COLLINS': 'Daily, end of day', 'NLEADS': 'On decision',
        'EasyApp': 'On request', 'Entra ID': 'On change'}
TABLE_SRC = {'ace_batch_run': 'All sources', 'valuation': 'SVAF', 'collateral_detail': 'CCMS',
             'npa_asset': 'AMIS, RPS', 'npa_sale': 'AMIS', 'lawsuit': 'LIT', 'hearing': 'LIT',
             'pod_receipt': 'WIN', 'gl_write_off': 'GL', 'collins_score': 'COLLINS',
             'party_product': 'SCBPDM', 'credit_decision': 'NLEADS', 'esign_request': 'EasyApp',
             'iam_group': 'Entra ID', 'account': 'ALS', 'customer': 'SCBPDM', 'efs_action': 'EFS'}

BUSKEY = {
    'ace_batch_run': '(source_system, business_date)', 'valuation': 'valuation_key',
    'collateral_detail': 'collateral_detail_key', 'npa_asset': 'npa_asset_key',
    'npa_sale': 'npa_sale_key', 'lawsuit': 'lawsuit_key', 'hearing': 'hearing_key',
    'pod_receipt': 'pod_key', 'gl_write_off': 'write_off_key', 'collins_score': 'score_key',
    'party_product': '(person_key, account_key, product_type, business_date)',
    'credit_decision': 'credit_decision_key', 'esign_request': 'esign_key',
    'iam_group': '(entra_group, role_code)',
}

by_table = OrderedDict()
for f in FIELDS:
    t = f['ACE object column'].split('.')[0]
    by_table.setdefault(t, []).append(f)

# ---- markdown ----
L = []
A = L.append
A('# RWB-ACE-001 ACE DB additions for the Recovery Workbench')
A('')
A('SCB Collections and Recovery. Henka Group, 15 November 2026.')
A('')
A('(C) Siam Commercial Bank and Henka Pte Ltd')
A('')
A('| Item | Value |')
A('|---|---|')
A('| Story key | RWB-ACE-001 |')
A('| Owner | ACE team |')
A('| Epic | ACE backlog, release 30 November 2026 |')
A('| Module | ACE ingestion and schema |')
A('| Feature | FEAT-RDF-26 ACE DB additions (ACE team) |')
A('| Requirement IDs | REQ-RDF-001, REQ-RDF-002 |')
A('| Decision | D-RCV-35 (U1, U2); DL43 |')
A('| Priority | Must - critical path for the 30 November release |')
A('| Depends on | None. This story is first on the recovery critical path |')
A('| Blocks | RWB-E1-069, RWB-E1-002, RWB-E1-016, RWB-E1-018, every Tier 2 feature |')
A('| Status | Ready for the ACE team estimate (DL43) |')
A('')
A('## 1. Story')
A('')
A('As the **ACE team lead**, I want **the tables and columns that the recovery module needs but ACE does not hold added to the ACE database, ingested by the existing ACE ingestion and recorded with a business date**, so that **the recovery module reads one copy of source data through its views, and no recovery load or staging table is built**.')
A('')
A('## 2. Business rationale')
A('')
A('The recovery module reads source data from ACE (D-RCV-35, ADR-010). ACE already holds account, payment, customer, contact, collateral, the collateral asset, collections activity, assignment, bucket history, product, branch and holiday. It does not hold the appraisal, the CCMS collateral detail, the NPA asset and sale, the lawsuit and hearing, the proof of delivery, the GL write-off, the COLLINS score, the SCBPDM product holding, the NLEADS credit decision, the EasyApp signature reference or the Entra group mapping. It also lacks a per-source business date record and 12 columns on account, customer and efs_action.')
A('')
A('This story adds exactly that: 14 tables, 12 columns and the batch record. It is the single dependency that unblocks the recovery data engine, and it is why DL43 is the top item on the programme risk log. Every field is listed in appendix A with its source, type and frequency, so the estimate is a table read, not a discovery.')
A('')
A('## 3. Preconditions')
A('')
A('- The ACE schema is at the common migration head (V026 at the time of writing).')
A('- The ACE ingestion framework accepts a new source: a file or API contract, a staging-to-target mapper, a batch record writer and a unique business key per target table.')
A('- The ACE DBA role that owns the schema is available for the migration window.')
A('- The recovery role name and the view-owner role name are agreed with the Workbench environment design.')
A('- Each source owner has confirmed the field list in appendix A: SVAF, CCMS, AMIS, RPS, LIT, WIN, GL, COLLINS, SCBPDM, NLEADS, EasyApp and the Entra ID administrator.')
A('')
A('## 4. Flow')
A('')
A('1. ACE team: applies migration `V027__rwb_ace_001_recovery_source_additions.sql` in DEV. It creates 14 tables and adds 12 columns in one transaction.')
A('2. ACE team: adds one ingestion job per source, each writing its target table and one `ace_batch_run` row per source and business date.')
A('3. ACE team: runs the population check (AC2) against one full file per source, comparing the row count with the trailer.')
A('4. ACE team: runs the ACE regression suite (AC6) and confirms no existing screen, job or report changes.')
A('5. ACE DBA: grants SELECT on the listed tables to the view-owner role, and nothing else (AC4).')
A('6. Recovery squad: creates the Section B views in RWB-E1-069 and reads them.')
A('7. ACE team: repeats steps 1 to 5 in SIT, then PROD in the release window.')
A('')
A('## 5. Exception paths')
A('')
A('| ID | Trigger | What happens | Covered by |')
A('|---|---|---|---|')
A('| X1 | A source file fails its trailer or checksum | The ingestion writes no row for that source and business date; `ace_batch_run` keeps the previous COMPLETED row as the latest | AC3 |')
A('| X2 | A field in appendix A has no column after the migration | The conformance test fails and names the field ID | AC8 |')
A('| X3 | A source re-sends a business date already loaded | The unique business key rejects the duplicate; the batch record keeps one row for that source and date | AC7 |')
A('| X4 | A new column would change an existing ACE column type | The migration is rejected at review; new columns are additive only | AC1, AC6 |')
A('| X5 | The view-owner role is granted more than SELECT | The grant check fails the security review | AC4 |')
A('| X6 | The migration must be backed out | The down script drops the 14 tables and the 12 columns; no ACE row is touched | AC5 |')
A('')
A('## 6. INVEST check')
A('')
A('| Test | Result |')
A('|---|---|')
A('| Independent | Needs nothing from the recovery module; it is the first item on the critical path |')
A('| Negotiable | The field list is fixed by appendix A; the ingestion design is the ACE team\'s choice |')
A('| Valuable | Removes 14 tables and a load estate from the Workbench, and gives ACE one more complete source set |')
A('| Estimable | 14 tables, 12 columns, 14 ingestion jobs, one grant, one conformance test |')
A('| Small | One migration plus the ingestion jobs; the ACE team sizes it in DL43 |')
A('| Testable | Eight criteria, each one automated test |')
A('')
A('## 7. Acceptance criteria')
A('')
A('```gherkin')
A('Feature: ACE DB additions for the Recovery Workbench')
A('')
A('  Scenario: AC1 Tables and columns deployed')
A('    Given the ACE schema at the common migration head')
A('    When the ACE team applies V027__rwb_ace_001_recovery_source_additions.sql in DEV and then in SIT')
A('    Then public holds the 14 new tables of section 11')
A('    Then account holds 7 new columns, customer 3 and efs_action 2')
A('    Then ace_batch_run has a primary key and the unique key (source_system, business_date)')
A('    Then no existing ACE column is renamed, retyped or dropped')
A('')
A('  Scenario: AC2 Every Workbench field is populated')
A('    Given one full source file for each source in appendix A')
A('    When ACE ingests each file for business date 2026-11-30')
A('    Then all 80 appendix A fields hold a value or an explicit null')
A('    Then the row count per target table equals the file trailer count')
A('')
A('  Scenario: AC3 Business date and completion recorded')
A('    Given the ALS file for 2026-11-30 is ingested and completes at 04:40')
A('    When the recovery module reads v_ace_batch_status')
A('    Then it returns ALS, 2026-11-30, COMPLETED, the record count and the completion time')
A('    Then a failed run for 2026-12-01 leaves 2026-11-30 as the latest COMPLETED row for ALS')
A('')
A('  Scenario: AC4 Read grant only')
A('    Given the view-owner role agreed with the Workbench environment design')
A('    When the ACE DBA applies the grant script')
A('    Then the role may select the 14 new tables and no other table')
A('    Then the 12 new columns on account, customer and efs_action are covered by the existing Tier 1 grant')
A('    Then the role may not insert, update, delete or truncate any table')
A('')
A('  Scenario: AC5 Reversible')
A('    Given a copy of PROD with the migration applied')
A('    When the down script runs')
A('    Then the 14 tables and the 12 columns are gone')
A('    Then account, payment, customer and efs_action row counts are unchanged')
A('')
A('  Scenario: AC6 Existing ACE reads unaffected')
A('    Given the ACE regression suite')
A('    When it runs after the migration')
A('    Then every existing screen, batch job and report passes')
A('    Then the row counts of account, payment, customer and efs_action are unchanged')
A('')
A('  Scenario: AC7 Idempotent reload')
A('    Given a source file already ingested for 2026-11-30')
A('    When the same file is ingested again')
A('    Then no duplicate row is created')
A('    Then ace_batch_run holds one row for that source and business date')
A('')
A('  Scenario: AC8 Field appendix matches the migration')
A('    Given the 80 rows of appendix A')
A('    When the conformance test compares them with the deployed columns')
A('    Then 80 of 80 resolve to a column of the right type')
A('    Then no appendix row is missing and no extra mapped column exists')
A('```')
A('')
A('## 8. Business rules')
A('')
A('| ID | Rule | Source |')
A('|---|---|---|')
A('| BR1 | Every table carries `source_system`, `business_date` and `loaded_at`; the business date is the source business date, not the ingest date | D-RCV-35 U2; E1-015 |')
A('| BR2 | Every table has a business key with a unique constraint; the Workbench links by that key and never by a generated id | D-RCV-35 U4 |')
A('| BR3 | New columns on existing ACE tables are additive only; no existing column is renamed, retyped or dropped | D-RCV-35 U3 |')
A('| BR4 | The batch record is one row per source and business date, written even when the source delivers zero rows | E1-015; E1-016 |')
A('| BR5 | Selective grant: the view-owner role reads the listed tables and writes nothing | D-RCV-35 U4; CTL-02 |')
A('| BR6 | A field is in this story only if the Workbench needs it; a field the Workbench does not read is not added | appendix A |')
A('')
A('## 9. State transitions')
A('')
A('None on a case. This story changes the ACE schema version (V026 to V027) and the ingestion job set (14 jobs added).')
A('')
A('## 10. Authority')
A('')
A('| Who | What they may do in this story |')
A('|---|---|')
A('| ACE team lead | Owns the story, the estimate and DL43 |')
A('| ACE DBA | Applies the migration and the grant |')
A('| ACE ingestion owner | Adds and schedules the 14 jobs |')
A('| View-owner role | Selects the 21 listed tables; writes nothing |')
A('| Recovery squad | Reads the views only; has no grant on a public table |')
A('')
A('## 11. Data')
A('')
A('### 11.1 New tables')
A('')
A('| Table | Columns | Source | Business key | Fields read by the Workbench |')
A('|---|---:|---|---|---:|')
for t in ['ace_batch_run', 'valuation', 'collateral_detail', 'npa_asset', 'npa_sale', 'lawsuit',
          'hearing', 'pod_receipt', 'gl_write_off', 'collins_score', 'party_product',
          'credit_decision', 'esign_request', 'iam_group']:
    cols = tables[t]
    n = len(by_table.get(t, []))
    A('| `%s` | %d | %s | `%s` | %d |' % (t, len(cols), TABLE_SRC.get(t, ''),
      BUSKEY[t], n))
A('')
A('### 11.2 New columns on existing tables')
A('')
A('| Table | Column | Type | Source | Field ID |')
A('|---|---|---|---|---|')
for t, c, typ in alter:
    fids = [f['Field ID'] for f in FIELDS if f['ACE object column'] == '%s.%s' % (t, c)]
    A('| `%s` | `%s` | %s | %s | %s |' % (t, c, typ, TABLE_SRC.get(t, ''), ', '.join(fids)))
A('')
A('### 11.3 The 80 fields')
A('')
A('Full table, with source field and frequency, is appendix A of this file and sheet `Fields` of the xlsx.')
A('')
A('| Table | Fields | Source |')
A('|---|---:|---|')
for t, fs in by_table.items():
    A('| `%s` | %d | %s |' % (t, len(fs), TABLE_SRC.get(t, '')))
A('')
A('## 12. Solution plan')
A('')
A('1. Migration `V027__rwb_ace_001_recovery_source_additions.sql`: 14 `CREATE TABLE`, 12 `ALTER TABLE ... ADD COLUMN`, the primary keys, the business-key unique constraints and the foreign keys to `account`, `asset`, `customer`, `npa_asset` and `lawsuit` as shown in section 11.')
A('2. Ingestion: one Spring Batch job per source; a shared `BatchRecordWriter` writes `ace_batch_run` once per run.')
A('3. Mapper: one class per source, generated from the STTM v4 gap sheet, with the type casts in section 11.')
A('4. Grant script: `SELECT` on the 21 listed tables to the view-owner role; `REVOKE` from PUBLIC.')
A('5. Conformance test: reads appendix A and `information_schema.columns`, fails on any missing or mismatched column (AC8).')
A('6. Down script: drops the 14 tables and the 12 columns in reverse dependency order.')
A('')
A('## 13. Appendix A - the 80 fields')
A('')
A('| Field ID | Workbench entity | Source | Source field | ACE column | Type | Frequency | Read through |')
A('|---|---|---|---|---|---|---|---|')
for t, fs in by_table.items():
    for f in fs:
        col = f['ACE object column'].split('.')[1]
        typ = ''
        for c, ty, _, _ in tables.get(t, []):
            if c == col:
                typ = ty
        A('| %s | %s.%s | %s | %s | `%s` | %s | %s | `%s` |' % (
            f['Field ID'], f['Entity'], f['Field'], f['Source system'],
            f['Source field'] if f['Source field'] not in ('', 'None') else '-',
            f['ACE object column'], typ, FREQ.get(f['Source system'].split(' via ')[0], ''), f['Read path']))
A('')
A('## 14. Tests')
A('')
A('| Test | Covers | Level |')
A('|---|---|---|')
for i, (ac, name) in enumerate([('AC1', 'Tables and columns deployed'), ('AC2', 'Every field populated'),
                                ('AC3', 'Business date and completion'), ('AC4', 'Read grant only'),
                                ('AC5', 'Reversible'), ('AC6', 'Existing ACE reads unaffected'),
                                ('AC7', 'Idempotent reload'), ('AC8', 'Field appendix matches')], 1):
    A('| TC-ACE-001-%02d | %s %s | System |' % (i, ac, name))
A('')
A('## 15. Traceability')
A('')
A('| Requirement | Story | Test |')
A('|---|---|---|')
A('| REQ-RDF-001 Recovery data products have one system of record | RWB-ACE-001 | TC-ACE-001-01 to 08 |')
A('| REQ-RDF-002 Recovery reads source data from ACE | RWB-ACE-001, RWB-E1-069 | TC-ACE-001-04, TC-E1-069-02 |')
A('| D-RCV-35 U2 the ACE team owns new ACE tables and columns | RWB-ACE-001 | all |')
A('')
A('The field appendix is the contract. If the ACE team changes a column, appendix A and the STTM v4 gap sheet change in the same pull request.')

io.open(r'04 User stories\Recovery Workbench ACE Team Stories v1.md', 'w', encoding='utf-8').write('\n'.join(L))

# ---- workbook ----
wb = openpyxl.Workbook()
H = Font(bold=True, color='FFFFFF')
FILL = PatternFill('solid', fgColor='1F3864')
WRAP = Alignment(wrap_text=True, vertical='top')


def head(ws, n):
    for c in range(1, n + 1):
        cell = ws.cell(row=1, column=c)
        cell.font = H
        cell.fill = FILL
        cell.alignment = Alignment(wrap_text=True, vertical='center')


ws = wb.active
ws.title = 'Story'
rows = [
    ('Story key', 'RWB-ACE-001'), ('Title', 'ACE DB additions for the Recovery Workbench'),
    ('Owner', 'ACE team'), ('Epic', 'ACE backlog, release 30 November 2026'),
    ('Feature', 'FEAT-RDF-26 ACE DB additions (ACE team)'),
    ('Requirement IDs', 'REQ-RDF-001, REQ-RDF-002'), ('Decision', 'D-RCV-35 (U1, U2); DL43'),
    ('Priority', 'Must - critical path'), ('Depends on', 'None'), ('Blocks', 'RWB-E1-069, RWB-E1-002, RWB-E1-016, RWB-E1-018'),
    ('Status', 'Ready for the ACE team estimate (DL43)'),
    ('Story', 'As the ACE team lead, I want the tables and columns the recovery module needs but ACE does not hold added to ACE, ingested by the existing ingestion and recorded with a business date, so that the recovery module reads one copy of source data through its views.'),
]
for r in rows:
    ws.append(list(r))
ws.column_dimensions['A'].width = 20
ws.column_dimensions['B'].width = 130
for row in ws.iter_rows(min_row=1, max_row=len(rows)):
    row[0].font = Font(bold=True)
    row[1].alignment = WRAP

ws2 = wb.create_sheet('Fields')
ws2.append(['Field ID', 'Workbench entity', 'Workbench field', 'Source system', 'Source field',
            'ACE table', 'ACE column', 'Type', 'Frequency', 'Read through'])
for f in FIELDS:
    t, c = f['ACE object column'].split('.')
    typ = ''
    for cc, ty, _, _ in tables.get(t, []):
        if cc == c:
            typ = ty
    ws2.append([f['Field ID'], f['Entity'], f['Field'], f['Source system'],
                f['Source field'] if f['Source field'] not in ('', 'None') else '',
                t, c, typ, FREQ.get(f['Source system'].split(' via ')[0], ''), f['Read path']])
head(ws2, 10)
ws2.freeze_panes = 'A2'
ws2.auto_filter.ref = 'A1:J%d' % (len(FIELDS) + 1)
for col, w in {'A': 13, 'B': 22, 'C': 24, 'D': 26, 'E': 26, 'F': 20, 'G': 28, 'H': 20, 'I': 18, 'J': 34}.items():
    ws2.column_dimensions[col].width = w

ws3 = wb.create_sheet('Tables')
ws3.append(['Table', 'Column', 'Type', 'Nullable', 'Key', 'Source', 'Field ID'])
for t, cols in tables.items():
    for c, typ, nul, key in cols:
        fids = [f['Field ID'] for f in FIELDS if f['ACE object column'] == '%s.%s' % (t, c)]
        ws3.append([t, c, typ, nul, key, TABLE_SRC.get(t, ''), ', '.join(fids)])
for t, c, typ in alter:
    fids = [f['Field ID'] for f in FIELDS if f['ACE object column'] == '%s.%s' % (t, c)]
    ws3.append([t, c, typ, 'YES', '', TABLE_SRC.get(t, ''), ', '.join(fids)])
head(ws3, 7)
ws3.freeze_panes = 'A2'
ws3.auto_filter.ref = 'A1:G%d' % (ws3.max_row)
for col, w in {'A': 22, 'B': 30, 'C': 24, 'D': 9, 'E': 6, 'F': 18, 'G': 22}.items():
    ws3.column_dimensions[col].width = w

ws4 = wb.create_sheet('Acceptance criteria')
ws4.append(['AC', 'Title', 'Gherkin'])
acs = [('AC1', 'Tables and columns deployed', 'Given the ACE schema at the common migration head, when V027 is applied in DEV and SIT, then the 14 tables and 12 columns exist, ace_batch_run has its keys, and no existing column changes.'),
       ('AC2', 'Every Workbench field is populated', 'Given one full file per source, when ACE ingests each for 2026-11-30, then all 80 fields hold a value or an explicit null and each target count equals the trailer.'),
       ('AC3', 'Business date and completion recorded', 'Given the ALS file for 2026-11-30 completes at 04:40, when the Workbench reads v_ace_batch_status, then it returns ALS, 2026-11-30, COMPLETED, the count and the time; a later failed run does not replace it.'),
       ('AC4', 'Read grant only', 'Given the view-owner role, when the grant is applied, then it selects the 14 new tables and writes nothing; the 12 new columns are covered by the Tier 1 grant.'),
       ('AC5', 'Reversible', 'Given a copy with the migration applied, when the down script runs, then the 14 tables and 12 columns are gone and ACE row counts are unchanged.'),
       ('AC6', 'Existing ACE reads unaffected', 'Given the ACE regression suite, when it runs after the migration, then every existing screen, job and report passes.'),
       ('AC7', 'Idempotent reload', 'Given a file already ingested for a business date, when it is ingested again, then no duplicate row exists and one batch row remains.'),
       ('AC8', 'Field appendix matches', 'Given the 80 appendix rows, when the conformance test runs, then 80 of 80 resolve to a column of the right type.')]
for a in acs:
    ws4.append(list(a))
head(ws4, 3)
for col, w in {'A': 7, 'B': 34, 'C': 120}.items():
    ws4.column_dimensions[col].width = w
for row in ws4.iter_rows(min_row=2, max_row=ws4.max_row):
    for cell in row:
        cell.alignment = WRAP

ws5 = wb.create_sheet('Tests')
ws5.append(['Test', 'Covers', 'Level', 'Data'])
for i, a in enumerate(acs, 1):
    ws5.append(['TC-ACE-001-%02d' % i, a[0] + ' ' + a[1], 'System', 'One full file per source, business date 2026-11-30; SIT ACE schema at V027'])
head(ws5, 4)
for col, w in {'A': 18, 'B': 40, 'C': 10, 'D': 80}.items():
    ws5.column_dimensions[col].width = w

wb.save(r'04 User stories\Recovery Workbench ACE Team Stories v1.xlsx')
print('wrote story md and xlsx; fields', len(FIELDS), 'tables', len(tables), 'alter', len(alter))
