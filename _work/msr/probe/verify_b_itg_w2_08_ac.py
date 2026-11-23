import re

leg = open('04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md', encoding='utf-8').read()
base = '04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/'


def block(t, head):
    i = t.index('## ' + head)
    j = t.index('**Data**', i)
    return t[i:j]


def acs(t):
    out = {}
    for m in re.finditer(r'Scenario: (AC\d+)(.*?)(?=\n\s*Scenario:|\n```)', t, re.S):
        out[m.group(1)] = [l.strip() for l in (m.group(1) + m.group(2)).splitlines() if l.strip()]
    return out


cases = [
    ('RWB-E3-006 Calculate the plan installment', 'E3006', 'AC2',
     'RWB ITG E3006 ITG Calculate the plan installment - integration v1.md'),
    ('RWB-E3-010 Book the plan and set the schedule', 'E3010', 'AC1',
     'RWB ITG E3010 ITG Book the plan and set the schedule - integration v1.md'),
]
for head, sid, ac, filen in cases:
    want = acs(block(leg, head))[ac]
    t = open(base + filen, encoding='utf-8').read()
    m = re.search(r'Scenario: ' + ac + r'.*?(?=\n\s*```)', t, re.S)
    got = [x.strip() for x in m.group(0).splitlines() if x.strip()]
    got[0] = re.sub(r'\s*\(legacy [^)]+\)$', '', got[0])
    print(sid, 'MATCH' if want == got else 'DIFF')
    if want != got:
        for a, b in zip(want, got):
            if a != b:
                print('  legacy:', a)
                print('  story :', b)
        print('  lengths', len(want), len(got))
