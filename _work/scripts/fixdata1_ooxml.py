"""Fix agent data1: CDM v6 pptx (D2, D3, G11 minor) and Party MDM v3 docx (D5/D8, D6, D9 note).
zipfile + XML string edits; every other part is copied unchanged."""
import os
import shutil
import tempfile
import zipfile
import xml.dom.minidom

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data'


def rewrite(path, edits):
    """edits: {part: [(old, new), ...]}; each old must occur exactly once."""
    zin = zipfile.ZipFile(path)
    fd, tmp = tempfile.mkstemp(suffix=os.path.splitext(path)[1])
    os.close(fd)
    zout = zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED)
    for info in zin.infolist():
        data = zin.read(info.filename)
        if info.filename in edits:
            x = data.decode('utf-8')
            for old, new in edits[info.filename]:
                assert x.count(old) == 1, (info.filename, old[:80], x.count(old))
                x = x.replace(old, new)
            xml.dom.minidom.parseString(x.encode('utf-8'))  # well-formed
            data = x.encode('utf-8')
        zout.writestr(info, data)
    zout.close()
    zin.close()
    with zipfile.ZipFile(tmp) as z:
        assert z.testzip() is None
    shutil.move(tmp, path)


# ---------- CDM v6 pptx ----------
rewrite(os.path.join(ROOT, 'Recovery Workbench Conceptual Data Model v6.pptx'), {
    'docProps/core.xml': [('<dc:title>Recovery Workbench Conceptual Data Model v5</dc:title>',
                           '<dc:title>Recovery Workbench Conceptual Data Model v6</dc:title>')],
    'ppt/slides/slide9.xml': [('The model holds what COLLINS carries.',
                               'The model holds the ACE account at its current state and the monthly bucket snapshot.')],
    'ppt/slides/slide10.xml': [('Retention follows the bank schedule once read.',
                                'Retention follows the bank schedule once received.')],
})

# ---------- Party and Customer MDM v3 docx ----------
D = 'word/document.xml'
M5_OLD = ('<w:t xml:space="preserve"> ACE treats the records as one firm; the partner and agency manager confirms '
          'the panel entry in the Workbench partner master.</w:t></w:r></w:p>')
M5_NEW = ('<w:t xml:space="preserve"> Run in the Workbench partner master, not in ACE ingestion: a partner firm is a '
          'Workbench record, not an ACE customer. The Workbench treats the records as one firm and the partner and '
          'agency manager confirms the panel entry.</w:t></w:r></w:p>'
          # D6: restored rule, same paragraph format as the M rules
          '<w:p><w:pPr><w:pStyle w:val="ListParagraph"/><w:spacing w:after="80" w:before="0" w:line="276"/>'
          '<w:ind w:left="0" w:firstLine="0"/></w:pPr>'
          '<w:r><w:rPr><w:rFonts w:ascii="Aptos" w:cs="Aptos" w:eastAsia="Aptos" w:hAnsi="Aptos"/><w:b/></w:rPr>'
          '<w:t>Cases.</w:t></w:r><w:r><w:t xml:space="preserve"> A case is never merged by the party match; '
          'duplicate cases follow R-UNI-17.</w:t></w:r></w:p>')
rewrite(os.path.join(ROOT, 'Recovery Workbench Party and Customer Master Data Design v3.docx'), {
    D: [
        ('<w:t>Run in ACE ingestion under M1 to M5. The Workbench',
         '<w:t>Run in ACE ingestion under M1 to M4. M5, the partner tax ID match, runs in the Workbench partner master. The Workbench'),
        ('<w:t>3. Matching rules run in ACE</w:t>', '<w:t>3. Matching rules</w:t>'),
        ('<w:t>M1 to M5 are ACE ingestion rules. They run',
         '<w:t>M1 to M4 are ACE ingestion rules; M5 matches partner firms and runs in the Workbench partner master. M1 to M4 run'),
        (M5_OLD, M5_NEW),
        ('party_type, id_type and segment appear in v_ace_customer when RWB-ACE-001 lands;',
         'party_type, id_type and segment appear in v_ace_customer (Section B, after RWB-ACE-001) when RWB-ACE-001 lands;'),
    ],
})
print('ooxml done')
