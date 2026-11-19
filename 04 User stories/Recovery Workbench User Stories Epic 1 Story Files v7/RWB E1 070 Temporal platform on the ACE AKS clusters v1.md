# RWB-E1-070 Temporal platform on the ACE AKS clusters

SCB Collections and Recovery. Henka Group, 16 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-070 |
| Epic | E1, release 30 November 2026 |
| Module | P3 Case and workflow |
| Feature | None (platform enabler) |
| Requirement IDs | REQ-DRI-007, REQ-DRI-010 |
| BRD section | Business Requirements Epic 1, section 3.2; Business Requirements Program, sections 5.1 and 5.2 |
| L3 process | All recovery processes |
| Decision | D-RCV-36 (T1); ADR-011 |
| Priority | Must |
| Depends on | RWB-E1-044, RWB-E1-056, RWB-E1-022 |
| Status | Ready for build |

## 1. Story

As a **platform administrator (RW-PLATADM)**, I want **a Temporal cluster per environment on the ACE AKS clusters, with its own persistence databases, the rwb-recovery namespace, mTLS and the Web UI behind Entra SSO**, so that **case workflows from Epic 3 have a durable engine that SCB IT runs like the rest of ACE**.

## 2. Business rationale

Case workflow begins in Epic 3, and a durable engine must exist before the first case workflow is written. ADR-011 replaces ADR-003 (DT09, DT10): Temporal runs the case lifecycle, while case data remains the system of record in the ACE DB recovery schema. If the engine is installed without its own database, identity, certificates and run book, Epic 3 builds on a shared service that nobody owns and a restart becomes a developer task.

This story provides the platform only: one Temporal cluster per environment on the ACE AKS clusters, the databases temporal and temporal_visibility owned by temporal_svc, the rwb-recovery namespace with 30-day retention and four search attributes, mTLS between the services, the Web UI behind Entra ID OIDC, metrics to the ACE monitoring stack and a run book with the eight sections of RWB-E1-056. It meets REQ-DRI-007 (a named owner and a tested way back for every failure) and REQ-DRI-010 (environment values come from parameters, not code). The measure is that DEV and SIT pass every check in section 16 and that operations restarts a stopped frontend in SIT from the run book alone.

## 3. Preconditions

- RWB-E1-044 is done: migrations run with parameterized schema names, and the ACE database exists in each environment.
- RWB-E1-056 is done: job_catalog, the run book catalog and RunbookCompletenessTest exist and accept a new run book with the eight sections.
- RWB-E1-022 is done: Entra ID SSO, MFA and the application roles exist, including RW-PLATADM and RW-AUDIT.
- The ACE AKS clusters for DEV, SIT, UAT and PROD exist with the ACE namespace, a zone-redundant PostgreSQL flexible server, Azure Key Vault and the ACE monitoring namespace.
- SCB IT approved the Temporal server and Java SDK release on 16 November 2026; the approved version is recorded in Environment and Deployment Design v4 and is not selected by the build.
- An internal DNS name and ingress exist for the Web UI; the frontend gRPC port 7233 is reachable only from the cluster network and the worker subnets.
- The ACE internal certificate authority issues the mTLS certificates, and the platform administrator may read the certificate from Key Vault.
- The platform administrator holds RW-PLATADM through the environment group; RW-AUDIT holds RW-AUDIT through the environment group.

## 4. Flow

1. Platform administrator: deploys Helm release rwb-temporal into the ACE namespace of DEV, then SIT, from the values file; the chart runs frontend, history, matching, internal-worker and web.
2. TemporalSchemaJob: creates the databases temporal and temporal_visibility owned by temporal_svc, then runs the Temporal schema tool at the pinned server version; a second run changes nothing.
3. NamespaceBootstrapJob: registers the namespace rwb-recovery with retention 30 days and the Keyword search attributes CaseId, Stage, ProductGroup and QueueCode; a second run changes nothing.
4. Platform administrator: binds the mTLS certificate and key from Key Vault to the frontend and the workers through the CSI driver; the certificate is issued by the ACE internal CA and names the namespace.
5. Platform administrator: configures the Web UI with Entra ID OIDC; the app roles map RW-PLATADM to operate and RW-AUDIT to read; any other role is refused.
6. Platform administrator: turns on the metrics scrape to the ACE monitoring stack and imports the platform dashboard.
7. Platform administrator: runs every check in section 16 and records the pinned server and SDK version in Environment and Deployment Design v4.
8. Platform administrator: writes the run book with the eight sections and asks operations to restart the frontend in SIT from the run book alone.
9. System: a frontend pod restart or reschedule keeps every workflow; history and visibility are durable in PostgreSQL, and the workers reconnect to the new pod.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A client connects to the frontend with no certificate, an expired certificate or a certificate for another namespace | The TLS handshake fails or the call is refused; no workflow call is served and the event is in the frontend log with the client identity only | None (TLS) | AC3 |
| X2 | A user with a Workbench role other than RW-PLATADM or RW-AUDIT signs in to the Web UI | The sign-in is refused; no namespace is listed and no workflow is shown | MSG-P4-002 | AC4 |
| X3 | A grant joins the two databases, for example temporal_svc on the recovery schema or recovery_svc on temporal | The access review check fails, the release is held and the grant is removed before the next environment | None (access review) | AC2 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Stands alone as infrastructure; it needs the ACE cluster, the schema of RWB-E1-044, the roles of RWB-E1-022 and the run book catalog of RWB-E1-056 |
| Negotiable | Pod sizes, storage class, replica count, certificate life and dashboard panels are Helm values; the separation of databases and the namespace settings are fixed |
| Valuable | Epic 3 starts on an engine that SCB IT can run, restart and review like the rest of ACE |
| Estimable | One Helm release, two databases, one namespace bootstrap, one OIDC app, one certificate binding, one dashboard and one run book |
| Small | Fits two weeks with its checks |
| Testable | Each criterion in section 7 is one check in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Temporal platform on the ACE AKS clusters

  Background:
    Given the ACE AKS clusters for DEV and SIT with the ACE namespace
    Given the platform administrator U-70 holds RW-PLATADM through the environment group

  Scenario: AC1 Cluster healthy
    Given the rwb-temporal Helm release is installed in the ACE namespace of DEV and SIT
    When U-70 opens the Temporal Web UI and selects the namespace rwb-recovery
    Then the frontend, history, matching and internal-worker deployments each show 2 of 2 pods ready
    Then the web deployment answers on its internal ingress
    Then the namespace rwb-recovery is listed with status REGISTERED
    Then no pod of the release restarted in the last 24 hours

  Scenario: AC2 Separate database grants
    Given temporal_svc owns the databases temporal and temporal_visibility
    Given recovery_svc owns the recovery schema in the ACE database
    When a session as temporal_svc runs SELECT on recovery.recovery_case
    Then PostgreSQL refuses the statement with SQLSTATE 42501 and returns no row
    When a session as recovery_svc runs SELECT on temporal.executions
    Then PostgreSQL refuses the statement with SQLSTATE 42501 and returns no row
    Then the access review report shows no grant between the two roles and the two databases

  Scenario: AC3 mTLS enforced
    Given the frontend requires a client certificate signed by the ACE internal CA
    When a worker connects to port 7233 with no certificate
    Then the TLS handshake fails and no workflow call is served
    When a worker connects with an expired certificate
    Then the TLS handshake fails with certificate expired
    When a worker connects with a certificate issued for another namespace
    Then the call is refused with PERMISSION_DENIED and no workflow is started

  Scenario: AC4 Web UI roles
    Given the Temporal Web UI uses the Entra ID OIDC application with the Workbench app roles
    When U-62 holds RW-CASEOWN only and signs in to the Web UI
    Then the sign-in is refused with MSG-P4-002 and no namespace is listed
    When U-53 holds RW-AUDIT and signs in
    Then U-53 sees the namespace rwb-recovery and every workflow page is read-only
    Then U-53 cannot terminate, reset or signal a workflow
    When U-70 holds RW-PLATADM and signs in
    Then U-70 may terminate and reset a workflow in DEV, and every action is in the frontend audit log

  Scenario: AC5 Namespace settings
    Given the namespace rwb-recovery in SIT
    When U-70 describes the namespace
    Then retention is 720 hours, 30 days
    Then the search attributes CaseId, Stage, ProductGroup and QueueCode are registered as Keyword
    Then no search attribute holds a name, a national ID or another personal data field

  Scenario: AC6 Frontend restart loses no workflow
    Given the smoke workflow platform-smoke-20261116 is RUNNING and waits on its timer
    When the frontend pod is deleted and a replacement pod becomes ready
    Then the workflow is still RUNNING with the same workflow ID and run ID
    When the timer fires and the activity completes
    Then the workflow status is COMPLETED
    Then the history holds every event once, with no gap and no duplicate start

  Scenario: AC7 Run book with the eight headings
    Given the run book docs/operations/runbooks/RWB-E1-070.md
    When RunbookCompletenessTest reads the run book
    Then the run book has the sections purpose, schedule, owner, dependencies, failure signs, checks, restart steps and escalation
    Then it names the five Temporal services, the two databases, the namespace, the certificate renewal step and the parameter temporal.target
    Then it names roles and service identities, never a person and never a personal data field
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One Temporal cluster per environment, on the ACE AKS clusters, deployed by the official Temporal Helm chart; the server and Java SDK version are pinned to the SCB IT approved release and recorded in Environment and Deployment Design v4 | D-RCV-36 T1; ADR-011 |
| BR2 | Temporal persistence is separate from the ACE database: databases temporal and temporal_visibility are owned by temporal_svc; temporal_svc has no grant on the ACE database and recovery_svc has no grant on the Temporal databases | D-RCV-36 T1 |
| BR3 | The frontend requires mTLS from every client; certificates come from the ACE internal CA through Key Vault and are renewed before expiry | D-RCV-36 T1 |
| BR4 | The Web UI is behind Entra ID OIDC: RW-PLATADM operates, RW-AUDIT reads, every other role is refused; decode is not in this story | D-RCV-36 T1; RWB-E1-022 |
| BR5 | One namespace per environment, rwb-recovery; retention is 30 days and the only search attributes are CaseId, Stage, ProductGroup and QueueCode as Keyword | D-RCV-36 T1 |
| BR6 | A frontend pod restart loses no workflow; history and visibility are durable in PostgreSQL | D-RCV-36 T1; AC6 |
| BR7 | The run book has the eight sections of RWB-E1-056 and is tested by RunbookCompletenessTest | RWB-E1-056 |
| BR8 | Server and SDK versions, replica counts, retention and node sizes are Helm values or parameters, never code | REQ-DRI-010 |

## 9. State transitions

None. This story changes no case status. It establishes the namespace and the cluster; a workflow created in Epic 3 moves through its own states. A namespace has one state, REGISTERED, and a server has one state, RUNNING; a server upgrade stays RUNNING and is checked by AC1 after the change.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM | Installs and upgrades the release, runs the namespace bootstrap, reads the database grants, operates the Web UI and restarts a service (Platform administration, U) |
| RW-AUDIT | Reads the namespace and workflow history in the Web UI (Platform administration, R) |
| RW-SECADM | Reads the certificate and OIDC configuration; decode through the codec server is RWB-E2-038, not this story |
| RW-CASEOWN and every other Workbench role | No Web UI access; a sign-in is refused with MSG-P4-002 |
| SY-CASEWF | Connects to the frontend as the worker with its own client certificate; no Web UI account |
| SY-RULES | Runs the Drools evaluator inside the recovery module and does not connect to Temporal directly |
| RW-TRIBE | Maintains the Helm values and the run book through the change process; may not deploy to PROD |
| No delegation of authority level applies | A platform deployment is not a credit decision |

## 11. Data

Temporal persistence is outside the recovery schema. This story reads and writes no table in the recovery schema, and no DF-REF, DF-CAS or DF-DEC field is added or changed.

| Store | What it holds | Owner | In the Physical Schema |
|---|---|---|---|
| temporal | Workflow histories, mutable state, timers, tasks | temporal_svc | No |
| temporal_visibility | Workflow visibility records and search attributes | temporal_svc | No |
| ACE database recovery schema | Case data, the system of record | recovery_svc | Yes, unchanged by this story |

The Physical Schema v6 counts 93 tables and does not include the Temporal tables. The databases are created by TemporalSchemaJob; no Flyway migration in the recovery module touches them.

## 12. Contract

No Workbench endpoint. This story adds no path under /api/recovery/v1. The platform interfaces are internal to the ACE network.

| Interface | Method | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|
| Temporal frontend | gRPC over mTLS, port 7233: StartWorkflowExecution, SignalWorkflowExecution, DescribeWorkflowExecution | namespace rwb-recovery, workflow type, workflow ID, task queue, encrypted input | workflow ID and run ID | TLS handshake failure; NOT_FOUND namespace; PERMISSION_DENIED; FAILED_PRECONDITION | Client certificate from the ACE internal CA with the namespace claim | Workflow ID is the idempotency key; a repeated start with the same ID returns the running execution |
| Temporal Web UI | HTTPS 443: HTTP GET and POST through the internal ingress (OIDC sign-in and UI pages) | Entra ID OIDC authorization code flow | namespace and workflow pages | 401 MSG-P4-001 when the user has no Workbench role; 403 MSG-P4-002 when the role is not RW-PLATADM or RW-AUDIT | Entra app role RW-PLATADM (operate) or RW-AUDIT (read) | Read only; sign-in is safe to repeat |
| Metrics endpoint | HTTPS GET /metrics, port 9090 | Prometheus scrape of the Temporal SDK metrics | OpenMetrics text | None | Network policy from the ACE monitoring namespace only | Read only |
| Health endpoint | HTTP GET /health, port 8080 | None | 200 when the service is ready, 503 when it is not | 503 | Cluster probe only | Read only |

The frontend never accepts a Workbench JWT. The Workbench API does not proxy case workflow calls in Epic 1; the smoke endpoint of RWB-E1-071 is the only Workbench path that starts a workflow, and the worker connects to the frontend directly.

## 13. Solution plan

**Package.** No Java package. The deployment assets live in `deploy/temporal/`; the run book lives in `docs/operations/runbooks/RWB-E1-070.md`; the dashboard lives in `ops/monitoring/`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| rwb-temporal-values.yaml | Helm values | Images, replica counts, resources, persistence, mTLS, metrics and ingress per environment |
| TemporalSchemaJob | Pipeline job | Creates temporal and temporal_visibility and runs the Temporal schema tool at the pinned version; idempotent |
| NamespaceBootstrapJob | Pipeline job | Registers rwb-recovery with retention 30 days and the four Keyword search attributes; idempotent |
| OidcConfig | Configuration | Entra ID app registration, redirect URI, role claims and the mapping to RW-PLATADM and RW-AUDIT |
| KeyVaultCertificateBinding | Configuration | CSI driver binding of the mTLS certificate and key; renewal before expiry |
| TemporalPlatformDashboard | Dashboard | Grafana JSON for service readiness, request rate, errors and persistence latency |
| TemporalPlatformRunBook | Document | The eight sections of RWB-E1-056, with the restart steps for each service |

**Database and namespace**

- Create the databases temporal and temporal_visibility with owner temporal_svc on the zone-redundant PostgreSQL flexible server.
- Create the roles temporal_svc and recovery_svc with no membership in each other; revoke PUBLIC on both databases.
- Register rwb-recovery with retention 720 hours and the search attributes CaseId, Stage, ProductGroup and QueueCode as Keyword.
- Keep ace-collection unregistered; it belongs to the ACE team.

**Configuration and reference data**

- Parameters through RWB-E1-042: temporal.target, temporal.namespace, temporal.taskqueue.platform, temporal.retention.days = 30.
- Helm values per environment: replica counts, resources, storage class, ingress host, certificate secret name, metrics scrape and log level.
- No business parameter and no reference table in this story.

**Build steps**

1. Write the values file for DEV and SIT and run helm lint and helm template in the pipeline.
2. Build TemporalSchemaJob with the schema tool; prove a second run changes nothing.
3. Build NamespaceBootstrapJob with retention and the four search attributes; prove a second run changes nothing.
4. Bind the certificate from Key Vault; test AC3 with no certificate, an expired certificate and a foreign certificate.
5. Configure the OIDC app roles; test AC4 with RW-CASEOWN, RW-AUDIT and RW-PLATADM.
6. Add the metrics scrape and import the dashboard; check that every service reports.
7. Run the database grant checks for AC2 and add them to the access review.
8. Write the run book and pass RunbookCompletenessTest; run the frontend restart in SIT for AC6.

**Feature flag.** `rwb.p3.temporal`. The flag controls the worker of RWB-E1-071, not the cluster. With the flag off, the cluster and namespace stay in place and nothing else changes.

**Done when.** The checks in section 16 pass in DEV and SIT, the database grants are in the access review, and operations restarts the frontend in SIT from the run book alone.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A Workbench role other than RW-PLATADM or RW-AUDIT signs in to the Web UI | You cannot {action} here. Your role does not include it. |

A certificate failure shows in the frontend log and the TLS alert only; no Workbench message is shown because no Workbench screen is involved. The run book names the alert text and the check.

## 15. Screens and states

No Workbench screen in this story. The operational view is the Temporal Web UI behind Entra ID, with two states: operate for RW-PLATADM and read-only for RW-AUDIT. A refused sign-in shows MSG-P4-002. The Grafana dashboard "Temporal platform" shows the five services, request rate, errors and persistence latency. The Workbench admin screens for platform settings come in Epic 8.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-070-01 | AC1, BR1, BR8 | System | rwb-temporal release in DEV and SIT; namespace rwb-recovery |
| TC-E1-070-02 | AC2, BR2 | Operational | Roles temporal_svc and recovery_svc; cross-database SELECT |
| TC-E1-070-03 | AC3, BR3 | System | Worker with no certificate, an expired certificate and a foreign certificate |
| TC-E1-070-04 | AC4, BR4 | Operational | Entra users U-62 RW-CASEOWN, U-53 RW-AUDIT and U-70 RW-PLATADM |
| TC-E1-070-05 | AC5, BR5 | System | Namespace describe in SIT; retention and four search attributes |
| TC-E1-070-06 | AC6, BR6 | Operational | Smoke workflow platform-smoke-20261116 and a frontend pod delete |
| TC-E1-070-07 | AC7, BR7 | Operational | Run book file and RunbookCompletenessTest |

The checks are run by the platform administrator and recorded in the release evidence; there is no Workbench endpoint and no Access test in this story. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: replica counts, retention, node sizes and versions are Helm values or parameters.
- No personal data in logs, tests, workflow history or prompts: search attributes hold case codes and queue codes only; the smoke payload is synthetic.
- No read of another module's tables; ACE data only through recovery.v_ace_* views: this story reads no recovery or ACE table.
- Temporal persistence is never placed in the ACE database, and the recovery schema is never granted to temporal_svc.
- No Web UI account for a role other than RW-PLATADM and RW-AUDIT; no shared operator account.
- No clear personal data in the Temporal payload; the codec is RWB-E1-071.
- No mTLS bypass in DEV or SIT; a test that needs a certificate uses a certificate from the test CA.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-007 | Every failure reaches a named owner; a tested way back | Epic 1, 3.2; Program, 5.2 | None (platform enabler) | All recovery processes | R-UNI-40; D-RCV-35 U1 | TC-E1-070-01, TC-E1-070-02, TC-E1-070-03, TC-E1-070-04, TC-E1-070-06, TC-E1-070-07 |
| REQ-DRI-010 | Environment values are versioned and changed without a code release | Epic 1, 3.2; Program, 5.1 and 5.7 | None (platform enabler) | All recovery processes | R-UNI-38 | TC-E1-070-01, TC-E1-070-05, TC-E1-070-07 |

## 19. Out of scope

- Case workflows (Epic 3) and the worker (RWB-E1-071).
- Workflow-level alerts, the stuck workflow scanner and the workflow dashboard (RWB-E2-037).
- The codec server, decode and the Temporal admin audit (RWB-E2-038).
- Backup, point-in-time restore, zone failover, upgrade procedure and archive (RWB-E2-039).
- The ace-collection namespace and the ACE team's own Temporal use.
- Workbench screens and the admin console (Epic 8).
