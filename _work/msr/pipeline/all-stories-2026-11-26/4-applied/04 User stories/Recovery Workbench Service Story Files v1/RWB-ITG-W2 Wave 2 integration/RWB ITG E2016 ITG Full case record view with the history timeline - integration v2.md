# RWB-ITG-E2016-ITG Full case record view with the history timeline

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2016-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-016 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP11, DP13, DP14, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P3-E2016-APP, RWB-P5-E2016-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-014, FR-PLT-015, FR-PLT-020) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-016 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-ITG-E2016-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **member of the integration and QA team**, I want **a repeatable cross-service journey harness that runs the case record timeline and the queue history through gateway-bff and the owning services**, so that **the wave 2 case history journey is proven end to end, with evidence, before the release is accepted**.

This story builds the harness and the evidence only. It builds no production screen, endpoint, table, workflow or schedule, and it owns no table. The real behaviour is owned by the two I stories RWB-P3-E2016-APP (the timeline, its filters, the queue history and the merge in rwb-case) and RWB-P5-E2016-APP (the document metadata the timeline reads for a case), and those two stories block the ITG run.

The merge in the journey also reads the P7 decision log and the P6 notices through their contracts, because a decision item links to its ledger entry and a notice item carries the notice facts. Those two sources are part of the journey even though no separate I story is listed for them; their behaviour is asserted through the published contracts and the §12.8 fakes, and it is not claimed as work of this story.

### 2. Business rationale

The legacy RWB-E2-016 journey crosses more than one service: rwb-case holds the case, its assignments and transfers, the interactions, the timers and the queues; rwb-decision holds the central decision ledger; rwb-document holds the document metadata; rwb-comms holds the notices; and rwb-access answers the authorisation check. Until the real services are exercised together through the gateway, the program cannot show that an owner reads the whole case in one place, which is the outcome the program targets at 5 days from 23 days.

The harness gives one repeatable run per business date that proves the composite route composes the timeline one hop at a time inside the 2 s budget, that items are merged newest first with type, actor and time, that a filter narrows the answer without a cross-schema read, that the queue history carries its reason code and rule ID, that a role without a right sees the items it may read and nothing more, and that one slow source degrades one part of the answer instead of the whole screen. It meets REQ-WKM-008, REQ-OCC-008, REQ-CWC-016 and REQ-DRI-002 at the integration level and leaves every business rule and every screen behaviour where the owning stories put them.

### 3. Preconditions

- The two I stories are published and deployed in the SIT environment: RWB-P3-E2016-APP (the timeline, the type and date filters, the paging, the queue history and the merge in rwb-case) and RWB-P5-E2016-APP (the document metadata for a case).
- gateway-bff is deployed with the composite route of DP-19 available. The gateway-bff composite timeline route path and its merge order: Not specified in the source documents (GAP-0400; ASM-0575).
- The contract fakes of §12.8 are published from the owning services' OpenAPI documents, so the harness can run green from Day 1 before the I stories land, including the P7 decision log, the P6 notices and the P5 document query.
- The masking rules and the reason-code reference data LOV-ASSIGN-REASON and LOV-TRANSFER-REASON are loaded by the owning stories through their contracts; the harness reads them and holds no copy.
- The harness environment, its test-data seeding and its evidence format and retention: Not specified in the source documents (GAP-0400; ASM-0575).

### 4. Flow

1. Harness: seeds the synthetic cases, the 30 events of RW-2026-000601, the queue history, the users and their scopes through the owning contracts or the published fakes.
2. Harness: calls the case timeline through gateway-bff with page 0 and size 50 and asserts the 30 items, newest first, each with type, actor and time.
3. Harness: applies the type filter DECISION and asserts the 6 decision items, each with its entry ID, then opens one entry through the P7 contract and reads the ledger entry.
4. Harness: applies the date filter from 2026-12-05 to 2026-12-08 and asserts the inclusive range.
5. Harness: opens the queue history and asserts the newest-first moves with from and to queue, from and to owner, reason code and rule ID, and the allocation first with reason ALLOCATION.
6. Harness: repeats the journey as RW-PHONECOL and asserts that no decision and no notice item is returned while the other item types are.
7. Harness: forces the document query to time out, asserts the other 25 items and MSG-GEN-006 naming Document hub in unavailableSources, then returns the fake to its healthy answer.
8. Harness: forces each remaining failure of §5 through the fakes and asserts the message and that nothing was written, including the out-of-scope case and the empty filter.
9. Harness: reads the 4,000-item case at page size 50, asserts the first 50 items within 2 s at the 95th percentile over 20 runs and a total of 4,000, then writes one run report per business date, keyed by story and business date; the report format and retention are Not specified in the source documents (GAP-0400; ASM-0575).

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|
| X1 | The document query does not answer within 2 s | The 25 items of the other sources are returned; the answer lists Document hub in unavailableSources and does not fail | MSG-GEN-006 | TC-E2-016-06-ITG |
| X2 | The caller lacks Decision log R or Litigation R | Decision items or notice items are left out, with no error and no gap in the other items | None | TC-E2-016-05-ITG |
| X3 | Date to is before date from | 422; nothing is read from the sources and nothing is written | MSG-GEN-003 | TC-E2-016-07-ITG |
| X4 | No item matches the filter | An empty page with MSG-P3-019 and total 0 | MSG-P3-019 | TC-E2-016-08-ITG |
| X5 | An assignment written before the queue was recorded | The move is returned with "Queue not recorded" and reason ALLOCATION, and the run continues | None | TC-E2-016-09-ITG |
| X6 | The case is outside the caller's scope | 404 from the composite route; nothing is returned and nothing is written | MSG-P4-003 | TC-E2-016-10-ITG |
| X7 | The caller holds no Case record R | 403 on the direct call and on the composite route; the answer carries the refusal, not an empty timeline | MSG-P4-002 | TC-E2-016-12-ITG |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs on its own once the two I stories are deployed; until then it runs against the §12.8 fakes |
| Negotiable | The harness pack, the data seeding and the evidence format are agreed with QA; no business value is fixed by the harness |
| Valuable | The case history is evidenced across services rather than per service, including the single-item links and the queue moves |
| Estimable | One harness project, one journey specification, one fake pack, one latency measurement and one run report |
| Small | Fits in one iteration with the owning stories' contract tests |
| Testable | Each scenario of §7 is one automated journey with synthetic data and a machine-checkable result |

### 7. Acceptance criteria

```gherkin
Feature: Full case record view with the history timeline - wave 2 integration harness

  Background:
    Given the business date is 2026-12-20
    Given case "RW-2026-000601" is owned by "U-CO-01" in team "MTG-BKK" and holds 30 events: 4 assignments, 3 transfers, 8 contacts, 6 decision log entries, 2 notices, 5 documents and 2 timer events
    Given case "RW-2026-000601" was allocated to "MTG-BKK-CO" on 2026-11-30 and transferred to "LIT-BKK-01" with reason "R05" on 2026-12-05, to "MTG-BKK-CO" with reason "R06" on 2026-12-08 and to "LIT-BKK-02" with reason "R01" on 2026-12-12

  Scenario: AC1 The composite timeline through gateway-bff (new, D-RCV-60)
    Given the harness calls the case timeline through gateway-bff at "Not specified in the source documents (GAP-0400; ASM-0575)" for "RW-2026-000601" with no type filter, page 0 and size 50
    When gateway-bff returns the composite answer and rwb-case merges its own records with the rwb-decision, rwb-document and rwb-comms contracts
    Then the route returns 30 items newest first, each with type, actor and time
    And the 30 items are merged from rwb-case, rwb-decision, rwb-document and rwb-comms with no gap and no duplicate
    And each source is called once, one hop, with the 2 s timeout and a breaker per downstream
    And no service reads another service's schema
    And the run report holds one trace spanning the gateway and each owning service
    And the first page is returned within 2 s at the 95th percentile over 20 runs

  Scenario: AC2 Ordering, filters and the queue history (new, D-RCV-60)
    Given the type filter is set to "DECISION" with page 0 and size 50
    When the timeline refreshes through gateway-bff
    Then only the 6 decision items are returned, newest first
    And each decision item carries its decision log entry ID
    When the harness opens one entry through GET /api/recovery/decision/v1/decision-log/{entryId}
    Then the ledger entry is returned with its entry ID and its decided time
    When the date filter is from 2026-12-05 to 2026-12-08
    Then only items dated 2026-12-05 to 2026-12-08 inclusive are returned
    When the harness opens the queue history of "RW-2026-000601"
    Then the moves are returned newest first with from queue, to queue, from owner, to owner, reason code and rule ID
    And the allocation on 2026-11-30 is the first entry with reason "ALLOCATION"
    When the harness reads case "RW-2026-000604" with 4,000 items at page size 50
    Then the first 50 items are returned within 2 s at the 95th percentile over 20 runs
    And the total is 4,000

  Scenario: AC3 Rights filtering and partial answers (new, D-RCV-60)
    Given user "U-PC-01" holds RW-PHONECOL with case "RW-2026-000601" in scope
    When "U-PC-01" opens the case timeline through gateway-bff
    Then no decision item and no notice item is returned
    And contacts, assignments, transfers, documents and timer events are returned
    Given the document query does not answer within 2 s
    When "U-CO-01" opens the case timeline through gateway-bff
    Then the 25 items from the other sources are returned
    And the answer lists "Document hub" in unavailableSources with MSG-GEN-006
    When the harness opens the queue history of "RW-2026-000602", whose assignment of 2026-11-30 recorded no queue
    Then the move is returned with "Queue not recorded" and its reason "ALLOCATION"
    Given the type filter is set to "NOTICE" and the dates 2026-11-01 to 2026-11-15
    When the timeline refreshes
    Then the answer carries MSG-P3-019 with no items and total 0

  Scenario: AC4 Validation and refusals (new, D-RCV-60)
    When "U-CO-01" sets the date filter from 2026-12-10 to 2026-12-01
    Then the request is refused with 422 and MSG-GEN-003 naming "to" and "from"
    And nothing is written
    When "U-CO-01" asks for page size 500
    Then the request is refused with 422 and MSG-GEN-002
    And nothing is written
    Given case "RW-2026-000603" belongs to team "SME-NTH" and "U-CO-01" has scope Own in team "MTG-BKK"
    When "U-CO-01" opens its timeline through gateway-bff
    Then the answer is 404 with MSG-P4-003
    And nothing is written
```

These four criteria are new for the ITG harness and do not restate the app criteria owned by the I stories.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The timeline holds every assignment, transfer, contact, decision log entry, notice, document and timer event of the case | REQ-WKM-008; casemodel.txt Case file |
| BR2 | Items are ordered newest first; items at the same time keep the order of their sources' sequence | events.txt Rules (ordering) |
| BR3 | A decision item shows only to a role with Decision log R, a document item only with Documents R, a notice item only with Litigation R | roles.txt Permissions; CTL-09 |
| BR4 | Queue history shows each assignment with its from and to queue, from and to owner, reason, reason code and rule ID | REQ-WKM-008; REQ-CWC-016 |
| BR5 | A decision item links to its decision log entry, which is never changed; a correction shows as a further entry | R-UNI-24; REQ-DRI-002 |
| BR6 | Personal data in a contact summary is masked by role | CTL-11; DL26 |
| BR7 | A source that does not answer in time does not stop the timeline | NFR-008 |

The harness asserts these rules against the owning services and the published contracts; it does not re-implement them. No BR row is changed by this story.

### 9. State transitions

None. The harness changes no case status and no case state; it reads records only. The facts below are caused by the owning services and are observed and asserted by the harness.

| Observed fact | Caused by | Asserted as |
|---|---|---|
| Case allocated to a queue | rwb-case allocation | The first queue-history entry with reason ALLOCATION (TC-E2-016-03-ITG) |
| Case transferred with a reason code | rwb-case transfer | A later queue-history entry with from and to queue, from and to owner, reason code and rule ID (TC-E2-016-03-ITG) |
| Decision recorded | rwb-decision ledger | A decision item with its entry ID (TC-E2-016-02-ITG) |
| Document attached | rwb-document metadata | A document item (TC-E2-016-01-ITG) |
| Notice sent | rwb-comms notice | A notice item, left out for RW-PHONECOL (TC-E2-016-05-ITG) |
| Timer started or breached | rwb-case timer | A timer item (TC-E2-016-01-ITG) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | The synthetic user the harness drives: reads the timeline and the queue history in scope (Case record R; Decision log R; Documents R; Litigation R) |
| RW-TEAMMGR, team manager | Reads the timeline and the queue history (Case record R; Decision log R); used by the access case |
| RW-PHONECOL, phone collector | Reads the timeline without decision items and without notice items (Case record R; Documents R) |
| RW-CONDUCT, conduct and QA officer | Reads every item (R in all areas) |
| RW-AUDIT, internal audit | Reads every item (R in all areas); changes nothing |

Authorisation is answered by rwb-access through POST /api/recovery/access/v1/authorise on every call, and the harness asserts the refusal of a role without Case record R.

### 11. Data

The harness owns no table. It reads the fields below through the owning services' contracts and asserts them; the field IDs are those of the Logical Data Model and Data Dictionary.

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-011 | recovery_case | team_code | Read |
| DF-WRK-002 | queue | queue_code | Read |
| DF-WRK-010 | assignment | case_id | Read |
| DF-WRK-012 | assignment | assignee_user_id | Read |
| DF-WRK-013 | assignment | assigned_at | Read |
| DF-WRK-014 | assignment | ended_at | Read |
| DF-WRK-015 | assignment | reason | Read |
| DF-WRK-016 | assignment | rule_id | Read |
| DF-WRK-039 | assignment | queue_id | Read |
| DF-WRK-040 | assignment | transfer_reason_code | Read |
| DF-INT-002 | interaction | case_id | Read |
| DF-INT-004 | interaction | occurred_at | Read |
| DF-INT-005 | interaction | channel | Read |
| DF-INT-006 | interaction | direction | Read |
| DF-INT-008 | interaction | contact_result | Read |
| DF-INT-011 | interaction | summary | Read |
| DF-WRK-030 | timer | timer_type | Read |
| DF-WRK-031 | timer | started_at | Read |
| DF-WRK-035 | timer | status | Read |
| DF-DEC-001 | decision_log_entry | id | Read through the P7 rwb-decision contract |
| DF-DEC-003 | decision_log_entry | decision_code | Read through the P7 rwb-decision contract |
| DF-DEC-004 | decision_log_entry | rule_id | Read through the P7 rwb-decision contract |
| DF-DEC-012 | decision_log_entry | final_call | Read through the P7 rwb-decision contract |
| DF-DEC-016 | decision_log_entry | decided_at | Read through the P7 rwb-decision contract |
| DF-DOC-001 | document | id | Read through the P5 rwb-document contract |
| DF-DOC-004 | document | document_type | Read through the P5 rwb-document contract |
| DF-DOC-005 | document | source | Read through the P5 rwb-document contract |
| DF-LEG-015 | notice | id | Read through the P6 rwb-comms contract |
| DF-LEG-018 | notice | notice_type | Read through the P6 rwb-comms contract |
| DF-LEG-019 | notice | sent_date | Read through the P6 rwb-comms contract |
| DF-LEG-022 | notice | delivery_status | Read through the P6 rwb-comms contract |

Test data is synthetic. No production case, party, notice or document is used, and no personal data is written to a run report.

### 12. Contract

#### 12.1 REST operations provided

None. The harness calls the owning services; it serves no operation.

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout and the circuit breaker per downstream of DP-11 apply to every row.

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}/timeline` | P3 rwb-case | The timeline items and the queue-history items of a case with the type, date and paging filters |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case facts, the team and the scope the answer is composed for |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | The ledger entry a decision item links to (Architecture v5 slide 14: central decision ledger) |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document | The document metadata the document items are built from |
| GET | `/api/recovery/comms/v1/notices/{noticeId}` | P6 rwb-comms | The notice a notice item is built from |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The role, scope and right check used by the composite route and by the direct calls (Architecture v5 slide 14 and slide 41: rwb-access IN POST /authorise) |

The composite screen route itself is gateway-bff (DP-19), owned by the platform edge story RWB-PLT-N001-CON. Its path and merge order are Not specified in the source documents (GAP-0400; ASM-0575).

#### 12.3 Events published

None. The harness produces no event.

#### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| rwb.decision-record.DecisionRecorded.v1 | rwb.decision-record.v1 | P7 rwb-decision (ledger); every service publishes its own record | The ledger entry a decision item links to is present in the central ledger within 5 minutes of the call, and the entry ID in the timeline item resolves to it |

The event is consumed for assertion only; order per case is guaranteed by the case key on the topic, and the harness reads the ledger through the P7 contract rather than from a topic.

#### 12.5 Workflows and activities

None added. The harness starts no workflow and adds no activity; it drives REST only. CaseWorkflow in rwb-case and the P7 ledger ingest it observes are owned and started by the owning services.

#### 12.6 Schedules

None. The harness run is started by the test pipeline, not by a Temporal Schedule and not by Airflow.

#### 12.7 Tables owned

None.

#### 12.8 Contract fakes

| Fake | Serves | Stubbed answers |
|---|---|---|
| rwb-case | timeline, case facts, authorise hand-off | RW-2026-000601 with 30 items and the four queue moves; RW-2026-000602 with an assignment that has no queue; RW-2026-000603 in SME-NTH; RW-2026-000604 with 4,000 items; 422 for to before from and for a page size outside 1 to 200 |
| rwb-decision | decision-log/{entryId} | The 6 entries of RW-2026-000601 with their IDs, decided times and decision codes; a ledger answer for the DecisionRecorded assertion |
| rwb-document | cases/{caseId}/documents | The 5 documents of RW-2026-000601; a slow answer beyond 2 s for the timeout case |
| rwb-comms | notices/{noticeId} | The 2 notices of RW-2026-000601 with type, sent date and delivery status |
| rwb-access | authorise | Allow RW-CASEOWN in scope; allow RW-PHONECOL without Decision log R and without Litigation R; refuse a role without Case record R with MSG-P4-002; refuse SME-NTH for a team MTG-BKK scope with MSG-P4-003 |

The fakes are published from the owning services' OpenAPI documents and are replaced by the real service as each I story lands, contract by contract. The harness repository and its environment: Not specified in the source documents (GAP-0400; ASM-0575).

#### 12.9 Call-type summary

| Call type | Used | Detail |
|---|---|---|
| REST | Yes | Six consumed operations of §12.2 through gateway-bff and the owning services; one hop, 2 s timeout, breaker per downstream |
| Kafka | Yes | Consumes rwb.decision-record.DecisionRecorded.v1 on rwb.decision-record.v1 for the ledger assertion; publishes nothing |
| Temporal | No | Starts no workflow and adds no activity or Nexus operation; it observes the case the owning workflow runs |
| File | No | Documents are asserted through the P5 metadata contract, never read from blob storage |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies named by this table are delivered by the platform wave and are not repeated in the metadata H list. The blocking dependencies of this story are the two I stories.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Test harness | Runs one journey per business date, keyed by story and business date, and stops at the first failed assertion with the trace |
| TimelineClient | Harness adapter | Calls the composite timeline route and the six consumed operations of §12.2 through gateway-bff with the type, from, to, page and size parameters |
| FakePack | WireMock project | Serves rwb-case, rwb-decision, rwb-document, rwb-comms and rwb-access from the published OpenAPI documents of §12.8 |
| SchemaBoundaryCheck | Assertion | Fails the run on any cross-schema reference found in the trace, so a service never reads another service's tables |
| OrderingCheck | Assertion | Fails the run when an item is not newest first, when items at the same time break their source sequence, or when the DECISION filter returns an item of another type |
| LatencyCheck | Assertion | Measures the first page over 20 runs and fails the run when the 95th percentile is above 2 s, at 30 items and at 4,000 items with page size 50 |
| RunReportWriter | Reporter | Writes one run report with the trace and the per-assertion result; format and retention Not specified in the source documents (GAP-0400; ASM-0575) |

**Environment and test data**

- Environment: SIT, one namespace, the two I stories deployed from their wave 2 builds or replaced by the §12.8 fakes. Harness repository, environment and data seeding: Not specified in the source documents (GAP-0400; ASM-0575).
- Data: synthetic cases RW-2026-000601 with 30 events and the four queue moves, RW-2026-000602 with an assignment that has no queue, RW-2026-000603 in SME-NTH, RW-2026-000604 with 4,000 items; the users U-CO-01 with RW-CASEOWN and U-PC-01 with RW-PHONECOL; the business date 2026-12-20. No production record is copied.
- Reset: each run starts from the seeded state, so a repeated run is deterministic and the same report is produced.

**Build steps**

1. Build JourneyRunner and TimelineClient against the published OpenAPI documents of the owning services.
2. Publish FakePack for the five services from the same documents, and prove the harness runs green from Day 1 on the fakes.
3. Add the composite route assertion of AC1, including the one-hop check, the 2 s per-call budget, the single trace and the SchemaBoundaryCheck.
4. Add the ordering, type filter, date filter, entry link, queue history and 4,000-item latency assertions of AC2.
5. Add the rights filtering and partial answers of AC3, including the unavailableSources answer with MSG-GEN-006 and the empty answer with MSG-P3-019.
6. Add the validation and refusals of AC4 and assert that nothing is written on a refusal.
7. Replace each fake with the real service as its I story lands, contract by contract, publish the run report per business date and add the pass/fail gate agreed with QA; the gate definition: Not specified in the source documents (GAP-0400; ASM-0575).

**Feature switch:** the harness has no production feature flag and runs in the test environment only. The production switch it exercises is `rwb.p3.full-timeline` from the legacy solution plan; the harness asserts the disabled state, where the case record shows the earlier timeline, and the enabled state, where the composite timeline is returned.

**Done when:** the journey runs green against the two deployed I stories in SIT, the run report for the business date holds every assertion of §7 and §16 with its trace, the 4,000-item case is measured and signed off by QA at the 95th percentile, and the pass/fail gate agreed with QA is met for one full business date.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-019 | No item matches the filter | Nothing on this case matches the filter. |
| MSG-GEN-002 | Page size outside 1 to 200 | {field} must be between {min} and {max}. |
| MSG-GEN-003 | Date to is before date from | {field} cannot be before {other}. |
| MSG-GEN-006 | A source module does not answer in time | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | A role without Case record R opens the timeline | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. |

The harness asserts the message ID and the substituted values, including "Document hub" in MSG-GEN-006 and "to" and "from" in MSG-GEN-003; it does not own the message text. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-04 Case timeline | Loading | The composite route answers with the first page and the thirty items; the harness reads the answer the loading state consumes |
| SCR-04 Case timeline | Filtered | The type and date filters narrow the answer; a decision item opens its ledger entry; the queue history is returned with reason code and rule ID; a slow source appears in unavailableSources |
| SCR-03 Case record | Read only | The timeline is opened from the record and the case facts come from the case operation; no edit control is exercised |

The harness opens no screen and renders no page; it asserts the composite route answer that the screen consumes. Screen-level behaviour remains with the owning APP stories. The harness environment and evidence detail: Not specified in the source documents (GAP-0400; ASM-0575).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-016-01-ITG | AC1, BR1, BR2; ITG AC1 | Integration | 30 items over seven types; 20 timed runs |
| TC-E2-016-02-ITG | AC2, BR5; ITG AC2 | Integration | Filter DECISION over the AC1 case |
| TC-E2-016-03-ITG | AC3, BR4; ITG AC2 | Integration | One allocation and three transfers with reasons R05, R06, R01 |
| TC-E2-016-04-ITG | AC4; ITG AC2 | Integration | Date filter 2026-12-05 to 2026-12-08 |
| TC-E2-016-05-ITG | AC5, BR3; ITG AC3 | Integration | RW-PHONECOL on the AC1 case |
| TC-E2-016-06-ITG | AC6, BR7; ITG AC3 | Integration | Stubbed document query delayed 3 seconds |
| TC-E2-016-07-ITG | AC7; ITG AC4 | Integration | From 2026-12-10, to 2026-12-01 |
| TC-E2-016-08-ITG | AC8; ITG AC3 | Integration | NOTICE filter in November |
| TC-E2-016-09-ITG | AC9; ITG AC3 | Integration | Assignment with no queue |
| TC-E2-016-10-ITG | AC10; ITG AC4 | Integration | Case of team SME-NTH |
| TC-E2-016-11-ITG | AC11; ITG AC2 | Integration | 4,000 synthetic items, page size 50 |
| TC-E2-016-12-ITG | Access; ITG AC4 | Component | RW-REFADM (no Case record right) calls the timeline; refused with MSG-P4-002 |

The AC column in Covers is the legacy AC of RWB-E2-016 that the copy is derived from; the ITG AC is the criterion of §7 that the copy asserts at integration level. The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the legacy test case ID.

### 17. Guardrails

- No business value in code: the type list, the labels, the page size limits, the 2 s timeout and the reason codes are data held by the owning services; the harness reads them and never holds a copy.
- No personal data in logs, tests, traces or reports: contact summaries are masked by role and never logged; the harness uses synthetic parties and stores IDs and assertions only.
- No read of another service's schema: every read goes through the owner's contract, the SchemaBoundaryCheck fails the run on a cross-schema reference, and only rwb-source-data reads the ACE views.
- No production data and no outside system: the harness calls only the owning services and their fakes, never an outside gateway or a production endpoint.
- One hop only: the harness fails a run when the trace shows a call chain deeper than the gateway and one owner.
- The timeline never writes: the harness asserts that a refusal and a successful read leave every source unchanged.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-008 | Queue and transfer history visible on the case | Business Requirements Epic 2, sections 3.3 and 4; Program, section 5.3 | FEAT-WKM-08, FEAT-WKM-09 | 06 Take over and own the case | R-UNI-24; CTL-09; CTL-11 | TC-E2-016-01-ITG to TC-E2-016-12-ITG |
| REQ-OCC-008 | History timeline of every state change, transfer, contact, document and decision | Business Requirements Epic 2, sections 3.3 and 4 | FEAT-WKM-08, FEAT-WKM-09 | 06 Take over and own the case; All recovery processes | None | TC-E2-016-01-ITG |
| REQ-CWC-016 | Every allocation, assignment, transfer and timer event is logged with the rule ID and the rule version that caused it | Business Requirements Epic 1, section 4 | FEAT-WKM-09 | 06 Take over and own the case | BR4 | TC-E2-016-03-ITG |
| REQ-DRI-002 | The decision log is append only; a correction is a new record naming the one it corrects | Business Requirements Epic 1, section 4 | FEAT-WKM-08 | 06 Take over and own the case | BR5; R-UNI-24 | TC-E2-016-02-ITG |
| REQ-WKM-014 | The next action is visible on the case record and in every queue view | Business Requirements Epic 2, section 4 | FEAT-WKM-08 | 06 Take over and own the case | None | None (out of scope, section 19) |

The two requirements the legacy story tabulates keep their legacy BRD section and rule text. The three it does not tabulate keep the feature and rule text the legacy story gives them; REQ-WKM-014 is traced for completeness only and is out of scope for this story.

### 19. Out of scope

- The two owning I stories: RWB-P3-E2016-APP (the timeline, the filters, the paging, the queue history and the merge) and RWB-P5-E2016-APP (the document metadata), and every screen, endpoint, table and rule they build.
- Production code in any service: the harness is test and evidence only.
- The contract baselines of rwb-case, rwb-decision, rwb-document, rwb-comms and rwb-access, which their CON stories own.
- Platform deployment, the gateway-bff composite route implementation (RWB-PLT-N001-CON) and the platform configuration of Kafka, Temporal and the observability stack.
- The next action on the case and in every queue view (REQ-WKM-014, RWB-E2-035).
- The clocks and deviations panels (RWB-E2-015).
- The decision log query screen for audit (SCR-38, P7).
- The accounts, parties and collateral sections of the record view (RWB-E1-023, FEAT-ACA-12).
