# RWB-PLT-E2039-CON Temporal resilience: backup, failover, upgrade and archive - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-E2039-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-WF |
| Wave | 0 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-039 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP10, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W0 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-021, FR-PLT-022, FR-PLT-023, FR-PLT-024, FR-PLT-025, FR-PLT-026, FR-PLT-028, FR-PLT-029) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-039 for the workflow platform epic; the restore consistency-check contract, the archive manifest contract, the archive payload rule, the upgrade contract, the drill evidence contract, the idempotency contract and the error vocabulary are published on Day 1 with three fakes. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-PLT-E2039-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **consumer of the Temporal resilience contract (the platform and operations teams, the archive and consistency-check implementations, internal audit and security administration)**, I want **the restore consistency-check contract, the archive manifest contract, the archive payload rule, the upgrade contract, the drill evidence contract, the idempotency contract and the error vocabulary published on Day 1 with three fakes**, so that **the restore, failover, upgrade and archive work and their drills are built and tested against one frozen set**.

This is the contract story of legacy key RWB-E2-039 under epic RWB-PLT-WF. It publishes, as a platform contract of the Temporal layer:

- The restore consistency-check contract: the namespace `rwb-recovery`, the visibility record compared with history presence, the two count fields (workflows in visibility with no history, and the reverse), the workflow identifiers of both sets, and the refusal of a mismatched pair so that no worker starts against it.
- The archive manifest contract: the path `dt=yyyy-mm-dd/<workflowId>/<runId>.json.gz`, the manifest fields workflow ID, run ID, workflow type, close time, archive time, path, checksum and status, the statuses WRITTEN, VERIFIED and FAILED, the checksum rule and the three-retry rule.
- The archive payload rule: codec metadata with the key version is mandatory in every exported payload; a history that fails the check is never written and raises an incident.
- The upgrade contract: one minor version at a time, the version step check that refuses a longer jump, the drain, upgrade, schema tool and worker start order, and the pinned version record in Environment and Deployment Design v5.
- The drill evidence contract: the timestamps and counts every drill records, against the ACE recovery point objective and recovery time objective (NFR-022, NFR-023).
- The idempotency contract and the error vocabulary of the four interfaces, so a repeated write, a repeated drill record and a refused pair answer the same way in every implementation.
- Three fakes — a fake archive store, a fake consistency check and a fake version step check — and a contract test, so the restore, failover, upgrade and archive work is built and tested with no cluster, no Blob container and no release pipeline.

The platform is shared platform, not one of the 19 services: Template and Rules §R4 has no platform row, so this contract declares no `rwb_*` schema, no `rwb.<short>.events.v1` topic and no `/api/recovery/<short>/v1` base (DP-13, DP-14). The namespace `rwb-recovery` and task queue `rwb-platform` are fixed by RWB-PLT-E1070-CON and RWB-PLT-E1071-CON and are recorded here, not republished.

The contract is published at status Draft (realignment v1) and is frozen when its consumers pass their contract tests. No approval is required to publish a Draft contract.

The archive immutability period, the role that owns the retry count, the manifest retention and the approved release the version step check compares against are named by no read source: Not specified in the source documents (GAP-1448; ASM-2543). The contract publishes those four values as the working read of that assumption, once, so that the archive store, the retry rule and the version check read them and not four private readings.

### 2. Business rationale

A restore, a zone failover, a minor upgrade and an archive are four different proofs of the same claim: that the engine is part of the case record and comes back. Each one is produced by different tooling — the control plane of the PostgreSQL flexible server, the zone pair, the deployment pipeline and the archive job — and each one is read by different people: the platform administrator runs it, internal audit reads the archive, security administration reads the payload check, and the release record carries the drill result. Nothing in that chain forces the four to agree unless a contract does.

The archive is the sharp end. A history that leaves Temporal after the retention window is gone unless a file was written before it, and a file with no manifest row, no checksum or a clear payload is worse than no archive at all: audit cannot find it, and the bank cannot prove it holds no personal data. The monolith made the manifest a habit inside one job; in the target the archive job runs on a shared platform next to eighteen other services, and the reader is a different team. So the path convention, the eight manifest fields, the checksum rule and the three-retry rule are published before the job exists.

The restore and the upgrade have the same shape: a step that must refuse rather than proceed. A pair of databases restored to two different timestamps looks healthy and silently loses histories; a target two minor versions ahead of the approved release passes a pipeline that checks nothing. In the legacy story both refusals were written in one run book. In the target the consistency check and the version step check are separate pieces built by whoever picks up the story, so the refusal has to be a published contract, not a paragraph.

ADR-020 makes the contract the first artefact, and REQ-DRI-007 is why: every failure reaches a named owner and has a tested way back. A tested way back is a drill result with its timestamps and counts, recorded against the ACE recovery point and time objective rather than asserted. The measure is that every contract test answers from the fakes on Day 1, that a history closed 31 days ago is readable in the archive, and that a breaking change raises v2 instead of editing v1.

### 3. Preconditions

- RWB-PLT-E1070-CON is published: namespace `rwb-recovery`, the mTLS client certificate profile, the frontend API subset (DescribeNamespace, ListWorkflowExecutions, GetWorkflowExecutionHistory) and the 30-day retention of the namespace.
- RWB-PLT-E1071-CON is published: the platform worker on task queue `rwb-platform`, its SDK version and the workflow kit the Schedule-started runs are built from.
- RWB-PLT-E2037-CON is published: the observability surface, the run book map and MSG-P3-037, so a failed drill is observed and reported like any other workflow failure.
- The PostgreSQL flexible server carries automated backups and point-in-time restore with a window of at least 35 days (assumed), and the restore right is held by the operations group.
- The Blob container `rwb-temporal-archive` exists with a write-once policy for the archive period, and RW-AUDIT holds Storage Blob Data Reader on it.
- Retention is 30 days and the archive lead time is 7 days, both held as parameters through the parameters contract (RWB-PLT-E1042-CON, DP-06), so no value is a literal in the archive job.
- The archive job's schedule, owner and run book path are read and written through the rwb-integration scheduled-jobs admin operation, never by a table read, as recorded in RWB-PLT-E2037-CON.
- The approved server version is recorded in Environment and Deployment Design v5; the approved release the version step check compares against is Not specified in the source documents (GAP-1448; ASM-2543).
- The contract is Draft (realignment v1) until RWB-PLT-E2039-APP and the sibling consumers pass their contract tests; no approval is required to publish a Draft contract.

### 4. Flow

1. The contract author writes the restore consistency-check contract: the namespace `rwb-recovery`, the one restore point that both databases must share, the visibility record set compared with history presence, the two count fields and the workflow identifiers of both sets.
2. The author writes the refusal: a pair whose counts are not zero is refused, no worker starts against it, the run book says to restore both databases to one timestamp and repeat the drill, and the drill is recorded as failed with both timestamps.
3. The author writes the archive manifest contract: the path `dt=yyyy-mm-dd/<workflowId>/<runId>.json.gz`, the eight fields of a row, the statuses WRITTEN, VERIFIED and FAILED, the checksum comparison on read-back and the rule that the next run re-exports a FAILED row and turns it VERIFIED.
4. The author writes the retry rule: a failed write, a failed read-back or a failed payload check marks the row FAILED, retries the export up to three times in the same run, and raises an incident; the owner of the retry count is Not specified in the source documents (GAP-1448; ASM-2543).
5. The author writes the archive payload rule: every exported payload carries codec metadata naming its key version, a history that fails the check is never written, and the incident reaches security administration and the platform administrator.
6. The author writes the upgrade contract: the one-minor-version rule, the version step check that refuses a longer jump before any pod is replaced and names the missing intermediate version, and the order drain, upgrade with Helm, schema tool, workers with the matching SDK; the pinned version is recorded in Environment and Deployment Design v4.
7. The author writes the drill evidence contract: the fields every drill records (the drill name, the restore or failover timestamps, the workflow counts before and after, the elapsed time, the ACE recovery point and time objective it is measured against, and the result Planned, Passed or Failed), the cadence of the archive at 02:00 daily, and the rule that a failed drill blocks the release.
8. The author writes the idempotency contract and the error vocabulary: one manifest row per workflow ID and run ID path with a repeated write refused while the immutability policy holds the file, the consistency check read only, the version step check a second run at the same version changing nothing, and the error identifiers of section 14.
9. The fake archive store, the fake consistency check and the fake version step check are generated from the documents, the contract test runs the fakes against the documents on every change, and v1 is published to the contract registry for the consumers to pin.

### 5. Exception paths

| ID | Trigger | What happens | Message |
|---|---|---|---|
| X1 | A drill restores the two databases to different timestamps | The consistency check reports the workflows in visibility with no history, no worker starts against the pair, and the drill is recorded as failed with both timestamps | None (drill evidence) |
| X2 | The archive read-back checksum differs, or the Blob write fails | The contract marks the row FAILED and never VERIFIED, the retry rule allows the export up to three times in the same run, and the incident rule applies | None (incident only) |
| X3 | An upgrade proposes a target two minor versions later | The version step check refuses the upgrade before any pod is replaced and names the missing intermediate version | None (pipeline failure) |
| X4 | An exported history holds a payload that is not codec-encrypted | The payload rule refuses the file, the row is FAILED, and the incident reaches security administration and the platform administrator | None (incident only) |
| X5 | A document declares a manifest field, a status, a path element or an error identifier that the fakes do not answer | The contract test fails naming the field and the fake, and the version is not published | Lint finding, no message id |
| X6 | A value the consumers need is named by no read source: the archive immutability period, the owner of the retry count, the manifest retention and the approved release the version check compares against | The value is published as the working read of the assumption, with the placeholder where it is still open, and the gap stays open | Not specified in the source documents (GAP-1448; ASM-2543) |
| X7 | A breaking change is made to a published field, status, path element or error identifier | v1 is not edited; the change raises v2 and deprecates v1, and no consumer sees a changed v1 | Lint finding, no message id |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes documents and three fakes; runs no drill, writes no file, reads no business data and depends on nothing |
| Negotiable | Field order inside the models, the example values and the internal structure of the fakes are open until the version is frozen; the path convention, the eight fields, the three statuses, the three-retry rule, the refusal of a mismatched pair and the one-minor-version rule are fixed |
| Valuable | The app story, the archive store, the consistency check and the version step check start on Day 1 against one frozen set and three fakes |
| Estimable | Three contract artifacts, one error table, one idempotency section, three fakes and one contract test |
| Small | One sprint for the documents, the fakes and the lint rules |
| Testable | Each criterion in section 7 is a schema, lint or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Temporal resilience contract: backup, failover, upgrade and archive

  Background:
    Given the platform is shared platform and owns no schema, no topic and no Workbench REST base
    Given the resilience surface serves the workflows of namespace rwb-recovery on task queue `rwb-platform`

  Scenario: AC1 The restore consistency-check contract is published (new, D-RCV-60)
    Given the restore consistency-check contract document
    When it is validated and linted
    Then it declares the namespace rwb-recovery and the one restore point both databases temporal and temporal_visibility must share
    Then it declares the visibility record set compared with history presence, and the two count fields: workflows in visibility with no history, and the reverse
    Then it declares the workflow identifiers of both sets, so a drill names what it found and not only how many
    Then a pair whose two counts are not zero is refused, no worker starts against the pair, and the drill is recorded as failed with both timestamps
    Then it declares the consistency check read only, with no write to either database

  Scenario: AC2 The archive manifest contract is published (new, D-RCV-60)
    Given the archive manifest contract document
    When it is validated against the manifest schema
    Then it declares the path dt=yyyy-mm-dd/<workflowId>/<runId>.json.gz under the container rwb-temporal-archive
    Then it declares the eight fields workflow ID, run ID, workflow type, close time, archive time, path, checksum and status
    Then it declares the statuses WRITTEN, VERIFIED and FAILED, and no other status
    Then the checksum is the checksum of the file at that path, and a row is VERIFIED only when the read-back checksum matches
    Then a failed write, a failed read-back or a failed payload check leaves the row FAILED, the export is retried up to three times in the same run, and the next run re-exports the history
    Then the path is the key, and a repeated write is refused while the immutability policy holds the file

  Scenario: AC3 The archive payload rule is published (new, D-RCV-60)
    Given the archive payload rule of the manifest contract
    When a manifest row and a file are reviewed against it
    Then every exported payload carries codec metadata naming its key version, and a payload without codec metadata fails the check
    Then a history that fails the check is never written, and its row is FAILED
    Then the incident reaches security administration and the platform administrator, and no clear value appears in the file, the manifest or the archive log
    Then the manifest holds the workflow ID, type and timestamps and no personal data field

  Scenario: AC4 The upgrade contract is published (new, D-RCV-60)
    Given the upgrade contract document
    When the version step check is reviewed against it
    Then the upgrade moves one minor version at a time, and a target two minor versions later is refused before any pod is replaced
    Then the refusal names the missing intermediate version, and the approved path is one minor version, verify, then the next
    Then the order is fixed: the workers are drained, the server is upgraded with Helm, the schema tool runs, and the workers start with the matching SDK
    Then the pinned version is recorded in Environment and Deployment Design v5
    Then the approved release the check compares against is published as the working read of the assumption, with the placeholder where it is still open

  Scenario: AC5 The drill evidence contract is published (new, D-RCV-60)
    Given the drill evidence contract document
    When a restore drill row, a failover drill row and an upgrade drill row are validated
    Then every row declares the drill name, the timestamps, the workflow counts before and after, the elapsed time and the result
    Then every row declares the ACE recovery point objective and recovery time objective it is measured against, NFR-022 and NFR-023, and neither value is set in the document or in code
    Then the restore row carries the one restore point and both database names, and the failover row carries the count of RUNNING workflows before and after
    Then the result is Planned, Passed or Failed, and a failed drill blocks the release
    Then no drill result is recorded as passed without its timestamps and counts

  Scenario: AC6 The idempotency contract is published (new, D-RCV-60)
    Given the idempotency section of the three documents
    When it is read against the fakes
    Then the manifest path is the key: one row per workflow ID and run ID, and a repeat while the immutability policy holds the file is refused and writes no second row
    Then the consistency check is read only, and a repeated check at the same restore point gives the same two counts
    Then the version step check is idempotent: a second run at the same version changes nothing
    Then a repeated drill record for one drill run overwrites nothing and is ignored, the way R-UNI-40 ignores a duplicate event with the same key

  Scenario: AC7 The fakes answer every example and the contract test is green (new, D-RCV-60)
    Given the fake archive store, the fake consistency check and the fake version step check, generated from the documents
    When the contract test runs
    Then the fake archive store answers the write, the read-back, the checksum match, the checksum difference, the immutability refusal and the three retries
    Then the fake consistency check answers zero counts, the mismatched pair with both counts and the refusal of a worker start
    Then the fake version step check answers one minor version, the two-minor-version refusal with the missing intermediate version, and the second run at the same version
    Then the payload rule example answers key version 2 and a payload without codec metadata
    Then every document validates, every lint rule passes and no example holds a personal value

  Scenario: AC8 A breaking change raises v2 (new, D-RCV-60)
    Given a published v1 of the three contract documents with the consumers pinning it
    When a manifest field, a status, a path element or an error identifier is changed
    Then v1 is not edited, the change raises v2 and marks v1 deprecated, and the fakes answer both versions
    Then every consumer sees the change as a version, not as a difference between environments
```

The eight criteria are new and test only the contract baseline: no legacy acceptance criterion is repeated here, and every value in the declarations and the examples is a value of RWB-E2-039, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Automated backups and point-in-time restore run on both Temporal databases, and a restore goes to a new server at one timestamp for both databases, never in place on the live server | D-RCV-36 T1; legacy RWB-E2-039 BR1 |
| BR2 | A restore and a failover are measured against the ACE recovery point objective and recovery time objective; NFR-022 and NFR-023 are open values (DL11) and are never set in code or in the document | NFR-022, NFR-023; legacy BR2 |
| BR3 | The consistency check compares the visibility record with history presence, publishes both count fields and the workflow identifiers, and refuses a mismatched pair: no worker starts against it and the drill is recorded as failed with both timestamps | Legacy AC6, X1 |
| BR4 | A closed history is exported before retention removes it; the archive lead time is 7 days against a 30-day retention, and both are parameters | Legacy BR5; Temporal and Drools Design slide 27 |
| BR5 | The archive is write-once for its period, checksummed and indexed by one manifest row with its status; the path is the key | Legacy BR6; legacy AC4, AC7 |
| BR6 | The archive holds codec-encrypted payloads only; a history that fails the payload check is not written, its row is FAILED and the incident reaches security administration and the platform administrator | NFR-045; legacy BR7, AC9 |
| BR7 | An upgrade moves one minor version at a time: workers drained, server upgraded with Helm, schema tool run, workers started with the matching SDK, the pinned version recorded in Environment and Deployment Design v5 | Legacy BR4, AC3, AC8 |
| BR8 | A drill result is release evidence with its timestamps and counts, a failed drill blocks the release, and every value of the four interfaces is configuration, never code | REQ-DRI-007; legacy BR9, BR10 |

### 9. State transitions

The contract has its own lifecycle, and the manifest rows and the drill records it describes have theirs. This story changes no case status.

| Object | From | Event | To |
|---|---|---|---|
| Contract document | Draft | Published (realignment v1) and open to comment | Draft |
| Contract document | Draft | The consumers pass against the published version | Published |
| Contract document | Published | The consumers pin the version and the change window closes | Frozen |
| Contract document | Published or Frozen | A breaking change is accepted | A new version, and the old version is Deprecated |
| Manifest row | None | The archive job writes the file and the row | WRITTEN |
| Manifest row | WRITTEN | The read-back checksum matches | VERIFIED |
| Manifest row | WRITTEN | The checksum differs, the write fails or the payload check fails | FAILED, and retried in the same run |
| Manifest row | FAILED | The next run re-exports the history and the read-back matches | VERIFIED |
| Manifest row | VERIFIED | The archive retention ends | Disposed by the archive retention decision, outside this contract |
| Drill record | Planned | The drill starts and its timestamps are recorded | Planned |
| Drill record | Planned | The drill passes inside the recovery point and time objective | Passed |
| Drill record | Planned | A step fails, or the pair is mismatched | Failed, and the release is blocked |

The workflow states CLOSED, RUNNING and COMPLETED are the engine's and are named only so that a drill can count them; this contract owns the document states and the answer vocabulary of the fakes.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the three documents, the error table, the idempotency section and the fakes |
| The platform owner of the Temporal layer | Approves a breaking change and a version freeze, and owns the namespace, the task queue and the archive container values |
| Security architecture | Confirms the payload rule, the codec metadata requirement and the incident path to security administration |
| Internal audit | Confirms the manifest fields, the checksum rule and the read-only access to the archive it depends on |
| The operations group | Holds the restore right on the PostgreSQL flexible server and the archive data roles; confirms the drill evidence fields it must produce |
| The ACE platform team | Owns the zone pair, the flexible server and the backup and restore capability the drills exercise |
| The rwb-case owner (P3) | Confirms the parameters contract that holds the retention, the archive lead time and the retry count (DP-06) |
| RW-PLATADM, RW-AUDIT, RW-SECADM | Read the contract; raise a change request rather than a private variant |
| No delegation of authority level applies | A resilience contract is a technical artefact, not a credit decision, and a restore or an upgrade is not a credit decision |

No personal name, no email address and no credential appears in a document, a schema, an example or a fake. Where a caller must be named, the example uses a role code or a service identity only.

### 11. Data

| Item | Value |
|---|---|
| Business data published | None. The documents publish field names, count names, path elements, status values, drill fields and error identifiers; no customer, account, case or document value appears |
| Workflow identifiers in examples | Synthetic, and only the ones the legacy story uses: case-RW-2026-000101, case-RW-2026-000102, case-RW-2026-000201, case-RW-2026-000202 and platform-smoke-20261116, with the run identifiers that go with them |
| Archive path in examples | The published path only, shown once as dt=2026-10-23/case-RW-2026-000101/<runId>.json.gz; the manifest row and the file hold no personal data field |
| Personal data | None. No name, no email address, no account number and no national identifier is published; the national identifier of the legacy payload example is used only as the string the payload check must find in no file, no manifest and no log |
| Tables published | None. This contract declares no table, no column and no migration; the archive and the manifest live in Blob storage, and the archive job's row lives in the rwb-integration catalogue and is read through its admin operation |
| Retention | None at the contract: a document keeps no data, the fakes hold only the examples they publish, and the manifest retention and the archive immutability period are Not specified in the source documents (GAP-1448; ASM-2543) |

### 12. Contract

#### 12.1 REST operations provided

None. The platform has no service short (Template and Rules §R4 has no platform row), so this contract declares no path under `/api/recovery/<short>/v1` and no Workbench endpoint (DP-13). The interfaces it publishes are internal ones: the consistency check and the version step check run inside the platform tooling and the deployment pipeline, and the archive manifest is a row written to Blob storage at the published path. No gateway route is added (DP-19).

#### 12.2 REST operations consumed

None. The contract itself consumes nothing. The consistency check reads the Temporal frontend API over mTLS and the version step check reads the approved version record; both are the app story's reads and are recorded in RWB-PLT-E2039-APP section 12.2, not here.

#### 12.3 Events published

None. The platform publishes no `rwb.<short>.events.v1` topic and no event schema (DP-14). A failed drill, a FAILED manifest row and a refused upgrade are incidents and release evidence, not events.

#### 12.4 Events consumed

None. The archive job reads CLOSED workflows through the Temporal frontend API and writes files and manifest rows; it subscribes to no topic and reads no outbox.

#### 12.5 Workflows and activities

The contract declares the shape of three interfaces and one record, and owns no workflow and no activity:

| Model | Fields |
|---|---|
| Restore consistency check request | namespace `rwb-recovery`; the one restore point both databases must share; the visibility record set and the history presence read for each workflow of that namespace |
| Restore consistency check response | the count of workflows in visibility with no history, the count of histories with no visibility record, the workflow identifiers of both sets, and the verdict consistent or refused; PERMISSION_DENIED and UNAVAILABLE where the frontend cannot be read |
| Archive manifest row | workflow ID, run ID, workflow type, close time, archive time, path `dt=yyyy-mm-dd/<workflowId>/<runId>.json.gz`, checksum, status WRITTEN, VERIFIED or FAILED |
| Archive payload check | for one exported history: the payload count, the key versions found in the codec metadata, the payloads without codec metadata, and the verdict written or refused |
| Version step check | the approved version, the proposed target version, the minor steps between them, and the verdict allowed or refused with the missing intermediate version |
| Drill evidence row | the drill name, the timestamps, the workflow counts before and after, the elapsed time, the ACE recovery point objective and recovery time objective (NFR-022, NFR-023) it is measured against, and the result Planned, Passed or Failed |

The archive job's run is a Schedule-started workflow on task queue `rwb-platform` at 02:00 daily (DP-10); this contract fixes the path, the row, the checksum and the retry rule, not the workflow's internals.

#### 12.6 Schedules

None owned by this contract. The 02:00 daily archive Schedule is the app story's (RWB-PLT-E2039-APP section 12.6); this contract fixes the cadence, the manifest row and the retry rule only, and records that the legacy Quartz job of D-RCV-36 T2 becomes a Temporal Schedule under DP-10.

#### 12.7 Tables owned

None. The contract owns no `rwb_*` schema and no table (DP-01, DP-15); `decision_log_entry` is rwb-decision's (P7) and is not written by a drill or by an archive run, and no migration of this story runs.

#### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| Fake archive store (this story) | The write at the published path, the read-back, the checksum match and difference, the immutability refusal, the three retries and the three statuses WRITTEN, VERIFIED and FAILED | RWB-PLT-E2039-APP, the archive store test |
| Fake consistency check (this story) | Zero counts for a consistent pair, the two counts and the workflow identifiers for a mismatched pair, the refusal of a worker start, and PERMISSION_DENIED and UNAVAILABLE | RWB-PLT-E2039-APP, the restore and failover drill tests |
| Fake version step check (this story) | One minor version allowed, a two-minor-version target refused with the missing intermediate version, and a second run at the same version changing nothing | RWB-PLT-E2039-APP, the upgrade test |
| Cluster and frontend fake (RWB-PLT-E1070-CON) | The namespace `rwb-recovery`, the frontend API subset and the search attributes, with a namespace that is not REGISTERED and an UNAVAILABLE answer | The consistency-check and drill-evidence examples |
| Parameters-contract fake (RWB-PLT-E1042-CON) | The retention of 30 days, the archive lead time of 7 days and the retry count of three as named values, with a value changed and a value missing | The archive and drill evidence examples |

The three fakes answer from the two owner fakes rather than from copied payloads, so a change to the namespace contract or to a parameter shows up as a contract-test failure here. They are test-only and are never deployed to SIT, UAT or PROD.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 0 | No service base, no gateway route; the consistency check and the version step check are internal interfaces |
| Kafka | 0 | 0 | No topic of its own and no event schema |
| Temporal | 3 internal interface contracts and 1 drill evidence record | 0 | Namespace `rwb-recovery`, task queue `rwb-platform`; the 02:00 archive run is the app story's |
| File | 1 path convention | 0 | The archive file at `dt=yyyy-mm-dd/<workflowId>/<runId>.json.gz` in container `rwb-temporal-archive` |

### 13. Solution plan

**Deliverables.**

- `resilience-contract.yaml`: the restore consistency check (the namespace, the one restore point, the two count fields, the workflow identifiers and the refusal), the version step check (the one-minor-version rule and the missing intermediate version) and the idempotency section.
- `archive-manifest.yaml`: the path convention, the eight manifest fields, the three statuses, the checksum rule, the three-retry rule and the archive payload rule.
- `drill-evidence.yaml`: the drill row fields, the timestamps and counts, the NFR-022 and NFR-023 measurement and the Planned, Passed and Failed results.
- The error and idempotency sections of this document, generated into the three artifacts.
- The fake archive store, the fake consistency check and the fake version step check, generated from the artifacts over the RWB-PLT-E1070-CON and RWB-PLT-E1042-CON fakes.
- The lint rules and the contract test.

**Pattern application**

| DP code | legacy marker | microservice pattern | dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | none: a drill, a restore and an archive run write no decision record |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

These are the Template and Rules §R5.5 rows that bear on a platform contract. DP-10 is the substantive one: the legacy archive job is a Quartz job at 02:00 and D-RCV-36 T2 kept Quartz, but the target makes every recurring job a Temporal Schedule on the owning task queue, so the contract declares the 02:00 cadence and the workflow kit dependency and the app story registers the Schedule — no reader of the document can rebuild the Quartz job. DP-06 is why the 30-day retention, the 7-day lead time and the retry count of three are published as named values of the parameters contract and never as literals: the archive job and the drill evidence read them, so a change of value is a configuration change and not a document version. DP-03, DP-05, DP-01, DP-13, DP-14, DP-15, DP-07 and DP-19 are declared as absences: the resilience path writes no decision record, reads no `rwb_*` table and no ACE view, publishes no `/api/recovery` base and no topic, runs no migration, keeps its severity and result vocabulary as values, and composes no Workbench screen. This story adds no build dependency of its own: it is a CON story, starts on Day 1 and is frozen when its consumers pass.

**Build steps**

1. Write `resilience-contract.yaml` with the consistency check, the one restore point, the two count fields, the workflow identifiers, the refusal and the version step check.
2. Write `archive-manifest.yaml` with the path convention, the eight fields, the three statuses, the checksum rule, the three-retry rule and the payload rule.
3. Write `drill-evidence.yaml` with the drill fields, the timestamps and counts, the NFR-022 and NFR-023 measurement and the three results.
4. Write the error table: MSG-P3-037 reused unchanged, and the reserved PLT-RES identifiers of section 14.
5. Write the idempotency section: the path as the key, the read-only consistency check, the idempotent version step check and the ignored duplicate drill record.
6. Add the lint rules: no service base and no topic name in the documents, no manifest field without a status, no status outside WRITTEN, VERIFIED and FAILED, no path outside the published convention, the payload rule mandatory, a personal-data scan over every example, and one row per workflow ID and run ID.
7. Generate the three fakes over the RWB-PLT-E1070-CON and RWB-PLT-E1042-CON fakes, write the contract test, and publish v1 to the contract registry with the version the consumers pin.

**Done when.** The three artifacts validate, every lint rule passes, the three fakes answer every example including the mismatched pair, the checksum difference, the three retries, the payload without codec metadata and the two-minor-version refusal, the contract test is green on the build of this story, and RWB-PLT-E2039-APP has pinned v1.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-P3-037 | A drill leaves a workflow failed or not moving, as any other workflow failure | Workflow {workflowId} has failed or has not moved for {hours} hours. | Reused unchanged from RWB-PLT-E2037-CON, with {workflowId} and {hours} |
| PLT-RES-401 | The consistency check is called with no client certificate, or a certificate that does not carry the namespace claim | The standard no-session text; the title and detail are Not specified in the source documents (GAP-1448; ASM-2543) | 401, reserved for this contract |
| PLT-RES-413 | One history export exceeds the page or size the export interface accepts | The request is refused before any file is written; the limit and the text are Not specified in the source documents (GAP-1448; ASM-2543) | 413, reserved for this contract |
| PLT-RES-422 | A manifest row would be written without a checksum, or an exported history fails the payload rule | The file is not written and the row is FAILED; the text names the field or the payload index, never the payload | 422, reserved for this contract |
| PLT-RES-503 | The Temporal frontend or Blob storage is unavailable during a run | No count is reported and no file is written; the run is retried under the retry rule and the text is Not specified in the source documents (GAP-1448; ASM-2543) | 503, reserved for this contract |

MSG-P3-037 is reused unchanged and is the only message identifier the documents borrow; a failed drill reports the workflow failure through it and adds its own release evidence. The four PLT-RES identifiers are reserved for this contract; when the message catalogue gains platform resilience entries they replace the placeholder text and no other value changes. No business text is invented for them here.

### 15. Screens and states

No screen in this story, and the document set declares none. The operational views are the Temporal Web UI, the Grafana dashboard of RWB-PLT-E2037-CON and the Azure portal listing of the archive container with the manifest; none is a Workbench screen and no route is added to the gateway (DP-19). The contract fixes the document states of section 9, the three manifest row states WRITTEN, VERIFIED and FAILED, and the three drill results Planned, Passed and Failed, so that the app story, internal audit and the release record share one vocabulary. The Workbench job monitor shows the archive job's last run, status and duration from the catalogue row and repeats none of this data.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-E2039-CON-01 | AC1 | Contract | `resilience-contract.yaml`: namespace `rwb-recovery`, the one restore point, the two count fields, the workflow identifiers of both sets, the refusal; read only; restore at 09:55 against `temporal` and `temporal_visibility` at 10:05 |
| TC-PLT-E2039-CON-02 | AC2 | Contract | `archive-manifest.yaml`: dt=2026-10-23/case-RW-2026-000101/<runId>.json.gz, the eight fields, the three statuses, the checksum rule, three retries, the refused repeat write |
| TC-PLT-E2039-CON-03 | AC3 | Contract | The payload rule: codec metadata with key version 2 mandatory, the synthetic national identifier of the legacy payload example absent from the file, the manifest and the log, the FAILED row and the incident |
| TC-PLT-E2039-CON-04 | AC4 | Contract | The upgrade contract: one minor version, the two-minor-version refusal with the missing intermediate version, the drain, Helm, schema tool and worker order, the pinned version record |
| TC-PLT-E2039-CON-05 | AC5 | Contract | `drill-evidence.yaml`: the restore, failover and upgrade rows, 12 RUNNING workflows before and after, 5 workflows on the upgrade, NFR-022 and NFR-023 as named values |
| TC-PLT-E2039-CON-06 | AC6 | Contract | The idempotency section: the path as the key, one row per workflow ID and run ID, the immutability refusal, the repeated consistency check, the idempotent version step check, the ignored duplicate drill record |
| TC-PLT-E2039-CON-07 | AC7 | Component | The three fakes over the RWB-PLT-E1070-CON and RWB-PLT-E1042-CON fakes: every example answered, the mismatched pair, the checksum difference, the retries, the payload without metadata |
| TC-PLT-E2039-CON-08 | AC8 | Component | A breaking change to a manifest field, a status, a path element and an error identifier: v2 raised, v1 deprecated, both answered by the fakes |

These test cases cover the published contract only and test no business behaviour: the drills themselves, the restore, the failover, the upgrade and the archive job are tested by RWB-PLT-E2039-APP, and the legacy test cases TC-E2-039-01 to TC-E2-039-11 stay with that story.

### 17. Guardrails

- No service base, no gateway route, no schema name and no topic name in the documents: the platform owns none of them (DP-13, DP-14), and the lint step fails the build if one appears.
- No business value in a document, an example or a fake: the retention, the lead time, the retry count, the immutability period and both recovery objectives are named values or documented assumptions, never literals.
- No personal data in a document, an example, a fake or a log: synthetic workflow identifiers only, and the payload rule makes a clear payload a refusal rather than a finding.
- The payload rule is mandatory: a history that fails the check is never written, and the manifest row is FAILED with no exception.
- No file without a manifest row and no row without a checksum; a row is VERIFIED only on a matching read-back.
- The path is the key: a repeated write is refused while the immutability policy holds the file, and no second row is written.
- No restore in place and no pair at two timestamps: the consistency check refuses a mismatched pair and no worker starts against it.
- No upgrade by more than one minor version and none without draining the workers first; the version step check refuses before any pod is replaced.
- No drill result recorded as passed without its timestamps and counts, and no failed drill in a release record that claims a pass.
- No table and no migration in this contract: the archive and the manifest live in Blob storage and the catalogue row belongs to rwb-integration.
- The contract is versioned: a breaking change raises v2 and deprecates v1 in place of editing v1.
- The fakes are test-only, hold synthetic data and are never deployed to SIT, UAT or PROD; no environment value points at one.

### 18. Traceability

| Requirement ID | Requirement (short) | Source | Test cases |
|---|---|---|---|
| REQ-DRI-007 | Every failure reaches a named owner and has a tested way back | RWB-E2-039 section 18 (Epic 2, 3.2; Program, 6.4) | TC-PLT-E2039-CON-01, TC-PLT-E2039-CON-02, TC-PLT-E2039-CON-05, TC-PLT-E2039-CON-07 |
| NFR-022 | Recovery point objective: the maximum data loss the business accepts | Program BRD v4, 6.4 (open, DL11) | TC-PLT-E2039-CON-05 |
| NFR-023 | Recovery time objective: the maximum time to restore service | Program BRD v4, 6.4 (open, DL11) | TC-PLT-E2039-CON-05 |
| NFR-045 | No production data is used in the development environment, and the user acceptance environment uses masked copies | Program BRD v4, NFR table | TC-PLT-E2039-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout: the contract is published with a fake before any code | Architecture Decision Records, ADR-020 | TC-PLT-E2039-CON-02, TC-PLT-E2039-CON-07 |
| DP-06 | The retention, the archive lead time and the retry count are named values of the parameters contract | Template and Rules §R5.5 DP-06; RWB-PLT-E1042-CON | TC-PLT-E2039-CON-02, TC-PLT-E2039-CON-05 |
| DP-10 | A Schedule replaces Quartz: the 02:00 archive is a Temporal Schedule on task queue `rwb-platform` | Template and Rules §R5.5 DP-10; RWB-PLT-E1071-CON; Architecture v5 slide 44 | TC-PLT-E2039-CON-02, TC-PLT-E2039-CON-06 |
| DP-01, DP-03, DP-05, DP-07, DP-13, DP-14, DP-15, DP-19 | Declared as absences: no table read, no decision record, no service base, no topic, no migration and no screen | Template and Rules §R5.5 | TC-PLT-E2039-CON-01, TC-PLT-E2039-CON-04 |
| R-UNI-40 | The same event arriving twice with the same key is ignored and the hit is recorded | Business Rules and Routing Logic v4, R-UNI-40 | TC-PLT-E2039-CON-06 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E2039-APP | App development | H consumer: implements the consistency check, the version step check, the drill runs, the archive job and the manifest writer against this contract and its fakes |
| RWB-PLT-E1070-CON | Contract | The namespace `rwb-recovery`, the frontend API subset, the client certificate profile and the 30-day retention the consistency check reads |
| RWB-PLT-E1071-CON | Contract | The platform worker on task queue `rwb-platform` and the workflow kit the 02:00 archive run is built from (DP-10) |
| RWB-PLT-E1027-CON | Contract | The local decision-record library the platform worker template wires; this contract writes no record through it (DP-03) |
| RWB-PLT-E1042-CON | Contract | The parameters that hold the retention, the archive lead time and the retry count (DP-06) |
| RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON | Contract | The reference values, the naming library and the Flyway convention this story declares as absences (DP-07, DP-14, DP-15) |
| RWB-PLT-N001-CON | Contract | gateway-bff; the archive and the drills add no screen and no route (DP-19) |
| RWB-PLT-E2037-CON | Contract | The observability surface, MSG-P3-037 and the alert-to-run-book map the drill evidence points at |
| RWB-P3-E1042-CON | Contract | C: the owner contract of the parameters this document names, built against and never read by table |
| RWB-P3-E1043-CON | Contract | C: the owner contract of the reference data, including the result and status vocabulary |
| RWB-PLT-E2040-CON | Contract | Sibling: the replay gate and the build ID rollout; the upgrade path here ends where the replay gate begins |
| RWB-PLT-N003-INF | Infrastructure | Sibling: the namespace `rwb-recovery` and the codec key the archive payload rule depends on |
| RWB-PLT-NF08-INF | Infrastructure | Sibling: the Temporal platform baseline, its persistence and its backup configuration |
| Legacy RWB-E2-037 (now RWB-PLT-E2037-APP, RWB-PLT-E2037-CON) | App development, Contract | Alerts, the stuck scanner and the dashboard; this contract reuses MSG-P3-037 and adds no alert |

### 19. Out of scope

- The backup policy, the drill run books, the consistency check, the version step check, the archive job, the payload check and the manifest writer themselves (RWB-PLT-E2039-APP).
- The cluster, the namespace, the mTLS identities and the persistence stores (RWB-PLT-E1070-CON and RWB-PLT-E1070-APP).
- The worker, the SDK wiring and the platform task queue (RWB-PLT-E1071-CON and RWB-PLT-E1071-APP); the 02:00 archive Schedule registration is the app story's.
- Alerts, the stuck scanner and the workflow dashboard (legacy RWB-E2-037; RWB-PLT-E2037-APP).
- The replay gate, history export for tests and build ID rollout (legacy RWB-E2-040; RWB-PLT-E2040-APP and RWB-PLT-E2040-CON).
- The codec server, decode and the administrative audit (legacy RWB-E2-038; RWB-PLT-E2038-APP and RWB-PLT-E2038-CON).
- Disaster recovery of the ACE AKS cluster itself and the region pair, which follow the ACE platform plan.
- The retention period itself (DL26) and the disposal decision after the archive period.
- Case-level restoration of a single case and any manual replay of a case workflow.
- Any Workbench screen for the archive, the drills or the upgrade (Epic 8).
