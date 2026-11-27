"""W2-tests re-runnable sync: staged v3 stories -> Test Cases v9, RTM v9, tc-backfill.csv.
Usage: python -I sync.py [--write]"""
import sys, os, re, csv, copy, collections, shutil, time
exec(open(os.path.join(os.path.dirname(os.path.abspath(globals().get('__file__') or sys.argv[0])), 'cov2.py'), encoding='utf-8').read())
import openpyxl

WRITE = '--write' in sys.argv
LOG = W + '/editlog/W2-tests.csv'
BACK = W + '/tc-backfill.csv'
MODEL = 'claude-sonnet-5-5'
FULL16 = {'RWB-P2-E2001-CON', 'RWB-S4-E5002-APP', 'RWB-S4-E5002-CON', 'RWB-P2-E2034-CON', 'RWB-P2-E2034-OPS'}   # story-local IDs, all rows created
# every ID any story names is reserved for that story
CITED = set()
for _s in stories.values():
    CITED |= set(re.findall(r'TC-[A-Z0-9]+(?:-[A-Z0-9]+)*', _s['text']))
KEEP_RULING = 'RD-P1-025 baseline'


def acl(s):
    s = str(s or '')
    out = []
    for a, b in re.findall(r'AC(\d+) to AC(\d+)', s):
        out += ['AC%d' % i for i in range(int(a), int(b) + 1)]
    out += re.findall(r'AC\d+[a-z]?', s)
    return list(dict.fromkeys(out))


def cov_of(r):
    c = str(r[4])
    return [] if c.startswith('Owner story') else acl(c.split('—')[0])


def s16(k):
    m = re.search(r'^### 16\..*?(?=^### 17\.)', stories[k]['text'], re.M | re.S)
    out = []
    for line in (m.group(0) if m else '').split('\n'):
        c = [x.strip() for x in line.split('|')]
        if len(c) > 4 and re.fullmatch(r'`?TC-[A-Z0-9-]+`?', c[1]):
            cov = c[2].split('—')[0]
            # in a CON table the Covers cell may name this story's key before each criterion
            cov = cov.replace(k + ' ', '')
            out.append(dict(id=c[1].strip('`'), cov=cov.strip(), acs=acl(cov), level=c[3], data=c[4].replace('`', '"')))
    return out


def header(k, name):
    m = re.search(r'^\| %s \| (.*?) \|\s*$' % name, stories[k]['text'], re.M)
    return m.group(1).strip() if m else ''


def work_type(k):
    p = k.split('-')
    return 'ITG' if p[1] == 'ITG' else next((x for x in reversed(p) if x in ('APP', 'CON', 'OPS', 'DB', 'INF')), 'APP')


DEF_LEVEL = {'APP': 'Component', 'CON': 'Contract', 'OPS': 'NFR', 'DB': 'Component', 'INF': 'NFR', 'ITG': 'Integration'}

wbw = openpyxl.load_workbook(TC)
ws = wbw['Story test cases']
rowno = {ws.cell(i, 1).value: i for i in range(5, ws.max_row + 1) if ws.cell(i, 1).value}
last_data = max(rowno.values())
template = last_data
rtw = openpyxl.load_workbook(RTM)
trs = rtw['Criterion trace']
rts = rtw['RTM']

log_rows, back_new = [], []
touched = collections.Counter()
added_ids, updated_ids, retired_ids = [], [], []
req_new = collections.defaultdict(list)   # requirement -> ids to add


def clip(s):
    s = str(s or '')
    return s if len(s) <= 400 else s[:399] + '…'


def log(action, file, section, before, after, k=''):
    log_rows.append([None, action, file, 'v8', 'v9', section, clip(before), clip(after), '', '', '', MODEL, 'W2-tests'])


TCF = 'Recovery Workbench Test Cases v9.xlsx'
RTF = 'Recovery Workbench Requirements Traceability Matrix v9.xlsx'


def setrow(tid, values):
    """write a dict {col index 0-based: value} into the sheet and the cache"""
    i = rowno[tid]
    r = list(tcs[tid])
    for c, v in values.items():
        ws.cell(i, c + 1).value = v
        r[c] = v
    tcs[tid] = tuple(r)
    for x in str(r[15] or '').split(';'):
        lst = byk.setdefault(x.strip(), [])
        for j, o in enumerate(lst):
            if o[0] == tid:
                lst[j] = tcs[tid]
                break
        else:
            lst.append(tcs[tid])


def texts(k, covered, data):
    """Given, When, Then for the criteria a row covers"""
    g, w, t = [], [], []
    for ac in covered:
        cg, cw, ct = compose(k, ac)
        if not ct and not cw:
            ttl = re.sub(r'^AC\d+[a-z]?\s*', '', title(k, ac)).replace('`', '"')
            ttl = re.sub(r'\s*\((?:new|changed)[^)]*\)$', '', ttl)
            cg = 'The fixture of the story section 16 row: ' + (data or 'the contract and the fakes of section 12')
            cw = 'The check named in the Covers column runs on that fixture'
            ct = ttl
        g.append('%s: %s' % (ac, cg))
        w.append('%s: %s' % (ac, cw))
        t.append('%s: %s' % (ac, ct))
    return '; '.join(g), '; '.join(w), '; '.join(t)


def new_id(k):
    base = 'TC-' + k[4:] + '-'
    n = 1
    while '%s%02d' % (base, n) in tcs or '%s%02d' % (base, n) in CITED:
        n += 1
    return '%s%02d' % (base, n)


def add_row(tid, k, covered, cov_cell, level, data, gwt=None, ttl=None):
    global last_data
    legacy = header(k, 'Legacy key').split(',')[0].strip()
    if not re.fullmatch(r'RWB-[A-Z0-9]+-\d+', legacy):
        legacy = k
    epic = next((r[2] for r in tcs.values() if r[1] == legacy and r[2]), None)
    if not epic:
        m = re.search(r'-E(\d)', legacy)
        epic = 'E' + m.group(1) if m else ''
    level = level.strip()
    if level in ('', 'Boundary') or len(level) > 14:
        level = DEF_LEVEL[work_type(k)]
    g, w, t = gwt or texts(k, covered, data)
    ttl = ttl or title(k, covered[0]).replace('`', '"')
    vals = [tid, legacy, epic, k.split('-')[1], cov_cell, ttl, level, g, w, t,
            data or 'Synthetic values stated in the Given steps', 'No', 'Live', None,
            header(k, 'Service') or '', k, level, 'new, RD-P1']
    last_data += 1
    for c, v in enumerate(vals, 1):
        cell = ws.cell(last_data, c)
        src = ws.cell(template, c)
        cell._style = copy.copy(src._style)
        cell.value = v
    if ws.row_dimensions[template].height:
        ws.row_dimensions[last_data].height = ws.row_dimensions[template].height
    rowno[tid] = last_data
    tcs[tid] = tuple(vals)
    byk.setdefault(k, []).append(tcs[tid])
    added_ids.append(tid)
    log('ADD', TCF, 'Story test cases %s (new row for version 3 of %s %s)' % (tid, k, cov_cell), '', t)


def keyed_rows(k, ac, live=True):
    return [r for r in byk.get(k, []) if ac in cov_of(r) and (r[12] == 'Live' or not live)]


def good(r, k, ac):
    if KEEP_RULING in str(r[9]):
        return True
    return fits(r, k, ac)


# ---------------------------------------------------------------- 0. rows whose section 16 row now names other criteria
def restate(tid, k, acs, cov_cell, data, why):
    acs = [a for a in acs if a in stories[k]['acs'] and not withdrawn(k, a)]
    if not acs:
        return
    g, w, t = texts(k, acs, data or tcs[tid][10])
    vals = {4: cov_cell, 5: title(k, acs[0]).replace('`', '"'), 7: g, 8: w, 9: t}
    if data:
        vals[10] = data
    vals = {c: v for c, v in vals.items() if tcs[tid][c] != v}
    if not vals:
        return
    before = '%s | %s' % (tcs[tid][4], tcs[tid][9])
    setrow(tid, vals)
    updated_ids.append(tid)
    log('EDIT', TCF, 'Story test cases %s (%s)' % (tid, why), before, '%s | %s' % (cov_cell, t))


for k in sorted(stories):
    for c in s16(k):
        if c['id'] not in tcs:
            continue
        r = tcs[c['id']]
        if r[12] != 'Live' or str(r[15]).strip() != k:
            continue
        if c['acs'] and cov_of(r) and not set(c['acs']) & set(cov_of(r)):
            restate(c['id'], k, c['acs'], c['cov'], c['data'], 're-pointed to the criterion section 16 of %s names' % k)
        elif k in FULL16 and not c['acs'] and cov_of(r) and r[17] == 'new, RD-P1':
            vals = {4: c['cov'], 5: '%s of %s' % (c['cov'], k),
                    7: 'The fixture of the story section 16 row: ' + c['data'],
                    8: 'The check named in the Covers column runs on that fixture',
                    9: '%s of %s holds as its sections 8 and 12 state it; any difference fails the test' % (c['cov'], k),
                    10: c['data']}
            before = '%s | %s' % (r[4], r[9])
            setrow(c['id'], vals)
            updated_ids.append(c['id'])
            log('EDIT', TCF, 'Story test cases %s (ID is the section 16 rule row of %s)' % (c['id'], k), before, '%s | %s' % (c['cov'], vals[9]))
if 'TC-AD-019-02' in tcs:
    c = next((x for x in s16('RWB-P3-AD019-APP') if x['id'] == 'TC-AD-019-02'), None)
    if c:
        restate('TC-AD-019-02', 'RWB-P3-AD019-APP', ['AC2'], c['cov'], c['data'], 'legacy stale-product text replaced by version 3 AC2')
for tid, k, acs, cell in [('TC-E1-065-01-ITG', 'RWB-ITG-E1065-ITG', ['AC1', 'AC2'], 'AC1, AC2, BR2, BR4, BR5, BR8, BR10, BR11'),
                          ('TC-W1J01-06-ITG', 'RWB-ITG-W1J01-ITG', ['AC5'], 'AC5, X6'),
                          ('TC-W1J01-08-ITG', 'RWB-ITG-W1J01-ITG', ['AC6'], 'AC6, X8'),
                          ('TC-W1J01-10-ITG', 'RWB-ITG-W1J01-ITG', ['AC7'], 'AC7')]:
    if tid in tcs and tcs[tid][12] == 'Live' and not all(a + ':' in str(tcs[tid][9]) and good(tcs[tid], k, a) for a in acs):
        restate(tid, k, acs, cell, '', 'restated to version 3 of %s' % k)

# ---------------------------------------------------------------- 1. criteria
need = collections.OrderedDict()
for k in sorted(stories):
    for ac in stories[k]['acs']:
        if (k.startswith('RWB-P1-') or status(k, ac) != 'same') and not withdrawn(k, ac) and (k, ac) != ('RWB-P5-E1024-APP', 'AC22'):
            need.setdefault(k, []).append(ac)

done_update = set()
links = {}   # (k, ac) -> [ids]
for k, acs_needed in need.items():
    cited = s16(k)
    for ac in acs_needed:
        titled_only = not compose(k, ac)[1] and not compose(k, ac)[2]
        rows = keyed_rows(k, ac)
        seen = {r[0] for r in rows}
        rows += [r for r in linked(k, ac) if r[12] == 'Live' and r[0] not in seen]
        if titled_only:
            fit = rows or [tcs[c['id']] for c in cited if ac in c['acs'] and c['id'] in tcs
                           and tcs[c['id']][12] == 'Live' and k in str(tcs[c['id']][15])]
        else:
            fit = [r for r in rows if good(r, k, ac)]
        # own synced rows that no longer match the story are rewritten in place
        for r in keyed_rows(k, ac):
            if titled_only or r[0] in done_update or str(r[15]).strip() != k or good(r, k, ac):
                continue
            covered = [a for a in cov_of(r) if a in stories[k]['acs'] and not withdrawn(k, a)]
            if not covered or not str(r[7]).startswith(tuple(a + ':' for a in covered)):
                continue
            g, w, t = texts(k, covered, r[10])
            if (g, w, t) == (r[7], r[8], r[9]):
                continue
            before = r[9]
            vals = {7: g, 8: w, 9: t}
            if str(r[5]).startswith(covered[0] + ' '):
                vals[5] = title(k, covered[0]).replace('`', '"')
            setrow(r[0], vals)
            done_update.add(r[0])
            updated_ids.append(r[0])
            log('EDIT', TCF, 'Story test cases %s (synced to version 3 of %s %s)' % (r[0], k, ', '.join(covered)), before, t)
            if good(tcs[r[0]], k, ac):
                fit = [x for x in fit if x[0] != r[0]] + [tcs[r[0]]]
        fit = [tcs[r[0]] for r in fit]
        # cited IDs of section 16 that cover this criterion and are not in the workbook
        for c in cited:
            if ac in c['acs'] and c['id'] not in tcs:
                covered = [a for a in c['acs'] if a in stories[k]['acs'] and not withdrawn(k, a)]
                add_row(c['id'], k, covered, c['cov'], c['level'], c['data'])
                fit.append(tcs[c['id']])
        if not fit:
            c = next((c for c in cited if ac in c['acs']), None)
            tid = new_id(k)
            add_row(tid, k, [ac], ac, c['level'] if c else '', c['data'] if c else '')
            fit = [tcs[tid]]
        links[(k, ac)] = list(dict.fromkeys(r[0] for r in fit))

_old = 'TC-E1-056-06'
if _old in tcs:
    if tcs[_old][4] == 'AC6':
        setrow(_old, {4: 'AC4, BR3'})
        updated_ids.append(_old)
        log('EDIT', TCF, 'Story test cases %s Covers (section 16 names AC4, legacy AC6)' % _old, 'AC6', 'AC4, BR3')
    _key = ('RWB-PLT-E1056-OPS', 'AC4')
    if _key in links and _old not in links[_key]:
        links[_key].append(_old)

# ---------------------------------------------------------------- 2. story-local IDs and section rows
for k in sorted(FULL16):
    if k not in stories:
        continue
    for c in s16(k):
        if c['id'] in tcs:
            continue
        covered = [a for a in c['acs'] if a in stories[k]['acs'] and not withdrawn(k, a)]
        if covered:
            add_row(c['id'], k, covered, c['cov'], c['level'], c['data'])
        else:
            add_row(c['id'], k, [], c['cov'], c['level'], c['data'],
                    gwt=('The fixture of the story section 16 row: ' + c['data'],
                         'The check named in the Covers column runs on that fixture',
                         '%s of %s holds as its sections 8 and 12 state it; any difference fails the test' % (c['cov'], k)),
                    ttl='%s of %s' % (c['cov'], k))

# ---------------------------------------------------------------- 2b. coverage lost when a shared legacy ID was given to one story
import pickle
_h, _v8 = pickle.load(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'v8.pkl'), 'rb'))
_ix = {n: i for i, n in enumerate(_h)}
restored = collections.OrderedDict()   # story -> [(old id, ac, new id)]


def _keys(s):
    return {x.strip() for x in str(s or '').split(';') if x.strip().startswith('RWB-')}


for _t, _r in _v8.items():
    if _t not in tcs:
        continue
    for k in sorted(_keys(_r[_ix['Story key (new)']]) - _keys(tcs[_t][15])):
        if k not in stories:
            continue
        for ac in acl(str(_r[_ix['Covers']])):
            if ac not in stories[k]['acs'] or withdrawn(k, ac) or (k, ac) in links or (k, ac) in trace:
                continue
            if keyed_rows(k, ac):
                continue
            tid = new_id(k)
            g, w, th = compose(k, ac)
            data = str(_r[_ix['Data']] or '')
            level = str(_r[_ix['Test level']] or _r[_ix['Level']] or '')
            if th and w:
                add_row(tid, k, [ac], ac, level, data)
            else:
                old = ['%s: %s' % (ac, re.sub(r'^AC\d+:\s*', '', str(_r[_ix[c]] or ''))) for c in ('Given', 'When', 'Expected result')]
                add_row(tid, k, [ac], ac, level, data, gwt=tuple(old))
            links[(k, ac)] = [tid]
            restored.setdefault(k, []).append((_t, ac, tid))
for k, lst in restored.items():
    log('REQUEST', os.path.basename(stories[k]['path']), '16 Test cases %s: the listed shared IDs now hold the case of another story' % k, '',
        '; '.join('%s → %s (%s)' % (o, n, a) for o, a, n in lst))
print('restored', sum(map(len, restored.values())), 'for', len(restored), 'stories')

# ---------------------------------------------------------------- 3. retire rows of criteria that left the story
for k, s in stories.items():
    if not s['acs']:
        continue
    for r in list(byk.get(k, [])):
        if r[12] != 'Live' or str(r[15]).strip() != k or r[17] != 'new, RD-P1':
            continue
        covered = cov_of(r)
        if covered and str(r[7]).startswith(covered[0] + ':') and all(a not in s['acs'] or withdrawn(k, a) for a in covered):
            why = 'criterion no longer in ' + k
            setrow(r[0], {12: 'Retired', 13: why})
            retired_ids.append(r[0])
            log('EDIT', TCF, 'Story test cases %s (%s)' % (r[0], why), 'Live', 'Retired')

for tid, why in [('TC-E1-002-02-ITG', 'Retired by RD-P1-024: no extract file or Power BI data set exists'),
                 ('TC-E1-013-03-ITG', 'Retired: AC3 is removed by DP-17 (no data lake) and is not reassigned'),
                 ('TC-E1-013-07-ITG', 'Retired: the data lake assertion of AC7 is removed by DP-17')]:
    if tid in tcs and tcs[tid][12] == 'Live':
        setrow(tid, {12: 'Retired', 13: why})
        retired_ids.append(tid)
        log('EDIT', TCF, 'Story test cases %s (%s)' % (tid, why), 'Live', 'Retired')
NOTE = re.compile(r'TC: (?:changed row to be restated|to be added|to be updated)')
for tid, r in list(tcs.items()):
    for col in (4, 5, 7, 8, 9, 10):
        if NOTE.search(str(r[col] or '')):
            setrow(tid, {col: clean_note(r[col])})
            log('EDIT', TCF, 'Story test cases %s column %d (editor note removed)' % (tid, col + 1), r[col], tcs[tid][col])
for i in range(5, trs.max_row + 1):
    v = str(trs.cell(i, 3).value or '')
    if 'TC: to be' in v:
        trs.cell(i, 3).value = clean_note(v)
        log('EDIT', RTF, 'Criterion trace %s %s title (editor note removed)' % (trs.cell(i, 1).value, trs.cell(i, 2).value), v, trs.cell(i, 3).value)

# Read me housekeeping
rm = wbw['Read me']
sup = 'Test Cases v8 (22 November 2026); v8 is unchanged'
if rm['B10'].value != sup:
    log('EDIT', TCF, 'Read me Supersedes', rm['B10'].value, sup)
    rm['B10'].value = sup
for n in (21, 22):
    b, c = rm.cell(n, 2), rm.cell(n, 3)
    if b.value:
        log('EDIT', TCF, 'Read me row %d (text moved to the Change column)' % n, c.value, b.value)
        c.value, b.value = b.value, None

# ---------------------------------------------------------------- 4. Criterion trace
tr_row = {}
for i in range(5, trs.max_row + 1):
    if trs.cell(i, 1).value:
        tr_row[(trs.cell(i, 1).value, trs.cell(i, 2).value)] = i
req_by_story = collections.defaultdict(list)
for (k, ac), i in tr_row.items():
    for q in str(trs.cell(i, 5).value or '').split(','):
        if q.strip() and q.strip() not in req_by_story[k]:
            req_by_story[k].append(q.strip())
rtm_ids = {}
hdr_row = next(i for i in range(1, 30) if rts.cell(i, 1).value == 'Requirement')
for i in range(hdr_row + 1, rts.max_row + 1):
    if rts.cell(i, 1).value:
        rtm_ids[rts.cell(i, 1).value] = i


def requirements(k):
    if req_by_story.get(k):
        return req_by_story[k]
    pat = re.compile(re.escape(k) + r'(?![A-Z0-9-])')
    out = [q for q, i in rtm_ids.items() if pat.search(str(rts.cell(i, 15).value or ''))]
    if not out:
        legacy = header(k, 'Legacy key').split(',')[0].strip()
        out = [q for q, i in rtm_ids.items() if re.search(re.escape(legacy) + r'(?!\d)', str(rts.cell(i, 14).value or ''))]
    if not out:
        txt = re.search(r'^### 18\..*?(?=^### 19\.)', stories[k]['text'], re.M | re.S)
        out = [q for q in rtm_ids if txt and re.search(r'\b%s\b' % re.escape(q), txt.group(0))]
    req_by_story[k] = out
    return out


tmpl_t = max(tr_row.values())
last_t = tmpl_t
trace_add = trace_upd = 0
no_req = set()
for (k, ac), ids in links.items():
    ttl = re.sub(r'^AC\d+[a-z]?\s*', '', title(k, ac))
    if (k, ac) in tr_row:
        i = tr_row[(k, ac)]
        cur = [x.strip() for x in str(trs.cell(i, 4).value or '').split(',') if x.strip()]
        new = [x for x in cur if x in tcs and tcs[x][12] == 'Live'
               and not (str(tcs[x][15]).strip() == k and cov_of(tcs[x]) and ac not in cov_of(tcs[x]))]
        new += [x for x in ids if x not in new]
        if new != cur:
            trs.cell(i, 4).value = ', '.join(new)
            trace_upd += 1
            log('EDIT', RTF, 'Criterion trace %s %s' % (k, ac), ', '.join(cur), ', '.join(new))
        if trs.cell(i, 3).value != ttl:
            trs.cell(i, 3).value = ttl
        reqs = [x.strip() for x in str(trs.cell(i, 5).value or '').split(',') if x.strip()]
    else:
        reqs = requirements(k)
        if not reqs:
            no_req.add(k)
        last_t += 1
        for c, v in enumerate([k, ac, ttl, ', '.join(ids), ', '.join(reqs)], 1):
            cell = trs.cell(last_t, c)
            cell._style = copy.copy(trs.cell(tmpl_t, c)._style)
            cell.value = v
        tr_row[(k, ac)] = last_t
        trace_add += 1
        log('ADD', RTF, 'Criterion trace %s %s' % (k, ac), '', ', '.join(ids) + ' | ' + ', '.join(reqs))
    for q in reqs:
        req_new[q] += ids
    for t in ids:
        if t not in back.get((k, ac), ()):
            back_new.append((k, ac, t))
# criteria withdrawn or removed from a story leave the trace
drop = sorted((i, k, ac) for (k, ac), i in tr_row.items()
              if k in stories and stories[k]['acs'] and (ac not in stories[k]['acs'] or withdrawn(k, ac)))
for i, k, ac in reversed(drop):
    log('REMOVE', RTF, 'Criterion trace %s %s (criterion withdrawn or removed)' % (k, ac), trs.cell(i, 4).value, '')
    trs.delete_rows(i)
if trs.auto_filter.ref:
    trs.auto_filter.ref = 'A4:E%d' % trs.max_row

# ---------------------------------------------------------------- 5. RTM requirement rows
for i in range(5, trs.max_row + 1):
    for q in str(trs.cell(i, 5).value or '').split(','):
        req_new[q.strip()] += [x.strip() for x in str(trs.cell(i, 4).value or '').split(',') if x.strip()]
for q, i in rtm_ids.items():
    cur = [x.strip() for x in str(rts.cell(i, 11).value or '').split(',') if x.strip()]
    new = [x for x in cur if not (x in tcs and tcs[x][12] == 'Retired' and x in retired_ids)]
    new += [x for x in dict.fromkeys(req_new.get(q, [])) if x not in new and x in tcs and tcs[x][12] == 'Live']
    if new != cur:
        rts.cell(i, 11).value = ', '.join(new)
        cov = str(rts.cell(i, 18).value or '')
        rts.cell(i, 18).value = re.sub(r'Tests: \d+ test cases', 'Tests: %d test cases' % len(new), cov)
        gained = [x for x in new if x not in cur]
        lost = [x for x in cur if x not in new]
        log('EDIT', RTF, 'RTM %s Tests' % q, 'removed: ' + ', '.join(lost), 'added: ' + ', '.join(gained))

# PRD P1 v3: FR-P1-022 (case list) retired by RD-P1-024; FR-P1-033 (account-page read) traced to REQ-CWC-001
for q, old, new_val in [('REQ-CWC-001', 'FR-P1-022', 'FR-P1-033'), ('REQ-RDF-007', 'FR-P1-022', None)]:
    i = rtm_ids[q]
    frs = [x.strip() for x in str(rts.cell(i, 16).value or '').split(';') if x.strip()]
    if old in frs:
        before = '; '.join(frs)
        frs = [new_val if x == old else x for x in frs]
        frs = list(dict.fromkeys(x for x in frs if x))
        rts.cell(i, 16).value = '; '.join(frs)
        cov = str(rts.cell(i, 18).value or '')
        rts.cell(i, 18).value = re.sub(r'PRD FR: \d+', 'PRD FR: %d' % len(frs), cov)
        log('EDIT', RTF, 'RTM %s PRD FR IDs (PRD P1 v3, RD-P1-024)' % q, before, '; '.join(frs))
        if new_val:
            ids_cell = rts.cell(i, 15)
            have = [x.strip() for x in str(ids_cell.value or '').split(';') if x.strip()]
            extra = [x for x in ('RWB-P1-E1002-APP', 'RWB-P1-E1015-CON') if x not in have]
            if extra:
                log('EDIT', RTF, 'RTM %s New story IDs (FR-P1-033)' % q, ids_cell.value, 'added: ' + '; '.join(extra))
                ids_cell.value = '; '.join(have + extra)

# ---------------------------------------------------------------- 6. totals
rows_total = sum(1 for t in tcs)
live_total = sum(1 for r in tcs.values() if r[12] == 'Live')
ws['A2'].value = re.sub(r'^\d+ rows, \d+ live', '%d rows, %d live' % (rows_total, live_total), ws['A2'].value)
cell = wbw['Read me']['C22']
cell.value = re.sub(r'Story test cases: \d+ rows \(\d+ Live\)',
                    'Story test cases: %d rows (%d Live)' % (rows_total, live_total), cell.value)
if ws.auto_filter.ref:
    ws.auto_filter.ref = 'A4:R%d' % last_data

print('stories needing criteria', len(need), 'criteria', len(links))
print('TC added', len(added_ids), 'updated', len(updated_ids), 'retired', len(retired_ids))
print('trace added', trace_add, 'updated', trace_upd, 'removed', len(drop), 'backfill rows', len(back_new))
print('rows', rows_total, 'live', live_total, 'log rows', len(log_rows), 'stories with no requirement row', sorted(no_req))
for name, lst in (('added', added_ids), ('updated', updated_ids), ('retired', retired_ids)):
    print(name, collections.Counter(tcs[t][15] for t in lst))

if WRITE and (log_rows or back_new):
    stamp = time.strftime('%H%M%S')
    bdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bak-' + stamp)
    os.makedirs(bdir)
    for p in (TC, RTM, BACK, LOG):
        shutil.copy(p, bdir)
    wbw.save(TC)
    rtw.save(RTM)
    with open(BACK, 'a', encoding='utf-8', newline='') as f:
        csv.writer(f, quoting=csv.QUOTE_ALL).writerows(back_new)
    csv.field_size_limit(10 ** 9)
    n = max(int(m.group(1)) for r in csv.reader(open(LOG, encoding='utf-8-sig'))
            for m in [re.match(r'W2-tests-(\d+)$', r[0] if r else '')] if m)
    for r in log_rows:
        n += 1
        r[0] = 'W2-tests-%04d' % n
    with open(LOG, 'a', encoding='utf-8', newline='') as f:
        csv.writer(f, quoting=csv.QUOTE_ALL).writerows(log_rows)
    print('written; backup in', bdir, 'last edit id', n)
