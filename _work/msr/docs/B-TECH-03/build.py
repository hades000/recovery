"""Build the next version of each module TSD (WP B-TECH-03). Writes only inside the v6 folder."""
from pathlib import Path
import json
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import content as C  # noqa: E402

ROOT = Path(r'.')
SRC = ROOT / '05 Technical architecture/Recovery Workbench Technical Specifications by Module v5'
DST = ROOT / '05 Technical architecture/Recovery Workbench Technical Specifications by Module v6'
DATA = json.loads((Path(__file__).resolve().parent / 'data.json').read_text(encoding='utf-8'))

HEADER = ("SCB Collections and Recovery. Henka Group, 22 November 2026.\n"
          "(C) Siam Commercial Bank and Henka Pte Ltd\n")
RUN_DATE = "22 November 2026"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
DEC = "D-RCV-60"
GC = "CG-B-TECH-03-"
GA = "ASM-B-TECH-03-"

NOT = {
    "P1": "It runs no source load and copies no source record: ACE ingests every source and P1 reads the result (D-RCV-35).",
    "P2": "It receives no inbound file: every inbound interface lands in ACE and is read through the views (D-RCV-35).",
    "P3": "It holds no rule package and no Drools table: the registry is P7's and evaluation is embedded (DP-04; ADR-017).",
    "P4": "It holds no partner user and no reference data: partner users are S9's and reference data is P3's (DP-07).",
    "P5": "It holds no notice text: templates and notices are P6's, and P5 keeps the generated document (DP-01).",
    "P6": "It holds no signature row and no letter content: both are P5's (DP-01; ASM-A6-tables-11).",
    "P7": "It holds no business table of another service: every decision arrives as an event or a contract call (EV-08).",
    "P8": "It holds no matching rule: the match rules are a rule package of rwb-decision (DP-04; ASM-B-TECH-03-5).",
    "P9": "It holds no data lake and no source copy: the projections are built from events (DP-17; ADR-018).",
    "P10": "It reaches no business table: every fact comes through the read-only tool gateway (DP-20).",
    "S1": "It writes no case row: the route decision is returned to P3 through the child workflow (DP-12).",
    "S2": "It holds no contract document: P5 generates and seals it and S2 keeps the reference (DP-11).",
    "S3": "It sends no notice itself: the guarantor notice is a P6 child workflow (DP-11).",
    "S4": "It instructs no partner itself: the law-firm instruction runs on S9's queue (DP-11).",
    "S5": "It holds no asset record: the asset is an ACE record read through the read path (DP-05).",
    "S6": "It publishes no data room: the pack is a P5 document set (DP-11).",
    "S7": "It posts nothing to the GL: the postings stay in ACE and are read through P1 (INT-16).",
    "S8": "It does not stop a case by writing case state: it raises the deviation event that P3 acts on (EV-06).",
    "S9": "It authenticates no staff user: staff arrive through gateway-bff and partners through the partner gateway (ADR-019).",
}


def req(text, needle, name):
    if needle not in text:
        raise SystemExit(f'MISSING {name}: {needle!r}')
    return text


def split_block(text, start, end):
    i = req(text, start, start)
    i = text.find(start)
    j = text.find(end, i + len(start))
    if j < 0:
        raise SystemExit(f'no end marker {end!r} after {start!r}')
    return text[:i], text[i:j], text[j:]


def doc_control(text, code, ver, prev_ver, prev_date):
    head, block, tail = split_block(text, '## Document control', '\n\n| Document | Type | Relationship |')
    rows = [l for l in block.splitlines() if l.startswith('|')]
    # only the attribute table: rows end at the first blank line after the first row
    first = next(i for i, l in enumerate(block.splitlines()) if l.startswith('|'))
    keep = []
    for l in block.splitlines()[first:]:
        if not l.startswith('|'):
            break
        keep.append(l)
    rest = block.splitlines()[first + len(keep):]
    cells = [[c.strip() for c in l.strip().strip('|').split('|')] for l in keep]
    cells = [c for c in cells if not all(set(x) <= set('-: ') for x in c)]
    out = []
    seen = set()
    for r in cells:
        k = r[0]
        if k in ('Attribute',):
            out.append(r)
            continue
        if k == 'Document ID':
            r = [k, f'{code}-RWB-TSD-v{ver}']
        elif k == 'Version':
            r = [k, str(ver)]
        elif k == 'Date':
            r = [k, RUN_DATE]
        elif k == 'Status':
            r = [k, 'Draft']
        elif k == 'Build squad':
            r = [k, f"{r[1]} ({GC}9; {GA}9: no squad is named per service)"]
        elif k == 'Decision':
            r = [k, f'{DEC} microservice realignment; {r[1]}']
        out.append(r)
        seen.add(k)
        if k == 'Date':
            out.append(['Supersedes', f'Version {prev_ver}, {prev_date}'])
    if 'Decision' not in seen:
        out.append(['Decision', f'{DEC} microservice realignment'])
    out.append(['Status note', f'Draft: no approval of version {ver} is recorded ({GC}8; {GA}1)'])
    out.append(['Change', f'{ver}, {RUN_DATE}, {DEC} microservice realignment, {TOOL}'])
    table = '\n'.join('| ' + ' | '.join(r) + ' |' for r in out)
    table = table.replace('| Attribute | Value |', '| Attribute | Value |\n|---|---|', 1)
    extra = '\n'.join(rest).strip('\n')
    tail = tail.lstrip('\n')
    mid = (extra + '\n\n') if extra else ''
    return head + '## Document control\n\n' + table + '\n\n' + mid + tail


def add_related(text):
    """Add the Ownership Map to the related-documents table."""
    m = re.search(r'(\| Document \| Type \| Relationship \|\n\|---\|---\|---\|\n(?:\|[^\n]*\n)+)', text)
    if not m:
        return text
    block = m.group(1)
    if 'Ownership Map' in block:
        return text
    row = ('| Recovery Workbench Microservice Ownership Map v1 | Ownership | Owner of every table, endpoint, event, '
           'workflow and job in T0 and T5.2 |\n')
    return text[:m.end()] + row + text[m.end():]


def t1(text, d):
    old = (f"{d['code']} {d['module']} is part of the recovery module in the ACE service: one service, "
           "one repository, one front end.")
    new = (f"{d['code']} {d['module']} is delivered as the service `{d['service']}` (module {d['code']}, wave "
           f"{d['wave']}, service epic `{d['epic']}`): one repository, one pipeline, one schema `{d['schema']}` with "
           "one login, behind gateway-bff (ADR-013, ADR-014).")
    return text.replace(old, new)


def cap_check_note(text):
    anchor = '\n## T1. Architecture overview'
    note = ("\nUnder D-RCV-60 the scheduler and batch row is delivered by the Temporal layer (ADR-016): Temporal "
            "Schedules and event-started workflows in the owning service replace the Quartz and Spring Batch jobs "
            "(DP-10). The outbox and retry row is delivered by the Kafka outbox, inbox and retry topics (ADR-015; "
            "DP-09).\n")
    i = text.find(anchor)
    return text[:i] + note + text[i:]


def t0(d):
    ev_list = ', '.join((e['ev'] + ' ' + e['name']) if e['ev'] else e['name'] for e in d['events']) or 'none'
    tbl = ', '.join('`' + t + '`' for t in d['tables']) or ('none recorded for this service in the Ownership Map '
                                                            'Tables sheet')
    wf_names = [r[1] for r in d['provided_temp'] if r[0].startswith('Temporal')]
    wf = ', '.join(d['workflows']) if d['workflows'] else 'none in the Ownership Map sheet'
    wf_count = len(d['workflows'])
    if not d['workflows'] and wf_names:
        wf += '; T5.2.1 names ' + ', '.join(wf_names)
        wf_count = len(wf_names)
    retired = [j for j, r in d.get('jobs_info', {}).items() if 'retired' in str(r).lower()]
    live = [j for j in d['jobs'] if j not in retired]
    jobs = ', '.join(live) if live else 'none'
    if retired:
        jobs += ('; retired under D-RCV-35: ' + ', '.join(retired)) if not live else \
            ('; retired: ' + ', '.join(retired))

    pats = []
    src = (SRC / d['src_name']).read_text(encoding='utf-8')
    for dp, (rx, land) in C.LANDS.items():
        m = re.search(rx, src)
        ev = '—'
        if m:
            top = re.sub(r'\n### T5\.2.*?\n## T6\.', '\n## T6.', src, flags=re.S)
            cand = [l for l in top.splitlines() if re.search(rx, l) and l.strip()
                    and not l.startswith('|---') and not l.startswith('#')]
            cand.sort(key=lambda l: l.lstrip().startswith('|'))
            if cand:
                line = re.sub(r'\s+', ' ', cand[0].strip().strip('|').strip())
                mm = re.search(rx, line)
                s = max(0, mm.start() - 40)
                e = min(len(line), mm.end() + 40)
                while s > 0 and line[s - 1] != ' ':
                    s -= 1
                while e < len(line) and line[e] != ' ':
                    e += 1
                ev = re.sub(r'\s*\|\s*', ' / ', line[s:e]).replace('`', "'")
                ev = ('…' if s > 0 else '') + ev.strip(' /') + ('…' if e < len(line) else '')
        if dp in C.CORE or m:
            pats.append((dp, ev, land.format(schema=d['schema'], base=d['base'], topic=d['topic'])))
    pat_rows = '\n'.join(f'| {a} | `{b}` | {c} |' if b != '—' else f'| {a} | — | {c} |' for a, b, c in pats)
    return f"""## T0. Service

{d['code']} {d['module']} is one of the 19 services of Architecture v5: `{d['service']}` (service name {d['service_name']}, module {d['code']}, wave {d['wave']}, service epic `{d['epic']}`). Version {d['ver']} adds this section so that the specification is read as the specification of one service: its identity, what it owns, and the decoupling patterns that replace the monolith's in-process calls. Every owner is taken from Microservice Ownership Map v1 and every identifier from Template and Rules R4 (ADR-013, ADR-014).

{d['mod_note']}

### T0.1 Service identity

| Item | Value |
|---|---|
| Module | {d['code']} {d['module']} |
| Service | `{d['service']}` ({d['service_name']}) |
| Service epic | `{d['epic']}` |
| Wave | {d['wave']} |
| Schema | `{d['schema']}` |
| Database login | `{d['schema']}`: one login per service, with its own connection pool cap |
| REST base | `{d['base']}` |
| Kafka topic | `{d['topic']}`, with `.retry` and `.dlt` topics |
| Event names | `rwb.{d['short']}.<Event>.v1`, CloudEvents 1.0 in binary mode, key `caseId` |
| Temporal | namespace `rwb-recovery`; task queue `{d['queue']}` |
| Java package | `{d['package']}` |
| Edge | {d['edge']} |
| Contract artefacts | `{d['api_file']}`; `{d['asyncapi_file']}` |
| Suggested owner, app development | TechX (suggested; any team may pick up this story) |
| Suggested owner, ACE DB | ACE team (suggested; any team may pick up this story) |

### T0.2 What this service owns

Architecture v5 slide 41 gives this service: {d['owns']}. Table T0.2 states the same ownership in the form the Ownership Map uses, with the counts this specification carries. A table that the map assigns to another service is not built here, whatever T3 says (see the note under T3).

| Area | Owner and artefact | Count |
|---|---|---|
| Business tables in `{d['schema']}` | {tbl} | {len(d['tables'])} |
| REST operations | appendix T-A and `{d['api_file'].split('/')[-1]}` | {len(d['ops'])} |
| Events published | {ev_list} | {len(d['events'])} |
| Workflows and schedules | {wf} | {wf_count} |
| Jobs | {jobs} | {len(live)} |

### T0.3 Decoupling patterns applied

The left column is the pattern of Template and Rules R5.5; the middle column quotes the line of this specification that carries the legacy marker, where one is present; the right column is what replaces it in this service.

| DP | Legacy marker in this specification | How the service lands it |
|---|---|---|
{pat_rows}

### T0.4 What this service is not

- It holds no other service's table and no ACE table beyond the read-only `recovery.v_ace_*` views (DP-01, DP-05).
- It runs no shared Quartz job and touches no ACE batch table (DP-10; ADR-016).
- {NOT[d['code']]}
- It is not a monolith module: the published Java interface of T2 is replaced by the contract set of T5.2 (DP-11; ADR-020).

"""


def t2_note(d):
    return ("\nThe published interface of this table is the contract set of T5.2: the REST operations, the events and "
            "the workflows, not a Java interface in a shared classpath (DP-11; ADR-020). Components that the Ownership\n"
            "Map places in another service are stated in T0.2 and T5.2 and are built by that service.\n")


def t3_note(d):
    return (f"\nEvery object of T3 that Microservice Ownership Map v1 assigns to `{d['service']}` lives in schema "
            f"`{d['schema']}` with the standard columns of T3.0 (DP-01, DP-15; ADR-014). {d['t3_note']}\n")


def contracts(d):
    blk = []
    # 5.2.1 provided REST
    if d['ops']:
        rows = '\n'.join(f"| {i} | {o['method']} | `{o['path']}` | `{o['operationId'] or '—'}` |"
                         for i, o in enumerate(d['ops'], 1))
        rest = ('| # | Method | Path | operationId |\n|---|---|---|---|\n' + rows)
    else:
        rest = 'None.'
    rest += {'S1': ('\nThe valuation path was moved here from S5 in the API split (Ownership Map ruling '
                    '`POST /assets/{assetKey}/valuations`, ASM-A6-api-6).'),
             }.get(d['code'], '')
    # 5.2.1 provided other
    other_rows = []
    for t, name, called_by, note in d['provided_temp']:
        other_rows.append(f'| {name} | {t} | {called_by} | {note} |')
    for t, name, target, note in d['files']:
        other_rows.append(f'| {name} | {t} | {target} | {note} |')
    other = ('| Contract | Type | Called by or target | Note |\n|---|---|---|---|\n' + '\n'.join(other_rows)) \
        if other_rows else 'None.'
    # 5.2.1 events
    if d['events']:
        ev_rows = '\n'.join(
            f"| {e['name']} | {e['ev'] or '—'} | `{e['channel'] or d['topic']}` | "
            f"{', '.join(e['consumers']) or '—'} |" for e in d['events'])
        evs = ('| Event | EV | Topic | Consumers |\n|---|---|---|---|\n' + ev_rows)
    elif d['code'] == 'P9':
        evs = (f"None published by this service: Architecture v5 slide 15 names ReportPublished on "
               f"`{d['topic']}` and the AsyncAPI document of 22 November 2026 does not carry it yet ({GC}6; {GA}7).")
    else:
        evs = f'None published by this service yet ({GC}6; {GA}7).'
    # 5.2.2 consumed calls
    cons_rows = []
    for t, op, prov, klass, fail in d['consumed_rest'] + d['consumed_temp']:
        cons_rows.append(f'| {op} | {t} | {prov} | {klass} | {fail} |')
    cons = ('| Contract | Type | Provider | Class | Failure path |\n|---|---|---|---|---|\n' + '\n'.join(cons_rows)) \
        if cons_rows else 'None.'
    # 5.2.2 consumed events
    def prov_label(prov):
        return prov if prov not in DATA else f'{prov} {DATA[prov]["service"]}'

    def prov_topic(prov):
        if prov == 'all':
            return 'all 19 service topics'
        return DATA[prov]['topic'] if prov in DATA else prov

    if d['consumed_events']:
        cev = '\n'.join(
            f"| {name} | {ev or '—'} | `{prov_topic(prov)}` | {prov_label(prov)} | C | {C.E_FAIL} |"
            for ev, name, prov in d['consumed_events'])
        cevt = ('| Event | EV | Provider topic | Provider | Class | Failure path |\n|---|---|---|---|---|---|\n' + cev)
    else:
        cevt = 'None.'
    # counts
    n_rest_p = len(d['ops'])
    n_rest_c = sum(1 for r in d['consumed_rest'] if r[0] == 'REST')
    n_kafka_p = len(d['events'])
    n_kafka_c = len(d['consumed_events'])
    n_tmp_p = sum(1 for r in d['provided_temp'] if r[0].startswith('Temporal'))
    n_tmp_c = sum(1 for r in d['consumed_temp'] if r[0].startswith('Temporal'))
    n_file_p = sum(1 for r in d['files'] if 'file' in r[0].lower())
    n_file_c = 0
    n_nex_p = 0
    n_nex_c = sum(1 for r in d['consumed_temp'] if r[0] == 'Nexus')
    n_sql_p = sum(1 for r in d['files'] if r[0].startswith('SQL'))
    n_sql_c = sum(1 for r in d['consumed_rest'] if r[0] == 'SQL')
    return f"""### T5.2 Contracts

Version {d['ver']} states every cross-module dependency of this module as a contract, so that the service is built
against a published artefact and its fake (ADR-020; DP-11). The artefact per call type is: OpenAPI 3.1 for REST,
AsyncAPI 3.0 for Kafka, the Temporal interface named here for a workflow or activity, the Interface Specifications
manifest for a file, the Nexus operation for the ACE restructure calculator, and a grant on the view for SQL. No row of
this section reads another service's table (DP-01). Every consumed contract is class C (Template and Rules R5.4): it
never blocks the build, because the consumer builds against the fake, and the real cross-service behaviour is class I
work on an integration story. Architecture v5 slides 13 to 20 name a few operations differently from the published
files of 22 November 2026; the published file is the artefact the fake is generated from and is the one cited here
({GC}7; {GA}8).

#### T5.2.1 Contracts provided

The REST operations of this service are published in `{d['api_file']}` (5.0.0, 22 November 2026) under the base
`{d['base']}`. Appendix T-A holds the endpoint IDs, the access right and the first release of each one.

{rest}

Workflows, schedules, files and views this service provides:

{other}

Events this service publishes (AsyncAPI 3.0, CloudEvents 1.0):

{evs}

#### T5.2.2 Contracts consumed

{cons}

Events this service consumes:

{cevt}

#### T5.2.3 Call-type summary

| Call type | Provided | Consumed | Artefact |
|---|---|---|---|
| REST | {n_rest_p} | {n_rest_c} | OpenAPI 3.1, one file per service |
| Kafka (events) | {n_kafka_p} | {n_kafka_c} | AsyncAPI 3.0, one file per service |
| Temporal | {n_tmp_p} | {n_tmp_c} | Workflow and activity interfaces, queue `{d['queue']}` |
| File | {n_file_p} | {n_file_c} | Interface Specifications manifest and the SAS link |
| Nexus | {n_nex_p} | {n_nex_c} | Nexus operation into ACE |
| SQL | {n_sql_p} | {n_sql_c} | Read-only grant on the view |

A contract change is a new version of the artefact, never a code change in the consumer (ADR-020). The provider named
in T5.2.2 is the owner in Microservice Ownership Map v1, and the consumer list of each event is the Arch v5 event
catalogue on slides 42 and 43.

"""


def events_section(d):
    rows = []
    for e in d['events']:
        rows.append(f"| {e['name']} | {e['ev'] or '—'} | Published | `{e['channel'] or d['topic']}` |")
    for ev, name, prov in d['consumed_events']:
        topic = 'all 19 service topics' if prov == 'all' else (DATA[prov]['topic'] if prov in DATA else prov)
        rows.append(f"| {name} | {ev or '—'} | Consumed | `{topic}` |")
    table = ('| Event | EV | Direction | Topic |\n|---|---|---|---|\n' + '\n'.join(rows)) if rows else \
        ('| Event | EV | Direction | Topic |\n|---|---|---|---|\n| None | — | — | — |')
    extra = {
        'P7': ('Architecture v5 slide 14 also names ApprovalDecided on `rwb.decision.events.v1`; the AsyncAPI document '
               f'of 22 November 2026 does not carry it ({GC}6; {GA}7).'),
        'P9': ('Architecture v5 slide 15 names ReportPublished on `rwb.reporting.events.v1`; there is no AsyncAPI '
               f'operation for this service yet ({GC}6; {GA}7).'),
        'S3': ('Architecture v5 slide 18 names GuaranteeClaimFiled and GuaranteeClaimSettled; the AsyncAPI document '
               f'carries the single message GuaranteeClaim ({GC}6; {GA}7).'),
        'S4': ('Architecture v5 slide 19 names LawsuitFiled on `rwb.litigation.events.v1`; the AsyncAPI document of '
               f'22 November 2026 does not carry it ({GC}6; {GA}7).'),
    }.get(d['code'], '')
    return f"""### T5.3 Events

The event contract of this service is `{d['asyncapi_file']}`; the shared decision-record contract is
`asyncapi/rwb.decision-record.v1.asyncapi.yaml`. Every service publishes DecisionRecorded (EV-08) to
`rwb.decision-record.v1` from its outbox in the same transaction as its state change (DP-03, DP-09; ADR-015, ADR-022);
consuming services dedupe through their inbox table. Events carry identifiers and facts, never personal data (Event and
Messaging Design v4, sheet Rules).

{table}

An event shown with `—` has no number in the numbered catalogue: the Arch v5 catalogue calls these rows `+`, so the
number is not specified in the source documents ({GC}6; {GA}7). {extra}
"""


def reflow(text):
    """Join hard-wrapped prose lines into one line per paragraph, outside fenced blocks and tables."""
    out, buf, fence = [], [], False
    prose = re.compile(r'^(?![|#>*\-]|\d+\.|```|    )')

    def flush():
        if buf:
            out.append(' '.join(x.strip() for x in buf))
            buf.clear()

    for line in text.splitlines():
        if line.startswith('```'):
            flush()
            fence = not fence
            out.append(line)
            continue
        if fence or not line.strip() or not prose.match(line):
            flush()
            out.append(line)
            continue
        buf.append(line)
    flush()
    # one blank line at most, outside fenced blocks
    tight, fence, prev_blank = [], False, False
    for line in out:
        if line.startswith('```'):
            fence = not fence
        if not line.strip() and not fence:
            if prev_blank:
                continue
            prev_blank = True
        else:
            prev_blank = False
        tight.append(line)
    return '\n'.join(tight) + '\n'


def t6(text, d):
    i = text.find('### T6.2 Authentication and authorization')
    j = text.find('\n## ', i)
    body = text[i:j]
    if d['code'] == 'P4':
        add = ("\n\nThis service is the authorisation provider of DP-08: it publishes the authorise, permission, "
               "delegation-limit and masking operations that the other 18 services call, and it applies the same "
               f"check to its own administration operations (H RWB-PLT-E1037-CON).\n")
    else:
        add = (f"\n\nEvery operation of T5.2.1 is authorised through the `{d['auth_provider']}` authorise contract with "
               f"the role, the scope and the delegation limit of T6.1 (DP-08; {d['auth_class']}); the caller caches "
               "the answer and refreshes it on AccessPolicyChanged and DoaLimitChanged.\n")
    return text[:j].rstrip('\n') + add + text[j:]


def ta(text, d):
    i = text.find('## Appendix T-A')
    text = text[:i] + text[i:].replace('/api/recovery/v1/', d['base'] + '/')
    anchor = '### T-A.2 Endpoint detail'
    note = (f"\nThe operation IDs, paths and operationIds of these endpoints are published in `{d['api_file']}`; where "
            f"an appendix row and the published operation differ, the published operation is the contract of T5.2.1 and "
            f"the row keeps its ID for traceability ({GC}7; {GA}8).\n\n")
    i = text.find(anchor)
    return text[:i] + note + text[i:]


ROWFIX = {
    "P1": [
        ("| Jobs | Case list build and publish (E1-002), JOB-04 daily reconciliation, JOB-13 decision log copy. All "
         "start on the ACE batch-complete record or on their schedule. JOB-01 and JOB-09 are retired under D-RCV-35 |",
         "| Jobs | Case list build and publish (E1-002) and JOB-04 daily reconciliation as event-started workflows "
         "(DP-10); JOB-01 and JOB-09 are retired under D-RCV-35; JOB-13 (decision log copy) is P7's job in the "
         "Ownership Map |"),
        ("| Published interface | Java interface other modules call: freshness, the ACE read methods and the "
         "dictionary. No table is read across modules |",
         "| Published interface | The contracts of T5.2: the freshness, ACE read and dictionary operations, and the "
         "activities of T5.2.1; no table is read across modules (DP-11) |"),
        ("Other recovery modules read ACE data through this repository's published interface",
         "Other recovery modules read ACE data through the contract of T5.2.1"),
    ],
    "P2": [
        ("| Jobs | Quartz and Spring Batch jobs the module owns: the outbound file runs, the data lake publish and the "
         "outbox relay |",
         "| Jobs | Outbound file runs as Temporal workflows and the outbox relay of the platform library (DP-09, "
         "DP-10); the data lake publish is removed (DP-17) |"),
        ("| Published interface | Java interface other modules call to queue outbound work; no table is read across "
         "modules |",
         "| Published interface | The contracts of T5.2: the outbound file activities and the operational operations; "
         "no table is read across modules (DP-11) |"),
    ],
    "P3": [
        ("| RulePackageRepository | Reads rule_package, rule_package_version and rule_row; holds the workbook, the DRL "
         "and the checksum of each version |",
         "| RulePackageRepository | Reads the rule package versions from the `rwb-decision` contract (T5.2.2); holds "
         "no rule package table in `rwb_case` (" + GC + "3; " + GA + "4) |"),
        ("| RuleCatalog | Published interface; reads action text, owner role, timer spec and outputs from rule_row by "
         "rule ID and package version |",
         "| RuleCatalog | Published interface; reads action text, owner role, timer spec and outputs from P7's rule "
         "package contract by rule ID and package version (T5.2.2) |"),
        ("| TimerCheckJob | JOB-05 on Quartz; the implementation of TimerScheduler in Epics 1 and 2 |",
         "| TimerCheckJob | Durable timers inside the workflow; JOB-05 on Quartz is retired under " + DEC + " "
         "(DP-10; ADR-016) |"),
    ],
    "P4": [
        ("P4 owns the four rule tables: rule_package (DF-REF-274 to 278), rule_package_version (279 to 295), rule_row "
         "(001 to 015 and 052 to 054, with 296 to 298 added) and rule_test_case (185 to 197, with 299 added).",
         "Version 3 gives P4 the four rule tables rule_package, rule_package_version, rule_row and rule_test_case; "
         "the Ownership Map places them in `rwb-decision` and Architecture v5 slide 41 gives P7 the DMN model "
         "registry, so they are built there (" + GC + "3). The field rows stay here for the trace of T3."),
        ("**rule_test_case** (NEW, owned by P4).",
         "**rule_test_case** (NEW; P7's table, field row kept for the T3 trace)."),
        ("**partner_user** (NEW).", "**partner_user** (NEW; S9's table, field rows kept for the T3 trace)."),
        ("**lov_value** (NEW).", "**lov_value** (NEW; P3's table, field rows kept for the T3 trace)."),
        ("| RulePackageStore | Owns rule_package, rule_package_version, rule_row and rule_test_case; stores each "
         "version with its workbook, DRL, checksum and checklist |",
         "| RulePackageStore | Reads rule_package, rule_package_version, rule_row and rule_test_case from P7's "
         "contract; the four tables are the P7 registry (Ownership Map; Architecture v5 slide 41; " + GC + "3) |"),
        ("The rule package store is the four tables rule_package, rule_package_version, rule_row and rule_test_case "
         "(ADR-012)",
         "The rule package store is the four tables rule_package, rule_package_version, rule_row and rule_test_case, "
         "which the Ownership Map places in `rwb-decision` (ADR-012; " + GC + "3)"),
    ],
}
T2_EXTRA = {
    "P3": (" T2.2 to T2.5 keep the version 3 text for the rule package, the timer port and the worker; where they name "
           "a table that the Ownership Map places in another service, T0.2 and T5.2 win and the table is built there "
           "(" + GC + "3)."),
    "P4": (" T2 of version 3 describes the rule package store; the registry tables are P7's and P4 reads them through "
           "the contract of T5.2.2 (" + GC + "3)."),
}


def build_one(code):
    d = dict(DATA[code])
    d.update(C.MODULES[code])
    d['mod_note'] = C.MODULES[code]['t0_note']
    d['ver'] = d['versions'][-1][0] + 1
    d['prev_ver'] = d['versions'][-1][0]
    d['src_name'] = d['versions'][-1][1]
    prev = (SRC / d['src_name']).read_text(encoding='utf-8')
    m = re.search(r'\| Date \| (\d+ \w+ \d{4}) \|', prev)
    d['prev_date'] = m.group(1) if m else '—'
    d['auth_provider'] = 'rwb-access' if code != 'P4' else 'rwb-access (this service)'
    d['auth_class'] = 'C RWB-P4-E1037-CON' if code != 'P4' else 'H RWB-PLT-E1037-CON'
    d['edge'] = ({
        'S9': 'gateway-bff for staff screens; the partner gateway in the DMZ for partner traffic',
        'P10': 'gateway-bff for the agent administration and evaluation screens',
        'P1': 'gateway-bff for the data-catalog and administration screens; no partner traffic',
        'P2': 'gateway-bff for the operations screens; no partner traffic',
    }).get(code, 'gateway-bff for the staff screens of this service')

    text = prev
    # 1. title block and header
    lines = text.splitlines()
    assert lines[0].startswith('# '), code
    title = lines[0][2:].strip()
    i = text.find('## Document control')
    body = text[i:]
    out = HEADER + '\n' + '# ' + title + '\n\n' + \
        f'Technical specification. SCB Collections and Recovery. Henka Group, {RUN_DATE}.\n\n' + \
        '(C) Siam Commercial Bank and Henka Pte Ltd\n\n' + body
    out = doc_control(out, code, d['ver'], d['prev_ver'], d['prev_date'])
    out = add_related(out)
    out = t1(out, d)
    out = out.replace('only through their published interfaces', 'only through the contracts of T5.2')
    out = cap_check_note(out)
    out = out.replace('\n## T1. Architecture overview', '\n' + t0(d) + '## T1. Architecture overview', 1)
    # T2 rows
    out = out.replace('| Jobs | Quartz and Spring Batch jobs the module owns |',
                      '| Jobs | Temporal Schedules and event-started workflows this service owns (T0.2, T5.2.1; DP-10) |')
    out = out.replace('| Published interface | Java interface other modules call; no table is read across modules |',
                      '| Published interface | The contracts of T5.2: REST operations, events and workflows other '
                      'services call; no table is read across modules (DP-11) |')
    out = out.replace('\n## T3. Data model', t2_note(d) + '\n## T3. Data model', 1)
    out = out.replace('\n### T3.0 Standard record columns', t3_note(d) + '\n### T3.0 Standard record columns', 1)
    # T5.2 and T5.3
    head, _b, tail = split_block(out, '### T5.2', '### T5.3')
    out = head + contracts(d) + tail
    head, _b, tail = split_block(out, '### T5.3', '\n## T6. Security and access control')
    out = head + events_section(d) + tail
    for a, b in ROWFIX.get(code, []):
        if a in out:
            out = out.replace(a, b, 1)
        else:
            print('ROWFIX not applied for', code, ':', a[:60])
    if code in T2_EXTRA:
        out = out.replace(t2_note(d), t2_note(d).rstrip('\n') + T2_EXTRA[code] + '\n', 1)
    out = t6(out, d)
    out = ta(out, d)
    head2, rest2 = out.split('\n', 2)[0] + '\n' + out.split('\n', 2)[1], out.split('\n', 2)[2]
    out = head2 + '\n' + reflow(rest2)
    # version history rows for the files that keep one
    if '| Version | Date | Change |' in out:
        out = out.replace('\n\n| Document | Type | Relationship |',
                          f'\n| {d["ver"]} | {RUN_DATE} | {DEC} microservice realignment: T0 Service, T5.2 as contracts, '
                          f'Ownership Map v1 owners |\n\n| Document | Type | Relationship |', 1)
    if '### Changes in version 3' in out:
        tbl = (f'### Changes in version {d["ver"]}\n\n| Area | Change |\n|---|---|\n'
               f'| T0 | Service section added: identity, ownership, decoupling patterns |\n'
               f'| T5.2 | Rewritten as contracts: provided and consumed REST, events, Temporal, files and views |\n'
               f'| T5.3 | Events restated with the EV numbers of the Arch v5 catalogue |\n'
               f'| Owners | Every owner taken from Microservice Ownership Map v1 |\n\n')
        out = out.replace('### Changes in version 3', tbl + '### Changes in version 3', 1)
    # drop trailing whitespace
    out = re.sub(r'[ \t]+\n', '\n', out)
    out = re.sub(r'\n{4,}', '\n\n\n', out)
    name = re.sub(r' v\d+\.md$', f' v{d["ver"]}.md', d['src_name'])
    (DST / name).write_text(out, encoding='utf-8')
    return name, d['ver']


def main():
    if not DST.exists():
        raise SystemExit('v6 folder missing: copy it first with office_write.py copy')
    names = []
    for code in C.MODULES:
        names.append(build_one(code))
    for n, v in names:
        print(n, v)


if __name__ == '__main__':
    main()
