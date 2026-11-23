# Edit log B-ITG-W3-01 — RWB-ITG-W3: legacy RWB-E4-001, RWB-E4-002, RWB-E4-045, RWB-E4-046, RWB-E4-047

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Decision: D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## Run

- Agent: aisdlc-msr-worker, fanout 5 (one task subagent per legacy key: RWB-E4-001, RWB-E4-002, RWB-E4-045, RWB-E4-046, RWB-E4-047; the WP allows 5). No merge — each subagent wrote its own story, fragment and jsonl rows.
- Source of the metadata values: the story line of each key in `_work/msr/wp/B-ITG-W3-01.md`, copied character for character.
- Legacy keys read: `04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md`, headings RWB-E4-001, RWB-E4-002, RWB-E4-045, RWB-E4-046 and RWB-E4-047. Only AC1 of each key is copied verbatim with its origin tag; AC2 stays with the app story of the key and is named as out of scope.
- Each AC1 sits in a gherkin block under a Background that carries only the harness facts the sources give (the fakes of section 12.8, the seeded case, and for RWB-E4-001 and RWB-E4-002 the 12-month appraisal limit from Temporal and Drools slide 17). The Scenario line and its Given/When/Then lines are the legacy text unchanged, with the origin tag appended.
- Release dates copied unchanged and marked "(tentative)": 28 February 2027 for all five keys.
- Patterns applied are exactly those the WP names: DP03, DP05, DP13, DP19 for RWB-E4-001 and RWB-E4-002; DP03, DP05, DP19 for RWB-E4-045, RWB-E4-046 and RWB-E4-047. Each has its section 13 row from the §R5.5 table. The platform H dependencies named by the DP table are not repeated in the metadata H row, which stays None.
- Section 12 of every story follows §R7.2: tables 12.1 to 12.9, "None" where empty, every owner and path taken from the Ownership Map or from the Architecture v5 contract slides. No `/api/recovery/v1/` base appears outside the DP-13 marker row, and no monolith base appears anywhere.
- Post-fanout corrections: the AC2 duplicate-order assumptions in RWB-ITG-E4001-ITG and RWB-ITG-E4046-ITG were replaced with the idempotency rule of Architecture v5 slide 11; the RWB-ITG-E4002-ITG acceptance write was reworded to the open P1/S1 writer of `valuation_ext` (`ownership.json` ruling ASM-0081; FSD P1 OQ-P1-05); RWB-ITG-E4045-ITG gained the rwb-case read it needs for its own data row; RWB-ITG-E4047-ITG gained the rwb-debtsale and rwb-writeoff operations that drive its sale and write-off routes, dropped the unused treatment row, and now states that the write-off route runs on the S7 fake in wave 3; both jsonl files were rewritten without a BOM and ordered by key.

## Files written

- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W3 Wave 3 integration/RWB ITG E4001 ITG Order an appraisal when the last one is stale - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W3 Wave 3 integration/RWB ITG E4002 ITG Receive the appraisal value from SVAF - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W3 Wave 3 integration/RWB ITG E4045 ITG Calculate fees and charges - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W3 Wave 3 integration/RWB ITG E4046 ITG Post a settlement booking to ALS - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W3 Wave 3 integration/RWB ITG E4047 ITG Post to the general ledger - integration v1.md
- _work/msr/fragments/RWB-ITG-E4001-ITG.json
- _work/msr/fragments/RWB-ITG-E4002-ITG.json
- _work/msr/fragments/RWB-ITG-E4045-ITG.json
- _work/msr/fragments/RWB-ITG-E4046-ITG.json
- _work/msr/fragments/RWB-ITG-E4047-ITG.json
- _work/msr/gaps/B-ITG-W3-01.jsonl
- _work/msr/assumptions/B-ITG-W3-01.jsonl
- _work/msr/editlog/B-ITG-W3-01.md

| Story | File | ACs owned | TCs | I dependencies |
|---|---|---|---|---|
| RWB-ITG-E4001-ITG | RWB ITG E4001 ITG Order an appraisal when the last one is stale - integration v1.md | AC1 (legacy RWB-E4-001) | TC-E4-001-01-ITG to TC-E4-001-04-ITG | RWB-S1-E4001-APP |
| RWB-ITG-E4002-ITG | RWB ITG E4002 ITG Receive the appraisal value from SVAF - integration v1.md | AC1 (legacy RWB-E4-002) | TC-E4-002-01-ITG to TC-E4-002-04-ITG | RWB-S1-E4002-APP |
| RWB-ITG-E4045-ITG | RWB ITG E4045 ITG Calculate fees and charges - integration v1.md | AC1 (legacy RWB-E4-045) | TC-E4-045-01-ITG to TC-E4-045-04-ITG | RWB-P8-E4045-APP |
| RWB-ITG-E4046-ITG | RWB ITG E4046 ITG Post a settlement booking to ALS - integration v1.md | AC1 (legacy RWB-E4-046) | TC-E4-046-01-ITG to TC-E4-046-04-ITG | RWB-P8-E4046-APP, RWB-P2-E4046-APP |
| RWB-ITG-E4047-ITG | RWB ITG E4047 ITG Post to the general ledger - integration v1.md | AC1 (legacy RWB-E4-047) | TC-E4-047-01-ITG to TC-E4-047-04-ITG | RWB-P8-E4047-APP |

## Gap and assumption rows

- Gap rows written to `_work/msr/gaps/B-ITG-W3-01.jsonl`: 5 (one combined row per story).
  - GAP-0429 — SVAF order interface, data product code, staleness parameter name and the wave 3 harness pack (Missing, P2, wave 3).
  - GAP-0430 — data product code, the internal acceptance write and its writer, the multi-appraisal choice and the wave 3 harness pack (Missing, P2, wave 3).
  - GAP-0431 — fee tables and their owner, the fee operation and fields in rwb-payment, the court fee and charge schedules, the data product code and the wave 3 harness pack (Missing, P2, wave 3).
  - GAP-0432 — ALS interface, the booking operation in rwb-payment, the data product code, the `outbound_item` field IDs and the wave 3 harness pack (Missing, P2, wave 3).
  - GAP-0433 — general ledger interface, the entry set per route, the posting reference, the data product code, the month-end close window, the Finance provision feed and the wave 3 harness pack (Missing, P2, wave 3).
- Assumption rows written to `_work/msr/assumptions/B-ITG-W3-01.jsonl`: 5 (one per story, confidence Medium, confirming role named in the row).
  - ASM-0605, ASM-0606, ASM-0607, ASM-0608, ASM-0609.
- Counts: CG 5, ASM 5. No gap row numbers a GAP-nnnn and no assumption row numbers an ASM-nnnn; numbering is left to step D1.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W3-01 --quick`

| Check | Result | Findings |
|---|---|---|
| C02 metadata rows | PASS | 0 |
| C03 19 sections | PASS | 0 |
| C05 AC origin tags | PASS | 0 |
| C12 person names and emails | PASS | 0 |
| C13 issue tracker | PASS | 0 |
| C18 write-only and legacy hashes | PASS | 0 |

Also run on the same file set: C14 header lines PASS, C15 release and tentative PASS, C16 service names and API base PASS, C17 gap and assumption citations PASS, C20 tool line PASS. No file outside the WP "Write only" list was written, and no existing file was edited.
