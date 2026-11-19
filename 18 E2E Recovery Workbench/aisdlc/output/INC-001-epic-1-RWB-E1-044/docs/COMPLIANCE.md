---
title: "RWB-E1-044 Database migrations versioned with parameterized schema names — compliance record"
run_id: "INC-001-epic-1-RWB-E1-044"
story: "RWB-E1-044"
stage: "docs (final documentation)"
date: "2026-11-18"
status: "DOCUMENTED — code gate PASS; no merge, human approval or release claimed"
---

# Compliance record — RWB-E1-044

Sections 2–7 carry `DOC-RWB-E1-044-013`..`-018`; §1 is their shared scope statement.

This record states what the story demonstrates and with which evidence. It is written after the code
gate passed (`../review/code-gate-review.md`, final verdict PASS 0 Critical / 0 High / 0 Medium /
0 Low at `89477bc`). It adds no new review and claims no approval.

## 1. Scope of this record

| Field | Value |
|---|---|
| Story | RWB-E1-044 Database migrations versioned with parameterized schema names, EPIC-001, build order 1 |
| Module | P3 Case and workflow (`casewf.migration`); test scope `architecture.migration` |
| Acceptance basis | AC1–AC9 and BR1–BR8 of story files v7, as restated in spec v14-7 |
| Change classification | `ENHANCEMENT_LOGIC_ONLY`; UI In Scope `NO`; API In Scope `NO`; `NO_API_CHANGE` |
| Runtime behaviour added | A start-up schema pin, a failure-reporting runner, and the inherited Flyway bean with `validateOnMigrate(true)` |
| Production migration | **None** (D-RCV-28; story v7 §13; D-RUN-07) |
| Personal data | None. Fixtures use synthetic names (`queue`, `timer`, `account_key`, `team_code`, `note_x`); no customer, account, card or address data |
| Banking compliance documentation | Not required: no customer data, financial value, holdings or account field is handled by this story |

## 2. Acceptance criteria trace

**DOC ID:** DOC-RWB-E1-044-013 · **Maps to:** AC1–AC9; SPEC-RWB-E1-044-001..-013, -017; T-044-01..-22; TASK-03..-14

| AC | Requirement (story v7, restated in spec v14-7) | SPEC | TASK | Test evidence | Result |
|---|---|---|---|---|---|
| AC1 | Fixture `V<seq>__rwb_e1_044_add_queue.sql` applies once; its version and checksum are in `flyway_schema_history_recovery`; a rerun applies nothing | SPEC-001, -011 | TASK-10, -14 | `RecoveryMigrationIT.appliesOnceAndARerunAppliesNothing` (T-044-10) | **PASS** |
| AC2 | A drift between the migration result and a target fails with `MSG-P3-016` naming `<schema>.<table>.<column>`; here a container-to-container check | SPEC-012 | TASK-05, -06, -14 | `RecoveryMigrationIT.driftComparisonFindsExactlyTheHandMadeColumn` (T-044-15, exactly `recovery.queue.note_x`); `SchemaComparatorTest` (T-044-19) | **PASS** |
| AC3 | The same fixture creates `recovery.timer` in two clean databases; the recorded checksums are equal | SPEC-001, -002, -007, -011 | TASK-08, -14 | `RecoveryMigrationIT.theSameFixtureCreatesTheTimerInTwoDatabasesWithEqualChecksums` (T-044-11); `MigrationPropertiesConfigTest` case (5) (T-044-08) | **PASS** |
| AC4 | `V0001` applied, then the file changed: migrate fails validation, the ERROR line names the version, the context does not start | SPEC-001, -003, -011 | TASK-10, -14 | `RecoveryMigrationIT.aChangedAppliedFileFailsValidationAndNamesTheVersion` (T-044-12); `RecoveryMigrationRunnerTest.aValidationFailureNamesTheInvalidVersionAndRethrows` (T-044-09) | **PASS** |
| AC5 | Fixture line 2 `CREATE INDEX ix_a ON recovery.queue (team_code)` gives `MSG-P3-016 … object=<file>:2 rule=L-LITERAL-SCHEMA` | SPEC-004, -007, -010 | TASK-03, -04 | `RecoveryMigrationLintTest.findingsUseTheMessageP3LineFormat` asserts the line-2 literal-schema finding on fixture `t06-format-fail` (`object=V0002__rwb_e1_044_ok.sql:2 rule=L-LITERAL-SCHEMA`); every object-name position and qualified type is covered by `t02-positions-fail`, `t02-types-fail`, `t02-schema-bare-fail` (T-044-02) | **PASS** |
| AC6 | Two non-fix files with key `rwb_e1_028` give one `L-KEY-DUP` finding naming both files and `RWB-E1-028` | SPEC-004, -006, -010 | TASK-03, -04 | Fixture `t03-keydup-fail` (T-044-03) | **PASS** |
| AC7 | `clean()` is refused with Flyway's message; a `U0001__…sql` file gives `L-UNDO` | SPEC-001, -005, -011, -013 | TASK-04, -10, -14 | `RecoveryMigrationIT.cleanIsRefusedAndAChangedDatabaseIsNotTouched` (T-044-13); fixture `t01-undo-fail` (T-044-04) | **PASS** |
| AC8 | A fixture whose second statement fails: the first statement's object is absent, no history row, the ERROR line names the version, the context does not start | SPEC-003, -011 | TASK-10, -14 | `RecoveryMigrationIT.aMigrationThatFailsPartWayRollsBackAndNamesItsVersion` (T-044-14); `RecoveryMigrationRunnerTest.aMigrationThatFailsPartWayNamesItsPendingVersion` (T-044-09) | **PASS** (the job-monitor display is out of scope, D-RCV-12) |
| AC9 | Two contexts migrate concurrently with one pending fixture: one history row and both start | SPEC-011 | TASK-14 | `RecoveryMigrationIT.twoContextsMigratingAtOnceApplyTheVersionOnceAndBothStart` (T-044-16) | **PASS** |

Story test cases map to spec tests as `TC-E1-044-01` → T-044-10, `-02` → T-044-15/-19, `-03` →
T-044-11/-08, `-04` → T-044-12/-09, `-05` → T-044-02/-06, `-06` → T-044-03, `-07` → T-044-13/-04,
`-08` → T-044-14/-09, `-09` → T-044-16. `TC-E1-044-10` (RW-CASEOWN refused with `MSG-P4-002`) is
out of scope with no named owner (D-RCV-12; OI-E044-G).

The rest of the test set supports the ACs and is green: T-044-01 and -03–-07 (lint fixtures and
format), T-044-08 (schema pin, six cases), T-044-17 (D-RUN-14 rights and the FK refusal), T-044-18
(baseline at 0), T-044-20 (search path and GRANT/REVOKE), T-044-21 (literals and comments are not
schema references), T-044-22 (the 15 adversarial tokenizer cases plus statement-view S1).

## 3. Business rules and decisions trace

**DOC ID:** DOC-RWB-E1-044-014 · **Maps to:** BR1–BR8; D-RCV-28, D-RUN-13, D-RCV-48; NFR-027, NFR-052; SPEC-001..-017; TASK-03..-19

| ID | Rule (story v7; spec v14-7 requirement rows) | SPEC | TASK | Test evidence | Result |
|---|---|---|---|---|---|
| BR1 | A pending migration applies once; version and checksum are recorded | SPEC-001, -011 | TASK-10, -14 | T-044-10 | **PASS** |
| BR2 | The schema comes from a parameter; the same file produces the table in schema `recovery` in two databases | SPEC-001, -002, -007, -011 | TASK-08, -14 | T-044-11 (equal checksums); T-044-08 (pin) | **PASS** |
| BR3 | One non-fix file per story key; the header carries the key | SPEC-004, -006, -010 | TASK-03, -04 | `t03-keydup-fail`, `t03-header-fail`, `t03-header-multi-fail`; `t01-nonsql-fail` (T-044-03) | **PASS** |
| BR4 | Forward only: no clean, no undo file, no repeatable file | SPEC-001, -005, -011, -013 | TASK-04, -10, -14 | `t01-undo-fail`, `t01-repeatable-fail` (T-044-04); T-044-13 (clean refused, objects unchanged) | **PASS** |
| BR5 | An applied migration edited later fails validation and the service does not start | SPEC-001, -003, -011 | TASK-10, -14 | T-044-12; T-044-09 | **PASS** |
| BR6 | The recovery module has its own history table | SPEC-001 | TASK-08, -10, -14 | `HISTORY_TABLE` constant; T-044-10 reads `flyway_schema_history_recovery`; inherited `RecoveryFlywayConfigTest` assertion | **PASS** |
| BR7 | Drift between the migration result and a target is reported per object | SPEC-012 | TASK-05, -06, -14 | T-044-15; T-044-19 | **PASS** |
| BR8 | No foreign key outside schema `recovery` | SPEC-008, -010, -017 | TASK-03, -04, -11, -12 | `t05-fk-public-fail` (one `L-FK-OUTSIDE` + one `L-LITERAL-SCHEMA`), `t05-fk-pgcatalog-fail`, `t05-fk-split-fail`, `t05-fk-pass` (T-044-05); `RecoveryMigrationIT.migratorRightsAreExactlyTheTwoDRun14RightsAndAnForeignKeyIntoPublicIsRefused` (T-044-17 (f): SQLSTATE `42501`, no history row) | **PASS** |
| D-RCV-28 (1) | Name pattern, contiguous sequence, one non-fix per key, fix rule, no `R__` | SPEC-005, -006 | TASK-03, -04 | `t01-*` and `t03-*` fixtures (T-044-01, -03) | **PASS** |
| D-RCV-28 (2) | Literal schema qualifiers and every `search_path` form are refused | SPEC-007 | TASK-02, -03, -04 | `t02-*`, `t20-searchpath-fail`, `t21-*` (T-044-02, -20, -21) | **PASS** |
| D-RUN-13 | Only identifiers are checked; strings and comments are ignored | SPEC-007, -008 | TASK-02, -03, -04 | `t21-literals-pass`, `t21-literal-negatives-fail`, adversarial N1–N15/P1–P3 (T-044-21, -22) | **PASS** |
| D-RCV-48 | First migrate on a non-empty schema baselines at 0 and applies `V0001` | SPEC-001, -011 | TASK-14 | `RecoveryMigrationIT.aNonEmptyRecoverySchemaWithoutHistoryBaselinesAtZeroAndAppliesTheFirstVersion` (T-044-18) | **PASS** |
| NFR-027 | Rollback by redeploying the previous tag | SPEC-013 | TASK-10, -14 | `cleanIsRefusedAndAChangedDatabaseIsNotTouched`; `aPreviousTagStartsAgainstALaterDatabaseAndAppliesNothing`; `aLowerPendingVersionFailsWithItsVersion` (T-044-13) | **PASS** |
| NFR-052 / BS-4.5 | Migration credentials stay outside the repository | SPEC-001 | TASK-08, -10 | `rwb.flyway.user/password` from environment or key store; runner test asserts the line holds no SQL or credential (T-044-09); code-gate "No PII/credential" check | **PASS** |
| MSG-P3-016 | Drift, checksum mismatch, lint failure, refused clean or undo, failed migration | SPEC-003, -004, -012, -013 | TASK-02, -04, -10 | `MigrationFinding.format()`; runner tests; T-044-06, -09, -12, -14. Refused clean uses Flyway's own message (DG-L11) | **PASS** |

Story §10 authority, §12 `GET /admin/jobs?type=MIGRATION`, §14 `MSG-P4-002`, §15 SCR-44 and
TC-E1-044-10 are mapped to **SPEC-017 out of scope by decision D-RCV-12** with no owner inferred
(OI-E044-G). Deployment by RW-PLATADM is a pipeline action outside this repository. TASK-19 checked
that none of that work was built. This is a recorded exclusion, not a passing test.

## 4. Coverage evidence (80% × 4)

**DOC ID:** DOC-RWB-E1-044-015 · **Maps to:** SPEC-RWB-E1-044-014; TASK-13, TASK-17; D-RUN-17; OI-E044-K (closed)

The gate is one `BUNDLE` in `recoveryCoverageVerification` over:

- every main class under `th/co/scb/ace/demo/recovery/**` (untested classes included);
- RWB-TE-001's test-scope boundary tooling;
- this story's `architecture/migration/**` test-output classes.

Only `*Test` and `*IT` classes are excluded from the tooling directories. **No main class is
excluded, no threshold is lowered and no waiver is used.** Execution data is the `test` task only.

| Metric | Covered | Missed | Total | Ratio | Required | Result |
|---|---|---|---|---|---|---|
| LINE | 1333 | 73 | 1406 | 0.9481 (94.81%) | 0.80 | **PASS** |
| INSTRUCTION (statements) | 7091 | 432 | 7523 | 0.9426 (94.26%) | 0.80 | **PASS** |
| BRANCH | 630 | 102 | 732 | 0.8607 (86.07%) | 0.80 | **PASS** |
| METHOD (functions) | 339 | 7 | 346 | 0.9798 (97.98%) | 0.80 | **PASS** |

| Evidence | Detail |
|---|---|
| Command | `./gradlew test recoveryCoverageVerification` from `backend/`, exit 0 |
| Unit suite | 243 passed, 0 failed, 0 skipped, 27 classes |
| Native report | `../implement/code-gate-fix/recoveryCoverageReport.xml`; `../implement/code-gate-fix/unit-coverage.log` |
| Container suite (separate, not coverage) | 18 passed (12 `RecoveryMigrationIT` + 6 `RecoveryDatabaseIT`), 0 failed, 0 skipped, `../implement/review-fix/it.log` |
| Frontend | `NOT_APPLICABLE` for this story: UI In Scope NO, no `frontend/` file changed. `npm run check` still ran in the merge gate: 28 tests, thresholds met (`../implement/merge-gate.log`) |

**Baseline and sequencing.** The 17 Nov 2026 recovery main scope was below 80% (LINE 133/415,
BRANCH 25/92, INSTRUCTION 686/2174, METHOD 41/135) from classes this story does not change. D-RUN-17
merged RWB-TE-001 first, and its coverage tests lift that scope before this story's code gate; the
pre-flight recorded the merged baseline (LINE 0.9746, INSTRUCTION 0.9731, BRANCH 0.9531,
METHOD 0.9791). OI-E044-K is closed by D-RUN-17. The seven uncovered methods are record accessors and
one runner/reader branch; all four counters are above the gate.

## 5. Reviews and the dynamic-SQL gap

**DOC ID:** DOC-RWB-E1-044-016 · **Maps to:** SPEC-RWB-E1-044-003, -009; TASK-18, TASK-19; DG-E044-DYN-01

### 5.1 Gates

| Gate | Result | Reference |
|---|---|---|
| Spec gate, round 7 | **PASS** 0 Critical / 0 High / 0 Medium / 0 Low; 28/28 requirement rows; 9 ACs, 8 BRs | `../review/spec-gate-review-7.md` |
| Plan gate, round 2 | **PASS** 0/0/0/0; PLAN-001..PLAN-008 closed; 20 tasks TASK-00..-19; every SPEC-001..-017 mapped | `../review/plan-gate-review-2.md` |
| Code gate, final | **PASS** 0/0/0/0 at `89477bc`; CODE-001..003 closed and verified; no test weakened | `../review/code-gate-review.md` |
| Security review | **PASS** after fixes: 0 Critical / 0 High / 0 Medium / 0 Low / 2 Informational | `../review/security-review.md` |
| Ponytail review | **Ship**; Must/Should/Nice closed except the view-column-type follow-up (Nice 9) | `../review/ponytail-review.md` |

The code gate first returned `PASS_WITH_WARNINGS` 0/0/0/3 and carried the Low-severity warning text.
Its three Lows were fixed at `89477bc` and re-verified:

| Finding | What it was | Disposition |
|---|---|---|
| CODE-001 | The SPEC-016 seam received `null` for a qualifier on a later line of a multi-line statement | Fixed: `statementAt` selects by identifier-view offset range; new multi-line test; no lint result changed |
| CODE-002 | `implement/unit-tests/report.md` still showed the first-round 239-test run | Fixed: refreshed to the final 243-test run with the code-gate-fix counters |
| CODE-003 | The ponytail review artifact had no closure; `deviations.md` said 17 container tests | Fixed: review closure and **Ship** recorded; deviations state 18 (12 + 6) |

### 5.2 Security findings and residual risks

The first security pass found four Low and one Informational finding; all four Lows were closed and
verified. Two Informational residuals remain and are not fail-open on a valid file.

| ID | Risk | Status |
|---|---|---|
| R-1 | With `SET TRUE`, a migration can `SET ROLE ace_view_owner` and read ACE tables; no lint rule refuses `SET ROLE` | Documented in SPEC-017 and OI-E044-J; AGENTS.md §3.12 and code review are the control. Inherent impact Medium. Open: needs the tech lead's acceptance (OPEN-051); D-RUN-14 is an orchestrator decision, not an acceptance |
| R-2 | Spring logs the rethrown Flyway exception, which can contain the failing SQL | Open: needs the tech lead's acceptance (OPEN-051). SPEC-003 states the reasoning: recovery migrations hold DDL and reference data only, never personal data; audit A-07 masking is RWB-TE-011's |
| R-3 | The drift container test reads both databases as the container superuser | Out of scope by D-RCV-05; the reader takes any `Connection`, so a read-only account can be passed later |
| R-4 | BS-2.5 v2 still says the migration account holds the ACE DBA role | Superseded for this story by D-RUN-14 and DG-L13; the standard text is its owner's to correct |
| R-5 | `00-roles-and-databases.sh` interpolates passwords into SQL | Pre-existing baseline, local-only, unchanged by this diff (comments only) |

### 5.3 The dynamic-SQL gap

| Local ID | Document | Gap | Second source | Blocker | Why | How this stage proceeded |
|---|---|---|---|---|---|---|
| DG-E044-DYN-01 | Spec v14-7, SPEC-RWB-E1-044-009 and T-044-20 | `L-GRANT` refuses GRANT/REVOKE only as the first word of a line or statement; it does not inspect inside `EXECUTE`/`DO` dynamic SQL, so `EXECUTE 'GRANT …'`, `EXECUTE $q$GRANT …$q$`, `format('GRANT …')` and a concatenation are not refused | `../review/security-review.md` §3 SEC-044-03 (Low), reproduced against the compiled test classes | **No** | The gated spec defines the rule exactly and the gate passed on that wording. The lint is a build-time test-scope control; D-RUN-14 leaves the migrator with no table privilege in `public`, and code review remains the control. Four review rounds that added dynamic-SQL analysis exceeded the gated spec and were reverted | The rule is restored to SPEC-009 exactly; out-of-spec fixtures were removed; the gap is recorded, not silently accepted. Suggested owner: recovery tech lead / specification owner. Suggested next step: a new `L-DYNAMIC-SQL` rule or a documented ban on dynamic SQL in migrations, each with its own gated spec change |

## 6. Deviations and implementation assumptions

**DOC ID:** DOC-RWB-E1-044-017 · **Maps to:** TASK-00, -03, -09, -10, -15, -18; DEV-E044-01..04; IA-E044-01..07

| ID | Deviation | Why | Effect |
|---|---|---|---|
| DEV-E044-01 | `scripts/dev.ps1 it` and `scripts/dev.ps1 test` could not run in this session: the machine policy is `AllSigned`, and the worktree's tracked `backend/gradlew.bat` disappears when the script launches Gradle (reproduced three times) | Local environment, not code. `scripts/dev.ps1` was not edited (shared file) | The commands the script runs were run directly and exit 0: `./gradlew test`, `./gradlew recoveryIntegrationTest`, `npm run check`. The wrapper itself is unverified and recorded for the orchestrator |
| DEV-E044-02 | The drift snapshot excludes `flyway_schema_history_recovery` | Flyway's generated NOT NULL constraint names embed OIDs and differ between identical databases (16 false differences before the fix) | T-044-15 reports exactly `recovery.queue.note_x`; the history table is Flyway bookkeeping, not a Workbench object |
| DEV-E044-03 | The failure report strips leading zeros: `0002` → `2`, `0001.0002` → `1.2` | Flyway 12.4.0 returns the raw padded version from `ValidateOutput.version` and `MigrationInfo.getVersion().getVersion()` | The ERROR line reads `object=2` / `object=1` as the spec states |
| DEV-E044-04 | A sequence is read from any `V<seq>__` prefix, even when the story token is malformed | Otherwise a malformed name in `t01-name-fail`/`t06-format-fail` would also raise `L-SEQ-GAP`; the full name pattern still decides `L-NAME` and the key rules | The two fixture folders assert exactly their planned lists |

Implementation-stage assumptions (`../implement/assumptions.md`) are recorded and not re-litigated:
IA-E044-01 complete-list assertions in registry order; -02 the sequence prefix rule above; -03 the
previous-tag case removes the later file from the classpath; -04 the history table is excluded from
the snapshot; -05 the `L-LEX` key is the opener offset; -06 `L-SEQ-DUP` keys on the four-digit
sequence and `L-SEQ-GAP` uses the missing version as file and key; -07 the container asserts the
history row by `script` because Flyway stores the padded version.

**Post-gate drifts, not scope changes.** `../implement/code-map.md` records "50 folders" for the lint
corpus; the delivered tree holds **55** fixture folders because review rounds added cases, and the
suite asserts all 55. `../implement/unit-tests/report.md`, the ponytail review closure and
`deviations.md` were refreshed during the code-gate fix (CODE-002, CODE-003). No gated spec, plan,
shared file or merged migration was edited to match.

## 7. Open items — no approval claimed

**DOC ID:** DOC-RWB-E1-044-018 · **Maps to:** SPEC-RWB-E1-044-017; OI-E044-A..J; OPEN-016, OPEN-050

| ID | Item | Status here | Owner |
|---|---|---|---|
| OI-E044-A | Confirm that the AC8/X6 "failure record" is the ERROR log with `MSG-P3-016` and the version, because PostgreSQL leaves no failed history row | **OPEN** (assumption ASM-E044-02 applied) | BA / Product Owner |
| OI-E044-B | Resolve RWB-E1-069 v7 against the lint this story ships: two non-fix files per key, and the Section A grants against `L-GRANT` and `L-LITERAL-SCHEMA` | **OPEN** (SEAM-E044-02) | Recovery tech lead / BA |
| OI-E044-C | The source documents still fix conflicting migration numbers; D-RUN-07 assigns numbers at merge here | **OPEN** (D-RUN-07 applied) | Recovery tech lead / BA |
| OI-E044-D | ACE-port items: D-RCV-45 `db-migrate` guard, H2 skip, Jenkins step | **OPEN** (not applicable in this repository) | Recovery tech lead |
| OI-E044-E | Update OPEN-018 and OPEN-036: the story v7 text is still unaligned with D-RCV-35/D-RCV-28 | **OPEN** | Orchestrator |
| OI-E044-F | Confirm the narrow `public` exception for the RWB-E1-069 view migrations, or name an ACE-schema parameter | **OPEN** (SEAM-E044-01) | Recovery tech lead with BA |
| OI-E044-G | No story owns the D-RCV-12 job-monitor parts (`MigrationRunRecorder`, `GET /admin/jobs?type=MIGRATION`, SCR-44, `MSG-P4-002`, TC-E1-044-10) | **OPEN** (out of scope, no owner inferred) | BA / Product Owner |
| OI-E044-I | Who applies R1 and R2 in SIT, UAT and PROD, and aligns RWB-E1-069 v7 §3 with §10 | **OPEN** (local init only here) | Recovery tech lead with ACE team lead / ACE DBA |
| OI-E044-J | Confirm D-RUN-14 and decide the residual `SET ROLE ace_view_owner` path | **OPEN** (D-RUN-14 applied as the orchestrator's decision) | Recovery tech lead |
| OI-E044-H | RWB-TE-001 tooling in the E1-044 coverage tasks | **CLOSED** by orchestrator triage on S22 (2026-11-18T00:55) | Orchestrator |
| OI-E044-K | Recovery main scope below 80% on 17 Nov 2026 | **CLOSED** by orchestrator decision D-RUN-17 | Orchestrator |
| OPEN-016 | Per-story approver names are not available in Jira | **OPEN.** No named approver or `AGENTS.md` §9 sign-off is recorded or claimed | Human review and merge |
| OPEN-050 | The one-module definition and D-RUN-21 are unratified | **OPEN.** D-RUN-21 reads "module" as the ACE module; the plan gate confirmed the settlement, not a human ratification | Recovery tech lead |

**Statement.** RWB-E1-044 is implemented and evidenced at branch tip `89477bc`. Every acceptance
criterion and business rule has a named test or an explicitly recorded out-of-scope decision; the
unit and container suites pass; all four coverage counters clear 80%; the code gate, security review
and ponytail review pass with no outstanding Critical, High or Medium finding. One Low-severity
security gap (DG-E044-DYN-01) and two Informational residuals are recorded, with code review and the
D-RUN-14 database boundary as the control. Human review and merge are outstanding (OPEN-016). This
document claims no approval, no merge, no release and no SIT or UAT exit.
