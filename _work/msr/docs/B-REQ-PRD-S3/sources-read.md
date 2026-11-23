SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# B-REQ-PRD-S3 working note — sources read and coverage

Not a deliverable. Scratch record for WP B-REQ-PRD-S3 (PRD S3 rwb-guarantee v1). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

## 1. Sources read

| Source | What was taken from it |
|---|---|
| 03 Requirements and specifications/Recovery Workbench Business Requirements Program v5.md | Section 5.10 (REQ-S3-001 to REQ-S3-007 with priority, owner and epic), section 6.1 to 6.12 (NFR-001 to NFR-078 with targets and status), section 10.2 and 10.3 (service epic RWB-SVC-S3, schema, wave 3, E4 release 28 Feb 2027 (tentative)) |
| 03 Requirements and specifications/Recovery Workbench Business Requirements Epics 3 to 8 v1.md | Sections 4.4, 5, 6, 7.1, 7.3, 8.2 (BR-022 to BR-025 and their source columns), 10 (KPI measures), 11.1 to 11.4, 12 (Q-001, Q-012, Q-013, Q-016), 13, 14 |
| 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6/Recovery Workbench FSD S3 Guarantees and guarantors v3.md | Document control, existing capability check, A1.1 to A1.4, A2.1 to A2.8 (steps, integration points, prerequisites, rules, field catalog, roles, acceptance criteria), Requirements served, Screens, appendices |
| _work/msr/extract/Recovery Workbench Technical Specifications by Module v5/Recovery Workbench TSD S3 Guarantees and guarantors v2.md | T3.0 to T3.3 (record columns, guarantee_claim, DF-TRT-015 to DF-TRT-022, LOVs, relationship), T4 (32 rules, 17 states), T5.1 (INT-29), T5.3, T6.1 (capability area Treatment and offer), T7, T-A.1 and T-A.2 |
| _work/msr/extract/Recovery Workbench Epics 3 to 8 Specification v3.md | Features sheet rows for E4 S3 (FEAT-GUA-01 to FEAT-GUA-08), APIs sheet rows for S3, integrations sheet INT-29 |
| _work/msr/extract/Recovery Workbench Business Rules and Routing Logic v4.md | R-GUA-01 to R-GUA-32 (from-state, event, condition, action, to-state), R-LIT-01 (route numbering) |
| _work/msr/extract/Recovery Workbench API Specification v4.yaml | Paths /cases/{caseId}/guarantee-claims and /guarantee-claims/{claimId}, GuaranteeClaim and its request and update schemas, x-module S3, x-capability area and right, error responses |
| _work/msr/extract/Recovery Workbench Event and Messaging Design v4.md | EV-13, EV-14, EV-15 (notice events) and the event table's end at EV-19 |
| _work/msr/extract/Recovery Workbench Physical Schema v6.sql | Confirm the view names v_ace_contact and v_ace_party_product exist among the 30 recovery.v_ace_* views |
| 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md | Slides 3, 4, 9 to 13 (call types, timeouts, retry, connection matrix incl. the S3 row), 14 to 20 (S3 contract on slide 18), 27, 30 (rwb_guarantee), 32, 37, 41 (S3 row), 42 and 43 (event catalogue), 44, 45 |
| 22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md | Slide 13 (workflow per stage), slides 15 and 16, slide 19 (S3 guarantee claims: seven steps, clocks, 32 rules, approvers, release authorities, point of no return), open decisions list |
| 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx and _work/msr/plan/ownership.json | Services S3 row (schema rwb_guarantee, REST base /api/recovery/guarantee/v1, topic, queue), Endpoints (POST, PATCH), Workflows (GuaranteeClaimWorkflow), Tables (guarantee_claim S3; dp_guarantee_claim P1), Rulings (dp_guarantee_claim, valuation_ext) |
| 22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md | R1, R3, R4, R5 (DP table, wave map), R8.1 (header), R8.2 (versioning), R9 (placeholder, row keys) |
| _work/msr/plan/ids.json | Confirmed D-RCV-60, ADR-013 to ADR-023 and DL44 to DL49 as the new identifiers; no new decision ID was needed |
| _work/msr/plan/split_plan.json | legacy rows RWB-E4-013 to RWB-E4-020: primary S3, wave 3, disposition Split (rework), slices RWB-S3-E40nn-CON and -APP |
| 03 Requirements and specifications/PRD/Recovery Workbench PRD S1 rwb-valuation v1.md | Section structure and register of the sibling PRD in the same family (read only, not edited) |

## 2. Identifier mapping used

| Generated | Traces to |
|---|---|
| CAP-S3-001 to CAP-S3-013 | FEAT-GUA-01 to FEAT-GUA-08 (with CAP-S3-011 and CAP-S3-013 spanning the validation rules and the eligibility rule), BR-022 to BR-025 |
| FR-S3-001 to FR-S3-032 | REQ-S3-001 to REQ-S3-007 by the FSD REQ column; R-GUA-01 to R-GUA-32 by the rule named in the statement |
| NFR-S3-001 to NFR-S3-030 | NFR-001, 008 to 011, 013 to 015, 020 to 027, 033 to 035, 039, 040, 042, 045 to 047, 049, 051 to 055, 059 to 061, 064, 066 to 068, 078 |
| AC-S3-001 to AC-S3-022 | AC-S3-001-01 to AC-S3-008-01 and the exception rows as evidence; the criteria themselves are written from the rules |
| ROL-S3-01 to ROL-S3-12 | BRD section 5 roles, TSD T6.1 RBAC matrix, FSD A2 roles per feature |
| JRN-S3-01 to JRN-S3-05 | FSD A2.1 to A2.8 grouped by actor and moment |
| OQ-S3-01 to OQ-S3-16 | CG-B-REQ-PRD-S3-1 to CG-B-REQ-PRD-S3-19 (the ones that need a decision) and the carried BRD questions Q-001, Q-012, Q-013 |

## 3. Coverage statement

7 of 7 program requirements (REQ-S3-001 to REQ-S3-007) and 4 of 4 BRD requirements of E4 naming this service (BR-022 to BR-025) are carried by at least one functional requirement. BR-025 has no program requirement of its own; the trace through REQ-S3-002 is an assumption (CG-B-REQ-PRD-S3-8; ASM-B-REQ-PRD-S3-8).

## 4. Registers written by this WP

19 gap rows (CG-B-REQ-PRD-S3-1 to CG-B-REQ-PRD-S3-19) and 23 assumption rows (ASM-B-REQ-PRD-S3-1 to ASM-B-REQ-PRD-S3-23). The numbering is the WP-local placeholder numbering; step D1 renumbers the rows as GAP-nnnn and ASM-nnnn and rewrites the citations.

## 5. Not written by this WP

`requirement/Traceability_Matrix.md` is not written: only the assembler writes master files (root rule 7) and that path is not in this WP's "Write only". The BR to CAP to FR/NFR to AC trace is held in section 11.2 of the PRD and is ready for the assembler to append.
