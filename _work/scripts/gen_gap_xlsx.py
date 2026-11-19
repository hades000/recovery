# -*- coding: utf-8 -*-
"""Generate the ACE field gap list workbook."""
import csv
import io
import re
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

FIELDS = list(csv.DictReader(io.open(r'_work\data\fields.csv', encoding='utf-8')))

# data product per entity from the LDM
wb_ldm = openpyxl.load_workbook(r'06 Data\Recovery Workbench Logical Data Model and Data Dictionary v6.xlsx', data_only=True)
ent_ws = wb_ldm['Entities']
prod = {}
for r in ent_ws.iter_rows(min_row=5, values_only=True):
    if r[0]:
        prod[r[0]] = r[3]

probe = io.open(r'_work\sql\ace_tier2_probe.sql', encoding='utf-8').read()
table_cols = []
for m in re.finditer(r'CREATE TABLE public\.([a-z_]+) \((.*?)\n\);', probe, re.S):
    table = m.group(1)
    for line in m.group(2).split('\n'):
        line = line.strip().rstrip(',')
        if not line or line.lower().startswith('constraint'):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        col, typ = parts[0], parts[1]
        nullable = 'NO' if 'not null' in line else 'YES'
        key = 'PK' if 'primary key' in line else ('FK' if 'references' in line else '')
        table_cols.append([table, col, typ, nullable, key, '', '', ''])

alter_cols = []
for m in re.finditer(r'ALTER TABLE public\.([a-z_]+)\s+ADD COLUMN ([a-z_]+) ([a-z0-9_(),]+);', probe):
    alter_cols.append([m.group(1), m.group(2), m.group(3), 'YES', '', '', '', ''])

newcol = table_cols + alter_cols

# LDM fields per ACE new column
by_target = {}
for f in FIELDS:
    if f['Disposition'] == 'ACE new':
        t = f['ACE object column'].strip()
        by_target.setdefault(t, []).append(f['Field ID'])

for row in newcol:
    t = '%s.%s' % (row[0], row[1])
    row[6] = ', '.join(by_target.get(t, []))

# source system per table
SRC = {
    'ace_batch_run': 'all sources', 'valuation': 'SVAF', 'collateral_detail': 'CCMS',
    'npa_asset': 'AMIS, RPS', 'npa_sale': 'AMIS', 'lawsuit': 'LIT', 'hearing': 'LIT',
    'pod_receipt': 'WIN', 'gl_write_off': 'GL', 'collins_score': 'COLLINS', 'party_product': 'SCBPDM',
    'account': 'ALS', 'customer': 'SCBPDM', 'efs_action': 'EFS',
}
for row in newcol:
    row[5] = SRC.get(row[0], '')

wb = openpyxl.Workbook()
ws = wb.active
ws.title = 'Summary'

H = Font(bold=True, color='FFFFFF')
FILL = PatternFill('solid', fgColor='1F3864')
TITLE = Font(bold=True, size=14)


def style_header(ws, row=1, ncol=10):
    for c in range(1, ncol + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = H
        cell.fill = FILL
        cell.alignment = Alignment(wrap_text=True, vertical='top')


def widths(ws, spec):
    for col, w in spec.items():
        ws.column_dimensions[col].width = w


ws['A1'] = 'Recovery Workbench ACE field gap list v1'
ws['A1'].font = TITLE
ws['A2'] = 'SCB Collections and Recovery. Henka Group, 15 November 2026. Frozen input to RWB-ACE-001, LDM v7 and STTM v4.'
ws['A3'] = 'Source: Logical Data Model and Data Dictionary v6, 133 fields with an external source. Decision: D-RCV-35.'

row = 5
ws.cell(row=row, column=1, value='Disposition').font = Font(bold=True)
ws.cell(row=row, column=2, value='Fields').font = Font(bold=True)
ws.cell(row=row, column=3, value='Meaning').font = Font(bold=True)
row += 1
from collections import Counter
c = Counter(f['Disposition'] for f in FIELDS)
for k in ['ACE reuse', 'ACE new', 'Recovery extension', 'Workbench']:
    ws.cell(row=row, column=1, value=k)
    ws.cell(row=row, column=2, value=c[k])
    ws.cell(row=row, column=3, value={
        'ACE reuse': 'Already in ACE. Read through a v_ace_* view; no new column.',
        'ACE new': 'Not in ACE. RWB-ACE-001 asks the ACE team for the table or column.',
        'Recovery extension': 'A Workbench flag about an ACE record, in a Tier 3 extension table.',
        'Workbench': 'Entered or recorded in the Workbench; no ACE ingestion.',
    }[k])
    row += 1
ws.cell(row=row, column=1, value='Total').font = Font(bold=True)
ws.cell(row=row, column=2, value=sum(c.values())).font = Font(bold=True)

row += 2
ws.cell(row=row, column=1, value='By source system').font = Font(bold=True)
row += 1
ws.cell(row=row, column=1, value='Source system').font = Font(bold=True)
ws.cell(row=row, column=2, value='Fields').font = Font(bold=True)
ws.cell(row=row, column=3, value='ACE new').font = Font(bold=True)
row += 1
for src, n in Counter(f['Source system'] for f in FIELDS).most_common():
    newn = sum(1 for f in FIELDS if f['Source system'] == src and f['Disposition'] == 'ACE new')
    ws.cell(row=row, column=1, value=src)
    ws.cell(row=row, column=2, value=n)
    ws.cell(row=row, column=3, value=newn)
    row += 1

row += 2
ws.cell(row=row, column=1, value='By ACE object (ACE new only)').font = Font(bold=True)
row += 1
ws.cell(row=row, column=1, value='ACE object').font = Font(bold=True)
ws.cell(row=row, column=2, value='Fields').font = Font(bold=True)
row += 1
for obj, n in Counter(f['ACE object column'].split('.')[0] for f in FIELDS if f['Disposition'] == 'ACE new').most_common():
    ws.cell(row=row, column=1, value=obj)
    ws.cell(row=row, column=2, value=n)
    row += 1

ws.column_dimensions['A'].width = 42
ws.column_dimensions['B'].width = 12
ws.column_dimensions['C'].width = 90

# Fields sheet
ws2 = wb.create_sheet('Fields')
headers = ['Field ID', 'Entity', 'Field', 'Data type', 'Data product', 'Source system', 'Source field',
           'Disposition', 'ACE object column', 'Read path', 'Note']
ws2.append(headers)
for f in FIELDS:
    ws2.append([f['Field ID'], f['Entity'], f['Field'], f['Data type'], prod.get(f['Entity'], ''),
                f['Source system'], f['Source field'], f['Disposition'], f['ACE object column'],
                f['Read path'], f['Note']])
style_header(ws2, 1, len(headers))
ws2.freeze_panes = 'A2'
ws2.auto_filter.ref = 'A1:K%d' % (len(FIELDS) + 1)
widths(ws2, {'A': 13, 'B': 22, 'C': 24, 'D': 11, 'E': 8, 'F': 28, 'G': 30, 'H': 18, 'I': 40, 'J': 40, 'K': 70})

# ACE additions sheet
ws3 = wb.create_sheet('ACE additions')
headers = ['ACE table', 'Column', 'Type', 'Nullable', 'Key', 'Source system', 'LDM field IDs', 'Note']
ws3.append(headers)
notes = {
    'ace_batch_run': 'New table. The Workbench freshness stamp (E1-015) and the intake trigger (E1-016, E1-018) read it.',
    'valuation': 'New table. Accepted, stale and valuer fields stay in recovery.valuation_ext.',
    'collateral_detail': 'New table. lien_rank moves from account_collateral to the collateral grain.',
    'npa_asset': 'New table. AMIS for property, RPS for vehicles.',
    'npa_sale': 'New table. AMIS sale contract, taxes and fees.',
    'lawsuit': 'New table. LIT court record.',
    'hearing': 'New table. LIT hearing, one row per hearing.',
    'pod_receipt': 'New table. WIN proof of delivery. The notice itself stays in recovery.notice.',
    'gl_write_off': 'New table. GL posting. The write-off decision stays in recovery.write_off.',
    'collins_score': 'New table, only if ACE does not already hold the score.',
    'party_product': 'New table. SCBPDM product holding.',
    'account': 'New column on an existing ACE table.',
    'customer': 'New column on an existing ACE table.',
    'efs_action': 'New column on an existing ACE table.',
}
for row in newcol:
    ws3.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], notes.get(row[0], '')])
style_header(ws3, 1, len(headers))
ws3.freeze_panes = 'A2'
ws3.auto_filter.ref = 'A1:H%d' % (len(newcol) + 1)
widths(ws3, {'A': 22, 'B': 30, 'C': 24, 'D': 9, 'E': 6, 'F': 16, 'G': 24, 'H': 90})

# Counts sheet
ws4 = wb.create_sheet('Counts')
ws4.append(['Item', 'v4 today', 'v5 target', 'Arithmetic'])
rows = [
    ['Workbench tables', 108, 92, '108 - 20 removed + 4 extension'],
    ['Views', 0, 30, '16 Tier 1 + 14 Tier 2'],
    ['Dictionary objects', 108, 122, '92 tables + 30 views'],
    ['Dictionary fields', 1256, 1366, '1256 - 243 removed + 49 extension + 304 view'],
    ['Source fields with an external source', 133, 133, '52 ACE reuse + 80 ACE new + 1 extension'],
    ['New ACE tables (RWB-ACE-001)', 0, 14, ''],
    ['New ACE columns (RWB-ACE-001)', 0, 12, 'account 7, customer 3, efs_action 2'],
    ['New ACE columns in total', 0, 166, '154 in the 14 new tables + 12 on existing tables'],
    ['Foreign keys into public.*', 0, 0, 'Boundary rule'],
    ['UUID foreign keys into a source copy', 23, 0, '14 re-keyed, 9 leave with their table'],
]
for r in rows:
    ws4.append(r)
style_header(ws4, 1, 4)
widths(ws4, {'A': 40, 'B': 12, 'C': 12, 'D': 70})

out = r'15 ACE DB Alignment\Recovery Workbench ACE Field Gap List v1.xlsx'
wb.save(out)
print('saved', out, 'fields', len(FIELDS), 'new columns', len(newcol))
