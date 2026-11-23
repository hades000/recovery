import re, json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
base = Path('04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration')
ids = ['RWB-ITG-E1030-ITG','RWB-ITG-E1031-ITG','RWB-ITG-E1032-ITG','RWB-ITG-E1034-ITG','RWB-ITG-E1037-ITG']
META = ["Story key","Work type","Suggested owner","Service","Service epic","Wave","Business epic","Release","Legacy key","Legacy disposition","Build status","Patterns applied","Parallel lane","Ready to start","Depends on (build)","Contract dependencies","Integration dependencies","External dependencies","PRD reference","Status"]
SECT = ["Story","Business rationale","Preconditions","Flow","Exception paths","INVEST check","Acceptance criteria","Business rules","State transitions","Authority","Data","Contract","Solution plan","Validation and messages","Screens and states","Test cases","Guardrails","Traceability","Out of scope"]
for i in ids:
    fs = [p for p in base.glob('*%s*.md' % i[-8:]) if p.name.startswith('RWB ITG')]
    # pick by id compact
    compact = i.split('-')[2]
    fs = [p for p in base.glob('RWB ITG %s ITG*.md' % compact)]
    p = fs[0]
    t = p.read_text(encoding='utf-8')
    print('='*100); print(p.name, len(t.splitlines()), 'lines')
    head = t.splitlines()[0]
    print('H1:', head)
    pre = t.split('### 1.',1)[0]
    rows = re.findall(r'^\|\s*([^|]+?)\s*\|', pre, re.M)
    got = [r for r in rows if r in META]
    print('META ok:', got == META)
    if got != META:
        print('  missing:', [r for r in META if r not in got], 'extra:', [r for r in got if r not in META])
    heads = re.findall(r'^### (\d+)\. (.+?)\s*$', t, re.M)
    print('SECTIONS ok:', [h[1] for h in heads[:19]] == SECT and [int(h[0]) for h in heads[:19]] == list(range(1,20)), 'count', len(heads))
    print('12.x:', re.findall(r'^#### (12\.\d)', t, re.M))
    scen = [l for l in t.splitlines() if re.match(r'^\s*Scenario:\s*AC\d+', l)]
    bad = [l for l in scen if not re.search(r'\((legacy RWB-[A-Z0-9-]+ AC\d+|new, D-RCV-60)\)', l)]
    print('scenarios:', len(scen), 'untagged:', len(bad))
    print('TC ids:', len(re.findall(r'\bTC-(?:E1-\d{3}|ITG-E\d{4}-ITG)-\d{2}(?:-ITG)?\b', t)))
    for w in ['Jira','jira','@','Co-Authored-By','Claude']:
        if w in t: print('  !! contains', w)
    # fragment
    fp = Path('_work/msr/fragments') / (i + '.json')
    d = json.loads(fp.read_text(encoding='utf-8'))
    keys = list(d)
    want = ["id","epic","service","wt","lane","ready","owner","business_epic","wave","release","legacy","disposition","H","C","I","X","acs","tcs","reqs","ops_provided","ops_consumed","events_published","events_consumed","workflows","prd_ref","gaps","assumptions","file"]
    print('fragment keys ok:', keys == want, 'acs', len(d['acs']), 'tcs', len(d['tcs']))
    print('file match:', d['file'] == '04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/' + p.name)
    # AC ids in fragment vs doc
    docids = [re.match(r'^\s*Scenario:\s*(AC\d+)', l).group(1) for l in scen]
    fragids = [a['id'] for a in d['acs']]
    print('AC ids align:', docids == fragids)
    # first lines present in doc
    miss = [a['text_first_line'] for a in d['acs'] if a['text_first_line'] not in t]
    print('AC first lines in doc:', len(miss) == 0, miss[:2])
