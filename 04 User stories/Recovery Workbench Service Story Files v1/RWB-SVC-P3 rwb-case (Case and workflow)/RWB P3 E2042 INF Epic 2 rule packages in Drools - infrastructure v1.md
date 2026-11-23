# RWB-P3-E2042-INF Epic 2 rule packages in Drools

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2042-INF |
| Work type | INF (Infrastructure) |
| Suggested owner | SCB IT infrastructure (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-042 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-AP |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-027, FR-P3-028, FR-P3-029) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-042 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **infrastructure engineer**, I want **the write-once Blob container `rule-packages` with its checksum metadata and private access, the Key Vault secret and certificate that let rwb-case authenticate to rwb-decision and read that container, the compute and memory to hold 20 KieBases per pod, the one-hop network path to rwb-decision and to the schema registry, and the isolated Testcontainers PostgreSQL that the schema gate migrates**, so that **the three Epic 2 workbooks are stored immutably, the fetched model is provably the approved one, and the service can hold and swap rule models without touching a table, a topic or another service's data**.

### 2. Business rationale

The Epic 2 packages are the only place where a business person changes how this service decides, and the target moves their governance to rwb-decision while keeping the evaluated copy local (Arch v5 slide 27; D-RCV-36 T3 to T6; DP-04). That split needs three pieces of infrastructure that the legacy monolith did not have: an immutable store for the workbook that is the authored artefact, an identity that can read that store and call rwb-decision over mTLS, and enough memory on each pod to keep up to 20 compiled models so that an evaluation never compiles a table (Temporal and Drools slide 16).

Without the immutable store, a workbook can be edited silently and the SHA-256, which is the only proof that a decision came from the approved version, proves nothing. Without the identity and the certificate, the model cannot be fetched at all. Without the memory, the cache of 20 versions either thrashes or the pod is killed under load, and a killed pod during a swap is exactly the case the last-good-model rule exists for.

This story creates no `rwb_*` table, no topic, no queue and no business value. It provisions and configures; the app story builds the cache and the swap, and the operations story owns the consumer group, the readiness signal, the dashboards and the alerts.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The platform Blob account and the platform Key Vault are available with the workload identity mechanism of the platform (RWB-PLT-LIB), so no credential sits in a file, a chart or a repository.
- The rwb-decision service is reachable through the platform service mesh with mTLS, and its front end presents a certificate the platform certificate authority issued (Arch v5 slides 11 and 20).
- The schema registry of RWB-PLT-N008-INF exists, because a service validates a produced payload against its subject before the outbox relay publishes it (DP-09, DP-14).
- The three package codes and the three version labels are agreed: RESTRUCTURE "RES-2026.12", PAYMENT_MATCH "PMT-2026.12" and BOOKING_MATCH "BKG-2026.12", all valid from 2026-12-15 (the valid-from date is the legacy assumption and is copied unchanged).
- The embedded Drools kit contract is available (RWB-PLT-E1072-CON, DP-04): the cache bound of 20 versions, the checksum check and the atomic swap are its elements.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Provision the Blob container `rule-packages` in the platform storage account for each environment, with a write-once (immutability) policy, a private access level and no public endpoint.
2. Set the object layout and the metadata contract: `<PACKAGE_CODE>/<VERSION_LABEL>.xlsx`, with the package code, the version label, the SHA-256 of the workbook and the author role in the object metadata.
3. Create the workload identity of rwb-case, grant it read on that container only, and grant it no list, no write and no delete outside the object read it needs.
4. Provision the Key Vault entries: the rwb-case mTLS client certificate and its secret reference for the rwb-decision front end, and the storage reference the workload identity uses for the container; no literal value reaches a values file, a chart template or a log.
5. Size the pod for the model cache: the heap request and limit that hold 20 KieBases of the three packages plus their working set, recorded as reviewed values and validated by a load test.
6. Open the one-hop network path from the rwb-case pods to rwb-decision and to the schema registry, with no broader egress, and record the allowed destinations as a reviewed list.
7. Provision an isolated PostgreSQL for the build's Testcontainers run of the schema gate: a database that is migrated from empty, holds no SIT, UAT or PROD data, and dies with the pipeline job.
8. Hand the naming, the metadata keys and the identity to RWB-P3-E2042-APP and the destinations and metrics to RWB-P3-E2042-OPS.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A write is attempted on an existing object path | The immutability policy refuses the overwrite; the old object and its checksum stay | None | AC2 |
| X2 | An object is stored without the checksum metadata | The verification step of the swap refuses the model; the object is flagged for the platform administrator | None | AC2 |
| X3 | The container policy allows public access, or the identity holds a broader grant | The provisioning check fails and the environment is not marked ready | None | AC1 |
| X4 | The mTLS certificate is missing, expired or not issued by the platform certificate authority | The call to rwb-decision fails the handshake; the swap is alerted and the model in force stays | None | AC3 |
| X5 | The pod is sized below the memory the cache needs | The load test shows an out-of-memory restart during a swap; the sizing is reviewed and the release is blocked | None | AC4 |
| X6 | A destination outside the one-hop list is called | The network policy drops the call; the attempt is counted and alerted | None | AC5 |
| X7 | A build job points the schema gate at a shared or non-test database | The pipeline refuses to run the gate; no migration touches a shared database | None | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Provisions storage, identity, certificate, sizing, network and a test database; no application code is built here |
| Negotiable | The retention period, the heap values and the port numbers are environment values settled with the platform team, not story decisions |
| Valuable | Makes the immutable workbook, the checksum-verified fetch and the cached model possible at all, and unblocks the app story on Day 1 |
| Estimable | One container with its policy, one identity and its grants, two Key Vault entries, one sizing decision, one network path set and one test database |
| Small | Fits one sprint with the provisioning checks |
| Testable | Every criterion tests an artefact: the container policy, a refused overwrite, a handshake, a load test, a dropped call and a gate run |

### 7. Acceptance criteria

```gherkin
Feature: Infrastructure for the Epic 2 rule packages in rwb-case

  Background:
    Given the platform storage account, Key Vault and service mesh are in force
    Given the three package codes are RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH

  Scenario: AC1 The container rule-packages exists with private access and a read-only identity (new, D-RCV-60)
    Given the container rule-packages in each environment
    When its access level and the grants of the rwb-case workload identity are inspected
    Then the container has no anonymous or public access
    Then the rwb-case workload identity holds read on that container only
    Then it holds no write, no delete and no list outside the object read it needs
    Then no other service's identity holds a grant on the container
    Then the provisioning check fails the environment when any of the four conditions is not met

  Scenario: AC2 The container is write-once and every object carries its checksum (new, D-RCV-60)
    Given an object stored at RESTRUCTURE/RES-2026.12.xlsx
    When a second write is attempted on the same path
    Then the immutability policy refuses the overwrite and the stored object is unchanged
    Then the object metadata carries the package code, the version label, the SHA-256 of the workbook and the author role
    Then an object without the checksum metadata is flagged and refused by the model verification step
    Then the retention and immutability period is the reviewed value recorded for the environment

  Scenario: AC3 The rwb-case identity and certificate reach rwb-decision over mTLS (new, D-RCV-60)
    Given the Key Vault entries of the environment
    When rwb-case calls the rwb-decision front end
    Then the client certificate and its secret are read from Key Vault by the workload identity and never from a file or a chart value
    Then the handshake succeeds only with a certificate the platform certificate authority issued, and fails when it is expired or unissued
    Then no secret, no key and no certificate body appears in a values file, a log, a dashboard or a chart template
    Then the rotation of the certificate is a Key Vault operation with no rebuild of the service

  Scenario: AC4 The compute and memory hold 20 KieBases per pod (new, D-RCV-60)
    Given the reviewed heap request and limit of the rwb-case pod
    When a load test caches 20 package versions and evaluates under load
    Then no out-of-memory restart occurs and no eviction touches a version in force
    Then the sizing is recorded as reviewed values per environment and is not hard-coded in a template
    Then the sizing figure itself is Not specified in the source documents (GAP-0723; ASM-1270)

  Scenario: AC5 The network path to rwb-decision and the schema registry is one hop (new, D-RCV-60)
    Given the network policy of the rwb-case pods
    When the allowed destinations are inspected
    Then rwb-decision and the schema registry are allowed, one hop each, on the reviewed ports
    Then no other destination outside the reviewed list is reachable
    Then a call to an unlisted destination is dropped, counted and alerted
    Then the Blob endpoint of the rule-packages container is allowed and no other storage endpoint is

  Scenario: AC6 The schema gate runs on an isolated Testcontainers PostgreSQL (new, D-RCV-60)
    Given the pipeline job that runs PaymentMatchRuleAbsentCheck
    When the gate runs
    Then it migrates a Testcontainers PostgreSQL from empty with the release migrations and then drops it
    Then it reads no SIT, UAT or PROD database and holds no production data
    Then it asserts 93 tables, no table named payment_match_rule and no column of DF-REF-261 to DF-REF-273
    Then a job pointed at a shared database is refused before any migration runs
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One container per environment, named `rule-packages`, with no public access and a write-once policy | Arch v5 slide 27 (a version is dated and never edited); DP-04 |
| BR2 | The object path is `<PACKAGE_CODE>/<VERSION_LABEL>.xlsx`, and the object metadata carries the package code, the version label, the SHA-256 and the author role | The authoring contract of RWB-P3-E2042-CON |
| BR3 | The rwb-case workload identity holds read on that container only; no service writes a workbook through the application | DP-02; DP-04 |
| BR4 | Every secret and every certificate comes from Key Vault through the workload identity; none appears in a file, a chart, a log or a dashboard | Template and Rules §R7.2 s17 |
| BR5 | The pod is sized to hold 20 KieBases plus the working set, and the figure is a reviewed value per environment, never a template constant | DP-04; Temporal and Drools slide 16 |
| BR6 | The service reaches rwb-decision and the schema registry one hop, on the reviewed ports, and nothing else outside the reviewed list | DP-11; ADR-020 |
| BR7 | The schema gate runs on a Testcontainers PostgreSQL migrated from empty and never on a shared database | RWB-PLT-E1044-CON; DP-15 |
| BR8 | This story creates no `rwb_*` table, no topic, no queue and no Schedule; storage and identity are the whole deliverable | Template and Rules §R7.2 s12 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not provisioned | Container created | The immutability policy, the private access level and the identity grant are in place | Provisioned |
| Provisioned | First workbook stored | The object carries the four metadata keys and the checksum matches the loaded version | Active |
| Active | New version stored | A new object under the same package code with a new version label | Active (two objects) |
| Active | Overwrite attempted | The path already exists | Unchanged; the write is refused |
| Active | Certificate rotated | The Key Vault entry is updated and the workload identity reloads it | Active (new certificate) |
| Active | A policy check fails after a platform change | The private access level or the grant drifts | Degraded; the environment is not marked ready |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SCB IT infrastructure | Owns the container, its policy, the identity grants, the Key Vault entries, the network policy and the sizing |
| ACE platform team | Owns the storage account, the Key Vault, the certificate authority and the service mesh this story configures against |
| Security | Approves the identity grant, the secret references and the network allow list |
| The rwb-case owner team | Confirms the sizing after the load test and consumes the container and the certificate |
| Platform administrator | Extends the immutability period when the audit requirement changes, and rotates the certificate |
| ACE database administrator | Confirms that the schema gate database is a test database and holds no shared data |

The identity name, the Key Vault entry names and the certificate subject are Not specified in the source documents (GAP-0722; ASM-1269); this story fixes their shape and leaves the names to the environment configuration.

### 11. Data

| Item | Content |
|---|---|
| Container | `rule-packages`, one per environment, private, write-once, no public endpoint |
| Object layout | `<PACKAGE_CODE>/<VERSION_LABEL>.xlsx` for RESTRUCTURE/RES-2026.12.xlsx, PAYMENT_MATCH/PMT-2026.12.xlsx and BOOKING_MATCH/BKG-2026.12.xlsx |
| Object metadata | package code, version label, SHA-256 of the workbook, author role, authored date, environment |
| Key Vault entries | The rwb-case mTLS client certificate and secret for the rwb-decision front end, and the storage reference for the container read |
| Network allow list | rwb-decision one hop, the schema registry one hop, the Blob endpoint of the container, on the reviewed ports |
| Pod sizing | Heap request and limit, the thread pool of the evaluator, the cache bound of 20 versions |
| Test database | A Testcontainers PostgreSQL per gate run, migrated from empty and dropped with the job |

The retention and immutability period, the exact heap values, the ports and the certificate subject are Not specified in the source documents (GAP-0723; ASM-1270); they are reviewed values per environment and are recorded here as assumptions, not as business values. The container holds workbooks and their metadata only: no case data, no personal data and no business value.

### 12. Contract

#### 12.1 REST operations provided

None. This story exposes no API, no cache read and no operator endpoint. The readiness and liveness endpoints are cluster-internal and are owned by RWB-P3-E2042-OPS.

#### 12.2 REST operations consumed

None as a business operation. The network path to rwb-decision and to the schema registry is a platform route configured here; the operations that run on it are consumed by RWB-P3-E2042-APP and declared in RWB-P3-E2042-CON. This story adds no call of its own.

#### 12.3 Events published

None. The story provisions no topic and publishes no event.

#### 12.4 Events consumed

None. The RulePackageInForce consumer group is RWB-P3-E2042-OPS; this story only ensures the network path and no message is read here.

#### 12.5 Workflows and activities

None. No Temporal workflow, activity or task queue is created by this story; the model swap workflow belongs to RWB-P3-E2042-APP.

#### 12.6 Schedules

None. The 00:01 promotion is JOB-20 in rwb-decision and this story registers no Schedule.

#### 12.7 Tables owned

None. This story creates no `rwb_*` table, no column and no index; the storage is a Blob container and the secrets are Key Vault entries, neither of which is an ACE DB table.

#### 12.8 Contract fakes

None. The fakes run in the pipeline and in SIT and belong to RWB-P3-E2042-CON and RWB-P3-E2042-OPS; no fake is deployed or configured here.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None | No operation is provided or consumed by this story; the routes it opens carry the app story's calls |
| Kafka | None | No topic, no producer, no consumer |
| Temporal | None | No workflow, activity or task queue |
| File | 1 storage path | The write-once container `rule-packages` with its three object paths and their metadata |

### 13. Solution plan

**Deliverables.** `infra/storage/rule-packages.json` (the container, its immutability policy, its access level and the object metadata rules), `infra/identity/rwb-case-workload.json` (the identity and its read grant), `infra/keyvault/entries.md` (the certificate and the storage reference), `infra/network/egress.yaml` (the one-hop allow list), `infra/sizing/rule-cache.yaml` (the heap values per environment) and `infra/testcontainers/schema-gate.yaml` (the isolated gate database).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-04 is the pattern this story serves: the local evaluated copy needs an immutable source, an identity to fetch it and memory to hold it. DP-15 is served by the isolated gate database, which migrates the service's own schema and nothing else. No other pattern adds work here; the table, topic, queue and Schedule rows of the other stories are untouched.

**Build steps**

1. Create the container with the immutability policy, the private access level and no public endpoint; add the provisioning check that verifies all three (AC1, AC2, X3).
2. Define the object layout and the four metadata keys; store the three workbooks as the first objects and verify each checksum (AC2).
3. Create the workload identity and the read grant on the container only; verify that write, delete and list are refused (AC1, X1).
4. Create the Key Vault certificate and secret reference for the rwb-decision front end; test the handshake with a valid, an expired and an unissued certificate (AC3, X4).
5. Size the pod: run the load test that caches 20 versions and evaluates under load, and record the heap values per environment (AC4, X5).
6. Write the one-hop egress list and the drop rule; test a call to an unlisted destination (AC5, X6).
7. Provision the Testcontainers PostgreSQL for the gate, isolate it from every shared database, and run `PaymentMatchRuleAbsentCheck` once against it (AC6, X7).
8. Hand the container name, the metadata keys and the identity reference to the app story, and the allowed destinations and the sizing to the operations story.

**Done when.** The container is private and write-once in all three environments, a second write to an existing path is refused, every object carries its checksum, the mTLS handshake succeeds with the issued certificate only, the load test caches 20 versions without an out-of-memory restart, the egress list is one hop, and the gate runs on a private test database.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| None | A policy, identity or certificate check fails | No business message is produced. The provisioning check fails the environment with the resource name and the violated rule, and the platform administrator acts on it. |

This story adds no message ID. The business messages of the capability keep their identifiers and texts from the legacy story and from the message catalogue: MSG-P3-027 (a rule version refused or no version in force), MSG-P7-002 (the author cannot approve), MSG-GEN-001, MSG-GEN-003 and MSG-GEN-004 (workbook and date checks) and MSG-P4-002 (a role without the right). The infrastructure reports a condition to the operator, never to a workbench user.

### 15. Screens and states

None. There is no screen in this story. The operator-facing surfaces are the environment's provisioning check, the container policy view and the load-test report; the model-cache readiness signal and the dashboards are RWB-P3-E2042-OPS.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E2042-INF-01 | AC1 | NFR | The container policy and the identity grants in DEV, SIT and UAT; a cross-service write, a delete and a list are each refused |
| TC-P3-E2042-INF-02 | AC2 | Component | A first store of RES-2026.12.xlsx, a second write to the same path, and an object stored without the checksum metadata |
| TC-P3-E2042-INF-03 | AC3 | NFR | mTLS with a valid, an expired and an unissued certificate; the Key Vault read by the workload identity; no secret in a chart value or a log |
| TC-P3-E2042-INF-04 | AC4 | NFR | A load test caching 20 package versions and evaluating under load; the heap values recorded per environment |
| TC-P3-E2042-INF-05 | AC5 | Component | The egress allow list; an allowed call to rwb-decision and the schema registry; a dropped call to an unlisted destination |
| TC-P3-E2042-INF-06 | AC6 | Integration | A Testcontainers PostgreSQL migrated from empty, 93 tables, no payment_match_rule, and a job pointed at a shared database is refused |

### 17. Guardrails

- No business value in a policy or a values file: rows, tolerances, windows, action text, owner roles and timers stay in the workbooks and the registry.
- No personal data in the container, in an object path, in an object metadata key or in a log: the container holds workbooks and identifiers only.
- One container, one identity, one read grant; no service writes a workbook through the application and no identity outside rwb-case holds a grant (DP-02).
- No secret, key or certificate body in a file, a chart value, a dashboard or a log; everything comes from Key Vault through the workload identity.
- The service reaches rwb-decision, the schema registry and its own storage endpoint and nothing else (DP-11).
- The immutability period is never shortened without the audit owner's approval, and an overwrite is never allowed as a convenience.
- The gate database is a private test database migrated from empty; no SIT, UAT or PROD data is read or copied into it.
- No `rwb_*` table, topic, queue or Schedule is created here; a change that needs one belongs to its own story.

### 18. Traceability

| Requirement ID | Requirement (short) | Infrastructure element | Test cases |
|---|---|---|---|
| REQ-CWC-013 | Rule change by validated load with a version and rollback by one call | The immutable workbook store and the checksum metadata that make a version provable | TC-P3-E2042-INF-01, TC-P3-E2042-INF-02 |
| REQ-CWC-014 | Schema, overlap, unreachable, default and scenario checks before a rule takes effect | The isolated gate database and the private container the gate reads | TC-P3-E2042-INF-02, TC-P3-E2042-INF-06 |
| ADR-017 | Embedded Drools per service; rule registry in rwb-decision | The identity and certificate for the rwb-decision call, and the memory for 20 KieBases | TC-P3-E2042-INF-03, TC-P3-E2042-INF-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The one-hop egress allow list | TC-P3-E2042-INF-05 |
| D-RCV-36 T10 | `payment_match_rule` is retired | The gate assertion on the isolated database | TC-P3-E2042-INF-06 |

### 19. Out of scope

- The cache, the swap, the catalog client and the model verification code (RWB-P3-E2042-APP).
- The authoring, consumption and activity contract as a document (RWB-P3-E2042-CON).
- The Helm values, the consumer group, the readiness signal, the dashboards, the alerts and the runbook (RWB-P3-E2042-OPS).
- The registry, the three seed rows, the admin operations and JOB-20 (RWB-P7-E2042-APP; ASM-0069).
- The storage account, the Key Vault, the certificate authority, the service mesh and the schema registry as platform products (RWB-PLT-LIB, RWB-PLT-EVT, RWB-PLT-N008-INF).
- The `rwb_case` schema design, its tables and its migrations (the database stories of the service epic).
- The retention period, the heap values, the ports and the certificate subject, which are reviewed values and Not specified in the source documents (GAP-0723; ASM-1270).
