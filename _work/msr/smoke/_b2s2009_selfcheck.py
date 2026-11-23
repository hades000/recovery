import json
import pathlib
import re

root = pathlib.Path('.')
d = root / '04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S2 rwb-treatment (Treatment and offer)'
files = {
    'APP': d / 'RWB S2 E3014 APP Unlock the asset as a non performing asset by rule v1.md',
    'CON': d / 'RWB S2 E3014 CON Unlock the asset as a non performing asset by rule - contract v1.md',
}
meta_order = ['Story key', 'Work type', 'Suggested owner', 'Service', 'Service epic', 'Wave', 'Business epic',
              'Release', 'Legacy key', 'Legacy disposition', 'Build status', 'Patterns applied', 'Parallel lane',
              'Ready to start', 'Depends on (build)', 'Contract dependencies', 'Integration dependencies',
              'External dependencies', 'PRD reference', 'Status']
sec = ['1. Story', '2. Business rationale', '3. Preconditions', '4. Flow', '5. Exception paths', '6. INVEST check',
       '7. Acceptance criteria', '8. Business rules', '9. State transitions', '10. Authority', '11. Data',
       '12. Contract', '13. Solution plan', '14. Validation and messages', '15. Screens and states',
       '16. Test cases', '17. Guardrails', '18. Traceability', '19. Out of scope']

g = [json.loads(x) for x in (root / '_work/msr/gaps/B2-S2-009.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
a = [json.loads(x) for x in (root / '_work/msr/assumptions/B2-S2-009.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
known = {r['id'] for r in g} | {r['id'] for r in a}

ok = True
for k, p in files.items():
    t = p.read_text(encoding='utf-8')
    lines = t.splitlines()
    print('==', k, p.name, len(t), 'bytes')
    print('  title', lines[0])
    print('  header', lines[2] == 'SCB Collections and Recovery. Henka Group, 22 November 2026.' and lines[3] == '(C) Siam Commercial Bank and Henka Pte Ltd')
    print('  change log has D-RCV-60 and tool', 'D-RCV-60' in t and 'T3 Code / OpenCode / DeepSeek v4.1 Flash' in t)
    rows = [m for m in re.findall(r'^\| ([^|]+?) \|', t, re.M)]
    found = [r for r in rows if r in meta_order]
    print('  meta rows in order', found == meta_order, len(found))
    heads = re.findall(r'^### (\d+\. .+)$', t, re.M)
    print('  sections in order', heads == sec, len(heads))
    print('  12.x', re.findall(r'^#### (12\.\d) ', t, re.M))
    acs = re.findall(r'^\s+Scenario: .+\((legacy RWB-E3-014 AC\d|new, D-RCV-60)\)$', t, re.M)
    print('  scenarios', len(acs), acs)
    cited = set(re.findall(r'(?:CG|ASM)-B2-S2-009-\d+', t))
    print('  citations resolve', cited <= known, sorted(cited - known))
    print('  monolith base as own', '/api/recovery/v1' in t)
    print('  email', '@' in t)
    print('  tentative', '31 January 2027 (tentative)' in t)
    # metadata values
    for lbl in ['Story key', 'Work type', 'Patterns applied', 'Parallel lane']:
        m = re.search(r'^\| ' + re.escape(lbl) + r' \| (.+?) \|$', t, re.M)
        print('   ', lbl, '=', m.group(1) if m else None)

for k in ['RWB-S2-E3014-APP', 'RWB-S2-E3014-CON']:
    fr = json.loads((root / '_work/msr/fragments' / (k + '.json')).read_text(encoding='utf-8'))
    print(k, 'fragment keys', len(fr), 'acs', len(fr['acs']), 'tcs', len(fr['tcs']), 'gaps', fr['gaps'], 'asms', len(fr['assumptions']))
    print('  file exists', (root / fr['file']).exists(), 'cited known', set(fr['gaps']) | set(fr['assumptions']) <= known)
print('gaps', len(g), 'assumptions', len(a))
