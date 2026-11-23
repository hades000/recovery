import io, re

p = r'03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md'
lines = io.open(p, encoding='utf-8').read().split('\n')
i = 0
bad = []
while i < len(lines):
    ln = lines[i]
    if ln.startswith('|') and i + 1 < len(lines) and re.match(r'^\|[\s\-:|]+\|$', lines[i + 1].strip()):
        head = ln.count('|')
        j = i + 1
        while j < len(lines) and lines[j].startswith('|'):
            if lines[j].count('|') != head:
                bad.append((j + 1, lines[j].count('|'), head, lines[j][:90]))
            j += 1
        i = j
    else:
        i += 1
print('mismatched rows:', len(bad))
for b in bad:
    print(b)
# stray placeholders
for n, ln in enumerate(lines, 1):
    if 'CONTINUE-PART' in ln or 'TODO' in ln or 'TBD' in ln:
        print('stray', n, ln[:80])
