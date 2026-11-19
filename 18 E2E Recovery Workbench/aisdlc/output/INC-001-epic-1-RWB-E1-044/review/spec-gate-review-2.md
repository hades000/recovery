---
title: "Spec gate review round 2: RWB-E1-044 (spec v14-2)"
run_id: INC-001-epic-1-RWB-E1-044
story: RWB-E1-044
gate: Specification (Compliance Reviewer, spec-gate mode)
round: 2 (round 1 is `spec-gate-review.md`, S01 to S11)
date: 2026-11-17
result: FAIL (Low findings only; non-blocking, REVIEW_GATE_WARNING below)
---

# Spec gate review round 2: RWB-E1-044

## 1. Scope

Reviewed, all under `aisdlc/output/INC-001-epic-1-RWB-E1-044/specify/`: `spec.md` (v14-2), `gate-response.md`,
`compliance-validation.md`, `assumptions.md`, `document-gaps.md`, `shared-updates.md`,
`contracts/backend-apis.json`, `contracts/frontend-integrations.json`, `figma/figma_report.md`, `agent-run-log.md`.
The `*.run1.*` files were used only to confirm what changed.

Checked against:

- Round 1 review `review/spec-gate-review.md` (S01 to S11).
- `AI-SDLC-BUILD-LOG.md`: D-RUN-07, D-RUN-08 (2026-11-17T23:26), D-RUN-13 (2026-11-17T23:49), and the
  orchestrator triage for RWB-E1-044 (2026-11-17T23:40:23, "Gate triage", REMEDIATE). These rulings were
  applied as given and are not re-opened here.
- `aisdlc/RUN-BRIEF.md` (precedence, D-RUN-07, D-RUN-08, document-gap rules).
- `aisdlc/docs/decisions/`: `INC-001-decisions.md` (D-RCV-05, -12, -28 (1)–(4), -40, -43, -44, -45, -48),
  `decision-register.md` (statuses; L-RCV-03, L-RCV-07), `d-rcv-35-ace-db-alignment.md` (U4, Section A).
- Document set v14 (`17 AI-First SDLC Repository v2/requirement/legacy/`, read only): story RWB-E1-044 v7
  (§3, §5, §7, §10, §12–§17); RWB-E1-069 v7 (§3 preconditions, flows 1 and 7); RWB-E1-056 v7; Decision Log v10
  row D-RCV-28; ADR v3 ADR-010; Environment and Deployment Design v4 §5; Physical Schema v6 (header, Section A
  `v_ace_account`, `sys_fields` rows, commented grant block); API Specification v4 `getAdminJobs`; Build
  Sequence v6.
- Code: `RecoveryFlywayConfig.java`, `RecoveryProperties.java`, `application.yaml`, `RecoveryMigrationLintTest.java`,
  `RecoveryDatabaseIT.java`, `backend/build.gradle.kts` (test, IT and JaCoCo tasks),
  `db/modulemigration/recovery/README.md`, `infra/postgres/init/00-roles-and-databases.sh`,
  `10-load-ace-database.sh`, `20-grants.sql.inc`.
- `aisdlc/.github/rules/specification-execution-gates.md`, `implementation-execution-gates.md`, `pdlc.md`;
  `aisdlc/.github/contexts/testing-standards.md` §6; `aisdlc/evidence/phase0-standards-audit.md` (A-17, A-19);
  `aisdlc/requirement/Traceability_Matrix.md` §2, §3, §7.

No git command was run. Only this file was written. No question was put to the user (L-RCV-03).

## 2. Round-1 findings

| Finding | Severity (round 1) | Status | Evidence |
|---|---|---|---|
| S01 Literal-schema rule blocks ADR-010 view migrations; conflict not recorded | High | **CLOSED** | DG-L09 cites ADR v3 ADR-010 ("30 views in two migrations … next free sequence", verified line 361), D-RCV-35 Section A ("Ships with RWB-E1-069", verified), Env v4 §5 (verified lines 120, 130), Physical Schema v6 Section A (`FROM public.account a`, verified line 6249) and RWB-E1-069 v7 against Decision Log v10 D-RCV-28, squad D-RCV-28 (2), the baseline lint and BS-2.6, with Blocker = No and the triage reason. SPEC-007 ships the rule as D-RCV-28 defines it; SPEC-016 gives one registry and one qualifier method and names SEAM-E044-01 (owner RWB-E1-069, not built), with a seam-marker fixture in T-044-02. No ACE-schema placeholder is invented. OI-E044-F is proposed. The status line now reports `CONTRADICTIONS: 7` and lists them. This matches the orchestrator triage. Residual seam detail: see S14 |
| S02 Job-monitor work assigned to RWB-E1-056 | Medium | **CLOSED** | Every receiver reference to RWB-E1-056 is gone (searched all current files; the remaining mentions are source rows, DG-L04, DG-L10 and the figma audit note). SPEC-017 lists the parts as out of scope with owner "None named"; DG-L10 cites D-RCV-12 ("deferred to the story that builds the job monitor", verified, register status Active) against RWB-E1-056 v7 (`job_catalog`, no migration runs, verified) and API Specification v4 `getAdminJobs` (`type` a free string, verified); OI-E044-G asks the BA / Product Owner for an owner. Both contract files carry `owner: null` |
| S03 80% gate waived for lint and comparator | Medium | **CLOSED** | SPEC-014 holds both class sets to 80% on LINE, INSTRUCTION, BRANCH and METHOD with no waiver, citing D-RCV-40 and D-RCV-43 (2) (verified) and testing-standards §6. The `build.gradle.kts` change is named and is feasible against the current tasks (class set from `sourceSets.test` output filtered to the tooling package, JUnit classes excluded by name, two new limits, execution data from `test`). The comparator is split so unit tests reach it (T-044-19). ASM-E044-07 withdraws the run-1 waiver and makes any shortfall a plan-gate finding, never an exclusion |
| S04 Container setup cannot run T-044-17; skips the bean | Low | **CLOSED** | SPEC-011 builds the container from `infra/postgres/init` with `RWB_LOAD_REFERENCE_SCHEMA=false`. Verified in `10-load-ace-database.sh` and `20-grants.sql.inc`: ACE schema v1 is loaded into `public`, an empty `recovery` is created and owned by `rwb_migrator`, and `public` is revoked from PUBLIC, so `REFERENCES public.account` as `rwb_migrator` fails. Every case builds Flyway through `RecoveryFlywayConfig#recoveryFlyway` with only `rwb.flyway.location` overridden. (Scope of the T-044-17 claim: S15) |
| S05 Version not mandatory; no-SQL claim too broad | Low | **CLOSED** | SPEC-003 table makes the version mandatory for validation failures and part-way failures, with `recoveryFlyway` only for failures with no version. The no-SQL claim is narrowed to the bean's own line, and the rethrown Flyway text (failing DDL, no personal data, password separate) is stated and accepted. Flyway API reliance is labelled ASM-E044-12. The contract `failureReport` matches |
| S06 L-SEARCH-PATH misses forms | Low | **CLOSED** | SPEC-007 matches the identifier `search_path` before string blanking; the form table lists `SET LOCAL/SESSION`, `set_config('search_path', …)`, `ALTER ROLE/DATABASE/FUNCTION … SET`, `RESET`, each marked New, with failing fixtures in T-044-20. Physical Schema v6 holds `search_path` only in its header `SET` (line 11), so no data literal is caught by mistake today |
| S07 D-RCV-48 test not fully covered | Low | **CLOSED** | T-044-18 proves the baseline at 0 and `V0001` applied on a non-empty `recovery`. DG-L12 records that the register text says `ace` and settles it by Decision Log v10 and L-RCV-07 (verified: "D-RCV-47 is superseded") |
| S08 Story lines not mapped | Low | **CLOSED** | Coverage rows now cover story §3 (migration and drift accounts, `RWB_SCHEMA`, slots), §10 (pipeline account, deployment, rerun and read authority) and §12/§14/§15/§16 items. A TC-E1-044-01..10 to T-044 table is added, with TC-E1-044-10 explicitly out of scope |
| S09 Squad-register text attributed to Decision Log v10 | Low | **CLOSED** | Sources split S-DL10 and S-SQREG. Verified: Decision Log v10 row D-RCV-28 holds naming, header, fix line and "recovery in every environment" only; parts (2)–(4) are in `INC-001-decisions.md` (row Active in `decision-register.md`). SPEC-002 now attributes "no per-environment override" to story v7 §13. DG-L11 records the refused-clean deviation and its basis; ASM-E044-11 labels the use of the register |
| S10 Values outside the gate vocabulary | Low | **PARTIALLY CLOSED** | Headings are exact; Coverage Type is only `DIRECT` / `INHERITED_EXISTING_BEHAVIOR`; Status is only `COVERED`; Changes Required is `YES` / `NO`; frontend row is `NOT_APPLICABLE` / `NOT_APPLICABLE`. Residual: the two backend rows set Unit Tests to `REQUIRED (T-044-08, T-044-09)` and `REQUIRED (T-044-01 to T-044-07, T-044-19 to T-044-21)`, not the bare value `REQUIRED`. Fix: set the cell to `REQUIRED` and move the test IDs to "Test Acceptance Criteria" or "Evidence and Rationale" |
| S11 Traceability rows do not match the matrix | Low | **CLOSED** | `shared-updates.md` §3 row uses the matrix columns (`INC \| Story \| Business \| Functional \| Spec / plan / evidence \| Status`, verified against matrix line 47); RWB-E1-044 is proposed for the §2 `BR-RWB-013` row (today it lists RWB-E1-001, -069, -064, -065, TE-004); NFR-027 and NFR-052 are cited by source ID with the reason; a §7 evidence-index row is proposed |

## 3. Orchestrator rulings and decisions applied

| Ruling | Applied in the spec | Result |
|---|---|---|
| Triage S01: ship the D-RCV-28 lint; gap; narrow exception as RWB-E1-069 seam | SPEC-007 consequence paragraph, SPEC-016 SEAM-E044-01, DG-L09, CLAR-012, OI-E044-F | Applied |
| Triage S02: no receiving story inferred; out of scope + gap + open item | SPEC-017, DG-L10, OI-E044-G, CLAR-002, contracts, figma report | Applied |
| Triage S03: no coverage waiver | SPEC-014, Unit Test Applicability, ASM-E044-07, OI-E044-H | Applied |
| D-RUN-07: no migration number fixed | Change Scope "Production migration file"; CLAR-005; DG-L04; SPEC-015 README rewording; fixture numbers labelled test-only (ASM-E044-14) | Applied |
| D-RUN-08: depend only on the repository or earlier stories; later work as seams | Change Scope "Dependencies"; SEAM-E044-01 to -04; SPEC-017. E1-044 is build order 1 (Build Sequence v6, verified) | Applied |
| D-RUN-13: schema-prefix lint checks identifiers only | SPEC-007 text preparation and "Identifiers only"; item 4 of L-LITERAL-SCHEMA; T-044-21; contract `identifiersOnly`. The 297 `'public.…'` lines from line 5826 of Physical Schema v6 are verified by search | Applied (lexing precision: S12) |

The spec, `gate-response.md`, `assumptions.md` and `agent-run-log.md` attribute these rulings to the orchestrator
and claim no human ruling. Observation only, not a finding: `gate-response.md` and `agent-run-log.md` give
D-RUN-13 as "2026-11-17T23:50"; the build log records it at 23:49 (decision row and event row 23:49:16). The
content cited is correct.

## 4. New findings

IDs continue from round 1.

### REVIEW-RWB-E1-044-S12: Comment and string removal is not specified as one lexical pass

- **Severity:** Low
- **Affects:** SPEC-RWB-E1-044-007 (text preparation), SPEC-016 (parsed file model), T-044-21; BR2 / X3 / AC5, BR8
- **Evidence:** SPEC-007 lists comment removal as one step and then, "for L-LITERAL-SCHEMA and L-FK-OUTSIDE only",
  blanks string literals; L-SEARCH-PATH runs on "comment-stripped text before string literals are blanked". It
  does not say that comment removal must skip text inside quotes or dollar bodies. Only statement splitting is
  described as quote-aware. The baseline lint skipped whole `--` lines only, so it could not hide code; the
  D-RUN-13 stripping is new and can.
- **Failure scenario:** a fixture with `INSERT INTO ${recoverySchema}.t (v) VALUES ('/*');` on line 2,
  `CREATE TABLE public.x (id int);` on line 3 and `-- */` on line 4. A comment pass that does not know about
  quotes removes lines 2 to 4 as one block comment, and L-LITERAL-SCHEMA reports nothing. `'a--b'` followed by
  code on the same line hides that code the same way. PostgreSQL also nests block comments
  (`/* a /* b */ public.x */` is all comment), and `E'…'` literals allow `\'`.
- **Required fix:** State that text preparation is one left-to-right pass that recognises `--` comments, nested
  `/* */` comments, `'…'` with `''`, `E'…'` with `\'`, `"…"` quoted identifiers and `$tag$…$tag$` bodies, and
  produces (a) comment-free text with strings kept, for L-SEARCH-PATH, and (b) comment- and string-blanked text
  with line numbers kept, for the schema-prefix rules. Add to T-044-21 negative fixtures where `'/*'`, `'--'`
  and `E'\''` precede a real `public.` reference, and a nested-comment positive fixture.

### REVIEW-RWB-E1-044-S13: The schema pin only runs when the recovery Flyway bean is created

- **Severity:** Low
- **Affects:** SPEC-RWB-E1-044-002, T-044-08, audit A-17
- **Evidence:** SPEC-002 places the check "on bean creation" of `recoveryFlyway`. `RecoveryFlywayConfig` is
  `@ConditionalOnProperty(name = "rwb.flyway.enabled", …, matchIfMissing = true)`, and `rwb.flyway.enabled` can be
  set to false through relaxed binding (`RWB_FLYWAY_ENABLED`). `application.yaml` also uses `rwb.schema` for
  `hibernate.default_schema`, and `PlatformInfoController` reads `properties.schema()`. Squad D-RCV-45 (ACE)
  already describes a mode where the recovery Flyway bean is off. Audit A-17: "Nothing pins `rwb.schema` to
  `recovery`".
- **Failure scenario:** `RWB_FLYWAY_ENABLED=false` and `RWB_SCHEMA=rwb_case`. No Flyway bean is created, so no
  check runs; the service starts and JPA uses schema `rwb_case`. A-17 stays open in that mode.
- **Required fix:** Make the pin independent of the Flyway flag, for example a check on `RecoveryProperties`
  binding (record constructor or a validated properties class). T-044-08 covers both values of
  `rwb.flyway.enabled`. Keep the error a configuration error with no message ID (ASM-E044-03).

### REVIEW-RWB-E1-044-S14: The RWB-E1-069 grant seam does not name L-LITERAL-SCHEMA

- **Severity:** Low
- **Affects:** SPEC-016 SEAM-E044-02, DG-L05, OI-E044-B
- **Evidence:** D-RCV-35 U4 "Adds 30 views and the grant they need"; Env v4 §5: Section A ships "with the grants
  and the revoke from PUBLIC", and `ace_view_owner` "holds SELECT on the ACE tables they read"; Physical Schema
  v6 lines 6830–6831 (commented grant block): `GRANT USAGE ON SCHEMA public …`, `GRANT SELECT ON public.account, …`.
  Under SPEC-007 these statements fail L-LITERAL-SCHEMA (item 3, bare `SCHEMA public`; item 4, `public.`), not
  only L-GRANT. SEAM-E044-01, as the triage defines it, allows `public` only inside `CREATE [OR REPLACE] VIEW
  ${recoverySchema}.v_ace_*` and "never … any other statement kind". SEAM-E044-02 names only L-GRANT and
  L-KEY-DUP, and DG-L05 does not cite D-RCV-35 U4.
- **Problem:** The record handed to RWB-E1-069 understates the conflict. The owner of OI-E044-B would resolve
  L-GRANT and still find the grant statements rejected by L-LITERAL-SCHEMA, with SEAM-E044-01 worded to exclude
  them. This does not change what E1-044 builds, and it does not re-open the triage on S01.
- **Required fix:** In SEAM-E044-02, DG-L05 and OI-E044-B, name L-LITERAL-SCHEMA (items 3 and 4) as also hit by
  the Section A grants on `public`, and cite D-RCV-35 U4 in DG-L05. Leave SEAM-E044-01 as triaged; state that any
  allowance for grant statements is part of the OI-E044-B resolution.

### REVIEW-RWB-E1-044-S15: A RWB-E1-069 precondition attributed to RWB-E1-044 is not recorded, and T-044-17 is stated more widely than it holds

- **Severity:** Low
- **Affects:** `document-gaps.md`; SPEC-016 / SPEC-017; coverage row BR8; T-044-17
- **Evidence:** RWB-E1-069 v7 §3 (line 44): "The recovery migration account holds the ACE DBA role for the release
  window, so it can grant on schema `public` and set a view owner (RWB-E1-044)." RWB-E1-044 v7 §3 and §10 name a
  migration account only, with no DBA role. In this repository `rwb_migrator` has no privilege in `public`
  (`00-roles-and-databases.sh`, `20-grants.sql.inc`), and SPEC-001 inherits that. The spec cites RWB-E1-069 v7
  for DG-L05 and DG-L09 but not for this line. The BR8 coverage row and T-044-17 call the database refusal of
  `REFERENCES public.account` "defence in depth".
- **Problem:** A later story names E1-044 as the source of a migrator privilege that E1-044 neither builds nor
  declines. Under D-RUN-08, the RWB-E1-069 spec could treat it as delivered. And if the migrator does hold ACE DBA
  rights while migrations run, the database would accept a foreign key into `public`. T-044-17 proves the local
  catalog only, and in that case the lint (L-FK-OUTSIDE) is the only control.
- **Required fix:** Add a document-gap row: RWB-E1-069 v7 §3 against RWB-E1-044 v7 §3/§10 and
  `infra/postgres/init/20-grants.sql.inc`. Blocker = No for E1-044, because the story does not grant or need
  that role. In SPEC-017 or SEAM-E044-02, state that E1-044 does not provide it (owner: RWB-E1-069 or the
  environment). Qualify the BR8 row and T-044-17 as proof against this repository's catalog grants, with
  L-FK-OUTSIDE as the control in every environment.

## 5. Required checks

| Check | Result |
|---|---|
| Authentication and authorization | No endpoint in scope. The read path, its access test TC-E1-044-10 and the §10 authority are out of scope by D-RCV-12, with no owner named (DG-L10, OI-E044-G). No method-security check applies to this story |
| Customer and account data protection | Pass. Fixtures are synthetic. BR8 is a dedicated lint rule (L-FK-OUTSIDE); the scope of the database-level proof is in S15 |
| Audit logging for sensitive financial actions | Not applicable. No case or decision change. The run record is the history table plus the MSG-P3-016 ERROR line (ASM-E044-02, OI-E044-A) |
| KYC, AML, suitability, consent, approval | Not in scope |
| Frontend integration versioning and error contract | Not applicable. NO_API_CHANGE, UI out of scope; contracts record the out-of-scope endpoint and screen with `owner: null` |
| Secrets and environment configuration | Pass. Migrator credentials come from the environment or key store; container passwords are synthetic test values. Schema pin gap in one mode: S13 |
| Test coverage and evidence | Planned correctly: backend main and test-scope tooling both `REQUIRED` at 80% on four JaCoCo counters, no waiver; container tests T-044-10 to T-044-18 before every MR (D-RCV-44), kept separate from unit coverage |
| Frontend and backend applicability | Frontend `NOT_APPLICABLE` justified (story v7 §15, no `frontend/` change). Backend `REQUIRED` |
| Precedence and invented requirements | Story deviations settled by Decision Log v10 D-RCV-28, squad register (labelled ASM-E044-11), D-RCV-05, D-RCV-12 or the orchestrator triage, each recorded as a gap. No invented financial, regulatory or security requirement found |
| Personal data in artefacts | None. No real names in the spec set; roles are named by title |

## 6. Result

| Severity | Count | IDs |
|---|---|---|
| Critical | 0 | — |
| High | 0 | — |
| Medium | 0 | — |
| Low | 5 | S10 (residual), S12, S13, S14, S15 |

Round-1 status: S01–S09 and S11 CLOSED; S10 PARTIALLY CLOSED.

No Critical, High or Medium finding remains, so the hand-off to the Implementation Planner is not blocked by
this review. Under `pdlc.md`, a review with Low findings keeps status `FAIL`, and every finding stays visible for
disposition. The Implementation Planner can carry S12 and S13 into the plan. S10, S14 and S15 are spec and
document-gap text corrections.

REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.

**Overall: FAIL (Low only, non-blocking)**
