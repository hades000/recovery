# Agent run log: Technical Specifier, INC-010-epic-1-RWB-E1-069

| Field | Value |
|---|---|
| Date | 2026-11-17 |
| Agent | Technical Specifier (`.claude/agents/technical-specifier.md`). The run follows `aisdlc/RUN-BRIEF.md`. |
| Started by | Human (stage start) |
| Scope | This run wrote only to `aisdlc/output/INC-010-epic-1-RWB-E1-069/specify/`, and to `review/` through the gate. It did not run git, did not edit code and did not change the document set. |
| MCP | Jira, Confluence, GitLab and Figma were N/A. No connector is configured (RUN-BRIEF rule 5). |

## Inputs read

- `RUN-BRIEF.md`.
- Increment card INC-010.
- Story RWB-E1-069 v1 (Story Files v7).
- ACE Source Views v1.sql.
- Physical Schema v6.sql. Read for the header, the extension tables, the helper functions, the views, the dictionary rows and the commented grants.
- ACE Team Stories v1 (RWB-ACE-001).
- Story RWB-E1-001 v1.
- RWB-E1-001 Specification Rulings v2.
- ADR v3 (ADR-010).
- Decision Log v10 (DL43 and the D-RCV-35 row).
- `d-rcv-35-ace-db-alignment.md`.
- `INC-001-decisions.md` (D-RCV-28, -34 and -37).
- Build Notes Epic 1 v6.
- Environment and Deployment Design v4.
- Security and Access Design v4.
- Build Sequence v6.
- ACE Schema PostgreSQL v1.sql.
- backend-context, backend-standards and testing-standards.
- `phase0-standards-audit.md`.
- `README.md`.
- `open-items.md`.
- `INDEX.md`.
- `Traceability_Matrix.md`.
- The RWB-TE-001 v2 spec.
- `specification-execution-gates.md`.
- Code (read only):
  - `RecoveryFlywayConfig`
  - `RecoveryBoundaryTest`
  - `RecoveryMigrationLintTest`
  - `RecoveryDatabaseIT`
  - `PlatformInfoController`
  - `infra/postgres/init/*`
  - `02-ace-tier2-probe.sql`
  - `docker-compose.yml`
  - `.env`
  - `backend/build.gradle.kts` (JaCoCo)

## Checks computed

- All 21 Tier 1 source tables named in story §11 exist in ACE Schema PostgreSQL v1. The 14 Tier 2 tables do not; they are added by RWB-ACE-001.
- The view bodies A1 to B14 match between ACE Source Views v1 and Physical Schema v6: 607 lines each, and the diff is empty. Each file holds 30 `CREATE OR REPLACE VIEW` statements.
- The 35 ACE source table names were compared with the 93 recovery tables. They collide on one name only, `hearing`.
- The local `ALTER DEFAULT PRIVILEGES` for `rwb_migrator` grants INSERT, UPDATE and DELETE on new tables to `recovery_svc`. Views count as tables for this purpose. The spec therefore adds a per-view `REVOKE ALL` (SPEC-004 step 4).
- `RecoveryFlywayConfig` sets `outOfOrder(false)`, `baselineVersion("0")` and `baselineOnMigrate(true)`. These settings give DG-L20.
- `recoveryCoverageVerification` enforces LINE and BRANCH at 0.80.

## Errors

`grep -P` is not supported under this locale. The run used `grep -o` and `awk` instead. No other errors occurred.

## Outputs

- `spec.md`
- `compliance-validation.md`
- `assumptions.md`
- `document-gaps.md`
- `shared-updates.md`
- `contracts/backend-apis.json`
- `contracts/frontend-integrations.json`
- `figma/figma_report.md`
- `agent-run-log.md`

## Spec gate

A Compliance Reviewer runs as a `general-purpose` subagent and writes `../review/spec-gate-review.md`. **Result: FAIL.** The review in `../review/spec-gate-review.md` raised 16 findings: 0 Critical, 3 High (101–103), 6 Medium (104–109) and 7 Low.

| Severity | ID | Finding |
|---|---|---|
| High | 101 | The verbatim `ace_to_date` raises an error on impossible dates on PostgreSQL 16.16, which breaks BR6. |
| High | 102 | The Section B grant pattern leaves out the transient CREATE grant, so `ALTER VIEW ... OWNER` fails. |
| High | 103 | In local Flyway mode, nothing grants `ace_view_owner` SELECT on the Tier 2 tables. |
| Medium | 104 | The coverage gate covers lines and branches only. |
| Medium | 105 | The X2 message is unreachable because `ace_batch_run` fails first. |
| Medium | 106 | The `sourceViews` equality check breaks between the Section A and Section B merges. |
| Medium | 107 | The Flyway-mode hand-over from the RWB-E1-001 spec has not been taken up. |
| Medium | 108 | There is no personal-data classification and no D-RCV-35 §3.3 controls; out of scope is missing. |
| Medium | 109 | Several AC clauses have no specified test, among them AC1's history and re-run, AC5's 1,062 fields and its totals, and BR7's record columns. |

Under the agent's instructions and `pdlc.md`, this stage stops and does not remediate on its own. A human must either resolve the findings, then rerun this stage and the gate as `spec-gate-review-2.md`, or explicitly accept them. The handoff to the Implementation Planner is blocked until then.

---

# Run 2: remediation of spec gate round 1 (Technical Specifier, 2026-11-17/18)

## Instruction and triage

- Stage started by the orchestrator as remediation run 1 after `../review/spec-gate-review.md` (FAIL: 3 High, 6 Medium, 7 Low).
- Orchestrator triage by Claude Code, the AI agent running this pipeline (not a human decision): fix every finding, Low included (D-RUN-09); answer a finding shown wrong with evidence; 101 specify required behaviour and test impossible dates on PG 16, record the source defect; 102/103 complete, testable grant sequence in both local modes; 104 use the RWB-TE-001 counters; 109 a test for every AC clause, citing both count sources; the narrow lint exception (`public.` only inside `CREATE [OR REPLACE] VIEW ${recoverySchema}.v_ace_*`) from the RWB-E1-044 spec.

## Inputs read

- `aisdlc/RUN-BRIEF.md` (D-RUN-07, D-RUN-08); `.claude/agents/technical-specifier.md`.
- Run-1 outputs in `specify/`; `../review/spec-gate-review.md`.
- `INC-009-epic-1-RWB-E1-001/specify/spec.md` (counting table, T6, T7, SPEC-010, ASM-E1001-01/-07).
- `INC-001-epic-1-RWB-E1-044/specify/spec.md` v14-2 (SPEC-016, SEAM-E044-01/-02/-04, rule IDs).
- `INC-002-epic-1-RWB-TE-001/specify/spec.md` v3 (SPEC-002, -003, -020, -021 withdrawn, T-TE001-10).
- Story RWB-E1-069 v1 (§3, §4, AC1–AC8, BR1–BR9, §10–§19); ACE Source Views v1; Physical Schema v6 (extension tables, helpers, views, `sys_fields`); Data Classification and Personal Data Inventory v4; D-RCV-35 (§3.2, §3.3, §8.2, §12 R5); D-RCV-36 (A.7, row 18); ACE Team Stories v1 RWB-ACE-001; Non-Functional Specification v3.
- Code and config, read only: `RecoveryFlywayConfig`, `RecoveryDatabaseIT`, `RecoveryBoundaryTest`, `RecoveryMigrationLintTest`, `build.gradle.kts`, `application.yaml`, `.env.example`, `docker-compose.yml`, `infra/postgres/init/*`, `02-ace-tier2-probe.sql`, `README.md`, audit A-02/A-04.

## Run 2 probe evidence ([E2])

A throwaway `postgres:16.16-alpine` container (`docker run --rm`), separate from the project stack, was started, used with synthetic objects in its own database, then stopped and removed. Nothing in the shared stack, the repository code or the document set was touched. Scripts: the session scratchpad (`probe1.sql`, `probe2.sql`), not kept in the repository. Results:
- Source `ace_to_date` expressions: `'2026-02-30'::date`, `to_date('20261345','YYYYMMDD')`, `to_date('31/02/2026','DD/MM/YYYY')`, `'0000-01-01'::date` → `date/time field value out of range`; `to_date('00000000','YYYYMMDD')` → `0001-01-01 BC`.
- `pg_input_is_valid(text,'date')` exists on PG 16. A shape-normalising body with it returned the SPEC-002 table exactly, as literal calls, through a view over dirty rows (5 NULL, 1 date) and under DateStyle `SQL, DMY` and `German`.
- `ace_to_boolean` and `ace_mask_value` (source bodies) return the SPEC-020 values.
- CREATE VIEW over `public.account` needs USAGE on `public` (else `permission denied for schema public`), not SELECT on the table.
- A new view gets `recovery_svc=arwd` from the default privileges (X8).
- ALTER VIEW OWNER needs membership of the new owner (`must be able to SET ROLE`) and CREATE on the schema for the new owner (`permission denied for schema recovery`).
- After REVOKE CREATE the owner holds neither USAGE nor CREATE on `recovery`, and the view still works. A member of the owner role can GRANT SELECT.
- With the owner lacking SELECT on the table, `recovery_svc` gets `permission denied for table account` (REVIEW-103 confirmed). With it: rows returned. Direct `public.account` read → `permission denied for schema public`; INSERT/DELETE on the view → `permission denied for view v_ace_account`; a role without a grant → the same.
- EXECUTE on a function in a view is checked for the caller: `permission denied for function` until `recovery_svc` holds EXECUTE; the owner needs none.
- Missing relation text: `relation "public.valuation" does not exist` (quoted).
- Verbatim check: after removing comments and blank lines, Source Views v1 lines 94–711 equal Physical Schema v6 lines 6204–6821 (524 lines; Section A 313, Section B 211); helpers identical. This supersedes run 1's "607 lines".

## Outputs

- Copied before change: `spec.run1.md`, `assumptions.run1.md`, `document-gaps.run1.md`, `compliance-validation.run1.md`, `shared-updates.run1.md`, `contracts/backend-apis.run1.json`.
- Rewritten: `spec.md` (SPEC-001..020; 42 coverage rows), `assumptions.md` (ASM-001..015), `document-gaps.md` (DG-L01..L28, no blocker), `compliance-validation.md`, `shared-updates.md` (OI-069-A..K, DG-INC010-01..11), `contracts/backend-apis.json`.
- New: `gate-response.md` (16 of 16 fixed).
- Not changed: `contracts/frontend-integrations.json`, `figma/figma_report.md`, the review file, any shared file, any code. No git command was run.

## Spec gate round 2

A `general-purpose` subagent runs the Compliance Reviewer (`.claude/agents/compliance-reviewer.md`) and writes `../review/spec-gate-review-2.md`. Result: see that file.

Round 2 result (2026-11-18, `../review/spec-gate-review-2.md`, REVIEW-RWB-E1-069-SG2): **FAIL**, with 0 Critical, 1 High, 1 Medium and 3 Low findings.
- Round-1 findings: 101–116 are resolved. 103, 107 and 109 hold within this spec, but they are overtaken by sibling-spec revisions; 111 is partly resolved.
- New findings:
  - 117 (High): the migration-account rights conflict with RWB-E1-044 v14-3 SPEC-017, OI-E044-I and T-044-17.
  - 118 (Medium): the spec is stale against RWB-E1-001 Revision 2: the S1/S2/S3 switches, `RecoveryDatabaseIT`, the totals 1,382/1,078 and 526 personal fields.
  - 119 (Low): "V0001" is used as a fixed name.
  - 120 (Low): the AC2 `has_table_privilege` checks run in the wrong session.
  - 121 (Low): test-setup ambiguities.
- Under the agent rules this stage stops here. The handoff to the Implementation Planner is blocked.
