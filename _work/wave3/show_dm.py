import io, re
d = io.open(r'04 User stories/Recovery Workbench Data Migration Stories v3.md', encoding='ascii').read()
for k in ['RWB-DM-005', 'RWB-DM-006', 'RWB-DM-011', 'RWB-DM-013']:
    b = re.search(r'(?ms)^## ' + k + r' .*?(?=^## RWB-)', d).group(0)
    g = re.search(r'(?ms)^```gherkin\n(.*?)^```', b).group(1)
    print('=====', k)
    print(g)
