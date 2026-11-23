"""Compare the rendered Markdown with the text extracted back from the docx."""
import re
import sys
from pathlib import Path

md = Path('_work/msr/docs/B-TESTDOC-39/Recovery Workbench Test Strategy v3.md').read_text(encoding='utf-8')
back = Path('_work/msr/docs/B-TESTDOC-39/verify/Recovery Workbench Test Strategy v3.md').read_text(encoding='utf-8')


def norm(t):
    out = []
    for line in t.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith('|'):
            cells = [c.strip() for c in line.strip('|').split('|')]
            if all(set(c) <= set('-: ') for c in cells):
                continue
            out.append(' | '.join(cells))
        elif line.startswith('#'):
            out.append(re.sub(r'^#+\s*', '', line))
        else:
            out.append(line)
    return out


a, b = norm(md), norm(back)
print('md lines', len(a), 'docx lines', len(b))
missing = [x for x in a if x not in b]
extra = [x for x in b if x not in a]
print('missing in docx:', len(missing))
for x in missing[:10]:
    print('  -', x[:160])
print('extra in docx:', len(extra))
for x in extra[:10]:
    print('  +', x[:160])
