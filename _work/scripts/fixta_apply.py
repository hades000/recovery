"""Apply verify defects to Target Architecture v5 (docx+pptx) and ACE Architecture Decision v3 (docx). In place."""
import zipfile, re, os, shutil
from xml.dom import minidom
D = "05 Technical architecture/"
TA_DOCX = D + "Recovery Workbench Target Architecture v5.docx"
TA_PPTX = D + "Recovery Workbench Target Architecture v5.pptx"
AD_DOCX = D + "Recovery Workbench ACE Architecture Decision v3.docx"

def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def rep(x, old, new):
    o, n = esc(old), esc(new)
    assert x.count(o) == 1, (old, x.count(o))
    return x.replace(o, n)

def clone_row(x, tag, anchor, texts):
    """Clone the table row holding anchor; set the cloned cells' texts; insert after it."""
    i = x.find(esc(anchor)); assert i > 0, anchor
    s = x.rfind('<%s:tr ' % tag, 0, i); s2 = x.rfind('<%s:tr>' % tag, 0, i); s = max(s, s2)
    e = x.find('</%s:tr>' % tag, i) + len('</%s:tr>' % tag)
    row = x[s:e]
    cells = re.findall(r'<%s:tc[ >].*?</%s:tc>' % (tag, tag), row, re.S)
    assert len(cells) == len(texts), (len(cells), texts)
    newrow = row
    for c, t in zip(cells, texts):
        ts = re.findall(r'<%s:t(?: [^>]*)?>[^<]*</%s:t>' % (tag, tag), c)
        assert len(ts) == 1, ('multi-run cell', c[:200])
        newc = c.replace(ts[0], '<%s:t xml:space="preserve">%s</%s:t>' % (tag, esc(t), tag) if tag == 'w' else '<a:t>%s</a:t>' % esc(t))
        newrow = newrow.replace(c, newc, 1)
    return x[:e] + newrow + x[e:]

def insert_para_after(x, anchor, text):
    i = x.find(esc(anchor)); assert i > 0
    s = max(x.rfind('<w:p ', 0, i), x.rfind('<w:p>', 0, i)); e = x.find('</w:p>', i) + 6
    p = x[s:e]
    ppr = re.search(r'<w:pPr>.*?</w:pPr>', p, re.S)
    rpr = re.search(r'<w:rPr>.*?</w:rPr>', p, re.S)
    np = '<w:p>%s<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:p>' % (ppr.group(0) if ppr else '', rpr.group(0) if rpr else '', esc(text))
    return x[:e] + np + x[e:]

def rewrite(path, edits):
    zin = zipfile.ZipFile(path)
    tmp = path + '.tmp'
    with zipfile.ZipFile(tmp, 'w') as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename in edits:
                x = data.decode('utf-8')
                x = edits[info.filename](x)
                minidom.parseString(x.encode('utf-8'))  # validate
                data = x.encode('utf-8')
            zout.writestr(info, data, compress_type=info.compress_type)
    zin.close()
    shutil.move(tmp, path)

# ---------- shared wording ----------
DL12_OLD = 'Taken, DL12'
DL12_NEW = 'Taken; D-RCV-35 (supersedes DL12 option A)'
E1_A_OLD = 'P1 read-only ACE views for Tier 1 and the extension tables'
E1_A_NEW = 'P1 read-only ACE views for Tier 1 (RWB-E1-069) and the extension tables'
E1_B_OLD = 'the Tier 2 views follow the ACE additions (DL43)'
E1_B_NEW = 'Tier 2 after RWB-ACE-001: the Tier 2 views ship when the ACE additions land (DL43)'
RISK_ANCHOR = 'A source is not ingested by ACE'
RISK = ['RWB-ACE-001 lands late',
        'The Tier 2 views, and the features that read them, cannot ship on their planned release',
        'Tier 2 features stay behind their feature flags until RWB-ACE-001 lands; Tier 1 views ship with RWB-E1-069; scope and dates confirmed under DL43']
ING_OLD = 'SVAF, CCMS, AMIS, RPS, LIT, WIN, GL, COLLINS scores, SCBPDM, NLEADS, EasyApp, Entra ID'
ING_NEW = 'ALS, EFS, COLLINS (today); SVAF, CCMS, AMIS, RPS, LIT, WIN, GL, COLLINS scores, SCBPDM, NLEADS, EasyApp, Entra ID'

def ta_docx(x):
    x = rep(x, DL12_OLD, DL12_NEW)                                           # 2
    x = rep(x, 'A load, a screen action', 'An ACE refresh, a screen action')   # 6.1
    x = rep(x, 'Personal data fields masked unless the role is allowed to see them',
               'Personal data masked in the views and at the API unless the role is allowed to see it')  # 8.2
    x = insert_para_after(x, 'Tier 1 views ship with RWB-E1-069',
        'The tier table above is the normative data tier diagram for this document. Slide 11 of the '
        'Recovery Workbench Target Architecture v5 deck draws the same four tiers and the single read path.')  # 8.1.1
    x = rep(x, E1_A_OLD, E1_A_NEW); x = rep(x, E1_B_OLD, E1_B_NEW)           # 9
    x = clone_row(x, 'w', RISK_ANCHOR, RISK)                                 # 11
    x = clone_row(x, 'w', 'Further ACE deployment slots',
                  ['DL43', 'Whether the ACE team accepts the RWB-ACE-001 scope and its dates (needed by 21 November 2026)'])  # 12
    return x

def s3(x): return rep(x, DL12_OLD, DL12_NEW)
def s2(x): return rep(x, ING_OLD, ING_NEW)
def s15(x): return rep(rep(x, E1_A_OLD, E1_A_NEW), E1_B_OLD, E1_B_NEW)
def s17(x):
    x = clone_row(x, 'a', RISK_ANCHOR, RISK)
    m = re.search(r'(<a:off x="566928" y="1051560"/><a:ext cx="11064240" cy=")(\d+)(")', x)
    x = x[:m.start(2)] + str(int(m.group(2)) + 256032) + x[m.end(2):]
    return x

def ad_docx(x):
    x = rep(x, "; recovery takes ACE's end of day data position", '')          # 2 option 1 Against
    x = rep(x, 'Spring Batch for loads and automated chains', 'Spring Batch for automated chains')  # 3.4
    x = rep(x, 'Batch for Epics 1 and 2; same-day triggers named now',
               'Option A (daily batch through COLLINS) superseded by D-RCV-35. Same-day triggers stay named; they depend on what ACE ingests')  # 8
    return x

if __name__ == '__main__':
    rewrite(TA_DOCX, {'word/document.xml': ta_docx})
    rewrite(TA_PPTX, {'ppt/slides/slide2.xml': s2, 'ppt/slides/slide3.xml': s3, 'ppt/slides/slide11.xml': s2,
                      'ppt/slides/slide15.xml': s15, 'ppt/slides/slide17.xml': s17})
    rewrite(AD_DOCX, {'word/document.xml': ad_docx})
    print('done')
