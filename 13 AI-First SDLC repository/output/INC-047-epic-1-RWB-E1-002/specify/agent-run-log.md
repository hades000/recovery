# Agent run log — RWB-E1-002 specification

| Field | Value |
|---|---|
| RUN_ID | `INC-047-epic-1-RWB-E1-002` |
| Stage | Specification (Technical Specifier) |
| Date | 2026-11-04 |
| Story | RWB-E1-002 — Case list v1 with case ID, owner and queue |
| Module | P1 Recovery data engine |
| Status | `SUCCESS` |
| Outputs | `spec.md`, `compliance-validation.md`, this log |

## 1. Sources read

| # | Source | Path | Use |
|---|---|---|---|
| 1 | Authoring guide | `output/SPEC-AUTHORING-GUIDE.md` | Required sections and status lines |
| 2 | Pilot spec (structure only) | `output/INC-043-epic-1-RWB-E1-020/specify/spec.md` | Section order and table shapes |
| 3 | Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 002 Case list v1 with case ID owner and queue v1.md` | Story, rules, ACs, contract, plan |
| 4 | Module FSD | `docs/prds/recovery-workbench-fsd-p1-recovery-data-engine-v2.md` (A2.18) | Functional behaviour and messages |
| 5 | Module TSD | `requirement/legacy/05-technical-architecture/recovery-workbench-tsd-p1-recovery-data-engine-v2.md` (T3.1 `case_list_row`, T5.1) | Data model and interface |
| 6 | API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v2.yaml` (API-P1-001, API-P1-002) | Existing job endpoints |
| 7 | Screen inventory | `requirement/legacy/07-screens-and-experience/recovery-workbench-screen-inventory-and-navigation-v2-xlsx.md` (SCR-02) | Confirmed the Workbench screen belongs to P3 |
| 8 | Message standard | `requirement/legacy/07-screens-and-experience/recovery-workbench-error-and-message-standard-v3-docx.md` | MSG-P1-001, 011, 012; MSG-P4-002 |
| 9 | Business requirements | `requirement/legacy/03-requirements-and-specifications/recovery-workbench-business-requirements-epic-1-v3-docx.md` | REQ-RDF-007 wording |

## 2. Steps performed

1. Read the guide and the pilot spec for structure only.
2. Read the story in full; extracted 8 business rules, 10 acceptance criteria and 8 exception paths.
3. Checked FSD A2.18 for the acceptance criteria and messages; checked TSD T3.1 for `case_list_row`.
4. Confirmed the story uses existing job endpoints; `API In Scope: NO`, `NO_API_CHANGE`.
5. Confirmed the Power BI report is owned by RW-BIANAL and the Workbench case list screen by
   RWB-E1-031; `UI In Scope: NO`.
6. Built the coverage table; assigned `SPEC-RWB-E1-002-001..016`.
7. Wrote the design, 12 test scenarios, 6 clarifications and the status block.
8. Wrote `compliance-validation.md`; no Critical, High or Medium finding.

## 3. Decisions and assumptions

| ID | Decision / assumption | Basis | Effect if wrong |
|---|---|---|---|
| D-01 | The case list is one row per open case and linked account | Story BR1; `uk_case_list_row` | A per-case list would lose accounts |
| D-02 | The list is replaced by business date in one transaction | Story BR6; AC7 | A merge could duplicate rows |
| D-03 | A count FAIL publishes the list in this story | Story AC4; RWB-E1-011 adds the hold | Holding here would pre-empt the reconciliation story |
| D-04 | The Power BI data set is not built here | Story §15; out of scope | UI scope would be overstated |
| D-05 | The column order is the report contract | Story AC2 | A silent reorder would break the report |

No business rule, threshold, role, field, message or route was invented.

## 4. Coverage result

| Metric | Count |
|---|---|
| Business rules mapped | 8 / 8 |
| Acceptance criteria mapped | 10 / 10 |
| Exception paths mapped | 8 / 8 |
| Record transitions mapped | 6 / 6 |
| SPEC IDs created | 16 |
| Unmapped or blocked rows | 0 |
| Clarifications | 6, all RESOLVED |

## 5. Open items

None. The spec is ready for human review and the Implementation Planner.

```text
RUN_STATUS: SUCCESS
COVERAGE: [RULES: 8/8] [ACS: 10/10] [EXCEPTIONS: 8/8] [TRANSITIONS: 6/6]
CLARIFICATIONS: [TOTAL: 6] [RESOLVED: 6] [OPEN: 0]
BLOCKERS: 0
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
