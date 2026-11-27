# RWB-ITG-TE008-ITG Decision log hash chain check — integration

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- JOB-14 is a job of rwb-decision, so the rwb-source-data job operations are removed: they list and rerun only rwb-source-data runs (RD-P1-012). The run record is read from the `ChainCheckWorkflow` result. Finding RWB-ITG-TE008-ITG#1.
- The rwb-decision rerun operation of JOB-14 is not published: AC4 and AC5 state it as pending (NEW-GAP-A1), and the rerun of a completed run is an open question (NEW-GAP-F04-1). Findings #1 and #2.
- AC1 expects run record type JOB-14, as step 8 writes it. Finding #3.
- Finishing pass: test case IDs of Test Cases v9 cited in place of the placeholders.
- No rerun of a completed JOB-14 run: AC4 asserts the refusal and the next 02:00 run; NEW-GAP-F04-1 is closed (RD-P1-065).

**Change log.** D-RCV-60, 22 November 2026: split from RWB-TE-008 for the wave-1 integration epic. The Quartz job JOB-14 becomes a 02:00 Temporal Schedule in rwb-decision with overlap policy SKIP and a catch-up window, the wait for the nightly copy of the decision log (JOB-13) becomes a wait for the continuous Kafka ingest watermark of `rwb.decision-record.v1`, the run record names that watermark instead of a copy job end time, and the check is proved on the real central ledger and the real local chain of every wave-1 service rather than on a fake. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 13 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-ITG-TE008-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP10, DP13, DP17, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-TE008-ITG-16); the squad sizes it at refinement |
| Depends on (build) | RWB-P7-E1008-APP, RWB-PLT-TE008-APP (not done yet) |
| Contract dependencies | Not specified in the source documents (DOR-RWB-ITG-TE008-ITG-21) |
| Contract version | v1 (the /v1 path of each operation in 12.2) |
| Integration dependencies | RWB-P7-E1008-APP, RWB-PLT-TE008-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-014, FR-PLT-015) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-012, RD-P1-065 |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **tech lead**, I want **the nightly decision-log hash-chain check exercised end to end on the real services and the real Schedule: JOB-14 firing at 02:00 as a Temporal Schedule in rwb-decision, waiting for the continuous ingest of `rwb.decision-record.v1` to reach the producer watermark, recomputing every `entry_hash` and comparing every `prev_hash` from chain_seq 1 to the highest chain_seq at the start in the central ledger and in every wave-1 local chain, naming a break in one service's local chain and a gap between a local record and the ledger, and telling Compliance the same day**, so that **a changed entry or a missing record is found by the morning after it happens on the architecture that will run it, not on a monolith job and not on a fake**.

### 2. Business rationale

The decision log is evidence only while nobody can change an entry unseen. The legacy story runs JOB-14 on Quartz, waits for the nightly copy of the log to the data lake (JOB-13), and reads one log in the recovery schema. In the target none of those three things exists as the legacy story describes them: each of the 19 services writes its own decision record in its own schema in the same transaction as its state change and publishes `DecisionRecorded` (Arch v5 slides 20 and 28, steps 1 and 2; Temporal design slides 11 and 14), rwb-decision collects the record into the central ledger it owns within 5 minutes (Arch v5 slide 28, step 3; ADR-022, DP-03), JOB-13 is continuous Kafka ingest rather than a 01:00 copy to a data lake (Arch v5 slide 44; DP-17, RWB-E1-014 retired), and JOB-14 is a Temporal Schedule at 02:00 with overlap policy SKIP and a catch-up window instead of a Quartz job (Arch v5 slides 14 and 44; Temporal design slide 16; DP-10). It meets REQ-DRI-003, supports control CTL-06 and is measured by one daily check with a same-day report.

Those pieces are proven by no single service story. A chain that is recomputed over the ledger alone misses a break in a service's local chain; a run that starts before the ingest has caught up reports a gap that is only lateness; a break that is found but not named, or named with a personal value, fails the audit; and a run that stops without a report leaves Compliance believing the chain was confirmed. Only the integration level, on the real services, the real topic and the real Schedule, can prove that all of them hold together.

### 3. Preconditions

- The nine wave-1 services are deployed in DEV and SIT, each with its own schema and login: rwb_source_data, rwb_case, rwb_access, rwb_document, rwb_comms, rwb_decision, rwb_reporting, rwb_agent and rwb_integration (Arch v5 slide 41, wave 1).
- Every wave-1 schema holds its local `decision_record` with `chain_seq`, `prev_hash`, `entry_hash` and the append-only rule, written in the same transaction as its state change (DP-03; the DB story of each service; RWB-P7-E1008-DB for rwb_decision).
- rwb-decision holds `decision_log_entry` with `chain_seq`, `prev_hash`, `entry_hash` and `corrects_entry_id`, the chain lock and the canonical form; the service role holds INSERT and SELECT and no UPDATE or DELETE grant (RWB-P7-E1008-APP, RWB-P7-E1008-DB).
- The topic `rwb.decision-record.v1` exists with its retry and `.dlt` topics, the consumer of rwb-decision ingests into the ledger within 5 minutes, and queue `rwb-decision` is registered in namespace `rwb-recovery` (RWB-PLT-EVT, RWB-PLT-WF; Arch v5 slides 20, 28 and 42; Temporal design slide 11).
- The 02:00 Schedule of JOB-14 is registered in rwb-decision by the release and can be started once by the harness through the Temporal client; the platform story of the same legacy key, RWB-PLT-TE008-APP, builds the scheduled-job and run-record parts of the check on the service template, and the rwb-decision story RWB-P7-E1008-APP builds the workflow, the ingest and the ledger.
- The run record is the result of the `ChainCheckWorkflow` run in rwb-decision, read by the harness through the Temporal client; the job operations of rwb-source-data list and rerun only rwb-source-data runs and are not used (RD-P1-012). Pending: the rwb-decision operation that reruns JOB-14 (gateway-bff view of RWB-PLT-TE008-APP), owner solution architect, tracked as NEW-GAP-A1. The Schedule itself is started by the harness with the same input the cadence uses.
- rwb-access answers the authorise call and holds the test roles RW-COMPLY, RW-AUDIT, RW-SECADM and RW-PLATADM with their Platform administration letters (RWB-P4-E1008-APP).
- The Compliance and PDPA officer group and the platform administrator group are reachable through the ACE Common notification path, and the break incident is raised with Compliance (legacy RWB-TE-008 sections 10 and 14).
- The parameters of the check are read through the parameters contract of rwb-case (DP-06) and the decision codes, outcome codes and approval levels used by the fixtures are read through its reference-data contract (DP-07), never as values in the harness code: start 02:00, latest start 04:00, batch size 1,000, all Asia/Bangkok.
- Which chains the run covers, what the ingest watermark is and where the incident and the report go across services is Not specified in the source documents (GAP-0380; ASM-0549, ASM-0550).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7). The harness is written on Day 1 against the two integration stories and the real Schedule, and it never substitutes a fake for a real service.

### 4. Flow

1. Harness: reads the service list, the topic, the retry and `.dlt` topics, the queue, the namespace, the Schedule name and the two read paths from configuration, and runs the preflight of section 13; a missing local `decision_record`, ledger table, chain object, topic, retry topic, task queue or Schedule stops the run before any test.
2. Schedule: `decisionChainCheck` fires JOB-14 at 02:00 Asia/Bangkok for business date 2 December 2026, the previous day, on queue `rwb-decision`, with overlap policy SKIP and a catch-up window (Arch v5 slides 14 and 44; Temporal design slide 16).
3. Workflow (`ChainCheckWorkflow`): reads the ingest watermark of `rwb.decision-record.v1` into the ledger; if the ledger is behind the producer watermark it re-reads every 5 minutes and starts the check when the watermark is reached, and it starts at 04:00 with the note "ingest not at watermark" when the watermark is not reached by then.
4. Workflow: reads the highest `chain_seq` at the start in the central ledger and in every wave-1 local chain, and fixes each of them as the end of the run for that chain; entries appended later are checked the next night.
5. Workflow: recomputes every `entry_hash` from the canonical form and compares every `prev_hash` with the entry before, from chain_seq 1 to the highest at the start, in batches of 1,000, for the central ledger and for each wave-1 local chain.
6. Workflow: counts every entry that fails in each chain, keeps the first per chain, and names the service and the chain of each break by entry ID and chain_seq.
7. Workflow: reconciles the local records with the ledger entries by entryId and names any local record with no ledger entry as a gap, and any ledger entry with no local record as an orphan.
8. Workflow: writes the run record with type JOB-14, business date, status, the ingest watermark it started on, and its checks: entries checked, last chain_seq, last entry_hash, result, first break chain_seq and entry ID per chain, failing count, gap count and rerun.
9. Workflow: sends MSG-P7-007 to the Compliance role (RW-COMPLY) when every chain is intact, or MSG-P7-008 with an incident naming the first break per chain and every gap when one is found.
10. Workflow: on an error that stops the run, records status FAILED, alerts the platform administrator group and sends MSG-P7-013 to Compliance with the date of the last complete check.
11. Platform administrator: reruns a FAILED JOB-14 run (a completed run is not rerun; it is re-verified by the next 02:00 run, RD-P1-065 rule 1) through the rwb-decision rerun operation (Pending: the rwb-decision operation that reruns JOB-14 (gateway-bff view of RWB-PLT-TE008-APP), owner solution architect, tracked as NEW-GAP-A1); a rerun is a new run record with rerun true and changes nothing else, and the Schedule refuses a second concurrent start by its SKIP policy.
12. Harness: reads the run record from the `ChainCheckWorkflow` result through the Temporal client and the entries through the two decision reads, times the incident and MSG-P7-008 from the run start, runs the 10,000,000-entry run against the 60 minute budget, reconciles one local record to one event to one ledger entry, and writes the run report.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | An entry does not match its `entry_hash` or its `prev_hash`, in the ledger or in a service's local chain | The run result is BROKEN for that chain; the first break and the failing count are recorded with the service and the chain; an incident is raised and Compliance is told | MSG-P7-008 | AC2 |
| X2 | The run stops on an error, for example a lost database connection | Status FAILED with the entries checked so far; the platform administrator group is alerted; Compliance is told the check did not complete | MSG-P7-013 | AC5 |
| X3 | A rerun of a completed run is requested for the same business date | Refused with 409 and the owner's "already complete or running" code; no run and no run record; the next 02:00 run re-verifies the chains | None | AC4 |
| X4 | A chain is empty | Result INTACT with count 0 and the genesis hash of 64 zeros for that chain | MSG-P7-007 | AC1 |
| X5 | The ingest has not reached the producer watermark at 02:00 | The workflow waits, re-reading the watermark every 5 minutes, and starts at 04:00 at the latest, recording that the watermark was not reached | MSG-P7-007 or MSG-P7-008 | AC3 |
| X6 | Entries are appended while the run is in progress | They are outside this run's end chain_seq and are checked the next night | None | AC3 |
| X7 | A local record has no ledger entry because its event is still in the retry topic | The gap is named by service, entry ID and chain_seq while both chains stay INTACT; an incident is raised and the next run closes it | MSG-P7-008 | AC4 |
| X8 | A role without Platform administration U calls the rerun | rwb-access refuses through the authorise call and the rerun answers 403 | MSG-P4-002 | AC5 |

X1 to X6 are the exception paths of the legacy story carried onto the real services and the real Schedule; X7 is the cross-service gap that only the split local-record and central-ledger design can produce; X8 is the authority of the legacy story in testable form. The incident and report route across services is Not specified in the source documents (GAP-0380; ASM-0549).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The harness is a test project of its own; it needs the two integration stories and the Schedule, and it owns no schema and no table |
| Negotiable | Fixture size, wait intervals, retry counts and report layout are configuration; the chain values, the message IDs, the times and the run order are fixed by the legacy story |
| Valuable | Proves across services what no single story can prove: the ledger and every local chain checked, a break named, a gap named, a stopped run reported |
| Estimable | One harness project, five test classes, four fixtures, three tamper steps, one Schedule start and one report |
| Small | Fits one sprint with the report |
| Testable | Every criterion is asserted on an observable: a run record, a workflow result, an incident, a message, a response code |

### 7. Acceptance criteria

```gherkin
Feature: Decision log hash chain check, proven across the wave-1 services and the real Schedule

  Background:
    Given the environment is DEV with synthetic data
    Given the nine wave-1 services run with their own schemas and login
    Given the central ledger in rwb_decision and one local decision_record chain in each wave-1 service schema
    Given the chain starts at chain_seq 1 with prev_hash of 64 zeros in each of them

  Scenario: AC1 The 02:00 Schedule checks the ledger and every wave-1 local chain and reports an intact chain (new, D-RCV-60)
    Given the central ledger holds 48,210 entries for business date 2 December 2026, none changed
    Given every wave-1 local chain holds the entries it published on rwb.decision-record.v1, none changed
    When decisionChainCheck fires at 02:00 on 3 December 2026 on queue rwb-decision as ChainCheckWorkflow with overlap policy SKIP
    Then the run record shows type "JOB-14", business date 2 December 2026, status "COMPLETED" and result "INTACT"
    Then its checks hold entries checked 48,210, last chain_seq 48,210 and that entry's entry_hash, recomputed in batches of 1,000 from chain_seq 1
    Then every wave-1 local chain is checked from chain_seq 1 to its highest chain_seq at the start and is reported "INTACT"
    Then MSG-P7-007 with the count and the last hash is sent to the Compliance role (RW-COMPLY)
    Then the same run over 10,000,000 synthetic entries finishes inside the 60 minute budget

  Scenario: AC2 A break in one service's local chain and two changed ledger entries are found and named (new, D-RCV-60)
    Given the actions of the record with chain_seq 30,005 in the local chain of a wave-1 service were changed in the DEV database with the trigger disabled and the trigger was restored
    Given the entries with chain_seq 12,001 and 40,350 in the central ledger were changed in the DEV database
    When decisionChainCheck runs at 02:00
    Then the first break in that local chain is chain_seq 30,005 and its entry ID, and the run record names the service and the chain
    Then the first break in the central ledger is chain_seq 12,001 and the failing count there is 2
    Then one incident is raised and MSG-P7-008 with the entry IDs is sent to the Compliance role (RW-COMPLY) before 08:00 on 3 December 2026
    Then the run record and the report name service names, chain_seq and entry IDs only, and no personal value

  Scenario: AC3 The run waits for the ingest watermark and keeps the 04:00 latest start (new, D-RCV-60)
    Given the ingest of rwb.decision-record.v1 into the ledger has not reached the producer watermark at 02:00
    When decisionChainCheck fires at 02:00
    Then the workflow re-reads the watermark every 5 minutes and starts the check when the ledger reaches it
    Then the run record names the ingest watermark and holds no copy job end time
    Then when the watermark is not reached by 04:00 the check starts at 04:00 with the note "ingest not at watermark"
    Given the ledger holds 48,210 entries when the run starts and 37 entries are ingested while it runs
    Then entries checked is 48,210 and last chain_seq is 48,210
    Then the next night's run checks 48,247 entries

  Scenario: AC4 A local record with no ledger entry is found and named as a gap (new, D-RCV-60)
    Given a wave-1 service has committed a local decision_record for case "RW-2026-000123"
    Given its DecisionRecorded event is held in the retry topic, so the ledger holds no entry with that entryId
    When decisionChainCheck runs
    Then the run names the service, the entryId and its chain_seq as a gap between the local chain and the ledger
    Then both chains are reported "INTACT" and the gap is the finding
    Then an incident is raised and MSG-P7-008 is sent with that entryId
    When test user "U-9301" holding RW-PLATADM asks to rerun the completed run of business date 2 December 2026 through the rwb-decision rerun operation of JOB-14 (pending, NEW-GAP-A1)
    Then the answer is 409 and no run record is written
    Then after the retry delivers the event the next 02:00 run writes its run record with result "INTACT" and no gap
    Then the Schedule refuses a second concurrent start while that run is running

  Scenario: AC5 A run that stops is reported and a rerun needs the Platform administration right (new, D-RCV-60)
    Given the ledger connection is closed in the test double after 20,000 entries
    When decisionChainCheck runs
    Then the run status is "FAILED" with entries checked 20,000
    Then the platform administrator group is alerted
    Then MSG-P7-013 is sent to the Compliance role (RW-COMPLY) with 2 December 2026 as the date of the last complete check
    When test user "U-8442" holding only RW-AUDIT calls the rwb-decision rerun operation of JOB-14 (pending, NEW-GAP-A1)
    Then rwb-access refuses through POST /api/recovery/access/v1/authorise and the answer is 403 with MSG-P4-002
    Then no ChainCheckWorkflow run starts and no run record is written
```

```
Scenario: AC6 The start times, the latest start and the batch size come from parameters, and every read goes through a published read path (new, D-RCV-60)
    Given the run parameters hold a start time, a latest start and a batch size
    When the Schedule starts a run after the parameters are changed in configuration
    Then the run uses the changed values without a code change and reads only the published read paths of the ledger and each local chain
```

```
Scenario: AC7 A redelivered DecisionRecorded event is ingested once and the chains do not change (new, D-RCV-60)
    Given a DecisionRecorded event on rwb.decision-record.v1 has been ingested into the central ledger
    When the same event is delivered again to ingestDecisionRecord
    Then the ledger holds one entry for its event id and that entry keeps its chain_seq and entry_hash
    Then a run of the check after the redelivery reports the same entries checked as before it

Scenario: AC8 A read of the ledger or a local chain that fails or does not answer ends the run as FAILED (new, D-RCV-60)
    Given the check is reading a published read path of the ledger or of a wave-1 local chain
    When that read fails or does not answer
    Then the run status is "FAILED" and the platform administrator group is alerted
    Then MSG-P7-013 is sent to the Compliance role (RW-COMPLY) with the date of the last complete check

Scenario: AC9 A run record status change the model does not allow is refused (new, D-RCV-60)
    Given a run record of the check holds status "COMPLETED"
    When a change of that run record to status "FAILED" is requested
    Then the change is refused and the run record keeps status "COMPLETED"
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The whole chain is recomputed every night and a break is reported to Compliance the same day | REQ-DRI-003; NFR-035; JOB-14 |
| BR2 | Each entry's `entry_hash` is recomputed from the canonical form and its `prev_hash` compared with the entry before it | RWB-E1-008, BR3 and BR4 |
| BR3 | A run covers chain_seq 1 to the highest chain_seq at its start, in each chain it checks | This story |
| BR4 | JOB-14 runs after the ingest of `rwb.decision-record.v1` reaches the producer watermark, starting no later than 04:00, and the run record names that watermark instead of a copy job end time | Arch v5 slides 28 and 44; DP-03, DP-17; parameters `rwb.decision.chaincheck.*` |
| BR5 | A run that does not complete is reported to Compliance with the date of the last complete check | NFR-035 |
| BR6 | Only one run of JOB-14 is active at a time (overlap policy SKIP); a rerun, allowed only for a FAILED run, is a new run record with rerun true (RD-P1-065) | DP-10; Arch v5 slide 44 notes; legacy job run record |
| BR7 | Start times, latest start and batch size are parameters, not code | Principle 1; DP-06 |
| BR8 | Every service keeps its own local chain in its own schema and publishes `DecisionRecorded` on `rwb.decision-record.v1`; the run checks the central ledger and every wave-1 local chain and names a break against the service and the chain it belongs to | Arch v5 slides 20 and 28 steps 1 to 3; Temporal design slides 11 and 14; ASM-0549 |
| BR9 | A report names service names, entry IDs, `chain_seq` and hashes only, never a personal value | Legacy guardrails; Arch v5 slide 42 notes |
| BR10 | rwb-decision ingests the record into the central ledger within 5 minutes; there is no data lake and no nightly copy of the log, and a gap between a local record and the ledger is a finding of the check | Arch v5 slide 28, step 3 and slide 37; DP-17; RWB-E1-014 retired |
| BR11 | The check reads the ledger and each local chain through their owners' published read paths and reads no other service's tables | DP-01; Arch v5 slide 29 |

### 9. State transitions

None for a case status. This story changes no case status of its own; it reads the chains and asserts the result.

The run, chain and ingest states the harness observes:

| Item | States |
|---|---|
| JOB-14 run | Waiting for the ingest watermark, Running, Completed with result INTACT or BROKEN, or Failed |
| Run record | One per run, with rerun false for the scheduled run and true for a rerun; never edited |
| Central ledger chain | Sequenced from chain_seq 1 (prev_hash 64 zeros) to the last chain_seq; unbroken or broken at the first entry whose `entry_hash` or `prev_hash` does not match |
| Local chain (each wave-1 service schema) | Same, in the service's own schema, from chain_seq 1 to its own last chain_seq |
| Ingest | Received, deduplicated through `processed_event`, appended, retried through the retry topic, or dead-lettered |
| Gap | A local record with no ledger entry, or a ledger entry with no local record; open until a run closes it |
| Harness run | Not started, running, passed, failed with the failing criterion and the service named |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of the integration harness | Owns the harness, the fixtures, the tamper steps and the run report |
| rwb-decision owner (RWB-P7-E1008-APP) | Owns the ledger, the ingest, `ChainCheckWorkflow` and the Schedule |
| Platform story owner (RWB-PLT-TE008-APP) | Owns the scheduled-job and run-record parts of the check built on the service template |
| Wave-1 service teams | Own their local `decision_record`, its schema objects and the publish of `DecisionRecorded` |
| rwb-decision owner (P7) | Owns the JOB-14 run record and the rerun operation (operation pending, NEW-GAP-A1) |
| rwb-access owner (P4) | Owns the Platform administration right check and the refusal |
| RW-COMPLY Compliance and PDPA officer | Receives every report; owns the check and its parameters |
| RW-AUDIT Internal audit | Reads the run records; may not rerun |
| RW-PLATADM Platform administrator | Receives failure alerts; reruns the job |
| RW-SECADM Security administrator | Receives the break incident with Compliance |
| No role | May update, delete or repair an entry of any chain |

The tamper steps of AC2 and AC3 run as the schema owner in DEV only, on the synthetic data set, and are switched off in SIT, UAT and production; each restores the trigger in the same run and asserts the restore.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` (rwb_decision) | all fields | Read |
| DF-DEC-028 | `decision_log_entry` (rwb_decision) | chain_seq | Read |
| DF-DEC-029 | `decision_log_entry` (rwb_decision) | corrects_entry_id | Read |
| DF-DEC-030 | `decision_log_entry` (rwb_decision) | actor_user_id | Read |
| DF-DEC-001 to DF-DEC-018 | `decision_record` (each wave-1 service schema) | all fields | Read |
| DF-DEC-028 to DF-DEC-030 | `decision_record` (each wave-1 service schema) | chain_seq, corrects_entry_id, actor_user_id | Read |
| Not specified in the source documents (DOR-RWB-ITG-TE008-ITG-7) | `processed_event` (rwb_decision and each wave-1 consumer schema) | event id, consumer group, processed at | Read |
| Not specified in the source documents (DOR-RWB-ITG-TE008-ITG-7) | JOB-14 run record | business date, status, checks, ingest watermark, rerun | Read |

Field IDs are those in the Logical Data Model and Data Dictionary and are copied from RWB-TE-008. The harness owns no schema, no table and no field: it reads the ledger and the local chains through their owners' read paths and starts the Schedule through the Temporal client. The run record is the result of the `ChainCheckWorkflow` run in rwb-decision, read through the Temporal client; the earlier reading through the rwb-source-data job list (ASM-B-ITG-W1-10-TE008-2, ASM-0550) is superseded (RD-P1-012; GAP-0380); the ingest watermark that the run waits on is the producer watermark of `rwb.decision-record.v1` (ASM-B-ITG-W1-10-TE008-1; GAP-0380).

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test project and provides no REST operation; the integration service base `/api/recovery/integration/v1` and queue `rwb-integration` carry nothing new for it.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | Reads the entries of one case in chain order, page and size, to reconcile a local record with its ledger entry |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | Reads one entry by entry ID, with chain_seq, prevHash and entryHash, to confirm the named break |
| POST | Pending: path of the JOB-14 rerun, tracked as NEW-GAP-A1 | P7 rwb-decision | Reruns JOB-14 for the business date; 403 with MSG-P4-002 without Platform administration U |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Platform administration U check for the rerun and the refusal of RW-AUDIT |

Every call is one hop to the owning service on its own base (DP-11, DP-13) with the 2 s client budget; the harness calls no service through another service.

#### 12.3 Events published

None. The harness publishes no business event; topic `rwb.integration.events.v1` is not used by this story. The event the check observes is produced by every wave-1 service and is listed in 12.4.

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | Produced by every wave-1 service; consumed by P7 rwb-decision and P9 rwb-reporting | CloudEvents 1.0 binary mode, key caseId, exactly one event per append, inbox dedupe in `processed_event`, retry 1 min, 10 min, 1 h then `.dlt`; the ingest into the ledger is the watermark the run waits on |

The harness reads the topic and the consumer offsets to compute the producer watermark; the watermark definition and the local-chain scope of the check are Not specified in the source documents (GAP-0380; ASM-0549).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `ChainCheckWorkflow` | Workflow | `rwb-decision` | Input business date, the chains to check and the ingest watermark; output per chain the count checked, last chain_seq, last entry_hash, result, first break chain_seq and entry ID, failing count, gap list and the incident reference |
| `ingestDecisionRecord` | Activity | `rwb-decision` | Input the DecisionRecorded envelope; output entry ID, chain_seq and entry_hash; idempotent on the event id through `processed_event`; its offset is the ingest watermark the run waits on |

Both are registered by the rwb-decision worker (RWB-P7-E1008-APP); this story starts them through the real Schedule and asserts their output, and it adds no workflow of its own. The scope of `ChainCheckWorkflow` is the central ledger and every wave-1 local chain: it reports the first break per chain with MSG-P7-008 and raises one incident, as assumed in ASM-B-ITG-W1-10-TE008-1 (GAP-0380).

Data classes (Data Classification and Personal Data Inventory v5): `decision_log_entry` `id` (DF-DEC-001), `case_id` (DF-DEC-002) and `corrects_entry_id` (DF-DEC-029) are Not personal. `rule_id` (DF-DEC-004), `prev_hash` (DF-DEC-017), `entry_hash` (DF-DEC-018) and `chain_seq` (DF-DEC-028) are Customer data, personal. `actor_user_id` (DF-DEC-030) is a Staff identifier, personal. Wherever this story says that no personal data or no personal value is carried, it means no customer value, person's name or direct identifier. The classed fields travel only as codes, ids or business facts, never beside a direct identifier, and a user is shown in events and logs by user id only.

#### 12.6 Schedules

| Schedule | Cadence | Registration | Legacy reference |
|---|---|---|---|
| `decisionChainCheck` | Daily at 02:00 Asia/Bangkok, overlap policy SKIP, catch-up window, latest start 04:00 for the ingest watermark | Registered by the rwb-decision release; started once by the harness through the Temporal client with the same input the cadence uses | JOB-14 Hash-chain check (Quartz job in RWB-TE-008) |

#### 12.7 Tables owned

None. The harness owns no table. The tables it exercises belong to rwb_decision, to each wave-1 service schema and to the platform library, and are listed in section 11 with their owners.

#### 12.8 Contract fakes

None. This is the integration level: the real services, the real topic and the real Schedule replace the contract fakes of the app stories. No contract fake of rwb-access, rwb-decision or rwb-source-data is used by this story, so it waits on no published fake and pins no fake library version.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 4 | Two decision reads, the rwb-decision rerun (path pending, NEW-GAP-A1) and the authorise call; the run record is read through the Temporal client; one hop, 2 s (DP-11, DP-13) |
| Kafka | None | 1 event type | `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` from each wave-1 service; read for the ingest watermark |
| Temporal | None | 1 workflow, 1 activity, 1 Schedule | `ChainCheckWorkflow`, `ingestDecisionRecord`; `decisionChainCheck` at 02:00 on `rwb-decision` |
| File | None | None | No file in this story; no lake copy exists (DP-17) |

### 13. Solution plan

**Deliverables.** One test project `integration/recovery-w1/chain-check`, with the five test classes `ChainIntactIT`, `ChainBreakIT`, `IngestWatermarkIT`, `LocalLedgerGapIT` and `StoppedRunIT`, the fixture files and the run report writer.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| HarnessRunner | Runner | Preflight, run order, report and exit code |
| ChainFixtureBuilder | Service | Builds the 48,210-entry chain and the 10,000,000-entry chain deterministically through the real write path, in the ledger and in one local chain per service, with the golden canonical form |
| IngestProbe | Service | Reads `rwb.decision-record.v1` and the consumer offsets and computes the producer watermark the run waits on |
| ChainCheckDriver | Service | Starts `decisionChainCheck` once, reads the workflow result for the ledger and for each local chain, and times the incident and MSG-P7-008 from the run start |
| TamperTool | Service | DEV only: disables the trigger, changes the actions of the records with chain_seq 30,005 in one local chain and 12,001 and 40,350 in the ledger, restores the trigger and verifies the restore |
| GapDriver | Service | Holds a DecisionRecorded event in the retry topic, waits for the run to name the gap, releases the event and waits for the ingest |
| RunRecordProbe | Service | Reads the run records from the `ChainCheckWorkflow` results through the Temporal client, asserts rerun true on the rerun and the SKIP refusal of a concurrent start |
| ReportWriter | Service | One row per test case, with the evidence and the elapsed times |

**Database.** None of its own. The harness writes only through the services' own write paths, and the only direct writes are the DEV tamper steps of AC2, which restore the trigger.

**Configuration and reference data**

- The service list, the topic, the retry and `.dlt` topics, the queue, the namespace and the Schedule name, all as configuration.
- The business date 2 December 2026, the synthetic case "RW-2026-000123" and the fixture package code.
- The parameters start 02:00, latest start 04:00 and batch size 1,000, read through the rwb-case parameters contract (DP-06).
- The decision codes, outcome codes and approval levels, read through the rwb-case reference-data contract (DP-07).
- The test roles RW-COMPLY, RW-AUDIT, RW-SECADM and RW-PLATADM with their Platform administration letters, from rwb-access.
- The 08:00 same-day report limit, the 5-minute ingest target, the 60 minute budget for 10,000,000 entries and the 2 s client budget.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; a gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H, C and X dependencies the DPs name (DP-03, DP-06, DP-07, DP-10, DP-19) stay with the service, platform and operations stories this harness proves; this story carries no H, C or X dependency and its I list names the two stories whose behaviour it exercises (Template and Rules §R5.4).

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Chain of 48,210 entries | 48,210 synthetic entries through the real write path, in the ledger and in each local chain, first prev_hash 64 zeros | AC1, AC3, TC-TE-008-01-ITG, TC-TE-008-05-ITG |
| Tampered chains | Entry 30,005 changed in one service's local chain; entries 12,001 and 40,350 changed in the ledger, each with the trigger restored | AC2, TC-TE-008-02-ITG, TC-TE-008-07-ITG |
| Held event | One DecisionRecorded held in the retry topic after the local commit | AC4 |
| Stopped run | The ledger connection closed after 20,000 entries | AC5, TC-TE-008-03-ITG |
| Late ingest | The consumer offset behind the producer watermark at 02:00, reached at 02:25, and not reached by 04:00 | AC3, TC-TE-008-06-ITG |
| Appends during the run | 37 entries ingested while the run is in progress | AC3, TC-TE-008-08-ITG |
| Role set | RW-PLATADM, and RW-AUDIT whose Platform administration letter is "-" | AC4, AC5, TC-TE-008-09-ITG |
| Budget chain | 10,000,000 synthetic entries for the 60 minute timing check | AC1 |

**Run order.** Preflight; the intact run over 48,210 entries in the ledger and every local chain (AC1); the ingest watermark with the 04:00 latest start and the 37 appends (AC3); the tampered local chain and ledger entries, then the 02:00 run (AC2); the held event, the gap and the rerun (AC4); the stopped run and the refused rerun (AC5); the 10,000,000-entry budget run; cleanup of the DEV fixtures with every trigger confirmed restored. A failing step stops the run and the report names the criterion, the service and the evidence.

**Done when.** The 14 test cases of section 16 pass on the real services in DEV and SIT, the run at 02:00 names chain_seq 30,005 in the local chain and chain_seq 12,001 in the ledger, a gap is named by service and entry ID, the incident and MSG-P7-008 arrive before 08:00 the same day, a rerun carries rerun true, a stopped run sends MSG-P7-013, and the 10,000,000-entry run finishes inside 60 minutes.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-007 | The chain is intact | The decision log check for {date} passed: {count} entries checked. The last hash is {hash}. |
| MSG-P7-008 | The chain is broken, or a local record has no ledger entry | The decision log check for {date} found a break at entry {entryId}. Entries from that entry on cannot be relied on until Compliance reviews them. |
| MSG-P7-013 | The run did not complete | The decision log check for {date} did not complete. The chain was last confirmed on {lastDate}. |
| MSG-P4-002 | Rerun without Platform administration U | You cannot {action} here. Your role does not include it. |

The four texts are copied unchanged from RWB-TE-008; this story adds no message text. The route of the incident and of the report to Compliance across services is Not specified in the source documents (GAP-0380; ASM-0549). Report lines of the harness are for developers and are not part of the message standard.

### 15. Screens and states

No screen in this story, and the harness renders nothing: the run records are read through the Temporal client and the entries through the two decision reads. The job monitor screen (SCR-44 Interface and job monitor) and the administration screens that show a broken chain as a control breach come with their own stories and are out of scope here. The states the harness observes are the run, chain, ingest and gap states of section 9. SCR-44 states for this story (empty, loading, error and no access) are Not specified in the source documents (CG-ALL-502).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-ITG-TE008-01 | AC1, BR1, BR8 | End to end | 48,210 entries in the ledger and in every wave-1 local chain; the 02:00 Schedule; MSG-P7-007; the 10,000,000-entry budget |
| TC-ITG-TE008-02 | AC2, BR2, BR9 | End to end | Local chain 30,005 changed; ledger 12,001 and 40,350 changed; one incident and MSG-P7-008 before 08:00, no personal value |
| TC-ITG-TE008-03 | AC3, BR4, BR10 | End to end | Watermark behind at 02:00, reached at 02:25, not reached by 04:00; 37 appends during the run; 48,247 the next night |
| TC-ITG-TE008-04 | AC4, BR6, BR10 | End to end | Held event, the named gap, the refused rerun of the completed run, the next 02:00 run and the SKIP refusal of a concurrent start |
| TC-ITG-TE008-05 | AC5, BR5 | Integration | Connection closed after 20,000 entries; RW-AUDIT rerun refused with MSG-P4-002 |
| TC-ITG-TE008-06 | AC6, BR7, BR11 | Integration | Start time, latest start and batch size changed in configuration; a read outside the published read paths is checked |
| TC-ITG-TE008-07 | §12 operations, events and activities | Contract | Each operation in 12.2, each event in 12.4 and each activity in 12.5 checked against contract version v1; the contract story is Not specified in the source documents (DOR-RWB-ITG-TE008-ITG-21) |
| TC-ITG-TE008-08 | AC7, BR8 | Integration | Event DecisionRecorded on rwb.decision-record.v1 redelivered after ingest; one ledger entry; chain_seq and entry_hash unchanged; same entries checked on the next run |
| TC-ITG-TE008-09 | AC8, BR5 | Integration | Ledger or local chain read fails or does not answer during the run; run status FAILED; MSG-P7-013 sent with the date of the last complete check |
| TC-ITG-TE008-10 | AC9 | Integration | Run record with status COMPLETED set to FAILED; change refused and status COMPLETED kept |

The legacy acceptance criteria and their test cases belong to RWB-PLT-TE008-APP, the story that owns the eight legacy RWB-TE-008 criteria on the target services, so this story carries none of them. The new criteria AC1 to AC9 carry TC-ITG-TE008-01 to TC-ITG-TE008-06 and TC-ITG-TE008-08 to TC-ITG-TE008-10 (AC7 to AC9), and TC-ITG-TE008-07 is the contract test of section 12.

### 17. Guardrails

- No business value in code: the start time, the latest start, the batch size, the fixture sizes, the report limit and the wait intervals are configuration, and the decision codes and approval levels are reference data (DP-06, DP-07).
- No personal data in events, workflow inputs, logs, fixtures or the report: service names, entry IDs, case IDs, `chain_seq`, rule IDs and hashes only (BR9).
- Each service writes only its own schema and reads no other service's tables (DP-01); the harness reads through the published read paths, and its only direct writes are the DEV tamper steps, which are refused in SIT, UAT and production and restore the trigger.
- The check never writes to a chain and never repairs an entry; a correction is a new entry naming the one it corrects.
- One canonical form implementation serves writing and verifying; a second implementation would make a real break indistinguishable from a hash mismatch.
- One Schedule and one event type for the record: a service that publishes its own decision event on its own topic, or a second copy of the log outside the ledger, fails the run (BR10, DP-17).
- The harness never uses production data and never points at a production namespace; the incident and the report are raised in the test environment only.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-003 | Hash chain checked every day, a break reported to Compliance the same day | `decision_log_entry` and `decision_record` `prev_hash` and `entry_hash`, `ChainCheckWorkflow`, `decisionChainCheck`, MSG-P7-007, MSG-P7-008, MSG-P7-013 | TC-ITG-TE008-01 to TC-ITG-TE008-10 |

### 19. Out of scope

- The store, the ingest, the ledger, `ChainCheckWorkflow` and the two decision read endpoints (RWB-P7-E1008-APP).
- The local `decision_record` of each wave-1 service and its publish of `DecisionRecorded` (the app and DB stories of each service).
- The contract and the AsyncAPI document of `rwb.decision-record.v1` (RWB-P7-E1008-CON).
- The `decision_log_entry` and `decision_record` schema design, the append-only trigger and the grants (RWB-P7-E1008-DB).
- The registration, the overlap policy and the catch-up window of the Schedule as a deployment step, and the scheduled-job and run-record parts of the check on the service template (RWB-PLT-TE008-APP).
- The Platform administration right and its refusal in rwb-access; this story exercises it and owns none of it.
- The check of each entry returned by an audit query, the Decision log query screen and the administration screens that show a broken chain as a control breach.
- The daily ledger seal to immutable storage (Arch v5 slide 14, step 4).
- The definition of the ingest watermark and the local-chain scope of the check until they are published (GAP-0380).

### 20. Remaining delivery steps

- Size the story (squad; DOR-RWB-ITG-TE008-ITG-16).
- Sign the epic design (solution architect).
- Fix the contract dependencies and publish the contracts of the two decision reads (rwb-decision team).
- Load the synthetic test data and register the 02:00 Schedule in DEV and SIT (QA with the rwb-decision team).
- Run the Test Cases v9 rows for the changed AC1, AC4 and AC5: TC-ITG-TE008-01, TC-ITG-TE008-04, TC-ITG-TE008-05.
- Pending: path and answers of the rwb-decision rerun of JOB-14, owner solution architect, tracked as NEW-GAP-A1.
- The JOB-14 rerun accepts a FAILED run only (RD-P1-065); publish its operation and refusal code (owner: rwb-decision owner, NEW-GAP-A1).
