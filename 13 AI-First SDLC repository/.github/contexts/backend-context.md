# Recovery Workbench — backend context

**Purpose:** the backend technology, module boundaries, contracts, data, integrations, security and
operational rules an agent needs to specify or build a Workbench service.
**Status:** documented from the approved architecture and design set. The ACE source code is not in
this workspace (`CTX-GAP-020`), so this file records intended behaviour, not verified implementation.

## 1. Stack and runtime

| Layer | Position | Source |
|---|---|---|
| Language and framework | Spring Boot (Java) | Engineering Practices §2.3; AI Assisted Development Approach §3.1 |
| Persistence | Spring JPA; PostgreSQL | Engineering Practices §2.3 |
| Workflow | Temporal, self-hosted on the ACE AKS clusters in the ACE namespace; namespace `rwb-recovery`; task queues `rwb-case`, `rwb-integration` and `rwb-platform`; one workflow per case from Epic 3 | ADR-011; D-RCV-36 |
| Rules | Drools embedded in the recovery module, KIE runtime libraries only (`drools-engine`, `drools-mvel`, `drools-decisiontables`, `drools-xml-support`); versioned rule packages in `rule_package` and `rule_package_version` | ADR-012; D-RCV-36 |
| Batch and scheduling | Spring Batch and Quartz for every Epic 1 and Epic 2 job; JOB-05 behind the `TimerScheduler` port | Engineering Practices section 3; ADR-011 (T2) |
| Security | Spring Security with method security and OAuth; Spring Session; Entra ID and the bank IAM | Engineering Practices §2.3; Security and Access Design v2 |
| Cloud | Spring Cloud Azure; ACE namespace on the shared ACE AKS clusters | Engineering Practices §2.3 |
| API style | RESTful API; Spring Data REST and Spring HATEOAS where appropriate; OpenAPI 3.1 contract | Engineering Practices §2.3; API Specification v2 |
| Events | AsyncAPI 3.0; outbox and idempotency | Event and Messaging Design v2; TE-006 |
| Schema changes | Flyway or Liquibase; one migration per story; forward-only in production; schema names from parameters | RWB-E1-044; AGENTS.md §3 |
| Type safety | End-to-end type safety and validation; front-end types generated from the back end | Engineering Practices §2.3 |

## 2. Module boundaries

```text
ACE service (one repository, one deployable)
├── common module        ACE team: sign-in, access check, audit and PII logging,
│                        shared case view, shared entities (customer, account, product,
│                        collateral, asset), shared tasks (TDR calculator)
├── collection module    Collection squad: phone, field, FCR and TDR work before day 90
└── recovery module      TechX recovery squads: case stages and tasks, Drools rule evaluator,
                         decision centre and log, document hub, partner portal, data loads,
                         recovery screens and data products
```

Rules:

1. A module calls another module only through its published interface or an application event. It
   never calls the inside of another module.
2. Each module owns its tables. Another module reads them only through the owning module's interface.
3. A module boundary test runs in the build and fails it on any violation.
4. A recovery component the collection module also needs moves to the common module by agreement with
   the ACE team.
5. Until the ACE team has moved ACE to the modular monolith, TechX builds in its own package (DL05).

Source: ADR-001, ADR-002, Engineering Practices §2.2.

## 3. API surface

The OpenAPI 3.1 contract is `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v2.yaml`.
It covers the following resource groups:

| Group | Representative paths |
|---|---|
| Cases | `/cases`, `/cases/{caseId}`, `/cases/{caseId}/timeline`, `/accounts`, `/parties`, `/transfer`, `/deviations`, `/legal-hold` |
| Work | `/me/tasks`, `/tasks/{taskId}`, `/queues`, `/queues/{queueId}/cases`, `/queues/{queueId}/placements`, `/cases/{caseId}/timers` |
| Decisions and approvals | `/cases/{caseId}/recommendation`, `/approvals`, `/approvals/{approvalId}/approve`, `/return`, `/refuse`, `/decision-log`, `/decision-log/{entryId}` |
| Treatment | `/cases/{caseId}/treatments`, `/treatments/{treatmentId}`, `/submit`, `/cases/{caseId}/route`, `/guarantee-claims` |
| Legal and notices | `/cases/{caseId}/notices`, `/notices/{noticeId}/approve`, `/legal-actions`, `/hearings` |
| Assets and debt sale | `/assets`, `/assets/{assetId}/valuations`, `/listings`, `/listings/{listingId}/rounds`, `/debt-sale-lots`, `/award` |
| Write-off and money | `/write-off-scans`, `/write-offs/{writeOffId}/committee-decision`, `/proceeds`, `/proceeds/{proceedsId}/match` |
| Documents | `/cases/{caseId}/documents`, `/documents/{documentId}`, `/content`, `/versions`, `/fields/{fieldId}`, `/custody` |
| Interactions and partners | `/cases/{caseId}/interactions`, `/partners`, `/cases/{caseId}/instructions`, `/partner/instructions`, `/partner/data-room/{lotId}` |
| Administration | `/admin/rule-packages`, `/admin/rule-package-versions/{versionId}/approve`, `/admin/rule-package-versions/{versionId}/rollback`, `/admin/lists/{listCode}`, `/admin/reference-loads`, `/admin/roles`, `/admin/access-log`, `/admin/jobs`, `/admin/data-quality/exceptions`, `/admin/agent-runs`, `/admin/agent-configs`, `/admin/agent-evaluations`, `/admin/agent-metrics` |
| Reports | `/reports/measures` |

Contract rules:

- Every endpoint has a Spring Security method check naming the capability area and the operation.
- Every endpoint returns the message table's message ID for a validation failure; do not invent codes.
- Every write that changes a case writes the decision log entry before the change is committed. A
  failed log write rolls the action back.
- Every write is idempotent where the caller may retry; use the idempotency key table.
- Pagination is server-side; filters are explicit; no endpoint returns an unbounded case list.
- Personal fields are masked in the response by the caller's masking profile.

## 4. Data model

| Item | Position | Source |
|---|---|---|
| Data products | 14: DP01 account and arrears, DP02 customer and party, DP03 case and ownership, DP04 treatment and offers, DP05 contact and promises, DP06 collateral and assets, DP07 legal events and cases, DP08 partner performance, DP09 debt sale, DP10 documents and extracted fields, DP11 scores and route economics, DP12 decision log, DP13 money and closure, DP14 reference data | Conceptual Data Model v5 |
| Entities | 108 entities across 17 subject areas | Conceptual Data Model v5; Logical Data Model v6 |
| Standard columns | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` on every table | TSD P1 §T3.0 |
| Case | `recovery_case` holds the case ID `RW-YYYY-NNNNNN`, customer, product, stage, status, route, owner, queue, exposure band, deviation flags and clocks | Logical Data Model v6; REQ-CWC-002..005 |
| Decision log | Append-only, hash-chained; one entry per decision with rule, model, agent and prompt versions, inputs, recommendation, approval, actions and outcome | ADR-009; NFR-033..035 |
| Interaction ledger | Ordered record of every contact, letter, promise, payment and hand-over | RWB-E1-066..068 |
| Reference data | Limits, lists of values, roles, permissions, templates, document types, checklists, service levels, legal periods and holidays, all versioned with valid-from, valid-to, author and approver. Rules are not reference tables; the reference data service holds reference tables only | RWB-E1-043 |
| Rule packages | `rule_package` holds the package code, title, owner role and hit policy; `rule_package_version` holds the version label, status, workbook reference, generated DRL, checksum, valid-from and valid-to dates, author, approver, test result and rollback link; `rule_row` is the parsed catalog linked to a package version | ADR-012; RWB-E1-072 |
| Migrations | One migration per story; forward-only in production; schema names from parameters | RWB-E1-044 |

Data rules:

- No module reads another module's tables.
- No component calls a system of record directly.
- Every data product carries a freshness stamp (source extract time and load time).
- Every load runs data quality rules; failed rows carry a reason code.
- The case list reconciles daily to the ALS count of accounts at 90+ DPD; no unexplained variance.
- Personal data is tokenized at load where the design says so (national ID, passport number); the
  clear value is not stored.
- Retention and archive rules are held as data and applied by a job; legal hold overrides retention.

## 5. Integrations

| Direction | System | What | How | Frequency |
|---|---|---|---|---|
| In | COLLINS | Core bank (ALS), EFS, UDP, SCBPDM, AAL, LIT status, scores | Daily batch into the ACE database | Daily, by 07:00 |
| In | CCMS | Collateral records | File load until a batch feed exists | Weekly/monthly today |
| In | SVAF | Appraisals | File load | Weekly/monthly today |
| In | AMIS | Property assets | File load | As agreed |
| In | RPS | Vehicle assets | File load | As agreed |
| In | WIN | Proof of delivery and dispatch status | File exchange | Per notice |
| In | GL | Write-off postings and proceeds | File load | Monthly |
| Out | Core bank (ALS) | Bookings for restructures, settlements and write-offs | Officer action; confirmed on the next load | Per booking |
| Out | WIN | Notices and letters for print and post | File | Per notice |
| Out | NSS and LINE OA | SMS and LINE messages | ACE notification path | Per contact |
| Out | Data lake / Power BI / COLLINS | Reporting and model learning | Daily batch | Daily |
| Out | Partners and debt buyers | Instructions, results, data room, awards | Partner portal / SFTP | Per instruction or sale |
| Out | Enterprise AI platform | Model calls | Private endpoint through the tool gateway | Per agent run |

Rules:

- One adapter pattern for file loads and outbound files: checks, logging, retry, exception queue.
- Retry three times per item, then the exception queue with a task for a named owner.
- The outbox holds outbound work until it is delivered; a duplicate delivery does not repeat the
  action.
- Same-day data needs are named under DL06 before an interface is built; the current position is
  end-of-day data available the next morning.

Source: Target Architecture §3; REQ-DRI-006..013; NFR-024..026; Interface Specifications v2; Event and
Messaging Design v2.

## 6. Security and access

| Control | Position | Source |
|---|---|---|
| Identity | Entra ID SSO with MFA; the bank IAM; Spring Security OAuth | RWB-E1-022; Security and Access Design v2 |
| Authorisation | Method security on every endpoint; role, capability area and scope; out-of-scope records are not returned | RWB-E1-037; CTL-09 |
| Permission model | Role-to-permission matrix as versioned data; permission letters C/R/U/D/A; default scope own, team or all | Users, Roles and Permissions v3 |
| Masking | Masking profile per role; national ID and passport tokenized at load; every personal read logged through PII Kafka | Personal Data Protection Design §4–5 |
| Delegation | Delegation of authority table as versioned data; approval level and limit checked on every approval | RWB-E1-038; CTL-04 |
| Separation of duty | The preparer of a decision cannot approve it | CTL-05 |
| Break-glass | Time-limited emergency access with a reason, approval and full logging | RWB-E1-039 |
| Audit | Every access, export and decision written to the decision log or access log; audit and SOC logs through ACE | RWB-E1-039; Audit and Logging Design v2 |
| Secrets | No credential, key or token in code, config or a prompt; use the bank secret store | AGENTS.md §4 |

## 7. Observability and operations

| Area | Position | Source |
|---|---|---|
| Logs | Structured logs with case ID, rule ID, version, correlation ID; no personal data | Audit and Logging Design v2 |
| Metrics | Request rate, error rate, latency, queue depth, job duration, load freshness, rule evaluation time, workflow failure and stuck counts, agent fallback rate | Observability and Monitoring Design v2 |
| Traces | End-to-end trace from screen to service to database; agent calls traced through the tool gateway | Observability and Monitoring Design v2 |
| Alerts | Load failure or late load, job failure, interface failure, queue breach, decision log write failure, hash-chain break, agent fallback spike | Observability and Monitoring Design v2; NFR-035 |
| Job monitor | Every scheduled job has a run book: purpose, schedule, owner, failure signs, restart steps, escalation | RWB-E1-056 |
| Interface monitor | Every interface has a status, last run, last success, error and rerun action | SCR-44 |
| Run books | Every Epic 1 job and service has a run book; operations can restart without the developer | RWB-E1-056 |
| Environments | DEV synthetic, SIT masked, UAT masked, production | Test Strategy §2 |
| Release | Monthly release, one week SIT, one week UAT, go decision, rollback by previous tag | Release Plan v3; NFR-027 |

## 8. Resilience and error handling

- Every failure is caught, classified, retried where safe, reported and recovered; the user sees a
  safe message with a message ID.
- A system-of-record outage queues the outbound action and retries; it does not lose the action.
- After three retries the item moves to the exception queue with a task for a named owner.
- An agent or model outage falls back to the rule result; the case still routes.
- A decision log write failure blocks the action; it does not proceed unlogged.
- A failed interaction ledger write raises an incident; no entry is discarded.
- A release rolls back by redeploying the previous tag.
- A duplicate event or file does not repeat the action; idempotency keys are held.

Source: Error Handling and Resilience Standard v2; NFR-024..027, NFR-077.

## 9. Rules and workflow

| Area | Position | Source |
|---|---|---|
| Rules | Versioned rule packages, not code: each package is an Excel XLS decision table compiled to a KieBase; first match through one activation-group; 448 rules in 10 route sets | ADR-012; D-RCV-36; Business Rules and Routing Logic v4 |
| Rule load | Upload an XLS workbook for a package, compile, check the schema, overlap, unreachable rows, the default row and at least 50 scenarios; approve by RW-RISK; in force from valid-from; roll back by one call; change log | RWB-E1-073; REQ-CWC-013..014 |
| Workflow | Temporal runs the case lifecycle from Epic 3, one workflow per case (`case-{caseId}`), with durable timers, retries and automated multi-step chains behind `WorkflowGateway`; case data stays the system of record in the ACE database recovery schema (PostgreSQL, schema `recovery`) | ADR-011; D-RCV-36 |
| Timers | Quartz and Spring Batch for every Epic 1 and Epic 2 job; JOB-05 implements the `TimerScheduler` port so Epic 3 can swap in Temporal durable timers; Temporal Schedules are not used in Epics 1 and 2 | Engineering Practices section 3; ADR-011 (T2); RWB-E1-028 |
| Case in flight | A change to workflow code must not break a case in flight: workflow code is deterministic, a change passes the replay test against recorded histories (E2-040), and workers roll out by build ID | ADR-011; E2-040 |

## 10. Documents, notifications and AI runtime

| Area | Position | Source |
|---|---|---|
| Document storage | Blob storage; write-once container for legal types; version history; custody of originals | ADR-007; Document Management Design v2; RWB-E1-024 |
| OCR and extraction | OCR service reads inbound scans; classification into six types; field extraction with confidence; low-confidence review queue | RWB-E1-049..054 |
| Document intake | Branch scanners, mailroom, partner SFTP and recovery mailboxes enter the same OCR intake with the source recorded | RWB-E1-057 |
| Notices | Template version approved by Legal; merge fields from case data; dispatch through WIN; proof of delivery writes back | RWB-E1-046, 052, 055; Notification and Correspondence Design v2 |
| Agent runtime | Orchestrator and tool gateway; autonomy L0–L4; shadow then live; 60-second answer target; fallback to rules; model, agent and prompt versions in the decision log | Agent Catalog v2; Model Integration Design v2; AI Decision Governance v2 |
| Agent permissions | An agent passes the same permission checks as a person and runs under a service identity; its write is logged with the model or agent version | REQ-CWC-018; NFR-078 |

## 11. Non-functional targets that shape the backend

| Target | Value | Source |
|---|---|---|
| Screen response | Under 2 seconds at P95 | NFR-008 |
| Rule evaluation | Under 300 ms at P95 | NFR-011 |
| Agent answer | Under 60 seconds, then fallback | NFR-010 |
| Case search | Under 3 seconds | NFR-012 |
| Document search | Under 5 seconds | NFR-012 |
| COLLINS load | Complete by 07:00 | NFR-013 |
| Rebalancing job | Complete by 07:00 | NFR-019 |
| Availability | 99.9% business hours; 99.5% outside | NFR-020, NFR-021 |
| Case history read | Under 2 seconds at 2031 size | NFR-070 |
| Decision log size | About 36 GB by 2031 | NFR-007 |
| Document estate | About 5.8 million documents, 2.8 TB by 2031 | NFR-069 |
| Unit coverage | 80% line coverage on new code | Test Strategy §1; toolkit gate |
| Pipeline checks | Nine checks before merge | Engineering Practices §1 |

## 12. Gaps and constraints

| ID | Gap | Impact |
|---|---|---|
| CTX-GAP-020 | The ACE source code is not in this workspace. | The context is intended behaviour from documents; implementation must verify against the ACE repository. |
| CTX-GAP-011 | RPO, RTO and availability targets are open (DL11). | Resilience tests cannot be baselined; use the ACE values until confirmed. |
| CTX-GAP-012 | Retention periods for the decision log, ledger and documents are open (DL26). | The retention job can be built with a placeholder class; the periods are loaded as data. |
| CTX-GAP-010 | Same-day data interfaces are not named (DL06). | The default is end-of-day; a story that needs same-day data is blocked until DL06. |
| CTX-GAP-013 | Partner external access is not live (DL03). | Partner portal integration tests are limited to the bank network until the gateway is live. |
| CTX-GAP-014 | The model endpoint is not approved (DL33). | Agents run in shadow with the rule fallback; no live model call is required for E1. |
