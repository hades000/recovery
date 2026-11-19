import os, re, io, glob

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14'
folders = [r'04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6']
bad = []
for folder in folders:
    for path in glob.glob(os.path.join(ROOT, folder, '*.md')):
        text = io.open(path, encoding='utf-8-sig', errors='replace').read()
        # scenario blocks inside gherkin fences
        for block in re.findall(r'```gherkin(.*?)```', text, re.S):
            cur = None
            whens = 0
            for line in block.split('\n'):
                m = re.match(r'\s*Scenario:\s*(.*)', line)
                if m:
                    if cur and whens > 1:
                        bad.append((os.path.basename(path), cur, whens))
                    cur = m.group(1).strip()
                    whens = 0
                elif re.match(r'\s*When\s+', line):
                    whens += 1
            if cur and whens > 1:
                bad.append((os.path.basename(path), cur, whens))
print('scenarios with >1 When:', len(bad))
for x in bad[:80]:
    print(x[2], '|', x[0], '|', x[1])
