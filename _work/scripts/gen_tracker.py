# -*- coding: utf-8 -*-
"""Generate the ACE DB alignment tracker workbook."""
import csv
import io
import os
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

files = list(csv.DictReader(io.open(r'_work\data\files.csv', encoding='utf-8')))
stories = list(csv.DictReader(io.open(r'_work\data\story_disposition.csv', encoding='utf-8')))
fields = list(csv.DictReader(io.open(r'_work\data\fields.csv', encoding='utf-8')))

H = Font(bold=True, color='FFFFFF')
FILL = PatternFill('solid', fgColor='1F3864')
BOLD = Font(bold=True)
WRAP = Alignment(wrap_text=True, vertical='top')


def header(ws, n):
    for c in range(1, n + 1):
        cell = ws.cell(row=1, column=c)
        cell.font = H
        cell.fill = FILL
        cell.alignment = Alignment(wrap_text=True, vertical='center')


def widths(ws, spec):
    for col, w in spec.items():
        ws.column_dimensions[col].width = w


wb = openpyxl.Workbook()

# Read me
ws = wb.active
ws.title = 'Read me'
ws['A1'] = 'Recovery Workbench ACE DB alignment tracker v1'
ws['A1'].font = Font(bold=True, size=14)
lines = [
    '',
    'SCB Collections and Recovery. Henka Group, 15 November 2026.',
    '',
    'What this workbook is',
    'The working tracker for the ACE alignment. It holds the per-document edit list, the per-story disposition and the',
    'governance actions. The narrative case for the change is in Recovery Workbench ACE DB Alignment Change Register v1.md.',
    '',
    'Status values',
    'Not started  - no new-version file exists yet',
    'Drafted      - the new-version file exists and the edit log is appended to the register',
    'In review    - the data architect or the ACE team lead is reading it',
    'Approved     - signed off; the old version may be retired at the next index update',
    'Superseded   - the document is replaced by a different document, not a new version',
    '',
    'One writer per file',
    'Each row has one owner agent. An agent writes only its own new-version file and returns an edit log. No agent edits a',
    'file another agent owns. Frozen inputs: the change register, the ACE schema dump, the Tier Map, LDM v7 and Physical Schema v5.',
    '',
    'Waves',
    'W0  register, Tier Map, gap list, views, schema dump (this pack)',
    'W1  STTM v4, LDM v7, Physical Schema v5, RWB-ACE-001, then verify',
    'W2  governance, architecture, requirements, data documents (45 files)',
    'W3  stories, build notes (16 files)',
    'W4  test, delivery (13 files)',
    'W5  index, control sheet, hub, verification (3 files)',
]
r = 2
for line in lines:
    ws.cell(row=r, column=1, value=line)
    if line in ('What this workbook is', 'Status values', 'One writer per file', 'Waves'):
        ws.cell(row=r, column=1).font = BOLD
    r += 1
ws.column_dimensions['A'].width = 120

# Documents
ws2 = wb.create_sheet('Documents')
hdr = ['#', 'Folder', 'Current file', 'New file', 'Size', 'Wave', 'Change', 'Owner', 'Status', 'Edit log ref', 'Date done']
ws2.append(hdr)
for i, f in enumerate(files, 1):
    status = 'Drafted' if f['new'] != '(new)' and os.path.exists(os.path.join(f['folder'], f['new'])) else (
        'Drafted' if f['new'] == '(new)' and os.path.exists(os.path.join(f['folder'], f['change'].split(',')[0].strip())) else 'Not started')
    if 'ACE Team Stories' in f['new']:
        status = 'Drafted'
    ws2.append([i, f['folder'], f['current'], f['new'], f['size'], f['wave'], f['change'], '', status, '', ''])
header(ws2, len(hdr))
ws2.freeze_panes = 'C2'
ws2.auto_filter.ref = 'A1:K%d' % (len(files) + 1)
widths(ws2, {'A': 5, 'B': 34, 'C': 58, 'D': 58, 'E': 7, 'F': 7, 'G': 95, 'H': 18, 'I': 14, 'J': 12, 'K': 12})
for row in ws2.iter_rows(min_row=2, max_row=len(files) + 1):
    for cell in row:
        cell.alignment = WRAP

# Stories
ws3 = wb.create_sheet('Stories')
hdr = ['Family', 'Story', 'Disposition', 'Title', 'Entities today', 'ACE action', 'Owner', 'Status', 'Note']
ws3.append(hdr)
ACTION = {
    'Remove': 'Move the story to the register appendix; record its later home.',
    'Rewrite': 'Rewrite around views and business keys; update Entities, Gherkin and test data.',
    'Minor': 'Find-and-replace entity and field names; check every reference resolves.',
    'No impact': 'No edit. Confirm at the Wave 5 sweep.',
}
for s in stories:
    ws3.append([s['family'], s['key'], s['disposition'], s['title'], s['entities'][:400],
                ACTION.get(s['disposition'], ''), '', 'Not started', ''])
# new stories
ws3.append(['E1', 'RWB-E1-069', 'New', 'Read-only ACE source views, grants and boundary rule', 'v_ace_* views, party_ext, contact_point_ext, account_ext, valuation_ext',
            'Write the story, its ACs and its tests.', '', 'Not started', ''])
ws3.append(['ACE', 'RWB-ACE-001', 'New', 'ACE DB additions for the Recovery Workbench', 'ace_batch_run, valuation, collateral_detail, npa_asset, npa_sale, lawsuit, hearing, pod_receipt, gl_write_off, collins_score, party_product',
            'Write the story from the gap list; ACE team owns it.', 'ACE team', 'Not started', ''])
header(ws3, len(hdr))
ws3.freeze_panes = 'C2'
ws3.auto_filter.ref = 'A1:I%d' % (len(stories) + 3)
widths(ws3, {'A': 8, 'B': 14, 'C': 12, 'D': 60, 'E': 70, 'F': 60, 'G': 12, 'H': 13, 'I': 30})
for row in ws3.iter_rows(min_row=2, max_row=len(stories) + 3):
    for cell in row:
        cell.alignment = WRAP

# Decisions
ws4 = wb.create_sheet('Decisions')
hdr = ['ID', 'Decision', 'Effect', 'Status', 'Owner', 'Note']
ws4.append(hdr)
DEC = [
    ('U1', 'No inbound source loads in the Workbench', 'All source data lands in ACE through ACE ingestion, including SVAF and CCMS. The Workbench only reads ACE.', 'Agreed', 'Recovery tech lead with data architect', 'Record as D-RCV-35.'),
    ('U2', 'The ACE team owns the new ACE tables and columns', 'One new story, RWB-ACE-001, lists every new table and column with its field appendix.', 'Agreed', 'ACE team lead', 'Critical path for 30 November.'),
    ('U3', 'Workbench fields ACE lacks go into extension tables', 'Four 1:1 tables keyed by ACE business keys. Existing ACE tables are never altered by the Workbench.', 'Agreed', 'Recovery tech lead', ''),
    ('U4', 'Read path is read-only views', 'recovery.v_ace_* SELECT-only views map names and types. No FK into ACE because ACE cascades deletes on account.', 'Agreed', 'Data architect', '26 views; two migrations.'),
    ('U5', 'Excel and SharePoint trackers leave system scope', 'Retirement handled in the Cutover plan; six teams retire their trackers.', 'Agreed', 'Product owner', ''),
    ('D-RCV-35', 'Decision log entry for U1 to U5', 'Supersedes DT12, DL06 option A and DL12 option A; amends DL20 and D-RCV-29.', 'To record', 'Recovery tech lead', 'Decision Log v9.'),
    ('ADR-010', 'Read source data from the ACE database through read-only views', 'Supersedes ADR-005; updates ADR-001 consequences.', 'To record', 'Solution architect', 'ADR v2.'),
    ('DL43', 'Does the ACE team accept the RWB-ACE-001 scope and dates?', 'The critical-path dependency for the 30 November release.', 'Open', 'ACE team lead', 'Decision Log v9.'),
    ('R4-note', 'Ruling R4 definitions still hold', 'The 14 data_product definitions are seeded from the Conceptual Data Model v6; system of record re-worded ACE (from X).', 'To record', 'Data architect', 'Rulings v2.'),
    ('GATE-1', 'Sign-off: approve and start Wave 1', 'U1 to U5 and the 30-view boundary accepted; Wave 1 released.', 'Agreed', 'Data architect / recovery tech lead / product owner', '15 Nov 2026.'),
    ('GATE-2', 'Sign-off: keep 30 views, one per ACE object family', 'No consolidation. Each ACE object family has one view, so the grant and the boundary test stay precise.', 'Agreed', 'Data architect', '15 Nov 2026.'),
    ('GATE-3', 'Sign-off: route NLEADS, EasyApp and Entra ID through ACE', 'The six fields move from Workbench-recorded to ACE-ingested. RWB-ACE-001 grows to 14 tables, 80 fields.', 'Agreed', 'Product owner with ACE team lead', '15 Nov 2026.'),
]
for d in DEC:
    ws4.append(list(d))
header(ws4, len(hdr))
widths(ws4, {'A': 12, 'B': 60, 'C': 80, 'D': 12, 'E': 36, 'F': 40})
for row in ws4.iter_rows(min_row=2, max_row=len(DEC) + 1):
    for cell in row:
        cell.alignment = WRAP

# Defects
ws5 = wb.create_sheet('Defects found')
hdr = ['ID', 'Found in', 'Defect', 'Evidence', 'Fix', 'Size', 'Status']
ws5.append(hdr)
DEF = [
    ('DEF-01', 'Physical Schema v4.sql', 'No data_product seed rows, although D-RCV-29 and rulings R1 and R4 require 14.',
     'The file does not load: the first sys_objects insert fails fk_sys_objects_data_product with DP03 not present. Reproduced in PostgreSQL 17.',
     'Physical Schema v5 seeds the 14 data_product rows before sys_objects, with definitions from the Conceptual Data Model v6.', 'S', 'Open'),
    ('DEF-02', 'Physical Schema v4.sql', 'data_product.refresh_cycle is varchar(10) but its comment and the LDM use words such as On change and By versioned load.',
     'A seed value of By versioned load fails with value too long for type character varying(10).',
     'Widen to varchar(30) in v5 and seed the words from the comment.', 'S', 'Open'),
    ('DEF-03', 'Physical Schema v4.sql', '33 sys_objects rows carry OPS, AGT or RPT, which are not data products, and data_product is NOT NULL.',
     'After the DEF-01 seed, the file still fails on data_product = OPS. Ruling R1 is not applied to v4.',
     'Apply R1 in v5: data_product nullable, 33 rows NULL, FK created.', 'S', 'Open'),
    ('DEF-04', 'ACE workbook', 'Two tables carry no primary key: ace_case_accounts and batch_job_execution_params.',
     'The Overview lists a blank primary key for both; the join tables rely on a unique index only.',
     'No Workbench change. Recorded so the view conformance test does not assume a key.', 'S', 'Accepted'),
    ('DEF-05', 'Physical Schema v5', '42 fields on retained tables still mirror an ACE column (hearing, legal_action, notice, write_off, asset_sale, proceeds and others).',
     'The dictionary lists them with their old source system even though the owning story now reads the view.',
     'Drop the column or declare it a Workbench snapshot, one story at a time.', 'M', 'Open'),
    ('DEF-06', 'Physical Schema v5', 'case_list_row and case_entry_exclusion were UNIQUE (business_date).',
     'One row per day in the whole table instead of one per case account. Found by E1-002 and E1-018.',
     'Fixed in v5: (business_date, case_id, account_no) and (business_date, account_key).', 'S', 'Fixed'),
    ('DEF-07', 'Physical Schema v5', 'dp_treatment and dp_guarantee_claim were UNIQUE (business_date).',
     'One stage-2 snapshot row per day instead of one per treatment or guarantee claim.',
     'Fixed in v5: (business_date, treatment_id) and (business_date, guarantee_claim_id).', 'S', 'Fixed'),
]
for d in DEF:
    ws5.append(list(d))
header(ws5, len(hdr))
widths(ws5, {'A': 9, 'B': 24, 'C': 70, 'D': 70, 'E': 60, 'F': 6, 'G': 10})
for row in ws5.iter_rows(min_row=2, max_row=len(DEF) + 1):
    for cell in row:
        cell.alignment = WRAP

out = r'15 ACE DB Alignment\Recovery Workbench ACE DB Alignment Tracker v1.xlsx'
wb.save(out)
print('saved', out, len(files), 'files', len(stories) + 2, 'stories')
