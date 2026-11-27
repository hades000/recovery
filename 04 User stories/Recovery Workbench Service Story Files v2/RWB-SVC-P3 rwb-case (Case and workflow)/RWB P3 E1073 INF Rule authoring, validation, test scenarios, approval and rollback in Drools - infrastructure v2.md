# RWB-P3-E1073-INF Rule authoring, validation, test scenarios, approval and rollback in Drools

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1073-INF |
| Work type | INF (Infrastructure) |
| Suggested owner | SCB IT infrastructure (suggested; any team may pick up this story) |
| Capability owner | P7 rwb-decision owns the registry and its endpoints; PLT owns the embedded kit |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-073 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P3-E1073-INF-16) |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-W |
| Ready to start | Day 1 |
| Depends on (build) | None; platform contracts RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-PLT-E1071-CON |
| Contract dependencies | RWB-P3-E1073-CON; RWB-P3-E1042-CON (DP-06); RWB-P3-E1043-CON (DP-07) |
| Contract version | v1 (the /v1 path) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-009, FR-P3-011, FR-P3-027, FR-P3-028, FR-P3-029) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-073 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (8 resolved, 33 cross-document, 5 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **infrastructure engineer**, I want **the embedded Drools kit of rwb-case deployed on a pinned base image and a pinned toolkit, with the JVM heap and the resource limits that hold the KieBase cache without an out-of-memory restart, one one-hop network path and a certificate from Key Vault to rwb-decision, one workload identity with no secret in code or chart, a readiness signal that a model is in force, and an image-scan policy that blocks a critical finding**, so that **the service can evaluate an approved package version on any pod at any time, a refused or missing model is visible before a case reaches it, and no credential, no workbook and no registry row is carried by the deployment**.

This story deploys the engine and its plumbing only. It creates no `rwb_*` table, no topic, no queue, no Schedule and no business value; the fact mapping, the pin and the scenario gate are RWB-P3-E1073-APP, and the seam they build against is RWB-P3-E1073-CON. The workbook container, its immutability policy and the identity that reads it are the Epic 2 deployment story of the same service (RWB-P3-E2042-INF) and are out of scope here.

### 2. Business rationale

Rule governance is central in rwb-decision and evaluation is local in the service that owns the decision (Arch v5 slide 27; Temporal and Drools design slides 15 and 16; ADR-017; DP-04). That split is only real if the local engine is deployed to a known shape: a base image and a toolkit version that compile the same DRL the same way, memory that holds the KieBase cache so no evaluation compiles a table on the hot path, one identity and one certificate so the model can be fetched at all, and a readiness signal so an operator sees a pod that holds no model in force before a case reaches it.

Without the pinned image and toolkit, a runner upgrade can change the DRL that a workbook compiles to, and a checksum that verified yesterday proves nothing today. Without the heap, the cache of 20 versions thrashes or the pod is killed under load, and a killed pod during a swap is exactly the case the last-good-model rule exists for. Without the identity and certificate, the model cannot be fetched. Without the readiness signal, a pod that holds no model fails a case at the moment of the decision instead of at the moment of the deployment.

The measure is that a pod starts, reports readiness only with a model in force for each package code it serves, evaluates under load without a restart, and reaches rwb-decision on one hop with a certificate read from Key Vault.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB), with the platform workload identity mechanism of DP-02, so no credential sits in a file, a chart or a repository.
- The platform Key Vault, the platform certificate authority and the service mesh are available (RWB-PLT-LIB), and rwb-decision is reachable through the mesh with mTLS.
- RWB-PLT-E1072-CON is published: the embedded Drools kit declares the KIE libraries only — `drools-engine`, `drools-mvel`, `drools-decisiontables` and `drools-xml-support` — with no KIE Server, no Business Central and no KJAR, and the cache bound of 20 versions with the atomic swap and the checksum check (DP-04; TSD P3 v3 T2.2).
- RWB-PLT-E1071-CON is published: the Temporal workflow kit, the namespace `rwb-recovery` and the task queue `rwb-case` (DP-10).
- RWB-PLT-E1044-CON and RWB-PLT-E1047-CON are published: the per-service Flyway sequence and the naming library (DP-15, DP-14).
- RWB-P3-E1073-CON is published: the seven consumed operations, the readiness element and the message set this deployment reports against.
- The package codes the pod serves are the five of the case side: ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT and TRANSFER. The version labels are rwb-decision rows and are read at run time, never written into a chart.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Pin the base image by digest and the toolkit by version: the platform Java runtime image plus the four KIE libraries, with no KIE Server, no Business Central and no KJAR in the artifact list.
2. Set the JVM heap request and limit for the KieBase cache and the working set of the service, as reviewed values per environment, and record them in the sizing file.
3. Set the container resource requests and limits for the pods, with no privileged container, a read-only root filesystem and the log target outside the image.
4. Create the rwb-case workload identity and grant it only what it needs: the database login of its own schema, the Key Vault read of its certificate and secret reference, and the call to rwb-decision.
5. Provision the Key Vault entry for the mTLS client certificate and its secret reference to the rwb-decision front end, and prove the handshake with an issued, an expired and an unissued certificate.
6. Open one egress path from the rwb-case pods to rwb-decision and to the platform services the kit needs, record the allowed destinations as a reviewed list, and drop and count anything else.
7. Wire the image-scan policy: the pipeline blocks a release on a critical finding in the base image or in a KIE library, and the patch cadence for the base image is recorded.
8. Publish the readiness signal: for each package code it serves, the pod reports whether a version is in force and which version label it holds, with no personal data and no case data.
9. Add the startup probe and the liveness probe on that signal and the evaluation path, and record the timings as reviewed values.
10. Hand the sizing, the destination list, the readiness signal and the scan policy to RWB-P3-E1073-CON and to the operations surface of the service.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A release carries a KIE Server, Business Central or a KJAR, or an unpinned base image | The pipeline refuses the release before the artefact is published | None | AC1 |
| X2 | A critical finding appears in the base image or in a KIE library | The image-scan gate blocks the release; the finding, the image and the library are named to the platform administrator | None | AC1, AC6 |
| X3 | The heap or the limit is below what the cache needs | The load test shows an out-of-memory restart or an eviction of a version in force; the sizing is reviewed and the release is blocked | None | AC2 |
| X4 | The certificate is missing, expired or not issued by the platform certificate authority | The handshake with rwb-decision fails; the readiness signal reports no model in force and the condition is alerted; the model already held stays in use | None | AC3 |
| X5 | A secret, a key or a certificate body appears in a chart value, a log or a dashboard | The provisioning check fails the environment; the value is removed and rotated | None | AC3, AC4 |
| X6 | A call is made to a destination outside the reviewed list | The network policy drops the call; the attempt is counted and alerted | None | AC3 |
| X7 | The pod reports ready while no version is in force for a package code it serves | The readiness check fails; the pod is taken out of service until a version is in force or the package code is removed from the served list | None | AC5 |
| X8 | The readiness signal carries a case fact, a user ID or any personal data | The review fails the release; the signal carries package codes, version labels and states only | None | AC5 |
| X9 | The container runs privileged, or the root filesystem is writable | The provisioning check fails the environment | None | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Provisions the image, the toolkit, the heap, the limits, the identity, the certificate, the path, the readiness signal and the scan policy; no application code is built here |
| Negotiable | The heap, the ports, the probe timings and the certificate subject are environment values settled with the platform team, not story decisions |
| Valuable | Makes the local evaluation possible at all and lets an operator see a pod without a model in force before a case reaches it |
| Estimable | One pinned image and toolkit, one sizing decision, one identity, one certificate entry, one destination list, one readiness signal and one scan policy |
| Small | Fits one sprint with the provisioning checks |
| Testable | Every criterion tests an artefact: an image manifest, a load test, a handshake, a dropped call, a readiness answer and a blocked release |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the embedded Drools kit for rwb-case

  Background:
    Given the platform base image, Key Vault, certificate authority and service mesh are in force
    Given the four KIE libraries are drools-engine, drools-mvel, drools-decisiontables and drools-xml-support

  Scenario: AC1 The base image and the toolkit are pinned (new, D-RCV-60)
    Given the image manifest of the rwb-case deployment
    When the image and the artifact list are inspected
    Then the base image is pinned by digest and the toolkit by version, and neither is a floating tag
    Then the artifact list holds the four KIE libraries and no KIE Server, no Business Central and no KJAR
    Then a release that adds a KIE Server, Business Central or a KJAR, or that floats the base image, is refused before publication
    Then the Java runtime and the Spring Boot versions come from the platform baseline and are not chosen by this story

  Scenario: AC2 The KieBase cache sizing and the JVM heap are reviewed values (new, D-RCV-60)
    Given the sizing file of the environment
    When a load test holds the cache bound of 20 package versions and evaluates under load
    Then no out-of-memory restart occurs and no eviction touches a version in force
    Then the heap request, the heap limit and the cache bound are values of the environment and appear in no chart constant and no code
    Then a sizing below the load-test result fails the provisioning check and blocks the release
    Then the heap figure itself is Not specified in the source documents (GAP-0701; ASM-1248)

  Scenario: AC3 The path and the certificate to rwb-decision are one hop (new, D-RCV-60)
    Given the network policy and the Key Vault entries of the environment
    When the allowed destinations and the certificate are inspected
    Then rwb-decision is allowed on the reviewed port, one hop, and the platform services the kit needs are allowed and nothing else
    Then the client certificate and its secret reference are read from Key Vault by the workload identity and never from a file or a chart value
    Then the handshake succeeds only with a certificate the platform certificate authority issued and fails when it is expired or unissued
    Then no secret, no key and no certificate body appears in a values file, a log or a dashboard, and a rotation needs no rebuild

  Scenario: AC4 The workload identity of DP-02 carries no secret in code (new, D-RCV-60)
    Given the rwb-case workload identity and its grants
    When the identity is inspected
    Then it holds the database login of schema rwb_case only, the Key Vault read of its own entries and the call to rwb-decision
    Then it holds no static credential, no long-lived token and no certificate in the repository, the chart or the environment file
    Then no other service's identity holds a grant of this service, and this identity holds no grant on another service's schema
    Then the provisioning check fails the environment when any of the three conditions is not met

  Scenario: AC5 Readiness reports whether a model is in force (new, D-RCV-60)
    Given a pod of rwb-case with the package codes it serves
    When the readiness endpoint is read
    Then it reports, for each package code it serves, whether a version is in force and which version label is held
    Then the pod is not ready while a package code it serves has no version in force
    Then the signal carries package codes, version labels and states only, with no case fact, no user ID and no personal data
    Then the signal is the element RWB-P3-E1073-CON declares and the probes read it, with the probe timings as reviewed values

  Scenario: AC6 The resource limits and the image-scan policy are fixed (new, D-RCV-60)
    Given the deployment of the environment
    When the pod specification and the pipeline gate are inspected
    Then the CPU and memory requests and limits are reviewed values per environment and appear in no chart constant
    Then the container is not privileged, the root filesystem is read-only and the log target is outside the image
    Then the image-scan gate blocks a release on a critical finding in the base image or in a KIE library and names the finding
    Then the base-image patch cadence is recorded, and the operational values themselves are Not specified in the source documents (GAP-0702; ASM-1249)
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The base image is pinned by digest and the toolkit by version; a floating tag or an added KIE Server, Business Central or KJAR fails the release | TSD P3 v3 T2.2 (KIE libraries only); DP-04 |
| BR2 | The pod is sized to hold the KieBase cache of at most 20 versions plus the working set, and the figure is a reviewed value per environment, never a template constant | Arch v5 slide 27; Temporal and Drools design slide 16; DP-04 |
| BR3 | Every secret and every certificate comes from Key Vault through the workload identity; none appears in a file, a chart, a log or a dashboard | Template and Rules §R7.2 s17; DP-02 |
| BR4 | One login per service: the identity of rwb-case holds no grant on another service's schema and no other identity holds a grant on `rwb_case` | DP-02; Template and Rules §R5.5 |
| BR5 | The service reaches rwb-decision one hop on the reviewed port and nothing outside the reviewed destination list | DP-11; ADR-020 |
| BR6 | The readiness signal reports, per package code served, whether a version is in force and which version label is held, and carries no case data and no personal data | RWB-P3-E1073-CON 12.5; R-UNI-38 |
| BR7 | The container is not privileged, the root filesystem is read-only and the log target is outside the image | Security baseline of the platform; Template and Rules §R7.2 s17 |
| BR8 | The image-scan gate blocks a release on a critical finding in the base image or in a KIE library | Platform pipeline baseline; Template and Rules §R5 |
| BR9 | This story creates no `rwb_*` table, no topic, no queue and no Schedule; the engine, its memory, its identity and its signal are the whole deliverable | Template and Rules §R7.2 s12 |
| BR10 | No business value is fixed here: rows, scenarios, tolerances, action text, owner roles, timers and queue codes stay in the workbooks and the registry, and every threshold of this story is a reviewed value | Template and Rules §R7.2 s17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not provisioned | Identity and Key Vault entries created | The grants, the certificate and the secret reference are in place | Provisioned |
| Provisioned | First pod starts | A version is in force for every package code served | Ready |
| Provisioned | First pod starts | A package code served has no version in force | Not ready; the condition is alerted |
| Ready | The certificate expires or is reissued | The Key Vault entry is updated and the identity reloads it | Ready (new certificate) or Not ready while the handshake fails |
| Ready | A package version becomes in force | rwb-decision announces it and the evaluated copy is refreshed | Ready (new version label reported) |
| Ready | A policy check fails after a platform change | The grant, the destination list or the scan policy drifts | Degraded; the environment is not marked ready |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SCB IT infrastructure | Owns the image, the toolkit pin, the sizing, the resource limits, the identity grants, the Key Vault entries, the network policy, the readiness signal and the scan policy |
| ACE platform team | Owns the base image, the Key Vault, the certificate authority, the service mesh and the pipeline gate this story configures against |
| Security | Approves the identity grant, the secret references, the network allow list and the image-scan policy |
| The rwb-case owner team | Confirms the sizing after the load test and consumes the readiness signal |
| Platform administrator | Rotates the certificate, extends the Key Vault entries and acts on a blocked release |
| ACE database administrator | Confirms that the login is the service's own and holds no grant outside `rwb_case` |

The identity name, the Key Vault entry names, the certificate subject, the ports and the heap are Not specified in the source documents (GAP-0701; ASM-1248) (GAP-0702; ASM-1249); this story fixes their shape and leaves the values to the environment configuration.

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Image | The platform base image pinned by digest, with the four KIE libraries pinned by version | BR1 |
| Sizing | The heap request and limit, the cache bound of 20 versions, the evaluator thread pool and the working set, as reviewed values per environment | BR2 |
| Resource limits | The CPU and memory requests and limits of the container, as reviewed values per environment | Not specified in the source documents (DOR-RWB-P3-E1073-INF-7) |
| Identity | The rwb-case workload identity of DP-02, with the login of schema `rwb_case`, the Key Vault read of its own entries and the call to rwb-decision | BR4 |
| Key Vault entries | The mTLS client certificate for the rwb-decision front end and its secret reference | BR3 |
| Network list | rwb-decision one hop, the platform services the workflow kit needs, on the reviewed ports | BR5 |
| Readiness signal | Per package code served: whether a version is in force and which version label is held; no case data and no personal data | BR6 |
| Scan policy | The block on a critical finding in the base image or in a KIE library, and the base-image patch cadence | BR8 |

The heap, the ports, the probe timings, the certificate subject and the scan window are Not specified in the source documents (GAP-0701; ASM-1248) (GAP-0702; ASM-1249); they are reviewed values per environment and are recorded as assumptions, not as business values. The deployment holds no workbook, no case data and no rule row: the workbook container and its immutability policy belong to RWB-P3-E2042-INF. The storage of the evaluated copy of a package is Not specified in the source documents (GAP-0701).

### 12. Contract

#### 12.1 REST operations provided

None as a business operation. The readiness and liveness endpoints are cluster-internal probes on the element RWB-P3-E1073-CON declares; no workbench user calls them and no composite route publishes them.

#### 12.2 REST operations consumed

None as a business operation. The one-hop route to rwb-decision that this story opens carries the seven operations declared in RWB-P3-E1073-CON; this story adds no call of its own. It consumes the platform services of the workflow kit and the Key Vault and Blob endpoints of the platform, which are platform routes and not service contracts.

#### 12.3 Events published

None. The story provisions no topic and publishes no event.

#### 12.4 Events consumed

None. The `RulePackageInForce` consumer group, its inbox and its `.dlt` route are the app story's; this story only ensures the path carries the traffic and no message is read here.

#### 12.5 Workflows and activities

None. No Temporal workflow, activity or task queue is created by this story; the worker that polls task queue `rwb-case` is deployed by the service's own deployment, and the rule-evaluation element is RWB-P3-E1073-CON.

#### 12.6 Schedules

None. The 00:01 promotion is the Temporal Schedule JOB-20 in rwb-decision and this story registers no Schedule (Arch v5 slide 44; DP-10).

#### 12.7 Tables owned

None. This story creates no `rwb_*` table, no column and no index; the storage it touches is the Key Vault entry and the image registry, neither of which is an ACE DB table.

#### 12.8 Contract fakes

None. The fakes of the seam run in the pipeline and in SIT and belong to RWB-P3-E1073-CON and RWB-P3-E1073-APP; no fake is deployed or configured here.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | None | No operation is provided or consumed by this story; the route it opens carries the app story's seven calls |
| Kafka | None | No topic, no producer, no consumer |
| Temporal | None | No workflow, activity or task queue is created here |
| File | None | No file is exchanged; the image and the sizing file are deployment artefacts of the pipeline |

### 13. Solution plan

**Deliverables.** `infra/image/toolkit.yaml` (the pinned base image digest and the four KIE libraries with their versions), `infra/sizing/kiebase-cache.yaml` (the heap and the cache bound per environment), `infra/resources/limits.yaml` (the CPU and memory requests and limits, the read-only root filesystem and the privilege settings), `infra/identity/rwb-case-workload.json` (the identity of DP-02 and its grants), `infra/keyvault/entries.md` (the certificate and its secret reference), `infra/network/egress.yaml` (the one-hop allow list to rwb-decision and the platform services), `infra/readiness/model-in-force.md` (the readiness element and the probe timings) and `infra/scan/policy.yaml` (the scan gate and the patch cadence).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P3-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-04 is the pattern this story serves, and DP-02 is the login rule its identity satisfies: the local evaluated copy needs a pinned engine, memory to hold it, an identity to fetch it and a signal that says whether it is in force. No other pattern adds work here.

**Build steps**

1. Pin the base image by digest and the four KIE libraries by version, and add the manifest check that refuses a KIE Server, Business Central, a KJAR or a floating tag (AC1, X1).
2. Add the image-scan gate and the base-image patch cadence; test a blocked release on a critical finding (AC6, X2).
3. Run the load test that holds 20 package versions and evaluates under load; record the heap request and limit and the cache bound per environment (AC2, X3).
4. Set the resource requests and limits, the non-privileged container, the read-only root filesystem and the log target outside the image (AC6, X9).
5. Create the workload identity of DP-02 and its three grants; verify that a grant outside them is refused (AC4, X5).
6. Create the Key Vault certificate and secret reference; test the handshake with an issued, an expired and an unissued certificate, and a rotation without a rebuild (AC3, X4).
7. Write the one-hop egress list and the drop rule; test a call to an unlisted destination (AC3, X6).
8. Publish the readiness element and the two probes; test a pod with no version in force for a package code it serves (AC5, X7).
9. Hand the sizing, the destination list, the readiness element and the scan policy to RWB-P3-E1073-CON and to the operations surface of the service.

**Done when.** The image and the toolkit are pinned in all three environments, the load test holds the cache bound without an out-of-memory restart, the mTLS handshake succeeds with an issued certificate only, the identity holds no credential in a file or a chart, a pod with no model in force reports not ready, the egress list is one hop, and a release with a critical finding is blocked.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| None | A policy, identity, certificate or sizing check fails | No business message is produced. The provisioning check fails the environment or the release with the resource name and the violated rule, and the platform administrator acts on it. |

This story adds no message ID. The business messages of the capability keep their identifiers and texts from the legacy story and are carried by RWB-P3-E1073-CON: MSG-P3-027 (a rule version refused or no version in force), MSG-P3-015 (a rollback with no earlier version), MSG-P7-002 (the author cannot approve), MSG-GEN-001, MSG-GEN-003 and MSG-GEN-004 (the workbook and date checks) and MSG-P4-002 (a role without the right). The infrastructure reports a condition to the operator, never to a workbench user, and the readiness element carries a state and a version label, never a message text.

### 15. Screens and states

None. There is no screen in this story. The operator-facing surfaces are the environment's provisioning check, the image and scan report, the load-test report and the readiness answer; the dashboards, the alerts and the runbook are owned by the operations surface of the service, and the case record that shows the pinned version is RWB-P3-E1023-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E1073-INF-01 | AC1, BR1 | Component | The image manifest pinned by digest; a release adding a KIE Server, Business Central or a KJAR is refused |
| TC-P3-E1073-INF-02 | AC2, BR2 | NFR | A load test holding 20 package versions and evaluating under load; the heap values recorded per environment |
| TC-P3-E1073-INF-03 | AC3, BR3, BR5 | NFR | mTLS with an issued, an expired and an unissued certificate; the Key Vault read; a dropped call to an unlisted destination |
| TC-P3-E1073-INF-04 | AC4, BR4 | Component | The identity grants: the own schema login, the Key Vault read and the call to rwb-decision; a grant outside them is refused |
| TC-P3-E1073-INF-05 | AC5, BR6 | Component | A pod with a version in force for every package code served, and a pod with one package code without a version |
| TC-P3-E1073-INF-06 | AC6, BR7, BR8 | NFR | The resource limits per environment; a privileged container and a writable root filesystem fail; a critical finding blocks the release |

### 17. Guardrails

- No business value in a policy or a values file: rows, scenarios, tolerances, action text, owner roles, timers and queue codes stay in the workbooks and the registry; every threshold here is a reviewed value.
- No personal data in the image, a log, a dashboard, the readiness element or a probe: package codes, version labels and states only.
- One identity, three grants; no service writes through another service's login and no identity holds a grant outside its own schema (DP-02).
- No secret, key or certificate body in a file, a chart value, a dashboard or a log; everything comes from Key Vault through the workload identity.
- The service reaches rwb-decision and the platform services of the kit on the reviewed list and nothing else (DP-11, ADR-020).
- No `rwb_*` table, topic, queue or Schedule is created here; a change that needs one belongs to its own story.
- No workbook is stored, read or copied by the deployment: the workbook container is RWB-P3-E2042-INF's and the evaluated copy is in memory.
- A critical finding is never waived as a convenience; the patch cadence is recorded and the base image is re-pinned by digest on every patch.

### 18. Traceability

| Requirement ID | Requirement (short) | Infrastructure element | Test cases |
|---|---|---|---|
| REQ-CWC-013 | Validated load with a version, no release, rollback by one call | The pinned engine that compiles the approved workbook to the same DRL, and the path on which the model is fetched | TC-P3-E1073-INF-01, TC-P3-E1073-INF-03 |
| REQ-CWC-014 | Schema, overlap, unreachable, default, compile and scenario checks before a version takes effect | The pinned toolkit whose compile result the checks are proved against, and the readiness signal that shows a model in force | TC-P3-E1073-INF-01, TC-P3-E1073-INF-05 |
| REQ-DRI-004 | Epic 1 records use versioned rules | The readiness element that names the version label held, and the identity that fetches it | TC-P3-E1073-INF-04, TC-P3-E1073-INF-05 |
| REQ-CWC-008 | Allocation rules apply first match and always have a default | The same pinned engine and cache for the allocation package | TC-P3-E1073-INF-01, TC-P3-E1073-INF-02 |
| ADR-017 | Embedded Drools per service; rule registry in rwb-decision | The identity and certificate for the rwb-decision call, and the memory for the KieBase cache | TC-P3-E1073-INF-02, TC-P3-E1073-INF-03, TC-P3-E1073-INF-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The one-hop egress allow list to rwb-decision | TC-P3-E1073-INF-03 |

### 19. Out of scope

- The fact mapping, the version pin, the scenario gate and the consumed client (RWB-P3-E1073-APP).
- The consumed contract, the model and catalog elements and the message set as a document (RWB-P3-E1073-CON).
- The workbook container `rule-packages`, its immutability policy, the identity that reads it and the sizing of the Epic 2 package set (RWB-P3-E2042-INF).
- The registry, the five authoring operations as built and the promotion Schedule JOB-20 (RWB-P7-E1073-APP; ASM-0069).
- The workflow interface, the worker versioning and the replay gate (RWB-P3-E2043-CON, RWB-PLT-E2040-APP).
- The dashboards, the alerts, the consumer group and the runbook of the service.
- The base image, the Key Vault, the certificate authority, the service mesh and the pipeline gate as platform products (RWB-PLT-LIB, RWB-PLT-TPL, RWB-PLT-EVT).
- The `rwb_case` schema design, its tables and its migrations (the database stories of the service epic).
- The real cross-service proof of the fetch, the evaluation and the readiness signal (RWB-ITG-E1073-ITG).
- The heap, the ports, the probe timings, the certificate subject and the scan window, which are reviewed values and Not specified in the source documents (GAP-0701; ASM-1248) (GAP-0702; ASM-1249).
