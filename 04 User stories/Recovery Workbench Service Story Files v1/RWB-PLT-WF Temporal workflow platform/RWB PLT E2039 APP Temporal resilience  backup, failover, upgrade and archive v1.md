# RWB-PLT-E2039-APP Temporal resilience: backup, failover, upgrade and archive

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-E2039-APP |
| Work type | APP (App development) |
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
| Parallel lane | L-PLT-WF-H |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E2039-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-PLT-E1070-CON, RWB-PLT-E2037-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-021, FR-PLT-022, FR-PLT-023, FR-PLT-024, FR-PLT-025, FR-PLT-026, FR-PLT-028, FR-PLT-029) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-039 for the workflow platform epic; the backup policy, the restore, failover and upgrade drills and the daily archive become platform work built against RWB-PLT-E2039-CON, the legacy 02:00 Quartz archive job becomes the Temporal Schedule `HistoryArchiveJob` on task queue `rwb-platform` in namespace `rwb-recovery` (DP-10; the Quartz scheduler is retired with RWB-TE-007), and the nine legacy criteria are carried whole with every value kept. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **the Temporal databases backed up, the zone failover and a minor upgrade tested, and closed histories archived before retention removes them**, so that **the engine meets the ACE availability targets and an audit can still read a closed workflow after its history has left Temporal**.

This is the split (rework) slice of legacy key RWB-E2-039 under epic RWB-PLT-WF (Template and Rules §R6). No legacy section is copied word for word, no "As built (monolith)" heading appears and no delta copy of an as-built story is made: section 7 carries the nine legacy criteria with every value kept, and the microservice change for the legacy key is described here. The change from the legacy story:

- **Placement.** The backup policy, the three drills and the archive stop being work inside the monolith's integration module and become work of the shared Temporal platform, owned once and used by every workbench namespace. The cluster, its persistence and its namespaces are the platform layer the platform team operates (Architecture v5 slides 23 and 24), so a resilience proof is a property of the platform spine and not of one service.
- **Contract first.** The drill evidence schema, the archive path and manifest schema, the consistency-check query contract, the payload-check result and the version-step rule are published on Day 1 by RWB-PLT-E2039-CON with fakes, before any code (ADR-020). This story builds against that contract and its fakes.
- **The archive job.** The legacy daily Quartz job is retired with RWB-TE-007 (Template and Rules §R6), because the target runs no Quartz and no shared job table. It becomes `HistoryArchiveJob`, a Temporal Schedule daily at 02:00 with overlap policy SKIP, on task queue `rwb-platform` in namespace `rwb-recovery`, and each run is a short `TemporalHistoryArchiveWorkflow` run (DP-10; RWB-PLT-E1071-CON; Architecture v5 slide 44).
- **The archive store.** Closed histories and their manifest leave the monolith's file share for Azure Blob container `rwb-temporal-archive`, immutable (write-once) for the archive period, at path `dt=yyyy-mm-dd/<workflowId>/<runId>.json.gz`, with one manifest row per file carrying the workflow ID, run ID, workflow type, close time, archive time, path and checksum.
- **The payload check.** The archive holds codec-encrypted payloads only: every exported history passes the codec metadata check before the file is written, and a clear payload fails the row rather than the file. Decode of an archived payload stays with the codec server of RWB-PLT-E2038-APP.
- **No schema and no topic.** The platform is not one of the 19 services: Template and Rules §R4 has no platform row, so this story writes no `rwb_*` schema, publishes no `rwb.<short>.events.v1` topic, owns no `/api/recovery/<short>/v1` base and creates no migration (DP-01, DP-13, DP-14, DP-15 declared).
- **The values.** Retention 30 days and the archive lead time of 7 days are parameters read through RWB-PLT-E1042-CON (DP-06); the container, its immutability period, the retry count and the approved server and SDK release are configuration; the manifest statuses and the drill states are reference values, not literals (DP-07).

The platform login that runs the archive run and the drills, its task-queue provisioning record, the owner of the backup and restore right, the immutability period of the archive container and the approved server and SDK release are named by no read source: Not specified in the source documents (GAP-1447; ASM-2542).

### 2. Business rationale

From Epic 3 every live case waits inside a Temporal workflow, so the engine becomes part of the case record: a lost history is a lost case step, and an engine that cannot be restored inside the ACE recovery time objective stops the recovery desk. RWB-PLT-E1070-APP installs the cluster and RWB-PLT-E2037-APP alerts when a workflow stops, but neither proves that the data comes back, that a zone loss is survived, that a minor upgrade keeps a running workflow, or that a closed history survives the 30-day retention.

This story adds the four proofs and the one archive: a point-in-time restore of both Temporal databases to one timestamp, a zone failover that completes the smoke workflow, a one-minor upgrade with no lost workflow, and a daily export of closed histories to write-once Blob storage before retention removes them. It meets REQ-DRI-007 (a named owner and a tested way back for every failure). The measure is that every drill passes in SIT inside the ACE recovery time objective, that a history closed 31 days ago is readable in the archive, and that no archived file holds clear personal data.

The split moves the proof to where the engine lives. A backup policy written inside one service proves nothing about the cluster the nineteen services share, and a Quartz job inside one module would be the only scheduler in a target that has retired Quartz altogether (D-RCV-36 T2; RWB-TE-007 retired). On the platform layer the policy, the three run books and the archive are written once, they are exercised against namespace `rwb-recovery`, and they are inherited by the next workbench that takes a namespace instead of a cluster (Architecture v5 slides 23 and 46). The alternative — a restore drill per service and a scheduler per module — would give the bank one proof per team and no single place where the engine is shown to come back.

### 3. Preconditions

- RWB-PLT-E2039-CON is published: the drill evidence schema, the archive path and manifest schema, the consistency-check query contract, the payload-check result contract, the version-step rule and the fakes.
- The nine platform contracts are published: RWB-PLT-E1027-CON (the local decision-record library the platform worker template wires), RWB-PLT-E1042-CON (parameters), RWB-PLT-E1043-CON (reference data), RWB-PLT-E1071-CON (the workflow kit, the platform worker on task queue `rwb-platform` and the Schedule template, DP-10), RWB-PLT-E1047-CON (naming), RWB-PLT-E1044-CON (the per-service Flyway convention this story does not use), RWB-PLT-N001-CON (gateway-bff, DP-19), RWB-PLT-E1070-CON (the cluster, the namespace `rwb-recovery`, mTLS, the client certificate profile and the frontend API subset) and RWB-PLT-E2037-CON (the dashboard and alert contract the drills are observed on).
- The two owner contracts are consumed as C rows through their fakes: RWB-P3-E1042-CON (parameters) and RWB-P3-E1043-CON (reference data).
- RWB-PLT-E1070-APP is done: the databases `temporal` and `temporal_visibility` on the zone-redundant PostgreSQL flexible server, namespace `rwb-recovery`, mTLS, the metrics scrape and the platform run book exist.
- RWB-PLT-E2037-APP is done: the failed, stuck and latency alerts, the dashboard and their run books exist, so a drill is observed like a live incident.
- RWB-PLT-E1071-APP is done: the platform worker polls task queue `rwb-platform` and runs the smoke workflow `platform-smoke-20261116`, so the drills have a proof workflow.
- The PostgreSQL flexible server has automated backups and point-in-time restore enabled with a window of at least 35 days (assumed), and the operations group holds the restore right.
- The Blob container `rwb-temporal-archive` exists with a write-once policy for the archive period, and RW-AUDIT holds Storage Blob Data Reader on it.
- Retention is 30 days (`temporal.retention.days` = 30; assumed, DL26) and the archive lead time is 7 days (assumed), so a history is exported before retention removes it.
- The SIT namespace holds the smoke workflow and synthetic histories for the drills; no production data is used.
- The approved server release is recorded in the environment design, and the next minor release is available to SIT.
- The platform login that runs the archive run and the drills, its task-queue provisioning record, the owner of the backup and restore right, the immutability period of the container and the approved server and SDK release are Not specified in the source documents (GAP-1447; ASM-2542).
- The feature flag `rwb.p3.temporal` is on in SIT, read through the parameters contract rather than from a code constant.
- No approval is required to start: the story is Draft (realignment v1) and builds against the published contracts and their fakes.

### 4. Flow

1. TemporalBackupPolicy: automated backups and point-in-time restore run on both databases, and the window, the schedule and the owner role are recorded as configuration of the flexible server.
2. Restore drill, run as `ResilienceDrillWorkflow` with mode `RESTORE`: note the workflows running at the restore point; restore `temporal` and `temporal_visibility` to one timestamp on a new server; repoint the frontend; start the workers; compare the workflow count and the last event of each workflow; record the elapsed time against the ACE recovery time objective.
3. Restore consistency check: `compareVisibilityWithHistory` reads the visibility records and the history presence through the Temporal frontend on the new server, and reports the workflows that exist in one and not the other before any worker starts.
4. Zone failover drill: fail the primary availability zone of the flexible server; the server fails over; the frontend reconnects; start and complete the smoke workflow; compare the running count before and after and record the failover time.
5. Upgrade drill: read the upgrade run book; drain the workers; upgrade the server by one minor release with Helm; run the schema tool; start the workers with the matching SDK; run the smoke workflow; sample the running workflows; record the pinned release in the environment design.
6. `HistoryArchiveJob` at 02:00 on task queue `rwb-platform`: starts `TemporalHistoryArchiveWorkflow`, which lists the CLOSED workflows whose close time is older than the archive lead time, exports each history through the Temporal frontend API, runs the payload check, writes the file at `dt=yyyy-mm-dd/<workflowId>/<runId>.json.gz` and the manifest row to Blob, reads the file back and compares the checksum.
7. `TemporalHistoryArchiveWorkflow`: marks a written row VERIFIED on a matching checksum; a failed write, a failed read-back or a failed payload check marks it FAILED, retries up to three times in the run and raises an incident; retention is left to remove the visibility record.
8. RW-AUDIT: lists the archive and opens a verified history file; the payloads stay encrypted and are decoded only through the codec server of RWB-PLT-E2038-APP.
9. Platform administrator: records each drill, the archive totals and the Schedule history as release evidence; a failed drill blocks the release.

The archive run is a Schedule-started workflow run, not a Quartz job and not a daemon: each 02:00 run is one short run on task queue `rwb-platform` with overlap policy SKIP, so a slow run never stacks behind itself (DP-10). The three drills, the run books and the archive rules are the legacy behaviour with its values unchanged.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A drill restores `temporal` and `temporal_visibility` to different timestamps | `compareVisibilityWithHistory` reports the workflows in visibility with no history in the history store and the reverse; no worker is started against the pair; the drill is recorded as failed with both timestamps | None (drill evidence) | AC6 |
| X2 | The archive read-back checksum differs, or the Blob write fails | The row is marked FAILED and not VERIFIED; the run retries the export up to three times in the same run; an incident reaches RW-PLATADM and RW-AUDIT | None (incident only) | AC7 |
| X3 | An upgrade proposes a target two minor releases later | VersionStepCheck refuses the upgrade before any pod is replaced and names the missing intermediate release | None (pipeline failure) | AC8 |
| X4 | An exported history holds a payload that is not codec-encrypted | `checkArchivePayload` finds the pattern, the file is not written, the row is FAILED and an incident reaches RW-SECADM and RW-PLATADM | None (incident only) | AC9 |
| X5 | A value the build needs is named by no read source (the platform login, the task-queue provisioning record, the owner of the restore right, the immutability period, the approved releases) | The value is used as the working read of the assumption, the placeholder is written where the value is still open, and the gap stays open; no code constant is written for it | Not specified in the source documents (GAP-1447; ASM-2542) | Section 13 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Adds one backup policy, three drill run books, one version check and one archive Schedule on the platform of RWB-PLT-E1070 and the worker of RWB-PLT-E1071; builds against RWB-PLT-E2039-CON and its fakes |
| Negotiable | The backup window, the archive lead time, the container, the immutability period, the retry count and the releases are configuration; the one-timestamp restore and the write-once archive are fixed |
| Valuable | The engine comes back after a zone loss, a restore or an upgrade, and a closed history outlives the retention |
| Estimable | One backup policy, three drill run books, one consistency check, one version check, one archive Schedule and its activities |
| Small | Fits two weeks with its drills |
| Testable | Each criterion in section 7 is one test or one recorded drill in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Temporal resilience: backup, failover, upgrade and archive

  Background:
    Given the Temporal cluster of RWB-E1-070 runs in SIT with databases temporal and temporal_visibility on the zone-redundant PostgreSQL flexible server
    Given the worker of RWB-E1-071 polls task queue `rwb-platform` and runs the smoke workflow
    Given retention is 30 days and the archive lead time is 7 days

  Scenario: AC1 A point-in-time restore brings the workflows back (legacy RWB-E2-039 AC1)
    Given workflow "case-RW-2026-000201" started at 09:40 on 16 November 2026 and completed activity "ReadAceSnapshot" at 09:42
    Given it waits on a timer that fires at 10:00 and was RUNNING at the restore point 09:55
    Given workflow "case-RW-2026-000202" started at 10:00, after the restore point
    When the platform administrator restores temporal and temporal_visibility to 09:55 on a new server in SIT
    Then the namespace rwb-recovery is REGISTERED and the frontend points at the new server
    Then the workers reconnect and "case-RW-2026-000201" continues when its timer fires
    Then its history holds one WorkflowExecutionStarted, one TimerStarted, one ActivityTaskCompleted and one TimerFired
    Then activity "ReadAceSnapshot" wrote one row under its idempotency key and did not run twice
    Then "case-RW-2026-000202" is absent and the run book says the caller starts it again, inside the recovery point objective
    Then the drill records the elapsed time against the ACE recovery time objective (NFR-023)

  Scenario: AC2 A zone failover completes the smoke workflow (legacy RWB-E2-039 AC2)
    Given 12 workflows are RUNNING in rwb-recovery at 14:00 on 16 November 2026
    When the primary availability zone of the PostgreSQL flexible server fails at 14:00 and the server fails over
    Then the frontend reconnects without a manual change and the namespace is REGISTERED
    Then the smoke workflow "platform-smoke-20261116" starts at 14:06 and ends COMPLETED
    Then the count of RUNNING workflows at 14:10 is 12
    Then no history holds a gap or a duplicate event
    Then the drill records the failover time against the ACE recovery time objective (NFR-023)

  Scenario: AC3 A one-minor upgrade loses no workflow (legacy RWB-E2-039 AC3)
    Given SIT runs the approved server version and the next minor version is available
    Given 5 workflows are RUNNING on task queue `rwb-platform`
    When the run book is followed: the workers are drained, the server is upgraded with Helm, the schema tool runs, and the workers start with the matching SDK
    Then the 5 workflows are RUNNING or COMPLETED after the upgrade with the same workflow ID and run ID
    Then no history holds a gap or a duplicate event
    Then the smoke workflow completes after the upgrade
    Then Environment and Deployment Design v4 records the next minor version as the pinned version

  Scenario: AC4 A closed history is archived and readable by RW-AUDIT (legacy RWB-E2-039 AC4)
    Given workflow "case-RW-2026-000101" closed COMPLETED on 16 October 2026
    When the archive job runs at 02:00 on 23 October 2026
    Then the history is written to Blob at dt=2026-10-23/case-RW-2026-000101/<runId>.json.gz
    Then the manifest row names the workflow ID, run ID, workflow type, close time, archive time, path and checksum, and its status is VERIFIED
    Then the visibility record is left to the 30-day retention and is gone on 15 November 2026
    When RW-AUDIT lists the archive on 16 November 2026
    Then the file is listed and readable and its checksum matches the manifest

  Scenario: AC5 The archive holds no clear personal data (legacy RWB-E2-039 AC5)
    Given the archived history of "case-RW-2026-000101" holds a salary slip payload with the synthetic national ID "1101700203456"
    When RW-AUDIT opens the file
    Then the payload is binary ciphertext with codec metadata naming key version 2
    Then the string "1101700203456" appears nowhere in the file, the manifest or the archive log
    Then the manifest holds the workflow ID, type and timestamps and no personal data field
    Then a clear read needs the codec server of RWB-E2-038 with an open break-glass grant

  Scenario: AC6 The two databases are restored to one timestamp (legacy RWB-E2-039 AC6)
    Given a drill restores temporal to 09:55 and temporal_visibility to 10:05
    When the frontend starts against the restored pair
    Then the consistency check reports workflows in visibility with no history in the history store
    Then no worker is started against the pair
    Then the run book says to restore both databases to one timestamp and repeat the drill
    Then the drill is recorded as failed with both timestamps

  Scenario: AC7 The archive verifies every file (legacy RWB-E2-039 AC7)
    Given the archive job writes the history of "case-RW-2026-000102" and the read-back checksum differs
    When verification runs
    Then the manifest row is FAILED with the reason and the file is not marked VERIFIED
    Then the job retries the export up to three times in the same run
    Then an incident reaches RW-PLATADM and RW-AUDIT
    Then the next run re-exports the history and the row becomes VERIFIED

  Scenario: AC8 An upgrade skips no minor version (legacy RWB-E2-039 AC8)
    Given SIT runs the approved server version and the proposed target is two minor versions later
    When the version step check runs in the pipeline and the run book is read
    Then the upgrade is refused before any pod is replaced
    Then the error names the missing intermediate version
    Then the approved path is one minor version, verify, then the next

  Scenario: AC9 A history with a clear payload is not archived (legacy RWB-E2-039 AC9)
    Given a SIT test workflow wrote its payload with the codec off, so its history holds the national ID "1101700203456" in clear text
    When the archive job exports that history
    Then the payload check finds the pattern and the file is not written
    Then the manifest row is FAILED and an incident reaches RW-SECADM and RW-PLATADM
    Then the test workflow is deleted and the test profile is corrected before the next run
```

The nine criteria above are copied from RWB-E2-039 with every value kept: case-RW-2026-000101, case-RW-2026-000102, case-RW-2026-000201, case-RW-2026-000202, "ReadAceSnapshot", 09:40, 09:42, 09:55, 10:00, 10:05, 12 workflows at 14:00, 14:06, 14:10, 5 workflows, 30 days, 7 days, 02:00 on 23 October 2026, dt=2026-10-23/case-RW-2026-000101/<runId>.json.gz, 15 November 2026, 16 October 2026, 16 November 2026, the national ID 1101700203456, key version 2, three retries, NFR-023 and the smoke workflow platform-smoke-20261116. The realignment changes no value and adds no scenario; it changes the mechanism and the phrasing: the 02:00 archive job is `HistoryArchiveJob`, a Temporal Schedule on task queue `rwb-platform` in namespace `rwb-recovery` instead of the legacy Quartz job (DP-10; the Quartz scheduler is retired with RWB-TE-007), the consistency check is the `compareVisibilityWithHistory` activity of this story, the payload check is `checkArchivePayload` of RWB-PLT-E2039-CON's result contract, the decode of AC5 is the codec server of RWB-PLT-E2038-APP, and the pinned version of AC3 stays the record that Environment and Deployment Design v4 names, carried to its next version in the target. The only textual change inside the criteria is the queue phrasing, which names task queue `rwb-platform`; every identifier, timestamp, count and national ID stands as it was written.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Automated backups and point-in-time restore run on both Temporal databases, and a restore goes to a new server at one timestamp for both databases, never in place on the live server | D-RCV-36 T1; RWB-PLT-E1070-CON; AC1, AC6 |
| BR2 | A restore and a failover are measured against the ACE recovery point objective and recovery time objective; the values are DL11 and are not set in code | NFR-022, NFR-023; RWB-PLT-E1042-CON |
| BR3 | The server is zone redundant, and a zone failover is tested in SIT at each release with the smoke workflow as the proof | RWB-PLT-E1070-CON; AC2 |
| BR4 | An upgrade moves one minor release at a time: workers drained, server upgraded, schema tool run, workers started with the matching SDK, release pinned and recorded in the environment and deployment design | D-RCV-36 T7; RWB-PLT-E1071-CON; AC3, AC8 |
| BR5 | A closed history is exported before retention removes it; the archive lead time is 7 days against a 30-day retention, and both are parameters | RWB-PLT-E1042-CON (DP-06); AC4 |
| BR6 | The archive is write-once for its period, checksummed and indexed by one manifest row with its status | RWB-PLT-E2039-CON; AC4, AC7 |
| BR7 | The archive holds codec-encrypted payloads only; a history that fails the payload check is not written and raises an incident to RW-SECADM | NFR-045; RWB-PLT-E2039-CON; AC9 |
| BR8 | RW-AUDIT lists and reads the archive; decode stays with the codec server of RWB-PLT-E2038-APP and its break-glass grant | RWB-PLT-E2038-APP; RWB-P4-E1039-CON; AC5 |
| BR9 | A drill result is release evidence with its timestamps and counts, and a failed drill blocks the release | REQ-DRI-007; AC1, AC2, AC6 |
| BR10 | The backup window, the archive lead time, the container, the immutability period, the retry count and the releases are configuration, never code | REQ-DRI-007; RWB-PLT-E1042-CON; RWB-PLT-E1043-CON |

### 9. State transitions

None for a case. The engine, a workflow execution, an archive row and the archive Schedule change state.

| From | Event | Condition | To |
|---|---|---|---|
| RUNNING (server) | Zone failover | - | RUNNING on the secondary zone |
| RUNNING (server) | Minor upgrade | Workers drained | RUNNING at the next minor release |
| RUNNING (workflow) | Restore to an earlier point | The workflow started before the point | RUNNING at the restored point |
| CLOSED (workflow) | Archive export by `HistoryArchiveJob` | 7 days after close | Manifest row WRITTEN |
| WRITTEN | Verification | The checksum matches | VERIFIED |
| WRITTEN | Verification | The checksum differs or the payload check fails | FAILED, and retried up to three times in the run |
| CLOSED (workflow) | Retention 30 days | Archived or not | Removed from visible history and visibility |
| VERIFIED | Archive retention ends | The immutability period has passed | Disposed by the archive retention decision |
| Scheduled (`HistoryArchiveJob`) | 02:00 fires while the previous run is open | Overlap policy SKIP | No new run; the open run finishes |

The manifest states WRITTEN, VERIFIED and FAILED are the reference values of RWB-PLT-E1043-CON and are read, never hard-coded; a drill has the states Planned, Passed and Failed with its timestamps. The engine and workflow states COMPLETED, RUNNING, FAILED and TIMED_OUT are Temporal's and live in its persistence and visibility, never in a `rwb_*` schema. The archive Schedule's own state is Temporal's, and this story reads the Schedule history rather than writing a job table.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM | Runs the backup, restore, failover and upgrade steps; runs the archive run and reads its result (Platform administration, U) |
| RW-AUDIT | Lists and reads the archive and the manifest (Platform administration and Decision log, R) |
| RW-SECADM | Receives a payload-check incident and decodes an archived history through RWB-PLT-E2038-APP only |
| RW-TRIBE | Maintains the backup policy, the drill scripts and the run books through the change process; may not restore PROD |
| SY-CASEWF | Runs the archive run and the drills and writes the Blob files and manifest rows |
| SY-RULES | No part in this story |
| The operations group | Holds the restore right on the PostgreSQL flexible server and the Blob data roles; the platform administrator acts through it |
| The platform identity that runs the archive run and the drills | Not specified in the source documents (GAP-1447; ASM-2542) |
| No delegation of authority level applies | A restore or an upgrade is not a credit decision |

Separation of duty: the platform administrator who runs a drill is not the auditor who reads its evidence, and no person signs off their own restore or upgrade drill.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| None (platform enabler) | None in a `rwb_*` schema | None | None |

No BR field is read or written and this story owns no table. Backup and restore state lives in the PostgreSQL flexible server and its backup store; workflow, timer and task state lives in Temporal persistence and visibility (RWB-PLT-E1070-APP); the archived histories and the manifest live in Azure Blob container `rwb-temporal-archive`. The archive Schedule's owner role, schedule text and run book path are configuration of the platform, not a catalogue row: the Ownership Map ruling is that each service's Schedules are not rows in `job_catalog`, so this story writes no `job_catalog` row and creates no table. `decision_log_entry` stays with rwb-decision (P7) and this story writes no entry to it, through DecisionLogApi or otherwise. No DF-REF, DF-CAS or DF-DEC field is added or changed, the Physical Schema is unchanged, and Temporal's own tables are not in the Physical Schema.

### 12. Contract

#### 12.1 REST operations provided

None. The platform has no service short (Template and Rules §R4 has no platform row), so it publishes no path under `/api/recovery/<short>/v1` and no Workbench endpoint (DP-13). The operator surfaces are the drill run books, the Schedule history, the dashboard of RWB-PLT-E2037-APP and the Azure portal listing of the archive container, none of which is a Workbench route (DP-19).

#### 12.2 REST operations consumed

None. The parameters, the reference values and the decision-record library are read in process through the published contracts RWB-PLT-E1042-CON, RWB-PLT-E1043-CON and RWB-PLT-E1027-CON, and the cluster, the frontend and Blob storage are Azure and Temporal surfaces, not service REST operations. This story calls no service over REST and adds no read to another service's API.

#### 12.3 Events published

None. The platform owns no topic, publishes no `rwb.<short>.events.v1` and has no event schema of its own (DP-14). The only event in the neighbourhood is `DecisionRecorded` on `rwb.decision-record.v1`, which belongs to the decision-record library of RWB-PLT-E1027-CON and is published from a caller's transaction; this story writes no decision record, so it publishes nothing.

#### 12.4 Events consumed

None. The archive run reads Temporal visibility and the history export through the frontend API, and the drills read the same API and the Azure control plane; no Kafka topic reaches this story and it subscribes to none.

#### 12.5 Workflows and activities

| Name | Type | Runs on | Purpose |
|---|---|---|---|
| `ResilienceDrillWorkflow` | Workflow | `rwb-platform` | One drill per run with mode RESTORE, FAILOVER or UPGRADE: the steps of section 4, the comparison of counts, the consistency check and the recorded evidence (BR1 to BR4, BR9) |
| `TemporalHistoryArchiveWorkflow` | Workflow, started by the `HistoryArchiveJob` Schedule | `rwb-platform` | The 02:00 archive: list, export, check, write, verify and raise the incident (BR5 to BR7) |
| `compareVisibilityWithHistory` | Activity | `rwb-platform` | Reads visibility records and history presence through the Temporal frontend on the restored server and reports the mismatch before any worker starts (AC6) |
| `checkArchivePayload` | Activity | `rwb-platform` | Refuses a history that holds a payload without codec metadata or a clear personal-data pattern (BR7, AC9) |
| `writeArchiveFile` | Activity | `rwb-platform` | Writes the history at `dt=yyyy-mm-dd/<workflowId>/<runId>.json.gz` and the manifest row, with the immutability header the container requires (BR6) |
| `verifyArchiveChecksum` | Activity | `rwb-platform` | Reads the file back, compares the checksum and sets the row VERIFIED or FAILED (AC7) |
| `recordDrillEvidence` | Activity | `rwb-platform` | Writes the drill evidence of RWB-PLT-E2039-CON with its timestamps and counts, and the archive totals, as release evidence (BR9) |

No other workflow is started and no activity of this story runs on a service task queue: every run of this story polls `rwb-platform` in namespace `rwb-recovery`, and the platform worker of RWB-PLT-E1071 executes it. The drills are started by the platform administrator through the workflow client; only the archive has a Schedule.

#### 12.6 Schedules

| Schedule | Cadence | Task queue | Legacy reference |
|---|---|---|---|
| `HistoryArchiveJob` | Daily at 02:00, overlap policy SKIP, catch-up window | `rwb-platform` | The legacy daily 02:00 archive job, carried by a Temporal Schedule instead of Quartz (DP-10; RWB-TE-007 retired) |

The Schedule is created from the workflow kit template of RWB-PLT-E1071-CON in namespace `rwb-recovery`, with the retention and tenant of the platform namespace. Its catch-up window and overlap policy are configuration, and a second bootstrap run changes nothing. No drill has a Schedule: a drill is run on purpose, by the platform administrator, and is never on a timer.

#### 12.7 Tables owned

None. The platform owns no `rwb_*` schema and no migration (DP-01, DP-15). The archived files and the manifest are Blob objects in `rwb-temporal-archive`; workflow and visibility state are Temporal's; `decision_log_entry` is rwb-decision's (P7) and is written only through DecisionLogApi, which this story does not call. No table of another service is read.

#### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| Archive store fake (RWB-PLT-E2039-CON) | The container path rule `dt=yyyy-mm-dd/<workflowId>/<runId>.json.gz`, the manifest row shape, the immutability refusal on a repeated write and the read-back with its checksum | The archive tests of AC4 and AC7 and the write-order tests of section 13 |
| History export fake (RWB-PLT-E2039-CON) | A CLOSED workflow with a history, a history with a payload without codec metadata and a history with a clear national ID, exported through the declared frontend call | AC4, AC5, AC7 and AC9 |
| Drill evidence fake (RWB-PLT-E2039-CON) | The evidence record with the drill mode, the timestamps, the counts and the Planned, Passed and Failed states | AC1, AC2, AC6 and BR9 |
| Consistency-check fake (RWB-PLT-E2039-CON) | A visibility record with no history, a history with no visibility record and a matched pair | AC6 |
| Fake frontend (RWB-PLT-E1070-CON) | A Temporal dev server with namespace `rwb-recovery`, its retention, the declared frontend API subset, the typed errors and the seeded smoke workflow `platform-smoke-20261116` | Every drill test and the archive list step |
| Workflow-kit Schedule fake (RWB-PLT-E1071-CON) | The Schedule template, the overlap policy SKIP and a run's task-queue and namespace values | The Schedule test of 12.6 and the configuration tests of section 13 |
| Parameters and reference-data fakes (RWB-PLT-E1042-CON, RWB-PLT-E1043-CON) | `temporal.retention.days` = 30, the archive lead time of 7 days, the manifest statuses and the drill states | The configuration tests and AC4 |

The fakes are test-only; they are not deployed into SIT, UAT or production, and no environment value points at one.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 0 | No Workbench endpoint and no service read; the cluster, the frontend and Blob are Azure and Temporal surfaces |
| Kafka | 0 | 0 | No topic of its own; the decision-record event belongs to RWB-PLT-E1027-CON and is not used here |
| Temporal | 2 workflows (`ResilienceDrillWorkflow`, `TemporalHistoryArchiveWorkflow`), 5 activities and 1 Schedule (`HistoryArchiveJob`, 02:00) | 0 | Namespace `rwb-recovery`, task queue `rwb-platform`, overlap policy SKIP |
| File | 1 write and 1 read-back per archived history | 1 read-back of the same file | `dt=yyyy-mm-dd/<workflowId>/<runId>.json.gz` in `rwb-temporal-archive`, immutable; the manifest row travels with the file |

### 13. Solution plan

**Package.** The drill workflow, the archive workflow and their activities in the platform workflow module (Java package `th.co.scb.ace.workbench.recovery.workflow.resilience`); the backup policy and the drill scripts in `deploy/temporal/resilience/`; the Helm and schema-tool steps in the deployment pipeline; the run books in `docs/operations/runbooks/`. The deployment names of the drill and archive workers follow the platform template of RWB-PLT-TPL and are Not specified in the source documents (GAP-1447; ASM-2542).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TemporalBackupPolicy | Configuration as code | The backup schedule, the point-in-time window and the owner role on the flexible server (BR1) |
| RestoreRunBook | Document | The one-timestamp restore steps, the frontend repoint, the worker start and the count comparison (BR1, AC1, AC6) |
| RestoreConsistencyCheck | Service, backed by `compareVisibilityWithHistory` | Compares visibility records with history presence and refuses a mismatched pair (AC6) |
| ZoneFailoverDrill | Script, run as `ResilienceDrillWorkflow` mode FAILOVER | Fails the primary zone, waits for the server, starts the smoke workflow and records the time (BR3, AC2) |
| UpgradeRunBook | Document | Drain, upgrade, schema tool, worker start, verification and the pinned release record (BR4, AC3) |
| VersionStepCheck | Pipeline check | Refuses a target more than one minor release ahead and names the missing intermediate release (AC8) |
| `HistoryArchiveJob` | Temporal Schedule | Daily at 02:00, overlap policy SKIP, starts `TemporalHistoryArchiveWorkflow` on task queue `rwb-platform` (BR5, DP-10) |
| ArchivePayloadCheck | Service, backed by `checkArchivePayload` | Refuses a history that holds a payload without codec metadata or a clear personal-data pattern (BR7, AC9) |
| ArchiveManifestStore | Repository | Writes and reads the manifest rows and their status in Blob (BR6, AC4, AC7) |
| ArchiveReadRole | Configuration | The Storage Blob Data Reader assignment for RW-AUDIT on the archive container (BR8) |

**Database.** No migration and no new table. This story runs no Flyway sequence (DP-15 declared, not used) and owns no `rwb_*` schema (DP-01); the archive and the manifest live in Blob storage and the persistence stores belong to RWB-PLT-E1070-APP.

**Configuration and reference data**

- `temporal.retention.days` = 30 (DL26) and the archive lead time of 7 days, both read as parameters through RWB-PLT-E1042-CON and never as code constants (DP-06).
- The backup schedule and the point-in-time window on the flexible server, owned by the operations group.
- The container `rwb-temporal-archive`, its write-once (immutable) period for the archive period and the retry count of 3; the immutability period is Not specified in the source documents (GAP-1447; ASM-2542) and is published as the working read of that assumption.
- The approved server release and the next minor release, recorded in the environment and deployment design (D-RCV-36 T7); the release numbers are Not specified in the source documents (GAP-1447; ASM-2542).
- The manifest statuses WRITTEN, VERIFIED and FAILED and the drill states Planned, Passed and Failed are read as reference values through RWB-PLT-E1043-CON (DP-07), not written as literals.
- Feature flag `rwb.p3.temporal` through the parameters contract. Off: no workflow runs, the archive run finds nothing to export and the drills are not run in that environment; the cluster, the backups and the container stay in place.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**DP-10** is the substantive row of this story: the legacy archive job was a Quartz trigger at 02:00 inside the monolith, and in the target it is `HistoryArchiveJob`, a Temporal Schedule on task queue `rwb-platform` every day at 02:00 with overlap policy SKIP, whose run is the short `TemporalHistoryArchiveWorkflow` (Architecture v5 slide 44; Ownership Map jobs; DP-10). The workflow kit of RWB-PLT-E1071-CON supplies the Schedule and the run, so the archive needs no scheduler table, no cluster-wide cron and no second job store, and the retired Quartz scheduler (RWB-TE-007) is not re-implemented anywhere. **DP-06** and **DP-07** keep the numbers out of the code: the retention, the lead time and the flag are parameter values and the statuses and drill states are reference values, so a retention or lead-time change is a configuration change and not a release. **DP-03** is declared and not exercised: a drill result and an archive row are operational state, never a credit decision, so this story writes no decision record; the dependency stays because the archive run and the drills execute on the platform worker built from the service template, which wires the local decision-record library of RWB-PLT-E1027-CON. **DP-01**, **DP-05**, **DP-13**, **DP-14**, **DP-15** and **DP-19** are declared as absences, which is what a platform story owes the split: no `rwb_*` schema is read or written, no ACE view and no extension table is read, no `/api/recovery` base is published, no topic is owned, no migration runs, and the archive listing is the Azure portal rather than a gateway route.

**Build steps**

1. Write `TemporalBackupPolicy` and prove the point-in-time window on the SIT server; test AC1 with the synthetic workflows.
2. Build `RestoreConsistencyCheck` and the restore run book; drill AC1 and AC6 on a new server.
3. Build the zone failover drill and run AC2 in SIT with the smoke workflow, recording the failover time.
4. Write the upgrade run book and `VersionStepCheck`; drill AC3 and AC8 against the approved release.
5. Build `TemporalHistoryArchiveWorkflow`, `checkArchivePayload`, `writeArchiveFile`, `verifyArchiveChecksum` and `ArchiveManifestStore`; test AC4, AC5, AC7 and AC9 on synthetic histories.
6. Create the container, the write-once policy and the RW-AUDIT read role, and prove a listed and readable file against its manifest.
7. Register `HistoryArchiveJob` on task queue `rwb-platform` at 02:00 with overlap policy SKIP and prove a second bootstrap changes nothing.
8. Run the full drill set in SIT and record every result as release evidence with its timestamps and counts, then read the Schedule history as the cadence proof.

**Done when.** The restore, failover and upgrade drills pass in SIT, a history closed 31 days ago is readable in the archive, the payload check refuses a history with a clear payload, the Schedule history shows the daily 02:00 runs, and the drill evidence is in the release record.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-037 | A drill leaves a workflow failed or not moving, as any other workflow failure | Workflow {workflowId} has failed or has not moved for {hours} hours. |

This story adds no message. A failed drill is recorded in the release evidence and raised as an incident to RW-PLATADM, and a failed archive row is raised as an incident to RW-PLATADM and RW-AUDIT; a payload-check failure is raised to RW-SECADM and RW-PLATADM. The workflow alerts are those of RWB-PLT-E2037-APP and reuse MSG-P3-037 unchanged. X3's pipeline failure names the refused target and the missing intermediate release, and it uses no message identifier; the platform has no `/api/recovery` base, so no operator signal of this story is a screen error.

### 15. Screens and states

No Workbench screen in this story. The operational views are the Temporal Web UI, the Grafana dashboard of RWB-PLT-E2037-APP and the Azure portal listing of the archive container with the manifest. The manifest row has the states WRITTEN, VERIFIED and FAILED; a drill has the states Planned, Passed and Failed with its timestamps and counts. The archive Schedule's last run, status and duration are read from the Schedule history, and the platform screens of Epic 8 do not repeat this data.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-039-01 | AC1, BR1, BR2 | Integration | Restore point 09:55; case-RW-2026-000201 started 09:40; case-RW-2026-000202 started 10:00 |
| TC-E2-039-02 | AC2, BR3 | NFR | Zone failover at 14:00; 12 running workflows; smoke workflow started 14:06 |
| TC-E2-039-03 | AC3, BR4 | Integration | One-minor upgrade in SIT; 5 workflows running on `rwb-platform` |
| TC-E2-039-04 | AC4, BR5, BR6 | Integration | History closed 16 October 2026; export on 23 October 2026; read on 16 November 2026 |
| TC-E2-039-05 | AC5, BR7, BR8 | Integration | Archived salary slip payload with national ID 1101700203456 |
| TC-E2-039-06 | AC6, BR1 | Integration | Restore temporal to 09:55 and temporal_visibility to 10:05 |
| TC-E2-039-07 | AC7, BR6 | Component | Read-back checksum changed; three retries |
| TC-E2-039-08 | AC8, BR4 | Component | Target two minor versions ahead of the approved version |
| TC-E2-039-09 | AC9, BR7 | Component | History written with the codec off; clear national ID in the payload |
| TC-E2-039-10 | Operational | NFR | Archive reconciliation: every closed workflow older than the retention has a VERIFIED row |
| TC-E2-039-11 | Operational | NFR | Restore drill evidence recorded with the ACE recovery time objective measured |

The eleven test cases are the legacy test cases of RWB-E2-039 with their identifiers and their data unchanged. Legacy levels map System to Integration and Operational to Component or NFR, as above: the drills that measure a recovery time objective keep the NFR level, and the archive reconciliation keeps it too because it is the completeness measure of the whole retention window. The drills are run by the platform administrator and the operations group in SIT and recorded in the release evidence; there is no Workbench endpoint and no Access test in this story. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the backup window, the retention, the archive lead time, the container, the immutability period, the retry count and the releases are configuration read through the published contracts.
- No personal data in logs, tests, workflow history, archived files or prompts: the archive holds codec-encrypted payloads only, the manifest holds identifiers and timestamps and no personal data field, and the drill data is synthetic.
- No read of another service's tables and no ACE view: this story reads no case table, no ACE table and no `rwb_*` schema, and the archive listing is Blob and the Azure portal (DP-01, DP-05).
- A restore is never made in place on the live server, and both databases are restored to one timestamp before any worker starts.
- No upgrade by more than one minor release, and no upgrade without draining the workers first.
- No archived file without a manifest row and a matching checksum, and no file with a clear payload is written.
- Retention is never extended or shortened by this story: the archive run goes before retention and leaves the deletion to Temporal, and the value stays DL26.
- No drill result is recorded as passed without its timestamps and counts, and a failed drill blocks the release.
- No Quartz, no scheduler table and no second job store: the archive is `HistoryArchiveJob`, a Temporal Schedule on task queue `rwb-platform` at 02:00 (DP-10).
- No platform topic, no platform `/api/recovery` base and no `rwb_*` schema: the platform is not one of the 19 services (DP-13, DP-14, §R4).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-007 | Every failure reaches a named owner and has a tested way back | Epic 2, 3.2; Program, 6.4 | None (platform enabler) | All recovery processes | R-UNI-40 | TC-E2-039-01, TC-E2-039-02, TC-E2-039-03, TC-E2-039-04, TC-E2-039-06, TC-E2-039-07, TC-E2-039-08, TC-E2-039-09, TC-E2-039-10 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E2039-CON | Contract | H: publishes the drill evidence schema, the archive path and manifest schema, the consistency-check query contract, the payload-check result and the version-step rule, with the fakes this story builds against |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library the platform worker template wires; no drill and no archive row is a decision, so this story writes no entry (DP-03 declared, not exercised) |
| RWB-PLT-E1042-CON | Contract | H: the parameters the retention, the lead time and the flag are read through (DP-06) |
| RWB-PLT-E1043-CON | Contract | H: the reference values behind the manifest statuses and the drill states (DP-07) |
| RWB-PLT-E1071-CON | Contract | H: the workflow kit, the platform worker on task queue `rwb-platform` and the Schedule template `HistoryArchiveJob` uses (DP-10) |
| RWB-PLT-E1047-CON | Contract | H: the naming library; the platform owns no topic and this story publishes none (DP-14) |
| RWB-PLT-E1044-CON | Contract | H: the Flyway convention this story deliberately does not use (DP-15) |
| RWB-PLT-N001-CON | Contract | H: gateway-bff; the archive listing is the Azure portal, not a Workbench route (DP-19) |
| RWB-PLT-E1070-CON | Contract | H: the cluster, the persistence stores, namespace `rwb-recovery`, mTLS, the client certificate profile and the frontend API the drills and the export read |
| RWB-PLT-E2037-CON | Contract | H: the dashboard and alert contract the drills are observed on |
| RWB-P3-E1042-CON, RWB-P3-E1043-CON | Contract | C: the owner contracts behind the parameters and reference-data reads (DP-06, DP-07) |
| RWB-PLT-E2040-APP, RWB-PLT-E2040-CON | Successors of RWB-E2-040 | Out of scope: the replay gate, the history export for tests and build ID rollout |
| RWB-PLT-E2038-APP, RWB-PLT-E2038-CON | Successors of RWB-E2-038 | Out of scope: the codec server, decode and the admin audit; the clear read of AC5 needs them |
| RWB-PLT-E2037-APP | App development | The dashboard and alerts the drills are observed on; not changed here |
| RWB-PLT-N003-INF, RWB-PLT-NF08-INF | Infrastructure | Siblings: the namespace `rwb-recovery` and codec key, and the platform baseline the drills run on |

### 19. Out of scope

- The Temporal cluster, the namespace, mTLS, the Web UI and the platform roles (legacy RWB-E1-070; RWB-PLT-E1070-APP, RWB-PLT-E1070-CON).
- The namespace `rwb-recovery` bootstrap and the codec key (RWB-PLT-N003-INF), and the platform baseline the drills run on (RWB-PLT-NF08-INF).
- The worker, the SDK wiring, the codec and the smoke workflow (legacy RWB-E1-071; RWB-PLT-E1071-APP).
- Alerts, the stuck workflow scanner and the workflow dashboard (legacy RWB-E2-037; RWB-PLT-E2037-APP).
- The codec server, decode of an archived payload and the administrative audit (legacy RWB-E2-038; RWB-PLT-E2038-APP).
- The replay gate, the history export for tests and the build ID rollout (legacy RWB-E2-040; RWB-PLT-E2040-APP).
- Disaster recovery of the ACE AKS cluster itself and the region pair, which follow the ACE platform plan.
- The retention period itself, which is DL26, and the disposal decision after the archive period.
- Case-level restoration of a single case and any manual replay of a case workflow (Epic 3).
- The contract documents and the fakes themselves: RWB-PLT-E2039-CON.
