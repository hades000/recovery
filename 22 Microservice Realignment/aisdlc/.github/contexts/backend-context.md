# Recovery Workbench — backend context

**Context ID:** `CTX-BACKEND-RWB-V2`
**Version:** 2.0, 16 November 2026
**Scope:** server-side implementation of `th.co.scb.ace.demo.recovery` in the ACE monorepo.
**Evidence labels:** `IMPLEMENTED` (verified in code or build), `DOCUMENTED/REQUIRED` (source design),
`RECOMMENDED`, `N/A`. This repository does not contain the ACE source; implementation facts come from
the ACE monorepo and the two preserved story runs.

## 1. Stack and runtime

| Item | Value | Evidence |
|---|---|---|
| Language | Java 21 (Spring Boot 4.2.0-M2 baseline in ACE) | `DOCUMENTED/REQUIRED`, ACE build |
| Framework | Spring Boot, Spring MVC, Spring Data JPA, Spring Security, Spring Batch, Spring Session, Spring Cloud Azure, Spring Data REST, Spring HATEOAS | `DOCUMENTED/REQUIRED` |
| Module system | Spring Modulith application module `recovery` with nested modules | `IMPLEMENTED` (RWB-TE-001) |
| Database | PostgreSQL; schema `recovery`; Flyway | `DOCUMENTED/REQUIRED`; `IMPLEMENTED` for E1-042 |
| Migrations | `backend/src/main/resources/db/modulemigration/recovery/`, own Flyway bean and history table | `IMPLEMENTED` (E1-044 evidence) |
| Workflow (Epic 3+) | Temporal Java SDK, workers `SY-CASEWF`, namespace `rwb-recovery` | `DOCUMENTED/REQUIRED` (ADR-011) |
| Rules | Embedded Drools KIE runtime (`drools-engine`, `drools-mvel`, `drools-decisiontables`, `drools-xml-support`) | `DOCUMENTED/REQUIRED` (ADR-012) |
| Scheduling | Quartz and Spring Batch for every Epic 1–2 job | `DOCUMENTED/REQUIRED` |
| Observability | Micrometer, OpenTelemetry traces, structured logs, health endpoints | `DOCUMENTED/REQUIRED` |
| Build | Gradle Kotlin DSL, Nx front end, JaCoCo + Vitest coverage | `IMPLEMENTED` (TE-001) |

## 2. Module boundaries

One Spring Modulith application module `recovery` at `th.co.scb.ace.demo.recovery`. Inside it, 19
design modules (P1–P10, S1–S9) are nested application modules with `api` and `internal` packages.

| Rule | Meaning | Evidence |
|---|---|---|
| BND-1 | Recovery code stays in the recovery module folder | `IMPLEMENTED` |
| BND-2 | Common and collection are reached only through published interfaces | `IMPLEMENTED` |
| BND-3 | Recovery module to recovery module only through `api`; Modulith `verify()` | `IMPLEMENTED` |
| BND-4 | A module uses only its own entities and repositories | `IMPLEMENTED` |
| BND-5 | Outbound HTTP/SFTP/Blob clients only in the named client packages | `IMPLEMENTED` |
| BND-6 | A recovery class may not name an ACE `public` table; read `recovery.v_ace_*` | `DOCUMENTED/REQUIRED` (RWB-E1-069) |

Module map: `backend/src/test/resources/architecture/recovery-modules.yaml`, read by
`RecoveryBoundaryTest`. Code owners: recovery tech lead plus the squad developers.

## 3. API surface

- Base path `/api/recovery/v1`, plain JSON, UUID identifiers, MSG codes, API Specification v4
  (ADR-RCV-001, an exception to ACE's HAL rule).
- Every endpoint has a Spring Security method check naming the capability area and operation.
- Errors use the message ID and the exact wording from the Error and Message Standard v4.
- Pagination: `page`, `size`, `sort`; default size 25, max 100.
- Idempotency: `Idempotency-Key` on POST commands that create or move a case.
- Versioning: additive only within v1; a breaking change creates v2.
- Main groups (Epic 1): cases, case record, documents, queues, allocation, transfer, decisions,
  reference data, parameters, admin jobs, agent shadow endpoints.
- Main groups (Epic 2): treatment, approvals, payments, notices, partner instructions, agent live
  endpoints.
- Temporal endpoints are operational only (`/admin/temporal/health`); the case API does not expose
  workflow internals.
- Rule package endpoints: `POST /admin/rule-packages` (upload), `POST /{id}/validate`,
  `POST /{id}/scenarios`, `POST /{id}/approve`, `POST /{id}/rollback`, `GET /{id}`; all behind
  `rwb.p3.drools`.

## 4. Data model and migrations

### 4.1 Schema and naming

| Item | Rule | Evidence |
|---|---|---|
| Schema | `recovery`, always `${recoverySchema}` | D-RCV-28, Physical Schema v6 |
| Table names | Business glossary names, no prefix | Physical Schema v6 |
| Migration file | `V<seq>__<story>_<name>.sql` | D-RCV-28 |
| Sequence | 4 digits, contiguous `0001..N`, taken in merge order | D-RCV-28, D-RCV-34 |
| Line 1 | `-- Story: <story key>` | D-RCV-28 |
| Corrective file | Next sequence, same story key, line 2 `-- Fix: <reason>` | D-RCV-28 |
| Change to merged file | Forbidden | D-RCV-28 |
| Repeatable migration | Forbidden (`R__*.sql` fails lint) | D-RCV-28 |
| Literal schema | Fails lint (`recovery.`, `ace.`, `public.`, `SET search_path`) | D-RCV-28 |
| Flyway bean | Own bean, own history table `flyway_schema_history_recovery`, `outOfOrder(false)` | D-RCV-18/28 |
| Flyway clean | Disabled in every environment | NFR-027 |

### 4.2 Structure

Physical Schema v6: 93 tables and 30 views in schema `recovery`.

| Tier | Owner | Content | Count |
|---|---|---|---|
| 1 | ACE team, read only | ACE tables that exist today, read through views | 22 tables, 16 views |
| 2 | ACE team | New ACE tables and columns for source data ACE does not hold | 14 tables, 12 columns, 14 views |
| 3 | Workbench | 1:1 extension tables keyed by ACE business key | 4 tables |
| 4 | Workbench | Case, workflow, treatment, legal, partner, debt sale, documents, decision log, reference, outbox, flags, agents | 88 tables |
| Removed | — | Source copies, load machinery and six absorbed columns | 20 tables, 243 fields |

- **Read boundary:** `recovery.v_ace_*` views only. The view owner holds SELECT on ACE tables; the
  recovery service role holds SELECT on views and no privilege in `public`.
- **No foreign key into `public`:** ACE uses `ON DELETE CASCADE` on `account`; links are business-key
  columns.
- **Extension tables:** `party_ext`, `collateral_ext`, `case_account_ext`, `asset_ext` (names fixed by
  the ACE Data Tier Map; confirm against the final V0001).
- **Dictionary:** 122 `sys_objects` and 1,366 `sys_fields` seeded in V0001 (D-RCV-29).
- **Baseline:** V0001 tables and dictionary; V0002 Tier 1 views; V0003 Tier 2 views after
  RWB-ACE-001.
- **Implemented:** RWB-E1-042 `parameter_catalog` and `parameter_value` migration, guarded against the
  V0001 baseline; 13 catalog rows and 28 value rows in the bootstrap. Evidence in
  `output/INC-003-epic-1-RWB-E1-042/implement/`.

### 4.3 Key entities

`recovery_case`, `case_account`, `case_party`, `queue`, `assignment`, `task`, `timer`, `treatment`,
`guarantee_claim`, `legal_action`, `notice`, `hearing`, `partner`, `partner_instruction`, `listing`,
`asset_sale`, `debt_sale_lot`, `document`, `document_index`, `document_checklist`, `decision_log_entry`,
`interaction_ledger`, `rule_package`, `rule_package_version`, `rule_row`, `parameter_catalog`,
`parameter_value`, `reference_*`, `outbox`, `feature_flag`.

## 5. Integrations

| Integration | Direction | Protocol | Notes |
|---|---|---|---|
| ACE source tables | Read | JDBC through views | No writes; no `public` table access |
| COLLINS / outbound files | Outbound | SFTP, file, adapter | Outbox with retry |
| Blob storage | Both | Azure Blob SDK | Write-once container for legal types |
| Entra ID | Inbound | OIDC | SSO and MFA |
| Temporal | Runtime | gRPC | Payload codec, mTLS |
| WIN, NSS, LINE OA, e-sign | Outbound | Adapters | Epic 2 |
| Jira / Confluence / GitLab | Delivery | MCP | Not runtime |

## 6. Security and access

- Entra ID SSO with MFA; roles from `Users, Roles and Permissions v4`.
- Spring Security method checks on every endpoint; capability area and operation in the annotation.
- Role-to-permission matrix is data, not code (RWB-E1-037).
- PDPA masking at the API by role; field-level classification in the Personal Data Inventory v4.
- Access log entry for every read of personal data and every admin action (RWB-E1-039).
- Break-glass admin is time-boxed and logged; no standing production access.
- Temporal payloads encrypted by `PdpaPayloadCodec` (AES-GCM, key in Key Vault); no clear personal
  data in workflow history.
- No credential in code or config; secrets from Key Vault or environment.

## 7. Observability and operations

- Structured JSON logs with case ID, correlation ID, user ID and capability area; no personal data.
- Metrics: request latency, error rate, queue depth, job outcome, decision-log write latency, Tempo
  workflow failures, Drools evaluation time.
- Health: `/actuator/health` liveness/readiness; Temporal health in `/admin/temporal/health`.
- Run book per job (RWB-E1-056) with owner, schedule, failure message and recovery action.
- Alerts: job failure, migration failure, decision-log write failure, view compile failure, rule
  package validation failure, Temporal task queue backlog.

## 8. Resilience and error handling

- Outbox pattern for every outbound side effect; retry with backoff; dead-letter queue.
- Idempotency key on commands; duplicate submit returns the first result.
- Timeouts: 5 s for internal calls, 30 s for external, 2 min for file transfer.
- Circuit breaker on external adapters; fallback to manual queue.
- Decision-log write is synchronous and blocks the action on failure (ADR-009).
- Temporal retries and durable timers replace hand-built chain retries from Epic 3.
- No retry on a non-idempotent POST without the key.

## 9. Rules and workflow

### 9.1 Temporal (D-RCV-36 T1/T2/T7)

| Item | Value |
|---|---|
| Cluster | Self-hosted, one per environment, ACE AKS, official Helm chart |
| Namespace | `rwb-recovery` |
| Task queues | `rwb-case`, `rwb-integration`, `rwb-platform` |
| Workflow ID | `case-{caseId}` |
| Case of record | ACE database, schema `recovery` |
| Persistence | `temporal`, `temporal_visibility`; role `temporal_svc`; no ACE grant |
| Retention | 30 days closed, archive to Blob in E2-039 |
| Search attributes | `CaseId`, `Stage`, `ProductGroup`, `QueueCode` — no personal data |
| Access | Web UI behind Entra ID; RW-PLATADM operate, RW-AUDIT read, RW-SECADM break-glass |
| Flags | `rwb.p3.temporal`; off returns the previous path |
| Parameters | `temporal.target`, `temporal.namespace`, `temporal.taskqueue.platform`, `temporal.retention.days=30` |

Epic 1 and Epic 2 jobs remain Quartz/Spring Batch. JOB-05 runs behind `TimerScheduler`. Temporal
Schedules are not used before Epic 3.

### 9.2 Drools (D-RCV-36 T3–T7, T10)

| Item | Value |
|---|---|
| Libraries | `drools-engine`, `drools-mvel`, `drools-decisiontables`, `drools-xml-support` |
| Authoring | RW-COE writes an XLS decision-table workbook; RuleSet = package code; NAME = rule ID |
| Upload | Compile to KieBase, checks, scenarios, dry run, store `rule_package_version` with workbook, DRL, checksum |
| Approval | RW-RISK; author cannot approve; valid-from date; rollback one call |
| Catalog | `rule_row` stays as the queryable rule catalog with `outputs` jsonb |
| Evaluation | Only inside a Temporal activity from Epic 3; package version returned and logged |
| Decision log | `rule_id` = Drools rule name; `rule_version` = package version label |
| Packages Phase 1 | ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT, TRANSFER, RESTRUCTURE, PAYMENT_MATCH, BOOKING_MATCH |
| Dropped | `payment_match_rule` table; replaced by package PAYMENT_MATCH |
| Parameters | `drools.kiebase.cache.max=20`, `rules.testcases.min=50` |
| Flags | `rwb.p3.drools`; off returns 404 for package endpoints and the previous path elsewhere |

## 10. Documents, notifications and AI runtime

- Document storage: Blob containers, write-once for legal types, virus scan on intake, retention
  classes, index by case/type/date/extracted fields.
- OCR and extraction: asynchronous pipeline, confidence threshold, review queue for low confidence.
- Notices: template + merge fields from reference data; dispatch record; proof of delivery from WIN.
- AI runtime: separate agent service behind `AgentRuntimeClient` with a fallback to the manual path
  (RWB-TE-013). No agent writes a case decision directly in Epic 1; it writes a recommendation.
- Agent platform: RWB-E1-058; shadow agents RWB-E1-059/062; evaluation RWB-E1-060/061/063.

## 11. Non-functional targets that shape the backend

| Target | Design response |
|---|---|
| p95 case list ≤ 2 s | Indexed queries, projection DTOs, pagination |
| p95 case record ≤ 3 s | Read model, bounded document fetch, cache reference data |
| 1,500 documents/day | Async OCR queue, back-pressure, Blob direct upload |
| 180 concurrent users | Stateless API, connection pool 50, session in Spring Session |
| Decision-log write ≤ 100 ms p95 | Append-only insert, hash chain computed in the same transaction |
| RPO 15 min / RTO 4 h | PostgreSQL PITR, Blob geo-redundancy, run book |
| 99.5% availability | Multi-instance, health checks, rolling deploy |

## 12. Gaps and constraints

| ID | Gap / constraint | Impact |
|---|---|---|
| `CTX-BE-GAP-01` | ACE source code is in a separate repository and not in this workspace | Implementation evidence is linked, not embedded |
| `CTX-BE-GAP-02` | The 21 Tier 1 ACE tables must be at the baseline head in DEV/SIT | E1-069 checks before views compile |
| `CTX-BE-GAP-03` | RWB-ACE-001 Tier 2 tables are an ACE-team dependency | Section B views stay behind flags |
| `CTX-BE-GAP-04` | Temporal and Drools versions are pinned at build | Record in Environment Design v4 |
| `CTX-BE-GAP-05` | The 10 removed stories leave gaps in the old Epic 1 numbering | Use the retirement register, not the old index |
| `CTX-BE-GAP-06` | Thai messages are proposed | English canonical until DL10 |

## 13. Recovery Flyway set-up and rulings

- Own Flyway bean in the recovery module, initialised after the ACE core bean.
- Folder `db/modulemigration/recovery/`, history table `flyway_schema_history_recovery`.
- `outOfOrder(false)`, `baselineVersion("0")`, `baselineOnMigrate(true)`, `cleanDisabled(true)`.
- `createSchemas(false)`; the `recovery` schema is created by the DBA in SIT/UAT/PROD and by the
  developer in DEV.
- Migration lint runs as a unit test: name pattern, contiguous sequence, one non-fix file per story,
  no `R__`, no literal schema, no `SET search_path`, no `GRANT`/`REVOKE` in recovery migrations.
- `@Tag("recovery-it")` Testcontainers tests run in `recoveryIntegrationTest`, outside `check`, and
  must run before every MR that touches a migration or the Flyway config (D-RCV-44).
- Corrective migration example: `V0043__rwb_e1_042_parameter_seed_fix.sql` with line 2
  `-- Fix: <defect>`.

## 14. Required guidance for implementation agents

1. Read this file with `project-context.md` and the story file before writing code.
2. Never read an ACE `public` table; use `recovery.v_ace_*`. BND-6 fails the build.
3. Never add an inbound load, tracker or source-copy table. D-RCV-35 removed them.
4. Put every value in reference data; never a literal threshold, queue, role, route or template.
5. Write the decision-log entry before the action; if the write fails, the action fails.
6. Add the method security check and the access-log entry on every endpoint.
7. Keep Temporal workflow code deterministic; I/O only in activities.
8. Compile and scenario-test a Drools package before approval; never bypass RW-RISK.
9. Add a migration only as `V<seq>__<story>_<name>.sql`; never edit a merged file.
10. Record an assumption in the plan's `Assumptions` section instead of asking a question.
