# RWB-PLT-NF08-INF Temporal platform baseline

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-NF08-INF |
| Work type | INF (Infrastructure) |
| Suggested owner | SCB IT infrastructure (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-WF |
| Wave | 0 |
| Business epic | NF |
| Release | Window 1 |
| Legacy key | NF-08 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Patterns applied | None |
| Parallel lane | L-PLT-WF-C |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-PLT-NF08-INF-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-PLT-E1070-CON (contract version Not specified in the source documents (DOR-RWB-PLT-NF08-INF-23)) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: moved to its epic with content unchanged, legacy key NF-08. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (11 resolved, 9 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As the **platform team**, I want **the baseline standard for the shared Temporal layer held as one versioned baseline record — the pinned version baseline of 1.30 or later, one cluster per environment, a namespace per workbench, one task queue per service, the deterministic-workflow rule, Continue-As-New at stage ends and at least every 28 days, Worker Versioning with the replay gate, the AES-GCM payload codec, the 30-day closed-workflow retention with its archive, the metrics, UI and codec-server baseline, the availability and recovery objectives of the ACE platform, the compatibility matrix, and the conformance check that produces the evidence**, so that **every story that builds on the layer is measured against one standard instead of nineteen readings of it, and the bank can show conformance per environment and per release**.

This is the moved non-functional story of legacy key NF-08 under epic RWB-PLT-WF. NF-08 stated the standard of the shared Temporal layer as a non-functional requirement; it is moved to its epic with content unchanged (Template and Rules §R6, "No impact" rows), and what changes is where the standard lives and how it is evidenced: it becomes one versioned baseline record, and the conformance check that reads it and reports PASS, FAIL or WAIVED-with-evidence is part of this story. No business rule, no retention value, no version family and no objective is altered by the move.

The platform is shared platform, not one of the 19 services. Template and Rules §R4 has no platform row, so this story creates no schema of the form `rwb_<name>`, publishes no `rwb.<short>.events.v1` topic, owns no `/api/recovery/<short>/v1` base and invents no service short. The platform task queue is task queue `rwb-platform`, which the Ownership Map gives to JOB-22.

This story owns the standard and its conformance evidence, and nothing else. The boundary with the six stories that build on the layer is explicit:

- **RWB-PLT-E1070-APP and RWB-PLT-E1070-CON** install the cluster, its two persistence databases, the frontend, the Web UI, the mTLS front door and the namespace bootstrap job, and publish the certificate, API and role contract.
- **RWB-PLT-N003-INF** provisions and operates the namespace `rwb-recovery`, its codec key in Key Vault, its entitlements, its search attributes and its namespace-level evidence pack.
- **RWB-PLT-N010** builds the workflow kit, and **RWB-PLT-E1071** builds the worker, the SDK wiring and the codec inside the worker.
- **RWB-PLT-E2037** owns the dashboard, the alerts, the stuck-workflow scan and the run books; **RWB-PLT-E2038** owns the codec server, the decode path and the admin audit; **RWB-PLT-E2039** owns the backup, the failover, the upgrade and the archive of closed histories to Blob.
- This story owns the baseline record, its version, its approval, its conformance check and its evidence, and it refuses an environment that departs from the record.

The baseline parameters a moved non-functional story must carry are named by no read source beyond the version family of 1.30 or later and the ACE availability and recovery objectives: the exact supported version range, the full compatibility matrix, the upgrade cadence and window, the measurement window of the availability and recovery objectives, and the conformance cadence. They are carried as the working read of one assumption and remain placeholders where they are still open: Not specified in the source documents (GAP-1452; ASM-2547).

### 2. Business rationale

A standard that lives in a paragraph of a requirements document cannot be checked. From wave 1 the layer carries the case workflows of every service, and the four properties that make it safe to replay — deterministic workflow code, Continue-As-New, Worker Versioning with a replay gate, and an encrypted payload — are exactly the properties that quietly erode first: a database call added to a workflow passes a review and fails a replay six weeks later, and a payload written with the codec off passes a demonstration and fails an audit.

The baseline record answers three questions in one place. What version of the server, the SDK and the schema tool is the layer at, and which combinations are supported. What must be true of the code that runs on it — no I/O in workflow code, Continue-As-New at stage ends and at least every 28 days, workers pinned to a build, every build replaying recorded histories. And what must be true of the platform that holds it — one cluster per environment with its own persistence, a namespace per workbench with its own retention and keys, one task queue per service, 30-day retention with the archive behind it, the metrics, the UI and the codec server in place, and the availability and recovery objectives of ACE.

The conformance check is what turns the record into a control. A baseline that is only read is a document; a baseline read by a job that reports PASS, FAIL or WAIVED-with-evidence per environment and per release is something internal audit and the change board can act on, and a waiver with its evidence is the only way to depart from it. Because the layer is reused — the next workbench takes a namespace and the kit and writes only its own domain workflows (Architecture v5 slides 23 and 46) — the check is also the artefact the second workbench is onboarded against, which is why it is Wave 0 work and not a later hardening item.

### 3. Preconditions

- The five-layer design fixes the standard: L1 cluster one per environment on the ACE AKS clusters with its own persistence database, L2 namespace per workbench with its own retention, rate limits, certificates and keys, L3 versioned workflow kit, L4 activity contracts on `rwb-<service>`, L5 domain workflows (Architecture v5 slides 23 and 24; Temporal and Drools Design slides 11 and 12).
- The server and Java SDK release family is 1.30 or later, for Nexus and Worker Versioning (Temporal and Drools Design slide 32 item 6).
- The retention value is 30 days for a closed workflow, and the archive to Blob sits behind it (Temporal and Drools Design slide 27; RWB-PLT-E2039).
- The codec is AES-GCM with keys in Key Vault per namespace, on every client and every worker (Architecture v5 slides 8 and 24).
- The search attributes are CaseId, Stage, ProductGroup and QueueCode and nothing else (Temporal and Drools Design slide 27).
- The availability and recovery objectives are those of ACE: 99.9 percent in business hours and 99.5 percent outside them, with the recovery point and recovery time objectives following the ACE objectives, which are still open (Program BRD v4 §6.4, NFR-020, NFR-021, NFR-022, NFR-023).
- The conformance check reads the cluster, the namespace and the build pipeline; it needs the metrics and health endpoints of RWB-PLT-E1070-CON, the namespace record of RWB-PLT-N003-INF and the build evidence of the pipeline, and it builds nothing on them.
- The baseline record is the standard and not an environment: it names no replica count, no node size, no hostname and no credential, so it can be read in DEV and in PROD without change.
- No approval is required to start. The record is published at status Draft (realignment v1) and is approved at the platform review, not before.
- The exact supported version range, the compatibility matrix, the upgrade cadence and window, the measurement window of the objectives and the conformance cadence are Not specified in the source documents (GAP-1452; ASM-2547).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7), because it publishes a standard and a check and builds nothing on another story.

### 4. Flow

1. Draft the baseline record from the sources of section 13: the version baseline of 1.30 or later, the topology of one cluster per environment, a namespace per workbench and one task queue per service, the deterministic-workflow rule, Continue-As-New, Worker Versioning and the replay gate, the codec, the retention and archive, the metrics, UI and codec-server baseline, the objectives and the compatibility matrix.
2. Mark every value that a source fixes with that source, and every value that no source fixes with the placeholder, so that the record cannot be read as if it invented a number.
3. Hold the record under version control: one version, one approval, and a change that raises a new version and supersedes the old one instead of editing it in place.
4. Build the conformance check: it reads the cluster version and the schema tool version from the frontend, the namespace record from the namespace register, the retention and the attributes from the namespace, the codec configuration from the worker deployment and the build evidence from the pipeline, and it compares each one with the record.
5. Define the three results: PASS when every item matches, FAIL when an item differs and no waiver exists, WAIVED-with-evidence when a named item has a written waiver with its owner, its reason and its expiry.
6. Run the check against DEV and SIT and record the result per environment and per release; a FAIL blocks the release and a waiver is accepted only with its evidence.
7. Hand the record and the check to RWB-PLT-E1070, RWB-PLT-N003-INF, RWB-PLT-N010, RWB-PLT-E1071, RWB-PLT-E2037, RWB-PLT-E2038, RWB-PLT-E2039 and the 19 service teams, and publish the check as the onboarding test for the next workbench.
8. Walk the domain workflows of the first services through the check once they exist, so that the code rules — no clock, no random, no Drools, no network and no database in workflow code — are tested on real code and not only declared.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | An environment runs a version outside the supported range or an unsupported combination of server, SDK and schema tool | The check returns FAIL for that environment, the record names the combination that is supported, and the release is held | MSG-PLT-NF08-01 | AC1 |
| X2 | A workflow class performs a database call, reads the system clock, uses randomness, calls Drools or opens a network connection | The check returns FAIL at the code rule, and the replay gate of RWB-PLT-E2040 fails the build | MSG-PLT-NF08-02 | AC3 |
| X3 | A workflow run reaches its stage end, or 28 days, without Continue-As-New | The check returns FAIL on the history length rule and the owning service is named | MSG-PLT-NF08-03 | AC4 |
| X4 | A payload is written without the codec, or a namespace carries a fifth search attribute | The check returns FAIL on the payload or attribute rule, and the namespace is not signed off | MSG-PLT-NF08-04 | AC5 |
| X5 | An environment departs from the record with a written waiver | The result is WAIVED-with-evidence and names the owner, the reason and the expiry; without the evidence the result is FAIL | None (waiver record) | AC7 |
| X6 | An attempt is made to edit an approved value of the record in place | The change is refused and a new version is required | MSG-PLT-NF08-05 | AC7 |
| X7 | A conformance cadence or an upgrade window is needed and no source names it | The record carries the placeholder and the cadence stays open, so the check runs on the schedule of the release and not on an invented calendar | Not specified in the source documents (GAP-1452; ASM-2547) | AC8 |

The sources support the first statement of X2 without qualification: workflow code decides the order of steps only, and all I/O, the clock, randomness, Drools and the network belong to activities, because Temporal replays workflow code from history after every restart (Temporal and Drools Design slide 27). The replay gate that proves it is RWB-PLT-E2040's, not this story's.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes one versioned record and one conformance check; reads the cluster, the namespace and the pipeline and builds nothing on another story |
| Negotiable | The exact supported range, the compatibility matrix, the conformance cadence and the upgrade window are agreed at the platform review; the version family, the topology, the code rules, the retention and the objectives are fixed by the sources |
| Valuable | Gives one standard for the shared layer and one PASS, FAIL or WAIVED result per environment and per release, instead of nineteen readings |
| Estimable | One record, one compatibility matrix, one conformance check, one evidence format and seven acceptance criteria |
| Small | Fits one sprint with the record, the check and two runs |
| Testable | Every criterion is tested against the record, the live environment and the evidence, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Temporal platform baseline and its conformance check

  Background:
    Given the shared Temporal layer is the platform layer of the Recovery Workbench, owned once and reused by every workbench
    Given the platform is not one of the 19 services and owns no schema, no topic, no Workbench REST base and no service short

  Scenario: AC1 The baseline record is one versioned record with the pinned version baseline and the compatibility matrix (new, D-RCV-60)
    Given the baseline record of this story
    When it is read
    Then it declares the version baseline as Temporal 1.30 or later, for Nexus and Worker Versioning
    Then it declares the compatibility matrix of the server, the SDK and the schema tool, with the supported combinations and the ones it refuses
    Then every value carries the source that fixes it, or Not specified in the source documents (GAP-1452; ASM-2547) where no source does
    Then it names no replica count, no node size, no host name and no credential, so it is the same record in DEV, SIT, UAT and PROD
    When the record is changed
    Then a new version is raised, the previous one is superseded and no approved value is edited in place

  Scenario: AC2 The record fixes one cluster per environment, a namespace per workbench and one task queue per service (new, D-RCV-60)
    Given the topology section of the baseline record
    When an environment is checked against it
    Then it has one Temporal cluster with its own persistence database and no grant on the ACE database
    Then it has a namespace per workbench, with rwb-recovery among them, each carrying its own retention, rate limits, certificates and encryption keys
    Then every service polls only its own task queue named for that service, and the platform's own queue is task queue `rwb-platform`
    Then a namespace is not shared between two workbenches, and a second workbench adds a namespace rather than a cluster

  Scenario: AC3 Workflow code is deterministic: all I/O is in activities and no clock, randomness, Drools or network call appears in workflow code (new, D-RCV-60)
    Given the code rules in the baseline record
    When a workflow class that reads the system clock, uses randomness, calls Drools, opens a network connection or reads a database is checked
    Then the check returns FAIL and names the class and the rule it breaks
    When a workflow class that only decides order, waits on timers and signals, starts children and calls activities is checked
    Then the check returns PASS
    Then the record states that rule evaluation, record writing and every external call happen inside an activity, whose result is recorded in history

  Scenario: AC4 Continue-As-New, Worker Versioning and the replay gate are part of the baseline (new, D-RCV-60)
    Given the versioning section of the baseline record
    When a workflow type is checked
    Then Continue-As-New is required at every stage end and at least every 28 days
    Then a child workflow started for a stage uses parent close policy ABANDON so that it survives the parent's Continue-As-New
    Then every worker is pinned to a build under Worker Versioning, and every build replays recorded histories through the replay gate of RWB-PLT-E2040 before release
    When a run reaches its stage end or the 28-day bound without Continue-As-New
    Then the check returns FAIL and names the workflow type and the owning service

  Scenario: AC5 The payload codec, the search attributes and the 30-day retention with its archive are part of the baseline (new, D-RCV-60)
    Given the data section of the baseline record
    When an environment is checked
    Then every client and every worker runs the AES-GCM codec with keys in Key Vault per namespace, and a payload written without the codec fails the check
    Then the only search attributes are CaseId, Stage, ProductGroup and QueueCode, all Keyword, and a fifth attribute fails the check
    Then retention is 720 hours, 30 days, for closed workflows and the archive to Blob sits behind it
    Then a history that holds a clear personal value fails the check, and the owner of the writer is named

  Scenario: AC6 The metrics, UI and codec-server baseline and the ACE availability and recovery objectives are recorded (new, D-RCV-60)
    Given the operations section of the baseline record
    When it is read
    Then it records the metrics and health endpoints, their ports and their result codes, and the ACE monitoring namespace as the only scraper
    Then it records the Web UI behind Entra ID with RW-PLATADM operate, RW-AUDIT read and RW-SECADM decode under break-glass
    Then it records the codec server of RWB-PLT-E2038 as the only decode path
    Then it records the availability objective of 99.9 percent in business hours and 99.5 percent outside them, and the recovery point and recovery time objectives as the ACE objectives, which are open
    Then the measurement window and the exact objectives are Not specified in the source documents (GAP-1452; ASM-2547)

  Scenario: AC7 The conformance check produces PASS, FAIL or WAIVED-with-evidence per environment and per release, and the record is never edited in place (new, D-RCV-60)
    Given the conformance check and the baseline record
    When the check runs against DEV and SIT
    Then it reports one result per environment and per item, with the observed value and the declared value
    Then the result is PASS when every item matches, FAIL when an item differs and no waiver exists, and WAIVED-with-evidence when a written waiver names its owner, its reason and its expiry
    Then a FAIL blocks the release and a waiver without its evidence is reported as FAIL
    When an approved value of the record is edited in place
    Then the change is refused and a new version is required
    Then the evidence is stored with the release and carries no payload, no personal value and no credential

  Scenario: AC8 A conformance cadence or an upgrade window that no source names carries the placeholder and the check runs on the release schedule (new, D-RCV-60)
    Given the cadence and upgrade window of the baseline record
    When no source names a conformance cadence or an upgrade window
    Then the record carries Not specified in the source documents (GAP-1452; ASM-2547) for that value
    Then the check runs on the schedule of the release and no calendar is invented
```

These eight criteria are new and test only the deliverable in the title: the baseline record, its topology section, its code rules, its versioning rules, its data rules, its operations section and its conformance evidence. No legacy acceptance criterion is repeated here and no business value is asserted.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The baseline is one versioned record: a change raises a new version and supersedes the previous one, and an approved value is never edited in place | Template and Rules §R8.2; Architecture v5 slides 23 and 36 | AC1 |
| BR2 | The version baseline is Temporal 1.30 or later, for Nexus and Worker Versioning, with the server, SDK and schema tool held as one compatibility matrix | Temporal and Drools Design slide 32 item 6; Architecture v5 slide 23 | AC1 |
| BR3 | One cluster per environment with its own persistence database and no grant on the ACE database; a namespace per workbench with its own retention, rate limits, certificates and encryption keys; one task queue per service | Architecture v5 slides 23 and 24; Temporal and Drools Design slides 11 and 12 | AC2 |
| BR4 | Workflow code is deterministic: it decides order only, all I/O is in activities, and no clock, randomness, Drools call, network call or database read appears in workflow code | Temporal and Drools Design slide 27; Architecture v5 slide 23 | AC3 |
| BR5 | Continue-As-New at every stage end and at least every 28 days, with a child workflow per stage under parent close policy ABANDON, so a run stays far below the history limits | Temporal and Drools Design slide 13; Architecture v5 slide 23 | AC4 |
| BR6 | Workers are pinned to a build under Worker Versioning, and every build replays recorded histories through the replay gate before release | Temporal and Drools Design slides 27 and 32; RWB-PLT-E2040 | AC4 |
| BR7 | Every payload is encrypted with the AES-GCM codec and a key in Key Vault per namespace; the search attributes are CaseId, Stage, ProductGroup and QueueCode only; a closed workflow is retained 30 days and archived to Blob | Temporal and Drools Design slide 27; Architecture v5 slides 8 and 24 | AC5 |
| BR8 | The availability and recovery objectives are the ACE objectives, 99.9 percent in business hours and 99.5 percent outside them, with the recovery point and recovery time objectives open under the ACE objectives | Program BRD v4 §6.4, NFR-020 to NFR-023 | AC6 |
| BR9 | The record is a standard and not an environment: it names no replica count, node size, host name, credential or business value, and a value that no source fixes carries the placeholder | Template and Rules §R7.2 s17 and §R9 | AC1 |

### 9. State transitions

No case status changes in this story: it publishes a standard and reports conformance, and it moves no workflow. What the story does have is a baseline-record lifecycle and a conformance lifecycle, described here so that the tests of AC1 and AC7 have something to assert.

| Object | From | Event | Condition | To |
|---|---|---|---|---|
| Baseline record | Absent | The first version is written from the sources of section 13 | Every value carries its source or the placeholder | DRAFT |
| Baseline record | DRAFT | The platform review accepts the record | The version family, the topology, the code rules, the data rules and the objectives are agreed | APPROVED |
| Baseline record | APPROVED | A value changes | The change is accepted and a new version is written | A new version, and the previous one is SUPERSEDED |
| Baseline record | SUPERSEDED | The new version is approved and every consumer pins it | No consumer remains on the previous version | Read-only, kept for the audit trail |
| Conformance | Absent | The check runs against an environment and a release | The environment answers all of its reads | PASS, FAIL or WAIVED-with-evidence |
| Conformance | FAIL | The item is corrected and the check reruns | The observed value matches the declared value | PASS |
| Conformance | FAIL | A written waiver is accepted | The waiver names its owner, its reason and its expiry | WAIVED-with-evidence |
| Conformance | WAIVED-with-evidence | The waiver expires | The item still differs | FAIL |

The transition owner is SCB IT infrastructure for the record and the platform review for its approval; the conformance transition owner is the release manager. The conformance cadence, the waiver expiry rule and the upgrade cadence are Not specified in the source documents (GAP-1452; ASM-2547).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SCB IT infrastructure | Owns this story, the baseline record, the conformance check and the evidence |
| ACE platform team | Owns the cluster, its persistence and the environments the check reads; approves a change to the topology section |
| Security architecture | Approves the codec rule, the search-attribute set, the retention and the decode path in the record |
| Key Vault owner | Confirms the key-per-namespace rule and that no key material appears in the record |
| Internal audit | Reads the record and the conformance evidence, and requires a waiver to carry its reason and its expiry |
| Platform on-call rota | Runs the check when an environment is suspected of departing from the record, and reports the result |
| Release manager | Accepts the conformance result per release, holds a release on a FAIL and registers a waiver |
| RWB-PLT-E1070, RWB-PLT-N003-INF owners | Supply the cluster, the namespace and the certificate facts the check reads; they never change a declared value |
| RWB-PLT-N010, RWB-PLT-E1071, RWB-PLT-E2037, RWB-PLT-E2038, RWB-PLT-E2039 owners | Supply the kit, worker, observability, codec-server and archive facts the check reads; they raise a change to the record rather than depart from it |

The exact supported version range, the full compatibility matrix, the upgrade cadence and window, the measurement window of the availability and recovery objectives and the conformance cadence are Not specified in the source documents (GAP-1452; ASM-2547). The remaining values are agreed at the platform infrastructure review before wave 0 exit, and section 13 carries the assumption in force until then.

### 11. Data

| Item | Value | BR Field ID |
|---|---|---|
| Sessions | None. The layer holds no session; a staff session belongs to the edge store of RWB-PLT-N006-INF | None |
| Baseline record | The version, its status, the version baseline, the compatibility matrix, the topology, the code rules, the versioning rules, the data rules, the operations baseline and the objectives, each with its source or the placeholder | BR1, BR9 |
| Conformance evidence | One result per environment and per item, the observed value, the declared value, the run time, the release it belongs to and, where applicable, the waiver with its owner, reason and expiry | BR9 |
| Business data | None. No case, customer, account, document, decision, payment or partner value is held by the record, the check or the evidence | BR9 |
| Personal data | None. The evidence names roles, services, environments and versions; no name, email address, account number, national identifier or contact detail appears | BR9 |
| Workflow histories | Not held by this story. The histories live in the namespace and are protected by the codec and the 30-day retention; this story declares the rule and checks it | BR7 |
| Field identifiers | None owned. No DF-REF, DF-CAS or DF-DEC field is added or changed, and the Physical Schema is not changed | None |
| Retention | The record and its evidence are kept for the audit period the bank sets; a superseded version is kept read-only, because the standard that applied at a release must remain readable | BR1 |
| Access | SCB IT infrastructure and the platform review write the record; every team reads it; the evidence is read by internal audit, the release manager and the platform rota | BR1, BR9 |

The record holds no field that a source does not define. Where a baseline parameter is named by no source — the exact supported range, the full matrix, the cadence and the measurement window — the record carries the placeholder and the value waits for the gap to close; no number is invented to fill it.

### 12. Contract

#### 12.1 REST operations provided

None. The platform has no service short (Template and Rules §R4 has no platform row), so it publishes no path under `/api/recovery/<short>/v1` and no Workbench endpoint. The record is published into the platform document set and the check runs from the pipeline; neither is a Workbench route.

#### 12.2 REST operations consumed

None. The check reads the frontend, the namespace register, the worker configuration and the pipeline through the platform's own tooling and the metrics and health endpoints of RWB-PLT-E1070-CON; it consumes no Workbench REST operation.

#### 12.3 Events published

None. The baseline publishes no `rwb.<short>.events.v1` topic and no event schema; the platform owns no topic, and a conformance result is evidence and not a business fact (DP-14 declared as an absence).

#### 12.4 Events consumed

None. The check reacts to a release and to a run of the pipeline, not to a Kafka event.

#### 12.5 Workflows and activities

None owned. The conformance check is a pipeline job and not a business workflow: it reads state and writes a report, so it never runs as a Temporal workflow and never starts one. The 19 services' workers poll only their own task queue `rwb-<service>` in the namespace `rwb-recovery`; the platform task queue `rwb-platform` carries the platform's own runs and belongs to RWB-PLT-E1071.

#### 12.6 Schedules

None owned. A monthly conformance run is a candidate platform Schedule on task queue `rwb-platform`, and its cadence is a placeholder until the platform review sets it: Not specified in the source documents (GAP-1452; ASM-2547). No Schedule is created by this story, and the archive and stuck-workflow runs belong to RWB-PLT-E2039 and RWB-PLT-E2037.

#### 12.7 Tables owned

None. The baseline record and its evidence are documents in the platform document set and not tables; the platform owns no `rwb_<name>` schema and no table in the ACE database. The row reads None for both platform stories.

#### 12.8 Contract fakes

None. The record has no service contract to fake. The check is exercised against a throwaway environment, the platform fake frontend of RWB-PLT-E1070-CON and a synthetic build, so a PASS, a FAIL and a WAIVED result are each produced before the check runs on a real environment.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 0 | No HTTP surface; the platform has no service short and no `/api/recovery` base |
| Kafka | 0 | 0 | The baseline owns no topic and consumes none |
| Temporal | The standard of the layer: the version baseline, the topology, the code rules, the versioning and replay rules, the codec, the retention and the objectives | 0 workflows and 0 activities of its own | The standard is applied by the cluster, the namespace and the workers; the platform task queue `rwb-platform` is not created here |
| File | 0 | 0 | The record and the evidence are documents; no file is exchanged with a service |
| Platform | 1 (the versioned baseline record and its conformance evidence) | None | One record, one compatibility matrix, one check, one evidence set per environment and release |

The summary is five lines and not four because the baseline record itself is the call type of this story: a platform artefact with no business surface and no business data.

### 13. Solution plan

**Deliverables.** The baseline record with its version and status, the compatibility matrix, the topology section, the code rules, the versioning and replay rules, the data rules, the operations baseline and the objectives; the conformance check with its three results; the evidence format and its storage; the waiver record; and the onboarding note for the next workbench.

**Settings in force**

| Setting | Value |
|---|---|
| Version baseline | Temporal 1.30 or later, for Nexus and Worker Versioning (Temporal and Drools Design slide 32 item 6) |
| Compatibility matrix | Server, SDK and schema tool per release; the exact supported combinations and the refused ones are Not specified in the source documents (GAP-1452; ASM-2547) |
| Topology | One cluster per environment with its own persistence database and no grant on the ACE database; a namespace per workbench; one task queue per service named for that service (Architecture v5 slides 23 and 24) |
| Namespace | `rwb-recovery` for this workbench, with its own retention, rate limits, certificates and keys (Template and Rules §R4; Architecture v5 slide 23) |
| Platform task queue | Task queue `rwb-platform` (Ownership Map, JOB-22; RWB-PLT-E1070-APP) |
| Retention | 720 hours, 30 days, for a closed workflow (Temporal and Drools Design slide 27) |
| Archive | A closed history is archived to Blob before retention removes it; the container and its immutability belong to RWB-PLT-E2039 |
| Continue-As-New | At every stage end and at least every 28 days; a stage child uses parent close policy ABANDON (Temporal and Drools Design slide 13) |
| Deterministic-workflow rule | All I/O in activities; no system clock, no randomness, no Drools call, no network call and no database read in workflow code (Temporal and Drools Design slide 27) |
| Versioning | Workers pinned to a build under Worker Versioning, plus `getVersion` for an in-place change, plus the replay gate of RWB-PLT-E2040 on every build (Temporal and Drools Design slide 27) |
| Payload codec | AES-GCM with a key in Key Vault per namespace, on every client and every worker (Architecture v5 slides 8 and 24) |
| Search attributes | CaseId, Stage, ProductGroup, QueueCode, all Keyword; no fifth attribute (Temporal and Drools Design slide 27) |
| Metrics and health baseline | HTTPS GET /metrics on port 9090 and HTTP GET /health on port 8080 answering 200 or 503, scraped only from the ACE monitoring namespace (RWB-PLT-E1070-CON) |
| UI baseline | The Temporal Web UI behind Entra ID: RW-PLATADM operate, RW-AUDIT read, RW-SECADM decode under break-glass (Temporal and Drools Design slide 11) |
| Codec-server baseline | The codec server of RWB-PLT-E2038 is the only decode path; no other decode surface is allowed (RWB-PLT-E2038) |
| Availability objective | 99.9 percent in business hours and 99.5 percent outside them, excluding the change window (NFR-020, NFR-021) |
| Recovery objectives | The ACE recovery point and recovery time objectives, which are open (NFR-022, NFR-023); this story records them and does not invent a target |
| Measurement window | Not specified in the source documents (GAP-1452; ASM-2547) |
| Upgrade cadence and window | Not specified in the source documents (GAP-1452; ASM-2547); the upgrade itself runs in the platform maintenance window outside business hours |
| Conformance cadence | Not specified in the source documents (GAP-1452; ASM-2547); the working read is one run per release and one run per environment |
| Waiver | A named item, an owner, a reason and an expiry; without the evidence the result is FAIL |

**Pattern application.** None of the decoupling-pattern markers of Template and Rules §R5.5 appears in this moved non-functional story: it introduces no legacy table, no legacy login, no legacy topic name, no legacy task queue and no legacy API base, so no DP row is applied and the metadata row "Patterns applied" reads None. The two patterns the baseline governs are applied by the platform stories that use these resources: DP-02 (one login per service) is applied by the service DB stories whose schemas the baseline never touches, and DP-13 (`/api/recovery/<short>/v1`) is applied by the 19 service contract stories, because the platform publishes no path of its own. DP-01, DP-14 and DP-15 are declared as absences in the topology and data rules: no schema, no topic, no migration.

**Build steps**

1. Write the record in its sections, with the source of every value and the placeholder where none exists; keep the version family, the topology, the code rules, the retention, the attributes and the objectives exactly as the sources state them.
2. Write the compatibility matrix: the supported server, SDK and schema tool combinations, the refused ones and the reason for each refusal; mark the exact range as the placeholder until the platform review.
3. Write the topology and data rules: one cluster per environment, a namespace per workbench, one queue per service, the codec, the attributes and the 30-day retention with the archive behind it.
4. Write the operations baseline: the metrics and health endpoints, the UI roles, the codec server as the only decode path, and the availability and recovery objectives with their sources and their open status.
5. Build the conformance check: one read per declared item, the observed and declared values in the report, and the three results with the waiver rule.
6. Run the check against DEV and SIT, record PASS or FAIL per item, and produce a WAIVED-with-evidence case once to prove the waiver path.
7. Publish the record and the check to the seven consumer stories and the 19 service teams, and add the check to the release evidence.
8. Use the check as the onboarding test for the next workbench: a namespace, the kit and the same conformance result.

**Done when.** The record is published as one version with its status, every value carries its source or the placeholder, the compatibility matrix is written, the check runs against DEV and SIT and reports per item, a PASS, a FAIL and a WAIVED-with-evidence result have each been produced once, the evidence is stored with the release, and the seven consumer stories read the same record.

### 14. Validation and messages

| ID | When | Message | Raised to |
|---|---|---|---|
| MSG-PLT-NF08-01 | An environment runs a combination outside the compatibility matrix | Environment {environment} runs {server} with {sdk} and {schemaTool}; the baseline supports {supported}. The release is held. | Release manager and SCB IT infrastructure |
| MSG-PLT-NF08-02 | Workflow code performs I/O or a non-deterministic call | {className} breaks the deterministic-workflow rule at {rule}. Move the call into an activity. | The owning service team and the platform team |
| MSG-PLT-NF08-03 | A run reaches its stage end or 28 days without Continue-As-New | Workflow {workflowType} reached {events} events without Continue-As-New. The baseline requires it at every stage end and at least every 28 days. | The owning service team and the platform team |
| MSG-PLT-NF08-04 | A payload is written without the codec, or a fifth search attribute is registered | The namespace {namespace} holds {finding}. The baseline allows the AES-GCM codec and four Keyword attributes only. | Security architecture and the platform team |
| MSG-PLT-NF08-05 | An approved value of the record is edited in place, or a waiver carries no evidence | The baseline record {version} refused the change: {reason}. Raise a new version, or attach the waiver evidence. | SCB IT infrastructure and internal audit |

The five message IDs belong to this story; they are operator and platform messages and not business messages, and none of them carries a payload, a user identifier or a personal value.

### 15. Screens and states

No Workbench screen in this story and no screen state either. The operational surfaces are the record itself, which is read as a document with the states of section 9, the conformance report, which is read per environment and per release, and the Temporal Web UI of RWB-PLT-E1070, which is an operational console behind Entra ID and not a Workbench screen. No screen is composed by gateway-bff for the platform, and this story adds no route to the edge.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-NF08-INF-01 | AC1 | Component | The record read against its sections: version baseline 1.30 or later, the compatibility matrix, a source or the placeholder on every value, no environment value, and a change that raises a new version instead of editing in place |
| TC-PLT-NF08-INF-02 | AC2 | Component | Two environments checked for one cluster each with its own persistence, a namespace per workbench including `rwb-recovery` with its own retention and keys, and workers polling only their own task queue; a second workbench sharing a namespace fails the check |
| TC-PLT-NF08-INF-03 | AC3 | Component | A workflow class that reads the clock, uses randomness, calls Drools, opens a network connection or reads a database fails the check with the class and the rule; a workflow class that only orders steps, waits and calls activities passes |
| TC-PLT-NF08-INF-04 | AC4 | Integration | A workflow type checked for Continue-As-New at a stage end and at 28 days, a stage child with parent close policy ABANDON, a worker pinned to a build and a build history replayed through the replay gate; a run without Continue-As-New fails |
| TC-PLT-NF08-INF-05 | AC5 | NFR | A namespace with codec-encrypted payloads, four Keyword attributes and 30-day retention with the archive behind it passes; a payload written without the codec, a fifth attribute and a clear personal value each fail the check |
| TC-PLT-NF08-INF-06 | AC6 | Component | The metrics and health endpoints on 9090 and 8080, the UI behind Entra ID with the three roles, the codec server as the only decode path, and the objectives 99.9 in business hours and 99.5 outside them, with the recovery objectives recorded as open |
| TC-PLT-NF08-INF-07 | AC7 | Integration | The check run against DEV and SIT with one result per item and the observed and declared values; a PASS, a FAIL and a WAIVED-with-evidence case produced once; a FAIL blocking the release; a waiver without evidence reported as FAIL; an in-place edit refused |

### 17. Guardrails

- No business value in configuration: the version family, the retention, the attributes and the objectives are platform settings with the sources of section 13, and none of them is a parameter of a business rule (BR9).
- No personal data in a payload, a history, a metric label, a report or a log line: the record and the evidence name services, roles, environments and versions only (BR7, AC5).
- Secrets only in Key Vault: the record names no key, no version identifier and no credential, and the codec rule points at Key Vault rather than at a value (BR7, AC6).
- Private access only: the check reads the frontend and the metrics endpoints inside the cluster network, and the Web UI is on its internal ingress behind Entra ID (BR3, AC6).
- No shared administrative credential: the check runs as its own identity and reads only; the UI maps three roles and refuses the rest.
- No cross-namespace read and no shared namespace: a namespace belongs to one workbench, and a second workbench adds a namespace rather than joining this one (BR3, AC2).
- A decode is break-glass only: the codec server of RWB-PLT-E2038 is the only decode path, and the check never decrypts a payload to test it — it inspects the codec metadata (AC5).
- The baseline is a versioned record and is never edited in place: a change raises a new version, supersedes the old one and leaves the standard that applied at a release readable (BR1, AC1, AC7).
- The check reads and never writes to the layer: it holds no grant on the namespace, the persistence or the key, except the read of the codec metadata and the namespace record.
- Every test environment is synthetic: no production history, payload or key is copied into DEV, SIT or a test (NFR-045).

### 18. Traceability

| Requirement ID | Requirement (short) | Source | What this story provides | Test cases |
|---|---|---|---|---|
| NFR-020 | The Workbench is available during business hours: 99.9 percent | Program BRD v4 §6.4 | The availability objective recorded in the baseline, and the topology that carries it: one cluster per environment, a namespace per workbench and the metrics baseline | TC-PLT-NF08-INF-02, TC-PLT-NF08-INF-06 |
| NFR-021 | Availability outside business hours: 99.5 percent, excluding the change window | Program BRD v4 §6.4 | The objective recorded with the change window excluded, and the upgrade carried by the platform maintenance window | TC-PLT-NF08-INF-06 |
| NFR-022 | Recovery point objective: the maximum data loss the business accepts | Program BRD v4 §6.4 (open; follows the ACE recovery point objective) | The objective recorded as the ACE objective and left open, with the codec and the retention rule that a restore depends on | TC-PLT-NF08-INF-05, TC-PLT-NF08-INF-06 |
| NFR-023 | Recovery time objective: the maximum time to restore service | Program BRD v4 §6.4 (open; follows the ACE recovery time objective) | The objective recorded as the ACE objective and left open, with the conformance check that proves the environment is the declared one after a restore | TC-PLT-NF08-INF-06, TC-PLT-NF08-INF-07 |
| NFR-045 | No production data is used in development; user acceptance uses masked copies | Program BRD v4 §6.7 | The payload and attribute rules, and the evidence that the check reads synthetic histories only | TC-PLT-NF08-INF-05 |
| NFR-053 | Data is encrypted at rest and in transit | Program BRD v4 §6.9 | The AES-GCM codec rule with a key in Key Vault per namespace, checked on every environment | TC-PLT-NF08-INF-05 |

| Decision or source | What it fixes here |
|---|---|
| ADR-014 | Schema and login per service in ACE PostgreSQL: the baseline forbids a workflow from reading a schema directly, and the layer owns no schema of its own |
| ADR-016 | The reusable Temporal layer and Schedules replacing Quartz: one cluster per environment, a namespace per workbench, the kit above it and no shared job table |
| ADR-023 | Observability per service: the metrics and health baseline is a platform surface, and each service keeps its own dashboard and alerts |
| Architecture v5 slides 23, 24, 46 | The five layers, one queue per service, the reuse rule and the rule that a new workbench takes a namespace and not a cluster |
| Temporal and Drools Design slides 12, 13, 27, 32 | The L1 and L2 ownership, Continue-As-New at stage ends and every 28 days, the deterministic-workflow rule, the codec, the attributes, the retention and version 1.30 or later |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1070-APP, RWB-PLT-E1070-CON | App development, Contract | Install the cluster, the persistence, the UI and the mTLS front door, and publish the metrics, health and role contract the check reads |
| RWB-PLT-N003-INF | Infrastructure | Provisions the namespace `rwb-recovery`, the AES-GCM codec key, the entitlements and the search attributes the check verifies |
| RWB-PLT-N010 | App development, Contract | Builds the versioned workflow kit whose templates must obey the code rules of this baseline |
| RWB-PLT-E1071 | App development, Contract | Builds the worker, the SDK wiring and the codec inside the worker, and inherits the versioning and replay rules |
| RWB-PLT-E2037 | App development, Contract | Owns the dashboard, the alerts and the run books that observe the objectives of this baseline |
| RWB-PLT-E2038 | App development, Contract | Owns the codec server, which the baseline records as the only decode path |
| RWB-PLT-E2039 | App development, Contract | Owns the backup, the failover, the upgrade and the archive that keeps a closed history after the 30 days |
| RWB-PLT-E2040 | App development | Owns the replay gate on every build, which is one of the rules the baseline declares |

The two open recovery objectives are the only requirement rows without a target: NFR-022 and NFR-023 are Open in the program BRD and follow the ACE objectives, so this story records them as open and never writes a number that no source gives.

### 19. Out of scope

- Installing the cluster, its two persistence databases, the frontend, the Web UI, the mTLS front door, the OIDC application, the metrics scrape and the run book: RWB-PLT-E1070-APP and RWB-PLT-E1070-CON.
- The namespace `rwb-recovery`, its codec key, its entitlements, its search attributes and its namespace-level evidence pack: RWB-PLT-N003-INF.
- The workflow kit templates and their semver: RWB-PLT-N010; this story declares the rules they must obey and does not build them.
- The worker, the SDK wiring, the codec inside the worker and the client retry policy: RWB-PLT-E1071.
- The dashboard, the alerts, the stuck-workflow scan and the run book catalog: RWB-PLT-E2037 and RWB-PLT-E1056-OPS.
- The codec server, the decode user interface and the Temporal admin audit: RWB-PLT-E2038.
- The backup policy, the point-in-time restore, the zone failover, the upgrade procedure and the archive run itself: RWB-PLT-E2039; this story records the cadence and the objectives and does not perform the drill.
- The replay gate implementation: RWB-PLT-E2040; this story names the gate as a baseline rule and reads its result.
- Nexus endpoints in the `ace-collection` namespace and the ACE team's own Temporal use; the baseline governs the Recovery layer.
- The 19 services' schemas, topics, task queues, REST bases and business models; the platform owns none of them, and a departure from the baseline is a change to the record or a waiver, never a local variation.
