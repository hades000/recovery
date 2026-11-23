# Edit log B-ITG-W1-09 — RWB-ITG-W1 (legacy RWB-E1-065, RWB-E1-066, RWB-E1-067, RWB-E1-069, RWB-E1-070)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60
Date: 22 November 2026
Work package: B-ITG-W1-09 (RWB-ITG-W1 Wave 1 integration)
Fanout: 5 subagents (aisdlc-msr-worker), one per legacy key, dispatched in one message. Two returned complete (E1067, E1070). The E1065, E1066 and E1069 dispatches failed at the transport layer (ECONNRESET, concurrency limit, ECONNREFUSED); their slices were finished and verified by the parent against the same per-key brief, and the parent then aligned all five fragments with their story files and held the register rows as one set.

## Story files written (5)

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1065 ITG Sandbox database with synthetic recovery data - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1066 ITG Interaction ledger store and writer - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1067 ITG Every Workbench action into the interaction ledger - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1069 ITG Read-only ACE source views, grants and boundary rule - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1070 ITG Temporal platform on the ACE AKS clusters - integration v1.md`

Each story carries the two header lines of Template and Rules §R8.1, the 20 metadata rows of §R7.1 in the fixed order with the values of its WP story line, the 19 section headings of §R7.2 in order, the nine sub-tables 12.1–12.9 with the §R7.2 s16 Level column in §16, an origin tag on every Scenario line, the release `30 November 2026 (tentative)`, and a D-RCV-60 change-log row with the tool line. No suite provides a REST operation, publishes an event or owns a table, so 12.1, 12.3 and 12.7 are `None` in every story except the E1069 12.7 owner table, which lists the objects the boundary reads and their owners without owning any.

## Fragments written (5)

- `_work/msr/fragments/RWB-ITG-E1065-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1066-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1067-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1069-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1070-ITG.json`

Every fragment has the 28 keys of the WP: id, epic, service, wt, lane, ready, owner, business_epic, wave, release, legacy, disposition, H, C, I, X, acs, tcs, reqs, ops_provided, ops_consumed, events_published, events_consumed, workflows, prd_ref, gaps, assumptions, file. Each `acs` entry carries the Scenario line exactly as written in its story, and each `tcs` id appears in the story §16 table.

## Candidate registers

- `_work/msr/gaps/B-ITG-W1-09.jsonl` — 5 rows, one combined gap row per story: GAP-0374 (per-schema seed volumes, seeding order and the cutover from one recovery schema to 19 schemas), GAP-0375 (interaction write wire shape, Idempotency-Key rule and the P3/P1 compensation), GAP-0376 (event-to-ledger map, cross-topic order, duplicate key, consumer registration and dead-letter incident), GAP-0377 (19 service logins, grant matrix on the 30 views and the two halves of BND-6) and GAP-0378 (worker registration, per-service certificate and cross-service call evidence). Count: CG = 5.
- `_work/msr/assumptions/B-ITG-W1-09.jsonl` — 10 rows, one per default: E1065 one, E1066 two, E1067 three, E1069 one, E1070 three. Count: ASM = 10.

The rows use the §R9 key sets, confidence Medium where a default is read, and every citation in the twelve artefacts resolves to a row in these two files.

## Coverage

| Story | Legacy | ACs | TCs | I dependencies |
|---|---|---|---|---|
| RWB-ITG-E1065-ITG | RWB-E1-065 | 6, all new | 16 (10 legacy copies + 6 new) | 5 |
| RWB-ITG-E1066-ITG | RWB-E1-066 | 7: AC1, AC2, AC3, AC4 and AC8 legacy verbatim, AC9 and AC10 new | 7 (5 legacy copies + 2 new) | 3 |
| RWB-ITG-E1067-ITG | RWB-E1-067 | 7: AC1, AC3 and AC5 legacy verbatim, AC6 to AC9 new | 7 (3 legacy copies + 4 new) | 3 |
| RWB-ITG-E1069-ITG | RWB-E1-069 | 6, all new | 14 (8 legacy copies + 6 new) | 2 |
| RWB-ITG-E1070-ITG | RWB-E1-070 | 7, all new | 7 (7 legacy copies) | 2 |

- Legacy ACs owned by this WP are copied verbatim in substance with the origin tag at the end of the Scenario line; only the monolith operation, schema and owner names are adapted to the target (`POST /api/recovery/source-data/v1/cases/{caseId}/interactions` for the P3 monolith path, `rwb_source_data` for `recovery`, the owning topic for the one outbox). No Given, When or Then line loses a value.
- E1065, E1069 and E1070 have `"acs": []` in the plan, so every acceptance criterion in those three suites is new and tests only the deliverable in the title. The legacy ACs stay with the sibling APP stories, and §18 says so.
- Test cases keep the legacy ids of the ACs each suite covers, with the `-ITG` suffix; new ids are added only where a new integration criterion has no legacy counterpart. Levels use the §R7.2 s16 vocabulary only (Integration, NFR, Contract, End to end).
- Business values are copied from the legacy stories and the extracts, never invented: `rwb_sandbox`, seed 20261128, 1,226 Mortgage / 1,296 Hire purchase / 290 SSME / 2,812 cases, 10 per exception shape, 122 objects, 1,366 fields, 30 views, 304 view fields, 54 roles, commit a1b2c3d and e4f5a6b, `RW-2026-000001` with 1,845,200.00, days past due 89 and 90, `ACC0000017` with delay_days 95, `P0000123`, `RW-2026-000201` with 6 entries and case_seq 7, 25,000.00 for 2026-12-15, `R-UNI-18` version 2026.11, `RW-2026-000301` with 6 events, `EV-02-RW-2026-000301-20261201`, hit count 1, `DOC-SYN-3011`, `DLE-SYN-3012`, `SLA-ASSIGNED`, `platform-smoke-20261116`, `rwb-recovery` with 720 hours / 30 days and the four Keyword search attributes.
- Patterns: E1065 DP01, DP03, DP04, DP05, DP07, DP13, DP15, DP19; E1066 DP01, DP03, DP05, DP07, DP09, DP11, DP13, DP15, DP18, DP19; E1067 DP01, DP03, DP07, DP09, DP11, DP15, DP18, DP19; E1069 DP01, DP02, DP03, DP05, DP06, DP07, DP08, DP11, DP15, DP19; E1070 DP01, DP02, DP04, DP05, DP06, DP07, DP13, DP14, DP15, DP19. Every pattern has its §R5.5 row in §13 with the dependency added and where it sits; the H, C, I and X lists stay exactly as the plan sets them (no H, no C, no X, and the I list on the metadata row).
- Owners come from the Ownership Map only: P1 rwb-source-data for the interaction ledger, both interaction operations, the 30 ACE views, the four extension tables and the data dictionary; P3 rwb-case for case, timeline, tasks, parameters and reference data; P4 rwb-access for roles, scope, DoA and the authorise check; P5 rwb-document for documents; P7 rwb-decision for the central ledger, the decision-log query and the rule registry; PLT for the Temporal platform and the outbox/inbox library.
- Service naming follows §R4: `/api/recovery/source-data/v1`, `/api/recovery/case/v1`, `/api/recovery/access/v1`, `/api/recovery/document/v1`, `/api/recovery/decision/v1`, `/api/recovery/integration/v1`; topics `rwb.case.events.v1`, `rwb.document.events.v1`, `rwb.source-data.events.v1` and the shared `rwb.decision-record.v1`; queues `rwb-source-data`, `rwb-case`, `rwb-decision`; schemas `rwb_source_data`, `rwb_case`, `rwb_access`, `rwb_document`, `rwb_decision`.
- No person name, no email address and no issue-tracker reference appears in any of the twelve artefacts; no legacy master file was changed; no web, git or external system call was made.
- The five ITG stories have no build dependency and no contract dependency: they are Day 1, hold only the I list of their plan line and wait on no build of their own.
- Five story paths and five fragment paths already held drafts from an earlier partial pass of this same WP. Because `_work/msr/plan/split_plan.json` fixes these exact `file` paths, the slices were written in place at those paths instead of a new version, and the earlier JSONL rows were kept and completed rather than duplicated.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W1-09 --quick` — C02, C03, C05, C12, C13, C18 all PASS.
- Additional checks run directly on the twelve WP artefacts through the checker functions: C02 (metadata rows), C03 (19 sections), C05 (origin tags), C12 (no person name or email), C13 (no issue tracker), C15 (release 30 November 2026 marked tentative), C16 (service names in topics, bases and queues; no monolith base), C17 (every cited CG/ASM id has a register row) and C20 (tool line) all PASS.
- C06, C07 and C10 are fragment-level checks over all 1034 plan slices; this WP adds no H and no C, its I lists sit only on ITG stories, and each of the five legacy keys keeps its AC ownership either in this suite or in the sibling APP stories named in §18.
- This edit log itself:

- `_work/msr/editlog/B-ITG-W1-09.md`
