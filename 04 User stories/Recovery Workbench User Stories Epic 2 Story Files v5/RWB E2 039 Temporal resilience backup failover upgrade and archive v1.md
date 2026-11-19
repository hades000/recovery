# RWB-E2-039 Temporal resilience: backup, failover, upgrade and archive

SCB Collections and Recovery. Henka Group, 16 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-039 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | None (platform enabler) |
| Requirement IDs | REQ-DRI-007 |
| BRD section | Business Requirements Epic 2, section 3.2; Business Requirements Program, section 6.4 |
| L3 process | All recovery processes |
| Decision | D-RCV-36 (T1); ADR-011 |
| Priority | Must |
| Depends on | RWB-E1-070, RWB-E2-037 |
| Status | Ready for build |

## 1. Story

As a **platform administrator (RW-PLATADM)**, I want **the Temporal databases backed up, the zone failover and a minor upgrade tested, and closed histories archived before retention removes them**, so that **the engine meets the ACE availability targets and an audit can still read a closed workflow after its history has left Temporal**.

## 2. Business rationale

From Epic 3 every live case waits inside a Temporal workflow, so the engine becomes part of the case record: a lost history is a lost case step, and an engine that cannot be restored inside the ACE recovery time objective stops the recovery desk. RWB-E1-070 installs the cluster and RWB-E2-037 alerts when a workflow stops, but neither proves that the data comes back, that a zone loss is survived, that a minor upgrade keeps a running workflow, or that a closed history survives the 30-day retention.

This story adds the four proofs and the one archive: a point-in-time restore of both Temporal databases to one timestamp, a zone failover that completes the smoke workflow, a one-minor upgrade with no lost workflow, and a daily export of closed histories to write-once Blob storage before retention removes them. It meets REQ-DRI-007 (a named owner and a tested way back for every failure). The measure is that every drill passes in SIT inside the ACE recovery time objective, that a history closed 31 days ago is readable in the archive, and that no archived file holds clear personal data.

## 3. Preconditions

- RWB-E1-070 is done: the databases temporal and temporal_visibility on the zone-redundant PostgreSQL flexible server, the namespace rwb-recovery, mTLS, the metrics scrape and the platform run book exist.
- RWB-E2-037 is done: the failed, stuck and latency alerts, the dashboard and their run books exist, so a drill is observed like a live incident.
- The PostgreSQL flexible server has automated backups and point-in-time restore enabled with a window of at least 35 days (assumed); the platform administrator holds the restore right through the operations group.
- The Blob container rwb-temporal-archive exists with a write-once policy for the archive period, and RW-AUDIT holds Storage Blob Data Reader on it.
- Retention is 30 days (temporal.retention.days = 30; assumed, DL26) and the archive lead time is 7 days (assumed), so a history is exported before retention removes it.
- The SIT namespace holds the smoke workflow of RWB-E1-071 and synthetic histories for the drill; no production data is used.
- The approved server version is recorded in Environment and Deployment Design v4, and the next minor version is available to SIT.
- The Quartz scheduler is available for the daily archive job (D-RCV-36 T2); no Temporal Schedule is created.

## 4. Flow

1. Backup policy: automated backups and point-in-time restore run on both databases, and the window, the schedule and the owner are recorded as configuration.
2. Restore drill: note the workflows running at the restore point; restore temporal and temporal_visibility to one timestamp on a new server; repoint the frontend; start the workers; compare the workflow count and the last event of each workflow; record the elapsed time against the ACE recovery time objective.
3. Zone failover drill: fail the primary availability zone of the flexible server; the server fails over; the frontend reconnects; start and complete the smoke workflow; compare the running count before and after.
4. Upgrade: read the upgrade run book; drain the workers; upgrade the server by one minor version with Helm; run the schema tool; start the workers with the matching SDK; run the smoke workflow; sample the running workflows; record the pinned version in Environment and Deployment Design v4.
5. Archive job (Quartz, daily at 02:00): lists CLOSED workflows whose close time is older than the archive lead time, exports each history through the Temporal API, checks the payloads, writes the file and the manifest row to Blob, reads the file back and compares the checksum.
6. Archive job: marks a written row VERIFIED on a matching checksum; a failed write, a failed read-back or a failed payload check marks it FAILED, retries up to three times in the run, and raises an incident; retention is left to remove the visibility record.
7. RW-AUDIT: lists the archive and opens a verified history file; the payloads stay encrypted and are decoded only through RWB-E2-038.
8. Platform administrator: records each drill and the archive totals as release evidence; a failed drill blocks the release.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A drill restores temporal and temporal_visibility to different timestamps | The consistency check reports workflows in visibility with no history; no worker starts against the pair; the drill is recorded as failed with both timestamps | None (drill evidence) | AC6 |
| X2 | The archive read-back checksum differs, or the Blob write fails | The row is marked FAILED and not VERIFIED; the job retries the export up to three times in the run; an incident reaches RW-PLATADM and RW-AUDIT | None (incident only) | AC7 |
| X3 | An upgrade proposes a target two minor versions later | The version step check refuses the upgrade before any pod is replaced and names the missing intermediate version | None (pipeline failure) | AC8 |
| X4 | An exported history holds a payload that is not codec-encrypted | The payload check finds the pattern, the file is not written, the row is FAILED and an incident reaches RW-SECADM and RW-PLATADM | None (incident only) | AC9 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the cluster and databases of RWB-E1-070 and the alerts of RWB-E2-037; it adds the drills, the upgrade check and the archive job |
| Negotiable | The backup window, the archive lead time, the container, the immutability period and the retry count are configuration; the one-timestamp restore and the write-once archive are fixed |
| Valuable | The engine comes back after a zone loss, a restore or an upgrade, and a closed history outlives the retention |
| Estimable | One backup policy, three drill run books, one version check and one archive job |
| Small | Fits two weeks with its drills |
| Testable | Each criterion in section 7 is one test or one recorded drill in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Temporal resilience: backup, failover, upgrade and archive

  Background:
    Given the Temporal cluster of RWB-E1-070 runs in SIT with databases temporal and temporal_visibility on the zone-redundant PostgreSQL flexible server
    Given the worker of RWB-E1-071 polls rwb-platform and runs the smoke workflow
    Given retention is 30 days and the archive lead time is 7 days

  Scenario: AC1 A point-in-time restore brings the workflows back
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

  Scenario: AC2 A zone failover completes the smoke workflow
    Given 12 workflows are RUNNING in rwb-recovery at 14:00 on 16 November 2026
    When the primary availability zone of the PostgreSQL flexible server fails at 14:00 and the server fails over
    Then the frontend reconnects without a manual change and the namespace is REGISTERED
    Then the smoke workflow "platform-smoke-20261116" starts at 14:06 and ends COMPLETED
    Then the count of RUNNING workflows at 14:10 is 12
    Then no history holds a gap or a duplicate event
    Then the drill records the failover time against the ACE recovery time objective (NFR-023)

  Scenario: AC3 A one-minor upgrade loses no workflow
    Given SIT runs the approved server version and the next minor version is available
    Given 5 workflows are RUNNING on task queue rwb-platform
    When the run book is followed: the workers are drained, the server is upgraded with Helm, the schema tool runs, and the workers start with the matching SDK
    Then the 5 workflows are RUNNING or COMPLETED after the upgrade with the same workflow ID and run ID
    Then no history holds a gap or a duplicate event
    Then the smoke workflow completes after the upgrade
    Then Environment and Deployment Design v4 records the next minor version as the pinned version

  Scenario: AC4 A closed history is archived and readable by RW-AUDIT
    Given workflow "case-RW-2026-000101" closed COMPLETED on 16 October 2026
    When the archive job runs at 02:00 on 23 October 2026
    Then the history is written to Blob at dt=2026-10-23/case-RW-2026-000101/<runId>.json.gz
    Then the manifest row names the workflow ID, run ID, workflow type, close time, archive time, path and checksum, and its status is VERIFIED
    Then the visibility record is left to the 30-day retention and is gone on 15 November 2026
    When RW-AUDIT lists the archive on 16 November 2026
    Then the file is listed and readable and its checksum matches the manifest

  Scenario: AC5 The archive holds no clear personal data
    Given the archived history of "case-RW-2026-000101" holds a salary slip payload with the synthetic national ID "1101700203456"
    When RW-AUDIT opens the file
    Then the payload is binary ciphertext with codec metadata naming key version 2
    Then the string "1101700203456" appears nowhere in the file, the manifest or the archive log
    Then the manifest holds the workflow ID, type and timestamps and no personal data field
    Then a clear read needs the codec server of RWB-E2-038 with an open break-glass grant

  Scenario: AC6 The two databases are restored to one timestamp
    Given a drill restores temporal to 09:55 and temporal_visibility to 10:05
    When the frontend starts against the restored pair
    Then the consistency check reports workflows in visibility with no history in the history store
    Then no worker is started against the pair
    Then the run book says to restore both databases to one timestamp and repeat the drill
    Then the drill is recorded as failed with both timestamps

  Scenario: AC7 The archive verifies every file
    Given the archive job writes the history of "case-RW-2026-000102" and the read-back checksum differs
    When verification runs
    Then the manifest row is FAILED with the reason and the file is not marked VERIFIED
    Then the job retries the export up to three times in the same run
    Then an incident reaches RW-PLATADM and RW-AUDIT
    Then the next run re-exports the history and the row becomes VERIFIED

  Scenario: AC8 An upgrade skips no minor version
    Given SIT runs the approved server version and the proposed target is two minor versions later
    When the version step check runs in the pipeline and the run book is read
    Then the upgrade is refused before any pod is replaced
    Then the error names the missing intermediate version
    Then the approved path is one minor version, verify, then the next

  Scenario: AC9 A history with a clear payload is not archived
    Given a SIT test workflow wrote its payload with the codec off, so its history holds the national ID "1101700203456" in clear text
    When the archive job exports that history
    Then the payload check finds the pattern and the file is not written
    Then the manifest row is FAILED and an incident reaches RW-SECADM and RW-PLATADM
    Then the test workflow is deleted and the test profile is corrected before the next run
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Automated backups and point-in-time restore run on both Temporal databases, and a restore goes to a new server at one timestamp for both databases, never in place on the live server | D-RCV-36 T1; AC1, AC6 |
| BR2 | A restore and a failover are measured against the ACE recovery point objective and recovery time objective; the values are DL11 and are not set in code | NFR-022, NFR-023 |
| BR3 | The server is zone redundant, and a zone failover is tested in SIT at each release with the smoke workflow as the proof | AC2 |
| BR4 | An upgrade moves one minor version at a time: workers drained, server upgraded, schema tool run, workers started with the matching SDK, version pinned and recorded in Environment and Deployment Design v4 | AC3, AC8 |
| BR5 | A closed history is exported before retention removes it; the archive lead time is 7 days against a 30-day retention, and both are parameters (assumed) | AC4 |
| BR6 | The archive is write-once for its period, checksummed and indexed by one manifest row with its status | AC4, AC7 |
| BR7 | The archive holds codec-encrypted payloads only; a history that fails the payload check is not written and raises an incident to RW-SECADM | NFR-045; AC9 |
| BR8 | RW-AUDIT lists and reads the archive; decode stays with RWB-E2-038 and its break-glass grant | RWB-E1-039; AC5 |
| BR9 | A drill result is release evidence with its timestamps and counts, and a failed drill blocks the release | REQ-DRI-007 |
| BR10 | The backup window, the archive lead time, the container, the immutability period, the retry count and the version are configuration, never code | REQ-DRI-007 |

## 9. State transitions

None for a case. The engine, a workflow execution and an archive row change state.

| From | Event | Condition | To |
|---|---|---|---|
| RUNNING (server) | Zone failover | - | RUNNING on the secondary zone |
| RUNNING (server) | Minor upgrade | Workers drained | RUNNING at the next minor version |
| RUNNING (workflow) | Restore to an earlier point | The workflow started before the point | RUNNING at the restored point |
| CLOSED (workflow) | Archive export | 7 days after close | Manifest row WRITTEN |
| WRITTEN | Verification | The checksum matches | VERIFIED |
| WRITTEN | Verification | The checksum differs or the payload check fails | FAILED, and retried |
| CLOSED (workflow) | Retention 30 days | Archived or not | Removed from visible history and visibility |
| VERIFIED | Archive retention ends | The immutability period has passed | Disposed by the archive retention decision |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM | Runs the backup, restore, failover and upgrade steps; runs the archive job and reads its result (Platform administration, U) |
| RW-AUDIT | Lists and reads the archive and the manifest (Platform administration and Decision log, R) |
| RW-SECADM | Receives a payload-check incident and decodes an archived history through RWB-E2-038 only |
| RW-TRIBE | Maintains the backup policy, the drill scripts and the run books through the change process; may not restore PROD |
| SY-CASEWF | Runs the archive job and writes the Blob files and manifest rows |
| SY-RULES | No part in this story |
| The operations group | Holds the restore right on the PostgreSQL flexible server and the Blob data roles; the platform administrator acts through it |
| No delegation of authority level applies | A restore or an upgrade is not a credit decision |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| None (platform enabler) | None in the recovery schema | None | None |

Backup and restore state lives in the PostgreSQL flexible server and its backup store, workflow and timer state lives in Temporal persistence and visibility (RWB-E1-070), and the archived histories and the manifest live in Blob storage, container rwb-temporal-archive. The archive job's schedule, owner and run book path live in job_catalog through RWB-E1-056. No DF-REF, DF-CAS or DF-DEC field is added or changed, the Physical Schema v6 is unchanged, and Temporal's own tables are not in the Physical Schema.

## 12. Contract

No Workbench endpoint. This story adds no path under /api/recovery/v1. The interfaces are the database backup service, the Temporal frontend, Blob storage and the deployment tooling.

| Interface | Method | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|
| PostgreSQL flexible server backup and restore | Azure control plane: restore to a new server at a point in time | Resource group, source server, target server, one timestamp for both databases | New server with both databases at the timestamp | Restore outside the window; target name in use; quota | Operations group right on the resource group; no Workbench role | A restore to the same timestamp gives the same result; the target server name is the key |
| Restore consistency check | Read-only comparison through the Temporal frontend | namespace rwb-recovery, visibility records and history presence | Count of workflows in visibility with no history, and the reverse | PERMISSION_DENIED; UNAVAILABLE | Client certificate of SY-CASEWF | Read only |
| Temporal frontend | gRPC over mTLS, port 7233: DescribeNamespace, ListWorkflowExecutions, GetWorkflowExecutionHistory | namespace rwb-recovery, workflow ID, run ID | Namespace, workflow and history summary | TLS handshake failure; NOT_FOUND; UNAVAILABLE | Client certificate of SY-CASEWF with the namespace claim | Read only |
| Blob storage (archive) | HTTPS PUT, GET and LIST on container rwb-temporal-archive | path dt=yyyy-mm-dd/<workflowId>/<runId>.json.gz, file, manifest row | 201 on write; 200 on read; manifest rows on list | 403 role; 409 or 412 immutability; 404 no such file | SY-CASEWF writes; RW-AUDIT reads with Storage Blob Data Reader | The workflow ID and run ID path is the key; a repeated write is refused while the immutability policy holds the file |
| Helm and Temporal schema tool | Deployment pipeline against the SIT and UAT clusters | Chart version, image tag, schema tool at the target version | Release at the target version | Schema version mismatch; pod not ready | RW-PLATADM through the pipeline; no PROD step without the release approval | A second run at the same version changes nothing |

The archive job never writes to the ACE database, and the restore never writes to the live server. RW-AUDIT reads no Temporal database.

## 13. Solution plan

**Package.** No Java business package. The backup policy and the drill scripts live in `deploy/temporal/resilience/`; the archive job lives in `recovery/integration/ops/temporal`; the run books live in `docs/operations/runbooks/`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TemporalBackupPolicy | Configuration as code | The backup schedule, the point-in-time window and the owner on the flexible server (BR1) |
| RestoreRunBook | Document | The one-timestamp restore steps, the frontend repoint, the worker start and the count comparison |
| RestoreConsistencyCheck | Service | Compares visibility records with history presence and refuses a mismatched pair (AC6) |
| ZoneFailoverDrill | Script | Fails the primary zone, waits for the server, starts the smoke workflow and records the time (BR3) |
| UpgradeRunBook | Document | Drain, upgrade, schema tool, worker start, verification and the pinned version record (BR4) |
| VersionStepCheck | Pipeline check | Refuses a target more than one minor version ahead (AC8) |
| HistoryArchiveJob | Job | Quartz, daily at 02:00: list, export, check, write, verify and raise the incident (BR5 to BR7) |
| ArchivePayloadCheck | Service | Refuses a history that holds a payload without codec metadata or a clear personal data pattern (BR7) |
| ArchiveManifestStore | Repository | Writes and reads the manifest rows and their status in Blob |
| ArchiveReadRole | Configuration | The Storage Blob Data Reader assignment for RW-AUDIT on the archive container (BR8) |

**Database.** No migration and no new table. The archive job gets one job_catalog row through RWB-E1-056 as a data change. The archive and the manifest live in Blob storage.

**Configuration and reference data**

- temporal.retention.days = 30 (assumed, DL26) and the archive lead time of 7 days (assumed), through RWB-E1-042.
- The backup schedule and the point-in-time window on the flexible server.
- The container rwb-temporal-archive, its write-once period and the retry count of three.
- The approved server version and the next minor version, recorded in Environment and Deployment Design v4.
- Feature flag rwb.p3.temporal through RWB-E1-047; with it off, no workflow runs and the archive job finds nothing to export.

**Build steps**

1. Write the backup policy and prove the point-in-time window on the SIT server.
2. Build RestoreConsistencyCheck and the restore run book; drill AC1 and AC6.
3. Build the zone failover drill and run AC2 in SIT with the smoke workflow.
4. Write the upgrade run book and the version step check; drill AC3 and AC8.
5. Build HistoryArchiveJob and ArchivePayloadCheck; test AC4, AC5, AC7 and AC9 on synthetic histories.
6. Create the container, the write-once policy and the RW-AUDIT read role; prove a listed and readable file.
7. Run the full drill set in SIT and record every result as release evidence with its timestamps and counts.

**Feature flag.** `rwb.p3.temporal`. Off: no workflow runs, the archive job finds nothing, and the drills are not run in that environment. The cluster, the backups and the archive container stay in place.

**Done when.** The restore, failover and upgrade drills pass in SIT, a history closed 31 days ago is readable in the archive, the archive passes the payload check, and the drill evidence is in the release record.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-037 | A drill leaves a workflow failed or not moving, as any other workflow failure | Workflow {workflowId} has failed or has not moved for {hours} hours. |

This story adds no message. A failed drill is recorded in the release evidence and raised as an incident to RW-PLATADM, and a failed archive row is raised as an incident to RW-PLATADM and RW-AUDIT. The workflow alerts are those of RWB-E2-037 and reuse MSG-P3-037 unchanged.

## 15. Screens and states

No Workbench screen in this story. The operational views are the Temporal Web UI, the Grafana dashboard of RWB-E2-037 and the Azure portal listing of the archive container with the manifest. The manifest row has the states WRITTEN, VERIFIED and FAILED; a drill has the states Planned, Passed and Failed with its timestamps. The Workbench job monitor of RWB-E1-056 shows the archive job's last run, status and duration. The platform screens of Epic 8 do not repeat this data.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-039-01 | AC1, BR1, BR2 | Operational | Restore point 09:55; case-RW-2026-000201 started 09:40; case-RW-2026-000202 started 10:00 |
| TC-E2-039-02 | AC2, BR3 | Operational | Zone failover at 14:00; 12 running workflows; smoke workflow started 14:06 |
| TC-E2-039-03 | AC3, BR4 | Operational | One-minor upgrade in SIT; 5 workflows running on rwb-platform |
| TC-E2-039-04 | AC4, BR5, BR6 | System | History closed 16 October 2026; export on 23 October 2026; read on 16 November 2026 |
| TC-E2-039-05 | AC5, BR7, BR8 | System | Archived salary slip payload with national ID 1101700203456 |
| TC-E2-039-06 | AC6, BR1 | Operational | Restore temporal to 09:55 and temporal_visibility to 10:05 |
| TC-E2-039-07 | AC7, BR6 | System | Read-back checksum changed; three retries |
| TC-E2-039-08 | AC8, BR4 | System | Target two minor versions ahead of the approved version |
| TC-E2-039-09 | AC9, BR7 | System | History written with the codec off; clear national ID in the payload |
| TC-E2-039-10 | Operational | Operational | Archive reconciliation: every closed workflow older than the retention has a VERIFIED row |
| TC-E2-039-11 | Operational | Operational | Restore drill evidence recorded with the ACE recovery time objective measured |

The drills are run by the platform administrator and the operations group in SIT and recorded in the release evidence; there is no Workbench endpoint and no Access test in this story. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the backup window, the retention, the archive lead time, the container and the retry count are configuration.
- No personal data in logs, tests, workflow history or prompts: the archive holds codec-encrypted payloads only, and the drill data is synthetic.
- No read of another module's tables; ACE data only through recovery.v_ace_* views: this story reads no case and no ACE table.
- A restore is never made in place on the live server, and both databases are restored to one timestamp.
- No upgrade by more than one minor version, and no upgrade without draining the workers first.
- No archived file without a manifest row and a matching checksum; no file with a clear payload is written.
- Retention is never extended or shortened by this story; the archive runs before retention and leaves the deletion to Temporal.
- No drill result is recorded as passed without its timestamps and counts.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-007 | Every failure reaches a named owner and has a tested way back | Epic 2, 3.2; Program, 6.4 | None (platform enabler) | All recovery processes | R-UNI-40 | TC-E2-039-01, TC-E2-039-02, TC-E2-039-03, TC-E2-039-04, TC-E2-039-06, TC-E2-039-07, TC-E2-039-08, TC-E2-039-09, TC-E2-039-10 |

## 19. Out of scope

- The Temporal cluster, namespace, mTLS and Web UI (RWB-E1-070).
- The worker, codec and smoke workflow (RWB-E1-071).
- Alerts, the stuck scanner and the dashboard (RWB-E2-037).
- The codec server, decode and the administrative audit (RWB-E2-038).
- The replay gate, history export for tests and build ID rollout (RWB-E2-040).
- Disaster recovery of the ACE AKS cluster itself and the region pair, which follow the ACE platform plan (SCB IT).
- The retention period itself, which is DL26, and the disposal decision after the archive period.
- Case-level restoration of a single case and any manual replay of a case workflow (Epic 3).
