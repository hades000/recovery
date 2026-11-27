"""TR-tests step 3: resync stale Given text of P1 rows and write the new test case IDs into the stories. Usage: python -I finish.py [--write]"""
import sys, csv, re, openpyxl
base = r'C:/Users/SahilMore/Downloads/Recovery Workbench SharePoint Set v14/_work/p1-ready/w2-sync'
WRITE = '--write' in sys.argv
__file__ = base + '/cov2.py'
exec(open(base + '/cov2.py', encoding='utf-8').read())
csv.field_size_limit(10 ** 9)
LOG = W + '/editlog/TR-tests.csv'
n = max(int(r[0].rsplit('-', 1)[1]) for r in csv.reader(open(LOG, encoding='utf-8-sig')) if r and r[0].startswith('TR-tests-'))
logs = []


def clip(s):
    return s if len(s) <= 400 else s[:399] + '…'


def log(action, file, section, before, after, old='v9', new='v9', ref=''):
    global n
    n += 1
    logs.append(['TR-tests-%04d' % n, action, file, old, new, section, clip(before), clip(after), ref, '', '', 'claude-sonnet-5-5', 'TR-tests'])


def norm(s):
    return re.sub(r'[\s;.`"\']+', '', str(s)).lower()


wb = openpyxl.load_workbook(TC)
ws = wb['Story test cases']
given = 0
for i in range(5, ws.max_row + 1):
    t, k = ws.cell(i, 1).value, str(ws.cell(i, 16).value or '').strip()
    if not t or ws.cell(i, 13).value != 'Live' or not k.startswith('RWB-P1-') or k not in stories:
        continue
    cov = [a for a in dict.fromkeys(re.findall(r'AC\d+[a-z]?', str(ws.cell(i, 5).value).split('—')[0])) if a in stories[k]['acs']]
    old = str(ws.cell(i, 8).value)
    if not cov or not old.startswith(tuple(a + ':' for a in cov)):
        continue
    new = '; '.join('%s: %s' % (a, compose(k, a)[0]) for a in cov)
    if norm(new) != norm(old):
        ws.cell(i, 8).value = new
        given += 1
        a, b = old.split('; '), new.split('; ')
        log('EDIT', '09 Testing and quality/Recovery Workbench Test Cases v9.xlsx',
            'Story test cases %s Given (resynced to %s %s)' % (t, k, ', '.join(cov)),
            '; '.join(x for x in a if x not in b), '; '.join(x for x in b if x not in a))

NEW = {'RWB-P1-DM005-APP': ('AC9', 'TC-P1-DM005-APP-04'), 'RWB-P1-DM006-APP': ('AC12', 'TC-P1-DM006-APP-04'),
       'RWB-P1-DM007-APP': ('AC14', 'TC-P1-DM007-APP-13'), 'RWB-P1-E2001-APP': ('AC19', 'TC-P1-E2001-APP-25')}
files = {}
for k, (ac, tid) in NEW.items():
    assert tid in tcs and tcs[tid][15] == k and tcs[tid][4].startswith(ac), (k, tid)
    p = stories[k]['path']
    text = open(p, 'rb').read().decode('utf-8')
    rel = p[len(W) + 7:].replace(chr(92), "/")
    subs = [(r'(?m)^\| TC: to be added in Test Cases[^|]*(?=\| %s\b)' % ac, '| %s ' % tid)]
    if k == 'RWB-P1-E2001-APP':
        subs.append((r'AC19 has no row in Test Cases v9 and is to be added\.', 'AC19 is proved by %s in Test Cases v9.' % tid))
    for pat, rep in subs:
        m = re.search(pat, text)
        assert m, (k, pat)
        log('EDIT', rel, '16 Test cases %s' % ac, m.group(0).strip(), rep.strip(), 'v3', 'v3')
        text = text[:m.start()] + rep + text[m.end():]
    files[p] = text

print('given resynced', given, 'story edits', len(logs) - given)
if WRITE:
    wb.save(TC)
    for p, text in files.items():
        open(p, 'wb').write(text.encode('utf-8'))
    with open(LOG, 'a', encoding='utf-8', newline='') as f:
        csv.writer(f, quoting=csv.QUOTE_ALL).writerows(logs)
    print('written, last edit id', n)
