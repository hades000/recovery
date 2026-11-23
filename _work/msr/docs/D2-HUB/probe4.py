import re
p = r'12 Project communication\Recovery Workbench Project Hub v14.html'
s = open(p, encoding='utf-8').read()
for pat in ['Document set', 'document set', 'v14', 'Version 14', 'library']:
    print('==', pat, s.count(pat))
    for m in re.finditer(pat, s):
        print('   ...', s[max(0,m.start()-120):m.start()+160].replace('\n',' | '))
