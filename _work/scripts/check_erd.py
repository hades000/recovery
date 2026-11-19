import re
s = open(r'06 Data/Recovery Workbench Entity Relationship Diagram v4.html', encoding='utf-8').read()
for label, a in [('ent cards', '<div class="ent '), ('view cards', 'class="ent view'), ('ext cards', 'class="ent ext'),
                 ('sections', '<section class="tab"'), ('nav buttons', '<button data-t=')]:
    print(label, s.count(a))
for name in ('loan_account', 'account_payment', 'load_run', 'tracker_inventory', 'dq_exception', 'score', 'party_id', 'asset_id'):
    print(name, s.count(name))
for a, b in [('<div', '</div>'), ('<table', '</table>'), ('<svg', '</svg>'), ('<section', '</section>'), ('<tr', '</tr>')]:
    print(a, s.count(a), b, s.count(b))
print('title', re.search(r'<title>(.*?)</title>', s).group(1))
