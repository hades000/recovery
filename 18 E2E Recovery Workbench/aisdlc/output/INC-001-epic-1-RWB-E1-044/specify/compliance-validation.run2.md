---
title: "Compliance validation: RWB-E1-044 spec (v14 re-baseline, remediation run 1)"
run_id: INC-001-epic-1-RWB-E1-044
date: 2026-11-17
status: SELF-CHECK PASS (spec gate round 2 in ../review/spec-gate-review-2.md; round 1 in ../review/spec-gate-review.md)
---

# Compliance validation (Technical Specifier self-check, spec v14-2)

The first-run version is kept as `compliance-validation.run1.md`. `gate-response.md` maps findings S01 to S11 to their resolutions.

## Gate checklist (`aisdlc/.github/rules/specification-execution-gates.md`)

| Check | Result | Evidence |
|---|---|---|
| `## Change Scope Declaration` with all required fields | PASS | spec, exact heading |
| `## Requirement-to-SPEC Logic Coverage` with allowed Coverage Type (`DIRECT` / `INHERITED_EXISTING_BEHAVIOR`) and Status (`COVERED` / `BLOCKED`) | PASS | 27 rows, all `COVERED`. Out-of-scope rows map to SPEC-017 with the decision in Implementation Notes |
| Intent, trigger and preconditions, field matrix, status-transition matrix, exceptions | PASS | spec sections of the same names. Story §3 preconditions each listed |
| API change assessment (NO_API_CHANGE) | PASS | spec "API Change Assessment"; `contracts/backend-apis.json` |
| UI N/A justification | PASS | spec "Frontend Specification"; `figma/figma_report.md` |
| `## Unit Test Applicability`: frontend and backend rows; `REQUIRED` / `NOT_APPLICABLE`; 80% on lines, statements, branches, functions (LINE, INSTRUCTION, BRANCH, METHOD) | PASS | Frontend NO / NOT_APPLICABLE. Backend main and backend test-scope tooling both REQUIRED at 80% on four counters. No waiver (S03) |
| Integration testing kept separately | PASS | "Verification beyond unit tests" table (T-044-10 to -18, D-RCV-44) |
| Every business-rule line mapped or marked inherited | PASS | Story §3, §10, §12, §14, §15, §16 lines added. TC-to-T table (S08) |
| Clarification Log; no open CLAR | PASS | CLAR-001 to -012 RESOLVED |
| Status lines (MCP, classification, coverage, design evidence, clarification) | PASS | spec "Status". CONTRADICTIONS: 7, each settled and listed |

## Source cross-check

| Statement in spec | Source | Agrees |
|---|---|---|
| E1-044 ships no production migration file; no number fixed | Decision Log v10 D-RCV-28; story v7 §13; D-RUN-07 (build log, RUN-BRIEF) | Yes |
| Schema `recovery`, `${recoverySchema}` | Decision Log v10 D-RCV-28 ("recovery in every environment"); L-RCV-07 | Yes (story §7/§12 disagree, DG-L01) |
| "No per-environment override" | Story v7 §13 (attributed there, not to D-RCV-28) | Yes |
| Bean settings inherited | `RecoveryFlywayConfig.java`; BS-2.3; squad D-RCV-48 | Yes |
| Literal-schema rule scope; search path "in every form" | Squad register `INC-001-decisions.md` D-RCV-28 (2) (not in Decision Log v10; ASM-E044-11) | Yes |
| Schema-prefix rules check identifiers only; literals and comments ignored | Build log D-RUN-13; squad D-RCV-28 (2) "accepted gap" for strings; Physical Schema v6: 297 lines with a `'public.…'` literal (`sys_fields` rows) | Yes |
| D-RCV-28 lint rejects ADR-010 view text; seam for RWB-E1-069 | ADR v3 ADR-010; D-RCV-35; Env v4 §5; Physical Schema v6 Section A; build log orchestrator triage 2026-11-17T23:40; D-RUN-08 | Conflict recorded (DG-L09), not blocking |
| Clean refusal uses Flyway's message | Squad register D-RCV-28 (4) | Yes (story v7 X5/AC7/§14 disagree, DG-L11) |
| IT tag, task, fail without Docker, run before every MR | Squad D-RCV-28 (3); D-RCV-44; `backend/build.gradle.kts` | Yes |
| Container built from `infra/postgres/init` | `RecoveryDatabaseIT`; `infra/postgres/init/*` | Yes |
| Real-environment drift out of scope | D-RCV-05; CLAR-001 A in the 10 Nov spec | Yes (story BR7 disagrees, DG-L02) |
| Job-monitor parts out of scope, no owner named | D-RCV-12; RWB-E1-056 v7; API Specification v4 `getAdminJobs` | Yes (gap DG-L10) |
| MSG-P3-016 ID and parameters | Error and Message Standard v4; story v7 §14; AGENTS.md §3.6 | Yes |
| No FK into `public` | Story v7 BR8; ADR v3 ADR-010; D-RCV-35 U4 | Yes |
| Rollback by previous tag | NFR spec v3 NFR-027 | Yes |
| Schema pin gap | Phase 0 audit A-17 | Yes |
| 80% on test-scope tooling | Squad D-RCV-40, D-RCV-43 (2); testing-standards §6; implementation-execution-gates | Yes |
| GRANT ban | BS-2.5, BS-2.6 | Yes (E1-069 v7 and Env v4 §5 disagree, DG-L05) |

## Guardrails (story v7 §17; AGENTS.md §4)

| Guardrail | Spec position |
|---|---|
| No business value in a migration | No production migration. Fixtures are test-only |
| No personal data | Synthetic fixture names only (ASM-E044-10). The rethrown Flyway message holds DDL or reference data only (SPEC-003) |
| No literal schema name | SPEC-007 (identifiers only, D-RUN-13) |
| No FK into `public` | SPEC-008, T-044-05, T-044-17, T-044-21 |
| No manual change; merged migration never edited | SPEC-001 (`validateOnMigrate`), T-044-12 |
| No new dependency | Flyway, Testcontainers and JaCoCo are already in `backend/build.gradle.kts` |
| No later-story work treated as existing (D-RUN-08) | Seams SEAM-E044-01 to -04 (SPEC-016); SPEC-017 |

## Requirement and traceability

REQ-RDF-001 and REQ-RDF-014 (Business Requirements Program v4 §5.1); BR-RWB-013 / FR-RWB-013 (Traceability Matrix v2.0); NFR-027 and NFR-052 cited by source ID (NFR spec v3). The rows for the matrix, in its own columns, are in `shared-updates.md`.
