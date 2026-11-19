import io
import re

p = r'06 Data\Recovery Workbench Physical Schema v4.sql'
txt = io.open(p, encoding='utf-8').read()

rows = re.findall(
    r'ALTER TABLE\s+([a-z0-9_]+)\s+ADD CONSTRAINT\s+([a-z0-9_]+)\s+FOREIGN KEY \(([a-z0-9_]+)\)\s+REFERENCES\s+([a-z0-9_.]+)\s*\(([a-z0-9_]+)\)([^;]*);',
    txt, re.I)
print('FKs', len(rows))
copy = {'party', 'contact_point', 'loan_account', 'account_payment', 'collateral',
        'account_collateral', 'valuation', 'asset', 'collections_history', 'party_product', 'score'}
n = 0
tabs = set()
for s, c, f, t, tf, rest in rows:
    if t.lower() in copy:
        n += 1
        tabs.add(s.lower())
        print('%-28s %-28s -> %-18s (%s)%s' % (s, f, t, tf, rest.strip()[:40]))
print('count', n, 'in tables', len(tabs))
print(sorted(tabs))
