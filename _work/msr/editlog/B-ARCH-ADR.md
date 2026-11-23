# Edit log B-ARCH-ADR — ADR v-next with ADR-013..023

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 microservice realignment. Date: 22 November 2026.
Source: `05 Technical architecture/Recovery Workbench Architecture Decision Records v3.md` (read only, not edited).

## Files written

- `05 Technical architecture/Recovery Workbench Architecture Decision Records v4.md`
- `_work/msr/gaps/B-ARCH-ADR.jsonl`
- `_work/msr/assumptions/B-ARCH-ADR.jsonl`
- `_work/msr/editlog/B-ARCH-ADR.md`

## What changed

- Header per Template and Rules §R8.1, document control with the change-log row `v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`.
- ADR-001, ADR-003 to ADR-008 and ADR-010 are copied word for word with their IDs, numbers and dates.
- ADR-002 gains the supersession note and the status `Superseded by ADR-013`; ADR-009 gains the supersession note and the status `Superseded by ADR-022`; ADR-011 and ADR-012 keep `Accepted` and gain an amendment note naming ADR-016 and ADR-017. The body of every existing ADR is unchanged.
- ADR-013 to ADR-023 are new, in the IDs allocated in `_work/msr/plan/ids.json`, in the same section format as the source: Status, Date, Deciders, Decision log, Context and problem, Decision drivers, Options considered, Decision, Consequences.
- Owners are taken from the Ownership Map and Architecture v5: rwb-source-data P1, rwb-integration P2, rwb-case P3, rwb-access P4, rwb-document P5, rwb-comms P6, rwb-decision P7, rwb-payment P8, rwb-reporting P9, rwb-agent P10, rwb-valuation S1, rwb-treatment S2, rwb-guarantee S3, rwb-litigation S4, rwb-asset S5, rwb-debtsale S6, rwb-writeoff S7, rwb-deviation S8, rwb-partner S9, and PLT for the shared platform and the workflow kit.
- No release date appears in the source ADR set, so no `(tentative)` marker was needed. Every decision date is copied unchanged.
- No new version of any .docx, .xlsx or .pptx was needed: this family is `.md` only.

## Counts

- Gap rows: 4 candidate rows in `_work/msr/gaps/B-ARCH-ADR.jsonl` (GAP-0090 to 4). Numbered GAP-nnnn in step D1.
- Assumption rows: 6 candidate rows in `_work/msr/assumptions/B-ARCH-ADR.jsonl` (ASM-0152 to 6). Numbered ASM-nnnn in step D1.
- Placeholders in the document: 2, both paired with a gap row and an assumption row (GAP-0090 with ASM-0152; GAP-0093 with ASM-0155).

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ARCH-ADR --quick` — see the report under `22 Microservice Realignment/checks/reports/wp-B-ARCH-ADR-*.md`.

## Notes

- ADR-017 records the amendment to D-RCV-36 T1 and T2 by reference, because the Temporal and Drools Change Register v1 text is not in the read set for this work package (GAP-0090).
- The Temporal release position is a three-way conflict (1.28.1, 1.29.7, 1.30+) and is recorded as GAP-0091; ADR-016 states 1.30 or later on the pinned release SCB IT approves at build.
- The Kafka host is still an open architecture decision (GAP-0092); ADR-015 therefore carries the status Proposed and keeps the outbox and the Event Hubs fallback.
- No person name appears in any file written by this work package.
