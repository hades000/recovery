import re
p = r'06 Data/Recovery Workbench Physical Schema v5.sql'
s = open(p, encoding='utf-8').read()
for t in ['data_product','data_product_access','data_contract','sys_objects','sys_fields','sys_field_version','reconciliation_result','lake_copy_watermark','retention_rule','dp_guarantee_claim']:
    m = re.search(r'^CREATE TABLE %s \((.*?)\n\);' % t, s, re.S | re.M)
    print('=====', t)
    if m:
        print(', '.join(ln.strip().split(' ')[0] for ln in m.group(1).split('\n') if ln.strip() and not ln.strip().startswith('CONSTRAINT')))
    else:
        print('MISSING')
