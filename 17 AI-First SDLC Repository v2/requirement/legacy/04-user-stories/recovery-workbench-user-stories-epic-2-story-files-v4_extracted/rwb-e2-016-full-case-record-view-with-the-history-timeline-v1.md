<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 016 Full case record view with the history timeline v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 016 Full case record view with the history timeline v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-016 Full case record view with the history timeline

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-016 |
| Epic | E2, release 31 December 2026 |
| Module | P3 Case and workflow, with P7 Decision center and log |
| Feature | FEAT-WKM-08 Show the full case record view with the history timeline; FEAT-WKM-09 Show queue history on the case |
| Requirement IDs | REQ-WKM-008, REQ-OCC-008 |
| BRD section | Business Requirements Epic 2, sections 3.3 and 4; Business Requirements Program, section 5.3 |
| L3 process | 06 Take over and own the case; All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-035, RWB-E2-015, RWB-E2-012 |
| Status | Ready for build |

## 1. Story

As a **case owner (RW-CASEOWN)**, I want **the case record view to show every action, decision, transfer, letter and document on one timeline with filters, and the queue history with the reason for each move**, so that **I read the whole case in one place**.

## 2. Business rationale

A case lives for months or years and passes through several teams, partners and courts. Today a new owner reads email threads and spreadsheets to learn what happened. This story puts the decision log entries, assignments and transfers, contacts, notices, documents and timer events of a case on one timeline, filtered by type and date, with a queue history that shows every queue and owner and the reason for each move. It meets REQ-WKM-008. The measure is that a case history with 30 events reads in under 2 seconds (NFR-009) and stays under 2 seconds at the 2031 data size (NFR-070).

## 3. Preconditions

- RWB-E1-035 is done: the timeline v1.1 on SCR-03 shows contacts, documents, assignments, transfers and status changes.
- RWB-E2-015 is done: the clocks and deviations panels on SCR-03.
- RWB-E2-012 is done: each assignment carries its queue and its transfer reason code.
- P7 publishes `DecisionLogQuery.forCase(...)`; P5 publishes `DocumentQuery.forCase(...)`; P6 publishes `NoticeQuery.forCase(...)`.
- The person holds a role with Case record R and the case is in scope. Decision, document and notice items need Decision log R, Documents R and Litigation R.

## 4. Flow

1. Case owner: opens SCR-04 Case timeline from SCR-03 Case record.
2. Front end: calls `GET /cases/{caseId}/timeline` with the filters kept for the session.
3. Timeline service: checks the scope and the caller's rights in Decision log, Documents and Litigation.
4. Timeline service: reads assignments, interactions and timer events from the P3 tables, and in parallel calls the P7, P5 and P6 interfaces for the sources the caller may read, each with a 2 second timeout.
5. Timeline service: maps each record to a timeline item with time, type, summary, actor and reference, merges them newest first and returns one page.
6. Front end: shows the timeline in state Loading, then the list; the filter by type and date reloads it in state Filtered.
7. Case owner: opens Queue history; the front end calls the timeline with type ASSIGNMENT and TRANSFER and shows from queue, to queue, from owner, to owner, reason code and rule ID for each move.
8. Case owner: opens a decision item; the front end opens the entry through `GET /decision-log/{entryId}` (P7).

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A source module does not answer within 2 seconds | The other items show; a notice names the missing source | MSG-GEN-006 | AC6 |
| X2 | The caller lacks Decision log R, Documents R or Litigation R | Those item types are left out without an error | None | AC5 |
| X3 | Date from is after date to | Refused | MSG-GEN-003 | AC7 |
| X4 | No item matches the filter | Empty sentence | MSG-P3-019 | AC8 |
| X5 | An assignment written before RWB-E2-012 has no queue | The move shows with "Queue not recorded" | None | AC9 |
| X6 | The case is outside the caller's scope | Not found | MSG-P4-003 | AC10 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads what other stories write; needs the queue on the assignment from RWB-E2-012 |
| Negotiable | Item wording and filter layout can change; the sources and the rights are fixed |
| Valuable | A new owner reads the case without asking the previous one |
| Estimable | One endpoint, one merge service, three interface calls, one screen |
| Small | Fits in one sprint with its tests |
| Testable | API tests with seeded P3 rows and stubbed interfaces; one load test |

## 7. Acceptance criteria

```gherkin
Feature: Full case record view with the history timeline

  Background:
    Given the business date is 2026-12-20
    Given user "U-CO-01" holds RW-CASEOWN and owns case "RW-2026-000601"

  Scenario: AC1 Timeline
    Given case "RW-2026-000601" has 30 events: 4 assignments, 3 transfers, 8 contacts, 6 decision log entries, 2 notices, 5 documents and 2 timer events
    When "U-CO-01" opens the case timeline
    Then the 30 items show newest first, each with type, actor and time
    Then the first page loads within 2 seconds at the 95th percentile over 20 runs

  Scenario: AC2 Filter
    Given the filter set to "DECISION"
    When the timeline refreshes
    Then only the 6 decision items show
    Then each carries its decision log entry ID and opens that entry

  Scenario: AC3 Queue history
    Given case "RW-2026-000601" was allocated to "MTG-BKK-CO" on 2026-11-30 and transferred three times: to "LIT-BKK-01" with reason "R05" on 2026-12-05, to "MTG-BKK-CO" with reason "R06" on 2026-12-08 and to "LIT-BKK-02" with reason "R01" on 2026-12-12
    When "U-CO-01" opens queue history
    Then the three moves show newest first with from queue, to queue, from owner, to owner, reason code and rule ID
    Then the allocation on 2026-11-30 shows as the first entry with reason "ALLOCATION"

  Scenario: AC4 Date filter
    Given the filter from 2026-12-05 to 2026-12-08
    When the timeline refreshes
    Then only items dated 2026-12-05 to 2026-12-08 inclusive show

  Scenario: AC5 Items the role may not read
    Given user "U-PC-01" holds RW-PHONECOL with case "RW-2026-000601" in scope
    When "U-PC-01" opens the case timeline
    Then no decision item and no notice item shows
    Then contacts, assignments, transfers, documents and timer events show

  Scenario: AC6 A source does not answer
    Given the document query does not answer within 2 seconds
    When "U-CO-01" opens the case timeline
    Then the 25 items from the other sources show
    Then a notice shows MSG-GEN-006 naming "Document hub"

  Scenario: AC7 Dates in the wrong order
    When "U-CO-01" sets the filter from 2026-12-10 to 2026-12-01
    Then the system refuses the request with MSG-GEN-003 naming "to" and "from"

  Scenario: AC8 Nothing matches
    Given the filter set to "NOTICE" and the dates 2026-11-01 to 2026-11-15
    When the timeline refreshes
    Then the screen shows MSG-P3-019

  Scenario: AC9 Assignment written before the queue was recorded
    Given case "RW-2026-000602" has an assignment from 2026-11-30 with no queue recorded
    When "U-CO-01" opens its queue history
    Then the move shows with "Queue not recorded" and its reason "ALLOCATION"

  Scenario: AC10 Case outside scope
    Given case "RW-2026-000603" belongs to team "SME-NTH" and "U-CO-01" has scope Own in team "MTG-BKK"
    When "U-CO-01" opens its timeline
    Then the system does not find the response with MSG-P4-003

  Scenario: AC11 Large history
    Given case "RW-2026-000604" has 4,000 timeline items
    When "U-CO-01" opens the case timeline with page size 50
    Then the first 50 items show within 2 seconds
    Then the total shows 4,000
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The timeline holds every assignment, transfer, contact, decision log entry, notice, document and timer event of the case | REQ-WKM-008; casemodel.txt Case file |
| BR2 | Items are ordered newest first; items at the same time keep the order of their sources' sequence | events.txt Rules (ordering) |
| BR3 | A decision item shows only to a role with Decision log R, a document item only with Documents R, a notice item only with Litigation R | roles.txt Permissions; CTL-09 |
| BR4 | Queue history shows each assignment with its from and to queue, from and to owner, reason, reason code and rule ID | REQ-WKM-008; REQ-CWC-016 |
| BR5 | A decision item links to its decision log entry, which is never changed; a correction shows as a further entry | R-UNI-24; REQ-DRI-002 |
| BR6 | Personal data in a contact summary is masked by role | CTL-11; DL26 |
| BR7 | A source that does not answer in time does not stop the timeline | NFR-008 |

## 9. State transitions

None. This story does not change a case status. It reads records only.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Reads the timeline and queue history (Case record R; Decision log R; Documents R; Litigation R) |
| RW-TEAMMGR, team manager | Reads the timeline and queue history (Case record R; Decision log R) |
| RW-PHONECOL, phone collector | Reads the timeline without decisions and notices (Case record R; Documents R) |
| RW-CONDUCT, conduct and QA officer | Reads every item (R in all areas) |
| RW-AUDIT, internal audit | Reads every item (R in all areas); changes nothing |

## 11. Data

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
| DF-INT-011 | interaction | summary | Read, masked by role |
| DF-WRK-030 | timer | timer_type | Read |
| DF-WRK-031 | timer | started_at | Read |
| DF-WRK-035 | timer | status | Read |
| DF-DEC-001 | decision_log_entry | id | Read, through the P7 interface |
| DF-DEC-003 | decision_log_entry | decision_code | Read, through the P7 interface |
| DF-DEC-004 | decision_log_entry | rule_id | Read, through the P7 interface |
| DF-DEC-012 | decision_log_entry | final_call | Read, through the P7 interface |
| DF-DEC-016 | decision_log_entry | decided_at | Read, through the P7 interface |
| DF-DOC-001 | document | id | Read, through the P5 interface |
| DF-DOC-004 | document | document_type | Read, through the P5 interface |
| DF-DOC-005 | document | source | Read, through the P5 interface |
| DF-LEG-015 | notice | id | Read, through the P6 interface |
| DF-LEG-018 | notice | notice_type | Read, through the P6 interface |
| DF-LEG-019 | notice | sent_date | Read, through the P6 interface |
| DF-LEG-022 | notice | delivery_status | Read, through the P6 interface |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**GET /cases/{caseId}/timeline** (P3)

| Item | Value |
|---|---|
| Request | Path `caseId`; query `type` (comma separated: DECISION, ASSIGNMENT, TRANSFER, INTERACTION, NOTICE, DOCUMENT, TIMER), `from` (date), `to` (date), `page` (new, default 0), `size` (new, default 50, 1 to 200) |
| Response | 200 `TimelinePage`: `items[]` of `TimelineItem` (`at`, `type`, `summary`, `by`, `reference`, and the new `reasonCode`, `fromQueueCode`, `toQueueCode`, `ruleId`), `page`, `size`, `total`, and the new `unavailableSources[]` |
| Errors | 401 (MSG-P4-001); 403 no Case record R (MSG-P4-002); 404 unknown or out of scope (MSG-P4-003); 422 `to` before `from` (MSG-GEN-003) or size outside 1 to 200 (MSG-GEN-002); 503 |
| Authorization | Case record, right R, scope applied; item types filtered by Decision log R, Documents R and Litigation R |
| Idempotency | Not applicable |

**GET /api/recovery/v1/decision-log/{entryId}** (P7) opens a decision item (Decision log R).

**Published interfaces used**

```java
// P7
List<DecisionSummary> DecisionLogQuery.forCase(UUID caseId, Instant from, Instant to);
// P5
List<DocumentSummary> DocumentQuery.forCase(UUID caseId, Instant from, Instant to);
// P6
List<NoticeSummary> NoticeQuery.forCase(UUID caseId, Instant from, Instant to);
```

Each call runs in parallel with a 2 second timeout. No events are published.

## 13. Solution plan

**Package.** `recovery.casewf.timeline` in the recovery module; front end folder `src/modules/recovery/casewf/timeline`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TimelineService | Service | Checks rights, calls the sources in parallel, merges, sorts, pages |
| TimelineItemMapper | Service | Maps assignments, interactions, timers, decisions, documents and notices to `TimelineItem`, with summaries built from codes |
| AssignmentHistoryRepository | Repository | Reads assignments with their queue codes for a case |
| InteractionRepository | Repository | Reads the case's interactions in the date range |
| CaseAndWorkflowController | Controller | The timeline endpoint and its parameter checks |
| CaseTimelinePage | React component | SCR-04 with Loading and Filtered states, type and date filters, the source notice |
| QueueHistoryTab | React component | The queue history view on SCR-04 |

**Database.** Reads `assignment`, `interaction`, `timer` and `queue`. Uses `ix_assignment_case_id`, `ix_interaction_case_time` and `ix_timer_case_id`. No new table.

**Configuration and reference data.** `timeline.source-timeout-ms` = 2000 and the page size limits in the configuration service. Type labels and reason code labels from LOV-ASSIGN-REASON and LOV-TRANSFER-REASON through the P4 list interface. Masking rules (Compliance, DL26).

**Build steps**

1. Build the two repositories and `TimelineItemMapper` for P3 records; unit test each item type.
2. Build `TimelineService` with the rights filter, parallel calls, timeouts and `unavailableSources`.
3. Add paging, the type and date filters and the new item fields to the endpoint.
4. Build `CaseTimelinePage` with filters kept in session storage and `QueueHistoryTab`.
5. Add the masking call for contact summaries through the ACE common module.
6. Write the tests in section 16, including the 4,000 item load test.

**Feature flag.** `rwb.p3.full-timeline`. Off: SCR-03 shows the RWB-E1-035 timeline.

**Done when.** The tests in section 16 pass, and the query plan for the 4,000 item case uses the case indexes only.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-019 | No item matches the filter | Nothing on this case matches the filter. |
| MSG-GEN-006 | A source module does not answer in time | {system} is not available. Your request is queued and will be retried. |
| MSG-GEN-003 | Date to is before date from | {field} cannot be before {other}. |
| MSG-GEN-002 | Page size outside 1 to 200 | {field} must be between {min} and {max}. |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. |
| MSG-P4-002 | A role without Case record R opens the timeline | You cannot {action} here. Your role does not include it. |

MSG-P3-019 is new (see Additions). Thai text follows DL10.

## 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-04 Case timeline | Loading | Sees skeleton rows |
| SCR-04 Case timeline | Filtered | Filters by type and date; opens a decision, a document or a notice; reads the queue history |
| SCR-03 Case record | Read only | Opens the timeline from the record |

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-016-01 | AC1, BR1, BR2 | System | 30 items over seven types; 20 timed runs |
| TC-E2-016-02 | AC2, BR5 | System | Filter DECISION over the AC1 case |
| TC-E2-016-03 | AC3, BR4 | System | One allocation and three transfers with reasons R05, R06, R01 |
| TC-E2-016-04 | AC4 | System | Date filter 2026-12-05 to 2026-12-08 |
| TC-E2-016-05 | AC5, BR3 | System | RW-PHONECOL on the AC1 case |
| TC-E2-016-06 | AC6, BR7 | System | Stubbed document query delayed 3 seconds |
| TC-E2-016-07 | AC7 | System | From 2026-12-10, to 2026-12-01 |
| TC-E2-016-08 | AC8 | System | NOTICE filter in November |
| TC-E2-016-09 | AC9 | System | Assignment with no queue |
| TC-E2-016-10 | AC10 | System | Case of team SME-NTH |
| TC-E2-016-11 | AC11 | System | 4,000 synthetic items, page size 50 |
| TC-E2-016-12 | Access | Access | RW-REFADM (no Case record right) calls the timeline; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code. Type lists, labels, timeouts and page sizes are data.
- No personal data in logs, tests or prompts. Summaries are built from codes; contact summaries are masked by role and never logged. Test data is synthetic.
- No read of another module's tables. Decisions, documents and notices come only through the P7, P5 and P6 interfaces.
- The timeline never writes; it does not copy other modules' records into P3 tables.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-008 | Queue and transfer history visible on the case | Business Requirements Epic 2, sections 3.3 and 4; Program, section 5.3 | FEAT-WKM-08, FEAT-WKM-09 | 06 Take over and own the case | R-UNI-24; CTL-09; CTL-11 | TC-E2-016-01 to TC-E2-016-12 |
| REQ-OCC-008 | History timeline of every state change, transfer, contact, document and decision | Business Requirements Epic 2, sections 3.3 and 4 | FEAT-WKM-08, FEAT-WKM-09 | 06 Take over and own the case; All recovery processes | None | TC-E2-016-01 |

## 19. Out of scope

- The next action on the case and in every queue view (REQ-WKM-014, RWB-E2-035).
- The clocks and deviations panels (RWB-E2-015).
- The decision log query screen for audit (SCR-38, P7).
- Accounts, parties and collateral sections of the record view (RWB-E1-023, P4 FEAT-ACA-12).
