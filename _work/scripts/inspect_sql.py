import re
p = r'06 Data/Recovery Workbench Physical Schema v5.sql'
s = open(p, encoding='utf-8').read()
for t in ['recovery_case','case_account','case_party','interaction','case_entry_exclusion','document','notice','signature_request','proceeds','listing','asset_sale','data_product_load','case_list_row','dp_treatment','valuation_ext']:
    m = re.search(r'^CREATE TABLE %s \((.*?)\n\);' % t, s, re.S | re.M)
    print('=====', t)
    if m:
        for ln in m.group(1).split('\n'):
            print('   ', ln.strip())
