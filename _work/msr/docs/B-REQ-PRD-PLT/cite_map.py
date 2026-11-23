import io, re

p = r'03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md'
lines = io.open(p, encoding='utf-8').read().split('\n')
for i, ln in enumerate(lines, 1):
    for m in re.finditer(r'(?:CG|ASM)-B-REQ-PRD-PLT-\d+|ASM-A6-tables-7|ASM-B-REQ-BRD-PROG-14', ln):
        print(i, m.group(0), '|', ln.strip()[:230])
