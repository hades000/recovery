"""Apply the graph changes to the catalog and rebuild the counted parts of the Dependency Map."""
import collections, copy, json, shutil, sys
import openpyxl
from w9lib import STAGE, log
from delta import changes, stories, cat
import graph

US = '04 User stories'
CAT_REL = US + '/Recovery Workbench Service Story Catalog v3.xlsx'
MAP_REL = '11 Delivery and operations/Recovery Workbench Dependency Map v7.xlsx'
CAT = STAGE + '\\' + CAT_REL.replace('/', '\\')
MAP = STAGE + '\\' + MAP_REL.replace('/', '\\')
SRC = ('Story headers of the staged v3 story files; RD-P1-022; RD-P1-024; RD-P1-044; RD-P1-047')
RDS = 'RD-P1-022; RD-P1-024; RD-P1-044; RD-P1-047'

# break the one blocking cycle: record the app-to-deployment edge as tracked
adds = dict(graph.adds)
if ('RWB-P1-E1067-APP', 'RWB-P1-E1066-OPS') not in cat:
    adds[('RWB-P1-E1067-APP', 'RWB-P1-E1066-OPS')] = 'X'
rem_keys = {(a, b) for a, b, _ in graph.rems}
new = {k: v for k, v in cat.items() if k not in rem_keys}
new.update(adds)
assert not graph.cycles(new)[0]

old_stories = {k: dict(v) for k, v in stories.items()}


def nonc(k):
    return stories[k]['Work type'] != 'Contract'


# ---- lanes: merge along new blocking edges ----
lane = {k: s['Lane'] for k, s in stories.items()}
size = collections.Counter(lane.values())


def rank(label):
    return (size[label], -len(label), [-ord(c) for c in label])


moved = {}
for (a, b), c in sorted(adds.items()):
    if c == 'H' and nonc(a) and nonc(b) and lane[a] != lane[b]:
        if lane[a] == 'Retired' or lane[b] == 'Retired':
            continue
        keep, drop = sorted([lane[a], lane[b]], key=rank, reverse=True)
        for k in lane:
            if lane[k] == drop:
                lane[k] = keep
                moved[k] = keep
        size[keep] += size.pop(drop)


def depth(graph_edges):
    out = collections.defaultdict(list)
    for (a, b), c in graph_edges.items():
        if c == 'H' and nonc(a) and nonc(b):
            out[a].append(b)
    memo = {}

    def d(n):
        if n not in memo:
            memo[n] = 1 + max((d(m) for m in out.get(n, [])), default=0)
        return memo[n]

    return {k: d(k) for k in list(out)}


d0, d1 = depth(cat), depth(new)
deep = sorted(k for k, v in d1.items() if v > 4)
deep_before = sorted(k for k, v in d0.items() if v > 4)


# ---- ready ----
def blockers(graph_edges, k):
    return sorted(b for (a, b), c in graph_edges.items() if a == k and c == 'H' and nonc(b))


ready = {}
for k in sorted({a for a, _ in list(adds) + list(rem_keys)}):
    now = blockers(new, k)
    if now != blockers(cat, k):
        ready[k] = 'After ' + ', '.join(now) if now else 'Day 1'

# ---- catalog ----
wb = openpyxl.load_workbook(CAT)
ws = wb['Dependencies']
rows = [tuple(c.value for c in r) for r in ws.iter_rows(min_row=2, max_col=3)]
rows = [r for r in rows if r[0]]
out = [(a, b, new[(a, b)]) for a, b, _ in rows if (a, b) in new]
for (a, b), c in sorted(adds.items()):
    idx = [i for i, r in enumerate(out) if r[0] == a]
    pos = idx[-1] + 1 if idx else next((i for i, r in enumerate(out) if r[0] > a), len(out))
    out.insert(pos, (a, b, c))
assert len(out) == len(new) and len({(a, b) for a, b, _ in out}) == len(out)
style = [copy.copy(ws.cell(2, c)._style) for c in (1, 2, 3)]
last_old = ws.max_row
tail_start = len(rows) + 2
tail = [[(ws.cell(r, c).value, copy.copy(ws.cell(r, c)._style)) for c in (1, 2, 3)] for r in range(tail_start, last_old + 1)]
assert all(v is None for row in tail for v, _ in row), 'unexpected content below the dependency rows'
for i, row in enumerate(out):
    for c in range(3):
        cell = ws.cell(i + 2, c + 1, row[c])
        cell._style = copy.copy(style[c])
for r in range(len(out) + 2, last_old + 1):
    for c in (1, 2, 3):
        ws.cell(r, c).value = None
if ws.auto_filter.ref:
    ws.auto_filter.ref = 'A1:C%d' % (len(out) + 1)

S = wb['Stories']
cols = {c.value: i + 1 for i, c in enumerate(S[1])}
ready_logged, lane_logged = [], []
for r in range(2, S.max_row + 1):
    k = S.cell(r, 1).value
    if k in ready and S.cell(r, cols['Ready']).value != ready[k]:
        ready_logged.append((k, S.cell(r, cols['Ready']).value, ready[k]))
        S.cell(r, cols['Ready']).value = ready[k]
    if k in moved and S.cell(r, cols['Lane']).value != moved[k]:
        lane_logged.append((k, S.cell(r, cols['Lane']).value, moved[k]))
        S.cell(r, cols['Lane']).value = moved[k]

all_rows = [dict(zip(cols, r)) for r in S.iter_rows(min_row=2, values_only=True) if r[0]]
E = wb['Epics']
epic_logged = []
day1_total = sum(1 for s in all_rows if str(s['Ready']).startswith('Day 1'))
for r in range(2, E.max_row + 1):
    epic = E.cell(r, 1).value
    mine = [s for s in all_rows if s['Epic'] == epic]
    if not mine:
        continue
    lanes = len({s['Lane'] for s in mine if s['Lane'] != 'Retired'})
    day1 = sum(1 for s in mine if str(s['Ready']).startswith('Day 1'))
    before = (E.cell(r, 4).value, E.cell(r, 5).value)
    if before != (lanes, day1):
        E.cell(r, 4).value, E.cell(r, 5).value = lanes, day1
        epic_logged.append((epic, before, (lanes, day1)))

memberships = sum(E.cell(r, 4).value for r in range(2, E.max_row + 1) if isinstance(E.cell(r, 4).value, int))
distinct = len({s['Lane'] for s in all_rows if s['Lane'] != 'Retired'})
rm = wb['Read me']
for r in range(1, rm.max_row + 1):
    v = rm.cell(r, 1).value
    if isinstance(v, str) and v.startswith('Epics sheet, Lanes column'):
        nv = v.split('so the column adds to')[0] + 'so the column adds to %d epic-lane memberships while the programme has %d distinct lane IDs (GAP-3200).' % (memberships, distinct)
        if nv != v:
            rm.cell(r, 1).value = nv
            log('EDIT', CAT_REL, 'v2', 'v3', 'Read me, lane counts', v, nv, decisions=RDS)
wb.save(CAT)

log('ADD', CAT_REL, 'v2', 'v3', 'Dependencies: %d rows added' % len(adds), '',
    '; '.join('%s>%s %s' % (a[4:], b[4:], c) for (a, b), c in sorted(adds.items()) if a.startswith('RWB-P1-')),
    findings='RWB-P1-AD018-APP#16; RWB-P1-AD019-APP#22; RWB-P1-E1065-APP#13; RWB-P1-E1065-DB#8; RWB-P1-E1066-APP#25; RWB-P1-E1067-CON#16; RWB-P1-E1068-APP#8; RWB-P1-E1016-DB#5; RWB-P1-E1069-DB#5; RWB-P1-DM010-APP#12',
    decisions=RDS)
log('REMOVE', CAT_REL, 'v2', 'v3', 'Dependencies: %d rows removed' % len(rem_keys),
    '; '.join('%s>%s %s' % (a[4:], b[4:], c) for a, b, c in graph.rems), '', decisions=RDS)
for k, a, b in ready_logged:
    log('EDIT', CAT_REL, 'v2', 'v3', 'Stories Ready: ' + k, a, b, decisions=RDS)
log('EDIT', CAT_REL, 'v2', 'v3', 'Stories Lane: %d stories moved to a merged lane' % len(lane_logged),
    '; '.join('%s %s' % (k[4:], a) for k, a, b in lane_logged), '; '.join('%s %s' % (k[4:], b) for k, a, b in lane_logged), decisions=RDS)
log('EDIT', CAT_REL, 'v2', 'v3', 'Epics: Lanes and Day-1 stories',
    '; '.join('%s %s' % (e, a) for e, a, b in epic_logged), '; '.join('%s %s' % (e, b) for e, a, b in epic_logged), decisions=RDS)

# ---- dependency map ----
wb = openpyxl.load_workbook(MAP)
ws = wb['Story dependencies v5']
data = []
r = 5
while ws.cell(r, 1).value and str(ws.cell(r, 1).value).startswith('RWB-'):
    data.append([ws.cell(r, c).value for c in range(1, 18)])
    r += 1
end = r - 1
notes = []
for rr in range(end + 1, ws.max_row + 1):
    notes.append((rr, [(ws.cell(rr, c).value, copy.copy(ws.cell(rr, c)._style)) for c in range(1, 18)], ws.row_dimensions[rr].height))
styles = [copy.copy(ws.cell(5, c)._style) for c in range(1, 18)]
existing = {(d[0], d[7]): d for d in data}
service = {}
for d in data:
    service[d[5]] = d[4]
    service[d[11]] = d[10]
BLOCK = {'H': 'Only H on a non-CON story (same lane)', 'C': 'No', 'I': 'ITG only', 'X': 'No; tracked'}
owner = {}
for d in data:
    owner.setdefault(d[3], collections.Counter())[d[16]] += 1


def code(k):
    return k.split('-')[1]


def side(k):
    s = stories[k]
    wave = s['Wave']
    for d in data:
        if d[0] == k:
            wave = d[6]
            break
        if d[7] == k:
            wave = d[12]
            break
    return s['Title'], s['Work type'], service[code(k)], code(k), wave


body = []
for a, b, c in out:
    d = existing.get((a, b))
    ta, wa, sa, ca, va = side(a)
    tb, wb_, sb, cb, vb = side(b)
    if d:
        d = list(d)
        d[1], d[8] = ta, tb
        d[13], d[14] = c, BLOCK[c]
    else:
        try:
            order = 'Earlier wave' if int(vb) < int(va) else 'Same wave' if int(vb) == int(va) else 'Later wave'
        except (TypeError, ValueError):
            order = 'Same wave'
        d = [a, ta, stories[a]['Epic'], wa, sa, ca, va, b, tb, wb_, sb, cb, vb, c, BLOCK[c], order,
             owner[wa].most_common(1)[0][0] if wa in owner else stories[a]['Suggested owner']]
    body.append(d)

merged = [str(m) for m in ws.merged_cells.ranges if m.min_row > end]
shift = len(body) - len(data)
for m in merged:
    ws.unmerge_cells(m)
for rr in range(5, max(ws.max_row, 4 + len(body) + (notes[-1][0] - end if notes else 0)) + 1):
    for c in range(1, 18):
        ws.cell(rr, c).value = None
for i, d in enumerate(body):
    for c in range(17):
        cell = ws.cell(5 + i, c + 1, d[c])
        cell._style = copy.copy(styles[c])
for rr, cells, height in notes:
    for c, (v, st) in enumerate(cells, 1):
        cell = ws.cell(rr + shift, c, v)
        cell._style = st
    ws.row_dimensions[rr + shift].height = height
from openpyxl.worksheet.cell_range import CellRange
for m in merged:
    cr = CellRange(m)
    cr.shift(0, shift)
    ws.merge_cells(cr.coord)
ws.auto_filter.ref = 'A4:Q%d' % (4 + len(body))

total = len(body)
n = collections.Counter(d[13] for d in body)
nstories = len({d[0] for d in body})
waves = collections.Counter((d[15], d[13]) for d in body)
ws['A2'].value = ('%s story-level dependencies of the realignment, rebuilt from the Dependencies sheet of Recovery Workbench Service Story Catalog v3 on 27 November 2026. Each row is one dependency; the story on the right is finished or contracted first, and the class says whether it blocks. H %s, C %s, I %s, X %s.'
                  % tuple(format(x, ',') for x in (total, n['H'], n['C'], n['I'], n['X'])))

changed = []


def setv(sheet, addr, value):
    cell = wb[sheet][addr]
    if cell.value != value:
        changed.append((sheet, addr, cell.value, value))
        cell.value = value


# By service and class
bs = wb['By service and class']
classes = ['H', 'C', 'I', 'X']
for r in range(5, 27):
    key = bs.cell(r, 1).value
    sel_out = [d for d in body if key == 'All' or d[5] == key]
    sel_in = [d for d in body if key == 'All' or d[11] == key]
    vals = [sum(1 for d in sel_out if d[13] == c) for c in classes] + [len(sel_out)]
    vals += [sum(1 for d in sel_in if d[13] == c) for c in classes] + [len(sel_in)]
    for i, v in enumerate(vals):
        setv('By service and class', bs.cell(r, 4 + i).coordinate, v)
assert sum(bs.cell(r, 8).value for r in range(5, 26)) == total
assert sum(bs.cell(r, 13).value for r in range(5, 26)) == total
for r in range(30, 36):
    w = bs.cell(r, 1).value
    sel = [d for d in body if w == 'All' or str(d[6]) == str(w)]
    for i, c in enumerate(classes):
        setv('By service and class', bs.cell(r, 3 + i).coordinate, sum(1 for d in sel if d[13] == c))
    setv('By service and class', bs.cell(r, 7).coordinate, len(sel))
other_wave = total - bs['G35'].value if False else None
setv('By service and class', 'A2', 'Rows each service consumes (out) and provides (in), by class, over the %s rows of Story dependencies v5. Codes, names and waves are the Ownership Map v3 Services sheet; PLT and ITG are the platform and integration epics.' % format(total, ','))
p3c = sum(1 for d in body if d[11] == 'P3' and d[13] == 'C')
plth = sum(1 for d in body if d[11] == 'PLT' and d[13] == 'H')
import re
setv('By service and class', 'A49', re.sub(r'\b248 C rows|\b\d+ C rows', '%d C rows' % p3c, bs['A49'].value))
setv('By service and class', 'A50', re.sub(r'provides [\d,]+ H rows', 'provides %s H rows' % format(plth, ','), bs['A50'].value))
setv('By service and class', 'A51', bs['A51'].value.replace('Ownership Map v1', 'Ownership Map v3'))

# Dependency classes
dc = wb['Dependency classes']
h_con = sum(1 for d in body if d[13] == 'H' and d[9] == 'Contract')
h_pltcon = sum(1 for d in body if d[13] == 'H' and d[9] == 'Contract' and d[11] == 'PLT')
h_other = collections.Counter(d[9] for d in body if d[13] == 'H' and d[9] != 'Contract')
h_breach = sum(1 for d in body if d[13] == 'H' and d[5] != d[11] and not (d[11] == 'PLT' and d[9] == 'Contract'))
c_breach = sum(1 for d in body if d[13] == 'C' and (d[5] == d[11] or d[9] != 'Contract'))
i_rows = [d for d in body if d[13] == 'I']
i_breach = sum(1 for d in i_rows if d[5] != 'ITG')
c_later = sum(1 for d in body if d[13] == 'C' and d[15] == 'Later wave')
x_same = sum(1 for d in body if d[13] == 'X' and d[5] == d[11])
x_plt = sum(1 for d in body if d[13] == 'X' and d[11] == 'PLT' and d[5] != 'PLT')
x_app = sum(1 for d in body if d[13] == 'X' and d[11] == 'PLT' and d[9] == 'App development')
x_other = n['X'] - x_same - x_plt
for r in range(1, dc.max_row + 1):
    a = dc.cell(r, 1).value
    rule = str(dc.cell(r, 2).value)
    detail = str(dc.cell(r, 5).value)
    dp_ids = re.findall(r'[HC] (RWB-[A-Z0-9-]+CON)', str(dc.cell(r, 4).value))
    if 5 <= r <= 9 and a in classes:
        setv('Dependency classes', 'E%d' % r, str(n[a]))
        setv('Dependency classes', 'F%d' % r, '%.1f%%' % (100 * n[a] / total))
    elif 5 <= r <= 9 and a == 'All':
        setv('Dependency classes', 'E%d' % r, str(total))
    elif a == 'H' and rule.startswith('H points only'):
        setv('Dependency classes', 'D%d' % r, '%d breaches' % h_breach)
        setv('Dependency classes', 'E%d' % r, '%s rows to a CON story (%s of them a platform CON); %s' % (
            format(h_con, ','), format(h_pltcon, ','), ', '.join('%d to a same-service %s story' % (v, k) for k, v in h_other.most_common())))
    elif a == 'C' and rule.startswith('C points only'):
        setv('Dependency classes', 'D%d' % r, '%d breaches' % c_breach)
        setv('Dependency classes', 'E%d' % r, '%d rows; %d point at a service built in a later wave, built against its fake' % (n['C'], c_later))
    elif a == 'I' and rule.startswith('I sits'):
        setv('Dependency classes', 'D%d' % r, '%d breaches' % i_breach)
        setv('Dependency classes', 'E%d' % r, '%d rows on %d ITG stories' % (len(i_rows), len({d[0] for d in i_rows})))
    elif a == 'X' and rule.startswith('X points'):
        setv('Dependency classes', 'D%d' % r, '%d rows to a platform APP enabler' % x_app)
        setv('Dependency classes', 'E%d' % r, '%d rows inside the same service, %d to platform technical-enabler work, %d across services to another story (GAP-3234; ASM-5649)' % (x_same, x_plt, x_other))
    elif a == '-' and 'distinct rows' in detail:
        setv('Dependency classes', 'E%d' % r, '%s distinct rows' % format(total, ','))
    elif a == '-' and 'rows over' in detail:
        setv('Dependency classes', 'E%d' % r, '%s rows over %d stories' % (format(total, ','), nstories))
    elif str(a).startswith('DP-') and dp_ids:
        setv('Dependency classes', 'E%d' % r, str(sum(1 for d in body if d[7] in dp_ids)))
setv('Dependency classes', 'A2', re.sub(r'[\d,]+ rows of the realigned', '%s rows of the realigned' % format(total, ','), dc['A2'].value))
con_rows = sum(1 for d in body if d[3] == 'Contract')
for r in range(1, dc.max_row + 1):
    a = dc.cell(r, 1).value
    if a == 'Day 1':
        setv('Dependency classes', 'E%d' % r, '%s stories' % format(day1_total, ','))
    if isinstance(a, str) and a.startswith('Rows by wave order:'):
        order = lambda o: ', '.join(format(waves[(o, c)], ',') + ' ' + c for c in classes[:3]) + ' and %s X' % format(waves[(o, 'X')], ',')
        setv('Dependency classes', 'A%d' % r, 'Rows by wave order: %s rows point at an earlier wave; %s rows sit inside one wave; %d C rows point at a later wave and are the ones a consumer builds against a fake.' % (order('Earlier wave'), order('Same wave'), c_later))

# Read me
rm = wb['Read me']
for r in range(1, rm.max_row + 1):
    a = rm.cell(r, 1).value
    if not isinstance(a, str):
        continue
    table = {'Rows in Story dependencies v5': format(total, ','), 'H rows': format(n['H'], ','), 'C rows': format(n['C'], ','),
             'I rows': format(n['I'], ','), 'X rows': format(n['X'], ','), 'Stories with at least one row': format(nstories, ','),
             'Day 1 stories': format(day1_total, ',')}
    if a in table:
        setv('Read me', 'B%d' % r, table[a])
        if a == 'Stories with at least one row':
            setv('Read me', 'C%d' % r, re.sub(r'the other \d+ carry', 'the other %d carry' % (1034 - nstories), rm.cell(r, 3).value))
    elif a == 'CON stories':
        pass
    else:
        nv = re.sub(r'(story dependency graph of the realignment: )[\d,]+ rows', r'\g<1>%s rows' % format(total, ','), a)
        nv = re.sub(r'(graph(?: on Story dependencies v5)? is updated to )[\d,]+ rows over \d+ stories', r'\g<1>%s rows over %d stories' % (format(total, ','), nstories), nv)
        nv = re.sub(r'^- \d+ C rows now point', '- %d C rows now point' % c_later, nv)
        setv('Read me', 'A%d' % r, nv)
for r in range(1, rm.max_row + 1):
    a = rm.cell(r, 1).value
    if isinstance(a, str) and a.startswith('- The story dependency graph is updated'):
        extra = ' Rows added or removed by the P1 story header changes of the staged v3 story files are carried into this sheet; CON stories hold no row.'
        if extra not in a:
            setv('Read me', 'A%d' % r, a + extra)
wb.save(MAP)

for sheet in ('Read me', 'Dependency classes', 'By service and class'):
    mine = [x for x in changed if x[0] == sheet]
    if mine:
        log('EDIT', MAP_REL, 'v6', 'v7', sheet + ': counts and notes recomputed',
            '; '.join('%s=%s' % (a, o) for _, a, o, _n in mine), '; '.join('%s=%s' % (a, v) for _, a, _o, v in mine), decisions=RDS)
log('EDIT', MAP_REL, 'v6', 'v7', 'Story dependencies v5: rows, titles and A2', '%d data rows' % len(data), ws['A2'].value, decisions=RDS)

summary = dict(total=total, classes=n, stories=nstories, day1=day1_total, lanes=distinct, memberships=memberships,
               p1_epic=[x for x in epic_logged if x[0] == 'RWB-SVC-P1'], ready=ready_logged, lanes_moved=len(lane_logged),
               deep_before=len(deep_before), deep_after=deep, breaches=(h_breach, c_breach, i_breach), con_rows=con_rows,
               skipped=graph.skipped)
json.dump(summary, open('summary.json', 'w'), indent=1, default=str)
print({k: v for k, v in summary.items() if k not in ('skipped', 'ready')})
for x in ready_logged:
    print(x)
