import openpyxl
P = '06 Data/Recovery Workbench Data Ownership and Stewardship v3.xlsx'
wb = openpyxl.load_workbook(P)
O = wb['Ownership']
row = {O.cell(r, 1).value: r for r in range(5, 19)}
tiers = {'DP01': '1 and 2', 'DP02': '1, 2 and 3', 'DP04': '1 and 4', 'DP05': '1, 2 and 4', 'DP06': '1, 2, 3 and 4'}
for dp, t in tiers.items():
    O.cell(row[dp], 11).value = t
sor = {'DP01': 'ACE team lead',
       'DP02': 'ACE team lead for Tier 1 and 2; application owner for Tier 3 (party_ext, contact_point_ext)',
       'DP06': 'ACE team lead for Tier 1 and 2; application owner for Tier 3 and 4',
       'DP11': 'ACE team lead for Tier 2; application owner for Tier 4',
       'DP13': 'ACE team lead for Tier 1 and 2; application owner for Tier 4'}
for dp, v in sor.items():
    O.cell(row[dp], 7).value = v
c = O.cell(row['DP07'], 6)
assert c.value == 'ACE (lawsuit and hearing) and the Workbench for instructions'
c.value = 'ACE (lawsuit, hearing and pod_receipt) and the Workbench for notices and instructions'
Q = wb['Quality measures']
assert Q['A5'].value == 'Completeness' and Q['A8'].value == 'Validity' and Q['A9'].value == 'Uniqueness'
Q['C5'] = 'ACE ingestion checks for Tier 1 and 2; Workbench data quality rules for Tier 3 and 4'
Q['C8'] = 'ACE ingestion checks for Tier 1 and 2; Workbench data quality rules and lov_value for Tier 3 and 4'
Q['C9'] = 'Workbench case entry rule (DL17), on the person_key that the ACE identity match M1 to M5 gives'
wb.properties.title = 'Recovery Workbench Data Ownership and Stewardship v3'
wb.save(P)
print('ok')
