import openpyxl, re
D = r'02 Business architecture and process/Recovery Workbench '
def scan(name, pat):
    wb = openpyxl.load_workbook(D + name)
    hits = [(ws.title, c.coordinate, str(c.value)[:90]) for ws in wb for row in ws.iter_rows() for c in row
            if isinstance(c.value, str) and re.search(pat, c.value)]
    return wb, hits
wb, h = scan('Users Roles and Permissions v4.xlsx', r'DATALOAD|RECOVERY')
print(wb.properties.title, wb.properties.modified); [print(x) for x in h]
r = wb['Roles']; print('roles', sum(1 for i in range(5, 59) if r.cell(i,1).value), [r.cell(i,3).value for i in range(5,59)].count('Non-human actor'))
print([c.value for c in wb['Permissions'][55]]); print(wb['Counts']['B8'].value)
wb, h = scan('Role to System Access Matrix v3.xlsx', r'steward|CCMS')
m = wb['Matrix']; print('Y col R:', [m.cell(i,1).value for i in range(5,59) if m.cell(i,25).value=='R'], 'L col:', [m.cell(i,12).value for i in range(5,59) if m.cell(i,12).value!='-'])
al = wb['Access list']; n = sum(1 for i in range(5, al.max_row+1) if al.cell(i,1).value); print('access pairs', n, al['A2'].value[:30], al.auto_filter.ref)
mx = sum(1 for i in range(5,59) for j in range(4,26) if m.cell(i,j).value != '-'); print('matrix non-dash', mx)
sy = wb['Systems']; print([ (sy.cell(i,1).value, sy.cell(i,3).value) for i in (13,26)])
for t in h: print(t)
wb, h = scan('Feature List v4.xlsx', r'COLLINS (batch|load|daily)|ALS load|data store|EFS file load')
f = wb['Features']; cls = [f.cell(i,4).value for i in range(5, f.max_row+1)]
print('live', sum(1 for c in cls if c in ('User','Admin','System')), 'retired', sum(1 for c in cls if c and c.startswith('Retired')))
for t in h: print(t)
wb, h = scan('Business Glossary v3.xlsx', r'v_ace_pod|ACE view')
for t in h: print(t)
