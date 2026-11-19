---

> Orchestrator note (19 Nov 2026, REVIEW-001 M-03/L-04): the E1-044 spec gate files predate the uniform gate line;
> the gate result is the reviewer's line "**Overall: PASS (0C / 0H / 0M / 0L)**" in this file. Where this file cites
> "build-log row 221", read the timeline row by its time instead; line numbers of the log change as rows are added.
title: "Spec gate review round 7: RWB-E1-044 (spec v14-7)"
run_id: INC-001-epic-1-RWB-E1-044
story: RWB-E1-044
gate: Specification (Compliance Reviewer, spec-gate mode)
round: 7 (round 1 is `spec-gate-review.md`, S01 to S11; round 2 `spec-gate-review-2.md`, S10 residual and S12 to S15; round 3 `spec-gate-review-3.md`, S16 to S19; round 4 `spec-gate-review-4.md`, S20 to S23; round 5 `spec-gate-review-5.md`, S24 to S26; round 6 `spec-gate-review-6.md`, S27 and S28)
date: 2026-11-18
result: PASS (0 Critical, 0 High, 0 Medium, 0 Low)
---

# Spec gate review round 7: RWB-E1-044

## 1. Scope

Reviewed, all under `aisdlc/output/INC-001-epic-1-RWB-E1-044/specify/`:

- `spec.md` v14-7. Every line changed since `spec.run6.md` was read in full: front matter, SPEC-002 (three bullets), SPEC-014 line 369, and the T-044-08 row. SPEC-002, SPEC-003, SPEC-014, the Trigger table, the Impacted Existing Nodes row, the Error table row for `rwb.schema`, the Unit Test Applicability backend row, CLAR-009 and Status were read again.
- `contracts/backend-apis.json` and `contracts/frontend-integrations.json`. Both parse as JSON and both are at `specVersion` `v14-7`. The only other change is `schemaPin`.
- `assumptions.md` (header only), `document-gaps.md` (unchanged since run 5), `shared-updates.md`, `compliance-validation.md`, `gate-response.md` (title, front matter and the "Round 6" section) and `agent-run-log.md` (the run 6 entry).
- The `*.run6.*` copies, used to see exactly what changed. The diff covers nothing outside the files and lines listed above.

Checked against:

- `review/spec-gate-review-6.md`: S27, S28 and the section 5 observations.
- The orchestrator's triage of review 6, as logged in `AI-SDLC-BUILD-LOG.md` row 2026-11-18T01:32:51 "RWB-E1-044 Gate triage, REMEDIATE (D-RUN-09)" and quoted in `gate-response.md` Round 6. These are orchestrator (Claude Code) rulings, not human ones. I checked how they were applied and did not reopen them.
- The RWB-TE-001 plan in `aisdlc/output/INC-002-epic-1-RWB-TE-001/plan/`:
  - `plan.md` line 143 (Relocation row for `RecoveryFlywayConfig`), line 163 (`RecoveryMigrationProperties(String schema, Flyway flyway)`, prefix `rwb`, `@EnableConfigurationProperties` on `RecoveryFlywayConfig`), line 192 (tooling include), and the "Coverage tests" row at line 210 for `casewf/migration/RecoveryFlywayConfigTest.java`;
  - `data-model.md` line 85;
  - `tasks.md` TASK-01, TASK-10 and TASK-12;
  - `tests/scenarios.md` T-TE001-12 and the "Coverage tests" note.

  The plan on disk is now **v2** (04:52, after plan-gate round 1). v1 is kept as `plan.run1.md`. I checked every cited line in both versions, and the cited content is the same in each (O-2).
- `aisdlc/output/INC-002-epic-1-RWB-TE-001/review/plan-gate-review.md`: round 1, FAIL, 0C/0H/0M/7L. None of PLAN-001 to PLAN-007 concerns the migration record, `RecoveryFlywayConfig` or its tests.
- The RWB-TE-001 v4 spec: SPEC-022 (with its Relocation table row `platform.internal.RecoveryFlywayConfig` → `casewf.migration`, P3, `pp`, line 211), SPEC-023, SPEC-024 and SPEC-025.
- `backend/build.gradle.kts`: Spring Boot plugin `4.1.2` (line 9), `spring-boot-starter-validation` as `implementation` (line 44) and `spring-boot-starter-validation-test` as `testImplementation` (line 75).
- `backend/src/main/resources/application.yaml`: `rwb.schema: recovery` is a literal at line 74 (no `${RWB_SCHEMA}` placeholder), and `hibernate.default_schema: ${rwb.schema}` is at line 23.
- `platform/internal/RecoveryProperties.java`. Today it has no validation annotations, and no `RecoveryFlywayConfigTest` exists yet.
- How Spring Boot 4.1.2 validates configuration properties. I read the bytecode (`javap`) of `spring-boot-4.1.2.jar` from the local Gradle cache: `ConstructorBound`, `ConfigurationPropertiesBinder`, `ValidationBindHandler` and its `ValidationResult`, `BindValidationException`, and `EnableConfigurationPropertiesRegistrar`. `hibernate-validator` 9.1.5.Final is in the same cache (see section 3).
- `AI-SDLC-BUILD-LOG.md` rows 217 to 222 and 235, for the rows the orchestrator says it added.
- `aisdlc/RUN-BRIEF.md`.

No git command, container or build was run. Only this file was written. Classes were extracted from the jar into the session scratchpad, not into the repository. No question was put to the user (L-RCV-03).

## 2. Round-6 findings

| Finding | Severity (round 6) | Status | Evidence |
|---|---|---|---|
| S27: SPEC-014 had the plan decide the build-file edit from "RWB-TE-001's merged filter" | Low | **CLOSED** | SPEC-014 line 369 now reads: "The plan states which case applies from RWB-TE-001's gated plan (its tooling include; …) The builder's first step confirms the case against the merged `build.gradle.kts` and stops and reports on a mismatch (Dependencies; ASM-E044-19)." That is the required wording, plus one added fact: plan v1 TASK-01 includes only `th/co/scb/ace/demo/recovery/architecture/boundary/**`, which does not take in this story's `architecture.migration` package (SPEC-016, line 402). I verified the fact in `tasks.md` TASK-01 and `plan.md` line 192, in both v1 and v2. SPEC-014 and Dependencies (line 75) now agree. No other part of SPEC-014 changed |
| S28 (1): `compliance-validation.md` cited "published sub-packages" for `casewf.migration` | Low | **CLOSED** | Row 55 now cites the RWB-TE-001 SPEC-022 Relocation table (`platform.internal.RecoveryFlywayConfig` to `casewf.migration`, P3, `pp`; verified at RWB-TE-001 spec line 211) and SPEC-025 (`casewf.migration` is not in the published list; verified at line 192). The quote is dropped |
| S28 (2): `shared-updates.md` card row 001 run label | Low | **CLOSED** | Row 001 now reads "remediation run 6, spec v14-7". Review 6 asked for "run 5", which was right for v14-6. This run bumped the spec to v14-7 (front matter line 6), and `gate-response.md` Round 6 explains the difference. The label matches the spec version, line 45 of the same file and the front matter, which is what the finding was about |

The round 6 section 5 observations were handled as follows:

- Plan start condition: build-log row 221 adds "Planner queued behind the TE-001 plan gate (D-RUN-17)".
- Build-log record of runs 4 and 5: rows 217 to 220 were added. See section 4 and O-1.
- Direct-call test against the compact constructor: settled by the `@Validated` choice. See section 3.
- Builder start condition: unchanged, and no change was needed.

## 3. Orchestrator triage of review 6: the `@Validated` choice

**Ruling.** Apply S27 and S28 as stated. The schema check must not break RWB-TE-001's `RecoveryFlywayConfigTest`: either take the `@Validated` option, or show with a citation that the test builds the record only with `recovery`. State the choice in the spec and test it.

**Applied.** The spec takes the `@Validated` option:

- SPEC-002 lines 151 to 153 state it.
- The "Why not a compact-constructor check" bullet withdraws the v14-6 constructor option and gives the reason.
- T-044-08 tests it in failing cases (1) to (4) and the new case (6).
- `schemaPin` in the contract says the same.
- `compliance-validation.md` row 56 traces it.

A search of the spec set for `compact`, `IllegalArgumentException`, "first option" and "either option" finds only the "Why not" bullet, so no text still offers the withdrawn option.

| Claim in the spec set | Checked against | Result |
|---|---|---|
| The RWB-TE-001 test calls `recoveryFlyway(...)` directly with a record it builds in code | RWB-TE-001 plan `plan.md` line 210 ("`recoveryFlyway(...)` called directly, `migrate` never called: schema and default schema, …"); S-TE001 SPEC-024 (line 191) "configuration built without running `migrate`"; `tasks.md` TASK-12 (the coverage methods, "mocks for JDBC … no database") | **Holds.** Same text in plan v1 and v2 |
| Neither the RWB-TE-001 plan nor its spec states the schema value that the direct-call test passes, so the citation route is not available | `plan.md` line 210 says only "schema and default schema". `data-model.md` line 85 gives `recovery` as the **bound** default, not a value for code-built records. SPEC-024 gives no value | **Holds.** The orchestrator's second option could not be met, so `@Validated` is the right choice |
| The record is `RecoveryMigrationProperties(String schema, Flyway flyway)`, prefix `rwb`, registered by `@EnableConfigurationProperties` on `RecoveryFlywayConfig` | `plan.md` line 163 | **Holds.** That registration is conditional, which is the case SPEC-002's first sub-bullet covers: E1-044 moves it to the unconditional class. Allowed change (2) under "Existing tests" covers the tests that then need the class |
| TASK-10 and T-TE001-12 binding tests stay green | `tasks.md` TASK-10 and `scenarios.md` T-TE001-12 bind from the real `application.yaml` through `ConfigDataApplicationContextInitializer`. `application.yaml` line 74 is the literal `recovery` | **Holds.** The constraint passes. At most allowed change (2) applies, and no assertion changes |
| `spring-boot-starter-validation` is already an `implementation` dependency, so no new dependency is added (AGENTS §4.4) | `build.gradle.kts` line 44. `hibernate-validator` 9.1.5.Final is in the Gradle cache | **Holds** |
| `@NotNull` plus `@Pattern(regexp = "recovery")` rejects null, blank and any other value, case-sensitive | Bean Validation: `@Pattern` treats null as valid, so `@NotNull` covers null. `@Pattern` matches the whole value with no flags, so the match is case-sensitive and anchored. Blank and `Recovery` fail | **Holds** |
| Spring Boot validates the record after binding, and a violation becomes a `BindValidationException` inside the configuration-properties bind failure | Boot 4.1.2 bytecode. `ConfigurationPropertiesBinder` adds a JSR-303 validator when `@Validated` is on the target and `ConfigurationPropertiesJsr303Validator.isJsr303Present(...)` is true, and it creates that validator itself, so no `ValidationAutoConfiguration` is needed in T-044-08's bare `ApplicationContextRunner`. `ValidationBindHandler` validates the constructed object in `onFinish` and throws `BindValidationException`. `Binder` wraps that in `BindException`. `ConstructorBound.from(...)` catches it and throws `new ConfigurationPropertiesBindException(bean, ex)`. The bean factory then wraps that in its creation exception | **Holds.** The chain is creation exception → `ConfigurationPropertiesBindException` → `BindException` → `BindValidationException`. `BindValidationException` is built from a message only, with no cause, so it is the root cause, as T-044-08 asserts |
| The `BindValidationException` message holds the field error on `schema`, the rejected value and the constraint message | `BindValidationException.getMessage(...)` builds "Binding validation errors on " + name, then `"%n   - %s"` for each error, using the error's `toString()`: object `rwb`, field `schema`, `rejected value […]`, codes (which include `rwb.schema`), and the default message. `ValidationBindHandler$ValidationResult.getActualFieldValue` reads the value from the handler's `boundResults`, so a record without a JavaBean getter still reports the rejected value | **Holds.** With the normative constraint message (SPEC-002 line 153: it names `rwb.schema` and D-RCV-28), the root-cause message names `rwb.schema`, the value found and `D-RCV-28` for cases (1) to (3), and `rwb.schema` and `D-RCV-28` for case (4) |
| Building the record in code is not affected | Bean Validation runs only through the binder. A record with no compact constructor runs no check | **Holds.** Case (6) (`rwb_case`, blank, null; nested value null; no context) guards against a constructor check being added later |
| `@Validated` on a `@ConfigurationProperties` record does not trigger method-validation proxying of a final class in the full application | `EnableConfigurationPropertiesRegistrar.registerMethodValidationExcludeFilter` registers `MethodValidationExcludeFilter.byAnnotation(ConfigurationProperties.class)` | **Holds.** No proxy is created. The spec does not need to say this; it is recorded here as evidence |
| `schemaPin` (contract) | `backend-apis.json` line 29: Bean Validation (`@Validated`; `@NotNull`, `@Pattern "recovery"` on `schema`) at binding, "not in its constructor", unconditional registration, failure names `rwb.schema`, the value and D-RCV-28 | **Holds.** Consistent with SPEC-002 and T-044-08. The JSON parses |

The T-044-08 cases still exercise the unconditional registration. Case (1) uses Flyway off, case (2) Flyway on with no `DataSource` (binding comes first), case (3) relaxed binding from the environment, case (4) a blank value, and case (5) the starting case. Their assertions changed only in naming the root-cause type. The Unit Test Applicability backend row still lists wrong and blank values with Flyway on and off. Coverage is unaffected, because annotations add no branch.

## 4. Build-log rows added by the orchestrator

| Row (time) | Content | Check |
|---|---|---|
| 217 (01:32:51) | Run 4 DONE: S20 to S23 fixed, paths aligned (D-RUN-17), CONTRADICTIONS 0 unresolved and 8 settled | Matches `agent-run-log.md` run 4 and `gate-response.md` Round 4 |
| 218 (01:32:51) | Round 5 FAIL 0C/0H/0M/3L: S24, S25, S26 | Matches `spec-gate-review-5.md` |
| 219 (01:32:51) | Run 5 DONE: "The one further round the 00:55 triage allowed the specifier under D-RUN-09"; S24 to S26 fixed; v14-6 | Matches the outputs. The stated basis for the extra round disagrees with `gate-response.md` Round 6. See O-1 |
| 220 (01:32:51) | Round 6 FAIL 0C/0H/0M/2L: S27, S28 | Matches `spec-gate-review-6.md` |
| 221 (01:32:51) | Gate triage, REMEDIATE (D-RUN-09): S27 and S28 as stated; `@Validated` or citation; re-gate as review-7; planner queued behind the TE-001 plan gate | Matches the triage quoted in `gate-response.md` Round 6 and `agent-run-log.md` run 6. Answers the round 6 queue observation |
| 222 (04:52:04) | About 01:37: "E1-044 run 6" among the agents stopped by HTTP 429; last writes 01:35 to 01:37 | Every run 6 output is dated 01:35 and complete: the diff is coherent, and `gate-response.md` Round 6 and the run 6 log entry are whole. See O-3 |
| 235 (04:54:35) | Run 6 DONE: S27, S28, `@Validated`, v14-7; "Gate round 7 running" | Matches the spec set |

All four missing rows that the orchestrator said it added (run 4, round 5, run 5, round 6) are present, along with the triage row. Rows 217 to 221 share the recording time 01:32:51 rather than each event's own time. Other batched rows in the log follow the same convention.

## 5. Regression check

| Item | Checked against | Result |
|---|---|---|
| D-RUN-17: TE-001 merges first; E1-044 is specified, planned and built against TE-001 v4's layout; code gate after the TE-001 merge | Dependencies (line 75), SPEC-001, SPEC-002, SPEC-014, SPEC-016, T-044-08, CLAR-008, ASM-E044-01, ASM-E044-19, contract `packageLayout` | **Holds.** No path changed. The new SPEC-014 sentence puts no merge-order condition on the plan and keeps the merged-code check at the builder's first step, as D-RUN-17 and round 5 require |
| D-RUN-14 | SPEC-017 R1 and R2, T-044-17 (a) to (f), OI-E044-I, OI-E044-J, DG-L13 | **Holds.** No diff in these lines, in `document-gaps.md` or in the OI rows |
| S20: status line reports unresolved contradictions | Status line 641 `CONTRADICTIONS: 0`, with the 8 settled listed | Unchanged |
| S21 (OI-E044-K under D-RUN-17), S22 (TE-001 SPEC-020 (b) owns the tooling wiring), S23 (key column in T-044-17 (f)) | SPEC-014 "Scope", "Withdrawn from v14-4", "Baseline and sequencing"; T-044-17 (f); SPEC-017 BR8 bullet | Unchanged. Only line 369 of SPEC-014 changed (S27) |
| S24: merged RWB-TE-001 tests, two permitted changes, SPEC-003 factory never migrates | SPEC-002 "Existing tests"; SPEC-003 lines 165 to 166 | Unchanged and still consistent. With `@Validated`, the direct-call methods need no change at all, and the binding methods need at most change (2) |
| S25: the plan works from TE-001's gated plan, and the builder confirms against merged code | Dependencies, SPEC-002, SPEC-014 lines 369, 377 and 383, ASM-E044-19 | **Holds**, and the S27 residual is now closed |
| S26: coverage baseline citation; Trigger row sub-package wording | SPEC-014 line 379; Trigger row (line 90) | Unchanged |
| Coverage gate (TE-001 SPEC-020 (a) to (d)) | SPEC-014, Unit Test Applicability, Verification table | Unchanged: one combined `BUNDLE` rule, four counters at 0.80, the whole main tree, `test` data only, outside `check`, no exclusion or waiver. Integration coverage is not substituted |
| D-RUN-07, -08, -09, -13; earlier triage | SEAM-E044-01 to -04, the no-waiver ruling, tokenizer, finding multiplicity | Unchanged. No regression in SPEC-003 to SPEC-013, SPEC-015 to SPEC-017, T-044-01 to T-044-22 (other than T-044-08 as reviewed) or the contracts |

Every ruling is attributed to the orchestrator (Claude Code). No human ruling is claimed (`gate-response.md` Round 6, `agent-run-log.md` run 6). No personal data appears in the spec set.

## 6. New findings

None. The next free ID is S29.

## 7. Observations (no change required for this gate)

- **O-1. For the orchestrator: build-log row 219 and `gate-response.md` disagree on what allowed the run 5 round.** Row 219 says run 5 was "the one further round the 00:55 triage allowed". `gate-response.md` Round 6 corrects its own Round 5 text: the extra round was allowed by the orchestrator's round 4 message to the stage, "not by the 00:55:29 log row". The 00:55:29 row (190) says only "re-gate as review-5". D-RUN-09 is the basis either way, and nothing in the spec depends on this. For one consistent record, reword row 219, for example: "the further round allowed by the orchestrator's round-4 message under D-RUN-09".
- **O-2. For the E1-044 planner: the RWB-TE-001 plan is now v2.** SPEC-002, SPEC-014 and `compliance-validation.md` cite "RWB-TE-001 plan v1" with line numbers. The plan on disk is v2 (04:52), and v1 is `plan.run1.md`. Every cited line (143, 163, 192, 210; TASK-01, TASK-10, TASK-12; T-TE001-12) has the same content in v2. "Not yet gated on 18 Nov 2026" is still true: plan-gate round 1 is FAIL (0C/0H/0M/7L) and none of its findings touches the migration record. The planner takes the version that passes the gate, as SPEC-002 and SPEC-014 already require.
- **O-3. For the orchestrator: the run 6 log entry does not mention the 01:37 usage-limit stop.** Build-log row 222 lists "E1-044 run 6" among the stopped agents. The run 6 outputs are complete and dated 01:35, so nothing was lost. The run 5 entry, by contrast, recorded the stop of run 4. A one-line note in the run 6 entry, or the next one, would keep the pattern.
- **O-4. For the E1-044 planner: T-044-08 row formatting.** Case (5) ends "… `RecoveryDatabaseIT` and T-044-10 start it", and **Direct construction case (6)** follows with no full stop. The meaning is clear. Add the full stop when the table is next edited.
- **O-5. For the orchestrator: cross-story finding RWB-TE-011 SG7-01 (Medium).** That finding, in `INC-006-epic-1-RWB-TE-011/review/spec-gate-review-7.md`, says RWB-E1-044's deliberately malformed test-fixture SQL would be scanned by the TE-011 lint when TE-011 merges. It is raised against the TE-011 spec, and its fix belongs there. If the TE-011 triage instead asks E1-044 to move or mark its fixtures, that becomes a change to this spec (SPEC-016 fixtures, T-044-22) and needs a re-gate.

## 8. Required checks

| Check | Result |
|---|---|
| Authentication and authorization | No endpoint is in scope (NO_API_CHANGE). The job-monitor read path, TC-E1-044-10 and the §10 read and rerun authority are out of scope by D-RCV-12 (DG-L10, OI-E044-G). Migration-account rights follow D-RUN-14 exactly |
| Customer and account data protection | Pass. Fixtures are synthetic. `rwb_migrator` cannot read ACE tables without `SET ROLE` (T-044-17 (d), (e)). The residual `SET ROLE` path is recorded (OI-E044-J) |
| Audit logging for sensitive financial actions | Not applicable. No case or decision change. The run record is the history table and the MSG-P3-016 ERROR line (ASM-E044-02, OI-E044-A) |
| KYC, AML, suitability, consent, approval | Not in scope |
| Frontend integration versioning and error contract | Not applicable to code (UI out of scope; NO_API_CHANGE). Both contract files parse at `v14-7` |
| Secrets and environment configuration | Pass. Migrator credentials come from the environment or key store. The schema pin is a Bean Validation constraint at binding and holds whether Flyway is on or off (unconditional registration; T-044-08 cases (1) to (5)). Its message holds no credential (SPEC-002) |
| Input validation | Pass. `rwb.schema` is validated with `@NotNull` and `@Pattern(regexp = "recovery")` at binding, and the start fails closed (T-044-08). Building the record in code is unaffected (case (6)) |
| Test coverage and evidence | Planned on RWB-TE-001's combined bundle (SPEC-020 (a), (b)): 80% LINE, INSTRUCTION, BRANCH and METHOD over the whole main tree with untested classes included and this story's tooling added, `test` data only, no waiver. Container tests T-044-10 to T-044-18 are kept apart. Merged RWB-TE-001 tests stay green with at most two named changes that weaken nothing. The baseline is recorded at the builder's first step |
| Frontend and backend applicability | Frontend `NOT_APPLICABLE` is justified (story v7 §15; no `frontend/` change). Backend is `REQUIRED` |
| Precedence and invented requirements | No invented financial, regulatory or security requirement. D-RUN-17, D-RUN-14 and the triage rows are applied as orchestrator rulings. All 13 DG rows are Blocker = No. The status line counts unresolved contradictions (0) |
| Personal data in artefacts | None. Roles are named by title. There are no personal names, IDs or account numbers |

## 9. Result

| Severity | Count | IDs |
|---|---|---|
| Critical | 0 | — |
| High | 0 | — |
| Medium | 0 | — |
| Low | 0 | — |

S27 and S28 are **CLOSED**. The orchestrator's round 6 triage is applied: the `@Validated` option is stated in SPEC-002, tested in T-044-08 (failing cases with `BindValidationException` as the root cause, plus direct-construction case (6)) and carried in the contract `schemaPin`. Its claims match the RWB-TE-001 plan (v1 and v2), the RWB-TE-001 v4 spec, `build.gradle.kts`, and Spring Boot 4.1.2's binder and validation code. D-RUN-14, D-RUN-17 and the S20 to S26 resolutions still hold. The build-log rows the orchestrator added are present, with one wording difference (O-1).

The specification is ready for the Implementation Planner. Under D-RUN-17 and build-log row 221, the planner starts once the RWB-TE-001 plan passes its gate.

**Overall: PASS (0C / 0H / 0M / 0L)**
