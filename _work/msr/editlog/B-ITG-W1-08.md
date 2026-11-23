# Edit log B-ITG-W1-08 — RWB-ITG-W1 (legacy RWB-E1-059, RWB-E1-060, RWB-E1-062, RWB-E1-063, RWB-E1-064)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60
Date: 22 November 2026
Work package: B-ITG-W1-08 (RWB-ITG-W1 Wave 1 integration)
Fanout: 5 subagents (aisdlc-msr-worker), one per legacy key, dispatched in one message. One subagent (RWB-E1-063) dropped its connection before writing and was re-dispatched; both E1063 files are from the retry. Each agent wrote only its own story and fragment. The five gap rows and the twenty-nine assumption rows were written once by the parent before the fanout, so every agent cited rows that already existed and no two agents wrote the same JSONL file.

## Story files written (5)

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1059 ITG Case intake agent in shadow [E1b] - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1060 ITG Extraction evaluation [E1c] - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1062 ITG Deviation screening agent in shadow [E2b] - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1063 ITG Agent monitoring dashboard v1 [E2c] - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1064 ITG Data dictionary for the 14 data products - integration v1.md`

Each story carries the two header lines of Template and Rules §R8.1, the 20 metadata rows of §R7.1 in the fixed order with the values of its WP story line, the 19 section headings of §R7.2 in order, the nine sub-tables 12.1–12.9, the §R7.2 s16 Level column, an origin tag on every Scenario line, the release marked `(tentative)` and a D-RCV-60 change-log row with the tool line. No suite provides a REST operation, publishes an event or owns a table, so 12.1, 12.3 and 12.7 are `None` in every story.

## Fragments written (5)

- `_work/msr/fragments/RWB-ITG-E1059-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1060-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1062-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1063-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1064-ITG.json`

Each fragment has the 28 keys of the WP in order: id, epic, service, wt, lane, ready, owner, business_epic, wave, release, legacy, disposition, H, C, I, X, acs, tcs, reqs, ops_provided, ops_consumed, events_published, events_consumed, workflows, prd_ref, gaps, assumptions, file. Every `acs` entry carries the Scenario line exactly as written in the story, every `tcs` id appears in the story §16 table, the H/C/I/X lists equal the plan line, and the `file` value equals the plan path.

## Candidate registers

- `_work/msr/gaps/B-ITG-W1-08.jsonl`
- `_work/msr/assumptions/B-ITG-W1-08.jsonl`

Counts: CG = 5 (one combined row per story: GAP-0369, -E1060-1, -E1062-1, -E1063-1, -E1064-1); ASM = 29 (E1059 six, E1060 five, E1062 six, E1063 six, E1064 six).

## Coverage

| Story | Legacy | ACs | TCs | I dependencies |
|---|---|---|---|---|
| RWB-ITG-E1059-ITG | RWB-E1-059 | 14: AC5 legacy verbatim, 13 new | 14 (9 legacy copies + 5 new) | 2 |
| RWB-ITG-E1060-ITG | RWB-E1-060 | 14, all new | 14 (9 legacy copies + 5 new) | 2 |
| RWB-ITG-E1062-ITG | RWB-E1-062 | 15, all new | 15 (10 legacy copies + 5 new) | 4 |
| RWB-ITG-E1063-ITG | RWB-E1-063 | 13, all new | 13 (8 legacy copies + 5 new) | 4 |
| RWB-ITG-E1064-ITG | RWB-E1-064 | 13, all new | 13 (9 legacy copies + 4 new) | 2 |

- Legacy ACs owned by this WP are copied word for word with only the origin tag added at the end of the Scenario line: RWB-E1-059 AC5. A line-by-line comparison against the legacy story found no difference in the Given, When or Then lines. E1060, E1062, E1063 and E1064 have `"acs": []` in the plan, so every acceptance criterion in those four suites is new and tests only the deliverable in the title; the legacy ACs stay with the sibling APP stories.
- Test cases keep the legacy ids of the criteria each suite covers, with the `-ITG` suffix. New ids are added only where a new integration criterion has no legacy counterpart: TC-ITG-E1059-ITG-10 to -14, TC-ITG-E1060-ITG-10 to -14, TC-ITG-E1062-ITG-11 to -15, TC-ITG-E1063-ITG-09 to -13 and TC-ITG-E1064-ITG-10 to -13. Levels use the §R7.2 s16 vocabulary only.
- Every business value is copied from its legacy story and none is invented. E1059: INTAKE, P1, SHADOW, 60 s, floor 0.80, PR1, intake-summary-v1, the four gap types, INTAKE-S1 v1 and v2, INTAKE-S3, RW-2026-000301/302/303, 2026-11-30 to 2026-12-04, data_as_of 2026-11-28, 200 cases, 182 agreeing, 0.9100, TIMED_OUT 1. E1060: EXTRACT, P1, PR1, extract-fields-v1, OCR_TEMPLATE/MODEL/OCR_AND_MODEL, EXTRACT-S1 v1, 40 COURT_NOTICE, court_name/case_number/hearing_date, 0.95, 30, 34/2/4, 0.9444/0.8947, 0.9310, TITLE_DEED 12, 0.91, document 7 of 40. E1062: SCREENING, P1, SHADOW, 60 s, 0.80, PR1, screening-v1, X1–X7, SCREEN-S1 v1, 200 cases, X6 18/2/6, 0.9000/0.7500, RW-2026-000401/402/403/404, D-1001, DEATH_CERTIFICATE, RW-FRAUD, RW-TEAMMGR, R-DEV-04, R-DEV-02 to -06, 0.72, X9, 30-day look-back, 180-day ledger window. E1063: INTAKE and SCREENING, P1, PR1, 2026-12-01, 120/9/1,840.0000, 150/21/2,310.5000, cap 2,000, RW-COE, 0.0750, COST_CAP, EXTRACT no runs, 2026-12-02 2,000.0000, 2026-11-30, JOB-15 01:30. E1064: 122/1,366, 92/1,062/49, 30/304/177/127, 297 of 304, 7 derived fields, ACC0000017, 95, DF-ACE-018/-020/-204, DC-ACE, DC-ACE-2, V0002/V0003, 2026-11-12/18, DOC-SYN-0640, CHK-01, DF-EXT-001 to -049.
- Patterns: E1059 DP01, DP03, DP05, DP06, DP07, DP09, DP11, DP13, DP15, DP19, DP20; E1060 DP01, DP06, DP07, DP13, DP15, DP19; E1062 DP01, DP04, DP06, DP07, DP09, DP13, DP15, DP18, DP19, DP20; E1063 DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP17, DP19; E1064 DP01, DP05, DP07, DP11, DP13, DP15, DP19. Every pattern has its §R5.5 row in §13 with the dependency added and where it sits; the H, C, I and X lists stay exactly as the plan sets them (no H, no C, no X, and the I list on the metadata row).
- Owners come from the Ownership Map only: P10 rwb-agent for agent policies, prompts, runs, samples, evaluations, metrics and AgentRunWorkflow; P3 rwb-case for case, timeline, accounts, parties, parameters and reference data; P5 rwb-document for document, fields and content; P1 rwb-source-data for data products, freshness, valuations, interaction ledger and admin jobs; P4 rwb-access for roles, session, masking and authorise; P7 rwb-decision for the rule registry and the central ledger; S8 rwb-deviation for deviations; P6 rwb-comms for notices and notifications; P9 rwb-reporting for measures; P2 rwb-integration for outbound items and files.
- Service naming follows §R4: `/api/recovery/agent/v1`, `/api/recovery/case/v1`, `/api/recovery/document/v1`, `/api/recovery/source-data/v1`, `/api/recovery/access/v1`, `/api/recovery/decision/v1`, `/api/recovery/deviation/v1`, `/api/recovery/comms/v1`, `/api/recovery/reporting/v1`, `/api/recovery/integration/v1`; topics `rwb.agent.events.v1`, `rwb.case.events.v1`, `rwb.document.events.v1`, `rwb.deviation.events.v1` and the shared `rwb.decision-record.v1`; queues `rwb-agent`, `rwb-case`, `rwb-document`, `rwb-source-data`, `rwb-decision`; schemas `rwb_agent`, `rwb_case`, `rwb_document`, `rwb_source_data`, `rwb_decision`.
- E1063 is the one story that records a removed capability rather than a moved one: the data lake, agent_run_daily, INT-19 and INT-20 are gone (DP-17), the daily measures are a P9 read model from events, JOB-15 is an Airflow trigger and its run record and rerun are read through P1 (GAP-0372; ASM-…-E1063-1 to -6).
- E1064 records the one conflict the load path creates: the reference-load operations are P3 in the Ownership Map while sys_fields stays with P1, so the suite drives the load through P3 and reads the result through P1 (GAP-0373; ASM-…-E1064-1).
- The monolith base never appears in any story or fragment. No story provides a REST operation, publishes an event or owns a table. No person name, no email address and no issue-tracker reference appears in any file; no legacy master file was changed; no web, git or external system call was made.
- The five ITG stories have no build dependency and no contract dependency: they are Day 1, hold only the I list of their plan line and wait on no build of their own.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W1-08 --quick` — C02, C03, C05, C12, C13, C18 all PASS.
- Additional checks run directly on the 13 WP artefacts: C06 (H and I classes), C14 (header), C15 (release 30 November 2026 marked tentative), C16 (service names in topics, bases and queues; no old monolith base), C17 (every cited CG/ASM id has a register row) and C20 (tool line) all PASS.
- After the first pass, three content corrections were made inside the WP's own outputs: the count sentence in E1059 §12.2, the gap citation in E1060 §18, and four right references in E1062 that said Platform administration instead of Rules and parameters. The quick check was rerun green after them.
- C19 was not run with the quick set; it reports the planned outputs of later WPs and the edit log of this WP, which is written after this line.
- This edit log itself:

- `_work/msr/editlog/B-ITG-W1-08.md`
