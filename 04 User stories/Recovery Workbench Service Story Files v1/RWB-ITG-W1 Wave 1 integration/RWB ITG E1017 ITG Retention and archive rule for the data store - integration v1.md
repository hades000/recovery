# RWB-ITG-E1017-ITG Retention and archive rule for the data store

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1017-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P1-E1017-APP, RWB-P5-E1017-APP, RWB-P7-E1017-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-RDF-013) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-017 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof of the RWB-E1-017 retention rule across rwb-document (P5, the owner), rwb-case (P3, legal hold), rwb-decision (P7, decision log excluded) and rwb-source-data (P1, the interaction ledger)**, so that **the archive, the legal hold and the decision-log exclusion are proved on real services before wave 1 exits**.

### 2. Business rationale

The legacy story runs JOB-17 inside P1 over the interaction table and a retention_rule copy held in the recovery schema. The Ownership Map ruling ASM-0076 moves retention to P5 rwb-document (Architecture v5 slides 16, 41 and 44) and P1 drops its retention_rule copy; the interaction ledger stays with P1 rwb-source-data under the default ruling and DP-18. The decision log is never archived by this job, and its entries stay in P7 rwb-decision. The archive is a write-once Blob container with a manifest, not a data lake: the data lake and its Power BI feed are removed (DP-17, ADR-018).

The target split for the legacy key is therefore: P5 rwb-document owns the retention rule, the retention action, the run and the document archive; P1 rwb-source-data owns the interaction ledger and applies the rule to its own schema; P3 rwb-case owns the case, the case number and the legal hold; P7 rwb-decision owns the decision log, which the rule may never name. This story is the integration proof across those four owners.

No service contract is faked. The suite exercises the published wave 1 contracts of the four services, the shared Temporal namespace and a real write-once container; the only stubs are the external ones named in section 12.8. Where the sources do not name the cross-service trigger for the P1 interaction rows, the run-status surface of the P5 retention run or the fixture composition, the suite asserts through the owners' contracts and records the open point as GAP-0342 and ASM-0436.

### 3. Preconditions

- RWB-P5-E1017-APP is done: the retention rule and retention action tables, the Schedule-started retention run and the archive writer are in SIT.
- RWB-P1-E1017-APP is done: the interaction ledger is owned by rwb-source-data and holds no retention_rule copy.
- RWB-P7-E1017-APP is done: the decision log is readable through the rwb-decision contract and is excluded from every retention load.
- The published contracts of P1 rwb-source-data, P3 rwb-case, P5 rwb-document and P7 rwb-decision are deployed under /api/recovery/<short>/v1.
- The harness RWB-ITG-W1J01-ITG is available with its synthetic documents, cases and interaction rows.
- The environment is SIT, Temporal namespace rwb-recovery, with a write-once Blob container (Azurite in the lower environment).
- No production data is used, and no production connection is opened.
- The release date 30 November 2026 is tentative; a date is not a condition of this story.

### 4. Flow

1. QA integration engineer: seeds the synthetic documents, cases and interaction rows of the harness RWB-ITG-W1J01-ITG; no production data is used.
2. Harness: stores the synthetic document through DocumentIntakeWorkflow on queue rwb-document and waits for rwb.document.DocumentStored.v1.
3. Harness: loads the retention rule version through the retention load path delivered by RWB-P5-E1017-APP; the load is validated in full before it is stored (the path is not named in the source documents; see GAP-0342).
4. Harness: sets the legal hold of one synthetic case through POST /api/recovery/case/v1/cases/{caseId}/legal-hold and reads the case back through GET /api/recovery/case/v1/cases/{caseId}.
5. Harness: moves the business date with the clock control and lets the monthly retention Schedule fire; the run starts on the rwb-document task queue.
6. Harness: follows the run through Temporal visibility and reads the run record through the P5 contract; the rule version in force and the record class are recorded on the run.
7. Harness: asserts the archive manifest in the write-once container, the live document through GET /api/recovery/document/v1/documents/{documentId}, the case documents through GET /api/recovery/document/v1/cases/{caseId}/documents, the hold report through the P3 case contract and the unchanged decision log through GET /api/recovery/decision/v1/decision-log.
8. Harness: repeats the run on the same run date and asserts that the archive holds one copy of the set.
9. Harness: posts the negative cases — a load that names the decision log, a load value outside the allowed range, a rerun while the run is active and a rerun by a role without the platform administration right — and records every message and status.
10. Harness: writes the evidence report, clears the legal hold and removes the synthetic fixtures.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A retention load names the decision log | The load is refused in full; the rule version in force stays in use; the decision log entries of rwb-decision are unchanged | MSG-P1-002 | AC4 |
| X2 | The archive container refuses writes | No live record is deleted; the run ends FAILED; the alert is raised; the rerun is taken from the job monitor | MSG-GEN-006 | AC5 |
| X3 | A retention load carries a value outside the allowed range | The load is refused in full; the previous rule version stays in force | MSG-GEN-002 | AC7 |
| X4 | A rerun is posted while the retention run is active | Status 409; the active run completes unchanged | MSG-P2-006 | AC9 |
| X5 | A role without the platform administration right posts a rerun | Status 403; no run starts | MSG-P4-002 | AC10 |
| X6 | A consumed contract call exceeds the 2 s timeout or returns a server error | The step is retried under the run policy; the evidence report records the call and the response; no archive or delete is asserted on unverified data | None | AC1, AC2 |
| X7 | The P3 legal-hold call fails before the run starts | The run does not start; the harness records the failed precondition and stops the scenario | None | AC3 |
| X8 | The synthetic fixture set does not match the harness RWB-ITG-W1J01-ITG expectations | The suite fails as a fixture fault and names the mismatched element; no service defect is raised | None | AC1, AC6 |
| X9 | The clock control cannot move the business date | The suite fails as a harness fault; the run date is unchanged and no archive assertion is made | None | AC2, AC8 |
| X10 | The archive manifest assertion finds an unexpected object in the container | The suite fails and names the object; the live record is not treated as archived | None | AC2, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is its own module and reuses the harness RWB-ITG-W1J01-ITG; it needs the three APP stories and the published contracts of P1, P3, P5 and P7, not their source code |
| Negotiable | Periods, record classes, the archive location and the fixture sizes are data rows of the harness; the story fixes the assertions and the call set |
| Valuable | The retention rule, the archive, the legal hold and the decision-log exclusion are proved on real services before wave 1 exits |
| Estimable | One suite module, one fixture pack, one run-date clock, one manifest assertion and one evidence report |
| Small | Ten scenarios over four services and one Schedule; no service code and no schema change |
| Testable | Every scenario asserts a contract response, a run state, a manifest entry or a message; all data is synthetic |

### 7. Acceptance criteria

```gherkin
Feature: Retention and archive rule for the data store, end-to-end across wave 1 services

  Background:
    Given the wave 1 services rwb-source-data, rwb-document, rwb-case and rwb-decision are deployed in SIT with their published contracts
    Given the RWB-ITG-W1J01-ITG synthetic data set is loaded and no production data is used
    Given a retention rule version is in force on the business date

  Scenario: AC1 The retention run is owned by rwb-document (new, D-RCV-60)
    Given the retention rule in force names a record class held by rwb-document
    When the monthly retention Schedule fires
    Then the rwb-document retention run starts on the service's own task queue
    Then the run records the rule version in force and the record class
    Then no service reads or writes another service's schema

  Scenario: AC2 A record past its retention age is archived and removed from the live store (new, D-RCV-60)
    Given a synthetic record older than the retention age in force
    When the retention run completes
    Then the archive manifest lists the record under the run date and record class
    Then the live store no longer returns the record
    Then the run record counts the archived row under the rule version

  Scenario: AC3 A case on legal hold is not archived (new, D-RCV-60)
    Given a synthetic case under legal hold with a record older than the retention age in force
    When the retention run completes
    Then the record stays in the live store
    Then the hold report lists the case
    Then the summary alert names the number of cases kept on legal hold

  Scenario: AC4 The decision log is never archived (new, D-RCV-60)
    Given a retention load that names the decision log
    When the load is validated
    Then the load is refused in full with MSG-P1-002 and the check names the decision log
    Then the rule version in force stays in use
    Then the decision log entries of rwb-decision are unchanged

  Scenario: AC5 An archive failure leaves the live record and ends FAILED (new, D-RCV-60)
    Given the archive container refuses writes
    When the retention run ends
    Then no live record is deleted
    Then the run ends FAILED with MSG-GEN-006 for the archive container

  Scenario: AC6 A repeat run does not duplicate the archive (new, D-RCV-60)
    Given the retention run archived a set of records on the run date
    When the same run is repeated on the same date
    Then the archive holds one copy of the set
    Then the run records no second archive of the same record

  Scenario: AC7 A retention rule outside the allowed range is refused (new, D-RCV-60)
    Given a retention load with a value outside the allowed range
    When the load is validated
    Then the load is refused in full with MSG-GEN-002 naming the field and the allowed range
    Then the rule version in force stays in use

  Scenario: AC8 A record exactly at its retention age stays (new, D-RCV-60)
    Given a synthetic record exactly at the retention age in force
    When the retention run completes
    Then the record stays in the live store
    Then the run record counts it as kept

  Scenario: AC9 A rerun while the retention run is active is refused (new, D-RCV-60)
    Given the retention run is active
    When a platform administrator posts a rerun
    Then the service refuses the rerun with status 409 and MSG-P2-006
    Then the active run completes unchanged

  Scenario: AC10 A role without the job right is refused (new, D-RCV-60)
    Given a user holds a role without the platform administration right
    When the user posts a rerun of the retention run
    Then the service refuses the call with status 403 and MSG-P4-002
    Then no run starts
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Each data product and table has one retention rule in force, held as a versioned data row | RWB-E1-017 BR1 |
| BR2 | A row older than its retention period on its age-basis field is archived and removed from the live store | RWB-E1-017 BR2 |
| BR3 | A legal hold keeps every row of the case, overriding the retention rule | RWB-E1-017 BR3 |
| BR4 | A row is removed only after its archive copy is written and checked | RWB-E1-017 BR4 |
| BR5 | The decision log is not archived by this job; its retention is set by Compliance | RWB-E1-017 BR5 |
| BR6 | A retention load with an exception is refused in full | RWB-E1-017 BR6 |
| BR7 | A new version applies from its valid-from date; earlier runs keep their recorded version | RWB-E1-017 BR7 |
| BR8 | P5 rwb-document owns the retention rule and the retention action; no other service holds a copy of the rule table | ASM-0076; Architecture v5 slides 16, 41 and 44 |
| BR9 | Each owning service applies the rule to its own schema; the suite asserts through the owner's contract and never queries another service's table | DP-01; ASM-0076 |
| BR10 | The interaction ledger stays with P1 rwb-source-data, the case and the legal hold stay with P3 rwb-case and the decision log stays with P7 rwb-decision; each is read only through its own API | Ownership Map; ASM-0076 |
| BR11 | Every cross-service call in the suite is one hop with a 2 s timeout | ADR-020 |
| BR12 | No personal data in the run record, the archive manifest assertion, the evidence report or the fixtures; identifiers and counts only | RWB-E1-017 section 17; ADR-015 |

### 9. State transitions

None. This story does not change a case status. It changes the JOB-17 run status (Running, Complete, Failed) and the retention rule version in force.

| Object | State | Meaning |
|---|---|---|
| Retention run | Running | The Schedule-started run is active on the rwb-document task queue |
| Retention run | Complete | The archive is written, the manifest is checked, the live rows are removed and the run record is written |
| Retention run | Failed | The archive write or the manifest check failed; no live row is deleted and the alert is raised |
| Retention rule version | In force | The approved version whose valid-from date covers the run date |
| Retention rule version | Superseded | Replaced by a later approved version; earlier runs keep the version they recorded |
| Case legal hold | On | Every record of the case is kept and the case is listed in the hold report |
| Case legal hold | Off | Set by P3 rwb-case when the hold is cleared; the record follows the rule again |

The suite sets and clears the hold through the P3 contract; it does not change the case status.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Runs the suite, seeds the synthetic fixtures, reads the evidence report |
| Compliance and PDPA officer | Owns the retention periods; reads the summary alert and the run result |
| Data steward | Reads the run result for their products |
| Platform administrator | Posts a rerun of the retention run and reads the job monitor |
| Service owner of rwb-document | Owns the retention rule, the retention action, the run and the document archive |
| Service owner of rwb-source-data | Owns the interaction ledger and its application of the rule |
| Service owner of rwb-decision | Owns the decision log and its exclusion from the rule |
| Service owner of rwb-case | Owns the case, the case number and the legal hold |

No other role is in scope for this story.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-002 | recovery_case (P3 rwb-case) | case_no | Read |
| DF-CAS-020 | recovery_case (P3 rwb-case) | legal_hold | Read |
| DF-INT-001 | interaction (P1 rwb-source-data) | id | Read |
| DF-INT-002 | interaction (P1 rwb-source-data) | case_id | Read |
| DF-INT-003 | interaction (P1 rwb-source-data) | person_key | Read |
| DF-INT-004 | interaction (P1 rwb-source-data) | occurred_at | Read |
| DF-INT-005 | interaction (P1 rwb-source-data) | channel | Read |
| DF-INT-006 | interaction (P1 rwb-source-data) | direction | Read |
| DF-INT-007 | interaction (P1 rwb-source-data) | action_code | Read |
| DF-INT-008 | interaction (P1 rwb-source-data) | contact_result | Read |
| DF-INT-009 | interaction (P1 rwb-source-data) | promise_amount | Read |
| DF-INT-010 | interaction (P1 rwb-source-data) | promise_date | Read |
| DF-INT-011 | interaction (P1 rwb-source-data) | summary | Read |
| DF-INT-012 | interaction (P1 rwb-source-data) | conduct_check | Read |
| DF-INT-013 | interaction (P1 rwb-source-data) | source_system | Read |
| DF-REF-116 | retention_rule (P5 rwb-document) | id | Read |
| DF-REF-117 | retention_rule (P5 rwb-document) | product_code | Read |
| DF-REF-118 | retention_rule (P5 rwb-document) | table_name | Read |
| DF-REF-119 | retention_rule (P5 rwb-document) | record_class | Read |
| DF-REF-120 | retention_rule (P5 rwb-document) | retention_months | Read |
| DF-REF-121 | retention_rule (P5 rwb-document) | age_basis_field | Read |
| DF-REF-123 | retention_rule (P5 rwb-document) | rule_version | Read |
| DF-REF-124 | retention_rule (P5 rwb-document) | valid_from | Read |
| DF-REF-125 | retention_rule (P5 rwb-document) | valid_to | Read |
| DF-REF-126 | retention_rule (P5 rwb-document) | approved_by | Read |
| Cross-service trigger and fixture composition | Retention run, document, case and interaction fixtures | Trigger, run-status surface and fixture set | Not specified in the source documents (GAP-0342; ASM-0436) |

The legacy story marks DF-INT-001 as a write because archived rows are deleted from the live table; in this suite the delete is performed by the owning service and the suite only asserts the result through that owner's contract. retention_rule is now owned by P5 rwb-document (ASM-0076), and P1 holds no copy. Field IDs are those in the Logical Data Model and Data Dictionary. Every row in the suite is synthetic.

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The names reserved for P2 rwb-integration — /api/recovery/integration/v1, rwb.integration.events.v1, rwb-integration and rwb_integration — are not used, and no rwb_integration table is written.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| GET /api/recovery/document/v1/documents/{documentId} | P5 rwb-document | Read the live document and its record class before and after the run |
| GET /api/recovery/document/v1/cases/{caseId}/documents | P5 rwb-document | Read the documents of a case and their archive state |
| GET /api/recovery/case/v1/cases/{caseId} | P3 rwb-case | Read the legal hold flag and the case number |
| POST /api/recovery/case/v1/cases/{caseId}/legal-hold | P3 rwb-case | Set and clear the legal hold |
| GET /api/recovery/decision/v1/decision-log | P7 rwb-decision | Prove the decision log is unchanged |
| GET /api/recovery/source-data/v1/admin/jobs | P1 rwb-source-data | Optional run evidence for the interaction path |

Every call is one hop with a 2 s timeout (ADR-020, DP-11).

#### 12.3 Events published

None. The suite publishes no event.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| rwb.document.DocumentStored.v1 | rwb.document.events.v1 | P5 rwb-document | The synthetic document is stored; the suite waits for it before the run |

No event is produced by the suite.

#### 12.5 Workflows and activities

| Workflow or activity | Owner | Task queue | Use |
|---|---|---|---|
| DocumentIntakeWorkflow | P5 rwb-document | rwb-document | Store the synthetic document for the record class under test |
| Retention run (Schedule-started) | P5 rwb-document | rwb-document | The run under test; the source documents name no workflow for it (see GAP-0342) |

The run reads only the rwb_document schema. No workflow, activity or the suite reads another service's schema.

#### 12.6 Schedules

| Job | Name | When | Owner | Use |
|---|---|---|---|---|
| JOB-17 | Retention | Monthly, first Sunday | rwb-document | The run under test, fired by a Temporal Schedule |
| JOB-12 | Document intake | Every 15 min | rwb-document | Used only to seed the synthetic document |

#### 12.7 Tables owned

None. The suite owns no table and never reads another service's schema (DP-01).

#### 12.8 Contract fakes

External stubs only:

| Stub | Use |
|---|---|
| Azurite Blob write-once container | The archive, its manifest and the deliberate write refusal |
| ACE document fixture (harness RWB-ITG-W1J01-ITG) | The synthetic documents and cases loaded for the run |
| Clock control for the run date | Moves the business date so the Schedule fires on the run date |

No service contract is faked: every P1, P3, P5 and P7 call goes to the real service in SIT.

#### 12.9 Call-type summary

| Call type | Provided by the suite | Consumed by the suite |
|---|---|---|
| REST | 0 | 6 |
| Kafka | 0 | 1 |
| Temporal | 0 | 1 workflow (DocumentIntakeWorkflow) and 1 Schedule-started run (retention) |
| File | 0 | 1 archive container |

### 13. Solution plan

| Component | Type | Responsibility |
|---|---|---|
| Suite module for RWB-ITG-W1, reusing harness RWB-ITG-W1J01-ITG | Integration suite | Runs the ten scenarios against SIT and holds no service code |
| Fixture pack | Test data | Synthetic documents, cases and interaction rows for the record classes under test |
| Run-date clock control | Harness control | Moves the business date and restores it after the scenario |
| Archive manifest assertion | Assertion | Reads the write-once container and checks the manifest entry per run date and record class |
| Evidence report | Report | Records per scenario the run id, the run state, the contract responses, the counts and the messages |

Decoupling patterns applied (Template and Rules v1 §R5.5):

| DP | Legacy marker | Microservice pattern | Dependency added | Where it sits |
|---|---|---|---|---|
| DP-01 | recovery.<table>, "recovery schema" | Owner's schema rwb_<name>; never read another service's tables | none | The suite asserts through contracts only; each of P1, P3, P5 and P7 writes its own schema |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic rwb.decision-record.v1 | H RWB-PLT-E1027-CON | On the P1, P5 and P7 APP stories; not a build dependency of this suite |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | On the APP stories; the suite only reads the case through the P3 contract |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON | On RWB-P5-E1017-APP; the suite observes the Schedule-started run |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | The six consumed REST operations of section 12.2 |
| DP-13 | /api/recovery/v1 | /api/recovery/<short>/v1 | none | Every consumed path in section 12.2 |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | On the APP stories; the suite changes no schema |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | Not used by this suite; no screen is in scope |

The dependency-added column records the build dependency of the owning story. This story has no build dependency: an ITG story waits on no build of its own, and its I dependencies are the APP stories listed in the metadata table.

Build steps:

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the SIT endpoints of P1, P3, P5 and P7.
2. Build the fixture pack: synthetic documents, cases and interaction rows, with the record class and legal hold as data rows.
3. Add the run-date clock control and the restore step.
4. Implement the ten scenarios of section 7 in TC order and assert only through the contracts of section 12.2, the events of section 12.4 and Temporal visibility.
5. Add the archive manifest assertion for the write-once container, including the write-refusal scenario.
6. Add the negative loads, the rerun while active and the role without the right, and assert the exact messages and statuses.
7. Write the evidence report with the run id, the rule version in force, the counts, the hold report and the decision-log comparison.
8. Run the suite in SIT against the wave 1 release candidate and keep the report with the wave exit evidence.

Done when: all ten test cases pass in SIT against the published wave 1 contracts, the evidence report is attached to the wave exit pack, and no service code or schema was changed by this story.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-020 | Retention run summary to Compliance (new, see additions) | {count} rows of {product} were archived under rule {rule} version {version}. {held} cases on legal hold were kept. |
| MSG-GEN-002 | retention_months outside 1 to 600 | {field} must be between {min} and {max}. |
| MSG-P1-002 | Retention load refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-006 | Archive container unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P2-006 | Rerun while JOB-17 runs | {job} is already running. Wait for it to finish before you rerun it. |
| MSG-P4-002 | Role without the right on the job monitor | You cannot {action} here. Your role does not include it. |

The message IDs and wording are copied from RWB-E1-017. No new message ID is added by this story. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story. The run is observed through Temporal visibility and the job run record, and the suite reads the same run through the P5 contract. Compliance reads the summary alert MSG-P1-020. SCR-47 Personal data belongs to Epic 8 and is out of scope here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-017-01-ITG | AC2 | Integration | 1,250 old and 4,800 recent synthetic interaction rows; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-017-02-ITG | AC1, AC2 | Integration | Version RET-2027.01 at 36 months; rows from 2024-01-15 and 2023-12-20; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-017-03-ITG | AC3 | Integration | Case RW-2024-000311 on legal hold with 40 old rows; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-017-04-ITG | AC7 | Integration | Load row with 0 months; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-017-05-ITG | AC5 | Integration | Archive container stub refusing writes; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-017-06-ITG | AC6 | Integration | JOB-17 run twice on 2026-12-06; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-017-07-ITG | AC8 | Integration | Row at exactly 24 months; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-017-08-ITG | AC4 | Integration | Load row for decision_log_entry; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-017-09-ITG | AC9 | Integration | Rerun posted during a running JOB-17; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-017-10-ITG | AC10 | Integration | RW-COMPLY posts a rerun of JOB-17; refused with MSG-P4-002; end-to-end: real services on the wave 1 contracts; no numeric business values added |

### 17. Guardrails

- Synthetic data only; the harness RWB-ITG-W1J01-ITG loads the fixtures and no production data is read, copied or connected to.
- No personal data in the run record, the archive manifest assertion, the logs, the evidence report or the fixtures: identifiers and counts only.
- No cross-service table read: every assertion goes through the owner's contract, and the suite owns no table.
- No business value in test code: periods, record classes and the archive location are data rows or properties.
- No live row is deleted before the archive copy is checked, and the suite never deletes a live row itself.
- One hop and a 2 s timeout on every call (ADR-020).
- No production access of any kind from the suite or its configuration.

### 18. Traceability

| Requirement or decision | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-RDF-013 | Retention and archive rule by record class | P5 retention rule and archive; P1 interaction ledger; P3 legal hold; P7 decision log; MSG-P1-020 | TC-E1-017-01-ITG to TC-E1-017-10-ITG |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | rwb.document.DocumentStored.v1 on rwb.document.events.v1 | TC-E1-017-02-ITG |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The six consumed REST operations of section 12.2 | TC-E1-017-01-ITG, TC-E1-017-09-ITG, TC-E1-017-10-ITG |
| DP-01 | Owner's schema, never another service's tables | One writer per schema; the suite asserts through contracts | All |
| DP-10 | Temporal Schedule replaces Quartz | JOB-17 on the rwb-document task queue | TC-E1-017-01-ITG, TC-E1-017-09-ITG |
| ASM-0076 | Retention is P5; P1 drops retention_rule | P5 owns retention_rule and retention_action; P1 keeps the interaction ledger | TC-E1-017-04-ITG, TC-E1-017-08-ITG |

The legacy story is RWB-E1-017. The integration dependencies are RWB-P1-E1017-APP, RWB-P5-E1017-APP and RWB-P7-E1017-APP; their component-level acceptance criteria AC1 to AC9 are owned by those stories, not by this one.

### 19. Out of scope

- The P1, P5 and P7 APP builds and their unit and component tests.
- The P1 CON and OPS stories.
- The legacy AC1 to AC9 at component level, which the sibling APP stories own.
- SCR-47 Personal data (Epic 8).
- The build of the harness RWB-ITG-W1J01-ITG.
- The NFR epic, including load, resilience and performance testing.
- The data lake, which is removed (DP-17, ADR-018).
