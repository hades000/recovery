---
title: "Compliance validation — RWB-E1-044"
run_id: "INC-001-epic-1-RWB-E1-044"
status: "SPECIFIED"
---

# Compliance validation — RWB-E1-044

Technical Specifier self-check of `spec.md` against the source story, the increment card, the
governing decisions and `.github/rules/specification-execution-gates.md`. Prepared 2026-11-09;
updated the same day with the Product Owner answers to CLAR-001 and CLAR-002 (Jira `TB0001-1205`
comment 1781236) and the ACE `develop` eedf5c75 re-check; updated 2026-11-10 with D-RCV-47 (schema `ace`,
prefix `rwb_`), the spec gate 2 remediation and the ACE `develop` 9f450bbd re-check; updated again 2026-11-10 with D-RCV-48 and the spec gate 3 remediation. The independent
Compliance Reviewer spec gate results are in §4.

## 1. Source cross-check

| Source item | Spec coverage | Result |
|---|---|---|
| BR1 versioned migrations only | SPEC-001, -005, -006, -016 | Covered |
| BR2 no literal schema; parameter | SPEC-002, -007 (story's `RWB_SCHEMA`/`${schema}` superseded by D-RCV-47: schema from the connection's `currentSchema`, `rwb_` prefix linted) | Covered |
| BR3 one file per story with key | SPEC-006, -008, -009 (D-RCV-28) | Covered |
| BR4 forward only | SPEC-003, -009, -010, -014 | Covered |
| BR5 checksums validated | SPEC-003, -005 | Covered |
| BR6 own history table | SPEC-001 | Covered |
| BR7 drift check before SIT/UAT/PROD | SPEC-012 (container comparison, T-044-02) | Covered — Product Owner CLAR-001 A; environment gate parked (D-RCV-05) |
| Flow 7, §12, §15 job monitor / SCR-44 | SPEC-013 | Deferred — Product Owner CLAR-002 A (D-RCV-12) |
| §14 MSG-P3-016 | SPEC-018 (CLAR-004 A), SPEC-003 (D-RCV-28 (4)) | Covered |
| §16 test cases TC-E1-044-01..07, -10 | T-044-01..07; TC-10 deferred (CLAR-002 A) | Covered |
| §17 guardrails | SPEC-007, -016, -019 | Covered |
| §19 out of scope | Guardrails section; CLAR-009 | Covered |
| Card risk: flag `rwb.p3.migration-drift-gate` | Not created (CLAR-001 A) | Covered |
| ACE `develop` eedf5c75 and 9f450bbd re-check | eedf5c75 → 9f450bbd: `AppConfig`, `SampleModuleConfig`, `application.yaml`, `build.gradle.kts`, `ModulithTest` unchanged; core duplicate versions 24–27 renumbered upstream (OPEN-025 settled, T-044-14); `SampleModuleConfig` uses the connection's `currentSchema=ace` (D-RCV-47 pattern) | Covered |
| D-RCV-47 schema `ace`, prefix `rwb_` | SPEC-001, -002, -004 (d), -005, -006, -007, -012, -018; T-044-03, -05, -12, -15; CON-001/-002; no `${recoverySchema}`, schema property or `createSchemas` left | Covered |
| D-RCV-48 baseline and `createSchemas` | SPEC-001 (`createSchemas(false)` explicit), SPEC-002 / X12 (missing schema fails, nothing created), SPEC-003 (`baselineVersion("0")`, `baselineOnMigrate(true)` with rationale), status-transition first-run row; T-044-03 (missing schema), T-044-16 (non-empty `ace` baselines at 0 and applies `V0001`), T-044-12 / -15 on pre-populated `ace`; CON-001 | Covered |
| Gate 3 REVIEW-018 / -019 / -020 | SPEC-007 (5) prefix on every table/sequence/index identifier in any statement with allow-list and derivation note, (6) `GRANT`/`REVOKE` ban; T-044-05 fixtures; X10, X11; SPEC-005 / Authorization DML via ACE default privileges; OPEN-019 same-role condition; OPEN-029 due before this story's `/planner`; CON-002 | Covered |
| Gate 2 REVIEW-012 / -013 / -014 | Card business outcome and authority notes; DEV in SPEC-005, triggers, preconditions, contract; runner fail-fast in SPEC-005, X9, T-044-12 | Covered |

## 2. Governance and standards

| Check | Result |
|---|---|
| Recovery code only in `th.co.scb.ace.demo.recovery` (AGENTS.md §3.1; D-RCV-02) | Pass — `recovery.casewf.internal.migration` (CLAR-003 A) |
| No business value / literal threshold in code (AGENTS.md §3.2, §4.8) | Pass — no schema value in code or config; the schema comes from ACE's datasource URL (D-RCV-47) |
| Method security on every endpoint (§3.3) | N/A — no endpoint |
| Decision record entry (§3.4) | N/A — no case change or decision |
| Messages by rule ID (§3.6) | Pass — ID + parameters only (CLAR-004 A) |
| Migration by script only, one per story (§3.7) | Pass — convention and lint; this story ships none |
| Test before code; no weakened test (§3.10, §4.5) | Pass — tests specified; ACE suite must stay green |
| No new dependency without approval (§4.4) | Flagged — Testcontainers test-scope additions (D-RCV-07) need ACE tech lead confirmation at plan approval; JaCoCo approved under OPEN-023 and added by RWB-TE-001 first (SPEC-015 (d)) |
| No change to merged migration (§4.6) | Pass |
| No credentials, PII or production data (§4.1, §4.7; NFR-052) | Pass — SPEC-016; synthetic fixtures only |
| Shared-file edits minimal and listed (CLAUDE.md) | Pass — `build.gradle.kts` test scope; new `application-db-migrate-recovery.yaml`; `AppConfig`/`application.yaml` untouched |
| Never run against a shared database | Pass — Testcontainers only (TS-RCV-8) |

## 3. Gate checklist (specification-execution-gates.md)

| Check | Result |
|---|---|
| Change Scope Declaration complete | Pass |
| Requirement-to-SPEC Logic Coverage has no BLOCKED rows | Pass |
| Unit Test Applicability: frontend and backend rows consistent with scope | Pass |
| API impact explicit | Pass — `NO_API_CHANGE` |
| Design evidence | `NOT_REQUIRED` (UI In Scope = NO) |
| SPEC IDs unique, traced to FR/NFR | Pass — SPEC-RWB-E1-044-001..019 |
| Clarification log | 0 OPEN, 10 RESOLVED |
| No TODO/placeholder text | Pass (open decisions are recorded as CLAR items) |
| PII / secrets scan | Pass |

## 4. Review gate

Spec gate 1 (2026-11-09): `FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 2] [LOW: 8]`, report
`output/INC-001-epic-1-RWB-E1-044/review/spec-gate-review.md`. Remediation, decided by the recovery
tech lead 2026-11-09:

| Finding | Severity | Remediation |
|---|---|---|
| REVIEW-RWB-E1-044-001 | Medium | D-RCV-44: `recoveryIntegrationTest` stays outside `check`; run before every MR touching recovery migrations or `RecoveryFlywayConfig`, result in implementation evidence; CI waits on Docker (OPEN-026); PO re-confirms BR7 run rule (OPEN-027). SPEC-012, SPEC-015 (c), coverage BR7 row, Unit Test Applicability. |
| REVIEW-RWB-E1-044-002 | Medium | D-RCV-45: bean disabled under `db-migrate` without `db-migrate-recovery`. SPEC-004 (d), T-044-15, contract `activation.dbMigrateWithoutRecovery`. |
| REVIEW-RWB-E1-044-003 | Low | Coverage table uses only `DIRECT` / `INHERITED_EXISTING_BEHAVIOR` and `COVERED`; X-paths split; §13 step 2 relabelled; §10 Authority row added. |
| REVIEW-RWB-E1-044-004 | Low | FR/NFR IDs in every SPEC "Traces to"; header lists D-RCV-40, -43..-46. |
| REVIEW-RWB-E1-044-005 | Low | Test-scope tooling `recovery/casewf/internal/migration/**` (non-test classes) added to the JaCoCo class directories (SPEC-015 (d), D-RCV-43 consistency). |
| REVIEW-RWB-E1-044-006 | Low | T-044-03 runs with `recovery` and `rwb_it`, plus invalid `Bad-Name`. |
| REVIEW-RWB-E1-044-007 | Low | SPEC-007 scans dollar-quoted bodies; accepted gap limited to single-quoted literals; fixtures in T-044-05; contract CON-002. |
| REVIEW-RWB-E1-044-008 | Low | INC-001 card: status, compliance, rollback route, flag, main-flow superseded note. |
| REVIEW-RWB-E1-044-009 | Low | D-RCV-46: Chitchaya Muanchonchana holds the PO gates; INC-001 and EPIC-001 cards, OPEN-018 settled row. |
| REVIEW-RWB-E1-044-010 | Low | Matrix CRLF restored; open-items separator fixed; run-log reference fixed. |

Spec gate 2 (2026-11-09): `FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 5]`, report
`output/INC-001-epic-1-RWB-E1-044/review/spec-gate-review-r2.md`. Round-1 findings 001–010 closed (001
conditional on OPEN-027). New Low: -011 stale status lines (fixed by recording this result), -012 card
business outcome / authority text still names the drift gate and SCR-44, -013 DEV environment not
covered by SPEC-005 / OPEN-019 / OPEN-020, -014 migrate-and-exit runner behaviour when the recovery bean
is absent, -015 TS-RCV-3 lacks the D-RCV-44 run rule (Context Updater).

`REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.`

Gate 2 remediation 2026-11-10 (recovery tech lead request): D-RCV-47 applied (schema `ace`, prefix `rwb_`); -012 card
business outcome and authority notes; -013 DEV in SPEC-005 (same image digest to DEV, SIT, UAT, PROD); -014 runner
fail-fast (SPEC-005, X9, T-044-12); -015 deferred to Context Updater as OPEN-029 (with OPEN-022); OPEN-025 settled
(ACE `develop` 9f450bbd).

Spec gate 3 (2026-11-10): `FAIL [CRITICAL: 0] [HIGH: 1] [MEDIUM: 1] [LOW: 4]`, **blocking**, report
`output/INC-001-epic-1-RWB-E1-044/review/spec-gate-review-r3.md`. Round-2 -011..-015 closed (-015 deferred, OPEN-029).
New: -016 High `baselineOnMigrate(false)` fails on the non-empty schema `ace`; -017 Medium Flyway `createSchemas`
defaults to true, so "no `createSchemas`" does not stop schema creation; -018 Low prefix-lint positions; -019 Low
application-account DML via inherited default privileges; -020 Low OPEN-029 due date vs this plan; -021 Low run log / §4.

Gate 3 remediation 2026-11-10 (recovery tech lead):

| Finding | Severity | Remediation |
|---|---|---|
| REVIEW-RWB-E1-044-016 | High | D-RCV-48: `baselineVersion("0")` + `baselineOnMigrate(true)` as `SampleModuleConfig`. SPEC-003 with safety rationale, status-transition first-run row, BR6 row, T-044-16 new, T-044-12 / -15 on pre-populated `ace`, CON-001. |
| REVIEW-RWB-E1-044-017 | Medium | D-RCV-48: `createSchemas(false)` set explicitly. SPEC-001 rationale corrected, SPEC-002, X12, T-044-03 asserts no schema of the missing name exists, CON-001; D-RCV-47 annotated, CLAR-005 updated. |
| REVIEW-RWB-E1-044-018 | Low | SPEC-007 (5): every table, sequence and index identifier in any statement (DDL, `FROM`/`JOIN`/`USING`, `TRIGGER ... ON`, `COMMENT ON`, ...) starts with `rwb_`, except `information_schema` / `pg_catalog`; derivation note for unnamed indexes and implicit sequences; T-044-05 fixtures; CON-002 `objectNames` aligned. |
| REVIEW-RWB-E1-044-019 | Low | SPEC-007 (6) forbids `GRANT`/`REVOKE`; SPEC-005 and Authorization cite ACE default privileges; OPEN-019 condition: recovery step uses the core step's database role. |
| REVIEW-RWB-E1-044-020 | Low | OPEN-029 needed by `/planner INC-001-epic-1-RWB-E1-044`; plan follows D-RCV-47/-48 over BS-2.3/BS-2.6/CTX-TECH-BE-FW-13 until done; D-RCV-48 and the lint rules added to its scope. |
| REVIEW-RWB-E1-044-021 | Low | Accepted by the recovery tech lead (2026-11-10), not fixed. This run is logged in `agent-run-log.md` §8. |

Spec gate 4 (2026-11-10): `FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 4]`, not blocking, report
`output/INC-001-epic-1-RWB-E1-044/review/spec-gate-review-r4.md`. Round-3 -016..-021 closed (-021 accepted). New Low:
-022 lint `FROM`/`USING` non-relation cases and `COMMENT ON COLUMN` in rule (1); -023 SPEC-003 dropped-history claim vs
`CREATE TABLE IF NOT EXISTS`, stale D-RCV-47 row in §1; -024 local start: core `clean()` drops `rwb_` objects, recovery
initializer order untested; -025 OPEN-019 role name `ACEDbFlywayRole_<ENV>` unverified, no default-privilege check.

`REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.`

Disposition (plan PRE-5): PRE-5 approved by the recovery tech lead (Jesniphat Pukkham), 2026-11-10: REVIEW-RWB-E1-044-022..-024 accepted as carried into tasks as written; REVIEW-RWB-E1-044-025 stays in OPEN-019 (DB role checked at the first DEV deploy), not a plan blocker; SPEC-015 (a) deviation accepted: no `spring-boot-testcontainers`, only `testcontainers-postgresql` as approved in D-RCV-49; no `/specify` re-run.
