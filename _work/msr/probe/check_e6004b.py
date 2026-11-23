import re, json, pathlib
META = ['Story key','Work type','Suggested owner','Service','Service epic','Wave','Business epic','Release','Legacy key','Legacy disposition','Build status','Patterns applied','Parallel lane','Ready to start','Depends on (build)','Contract dependencies','Integration dependencies','External dependencies','PRD reference','Status']
SHORTS = {'debtsale','case','access','decision','partner','source-data','document','comms','payment','reporting','agent','integration','valuation','treatment','guarantee','litigation','asset','writeoff','deviation'}
base = pathlib.Path("04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S6 rwb-debtsale (Debt sale)")
files = [base / "RWB S6 E6004 APP Take buyer bids v1.md", base / "RWB S6 E6004 CON Take buyer bids - contract v1.md"]
ids = set()
for p in list(pathlib.Path('_work/msr/gaps').glob('*.jsonl')) + list(pathlib.Path('_work/msr/assumptions').glob('*.jsonl')):
    for l in p.read_text(encoding='utf-8').splitlines():
        if l.strip():
            ids.add(json.loads(l)['id'])
for p in files:
    t = p.read_text(encoding='utf-8'); f = []
    rows = [r for r in re.findall(r'^\|\s*([^|]+?)\s*\|', t.split('### 1.', 1)[0], re.M) if r in META]
    if rows != META: f.append('meta %s' % [r for r in META if r not in rows])
    for line in t.splitlines():
        if re.match(r'^\s*Scenario:\s*AC\d+', line) and not re.search(r'\((legacy RWB-[A-Z0-9-]+ AC\d+|new, D-RCV-60)\)', line):
            f.append('ac tag: ' + line[:70])
    for rx, g in [(r'\brwb\.([a-z-]+)\.events\.v1\b', 1), (r'/api/recovery/([a-z-]+)/v1\b', 1), (r'\bqueue rwb-([a-z-]+)\b', 1)]:
        for m in re.finditer(rx, t):
            if m.group(g) not in SHORTS: f.append('svc name ' + m.group(0))
    if re.search(r'/api/recovery/v1/', t): f.append('monolith base')
    if re.search(r'(?i)\bjira\b|atlassian\.net', t): f.append('tracker')
    if re.search(r'\b[\w.+-]+@[\w-]+\.[\w.]+\b', t): f.append('email')
    if 'As built (monolith)' in t: f.append('as-built in a non-preserved story')
    for c in sorted(set(re.findall(r'\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b', t))):
        if c not in ids: f.append('bad cite ' + c)
    print(p.name, 'OK' if not f else f)
