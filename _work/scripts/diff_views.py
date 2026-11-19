import io, re
v = io.open(r'15 ACE DB Alignment\Recovery Workbench ACE Source Views v1.sql', encoding='utf-8').read()
parts = re.split(r'CREATE OR REPLACE VIEW recovery\.', v)[1:]
for p in parts:
    name = re.match(r'([a-z_]+)', p).group(1)
    if ' AS\n' not in p:
        continue
    body = p.split(' AS\n', 1)[1]
    m = re.search(r'\nFROM ', body)
    sel = body[:m.start()] if m else body
    total = len(re.findall(r'\bAS\s+([a-z_][a-z0-9_]*)', sel))
    line = 0
    for ln in sel.split('\n'):
        ln = ln.strip().rstrip(',')
        if re.match(r"^(.*?)\s+AS\s+([a-z_][a-z0-9_]*)$", ln):
            line += 1
    if total != line:
        print('MISMATCH', name, total, line)
        for ln in sel.split('\n'):
            ln2 = ln.strip().rstrip(',')
            if ' AS ' in ln2 and not re.match(r"^(.*?)\s+AS\s+([a-z_][a-z0-9_]*)$", ln2):
                print('   ', ln2[:120])
