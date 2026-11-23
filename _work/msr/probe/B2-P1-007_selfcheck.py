import re, csv, json
from pathlib import Path

p = Path('04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 DM008 APP Migrate partner performance v1.md')
t = p.read_text(encoding='utf-8')
MET = ['Story key', 'Work type', 'Suggested owner', 'Service', 'Service epic', 'Wave', 'Business epic', 'Release',
       'Legacy key', 'Legacy disposition', 'Build status', 'Patterns applied', 'Parallel lane', 'Ready to start',
       'Depends on (build)', 'Contract dependencies', 'Integration dependencies', 'External dependencies', 'PRD reference', 'Status']
rows = re.findall(r'^\|\s*([^|]+?)\s*\|', t.split('### 1.', 1)[0], re.M)
got = [r for r in rows if r in MET]
print('meta ok:', got == MET, len(got))
SEC = ['Story', 'Business rationale', 'Preconditions', 'Flow', 'Exception paths', 'INVEST check', 'Acceptance criteria',
       'Business rules', 'State transitions', 'Authority', 'Data', 'Contract', 'Solution plan', 'Validation and messages',
       'Screens and states', 'Test cases', 'Guardrails', 'Traceability', 'Out of scope']
h = re.findall(r'^### (\d+)\. (.+?)\s*$', t, re.M)
print('sections ok:', [x[1] for x in h] == SEC, [int(x[0]) for x in h] == list(range(1, 20)))
print('ac lines:', [l for l in t.splitlines() if re.match(r'^\s*Scenario:\s*AC\d+', l)])
print('jira hit:', bool(re.search(r'(?i)\bjira\b|atlassian\.net', t)))
print('emails:', re.findall(r'\b[\w.+-]+@[\w-]+\.[\w.]+\b', t))

names = set()
for q in Path('.').glob('21*/**/*'):
    if q.suffix.lower() == '.csv':
        with open(q, encoding='utf-8', errors='ignore', newline='') as f:
            for row in csv.DictReader(f):
                for k, v in row.items():
                    if k and re.search(r'(?i)assignee|reporter|creator|watcher|author|updated by', k) and v and ' ' in v.strip():
                        names.add(v.strip().lower())
    elif q.suffix.lower() == '.json':
        txt = q.read_text(encoding='utf-8', errors='ignore')
        names.update(n.lower() for n in re.findall(r'"displayName"\s*:\s*"([^"@]+ [^"@]+)"', txt))
print('names count:', len(names))
files = {
    'story': t.lower(),
    'gaps': Path('_work/msr/gaps/B2-P1-007.jsonl').read_text(encoding='utf-8').lower(),
    'asm': Path('_work/msr/assumptions/B2-P1-007.jsonl').read_text(encoding='utf-8').lower(),
    'frag': Path('_work/msr/fragments/RWB-P1-DM008-APP.json').read_text(encoding='utf-8').lower(),
}
for k, v in files.items():
    print('name hits', k, sorted(n for n in names if n in v))

f = json.loads(files['frag'])
for k in ['id', 'epic', 'service', 'wt', 'lane', 'ready', 'owner', 'business_epic', 'wave', 'release', 'legacy',
          'disposition', 'H', 'C', 'I', 'X', 'acs', 'tcs', 'reqs', 'ops_provided', 'ops_consumed',
          'events_published', 'events_consumed', 'workflows', 'prd_ref', 'gaps', 'assumptions', 'file']:
    if k not in f:
        print('fragment missing key:', k)
print('tentative in story:', '(tentative)' in t)
print('release in frag:', f['release'])
print('D-RCV-60 in story:', 'D-RCV-60' in t)
print('task queue token check:', sorted(set(re.findall(r'queue `?rwb-([a-z-]+)', t))))
print('topics:', sorted(set(re.findall(r'rwb\.([a-z-]+)\.events\.v1', t))))
print('api bases:', sorted(set(re.findall(r'/api/recovery/([a-z-]+)/v1', t))))
print('bytes:', len(t.encode('utf-8')))
