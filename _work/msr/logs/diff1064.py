import io, re, sys
leg = io.open(r'04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB E1 064 Data dictionary for the 14 data products v1.md', encoding='utf-8').read()
new = io.open(r'04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1064 APP Data dictionary for the 14 data products v1.md', encoding='utf-8').read()

def block(t):
    s = t.split('```gherkin', 1)[1].split('```', 1)[0]
    return [l.rstrip() for l in s.splitlines()]

a = block(leg); b = block(new)
print('lines', len(a), len(b))
norm = lambda ls: [re.sub(r'\(legacy RWB-E1-064 AC\d+\)$', '', l).rstrip() for l in ls]
a2 = norm(a); b2 = norm(b)
for i, (x, y) in enumerate(zip(a2, b2)):
    if x != y:
        print('DIFF', i, repr(x), '||', repr(y))
if len(a2) != len(b2):
    print('extra in new:', b2[len(a2):])
    print('missing:', a2[len(b2):])
