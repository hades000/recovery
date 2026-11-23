# Edit log B-ITG-W1-07 — RWB-ITG-W1 (legacy RWB-E1-052, RWB-E1-054, RWB-E1-055, RWB-E1-057, RWB-E1-058)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60
Date: 22 November 2026
Work package: B-ITG-W1-07 (RWB-ITG-W1 Wave 1 integration)
Fanout: 5 subagents (aisdlc-msr-worker), one per legacy key, dispatched in one message. Each wrote only its own story and fragment and cited the register rows written once by the parent before the fanout, so no two agents wrote the same JSONL file.

## Story files written (5)

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1052 ITG Notice generation v1 - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1054 ITG Review queue for low-confidence documents - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1055 ITG Proof of delivery capture design with WIN - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1057 ITG Intake from branches, mailroom, partner SFTP and email - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1058 ITG Agent platform set-up [E1a] - integration v1.md`

Each story carries the two header lines of Template and Rules §R8.1, the 20 metadata rows of §R7.1 in the fixed order with the values of its WP story line, the 19 section headings of §R7.2 in order, the nine sub-tables 12.1–12.9, the §R7.2 s16 Level column, an origin tag on every Scenario line, the release marked `(tentative)` and a D-RCV-60 change-log row with the tool line. No REST operation, event or table is provided by any of the five suites, so 12.1, 12.3 and 12.7 are `None` in every story.

## Fragments written (5)

- `_work/msr/fragments/RWB-ITG-E1052-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1054-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1055-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1057-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1058-ITG.json`

Each fragment has the 28 keys of the WP in order: id, epic, service, wt, lane, ready, owner, business_epic, wave, release, legacy, disposition, H, C, I, X, acs, tcs, reqs, ops_provided, ops_consumed, events_published, events_consumed, workflows, prd_ref, gaps, assumptions, file. Every `acs` entry carries the Scenario line exactly as written in the story, and every `tcs` id appears in the story §16 table.

## Candidate registers

- `_work/msr/gaps/B-ITG-W1-07.jsonl` — 5 rows, one combined gap row per story: GAP-0364 (notice path, merge snapshot home and stale-batch signal), GAP-0365 (review operation names, scope source and attach evidence), GAP-0366 (WIN file path, proof-of-delivery read and ledger home), GAP-0367 (partner eligibility, channel configuration and job monitor), GAP-0368 (model endpoint path, masking route and run evidence). Count: CG = 5.
- `_work/msr/assumptions/B-ITG-W1-07.jsonl` — 26 rows, one per default per story (E1052 five, E1054 four, E1055 five, E1057 six, E1058 six). Count: ASM = 26.

The register rows were written once by the parent before the fanout with a per-key id, so the five parallel subagents could cite them without a concurrent write to the same file.

## Coverage

| Story | Legacy | ACs | TCs | I dependencies |
|---|---|---|---|---|
| RWB-ITG-E1052-ITG | RWB-E1-052 | 12: AC7 legacy verbatim, 11 new | 14 (11 legacy copies + 3 new) | 7 |
| RWB-ITG-E1054-ITG | RWB-E1-054 | 16, all new | 20 (19 legacy copies + 1 new) | 5 |
| RWB-ITG-E1055-ITG | RWB-E1-055 | 13: AC1 and AC9 legacy verbatim, 11 new | 13 (12 legacy copies + 1 new) | 7 |
| RWB-ITG-E1057-ITG | RWB-E1-057 | 16: AC2, AC3, AC7, AC9 and AC13 legacy verbatim, 11 new | 18 (17 legacy copies + 1 new) | 2 |
| RWB-ITG-E1058-ITG | RWB-E1-058 | 18, all new | 19 (16 legacy copies + 3 new) | 3 |

- Legacy ACs owned by this WP are copied word for word with only the origin tag added at the end of the Scenario line: RWB-E1-052 AC7, RWB-E1-055 AC1 and AC9, RWB-E1-057 AC2, AC3, AC7, AC9 and AC13. A line-by-line comparison against the legacy stories found no difference in the Given, When or Then lines.
- E1054 and E1058 have `"acs": []` in the plan, so every acceptance criterion in those two suites is new and tests only the deliverable in the title. The legacy ACs stay with the sibling APP stories, and §18 names them.
- Test cases keep the legacy ids of the ACs each suite covers, with the `-ITG` suffix. Three new ids are added only where a new integration criterion has no legacy counterpart: TC-ITG-E1052-ITG-12/-13/-14, TC-ITG-E1054-ITG-20, TC-ITG-E1055-ITG-13, TC-ITG-E1057-ITG-18 and TC-ITG-E1058-ITG-17/-18/-19. Levels use the §R7.2 s16 vocabulary only.
- Every business value is copied from its legacy story and none is invented: DEMAND-MTG TH v2, RECALL-HP TH v1 Draft, RW-2026-000123, RW-2026-000456, P-0001, P-0999, 1,250,000.00, 2026-11-25/24/27/28/30, WIN-77001, RR123456789TH, POD-0001; IN-0101 to IN-0112, COURT_NOTICE 0.62, DEMAND_LETTER 0.21, DOC-0103, DOC-0109, DOC-0111, RW-2026-000201/202/203/150, `Por 2001/2569`, 2026-12-15/16; RC-2026-000123, N-0001, N-0002, CT-77001, WIN-POD-SAMPLE-v1, 26/27/28/30 November and 1 December 2026; BR-0123, LF-007, LF-008, LF-099, MBX-RECOVERY-01, scan-0001.pdf 1.2 MB, 09:12/09:15, 25.0/25.1 MB, H1, 30 November/2 December; ECHO, P1, PR1/PR2, MODEL-A-2026-10, 60 seconds, 0.80/0.79, 1,200 ms, 900/150 tokens, 0.0500/0.0525 baht, ECHO-S1/S2, 20 rows.
- Patterns: E1052 DP01, DP02, DP03, DP05, DP07, DP09, DP11, DP13, DP15, DP19; E1054 DP01, DP03, DP07, DP09, DP11, DP13, DP15, DP19; E1055 DP01, DP05, DP07, DP09, DP10, DP11, DP15, DP18, DP19; E1057 DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19; E1058 DP01, DP03, DP06, DP07, DP08, DP09, DP11, DP13, DP15, DP19, DP20. Every pattern has its §R5.5 row in §13 with the dependency added and where it sits; the H, C, I and X lists stay exactly as the plan sets them (no H, no C, no X, and the I list on the metadata row).
- Owners come from the Ownership Map only: P6 rwb-comms for notice, template, merge field, dispatch and proof of delivery; P5 rwb-document for document, generated document, review, intake item and field; P3 rwb-case for case, parties, tasks, timers and case status; P1 rwb-source-data for data products, freshness, interaction ledger, data-quality exceptions and the admin job view; P7 rwb-decision for the central ledger and the decision-log query; P4 rwb-access for roles, scope and session; P2 rwb-integration for outbound items and file delivery; S9 rwb-partner for partner and panel status; P10 rwb-agent for agent policies, runs, evaluations and the run workflow.
- Service naming follows §R4: `/api/recovery/comms/v1`, `/api/recovery/document/v1`, `/api/recovery/case/v1`, `/api/recovery/source-data/v1`, `/api/recovery/decision/v1`, `/api/recovery/access/v1`, `/api/recovery/integration/v1`, `/api/recovery/partner/v1`, `/api/recovery/agent/v1`; topics `rwb.comms.events.v1`, `rwb.document.events.v1`, `rwb.integration.events.v1`, `rwb.agent.events.v1` and the shared `rwb.decision-record.v1`; queues `rwb-comms`, `rwb-document`, `rwb-agent`; schemas `rwb_comms`, `rwb_document`, `rwb_agent`. `DecisionRecorded` is written on the shared topic `rwb.decision-record.v1`, never as a per-service event.
- The monolith base never appears outside a legacy marker, and a DP-13 row writes `/api/recovery/v1` with no trailing slash. No story provides a REST operation, publishes an event or owns a table.
- No person name, no email address and no issue-tracker reference appears in any file; no legacy master file was changed; no web, git or external system call was made.
- The five ITG stories have no build dependency and no contract dependency: they are Day 1, hold only the I list of their plan line and wait on no build of their own.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W1-07 --quick` — C02, C03, C05, C12, C13, C18 all PASS.
- Additional checks run directly on the 12 WP artefacts: C01 (baseline hashes unchanged), C12, C13, C14 (header), C15 (release 30 November 2026 marked tentative), C16 (service names in topics, bases and queues; no old monolith base), C17 (every cited CG/ASM id has a register row) and C20 (tool line) all PASS.
- C19 reports only planned outputs of later WPs; every B-ITG-W1-07 planned output is present after this log.
- C10 and C11 still report legacy ACs and test cases of the sibling APP stories not yet written (for example RWB-E1-054 AC17 and the component-level tests); the ITG copies in this WP keep their legacy prefixes so those findings clear when the APP stories land.
- This edit log itself:

- `_work/msr/editlog/B-ITG-W1-07.md`
