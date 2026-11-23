# RWB-PLT-TE008-APP Decision log hash chain check
SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-TE008-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-TPL |
| Wave | 0 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP10, DP13, DP17, DP19 |
| Parallel lane | L-PLT-TPL-P |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P7-E1008-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-014, FR-PLT-015) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: rework of RWB-TE-008 for the 19-schema target. The decision log is no longer one central table: each of the 19 services writes its decision record in its own schema `rwb_<name>` in the same transaction as the state change, hash-links it to the record before, and publishes `DecisionRecorded` through its outbox, and rwb-decision ingests it into the central ledger and seals a daily fingerprint in write-once storage. The chain check therefore becomes a template capability — one reusable Temporal Schedule template in the workflow kit and one chain-check library in the service template, applied to every service's own local chain, with one instance for the central ledger — and Quartz JOB-14 becomes a Temporal Schedule owned by rwb-decision (DP-10). The data lake is removed (DP-17), so the legacy decision-log copy job is retired and the check waits for the day's ledger ingest instead of that copy. The legacy acceptance criteria are kept word for word and re-pointed, and every legacy value is unchanged (48,210 entries; chain_seq 30,005; 20,000 entries; chain_seq 12,001 and 40,350; 37 entries; 2 and 3 December 2026; 02:25; 04:00; 08:30; user U-9301). One criterion is added for the template, the per-service chain and the retired copy job, and the legacy contract table is rewritten: this platform story provides no REST operation of its own. The integration copy of the same legacy key is RWB-ITG-TE008-ITG. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **internal auditor (RW-AUDIT)**, I want **the hash chain of the decision log checked every night — on each service's own local chain and on the central ledger — with each run recorded against the last hash and a break, an incomplete run or an intact chain reported to Compliance the same day**, so that **a changed entry is found the day it happens and the log can be relied on in audit**.

The rework keeps the intent of RWB-TE-008 and changes the object of the check. In the monolith the decision log is one table in one `recovery` schema, one Quartz job walks it from `chain_seq` 1 to the highest value at its start, and a nightly copy to the data lake at 01:00 runs before it so that the check works on a settled copy. Arch v5 removes both assumptions: the log is written locally by each of the 19 services into its own schema in the same transaction as the state change and collected centrally by rwb-decision (slides 20 and 28), and there is no data lake at all (DP-17). A single nightly walk of one table is therefore no longer a description of the evidence.

What this story builds is the check as a capability rather than as one job: a reusable Temporal Schedule template in the workflow kit, a chain-check library in the service template, and the instance of that template that owns the central ledger in rwb-decision, which is where JOB-14 goes on the Ownership Map (owner P7, mechanism Schedule, 02:00). Every service generated from the template gets the same check over its own chain, with no new code, and the central ledger gets the one instance this story must land.

Everything a role sees or reads stays as the legacy story left it: the same roles, the same three report messages and the same refusal message, the same nightly start, the same latest start, the same batch size, the same rerun path and every legacy number. What changes is where the values come from and where the run record lives — the parameters come through the parameters contract of rwb-case, the calendar and the service list through its reference-data contract, the schedule through the workflow kit, and the run record is the workflow history of the Schedule instead of an ACE job run row.

### 2. Business rationale

The decision log is evidence only while nobody can change an entry unseen. Each service refuses updates and deletes inside its own schema, but a change made outside the service, for example by a database administrator, is found only by recomputing the chain. This story runs that check every night after the day's ledger ingest, records each run with its last hash, and tells Compliance of a break, an incomplete run or an intact chain. It meets REQ-DRI-003 and NFR-035 and supports control CTL-06. The measure is a daily check with a same-day report: target 100 percent of nights.

The change the rework carries is the object of the check and the vehicle that runs it. Slide 28 puts the decision record inside each of the 19 services: the service writes the record and the change in one transaction, the record is chained to the one before it so gaps or edits show, rwb-decision reads the shared topic into the central ledger within 5 minutes, and a fingerprint of the ledger is sealed daily into write-once storage. Slide 20 gives every service the same block — its own schema, its own outbox and inbox, its own `decision_record` table, its own task queue and its own Schedules. Slide 29 makes the boundary hard: one login per service, grants on its own schema only, no cross-schema join and no cross-schema key, and a boundary test in every build. A chain therefore exists per service, not only centrally, and a check that reads one central table would miss a change in a service's own chain altogether. That is the reason the check becomes a template capability: the same recomputation runs inside the service that owns the chain, on its own schema, and the central ledger gets its own instance through the contract that publishes the ledger.

The vehicle changes with it. Quartz is replaced by Temporal Schedules in the owning service (DP-10; slide 44, JOB-14 owner rwb-decision, mechanism Schedule at 02:00), so the run record is the workflow history of that Schedule and no shared Quartz table is written. The data lake is removed (DP-17), so the 01:00 copy that the legacy check waits for no longer exists; the check waits instead for the day's central-ledger ingest to be reported complete, which is the signal that the ledger holds the business date's records. And the parameters are no longer values in code or in a catalog the job reads directly: they are read through the parameters contract of rwb-case (DP-06) and the calendar and service list through its reference-data contract (DP-07), so the same three legacy keys keep their values without a build to change them.

The estate this check protects is the one the 19 services write, and every service's chain is only as good as the code that computes it: one canonical-form implementation shared with the writer, which is the local decision-record library of RWB-PLT-E1027-CON (DP-03). The 19 schemas and their logins are database work outside this story. What this story owns is the check itself — its template, its library, its schedule definition, its report and its run states — and the proof that a break in any chain, a run that does not complete, or a service with no check at all is visible to Compliance the same day.

### 3. Preconditions

- **RWB-PLT-E1071-CON** is published: the Temporal worker and SDK in the recovery module and the workflow kit that carries the Schedule templates (DP-10). The chain check is one template of that kit, not a second scheduler.
- **RWB-PLT-E1042-CON** is published: the parameters contract of rwb-case and its client library (DP-06). The three parameter keys and their values are read through it and are never values in code.
- **RWB-PLT-E1043-CON** is published: the reference-data contract of rwb-case and its versioned tables (DP-07). The business-date calendar and the list of the services whose chains are checked are reference rows read through it.
- **RWB-PLT-E1027-CON** is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03). The chain-check library recomputes the hash with the same canonical form that library writes, so the check and the writer cannot drift apart.
- **RWB-PLT-N001-CON** is published: the gateway-bff composite route contract (DP-19). The readiness and run surface a role reads is a composite route behind gateway-bff; this story provides no route of its own.
- The **three service CON dependencies of the run** are published: **RWB-P3-E1042-CON** (parameters), **RWB-P3-E1043-CON** (reference data) and **RWB-P7-E1008-CON** (the decision log store, append-only and hash-chained, which publishes the central ledger's chain read). All three are consumed as published contracts and their fakes, so none blocks the build (Template and Rules §R5.4, C).
- rwb-decision (P7) ingests `DecisionRecorded` from `rwb.decision-record.v1` idempotently into the central ledger within 5 minutes and reports, per business date, whether the ingest for that date is complete (Arch v5 slides 20 and 28).
- Every service generated from the template writes its decision record in its own `rwb_<name>` schema in the same transaction as the state change, hash-links it to the record before, and publishes it through its outbox (Arch v5 slide 20; DP-03).
- The Compliance and PDPA officer group, the platform administrator group and the security administrator group are set in the ACE notification path, with RW-COMPLY as the owner of the three parameters.
- The schedule ID and its display name, the precise catch-up and backfill semantics of the Schedule, the completeness signal of the ledger ingest, where run records are read from, the retention of those run records and the report channel to Compliance are Not specified in the source documents (GAP-1437); the working defaults of section 13 are ASM-2528, ASM-2529 and ASM-2530.

### 4. Flow

1. Temporal Schedule: the `ChainCheckSchedule` instance in rwb-decision fires at 02:00 Asia/Bangkok for the business date of the previous day, on the owner's task queue `rwb-decision` in namespace `rwb-recovery` (DP-10; Arch v5 slide 44, JOB-14 owner P7, time 02:00, mechanism Schedule).
2. ChainCheckRunner: reads `rwb.decision.chaincheck.start`, `rwb.decision.chaincheck.latest-start` and `rwb.decision.chaincheck.batch-size` through the parameters contract of rwb-case (DP-06), and the business-date calendar and the list of services whose chains are checked through the reference-data contract (DP-07).
3. LedgerIngestWait: holds the run until rwb-decision reports the business date's ledger ingest complete, and stops waiting at the latest start of 04:00, recording the state it saw. This replaces the wait for the retired decision-log copy job (DP-17; ASM-2529).
4. ChainStateReader: for each chain of the run, reads the highest `chain_seq` at the start and fixes it as the end of the run; entries appended later are checked the next night. A service's chain is read only by that service's own instance of the template, and the central ledger's chain only through `RWB-P7-E1008-CON` (DP-01).
5. ChainCheck: recomputes each entry's `entry_hash` from the canonical form of the shared library and compares each `prev_hash` with the entry before, over `chain_seq` 1 to the end, in batches of the configured batch size (1,000).
6. ChainCheck: counts every entry that fails and keeps the first, with its `chain_seq` and entry ID.
7. ChainCheckRunner: ends the run with the run record in the workflow history of the Schedule: type chain check, business date, chain, status, entries checked, last `chain_seq`, last `entry_hash`, result, first break `chain_seq` and entry ID, failing count, rerun, and the ingest state it waited on.
8. ChainCheckReporter: sends MSG-P7-007 to the Compliance group when the chain is intact, or MSG-P7-008 with an incident when it is broken.
9. ChainCheckReporter: on an error that stops the run, records status FAILED, alerts the platform administrator and sends MSG-P7-013 to the Compliance group.
10. Platform administrator: can rerun the check for the business date through the gateway-bff readiness view; a rerun is a new run and does not interrupt a run that is active.
11. Internal auditor: reads the run states and the last confirmed date through the gateway-bff composite route behind `RWB-PLT-N001-CON`, and never through a path of this story (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | An entry does not match its hash or its prev_hash, in a service's local chain or in the central ledger | Run result BROKEN; first break and failing count recorded; incident; Compliance told | MSG-P7-008 | AC2, AC7 |
| X2 | The run stops on an error, for example a lost database connection | Status FAILED; platform administrator alerted; Compliance told the check did not complete | MSG-P7-013 | AC3 |
| X3 | The check is rerun for the same business date | A new run with the same checks; the report says it is a rerun; no second scheduled run starts | MSG-P7-007 or MSG-P7-008 | AC4 |
| X4 | The chain is empty | Result INTACT with count 0 and the genesis hash of 64 zeros | MSG-P7-007 | AC5 |
| X5 | The business date's ledger ingest is reported complete after 02:00 | The run waits up to 04:00, starts when the ingest completes, and records the ingest completion state it waited on where the legacy run recorded the copy end time | MSG-P7-007 or MSG-P7-008 | AC6 |
| X6 | Entries are appended while the run runs | They are outside this run and are checked the next night | None | AC8 |
| X7 | The day's ledger ingest is not complete for the business date by the latest start | The run starts at 04:00 with the note that the ingest was not complete, records the ledger portion it checked, and Compliance is told the check did not cover the whole date; the missing records stay open in the ledger | MSG-P7-013 | AC6, AC9 |
| X8 | A service generated from the template has no chain-check schedule, or a service of the reference list has no chain instance | The readiness view shows that service as not covered instead of intact; the platform administrator is alerted and Compliance is told the chain of that service was not confirmed; the coverage gap is raised to the platform team | MSG-P7-013 | AC9 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the workflow kit and the parameters, reference-data and decision-record contracts; the ledger chain read comes through a contract and its fake, so no service has to be built first; no screen |
| Negotiable | The schedule ID, the catch-up semantics, the ingest completeness signal, the run-record surface and the retention are working defaults recorded as assumptions; the three parameter values, the roles, the messages and the run states are fixed by the legacy story and NFR-035 |
| Valuable | A changed entry is found by the morning after it is changed, in whichever chain holds it, and a chain nobody checks is visible instead of silently trusted |
| Estimable | One workflow-kit template, one library in the service template, one ledger instance, one report, one readiness view, no table and no screen |
| Small | Fits in one week with its tests |
| Testable | Each criterion below is one test in section 16, with the three contract fakes of section 12.8 and the schedule's own clock |

### 7. Acceptance criteria

```gherkin
Feature: Decision log hash chain check

  Background:
    Given the environment is SIT with the synthetic decision log
    Given JOB-13 for business date 2 December 2026 ended at 01:40 on 3 December 2026

  Scenario: AC1 Chain intact (legacy RWB-TE-008 AC1)
    Given the rwb-case parameter contract mock returns rwb.decision.chaincheck.start=02:00, rwb.decision.chaincheck.latest-start=04:00 and rwb.decision.chaincheck.batch-size=1000
    Given the decision log holds 48,210 entries and none has been changed
    When JOB-14 runs at 02:00 on 3 December 2026
    Then the job run record shows type "JOB-14", business date 2 December 2026, status "COMPLETED" and result "INTACT"
    Then its checks hold entries checked 48,210, last chain_seq 48,210 and that entry's entry_hash
    Then MSG-P7-007 with the count and the last hash is sent to the Compliance group

  Scenario: AC2 Break (legacy RWB-TE-008 AC2)
    Given the actions of the entry with chain_seq 30,005 were changed in the SIT database with the trigger disabled
    When JOB-14 runs
    Then the run result is "BROKEN" with first break chain_seq 30,005 and its entry ID
    Then the system raises an incident and MSG-P7-008 with the entry ID is sent to the Compliance group before 08:00 on 3 December 2026

  Scenario: AC3 A run that stops is reported (legacy RWB-TE-008 AC3)
    Given the database connection is closed in the test double after 20,000 entries
    When JOB-14 runs
    Then the run status is "FAILED" with entries checked 20,000
    Then the system alerts the platform administrator group
    Then the system sends MSG-P7-013 to the Compliance group with the date of the last complete check, 2 December 2026

  Scenario: AC4 A rerun gives a new record and no second scheduled run (legacy RWB-TE-008 AC4)
    Given JOB-14 for business date 2 December 2026 failed at 02:20
    When test user "U-9301" holding RW-PLATADM reruns it from the job monitor at 08:30
    Then a second run record for business date 2 December 2026 is written with rerun true
    Then the system marks the report to Compliance as a rerun
    Then while the rerun is running a second start of JOB-14 is refused by the scheduler

  Scenario: AC5 An empty log is intact (legacy RWB-TE-008 AC5)
    Given the decision log holds no entry
    When JOB-14 runs
    Then the result is "INTACT" with entries checked 0 and last hash of 64 zeros

  Scenario: AC6 The job waits for the decision log copy (legacy RWB-TE-008 AC6)
    Given JOB-13 for business date 2 December 2026 is still running at 02:00 and ends at 02:25
    When JOB-14 fires at 02:00
    Then it starts the check at 02:25 and records the JOB-13 end time
    Then if JOB-13 has not ended by 04:00 the check starts at 04:00 with the note "JOB-13 not ended"

  Scenario: AC7 Several changed entries (legacy RWB-TE-008 AC7)
    Given the entries with chain_seq 12,001 and 40,350 were changed in the SIT database
    When JOB-14 runs
    Then the first break is chain_seq 12,001 and the failing count is 2
    Then one incident and one MSG-P7-008 report name both entry IDs

  Scenario: AC8 Entries written during the run (legacy RWB-TE-008 AC8)
    Given the log holds 48,210 entries when JOB-14 starts
    Given 37 entries are appended while it runs
    When the run ends
    Then entries checked is 48,210 and last chain_seq is 48,210
    Then the next night's run checks 48,247 entries

  Scenario: AC9 The schedule, the per-service chain and the retired copy job (new, D-RCV-60)
    Given the ChainCheckSchedule template is in the workflow kit and the chain-check library is in the service template
    Given the rwb-case parameter contract mock returns rwb.decision.chaincheck.start=02:00, rwb.decision.chaincheck.latest-start=04:00 and rwb.decision.chaincheck.batch-size=1000
    Given the rwb-case reference-data contract mock returns the business-date calendar and the list of the 19 services
    When the schedule fires at 02:00 in Asia/Bangkok for the business date of the previous day
    Then the run starts on task queue rwb-decision as a Temporal Schedule and takes the start time, the latest start and the batch size from the parameter contract
    Then every service generated from the template recomputes its own local rwb_<name> chain through the chain-check library and reads no other service's schema
    Then the ledger instance reads the central ledger's chain through RWB-P7-E1008-CON
    Then the run waits for the business date's ledger ingest to be reported complete and waits for no copy job of the data lake
    When a chain is broken or the run does not complete
    Then ChainCheckReporter reports it to the Compliance group the same day
    Then no REST path of the monolith is called and this story provides no REST operation of its own
```

**Note on the criteria.** AC1 to AC8 are the legacy criteria of RWB-TE-008, copied word for word with the origin tag added to each `Scenario` line; no legacy line and no legacy value was changed. AC1 carries one extra `Given` as its first step, the parameter answer the run reads through the contract of rwb-case, and every legacy `Given`, `When` and `Then` of AC1 is kept. AC9 is the only new criterion and it carries no business value: it tests the template, the per-service chain, the ledger instance and the retired copy job of the target. JOB-13 is retired under DP-17, so the copy the legacy background and AC6 name no longer exists; the wait they describe is exercised against the business date's ledger ingest completeness signal, which is ASM-2529, and the gap of that replacement is GAP-1437.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The whole chain is recomputed every night, on every chain of the estate — each service's local `rwb_<name>` chain and the central ledger — and a break is reported to Compliance the same day | REQ-DRI-003; NFR-035; JOB-14; Arch v5 slides 20 and 28 |
| BR2 | Each entry's entry_hash is recomputed from the canonical form of the shared decision-record library and its prev_hash compared with the entry before; one canonical-form implementation is shared with the writer | Legacy RWB-E1-008, BR3 and BR4; DP-03; `RWB-PLT-E1027-CON` |
| BR3 | A run covers chain_seq 1 to the highest chain_seq of that chain at its start; entries appended later are checked the next night | This story (legacy BR3, per chain) |
| BR4 | The check runs for a business date after that date's ledger ingest is complete and starts no later than 04:00, at 02:00 by default; the three values are read through the parameters contract | Legacy batch.txt, daily timeline; parameters rwb.decision.chaincheck.*; DP-06; Arch v5 slide 44 |
| BR5 | A run that does not complete is reported to Compliance with the date of the last complete check | NFR-035 |
| BR6 | Only one run of a chain is active at a time and the Schedule never runs twice at once; a rerun is a new run and changes nothing else | Legacy RWB-TE-007; Temporal Schedule overlap policy (Arch v5 slide 44); DP-10 |
| BR7 | Start times and batch size are parameters, not code; the calendar and the list of chains are reference rows | Principle 1; DP-06; DP-07 |
| BR8 | The chain check is one capability: a single Temporal Schedule template in the workflow kit plus a chain-check library in the service template, generated into every service and applied to that service's own local chain, with one instance for the central ledger in rwb-decision; no service and no instance reads another service's chain or schema | Arch v5 slides 20, 28 and 29; DP-01, DP-03, DP-10; this story |

### 9. State transitions

None. This story does not change a case status. A run moves from Waiting for the ledger ingest to Running, then to Completed with result INTACT or BROKEN, or to Failed, and a second start of a chain that is already running is Skipped.

| From | Event | Condition | To |
|---|---|---|---|
| Not started | The Temporal Schedule fires for the business date | None | Waiting for the ledger ingest |
| Waiting for the ledger ingest | rwb-decision reports the business date's ingest complete | Before the latest start of 04:00 | Running (the start and the ingest completion are both recorded) |
| Waiting for the ledger ingest | The latest start of 04:00 is reached | The ingest is not reported complete | Running with the note that the ingest was not complete (X7) |
| Running | Every entry of every chain of the run matches | None | Completed INTACT |
| Running | An entry does not match its hash or its prev_hash | None | Completed BROKEN (first break and failing count recorded) |
| Running | The run stops on an error | None | Failed (platform administrator alerted, Compliance told) |
| Running | A second start of the same chain is requested | A run is active | Skipped (the active run is not interrupted; the request is recorded) |
| Completed or Failed | The platform administrator reruns the business date | The earlier run has ended | Running (a new run, marked as a rerun) |
| Any state | The service has no chain-check instance | The service is on the reference list | Not covered (shown by the readiness view, X8) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DECLOG Decision log writer | The identity the check runs under: in the legacy one service identity that reads the log, in the target each instance runs under the login of the service that owns the chain, and the central-ledger instance reads the ledger through `RWB-P7-E1008-CON`; no instance writes an entry |
| RW-COMPLY Compliance and PDPA officer | Receives every report and the incident; owns the three parameters and their values through the parameters contract (DP-06) |
| RW-AUDIT Internal audit | Reads the run states and the last confirmed date through the gateway-bff composite route; may not rerun |
| RW-PLATADM Platform administrator | Receives failure alerts and coverage alerts; reruns a business date; reads the readiness and run surface behind gateway-bff |
| RW-SECADM Security administrator | Receives the break incident with Compliance |
| No role | May read another service's chain or schema, repair or rewrite an entry, start a second run of a chain that is running, change a parameter value in code, or reach the check through a path of the monolith |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read |
| DF-DEC-028 | decision_log_entry | chain_seq | Read |
| DF-DEC-030 | decision_log_entry | actor_user_id | Read |
| DF-DEC-029 | decision_log_entry | corrects_entry_id | Read |

Field IDs are those in the Logical Data Model and Data Dictionary. The run result is written to the workflow history of the Schedule, not to a recovery table.

`decision_log_entry` now lives in `rwb_decision` (P7 rwb-decision, Ownership Map, Arch v5 slides 29 and 41), and each service's decision records live in that service's own `rwb_<name>` schema. This story reads a service's chain only inside that service's own instance of the template, under that service's own login, and it never reads across a schema boundary (DP-01; Arch v5 slide 29). The central ledger's chain is read through `RWB-P7-E1008-CON`, which is the owner's contract, not a table of the owner. The run record is the Temporal workflow history of the Schedule and its activities — status, business date, chain, entries checked, last `chain_seq`, last `entry_hash`, result, first break, failing count, rerun and the ingest state it waited on — and it is not an ACE job run row and not a table this story creates.

Where the run records are read from, how long they are kept and which retention the schedule history of the `rwb-recovery` namespace carries are Not specified in the source documents (GAP-1437); the working default of section 13 and ASM-2530 is the workflow history of the Schedule plus the gateway-bff readiness view, with no new platform table.

### 12. Contract

The service row of this story is `platform`, which is not one of the 19 service rows of Template and Rules §R4: it has no REST base, no topic, no task queue and no schema of its own, and none is invented for it. The one instance this story lands runs inside rwb-decision (P7), on that service's queue, under that service's login.

#### 12.1 REST operations provided

None. This platform story provides no REST operation, no REST base, no topic, no task queue and no schema of its own, and none is invented. The check is a Temporal Schedule and its activities, and the readiness and run surface a role reads is a gateway-bff composite route behind `RWB-PLT-N001-CON` (DP-19), owned by the gateway, not by this story.

#### 12.2 REST operations consumed

None as a path of this story: the ledger chain read and the two parameter and reference-data reads are consumed as published contracts and their fakes, and no path, version or payload of them is repeated here.

| Contract dependency | Owner | What this story needs from it |
|---|---|---|
| `RWB-P3-E1042-CON` (the platform contract behind it is `RWB-PLT-E1042-CON`) | P3 rwb-case | The parameter catalog: `rwb.decision.chaincheck.start`, `rwb.decision.chaincheck.latest-start` and `rwb.decision.chaincheck.batch-size`, with their values, their type and their effective dating (DP-06) |
| `RWB-P3-E1043-CON` (the platform contract behind it is `RWB-PLT-E1043-CON`) | P3 rwb-case | The business-date calendar and the list of services whose chains the run checks, with the reference-data version in force (DP-07) |
| `RWB-P7-E1008-CON` | P7 rwb-decision | The central ledger's chain as the owner publishes it: the highest `chain_seq`, the entries in `chain_seq` order with `prev_hash` and `entry_hash`, and the completeness state of the ingest for a business date (DP-01, DP-03) |

The ledger chain read is one hop to the owning service on that service's own base with the 2 s client budget (DP-11, DP-13); the path itself belongs to `RWB-P7-E1008-CON`.

#### 12.3 Events published

None. The check publishes no event: it reads chains and reports through the ACE notification path. The decision records it checks travel on the shared topic `rwb.decision-record.v1`, produced by the owning services through their outboxes and consumed by rwb-decision (Arch v5 slides 20 and 28); this story produces nothing on a topic and owns no topic.

#### 12.4 Events consumed

None. The run waits on the ledger ingest completeness state of the business date, which it reads through `RWB-P7-E1008-CON`, and not on a topic subscription; the completeness signal itself is a gap (GAP-1437; ASM-2529).

#### 12.5 Workflows and activities

| Workflow or activity | Where it runs | What it does |
|---|---|---|
| `ChainCheckWorkflow`, from the workflow-kit template `ChainCheckSchedule` | namespace `rwb-recovery`; on task queue `rwb-decision` for the ledger instance, and on each generated service's own queue for that service's instance | Wraps the run: waits for the ingest, fixes the end `chain_seq` per chain, drives the batch check, ends the run record and hands the result to the report |
| Activity `ChainCheck` | the same queue | Recomputes `entry_hash` with the shared canonical form and compares `prev_hash`, in batches of the configured size; counts every failing entry and keeps the first |
| Activity `LedgerChainRead` | the same queue | Reads the central ledger's chain and the business date's ingest completeness through `RWB-P7-E1008-CON`; used by the ledger instance only |
| Activity `ChainReport` | the same queue | Sends MSG-P7-007, MSG-P7-008 or MSG-P7-013 to the Compliance group and raises the incident on a break |

The wait of step 3 has no activity of its own: it is a durable timer in the workflow plus the ingest completeness answer read on each poll, so a run holds no worker slot while it waits.

#### 12.6 Schedules

| Item | Value |
|---|---|
| Template | `ChainCheckSchedule`, a specialisation of the workflow kit's Scheduled job template (Temporal design slide 12, layer L3; DP-10) |
| Schedule ID and display name | Not specified in the source documents (GAP-1437); `chain-check-daily` and "Daily decision log hash chain check" are the working defaults of ASM-2528 |
| Instance owner | rwb-decision (P7), per the Ownership Map row for JOB-14 and Arch v5 slide 44 (owner rwb-decision, time 02:00, mechanism Schedule) |
| Cron | `0 0 2 * * ?` in Asia/Bangkok, the legacy cron kept; the start time is read through `rwb.decision.chaincheck.start` (02:00) and is a parameter, not code |
| Latest start | 04:00, read through `rwb.decision.chaincheck.latest-start`; the run starts at the latest start and records a late or incomplete ingest |
| Batch size | 1,000, read through `rwb.decision.chaincheck.batch-size` |
| Catch-up and backfill | One business date only, as a parameter; a missed run is caught up once for the most recent business date and no run chains several missed days together; a rerun of an older business date is an explicit rerun by business date (GAP-1437; ASM-2528) |
| Overlap policy | One run at a time: a start while a run is active is skipped and the active run is not interrupted, which is the legacy DisallowConcurrentExecution carried over and the overlap policy of Arch v5 slide 44 (AC4, BR6) |
| Per-service instances | Generated with each service from the template at 02:00 in that service's own namespace queue and over that service's own chain; this story publishes the template and lands only the ledger instance |

#### 12.7 Tables owned

None. This story owns no table, creates no schema and writes no row: the run record is the workflow history of the Schedule, the ledger tables are rwb-decision's, and each service's `decision_record` table is that service's own (DP-01; Arch v5 slides 20 and 29).

#### 12.8 Contract fakes

| Fake | Serves | Documented answer used by the tests |
|---|---|---|
| rwb-case parameters fake | `RWB-P3-E1042-CON` behind `RWB-PLT-E1042-CON` | `rwb.decision.chaincheck.start=02:00`, `rwb.decision.chaincheck.latest-start=04:00` and `rwb.decision.chaincheck.batch-size=1000`, with a changed latest start for the X7 case (AC1, AC6, AC9, TC-TE-008-06, TC-PLT-TE008-APP-10) |
| rwb-case reference-data fake | `RWB-P3-E1043-CON` behind `RWB-PLT-E1043-CON` | The business-date calendar with 2 December 2026 as the date of the run, a reference-data version, and the list of the 19 services; the same list with one service removed for the X8 case (AC9, TC-PLT-TE008-APP-10) |
| rwb-decision ledger fake | `RWB-P7-E1008-CON` | A chain of synthetic entries with `prev_hash` and `entry_hash`, the highest `chain_seq`, a changed entry, an empty chain, and a business date whose ingest is reported complete late and then not at all (AC1, AC2, AC5, AC6, AC7, AC9) |

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | None provided, 1 contract consumed | No REST operation of this story; the ledger chain read is consumed as `RWB-P7-E1008-CON`, one hop, 2 s (DP-11, DP-13) |
| Kafka | None | The check publishes and consumes no event of its own; the records it checks travel on `rwb.decision-record.v1`, produced by the owning services, and the ledger ingest that completes them is rwb-decision's |
| Temporal | 1 Schedule, 3 activities | The `ChainCheckSchedule` template and its instance in rwb-decision, the workflow `ChainCheckWorkflow`, and the activities `ChainCheck`, `LedgerChainRead` and `ChainReport` on the owner's queue (DP-10) |
| File | None | The daily ledger fingerprint in write-once storage is rwb-decision's and is out of scope; this story writes no file |

### 13. Solution plan

**Package.** The chain-check library goes into the service-template module that every service is generated from (`recovery-service-template`, Java package `th.co.scb.ace.workbench.recovery.template.chaincheck`), and the Schedules template goes into the workflow kit (`recovery-workflow-kit`, platform-owned, layer L3 of the Temporal layer model, Temporal design slide 12). The ledger instance is generated into rwb-decision from the same two artifacts, and this story adds no second scheduler.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-13 | The monolith REST base | `/api/recovery/<short>/v1` | none |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ChainCheckScheduleTemplate | Workflow-kit template | The reusable Schedule template: cron, latest start, batch size, catch-up and overlap policy as parameters, with no business term in its interface (BR7, BR8; DP-10) |
| ChainCheckRunner | Workflow and activity pair | Fixes the end `chain_seq` per chain, drives the batch recomputation, ends the run record in the workflow history (BR1, BR3) |
| ChainStateReader | Library | Reads one chain in `chain_seq` order inside the schema of the service the instance runs in, and the central ledger through `RWB-P7-E1008-CON`; never reads across a schema boundary (BR2, BR8; DP-01) |
| LedgerIngestWait | Workflow step | Durable timer plus the ingest completeness answer of the business date, stopping at the latest start (BR4, X5, X7) |
| ChainCheckReporter | Activity | Sends MSG-P7-007, MSG-P7-008 or MSG-P7-013 to the Compliance group and raises the incident on a break (BR1, BR5) |
| ChainCheckRunView | Read model behind gateway-bff | The readiness and run surface: per chain and business date, the last run, its result, its last `entry_hash` and the date of the last complete check; it calls the owning service through the composite route and holds no table (DP-19) |

**Database.** No new business table, no schema and no Flyway migration. The check reads an entry table that the owning service already has, and its run record is the workflow history of the Schedule; nothing is written except the report and the incident, which the ACE notification path and the incident channel own.

**Configuration and reference data.**

- `rwb.decision.chaincheck.start=02:00`, `rwb.decision.chaincheck.latest-start=04:00` and `rwb.decision.chaincheck.batch-size=1000`, read through the parameters contract of rwb-case (DP-06; `RWB-PLT-E1042-CON`, `RWB-P3-E1042-CON`) and owned by RW-COMPLY; the values are the legacy ones and are never values in code.
- The business-date calendar and the list of services whose chains are checked, read as reference rows with their version through the reference-data contract (DP-07; `RWB-PLT-E1043-CON`, `RWB-P3-E1043-CON`); the reference-data version in force is recorded with the run.
- The ledger chain and the business date's ingest completeness, read through `RWB-P7-E1008-CON`.
- The schedule parameters of the template: the schedule ID `chain-check-daily`, the display name "Daily decision log hash chain check", the catch-up rule and the overlap policy, the working defaults of ASM-2528 (GAP-1437).
- Feature flag: `rwb.decision.hash-check`, unchanged from the legacy story.

**Build steps**

1. Add the `ChainCheckSchedule` template to the workflow kit: cron, latest start, batch size, catch-up and overlap policy as parameters, one run at a time (BR6, BR7; DP-10).
2. Build ChainStateReader and the shared canonical-form call against `RWB-PLT-E1027-CON`, with the boundary rule that an instance reads only its own schema or the ledger contract (BR2, BR8; DP-01).
3. Build ChainCheckRunner and the `ChainCheck` activity with the batch walk and the fixed end `chain_seq`; tests for AC1, AC5 and AC8.
4. Build the counting of every failing entry and the first break; tests for AC2 and AC7.
5. Build LedgerIngestWait with the 04:00 latest start and the incomplete-ingest note; test AC6 and X7 against the ingest completeness fake.
6. Build ChainCheckReporter with the three messages and the incident; tests for AC1, AC2 and AC3.
7. Land the ledger instance in rwb-decision with `LedgerChainRead` on the owner's queue, and generate the per-service instance from the template in a throwaway service; test the rerun path and the concurrency guard for AC4 and the coverage case X8 for AC9.
8. Run the timing check on 10 million synthetic entries against a 60 minute budget (assumed; DL11), and record the schedule ID, the catch-up rule and the run-record retention as the open items of GAP-1437.

**Done when.** The ten test cases of section 16 pass, the template has produced a chain-check instance for the central ledger and for one generated service, a break in either chain reaches the Compliance group the same day, a run that waits on the ingest starts at the latest start and says so, a service with no instance shows as not covered, and the run book of the legacy JOB-14 has been rewritten for the Schedule and the readiness view (RWB-E1-056).

The schedule ID, the catch-up and backfill semantics, the ingest completeness signal, the run-record surface and retention, and the report channel to Compliance are Not specified in the source documents (GAP-1437); the working defaults are ASM-2528, ASM-2529 and ASM-2530, and the solution architect closes them before the template is published.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-007 | The chain is intact (new) | The decision log check for {date} passed: {count} entries checked. The last hash is {hash}. |
| MSG-P7-008 | The chain is broken | The decision log check for {date} found a break at entry {entryId}. Entries from that entry on cannot be relied on until Compliance reviews them. |
| MSG-P7-013 | The run did not complete (new) | The decision log check for {date} did not complete. The chain was last confirmed on {lastDate}. |
| MSG-P4-002 | Rerun without Platform administration U | You cannot {action} here. Your role does not include it. |

The four texts are copied unchanged from RWB-TE-008 and this story adds no message text. In MSG-P7-007, MSG-P7-008 and MSG-P7-013 the {date} is the business date of the run and, where the run covers more than one chain, the report names the chain and the service that owns it; the entry ID and the `chain_seq` are the only identifiers reported. Thai text for each message follows DL10; the proposed Thai for the two new messages is in the additions file.

### 15. Screens and states

No screen in this story, and no new screen state. The run states of section 9 are read on the readiness and run surface, which is a gateway-bff composite route behind `RWB-PLT-N001-CON` (DP-19) over the owner's read model and the workflow platform's visibility: per chain and business date, the last run, its result, the last `entry_hash`, the date of the last complete check, and the services that have no chain-check instance. This story invents no route, no path and no screen; the composite route and its operations belong to the gateway and to the stories that publish them.

Compliance receives each report by the ACE notification path, as in the legacy story, and never from a screen of this story.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-008-01 | AC1, BR1, BR2 | Component | 48,210 synthetic entries, none changed |
| TC-TE-008-02 | AC2, BR1 | Component | One entry changed in SIT with the trigger disabled |
| TC-TE-008-03 | AC3, BR5 | Component | Connection closed after 20,000 entries |
| TC-TE-008-04 | AC4, BR6 | Component | Failed run, then a rerun at 08:30 |
| TC-TE-008-05 | AC5 | Component | Empty log |
| TC-TE-008-06 | AC6, BR4 | Component | JOB-13 ending at 02:25; JOB-13 not ended by 04:00 |
| TC-TE-008-07 | AC7, BR2 | Component | Two entries changed |
| TC-TE-008-08 | AC8, BR3 | Component | 37 entries appended during the run |
| TC-TE-008-09 | Access | End to end | A role without the right is refused with MSG-P4-002 |
| TC-PLT-TE008-APP-10 | AC9, BR8 | Integration | The template and the library, the three contract fakes, the Schedule at 02:00, one generated service with a broken local chain, and a business date whose ledger ingest completes late and then not at all |

The nine legacy test case rows keep their ID, Covers and Data cells word for word, and only the Level cell is mapped to the target shape: the legacy System rows TC-TE-008-01 to TC-TE-008-08 become Component, and the legacy Access row TC-TE-008-09 becomes End to end. TC-PLT-TE008-APP-10 is the new row for AC9. The full test, with its Given, When and Then, stays in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same TC ID.

### 17. Guardrails

- No business value in code: the three parameter values, the calendar and the list of chains are read through the contracts of rwb-case (DP-06, DP-07) and are owned by RW-COMPLY and the reference-data owner.
- No personal data in logs, reports, tests or prompts: the run record, the report and the incident name entry IDs, `chain_seq`, counts and hashes only, never a value of an entry.
- No read of another service's schema: an instance reads the chain of the service it runs in, and the central ledger only through `RWB-P7-E1008-CON`; a boundary test fails a cross-schema reference (DP-01).
- The check never writes to an entry table and never repairs an entry: a broken chain is reported, not corrected.
- One canonical-form implementation, shared with the decision-record library, so the writer and the check cannot drift apart (DP-03; BR2).
- The Schedule never runs twice at once: one run at a time per chain, and a second start is skipped without interrupting the active run (BR6).
- No path of the monolith is called and none is kept, and this platform story adds no REST operation, no topic and no schema of its own (DP-13).
- A chain nobody checks is a visible state: a service with no instance of the template is shown as not covered and reported, never treated as intact (X8).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-003 | Hash chain checked every day, break reported to Compliance the same day | Business Requirements Epic 1, section 3.7; Business Requirements Program, sections 5.7 and 6.6 | FEAT-DRI-01 (the store and the ledger this check verifies) | 17 Run the decision center | BR1 to BR8 | TC-TE-008-01 to TC-TE-008-09, TC-PLT-TE008-APP-10 |

| Target element | Source | What this story does with it | Test cases |
|---|---|---|---|
| DP-01 | Template and Rules §R5.5; Arch v5 slide 29 | A chain is read inside the service that writes it, and the central ledger only through its owner's contract; no cross-schema read | TC-TE-008-01, TC-PLT-TE008-APP-10 |
| DP-03 | Template and Rules §R5.5; Arch v5 slides 20 and 28 | The check uses the canonical form of the local decision-record library and reads the records the services publish on `rwb.decision-record.v1` | TC-TE-008-01, TC-TE-008-02 |
| DP-06 | Template and Rules §R5.5 | The start time, the latest start and the batch size are read through the parameters contract and are never values in code | TC-TE-008-01, TC-TE-008-06, TC-PLT-TE008-APP-10 |
| DP-07 | Template and Rules §R5.5 | The business-date calendar and the list of chains are reference rows read through the reference-data contract, with a version | TC-TE-008-06, TC-PLT-TE008-APP-10 |
| DP-10 | Template and Rules §R5.5; Arch v5 slide 44; Temporal design slide 12 | Quartz JOB-14 becomes a Temporal Schedule from the workflow kit, owned by rwb-decision, 02:00 | TC-TE-008-01, TC-TE-008-04, TC-PLT-TE008-APP-10 |
| DP-13 | Template and Rules §R5.5 | No base path of the monolith remains and this story provides no REST operation of its own | TC-PLT-TE008-APP-10 |
| DP-17 | Template and Rules §R5.5; Ownership Map (JOB-13) | The data lake is removed, the decision-log copy job is retired, and the check waits for the ledger ingest completeness instead | TC-TE-008-06, TC-PLT-TE008-APP-10 |
| DP-19 | Template and Rules §R5.5; Arch v5 slide 20 | The readiness and run surface a role reads is a gateway-bff composite route, and this story provides no route of its own | TC-TE-008-09, TC-TE-008-04 |
| Arch v5 slide 20 | Every service writes its own schema plus outbox and inbox, its own `decision_record`, its own queue and its own Schedules | The check is generated into every service and runs on that service's own chain | TC-PLT-TE008-APP-10 |
| Arch v5 slide 28 | Recorded locally at once, chained, collected centrally within 5 minutes, sealed daily in write-once storage | Each chain is checked where it is written, and the ledger gets the instance that owns JOB-14 | TC-TE-008-01, TC-PLT-TE008-APP-10 |
| Arch v5 slide 29 | One schema and one login per service; no cross-schema join or key; boundary test in every build | The check reads one chain per instance and never across a schema boundary | TC-PLT-TE008-APP-10 |
| Arch v5 slide 44 | The job map: JOB-14 hash-chain check, 02:00, owner rwb-decision, mechanism Schedule; JOB-13 ingest is continuous on Kafka | The Schedule and its owner, the overlap policy, the catch-up window, and the retirement of the copy the check used to wait for | TC-TE-008-04, TC-TE-008-06, TC-PLT-TE008-APP-10 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON | Contract | H: the decision-record library, the parameters contract, the reference-data contract, the workflow kit and the gateway-bff route contract this story builds against |
| RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P7-E1008-CON | Contract | C: the parameters and reference-data contracts consumed at run time, and the ledger chain read of rwb-decision |
| RWB-ITG-TE008-ITG | Integration | The integration copy of RWB-TE-008; it exercises this check across the chains and owns none of it |
| JOB-13 (retired, DP-17) | Legacy job | The decision log copy to the data lake, which no longer exists; the wait it carried is replaced by the ledger ingest completeness signal |

### 19. Out of scope

- The store, the hash computation and the on-demand verifier: the legacy RWB-E1-008, now rwb-decision with `RWB-P7-E1008-CON`.
- The check of each entry returned by an audit query (RWB-E2-005 in the legacy numbering).
- The decision log copy to the data lake (RWB-E1-014, JOB-13), retired under DP-17.
- The central ledger ingest and the daily write-once seal: rwb-decision (P7) owns both, and this story reads the ledger's chain and its ingest completeness through the contract only.
- The broken-chain control view of the administration screens (Epic 8, FEAT-ADM-10).
- The integration copy of this legacy key, RWB-ITG-TE008-ITG, which exercises the check end to end across the chains.
- The 19 schemas, the 19 logins and their grants: RWB-PLT-NF06-DB and the per-service database stories.
- The contents of `RWB-PLT-E1027-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`, `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON` and `RWB-P7-E1008-CON`; this story builds against them and adds no path, no topic and no table.
