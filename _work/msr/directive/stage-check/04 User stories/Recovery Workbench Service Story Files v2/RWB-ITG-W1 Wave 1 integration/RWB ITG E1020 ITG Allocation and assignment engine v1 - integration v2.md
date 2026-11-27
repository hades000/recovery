# RWB-ITG-E1020-ITG Allocation and assignment engine v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1020-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-020 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-E1020-ITG-16); the squad sizes the story at refinement |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | Not specified in the source documents (DOR-RWB-ITG-E1020-ITG-23); paths /api/recovery/decision/v1, /api/recovery/case/v1 and /api/recovery/source-data/v1 |
| Integration dependencies | RWB-P3-E1020-APP, RWB-P4-E1020-APP, RWB-P7-E1020-APP, RWB-S8-E1020-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-020) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-020 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E1020-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (39 resolved, 23 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof of the RWB-E1-020 allocation and assignment engine across rwb-case (the JOB-03 step of DailyCaseRun, the two package evaluations, the case commit with its outbox row and the allocation events), rwb-decision (the package registry with its checksum and the central decision ledger), rwb-access (the Platform administration right that guards a rerun) and rwb-deviation (the deviation event that sends a case to the deviation handler queue)**, so that **every new case is queued and owned by rule before 07:00, at most once per business date, with its decision record in the central ledger, and the wait on case creation is proved on the real services before wave 1 exits**.

### 2. Business rationale

RWB-E1-020 places every new recovery case in a queue and gives it an owner by the ALLOCATION and ASSIGNMENT rule packages on the morning the case arrives, so that no case at 90 days past due waits with no owner and nobody allocates by hand. The component copy of the behaviour already exists: RWB-P3-E1020-APP owns the legacy criteria AC1 to AC9 and AC11 to AC13 in rwb-case, against the published contracts of the services it needs. This integration story owns the one criterion a single service cannot prove: AC10, the run waits for case creation. The fact AC10 turns on is not produced inside the allocating step at all — the JOB-02 step of the same run must have completed for the business date, and the readiness signal that starts the run belongs to rwb-source-data — so an assertion made inside rwb-case alone would pass while the gate itself was wrong.

The rest of what this story proves is cross-service in the same way. The rule packages are governed in rwb-decision and only evaluated locally, so a suite that read a local table would never notice an unapproved or unchecksummed version reaching the run. The decision record of an allocation commits in rwb-case but is collected into the central ledger of rwb-decision within five minutes (ADR-022), and an assertion on the local record alone would pass while the ledger stayed empty. The allocation facts leave as `rwb.case.CaseAllocated.v1` and `rwb.case.CaseAllocationFailed.v1` on the owner's topic, and a case with an open deviation is diverted on the event of rwb-deviation rather than on a flag read from another service's table. None of those can be proved inside one service.

The legacy story runs JOB-03 as a Quartz job (D-RCV-36 T2), writes the decision log entry through a published interface of the case module, and reads the target queue, the cap and the rule rows from the monolith schema. The target delta is the mechanism and the delivery path, not the behaviour. DP-10 makes JOB-03 a step of DailyCaseRun in rwb-case, started by AceDataReady for the business date and complete by 07:00, with no Quartz table and no second timer (Arch v5 slide 44). DP-04 makes rwb-decision the registry: each version carries its SHA-256, the service fetches both packages, verifies the checksum and evaluates its own copy inside the EvaluateRules activity, so no shared rule server sits on the hot path. DP-03 splits the record: the local record commits in `rwb_case` with the case change in one transaction and leaves as `rwb.decision.DecisionRecorded.v1` for the ledger of rwb-decision. DP-09 and DP-14 keep the announcement on `rwb.case.events.v1` in the CloudEvents envelope, key caseId, IDs and facts only. DP-13 renames the base to `/api/recovery/<short>/v1`, DP-05 keeps the ACE views behind rwb-source-data, DP-06 and DP-07 read the parameters and the lists as data through the rwb-case contracts, DP-01 keeps `recovery_case`, `queue`, `queue_member`, `assignment` and the local record in `rwb_case`, DP-15 gives each service its own Flyway sequence, and DP-19 puts any screen behind gateway-bff.

No service contract is faked in this story: the four integration dependencies are the real services on their published contracts, and a fake would defeat the purpose of the run. What the sources do not fix is the surface the suite reads the JOB-03 run through — the catalogue read and the rerun belong to the rwb-source-data job catalogue while the run itself is a workflow step of rwb-case — and it is recorded as GAP-0345 with ASM-0439. The legacy values stay as they are: packages "ALLOC-2026.11" and "ASSIGN-2026.11", queues "MTG-BKK-CO", "MTG-BKK-OVF", "RWB-EXC" and "DEV-HANDLER", the cap of 150, the business date 2026-12-01 and the criterion of 07:00. Release 30 November 2026 is tentative and is never a condition of this story.

### 3. Preconditions

- RWB-P3-E1020-APP is done: the JOB-03 step of DailyCaseRun, the two `RuleEvaluator` calls for ALLOCATION and ASSIGNMENT, the assignment engine with its cap and round-robin cursor, the idempotency of the business date, the allocation summary and the allocation case reads are in SIT on rwb-case.
- RWB-P7-E1020-APP is done: the package versions of ALLOCATION and ASSIGNMENT with their checksums, the rule-package version list, the rollback and the central decision ledger are published by rwb-decision.
- RWB-P4-E1020-APP is done: the Platform administration right U and its refusal on the administrative operations are enforced by rwb-access.
- RWB-S8-E1020-APP is done: `rwb.deviation.DeviationRaised.v1` leaves rwb-deviation on `rwb.deviation.events.v1` for the case that is screened, and the deviation flag is observable through the owners' contracts.
- The published contracts of P3, P4, P7 and S8 are versioned in the registry, and the harness consumes only those contracts; the suite opens no service schema.
- The harness RWB-ITG-W1J01-ITG is available with its synthetic case set, its synthetic queues and members and its caps for business date 2026-12-01.
- SIT is in place: the Temporal namespace `rwb-recovery`, the task queues `rwb-case`, `rwb-decision`, `rwb-access` and `rwb-deviation`, and the topics `rwb.case.events.v1`, `rwb.decision-record.v1`, `rwb.decision.events.v1` and `rwb.deviation.events.v1` with their retry and `.dlt` topics, plus the schema registry.
- The agreed test-only fault switch on the decision-record library of rwb-case can fail the record write for one case (AC20) and for every case of a run (TC-E1-020-15-ITG), and its use is agreed with the rwb-case owner.
- No production data is read, copied or connected to; every case number, owner id, queue code, product group and region used by the run is synthetic.
- This story has no build dependency, so it is ready on Day 1 under Template and Rules §R5.7. The release date 30 November 2026 is tentative and is copied unchanged.

### 4. Flow

1. QA integration engineer: records the package evidence through `GET /api/recovery/decision/v1/approvals` and `GET /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` for ALLOCATION and ASSIGNMENT — the version in force from 2026-11-30, the approver role RW-RISK and the SHA-256 of each version — then seeds the synthetic cases, queues, members and caps of the harness RWB-ITG-W1J01-ITG for business date 2026-12-01; no production data is used.
2. Harness: waits on `rwb.decision.RulePackageInForce.v1` on `rwb.decision.events.v1` for the promotion of "ALLOC-2026.11" and "ASSIGN-2026.11" by the JOB-20 promote at 00:01, so that both packages are in force before any case is asserted.
3. Harness: publishes the readiness signal for 2026-12-01 through the P1 readiness operation and confirms that DailyCaseRun started on queue `rwb-case` for that business date, with the JOB-02 step before the JOB-03 step.
4. System: the JOB-02 step creates the new cases with status NEW, product group, region and exposure band; the JOB-03 step then selects every NEW case whose `last_allocation_date` is before the business date and allocates it through the two packages.
5. Harness: reads `GET /api/recovery/case/v1/cases` for the cases of 2026-12-01 and then `GET /api/recovery/case/v1/cases/{caseId}` for each one, asserting status "ASSIGNED", the queue, the team, the owner and the ALLOCATION package version on the case record.
6. Harness: reads `GET /api/recovery/case/v1/queues` for the queue codes, the method, the cap of 150 and the overflow queue of "MTG-BKK-CO", then `GET /api/recovery/case/v1/queues/{queueId}/cases` for "MTG-BKK-OVF", "RWB-EXC" and "DEV-HANDLER" and reconciles every count of the run with the case reads and the two summary lines MSG-P3-011 and MSG-P3-012.
7. Harness: consumes `rwb.case.CaseAllocated.v1` and `rwb.case.CaseAllocationFailed.v1` on `rwb.case.events.v1` and asserts the CloudEvents envelope, the key caseId, the case number, the queue code and the absence of any personal data field.
8. Harness: waits on `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` for every allocation, reads `GET /api/recovery/decision/v1/decision-log` and measures the elapsed collection of each record against the five-minute target, asserting exactly one record per allocation with rule ID and package version.
9. Harness: moves the clock past 07:00 on a business date whose ALS batch row in the rwb-source-data contract fake is not COMPLETE, reads the job catalogue through `GET /api/recovery/source-data/v1/admin/jobs` and asserts that the JOB-03 step has not started, that the run record carries MSG-P1-001 and that every NEW case keeps no queue and no owner (AC10).
10. Harness: runs the remaining controls — the rerun of the same business date through `POST /api/recovery/source-data/v1/admin/jobs/JOB-03/rerun`, the rerun by an identity without Platform administration U, the rollback of the ALLOCATION version and its promote back for the held date, the deviation event of S8, and the forced record failure of AC20 — records every status, message and count, proves from the call set of the run that no service schema and no Quartz table was read, then writes the evidence report, removes the synthetic fixtures and restores the clock and the packages.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The JOB-02 step has not completed for the business date | The JOB-03 step does not start for that date, no case is allocated, and the run shows the waiting line for the predecessor step | MSG-P1-001 | AC10 |
| X2 | No ALLOCATION or ASSIGNMENT version is in force on the business date | The run is refused before any case is touched, the whole business date is held, every case keeps status "NEW" and the run record names the package code | MSG-P3-027 | AC16 |
| X3 | A package version is fetched with a checksum that does not match the one held by rwb-decision | The version is refused, the run stops before the first allocation, and the evidence report names the package and the version | None | AC12 |
| X4 | A case has an open deviation, raised on `rwb.deviation.events.v1` | The case goes to the deviation handler queue "DEV-HANDLER" with no case owner and status "NEW", and no CaseAllocated event leaves for it | None | AC15 |
| X5 | Every owner of the target queue is at the cap of 150 | The case goes to the overflow queue named by the ASSIGNMENT row, keeps status "NEW", and is counted in the summary | MSG-P3-011 | AC18 |
| X6 | No ALLOCATION rule matches the case | The case goes to the exception queue "RWB-EXC", the rule gap is recorded, and `rwb.case.CaseAllocationFailed.v1` leaves with reason "NO_ROW_MATCHED" | MSG-P3-012 | AC14, AC18 |
| X7 | The decision record of one case cannot be written | That case is not allocated and stays "NEW" with no queue and no owner, the rest of the run continues, and the run record names the case | MSG-P3-013 | AC20 |
| X8 | The same business date is run again | The cases already allocated for the date are skipped, so no second assignment and no second ledger entry exists | None | AC17 |
| X9 | A second rerun reaches a case the first run still holds | The case row lock stops the second worker, and each case is allocated once; a rerun of a run still in flight is refused as a conflict | MSG-P2-006 | AC17, TC-E1-020-11-ITG |
| X10 | An identity without Platform administration U reruns the JOB-03 step | The call is refused with status 403, no run starts and no case is allocated | MSG-P4-002 | AC19, TC-E1-020-14-ITG |
| X11 | A consumed contract drifts from the published one (path, field, status or event schema) | The preflight fails on the contract test and the run stops before any assertion; the drift is reported against the owning service and no fake is put in its place | None | Preflight, AC11 |
| X12 | The W1J01 synthetic set or the agreed fault switch is missing or does not match the run | The run fails as a fixture fault and names the missing element; no production value is substituted | None | AC19, AC20 |

X1 to X10 are the exception paths of the legacy story read on the wave 1 services; X11 and X12 are the failures that only appear when the run leaves one service or loses its fixture, so that a timeout or a fixture fault never becomes a pass.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is its own module and reuses the harness RWB-ITG-W1J01-ITG; it needs the four integration dependencies and the published contracts of P3, P4, P7 and S8, not their source code, and it owns no schema and no table |
| Negotiable | The fixture composition, the poll interval, the wait window and the report layout are configuration; the gate behaviour, the message IDs, the package versions, the queue codes and the cap are fixed by the legacy story |
| Valuable | Proves across services what no single service story can prove: the wait on case creation, the governed package with its checksum, one ledger record per allocation within five minutes, the allocation events, the deviation diversion, the held date and the idempotency of a rerun |
| Estimable | One suite module, one fixture builder, four contract probes, one clock and gate control, one package rollback step and one evidence report |
| Small | Fits one sprint with the report; eleven scenarios over four services, four topics and four consumed operations of the run |
| Testable | Every criterion is asserted on an observable: a REST response, a Kafka event, a workflow result, a ledger record or a run count |

### 7. Acceptance criteria

```gherkin
Feature: Allocation and assignment engine v1, proven across the wave 1 services

  Background:
    Given package ALLOCATION version "ALLOC-2026.11" is in force from 2026-11-30
    Given package ASSIGNMENT version "ASSIGN-2026.11" is in force and gives queue "MTG-BKK-CO" the method "ROUND_ROBIN" with a caseload cap of 150
    Given the queue "MTG-BKK-CO" belongs to team "MTG-BKK" and role RW-CASEOWN
    Given the queue "MTG-BKK-CO" has the overflow queue "MTG-BKK-OVF"
    Given the business date is 2026-12-01
    Given all involved services are deployed in SIT with published contracts
    Given the RWB-ITG-W1J01-ITG synthetic set is loaded

  Scenario: AC10 The run waits for case creation (legacy RWB-E1-020 AC10)
    Given the JOB-02 step of DailyCaseRun has not completed for 2026-12-01 because the rwb-source-data contract fake holds no COMPLETED ALS batch row for that date
    When 07:00 passes
    Then the JOB-03 step of DailyCaseRun has not started for 2026-12-01
    Then the run record shows the JOB-03 step waiting on the JOB-02 step with MSG-P1-001
    Then every NEW case keeps no queue and no owner

  Scenario: AC11 JOB-03 is a step of the run and every new case is allocated before 07:00 (new, D-RCV-60)
    Given AceDataReady for ALS and 2026-12-01 starts DailyCaseRun on queue "rwb-case"
    Given 3 new cases including RW-2026-000201 are created by the JOB-02 step of the same run
    When the JOB-03 step runs after the JOB-02 step
    Then the run record of DailyCaseRun shows the JOB-03 step after the JOB-02 step and no Quartz job row exists for the JOB-03 step
    Then every new case has a queue and an owner from packages "ALLOC-2026.11" and "ASSIGN-2026.11" before 07:00 on 2026-12-01

  Scenario: AC12 Both packages come from rwb-decision with a verified checksum (new, D-RCV-60)
    Given package ALLOCATION "ALLOC-2026.11" and package ASSIGNMENT "ASSIGN-2026.11" are in force and were announced by rwb.decision.RulePackageInForce.v1
    Given each version carries its SHA-256 in rwb-decision
    When the EvaluateRules activity evaluates a new case
    Then the activity fetches both versions from rwb-decision and checks each SHA-256 before use
    Then the rule is evaluated inside the activity on the service's own copy of the package
    Then the RuleResult carries packageCode, packageVersion, ruleId and outputs for each package
    Then a version whose checksum does not match is refused and no case is allocated

  Scenario: AC13 Every allocation leaves one record in the central ledger within five minutes (new, D-RCV-60)
    Given case RW-2026-000205 matches rule "ALLOC-014" (test-data rule ID; the source rule ID is Not specified in the source documents (CG-ALL-242)) and owner U-02 is below the cap of 150
    When the JOB-03 step allocates the case
    Then exactly one record exists for the case in GET /api/recovery/decision/v1/decision-log within five minutes
    Then that record carries the ALLOCATION rule ID "ALLOC-014" and package version "ALLOC-2026.11"
    Then one rwb.decision.DecisionRecorded.v1 event carries the same rule ID and package version

  Scenario: AC14 The allocation events leave the case service in the CloudEvents envelope (new, D-RCV-60)
    Given case RW-2026-000205 is allocated to U-02 in queue "MTG-BKK-CO"
    Given case RW-2026-000204 with product group "SSME" and region "NE3" matches no allocation rule
    When the JOB-03 step completes for 2026-12-01
    Then one rwb.case.CaseAllocated.v1 leaves on rwb.case.events.v1 for RW-2026-000205 with key caseId
    Then one rwb.case.CaseAllocationFailed.v1 leaves on rwb.case.events.v1 for RW-2026-000204 with reason "NO_ROW_MATCHED"
    Then each event carries the CloudEvents 1.0 headers, the case number and the queue code and no personal data field

  Scenario: AC15 An open deviation sends the case to the deviation queue (new, D-RCV-60)
    Given rwb-deviation publishes rwb.deviation.DeviationRaised.v1 for case RW-2026-000206 on rwb.deviation.events.v1
    Given case RW-2026-000206 has deviation_open true at the JOB-03 step
    When the JOB-03 step allocates the cases of 2026-12-01
    Then the case is placed in queue "DEV-HANDLER" with no case owner and status "NEW"
    Then no rwb.case.CaseAllocated.v1 leaves for the case

  Scenario: AC16 No version in force holds the whole business date (new, D-RCV-60)
    Given no ALLOCATION version is in force on 2026-12-01
    When the JOB-03 step runs for 2026-12-01
    Then no case is allocated for the date and every case keeps status "NEW" with no queue and no owner
    Then the run record carries MSG-P3-027 for the package in force check with package code "ALLOCATION"
    Then no rwb.case.CaseAllocated.v1 and no ledger record exists for the date

  Scenario: AC17 A rerun of the same business date has no further effect (new, D-RCV-60)
    Given the JOB-03 step has allocated case RW-2026-000201 to U-03 on 2026-12-01
    When the JOB-03 step for 2026-12-01 is started again through POST /api/recovery/source-data/v1/admin/jobs/JOB-03/rerun
    Then case RW-2026-000201 keeps owner U-03 and its one assignment record
    Then exactly one ledger record exists for the case and no second rwb.decision.DecisionRecorded.v1 leaves
    Then the run record shows 1 case skipped as already allocated

  Scenario: AC18 The overflow and exception counts reconcile with the case reads (new, D-RCV-60)
    Given U-01, U-02 and U-03 each hold 150 open cases in queue "MTG-BKK-CO"
    Given case RW-2026-000203 is placed in queue "MTG-BKK-CO" and case RW-2026-000204 matches no allocation rule
    When the JOB-03 step completes for 2026-12-01
    Then the cases read in queue "MTG-BKK-OVF" through GET /api/recovery/case/v1/queues and /queues/{queueId}/cases equal the overflow count of the run
    Then the cases read in queue "RWB-EXC" equal the exception count of the run
    Then the summary for team "MTG-BKK" carries MSG-P3-011 with the overflow count and MSG-P3-012 with the exception count

  Scenario: AC19 A role without Platform administration U is refused the rerun (new, D-RCV-60)
    Given a test identity holds RW-CASEOWN and no Platform administration right U
    When the identity calls POST /api/recovery/source-data/v1/admin/jobs/JOB-03/rerun for 2026-12-01
    Then the call returns status 403 with MSG-P4-002
    Then no run starts, no case is allocated and no ledger record is written by the attempt

  Scenario: AC20 A failed record leaves that one case new and the run continues (new, D-RCV-60)
    Given the decision-record write fails for case RW-2026-000207 through the agreed test-only fault switch
    When the JOB-03 step allocates the cases of 2026-12-01
    Then case RW-2026-000207 keeps status "NEW" with no queue and no owner
    Then the other cases of the run are allocated and each has one record in GET /api/recovery/decision/v1/decision-log
    Then the run record carries MSG-P3-013 for case RW-2026-000207

  Scenario: AC21 The rules of section 8 without a criterion hold across the run (new, D-RCV-60)
    Given the JOB-03 step of DailyCaseRun runs for 2026-12-01 on the synthetic set
    When the JOB-03 step completes
    Then no case change commits without its decision record (BR7)
    Then the ALLOCATION package has a default row as its last row, checked at load and not at run time (BR10)
    Then JOB-03 is a step of DailyCaseRun with no Quartz job row and completes by 07:00 (BR11)
    Then both packages are fetched from rwb-decision with their SHA-256 and evaluated on the service's own copy (BR12)
    Then the decision record is in the central ledger within five minutes and is answered through the decision-log read (BR13)
    Then the allocation and gap events leave on rwb.case.events.v1 with IDs and facts only and no personal data (BR14)
    Then an open deviation is taken from the deviation event and diverts the case to the deviation handler queue with no owner (BR15)
    Then a run for a business date with no version in force holds that whole date with MSG-P3-027 and touches no case (BR16)
    Then every cross-service call of the run is one hop to the owning service within the 2 s client budget (BR17)
    Then the counts of the run reconcile with the queue reads and with MSG-P3-011 and MSG-P3-012 (BR18)

  Scenario: AC22 An activity retry or timeout commits no case change without its decision record (new, D-RCV-60)
    Given the EvaluateRules activity for a new case is retried or times out
    When the JOB-03 step runs for 2026-12-01
    Then no case change for that case commits without its decision record (BR7)
    Then the run record shows the retry or timeout of the EvaluateRules activity for that case
    Then the other cases of the run are allocated

  Scenario: AC23 A consumed call that fails or does not answer leaves its case new and the run continues (new, D-RCV-60)
    Given a consumed call of the run to the owning service fails or does not answer within the 2 s client budget (BR17)
    When the JOB-03 step allocates the cases of 2026-12-01
    Then the case of the failed call keeps status "NEW" with no queue and no owner
    Then no rwb.case.CaseAllocated.v1 leaves for the case of the failed call
    Then the other cases of the run are allocated and each has one record in GET /api/recovery/decision/v1/decision-log
```

**Target reading.** Against the monolith, DP-10 replaces the Quartz trigger of JOB-03 with a step of DailyCaseRun in rwb-case, started by AceDataReady for the business date and finished by 07:00, with no Quartz table and no shared scheduler; DP-04 makes rwb-decision the registry, so the suite waits for the JOB-20 promote, fetches each version with its SHA-256 and lets the service evaluate its own copy inside the EvaluateRules activity; DP-03 keeps the record local to the transaction of the case change and collects it into the central ledger of rwb-decision as `rwb.decision.DecisionRecorded.v1` within five minutes; and DP-09 keeps the announcement of an allocation on `rwb.case.events.v1`, where the case commits with its outbox row and the suite reads the event rather than a table copy. DP-01, DP-05, DP-06, DP-07, DP-11, DP-13, DP-14, DP-15 and DP-19 change the schema, view, parameter, list, call, path, topic, migration and screen surfaces of the same behaviour. What the sources leave open — the surface the suite reads the JOB-03 run through, given that the job catalogue belongs to rwb-source-data and the run to rwb-case — is recorded as GAP-0345 and ASM-0439, and no value is invented in its place.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A case is allocated by the first rule of package ALLOCATION, in row order, whose product group, region and exposure band match the case; a column value of "any" matches every value | Package ALLOCATION; D-RCV-36 T5; DL24; REQ-CWC-008 |
| BR2 | The owner is chosen by the ASSIGNMENT rule for the queue, whose outputs hold the method — ROUND_ROBIN, LOWEST_LOAD, NAMED_OWNER or SKILL — and the cap | Package ASSIGNMENT; queue.assignment_method (DF-WRK-006); LOV-ASSIGN |
| BR3 | An owner at or above the queue's caseload cap is skipped; open cases are the cases in the queue owned by the person with a status other than CLOSED | queue.capacity_cap (DF-WRK-007); DL23 |
| BR4 | A case that cannot be given an owner goes to the overflow queue named in the ASSIGNMENT row; a row with no overflow queue sends it to the exception queue with reason "NO_OVERFLOW_QUEUE" | queue.overflow_queue_id (DF-WRK-008) |
| BR5 | A case that matches no rule goes to the exception queue and the gap is logged; R-UNI-41 handles the case once a person decides | R-UNI-41; FEAT-CWC-09 |
| BR6 | A case with an open deviation goes to the deviation handler queue "DEV-HANDLER" with no case owner | R-DEV-01 |
| BR7 | A decision that cannot be recorded does not proceed: no case change commits without its decision record | Principle 5; R-UNI-39; CTL-06 |
| BR8 | A case is allocated at most once per business date, so a repeated run of the date adds no assignment and no ledger record | R-UNI-40; events.txt rule "Duplicates" |
| BR9 | Each allocation records the ALLOCATION rule ID and package version on the decision record and the ASSIGNMENT rule ID and package version on the assignment row | REQ-CWC-016; CTL-03; D-RCV-36 T5 |
| BR10 | The ALLOCATION package always has a default row as its last row; the check is at load and is not repeated at run time | REQ-CWC-008; D-RCV-36 T5 |
| BR11 | JOB-03 is the allocation step of DailyCaseRun in rwb-case, after the JOB-02 step of the same run and complete by 07:00; it is not a Quartz job and holds no schedule of its own; its state is read from the rwb-case run result, and its rerun goes through the P1 job catalogue | Arch v5 slide 44 (JOB-03 DailyCaseRun step); DP-10 |
| BR12 | Both packages are fetched from rwb-decision with their package version, their valid-from date and their SHA-256, the checksum is verified, and the evaluation runs inside the service's activity on its own copy of the model, never against a shared rule server and never against `drl_source` | DP-04; Drools design slide 15; D-RCV-36 T3, T6 |
| BR13 | The decision record commits in `rwb_case` in the same transaction as the case change and leaves as `rwb.decision.DecisionRecorded.v1`; rwb-decision collects it into the central ledger within five minutes and answers it through the decision-log read | DP-03; ADR-022; REQ-CWC-016 |
| BR14 | An allocation leaves as `rwb.case.CaseAllocated.v1` and a rule gap as `rwb.case.CaseAllocationFailed.v1` on `rwb.case.events.v1` in the CloudEvents 1.0 envelope, key caseId, with IDs and facts only and no personal data | DP-09; DP-14; ADR-015; Arch v5 slide 42 rows 02 and 03 |
| BR15 | An open deviation is taken from the deviation event of rwb-deviation, not from a read of the deviation schema, and it diverts the case to the deviation handler queue with no owner | R-DEV-01; DP-01 |
| BR16 | A version not in force holds the whole business date with MSG-P3-027 and touches no case; it is a run-level refusal, not a per-case failure, and it is never replaced by a default decision | R-UNI-41; D-RCV-36 T5 |
| BR17 | Every cross-service call of the run is one hop to the owning service with the 2 s client budget, and no service is called through another service | ADR-020; DP-11; DP-13 |
| BR18 | The counts of the run — read, assigned, overflow, exception, failed — reconcile with the queue reads through the case contract and with the two summary lines MSG-P3-011 and MSG-P3-012 | RWB-E1-020 section 4 steps 8 and 9; CTL-03 |

### 9. State transitions

The legacy case states of RWB-E1-020, observed through the case contract:

| From | Event | Condition | To |
|---|---|---|---|
| New | Allocation rule matched | ALLOCATION rule matched and the ASSIGNMENT rule gives an owner below the cap | Assigned |

Queue placement without an owner is not a status transition; the case status stays New. This applies when every owner is at the cap (queue MTG-BKK-OVF), when no ALLOCATION rule matched (queue RWB-EXC) and when deviation_open = true after DeviationRaised, R-DEV-01 (queue DEV-HANDLER).

The states the run observes across the services:

| Item | States |
|---|---|
| DailyCaseRun | Not started, started by AceDataReady, waiting at the JOB-02 step, running the JOB-03 step, completed with the run counts, held for the whole business date |
| Case | New, Assigned; the case is never written by the suite, and the queue and the owner are read back through the case contract |
| Rule package version | LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED |
| Decision record | Recorded locally in `rwb_case`, published as DecisionRecorded, collected in the ledger of rwb-decision |
| Suite run | Not started, running, passed, failed with the failing test case named |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Owns the suite module, the fixtures, the clock and gate control, the package rollback step and the evidence report |
| Service owner of rwb-case | Owns the JOB-03 step, the two package evaluations, the assignment engine, the case commit with its outbox row and the allocation events |
| Service owner of rwb-decision | Owns the package versions, the checksum, the promote at 00:01, the rollback and the central decision ledger |
| Service owner of rwb-access | Owns the Platform administration right U and its refusal on the administrative operations |
| Service owner of rwb-deviation | Owns the deviation screening and the DeviationRaised event that diverts a case |
| RW-TEAMMGR team manager | Receives MSG-P3-011 and MSG-P3-012 and reads the queues in team scope |
| RW-PLATADM platform administrator | Reruns the JOB-03 step through the job catalogue (Platform administration U) and reads the run record |
| RW-CASEOWN case owner | Reads the cases given to them and may not rerun the run |
| No role | Reads a service schema directly, or takes production data into the run |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read through the P3 contract; written by rwb-case |
| DF-CAS-002 | recovery_case | case_no | Read through the P3 contract; written by rwb-case |
| DF-CAS-003 | recovery_case | product_group | Read through the P3 contract; written by rwb-case |
| DF-CAS-005 | recovery_case | status | Read through the P3 contract; written by rwb-case |
| DF-CAS-009 | recovery_case | owner_user_id | Read through the P3 contract; written by rwb-case |
| DF-CAS-010 | recovery_case | queue_id | Read through the P3 contract; written by rwb-case |
| DF-CAS-011 | recovery_case | team_code | Read through the P3 contract; written by rwb-case |
| DF-CAS-012 | recovery_case | region_code | Read through the P3 contract; written by rwb-case |
| DF-CAS-015 | recovery_case | exposure_band | Read through the P3 contract; written by rwb-case |
| DF-CAS-018 | recovery_case | stage_clock_start | Read through the P3 contract; written by rwb-case |
| DF-CAS-019 | recovery_case | deviation_open | Read through the P3 contract and asserted from the S8 event; written by rwb-case |
| DF-CAS-021 | recovery_case | rule_version (the ALLOCATION package version label) | Read through the P3 contract; written by rwb-case |
| DF-CAS-054 | recovery_case | last_allocation_date | Read through the P3 contract; written by rwb-case |
| DF-WRK-001 | queue | id | Read through the P3 queue contract; written by rwb-case |
| DF-WRK-002 | queue | queue_code | Read through the P3 queue contract; written by rwb-case |
| DF-WRK-004 | queue | team_code | Read through the P3 queue contract; written by rwb-case |
| DF-WRK-005 | queue | role_code | Read through the P3 queue contract; written by rwb-case |
| DF-WRK-006 | queue | assignment_method | Read through the P3 queue contract; written by rwb-case |
| DF-WRK-007 | queue | capacity_cap | Read through the P3 queue contract; written by rwb-case |
| DF-WRK-008 | queue | overflow_queue_id | Read through the P3 queue contract; written by rwb-case |
| DF-WRK-037 | queue | rr_cursor_user_id | Read through the P3 contract; written by rwb-case |
| DF-WRK-047 | queue_member | user_id | Read through the P3 contract; written by rwb-case |
| DF-WRK-048 | queue_member | capacity | Read through the P3 contract; written by rwb-case |
| DF-WRK-009 to DF-WRK-016 | assignment | all fields | Read through the P3 contract; written by rwb-case |
| DF-REF-002 | rule_row | rule_id | Read through the P7 package contract |
| DF-REF-003 | rule_row | rule_version (the package version label) | Read through the P7 package contract |
| DF-REF-007 | rule_row | condition_expr | Not read by the suite |
| DF-REF-012 | rule_row | valid_from | Read through the P7 package contract |
| DF-REF-013 | rule_row | valid_to | Read through the P7 package contract |
| DF-REF-052 | rule_row | rule_table | Read through the P7 package contract |
| DF-REF-053 | rule_row | row_order | Read through the P7 package contract |
| DF-REF-054 | rule_row | target_queue_code | Read through the P7 package contract |
| DF-REF-296 to DF-REF-298 | rule_row | package_version_id, drools_rule_name, outputs | Read through the P7 package contract |
| DF-ACE-178 to DF-ACE-186 | v_ace_batch_status | source_system, business_date, status, is_complete | Synthetic rows only, seeded through the P1 data set; read through the P1 contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Written locally by rwb-case and in the ledger by rwb-decision; read through the P7 contract |

Field IDs are those of RWB-E1-020 and are copied unchanged, with the ACE rows of DF-ACE-178 to DF-ACE-186 taken from RWB-E1-018 and used only for the batch gate. The suite owns no field and no table: every row is seeded synthetically by the harness RWB-ITG-W1J01-ITG or read through an owner's contract of section 12.2 or an event of section 12.4. The exact fixture composition — the number of synthetic NEW cases, the load of each named owner beyond the three owners the criteria name, and the case that carries the forced record failure — is Not specified in the source documents (GAP-0345; ASM-0439).

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The names reserved for P2 rwb-integration — `/api/recovery/integration/v1`, `rwb.integration.events.v1`, `rwb-integration` and `rwb_integration` — are recorded but unused, and no `rwb_integration` table is written.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| GET /api/recovery/case/v1/cases | P3 rwb-case | The cases of business date 2026-12-01 with status "NEW" before the run and their queue and owner after it |
| GET /api/recovery/case/v1/cases/{caseId} | P3 rwb-case | One case: status, queue, team, owner, the ALLOCATION package version and `last_allocation_date` |
| GET /api/recovery/case/v1/queues | P3 rwb-case | The queue codes, team, method, cap of 150 and overflow queue, and the queue id of "MTG-BKK-OVF", "RWB-EXC" and "DEV-HANDLER" |
| GET /api/recovery/case/v1/queues/{queueId}/cases | P3 rwb-case | The cases of a queue, for the overflow, exception and deviation counts of AC18 and the no-owner assertion of AC15 |
| GET /api/recovery/source-data/v1/admin/jobs | P1 rwb-source-data, job catalogue | The job catalogue and the state of the JOB-02 and JOB-03 steps on the monitor, including the waiting line of MSG-P1-001 |
| POST /api/recovery/source-data/v1/admin/jobs/JOB-03/rerun | P1 rwb-source-data, job catalogue | The rerun of the same business date for AC17, and the refused attempt of AC19 |
| GET /api/recovery/decision/v1/decision-log | P7 rwb-decision | Exactly one record per allocation, with the ALLOCATION rule ID and package version, and the elapsed collection against five minutes |
| GET /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions | P7 rwb-decision | The version in force of ALLOCATION and ASSIGNMENT, its valid-from date and its SHA-256, for AC12 and AC16 |
| GET /api/recovery/decision/v1/approvals | P7 rwb-decision | The approval evidence of each version: the approver role RW-RISK, who is not the author |
| POST /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/rollback | P7 rwb-decision | AC16: the one-call rollback that removes the ALLOCATION version from force for the held date, and the promote back |

Every call is one hop to the owning service on its own base with the 2 s client budget (ADR-020, DP-11, DP-13); the suite calls no service through another service and writes nothing through these paths except the rerun and the rollback. The job catalogue read and the rerun are x-module P1 in the API specification, while the JOB-03 run itself is registered by rwb-case as a step of DailyCaseRun, so the suite reads the run through the catalogue and asserts the step through the workflow; the surface that shows the JOB-03 step of a workflow run and the exact rerun façade at the nominal time are Not specified in the source documents (GAP-0345; ASM-0439).

#### 12.3 Events published

None. The suite publishes no business event; it observes the events of the owning services, listed in 12.4.

#### 12.4 Events consumed

| Event | Topic | Owner | What the suite asserts |
|---|---|---|---|
| `rwb.case.CaseAllocated.v1` | `rwb.case.events.v1` | P3 rwb-case | Exactly one event per allocation, key caseId, case number, queue code and the ALLOCATION rule ID with its package version; CloudEvents 1.0 and no personal data field |
| `rwb.case.CaseAllocationFailed.v1` | `rwb.case.events.v1` | P3 rwb-case | One event for a case that matched no rule, with reason "NO_ROW_MATCHED"; the assertion of AC14 on the platform |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision, with the record written by each producing service | The record of each allocation reaches the central ledger; rule ID "ALLOC-014" and package version "ALLOC-2026.11", collected within five minutes |
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | P7 rwb-decision | The JOB-20 promote at 00:01 puts "ALLOC-2026.11" and "ASSIGN-2026.11" in force before the run, and the promote back after the rollback of AC16 |
| `rwb.deviation.DeviationRaised.v1` | `rwb.deviation.events.v1` | S8 rwb-deviation | The open deviation of case RW-2026-000206 that diverts it to "DEV-HANDLER" with no owner in AC15 |

The envelope is CloudEvents 1.0 and a consumer dedupes on the event ID through its inbox (ADR-015, DP-09). The payload of each event is the owner's published schema; the event and ledger assertions replace the in-process `caseAllocated` call and the local decision log of the legacy criterion.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| CaseWorkflow | Workflow, one per case | `rwb-case` | Holds the case from entry to closure; the suite asserts the state the allocation put it in through the case read and takes no part in the order of its steps |
| DailyCaseRun | Workflow, started by AceDataReady (primary) and by one catch-up Schedule per business date with overlap policy SKIP | `rwb-case` | Runs the JOB-02 step and then the JOB-03 step for the business date, complete by 07:00 Asia/Bangkok (the deadline the alert measures); its output is the run result that AC11 and AC13 are read against |
| EvaluateRules | Activity | `rwb-case` | Input package code, facts and business date; fetches the version from rwb-decision, verifies the checksum and returns package code, package version, rule ID and outputs (DP-04) |
| RecordAndApply | Activity | `rwb-case` | Writes the decision record, the case change, the assignment and the outbox rows in one transaction and fails as one unit (DP-03, DP-09) |

All four are registered by RWB-P3-E1020-APP on task queue `rwb-case` in namespace `rwb-recovery` (Arch v5 slides 13 and 14; Drools design slide 13). The suite starts no workflow of its own: it observes DailyCaseRun and CaseWorkflow through the case contract, the run result and the topics, and it triggers the step only through the readiness signal and the rerun of the job catalogue.

#### 12.6 Schedules

| Schedule or start | Cadence | Registration | Legacy reference |
|---|---|---|---|
| JOB-02 case creation | Event-started: AceDataReady for the business date starts DailyCaseRun | Registered by the rwb-case release | JOB-02 Case creation |
| JOB-03 Morning allocation | A step of DailyCaseRun, after the JOB-02 step and by 07:00; not a Schedule of its own | Runs in rwb-case, not a Schedule | JOB-03 Morning allocation (Arch v5 slide 44) |
| JOB-20 rule promote | Temporal Schedule at 00:01, overlap policy SKIP, catch-up window; publishes RulePackageInForce | Registered by the rwb-decision release | JOB-20 Rule promote |

The suite starts no Schedule, moves no Schedule and waits for no Schedule of its own. It moves its own test clock past 07:00 for AC10, triggers the JOB-03 step through the readiness signal and the rerun of section 12.2, and takes the JOB-20 promote as an observed event.

#### 12.7 Tables owned

None. The suite owns no table and never reads another service's schema (DP-01). The tables it exercises — `recovery_case`, `queue`, `queue_member`, `assignment` and the local decision record in `rwb_case`, the package versions and the ledger in `rwb_decision` — are listed in section 11 with their owners and are read only through the contracts of 12.2 and the events of 12.4.

#### 12.8 Contract fakes

Contract fake: rwb-source-data (job catalogue and ALS batch rows), named in the table below; fake library version: Not specified in the source documents (DOR-RWB-ITG-E1020-ITG-22). No published contract of P3, P4, P7 or S8 is faked: a run that needs such a fake fails the preflight. The other stubs in the table are external to the nineteen services:

| Stub | Purpose |
|---|---|
| Synthetic case, queue, member and cap fixture (RWB-ITG-W1J01-ITG) | Stands in for the ACE ingestion and the case set that the bank's Airflow and the case service produce, outside the nineteen services |
| Synthetic ALS batch rows | Stand in for the batch record of the source system, so that the gate of AC10 can be held and released without a production row |
| Mock Entra sign-in | Gives the run its synthetic test identities, including the identity of RW-CASEOWN for AC19, as the platform demo sign-in does |
| Agreed test-only fault switch on the decision-record library of rwb-case | Stands in for a store that fails one record write (AC20) and every record write (TC-E1-020-15-ITG); its exact scope and reset are Not specified in the source documents (GAP-0345; ASM-0439) |
| rwb-source-data contract fake | Stands in for the job catalogue read, the job rerun and the ALS batch rows of rwb-source-data (AC10, AC17, AC19); library version Not specified in the source documents (DOR-RWB-ITG-E1020-ITG-22) |

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 10 | Three case reads, the queue read and the queue-case read, the job catalogue read and the rerun, the decision-log read, the version list, the approvals read and the rollback; one hop, 2 s (DP-11, DP-13) |
| Kafka | None | 5 event types | `rwb.case.CaseAllocated.v1`, `rwb.case.CaseAllocationFailed.v1` on `rwb.case.events.v1`; `rwb.decision.DecisionRecorded.v1`; `rwb.decision.RulePackageInForce.v1`; `rwb.deviation.DeviationRaised.v1`; CloudEvents 1.0, key caseId |
| Temporal | None | 2 workflows and 2 activities observed | DailyCaseRun and CaseWorkflow, with the EvaluateRules and RecordAndApply activities, all on `rwb-case`; the JOB-02, JOB-03 and JOB-20 starts of 12.6 are observed, never started by the suite |
| File | None | None | No file in this story |

### 13. Solution plan

**Deliverables.** One suite module that reuses the harness RWB-ITG-W1J01-ITG: a fixture builder for the synthetic case set, the queues, the members and the caps, a clock and gate control for the JOB-02 wait, a set of contract probes across P3, P4, P7 and S8, a package rollback and promote-back step, and an evidence report with one verdict per test case. No service code and no schema change: the suite builds nothing that a service owns.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| SuiteRunner | Test harness | Preflight against the published contracts, run order, report and exit code |
| CaseFixtureDriver | Test harness | Seeds the synthetic NEW cases of 2026-12-01, the queues "MTG-BKK-CO", "MTG-BKK-OVF", "RWB-EXC" and "DEV-HANDLER" and the members U-01, U-02 and U-03 with their loads, through the W1J01 set |
| GateControl | Test harness | Holds and releases the JOB-02 step for the business date and moves the clock past 07:00, so the wait of AC10 is proved rather than assumed |
| CaseProbe | Test harness | Calls the four case operations and asserts status, queue, team, owner, package version and the counts of overflow, exception and deviation |
| PackageProbe | Test harness | Reads the version list and the approvals, waits for RulePackageInForce, and asserts the checksum of AC12 and the held date of AC16 |
| LedgerProbe | Test harness | Consumes DecisionRecorded, reads the decision log and measures each collection against five minutes |
| EventProbe | Test harness | Consumes CaseAllocated, CaseAllocationFailed and DeviationRaised, and asserts the envelope, the key, the count per case and the absence of a personal data field |
| RerunStep | Test harness | Calls the job-catalogue rerun for AC17 and the refused rerun of AC19, then asserts the counts and the ledger entry count |
| RecordFaultStep | Test harness | Drives the agreed test-only fault switch for one case (AC20) and for every case (TC-E1-020-15-ITG) |
| ReportWriter | Test harness | One row per test case, with the evidence and the elapsed time, and the cleanup record |

**Database.** None of its own. The suite writes no service table and no schema object, and it holds no client for a service schema.

**Configuration and reference data**

- The SIT endpoints of P3, P4, P7 and S8, the topic names, the task queues, the namespace `rwb-recovery` and the schema-registry address, all as configuration.
- The synthetic case numbers RW-2026-000201 to RW-2026-000209, the owners U-01, U-02 and U-03 with the loads of 120, 95, 140, 149 and 150, the queues "MTG-BKK-CO", "MTG-BKK-OVF", "RWB-EXC" and "DEV-HANDLER", the cap of 150 and the business date 2026-12-01.
- The package codes ALLOCATION and ASSIGNMENT with the versions "ALLOC-2026.11" and "ASSIGN-2026.11", read through the P7 contracts and never written in the suite code.
- The rule ID "ALLOC-014" and the assignment rule ID "ASSIGN-007", taken from the package answer and never computed by the suite.
- The parameters and lists through the P3 contracts (DP-06, DP-07): `allocation.exception.queue.code`, `allocation.deviation.queue.code`, LOV-ASSIGN and LOV-CASE-STATUS.
- The 2 s client budget, the poll interval, the 07:00 cut-off and the five-minute collection target.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C: Not specified in the source documents (CG-ALL-240) |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H and C entries of the table belong to the owning APP stories — RWB-P3-E1020-APP for the step, the evaluations and the local record, RWB-P7-E1020-APP for the registry and the ledger — and this ITG story carries no H, no C and no X of its own. Its I list is the four services whose behaviour the run exercises, and an integration story never becomes a build dependency of another story (Template and Rules §R5.4, §R5.7).

**Build steps**

1. Create the suite module next to harness RWB-ITG-W1J01-ITG, wire it to the SIT endpoints of P3, P4, P7 and S8, the four topics and the task queues, and write the preflight: the four services answer, the topics and their retry and `.dlt` topics exist, the queues are registered in `rwb-recovery` and both packages are in force.
2. Build CaseFixtureDriver and the W1J01 fixtures for the NEW cases, the queues, the members and the caps; hold the ALS batch row and prove that no case is created and no case is allocated before the readiness signal.
3. Build GateControl and AC10: the held JOB-02 step, the clock past 07:00, the catalogue read with MSG-P1-001, and every NEW case with no queue and no owner; then release the step and assert that the same cases are allocated.
4. Build the CaseProbe assertions of AC11 and AC18: the JOB-03 step after the JOB-02 step in the history of DailyCaseRun, no Quartz row for JOB-03, and the overflow and exception counts reconciled with the queue reads and MSG-P3-011 and MSG-P3-012.
5. Build PackageProbe for AC12 and AC16: the version list with its SHA-256 and valid-from date, the approvals read, the RulePackageInForce wait, the refusal of a mismatched checksum, and the rollback of the ALLOCATION version with the promote back.
6. Build LedgerProbe and AC13: exactly one ledger record per allocation with "ALLOC-014" and "ALLOC-2026.11", and the elapsed collection measured against five minutes.
7. Build EventProbe for AC14 and AC15: the CloudEvents envelope, the key, one CaseAllocated per allocation, one CaseAllocationFailed with "NO_ROW_MATCHED", and the DeviationRaised event that diverts RW-2026-000206 to "DEV-HANDLER" with no owner.
8. Build RerunStep and RecordFaultStep for AC17, AC19 and AC20, with the refused rerun of RW-CASEOWN, the single assignment and single ledger record of a repeated date, and the one case left NEW by a failed record write while the rest of the run continues.
9. Build ReportWriter, the cleanup of the synthetic set and the evidence report; run the whole suite twice to prove that a repeated run adds no assignment and no ledger entry.

**Done when.** The fifteen test cases of section 16 pass on the real services in SIT, AC10 and the ten new criteria are signed off against the contracts, exactly one `rwb.case.CaseAllocated.v1` and one ledger record exist per allocation inside five minutes, the held date carries MSG-P3-027 and no case, the repeated date adds no assignment and no ledger entry, no service schema and no Quartz table was read, the synthetic set is restored and the packages are back in force, and the evidence report names every criterion with its observable.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-011 | Allocation summary, case in overflow | {count} new cases are waiting in the overflow queue for {team}. Every owner is at the caseload cap. |
| MSG-P3-012 | Allocation summary, no row matched | {count} new cases matched no allocation row and are in the exception queue. |
| MSG-P3-013 | Decision record write failed for a case | The case was not allocated because the decision could not be recorded. It will be tried again in the next run. |
| MSG-P3-027 | No ALLOCATION or ASSIGNMENT version is in force at the run | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-P1-001 | The JOB-03 step waits because the ALS batch has not completed | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | A role without the right reruns the run | You cannot {action} here. Your role does not include it. |
| MSG-P2-006 | A rerun is asked while the first run still holds the date | {job} is already running. Wait for it to finish before you run it again. |

The texts of MSG-P3-011, MSG-P3-013, MSG-P1-001 and MSG-P4-002 are copied unchanged from RWB-E1-020; the MSG-P3-012, MSG-P3-027 and MSG-P2-006 texts are copied from Error and Message Standard v4; this story creates no new message ID. For MSG-P3-027 the {check} value is "package in force" and the {table} names the package code only. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen is built or tested by this story. SCR-02 Case list (states Empty; Loading; list; filtered; Error and No access: Not specified in the source documents (CG-ALL-251)) shows the queue, the owner and the status of each case after the run, and the suite reads the same facts through `GET /api/recovery/case/v1/cases/{caseId}` behind the gateway-bff composite route (DP-19). SCR-09 Exception queue (states list; Loading; Empty, Error and No access: Not specified in the source documents (CG-ALL-253)) shows the cases placed in "RWB-EXC" and the suite asserts the same cases and the count of MSG-P3-012 through the queue read. The team manager receives the allocation summary after each run, which the suite asserts on MSG-P3-011 and MSG-P3-012. Queue screens come in Epic 2 (SCR-07; states Loading; Empty, Error and No access: Not specified in the source documents (CG-ALL-252)) and are out of scope.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-020-14-ITG | Access | Integration | RW-CASEOWN reruns JOB-03 and is refused with MSG-P4-002; end-to-end: real services on the wave 1 contracts |
| TC-E1-020-01-ITG | AC1, BR1; run by RWB-P3-E1020-APP | Integration | One case per product group and region in the synthetic set; package ALLOCATION "ALLOC-2026.11"; end-to-end: real services on the wave 1 contracts |
| TC-E1-020-15-ITG | Principle 5 | NFR | Decision record write forced to fail for every case in the run; end-to-end: real services on the wave 1 contracts |
| TC-E1-020-08-ITG | AC8, BR8; run by RWB-P3-E1020-APP | Integration | The same run repeated for 2026-12-01; end-to-end: real services on the wave 1 contracts |
| TC-E1-020-02-ITG | AC2, BR2; run by RWB-P3-E1020-APP | Integration | Three owners with 120, 95 and 140 open cases, round robin; end-to-end: real services on the wave 1 contracts |
| TC-E1-020-03-ITG | AC3, BR3; run by RWB-P3-E1020-APP | Integration | Next owner at 150 open cases; end-to-end: real services on the wave 1 contracts |
| TC-E1-020-04-ITG | AC4, BR4; run by RWB-P3-E1020-APP | Integration | Every owner at 150 open cases; end-to-end: real services on the wave 1 contracts |
| TC-E1-020-05-ITG | AC5, BR5; run by RWB-P3-E1020-APP | Integration | Product group SSME and region NE3 with no rule; end-to-end: real services on the wave 1 contracts |
| TC-E1-020-06-ITG | AC6, BR9; run by RWB-P3-E1020-APP | Integration | Allocation run over the synthetic set; one decision record checked per case; decision record write forced to fail for one case; end-to-end: real services on the wave 1 contracts |
| TC-E1-020-07-ITG | AC7, BR6; run by RWB-P3-E1020-APP | Integration | Case with deviation_open = true; end-to-end: real services on the wave 1 contracts |
| TC-E1-020-09-ITG | AC9; run by RWB-P3-E1020-APP | Integration | No NEW cases; end-to-end: real services on the wave 1 contracts |
| TC-E1-020-10-ITG | AC10 | Integration | The JOB-02 step of DailyCaseRun not complete for the business date; end-to-end: real services on the wave 1 contracts |
| TC-E1-020-11-ITG | AC11, BR8 | Integration | Two workers on the same case; end-to-end: real services on the wave 1 contracts |
| TC-E1-020-12-ITG | AC12, BR3 | Integration | Next owner at 149 open cases; end-to-end: real services on the wave 1 contracts |
| TC-E1-020-13-ITG | AC13, BR4 | Integration | Queue HP-CEN-CO with no overflow queue and every owner at 150; end-to-end: real services on the wave 1 contracts |
| TC-E1-020-16-ITG | AC14 | Integration | Case RW-2026-000205 allocated to U-02 and case RW-2026-000204 matches no rule; end-to-end: real services on the wave 1 contracts |
| TC-E1-020-17-ITG | AC15 | Integration | Deviation raised for case RW-2026-000206 with deviation_open true; end-to-end: real services on the wave 1 contracts |
| TC-E1-020-18-ITG | AC16 | Integration | No ALLOCATION version in force on 2026-12-01; end-to-end: real services on the wave 1 contracts |
| TC-E1-020-19-ITG | AC17 | Integration | Case RW-2026-000201 allocated to U-03, then the JOB-03 step of DailyCaseRun for 2026-12-01 started again; end-to-end: real services on the wave 1 contracts |
| TC-E1-020-20-ITG | AC18 | Integration | U-01, U-02 and U-03 at 150 open cases; case RW-2026-000203 in MTG-BKK-CO and case RW-2026-000204 matches no rule; end-to-end: real services on the wave 1 contracts |
| TC-E1-020-21-ITG | AC19 | Integration | Identity holding RW-CASEOWN without Platform administration U calls the rerun; end-to-end: real services on the wave 1 contracts |
| TC-E1-020-22-ITG | AC20 | Integration | Decision-record write fails for case RW-2026-000207 through the test-only fault switch; end-to-end: real services on the wave 1 contracts |
| TC-E1-020-23-ITG | AC21; BR7, BR10 to BR18 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E1020-ITG-AC21); end-to-end: real services on the wave 1 contracts |
| TC-E1-020-24-ITG | AC22 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E1020-ITG-AC22); end-to-end: real services on the wave 1 contracts |
| TC-E1-020-25-ITG | AC23 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E1020-ITG-AC23); end-to-end: real services on the wave 1 contracts |
| TC-E1-020-26-ITG | Contract of section 12 | Contract | Operations, events and activities of section 12 checked against the published contracts and schemas of P3, P4, P7 and S8 |

TC-E1-020-10-ITG is the copy this story signs off, for AC10. TC-E1-020-16-ITG to TC-E1-020-22-ITG cover AC14 to AC20, which this story adds. TC-E1-020-23-ITG to TC-E1-020-25-ITG cover AC21 to AC23. TC-E1-020-26-ITG is the contract test of section 12. The other fourteen legacy copies are regression evidence for the component copy RWB-P3-E1020-APP, which owns their criteria, and they are run here on the real services so that a change in one service cannot pass unnoticed; the Covers column names the legacy criterion each copy exercises, not the scenario number of section 7. The Level column follows Template and Rules §R7.2: the legacy System level becomes Integration, the legacy Access level becomes Integration, and the legacy Resilience level of TC-E1-020-15 becomes NFR. The full test of each legacy copy, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the legacy test case id.

### 17. Guardrails

- Synthetic data only: the harness RWB-ITG-W1J01-ITG loads every case number, owner id, queue, member, cap and batch row, and no production data is read, copied or connected to; the suite refuses to start against an environment that is not SIT.
- No personal data in events, logs, workflow history, fixtures or the report: case numbers, queue codes, owner ids, rule IDs, package versions and business dates only.
- No cross-service table read: every fact is read through a contract of 12.2 or an event of 12.4, the ACE views stay behind rwb-source-data (DP-01, DP-05), and the suite ships with no client for a service schema and none for the Quartz tables.
- No business value in the test code: the cap of 150, the queue codes, the method, the rule IDs, the product groups and the regions are the packages, the queues and the parameters in force, read through the P3 and P7 contracts (DP-04, DP-06, DP-07).
- One evaluator and one copy: ALLOCATION and ASSIGNMENT are evaluated only inside the EvaluateRules activity of the owning service on a checksum-verified copy of the package, and the suite never reads `drl_source`, a workbook or a rule row directly.
- No package state is left changed: a version rolled back for AC16 is promoted back in the same run, and the evidence report records the state before and after.
- CloudEvents 1.0 with IDs and facts only on every asserted event, one allocation event per case, and the consumer inbox as the only dedupe.
- One hop and a 2 s budget on every REST call, and a timeout is never retried into a pass (ADR-020, DP-11).
- Clean-up in the same run: the synthetic cases, the business dates, the held batch row, the fault switch and the started workflows are removed or restored, and the report records what was cleaned.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-CWC-007 | Every new case placed in a queue and assigned by rule | DailyCaseRun with the JOB-02 and JOB-03 steps, `GET /api/recovery/case/v1/cases/{caseId}`, `rwb.case.CaseAllocated.v1`, MSG-P1-001 | TC-E1-020-01-ITG, TC-E1-020-09-ITG, TC-E1-020-10-ITG |
| REQ-CWC-008 | Allocation rules apply first match and always have a default | `GET /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions`, the EvaluateRules activity, MSG-P3-027 | TC-E1-020-01-ITG, TC-E1-020-05-ITG, TC-E1-020-07-ITG |
| REQ-CWC-009 | Round robin, lowest load, named owner, cap and overflow | `GET /api/recovery/case/v1/queues`, `/queues/{queueId}/cases`, MSG-P3-011, MSG-P3-012 | TC-E1-020-02-ITG, TC-E1-020-03-ITG, TC-E1-020-04-ITG, TC-E1-020-12-ITG, TC-E1-020-13-ITG |
| REQ-CWC-016 | Every allocation logged with rule ID and version | `rwb.decision.DecisionRecorded.v1`, `GET /api/recovery/decision/v1/decision-log`, MSG-P3-013 | TC-E1-020-06-ITG, TC-E1-020-08-ITG, TC-E1-020-11-ITG, TC-E1-020-15-ITG |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | `rwb.case.CaseAllocated.v1` and `rwb.case.CaseAllocationFailed.v1` on `rwb.case.events.v1`, the inbox dedupe, schema-registry versioning | TC-E1-020-06-ITG, TC-E1-020-08-ITG |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | The JOB-03 step of DailyCaseRun, the JOB-02 event start and the JOB-20 Schedule | TC-E1-020-10-ITG, TC-E1-020-11-ITG |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The ten REST operations of 12.2 and the preflight contract test | TC-E1-020-14-ITG, TC-E1-020-10-ITG, TC-E1-020-26-ITG |
| ADR-022 | Local decision record plus central ledger | `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`, the decision-log read, the five-minute target | TC-E1-020-06-ITG, TC-E1-020-15-ITG |
| DP-03 | Decision record library and the shared topic | RecordAndApply writing the record, the case change and the outbox row in one transaction | TC-E1-020-06-ITG, TC-E1-020-15-ITG |
| DP-04 | Embedded Drools kit and rule packages from rwb-decision | The two versions, the checksum, the approvals read, the version list and the rollback | TC-E1-020-01-ITG, TC-E1-020-05-ITG |
| DP-09 | Outbox and inbox with CloudEvents | The two case events and the DecisionRecorded event of 12.4 | TC-E1-020-06-ITG, TC-E1-020-08-ITG |
| DP-10 | Quartz replaced by a Temporal step or Schedule | The JOB-03 step and the JOB-02 and JOB-20 starts of 12.6 | TC-E1-020-10-ITG, TC-E1-020-11-ITG |
| DP-14 | Topic naming of the owner | `rwb.case.events.v1`, `rwb.decision-record.v1`, `rwb.decision.events.v1`, `rwb.deviation.events.v1` | TC-E1-020-06-ITG, TC-E1-020-07-ITG |
| RWB-E1-020 (legacy story) | Allocation and assignment engine v1: AC10 owned here | The ten REST operations, the five events, the two workflows and the two activities of section 12 | TC-E1-020-10-ITG, signed off; AC11 to AC20 of section 7 |
| RWB-P3-E1020-APP (component copy) | The allocation and assignment behaviour in rwb-case, owning legacy AC1 to AC9 and AC11 to AC13 | The JOB-03 step, the evaluations, the assignment engine, the case commit and the allocation events | The fourteen regression copies of section 16 |

### 19. Out of scope

- The four application builds this run depends on: RWB-P3-E1020-APP, RWB-P4-E1020-APP, RWB-P7-E1020-APP and RWB-S8-E1020-APP, with their unit and component tests.
- The contract, database, operations and infrastructure stories of the legacy key RWB-E1-020 and of the four services.
- The criteria this story does not own: legacy AC1 to AC9 and AC11 to AC13, which belong to RWB-P3-E1020-APP, and every criterion of RWB-E1-021.
- Manual transfer and reassignment (RWB-E2-011, RWB-E2-012), daily rebalancing (RWB-E1-030) and the values of the caps and service levels (DL22, DL23).
- Loading, validating, approving and rolling back the ALLOCATION and ASSIGNMENT packages as a process; only the one call the held date needs is exercised here, and the process itself is RWB-E1-073.
- The build of the harness RWB-ITG-W1J01-ITG itself, which is a precondition here and not a deliverable.
- The non-functional epic RWB-ITG-NFR and load or performance testing of the allocation run; the 3,110 synthetic cases of the legacy target are not run here.
- The data lake: it is removed from the target architecture (DP-17) and no copy of a case or a decision goes to it.
