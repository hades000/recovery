import io, re, glob, json, os

p = r'03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md'
t = io.open(p, encoding='utf-8').read()

ids = set()
for g in glob.glob(r'_work/msr/gaps/*.jsonl') + glob.glob(r'_work/msr/assumptions/*.jsonl'):
    for ln in io.open(g, encoding='utf-8'):
        ln = ln.strip()
        if ln:
            ids.add(json.loads(ln).get('id'))

cited = sorted(set(re.findall(r'\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b', t)))
missing = [c for c in cited if c not in ids]
print('cited', len(cited), 'missing', missing)

# ID uniqueness and monotonic checks
fr = re.findall(r'FR-PLT-(\d{3})', t)
cap = re.findall(r'CAP-PLT-(\d{3})', t)
nfr = re.findall(r'NFR-PLT-(\d{3})', t)
ac = re.findall(r'AC-PLT-(\d{3})', t)
q = re.findall(r'Q-PLT-(\d{2})', t)
for name, seq in (('FR', fr), ('CAP', cap), ('NFR', nfr), ('AC', ac), ('Q', q)):
    print(name, 'distinct', len(set(seq)), 'min', min(seq), 'max', max(seq))
