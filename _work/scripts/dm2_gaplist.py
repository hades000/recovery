# -*- coding: utf-8 -*-
"""DM2: fix the ACE Field Gap List v1 in place (D4 DF-DEC-006, DF-PTY-016 read path, PK not null, UK markers)."""
import openpyxl
from collections import Counter
import dm2_lib as L

wb = openpyxl.load_workbook(L.GAP)
wb.properties.title = 'Recovery Workbench ACE Field Gap List v1'

# ---- Fields
ws = wb['Fields']
hdr = [c.value for c in ws[1]]
col = {h: i + 1 for i, h in enumerate(hdr)}
for r in range(2, ws.max_row + 1):
    fid = ws.cell(r, 1).value
    for c in range(1, ws.max_column + 1):
        if ws.cell(r, c).value == 'None':
            ws.cell(r, c).value = None
    if fid == 'DF-DEC-006':
        ws.cell(r, col['Disposition']).value = 'ACE new'
        ws.cell(r, col['Note']).value = ('COLLINS score gap (D4). Same ACE column as DF-DEC-023, '
                                         'collins_score.model_version; read at decision time.')
    if fid == 'DF-PTY-016':
        ws.cell(r, col['Read path']).value = 'v_ace_contact.contact_value'
fields = [dict(zip(hdr, row)) for row in ws.iter_rows(min_row=2, values_only=True)]
disp = Counter(f['Disposition'] for f in fields)
assert disp['ACE reuse'] == 51 and disp['ACE new'] == 81 and disp['Recovery extension'] == 1, disp
new_by_target = {}
for f in fields:
    if f['Disposition'] == 'ACE new':
        new_by_target.setdefault(f['ACE object column'], []).append(f['Field ID'])

# ---- ACE additions
tables, alters = L.parse_probe()
spec = {}
for t, cols in tables.items():
    for c in cols:
        spec[(t, c['col'])] = c
for a in alters:
    spec[(a['table'], a['col'])] = a
ws3 = wb['ACE additions']
for r in range(2, ws3.max_row + 1):
    t, c = ws3.cell(r, 1).value, ws3.cell(r, 2).value
    s = spec[(t, c)]
    ws3.cell(r, 3).value = s['type']
    ws3.cell(r, 4).value = s['nullable']
    ws3.cell(r, 5).value = s['key'] or None
    ws3.cell(r, 6).value = L.TABLE_SRC[t] if t != 'ace_batch_run' else 'all sources'
    ws3.cell(r, 7).value = ', '.join(new_by_target.get('%s.%s' % (t, c), [])) or None
    if t in L.NOTE_EXTRA:
        ws3.cell(r, 8).value = L.NOTE_EXTRA[t]
assert ws3.max_row - 1 == 166
ws3.column_dimensions['E'].width = 44

# ---- Summary
ws4 = wb['Summary']
ws4['A4'] = ('Amended 15 November 2026 (coordinator decision D4): DF-DEC-006 decision_log_entry.model_version '
             're-classed from ACE reuse to ACE new, because collins_score is a Tier 2 table. DF-PTY-016 read path is '
             'v_ace_contact.contact_value. Primary keys are NOT NULL; UK marks the business key.')
src_new = Counter(f['Source system'] for f in fields if f['Disposition'] == 'ACE new')
src_all = Counter(f['Source system'] for f in fields)
obj_new = Counter(f['ACE object column'].split('.')[0] for f in fields if f['Disposition'] == 'ACE new')
section = None
for r in range(5, ws4.max_row + 1):
    a, b = ws4.cell(r, 1).value, ws4.cell(r, 2).value
    if a in ('Disposition', 'By source system', 'By ACE object (ACE new only)'):
        section = a
        continue
    if a in (None, 'Source system', 'ACE object'):
        continue
    if section == 'Disposition':
        if a == 'Total':
            ws4.cell(r, 2).value = sum(disp.values())
        else:
            ws4.cell(r, 2).value = disp.get(a, 0)
    elif section == 'By source system':
        ws4.cell(r, 2).value = src_all[a]
        ws4.cell(r, 3).value = src_new.get(a, 0)
    elif section == 'By ACE object (ACE new only)':
        ws4.cell(r, 2).value = obj_new[a]

# ---- Counts
ws5 = wb['Counts']
for r in range(2, ws5.max_row + 1):
    if ws5.cell(r, 1).value == 'Source fields with an external source':
        ws5.cell(r, 4).value = '51 ACE reuse + 81 ACE new + 1 extension'
if not any(ws5.cell(r, 1).value == 'Distinct ACE columns behind the ACE-new fields' for r in range(1, ws5.max_row + 1)):
    ws5.append(['Distinct ACE columns behind the ACE-new fields', 0, 79,
                '81 fields; efs_action.contact_result serves DF-INT-008 and DF-INT-036, and '
                'collins_score.model_version serves DF-DEC-006 and DF-DEC-023'])
    ws5.append(['ACE tables the 30 views read (ace_view_owner SELECT grant)', 0, 35,
                '21 Tier 1 tables read by Section A + 14 Tier 2 tables (D2)'])

wb.save(L.GAP)
print('gap list saved', dict(disp), 'additions', ws3.max_row - 1, 'distinct new cols', len(new_by_target))
