# Recovery Workbench — backend standards

**Context ID:** `CTX-BACKEND-STANDARDS-V2`
**Version:** 2.0, 16 November 2026
**Applies to:** `th.co.scb.ace.demo.recovery` in the ACE monorepo.

## BS-1 Module structure

- **BS-1.1** One Spring Modulith application module `recovery`. Inside it, nested application modules
  for P1–P10 and S1–S9, each with `api` and `internal`.
- **BS-1.2** A module exposes only `api` interfaces; an `internal` class, entity or repository is never
  injected or imported by another module.
- **BS-1.3** The module map is `backend/src/test/resources/architecture/recovery-modules.yaml`; the
  build reads it, the jar does not package it.
- **BS-1.4** BND-1–BND-5 are ArchUnit/Modulith tests in `RecoveryBoundaryTest`. **BND-6** forbids a
  recovery class from naming a `public` table; it fails the build. BND-1/BND-2 use
  `allowEmptyShould(true)` until those packages exist.
- **BS-1.5** No new dependency without plan approval. Approved for this baseline: Testcontainers
  PostgreSQL, JaCoCo, Vitest (front end), Drools KIE runtime (ADR-012), Temporal SDK (ADR-011).

## BS-2 Database and migrations

- **BS-2.1** Schema `recovery`. Always reference it as `${recoverySchema}`; never a literal.
- **BS-2.2** One migration file per story: `V<seq>__<story>_<name>.sql`; 4-digit contiguous sequence
  taken at merge; line 1 `-- Story: <key>`. A corrective file takes the next sequence, keeps the story
  key and adds line 2 `-- Fix: <reason>`. No `R__*.sql`.
- **BS-2.3** Flyway: own bean, folder `db/modulemigration/recovery/`, history table
  `flyway_schema_history_recovery`, `outOfOrder(false)`, `baselineVersion("0")`,
  `baselineOnMigrate(true)`, `cleanDisabled(true)`, `createSchemas(false)`.
- **BS-2.4** Never edit a merged migration. A change is a new corrective file.
- **BS-2.5** Recovery migrations contain no `GRANT`/`REVOKE`; the view grants live in the view story
  and are executed by the migration account with the ACE DBA role for the release window.
- **BS-2.6** Lint as a unit test: name, sequence, one non-fix file per story, header, no literal
  schema, no `SET search_path`, no repeatable file, no `GRANT`/`REVOKE`.
- **BS-2.7** Read ACE data only through `recovery.v_ace_*`. No FK into `public`. A link is a
  business-key column.
- **BS-2.8** No inbound load, source copy, tracker or data-quality load table. D-RCV-35 removed them.
- **BS-2.9** Testcontainers PostgreSQL 16, `@Tag("recovery-it")`, `recoveryIntegrationTest` outside
  `check`, fail (not skip) without Docker.

## BS-3 API

- **BS-3.1** Base `/api/recovery/v1`; plain JSON; UUIDs; MSG codes; API Specification v4.
- **BS-3.2** Method security on every endpoint, naming the capability area and operation.
- **BS-3.3** Error response `{ code, messageId, message, fieldErrors, traceId }`; exact message text
  from the message table.
- **BS-3.4** Pagination `page/size/sort`, default 25, max 100; stable sort key.
- **BS-3.5** `Idempotency-Key` on create/move commands; duplicate returns the first result.
- **BS-3.6** No entity in a response; map to a DTO. No lazy loading outside a transaction.
- **BS-3.7** Additive changes only within v1; a breaking change creates v2.

## BS-4 Security, privacy and audit

- **BS-4.1** Entra ID SSO/MFA; roles from the role-to-permission matrix.
- **BS-4.2** Mask personal data at the API by role; never send an unmasked value to an unauthorised role.
- **BS-4.3** Write the decision-log entry before the action; a failed write blocks the action.
- **BS-4.4** Write an access-log entry for every read of personal data and every admin action.
- **BS-4.5** No credential in code, config, test or log. Secrets from Key Vault or environment.
- **BS-4.6** No personal data in a log line, metric label, trace tag or Temporal history; use the
  payload codec.
- **BS-4.7** Break-glass is time-boxed, logged and reviewed.

## BS-5 Batch and scheduling

- **BS-5.1** Every Epic 1–2 scheduled job is Quartz or Spring Batch; no Temporal Schedules before
  Epic 3.
- **BS-5.2** JOB-05 timer check runs behind the `TimerScheduler` port; Epic 3 swaps in a Temporal
  implementation without a caller change.
- **BS-5.3** A job is idempotent for a business date; a second run writes DUPLICATE and does nothing.
- **BS-5.4** A job writes its outcome (date, count, start, end, status) and alerts on failure.
- **BS-5.5** Every job has a run book with owner, schedule, failure message and recovery action.

## BS-6 Workflow and rules

- **BS-6.1** Temporal workflow code is deterministic: no clock, random, I/O or direct DB access.
  I/O is in activities.
- **BS-6.2** Workflow ID `case-{caseId}`; namespace `rwb-recovery`; task queues `rwb-case`,
  `rwb-integration`, `rwb-platform`.
- **BS-6.3** The package version is chosen at evaluation time, returned in the result and written to
  the decision log.
- **BS-6.4** Drools is embedded; no KIE Server, Business Central or KJAR. Authoring is XLS; approval is
  RW-RISK; the author cannot approve.
- **BS-6.5** `rule_row` is the catalog; stories read `action_text`, `owner_role`, `timer_spec` and
  `target_queue_code` by rule ID and version.
- **BS-6.6** `payment_match_rule` is not created; payment matching is package PAYMENT_MATCH.
- **BS-6.7** Feature flags `rwb.p3.temporal` and `rwb.p3.drools` return the previous path when off.

## BS-7 Quality gates

- **BS-7.1** Test before code; a change with no test is not complete.
- **BS-7.2** 80% line/branch coverage on recovery packages; no global drop.
- **BS-7.3** No disabled, skipped or weakened test. A skip names the reason and the approval.
- **BS-7.4** Every finding from a review is visible; a Critical/High finding blocks the handoff.
- **BS-7.5** Record the command, environment and result for every test claim.

## BS-8 N/A and evidence scope

- N/A — this repository does not contain the ACE source; implementation evidence is linked, not embedded.
- N/A — no production credentials are held; secrets come from the runtime secret store.
