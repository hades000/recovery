# Edit log B-PLT-TPL-03 — RWB-PLT-TPL, legacy RWB-TE-008, RWB-TE-011 and RWB-TE-012

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Decision D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## What was done

Four legacy keys sit in this work package; three are story slices of the `platform` row under epic
RWB-PLT-TPL and each was written by its own fanout worker (one task subagent per legacy key, three at
once), then consolidated here.

| Legacy key | Story | Work type | Disposition | ACs owned | Test cases |
|---|---|---|---|---|---|
| RWB-TE-008 | RWB-PLT-TE008-APP Decision log hash chain check | APP | Split (rework) | AC1-AC8 legacy, AC9 new | TC-TE-008-01 to TC-TE-008-09, TC-PLT-TE008-APP-10 |
| RWB-TE-011 | RWB-PLT-TE011-APP PDPA lint for code, tests and logs | APP | Split (rework) | AC1-AC10 legacy, AC11 new | TC-TE-011-01 to TC-TE-011-11, TC-PLT-TE011-APP-12 |
| RWB-TE-012 | RWB-PLT-TE012-APP Document storage containers | APP | Moved (no impact) | AC1-AC12 legacy, AC13 new | TC-TE-012-01 to TC-TE-012-13, TC-PLT-TE012-APP-14 |

All three stories keep the legacy sections word for word where the disposition requires it, add one
`(new, D-RCV-60)` criterion each for the part of the target that no legacy criterion can test, re-point
the legacy text to the per-service shape (schema per service, contract with a fake, Temporal Schedule
instead of Quartz, per-service base path, gateway-bff route), and carry no value that a source does not
state. No legacy master file was edited, and no file outside "Write only" was touched.

## Files written

- 04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-TPL Service template and repositories/RWB PLT TE008 APP Decision log hash chain check v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-TPL Service template and repositories/RWB PLT TE011 APP PDPA lint for code, tests and logs v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-TPL Service template and repositories/RWB PLT TE012 APP Document storage containers v1.md
- _work/msr/fragments/RWB-PLT-TE008-APP.json
- _work/msr/fragments/RWB-PLT-TE011-APP.json
- _work/msr/fragments/RWB-PLT-TE012-APP.json
- _work/msr/gaps/B-PLT-TPL-03.jsonl
- _work/msr/assumptions/B-PLT-TPL-03.jsonl
- _work/msr/editlog/B-PLT-TPL-03.md

## Counts

- Candidate gap rows: 3 in `_work/msr/gaps/B-PLT-TPL-03.jsonl` (one combined row per story: GAP-1437, GAP-1436, GAP-1438). Numbering stays with step D1.
- Candidate assumption rows: 9 in `_work/msr/assumptions/B-PLT-TPL-03.jsonl` (three per story: ASM-2528..3, ASM-2525..3, ASM-2531..3). Numbering stays with step D1.

## Decisions and defaults applied

| # | Decision | Where |
|---|---|---|
| 1 | The three stories are written against the `platform` row, which is not one of the 19 service rows: no REST base, no topic, no task queue and no schema is invented for it (Template and Rules §R4) | sections 12.1 and 12.7 of all three stories |
| 2 | RWB-TE-008 becomes a template capability: one Schedule template in the workflow kit plus a chain-check library in the service template, applied to each service's own local `rwb_<name>` chain, with one instance for the central ledger in rwb-decision (Ownership Map JOB-14, owner P7, 02:00) | RWB-PLT-TE008-APP sections 1, 12.5, 12.6, 13 |
| 3 | DP-17 retires the decision log copy (RWB-E1-014, JOB-13), so the legacy AC6 wait is exercised against the business date's ledger ingest completeness (ASM-2529) | RWB-PLT-TE008-APP section 7 note, sections 4 and 9 |
| 4 | RWB-TE-011 becomes one generated pipeline step for all 19 repositories, generated from one pinned dictionary version read through the reference-data contract of rwb-case; the approver of an allow-list change is the code-owner role read through the authorise contract of rwb-access | RWB-PLT-TE011-APP sections 2, 4, 12.2, 13 |
| 5 | RWB-TE-012 keeps its business behaviour and its blueprint: one storage account and four containers per environment, reached only by rwb-document's identity; the retention run is a Temporal Schedule on task queue rwb-document (JOB-17); the legacy upload path is re-pointed to the per-service base path | RWB-PLT-TE012-APP sections 4, 7 note, 12.5, 12.6 |
| 6 | Every legacy value is kept character for character: parameters 02:00, 04:00 and 1,000; 48,210 entries, chain_seq 30,005, 12,001 and 40,350, 48,247; the six PDPA rule ids and every fixture value; the four container names, 3,650 days, 30 days, the 10 s timeout, the four identities and the three storage error strings; all message ids | sections 7 and 16 of each story |
| 7 | No breach of the standing rules: no person name, no email address, no issue-tracker reference, no monolith base path outside a quoted legacy line, no write outside "Write only", no edit of an existing file | whole work package |

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-PLT-TPL-03 --quick` — all six checks pass
(C02, C03, C05, C12, C13, C18). No failure was left open.

## Notes for the assembler (stage C)

- The three fragments carry `scope PLT`, `service platform`, `wave 0`, `business epic EP01-TE` and
  `release 30 November 2026`, copied from the plan; the release date is tentative.
- `RWB-ITG-TE008-ITG` is the integration copy of RWB-TE-008 and is not written here; the story names it in
  sections 18 and 19 only.
- RWB-TE-011 and RWB-TE-012 have no integration copy in the plan.
- Nothing in this work package opens a later lifecycle stage.
