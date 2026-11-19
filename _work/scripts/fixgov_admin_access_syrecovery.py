import zipfile, shutil, os, tempfile, re
from xml.dom import minidom
P = '01 Decisions and governance/Recovery Workbench Admin and Access Model v5.docx'
zin = zipfile.ZipFile(P)
x = zin.read('word/document.xml').decode('utf-8')
spans = [m.span() for m in re.finditer(r'<w:p[ >].*?</w:p>', x, flags=re.S)]
paras = [x[a:b] for a, b in spans]
def text(p): return ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', p))
def find(pred):
    hits = [i for i, p in enumerate(paras) if pred(text(p))]
    assert len(hits) == 1, hits
    return hits[0]
edits = {}
def set_text(i, old, new):
    p = paras[i]; assert p.count('>' + old + '<') == 1 or p.count(old) == 1, (i, old)
    edits[i] = p.replace(old, new, 1)
i = find(lambda t: t.startswith('A permission matrix of 53 roles'))
set_text(i, '53 roles', '54 roles')
nh = find(lambda t: t == 'Non-human actor')
assert text(paras[nh + 1]) == '5' and text(paras[nh + 4]) == 'Total' and text(paras[nh + 5]) == '53'
set_text(nh + 1, '>5<', '>6<')
set_text(nh + 5, '>53<', '>54<')
i = find(lambda t: t.startswith('The five non-human actors are'))
set_text(i, 'The five non-human actors are the case workflow module, the rules component, the OCR and extraction pipeline, the decision log writer and the agent platform. None of them loads source data; the read path is the ACE views.',
         'The six non-human actors are the case workflow module, the rules component, the OCR and extraction pipeline, the decision log writer, the agent platform and SY-RECOVERY, the recovery service identity. None of them loads source data; SY-RECOVERY holds SELECT on the recovery.v_ace_* views only and has no write on ACE.')
i = find(lambda t: t.startswith('The read path adds two database identities'))
old = text(paras[i])
assert paras[i].count(old) == 1
set_text(i, old,
    'The read path adds one non-human actor and one database role. SY-RECOVERY, the recovery service identity, is the sixth non-human actor in the role catalog: it holds SELECT on the recovery.v_ace_* views only, has no direct read of a public ACE table and no write on any ACE table or view, so a direct read of a public table fails at the database. The ACE view owner (ace_view_owner) is a database role, not a catalog role: it owns the recovery.v_ace_* views and holds SELECT on the ACE tables; it is the only recovery identity that reads the public ACE tables, and it writes neither schema.')
for i in sorted(edits, reverse=True):
    a, b = spans[i]
    x = x[:a] + edits[i] + x[b:]
minidom.parseString(x.encode('utf-8'))
fd, tmp = tempfile.mkstemp(suffix='.docx', dir=os.path.dirname(P)); os.close(fd)
with zipfile.ZipFile(tmp, 'w') as zout:
    for item in zin.infolist():
        data = x.encode('utf-8') if item.filename == 'word/document.xml' else zin.read(item.filename)
        zout.writestr(item, data, compress_type=item.compress_type)
zin.close(); shutil.move(tmp, P)
print('ok', sorted(edits))
