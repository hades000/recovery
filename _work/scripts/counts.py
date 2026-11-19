import io
import openpyxl

p = r'06 Data\Recovery Workbench Logical Data Model and Data Dictionary v6.xlsx'
wb = openpyxl.load_workbook(p, data_only=True)
ws = wb['Fields']
rows = [r for r in ws.iter_rows(min_row=5, values_only=True) if r[0]]
from collections import Counter
c = Counter(r[1] for r in rows)
targets = ['loan_account', 'account_payment', 'party', 'contact_point', 'collateral', 'account_collateral',
           'collections_history', 'party_product', 'valuation', 'score', 'asset',
           'load_run', 'dq_exception', 'dq_rule', 'source_field_map', 'source_code_map',
           'interface_run', 'interface_signoff', 'tracker_inventory', 'tracker_row',
           'interface_config', 'data_product_load', 'reconciliation_result', 'case_list_row',
           'case_entry_exclusion', 'interaction']
tot = 0
for t in targets:
    print('%-24s %3d' % (t, c[t]))
    tot += c[t]
print('total', tot)
print()
print('entities with counts:')
for k, v in sorted(c.items(), key=lambda x: -x[1])[:20]:
    print('%3d %s' % (v, k))
