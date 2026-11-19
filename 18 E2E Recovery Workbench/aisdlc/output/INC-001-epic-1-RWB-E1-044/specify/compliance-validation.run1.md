---
title: "Compliance validation: RWB-E1-044 spec (v14 re-baseline)"
run_id: INC-001-epic-1-RWB-E1-044
date: 2026-11-17
status: SELF-CHECK PASS (spec gate review in ../review/spec-gate-review.md)
---

# Compliance validation (Technical Specifier self-check)

## Gate checklist (`aisdlc/.github/rules/specification-execution-gates.md`)

| Check | Result | Evidence |
|---|---|---|
| Change Scope Declaration with all required fields | PASS | spec §1 |
| Requirement-to-SPEC Logic Coverage table with Coverage Type | PASS | spec §4 (19 rows: 16 covered, 3 deferred by decision) |
| Intent, trigger and preconditions, field matrix, status-transition matrix, exceptions | PASS | spec §2, §3, §7, §8, §9 |
| API assessment (NO_API_CHANGE) | PASS | spec §12; `contracts/backend-apis.json` |
| UI N/A justification | PASS | spec §13; `figma/figma_report.md` |
| Unit Test Applicability with 80% gate | PASS | spec §11; SPEC-014 |
| Frontend and Backend Specification sections | PASS | spec §5, §13 |
| Clarification Log; no open item | PASS | spec §15; `assumptions.md` |
| Status lines (MCP, classification, coverage, design evidence, clarification) | PASS | spec §16 |

## Source cross-check

| Statement in spec | Source | Agrees |
|---|---|---|
| E1-044 ships no production migration file | Decision Log v10 D-RCV-28; story v7 §13; `docs/architecture/migration-merge-order-map.md` | Yes |
| Schema `recovery`, `${recoverySchema}`, no per-environment override | D-RCV-28; story v7 §13; AGENTS.md §2; L-RCV-07 | Yes (story §7/§12 disagree, DG-L01) |
| Bean settings inherited | `RecoveryFlywayConfig.java`; BS-2.3; D-RCV-48 | Yes |
| Literal-schema rule scope | D-RCV-28 (2) | Yes |
| Clean refusal uses Flyway's message | D-RCV-28 (4) | Yes |
| IT tag, task, fail without Docker, run before every MR | D-RCV-28 (3); D-RCV-44; `backend/build.gradle.kts`; `.gitlab-ci.yml` `backend-recovery-it` | Yes |
| Real-environment drift parked | D-RCV-05; 10 Nov spec CLAR-001 A | Yes (story BR7 disagrees, DG-L02) |
| Job monitor deferred | D-RCV-12; Build Sequence v6 (E1-056 order 18) | Yes |
| MSG-P3-016 ID and parameters | Error and Message Standard v4; story v7 §14; AGENTS.md §3.6 | Yes |
| No FK into `public` | Story v7 BR8; ADR v3 ADR-010; D-RCV-35 U4 | Yes |
| Rollback by previous tag | NFR spec v3 NFR-027 | Yes |
| Schema pin gap | Phase 0 audit A-17 | Yes |
| GRANT ban | BS-2.5, BS-2.6 | Yes (E1-069 v7 and Env and Deployment Design v4 §5 disagree, DG-L05) |

## Guardrails (story v7 §17; AGENTS.md §4)

| Guardrail | Spec position |
|---|---|
| No business value in a migration | No production migration; fixtures are test-only |
| No personal data | Synthetic fixture names only (ASM-E044-10) |
| No literal schema name | SPEC-007 |
| No FK into `public` | SPEC-008, T-044-05, T-044-17 |
| No manual change; merged migration never edited | SPEC-001 (`validateOnMigrate`), T-044-12 |
| No new dependency | Flyway, Testcontainers and JaCoCo already present in `backend/build.gradle.kts` |

## Requirement and traceability

REQ-RDF-001, REQ-RDF-014 (Business Requirements Program v4 §5.1); BR-RWB-013 / FR-RWB-013 (Traceability Matrix v2.0); NFR-027, NFR-052 (NFR spec v3). Rows for the matrix are in `shared-updates.md`.
