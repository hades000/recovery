SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Requirements Traceability Matrix v7 - realignment notes (D-RCV-60)

Change log: v7, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash

## 1. What changed and what did not

| Item | v6 | v7 |
|---|---|---|
| Requirement rows | 231 | 231, the same IDs in the same order |
| Columns A to M | 13 | 13, unchanged values |
| Columns N to R | none | Legacy keys, New story IDs, PRD FR IDs, Owner, Coverage and flags |
| Coverage sheet | one block | the v6 block unchanged, plus the realignment block |
| Header lines | none | the Template and Rules section R8.1 header on RTM rows 1 and 2 |
| Change log row | none | v7, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |

## 2. How a row reads

Requirement -> legacy key (column N, from the v6 Stories column) -> realigned story IDs (column O, the split_plan slices of that key) -> PRD FR IDs (column P, from the PRD section 11.2 trace summary and the FR tables) -> owner (column Q: the service whose PRD functional requirements carry the requirement, else the Ownership Map owner of its legacy key) -> coverage and flags (column R).

Where no legacy key exists, column O carries the stories whose section 18 names the requirement (ASM-C2-RTM-5).

## 3. Counts

| Measure | Count |
|---|---|
| Requirements | 231 |
| Requirements with a legacy key | 134 |
| Requirements with realigned story IDs | 220 |
| Orphaned requirements (no realigned story) | 9 |
| Requirements with no PRD FR | 6 |
| Requirements whose owner differs from the v6 Module | 14 |
| Requirements citing a retired legacy story | 5 |
| Gap rows written | 8 |
| Assumption rows written | 8 |

## 4. Flags raised

| Flag | Requirement | Reason |
|---|---|---|
| CG-C2-RTM-1 | 14 rows | the v6 Module value differs from the owner read from the PRD FRs and the Ownership Map |
| CG-C2-RTM-2 | REQ-DVH-011, REQ-ILG-004, REQ-ILG-009, REQ-ILG-011, REQ-ILG-012, REQ-ILG-013 | named in a PRD, carried by no functional requirement |
| CG-C2-RTM-3 | REQ-DCM-014, REQ-S1-005, REQ-S3-006, REQ-S4-008, REQ-S4-009, REQ-S5-002, REQ-S5-007, REQ-S5-009, REQ-S8-006 | no realigned story names the requirement in section 18 |
| CG-C2-RTM-4 | REQ-RDF-004 | the slices of its legacy keys do not name it; the E3 integration stories do |
| CG-C2-RTM-5 | 97 rows | no legacy key existed in v6 |
| CG-C2-RTM-6 | Coverage sheet | the v6 coverage statement is outdated |
| CG-C2-RTM-7 | whole run | no issue, branch, commit or pull request metadata exists |
| CG-C2-RTM-8 | 231 rows | every row is Draft, no approval exists in this run |

Owner roles only; no names of people are used anywhere in this document.

## 5. Assumptions

| Assumption | Text |
|---|---|
| ASM-C2-RTM-1 | For every requirement the Owner column is the service whose PRD functional requirements carry it, and the Ownership Map owner of its legacy key where it has no functional requirement; a withdrawn row keeps the v6 Module value. The v6 Module value is kept unchanged beside it. |
| ASM-C2-RTM-2 | A requirement named in a PRD as an upstream ID but carried by no functional requirement is flagged, not mapped to a nearby FR. |
| ASM-C2-RTM-3 | A requirement that no story section 18 cites and that has no legacy key is recorded as an orphan rather than linked to the nearest story. |
| ASM-C2-RTM-4 | For REQ-RDF-004 the matrix lists the legacy slices and the citing E3 integration stories, and keeps the v6 legacy keys in column N. |
| ASM-C2-RTM-5 | Where no legacy key exists, the story link is read from section 18 of the realigned story files. |
| ASM-C2-RTM-6 | The v6 coverage block is kept unchanged and a realignment block is added below it. |
| ASM-C2-RTM-7 | No issue, branch, commit or pull request value is recorded for any row, because none exists in this run. |
| ASM-C2-RTM-8 | Every row carries review status Draft, because no human approval exists in this run. |

## 6. Status

Draft. No human approval exists in this run. The numbers in this file are the candidate numbers written by WP C2-RTM and are renumbered at step D1.
