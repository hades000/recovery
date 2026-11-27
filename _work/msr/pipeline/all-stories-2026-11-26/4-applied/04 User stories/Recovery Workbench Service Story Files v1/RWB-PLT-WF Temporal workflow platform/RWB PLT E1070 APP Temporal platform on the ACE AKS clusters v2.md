# RWB-PLT-E1070-APP Temporal platform on the ACE AKS clusters

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-E1070-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-WF |
| Wave | 0 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-070 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP04, DP05, DP06, DP07, DP13, DP14, DP15, DP19 |
| Parallel lane | L-PLT-WF-D |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1070-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P4-E1022-CON |
| Integration dependencies | None |
| External dependencies | RWB-PLT-E1056-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-016, FR-PLT-017, FR-PLT-018, FR-PLT-021, FR-PLT-022, FR-PLT-023, FR-PLT-024, FR-PLT-025, FR-PLT-026, FR-PLT-028, FR-PLT-029) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-070 for the workflow platform epic; the cluster is now the shared L1 and L2 platform in namespace rwb-recovery, the monolith schema and login in AC2 are expressed as the P3 rwb-case login and schema rwb_case, and the platform is recorded as owning no schema, no topic and no Workbench REST base. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-PLT-E1070-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **one Temporal cluster per environment on the ACE AKS clusters, with its own persistence databases, the rwb-recovery namespace, mTLS and the Web UI behind Entra ID OIDC**, so that **Epic 3 workflows have a durable engine that SCB IT runs like the rest of ACE**.

This is the app story of legacy key RWB-E1-070 under epic RWB-PLT-WF, the Temporal workflow platform of the realignment. The platform is L1 and L2 of the five-layer Temporal design (Architecture v5 slides 23 and 24; Temporal and Drools Design slides 11 and 12): **L1** is the cluster, one per environment on the ACE AKS clusters, with its own persistence database and no grant on the ACE database; **L2** is the namespace `rwb-recovery`, carrying its own retention, certificates and codec keys. The cluster is shared, one per environment, and the next workbench takes a namespace on it rather than a second cluster (Architecture v5 slide 46).

The platform is **not one of the 19 services**. Template and Rules §R4 has no platform row, so the platform owns no `rwb_*` schema, no `rwb.<short>.events.v1` topic, no `/api/recovery/<short>/v1` base and no service short; Architecture v5 slides 4 and 41 keep the shared platform pieces outside the service catalogue, and the platform owns no schema of the ACE database. The server and Java SDK release is Temporal 1.30 or later, for Nexus and Worker Versioning (Temporal and Drools Design slide 32 item 6). The platform identity, meaning its database login, its admin base and the approved release line item, is not in the read sources: Not specified in the source documents (GAP-1440; ASM-2535). The platform task queue is task queue `rwb-platform`, which the Ownership Map gives to JOB-22, and the Workbench gives the platform one operation, `POST /admin/workflows/smoke`, both outside this story.

### 2. Business rationale

Case workflow begins in Epic 3, and a durable engine must exist before the first case workflow is written. The realignment keeps the decision that Temporal runs the case lifecycle while case data stays the system of record in each owner service's `rwb_*` schema; the engine therefore needs its own persistence database, its own identity, its own certificates and its own run book, or Epic 3 builds on a shared service that nobody owns and a restart becomes a developer task.

The split changes three things. First, the cluster is the shared platform layer: one cluster per environment for Recovery and for ACE, namespaces as the unit of isolation, one task queue per service, and workers that stay inside each of the 19 services (Architecture v5 slides 23, 24 and 46). Second, the monolith's single `recovery_svc` login and single `recovery` schema no longer exist, so the separation of databases is proved against one named service: the P3 rwb-case login and schema `rwb_case` (DP-01, DP-02). Third, the platform publishes nothing into the Workbench: no `rwb_*` schema, no topic, no `/api/recovery` base, and no screen, because the Web UI is an operational console behind Entra ID rather than a Workbench screen (DP-13, DP-14, DP-19).

This story provides the platform only: the cluster, the two persistence databases owned by `temporal_svc`, the namespace with 30-day retention and four search attributes, mTLS between the services and the frontend, the Web UI behind Entra ID OIDC, metrics to the ACE monitoring stack and a run book with the eight sections of the run book catalog. It meets REQ-DRI-007 (a named owner and a tested way back for every failure) and REQ-DRI-010 (environment values come from parameters, not code). The measure is that DEV and SIT pass every check in section 16 and that operations restarts a stopped frontend in SIT from the run book alone.

### 3. Preconditions

- RWB-PLT-E1070-CON is published: the namespace and client contract (namespace `rwb-recovery`, retention, the four search attributes, the client certificate profile, the frontend API subset and its typed errors, the OIDC role mapping, the metrics and health contract) and the fake frontend.
- RWB-PLT-E1072-CON is published: the embedded Drools kit the services' workers run inside their activities (DP-04). The platform hosts those workers and never calls the kit itself.
- RWB-PLT-E1042-CON and RWB-PLT-E1043-CON are published: the platform parameters contract and the reference-data contract, with the client library (DP-06, DP-07).
- RWB-PLT-E1047-CON is published: the topic and event naming library (DP-14). The platform owns no topic and reads it only to prove that no platform topic exists.
- RWB-PLT-E1044-CON is published: the per-service Flyway sequence and migration conventions (DP-15). The Temporal persistence stores are created by the schema job, not by a Flyway migration.
- RWB-PLT-N001-CON is published: the gateway-bff composite route surface (DP-19). The Web UI is not a Workbench screen and is not served through it.
- RWB-P3-E1042-CON and RWB-P3-E1043-CON are built against their published contracts and fakes: the parameters and reference data owned by rwb-case, read by the cluster configuration through the platform parameters contract.
- RWB-P4-E1022-CON is built against its published contract and fake: the roles RW-PLATADM and RW-AUDIT that the Web UI maps, and every other Workbench role that it refuses.
- The ACE AKS clusters for DEV, SIT, UAT and PROD exist with the ACE namespace, a zone-redundant PostgreSQL flexible server, Azure Key Vault and the ACE monitoring namespace.
- The SCB IT approved Temporal server and Java SDK release is recorded in Environment and Deployment Design v5, approved 16 November 2026; the approved release is not selected by the build. The release number itself is not in the read sources: Not specified in the source documents (GAP-1440; ASM-2535).
- An internal DNS name and ingress exist for the Web UI; the frontend gRPC port 7233 is reachable only from the cluster network and the worker subnets.
- The ACE internal certificate authority issues the mTLS certificates, and the platform administrator may read the certificate from Key Vault.
- The platform administrator holds RW-PLATADM through the environment group; RW-AUDIT holds RW-AUDIT through the environment group.

### 4. Flow

1. Platform administrator: deploys the Helm release `rwb-temporal` into the ACE namespace of DEV, then SIT, from `rwb-temporal-values.yaml`; the chart runs the frontend, history, matching, internal-worker and web deployments, pinned to the SCB IT approved release.
2. TemporalSchemaJob: creates the databases `temporal` and `temporal_visibility` owned by `temporal_svc` on the zone-redundant PostgreSQL flexible server, then runs the Temporal schema tool at the pinned release; a second run changes nothing and no Flyway migration touches the two stores.
3. NamespaceBootstrapJob: registers the namespace `rwb-recovery` with retention 30 days and the Keyword search attributes CaseId, Stage, ProductGroup and QueueCode; a second run changes nothing.
4. Platform administrator: binds the mTLS certificate and key from Key Vault to the frontend and to each service's worker through the CSI driver; the certificate is issued by the ACE internal CA and names the namespace, and the profile is the one RWB-PLT-E1070-CON publishes.
5. Platform administrator: configures the Web UI with Entra ID OIDC; the app roles map RW-PLATADM to operate and RW-AUDIT to read, and any other Workbench role is refused.
6. Platform administrator: turns on the metrics scrape to the ACE monitoring namespace on the contract endpoints and imports the platform dashboard.
7. Platform administrator: runs every check in section 16 and records the pinned server and SDK release in Environment and Deployment Design v5.
8. Platform administrator: writes the run book with the eight sections and asks operations to restart the frontend in SIT from the run book alone; RWB-PLT-E1056-OPS registers it in the run book catalog and runs RunbookCompletenessTest.
9. System: a frontend pod restart or reschedule keeps every workflow; history and visibility are durable in PostgreSQL, and the workers of the five services in scope reconnect to the replacement pod through the frontend without a replay error.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A client connects to the frontend with no certificate, an expired certificate or a certificate for another namespace | The TLS handshake fails or the call is refused; no workflow call is served and the event is in the frontend log with the client identity only | None (TLS) | AC3 |
| X2 | A user with a Workbench role other than RW-PLATADM or RW-AUDIT signs in to the Web UI | The sign-in is refused; no namespace is listed and no workflow is shown | MSG-P4-002 | AC4 |
| X3 | A grant joins the two databases, for example `temporal_svc` on schema `rwb_case` or the P3 rwb-case login on `temporal` | The access review check fails, the release is held and the grant is removed before the next environment | None (access review) | AC2 |
| X4 | A value the build needs is named by no read source (the platform login, the platform admin base, the approved release number) | The value is used as the working read of the assumption, the placeholder is written where the value is still open, and the gap stays open | Not specified in the source documents (GAP-1440; ASM-2535) | AC1, AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Stands alone as platform infrastructure; it needs the ACE cluster, the persistence database server, the Entra app roles, the Key Vault certificate and the run book catalog |
| Negotiable | Pod sizes, storage class, replica count, certificate life and dashboard panels are Helm values; the separation of databases, the namespace settings and the certificate profile are fixed by the contract |
| Valuable | Epic 3 starts on an engine that SCB IT can run, restart and review like the rest of ACE, with one cluster per environment instead of one per workbench |
| Estimable | One Helm release, two persistence databases, one namespace bootstrap, one OIDC app, one certificate binding, one dashboard and one run book |
| Small | Fits two weeks with its checks |
| Testable | Each criterion in section 7 is one check in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Temporal platform on the ACE AKS clusters

  Background:
    Given the ACE AKS clusters for DEV and SIT with the ACE namespace
    Given the platform administrator U-70 holds RW-PLATADM through the environment group

  Scenario: AC1 Cluster healthy (legacy RWB-E1-070 AC1)
    Given the rwb-temporal Helm release is installed in the ACE namespace of DEV and SIT
    When U-70 opens the Temporal Web UI and selects the namespace rwb-recovery
    Then the frontend, history, matching and internal-worker deployments each show 2 of 2 pods ready
    Then the web deployment answers on its internal ingress
    Then the namespace rwb-recovery is listed with status REGISTERED
    Then no pod of the release restarted in the last 24 hours

  Scenario: AC2 Separate database grants (legacy RWB-E1-070 AC2)
    Given temporal_svc owns the databases temporal and temporal_visibility
    Given the P3 rwb-case service login owns schema rwb_case in the ACE database
    When a session as temporal_svc runs SELECT on rwb_case.recovery_case
    Then PostgreSQL refuses the statement with SQLSTATE 42501 and returns no row
    When a session as the P3 rwb-case service login runs SELECT on temporal.executions
    Then PostgreSQL refuses the statement with SQLSTATE 42501 and returns no row
    Then the access review report shows no grant between the two roles and the two databases

  Scenario: AC3 mTLS enforced (legacy RWB-E1-070 AC3)
    Given the frontend requires a client certificate signed by the ACE internal CA
    When a worker connects to port 7233 with no certificate
    Then the TLS handshake fails and no workflow call is served
    When a worker connects with an expired certificate
    Then the TLS handshake fails with certificate expired
    When a worker connects with a certificate issued for another namespace
    Then the call is refused with PERMISSION_DENIED and no workflow is started

  Scenario: AC4 Web UI roles (legacy RWB-E1-070 AC4)
    Given the Temporal Web UI uses the Entra ID OIDC application with the Workbench app roles
    When U-62 holds RW-CASEOWN only and signs in to the Web UI
    Then the sign-in is refused with MSG-P4-002 and no namespace is listed
    When U-53 holds RW-AUDIT and signs in
    Then U-53 sees the namespace rwb-recovery and every workflow page is read-only
    Then U-53 cannot terminate, reset or signal a workflow
    When U-70 holds RW-PLATADM and signs in
    Then U-70 may terminate and reset a workflow in DEV, and every action is in the frontend audit log

  Scenario: AC5 Namespace settings (legacy RWB-E1-070 AC5)
    Given the namespace rwb-recovery in SIT
    When U-70 describes the namespace
    Then retention is 720 hours, 30 days
    Then the search attributes CaseId, Stage, ProductGroup and QueueCode are registered as Keyword
    Then no search attribute holds a name, a national ID or another personal data field

  Scenario: AC6 Frontend restart loses no workflow (legacy RWB-E1-070 AC6)
    Given the smoke workflow platform-smoke-20261116 is RUNNING and waits on its timer
    When the frontend pod is deleted and a replacement pod becomes ready
    Then the workflow is still RUNNING with the same workflow ID and run ID
    When the timer fires and the activity completes
    Then the workflow status is COMPLETED
    Then the history holds every event once, with no gap and no duplicate start

  Scenario: AC7 Run book with the eight headings (legacy RWB-E1-070 AC7)
    Given the run book docs/operations/runbooks/RWB-E1-070.md
    When RunbookCompletenessTest reads the run book
    Then the run book has the sections purpose, schedule, owner, dependencies, failure signs, checks, restart steps and escalation
    Then it names the five Temporal services, the two databases, the namespace, the certificate renewal step and the parameter temporal.target
    Then it names roles and service identities, never a person and never a personal data field
```

The seven criteria are copied from RWB-E1-070 and keep every value; the monolith schema and login names are expressed in target terms (DP-01, DP-02, DP-13).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One Temporal cluster per environment, on the ACE AKS clusters, deployed by the official Temporal Helm chart; the server and Java SDK release are pinned to the SCB IT approved release recorded in Environment and Deployment Design v5, and the release is 1.30 or later for Nexus and Worker Versioning | Template and Rules §R5.5 DP table; ADR-016; Architecture v5 slide 23; Temporal and Drools Design slide 32 item 6 |
| BR2 | Temporal persistence is separate from the ACE database: the databases `temporal` and `temporal_visibility` are owned by `temporal_svc`; `temporal_svc` has no grant on the ACE database and no service login has a grant on the Temporal databases | Architecture v5 slides 8 and 9; Temporal and Drools Design slide 11 |
| BR3 | The frontend requires mTLS from every client; certificates come from the ACE internal CA through Key Vault, name the namespace, and are renewed before expiry | Architecture v5 slide 35; RWB-PLT-E1070-CON |
| BR4 | The Web UI is behind Entra ID OIDC: RW-PLATADM operates, RW-AUDIT reads, every other Workbench role is refused; decode is not in this story | Architecture v5 slide 35; RWB-PLT-E1070-CON; RWB-P4-E1022-CON |
| BR5 | One namespace per environment, `rwb-recovery`; retention is 30 days and the only search attributes are CaseId, Stage, ProductGroup and QueueCode as Keyword | Architecture v5 slides 23 and 24; Temporal and Drools Design slide 27 |
| BR6 | A frontend pod restart loses no workflow; history and visibility are durable in PostgreSQL and a worker reconnects without a replay error | Temporal and Drools Design slide 28; AC6 |
| BR7 | The run book has the eight sections of the run book catalog and is tested by RunbookCompletenessTest | RWB-PLT-E1056-OPS |
| BR8 | Server and SDK releases, replica counts, retention and node sizes are Helm values or parameters, never code | REQ-DRI-010; Architecture v5 slide 20 |

### 9. State transitions

None. This story changes no case status. It establishes the namespace and the cluster; a workflow created in Epic 3 moves through its own states.

| Object | State | Meaning |
|---|---|---|
| Namespace | REGISTERED | `rwb-recovery` is registered on the cluster with retention 720 hours and the four Keyword search attributes |
| Server | RUNNING | The five deployments are ready and the frontend serves gRPC on 7233 and the Web UI on its ingress |
| Server | RUNNING (after upgrade) | An upgrade keeps the server RUNNING; AC1 is re-run after the change and no workflow is lost |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM | Installs and upgrades the release, runs the namespace bootstrap, reads the database grants, operates the Web UI and restarts a service (Platform administration, U) |
| RW-AUDIT | Reads the namespace and workflow history in the Web UI (Platform administration, R) |
| RW-SECADM | Reads the certificate and OIDC configuration; decode through the codec server is RWB-E2-038, not this story |
| SY-CASEWF | Connects to the frontend as a worker with its own client certificate; no Web UI account |
| SY-RULES | Runs the embedded Drools kit inside its own service's activities and does not connect to Temporal directly |
| RW-TRIBE | Maintains the Helm values and the run book through the change process; may not deploy to PROD |
| RW-CASEOWN and every other Workbench role | No Web UI access; a sign-in is refused with MSG-P4-002 |
| No delegation of authority level applies | A platform deployment is not a credit decision |

### 11. Data

Temporal persistence is outside the ACE database. This story reads and writes no table in any `rwb_*` schema and no ACE view, and no DF-REF, DF-CAS or DF-DEC field is added or changed.

| Store | What it holds | Owner | In the Physical Schema |
|---|---|---|---|
| temporal | Workflow histories, mutable state, timers, tasks | temporal_svc | No |
| temporal_visibility | Workflow visibility records and search attributes | temporal_svc | No |
| ACE database schemas of the 19 services | Each service's own `rwb_*` schema, the system of record for its data | the 19 services, one login each (DP-02) | Yes, unchanged by this story, no table read or written |

The Physical Schema does not include the Temporal tables. The two stores are created by TemporalSchemaJob at the pinned release; no Flyway migration in any service touches them (DP-15). No field identifier is added by this story.

### 12. Contract

#### 12.1 REST operations provided

None. The platform owns no service short (Template and Rules §R4 has no platform row), so it provides no path under `/api/recovery/<short>/v1` and no Workbench endpoint. The one Workbench operation the Ownership Map gives the platform, `POST /admin/workflows/smoke`, belongs to the platform smoke story (JOB-22) and is out of scope here.

#### 12.2 REST operations consumed

None. The platform calls no Workbench service over REST. The cluster reads its configuration through the platform parameters contract of section 13, and the Web UI calls only the frontend and the OIDC provider.

#### 12.3 Events published

None. The platform is shared platform and publishes no `rwb.<short>.events.v1` topic and no event schema (DP-14). The decision-record events, the case events and the audit events keep their owners; the ledger seal is out of scope.

#### 12.4 Events consumed

None. The platform consumes no Kafka topic. The events that reach a workflow reach it through the owning service's worker and its own consumer, never through the platform.

#### 12.5 Workflows and activities

None owned. The cluster hosts the workers of the 19 services: each service runs its own worker, polls only its own task queue `rwb-<short>` in namespace `rwb-recovery`, and KEDA scales it on backlog (Architecture v5 slide 24). The platform task queue is task queue `rwb-platform`; it carries the platform smoke workflow and the stuck-workflow scan (JOB-21 and JOB-22 in the Ownership Map), both outside this story.

#### 12.6 Schedules

None. The platform owns no Schedule in this story. The two platform jobs, the stuck-workflow scan and the smoke workflow, are the observability story's work and are owned there.

#### 12.7 Tables owned

| Store | Owner | Note |
|---|---|---|
| temporal | temporal_svc | Workflow histories, mutable state, timers and tasks; a Temporal persistence store, not an ACE table and not an `rwb_*` table |
| temporal_visibility | temporal_svc | Workflow visibility records and the four Keyword search attributes; a Temporal persistence store, not an ACE table and not an `rwb_*` table |

The two stores are Temporal persistence and sit outside the Physical Schema of the ACE database. The platform owns no `rwb_*` schema and no table in the ACE database.

#### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| Temporal platform fake frontend (RWB-PLT-E1070-CON) | A Temporal dev server with the namespace `rwb-recovery`, test CA certificates, the declared frontend API subset and a seeded smoke workflow | This story's checks before the cluster exists, the five services' worker tests, the integration harness |

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 0 | The platform has no `/api/recovery` base and no service short; the Web UI is an operational console, not a Workbench route |
| Kafka | 0 | 0 | The platform owns no topic and consumes none (DP-14) |
| Temporal | The cluster itself: frontend gRPC over mTLS on port 7233, Web UI over HTTPS, metrics on 9090 and health on 8080 | 0 workflows and 0 activities of its own | The 19 services' workers run on this cluster; namespace `rwb-recovery`; task queue `rwb-platform` is the platform queue |
| File | 0 | 0 | No file is read or written; the ledger seal file is out of scope |

### 13. Solution plan

**Package.** No Java package. The deployment assets live in `deploy/temporal/`; the run book lives in `docs/operations/runbooks/RWB-E1-070.md`; the dashboard lives in `ops/monitoring/`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| rwb-temporal-values.yaml | Helm values | Images, replica counts, resources, persistence, mTLS, metrics and ingress per environment |
| TemporalSchemaJob | Pipeline job | Creates `temporal` and `temporal_visibility` and runs the Temporal schema tool at the pinned release; idempotent |
| NamespaceBootstrapJob | Pipeline job | Registers `rwb-recovery` with retention 30 days and the four Keyword search attributes; idempotent |
| OidcConfig | Configuration | Entra ID app registration, redirect URI, role claims and the mapping to RW-PLATADM and RW-AUDIT |
| KeyVaultCertificateBinding | Configuration | CSI driver binding of the mTLS certificate and key; renewal before expiry |
| TemporalPlatformDashboard | Dashboard | Grafana JSON for service readiness, request rate, errors and persistence latency |
| TemporalPlatformRunBook | Document | The eight sections of the run book catalog, with the restart steps for each service |

**Database and namespace**

- Create the databases `temporal` and `temporal_visibility` with owner `temporal_svc` on the zone-redundant PostgreSQL flexible server.
- Create the role `temporal_svc` with no membership in any service login, and no service login with a grant on the two Temporal databases; revoke PUBLIC on both databases.
- Register `rwb-recovery` with retention 720 hours and the search attributes CaseId, Stage, ProductGroup and QueueCode as Keyword.
- Keep the ACE namespace `ace-collection` unregistered by this story; it belongs to the ACE team and is reached through Nexus.

**Configuration and reference data**

- Parameters through RWB-E1-042, published as the platform parameters contract RWB-PLT-E1042-CON (DP-06): `temporal.target`, `temporal.namespace`, `temporal.taskqueue.platform`, `temporal.retention.days` = 30.
- Helm values per environment: replica counts, resources, storage class, ingress host, certificate secret name, metrics scrape and log level.
- No business parameter and no reference table in this story; reference data is read through RWB-PLT-E1043-CON (DP-07) and no value is copied into a values file.
- The platform login and the platform admin base are not in the read sources: Not specified in the source documents (GAP-1440; ASM-2535).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**DP-01.** The cluster writes no ACE schema. It owns the two persistence stores and nothing else, and AC2 proves that `temporal_svc` cannot read `rwb_case.recovery_case`, so the split of the old `recovery` schema into per-service schemas is not quietly undone by a platform grant.

**DP-02.** One login per service, and `temporal_svc` is separate. The monolith's single `recovery_svc` login is replaced by one login per service; this story creates only `temporal_svc` and uses the P3 rwb-case login as the named counterparty in AC2, because rwb-case is the first owner of case data the engine serves.

**DP-04.** The Drools kit runs in each service's worker inside an activity and never in workflow code (Temporal and Drools Design slide 12). The platform hosts those workers; it installs no rule engine, holds no KieBase and makes no Drools call, and the kit contract is a precondition only.

**DP-05.** No service reads the ACE views except rwb-source-data, and the platform reads no ACE view at all. The workflows the cluster runs get their ACE data through the owning service's activity, so the cluster needs no view grant and no ACE login.

**DP-06.** Parameters arrive through the platform parameters contract rather than a values file: `temporal.target`, `temporal.namespace`, `temporal.taskqueue.platform` and `temporal.retention.days` = 30 are read at deploy time, and a change of environment value is a parameter change, not a rebuild.

**DP-07.** Reference data is read through RWB-PLT-E1043-CON and never copied into the chart. The only list this story touches is the environment list, which is a Helm value, and the role codes the Web UI maps, which come from RWB-P4-E1022-CON.

**DP-13.** There is no monolith API base and no `/api/recovery` base on the platform. The platform has no service short, so no path is published; the Web UI is reached on its own ingress and the frontend on gRPC 7233, both internal to the ACE network.

**DP-14.** The platform has no topic and events keep the owners' names. The decision-record topic, the case topic and the audit events stay with their owners, and the platform's Helm values carry no topic name at all.

**DP-15.** The Temporal schema job is not a Flyway migration. The two persistence stores are created and upgraded by the Temporal schema tool at the pinned release, outside the per-service Flyway sequence, so no service migration history records a Temporal object.

**DP-19.** The Web UI is not a Workbench screen, and screens go through gateway-bff. The console is an operational view with Entra ID sign-in behind it; no case screen is served by the platform, and the platform adds no route to the gateway.

**Build steps**

1. Write the values file for DEV and SIT and run helm lint and helm template in the pipeline, against the pinned release.
2. Build TemporalSchemaJob with the schema tool; prove a second run changes nothing and that no Flyway migration touches the two stores.
3. Build NamespaceBootstrapJob with retention and the four search attributes; prove a second run changes nothing.
4. Bind the certificate from Key Vault; test AC3 with no certificate, an expired certificate and a foreign certificate, using the profile the contract publishes.
5. Configure the OIDC app roles; test AC4 with RW-CASEOWN, RW-AUDIT and RW-PLATADM.
6. Add the metrics scrape on the contract endpoints and import the dashboard; check that every service reports.
7. Run the database grant checks for AC2 and add them to the access review.
8. Write the run book, hand it to RWB-PLT-E1056-OPS for the catalog and RunbookCompletenessTest, and run the frontend restart in SIT for AC6.

**Feature flag.** `rwb.p3.temporal`, read through the platform parameters contract. The flag controls the worker of RWB-PLT-E1071, not the cluster. With the flag off, the cluster and namespace stay in place and nothing else changes.

**Done when.** The checks in section 16 pass in DEV and SIT, the database grants are in the access review, the contract test of RWB-PLT-E1070-CON stays green, and operations restarts the frontend in SIT from the run book alone.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A Workbench role other than RW-PLATADM or RW-AUDIT signs in to the Web UI | You cannot {action} here. Your role does not include it. |

A certificate failure shows in the frontend log and the TLS alert only; no Workbench message is shown because no Workbench screen is involved. The run book names the alert text and the check. The platform login, the platform admin base and the approved release number are Not specified in the source documents (GAP-1440; ASM-2535).

### 15. Screens and states

No Workbench screen in this story. The operational view is the Temporal Web UI behind Entra ID, with two states: operate for RW-PLATADM and read-only for RW-AUDIT. A refused sign-in shows MSG-P4-002. The Grafana dashboard "Temporal platform" shows the five deployments, request rate, errors and persistence latency. The Web UI is not a Workbench screen and is not composed by gateway-bff (DP-19); the Workbench admin screens for platform settings come in Epic 8.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-070-01 | AC1, BR1, BR8 | Component | rwb-temporal release in DEV and SIT; namespace rwb-recovery |
| TC-E1-070-02 | AC2, BR2 | Component | Roles temporal_svc and the P3 rwb-case service login; cross-database SELECT on rwb_case.recovery_case and temporal.executions |
| TC-E1-070-03 | AC3, BR3 | Component | Worker with no certificate, an expired certificate and a foreign certificate |
| TC-E1-070-04 | AC4, BR4 | Component | Entra users U-62 RW-CASEOWN, U-53 RW-AUDIT and U-70 RW-PLATADM |
| TC-E1-070-05 | AC5, BR5 | Component | Namespace describe in SIT; retention and four search attributes |
| TC-E1-070-06 | AC6, BR6 | Integration | Smoke workflow platform-smoke-20261116 and a frontend pod delete |
| TC-E1-070-07 | AC7, BR7 | Component | Run book file and RunbookCompletenessTest |

The checks are run by the platform administrator and recorded in the release evidence; there is no Workbench endpoint and no Access test in this story. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: replica counts, retention, node sizes and releases are Helm values or parameters (BR8, DP-06).
- No personal data in logs, tests, workflow history or prompts: search attributes hold case codes and queue codes only; the smoke payload is synthetic.
- No read of another service's tables and no ACE view: the platform reads no `rwb_*` table and no `recovery.v_ace_*` view (DP-01, DP-05).
- Temporal persistence is never placed in the ACE database, and no service login is granted on the two Temporal stores (BR2).
- No Workbench account for a role other than RW-PLATADM and RW-AUDIT; no shared operator account (BR4).
- No clear personal data in a Temporal payload; the codec is the codec-server story's work.
- No mTLS bypass in DEV or SIT; a test that needs a certificate uses a certificate from the test CA, as the contract's fake declares.
- No platform topic, no platform `/api/recovery` base and no `rwb_*` schema: the platform is not one of the 19 services (DP-13, DP-14).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-007 | Every failure reaches a named owner; a tested way back | Epic 1, 3.2; Program, 5.2 | None (platform enabler) | All recovery processes | R-UNI-40; D-RCV-35 U1 | TC-E1-070-01, TC-E1-070-02, TC-E1-070-03, TC-E1-070-04, TC-E1-070-06, TC-E1-070-07 |
| REQ-DRI-010 | Environment values are versioned and changed without a code release | Epic 1, 3.2; Program, 5.1 and 5.7 | None (platform enabler) | All recovery processes | R-UNI-38 | TC-E1-070-01, TC-E1-070-05, TC-E1-070-07 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1070-CON | Contract | H consumer: publishes the namespace, client-identity, frontend API subset, OIDC role mapping, metrics and health contract and the fake frontend this story installs against |
| RWB-PLT-E1072-CON | Contract | H: the Drools kit the services' workers run; the platform hosts the workers and never calls Drools |
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON | Contract | H: the platform parameters and reference data read at deploy time, in place of values copied into code |
| RWB-PLT-E1047-CON | Contract | H: the topic naming library; the platform owns no topic |
| RWB-PLT-E1044-CON | Contract | H: the Flyway convention that the Temporal persistence stores deliberately do not use |
| RWB-PLT-N001-CON | Contract | H: gateway-bff; the Web UI is not a Workbench screen and the platform adds no route to the edge |
| RWB-PLT-E1056-OPS | DevOps | X: registers the run book in the run book catalog and runs RunbookCompletenessTest |
| RWB-P3-E1042-CON, RWB-P3-E1043-CON | Contract | C: parameters and reference data built against their published contracts and fakes |
| RWB-P4-E1022-CON | Contract | C: the RW-PLATADM and RW-AUDIT roles the Web UI maps, and the other roles it refuses |
| RWB-E2-037, RWB-E2-038, RWB-E2-039 | Legacy successors | Out of scope: workflow observability and run books, the codec server and admin audit, and backup, restore, zone failover, upgrade and archive |

### 19. Out of scope

- Case workflows (Epic 3) and the worker and SDK of the worker story (RWB-PLT-E1071).
- Workflow-level alerts, the stuck workflow scanner and the workflow dashboard (the successors of RWB-E2-037).
- The codec server, decode and the Temporal admin audit (the successors of RWB-E2-038).
- Backup, point-in-time restore, zone failover, upgrade procedure and archive (the successors of RWB-E2-039).
- The `ace-collection` namespace and the ACE team's own Temporal use; the platform registers `rwb-recovery` only.
- The Workbench smoke operation `POST /admin/workflows/smoke` and the platform task queue's own workflows (JOB-21 and JOB-22).
- Workbench screens and the admin console (Epic 8); the Web UI is an operational console, not a Workbench screen.
- The 19 services' schemas, topics, task queues and REST bases; the platform owns none of them.
