# Edit log B-REQ-PRD-PLT

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Work package: B-REQ-PRD-PLT — PRD PLT Platform v1 (PRD Builder).
Decision: D-RCV-60 microservice realignment.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Agent: aisdlc-prd-builder. Fanout: 0 (no subagent delegation was needed or used).

## 1. Files written

| File | What it is |
|---|---|
| 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md | The new PRD: 13 sections, Appendix A, front matter `status: Draft`, empty approval table |
| _work/msr/gaps/B-REQ-PRD-PLT.jsonl | 13 candidate gap rows, GAP-1664 to GAP-1676 |
| _work/msr/assumptions/B-REQ-PRD-PLT.jsonl | 18 candidate assumption rows, ASM-2807 to ASM-2824 |
| _work/msr/editlog/B-REQ-PRD-PLT.md | This edit log |
| _work/msr/docs/B-REQ-PRD-PLT/ | Scratch folder: the Architecture v5 and Temporal and Drools slide extracts used as evidence, the story inventory of the 7 platform epics, the requirement rows read from the FSD, the register writer and the id and table validators |

No other file was created, edited or deleted. Every source document was read only: the BRD Program v5 and the three epic BRDs, the FSD v6 module set and the TSD v5 module set, the Architecture v5 Text Extract, the Temporal and Drools Design Text Extract, the Non Functional Specification v3, the Ownership Map v1, the Story Template and Rules v1, the plan files (split_plan stats and legacy, ownership, ids, docs, legacy_index) and the already-written platform story files, which were read for internal consistency and not changed.

## 2. Counts

| Item | Count |
|---|---|
| Capabilities (CAP-PLT) | 15 |
| Functional requirements (FR-PLT) | 34 |
| Non-functional requirements (NFR-PLT) | 18 |
| Acceptance criteria (AC-PLT) | 25 |
| Open questions (Q-PLT) | 11 |
| Candidate gap rows (CG-B-REQ-PRD-PLT) | 13 |
| Candidate assumption rows (ASM-B-REQ-PRD-PLT) | 18 |
| Business and non-functional requirement IDs traced (Appendix A.1) | 64 (26 business requirements of BRD Program v5 section 5 and 38 non-functional requirements of section 6) |

## 3. Decisions taken in this version

| Decision | Basis |
|---|---|
| The PRD is issued at version 1 and status Draft, with an empty approval table | No predecessor PRD exists in the PLT family; the BRD carries no approval record or status field (GAP-1665, GAP-1671; ASM-2808, ASM-2824) |
| The functional requirements trace to the FSD requirement of the module the platform mechanism serves, and to the BRD non-functional requirement that sets the target | The FSD v6 set has no module for the platform (GAP-1664; ASM-2809) |
| Every platform capability is Must and lands in wave 0, with a second wave-0 increment on 31 December 2026 (tentative) for the four Temporal governance stories | Architecture v5 slide 38; BRD Program v5 section 10.3; RWB-E2-037 to RWB-E2-040 |
| The platform is kept outside the 19 services: no schema, topic, REST base or task queue of its own, and the library objects exist inside each service schema | Ownership Map Services sheet, Tables sheet rulings ASM-0073 and ASM-0074; Arch v5 slides 4 and 41 (ASM-2813) |
| The feature-flag store is read as one platform store served by rwb-integration against the library | Ownership Map rulings ASM-0073 and ASM-0039 (GAP-1667; ASM-2816) |
| The three retry statements of the BRD, the Architecture and the Temporal design are read as three call-type paths, not as one limit | BRD NFR-026; Arch v5 slide 11; Temporal and Drools Design slide 28 (GAP-1666; ASM-2815) |
| Release dates are copied unchanged and marked (tentative); no date was raised as a gap | Story Template and Rules U7, R8.2; DL48 |
| No design beyond the confirmed Architecture v5 constraints: no class, table column or endpoint signature is invented | Architecture v5 slides 11, 20, 23, 24, 33, 38, 41 and 44 |

## 4. Checks

| Check | Result |
|---|---|
| `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-REQ-PRD-PLT --quick` | PASS on all six checks: C02, C03, C05, C12, C13, C18 |
| Citation check over the two registers | 28 distinct CG and ASM identifiers cited in the PRD, all present as rows; the two external rows cited (ASM-0073, ASM-2616) exist in their own work-package registers |
| Identifier check | FR-PLT-001 to 034, CAP-PLT-001 to 015, NFR-PLT-001 to 018, AC-PLT-001 to 025, Q-PLT-01 to 11; no gap and no duplicate |
| Markdown table check | No table row differs from its header in column count; no placeholder marker remains in the document |
