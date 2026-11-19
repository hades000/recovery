import io
p = r'E1-042 Migration and Clarifications\sql\V0042__rwb_e1_042_parameter_catalog_and_seed.sql'
t = io.open(p, encoding='utf-8-sig').read()
t = t.replace('${recoverySchema}', 'recovery')
io.open(r'_work\sql\e1042_test.sql', 'w', encoding='utf-8').write(t)
print('substituted', len(t))
