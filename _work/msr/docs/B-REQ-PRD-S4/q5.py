import re
t = open('_work/msr/extract/Recovery Workbench Functional Specifications by Module v6/Recovery Workbench FSD S4 Litigation and enforcement v3.md', encoding='utf-8').read()
ids = sorted({int(m) for m in re.findall(r'R-LIT-(\d+)', t)})
print('count', len(ids))
print(ids)
print('missing 1..79:', [i for i in range(1, 80) if i not in ids])
