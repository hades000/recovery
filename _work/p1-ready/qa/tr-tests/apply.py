"""TR-tests: give legacy test case IDs back to their v8 content / free them, move P1 content to TC-P1 IDs.
Usage: python -I apply.py [--write]. Always reads the workbooks and stories from bak/, so a re-run is safe."""
import os, sys, re, csv, copy, glob, io, pickle, collections
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')
WRITE = '--write' in sys.argv
SET = r'C:/Users/SahilMore/Downloads/Recovery Workbench SharePoint Set v14'
W = SET + '/_work/p1-ready'
Q = W + '/qa/tr-tests'
BAK = Q + '/bak'
TCN = 'Recovery Workbench Test Cases v9.xlsx'
RTN = 'Recovery Workbench Requirements Traceability Matrix v9.xlsx'
ST09 = W + '/stage/09 Testing and quality/'
P1DIR = 'RWB-SVC-P1 rwb-source-data (Source data)'
P1ST = W + '/stage/04 User stories/Recovery Workbench Service Story Files v3/' + P1DIR
MODEL = 'claude-sonnet-5-5'
csv.field_size_limit(10 ** 9)

C1, C2, _ = pickle.load(open(Q + '/sets.pkl', 'rb'))
h8, v8, h9, v9 = pickle.load(open(Q + '/wb.pkl', 'rb'))
stories = pickle.load(open(Q + '/st.pkl', 'rb'))[0]

# legacy rows P1 retired that no non-P1 story cites and whose behaviour a ruling removed or replaced
KEEP_RETIRED = {'TC-E1-002-%02d' % i for i in range(1, 11)} | {'TC-E1-015-04', 'TC-E1-015-05', 'TC-E1-015-06'}

logs = []


def clip(s):
    s = str('' if s is None else s)
    return s if len(s) <= 400 else s[:399] + '…'


def log(action, file, section, before='', after='', old='v9', new='v9'):
    logs.append(['TR-tests-%04d' % (len(logs) + 1), action, file, old, new, section, clip(before), clip(after),
                 '', '', '', MODEL, 'TR-tests'])


# ------------------------------------------------------------------ ID mapping
moved1 = [t for t in C1 if v9[t][15]]
taken = set(v9)
for _, (p, t) in stories.items():
    taken |= set(re.findall(r'TC-[A-Z0-9]+(?:-[A-Z0-9]+)*', t))


def idkey(t):
    a, b = t.rsplit('-', 1)
    return a, int(b)


highest = collections.Counter()
for t in taken:
    m = re.fullmatch(r'(TC-P1-[A-Z0-9]+-[A-Z]+-)(\d+)', t)
    if m:
        highest[m.group(1)] = max(highest[m.group(1)], int(m.group(2)))
MAP = {}
for t in sorted(moved1 + C2, key=idkey):
    owner = str(v9[t][15])
    assert re.fullmatch(r'RWB-P1-[A-Z0-9]+-[A-Z]+', owner), (t, owner)
    pre = 'TC-' + owner[4:] + '-'
    highest[pre] += 1
    MAP[t] = '%s%02d' % (pre, highest[pre])
    assert MAP[t] not in taken
TOK = re.compile(r'TC-[A-Z0-9]+(?:-[A-Z0-9]+)*')


def map_text(s):
    return TOK.sub(lambda m: MAP.get(m.group(0), m.group(0)), s)


# ------------------------------------------------------------------ Test Cases v9
wb = openpyxl.load_workbook(BAK + '/' + TCN)
ws = wb['Story test cases']
rowno = {ws.cell(i, 1).value: i for i in range(5, ws.max_row + 1) if ws.cell(i, 1).value}
last = max(rowno.values())
tcf = '09 Testing and quality/' + TCN


def vals(i):
    return [ws.cell(i, c).value for c in range(1, 19)]


# P1-owned rows that point at a moved P1 case in "Later home"
for t, i in rowno.items():
    if str(ws.cell(i, 16).value or '').startswith('RWB-P1-') and t not in C1:
        c = ws.cell(i, 14)
        if c.value and map_text(c.value) != c.value:
            log('EDIT', tcf, 'Story test cases %s Later home' % t, c.value, map_text(c.value))
            c.value = map_text(c.value)

for t in sorted(C2, key=idkey):
    i = rowno.pop(t)
    ws.cell(i, 1).value = MAP[t]
    rowno[MAP[t]] = i
    log('EDIT', tcf, 'Story test cases %s: ID freed (non-P1 stories use it for their own cases; not in v8)' % t, t, MAP[t])

restored_live = []
for t in sorted(C1, key=idkey):
    i = rowno[t]
    now = vals(i)
    if t in MAP:
        new = [MAP[t]] + now[1:]
        if new[13]:
            new[13] = map_text(new[13])
        last += 1
        for c, v in enumerate(new, 1):
            cell = ws.cell(last, c)
            cell._style = copy.copy(ws.cell(i, c)._style)
            cell.value = v
        if ws.row_dimensions[i].height:
            ws.row_dimensions[last].height = ws.row_dimensions[i].height
        rowno[MAP[t]] = last
        log('ADD', tcf, 'Story test cases %s (P1 content moved from %s, %s %s)' % (MAP[t], t, now[15], now[4]),
            '', '%s | %s | %s' % (now[12], now[5], now[9]))
    old = list(v8[t])
    keep = t in KEEP_RETIRED
    if keep:
        assert now[12] == 'Retired', t
        old[12], old[13] = 'Retired', map_text(now[13])
    else:
        restored_live.append(t)
    for c, v in enumerate(old, 1):
        ws.cell(i, c).value = v
    log('EDIT', tcf, 'Story test cases %s restored to the v8 row%s' % (t, ', status stays Retired' if keep else ''),
        '%s | %s | %s | %s' % (now[12], now[15], now[5], now[9]),
        '%s | %s | %s | %s' % (old[12], old[15], old[5], old[9]))

live = sum(1 for t, i in rowno.items() if ws.cell(i, 13).value == 'Live')
total = len(rowno)
ws.auto_filter.ref = 'A4:R%d' % last
a2 = ws['A2'].value
ws['A2'].value = re.sub(r'^\d+ rows, \d+ live', '%d rows, %d live' % (total, live), a2)
rm = wb['Read me']
rm['C22'].value = re.sub(r'Story test cases: \d+ rows \(\d+ Live\)',
                         'Story test cases: %d rows (%d Live)' % (total, live), rm['C22'].value)
note = (' Legacy test case IDs that other services cite keep their version 8 row; the rwb-source-data cases that had '
        'taken them carry TC-P1 IDs.')
before = rm['C21'].value
rm['C21'].value = before + note
log('EDIT', tcf, 'Read me C21 (what changed: test case IDs)', '', note.strip())

# ------------------------------------------------------------------ RTM v9
rt = openpyxl.load_workbook(BAK + '/' + RTN)
rtf = '09 Testing and quality/' + RTN


def split(s):
    return [x.strip() for x in str(s or '').split(',') if x.strip()]


trs = rt['Criterion trace']
for i in range(5, trs.max_row + 1):
    k = trs.cell(i, 1).value
    if not k:
        continue
    cur = split(trs.cell(i, 4).value)
    new = list(dict.fromkeys(MAP.get(x, x) for x in cur))
    if new != cur:
        assert k.startswith('RWB-P1-'), k
        trs.cell(i, 4).value = ', '.join(new)
        log('EDIT', rtf, 'Criterion trace %s %s' % (k, trs.cell(i, 2).value), ', '.join(cur), ', '.join(new))

r8 = openpyxl.load_workbook(SET + '/09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v8.xlsx',
                            read_only=True)['RTM']
old_req = {r[0]: split(r[10]) for r in r8.iter_rows(min_row=11, values_only=True) if r and r[0]}
rts = rt['RTM']
status = {t: ws.cell(i, 13).value for t, i in rowno.items()}
inv = {v: k for k, v in MAP.items()}
for i in range(11, rts.max_row + 1):
    q = rts.cell(i, 1).value
    if not q:
        continue
    cur = split(rts.cell(i, 11).value)
    new = [MAP.get(x, x) for x in cur]
    new = [x for x in new if not (x in inv and status[x] != 'Live')]
    new += [x for x in old_req.get(q, []) if x in restored_live]
    new = list(dict.fromkeys(new))
    if new != cur:
        rts.cell(i, 11).value = ', '.join(new)
        cov = str(rts.cell(i, 18).value or '')
        rts.cell(i, 18).value = re.sub(r'Tests: \d+ test cases', 'Tests: %d test cases' % len(new), cov)
        log('EDIT', rtf, 'RTM %s Tests (%d to %d)' % (q, len(cur), len(new)),
            'removed: ' + ', '.join(x for x in cur if x not in new),
            'added: ' + ', '.join(x for x in new if x not in cur))

# ------------------------------------------------------------------ tc-backfill.csv
rows = list(csv.reader(open(BAK + '/tc-backfill.csv', encoding='utf-8-sig')))
nbk = 0
for r in rows[1:]:
    if r[2] in MAP:
        assert r[0].startswith('RWB-P1-'), r
        log('EDIT', 'tc-backfill.csv', '%s %s' % (r[0], r[1]), r[2], MAP[r[2]], '', '')
        r[2] = MAP[r[2]]
        nbk += 1

# ------------------------------------------------------------------ P1 story citations
ONE = r'`?TC-[A-Z0-9]+(?:-[A-Z0-9]+)*?-\d{2}(?![\w-])`?'
MORE = r'(?:(?:, and |, | and | to )(?:%s|-?\d{2}(?![\w-])`?))' % ONE
GROUP = re.compile(r'(?<![\w-])%s%s*' % (ONE, MORE))
PART = re.compile(r'(, and |, | and | to )?(`?)(TC-[A-Z0-9-]+?-\d{2}|-?\d{2})(?![\w-])(`?)')


def regroup(m):
    text = m.group(0)
    ids, stem, tick, joins = [], None, False, []
    for join, t1, tok, t2 in PART.findall(text):
        if tok.startswith('TC-'):
            stem, n = tok.rsplit('-', 1)
        else:
            n = tok.lstrip('-')
        tick = tick or bool(t1)
        joins.append(join)
        full = '%s-%s' % (stem, n)
        if join == ' to ':
            a_stem, a = ids[-1].rsplit('-', 1)
            assert a_stem == stem and int(n) > int(a), text
            ids += ['%s-%02d' % (stem, x) for x in range(int(a) + 1, int(n) + 1)]
        else:
            ids.append(full)
    if not any(x in MAP for x in ids):
        return text
    new = list(dict.fromkeys(MAP.get(x, x) for x in ids))
    q = (lambda x: '`%s`' % x) if tick else (lambda x: x)
    runs = []
    for x in new:
        s, n = x.rsplit('-', 1)
        if runs and runs[-1][0] == s and int(n) == runs[-1][2] + 1:
            runs[-1][2] += 1
        else:
            runs.append([s, int(n), int(n)])
    items = []
    for s, a, b in runs:
        if b - a >= 2:
            items.append('%s to %s' % (q('%s-%02d' % (s, a)), q('%s-%02d' % (s, b))))
        else:
            items += [q('%s-%02d' % (s, x)) for x in range(a, b + 1)]
    if joins[-1] in (' and ', ', and ') and len(items) > 1:
        return ', '.join(items[:-1]) + ' and ' + items[-1]
    return ', '.join(items)


def edit_line(key, line):
    # lineage and history statements name the legacy case itself, not the P1 case
    if re.search(r'^\s*Scenario.*\(legacy ', line):
        return line
    if key == 'RWB-P1-E1015-OPS' and 'version 2 rows that reused' in line:
        return line
    if key == 'RWB-P1-E1002-APP' and 'The version 2 rows TC-E1-002-01 to TC-E1-002-19' in line:
        return line.replace('TC-E1-002-01 to TC-E1-002-19',
                            'TC-E1-002-01 to TC-E1-002-10, %s, %s, TC-E1-002-14 to TC-E1-002-19'
                            % (MAP['TC-E1-002-12'], MAP['TC-E1-002-13']))
    return GROUP.sub(regroup, line)


story_out, kept = {}, []
for p in sorted(glob.glob(BAK + '/P1-stories/*.md')):
    raw = open(p, 'rb').read().decode('utf-8')
    key = re.search(r'^\ufeff?# (RWB-[A-Z0-9-]+)\s', raw, re.M).group(1)
    rel = '04 User stories/Recovery Workbench Service Story Files v3/%s/%s' % (P1DIR, os.path.basename(p))
    lines = raw.split('\n')
    changed = False
    for n, line in enumerate(lines):
        body = line.rstrip('\r')
        new = edit_line(key, body)
        if new != body:
            log('EDIT', rel, 'line %d (test case IDs only)' % (n + 1), body.strip(), new.strip(), 'v3', 'v3')
            # trim the log text to the part that differs
            logs[-1][6] = clip('; '.join(GROUP.findall(body)))
            logs[-1][7] = clip('; '.join(GROUP.findall(new)))
            lines[n] = new + line[len(body):]
            changed = True
        left = [x for x in TOK.findall(new) if x in MAP]
        if left:
            kept.append((key, n + 1, sorted(set(left))))
    if changed:
        story_out[os.path.basename(p)] = '\n'.join(lines)

print('moved IDs', len(MAP), '| from v8 collisions', len(moved1), '| freed new-in-v9', len(C2))
print('restored rows', len(C1), '| live', len(restored_live), '| kept retired', len(C1) - len(restored_live))
print('rows', total, 'live', live, '| backfill pairs', nbk, '| stories changed', len(story_out),
      '| story lines', sum(1 for l in logs if l[2].startswith('04 ')), '| log rows', len(logs))
print('references left on purpose:', kept)

if WRITE:
    wb.save(ST09 + TCN)
    rt.save(ST09 + RTN)
    with open(W + '/tc-backfill.csv', 'w', encoding='utf-8', newline='') as f:
        csv.writer(f, quoting=csv.QUOTE_ALL).writerows(rows)
    for name, text in story_out.items():
        open(P1ST + '/' + name, 'wb').write(text.encode('utf-8'))
    with open(W + '/editlog/TR-tests.csv', 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        w.writerow('edit_id,action,file,old_version,new_version,section,before,after,finding_refs,decision_refs,gap_asm_refs,model,agent'.split(','))
        w.writerows(logs)
    pickle.dump(MAP, open(Q + '/map.pkl', 'wb'))
    print('written')
else:
    open(Q + '/dry-stories.txt', 'w', encoding='utf-8').write(
        '\n'.join('%s | %s\n   - %s\n   + %s' % (l[2].split('/')[-1][:40], l[5], l[6], l[7]) for l in logs if l[2].startswith('04 ')))
