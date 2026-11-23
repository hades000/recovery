import re
src = r'03 Requirements and specifications/Recovery Workbench Business Requirements Epics 3 to 8 v1.md'
dst = r'_work/msr/docs/B-REQ-BRD-E38/Recovery Workbench Business Requirements Epics 3 to 8 v1.docx.md'
t = open(src, encoding='utf-8').read()
lines = t.splitlines()
# drop the YAML front-matter block (between the first two --- lines) so the docx body starts with the header lines
start = next(i for i, l in enumerate(lines) if l.strip() == '---')
end = next(i for i, l in enumerate(lines[start + 1:], start + 1) if l.strip() == '---')
kept = lines[:start] + lines[end + 1:]
while kept and not kept[0].strip():
    kept.pop(0)
open(dst, 'w', encoding='utf-8', newline='\n').write('\n'.join(kept) + '\n')
print('wrote', dst, len(kept), 'lines')
