import openpyxl, re
P = '01 Decisions and governance/Recovery Workbench RWB-E1-001 Specification Rulings v2.md'
CDM = '06 Data/Recovery Workbench Conceptual Data Model v6.xlsx'
t = open(P, encoding='utf-8').read()

def rep(old, new, count=1):
    global t
    assert t.count(old) == count, (old, t.count(old))
    t = t.replace(old, new)

rep('| Superseded by | D-RCV-35 |', '| Superseded by | Counts superseded by D-RCV-35 (section 0) |')

# seed table: definitions, names and systems of record from CDM v6 Data products
ws = openpyxl.load_workbook(CDM, read_only=True)['Data products']
cdm = {r[0]: r for r in ws.iter_rows(values_only=True) if r[0] and re.fullmatch(r'DP\d\d', str(r[0]))}
assert len(cdm) == 14
lines = t.split('\n')
n = 0
for i, l in enumerate(lines):
    m = re.match(r'\| (DP\d\d) \| [^|]+ \| [^|]+ \| [^|]+ \| ([A-Z]+) \| (2026-11-20) \|$', l)
    if m:
        c = cdm[m.group(1)]
        lines[i] = f'| {c[0]} | {c[1]} | {c[2]} | {c[3]} | {m.group(2)} | {m.group(3)} |'
        n += 1
assert n == 14, n
t = '\n'.join(lines)
rep('(definition text from Conceptual Data Model v6 Data products tab; product owners approve):',
    '(name, definition and system of record copied from the Conceptual Data Model v6 Data products tab; product owners approve):')
rep('the seed table below is unchanged except for the system-of-record wording.',
    'the seed table below carries the CDM v6 names, definitions and systems of record word for word.')

# section 10 re-based on Physical Schema v5
old10 = t[t.index('## 10. Verification steps for V0001'):t.index('## 11. Fallback')]
new10 = '''## 10. Verification steps for V0001

These steps are re-based on Physical Schema v5 and D-RCV-35; the v4 figures (44 tables, 108 / 1,256, 533 of 533) no longer apply.

1. Build V0001 from Physical Schema v5; run on an empty PostgreSQL container with `recoverySchema = recovery`. Then apply V0002 (Tier 1 views) and, once RWB-ACE-001 lands, V0003 (Tier 2 views).
2. Assert: 92 tables in schema recovery and, after V0002 and V0003, 30 `recovery.v_ace_*` views; sys_objects holds 122 rows (92 tables and 30 views), of which 98 name a product and 24 (OPS 13, AGT 8, RPT 3) hold NULL; sys_fields holds 1,366 rows; data_product holds 14 rows with definition, owner_role and valid_from populated; delegation_limit holds 0 rows; fk_sys_objects_data_product exists; no constraint in schema recovery references a table in schema public.
3. Assert the view: for v_ace_account.days_past_due - DF-ACE-018, NUMBER, integer, source ACE, source field public.account.delay_days, product DP01 with system of record "ACE (ingested from ALS)", refresh DAILY, owner role RW-DATASTEW.
4. Run DataDictionaryConformanceTest and assert 1,366 of 1,366 sys_fields rows match their table or view column by name and physical type; run the view conformance test (every `v_ace_*` view compiles; the recovery role cannot read a public table directly or write to any table).
5. Reapply in SIT; assert no change (Flyway skips version 1.001).

'''
t = t.replace(old10, new10)
open(P, 'w', encoding='utf-8', newline='\n').write(t)
print('ok')
