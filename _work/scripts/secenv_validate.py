import sys, zipfile, re
from lxml import etree
import docx
for f in sys.argv[1:]:
    z = zipfile.ZipFile(f)
    assert z.testzip() is None
    for n in z.namelist():
        if n.endswith('.xml') or n.endswith('.rels'):
            etree.fromstring(z.read(n))
    d = docx.Document(f)
    txt = '\n'.join([p.text for p in d.paragraphs] + [c.text for t in d.tables for r in t.rows for c in r.cells])
    print(f, 'OK', d.core_properties.title, d.core_properties.modified, 'paras', len(d.paragraphs))
    for w in ['tokenized at load', 'data load,', 'for loads', 'Load failure', 'previous load', 'Version | 1']:
        if w.lower() in txt.lower(): print('  STILL:', w)
    print('  styles:', sorted({p.style.name for p in d.paragraphs}))
