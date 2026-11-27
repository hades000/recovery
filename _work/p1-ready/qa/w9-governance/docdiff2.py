import difflib, os, sys
import docx
from docx.oxml.ns import qn
from w9lib import SET, STAGE


def lines(p):
    d = docx.Document(p)
    out = []
    for el in d.element.body.iterchildren():
        if el.tag == qn('w:p'):
            t = ''.join(x.text or '' for x in el.iter(qn('w:t')))
            if t.strip():
                out.append('P ' + t)
        elif el.tag == qn('w:tbl'):
            for tr in el.findall(qn('w:tr')):
                out.append('R ' + ' | '.join(''.join(x.text or '' for x in tc.iter(qn('w:t'))) for tc in tr.findall(qn('w:tc'))))
    return out


if __name__ == '__main__':
    a = lines(os.path.join(SET, sys.argv[1]))
    b = lines(os.path.join(STAGE, sys.argv[2]))
    for line in difflib.unified_diff(a, b, lineterm='', n=0):
        print(line[:1200])
