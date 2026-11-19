# Compliance validation: RWB-TE-001 specification v3 (specifier self-check)

| Field | Value |
|---|---|
| Artifact | `aisdlc/output/INC-002-epic-1-RWB-TE-001/specify/spec.md` (v4, 18 Nov 2026; v3 kept as `spec.run2.md`) |
| Contracts | `contracts/backend-apis.json` (v4), `contracts/frontend-integrations.json` (unchanged) |
| Stage | Specification, before the spec gate (round 3) |
| Prepared by | Technical Specifier (agent run) |
| Formal gate | Compliance Reviewer, written to `review/spec-gate-review-3.md` (round 3; rounds 1 and 2 are `review/spec-gate-review.md` and `review/spec-gate-review-2.md`) |
| Supersedes | `_v2-baseline/specify/compliance-validation.md` (REVIEW-RWB-TE-001-SPEC-004, history) |

## 1. Scope

Checked against `aisdlc/.github/rules/specification-execution-gates.md`, the contexts
(`backend-context.md`, `frontend-context.md`, `testing-standards.md` CTX-TESTING-RWB-V2 2.0,
`backend-standards.md`, `frontend-standards.md`), story file v7 RWB-TE-001 v1, D-RCV-35 §8.2, D-RCV-36 §3.3,
ADR v3, Decision Log v10, the local decisions D-RCV-02..-52 and L-RCV-03/-14, the audit
`aisdlc/evidence/phase0-standards-audit.md`, and the code of this repository as read on 17 Nov 2026.

## 2. Earlier findings

All ten findings of `review/spec-gate-review.md` (REVIEW-RWB-TE-001-019..028) are addressed; the
mapping is in `gate-response.md`. The four Low findings of `review/spec-gate-review-2.md` (029–032)
are addressed in v4; the mapping is in `gate-response.md` "Round 2".

### Round 2 checks (18 Nov 2026)

| Check | Result | Evidence |
|---|---|---|
| 029: downstream re-base | PASS | SU-08 now covers INC-003 RWB-E1-042 (`casewf.config(.api)`, property records, problem types in P4, no P4 → P3 cycle, merge order) and INC-005 RWB-TE-003 (new homes; `propagate = false` for generated packages). INC-008 is extended for D-RUN-10/-11. |
| D-RUN-10 / D-RUN-11 room in the map | PASS | `config.api` and `refdata.api` are valid P3 `published` entries under the existing pattern; the owning story adds each with its `@NamedInterface` (field matrix). The constraint is dependency direction (P4 must not depend on P3), recorded in SPEC-022 (d), ASM-01 and SU-08. |
| 030: published surface | PASS | Temporal and Quartz implementation in non-published `casewf.workflow.internal` / `casewf.timers.internal`; `propagate = false` on every `@NamedInterface` (SPEC-001, -004 (d)); `PdpaPayloadCodec` package-private; SPEC-025 lists the public types per published package; T-TE001-14. |
| Relocation compiles | PASS (by reading) | Round-2 read of `TemporalAdminController`: it reads the package-private `TemporalProperties`. v3 would not have compiled after the move to `casewf.admin`. Fixed: `TemporalProperties` is public in the non-published `casewf.workflow.internal`. No other package-private type is used across the new package lines (searched: `TemporalProperties`, `TemporalConfig`, `DroolsProperties`, `DroolsRuleEngine`, `RecoveryProperties`, `ProblemFactory`, `PlatformConfig`, `QuartzTimerScheduler`, `BlobDocumentStore`). |
| 031: test strings | PASS | SPEC-022 (f) names both workbook rows (`Import`, `Variables`). A search found no other old-package string literal in `backend/src` or in the non-Java build and config files. |
| 032: step 7 | PASS (local) / HV-01 (host) | SPEC-012 (b), (c); T-TE001-13 (backend and frontend negative controls through `./scripts/dev.ps1 test`); HV-01 and SU-13. Host-side blocking is not claimed as tested. |

## 3. Checks performed

| Check | Result | Evidence |
|---|---|---|
| Required spec sections ([SEG]) | PASS | Change Scope, Requirement-to-SPEC, intent, trigger, field matrix, status matrix, exceptions, API assessment, Unit Test Applicability (both surfaces), SPEC table, Clarification Log, status lines present. |
| Change classification | PASS | `NEW_STORY`, UI NO, Logic YES, API NO, `NO_API_CHANGE`; endpoint classes move package without contract change. |
| Requirement-to-SPEC coverage | PASS | BR1–BR6 and AC1–AC7 mapped (13 rules); X1–X6 mapped; X7 moved out of scope (D-RCV-52). AC3 and AC6 deviations recorded against the ACs. |
| Unique SPEC IDs | PASS | SPEC-RWB-TE-001-001..-026, each defined once; -021 marked withdrawn. |
| D-RCV-35 / D-RCV-36 alignment | PASS | Published packages `casewf.rules`, `casewf.timers`, `casewf.workflow` per D-RCV-36 §3.3; BND-6 left to RWB-E1-069 per D-RCV-35 §8.2. Interface signatures stay for E1-028 / E1-072 (DG-08). |
| Implementable on this repository | PASS (by design) | Relocation table covers every main class found under `recovery/**`; published lists equal what exists (SPEC-025); BND-5 passes with `dochub.storage`; module-map rule passes after the move (T-TE001-05). Not executed in this stage (no code edited). |
| Backend coverage scope | PASS (expected FAIL at baseline stated) | Whole recovery tree plus tooling, 4 counters, no exclusions; SPEC-024 lists the tests that raise it. |
| Frontend coverage scope | PASS | Inherited config; existing code at baseline 91.66% lines; no change to runtime code. |
| Dependencies and shared files | PASS | No new dependency; only `backend/build.gradle.kts` edited among shared build files. |
| Authorization | N/A | No runtime authorization added; `SecurityConfig` moves unchanged. |
| PDPA, personal data, secrets | PASS | Class and package names and synthetic values only. |
| Error contract | PASS | Build-log texts only; `ApiError` codes unchanged. |
| Design evidence | N/A | `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`. |
| No-question rule | PASS | Nine assumptions (`assumptions.md`); two open-item requests (SU-02 for DG-05, SU-13 for HV-01). |
| Source citation | PASS | Every SPEC row cites a document and version or a labelled assumption; source keys in spec.md. |
| Document gaps | PASS | DG-01..DG-09 with two citations each; none a blocker. |

## 4. Residual risks for the planner

- Spring Modulith 2.1.1 must import test-scope fixtures for TC-TE-001-03; if it cannot, the plan stops (SPEC-007, ASM-05).
- `SecurityConfig` coverage needs tests that do not call an identity provider (SPEC-024).
- The relocation touches every main class; the plan sequences it before the new rules so that `ModulithTest` and the moved unit tests stay green at each step.

## 5. Status lines

```text
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 13] [COVERED_RULES: 13] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: build-time rules and package relocation without behaviour change]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
```
