# Edit log — WP C-BN1 (Build Notes Epic 1, next version)

Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Agent: aisdlc-msr-worker. WP file: `_work/msr/wp/C-BN1.md`. Fanout: 0 (no subagents).

## Files written

| File | What it is |
|---|---|
| `04 User stories/Recovery Workbench Build Notes Epic 1 v7.md` | The next version of the Epic 1 build notes; the only deliverable outside the scratch area |
| `_work/msr/gaps/C-BN1.jsonl` | 21 candidate gap rows, GAP-3154 to GAP-3174 |
| `_work/msr/assumptions/C-BN1.jsonl` | 23 candidate assumption rows, ASM-5544 to ASM-5566 |
| `_work/msr/editlog/C-BN1.md` | This edit log |
| `_work/msr/docs/C-BN1/` | Scratch: the source extract of the Service Story Catalog v1 (298 Epic 1 story rows and their dependencies), the generator, the row writer and the verification script |

The source `04 User stories/Recovery Workbench Build Notes Epic 1 v6.md` was read only and is unchanged.

## What changed in the document

- Header is the Template and Rules §R8.1 pair of lines, and the change-log row is
  v7, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash.
- All 72 source sections are reproduced byte for byte (checked programmatically), in source order, with every ID, number and date kept.
  Release dates added in the new tables carry "(tentative)".
- Each of the 72 sections gains a `**Service and lane.**` block (services, new story IDs with work type, lane and ready-to-start),
  a `**Tables and owner.**` block (Ownership Map v1 owner and schema for every table the source note names) and a
  `**Dependencies.**` block (patterns and the H, C, I and X dependencies of the new stories), then a `**What moves.**` paragraph.
- New shared sections: "Epic 1 and the 19 services", "What D-RCV-60 retires, preserves and keeps in Epic 1", and
  "The 72 story notes, by legacy key" (one row per source note: disposition, primary, new stories, lanes, ready-to-start).
- "The 30 views and their sources" gains a "Read by (D-RCV-60)" column: P1 `rwb_source_data` only, per DP-05.
- "The grants" keeps the source table, adds the D-RCV-60 ruling (one login per service, DP-02; `recovery_svc` retired at cutover)
  and a per-service schema and privilege table for the 19 services.
- "Freshness" keeps the 14-product table, adds an owning-service column with the §R9 placeholder, and states that P1 publishes
  `GET /freshness`, `AceDataReady` and `AceDataLate` and no other service names `v_ace_batch_status`.
- "The boundary" keeps the four source bullets and adds the per-service reading of BND-6 (ADR-014, ADR-020).

## Gaps and assumptions

- Gap rows written: 21 (GAP-3154 to GAP-3174).
- Assumption rows written: 23 (ASM-5544 to ASM-5566).
- Every gap has a matching assumption with the same number (CG-BN1-n / ASM-BN1-n). ASM-5565 and ASM-5566 are general
  (Epic 1 platform stories in wave 0 lanes; the notes released as Draft).
- Every CG and ASM citation in the document resolves to a row in the two jsonl files (checked programmatically).

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp C-BN1 --quick`

| Check | Result |
|---|---|
| C02 | PASS |
| C03 | PASS |
| C05 | PASS |
| C12 | PASS |
| C13 | PASS |
| C18 | PASS |

## Notes and risks

- The Service Story Catalog v1 (read only) supplies the new story IDs, work types, lanes and ready-to-start values; the split plan
  supplies the disposition, primary service and patterns; the Ownership Map v1 supplies every table owner. No value was invented.
- Where a value is missing it is written as the §R9 placeholder or named as "not fixed in the source documents" with its CG and ASM.
- The largest open items for the assembler are the per-service login naming (GAP-3155), the data product owners (GAP-3154) and the
  rule registry location (GAP-3157).
- Two checks fail on other work packages and nothing in this one: C10 reports one legacy acceptance criterion not owned by any new
  story (`RWB-E1-056` AC9), which is a stage B fragment question, and C19 lists planned outputs whose work packages have not run yet.
  Both were left untouched; this WP writes no fragment and no other package's file.
