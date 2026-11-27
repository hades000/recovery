import re,sys
s=open('recovery_views.sql',encoding='utf-8').read()
for v in ['v_ace_customer','v_ace_contact','v_ace_account','v_ace_ca_relation','v_ace_collateral','v_ace_collateral_detail','v_ace_pod','v_ace_batch_status','v_ace_payment']:
    i=s.find('VIEW recovery.'+v+' ')
    if i<0:
        m=re.search(r'VIEW\s+(recovery\.)?'+v+r'\b',s); i=m.start() if m else -1
    if i<0: print('MISSING',v); continue
    j=s.find(';',i)
    print('=====',v, s[:i].count('\n')+1)
    print(s[i:j])
