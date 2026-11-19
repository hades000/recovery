# -*- coding: utf-8 -*-
"""Build Source to Target Mapping v4."""
import csv
import io
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

LDM = r'06 Data\Recovery Workbench Logical Data Model and Data Dictionary v7.xlsx'
OUT = r'06 Data\Recovery Workbench Source to Target Mapping v4.xlsx'

wb_ldm = openpyxl.load_workbook(LDM, data_only=True)
ws = wb_ldm['Fields']
meta = {}
for r in ws.iter_rows(min_row=5, values_only=True):
    if r[0]:
        meta[r[0]] = r  # field id -> row

ent = {}
for r in wb_ldm['Entities'].iter_rows(min_row=5, values_only=True):
    if r[0]:
        ent[r[0]] = r

FIELDS = list(csv.DictReader(io.open(r'_work\data\fields.csv', encoding='utf-8')))

IFACE = {
    'Core bank (ALS) via COLLINS': 'INT-01, INT-02',
    'SCBPDM via COLLINS': 'INT-04',
    'EFS via COLLINS': 'INT-07',
    'COLLINS': 'INT-08',
    'LIT': 'INT-09',
    'LIT via COLLINS': 'INT-09',
    'CCMS': 'INT-10',
    'SVAF': 'INT-11',
    'AMIS': 'INT-12',
    'RPS': 'INT-13',
    'WIN': 'INT-15',
    'GL': 'INT-16',
    'ACE': 'INT-34',
    'Entra ID': 'INT-21',
    'NLEADS': 'New ACE interface (number in Interface Specifications v3)',
    'EasyApp': 'New ACE interface (number in Interface Specifications v3)',
    'Aric via COLLINS': 'INT-03',
}
FREQ = {
    'Core bank (ALS) via COLLINS': 'Daily, end of day',
    'SCBPDM via COLLINS': 'Daily, end of day',
    'EFS via COLLINS': 'Daily, end of day',
    'COLLINS': 'Daily, end of day',
    'LIT': 'Daily, end of day',
    'LIT via COLLINS': 'Daily, end of day',
    'CCMS': 'Weekly',
    'SVAF': 'Weekly',
    'AMIS': 'Monthly',
    'RPS': 'Weekly',
    'WIN': 'Weekly',
    'GL': 'Monthly',
    'ACE': 'Per request',
    'Entra ID': 'At each sign-in',
    'NLEADS': 'On decision',
    'EasyApp': 'On request',
    'Aric via COLLINS': 'Daily, end of day',
}

H = Font(bold=True, color='FFFFFF')
FILL = PatternFill('solid', fgColor='1F3864')
WRAP = Alignment(wrap_text=True, vertical='top')


def head(ws, n):
    for c in range(1, n + 1):
        cell = ws.cell(row=1, column=c)
        cell.font = H
        cell.fill = FILL
        cell.alignment = Alignment(wrap_text=True, vertical='center')


def widths(ws, spec):
    for k, v in spec.items():
        ws.column_dimensions[k].width = v


wb = openpyxl.Workbook()

# Mapping
ws = wb.active
ws.title = 'Mapping'
ws.append(['Field ID', 'Data product', 'Workbench entity', 'Workbench field', 'Data type', 'Mandatory',
           'Source system (ACE ingests it)', 'Source field', 'ACE object column', 'Read path', 'Transformation',
           'Frequency', 'Interface', 'Status'])
for f in FIELDS:
    m = meta.get(f['Field ID'], [])
    dp = ent.get(f['Entity'], ['', '', '', ''])
    dispo = f['Disposition']
    if dispo == 'ACE reuse':
        trans = 'Read directly. The view maps the name and the type.'
    elif dispo == 'ACE new':
        trans = 'Added by RWB-ACE-001. Read from the view once ACE ingests it.'
    elif dispo == 'Recovery extension':
        trans = 'Workbench flag in party_ext, keyed by person_key.'
    else:
        trans = 'Recorded in the Workbench.'
    status = {'ACE reuse': 'Ready', 'ACE new': 'Waiting on RWB-ACE-001',
              'Recovery extension': 'Ready', 'Workbench': 'Ready'}[dispo]
    ws.append([f['Field ID'], dp[3] if len(dp) > 3 else '', f['Entity'], f['Field'],
               m[3] if m else f['Data type'], m[6] if m else '',
               f['Source system'], f['Source field'] if f['Source field'] not in ('', 'None') else '',
               f['ACE object column'], f['Read path'], trans, FREQ.get(f['Source system'], ''),
               IFACE.get(f['Source system'], ''), status])
head(ws, 14)
ws.freeze_panes = 'A2'
ws.auto_filter.ref = 'A1:N%d' % (len(FIELDS) + 1)
widths(ws, {'A': 13, 'B': 8, 'C': 22, 'D': 22, 'E': 9, 'F': 9, 'G': 26, 'H': 24, 'I': 34, 'J': 38, 'K': 46, 'L': 20, 'M': 26, 'N': 22})
for row in ws.iter_rows(min_row=2, max_row=len(FIELDS) + 1):
    for cell in row:
        cell.alignment = WRAP

# ACE gaps
ws2 = wb.create_sheet('ACE gaps')
ws2.append(['Field ID', 'Source system', 'Source field', 'ACE table', 'ACE column', 'Workbench view', 'Type', 'Frequency'])
for f in FIELDS:
    if f['Disposition'] != 'ACE new':
        continue
    t, c = f['ACE object column'].split('.')
    m = meta.get(f['Field ID'], [])
    ws2.append([f['Field ID'], f['Source system'], f['Source field'], t, c, f['Read path'].split('.')[0],
                m[4] if m else '', FREQ.get(f['Source system'], '')])
head(ws2, 8)
ws2.freeze_panes = 'A2'
ws2.auto_filter.ref = 'A1:H%d' % (ws2.max_row)
widths(ws2, {'A': 13, 'B': 26, 'C': 26, 'D': 22, 'E': 26, 'F': 30, 'G': 4, 'H': 20})

# By source
ws3 = wb.create_sheet('By source')
ws3.append(['Source system', 'Fields', 'ACE reuse', 'ACE new', 'Extension', 'Refresh', 'Interface', 'ACE table(s)'])
from collections import Counter, defaultdict
c = Counter(f['Source system'] for f in FIELDS)
reuse = Counter(f['Source system'] for f in FIELDS if f['Disposition'] == 'ACE reuse')
new = Counter(f['Source system'] for f in FIELDS if f['Disposition'] == 'ACE new')
ext = Counter(f['Source system'] for f in FIELDS if f['Disposition'] == 'Recovery extension')
for src, n in c.most_common():
    tables = sorted({f['ACE object column'].split('.')[0] for f in FIELDS if f['Source system'] == src})
    ws3.append([src, n, reuse[src], new[src], ext[src], FREQ.get(src, ''), IFACE.get(src, ''), ', '.join(tables)])
ws3.append(['Total', sum(c.values()), sum(reuse.values()), sum(new.values()), sum(ext.values()), '', '', ''])
head(ws3, 8)
widths(ws3, {'A': 30, 'B': 8, 'C': 10, 'D': 9, 'E': 10, 'F': 22, 'G': 40, 'H': 60})
for row in ws3.iter_rows(min_row=2, max_row=ws3.max_row):
    for cell in row:
        cell.alignment = WRAP

# Mapping rules
ws4 = wb.create_sheet('Mapping rules')
ws4.append(['Rule', 'Detail'])
rules = [
    ('No load-time transform', 'The Workbench does not transform source data at load. There is no load. A rename or a type cast happens in the recovery.v_ace_* view.'),
    ('Name mapping', 'The view field is named for the Workbench. The ACE column name appears only in the view definition and the ACE mapping tab of the LDM.'),
    ('Type casts', 'payment.pay_date is varchar in ACE and becomes date through recovery.ace_to_date, which returns NULL rather than failing. account.is_restructured and customer.is_deceased are Y/N text and become boolean through recovery.ace_to_boolean.'),
    ('Masking', 'customer.identification_number is never exposed in clear. v_ace_customer returns id_no_masked and id_no_last4. Phone, email and address are exposed in full because notices need them; display masking is E1-037 at the API.'),
    ('Business date', 'The business date is read from recovery.v_ace_batch_status, one row per source and business date, written by ACE ingestion (RWB-ACE-001). No row carries a Workbench load date.'),
    ('Codes', 'Source codes map to Workbench lists in the view or in the list load, not in a load-time map table. LOV-ACTION-CODE reads v_ace_efs_action_code.'),
    ('Amounts', 'Amounts are numeric(18,2) in baht. ACE numeric(38,2) columns are cast in the view where the Workbench column is narrower.'),
    ('New fields', 'A field ACE does not hold is raised once in RWB-ACE-001 and then read from its view. It never becomes a Workbench column.'),
    ('Links', 'A Workbench link to a source record is a business key (varchar 255) with no foreign key. The 14 re-keyed links are listed in the Tier Map.'),
    ('Status', 'Ready means the field is in an ACE table today. Waiting on RWB-ACE-001 means the field is in the ACE story and the dependent feature stays behind its flag.'),
]
for r in rules:
    ws4.append(list(r))
head(ws4, 2)
widths(ws4, {'A': 30, 'B': 130})
for row in ws4.iter_rows(min_row=2, max_row=ws4.max_row):
    for cell in row:
        cell.alignment = WRAP

wb.save(OUT)
print('saved', OUT, 'mapping rows', len(FIELDS), 'gaps', sum(new.values()))
