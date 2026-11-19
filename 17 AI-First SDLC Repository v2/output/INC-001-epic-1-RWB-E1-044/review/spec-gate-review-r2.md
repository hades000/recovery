# Spec gate review, round 2: RWB-E1-044 (INC-001-epic-1-RWB-E1-044)

| Field | Value |
|---|---|
| Review type | SPEC GATE (specification stage), round 2 (re-review after remediation) |
| Story | RWB-E1-044 (Jira `TB0001-1205`, epic `TB0001-1162`) |
| Reviewer | Compliance Reviewer (agent run), 2026-11-09 |
| Round 1 | `output/INC-001-epic-1-RWB-E1-044/review/spec-gate-review.md`: FAIL, Medium -001, -002; Low -003..-010 |
| Artifacts reviewed | `specify/spec.md`, `specify/compliance-validation.md`, `specify/agent-run-log.md`, `specify/contracts/backend-apis.json`, `specify/contracts/frontend-integrations.json` (both parse as JSON); `requirement/Traceability_Matrix.md` rows 126, 140, 337; `docs/increments/INC-001-epic-1-RWB-E1-044.md`; `docs/increments/epics/EPIC-001-foundation-1.md` (owners table); `docs/open-items.md`; `docs/decisions/INC-001-decisions.md` D-RCV-44..46 |
| Sources | Story file v5 (`RWB E1 044 ... v1.md`); `requirement/RecoveryWorkbench_Requirements.md`; `.github/contexts/backend-context.md` §13, `testing-standards.md` TS-RCV-3/-4; INC-002 plan (`plan.md` §JaCoCo, `tasks.md` TASK-11) |
| ACE evidence (read-only) | `ace-monorepo` `develop` eedf5c75: `application.yaml` has three Flyway-relevant documents only (default: `enabled: true`, H2; `scb-aks` 221–245: `enabled: false`; `db-migrate` 264–303: `enabled: true`, `then-exit: true`, PostgreSQL `currentSchema=ace`, DEV database `scbaceseaapgdb001dev` as default host, location `db/migration-env/dev`); `AppConfig.java` 176–218 (`flywayMigrationStrategy`, `coreFlyway`, `coreFlywayMigrationInitializer`, all `@ConditionalOnProperty("spring.flyway.enabled")`). |
| Line endings | `requirement/Traceability_Matrix.md` is CRLF in the working tree and at HEAD; `git diff --stat` = 2 lines changed. |
| Overall status | **FAIL** |
| Blocking | **NO**: Low findings only (REVIEW-RWB-E1-044-011..-015). `REVIEW_GATE_WARNING` applies. |

## Summary

Both Medium findings of round 1 are closed in the artefacts. D-RCV-44 replaces the "runs in the build"
claim with an explicit run rule (before every MR touching recovery migrations or `RecoveryFlywayConfig`,
result in the implementation evidence, CI after Docker is confirmed), and the spec, Unit Test Applicability,
coverage table, CLAR-001 and card all say the same. The Product Owner re-confirmation that round 1 asked
for is not yet on Jira; it is tracked as OPEN-027 and tied to the Product Owner specification approval,
which is the correct gate for it. D-RCV-45 removes the recovery bean whenever `db-migrate` runs without
`db-migrate-recovery`; checked against `AppConfig` and `application.yaml`, this closes the ordering
dependency on the core `System.exit`, and T-044-15 proves it. All eight Low findings are fixed.

The fresh read found five Low items: stale status lines after remediation, card text that still promises
an environment drift gate, the DEV environment missing from the deployed-run rule, an unstated failure
mode of the migrate-and-exit runner, and `testing-standards.md` not carrying the D-RCV-44 run rule.

## Round 1 closure

| Finding | Severity | Closure | Evidence |
|---|---|---|---|
| REVIEW-RWB-E1-044-001 | Medium | **CLOSED** (spec content). Condition: OPEN-027 answered with the Product Owner specification approval. If the PO does not accept "before every MR", BR7 / CLAR-001 reopen. | D-RCV-44; `spec.md:53` BR7 row, `:57` Flow 4, `:145` UTA criteria, `:162` SPEC-012 run rule, `:165` SPEC-015 (c), `:225` CLAR-001; card `:41`, `:126`, `:154`; `open-items.md:26-27` OPEN-026/-027. "Runs in the build" no longer appears; `recoveryIntegrationTest` stays outside `check`, consistent with D-RCV-05. |
| REVIEW-RWB-E1-044-002 | Medium | **CLOSED** | D-RCV-45; `spec.md:154` SPEC-004 (d); `:206` T-044-15; `backend-apis.json` `activation.dbMigrateWithoutRecovery`. Checked: under `db-migrate,db-migrate-recovery` the profile file `application-db-migrate-recovery.yaml` sets `spring.flyway.enabled: false` and overrides the `db-migrate` document, so core beans are absent (T-044-12); under `db-migrate` alone the recovery bean is absent (T-044-15). No other ACE profile enables Flyway on PostgreSQL. |
| REVIEW-RWB-E1-044-003 | Low | **CLOSED** | Coverage table `:45-68` uses only `DIRECT` / `INHERITED_EXISTING_BEHAVIOR` and `COVERED`; X-paths split (`:63-64`); §13 step 2 relabelled `DIRECT` with out-of-scope note (`:61`); §10 Authority row (`:65`). |
| REVIEW-RWB-E1-044-004 | Low | **CLOSED** | Every SPEC row 001..019 names FR-RWB-020 and, where relevant, FR-RWB-001 / NFR-RWB-006; header `:19` lists D-RCV-40, -43..-46. |
| REVIEW-RWB-E1-044-005 | Low | **CLOSED** | `:145` UTA and `:165` SPEC-015 (d): test-scope class directory `recovery/casewf/internal/migration/**` minus `*Test`/`*IT`, consistent with D-RCV-43 and INC-002 TASK-11. |
| REVIEW-RWB-E1-044-006 | Low | **CLOSED** | `:195` T-044-03: `recovery` vs `rwb_it`, plus `Bad-Name` negative case. |
| REVIEW-RWB-E1-044-007 | Low | **CLOSED** | `:157` SPEC-007 scans dollar-quoted bodies; accepted gap limited to single-quoted literals; fixtures in T-044-05 (`:197`); contract CON-002 `forbidden` / `acceptedGap`. |
| REVIEW-RWB-E1-044-008 | Low | **CLOSED** (residual text in REVIEW-012) | Card `:41` superseded note, `:125-126` rollback and flag, `:154-155` status lines. |
| REVIEW-RWB-E1-044-009 | Low | **CLOSED** | D-RCV-46; card owners table `:92-105`; EPIC-001 owners table; OPEN-018 settled row. Consistent with INC-002, where the same person approved the spec as TechX PO. |
| REVIEW-RWB-E1-044-010 | Low | **CLOSED** | Matrix CRLF (diff = 2 lines); `open-items.md` settled table separator under header (`:31-32`); run log `:5` points to §6, which exists. |

## New findings

| ID | Severity | Location | Maps to | Issue | Required fix |
|---|---|---|---|---|---|
| REVIEW-RWB-E1-044-011 | Low | `spec.md:252-253` (Status reporting); `compliance-validation.md:84`; card `:146` | Gate checklist "re-read spec and compliance-validation"; traceability-standards | After remediation the spec's status block still says `REVIEW_STATUS: FAIL [MEDIUM: 2] [LOW: 8] — handoff blocked` and `NEXT_STEP: ... re-run Technical Specifier and the spec gate`, which no longer describes the state. `compliance-validation.md` §4 ends "Spec gate 2: result below." with nothing below. The card's evidence row "Review findings ... (TBC)" although `review/` now holds two reports. | Update the status block and §4 with this round-2 result, and the card's evidence row with both report paths. |
| REVIEW-RWB-E1-044-012 | Low | Card `docs/increments/INC-001-epic-1-RWB-E1-044.md:49` (business outcome), `:83-85` (story authority) | CLAR-001 A, CLAR-002 A; card vs spec consistency | The business outcome still says the story "fails the pipeline on drift" and measures "zero schema differences between a clean build and each environment at every release"; the authority table still says RW-PLATADM / DATASTEW / AUDIT read migration runs on SCR-44. After CLAR-001 A there is no environment comparison and no pipeline step; after CLAR-002 A there is no SCR-44 view. A reader of the card is told the story delivers what the PO parked. | Add the same "story text, superseded by ..." note used for the main flow (`:41`) to the business outcome and authority sections, naming CLAR-001 A / CLAR-002 A and D-RCV-44. |
| REVIEW-RWB-E1-044-013 | Low | `spec.md:155` SPEC-005, `:86` Triggers; `open-items.md` OPEN-019, OPEN-020; OPEN-013/-014 rulings | Story §3 ("parameter set per environment (DEV, SIT, UAT, PROD)"), §13 "Done when ... DEV and SIT"; BS-2.8, BS-2.9 | The deployed run rule, the Jenkins change and the DBA request cover SIT, UAT and PROD only. ACE has a deployed DEV database (`application.yaml` `db-migrate` document: DEV host `scbaceseaapgdb001dev`, location `db/migration-env/dev`; testing context lists DEV as an environment). The spec does not say how recovery migrations reach DEV: if DEV gets the same second Jenkins step, `createSchemas(false)` fails until someone creates schema `recovery` there; if DEV has no step, recovery tables never appear in DEV. | State DEV's route in SPEC-005 (same second step, or another named route) and extend OPEN-019 and OPEN-020 to DEV, or record why DEV is excluded. |
| REVIEW-RWB-E1-044-014 | Low | `spec.md:154` SPEC-004 (a), `:155` SPEC-005; `:204` T-044-12 | BR1, BR5; OPEN-013 ruling; X8 | SPEC-004 (a) makes a non-PostgreSQL data source skip the recovery bean with an INFO line. The spec does not say what the migrate-and-exit runner does under `db-migrate-recovery` when the recovery bean is absent (wrong data source, failed detection). If the runner is conditional on the bean, the Jenkins step can exit 0 with nothing migrated: a silent false success in SIT/UAT/PROD. | State that under `db-migrate-recovery` a missing recovery bean or non-PostgreSQL data source exits non-zero with a `MSG-P3-016` log line (fail fast; no H2 skip in the migration job). Add that negative case to T-044-12. |
| REVIEW-RWB-E1-044-015 | Low | `.github/contexts/testing-standards.md:147` TS-RCV-3 | D-RCV-44; OPEN-026 | D-RCV-44 sets a rule that binds every later recovery migration story (RWB-E1-042, -043, -001, ...): `recoveryIntegrationTest` runs before every MR touching recovery migrations or `RecoveryFlywayConfig`, with the result in the implementation evidence. TS-RCV-3 still says only that the task exists and Docker is open with K. Tee. Planners of later stories read the context, so the rule may not reach their plans. (Context files are not changed by this review.) | Context Updater adds the D-RCV-44 run rule and OPEN-026 to TS-RCV-3 (and backend-context §13 if it lists the test tasks). |

## Checks with no finding

| Check | Result |
|---|---|
| Change Scope Declaration | Unchanged and consistent: NEW_STORY, UI NO, Logic YES, API NO / NO_API_CHANGE; contracts agree. |
| Unit Test Applicability | Frontend NO / NOT_APPLICABLE with evidence; Backend YES / REQUIRED / 80% LINE, INSTRUCTION, BRANCH, METHOD; scope now includes test-scope tooling; references implementation-execution-gates; acceptance criteria include T-044-15 and the D-RCV-44 evidence rule. |
| Requirement coverage | BR1–BR7, flows, §10, §12–§14, guardrails, NFR-027 each map to SPEC items; allowed vocabulary only; no BLOCKED rows. |
| SPEC to FR/NFR | All 19 SPEC rows trace to FR-RWB-020 (plus FR-RWB-001 / NFR-RWB-006 where relevant). Matrix range row kept, as round 1 allowed. |
| D-RCV-44..46 | Recorded in the decisions register with decider, date, source finding and spec refs; new IDs continue from D-RCV-43 (squad numbering from D-RCV-38). |
| ACE footprint | `AppConfig`, `application.yaml` untouched; `build.gradle.kts` test scope only; new `application-db-migrate-recovery.yaml`; JaCoCo shape matches INC-002 TASK-11 (both merge orders handled). |
| Security, secrets, PII | No endpoint; DDL only for the migration-job account; `mainDataSource` reused; synthetic fixtures; no credentials or real data in any reviewed artefact. |
| Contracts | Valid JSON; `activation` mirrors SPEC-004 (a)–(d) and SPEC-005; CON-002 mirrors SPEC-006..-009. |
| Design evidence | `NOT_REQUIRED` with UI NO. |
| Clarifications | CLAR-001..010 RESOLVED; CLAR-001 records D-RCV-44 and OPEN-027. |

## Gate result

```text
REVIEW_STATUS: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 5]
REVIEW_BLOCKING: NO (Low only: REVIEW-RWB-E1-044-011..-015)
ROUND_1_CLOSURE: -001 CLOSED (condition: OPEN-027 answered with PO spec approval); -002..-010 CLOSED
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
NEXT_STEP: Human disposition of REVIEW-RWB-E1-044-011..-015 (fix or accept); Product Owner specification approval together with the OPEN-027 answer on Jira TB0001-1205. Then the human starts /planner INC-001-epic-1-RWB-E1-044.
```
