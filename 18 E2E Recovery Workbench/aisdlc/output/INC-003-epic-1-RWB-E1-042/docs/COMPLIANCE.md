---
title: "RWB-E1-042 Central configuration service and parameter catalog — compliance"
run_id: "INC-003-epic-1-RWB-E1-042"
story: "RWB-E1-042"
stage: "docs (final documentation)"
date: "2026-11-18"
status: "DOCUMENTED against branch tip 25c8f94; no approval recorded (D-RUN-09)"
---

# Compliance — RWB-E1-042

This file traces the story's requirements to the specification, plan, code and tests, using the run's
evidence only. Sections 2–8 carry `DOC-RWB-E1-042-016`..`-022`. It records no approval or acceptance
(D-RUN-09; OPEN-016).

## 1. Scope and sources

| Source | Version / location |
|---|---|
| Story | RWB-E1-042 story v7 (increment card `aisdlc/docs/increments/INC-003-epic-1-RWB-E1-042.md`) |
| Specification | `specify/spec.md`, rev 13, spec gate round 12 PASS |
| Plan | `plan/tasks.md` (TASK-00..TASK-25), `plan/tests/scenarios.md` (T-E1-042-01..-46), plan gate round 2 PASS |
| Code | Worktree `rwb-wt/RWB-E1-042`, branch `feature/RWB-E1-042-parameter-catalog`, tip `25c8f94` |
| Code units | `implement/traceability.md` (CODE-01..CODE-30) |
| Figures of record | `implement/code-gate-fix/test-and-coverage-counts.txt` |
| Document set | v14 (API Specification v4, Physical Schema v6, Error and Message Standard v4, Users, Roles and Permissions v4, Event and Messaging Design v4) |

## 2. Acceptance criteria trace

**DOC ID:** DOC-RWB-E1-042-016

| AC | Summary | SPEC | TC | Tests (class#method) | Result |
|---|---|---|---|---|---|
| AC1 | `case.entry.dpd` = 90 PROD v1 read on 2026-12-01 | 006, 007 | TC-01 | `ParameterConfigIT#prodContextReadsSeedVersionOne` | Pass |
| AC2 | Literal 90 in `casewf.casecreation` fails the build | 004 | TC-02 | `RwbMagicNumberCheckTest#literalNinetyFailsNamingFileLineAndKey` | Pass |
| AC3 | Uncatalogued `allocation.retry.limit` fails the build | 003 | TC-03, TC-21 | `CatalogCompletenessCheckTest#readsOfAnUncataloguedKeyFail`, `#readerCallCases`, `#productRowWithoutDefaultPassesAndWithoutOwnerFails` | Pass |
| AC4 | Required UAT key missing: readiness DOWN, MSG-P3-032 | 016, 022 | TC-04, TC-32 | `ParameterStartupCheckTest#downWhenNoValueInForceAndNoDefault`; `ParameterConfigIT#readinessIsDownNamingTheKeyAndEnvironmentWhenNoValueAndNoDefault` (DEV-11, DEV-16, DEV-20) | Pass |
| AC5 | 400 PROD refused MSG-GEN-002 min 1 max 365 | 012, 025 | TC-05 | `ParameterLoadValidatorTest#outOfRangeRefusesWithGen002`; `ParameterConfigIT#loadOutOfRangeIsRefusedWhole` | Pass |
| AC6 | "ninety" refused MSG-P1-002 | 012, 025 | TC-06 | `ParameterLoadValidatorTest#wrongTypeRefusesWithP1002`; `ParameterConfigIT#loadWrongTypeIsRefusedWhole` | Pass |
| AC7 | Author approves own load: MSG-P7-002 | 014 | TC-07 | `ParameterLoadHandlerTest#authorCannotApprove`; `ParameterConfigIT#authorApproveIsRefused` | Pass |
| AC8 | SIT 30, PROD 300, each environment its own | 008, 012, 014 | TC-08 | `ParameterConfigIT#eachEnvironmentResolvesItsOwnValue` | Pass |
| AC9 | `ace.db.password` listed, no value | 010, 011 | TC-09 | `ParameterServiceTest#secretIsNeverServed`; `ParameterConfigIT#secretIsListedWithoutValue` | Pass |
| AC10 | Rollback of v2 puts v1 in force | 015 | TC-10 | `ParameterValidityTest#recomputeMakesTheEarlierVersionInForce`; `ParameterConfigIT#rollbackRestoresTheEarlierVersion`, `#failedRollbackCommitLeavesTheRowsApproved` (DEV-20) | Pass |
| AC11 | v2 = 91 from 2026-12-10: 90 on 12-09, 91 on 12-10, no restart | 007, 009, 014 | TC-11 | `ParameterCacheTest#aVersionStartsOnItsValidFromWithNoRestart`; `ParameterConfigIT#futureVersionStartsOnItsDate` | Pass |

Every AC has at least one passing test at `25c8f94`. Method names follow `plan/tests/scenarios.md`
except where DEV-20 maps a planned name to the test that ran.

## 3. Business rules, exceptions and guardrails

**DOC ID:** DOC-RWB-E1-042-017

| Rule | SPEC | TC | Status |
|---|---|---|---|
| BR1 No changeable business value as a constant | 004–007 | TC-01, -02, -25, -26, -42, -43 | Covered |
| BR2 Every parameter in use is catalogued | 003, 005 | TC-03, -21, -41 | Covered |
| BR3 A value changes only through a checked, approved, dated load | 012–015 | TC-05..-07, -16..-19, -23 | Covered |
| BR4 Author cannot approve (Risk approval: RWB-E1-043 / RWB-E1-037) | 014 | TC-07 | Covered (author rule); approver role out of scope |
| BR5 Every read returns `versionNo` | 007, 009 | TC-01, -11 | Covered |
| BR6 Secrets listed, never held | 002, 003, 010 | TC-09, -44 | Covered |
| BR7 No start without required parameters | 016 | TC-04, -32 | Covered (readiness DOWN, CLAR-012) |
| X1–X8, X10 | 003, 004, 010, 012, 014–016 | TC-02..-11 | Covered |
| X9 Role without Rules and parameters R: 403 MSG-P4-002 | 011, 020 | TC-24 (seam); **TC-12 Blocked** | Seam covered; live case Blocked (OI-E1-042-001) |
| GR1 No business value in code | 004 | TC-02, -25 | Covered |
| GR2 No personal data, no secret value | 010, 027 | TC-09, -28, -29, -30 | Covered |
| GR3 No read of another module's tables; P3 through `ParameterService`, others through `CatalogParameterReader` | 026 | TC-45, -46 | Covered (D-RUN-19 unratified, OPEN-050) |
| GR4 A value change needs no deployment | 003, 009, 012 | TC-11, -16 | Covered |

## 4. SPEC → TASK → CODE → test

**DOC ID:** DOC-RWB-E1-042-018

| SPEC | Subject | TASK | CODE | TC |
|---|---|---|---|---|
| 001 | One migration `V<seq>__rwb_e1_042_parameter_catalog_and_seed.sql` | 14, 15 | 16 | 13, 14, 15 |
| 002 | Table shapes (Physical Schema v6) + three columns | 14 | 16, 24 | 13, 14, 27 |
| 003 | `CatalogCompletenessCheck` | 02, 04, 05 | 01, 03, 04, 05 | 03, 21, 41, 44 |
| 004 | `RwbMagicNumberCheck` | 02, 04, 05 | 02, 05, 30 | 02, 25, 43 |
| 005 | Generated `ParameterKeys` | 06, 07 | 06, 07, 08, 18, 20 | 26, 27, 42 |
| 006 | Seed rows | 14, 15 | 16 | 13, 27 |
| 007 | `ParameterService.get` | 16, 17 | 10, 17, 18, 24 | 01, 11 |
| 008 | Environment resolution | 17 | 17 | 08 |
| 009 | Per-instance cache, date resolved on read | 17 | 19 | 11, 28 |
| 010 | Secrets never served | 17 | 17 | 09 |
| 011 | `GET /admin/parameters` | 16, 17 | 21, 24 | 09, 31, 34 |
| 012 | Load checks | 18, 19 | 01, 25, 28 | 05, 06, 23 |
| 013 | Idempotency and content hash | 18, 19 | 24, 26, 28 | 16, 17, 33 |
| 014 | Approve | 18, 19 | 25, 27, 28 | 07, 20, 36, 38 |
| 015 | Rollback | 18, 19 | 25, 27, 28 | 10, 18, 19, 37, 39 |
| 016 | `ParameterStartupCheck` readiness | 16, 17 | 20, 22 | 04, 32 |
| 017 | `ParameterLoadHandler` published | 09, 19 | 10, 11, 28 | 35, 40 |
| 018 | `ParameterVersionApproved` after commit | 19 | 11, 19, 28 | 28 |
| 019 | `VersionDecisionRecorder` "AC-VERS" | 19 | 28, 29 | 29 |
| 020 | `CapabilityCheck` method check | 13 | 12, 15, 21 | 24 (12 Blocked) |
| 021 | Flag `rwb.p3.configservice` | 17, 21 | 30 | 22 |
| 022 | `MessageResolver`, `FixedMessageCatalog` | 11 | 12, 13, 14, 17 | 30 |
| 023 | `BusinessDateProvider` | 17 | 10, 17, 20, 23 | 23, 46 |
| 024 | D-RCV-36 keys | 03, 17 | 04, 07, 17 | 26, 27 |
| 025 | RFC 7807 problems via `ApiProblemException` | 11, 17 | 13, 21 | 05, 06, 29, 30, 34 |
| 026 | Module placement | 08, 09, 17 | 09, 10, 12, 23 | 45, 46 |
| 027 | No personal data, no secret | 11, 19 | 13, 29 | 28, 29, 30 |

TASK numbers are from `plan/tasks.md`; CODE numbers from `implement/traceability.md`; TC numbers are
`TC-E1-042-nn`. The SPEC column is `SPEC-RWB-E1-042-nnn`. Where `implement/traceability.md` and this
table differ, the traceability file is the source (it is the builder's record).

## 5. Tests and coverage (figures of record)

**DOC ID:** DOC-RWB-E1-042-019

| Suite | Count | Failures / errors / skipped | Source |
|---|---|---|---|
| Unit (`test`) | 388 tests, 44 classes | 0 / 0 / 0 | `code-gate-fix/test-and-coverage-counts.txt` |
| Container (`recoveryIntegrationTest`) | 59 tests (`ParameterConfigIT` 33, `$FlagOff` 4, `ParameterMigrationIT` 4, `RecoveryMigrationIT` 12, `RecoveryDatabaseIT` 6) | 0 / 0 / 0 | same |
| API (`apiTest`, API Tester run5) | 13 (`ParameterApiContractIT` 12 + `$FlagOff` 1) | 0 / 0 / 0 | `api-tests/report.md`, `evidence/apiTest-run5.log` |

| JaCoCo counter (`recoveryCoverageReport.xml`) | Covered / total | % | Threshold |
|---|---|---|---|
| LINE | 2579 / 2833 | 91.0 | 80 |
| INSTRUCTION | 14045 / 15482 | 90.7 | 80 |
| BRANCH | 1289 / 1594 | 80.9 | 80 |
| METHOD | 552 / 576 | 95.8 | 80 |

All four counters meet the 0.80 BUNDLE rule. The round 3 and round 4 code gates recomputed the counts from the
native XML and found the same figures. Frontend: not applicable (no screen in this story).

## 6. Reviews and gates

**DOC ID:** DOC-RWB-E1-042-020

| Gate | Round | Result | Findings |
|---|---|---|---|
| Spec gate | 12 | PASS | — |
| Plan gate | 2 | PASS | — |
| Security review | 2 | PASS | SEC-042-01..04 addressed in the review-fix round (DEV-13..DEV-18) |
| Ponytail review | 2 | Ship | — |
| Code gate | 1 | FAIL | CODE-001 (identical repeat of an APPROVED load answered 409); fixed at `9056ed2` |
| Code gate | 2 | FAIL 0C/0H/0M/3L | CODE2-001 (missing TC-20/-22/-23 container tests), CODE2-002 (duplicate DEV-13), CODE2-003 (stale Javadoc); fixed at `25c8f94` |
| Code gate | 3 (`review/code-gate-review-3.md`) | FAIL 0C/0H/0M/1L | CODE3-001 (Low): six planned test names in `scenarios.md` had no rename note; fixed by DEV-20 (rename table in `implement/deviations.md`) |
| Code gate | 4 (`review/code-gate-review-4.md`) | **PASS 0C/0H/0M/0L** at `25c8f94` | CODE3-001 closed by DEV-20 and re-reviewed |

**Gate history.** Round 1 FAIL 0/1/0/2, round 2 FAIL 0/0/0/3, round 3 FAIL 0/0/0/1, round 4 PASS
0/0/0/0 (Critical/High/Medium/Low). Each FAIL round was fixed and re-gated; no finding was accepted.
The PASS is a review result, not an approval: human sign-off is still not recorded (OPEN-016).

## 7. Deviations

**DOC ID:** DOC-RWB-E1-042-021

| DEV | Summary | File |
|---|---|---|
| DEV-01 | No JPA entity/repository for `parameter_catalog` (no code reads it) | `implement/deviations.md` |
| DEV-02 | No `@ApplicationModule` on `casewf/config/package-info.java` | same |
| DEV-03 | Published set also lists `ParameterVersionApproved$Version` | same |
| DEV-04 | `config.api` named interface asserted as a bounded subset | same |
| DEV-05 | `ModuleMapLoaderTest#loadsTheRealMap` also gains `config.api` | same |
| DEV-06 | `ApiExceptionHandler` takes `ObjectProvider<MessageResolver>` | same |
| DEV-07 | `kind()`, `scope()`, `valueSource()` return `String` tokens | same |
| DEV-08 | afterCommit synchronization instead of `@TransactionalEventListener(AFTER_COMMIT)` | same |
| DEV-09 | `ParameterCatalogControllerTest` is a `@WebMvcTest` with method security | same |
| DEV-10 | TC-34 system assertion covered by MockMvc test, not a container test | same |
| DEV-11 | TC-04/TC-32 readiness with removed default covered at unit level | same |
| DEV-12 | One results row per surface; frontend NOT_APPLICABLE | same |
| DEV-13 | Native `pg_advisory_xact_lock` query in main code | `implement/review-fix/deviations-review-fix.md` |
| DEV-14 | GET answers 422 MSG-GEN-002 for an unknown environment | same |
| DEV-15 | Six credential words beyond spec §7.1's eleven | same |
| DEV-16 | Real readiness-group assertion replaces `readinessIsUpOnTheSeededCatalog` | same |
| DEV-17 | Flag-off GET 404 body not asserted (RWB-E1-043 owns it) | same |
| DEV-18 | Generator accepts `-PparameterCatalog=<path>` | same |
| DEV-19 | Check 11 runs before check 12 inside the load transaction | `implement/deviations.md` |
| DEV-20 | Planned test names mapped to the tests that ran (closes CODE3-001; re-reviewed in code gate round 4) | same |

The builder states that none of DEV-01..DEV-20 lowers a coverage counter, removes or skips a test, or
relaxes an assertion. The deviation set is DEV-01..DEV-20.

## 8. Open items and statement

**DOC ID:** DOC-RWB-E1-042-022

| Item | Subject | Blocker |
|---|---|---|
| TC-E1-042-12 | Live X9 case Blocked until RWB-E1-022 (identity) and RWB-E1-037 (matrix PM-2026.11); OI-E1-042-001 | No |
| OI-E1-042-002 | Story's two-file migration names; spec uses one `V<seq>` file | No |
| OI-E1-042-003 | Full Epic 1 catalog absent; 19-row bootstrap | No |
| OI-E1-042-004 | No message table or owner; `FixedMessageCatalog` interim | No |
| OI-E1-042-005 | No per-table-code CSV template register | No |
| OI-E1-042-006 | Key naming conflicts (`case.entry.dpd` vs others) | No |
| OI-E1-042-007 | PRODUCT rows have no default | No |
| OI-E1-042-008 | Three added `parameter_value` columns; Physical Schema update requested | No |
| OI-E1-042-009 | `recoverySchema` placeholder property | No |
| OI-E1-042-010 | PRODUCT target table, `DOCUMENT_HUB_PARAMETER`, `RETENTION_CLASS` dispatch | No |
| OI-E1-042-011 | Reference-load OpenAPI hardening; identical-repeat response not in API v4 | No |
| OI-E1-042-012 | Modulith event-publication table absent from Physical Schema v6 (DEV-08) | No |
| OI-E1-042-013 | Modulith 2.1.1 does not surface the nested named interface (DEV-04) | No |
| DG-E042-ENV-422 | 422 on GET not declared in API v4 | No |
| OPEN-016 | Per-story approver names not available; no human sign-off recorded | No (recorded) |
| OPEN-050 | D-RUN-18, -19, -20, -21 are orchestrator decisions, not ratified | No |
| Known evidence issues | CODE-08 "11 constants" vs 19; `implement/shared-updates.md` §5 lock text and §2 path; stale merge-gate logs (see `document-gaps.md` §3; builder files not edited) | No |

**Statement.** This file records the evidence. It does not approve, accept or sign off the story, the
code or any gate (D-RUN-09). Merge needs a named human reviewer (AGENTS.md §8, §9).
