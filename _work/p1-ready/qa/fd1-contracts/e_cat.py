"""Service Contract Catalog v3 (.md and .xlsx): batch D pairs, operations and section 6.1."""
import copy
import os
import re

import openpyxl

from ed import STAGE, log

NAME = '05 Technical architecture/Recovery Workbench Service Contract Catalog v3'
MD = os.path.join(STAGE, NAME + '.md')
XL = os.path.join(STAGE, NAME + '.xlsx')
CODE = {'P1': 'rwb-source-data', 'P2': 'rwb-integration', 'P3': 'rwb-case', 'P4': 'rwb-access', 'P5': 'rwb-document',
        'P6': 'rwb-comms', 'P8': 'rwb-payment', 'P9': 'rwb-reporting', 'S1': 'rwb-valuation', 'S2': 'rwb-treatment',
        'S5': 'rwb-asset', 'S8': 'rwb-deviation', 'S9': 'rwb-partner'}
SEC = {'P1': '6.1', 'P2': '6.2', 'P3': '6.3', 'P4': '6.4', 'P5': '6.5', 'P6': '6.6', 'P8': '6.8', 'P9': '6.9',
       'S1': '6.11', 'S2': '6.12', 'S5': '6.15', 'S8': '6.18', 'S9': '6.19'}
A_SD = 'OpenAPI 3.1, /api/recovery/source-data/v1'
A_AC = 'OpenAPI 3.1, /api/recovery/access/v1'
A_EV = 'AsyncAPI 3.0, rwb.source-data.events.v1'
FAKE = "The provider's published contract and its fake"


def full(c):
    return c if c not in CODE else '%s %s' % (c, CODE[c])


INTERACTIONS = 'POST /cases/{caseId}/interactions'
# provider, consumer, type, interface, artefact, class, harness wave, source
NEW = [
    ('P1', 'P6', 'REST', 'GET /customers/{personKey} (recipient name and postal address for notices)', A_SD, 'C', 1, 'RD-P1-060'),
    ('P1', 'P2', 'REST', 'GET /customers/{personKey} (INT-14 outbound file)', A_SD, 'C', 1, 'RD-P1-060'),
    ('P1', 'P3', 'REST', 'GET /customers/{personKey}; GET /accounts/{accountKey}; GET /collateral/{assetKey}', A_SD, 'C', 1, 'RD-P1-060'),
    ('P1', 'P8', 'REST', 'GET /accounts/{accountKey} (fee facts)', A_SD, 'C', 2, 'RD-P1-060'),
    ('P1', 'S5', 'REST', 'GET /collateral/{assetKey}', A_SD, 'C', 2, 'RD-P1-060; RD-P1-069'),
    ('P1', 'P8', 'REST', 'GET /batch-status', A_SD, 'C', 2, 'RD-P1-066'),
    ('P1', 'P2', 'Kafka', 'AceDataReady', A_EV, 'C', 1, 'RD-P1-066'),
    ('P1', 'gateway-bff', 'REST', 'GET /payments?accountKey=', A_SD, 'X', 1, 'RD-P1-061'),
    ('P1', 'P5', 'REST', INTERACTIONS, A_SD, 'C', 1, 'RD-P1-064'),
    ('P1', 'P8', 'REST', INTERACTIONS, A_SD, 'C', 2, 'RD-P1-064'),
    ('P1', 'S2', 'REST', INTERACTIONS, A_SD, 'C', 2, 'RD-P1-064'),
    ('P1', 'S9', 'REST', INTERACTIONS + ' (partner results)', A_SD, 'C', 4, 'RD-P1-064'),
    ('P1', 'S5', 'REST', 'GET /cases/{caseId}/interactions (notice delivery state)', A_SD, 'C', 2, 'RD-P1-064'),
    ('P4', 'P1', 'REST', 'POST /authorise (request and answer pending, NEW-GAP-F09-3)', A_AC, 'C', 1, 'RD-P1-063'),
]
CHANGED = [  # old interface, new interface, old source or None, new source
    ('GET /customers/{id}; GET /accounts/{id}; GET /data-products/freshness (composite case screen, one hop each in parallel)',
     'GET /customers/{personKey}; GET /accounts/{accountKey}; GET /data-products/freshness (composite case screen, one hop each in parallel)',
     'slide 15, slide 20', 'slide 15, slide 20; RD-P1-060'),
    ('Collateral and appraisals (GET /collateral/{id})', 'Collateral and appraisals (GET /collateral/{assetKey})',
     'slide 13, slide 18', 'slide 13, slide 18; RD-P1-060'),
    ('Party flags', 'Party flags (GET /customers/{personKey})', 'slide 13, slide 15', 'slide 13, slide 15; RD-P1-060'),
    ('GET /payments?accountId= (answer shape pending, NEW-GAP-S2B-17)', 'GET /payments?accountKey= (baseline measures)',
     'RD-P1-022', 'RD-P1-022; RD-P1-061'),
]
OWNED = {'P1': ['GET /accounts/{accountKey}', 'GET /collateral/{assetKey}', 'GET /customers/{personKey}'],
         'P3': ['GET /parameters/{key}'], 'P4': ['POST /authorise']}
BASE = {'P1': '/api/recovery/source-data/v1', 'P3': '/api/recovery/case/v1', 'P4': '/api/recovery/access/v1'}
OPEN_NEW = [
    ('NEW-GAP-F09-3', 'Request and answer fields of POST /authorise are not published',
     'The path is in rwb-access.yaml 5.1.0; callers assert only allow or deny and the messageCode', 'rwb-access contract owner'),
    ('NEW-GAP-FD1-contracts-1', 'Name of the business date query parameter of GET /parameters/{key}',
     'rwb-case.yaml 5.1.0 publishes the path parameter only', 'rwb-case service owner'),
    ('NEW-GAP-D1', 'Masking rule rows that unmask recipient name and postal address for the rwb-comms notice and rwb-integration outbound-file identities',
     'GET /customers/{personKey} answers masked values until the rows exist', 'Data protection officer with the rwb-access owner'),
]
CHANGE = ('; batch D (RD-P1-060 to RD-P1-066): customer, account and collateral reads, one GET /payments with two query forms, '
          'ledger callers, authorise and parameter reads, new consumer pairs, section 6.1 aligned to Service Catalog v2')

# ------------------------------------------------------------------ markdown
raw = open(MD, 'rb').read()
EOL = '\r\n' if b'\r\n' in raw else '\n'
lines = raw.decode('utf-8').split(EOL)
D = 'RD-P1-060;RD-P1-061;RD-P1-063;RD-P1-064;RD-P1-066'


def cells(l):
    return [c.strip() for c in l.strip().strip('|').split('|')]


def row(*c):
    return '| ' + ' | '.join(str(x) for x in c) + ' |'


def find(pred, start=0, end=None):
    for i in range(start, len(lines) if end is None else end):
        if pred(lines[i]):
            return i
    raise AssertionError('not found')


def section(num):
    a = find(lambda l: l.startswith('## %s ' % num))
    try:
        b = find(lambda l: l.startswith('## ') or l.startswith('# '), a + 1)
    except AssertionError:
        b = len(lines)
    return a, b


def table_end(i):
    """Index after the last row of the first table that starts at or after line i."""
    i = find(lambda l: l.startswith('|'), i)
    while i < len(lines) and lines[i].startswith('|'):
        i += 1
    return i


def replace(old, new, what, d=D, count=None, g='', f=''):
    n = 0
    for i, l in enumerate(lines):
        if old in l:
            lines[i] = l.replace(old, new)
            n += 1
    assert n and (count is None or n == count), (old, n)
    log('EDIT', NAME + '.md', '%s (%d lines)' % (what, n), old, new, d, f, g, 'v2', 'v3')


# changed pairs: every mirror row (section 5, provider and consumer sections)
for old, new, osrc, nsrc in CHANGED:
    n = 0
    for i, l in enumerate(lines):
        if l.startswith('|') and old in cells(l):
            c = cells(l)
            c = [new if x == old else x for x in c]
            if c[-1] == osrc:
                c[-1] = nsrc
            lines[i] = row(*c)
            n += 1
    assert n, old
    log('EDIT', NAME + '.md', 'pair interface (%d rows)' % n, old, new, D, 'RWB-PLT-N001-CON#1' if 'customers' in old else '', '', 'v2', 'v3')

# new pairs
a = find(lambda l: l.startswith('# 5. '))
hdr = find(lambda l: l.startswith('| Provider | Consumer | Call type'), a)
end = table_end(hdr)
lines[end:end] = [row(full(p), full(c), t, i, art, cl, src) for p, c, t, i, art, cl, w, src in NEW]
for p, c, t, i, art, cl, w, src in NEW:
    for who, other, column in ((p, c, 'provided'), (c, p, 'consumed')):
        if who not in SEC:
            continue
        a, b = section(SEC[who])
        h = find(lambda l: l == ('**Contracts provided**' if column == 'provided' else '**Contracts consumed**'), a, b)
        end = table_end(h + 1)
        new = row(t, full(other), i, art, cl, src) if column == 'provided' else row(t, full(other), i, art, cl, FAKE, src)
        header = lines[find(lambda l: l.startswith('| Call type'), h)]
        assert len(cells(header)) == len(cells(new)), (who, column, header)
        lines.insert(end, new)
    log('ADD', NAME + '.md', 'contract pair (section 5 and sections 6)', '', '%s -> %s %s %s' % (full(p), full(c), t, i), src, '', '', 'v2', 'v3')

# counts
rest = sum(1 for n in NEW if n[2] == 'REST')
kafka = sum(1 for n in NEW if n[2] == 'Kafka')
replace('| REST | 38 |', '| REST | %d |' % (38 + rest), 'section 5 count REST', count=1) if False else None
a = find(lambda l: l.startswith('# 5. '))
for label, add in (('REST', rest), ('Kafka', kafka), ('Total', rest + kafka)):
    i = find(lambda l: re.match(r'\| %s \| \d+ \|$' % label, l), a)
    old = lines[i]
    lines[i] = row(label, int(cells(old)[1]) + add)
    log('EDIT', NAME + '.md', 'section 5 count ' + label, old, lines[i], D, '', '', 'v2', 'v3')

# operations owned
for code, ops in OWNED.items():
    a, b = section(SEC[code])
    h = find(lambda l: l.startswith('**REST operations owned'), a, b)
    first = find(lambda l: l.startswith('|'), h)
    end = table_end(first)
    body = lines[first + 2:end]
    body += [row(o, BASE[code] + o.split(' ', 1)[1], code) for o in ops]
    body.sort(key=lambda l: (cells(l)[0].split(' ', 1)[0], cells(l)[0].split(' ', 1)[1]))
    lines[first + 2:end] = body
    log('ADD', NAME + '.md', 'section %s REST operations owned' % SEC[code], '', '; '.join(ops), 'RD-P1-060;RD-P1-063', '', '', 'v2', 'v3')
replace('29 operations (RD-P1-005)', '32 operations (RD-P1-005, RD-P1-060)', 'section 6.1 operation count', d='RD-P1-060', count=1)

# section 6.1 against Service Catalog v2
replace('| Owns (Arch v5 slide 41) | ACE view contract, extension tables, freshness, reconciliation |',
        '| Owns (Arch v5 slide 41) | ACE view contract, extension tables, freshness, reconciliation, product-to-source map (RD-P1-021) |',
        'section 6.1 Owns', d='RD-P1-021', count=1)
i = find(lambda l: l.startswith('Task queue rwb-source-data; no case-list workflow'))
old = lines[i]
lines[i] = old.replace('no case-list workflow or Schedule exists in P1 (RD-P1-024).',
                       'no case-list workflow or Schedule exists in P1 (RD-P1-024). Provided activities: listEligibleAccounts and snapshot(page); provided query: FreshnessQuery (Service Catalog v2 section 6.1).')
lines[i] = lines[i].replace('rwb.document.events.v1 and rwb.decision-record.v1 for the ledger intake, one consumer group per topic (RD-P1-003, RD-P1-009).',
                            'rwb.document.events.v1 and rwb.decision-record.v1 for the ledger intake, one consumer group per topic (RD-P1-003, RD-P1-009). Consumers of AceDataReady are rwb-case, rwb-payment, rwb-integration, rwb-deviation and rwb-writeoff, each with one consumer group <service>.rwb.source-data.events.v1; every consumer has WRITE and READ on the retry topics and WRITE on the .dlt topic of each topic it reads (RD-P1-066).')
assert lines[i] != old
log('EDIT', NAME + '.md', 'section 6.1 workflows, activities, query, consumer groups and ACLs', old, lines[i], 'RD-P1-066;RD-P1-022', '', '', 'v2', 'v3')

# open points
i = find(lambda l: l.startswith('| NEW-GAP-S10-14 |'))
old = lines[i]
lines[i:i + 1] = []
log('REMOVE', NAME + '.md', 'section 11 open point closed', old, '', 'RD-P1-061', '', 'NEW-GAP-S10-14', 'v2', 'v3')
i = find(lambda l: l.startswith('| NEW-GAP-W1-contracts-2 |'))
lines[i + 1:i + 1] = [row(*o) for o in OPEN_NEW]
for o in OPEN_NEW:
    log('ADD', NAME + '.md', 'section 11 open point', '', row(*o), 'RD-P1-060;RD-P1-063', '', o[0], 'v2', 'v3')

# change log row of version 3
hits = 0
for i, l in enumerate(lines):
    if l.startswith('| 3 | 27 November 2026 |') and 'registration of version 5.1.0.' in l:
        lines[i] = l.replace('registration of version 5.1.0.', 'registration of version 5.1.0' + CHANGE + '.')
        hits += 1
log('EDIT', NAME + '.md', 'version 3 change log row (%d)' % hits, 'registration of version 5.1.0.', 'registration of version 5.1.0' + CHANGE + '.', D, '', '', 'v2', 'v3')
assert hits >= 1
open(MD, 'wb').write(EOL.join(lines).encode('utf-8'))

# ------------------------------------------------------------------ workbook
wb = openpyxl.load_workbook(XL)


def style_like(ws, src, dst):
    for col in range(1, ws.max_column + 1):
        ws.cell(dst, col)._style = copy.copy(ws.cell(src, col)._style)
    if ws.row_dimensions[src].height:
        ws.row_dimensions[dst].height = ws.row_dimensions[src].height


def last_row(ws):
    r = ws.max_row
    while r > 1 and ws.cell(r, 1).value in (None, ''):
        r -= 1
    return r


def append(ws, values):
    r = last_row(ws) + 1
    style_like(ws, r - 1, r)
    for col, v in enumerate(values, 1):
        ws.cell(r, col).value = v
    return r


def refilter(ws):
    if ws.auto_filter.ref:
        first, end = ws.auto_filter.ref.split(':')
        ws.auto_filter.ref = '%s:%s%d' % (first, re.match(r'[A-Z]+', end).group(0), last_row(ws))


def xlog(action, sheet, before, after, d, g=''):
    log(action, NAME + '.xlsx', sheet, before, after, d, '', g, 'v2', 'v3')


ws = wb['Contract pairs']
for r in range(2, last_row(ws) + 1):
    for old, new, osrc, nsrc in CHANGED:
        if ws.cell(r, 5).value == old:
            ws.cell(r, 5).value = new
            if ws.cell(r, 9).value == osrc:
                ws.cell(r, 9).value = nsrc
            xlog('EDIT', 'Contract pairs row %d' % r, old, new, D)
for p, c, t, i, art, cl, w, src in NEW:
    n = int(ws.cell(last_row(ws), 1).value) + 1
    kind = type(ws.cell(last_row(ws), 1).value)
    r = append(ws, [kind(n), full(p), full(c), t, i, art, cl, 'RWB-ITG-W%d harness' % w, src])
    xlog('ADD', 'Contract pairs row %d' % r, '', '%s -> %s %s %s' % (full(p), full(c), t, i), src)
refilter(ws)

ws = wb['REST operations']
for code, ops in OWNED.items():
    for o in ops:
        if any(ws.cell(r, 1).value == o and ws.cell(r, 2).value == code for r in range(2, last_row(ws) + 1)):
            continue
        # keep the sheet sorted by method and path
        key = tuple(o.split(' ', 1))
        pos = next((r for r in range(2, last_row(ws) + 1) if tuple(str(ws.cell(r, 1).value).split(' ', 1)) > key), last_row(ws) + 1)
        end = last_row(ws)
        for r in range(end, pos - 1, -1):
            for col in range(1, 5):
                ws.cell(r + 1, col).value = ws.cell(r, col).value
            style_like(ws, r, r + 1)
        for col, v in enumerate([o, code, BASE[code] + o.split(' ', 1)[1], BASE[code]], 1):
            ws.cell(pos, col).value = v
        xlog('ADD', 'REST operations row %d' % pos, '', o, 'RD-P1-060;RD-P1-063')
refilter(ws)

ws = wb['Events']
for r in range(2, ws.max_row + 1):
    if ws.cell(r, 1).value == 'EV-26':
        old = ws.cell(r, 5).value
        ws.cell(r, 5).value = old + '; P2 rwb-integration'
        xlog('EDIT', 'Events EV-26 consumers', old, ws.cell(r, 5).value, 'RD-P1-066')

ws = wb['Services']
for r in range(2, ws.max_row + 1):
    if ws.cell(r, 1).value == 'P1':
        old = ws.cell(r, 11).value
        if 'product-to-source' not in old:
            ws.cell(r, 11).value = old + ', product-to-source map (RD-P1-021)'
            xlog('EDIT', 'Services P1 Owns', old, ws.cell(r, 11).value, 'RD-P1-021')

ws = wb['Temporal contracts']
if not any(ws.cell(r, 2).value == 'FreshnessQuery' for r in range(1, ws.max_row + 1)):
    r = append(ws, ['Query', 'FreshnessQuery', 'P1 rwb-source-data', 'rwb-source-data', 'Activity contract jar', 'None named in the sources', 'Service Catalog v2 section 6.1; RD-P1-022'])
    refilter(ws)
    xlog('ADD', 'Temporal contracts row %d' % r, '', 'Query FreshnessQuery', 'RD-P1-022')

ws = wb['Open points']
for r in range(last_row(ws), 1, -1):
    if ws.cell(r, 1).value == 'NEW-GAP-S10-14':
        before = ' | '.join(str(ws.cell(r, c).value) for c in range(1, 5))
        for s in range(r, last_row(ws)):
            for col in range(1, 5):
                ws.cell(s, col).value = ws.cell(s + 1, col).value
        end = last_row(ws)
        for col in range(1, 5):
            ws.cell(end, col).value = None
        xlog('REMOVE', 'Open points', before, '', 'RD-P1-061', 'NEW-GAP-S10-14')
for o in OPEN_NEW:
    # first empty row after the data
    r = last_row(ws) + 1
    style_like(ws, r - 1, r)
    for col, v in enumerate(o, 1):
        ws.cell(r, col).value = v
    xlog('ADD', 'Open points row %d' % r, '', o[0], 'RD-P1-060;RD-P1-063', o[0])
refilter(ws)

ws = wb['Change log']
for row_ in ws.iter_rows():
    for c in row_:
        if isinstance(c.value, str) and 'registration of version 5.1.0.' in c.value:
            c.value = c.value.replace('registration of version 5.1.0.', 'registration of version 5.1.0' + CHANGE + '.')
            xlog('EDIT', 'Change log ' + c.coordinate, 'registration of version 5.1.0.', CHANGE, D)
wb.save(XL)
print('ok', rest, kafka)
