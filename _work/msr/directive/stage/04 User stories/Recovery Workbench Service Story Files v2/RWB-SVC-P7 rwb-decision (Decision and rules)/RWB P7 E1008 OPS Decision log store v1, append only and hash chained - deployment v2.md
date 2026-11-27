# RWB-P7-E1008-OPS Decision log store v1, append only and hash chained - deployment

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: deployment slice of RWB-E1-008 for rwb-decision — the pipeline and the Flyway run at start in schema `rwb_decision`, the drift gate, the configuration and key-store references, the ingest and chain-check jobs with their alerts, the append-only verification job, the backup and restore of an append-only ledger, and the run book. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (10 resolved, 31 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P7-E1008-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 1 |
| Size | Set by the squad at refinement |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP10, DP13, DP15, DP17, DP19 |
| Parallel lane | L-P7-C |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P7-E1008-CON (build status Not started, not Done) |
| Contract version | Not specified in the source documents (DOR-RWB-P7-E1008-OPS-23); /v1 path only |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (FR-P7-001, FR-P7-003, FR-P7-004, FR-P7-005, FR-P7-006, FR-P7-009, FR-P7-010, FR-P7-011, FR-P7-012, FR-P7-013, FR-P7-029, FR-P7-036) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **DevOps engineer of the platform**, I want **the `rwb-decision` service deployed with Flyway running on start in `rwb_decision` under the service's own login, a drift gate before SIT, UAT and PROD, the ingest consumer and the 02:00 chain check running with their alerts, an append-only verification job that proves the grant and the trigger are still in place, a backup and restore procedure that is safe for a ledger nothing may change, and a run book for each failure**, so that **the ledger is deployed, watched, proven immutable and recoverable without a hand ever touching a row**.

This is the deployment slice of legacy RWB-E1-008. It delivers:

- the **pipeline** of the service on the golden template — build, unit and contract tests, image, the migration stage, the API deployment and the worker deployment on the same task queue (ADR-021; Architecture v5 slide 33);
- **Flyway on service start** in `rwb_decision` with the service's own login from the key store, the service's own history table and the two-instance lock, so a start applies exactly the pending migrations of this service (DP-15);
- the **drift gate** before SIT, UAT and PROD: the migrations applied to a clean container and compared with the target schema through a read-only account, and the deployment stopped on a difference;
- the **configuration and the secrets**: the consumer group and its retry and dead-letter topics, the chain algorithm parameters, the 15-minute notice budget, the notification group, the seal target, and every credential as a key-store reference (NFR-052);
- the **ingest consumer and the chain-check job** as operational objects: the consumer lag monitor against the 5-minute completeness target of BR10, the 02:00 Schedule, the incident route and the Compliance notice;
- the **append-only verification job** that queries the catalogue for a missing trigger, a missing function and any UPDATE or DELETE grant on `decision_log_entry`, and fails an alert when one is found (BR2 of the DB story, AC1 of the app story);
- the **backup and restore** of an append-only ledger: point-in-time recovery, a restore into an isolated environment, the chain re-verified from the first entry to the last after the restore, and the seal files in immutable storage used as the external reference of the last hash;
- the **run book**: one entry per failure — a failed migration, a lagging consumer, a dead-lettered envelope, a chain break, a missing seal, a drift finding and a restore.

The eight legacy acceptance criteria stay with `RWB-P7-E1008-APP`; every criterion in section 7 is new (D-RCV-60) and tests only the deployment deliverable.

### 2. Business rationale

A ledger that nothing may change is only as trustworthy as the deployment that surrounds it. Three failure modes are specific to this story and none of them is a code defect:

- **A migration applied by the wrong principal.** The append-only guarantee is a grant plus a trigger. If the pipeline applies migrations as the service login, or if a later migration is run by hand with an owner that grants too much, the first half of the guarantee is gone and nothing notices: the table still looks right, the inserts still work, and an UPDATE simply succeeds. The run-at-start rule with the migration account from the key store, and the verification job of this story, are what keep the pair intact (ADR-021; NFR-052).
- **A silent gap in the ingest.** The ledger is complete only if the consumer keeps up: Architecture v5 slide 28 sets a 5-minute completeness target and an alert for a missing record. A consumer that is down, a dead-lettered envelope that nobody reads, or a lag that grows overnight produces exactly the failure the legacy story was written to prevent — a decision that happened and was never recorded.
- **A restore that quietly rewrites the past.** A restore is the one operation that can produce a ledger which is internally consistent and yet wrong: a point-in-time restore to before the last entries, a restored copy with the trigger missing, or a restore that is then "repaired" by an update. The chain makes the first detectable and the seal in immutable storage makes it provable; the run book makes the second and the third forbidden.

The deployment is also the place where three target facts become operational. The base of the service is `/api/recovery/decision/v1` behind gateway-bff (DP-13, DP-19), so the route a smoke test calls is the gateway's and not a pod's. The ingest is a Kafka consumer on the shared topic `rwb.decision-record.v1` (DP-03), so its health is measured in lag and dead letters and not in HTTP 200. And there is no data-lake copy (DP-17), so the nightly job that used to ship partitions is replaced by the 02:00 chain check and its seal — the same JOB-14 id, a different mechanism (DP-10; Architecture v5 slide 44).

### 3. Preconditions

- The service is built from the platform template and deployed by the golden pipeline: an API deployment and a worker deployment on the same task queue, on the platform's Helm chart (RWB-PLT-TPL; Architecture v5 slide 33).
- Schema `rwb_decision`, its `flyway_schema_history` table and the `decision_log_entry` objects exist on the per-service Flyway sequence of RWB-PLT-E1044-CON and from RWB-P7-E1008-DB (DP-15).
- The migration account, the read-only drift account and the runtime account of `rwb-decision` are entries in the key store (NFR-052); their names are Not specified in the source documents (GAP-1232; ASM-2196).
- The shared topic `rwb.decision-record.v1` exists with its retry topic and its `.dlt` on the Kafka platform of RWB-PLT-EVT; the consumer group of the ingest is this story's to configure, and its name is Not specified in the source documents (GAP-1233; ASM-2197).
- The workflow kit and the `rwb-recovery` namespace are live (RWB-PLT-E1071-CON), so the 02:00 Schedule runs on the `rwb-decision` queue.
- The gateway route of RWB-PLT-N001-CON exists, so the smoke test calls the two reads through gateway-bff and not a pod.
- The 5-minute completeness target, the 15-minute notice budget and the 02:00 run time are the architecture's; the alert thresholds, the dashboard panel set, the RPO and the RTO are Not specified in the source documents and are set as the working read (GAP-1233; ASM-2197), (GAP-1234; ASM-2198).
- No build dependency: the story has no build dependency and is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Pipeline: build the service image from the template, run the unit tests and the contract tests against the published baseline and its fakes, and publish the image.
2. Pipeline: run the migration stage — apply every pending migration of `rwb_decision` to a clean container with the migration account read from the key store.
3. Pipeline: run the drift gate before the deployment to SIT, UAT and PROD — compare the object list produced by the migrations with the target schema through the read-only account, and stop the deployment on a difference.
4. Deployment: on service start, Flyway reads the migration account from the key store, applies each pending migration once in version order and writes the checksum to the service's own history table; a second instance that starts at the same moment waits for the Flyway lock and finds nothing pending.
5. Deployment: the API pods become ready only after the migrations and after the ingest consumer has joined its group; a readiness gate holds traffic until both are true.
6. Runtime: the ingest consumer reads `rwb.decision-record.v1` with the retry topic and the `.dlt`; the consumer lag is exported and compared with the 5-minute completeness target; a dead-lettered envelope raises an alert with its `ce_id`, its `ce_type` and its reason.
7. Runtime: at 02:00 the Schedule `decision-log-chain-check` starts `DecisionChainCheckWorkflow` on the `rwb-decision` queue; the run writes one seal file per verified business date to immutable storage and raises an incident and the Compliance notice on a break.
8. Runtime: the append-only verification job runs on a schedule and queries the catalogue: the trigger `tr_declog_append_only` exists and is enabled, the function `refuse_change` exists, and no login other than the schema owner holds UPDATE or DELETE on `decision_log_entry`; a hit raises an alert and is a P2 incident.
9. Runtime: the dashboards show the ingest lag, the entries per hour, the dead-letter count, the last chain-check result, the last seal for each business date, the drift gate result of the last deployment and the append-only verification result.
10. Backup: the schema is covered by the ACE database backup policy with point-in-time recovery; the seal files are kept in immutable storage with their own retention.
11. Restore: a restore is run into an isolated environment, to a point in time after the last verified seal; after the restore the chain is re-verified from the first entry to the last, the append-only verification job runs, and only then is the restored copy accepted; a restore that fails either check is not promoted.
12. Run book: each failure of section 5 has one entry in the run book with its symptom, its first check, its recovery step and the record it leaves.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A pending migration fails at service start | The transaction rolls back, the history records the failure, the pod does not become ready and the deployment stops | MSG-P3-016 | AC1 |
| X2 | The drift gate finds an object the migrations do not produce | The deployment stops before it starts and the object is named | MSG-P3-016 | AC2 |
| X3 | The migration account or the read-only account cannot be read from the key store | The pod does not start; the failure is logged without the secret | None | AC3 |
| X4 | The ingest lag passes the 5-minute completeness target | An alert names the group, the topic, the partition and the lag; the run book's first check is the consumer and the dead-letter topic | A missing-record alert | AC4 |
| X5 | An envelope is dead-lettered | The alert carries `ce_id`, `ce_type` and the reason; the run book steps are the replay and the incident | MSG-P7-009 where the body was refused | AC4 |
| X6 | The chain check finds a break | An incident is raised and MSG-P7-008 goes to Compliance within 15 minutes; the seal of that date is not written | MSG-P7-008 | AC5 |
| X7 | The append-only verification job finds a missing trigger, a missing function or a grant | The alert is raised as a P2 incident and the grant or the trigger is restored by the DB story's migration; no row is touched | None | AC6 |
| X8 | A restore is run | The chain is re-verified and the append-only job is run before the copy is accepted; a failure stops the promotion | MSG-P7-008 on a break | AC7 |
| X9 | Two instances of the service start together | One applies the migrations, the other waits for the lock and finds nothing pending | None | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the template, the chart, the schema and login, the Kafka platform, the workflow kit, the gateway route and the ACE backup policy |
| Negotiable | The dashboard panels, the alert thresholds and the run-book wording are settled with the operations team; the rules of section 8 are fixed |
| Valuable | The ledger is deployed, watched and restored without an operation that can change a row, and a silent gap is impossible |
| Estimable | One pipeline, one drift gate, one consumer and one Schedule in production, one verification job, one restore procedure, one run book |
| Small | Fits one sprint with its tests |
| Testable | Each criterion runs in a pipeline, in a container or in a restore exercise in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: deployment of the central decision ledger

  Background:
    Given the service schema is rwb_decision and the baseline version is V0001
    Given the migration account and the read-only drift account are secret references in the key store
    Given the ledger is written only by the ingest of rwb.decision-record.v1 and read on /api/recovery/decision/v1

  Scenario: AC1 Start applies the pending migrations once, with the two-instance lock (new, D-RCV-60)
    Given a service with two pending migrations in SIT
    When the service starts twice, the second instance starting while the first is still migrating
    Then both migrate in version order and the history records them with their checksums
    Then the second instance waits for the Flyway lock, finds nothing pending and becomes ready
    Then a migration that fails rolls back, the history records the failure and the pod does not become ready

  Scenario: AC2 The drift gate runs before SIT, UAT and PROD (new, D-RCV-60)
    Given the migration stage of the pipeline
    When a column has been added by hand to rwb_decision, or an index has been dropped
    Then the gate fails with MSG-P3-016, names the object and stops the deployment in SIT, UAT and PROD
    Then in DEV the gate reports the same difference and the deployment continues
    Then the gate compares the object list of the migrations with the target through the read-only account and never writes

  Scenario: AC3 The accounts are secret references and none is in a file (new, D-RCV-60)
    Given the migration, read-only and runtime accounts of the service in the key store
    When the pipeline and the pod read them
    Then each account is a secret reference and never a value in a pipeline file, a chart value, an image layer, a log or a prompt
    Then a scan of the pipeline files, the chart, the image and the startup log finds no credential
    Then the runtime login of the ingest is the service login and holds no UPDATE and no DELETE on decision_log_entry

  Scenario: AC4 The ingest is monitored and a gap is alerted (new, D-RCV-60)
    Given the consumer group of the ingest on rwb.decision-record.v1 with its retry topic and its .dlt
    When the lag passes the 5-minute completeness target, or an envelope is dead-lettered
    Then an alert names the group, the topic, the partition, the lag or the ce_id and the reason
    Then the run book entry for the case is linked from the alert and states the replay step
    Then the dead-letter count, the entries per hour and the lag appear on the dashboard of the service

  Scenario: AC5 The chain check runs at 02:00 and its failure reaches Compliance (new, D-RCV-60)
    Given the Schedule decision-log-chain-check at 02:00 on the rwb-decision queue
    When the run verifies a clean range
    Then one seal file for the business date is written to immutable storage with the count, the last chain_seq and the last entry_hash
    When the run finds a break
    Then an incident is raised and MSG-P7-008 reaches the Compliance and PDPA officer group within 15 minutes of the run start
    Then no seal is written for that business date, and the missing seal is itself an alert

  Scenario: AC6 The append-only verification job proves the guarantee in place (new, D-RCV-60)
    Given the scheduled verification job
    When it queries the catalogue of rwb_decision
    Then it passes only when tr_declog_append_only exists and is enabled, refuse_change exists and no login other than the schema owner holds UPDATE or DELETE on decision_log_entry
    When the trigger is dropped or disabled, or an UPDATE grant is added
    Then the job fails with the object named and raises a P2 incident
    Then the recovery step is the DB story's migration and no row of the ledger is updated

  Scenario: AC7 A restore of the ledger is verified before it is accepted (new, D-RCV-60)
    Given a point-in-time restore of the ACE database into an isolated environment, to a time after the last verified seal
    When the restore completes
    Then the chain is re-verified from the first entry to the last and every seal file of immutable storage matches the last chain_seq and entry_hash of its date
    Then the append-only verification job passes on the restored copy
    Then a restored copy that fails either check is not promoted, and no UPDATE and no DELETE is run on it to make it pass

  Scenario: AC8 The run book covers every failure of this story (new, D-RCV-60)
    Given the run book of the service
    When it is reviewed against the exception paths X1 to X9
    Then each path has one entry with its symptom, its first check, its recovery step and the record it leaves
    Then no entry instructs an update or a delete on decision_log_entry, and every entry that needs one escalates to the DB story instead

  Scenario: AC9 The two reads are reached through gateway-bff and no job deletes a ledger row (new, D-RCV-60)
    Given the two reads of the ledger and the retention of the ledger and of the seal files
    When a smoke test calls each read through gateway-bff and the retention of each class is checked against the bank schedule
    Then each read answers through gateway-bff and no pod is reached directly
    Then no job of this story deletes a row of decision_log_entry

  Scenario: AC10 A consumed call that fails or does not answer leaves no partial entry (new, D-RCV-60)
    Given the ingest of rwb.decision-record.v1 with its retry topic and its .dlt
    When a consumed call fails or does not answer
    Then the envelope is retried on the retry topic and then dead-lettered to the .dlt
    Then no partial row is written to decision_log_entry and the alert of AC4 names the ce_id and the reason

  Scenario: AC11 A seal for a business date that did not verify is refused (new, D-RCV-60)
    Given a business date for which the chain check of AC5 found a break
    When a seal is requested for that business date
    Then the request is refused, no seal file is written and the missing seal is itself an alert
```

These criteria are new and test the deployment artefacts only: no legacy acceptance criterion is repeated, and every identifier, time, topic and target is the architecture's or the technical specification's value, character for character.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | Flyway runs on service start in every environment and applies each pending migration of this service once, under the service's own login from the key store | ADR-021; DP-15; RWB-PLT-E1044-OPS | AC1; TC-P7-E1008-OPS-01 |
| BR2 | The drift gate runs before every deployment to SIT, UAT and PROD and stops it on a difference; DEV reports and continues | RWB-PLT-E1044-OPS BR3; ADR-021 | AC2; TC-P7-E1008-OPS-02 |
| BR3 | Every credential is a key-store reference and no credential appears in a file, an image, a log or a prompt | NFR-052 | AC3; TC-P7-E1008-OPS-03 |
| BR4 | The ingest keeps up with the shared topic: the lag against the 5-minute completeness target and the dead-letter count are alerted, not merely graphed | Architecture v5 slide 28 (BR10 of the app story) | AC4; TC-P7-E1008-OPS-04 |
| BR5 | The chain check runs at 02:00 as a Schedule of this service and a break reaches Compliance within 15 minutes; a date that did not verify is not sealed | Architecture v5 slide 44 (JOB-14); NFR-035 | AC5; TC-P7-E1008-OPS-05 |
| BR6 | The append-only guarantee is verified in place on a schedule: the trigger, the function and the absence of an UPDATE and DELETE grant | REQ-DRI-002; the DB story's BR2 | AC6; TC-P7-E1008-OPS-06 |
| BR7 | A restore is verified by the chain and by the seals before it is accepted, and no UPDATE or DELETE is ever run on the ledger to make a check pass | REQ-DRI-002; REQ-DRI-003; DP-17's "no repair by hand" | AC7; TC-P7-E1008-OPS-07 |
| BR8 | There is no data-lake copy, no watermark job and no partition step; the 02:00 run and its seal replace the legacy 01:00 copy | DP-17; ADR-018; Architecture v5 slide 44 | AC5; TC-P7-E1008-OPS-05 |
| BR9 | The two reads are reached through gateway-bff and never from a pod, so a smoke test proves the route and not only the container | DP-19; Template and Rules §R4 | AC9; TC-P7-E1008-OPS-10 |
| BR10 | Retention follows the bank schedule for the ledger and its own class for the seal files; no job of this story deletes a ledger row | DL26; the DB story's BR9 | AC9; TC-P7-E1008-OPS-10 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Deployment starts | The drift gate passes | Migrating |
| Migrating | All pending versions applied | The history records every checksum | Starting |
| Starting | The ingest joins its group and the API is ready | The readiness gate is satisfied | Serving |
| Migrating | A version fails | A statement or a validation fails | Failed (rolled back, the pod not ready) |
| Serving | The lag passes the target, or an envelope is dead-lettered | The alert rule fires | Degraded (alerted, catching up) |
| Degraded | The lag returns inside the target | The group catches up | Serving |
| Serving | The 02:00 run verifies the range | Every hash and link matches | Sealed for the business date |
| Serving | The 02:00 run finds a break | The first mismatch is named | Broken (incident, no seal) |
| Serving | The verification job finds a grant or a trigger missing | The catalogue query hits | Guard lost (P2 incident, restored by migration) |
| Broken, Guard lost, or a data loss | Restore into an isolated environment | After the last verified seal | Restored (chain and seals verified before promotion) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer of the platform | Owns the pipeline, the drift gate, the chart values, the dashboards, the alerts and the run book |
| RW-PLATADM Platform administrator | Reads the deployment and the job runs; reruns a failed migration job after the fix is a new version |
| The pipeline migration account of the service | Applies the migrations of `rwb_decision` with the service's login from the key store |
| The runtime login of the service | Ingests the shared topic and reads the ledger; never updates and never deletes a ledger row (DP-02) |
| Key store administrator | Owns the secret entries and their rotation; not a Workbench role |
| RW-COMPLY Compliance and PDPA officer | Receives the break notice; takes no operational action in this story |
| RW-AUDIT Internal audit | Reads the ledger through the two operations and the run records; no direct SQL |
| No delegation of authority level applies | A deployment is not a credit decision |

No personal name, no e-mail address and no credential appears in a pipeline file, a chart value, a dashboard, a run book or a test.

### 11. Data

No business field. The deployment writes run records — one per migration run, one per chain-check run, one per verification job run, each with the service, the schema, the version, the checksum, the counts, the start and end time and a status — to the P1 job view and to the platform's logs. It reads the catalogue of `rwb_decision`, the consumer offsets of the ingest, the sandbox seal files and the key store references. It writes no row of `decision_log_entry` and no business row of any kind. It carries no field classed as personal data in Data Classification v5; a field of that class is not written to a run record, a log or a metric.

The alert thresholds, the dashboard panel set, the seal file layout and the retention class of a run record are the working read of the assumptions (GAP-1233; ASM-2197), (GAP-1234; ASM-2198); the times, the topic, the target and the message identifiers are the architecture's values.

The directive resolves the open decisions DL10 (assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863) and DL26 (assumptions ASM-0247, ASM-0264, ASM-0275, ASM-0355) on their recommended option and confirms those assumptions; no decision of this story remains open.

| Object | Kind | Read or written |
|---|---|---|
| flyway_schema_history | Flyway history table in `rwb_decision` | Read |
| decision_log_entry | Ledger table in `rwb_decision` | Read; never written |
| tr_declog_append_only | Trigger on `decision_log_entry` | Read (catalogue) |
| refuse_change | Function on `decision_log_entry` | Read (catalogue) |

### 12. Contract

#### 12.1 REST operations provided

None. The deployment provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | The smoke test after each deployment: one known entry of the seeded range, through gateway-bff, with 200 and its two hashes |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The smoke test of the page: one page in `chain_seq` order |
| GET | `/api/recovery/source-data/v1/admin/jobs` | P1 rwb-source-data | Reads the run records of the migration, the chain check and the verification job |
| POST | `/api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` | P1 rwb-source-data | Reruns a failed migration job after the fix is merged as a new version |

#### 12.3 Events published

None. A deployment, a run and an alert publish no business event; the dead-letter topic of the platform is an operational channel and not an event of this service.

#### 12.4 Events consumed

| Event | Topic | Use | Owner service |
|---|---|---|---|
| rwb.decision.DecisionRecorded.v1 | rwb.decision-record.v1 | The deployment's own health measure: the lag and the dead-letter count of this subscription are the object of AC4, and no envelope is processed by the deployment itself | rwb-decision (subscriber); producer: Not specified in the source documents (DOR-RWB-P7-E1008-OPS-24) |

#### 12.5 Workflows and activities

| Workflow or activity | Queue | Use |
|---|---|---|
| `DecisionChainCheckWorkflow` | `rwb-decision` | The 02:00 run whose Schedule, catch-up window and alerting this story operates |
| `verifyChainRange`, `raiseChainBreak`, `sendComplianceNotice`, `writeLedgerSeal` | `rwb-decision` | The four activities whose failures the run book covers |

This story registers none of them: it schedules, watches and reruns them, and the implementation is RWB-P7-E1008-APP's.

#### 12.6 Schedules

| Schedule | Cron | Queue | Job | Operations |
|---|---|---|---|---|
| `decision-log-chain-check` | 02:00 daily | `rwb-decision` | JOB-14 Hash-chain check | Overlap policy SKIP, catch-up window of one day, one alert on a failed run and one on a missing seal |
| `decision-log-append-only-check` | Daily, before the chain check | platform | The catalogue verification of AC6 | One alert on any hit; the recovery is a migration and never a statement on a row |

The 02:00 time is the architecture's (Architecture v5 slide 44); the time of the verification job is this story's to set and is Not specified in the source documents (GAP-1233; ASM-2197).

#### 12.7 Tables owned

None. The deployment owns no business table. Flyway writes `flyway_schema_history` inside `rwb_decision`, and this story reads that table and the catalogue; it writes no row of `decision_log_entry`, of the library objects or of any other table.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| P1 job view fake (rwb-source-data) | `GET /api/recovery/source-data/v1/admin/jobs` answering one run record of each type, with the service, the schema, the version, the checksum, the counts, the status and the times; `POST …/{jobId}/rerun` answering 202 | The end-to-end tests of this story |
| Ledger read fake | The two decision-log reads of RWB-P7-E1008-CON, answering one entry and one page | The smoke test, run against the fake before a live environment exists |

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | 4: two smoke reads of this service and two operations of the P1 job view | All through the gateway of their owner |
| Kafka | None | 1 subscription monitored, not processed by the deployment | Lag and dead letters are the operational objects |
| Temporal | None registered; 1 Schedule and 1 workflow operated | None | Queue `rwb-decision` |
| File | None | None | The seal file is written by the service to immutable storage; this story verifies it exists |

### 13. Solution plan

**Deliverables.** The pipeline of the service on the golden template, the chart values that read the three accounts from the key store and set `RWB_SCHEMA=rwb_decision` per environment, the start configuration (`spring.flyway.baseline-on-migrate=false`, `clean-disabled=true`, validation on start, out-of-order off, the lock on), the drift gate stage, the consumer configuration with its retry and `.dlt`, the 02:00 Schedule and the verification job, the dashboard, the eight alerts, the restore procedure and the run book.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The deployment touches `rwb_decision` only | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`. The deployment operates the subscription of the ledger | H RWB-PLT-E1027-CON (carried by the app story; named here) |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case. The deployment changes no reference value | referred to; the consuming story carries the dependency |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit. The 02:00 run is a Schedule of this service, not a Quartz row | H RWB-PLT-E1071-CON (carried by the app story; named here) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`. The smoke test calls the decision base through the gateway | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema. The run at start applies this service's sequence and no other | H RWB-PLT-E1044-CON (the sequence owner; named here) |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting. No copy job, no watermark and no partition step exists in the pipeline | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route. The smoke test goes through the gateway | H RWB-PLT-N001-CON (carried by the app story; named here) |

The patterns **not claimed** here are DP-02 (the login is created by the platform DB work and used here), DP-04, DP-05, DP-06, DP-08, DP-09 (the library objects and the relay are the app and DB stories'), DP-11, DP-12, DP-14, DP-16, DP-18 and DP-20.

**Configuration and secrets.** Non-secret configuration: the consumer group and its topic, the retry topic and the `.dlt`, the verifier batch size of 1,000, the completeness target of 5 minutes, the notice budget of 15 minutes, the genesis hash of 64 zeros, the Schedule cron of `0 0 2 * * *`, the seal target and the notification group. Secrets, all as key-store references: the migration account, the read-only drift account and the runtime account of the service. The consumer group name, the seal target path and the alert thresholds are Not specified in the source documents (GAP-1233; ASM-2197).

**Alerts.** One per failure mode: a failed migration; a drift finding; a consumer lag past the target; a dead-lettered envelope; a failed chain-check run; a missing seal for a business date; an append-only verification hit; a restore verification failure. Each alert links its run book entry and carries no personal data — an envelope is named by its `ce_id`, never by a customer reference.

**Backup and restore of an append-only ledger.** The schema is covered by the ACE backup policy with point-in-time recovery; the seal files live in immutable storage under their own retention, so the last verified `chain_seq` and `entry_hash` of a date exist outside the database. A restore is always run into an isolated environment first, to a point in time after the last verified seal; the chain is re-verified end to end, the seals are compared, the append-only verification job runs, and only then is the copy promoted. A restored copy that fails is not repaired by a statement: it is restored again, or the gap is recorded. The RPO, the RTO and the retention of a restore exercise are Not specified in the source documents (GAP-1234; ASM-2198).

**Run book entries.** (1) A failed migration: the version, the checksum and the statement; the fix is a new version. (2) A drift finding: the object, and the migration that should produce it. (3) A lag: the consumer, the partition, the last offset and the dead-letter count. (4) A dead-lettered envelope: the `ce_id`, the reason, and the replay after the fix. (5) A chain break: the first `chain_seq` and entry ID, the incident, the Compliance notice and the quarantine of the range from that entry on. (6) A missing seal: the run and the night. (7) An append-only hit: the grant or the trigger and the migration that restores it. (8) A restore: the point in time, the seal compared and the two checks. (9) A gateway-only failure: the route, the two reads and the pod health behind it.

**Done when.** The eight criteria of section 7 pass in SIT, the drift gate stops a drifted SIT, UAT and PROD deployment and passes it in DEV, two instances start together inside the connection cap, a break reaches Compliance inside 15 minutes, the verification job catches a dropped trigger and a widened grant, and a restore is verified by the chain and the seals before promotion.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-016 | Drift found, checksum mismatch, a refused clean or undo, or a failed migration | Schema check failed in {schema}: {object}. The deployment was stopped. |
| MSG-P7-008 | The chain check finds a break | The decision log check for {date} found a break at entry {entryId}. Entries from that entry on cannot be relied on until Compliance reviews them. |
| MSG-P7-003 | The ingest cannot write an entry and the envelope is retried | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A caller without Decision log R runs the smoke read | You cannot {action} here. Your role does not include it. |
| Not specified in the source documents (DOR-RWB-P7-E1008-OPS-9) | Not specified in the source documents (DOR-RWB-P7-E1008-OPS-9) | Not specified in the source documents (DOR-RWB-P7-E1008-OPS-9) |
| An operational alert, no message id | Lag, dead letter, missing seal or append-only hit | Raised to the platform queue with the object named; no business user sees it |

MSG-P3-016 is the message of the migration work of RWB-E1-044, carried unchanged; MSG-P7-008 and MSG-P7-003 are the ledger's and are relayed, not rewritten. Thai text for each message follows DL10.

### 15. Screens and states

No new business screen. The service's dashboard shows the ingest lag against the 5-minute target, the entries per hour, the dead-letter count, the last chain-check result, the last seal for each business date, the last drift gate result and the last append-only verification result; SCR-44 Interface and job monitor shows the three run records. Its empty, loading, error and no access states are Not specified in the source documents (CG-ALL-6868). The operational states of a deployment and of a business date are the ones in section 9 — Serving, Degraded, Sealed, Broken, Guard lost and Restored — and none of them is a business state of a case.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P7-E1008-OPS-01 | AC1 | Component | A service with two pending migrations; two instances starting together; a failed version rolled back |
| TC-P7-E1008-OPS-02 | AC2 | End to end | A hand-added column and a dropped index in SIT, UAT and PROD stop the deployment; the same in DEV only reports |
| TC-P7-E1008-OPS-03 | AC3 | NFR | A scan of the pipeline files, the chart, the image and the startup log; three accounts as secret references; the runtime grant set |
| TC-P7-E1008-OPS-04 | AC4 | End to end | A lag past the target and one dead-lettered envelope; the alert, the dashboard panels and the run book link |
| TC-P7-E1008-OPS-05 | AC5 | End to end | A clean 02:00 run writing one seal, and a break reaching Compliance inside 15 minutes with no seal |
| TC-P7-E1008-OPS-06 | AC6 | Component | The verification job on a clean schema, then with the trigger dropped, then with an UPDATE grant added |
| TC-P7-E1008-OPS-07 | AC7 | NFR | A point-in-time restore into an isolated environment; the chain re-verified; the seal compared; a failed restore not promoted |
| TC-P7-E1008-OPS-08 | AC8 | Component | The run book reviewed against X1 to X9; no entry instructs a statement on a ledger row |
| TC-P7-E1008-OPS-09 | AC4 | Contract | The DecisionRecorded.v1 subscription on rwb.decision-record.v1 read against its event contract; the lag and dead-letter reads of that subscription |
| TC-P7-E1008-OPS-10 | AC9 | End to end | A smoke test of each read through gateway-bff with no direct pod call; a retention check of the ledger and the seal files; a job scan for deletes on decision_log_entry |
| TC-P7-E1008-OPS-11 | AC10 | Component | A consumed call of rwb.decision-record.v1 that fails and one that does not answer; the retry topic, the .dlt, the alert, and no partial row in decision_log_entry |
| TC-P7-E1008-OPS-12 | AC11 | Component | A business date with a chain break; a seal requested for it; the refusal, no seal file, and the missing-seal alert |

The legacy test cases of RWB-E1-008 are executed by RWB-P7-E1008-APP and RWB-ITG-E1008-ITG; these twelve are the deployment's own and no legacy identifier is renumbered.

### 17. Guardrails

- One schema and one login per service: the run and the subscription use the `rwb-decision` login and touch no other schema (DP-01, DP-02).
- No credential in a pipeline file, a chart value, an image layer, a log or a prompt; every account is a key-store reference (BR3).
- No clean and no undo in PROD; a fix is a new version through the pipeline (BR2).
- No statement on a ledger row from a pipeline, a run book or an alert response; the only recovery is a migration or a restore, and a restore is verified before promotion (BR7).
- No data-lake job, no watermark and no partition step (BR8, DP-17); the 02:00 run and its seal are the only nightly work.
- No personal data in an alert, a dashboard, a run record or a seal file: an envelope is named by `ce_id`, a run by its business date.
- The smoke test goes through gateway-bff and never to a pod (BR9).
- No business value in the configuration beyond the values the architecture fixes; the thresholds and the cron of the verification job are configuration and not code.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-DRI-001 | One record per decision with the seven field groups | The ingest subscription and its lag target keep the ledger complete; consumer group and alert threshold Not specified in the source documents (GAP-1617, GAP-1233) | TC-P7-E1008-OPS-04 |
| REQ-DRI-002 | Append only; a correction is a new record naming the one it corrects | The run at start with the service login, the verification job and the restore rule | TC-P7-E1008-OPS-03, TC-P7-E1008-OPS-06, TC-P7-E1008-OPS-07 |
| REQ-DRI-003 | Hash chained, checked, break reported to Compliance the same day | The 02:00 Schedule, the seal, the incident and the 15-minute notice; the append-only verification job time and the immutable-storage path per environment are Not specified in the source documents (GAP-1233) | TC-P7-E1008-OPS-05, TC-P7-E1008-OPS-07 |
| NFR-052 | Database and drift accounts held in the key store | The three accounts as secret references and the scan | TC-P7-E1008-OPS-03 |
| ADR-021 | Per-service Flyway and migration ownership | One run per service, forward only in PROD, the lock and the drift gate | TC-P7-E1008-OPS-01, TC-P7-E1008-OPS-02 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P7-E1008-APP | App development | The service, the ingest, the chain check and the seal this story operates |
| RWB-P7-E1008-CON | Contract | The two reads the smoke test calls |
| RWB-P7-E1008-DB | Database | The schema, the table, the trigger, the grants and the login this story applies and verifies; the DP-09 outbox, inbox and processed_event objects are created there from the library template (GAP-1228) |
| RWB-PLT-E1044-OPS | DevOps | The golden pipeline, the drift gate and the run-at-start pattern this story reuses |
| RWB-PLT-EVT | Platform | The shared topic, its retry topic and its `.dlt` |
| RWB-PLT-E1071-CON | Contract | The namespace and the Schedule mechanism |
| RWB-PLT-OBS | Platform | The dashboards and the alert route of the platform |
| RWB-P1-E1069-APP and the P1 job view | App development | The run records read and the rerun path |

### 19. Out of scope

- The service code, the ingest, the chain and the two operations: RWB-P7-E1008-APP.
- The schema, the table, the trigger, the functions and the grants: RWB-P7-E1008-DB.
- The contract of the two reads and the envelope: RWB-P7-E1008-CON.
- The golden pipeline, the template, the chart and the drift gate as a platform stage: RWB-PLT-E1044-OPS and RWB-PLT-TPL.
- The Kafka platform, the topic, the retry topic and the dead-letter topic: RWB-PLT-EVT.
- The Temporal namespace, the worker and the Schedule mechanism: RWB-PLT-WF and RWB-PLT-E1071-CON.
- The platform dashboards, the alert route and the log platform: RWB-PLT-OBS.
- The ACE database backup policy itself and the restore of another schema: the platform DB work.
- The decision-log screens and the query filters: RWB-P7-E2005-APP.
- Retention periods (DL26) beyond the run records of this story.
