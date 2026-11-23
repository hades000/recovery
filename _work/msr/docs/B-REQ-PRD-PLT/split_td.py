import io, re

p = r'_work/msr/extract/Recovery Workbench Temporal and Drools Design Text Extract v1.md'
t = io.open(p, encoding='utf-8').read()
parts = t.split('## Slide ')
for s in parts[1:]:
    n = s.split('\n', 1)[0].strip()
    io.open(r'_work/msr/docs/B-REQ-PRD-PLT/td-slide-%s.md' % n, 'w', encoding='utf-8').write(s.split('\n', 1)[1])
print('ok', len(parts) - 1)
