import re, sys, io
p = r'04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E2017 APP Contract, CA and mortgage document generation screens v1.md'
t = open(p, encoding='utf-8').read()
S = ['Story','Business rationale','Preconditions','Flow','Exception paths','INVEST check','Acceptance criteria','Business rules','State transitions','Authority','Data','Contract','Solution plan','Validation and messages','Screens and states','Test cases','Guardrails','Traceability','Out of scope']
h = re.findall(r'^### (\d+)\. (.+?)[ \t]*$', t, re.M)
print('sections ok:', [x for n, x in h[:19]] == S, [int(n) for n, _ in h[:19]] == list(range(1, 20)), len(h))
acs = re.findall(r'^\s*Scenario: AC\d+.*$', t, re.M)
print('ac count', len(acs))
for a in acs:
    print(' ', a[:40], '|', a[-22:])
print('cites', sorted(set(re.findall(r'\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b', t))))
print('tcs', len(set(re.findall(r'TC-(?:E2-017|P6-E2017-APP)-\d+', t))))
# metadata order check
pre = t.split('### 1.', 1)[0]
rows = [r.strip() for r in re.findall(r'^\|\s*([^|]+?)\s*\|', pre, re.M)]
META = ["Story key","Work type","Suggested owner","Service","Service epic","Wave","Business epic","Release","Legacy key","Legacy disposition","Build status","Patterns applied","Parallel lane","Ready to start","Depends on (build)","Contract dependencies","Integration dependencies","External dependencies","PRD reference","Status"]
got = [r for r in rows if r in META]
print('meta ok:', got == META, len(got))
# per-section sizes
parts = re.split(r'^### (\d+)\. ', t, flags=re.M)
print('total bytes', len(t.encode('utf-8')))
for i in range(1, len(parts), 2):
    print(parts[i], len(parts[i+1].encode('utf-8')))
