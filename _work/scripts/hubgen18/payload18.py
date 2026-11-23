"""Build the v18 hub payload from the current (D-RCV-60) document set.

Reads only. Writes _work/data/hub18_payload.json and hub18_blobs.json.
"""
import base64
import gzip
import io
import json
import os
import re
import sys
import zipfile

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14'
sys.path.insert(0, os.path.join(ROOT, '_work', 'scripts', 'hubgen'))
import types            # noqa: E402
from html.parser import HTMLParser  # noqa: E402

# bs4 is not installed: stub it, and read HTML with the standard library instead
sys.modules.setdefault('bs4', types.SimpleNamespace(BeautifulSoup=None))
import extract          # noqa: E402  (read-only reuse of the v16 extractor)


class _HtmlSecs(HTMLParser):
    SKIP = {'script', 'style', 'noscript', 'svg', 'nav'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.secs, self.cur, self.skip, self.head = [], {'h': 'Top', 'l': 1, 'lines': []}, 0, None
        self.row, self.cell = None, None

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        elif tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6') and not self.skip:
            self.head = (int(tag[1]), [])
        elif tag == 'tr':
            self.row = []
        elif tag in ('td', 'th') and self.row is not None:
            self.cell = []
        elif tag in ('br', 'p', 'li', 'div') and not self.skip:
            self.cur['lines'].append('')

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip = max(0, self.skip - 1)
        elif self.head and tag == 'h%d' % self.head[0]:
            text = re.sub(r'\s+', ' ', ''.join(self.head[1])).strip()
            if text:
                extract._flush(self.secs, self.cur)
                self.cur = {'h': text, 'l': self.head[0], 'lines': []}
            self.head = None
        elif tag in ('td', 'th') and self.cell is not None:
            self.row.append(re.sub(r'\s+', ' ', ''.join(self.cell)).strip())
            self.cell = None
        elif tag == 'tr' and self.row is not None:
            if any(self.row):
                self.cur['lines'].append(' | '.join(self.row))
            self.row = None

    def handle_data(self, data):
        if self.skip:
            return
        if self.head:
            self.head[1].append(data)
        elif self.cell is not None:
            self.cell.append(data)
        elif data.strip():
            self.cur['lines'].append(data.strip())


def _extract_html(path):
    p = _HtmlSecs()
    p.feed(io.open(path, encoding='utf-8-sig', errors='replace').read())
    extract._flush(p.secs, p.cur)
    return p.secs or [{'h': 'Document', 'l': 1, 't': ''}]


extract.extract_html = _extract_html
import build_payload as bp  # noqa: E402

DATA = os.path.join(ROOT, '_work', 'data')
OUT = os.path.join(DATA, 'hub18_payload.json')
BLOBS = os.path.join(DATA, 'hub18_blobs.json')

FOLDERS = [
    '01 Decisions and governance', '02 Business architecture and process',
    '03 Requirements and specifications', '04 User stories', '05 Technical architecture',
    '06 Data', '07 Screens and experience', '08 AI and agents', '09 Testing and quality',
    '10 Policy, controls and compliance', '11 Delivery and operations',
    '12 Project communication', '14 Story Updates', '15 ACE DB Alignment',
    '16 Temporal and Drools Adoption', '22 Microservice Realignment', '23 Document Gaps',
]
TEXT_EXT = {'.md', '.docx', '.pptx', '.xlsx', '.html', '.sql', '.yaml', '.yml', '.pdf', '.zip', '.txt'}
MEMBER_EXT = {'.md', '.yaml', '.yml', '.sql', '.txt'}
# versioned sub-folders read member by member (latest version of each family only)
SUBFOLDER_FAMILIES = ('Functional Specifications by Module', 'Technical Specifications by Module',
                      'API Specification', 'Physical Schema')
UNVERSIONED_SUBFOLDERS = {('03 Requirements and specifications', 'PRD')}
EMBED_MAX = 4 * 1024 * 1024    # larger originals stay in the SharePoint folder only
VER = re.compile(r'^(.*?)\s+v(\d+)$')

# new keys: RWB-P1-E1001-APP, RWB-PLT-N001-CON, RWB-ITG-E1001-ITG ...
NEWKEY = r'RWB-(?:P10|P[1-9]|S[1-9]|PLT|ITG|ACE|AD|DM|TE)-(?=[A-Z]*\d)[A-Z0-9]{3,7}-[A-Z]{2,3}(?:-\d+)?'
EXTRA_KINDS = {
    'NSTORY': 'Service story (D-RCV-60)',
    'SEPIC': 'Service, platform or integration epic',
    'GAP': 'Document gap',
    'ASM': 'Assumption',
    'FR': 'PRD functional requirement',
    'DP': 'Design pattern',
}
EXTRA_PATTERNS = [
    ('NSTORY', NEWKEY),
    ('SEPIC', r'RWB-(?:SVC-(?:P10|P[1-9]|S[1-9])|PLT-[A-Z]{2,4}|ITG-(?:W[1-4]|NFR))'),
    ('GAP', r'GAP-\d{4}'),
    ('ASM', r'ASM-\d{4}'),
    ('FR', r'FR-(?:P10|P[1-9]|S[1-9])-\d{3}'),
]


def fam(name):
    stem, ext = os.path.splitext(name)
    m = VER.match(stem)
    return (m.group(1), int(m.group(2))) if m else (stem, 0), ext.lower()


def latest(names):
    best = {}
    for n in names:
        (stem, ver), ext = fam(n)
        k = (stem, ext)
        if k not in best or ver > best[k][0]:
            best[k] = (ver, n)
    return sorted(v[1] for v in best.values())


def manifest():
    rows = []
    for folder in FOLDERS:
        base = os.path.join(ROOT, folder)
        if not os.path.isdir(base):
            continue
        files = [n for n in os.listdir(base) if os.path.isfile(os.path.join(base, n))
                 and os.path.splitext(n)[1].lower() in TEXT_EXT and 'Project Hub' not in n]
        if folder == '04 User stories':
            files = [n for n in files if 'Story Files' not in n or 'Service Story Files' in n]
        for n in latest(files):
            rows.append({'folder': folder, 'file': n, 'path': os.path.join(base, n)})
        dirs = [n for n in os.listdir(base) if os.path.isdir(os.path.join(base, n))]
        pick = [d for d in latest([d + '.dir' for d in dirs if any(f in d for f in SUBFOLDER_FAMILIES)])]
        pick = [p[:-4] for p in pick] + [d for d in dirs if (folder, d) in UNVERSIONED_SUBFOLDERS]
        for d in sorted(pick):
            for dp, _, fs in os.walk(os.path.join(base, d)):
                for f in sorted(fs):
                    if os.path.splitext(f)[1].lower() not in MEMBER_EXT:
                        continue
                    full = os.path.join(dp, f)
                    rel = os.path.relpath(full, base).replace('\\', '/')
                    rows.append({'folder': folder, 'file': rel, 'path': full, 'sub': d})
    return rows


def build_docs(rows):
    docs, fails = [], []
    for r in rows:
        name, ext = r['file'], os.path.splitext(r['file'])[1].lower()
        try:
            if ext == '.zip':
                with zipfile.ZipFile(r['path']) as z:
                    mem = [i.filename for i in z.infolist() if not i.is_dir()]
                secs = [{'h': 'Contents', 'l': 1, 't': '\n'.join(mem) + '\n\n%d files.' % len(mem)}]
            else:
                secs = extract.extract_file(r['path'], ext)
        except Exception as exc:   # keep going; record
            fails.append('%s: %s' % (name, exc))
            secs = [{'h': 'Document', 'l': 1, 't': 'The text of this file could not be read into the hub.'}]
        docs.append({'folder': r['folder'], 'file': name,
                     'name': os.path.splitext(name.split('/')[-1])[0],
                     'ext': ext[1:], 'inzip': '', 'sub': r.get('sub', ''), 'secs': secs})
    order = {f: i for i, f in enumerate(FOLDERS)}
    docs.sort(key=lambda d: (order.get(d['folder'], 99), d['file'].lower()))
    return docs, fails


def build_files(rows):
    files, fmeta, blobs, skipped = {}, {}, [], []
    for r in rows:
        if r.get('sub'):
            continue
        size = os.path.getsize(r['path'])
        if size > EMBED_MAX:
            skipped.append({'file': r['file'], 'folder': r['folder'], 'size': size})
            continue
        raw = io.open(r['path'], 'rb').read()
        files[r['file']] = len(blobs)
        fmeta[r['file']] = {'folder': r['folder'], 'size': size}
        blobs.append(base64.b64encode(gzip.compress(raw, 9)).decode('ascii'))
    return files, fmeta, blobs, skipped


def main():
    # extend the code patterns used by build_ids
    bp.PATTERNS[:0] = EXTRA_PATTERNS
    bp.KINDS.update(EXTRA_KINDS)
    bp.IDRX = re.compile(r'(?<![A-Za-z0-9-])(' + '|'.join('(?:%s)' % p for _, p in bp.PATTERNS) +
                         r')(?![A-Za-z0-9-])')

    def kind_of(code):
        for k, p in bp.PATTERNS:
            if re.fullmatch(p, code):
                return k
        return '?'
    bp.kind_of = kind_of
    bp.PREFERRED.update({'NSTORY': ['User Stories', 'Technical Enabler Stories', 'Administration Stories',
                                    'Data Migration Stories', 'ACE Team Stories'],
                         'SEPIC': ['Service Epics'], 'GAP': ['Gap Register'],
                         'ASM': ['Assumptions Register'], 'FR': ['PRD']})
    bp.REMOVED_STORIES = set(bp.REMOVED_STORIES)

    rows = manifest()
    docs, fails = build_docs(rows)
    # stories that live only in the per-story files (no legacy key, so in no master)
    have = set()
    for x in docs:
        for s in x['secs']:
            mm = re.match(r'^(RWB-\S+)\s', (s['h'] or '').strip() + ' ')
            if mm and re.search(r'\|\s*Story key\s*\|', s['t'] or ''):
                have.add(mm.group(1))
    sdir = os.path.join(ROOT, '04 User stories', 'Recovery Workbench Service Story Files v1')
    extra = []
    for dp, _, fs in os.walk(sdir):
        for fn in sorted(fs):
            if not fn.endswith('.md'):
                continue
            full = os.path.join(dp, fn)
            head = io.open(full, encoding='utf-8').read(6000)
            mm = re.search(r'\|\s*Story key\s*\|\s*([^|\s]+)', head)
            if mm and mm.group(1) not in have:
                rel = os.path.relpath(full, os.path.join(ROOT, '04 User stories')).replace('\\', '/')
                extra.append({'folder': '04 User stories', 'file': rel, 'path': full, 'sub': 'Service Story Files v1'})
    xd, xf = build_docs(extra)
    docs += xd
    fails += xf
    order = {f: i for i, f in enumerate(FOLDERS)}
    docs.sort(key=lambda d: (order.get(d['folder'], 99), d['file'].lower()))
    print('stories only in story files', len(extra))
    print('docs', len(docs), 'fails', len(fails))
    ids = bp.build_ids(docs)
    files, fmeta, blobs, skipped = build_files(rows)
    payload = {'docs': docs, 'ids': ids, 'kinds': bp.KINDS, 'files': files, 'fmeta': fmeta,
               'notembedded': skipped}
    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(payload, ensure_ascii=False, separators=(',', ':')))
    io.open(BLOBS, 'w', encoding='utf-8').write(json.dumps(blobs, separators=(',', ':')))
    print('ids', len(ids), 'files', len(files), 'not embedded', len(skipped))
    print('payload MB', round(os.path.getsize(OUT) / 1048576, 1),
          'blobs MB', round(os.path.getsize(BLOBS) / 1048576, 1))
    for f in fails[:20]:
        print('FAIL', f)


if __name__ == '__main__':
    main()
