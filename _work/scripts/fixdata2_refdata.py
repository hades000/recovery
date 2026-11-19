import openpyxl
P = '06 Data/Recovery Workbench Reference Data and Lists of Values v4.xlsx'
wb = openpyxl.load_workbook(P)
L = wb['Lists']
def rep(cell, old, new):
    v = L[cell].value
    assert v.count(old) == 1, (cell, v)
    L[cell] = v.replace(old, new)
rep('E8', 'score.route_code', 'v_ace_score.route_code')
rep('E114', 'treatment.credit_result', 'v_ace_credit_decision.credit_result')
SB = ' (Section B, after RWB-ACE-001)'
for cell, ref in [('E21', 'v_ace_customer.party_type'), ('E22', 'v_ace_customer.id_type'),
                  ('E23', 'v_ace_customer.segment'), ('E57', 'v_ace_efs_action.contact_result'),
                  ('E130', 'v_ace_account.business_unit'), ('E131', 'v_ace_account.daily_bucket')]:
    rep(cell, ref, ref + SB)
wb.properties.title = 'Recovery Workbench Reference Data and Lists of Values v4'
wb.save(P)
for c in ('E8','E114','E21','E22','E23','E57','E130','E131'): print(c, L[c].value)
