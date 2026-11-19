---
title: "Spec gate review round 3: RWB-E1-044 (spec v14-3)"
run_id: INC-001-epic-1-RWB-E1-044
story: RWB-E1-044
gate: Specification (Compliance Reviewer, spec-gate mode)
round: 3 (round 1 is `spec-gate-review.md`, S01 to S11; round 2 is `spec-gate-review-2.md`, S10 residual and S12 to S15)
date: 2026-11-18
result: FAIL (Low findings only; non-blocking, REVIEW_GATE_WARNING below)
---

# Spec gate review round 3: RWB-E1-044

## 1. Scope

Reviewed, all under `aisdlc/output/INC-001-epic-1-RWB-E1-044/specify/`: `spec.md` (v14-3), `gate-response.md`
(round 2 section), `compliance-validation.md`, `assumptions.md`, `document-gaps.md`, `shared-updates.md`,
`contracts/backend-apis.json`, `contracts/frontend-integrations.json`, `figma/figma_report.md`, `agent-run-log.md`.
The `*.run2.*` files (v14-2) were used only to see what changed (a full diff of `spec.run2.md` to `spec.md` was read).

Checked against:

- Round 2 review `review/spec-gate-review-2.md` (S10 residual, S12 to S15) and round 1 `review/spec-gate-review.md`.
- `AI-SDLC-BUILD-LOG.md` §1 D-RUN-07 to D-RUN-13, and the event rows 2026-11-17T23:40:23 (round-1 triage),
  2026-11-17T23:41:42 (D-RUN-09), 2026-11-17T23:49:16 (D-RUN-13) and 2026-11-18T00:01:20 (RWB-E1-044 "Gate triage",
  REMEDIATE: "fix all five; S12 one quote-aware tokenizer pass (single quotes, dollar quotes, both comment forms) with
  adversarial tests; S13 schema pin checked in both modes; S15 settle from ADR-010 least privilege, record or decline
  with citation"). These are orchestrator rulings. They were applied as given and are not re-opened here.
- `aisdlc/RUN-BRIEF.md` (precedence, document-gap rules, D-RUN-07, D-RUN-08, hard rules).
- `aisdlc/docs/decisions/`: `d-rcv-35-ace-db-alignment.md` (U3, U4), `INC-001-decisions.md` (D-RCV-28, -40, -43),
  `decision-register.md`.
- Code: `RecoveryProperties.java`, `PlatformConfig.java`, `PlatformInfoController.java`, `RecoveryFlywayConfig.java`,
  `application.yaml`, `RecoveryMigrationLintTest.java`, `RecoveryDatabaseIT.java` (properties line),
  `backend/build.gradle.kts` (dependencies, `recoveryCoverageReport`, `recoveryCoverageVerification`, lines 130–160),
  `infra/postgres/init/00-roles-and-databases.sh`, `10-load-ace-database.sh`, `20-grants.sql.inc`. A search of
  `backend/src/test` for `RecoveryProperties`, `PlatformConfig`, `rwb.schema` and context-test annotations.
- Document set v14 (read only, `17 AI-First SDLC Repository v2/requirement/legacy/`): RWB-E1-044 story v7 (§3 line 40,
  §10 line 166, §13 line 228); RWB-E1-069 story v7 (§3 line 44, §4 flow 1, §10); ACE Team Stories v1 RWB-ACE-001
  (§3, §4 flow 5, §10); ADR v3 ADR-010 (drivers, Decision); Environment and Deployment Design v4 §5 (lines 64, 120,
  124, 130); Physical Schema v6 (line 11; dollar bodies at 2390, 6145, 6163, 6185; Section A; grant block from 6823).
- `aisdlc/.github/rules/specification-execution-gates.md`, `implementation-execution-gates.md` (lines 55–59),
  `pdlc.md` (line 23); `aisdlc/.github/contexts/testing-standards.md` §6.

No git command was run. Only this file was written. No question was put to the user (L-RCV-03).

## 2. Round-2 findings

| Finding | Severity (round 2) | Status | Evidence |
|---|---|---|---|
| S10 (residual) Unit Tests cells not the bare gate value | Low | **CLOSED** | Both backend rows of `## Unit Test Applicability` (spec lines 522–523) hold exactly `REQUIRED`; the test IDs are in Test Acceptance Criteria. Frontend row `NO` / `NOT_APPLICABLE` / `NOT_APPLICABLE`. Coverage Type values are only `DIRECT` / `INHERITED_EXISTING_BEHAVIOR`, Status only `COVERED` (28 rows, matching `TOTAL_RULES: 28`) |
| S12 Comment and string removal not one lexical pass | Low | **CLOSED** | SPEC-007 now specifies one left-to-right tokenizer with a token table: `--`; nested `/* */` (count kept); `E'…'` with `''`, `\'`, `\\`; standard and prefixed `'…'` with `''`; `"…"` with `""`; the Flyway `${…}` placeholder; `$tag$` bodies (tag rule, `$1` excluded, end found first). It yields (a) code text with strings kept (L-SEARCH-PATH, L-GRANT) and (b) identifier text with comments and strings blanked (L-LITERAL-SCHEMA, L-FK-OUTSIDE), line structure kept. Every case asked for in round 2 is in T-044-22: `'/*'` (N1), `'--'` (N2), `''` (N3), `E'\'--'` (N4), nested-comment positive (P1), plus quoted-identifier, dollar-body and unterminated cases. I traced N1 to N14 and P1 to P3 against PostgreSQL lexical rules and the stated recovery rule; each expected result follows from the spec. P3 matches the Physical Schema v6 `ace_to_date` pattern (verified line 6149, `'^\d{8}$'` inside `$$`). L-LEX (ASM-E044-16) keeps a stray opener from hiding the rest of the file. Matches the logged triage on S12. Residual precision on finding multiplicity: S17 |
| S13 Schema pin only runs when the Flyway bean is created | Low | **CLOSED** | SPEC-002 moves the check to `RecoveryProperties` binding (compact constructor, or `@Validated`; `spring-boot-starter-validation` verified at `build.gradle.kts` line 44). Verified: `PlatformConfig` has no condition and carries `@EnableConfigurationProperties(RecoveryProperties.class)`; `recoveryFlags` consumes the properties; `RecoveryFlywayConfig` is `@ConditionalOnProperty(rwb.flyway.enabled, matchIfMissing = true)`; `application.yaml` sets `hibernate.default_schema: ${rwb.schema}`. No test constructs `RecoveryProperties` (search verified; the only context test is `RecoveryDatabaseIT`, which loads `application.yaml`). The error stays a configuration error with no message ID (ASM-E044-03). T-044-08 covers both flag values and the A-17 relaxed-binding case. One of its five cases cannot pass as written: S16 |
| S14 RWB-E1-069 grant seam does not name L-LITERAL-SCHEMA | Low | **CLOSED** | SEAM-E044-02, DG-L05 and OI-E044-B now name L-GRANT and L-LITERAL-SCHEMA items 3 and 4 for the Section A grants; DG-L05 cites D-RCV-35 U4 ("Adds 30 views and the grant they need", verified line 38). SEAM-E044-01 is unchanged and states that any allowance for grant statements belongs to OI-E044-B. The added route (ACE DBA applies the grant) is supported: RWB-ACE-001 v1 §4 flow 5 ("ACE DBA: grants SELECT on the listed tables to the view-owner role") and §10; RWB-E1-069 v7 §10 ("ACE team lead and ACE DBA … grant SELECT to `ace_view_owner`") |
| S15 RWB-E1-069 precondition attributed to E1-044 not recorded; T-044-17 stated too widely | Low | **CLOSED** | DG-L13 records RWB-E1-069 v7 §3 (verified line 44) against RWB-E1-044 v7 §3 (line 40, accounts "held in the key store") and §10 (line 166, "not a Workbench role"), RWB-E1-069 v7 §10, RWB-ACE-001 v1, ADR v3 ADR-010 (driver "A boundary the database enforces", line 348; Decision: views owned by "a dedicated role that holds SELECT on the ACE tables"), D-RCV-35 U3 ("Existing ACE tables are never altered by the Workbench", line 37) and U4, and the init grants (`rwb_migrator` has nothing in `public`: verified `REVOKE ALL ON SCHEMA public FROM PUBLIC; GRANT USAGE ON SCHEMA public TO ace_view_owner`). Blocker = No with the precedence reason. SPEC-017 declines the role with an owner (RWB-E1-069 or the ACE DBA, OI-E044-I) and the contract carries `declinedPreconditions`. The BR8 row and T-044-17 now limit the database proof to this repository's grants and name L-FK-OUTSIDE as the control in every environment; T-044-17 first asserts `has_schema_privilege('rwb_migrator','public','USAGE')` is false, which holds for the init above. Matches the logged triage on S15 |

## 3. Orchestrator rulings and decisions applied

| Ruling | Applied in the spec | Result |
|---|---|---|
| Round-1 triage (2026-11-17T23:40:23): S01 ship D-RCV-28 lint, gap, RWB-E1-069 seam; S02 no receiving story; S03 no waiver | SPEC-007, SPEC-016 (SEAM-E044-01 unchanged), SPEC-017, SPEC-014, DG-L09, DG-L10, OI-E044-F, OI-E044-G | Applied, unchanged from v14-2 |
| Round-2 triage (2026-11-18T00:01:20), D-RUN-09: fix all five; S12 one quote-aware pass with adversarial tests; S13 pin in both modes; S15 settle from ADR-010, record or decline with citation | S10 cells; SPEC-007 tokenizer, L-LEX, T-044-22; SPEC-002 on properties binding, T-044-08; SEAM-E044-02, DG-L05, OI-E044-B; SPEC-017 decline, DG-L13, OI-E044-I, CLAR-013 | Applied (test precision: S16, S17) |
| D-RUN-07: no migration number fixed | Change Scope "Production migration file", CLAR-005, DG-L04, ASM-E044-14 (fixture numbers are test-only) | Applied |
| D-RUN-08: depend only on the repository or earlier stories; later work as seams | Change Scope "Dependencies"; SEAM-E044-01 to -04; SPEC-017; OI-E044-I says the RWB-E1-069 spec must not treat the DBA role as delivered | Applied |
| D-RUN-09: Low-only failures are remediated and re-gated | This round | Applied |
| D-RUN-13: schema-prefix lint checks identifiers only | SPEC-007 view (b), item 4, T-044-21, T-044-22, contract `identifiersOnly` | Applied. Treating dollar-quoted bodies as code is labelled ASM-E044-15 and follows D-RUN-13's stated reason ("A literal is not a schema reference"); every dollar body in Physical Schema v6 is a function body (verified). Not re-opened |
| D-RUN-10, D-RUN-11, D-RUN-12 | Concern RWB-E1-042, -043 and -001 | Not applicable to this story |

The spec set attributes every ruling to the orchestrator and claims no human ruling or disposition (verified in
`gate-response.md`, `assumptions.md`, `agent-run-log.md`). No personal name appears in the spec set.

Observations (not findings, no change required for this gate):

- `gate-response.md` round 2 gives a per-finding "Orchestrator triage" wording for S10 ("Fix the cell format") and S14
  ("Cover … in the RWB-E1-069 seam, or exclude them with a cited reason"), and for S15 adds D-RCV-35. The logged row
  says "fix all five" and, for S15, "ADR-010 least privilege". The content applied is consistent with the logged ruling;
  where the wording came from an orchestrator instruction not in the log, the log row is the record.
- `gate-response.md` front matter still says `date: 2026-11-17`; round 2 is dated 2026-11-18 in its own table.
- L-LITERAL-SCHEMA item 1 matches positions lexically, so `EXTRACT(YEAR FROM a.created_at)`, `x IS DISTINCT FROM
  a.y` and PL/pgSQL `SELECT … INTO NEW.id` would be reported (an alias or record qualifier after `FROM` / `INTO`). This
  fails closed, Physical Schema v6 contains none of these forms (searched), and ASM-E044-06 lets a later rule change
  refine it. Worth one line in the README of SPEC-015 so a later story knows why.
- Environment and Deployment Design v4 §5 (line 124) also says the Section A migration "creates or confirms the two
  database roles". That is a further privilege question for OI-E044-I when the orchestrator applies it; RWB-E1-069 v7
  §3 makes the roles a precondition, so E1-044 is not affected.

## 4. New findings

IDs continue from round 2.

### REVIEW-RWB-E1-044-S16: T-044-08 case (5) cannot start as written, and two cases assert on beans of a failed context

- **Severity:** Low
- **Affects:** T-044-08; SPEC-002; Unit Test Applicability (backend main)
- **Evidence:** T-044-08 runs `ApplicationContextRunner` with `PlatformConfig` and `RecoveryFlywayConfig` only, so
  `application.yaml` is not loaded. Case (5) sets only `rwb.flyway.enabled=false` and `rwb.schema=recovery` and expects
  "the context starts". `RecoveryProperties` is a record with nested records `P3`, `Flyway` and `Security`. With
  constructor binding, a nested record with no bound properties is `null` (no `@DefaultValue` is declared).
  `PlatformConfig.recoveryFlags` calls `properties.p3().temporal()`. That is why `RecoveryDatabaseIT` sets
  `rwb.p3.temporal=false` and `rwb.p3.drools=false` explicitly (line 31). Case (1) also asserts "no `Flyway` bean exists"
  in a context that has failed, so no bean can be queried.
- **Failure scenario:** the builder writes case (5) as specified. Binding succeeds, `recoveryFlags` throws a
  `NullPointerException`, and the context fails. The positive half of the A-17 proof (Flyway off, correct schema,
  service starts) is red for a reason unrelated to the pin. The builder must then change the test outside the spec, or
  the spec reads as unmet at the code gate.
- **Required fix:** In T-044-08, state the base property set every case uses (at least `rwb.p3.temporal=false` and
  `rwb.p3.drools=false`, as `RecoveryDatabaseIT` does). For the failing cases (1) to (4), assert on the startup failure:
  the cause chain holds the configuration-properties bind failure, and its root message names `rwb.schema`, the value
  and D-RCV-28. In case (2), the chain holds no Flyway or `DataSource` error. Remove "no `Flyway` bean exists" from
  case (1) and keep it in case (5), where the context starts.

### REVIEW-RWB-E1-044-S17: Finding multiplicity and the source of the statement view are not defined, but T-044-22 asserts the complete finding list

- **Severity:** Low
- **Affects:** SPEC-004, SPEC-007 (items 1–4, view (c)), SPEC-008, SPEC-016 (`isAllowedQualifier`); T-044-21, T-044-22
- **Evidence:** One `public.x` occurrence can match several clauses of L-LITERAL-SCHEMA. For example, `CREATE TABLE
  public.x` matches item 1 (name after `TABLE`) and item 4 (`public.` followed by an identifier). The spec says items are
  "folded into the same rule ID" but not how many findings one occurrence gives. T-044-22 expects exactly one
  L-LITERAL-SCHEMA per such line, and says "a missing or an extra finding fails". SPEC-008 says a `REFERENCES public.…`
  finding "may be reported" under both L-FK-OUTSIDE and L-LITERAL-SCHEMA, but T-044-21 expects both. The view table
  marks every column of view (c) Statements as "—". It does not say whether statements are cut from the code text, the
  identifier text or the raw text. Statement kind matters for `isAllowedQualifier(statement, qualifier)` (SEAM-E044-01
  keys on `CREATE [OR REPLACE] VIEW ${recoverySchema}.v_ace_*`) and for L-GRANT at statement start.
- **Failure scenario:** A builder reports one finding for each item that matches. N1, N2, N3, N5 to N13 then each give
  two L-LITERAL-SCHEMA findings on the same line. T-044-22 fails, or the builder changes the expectations to fit.
  Either way the acceptance test no longer fixes the behaviour. A second builder, reading "may", reports `REFERENCES
  public.account` under L-FK-OUTSIDE only, and T-044-21 fails. If statements are cut from raw text, a leading `/* … */`
  or `-- …` line before `CREATE VIEW` changes the statement kind that RWB-E1-069's exception will test.
- **Required fix:** In SPEC-004 or SPEC-007, state the rule: L-LITERAL-SCHEMA gives one finding per qualified-name
  occurrence (file, line, qualifier), whichever items match it. In SPEC-008, replace "may" with "is": a qualified
  `REFERENCES` outside `${recoverySchema}` gives one L-FK-OUTSIDE finding and one L-LITERAL-SCHEMA finding. In the view
  table, state that view (c) is cut from the identifier text (b), keeping offsets, so statement kind and first word
  never come from a comment or a string. Add one T-044-22 case, `REFERENCES public.t(id)` after a `'--'` literal, with
  the two expected findings.

### REVIEW-RWB-E1-044-S18: The coverage gate is stated per class set, but the named build change measures one combined bundle

- **Severity:** Low
- **Affects:** SPEC-014; Unit Test Applicability (both backend rows); "Verification beyond unit tests" row
  `build.gradle.kts` coverage wiring
- **Evidence:** SPEC-014 declares two surfaces: changed main classes, and test-scope tooling. It says "Each must reach
  at least 80%". The verification table says `recoveryCoverageVerification` "fails below 80% on any of the four counters
  for either class set". The named change adds the tooling classes to the `classDirectories` of the existing task.
  `backend/build.gradle.kts` lines 148–159 hold one `rule { … }` with no `element`, so JaCoCo's default `BUNDLE`
  applies. All class directories are then measured as one total. `implementation-execution-gates.md` line 58: "Each
  required surface must independently meet an 80% coverage gate". Line 59 rejects combined averages in place of surface
  totals. The spec splits backend into two rows itself.
- **Failure scenario:** The recovery main classes measure 76% BRANCH. The new lint and tokenizer, which are large and
  heavily tested, measure 93%. The bundle total is above 80%, so `recoveryCoverageVerification` passes. The evidence
  row then reports a per-set pass that the build never checked.
- **Required fix:** Pick one and state it. (a) Keep the two surfaces and enforce each: a second
  `JacocoCoverageVerification` task, or a second `rule` with `element = "PACKAGE"` and `includes` for the tooling
  package. Each has the four limits at 0.80, and the report shows each set's totals. (b) Declare one backend surface
  (main plus test-scope tooling in one bundle, as testing-standards §6 and squad D-RCV-43 (2) describe), merge the two
  backend rows, and remove "for either class set" and "Each must reach". Either way, say that the gate measures the
  whole recovery main scope, not only the changed classes (implementation gates line 59: untested files included).

### REVIEW-RWB-E1-044-S19: The contract files are not fully aligned with v14-3

- **Severity:** Low
- **Affects:** `contracts/frontend-integrations.json`, `contracts/backend-apis.json` (`CON-RWB-E1-044-002.identifiersOnly`)
- **Evidence:** `frontend-integrations.json` still carries `"specVersion": "v14-2"`, while the spec, the run log
  ("unchanged") and `backend-apis.json` are v14-3. In `backend-apis.json`, `identifiersOnly` reads "single-quoted with
  '', E'' with ', quoted identifiers". The backslash of `\'` was lost in the JSON string, so the escape rule for escape
  strings (`\'`, `\\`) is unreadable. This is the rule that T-044-22 N4 depends on.
- **Failure scenario:** A consumer that checks contract versions against the spec version, such as the plan stage or
  the traceability manager, finds a v14-2 contract in a v14-3 set and cannot tell whether it was reviewed. A reader
  who uses the backend contract as the summary of lexing rules implements `E'…'` without `\'`. That is the N4 defect.
- **Required fix:** Set `frontend-integrations.json` `specVersion` to `v14-3`; its content needs no other change. In
  `identifiersOnly`, write the escape rules with JSON escaping, for example `E'…' with '' , \\' and \\\\`, or refer to
  the SPEC-007 token table instead of restating it.

## 5. Required checks

| Check | Result |
|---|---|
| Authentication and authorization | No endpoint in scope. The read path, TC-E1-044-10 and the §10 read and rerun authority are out of scope by D-RCV-12 with no owner (DG-L10, OI-E044-G). No method-security check applies (AGENTS §3.3 applies to endpoints) |
| Customer and account data protection | Pass. Fixtures are synthetic. BR8 is L-FK-OUTSIDE in every environment. The database refusal is proved only against this repository's grants (T-044-17), and the migration account gets no privilege in `public` (SPEC-017, DG-L13) |
| Audit logging for sensitive financial actions | Not applicable. No case or decision change. The run record is the history table plus the MSG-P3-016 ERROR line (ASM-E044-02, OI-E044-A) |
| KYC, AML, suitability, consent, approval | Not in scope |
| Frontend integration versioning and error contract | Not applicable to code (NO_API_CHANGE, UI out of scope). The contract file version is stale: S19 |
| Secrets and environment configuration | Pass. Migrator credentials come from the environment or key store. The schema pin now holds whether `rwb.flyway.enabled` is true or false (S13 closed). The pin error carries no credential. Container passwords are synthetic |
| Test coverage and evidence | Planned: backend `REQUIRED`, 80% on LINE, INSTRUCTION, BRANCH and METHOD, no waiver. Container tests T-044-10 to T-044-18 run before every MR and are kept apart from unit coverage. Per-surface enforcement is overstated: S18. T-044-08 setup: S16. Lint acceptance precision: S17 |
| Frontend and backend applicability | Frontend `NOT_APPLICABLE` is justified (story v7 §15, no `frontend/` change). Backend `REQUIRED` |
| Precedence and invented requirements | Story deviations are settled by Decision Log v10, the squad register (ASM-E044-11), D-RCV-35 and ADR v3 (DG-L13), or the orchestrator triage, each recorded as a gap. No invented financial, regulatory or security requirement was found. ASM-E044-15 is labelled and does not narrow a control |
| Personal data in artefacts | None. Roles are named by title; no personal name, ID or account number in the spec set |

## 6. Result

| Severity | Count | IDs |
|---|---|---|
| Critical | 0 | — |
| High | 0 | — |
| Medium | 0 | — |
| Low | 4 | S16, S17, S18, S19 |

Round-2 status: S10 (residual), S12, S13, S14 and S15 all CLOSED. Rounds 1 and 2 have no open finding.

No Critical, High or Medium finding remains, so this review does not block the hand-off to the Implementation Planner.
Under `pdlc.md`, a review with Low findings keeps status `FAIL`, and every finding stays visible for disposition.

- S16, S17 and S18 are short corrections to the spec's test and gate text, and the plan can carry them.
- S19 is a contract-file correction.

REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.

**Overall: FAIL (Low only, non-blocking)**
