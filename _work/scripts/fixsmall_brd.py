import sys; sys.path.insert(0, r'_work/scripts')
from fixsmall_lib import load, rep1, set_modified, save
P = r'03 Requirements and specifications/Recovery Workbench Lean BRD Epic 1 v3.docx'
z, x, core = load(P)
assert 'tracker inventory, load and retirement' not in x
# 2.2 Out of scope: clone the 'Full administration' row, insert it before the final row
a = x.index('Full administration, agent autonomy')
s = x.rfind('<w:tr>', 0, a); e = x.index('</w:tr>', a) + len('</w:tr>')
row = x[s:e]
new = row.replace('Full administration, agent autonomy step-ups, regulatory returns',
                  'Excel and SharePoint tracker inventory, load and retirement')
new = new.replace('>Epic 8<', '>Cutover and Go Live Plan (U5; E1-005, E1-010, E1-012 removed)<')
assert new.count('Cutover and Go Live Plan') == 1
x = x[:e] + new + x[e:]
# 7 Success measures
x = rep1(x, 'All retired or out of scope; retired after ten clean days in parallel',
         'All retired or out of scope; retired after ten clean days in parallel under the Cutover and Go Live Plan retirement procedure (U5)')
save(P, z, x, set_modified(core))
print('BRD done')
