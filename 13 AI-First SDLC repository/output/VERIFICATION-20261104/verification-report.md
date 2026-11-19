# Verification report

Run: 2026-11-04
Checks: **79** · Passed: **79** · Failed: **0**

## Summary

| Measure | Value |
|---|---:|
| Required files | 24 |
| Story increment cards | 78 |
| CTX IDs in project-context | 145 |
| CTX rows in matrix | 113 |
| Build-sequence story keys | 115 |
| US rows in matrix | 115 |
| Manifest entries | 411 |
| Document map rows | 411 |
| Spec SPEC IDs | 18 |

## Checks

| Check | Result | Detail |
|---|---|---|
| file exists: AGENTS.md | PASS |  |
| file exists: README.md | PASS |  |
| file exists: .github/contexts/project-context.md | PASS |  |
| file exists: .github/contexts/domain-context.md | PASS |  |
| file exists: .github/contexts/frontend-context.md | PASS |  |
| file exists: .github/contexts/backend-context.md | PASS |  |
| file exists: .github/contexts/testing-standards.md | PASS |  |
| file exists: requirement/Context_RecoveryWorkbench.md | PASS |  |
| file exists: requirement/BRD_RecoveryWorkbench.md | PASS |  |
| file exists: requirement/RecoveryWorkbench_Requirements.md | PASS |  |
| file exists: requirement/Intake_Gap_Report_RecoveryWorkbench.md | PASS |  |
| file exists: requirement/Traceability_Matrix.md | PASS |  |
| file exists: docs/increments/INDEX.md | PASS |  |
| file exists: docs/increments/epics/EPIC-001-foundation-1.md | PASS |  |
| file exists: docs/increments/epics/EPIC-001-tailoring.md | PASS |  |
| file exists: docs/increments/epics/EPIC-002-foundation-2.md | PASS |  |
| file exists: docs/increments/epics/EPIC-002-tailoring.md | PASS |  |
| file exists: output/CONTEXT-20261104/agent-run-log.md | PASS |  |
| file exists: output/INC-043-epic-1-RWB-E1-020/specify/spec.md | PASS |  |
| file exists: output/INC-043-epic-1-RWB-E1-020/specify/compliance-validation.md | PASS |  |
| file exists: output/INC-043-epic-1-RWB-E1-020/agent-run-log.md | PASS |  |
| file exists: requirement/legacy/DOCUMENT_MAP.md | PASS |  |
| file exists: requirement/legacy/_conversion-report.md | PASS |  |
| file exists: requirement/legacy/_manifest.json | PASS |  |
| project context has CTX IDs | PASS | 145 unique |
| no duplicate CTX IDs in the project-context tables | PASS | 0 duplicate table rows |
| all requirement CTX IDs are in the matrix | PASS | 113 matrix rows |
| CTX-TECH and CTX-GAP are intentionally outside the requirement matrix | PASS | 32 excluded (technical context and gaps) |
| matrix has the 16 required columns | PASS | 17 pipes |
| all build-sequence story keys are in the matrix | PASS | 115 keys |
| spec section: ## Change Scope Declaration | PASS |  |
| spec section: ## Requirement-to-SPEC Logic Coverage | PASS |  |
| spec section: ## Unit Test Applicability | PASS |  |
| spec section: ## Clarification Log | PASS |  |
| spec section: ## Status reporting | PASS |  |
| spec has SPEC IDs | PASS | 18 unique |
| spec declares UI/Logic/API scope | PASS |  |
| spec declares design evidence status | PASS |  |
| spec declares clarification status | PASS |  |
| spec has frontend and backend unit-test rows | PASS |  |
| all clarifications are resolved | PASS | no OPEN CLAR rows |
| compliance review has a status | PASS |  |
| compliance review has findings | PASS |  |
| EPIC-001-foundation-1.md section: ## Identification | PASS |  |
| EPIC-001-foundation-1.md section: ## Project type | PASS |  |
| EPIC-001-foundation-1.md section: ## Scope | PASS |  |
| EPIC-001-foundation-1.md section: ## Reused approved artefacts | PASS |  |
| EPIC-001-foundation-1.md section: ## Lifecycle tailoring | PASS |  |
| EPIC-001-foundation-1.md section: ## Owners and approvals | PASS |  |
| EPIC-001-foundation-1.md section: ## Agents selected | PASS |  |
| EPIC-001-foundation-1.md section: ## Risk, rollback and stop signals | PASS |  |
| EPIC-001-foundation-1.md section: ## Evidence links | PASS |  |
| EPIC-002-foundation-2.md section: ## Identification | PASS |  |
| EPIC-002-foundation-2.md section: ## Project type | PASS |  |
| EPIC-002-foundation-2.md section: ## Scope | PASS |  |
| EPIC-002-foundation-2.md section: ## Reused approved artefacts | PASS |  |
| EPIC-002-foundation-2.md section: ## Lifecycle tailoring | PASS |  |
| EPIC-002-foundation-2.md section: ## Owners and approvals | PASS |  |
| EPIC-002-foundation-2.md section: ## Agents selected | PASS |  |
| EPIC-002-foundation-2.md section: ## Risk, rollback and stop signals | PASS |  |
| EPIC-002-foundation-2.md section: ## Evidence links | PASS |  |
| EPIC-001-tailoring.md has phase decisions | PASS |  |
| EPIC-001-tailoring.md has reuse records | PASS |  |
| EPIC-002-tailoring.md has phase decisions | PASS |  |
| EPIC-002-tailoring.md has reuse records | PASS |  |
| 78 Epic 1 story increment cards | PASS | 78 cards |
| story increment card names are unique | PASS | 0 duplicates |
| INDEX.md lists 78 story increments | PASS | 78 rows |
| every story card RUN_ID matches its card name | PASS | 78 cards |
| every story card has an output run folder | PASS | 78 runs |
| every story card has the template sections | PASS | 78 cards |
| old epic card names are retired | PASS |  |
| conversion has no failures | PASS | 0 failures |
| manifest has 411 entries | PASS | 411 entries |
| manifest has 256 source files and 155 zip entries | PASS | 256 files / 155 zip entries |
| document map has 411 rows | PASS | 411 rows |
| document map reports no failures | PASS |  |
| no tiny generated markdown outside the legacy corpus | PASS |  |
| no obvious PII patterns in generated docs | PASS |  |

## Result

**PASS** — the package is internally consistent. The open items are the recorded
gaps (GAP-001..020) and the `TBC` approvers, not verification failures.

## What this verifies

- Every required artifact exists.
- The context package has unique CTX IDs and the requirement CTX IDs are in the matrix.
- The matrix has the required 16 columns and every build-sequence story key.
- The pilot spec (`INC-043`) has the required sections, unique SPEC IDs, both unit-test rows and no open clarification.
- The pilot compliance review has a status and findings.
- The increment structure has 2 epic cards, 2 tailoring records, 78 story cards and an INDEX;
- Story card names and RUN_IDs match the output run folders.
- The conversion has 411 entries, 0 failures and a 411-row map.
- No obvious PII patterns in the generated docs.

## What this does not verify

- Spec-to-story AC alignment; the 15 stale or mismatched specs are listed in `docs/increments/INDEX.md`.
- The accuracy of every converted table against the original binary file (spot checks only).
- The truth of the source documents; it verifies that the package reflects them.
- Implementation behaviour, API execution or test results; those need the ACE repository.
- Named approvers; they are `TBC` by design (GAP-006).
