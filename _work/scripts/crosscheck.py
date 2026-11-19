import os, re
base = r'_work/staging'
files = ['Recovery Workbench TSD P1 Recovery data engine v2.md',
         'Recovery Workbench TSD P2 Integration v2.md',
         'Recovery Workbench TSD P3 Case and workflow v2.md',
         'Recovery Workbench TSD P8 Payments and posting v2.md',
         'Recovery Workbench TSD S1 Valuation and route v2.md',
         'Recovery Workbench TSD S5 Assets and auction v2.md']
pats = ['COLLINS batch', 'file load', 'File load', 'LoadCompleted', 'LoadRefused', 'JOB-01', 'JOB-09',
        'tracker', 'dq_exception', 'interface_run', 'interface_signoff', 'load_run', 'loan_account',
        'account_payment', 'collections_history', 'contact_point_id', 'account_id', 'party_id',
        'asset_id', 'account_payment_id', 'COLLINS daily', 'via COLLINS']
for f in files:
    s = open(os.path.join(base, f), encoding='utf-8').read()
    print('=====', f)
    for pat in pats:
        for m in re.finditer(re.escape(pat), s):
            line = s[:m.start()].count('\n') + 1
            ctx = s.splitlines()[line - 1].strip()
            print('  %-18s %4d  %s' % (pat, line, ctx[:150]))
