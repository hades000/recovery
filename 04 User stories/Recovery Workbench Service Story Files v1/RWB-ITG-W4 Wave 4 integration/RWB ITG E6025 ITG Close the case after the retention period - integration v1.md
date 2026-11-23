# RWB-ITG-E6025-ITG Close the case after the retention period

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E6025-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-025 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-S7-E6025-APP, RWB-P3-E6025-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E6-025 for the wave 4 integration proof that the placement is closed and the retention timer started, that the retention expiry closes the case, stops every timer, applies the retention class to every document and writes the closing entry. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Credit Administration officer**, I want **a wave 4 integration harness that drives the placement term expiry and the retention expiry on synthetic SIT data and proves that the placement is closed, the retention timer started, the case closed, every timer stopped, the retention class applied to every document and the closing entry written with cash recovered and loss**, so that **a closed write-off case carries its documents, its cash recovered and its loss, and no case is closed while a placement, a sale or an exception is still open**.

This story builds the harness and the evidence, and nothing else. The close itself is S7's, in `WriteOffWorkflow` on `rwb-writeoff` under R-WO-36 and R-WO-47; the case state, the closed_date, the closure_reason and the timers are P3's in `rwb-case`; the retention class of every document is P5's in `rwb-document`; the closing entry and its rule version are P7's in `rwb-decision`. The story builds no production endpoint, no table, no workflow, no schedule and no screen; it reads the owners' published contracts, asserts what they answer, and writes one report per case. It owns none of the four legacy acceptance criteria: all four sit with RWB-S7-E6025-APP and RWB-P3-E6025-APP.

### 2. Business rationale

A write-off case that is placed with an agency and then left standing once its term has run keeps an open placement, a placement timer and an assignment that nobody can act on, and the case never reaches the end of its life. When the retention timer does expire, the case must close into a record that can be audited years later: the date it closed, the reason, the cash recovered after charge-off, the loss, the retention class of every document, and one closing entry in the decision ledger that names the rule and its version. If the close is taken while one placement, one sale or one exception is open, or while one document carries no retention class, an obligation is cut short and the evidence for it is gone; if the close is taken without a decision record, the ledger loses the entry that the regulator and internal audit read.

The retention period itself is not set: NFR-031 leaves it **Not set** under DL26, and NFR-028 records that retention classes exist while the periods do not. So the harness asserts the mechanism and never a period: that the placement term expiry starts exactly one retention timer whose `expires_at` comes from the retention rule version in force, and that the retention expiry closes the case only when its condition holds. Where the period or the rule version is needed, the sources are silent and the placeholder in the preconditions and in section 12.8 stands.

The harness is decoupled the way the services are. The case state, the closed_date, the closure_reason and the timers come from P3's contract and never from its schema (DP-01); the retention class of a document comes from P5's contract; cash recovered and loss come from DP13 Money and closure through P1's data-product contract, never from an ACE view read directly (DP-05, DP-18); the closing entry and its rule version come from P7's decision log, and the local decision record travels on `rwb.decision-record.v1` (DP-03); every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13); where a screen would compose these calls the path is the gateway-bff composite route (DP-19), and this harness builds no screen.

### 3. Preconditions

- The published contracts of P3 rwb-case (case and timers), P5 rwb-document (documents and retention), P7 rwb-decision (decision log), P1 rwb-source-data (DP13 and freshness), P4 rwb-access (session) and S7 rwb-writeoff (the seven steps of `WriteOffWorkflow`) are in the contract registry, and a stub set is generated from each one.
- DP13 Money and closure is published with one system of record, so cash recovered and loss have a named owner before the closing entry is compared (LDM v8).
- The synthetic case sits in SIT in PLACED_WITH_AGENCY with a placement whose `ends_at` has passed and `recovered_amount` 0, and it carries three documents, each with its retention class. The synthetic keys and dates are fixture data, never a business value.
- The retention rule version in force and its period: Not specified in the source documents (GAP-0457; ASM-0649). The run asserts the version the owner names and never a period, because NFR-031 leaves the period Not set under DL26.
- RWB-S7-E6025-APP owns the close and RWB-P3-E6025-APP owns the case state and the timers; until both land, the stubs of section 12.8 answer in their place on Day 1.
- The harness environment and its base hosts, the synthetic clock mechanism and the fixture dates, the shape of the retention evidence, the evidence retention, the pass or fail gate, and the synthetic case and document keys: Not specified in the source documents (GAP-0457; ASM-0649).

### 4. Flow

1. Harness: loads the closure fixture for the closed-case test: case `RW-2026-000725` in state PLACED_WITH_AGENCY, one placement whose `ends_at` 2026-11-15 has passed with `recovered_amount` 0, no open sale and no open exception, and the documents `DOC-SYN-000725-01`, `DOC-SYN-000725-02` and `DOC-SYN-000725-03`, each carrying the retention class its document type carries. On Day 1, before the owners are live, the stubs of section 12.8 return the same records.
2. Harness: reads `GET /api/recovery/case/v1/cases/{caseId}` and asserts PLACED_WITH_AGENCY, then reads `GET /api/recovery/case/v1/cases/{caseId}/timers` and asserts the placement timer running with its `started_at` and `expires_at`.
3. Harness: advances the clock fixture to the instant after the placement term. No expiry operation is called, because the Ownership Map publishes none for the placement, the retention timer or the case close. The harness then reads the case again and asserts RETENTION_RUNNING, the placement timer stopped, and exactly one retention timer running on the case.
4. Harness: reads the retention timer's `expires_at` as the owner reports it and reads `GET /api/recovery/decision/v1/decision-log?caseId={caseId}`, asserting the entry that names R-WO-36 and the rule version. Where the version or the period is needed, the placeholder of section 3 stands; the run pins the value it read and never writes one.
5. Harness: advances the clock fixture to that `expires_at` and reads the case: CASE_CLOSED with `closed_date` and `closure_reason` written (DF-CAS-022, DF-CAS-023), and `GET /api/recovery/case/v1/cases/{caseId}/timers` returning no running timer for the case.
6. Harness: reads `GET /api/recovery/source-data/v1/data-products/DP13/records?caseId={caseId}` with `GET /api/recovery/source-data/v1/data-products/freshness?product=DP13`, and asserts the closing entry carries cash recovered and loss equal to the DP13 values field by field, and that the central ledger holds one entry for the close.
7. Harness: reads `GET /api/recovery/document/v1/cases/{caseId}/documents` and then each document through `GET /api/recovery/document/v1/documents/{documentId}`, and asserts that every document answers with its `retention_class` set, that the retention action for the case and the run month is recorded, and that no document is removed inside its retention period.
8. Harness: calls `GET /api/recovery/access/v1/me/session` and asserts the caller's rights for the run, and repeats the read of the retention evidence as a synthetic caller without Document hub R.
9. Harness: repeats the retention expiry for the same case and asserts one closing entry, one ledger entry, CASE_CLOSED and the original `closed_date` unchanged.
10. Harness: sets, run by run, one open placement, one open sale, one open exception and one document whose retention class is empty, then a legal hold, and asserts each time that the case stays RETENTION_RUNNING, that nothing is written and that the report names the case and the blocking condition.
11. Harness: forces the local decision record and the central ledger unavailable and asserts that the case stays RETENTION_RUNNING, that the timers stay as they were, that no closing entry is written and that the answer carries MSG-P7-003.
12. Harness: writes one run report per case keyed by story and case, naming the contract version of each hop, whether the hop was a stub or the owner, the two clock instants, the retention class of each document, the closing entry and the ledger entry, every blocking condition and the six criteria.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-E6-025-01-ITG (ITG AC1) |
| X2 | The clock fixture is advanced and the owner's state does not change | The run fails on AC1 or AC2 and the report names the case, the instant and the state it read, so a clock the owner did not honour is a failure and not a pass | None | TC-E6-025-01-ITG (ITG AC1); TC-E6-025-02-ITG (ITG AC2) |
| X3 | The case closes while an open placement, an open sale or an open exception stands, or with one document without a retention class | The run fails on AC3 and the report names the case, the blocking condition and the document, so a closure that cut an obligation short is never reported as a pass | None | TC-E6-025-03-ITG (ITG AC3) |
| X4 | A document answers with an empty retention class after the close, or the close is taken under a legal hold | The run fails on AC4 and the report names the document and the hold, because a legal hold overrides the retention class and stops the expiry (NFR-072) | None | TC-E6-025-03-ITG (ITG AC3) |
| X5 | A repeated expiry writes a second closing entry, a second ledger entry or moves the closed_date | The run fails on AC5 and the report names the two entries and the two dates | None | TC-E6-025-02-ITG (ITG AC2) |
| X6 | The retention expiry is reached while the local decision record or the central ledger is unavailable and the case closes anyway | The run fails on AC6 and the report names the hop and the message; the close is never taken without its decision record | MSG-P7-003 (expected, and missing) | TC-E6-025-06-ITG (ITG AC6) |
| X7 | A synthetic caller without Document hub R reads the retention evidence | The run fails on the access criterion and the report names the caller role and the operation; a caller without the right who is answered is reported as such | MSG-P4-002 (expected, and missing) | TC-E6-025-05-ITG (Access) |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the two waits, RWB-S7-E6025-APP and RWB-P3-E6025-APP, replace their stubs and never block the lane |
| Negotiable | The fixture layout, the clock mechanism, the retention evidence shape, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The two expiries of a closed write-off case are proven end to end before wave 4 opens: the retention timer starts once, the close stops every timer, every document carries its class, and the closing entry agrees with DP13 and the ledger |
| Estimable | One runner, one stub set, two fixtures, one clock fixture, five assertions and one report |
| Small | Fits in one sprint with its six tests |
| Testable | Each criterion runs against the stubs and again against the real owners as the two I stories land |

### 7. Acceptance criteria

```gherkin
Feature: Close the case after the retention period - wave 4 closure and retention harness

  Background:
    Given the synthetic case "RW-2026-000725" sits in state "PLACED_WITH_AGENCY" with a placement whose ends_at "2026-11-15" has passed and recovered_amount 0
    Given the case carries the documents "DOC-SYN-000725-01", "DOC-SYN-000725-02" and "DOC-SYN-000725-03", each with a retention class
    Given the clock fixture holds the two instants, the placement term expiry and the retention expiry, as fixture data and never as a business value
    Given the owners' contracts are published and the stubs of section 12.8 answer from Day 1

  Scenario: AC1 The placement term expiry closes the placement and starts the retention timer (new, D-RCV-60)
    Given a case in state "PLACED_WITH_AGENCY" with ends_at passed and recovered_amount 0
    When the placement term expiry is reached on the clock fixture
    Then the placement is closed and the case moves to "RETENTION_RUNNING" under "R-WO-36"
    And the placement timer is stopped and exactly one retention timer runs on the case
    And its expires_at is the value the owner reads from the retention rule version in force
    And the decision record names "R-WO-36" and its version

  Scenario: AC2 The retention expiry closes the case and stops every timer (new, D-RCV-60)
    Given a case in state "RETENTION_RUNNING" whose retention timer has expired
    When the retention expiry is reached on the clock fixture
    Then the case moves to "CASE_CLOSED" under "R-WO-47"
    And closed_date and closure_reason are written on the case
    And GET "/api/recovery/case/v1/cases/{caseId}/timers" returns no running timer for the case
    And the closing entry is written with cash recovered and loss read from DP13 Money and closure
    And the central ledger holds one entry for the close

  Scenario: AC3 A case with an open action or an untagged document is not closed (new, D-RCV-60)
    Given a case in state "RETENTION_RUNNING" with an open placement, an open sale or an open exception standing, or with one document whose retention class is empty
    When the retention expiry is reached on the clock fixture
    Then the case stays in "RETENTION_RUNNING"
    And nothing is written on the case
    And the report names the case and the blocking condition

  Scenario: AC4 The close applies the retention class to every document (new, D-RCV-60)
    Given the case is closed and its three documents are read through the rwb-document contract
    When the harness reads the documents of the case
    Then every document answers with its retention_class set
    And the retention action for the case and the run month is recorded
    And no document is removed inside its retention period
    And a legal hold on the case stops the closure and the document retention

  Scenario: AC5 A repeated expiry writes no second closing entry and does not reopen the case (new, D-RCV-60)
    Given the case was closed on the first retention expiry
    When the same expiry is run a second time
    Then there is one closing entry and one ledger entry for the close
    And the case stays in "CASE_CLOSED" with its original closed_date
    And reopening it needs a written rule, a reason and an approver

  Scenario: AC6 The close is not taken when the decision cannot be recorded (new, D-RCV-60)
    Given the local decision record and the central ledger are both unavailable
    When the retention expiry is reached on the clock fixture
    Then the case stays in "RETENTION_RUNNING"
    And the timers stay as they were before the expiry
    And no closing entry is written
    And the answer carries "MSG-P7-003"
```

The four legacy acceptance criteria belong to RWB-S7-E6025-APP and RWB-P3-E6025-APP, and the six criteria above are the ones this ITG story owns.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | When the agency placement's `ends_at` has passed and `recovered_amount` is 0, the placement is closed and the retention timer starts | R-WO-36 |
| BR2 | The case closes only when no placement, no sale and no exception is open and every document carries a retention class | R-WO-47 |
| BR3 | On closure the case closes, every timer stops, and the closing entry is written with cash recovered and loss | R-WO-47 |
| BR4 | A document with no retention class holds the closure and raises a document task; the case stays in RETENTION_RUNNING | R-WO-48; NFR-028 |
| BR5 | Every document type carries a retention class, and the class sets how long the document is kept | NFR-028; R-WO-47 |
| BR6 | A legal hold stops deletion and expiry for the case or the document it covers, overriding the retention class | NFR-072 |
| BR7 | A document reaching the end of its retention period is disposed of or extended by a recorded decision, and is never removed silently | NFR-074 |
| BR8 | A case closes after its retention period, and reopening a closed case needs a written rule, a reason and an approver | REQ-S7-008 |
| BR9 | On case closure the retention class is applied to every document of the case | FEAT-COM-08 |

The harness asserts these rules and changes none of them. The retention period they depend on is **Not set** in the sources (NFR-031, open under DL26), so the run asserts the rule, the version and the mechanism and never a period.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| PLACED_WITH_AGENCY | PLACEMENT_TERM_EXPIRED | `ends_at` passed and `recovered_amount` = 0 | RETENTION_RUNNING, the placement closed and the retention timer started (R-WO-36) |
| RETENTION_RUNNING | RETENTION_TIMER_EXPIRED | No open placement, no open sale, no open exception, and a retention class on every document | CASE_CLOSED, every timer stopped and the closing entry written (R-WO-47) |
| RETENTION_RUNNING | RETENTION_TIMER_EXPIRED with one action open or one class missing | An open placement, an open sale or an open exception stands, or one document has no retention class | RETENTION_RUNNING, unchanged, and the blocking condition is named (R-WO-48) |
| RETENTION_RUNNING | RETENTION_TIMER_EXPIRED under a legal hold | A legal hold is in place on the case | RETENTION_RUNNING, unchanged, and the document retention stops (NFR-072) |
| CASE_CLOSED | RETENTION_TIMER_EXPIRED, repeated | The same expiry is run again for the closed case | CASE_CLOSED, unchanged, with the original closed_date and no second entry |
| CASE_CLOSED | A reopening request | A written rule, a reason and an approver are recorded | Out of scope here (REQ-S7-008; section 19) |

The harness changes no state. Every change in the table is made by an owner: S7 rwb-writeoff runs `WriteOffWorkflow` and its eligibility, committee, posting and post-charge-off steps; P3 rwb-case holds the state, the closed_date, the closure_reason and the timers; P5 rwb-document holds the retention class and the retention action; P7 rwb-decision holds the closing entry and the central ledger. A state the harness had set by hand would prove nothing, so the report names the owner and the operation behind every value it asserts.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CREDITAD, Credit Administration | Owns the closed case and reads the closing entry, the cash recovered and the loss; holds Write-off and posting A and C |
| RW-WOCOMM, RW-WRITEOFF, RW-FINANCE | Read the same closure evidence for their step of the write-off; hold Write-off and posting A (and C for RW-WRITEOFF) |
| RW-COMPLY | Reads the retention class of every document, the retention action and the legal hold outcome |
| RW-OFF, RW-AGENCYMG, RW-TRIBE | Subject-matter readers of the run report; they take no decision in this story |
| RW-PLATADM | Holds Platform administration R and reads the run report; the harness never acts as this role |
| QA lead | Owns the harness configuration, the fixtures, the clock fixture, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | S7 runs `WriteOffWorkflow`, P3 holds the state and the timers, P5 holds the retention, P7 writes the closing entry, P1 publishes DP13 and P4 answers the session; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; the session and the rights are answered by rwb-access |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | case_no, status, route_state, closed_date (DF-CAS-022), closure_reason (DF-CAS-023) | Read through the rwb-case contract |
| DF-WRK-027 to DF-WRK-044 | timer | case_id, timer_type, started_at, expires_at, paused, status, escalation_level | Read through the rwb-case contract |
| DF-DOC-001 to DF-DOC-033 | document | case_id, document_type, retention_class (DF-DOC-009), doc_version | Read through the rwb-document contract |
| DF-DOC-091 to DF-DOC-095 | retention_action | document_id, run_month, action, decision_log_id | Read through the rwb-document contract |
| DF-REF-116 to DF-REF-127 | retention_rule | record_class, retention_months, age_basis_field, end_action, rule_version, valid_from, valid_to | Read through the rwb-document contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | case_id, decision_code, rule_id, rule_version, final_call, outcome, decided_at | Read through the rwb-decision contract |
| DF-REF-001 to DF-REF-015 | rule_row | rule_id, rule_version, route_set, from_state, event_code | Read through the rwb-decision contract |

Field IDs are those in the Logical Data Model and Data Dictionary v8. The tables are the owners' and the harness reads them only through the owners' contracts. Cash recovered and loss are DP13 Money and closure, read through the rwb-source-data data-product contract, never from a view and never from a table. The harness owns no table and writes no row.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case state, the closed_date and the closure_reason (AC1, AC2, AC3, AC5, AC6) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | The placement timer and the retention timer, and no running timer after the close (AC1, AC2, AC6) |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document | Every document of the case and its retention class (AC4) |
| GET | `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document | One document's retention class and version (AC4) |
| GET | `/api/recovery/source-data/v1/data-products/DP13/records?caseId={caseId}` | P1 rwb-source-data | Cash recovered and loss at closure (AC2) |
| GET | `/api/recovery/source-data/v1/data-products/freshness?product=DP13` | P1 rwb-source-data | The business date and the load time of DP13 (AC2) |
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | The close entry, its rule version and the ledger entry (AC1, AC2, AC4, AC5, AC6) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's roles and rights for the run (AC4, Access) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). No operation is invented in this story: each path is the owner's published operation. The Ownership Map publishes no read operation for a write-off record and no retention operation for a document, so the harness reads the case, the timers, the documents, DP13 and the decision log, and drives the two expiries through the clock fixture instead of through a call. Where a screen would compose these calls the path would be the gateway-bff composite route (DP-19), and this harness builds none.

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | What the harness asserts |
|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 rwb-case | One event per transition, PLACED_WITH_AGENCY to RETENTION_RUNNING and RETENTION_RUNNING to CASE_CLOSED, keyed by caseId, in that order and once each (AC1, AC2, AC5). Its consumers are rwb-comms and rwb-reporting (Architecture v5 slide 42, row 05) |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | Every service, written locally by S7 and P3 for this close | One decision record for the close, carrying R-WO-47 and the rule version, that the central ledger in rwb-decision holds once (AC1, AC2, AC6) |

The harness reads the two topics with a test consumer that registers no production consumer group and drains with a cutoff, so the run fails when a state change is published twice or not at all. The consumer group, the cutoff and the evidence retention are Not specified in the source documents (GAP-0457; ASM-0649) and are configuration agreed at the wave entry check.

#### 12.5 Workflows and activities

None added. `WriteOffWorkflow` on task queue `rwb-writeoff` is observed and not built here: its step 6 is "Agency or sale after" under R-WO-29, R-WO-30 and R-WO-32, and its step 7 is "Retention, then close" under R-WO-47 with JOB-17 (Temporal and Drools Design v1, slide 23). The harness observes the two steps through the state they leave and through the decision record they write; it starts no workflow, changes no activity and owns no timer. Workflow history for a closed workflow is retained 30 days and then archived to Blob, which is the platform's and not this story's.

#### 12.6 Schedules

| Job | Owner | When | In this story |
|---|---|---|---|
| JOB-16 Write-off scan | S7 rwb-writeoff, a Temporal Schedule | Monthly, 3rd working day | Observed and not changed. It is the Schedule that starts `WriteOffWorkflow` (Architecture v5 slide 44; Temporal and Drools Design v1, slide 23) |
| JOB-17 Retention | P5 rwb-document, a Temporal Schedule | Monthly, 1st Sunday | Observed and not changed. It is the retention run whose action the harness reads for the case and the run month (Architecture v5 slide 44) |

The harness sets no cron, adds no Schedule and changes neither window.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); the case and the timers are P3's, the documents and the retention are P5's, the closing entry is P7's, the DP13 record is P1's and the write-off is S7's.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-writeoff | The seven steps of `WriteOffWorkflow` and its post-charge-off state | The case in PLACED_WITH_AGENCY with one placement whose `ends_at` 2026-11-15 has passed and `recovered_amount` 0; the placement closed and the retention started at the first instant; the close taken at the second instant, with the R-WO-36 and R-WO-47 decision records written |
| Stub for rwb-case | `GET /cases/{caseId}` and `/cases/{caseId}/timers` | The state PLACED_WITH_AGENCY, then RETENTION_RUNNING, then CASE_CLOSED with `closed_date` and `closure_reason`; one placement timer, then one retention timer with its `expires_at`, then no running timer |
| Stub for rwb-document | `GET /cases/{caseId}/documents` and `GET /documents/{documentId}` | The three documents with their retention class, the retention action for the case and the run month, and the empty class on one document in the AC3 and AC4 runs |
| Stub for rwb-decision | `GET /decision-log?caseId={caseId}` | The R-WO-36 entry with its rule version, the R-WO-47 close entry with cash recovered and loss, and one ledger entry for the close; unavailable in the AC6 run |
| Stub for rwb-source-data | `GET /data-products/DP13/records?caseId={caseId}` and `GET /data-products/freshness?product=DP13` | One DP13 record for the case with the cash recovered and the loss at closure, and the freshness of the product by business date |
| Stub for rwb-access | `GET /me/session` | Allows RW-CREDITAD with Document hub R; refuses a synthetic caller without Document hub R with 403 and MSG-P4-002 |
| Retention rule fixture | The retention rule rows of the legacy story | The retention rule version in force with `record_class`, `retention_months`, `end_action` and `valid_from`; the period and the version: Not specified in the source documents (GAP-0457; ASM-0649) |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and its base hosts, the clock mechanism and the fixture dates, the shape of the retention evidence, the evidence retention, the pass or fail gate, and the synthetic case and document keys are Not specified in the source documents (GAP-0457; ASM-0649).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 8 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published; two consumed, `rwb.case.CaseStateChanged.v1` on `rwb.case.events.v1` and `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` |
| Temporal | None added; `WriteOffWorkflow` on `rwb-writeoff` (steps 6 and 7), the JOB-16 Schedule in `rwb-writeoff` and the JOB-17 Schedule in `rwb-document` are observed and not changed |
| File | The closure fixture and the retention rule fixture, both read as files |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1027-CON and RWB-PLT-N001-CON) are delivered by the platform waves and are not repeated in the metadata H field of this story, which stays empty. The two blocking dependencies are the I stories RWB-S7-E6025-APP and RWB-P3-E6025-APP, which replace their stubs; until they are live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| ClosureRunner | Job | Runs the six owned criteria in order for one case and holds the run lock |
| StubSet | Fake | The six stubs and the retention rule fixture of section 12.8, generated from the published contracts, with each contract version pinned |
| ClosureFixture | Fixture | The synthetic case, its placement, its three documents and their retention class, read as data |
| ClockFixture | Fixture | The two instants, the placement term expiry and the retention expiry, as fixture data; it never carries a period or a business value |
| CaseStateAssertion | Service | Asserts PLACED_WITH_AGENCY, RETENTION_RUNNING and CASE_CLOSED through the rwb-case contract, with closed_date and closure_reason, and names the blocking condition when the close is withheld |
| TimerAssertion | Service | Asserts one placement timer, then one retention timer with its expires_at, then no running timer, and that a repeated expiry restarts none |
| RetentionAssertion | Service | Asserts the retention class of every document, the retention action for the case and the run month, that no document is removed inside its period, and that a legal hold stops the expiry |
| ClosingEntryAssertion | Service | Compares the close entry's cash recovered and loss with DP13 and asserts one closing entry and one ledger entry |
| EvidenceReport | Service | Writes one report per case keyed by story and case, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real owners as the two I stories land, on the synthetic case `RW-2026-000725`, its placement with `ends_at` 2026-11-15 and `recovered_amount` 0, and the documents `DOC-SYN-000725-01`, `DOC-SYN-000725-02` and `DOC-SYN-000725-03`. The two instants are fixture data and never a business value: the first is the placement term, the second is the `expires_at` the owner reports for the retention timer, because the retention period itself is **Not set** under DL26 (NFR-031). The environment and its base hosts, the clock mechanism and the fixture dates, the shape of the retention evidence, the evidence retention, the pass or fail gate, and the synthetic case and document keys are Not specified in the source documents (GAP-0457; ASM-0649). The harness seeds nothing by hand and never writes a schema row.

**Build steps**

1. Generate the six stubs from the published contracts, build the retention rule fixture, and pin each contract version in the run report; fail the run on a mismatch (X1).
2. Build the ClosureFixture and the ClockFixture, and prove the two instants are read as data and that no period is written in code (X2).
3. Build the CaseStateAssertion and the TimerAssertion for AC1: the placement timer running, the case PLACED_WITH_AGENCY, then RETENTION_RUNNING with the placement timer stopped and one retention timer running with its expires_at, and the R-WO-36 decision record naming its rule version.
4. Add AC2: the close at the second instant, CASE_CLOSED with closed_date and closure_reason, no running timer, the closing entry with cash recovered and loss compared with DP13 and its freshness, and one ledger entry.
5. Add the RetentionAssertion for AC4: every document with its retention class, the retention action for the case and the run month, no document removed inside its period, and the legal hold path (X4).
6. Add AC3 and AC5: one open placement, one open sale, one open exception and one empty retention class each leave the case in RETENTION_RUNNING with the blocking condition named, and a repeated expiry writes one closing entry, one ledger entry and keeps the original closed_date (X3, X5).
7. Add the AC6 path with the decision record and the ledger forced unavailable, then the access path through `GET /api/recovery/access/v1/me/session`, then the EvidenceReport and the gate, and swap a stub for the real owner as each I story lands (X6, X7).

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-S7-E6025-APP and RWB-P3-E6025-APP when they land, and the wave entry check holds a run report keyed by story and case.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-S7-001 | Error | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text. MSG-S7-001 is asserted where the fixture carries a population whose scan is on hold: that case never reaches PLACED_WITH_AGENCY and AC1 is not taken on it. MSG-GEN-001 is asserted on the synthetic caller's missing field. MSG-P4-002 is asserted on the access criterion, and MSG-P7-003 on the close that cannot record its decision.

### 15. Screens and states

The legacy story's screen is SCR-27 Write-off proposal, and it is RWB-S7-E6025-APP's: this harness builds no screen and reads none. The states it asserts are read through rwb-case, and the retention evidence through rwb-document.

| State | What the case and the documents show |
|---|---|
| PLACED_WITH_AGENCY | The case on the agency placement, the placement timer running with its expires_at, cash recovered 0 |
| RETENTION_RUNNING | The placement closed, the placement timer stopped, one retention timer running, and the case waiting for the retention expiry |
| CASE_CLOSED | The case closed with closed_date and closure_reason, no running timer, every document with its retention class, one closing entry and one ledger entry |

The harness renders no screen. The retention period value the states depend on is Not specified in the source documents (GAP-0457; ASM-0649), because NFR-031 leaves it **Not set** under DL26; what the wave entry check looks at instead is the run report.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-025-01-ITG | ITG AC1 | Integration | A case in PLACED_WITH_AGENCY with the placement term passed |
| TC-E6-025-02-ITG | ITG AC2 | Integration | A case in RETENTION_RUNNING whose retention timer has expired |
| TC-E6-025-03-ITG | ITG AC3 | Integration | One open placement, one open sale and one document without a retention class |
| TC-E6-025-04-ITG | ITG AC6 | Integration | A forced decision-record and ledger failure at the close |
| TC-E6-025-05-ITG | Access | Component | A synthetic caller without Document hub R reading the retention evidence, refused with MSG-P4-002 |
| TC-E6-025-06-ITG | Principle 5; ITG AC6 | Integration | A forced decision-record failure stops the close with MSG-P7-003 |

The AC column names the ITG AC each copy asserts, and the four legacy ACs stay with RWB-S7-E6025-APP and RWB-P3-E6025-APP.

### 17. Guardrails

- No business value in code: the synthetic case and document keys, the two clock instants, the fixture contents, the retention evidence and the report layout are data.
- No personal data in logs, fixtures or reports: every key is synthetic and no customer record is read at all.
- No read of another service's schema and no direct view read: the case and the timers come from rwb-case, the documents and the retention from rwb-document, the closing entry from rwb-decision, and the cash recovered and loss from DP13 through the rwb-source-data contract (DP-01, DP-05).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11).
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never writes a row by hand.
- A failing criterion is fixed in the service that owns it or reported as a gap; it is never waived in the script.
- The legal hold rule is never bypassed by the harness: a hold on the case stops the closure and the document retention, and a run that closes anyway is a failure (NFR-072).

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-E6-025 Close the case after the retention period | Recovery Workbench User Stories Epics 3 to 8 v3, lines 10563 to 10658 | Sections 1, 3, 11, 14 and 19 of this file |
| Legacy AC1 to AC4 and the six legacy test cases TC-E6-025-01 to TC-E6-025-06 | The same, lines 10577 to 10604 and 10645 to 10654 | The four ACs stay with RWB-S7-E6025-APP and RWB-P3-E6025-APP (section 19); the six cases are copied as -ITG in section 16. No legacy AC is owned here |
| R-WO-36 and R-WO-47, with R-WO-48 on the missing retention class | Business Rules and Routing Logic v4, lines 367, 378 and 379 | Sections 7, 8 and 9 |
| JOB-16 Write-off scan and JOB-17 Retention | Architecture v5 Text Extract v1 slide 44; Temporal and Drools Design v1, slide 23 | Sections 12.5 and 12.6 |
| REQ-S7-008 | Business Requirements Program v4, line 399 | Section 8, BR8; section 7, AC5 |
| NFR-028, NFR-031, NFR-072, NFR-074 | The same, lines 505, 508, 510 and 512 | Sections 2, 3, 8 and 15 |
| FEAT-WOF-13 Close the case after the retention period and FEAT-COM-08 Apply retention on case closure | Epics 3 to 8 Specification v3, lines 120 and 156 | Sections 2 and 7 |
| DF-CAS-001 to DF-CAS-023, DF-WRK-027 to DF-WRK-044, DF-DOC-001 to DF-DOC-033, DF-DOC-091 to DF-DOC-095, DF-REF-116 to DF-REF-127, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015 | Logical Data Model and Data Dictionary v8 | Section 11 |
| DP-03, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |
| ADR-015, Kafka with outbox and CloudEvents | Decision Log D-RCV-60; Template and Rules v1 §R8.4 | Sections 12.4 and 12.9, the two consumed events and the decision record |
| ADR-020, contract-first REST, one hop and a 2 s timeout | The same | Section 12.2 and section 17 |
| DL26, the retention period open | Decision Log v10, DL26 | Sections 2, 3 and 15, where the period stays Not set |
| RWB-E1-042 and RWB-E1-043, parameters and reference data | Epic 1 story masters | Section 11, the retention rule rows read through rwb-document |

### 19. Out of scope

- RWB-S7-E6025-CON and RWB-S7-E6025-APP: the close contracts, `WriteOffWorkflow`, the R-WO-36 and R-WO-47 build and all four legacy acceptance criteria.
- RWB-P3-E6025-APP: the case state, the closed_date, the closure_reason and the timers, and the legacy acceptance criteria that belong to P3.
- The agency placement and its fee: RWB-E6-029, the other RWB-E7 keys and S9's stories.
- The post charge-off payment (RWB-E6-027) and the sale of a post charge-off population (RWB-E6-028).
- The retention rule and its periods as a reference-data product: P5's retention stories.
- The legal hold workflow; this harness only asserts that a hold stops the closure and the retention.
- SCR-27 Write-off proposal, RWB-S7-E6025-APP's screen.
- The document hub itself: storage, custody, OCR and the WORM container are P5's.
- Platform deployment and configuration, including workflow history retention and the archive to Blob.
