"""Replace temporary gap/assumption IDs with register IDs in every staged file.
Usage: python -I replace_ids.py <mapping.csv> [--write]
mapping.csv columns: temp_id, register_id   (register_id empty -> skipped and reported)
Whole-token match only: NEW-GAP-S5-1 never matches inside NEW-GAP-S5-10.
Dry run by default: reports counts per file. With --write, edits files in place and logs to editlog/IDMAP-replace.csv.
"""
import csv, os, re, sys, glob, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = os.path.join(HERE, 'stage')
LOG = os.path.join(HERE, 'editlog', 'IDMAP-replace.csv')
mp = {}
for r in csv.DictReader(open(sys.argv[1], encoding='utf-8-sig')):
    t, g = (r.get('temp_id') or '').strip(), (r.get('register_id') or '').strip()
    if t and g: mp[t] = g
WRITE = '--write' in sys.argv
if not mp: sys.exit('empty mapping')
# longest first, whole token: not preceded by [A-Za-z0-9-] and not followed by [A-Za-z0-9] or -[0-9A-Za-z]
alts = '|'.join(re.escape(k) for k in sorted(mp, key=len, reverse=True))
rx = re.compile(r'(?<![A-Za-z0-9-])(' + alts + r')(?![A-Za-z0-9]|-[A-Za-z0-9])')
def sub(s):
    n = [0]
    def f(m): n[0] += 1; return mp[m.group(1)]
    return rx.sub(f, s), n[0]
rows, total = [], 0
for p in glob.glob(os.path.join(STAGE, '**', '*'), recursive=True):
    if os.path.isdir(p): continue
    if os.sep+'23 Document Gaps'+os.sep in p: continue
    ext = os.path.splitext(p)[1].lower(); cnt = 0
    try:
        if ext in ('.md', '.yaml', '.yml', '.csv', '.sql', '.txt', '.json'):
            raw = open(p, 'rb').read(); txt = raw.decode('utf-8')
            new, cnt = sub(txt)
            if cnt and WRITE: open(p, 'wb').write(new.encode('utf-8'))
        elif ext == '.xlsx':
            import openpyxl
            wb = openpyxl.load_workbook(p)
            for ws in wb.worksheets:
                for row in ws.iter_rows():
                    for c in row:
                        if isinstance(c.value, str) and 'NEW-' in c.value:
                            v, k = sub(c.value)
                            if k: cnt += k; c.value = v
            if cnt and WRITE: wb.save(p)
        elif ext == '.docx':
            import docx
            d = docx.Document(p)
            paras = list(d.paragraphs) + [pp for t in d.tables for row in t.rows for cell in row.cells for pp in cell.paragraphs]
            for pp in paras:
                if 'NEW-' not in pp.text: continue
                done = False
                for run in pp.runs:  # in-run first, keeps formatting
                    v, k = sub(run.text)
                    if k: run.text = v; cnt += k; done = True
                if not done:
                    v, k = sub(pp.text)
                    if k and pp.runs:  # token split across runs: put text in first run, clear others
                        pp.runs[0].text = v
                        for r_ in pp.runs[1:]: r_.text = ''
                        cnt += k
            if cnt and WRITE: d.save(p)
    except Exception as e:
        print('ERROR', p, e); continue
    if cnt:
        total += cnt; rows.append((os.path.relpath(p, STAGE), cnt))
for f, c in sorted(rows): print(c, f)
print('files', len(rows), 'replacements', total, '(written)' if WRITE else '(dry run)')
if WRITE:
    new = not os.path.exists(LOG)
    with open(LOG, 'a', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh, quoting=csv.QUOTE_ALL)
        if new: w.writerow(['edit_id','action','file','old_version','new_version','section','before','after','finding_refs','decision_refs','gap_asm_refs','model','agent'])
        for i, (f, c) in enumerate(sorted(rows), 1):
            w.writerow([f'IDMAP-{i:04d}', 'EDIT', f, '', '', 'temp ID replacement', f'{c} temp IDs', 'register IDs per mapping', '', '', os.path.basename(sys.argv[1]), 'script', 'orchestrator'])
