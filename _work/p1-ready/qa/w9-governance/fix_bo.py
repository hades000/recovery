import collections, re
import docx, openpyxl
from docx.oxml.ns import qn
from w9lib import SET, STAGE, log

REL = '11 Delivery and operations/Recovery Workbench Story Build Order v5.docx'
RDS = 'RD-P1-022; RD-P1-024; RD-P1-044'
d = docx.Document(STAGE + '/' + REL)
old = docx.Document(SET + '/11 Delivery and operations/Recovery Workbench Story Build Order v4.docx')


def load(path):
    wb = openpyxl.load_workbook(path)
    cols = [c.value for c in wb['Stories'][1]]
    return {r[0]: dict(zip(cols, r)) for r in wb['Stories'].iter_rows(min_row=2, values_only=True) if r[0]}


S0 = load(SET + '/04 User stories/Recovery Workbench Service Story Catalog v2.xlsx')
S = load(STAGE + '/04 User stories/Recovery Workbench Service Story Catalog v3.xlsx')


def set_text(p, text):
    runs = p.runs
    if runs:
        runs[0].text = text
        for r in runs[1:]:
            r._element.getparent().remove(r._element)
    else:
        p.add_run(text)


def set_cell(cell, text):
    set_text(cell.paragraphs[0], text)


numbers, changed, items = [], [], []
assert len(d.tables) == len(old.tables)
for ti, (t, o) in enumerate(zip(d.tables, old.tables)):
    head = [c.text for c in t.rows[0].cells]
    if head[0] not in ('#', 'Legacy key'):
        continue
    assert len(t.rows) == len(o.rows)
    for row, orow in zip(t.rows[1:], o.rows[1:]):
        cells, ocells = row.cells, orow.cells
        if head[0] == '#' and cells[0].text != ocells[0].text:
            numbers.append((cells[1].text, cells[0].text, ocells[0].text))
            set_cell(cells[0], ocells[0].text)
        if 'New story' not in head:
            continue
        key = cells[head.index('New story')].text
        if head[0] == '#':
            items.append(key)
        if key == 'RWB-P1-E1002-CON':
            continue
        li, ri = head.index('Parallel lane'), head.index('Ready to start')
        for idx, field in ((li, 'Lane'), (ri, 'Ready')):
            new = str(S[key][field])
            if S[key][field] != S0[key][field] and cells[idx].text != new:
                changed.append((key, field, cells[idx].text, new))
                set_cell(cells[idx], new)
if numbers:
    log('EDIT', REL, 'v4', 'v5', 'Item number column: rows of item 92 restored',
        '; '.join('%s shown as %s' % (k, a) for k, a, b in numbers), 'Item number %s, as in version 4.' % numbers[0][2])
if changed:
    log('EDIT', REL, 'v4', 'v5', 'Story tables: Parallel lane and Ready to start from Service Story Catalog v3',
        '; '.join('%s %s' % (k[4:], a) for k, f, a, b in changed), '; '.join('%s %s' % (k[4:], b) for k, f, a, b in changed), decisions=RDS)

retired = {'RWB-P1-E1002-CON'}
active = [k for k in items if k not in retired]
isday = lambda k: str(S[k]['Ready']).startswith('Day 1')
all_active = {k: s for k, s in S.items() if k not in retired}

# team table
team = d.tables[10]
before = [[c.text for c in r.cells] for r in team.rows]
count = collections.Counter(S[k]['Suggested owner'].split(' (')[0] for k in active if isday(k))
for r in team.rows[1:]:
    name = r.cells[0].text
    set_cell(r.cells[1], str(sum(count.values()) if name == 'All' else count[name]))
log('EDIT', REL, 'v4', 'v5', 'Day-1 stories of the 115 items by team type',
    '; '.join('%s %s' % (r[0], r[1]) for r in before[1:]), '; '.join('%s %s' % (r.cells[0].text, r.cells[1].text) for r in team.rows[1:]), decisions=RDS)

# wave table
wave = d.tables[11]
before = [[c.text for c in r.cells] for r in wave.rows]
for r in wave.rows[1:]:
    name = r.cells[0].text
    st = [s for s in all_active.values() if name == 'All' or 'Wave %s' % s['Wave'] == name]
    lanes = len({s['Lane'] for s in st})
    day = sum(1 for s in st if str(s['Ready']).startswith('Day 1'))
    for i, v in ((1, len(st)), (2, lanes), (4, day), (5, len(st) - day)):
        set_cell(r.cells[i], str(v))
log('EDIT', REL, 'v4', 'v5', 'Position by wave',
    '; '.join(' '.join(r) for r in before[1:]), '; '.join(' '.join(c.text for c in r.cells) for r in wave.rows[1:]), decisions=RDS)

# deep chains inside a lane
cat = openpyxl.load_workbook(STAGE + '/04 User stories/Recovery Workbench Service Story Catalog v3.xlsx')['Dependencies']
edges = collections.defaultdict(list)
for a, b, c in cat.iter_rows(min_row=2, max_col=3, values_only=True):
    if a and c == 'H' and S[a]['Work type'] != 'Contract' and S[b]['Work type'] != 'Contract':
        edges[a].append(b)
memo = {}


def depth(n):
    if n not in memo:
        memo[n] = 1 + max((depth(m) for m in edges.get(n, [])), default=0)
    return memo[n]


deep = sorted(k for k in list(edges) if depth(k) > 4)
longest = max(depth(k) for k in list(edges))

n_active, n_day = len(active), sum(1 for k in active if isday(k))
lanes115 = len({S[k]['Lane'] for k in active})
con115 = sum(1 for k in active if S[k]['Work type'] == 'Contract')
tot, totday = len(all_active), sum(1 for s in all_active.values() if str(s['Ready']).startswith('Day 1'))
totlanes = len({s['Lane'] for s in all_active.values()})


def lane_of(key):
    return S[key]['Lane']


body = [p for p in d.paragraphs]


def edit_para(p, new, section):
    if p.text != new:
        before = p.text
        set_text(p, new)
        log('EDIT', REL, 'v4', 'v5', section, before, new, decisions=RDS)


for p in body:
    t = p.text
    if t.startswith('This version gives every story its lane'):
        nt = re.sub(r'carried by [\d,]+ active stories: \d+ are Day 1 and \d+ wait for a story in their own lane, in \d+ lanes\. The \d+ active contract',
                    'carried by %d active stories: %d are Day 1 and %d wait for a story in their own lane, in %d lanes. The %d active contract' % (n_active, n_day, n_active - n_day, lanes115, con115), t)
        edit_para(p, nt, 'Lanes and Day 1: the 115 items')
    elif t.startswith('The whole story set of this run'):
        nt = re.sub(r'has [\d,]+ active stories in \d+ lanes, of which \d+ are Day 1', 'has %d active stories in %d lanes, of which %d are Day 1' % (tot, totlanes, totday), t)
        edit_para(p, nt, 'Lanes and Day 1: whole story set')
    elif 'The longest chain of build dependencies inside any lane of the set is four stories.' in t and deep:
        nt = t.replace('The longest chain of build dependencies inside any lane of the set is four stories.',
                       'The rule limits a chain of build dependencies inside a lane to four stories. After the P1 story header changes the longest chain is %d, and %d stories sit deeper than four: %s. Pending: cut of these chains, owner Solution architect.' % (longest, len(deep), ', '.join(deep)))
        edit_para(p, nt, 'Lane depth statement')
    elif t.startswith('The critical path in the lane terms of this version'):
        nt = t

        def fix(m):
            return m.group(0)

        for legacy_key, story in [('RWB-ACE-001 is lane ', 'RWB-P1-ACE001-DB'), ('RWB-E1-069 is lane ', 'RWB-P1-E1069-DB')]:
            m = re.search(re.escape(legacy_key) + r'(L-[A-Z0-9-]+[A-Z0-9])', nt)
            if m:
                shown = m.group(1)
                if story == 'RWB-P1-E1069-DB' and shown == S0['RWB-P1-E1069-APP']['Lane']:
                    story = 'RWB-P1-E1069-APP'
                if shown != lane_of(story) and S0[story]['Lane'] == shown:
                    nt = nt[:m.start(1)] + lane_of(story) + nt[m.end(1):]
        edit_para(p, nt, 'Critical path lane names')

d.save(STAGE + '/' + REL)
print('numbers', len(numbers), 'cells', len(changed))
print('115:', n_active, n_day, n_active - n_day, lanes115, con115, '| all:', tot, totday, totlanes, '| deep', longest, deep)
for k in ('RWB-P1-ACE001-DB', 'RWB-P1-E1069-DB', 'RWB-P1-E1069-APP'):
    print(k, S0[k]['Lane'], '->', S[k]['Lane'])
for p in d.paragraphs:
    if p.text.startswith(('The critical path in the lane', 'This version gives', 'The whole story', 'Every service has at least')):
        print(p.text)
