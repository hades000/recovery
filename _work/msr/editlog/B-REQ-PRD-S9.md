# Edit log B-REQ-PRD-S9 — PRD S9 rwb-partner v1

Tool line: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60. Agent: aisdlc-prd-builder. fanout: 0 (no subagent used).

## Files written

- 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md
- _work/msr/gaps/B-REQ-PRD-S9.jsonl
- _work/msr/assumptions/B-REQ-PRD-S9.jsonl
- _work/msr/editlog/B-REQ-PRD-S9.md

Scratch files, all inside the sanctioned scratch folder `_work/msr/docs/B-REQ-PRD-S9/`:

| File | What it is |
|---|---|
| `emit_registers.py` | Emits the two register files from one data structure, so every row is valid JSON and every citation resolves; it also normalises the section references to the final numbering |
| `patch_refs.py` | Used once to align the assumption `applied_in` references with the final functional-requirement numbering, then superseded by the normalisation in `emit_registers.py` |
| `consistency.py` | Counts the IDs, checks both directions of the coverage (every FR in an AC, every FR and NFR in the trace summary, every CAP in an FR) and scans for odd characters |
| `local_checks.py` | Runs the non-quick checks of `run_all.py` against this WP's outputs only |

## Register counts

| Register | File | Rows | IDs |
|---|---|---|---|
| Candidate gaps | _work/msr/gaps/B-REQ-PRD-S9.jsonl | 25 | GAP-1835 to GAP-1859 |
| Candidate assumptions | _work/msr/assumptions/B-REQ-PRD-S9.jsonl | 30 | ASM-3016 to ASM-3045 |

Gap severity split: P1 = 6 (GAP-1835, -2, -6, -9, -10, -11), P2 = 16, P3 = 3. Gap type split: Missing 12, Conflict 9, Ambiguous 3, Outdated 1. Gap wave split: wave 1 = 2, wave 2 = 4, wave 3 = 1, wave 4 = 18. Assumption confidence split: High 10, Medium 20. Every gap row carries its paired assumption in the `asm` column, and every assumption row names the gap it answers, except the five general rows (ASM-3038 to ASM-3042) that carry no gap.

## What the version does

1. Version 1 is the next version of this family: the PRD folder held no S9 file, so this is the first PRD of the family (ASM-3039). The document is new; no earlier S9 PRD exists to copy.
2. The document is the FSD S9 Partner management v3 baseline re-expressed as product behaviour, with every FSD requirement, feature, validation rule, business rule, message, list, screen, field and acceptance criterion ID carried character for character (ASM-3041).
3. Eighteen capabilities (CAP-S9-001 to CAP-S9-018), 43 functional requirements (FR-S9-001 to FR-S9-043), 26 non-functional requirements (NFR-S9-001 to NFR-S9-026), 30 acceptance criteria (AC-S9-001 to AC-S9-030), 8 journeys, 15 roles and 24 open questions.
4. Release slicing follows the waves and the ordering the split plan creates: wave 0 platform; the three earlier contract slices (wave 1 at 30 November 2026 (tentative), wave 2 at 31 December 2026 (tentative), wave 3 at 28 February 2027 and 31 March 2027 (tentative)); EP06 in wave 4 at 30 April 2027 (tentative); EP07 in wave 4 at 31 May 2027 (tentative); then the later increments with their unlock.
5. Status is Draft and the approval table is empty; the missing approval is ASM-3038 and the BRD is read as approved for this run.
6. BR coverage: BR-059, BR-060, BR-070 and BR-071 (4 of the 4 BRD requirements that name this service) each trace to at least one functional requirement, and all 43 functional requirements trace to one of them. REQ-S9-002 is carried by FR-S9-003 because no FSD feature serves it (GAP-1851), and FEAT-PRM-06 traces through BR-059 because it has no REQ-S9 row (GAP-1854).
7. The service is created in wave 4 while the split plan places four of its stories earlier and two wave-3 services call it, so three conflict gaps carry the ordering and section 10.2 answers it with contract-first delivery (GAP-1843, -10, -11).

## Checks

| Step | Command | Result |
|---|---|---|
| Quick gate for this WP | `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-REQ-PRD-S9 --quick` | C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS |
| Full set run against this WP's outputs | C01, C12, C13, C14, C15, C16, C17, C18, C20 through `local_checks.py` | PASS on every one of them |
| Register completeness | Every gap row carries the fifteen keys of the gap contract and every assumption row the ten keys of the assumption contract, checked in code | PASS |
| Citation resolution (C17) | Every CG and ASM cited in the PRD exists as a row in the two register files or in another WP's register | PASS |
| Trace consistency inside section 11.2 | each requirement row against the summary table, both directions | 0 inconsistencies: all 43 functional requirements appear in at least one acceptance criterion, all 43 appear in the summary, all 26 non-functional requirements appear in the summary, and every capability is carried by at least one functional requirement |
| Queue-level check C04 | not a gate for this WP | reports other WPs' planned story files that are still missing; nothing of this WP is named |

Corrections made during the run: a first pass of the register script wrote its two output files under a doubled relative path; the script root was corrected, both files were re-emitted to the intended paths, and the stray folder was removed. The register files named above are the corrected ones. Two citations were also reduced to their assumption where a row has no paired gap, the `applied_in` references were aligned with the final functional-requirement numbering after the requirement list was completed, and three acceptance criteria were reworded so that no test scenario states a business value the sources do not give.

No file was edited that already existed, no repository command was run, and no external system was called.

## Deferred and not written

The row append to the traceability matrix is not written: the write-only list of this WP does not include the matrix file and the master files belong to the assembler stage, so the end-to-end BR to CAP to FR/NFR to AC trace is carried inside the PRD at section 11.2 (ASM-3042).

The two BRD docx files were converted to text with the sanctioned converter into `_work/msr/extract/B-REQ-PRD-S9`, the path the WP names for exactly that purpose, so that the requirement text of section 8.4 and 8.5 of the epic BRD and section 5.16, 6 and 10 of the program BRD could be read character for character. No source file was edited.

## Sources read

Business Requirements Program v5 and Business Requirements Epics 3 to 8 v1 (folder 03, converted with `convert_sources.py` into the WP scratch extract path); FSD S9 Partner management v3 in the FSD v6 folder; Recovery Workbench Architecture v5 Text Extract v1 (slides 4, 9 to 21, 29, 37, 38, 41 to 45); Recovery Workbench Temporal and Drools Design Text Extract v1 (slides 5, 12, 13 and 25); Recovery Workbench Business Rules and Routing Logic v4 (R-UNI-25 to R-UNI-29, R-UNI-45, R-WO-30 to R-WO-35, R-LIT-24 to R-LIT-29 and the ten route sets); Recovery Workbench Logical Data Model and Data Dictionary v8 (partner, partner_instruction, partner_user and their lists); Recovery Workbench Physical Schema v6.sql (the three partner tables); Recovery Workbench Non Functional Specification v3 through the BRD's section 6; Microservice Ownership Map v1 through the xlsx and `_work/msr/plan/ownership.json`; Microservice Story Template and Rules v1 sections R1, R3, R5, R8 and R9; `_work/msr/plan/split_plan.json` (`stats` and `legacy` only) and `_work/msr/plan/ids.json`. No issue tracker, no web call and no git command was used.
