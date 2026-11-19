# RWB-E1-035 Case record view v1.1 with documents and history timeline

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-035 |
| Epic | E1, release 30 November 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-ACA-12 Show the case record view with the history timeline |
| Requirement IDs | REQ-CWC-016, REQ-OCC-007 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 3.6; Business Requirements Program, sections 5.3 and 5.6 |
| L3 process | 06 Take over and own the case |
| Decision | None |
| Priority | Should |
| Depends on | RWB-E1-021, RWB-E1-023, RWB-E1-027 |
| Status | Ready for build |

## 1. Story

As a **case owner (RW-CASEOWN)**, I want **a timeline on the case record view with contacts, documents, assignments, transfers and status changes in time order, each with who or which rule caused it**, so that **I see what happened to the case without asking anyone**.

## 2. Business rationale

A case that changes owner today arrives with no history except what the last owner remembers. This story adds a timeline panel to SCR-03 that merges the interaction ledger, the documents, the assignments and the decision log entries for the case in time order, and shows the person or the rule and version behind each event, including the coded reason of a manual transfer. It meets REQ-CWC-016 (every workflow event carries its rule ID and version, now visible) and REQ-OCC-007 (contact history and documents on the case view).

## 3. Preconditions

- RWB-E1-023 is done: SCR-03 shows the read-only case record.
- RWB-E1-021 is done: transfers write assignments with a transfer reason and a decision log entry.
- RWB-E1-027 is done: decision log entries can be read by case through the P7 interface.
- The P5 document hub lists documents by case.
- The user holds Case record R and the case is in scope.

## 4. Flow

1. Case owner: opens SCR-03 for case RW-2026-000801 and selects the Timeline panel.
2. TimelinePanel: calls GET /cases/{caseId}/timeline with page 0 and size 50.
3. CaseAndWorkflowController: checks Case record R and the scope.
4. TimelineService: reads interactions and assignments from P3 tables, documents through the P5 interface and decision log entries through the P7 interface, for the case.
5. TimelineService: maps each record to a TimelineItem with time, type, summary, by and reference.
6. TimelineService: sorts by time, then by a fixed type order for equal times, then by record ID, and returns the page with the total.
7. TimelinePanel: shows each item with an icon for its type; "by" shows a person's name, or a rule ID with its version.
8. Case owner: opens a transfer item; the panel shows the transfer reason, the from and to queue and owner, and the rule version.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The decision log query does not answer | Other events show; the panel shows the section message | MSG-P3-023 | AC3 |
| X2 | The case has only its creation entry | One item "Case created" shows with the entry rule and version | None | AC4 |
| X3 | Two events have the same time | Fixed order by type, then record ID | None | AC5 |
| X4 | The case has more than 50 events | Paged by 50; the total shows | None | AC6 |
| X5 | The case is outside the user's scope | 404 | MSG-P4-003 | AC7 |
| X6 | A role without Case record R opens the timeline | Refused with 403 | MSG-P4-002 | Access test TC-E1-035-08 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads records that RWB-E1-018 to RWB-E1-028 write; adds one panel |
| Negotiable | The type order and icons are design choices |
| Valuable | A new owner sees the case history in one place |
| Estimable | One endpoint, one merge service, one panel |
| Small | Fits one week |
| Testable | Every criterion has a test case in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Case record view v1.1 with documents and history timeline

  Background:
    Given case owner U-81 owns case RW-2026-000801

  Scenario: AC1 Timeline order
    Given case RW-2026-000801 has a rule transfer at 2026-12-02 08:10 by row "TRF-007" version "TRF-2026.11"
    Given documents "Demand letter" stored at 2026-12-02 10:30 and "Title deed" at 2026-12-03 09:00
    Given a status change from "ASSIGNED" to "IN_PROGRESS" at 2026-12-03 11:15 by U-81
    When the timeline opens
    Then the four events show in the order transfer, demand letter, title deed, status change
    Then the transfer shows "TRF-007" with version "TRF-2026.11" and the status change shows U-81

  Scenario: AC2 Transfer reason
    Given a manual transfer at 2026-12-04 14:00 by team manager U-71 with transfer reason "R04"
    When the event is opened
    Then the reason "R04 Owner absent", the from owner, the to owner and the rule version "TRF-2026.11" are shown

  Scenario: AC3 Decision log unavailable
    Given the decision log query does not answer within 3 seconds
    When the timeline opens
    Then the interactions, documents and assignments show in time order
    Then the panel shows MSG-P3-023 for "Decisions"

  Scenario: AC4 A new case shows only its creation
    Given case RW-2026-000802 was created on 2026-12-02 and its only record is the creation entry in the decision log
    When the timeline opens
    Then one item shows with type "Case created", time 2026-12-02 and the entry rule version

  Scenario: AC5 Events at the same time
    Given an assignment and a decision log entry both at 2026-12-02 07:00:00
    When the timeline opens
    Then the decision log entry shows before the assignment, by the fixed type order
    Then the order is the same on every opening

  Scenario: AC6 More than 50 events
    Given case RW-2026-000803 has 132 events
    When the timeline opens
    Then the first page shows the 50 most recent events and total 132
    Then the third page shows 32 events

  Scenario: AC7 Case outside the scope
    Given case RW-2026-000804 belongs to team "LIT-BKK" and U-81 has scope Own
    When U-81 calls the timeline for RW-2026-000804
    Then the response is 404 with MSG-P4-003
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Events show in time order; equal times follow the type order decision, status change, assignment, transfer, contact, document, then record ID | FSD A2.45; FEAT-ACA-12 |
| BR2 | An event caused by a rule shows the rule ID and version; an event by a person shows the person | REQ-CWC-016 |
| BR3 | A manual transfer shows its transfer reason | REQ-WKM-003; RWB-E1-021 |
| BR4 | Only cases in the caller's scope open | CTL-09 |
| BR5 | Personal fields in a contact summary follow the masking rules | REQ-ACA-005; DL26 |
| BR6 | The timeline reads in under 2 seconds at the ledger's 2031 size | NFR-070 |

## 9. State transitions

None. This story does not change a case status. It reads the records of past changes.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN | Reads the timeline of own cases (Case record R) |
| RW-TEAMMGR | Reads the timeline of team cases |
| RW-CONDUCT, RW-AUDIT | Read the timeline of every case |
| RW-REFADM | No Case record right; refused |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-INT-002 | interaction | case_id | Read |
| DF-INT-004 | interaction | occurred_at | Read |
| DF-INT-005 | interaction | channel | Read |
| DF-INT-006 | interaction | direction | Read |
| DF-INT-008 | interaction | contact_result | Read |
| DF-INT-011 | interaction | summary | Read |
| DF-WRK-010 | assignment | case_id | Read |
| DF-WRK-012 | assignment | assignee_user_id | Read |
| DF-WRK-013 | assignment | assigned_at | Read |
| DF-WRK-014 | assignment | ended_at | Read |
| DF-WRK-015 | assignment | reason | Read |
| DF-WRK-016 | assignment | rule_id | Read |
| DF-WRK-040 | assignment | transfer_reason_code | Read |
| DF-DOC-001 | document | id | Read |
| DF-DOC-004 | document | document_type | Read |
| DF-DOC-005 | document | source | Read |
| DF-DEC-002 | decision_log_entry | case_id | Read |
| DF-DEC-003 | decision_log_entry | decision_code | Read |
| DF-DEC-004 | decision_log_entry | rule_id | Read |
| DF-DEC-005 | decision_log_entry | rule_version | Read |
| DF-DEC-010 | decision_log_entry | approver_user_id | Read |
| DF-DEC-012 | decision_log_entry | final_call | Read |
| DF-DEC-016 | decision_log_entry | decided_at | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**GET /api/recovery/v1/cases/{caseId}/timeline**

| Item | Value |
|---|---|
| Request | Path caseId (uuid); query type, from, to; page and size (new query parameters, see additions) |
| Response | TimelinePage of TimelineItem: at, type, summary, by, reference, and the new fields reasonCode, fromQueueCode, toQueueCode and ruleId (recorded with RWB-E2-016) |
| Errors | 401 (MSG-P4-001); 403 no Case record R (MSG-P4-002); 404 not found or out of scope (MSG-P4-003); 503 P3 store unavailable |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

The endpoint is first listed for E2 in api.yaml; this story delivers it in E1 behind the flag.

**Published interfaces used**

```java
// P7 (RWB-E1-027)
public interface DecisionLogQuery {
    List<DecisionLogSummary> entriesForCase(UUID caseId, Instant from, Instant to);
}
// P5 (RWB-E1-024)
public interface DocumentQuery {
    List<DocumentSummary> documentsForCase(UUID caseId);
}
```

## 13. Solution plan

**Package.** Back end `recovery/casewf/timeline` (Java package `recovery.casewf.timeline`); front end `src/modules/recovery/casewf/caserecord/timeline`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseAndWorkflowController | Controller | GET /cases/{caseId}/timeline |
| TimelineService | Service | Reads four sources, maps to TimelineItem, sorts by BR1, pages |
| TimelineItemMapper | Service | One mapper per source; rule ID and version or person in "by" |
| CaseAndWorkflowRepository | Repository | interaction and assignment by case (ix_interaction_case_time, ix_assignment_case_id) |
| TimelinePanel | React component | Panel on SCR-03 with paging, item detail and section messages |

**Database**

- Reads interaction and assignment only; no migration.

**Configuration and reference data**

- Type order list held as parameter `timeline.type.order` (RWB-E1-042).
- LOV-TRANSFER-REASON labels (RWB-E1-021), LOV-DOC-TYPE, LOV-CHANNEL.
- Parameter `caserecord.section.timeout.ms` = 3000 (assumed; DL11).

**Build steps**

1. Mappers for interaction, assignment, document and decision log entry; unit tests.
2. Merge and sort with the type order and record ID tie break; tests AC1, AC5.
3. Paging with total; test AC6.
4. Source timeout and partial result with the section message; test AC3.
5. Scope check; test AC7; a case with only its creation entry; test AC4.
6. TimelinePanel with item detail for transfers; test AC2.
7. Access test.

**Feature flag.** `rwb.p3.timeline`. Off: SCR-03 hides the Timeline panel and the endpoint returns 404.

**Done when.** The tests in section 16 pass and the timeline of a case with 500 events reads in under 2 seconds in SIT (NFR-070).

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-023 | One source does not answer | {section} cannot be shown now. The rest of the case is shown. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the scope | This case is not in your scope. |

## 15. Screens and states

SCR-03 Case record gains the Timeline panel. Loading: skeleton rows. Read only: items in time order with type, summary, by and time; a new case shows its creation item. Error: MSG-P3-023 for the missing source. The full timeline screen with filters, SCR-04, comes in Epic 2 (RWB-E2-016).

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-035-01 | AC1, BR1, BR2 | System | Transfer, two documents and a status change |
| TC-E1-035-02 | AC2, BR3 | System | Manual transfer with R04 |
| TC-E1-035-03 | AC3 | System | Decision log query timing out |
| TC-E1-035-04 | AC4 | System | Case with only its creation entry |
| TC-E1-035-05 | AC5, BR1 | System | Two records at 07:00:00 |
| TC-E1-035-06 | AC6 | System | 132 events |
| TC-E1-035-07 | AC7, BR4 | System | Case of another team |
| TC-E1-035-08 | Access | Access | RW-REFADM calls GET /cases/{caseId}/timeline and is refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the type order and labels are data.
- No personal data in logs, tests or prompts; contact summaries follow masking by role.
- No read of another module's tables: documents through DocumentQuery (P5), decisions through DecisionLogQuery (P7).
- The timeline never writes; it shows records as they were written.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-016 | Every workflow event with its rule ID and version | Epic 1, 3.3; Program, 5.3 | FEAT-ACA-12 | 06 Take over and own the case | None | TC-E1-035-01, TC-E1-035-02, TC-E1-035-05 |
| REQ-OCC-007 | Contact history and documents on the case view | Epic 1, 3.6; Program, 5.6 | FEAT-ACA-12 | 06 Take over and own the case | None | TC-E1-035-03, TC-E1-035-04, TC-E1-035-06, TC-E1-035-07 |

## 19. Out of scope

- The full timeline screen with filters and queue history (RWB-E2-016).
- The full case record view with collateral, decisions and timers (Epic 2, FEAT-WKM-08).
- Communications and notices on the timeline (Epic 2, P6).
