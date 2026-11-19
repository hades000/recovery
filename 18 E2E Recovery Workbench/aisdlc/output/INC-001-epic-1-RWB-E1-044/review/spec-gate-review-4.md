---
title: "Spec gate review round 4: RWB-E1-044 (spec v14-4)"
run_id: INC-001-epic-1-RWB-E1-044
story: RWB-E1-044
gate: Specification (Compliance Reviewer, spec-gate mode)
round: 4 (round 1 is `spec-gate-review.md`, S01 to S11; round 2 is `spec-gate-review-2.md`, S10 residual and S12 to S15; round 3 is `spec-gate-review-3.md`, S16 to S19)
date: 2026-11-18
result: FAIL (1 Medium, 3 Low; the Medium blocks the hand-off)
---

# Spec gate review round 4: RWB-E1-044

## 1. Scope

Reviewed, all under `aisdlc/output/INC-001-epic-1-RWB-E1-044/specify/`: `spec.md` (v14-4), `gate-response.md` (the
round 3 section in full), `compliance-validation.md`, `assumptions.md`, `document-gaps.md`, `shared-updates.md` (with
the proposed Traceability Matrix rows), `contracts/backend-apis.json`, `contracts/frontend-integrations.json`,
`figma/figma_report.md` and `agent-run-log.md`. The `*.run3.*` files (v14-3) were used only to see what changed. I read
a full diff of `spec.run3.md` to `spec.md`.

Checked against:

- The round 3 review `review/spec-gate-review-3.md` (S16 to S19), and rounds 1 and 2.
- `AI-SDLC-BUILD-LOG.md` §1: D-RUN-07, -08, -09, -13 and **D-RUN-14** (2026-11-18T00:31). Also the event rows
  2026-11-18T00:28:08 (round-3 triage, REMEDIATE: "S18: name one JaCoCo verification rule per class set"),
  00:31:45 (D-RUN-14; RWB-E1-069 HELD until E1-044 applies it), 00:32:20 (D-RUN-14 sent to this run: "amend SPEC-017,
  OI-E044-I, T-044-17") and 00:39:15 (RWB-TE-001 spec gate round 5 PASS; RWB-TE-001 Plan STARTED). These are
  orchestrator rulings. I checked how they were applied. I did not re-open them.
- `aisdlc/RUN-BRIEF.md`; `aisdlc/.github/rules/specification-execution-gates.md`, `planning-execution-gates.md`
  (lines 37–44, 67), `implementation-execution-gates.md` (lines 55–68), `pdlc.md` (lines 22–29).
- Code: `platform/internal/RecoveryProperties.java`, `PlatformConfig.java`, `RecoveryFlywayConfig.java`,
  `platform/api/RecoveryFlags.java`, `RecoveryDatabaseIT.java`, `backend/build.gradle.kts` (dependencies; coverage
  tasks, lines 130–160), `backend/build/reports/jacoco/recoveryCoverageReport.xml` (report totals),
  `infra/postgres/init/00-roles-and-databases.sh`, `10-load-ace-database.sh`, `20-grants.sql.inc`,
  `infra/postgres/schema/01-ace-schema-v1.sql` (`public.account`, line 804 `pk_account PRIMARY KEY (id)`).
- Sibling specs, read only for cross-story consistency: RWB-TE-001 `specify/spec.md` (SPEC-020, SPEC-024, Unit Test
  Applicability, T-TE001-10), and the `REQUIREMENT_COVERAGE_RESULT` lines of the other nine stories;
  RWB-E1-069 `review/spec-gate-review-2.md` (finding 117).
- Document set v14 (read only, `17 AI-First SDLC Repository v2/requirement/legacy/`): Environment and Deployment Design
  v4 §5 (line 124 verified: the Section A migration "creates or confirms the two database roles"); ACE Source Views v1
  (line 727 verified: `ALTER VIEW recovery.v_ace_account OWNER TO :ace_view_owner`); Test Cases v7 TC-ACE-001-04 (line
  1168 verified: "The ACE DBA applies the grant script"); RWB-E1-069 story v7 §3 (line 44); Physical Schema v6 grant
  block (from line 6822); Build Sequence v6 (orders 1 and 2; RWB-TE-001 has no "Depends on").

**Probe.** I ran one throwaway container from the local `postgres:16.16-alpine` image (no download) and removed it
afterwards. I touched no repository file and did not touch the running local stack. It reproduces the D-RUN-14 grants
on a minimal `public.account (id bigint PRIMARY KEY, account_key varchar)` and checks the claims below. Results are
quoted where used.

No git command was run. Only this file was written. No question was put to the user (L-RCV-03).

## 2. Round-3 findings

| Finding | Severity (round 3) | Status | Evidence |
|---|---|---|---|
| S16 T-044-08 case (5) cannot start; failing cases assert on beans | Low | **CLOSED** | T-044-08 now gives the runner in full: `withUserConfiguration(PlatformConfig.class, RecoveryFlywayConfig.class)`, base properties `rwb.p3.temporal=false` and `rwb.p3.drools=false`, and a test class in `…platform.internal`. I checked this against the code. `PlatformConfig` and `RecoveryFlywayConfig` are both package-private. `RecoveryProperties` is a record with nested records `P3`, `Flyway` and `Security` and no `@DefaultValue`. `recoveryFlags` calls `properties.p3().temporal()` and `.drools()` into `RecoveryFlags(boolean, boolean)`. `RecoveryDatabaseIT` line 31 sets the same two properties. `Security` is read by neither configuration. Cases (1) to (4) now assert only on the startup failure: `ConfigurationPropertiesBindException` in the cause chain, the root message, and no NPE, `FlywayException` or `NoSuchBeanDefinitionException`. "No `Flyway` bean" moved to case (5), which starts. Case (2) is sound: `RecoveryProperties` is the first parameter of `recoveryFlyway` (line 28), and whichever bean is built first fails at binding. Case (3) is sound: it replaces the `systemEnvironment` source under the same name, which Spring Boot requires before it maps `RWB_SCHEMA` to `rwb.schema` |
| S17 Finding multiplicity and statement-view source undefined | Low | **CLOSED** | SPEC-004 now defines finding identity as (rule, file, line, key) and gives a key per rule. L-LITERAL-SCHEMA's key is the resolved schema name, so `CREATE TABLE public.x` (items 1 and 4) gives one finding. SPEC-007 says items 1 to 4 are ways of matching, not separate findings. SPEC-008 says "is" and gives the `information_schema` / `pg_catalog` exception. The view table derives (c) from (b), with offsets kept, cut at top-level `;` tokens taken from the token list. The start line, first word and kind come from (b), and L-GRANT reads the same range in (a). T-044-05 states the exact pair. T-044-22 adds N15 (two findings at :2) and S1 (leading comments do not supply the kind). I traced N1 to N15 and S1 against the rules as written, and each expected list follows. The contract `findingMultiplicity` matches. One wording point is in §5 |
| S18 One combined JaCoCo bundle measured, per-set gate stated | Low | **CLOSED** (follow-on: S21, S22) | SPEC-014 applies the round-3 triage ("one JaCoCo verification rule per class set") as option (a). Rule MAIN stays in `recoveryCoverageVerification` over `recoveryClasses`, the whole `th/co/scb/ace/demo/recovery/**` main tree, untested classes included. Rule TOOLING is a new `recoveryToolingCoverageVerification` over the tooling package from the test output. Each task has one `BUNDLE` rule with LINE, INSTRUCTION, BRANCH and METHOD at 0.80. The reason for two tasks is correct: a task's class directories form one bundle, and `PACKAGE` measures each package separately. The finalizer wiring also runs TOOLING when MAIN fails. There are two reports, and the evidence quotes each set separately. "For either class set" is now true of the build. The MAIN baseline is verified against the report: INSTRUCTION 686/2174, BRANCH 25/92, LINE 133/415, METHOD 41/135 (31.6 / 27.2 / 32.0 / 30.4%). See S21 and S22 for its consequences |
| S19 Contract files not aligned | Low | **CLOSED** | Both contract files parse as JSON and carry `"specVersion": "v14-4"`, matching `spec.md`. `identifiersOnly` names the SPEC-007 token table as authoritative and gives the `E'…'` escape rule in words, so JSON escaping cannot lose it. `findingMultiplicity` and `migratorRights` are added and agree with SPEC-004, SPEC-008 and SPEC-017 |

Rounds 1, 2 and 3 have no open finding.

## 3. Orchestrator rulings and decisions applied

| Ruling | Applied in the spec | Result |
|---|---|---|
| Round-3 triage (00:28:08): remediation run 3; S18 one rule per class set | SPEC-014, SEAM-E044-04, Unit Test Applicability, Verification table, CLAR-011, ASM-E044-07, OI-E044-H, OI-E044-K | Applied. Cross-story effect not recorded: S22 |
| **D-RUN-14** (00:31): `rwb_migrator` gets `USAGE ON SCHEMA public` with no table privilege, and `GRANT ace_view_owner TO rwb_migrator WITH INHERIT FALSE, SET TRUE`. Never the ACE DBA role or SELECT on a `public` table. SELECT grants to `ace_view_owner` stay with the ACE DBA. An open item asks the recovery tech lead to confirm | SPEC-017 R1 and R2 (statements as in the decision; `ADMIN` false), the still-declined list, the BR8 reasoning, residual `SET ROLE` risk, local application in `20-grants.sql.inc` (Change Scope, ASM-E044-18), T-044-17 (a) to (f), OI-E044-I reworded, OI-E044-J (confirmation), DG-L13, CLAR-013, contract `migratorRights` | **Applied as decided.** Every element of the decision is present, and nothing beyond it is granted. The citations check out (Env v4 line 124, ACE Source Views v1 line 727, TC-ACE-001-04). The probe confirms the mechanism. With R1 and R2, `pg_auth_members` shows `inherit_option f, set_option t, admin_option f`. The T-044-17 (d) count is 0. As `rwb_migrator`, `CREATE VIEW recovery.v_ace_account AS … FROM public.account` succeeds and `ALTER VIEW … OWNER TO ace_view_owner` succeeds. A direct `SELECT` on `public.account` is refused ("permission denied for table account"). An FK to `public.account(id)` is refused. T-044-17 precision: S23 |
| D-RUN-07, D-RUN-08, D-RUN-09, D-RUN-13; round-1 and round-2 triage | Unchanged from v14-3 (SEAM-E044-01, the no-waiver ruling, the identifiers-only scope, the tokenizer) | Applied. D-RUN-08 and the MAIN baseline: S21 |

The spec set attributes every ruling to the orchestrator and claims no human ruling or disposition (checked in
`gate-response.md` round 3, `assumptions.md`, `agent-run-log.md`, SPEC-017). The per-finding triage wording for S16, S17
and S19 comes from the orchestrator's run instruction. The spec says the log row is the record, as noted in round 3. No
personal name appears in the spec set.

## 4. New findings

IDs continue from round 3.

### REVIEW-RWB-E1-044-S20: `CONTRADICTIONS: 8` fails the planner's upstream-readiness hard gate, though every contradiction is settled

- **Severity:** Medium
- **Affects:** spec `## Status` `REQUIREMENT_COVERAGE_RESULT`; `compliance-validation.md` row "Status lines"
- **Evidence:** The spec reports `REQUIREMENT_COVERAGE_RESULT: SUCCESS … [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0]
  [CONTRADICTIONS: 8]` (line 630). It then says each of the 8 is "settled by RUN-BRIEF precedence, a recorded decision or
  the orchestrator triage, and none is a blocker". `planning-execution-gates.md` (Hard Gates, "Upstream Spec Readiness
  Required", line 44) requires "`REQUIREMENT_COVERAGE_RESULT` present with `MISSING_RULES: 0` and `CONTRADICTIONS: 0`"
  before the plan can complete. `implementation-execution-gates.md` line 68 repeats this for the build. `pdlc.md`
  line 29: "independent stage hard gates remain blocking". The specification gate does not define the field. The
  planner gate's own wording ("unresolved conflicts", line 40) shows the count it expects is of unresolved
  contradictions. Siblings use it that way. RWB-TE-001 (which passed its spec gate), RWB-E1-042, RWB-TE-002, RWB-TE-003,
  RWB-TE-011, RWB-TE-012 and RWB-E1-069 report `CONTRADICTIONS: 0` with their gaps recorded. RWB-E1-001 writes
  "CONTRADICTIONS: 2 unresolved by precedence". My round-1 required fix for S01 asked the spec not to "claim zero
  contradictions without this entry", and rounds 2 and 3 passed the count of 7 and then 8 without comment. That wording
  contributed to the problem, and I record the miss here.
- **Failure scenario:** The Implementation Planner reads `CONTRADICTIONS: 8` and applies its hard gate. It stops with
  `BLOCKED` before writing `plan.md`, even though no contradiction is open. The alternative is that it reads past the
  number, and then the gate signal means different things in different stories. Either way the hand-off to the plan stage
  fails or becomes unreliable.
- **Required fix:** Report the field as the count of unresolved contradictions, which is 0 here. Keep the eight settled
  ones visible on the same line, for example `[CONTRADICTIONS: 0] (unresolved; 8 source contradictions settled by
  precedence or recorded rulings: DG-L01, -L02, -L04, -L05, -L09, -L11, -L12, -L13)`. Update the
  `compliance-validation.md` "Status lines" row the same way. Do not delete or merge any DG row.

### REVIEW-RWB-E1-044-S21: The MAIN-baseline sequencing decision is needed before planning, but the spec marks it resolved

- **Severity:** Low
- **Affects:** SPEC-014 ("Baseline of the MAIN set"); Unit Test Applicability (backend main); CLAR-011; Status
  `CLARIFICATION_STATUS`; ASM-E044-07; OI-E044-K
- **Evidence:** SPEC-014 records that rule MAIN fails at baseline on all four counters (verified, §2 S18). The failures
  come from classes E1-044 does not change. The spec also states that "This story does not write tests for classes it
  does not change". It leaves "whether the E1-044 code gate waits for RWB-TE-001 or the orchestrator rules otherwise" to
  OI-E044-K. Even so, CLAR-011 is "RESOLVED", and the status line says `CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]`.
  The implied default is to hold E1-044's code gate until RWB-TE-001 SPEC-024 lands. That makes E1-044's completion
  depend on a story later in Build Sequence v6 (order 2), which D-RUN-08 does not allow without a ruling. The other path,
  where E1-044 lifts the whole main scope itself, changes the plan's test list a great deal and overlaps RWB-TE-001
  SPEC-024. `planning-execution-gates.md` (lines 39 and 43) forbids final plan outputs while a CLAR item or a hard-gate
  note is unresolved. AGENTS.md §7 requires the plan to list the tests to write. Build Sequence v6 gives RWB-TE-001 no
  dependency on RWB-E1-044, so reordering is possible, but only the orchestrator can decide it.
- **Failure scenario:** The planner treats CLAR-011 as resolved and writes a plan with tests for the changed classes
  only. The implementation then fails rule MAIN at 32% LINE. That is an expected and avoidable failure, and the
  implementation gates make it a blocker. Or the planner adds tests for about 28 unrelated classes, which duplicates
  RWB-TE-001 SPEC-024 and breaks AGENTS.md "extend or correct, never duplicate".
- **Required fix:** The orchestrator rules on OI-E044-K before the plan stage. The options are to reorder E1-044's code
  gate after RWB-TE-001's coverage tests, to assign the MAIN lift to E1-044, or another ruling, with the human
  disposition route under D-RUN-09 if it is needed. The spec then records that ruling in SPEC-014, CLAR-011, the backend
  main Unit Test Applicability row and ASM-E044-07. Until then, CLAR-011 and `CLARIFICATION_STATUS` must show the item as
  open, not resolved.

### REVIEW-RWB-E1-044-S22: SEAM-E044-04 and OI-E044-H state the opposite of RWB-TE-001's approved coverage wiring

- **Severity:** Low
- **Affects:** SPEC-016 SEAM-E044-04; `shared-updates.md` OI-E044-H; SPEC-014
- **Evidence:** SEAM-E044-04 says RWB-TE-001 "adds its own test-scope tooling class directory to the TOOLING set, that
  is, to `recoveryToolingCoverageReport` and `recoveryToolingCoverageVerification`". OI-E044-H is framed as "Inform
  RWB-TE-001". RWB-TE-001's spec passed its gate in round 5 (build log 00:39:15) and is now in Plan. Its SPEC-020 (b)
  says: "Both tasks add the test-output class directory of the tooling package … to `classDirectories` … the main
  `recovery/**` tree stays whole". Its Unit Test Applicability row measures "all main classes … plus the test-scope
  boundary tooling package" in `recoveryCoverageVerification`. T-TE001-10 asserts each counter "over all recovery main
  classes plus tooling". That is one combined bundle, the shape the round-3 triage ruled out for E1-044. E1-044 merges
  first (order 1), so RWB-TE-001's build would edit E1-044's rule MAIN.
- **Failure scenario:** RWB-TE-001 is planned and built from its approved SPEC-020 (b). It adds its tooling directory to
  `recoveryCoverageVerification`. Rule MAIN then measures main plus TE-001 tooling as one total again. The per-set
  evidence E1-044 relies on is no longer per set, and nothing in either spec catches it. If TE-001 follows E1-044's seam
  instead, it departs from its own approved spec and T-TE001-10 without a recorded ruling.
- **Required fix:** In SEAM-E044-04, state the conflict by reference: RWB-TE-001 SPEC-020 (b), its Unit Test
  Applicability row and T-TE001-10 against SPEC-014 and the round-3 triage. Reword OI-E044-H from "inform" to a
  cross-story conflict for orchestrator triage, raised before the RWB-TE-001 plan gate. Do not claim RWB-TE-001's scope
  until the orchestrator has ruled.

### REVIEW-RWB-E1-044-S23: Under D-RUN-14, T-044-17 (f) gets 42501 only if the referenced column is the key, and the fixture leaves the column out

- **Severity:** Low
- **Affects:** T-044-17 (f); SPEC-017 ("BR8 holds in the database")
- **Evidence:** T-044-17 (f) specifies "a fixture with `REFERENCES public.account(…)` … fails in the database with
  SQLSTATE `42501`". Under v14-3, `rwb_migrator` had no USAGE on `public`, so any reference failed at name lookup with
  42501, whatever the column. R1 now gives USAGE. PostgreSQL then checks the referenced columns before it checks the
  `REFERENCES` privilege ("permission checks wait till we have the column numbers"). The probe as `rwb_migrator`, with
  R1 and R2, shows this:
  - `REFERENCES public.account(id)`: "permission denied for table account" (42501).
  - `REFERENCES public.account` with no column list: 42501.
  - `REFERENCES public.account(account_key)`: "there is no unique constraint matching given keys" (42830).
  - `REFERENCES public.account(account_id)`: "column … does not exist" (42703).

  In ACE schema v1, `public.account` has `pk_account PRIMARY KEY (id)`, with `id bigint` (`01-ace-schema-v1.sql` line
  804).
- **Failure scenario:** A builder picks a natural-looking but non-key column, such as `account_key`. The test fails with
  42830 and passes nothing about privilege. Or the builder loosens the assertion to "any error", and then the test no
  longer proves that the database refuses the FK.
- **Required fix:** In T-044-17 (f), name the referenced column as the primary key (`REFERENCES public.account(id)`,
  with a `bigint` referencing column) or use no column list. State that the expected error is 42501 because the target
  is the key, and cite `01-ace-schema-v1.sql` `pk_account`.

## 5. Observations (no change required for this gate)

- **S1 statement count.** "Exactly two statements" depends on a range with no non-blank character in (b), such as the
  remainder after the last `;`, not counting as a statement. That follows from "first non-blank characters of the range",
  but one sentence in SPEC-007 would make it explicit.
- **ASM-E044-17 basis.** It says the finding format "carries only file and line". SPEC-004 also puts the key in the
  detail (`literal schema <name>`). The choice still holds; only the reason is worded loosely.
- **For OI-E044-J (the `SET ROLE` lint question).** With `INHERIT FALSE`, `rwb_migrator` loses owner rights once a view
  passes to `ace_view_owner`. In the probe, `CREATE OR REPLACE VIEW recovery.v_ace_account …` as `rwb_migrator` after the
  owner change failed with "must be owner of view". Any later migration that changes a Section A view therefore needs
  `SET ROLE ace_view_owner`, so a blanket lint ban on `SET ROLE` would block it. This is for RWB-E1-069 and the recovery
  tech lead. No E1-044 change is needed.
- **For OI-E044-I (environments outside this repository).** `ALTER VIEW … OWNER TO ace_view_owner` also requires
  `ace_view_owner` to hold CREATE on `recovery`. The local init grants it (`20-grants.sql.inc` line 7). The rights list
  for SIT, UAT and PROD should carry it too.
- **For RWB-E1-069.** `ALTER DEFAULT PRIVILEGES FOR ROLE rwb_migrator … ON TABLES TO recovery_svc` (`20-grants.sql.inc`
  lines 56–57) also applies to views that `rwb_migrator` creates, and the grant survives the owner change. A
  Flyway-created `v_ace_*` view would therefore carry INSERT, UPDATE and DELETE grants for `recovery_svc`. A write is
  still refused through `ace_view_owner`'s base-table rights, but `RecoveryDatabaseIT.aceViewsAreReadOnlyForTheService`
  and the Env v4 §5 conformance check test for the absence of the grant. RWB-E1-069 owns the fix, for example a REVOKE
  in its view migration.
- **Comments in the init files.** When the plan adds R1 and R2 to `20-grants.sql.inc`, the role comments in
  `00-roles-and-databases.sh` (lines 8–13) and `20-grants.sql.inc` line 9 ("ace_view_owner reads ACE; nobody else
  does") should say that `rwb_migrator` now holds USAGE on `public` and a non-inheriting membership.

## 6. Required checks

| Check | Result |
|---|---|
| Authentication and authorization | No endpoint in scope. The job-monitor read path, TC-E1-044-10 and the §10 read and rerun authority are out of scope by D-RCV-12, with no owner (DG-L10, OI-E044-G). The migration account's database rights follow D-RUN-14 exactly. The ACE DBA role, any table privilege in `public`, `CREATE` on `public` and `ADMIN` are declined, and the residual `SET ROLE` read path is recorded for confirmation (OI-E044-J) |
| Customer and account data protection | Pass. Fixtures are synthetic. `rwb_migrator` cannot read ACE tables without `SET ROLE` (probe: 42501; T-044-17 (d), (e)). BR8 is L-FK-OUTSIDE in every environment, plus the database refusal against this repository's grants (T-044-17 (f); precision S23) |
| Audit logging for sensitive financial actions | Not applicable. There is no case or decision change. The run record is the history table plus the MSG-P3-016 ERROR line (ASM-E044-02, OI-E044-A) |
| KYC, AML, suitability, consent, approval | Not in scope |
| Frontend integration versioning and error contract | Not applicable to code (NO_API_CHANGE; UI out of scope). Both contract files are at `v14-4` and parse (S19 closed) |
| Secrets and environment configuration | Pass. Migrator credentials come from the environment or the key store. The schema pin holds with Flyway on or off (T-044-08, S16 closed). The init grants hold no credential, and container passwords are synthetic |
| Test coverage and evidence | Planned: backend `REQUIRED` on two class sets, each with its own `BUNDLE` rule at 0.80 on LINE, INSTRUCTION, BRANCH and METHOD, no waiver, untested main classes included. Container tests T-044-10 to T-044-18 are kept apart from unit coverage. The MAIN baseline (32.0% LINE) makes the code gate fail without a ruling (S21). The cross-story wiring is in conflict (S22) |
| Frontend and backend applicability | Frontend `NOT_APPLICABLE` is justified (story v7 §15; no `frontend/` change). Backend `REQUIRED` |
| Precedence and invented requirements | No invented financial, regulatory or security requirement was found. D-RUN-14 is applied as the orchestrator's decision with its own citations, and DG-L13 stays Blocker = No. The status signal for settled contradictions is S20 |
| Personal data in artefacts | None. Roles are named by title. There is no personal name, ID or account number in the spec set |

## 7. Result

| Severity | Count | IDs |
|---|---|---|
| Critical | 0 | — |
| High | 0 | — |
| Medium | 1 | S20 |
| Low | 3 | S21, S22, S23 |

Round-3 status: S16, S17, S18 and S19 are all CLOSED. D-RUN-14 is applied as decided.

S20 is Medium because, as written, the spec stops the Implementation Planner at that stage's own hard gate
(`planning-execution-gates.md` line 44), so the hand-off cannot go ahead until it is fixed and re-reviewed (`pdlc.md`
line 22). The fix is the status line only.

S21 needs an **orchestrator ruling on OI-E044-K before the plan stage**. After that, the spec only records the ruling.
S22 needs orchestrator triage across RWB-E1-044 and RWB-TE-001, whose plan has already started. S23 is a one-line test
correction.

**Overall: FAIL (blocking: 1 Medium)**
