"""Build the project hub payload from the current document set."""
import base64
import gzip
import io
import json
import os
import re
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14'
OUT = os.path.join(ROOT, '_work', 'data', 'hub_payload.json')
BLOBS = os.path.join(ROOT, '_work', 'data', 'hub_blobs.json')

FOLDER_ORDER = [
    '01 Decisions and governance', '02 Business architecture and process',
    '03 Requirements and specifications', '04 User stories', '05 Technical architecture',
    '06 Data', '07 Screens and experience', '08 AI and agents', '09 Testing and quality',
    '10 Policy, controls and compliance', '11 Delivery and operations',
    '12 Project communication', '15 ACE DB Alignment', '14 Story Updates',
]

REMOVED_STORIES = {
    'RWB-E1-003', 'RWB-E1-004', 'RWB-E1-005', 'RWB-E1-006', 'RWB-E1-009',
    'RWB-E1-010', 'RWB-E1-012', 'RWB-E1-051', 'RWB-E2-023',
}

KINDS = {
    'AC-ALT': 'Acceptance code, alternate flow',
    'AC-EXC': 'Acceptance code, exception flow',
    'AC-BG': 'Acceptance code, background event',
    'AC': 'Acceptance code, main flow',
    'BR': 'Business rule',
    'VR': 'Validation rule',
    'SC': 'System constraint',
    'STORY': 'User story',
    'REQ': 'Requirement',
    'FEAT': 'Feature',
    'DF': 'Data field',
    'MSG': 'Message',
    'LOV': 'List of values',
    'D-RCV': 'Recovery decision',
    'DL': 'Open decision',
    'DT': 'Technical decision',
    'DEV': 'Deviation type',
    'R-UNI': 'Universal rule',
    'TC': 'Test case',
    'RW': 'Role',
    'SY': 'Service identity',
    'JOB': 'Scheduled job',
    'SCR': 'Screen',
    'INT': 'Interface',
    'CTL': 'Control',
    'EV': 'Event',
    'NFR': 'Non functional requirement',
    'DQ': 'Data quality check',
    'ADR': 'Architecture decision',
    'REC': 'Reconciliation',
}

PATTERNS = [
    ('AC-ALT', r'AC-ALT-[A-Z0-9]{1,5}-\d{2,3}(?:-\d+)?'),
    ('AC-EXC', r'AC-EXC-[A-Z0-9]{1,5}-\d{2,3}(?:-\d+)?'),
    ('AC-BG', r'AC-BG-[A-Z0-9]{1,5}-\d{2,3}(?:-\d+)?'),
    ('AC', r'AC-[A-Z0-9]{1,5}-\d{2,3}(?:-\d+)?'),
    ('BR', r'BR-[A-Z0-9]{1,5}-\d{2,3}(?:-\d+)?'),
    ('VR', r'VR-[A-Z0-9]{1,5}-\d{2,3}(?:-\d+)?'),
    ('SC', r'SC-[A-Z0-9]{1,5}-\d{2,3}'),
    ('STORY', r'RWB-[A-Z]{1,3}\d?-\d{3}'),
    ('REQ', r'REQ-[A-Z0-9]{2,5}-\d{3}'),
    ('FEAT', r'FEAT-[A-Z0-9]{2,5}-\d{2,3}'),
    ('DF', r'DF-[A-Z]{2,4}-\d{3}'),
    ('MSG', r'MSG-[A-Z0-9]{1,5}-\d{3}'),
    ('LOV', r'LOV-[A-Z_]{3,30}'),
    ('R-UNI', r'R-UNI-\d{2}'),
    ('TC', r'TC-[A-Z0-9]{1,4}-\d{3}-\d{2}'),
    ('RW', r'RW-[A-Z]{3,9}'),
    ('SY', r'SY-[A-Z]{3,9}'),
    ('JOB', r'JOB-\d{2}'),
    ('SCR', r'SCR-\d{2}'),
    ('INT', r'INT-\d{2}'),
    ('CTL', r'CTL-\d{2}'),
    ('EV', r'EV-\d{2}'),
    ('NFR', r'NFR-\d{3}'),
    ('DQ', r'DQ-\d{3}'),
    ('ADR', r'ADR-\d{3}'),
    ('REC', r'REC-\d{2}'),
    ('D-RCV', r'D-RCV-\d{2}'),
    ('DL', r'DL\d{2}'),
    ('DT', r'DT\d{2}'),
]

IDRX = re.compile(r'(?<![A-Za-z0-9-])(' + '|'.join('(?:%s)' % p for _, p in PATTERNS) +
                  r')(?![A-Za-z0-9-])')


def kind_of(code):
    for kind, _ in sorted(PATTERNS, key=lambda x: -len(x[0])):
        prefix = 'RWB' if kind == 'STORY' else kind
        if code.startswith(prefix):
            return kind
    return '?'


def load_manifest():
    rows = json.load(io.open(os.path.join(ROOT, '_work', 'scripts', 'manifest_candidate.json'),
                             encoding='utf-8'))
    out = []
    for r in rows:
        name = r['file']
        if name.lower().endswith('.py'):
            continue
        if name == 'ACE-data-schema_20261104.xlsx':
            continue
        if 'Project Hub' in name:
            continue
        out.append(r)
    # the removals note explains the eight stories the ACE re-base took out
    out.append({'folder': '14 Story Updates',
                'file': 'Recovery Workbench Data Load Story Removals v1.md',
                'base': 'Recovery Workbench Data Load Story Removals', 'ver': 1, 'size': 0})
    return out


BANNERS = {
    'Recovery Workbench Build Notes Epic 2 v2.md':
        'SUPERSEDED for the ACE re-base (D-RCV-35). This note still describes the pre-re-base inbound load steps. '
        'The current developer action plan is section 13 of each RWB-E2 story in User Stories Epic 2 v6. '
        'Build Notes Epic 2 v3 has not been issued yet.',
    'Recovery Workbench Build Notes Technical Enablers v1.md':
        'SUPERSEDED for the ACE re-base (D-RCV-35). This note still describes the pre-re-base load and identity steps. '
        'The current developer action plan is section 13 of each RWB-TE story in Technical Enabler Stories v6. '
        'Build Notes Technical Enablers v2 has not been issued yet.',
    'Recovery Workbench Data Load Story Removals v1.md':
        'HISTORICAL CHANGE NOTE. The eight inbound load stories in this file are removed under D-RCV-35 and must not be built. '
        'Live stories are in User Stories Epic 1 v8 and User Stories Epic 2 v6; ACE owns the loads.',
    'Recovery Workbench User Stories Epic 2 Story Files v4.zip':
        'SUPERSEDED. These one-file stories are Epic 2 v4 and predate the ACE re-base. '
        'Use User Stories Epic 2 v6 (Markdown and workbook) and the current story section 13.',
}


def add_banners(docs):
    for doc in docs:
        text = BANNERS.get(doc['file'])
        if not text:
            continue
        doc['secs'] = [{'h': 'Status', 'l': 1, 't': text}]
        if doc['file'] == 'Recovery Workbench Build Notes Epic 2 v2.md':
            doc['secs'].append({'h': 'What to use instead', 'l': 1,
                               't': 'Open User Stories Epic 2 v6, choose the story, and read section 13 Solution plan. '
                                    'It lists the components, the database change, the configuration and the numbered build steps for that story.'})
        elif doc['file'] == 'Recovery Workbench Build Notes Technical Enablers v1.md':
            doc['secs'].append({'h': 'What to use instead', 'l': 1,
                               't': 'Open Technical Enabler Stories v6, choose the story, and read section 13 Solution plan. '
                                    'It lists the components, the database change, the configuration and the numbered build steps for that story.'})
        elif doc['file'] == 'Recovery Workbench User Stories Epic 2 Story Files v4.zip':
            doc['secs'].append({'h': 'What to use instead', 'l': 1,
                               't': 'Open User Stories Epic 2 v6 in Documents, or download the current Markdown and workbook. '
                                    'The old archive stays on the Original files tab for reference only.'})
    return docs


def build_docs():
    docs, failures = [], []
    seen_files = {}
    manifest = load_manifest()
    for r in manifest:
        folder, name = r['folder'], r['file']
        path = os.path.join(ROOT, folder, name)
        if not os.path.exists(path):
            failures.append('missing ' + path)
            continue
        ext = os.path.splitext(name)[1].lower()
        try:
            secs = extract.extract_file(path, ext)
        except Exception as exc:
            failures.append('%s: %s' % (name, exc))
            secs = []
        if ext == '.zip':
            with zipfile.ZipFile(path) as z:
                members = [i.filename for i in z.infolist() if not i.is_dir()]
            secs = [{'h': 'Contents', 'l': 1,
                     't': '\n'.join(members) + '\n\n%d files.' % len(members)}]
        docs.append({
            'folder': folder,
            'file': name,
            'name': os.path.splitext(name)[0],
            'ext': ext[1:],
            'inzip': '',
            'secs': secs,
        })
        seen_files.setdefault(name, []).append(folder)
        if ext == '.zip' and ('Functional Specifications by Module' in name or
                              'Technical Specifications by Module' in name):
            try:
                members = extract.extract_zip_members(path, name)
            except Exception as exc:
                failures.append('%s members: %s' % (name, exc))
                members = []
            for m in members:
                m['folder'] = folder
                docs.append(m)
    dupes = {k: v for k, v in seen_files.items() if len(v) > 1}
    if dupes:
        failures.append('duplicate file names: %r' % dupes)
    order = {f: i for i, f in enumerate(FOLDER_ORDER)}
    docs.sort(key=lambda d: (order.get(d['folder'], 99), d['file'].lower()))
    add_banners(docs)
    return docs, failures


def doc_text(doc):
    return '\n'.join((s['h'] or '') + '\n' + (s['t'] or '') for s in doc['secs'])


PREFERRED = {
    'STORY': ['User Stories', 'Technical Enabler Stories', 'Administration Stories',
              'Data Migration Stories', 'ACE Team Stories'],
    'DF': ['Logical Data Model', 'Physical Schema', 'User Stories'],
    'BR': ['Business Rules', 'User Stories'],
    'MSG': ['Error and Message Standard', 'User Stories'],
    'REQ': ['Business Requirements', 'Epics 3 to 8 Specification'],
    'FEAT': ['Feature List', 'Epics 3 to 8'],
    'DL': ['Decision Log'],
    'DT': ['Decision Log'],
    'D-RCV': ['Decision Log', 'Change Register'],
    'TC': ['Test Cases', 'User Stories'],
    'AC-ALT': ['Functional Specifications', 'User Stories'],
    'AC-EXC': ['Functional Specifications', 'User Stories'],
    'AC-BG': ['Functional Specifications', 'User Stories'],
    'AC': ['Functional Specifications', 'User Stories'],
    'SCR': ['Screen Specifications'],
    'NFR': ['Non Functional Specification'],
    'LOV': ['Reference Data'],
    'CTL': ['Controls Catalog'],
    'INT': ['Interface Specifications'],
    'JOB': ['Batch and Scheduling'],
    'EV': ['Event and Messaging'],
    'REC': ['Data Quality and Reconciliation'],
    'DQ': ['Data Quality'],
    'ADR': ['Architecture Decision Records'],
}


def candidate_lines(doc, di, si, code, kind):
    sec = doc['secs'][si]
    name = doc['file']
    pref = PREFERRED.get(kind, [])
    boost = 80 if any(p.lower() in name.lower() for p in pref) else 0
    if 'Build Notes' in name:
        boost -= 40
    cands = []
    if code in (sec['h'] or ''):
        score = 100 + boost
        if kind in ('STORY', 'SCR', 'ADR'):
            score += 40
        cands.append((score, di, si, sec['h'], 'h'))
    for line in (sec['t'] or '').split('\n'):
        if code not in line:
            continue
        raw = line.strip()
        score = 10 + boost
        if raw.startswith('|'):
            cells = [c.strip() for c in raw.strip('|').split('|')]
            if cells and cells[0] == code:
                score = 130 + boost
            elif any(c == code for c in cells[:3]):
                score = 110 + boost
            else:
                score = 40 + boost
        if re.match(r'^\s*(Scenario|Example|Background)\s*:', raw) and code in raw:
            score = 130 + boost
        if raw.startswith(code):
            score = max(score, 120 + boost)
        if ' — ' + code in raw or code + ' — ' in raw:
            score = max(score, 60 + boost)
        score -= min(len(raw) // 300, 15)
        cands.append((score, di, si, raw, 't'))
    return cands


def clean_value(text):
    text = re.sub(r'\s+', ' ', text or '').strip()
    text = text.strip(' -—:|')
    if len(text) > 400:
        text = text[:397].rsplit(' ', 1)[0] + '...'
    return text


DROP_CELL = re.compile(r'^(none|read|write|read \(|write \()', re.I)


def row_values(cells, code):
    vals = []
    for c in cells:
        c = c.strip()
        if not c or c == code or DROP_CELL.match(c):
            continue
        vals.append(c)
    return vals


def definition_for(code, kind, chosen, docs):
    _, di, si, line, where = chosen
    doc = docs[di]
    sec = doc['secs'][si]
    if where == 'h':
        rest = sec['h'].replace(code, '', 1).strip(' -—:|')
        if kind == 'STORY':
            rationale = ''
            for nxt in doc['secs'][si + 1:si + 8]:
                if re.search(r'Business rationale', nxt['h'] or '', re.I):
                    rationale = clean_value(nxt['t'])[:220]
                    break
            if rest and rationale:
                return clean_value(rest + ' — ' + rationale)
            if rest:
                return clean_value(rest)
        elif rest:
            return clean_value(rest)
    raw = line
    if raw.startswith('|'):
        cells = [c.strip() for c in raw.strip('|').split('|')]
        vals = row_values(cells, code)
        if vals:
            return clean_value(' — '.join(vals[:4]))
    if ' | ' in raw:
        cells = [c.strip() for c in raw.split(' | ')]
        vals = row_values(cells, code)
        if vals:
            return clean_value(' — '.join(vals[:4]))
    if re.match(r'^\s*(Scenario|Example|Background)\s*:', raw):
        text = re.sub(r'^\s*(Scenario|Example|Background)\s*:?\s*', '', raw)
        text = text.replace(code, '', 1)
        return clean_value(text)
    text = raw.replace(code, '', 1)
    return clean_value(text) or clean_value(sec['h'])


def build_ids(docs):
    allowed_df = set()
    fields_path = os.path.join(ROOT, '_work', 'data', 'schema_sysfields.json')
    if os.path.exists(fields_path):
        text = io.open(fields_path, encoding='utf-8').read()
        allowed_df = {r['field_id'] for r in json.loads(text[text.find('['):text.rfind(']') + 1])}
    occurrences = {}
    for di, doc in enumerate(docs):
        for si, sec in enumerate(doc['secs']):
            text = (sec['h'] or '') + '\n' + (sec['t'] or '')
            for m in IDRX.finditer(text):
                code = m.group(1)
                if code in REMOVED_STORIES:
                    continue
                if kind_of(code) == 'DF' and allowed_df and code not in allowed_df:
                    continue
                occurrences.setdefault(code, set()).add((di, si))
    ids = {}
    for code, occ in occurrences.items():
        kind = kind_of(code)
        best = None
        for di, si in occ:
            for cand in candidate_lines(docs[di], di, si, code, kind):
                if best is None or cand[0] > best[0]:
                    best = cand
        if best is None:
            di, si = sorted(occ)[0]
            best = (0, di, si, docs[di]['secs'][si]['h'], 'h')
        ids[code] = {
            'k': kind,
            'd': [best[1], best[2]],
            't': definition_for(code, kind, best, docs),
            'u': [list(x) for x in sorted(occ)],
        }
    return ids


def build_files(manifest):
    files, fmeta, blobs = {}, {}, []
    for r in manifest:
        name = r['file']
        path = os.path.join(ROOT, r['folder'], name)
        if name in files or not os.path.exists(path):
            continue
        raw = io.open(path, 'rb').read()
        files[name] = len(blobs)
        fmeta[name] = {'folder': r['folder'], 'size': len(raw)}
        blobs.append(base64.b64encode(gzip.compress(raw, 9)).decode('ascii'))
    return files, fmeta, blobs


def main():
    manifest = load_manifest()
    docs, failures = build_docs()
    ids = build_ids(docs)
    files, fmeta, blobs = build_files(manifest)
    payload = {'docs': docs, 'ids': ids, 'kinds': KINDS, 'files': files, 'fmeta': fmeta}
    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(payload, ensure_ascii=False, separators=(',', ':')))
    io.open(BLOBS, 'w', encoding='utf-8').write(json.dumps(blobs, separators=(',', ':')))
    print('docs', len(docs), 'ids', len(ids), 'files', len(files))
    print('text chars', sum(len(doc_text(d)) for d in docs))
    print('payload MB', round(os.path.getsize(OUT) / 1048576, 2),
          'blobs MB', round(os.path.getsize(BLOBS) / 1048576, 2))
    if failures:
        print('FAILURES', len(failures))
        for f in failures[:20]:
            print(' ', f)
    else:
        print('no extraction failures')


if __name__ == '__main__':
    main()
