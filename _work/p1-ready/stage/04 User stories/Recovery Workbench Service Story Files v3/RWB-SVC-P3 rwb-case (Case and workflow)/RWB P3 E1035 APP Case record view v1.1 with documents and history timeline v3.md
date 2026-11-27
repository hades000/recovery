# RWB-P3-E1035-APP Case record view v1.1 with documents and history timeline

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- D-RCV-60 finishing pass: RD-P1-004.

| Item | Value |
|---|---|
| Story key | RWB-P3-E1035-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Size | Not specified in the source documents (DOR-RWB-P3-E1035-APP-16) |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-035 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP11, DP13, DP14, DP15, DP18, DP19 |
| Parallel lane | L-P3-F |
| Ready to start | After RWB-P3-E1023-APP (not done yet; build dependency still open) |
| Depends on (build) | RWB-P3-E1035-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P3-E1023-APP, RWB-P3-E1021-CON |
| Contract dependencies | RWB-P7-E1027-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-012, FR-P3-013, FR-P3-019, FR-P3-020, FR-P3-021, FR-P3-030, FR-P3-031) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-004 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-035 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P3-E1035-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 10 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **a timeline on the case record view with contacts, documents, assignments, transfers and status changes in time order, each with who or which rule caused it**, so that **I see what happened to the case without asking anyone**.

In the target the panel is one operation of rwb-case, `GET /api/recovery/case/v1/cases/{caseId}/timeline`, served to SCR-03 as the gateway-bff composite route of RWB-PLT-N001-CON (DP-19). It merges four sources one hop each, never a table read: the assignments, transfers and case state of schema `rwb_case` (DP-01); the decision records of the case through the rwb-decision decision-record query (DP-03, C RWB-P7-E1027-CON); the contact ledger through the interaction read owned by rwb-source-data (DP-18); the documents through rwb-document (DP-11). This story delivers the full four-source timeline, the transfer item detail, the paged total, the fixed type order and the per-section degradation; the read-only case header and the contact history behind the same screen are RWB-P3-E1023-APP.

The type order, the section timeout and every label are data read through the parameters and reference-data contracts of rwb-case (DP-06, DP-07); no business value sits in code. The right and the scope are checked by the authorise guard that the service template provides and RWB-P3-E1023-APP wires (ASM-3637), so this story adds no access decoupling row.

### 2. Business rationale

A case that changes owner today arrives with no history except what the last owner remembers. The legacy story added a timeline panel to SCR-03 that merged the interaction ledger, the documents, the assignments and the decision log entries in time order and showed the person or the rule and version behind each event, including the coded reason of a manual transfer. It met REQ-CWC-016 (every workflow event carries its rule ID and version, now visible) and REQ-OCC-007 (contact history and documents on the case view).

The split changes where each record comes from, not what the case owner sees. The interaction ledger now belongs to rwb-source-data, the decision record is written locally and sealed in the ledger of rwb-decision, the documents belong to rwb-document, and rwb-case keeps only what it owns: the case, its assignments and its queue. The panel therefore becomes one contract operation with three mocked calls behind it, and the timeline reads in under 2 seconds against a ledger at its 2031 size (NFR-070, BR6).

### 3. Preconditions

- RWB-P3-E1023-APP is done: SCR-03 shows the read-only case record; the timeline operation is published with its page and size parameters and the panel mounts behind the flag.
- RWB-P3-E1035-CON is done: the v1.1 timeline item shape, the partial-result envelope and its fakes, through which this story builds.
- RWB-P3-E1021-CON is done: the transfer rules write `assignment.transfer_reason_code`, `assignment.rule_id` and the closed assignment row this story reads.
- RWB-P3-E1023-APP already applies the authorise guard of the service template: Case record R and the scope are checked by it, and this story adds no access decoupling row (ASM-3637).
- C RWB-P7-E1027-CON is published with its fake: the decision-record query by case. Its path, its time filter and its field list are Not specified in the source documents (GAP-2210; ASM-3635).
- The rwb-document documents-by-case operation is published with its fake, and rwb-source-data publishes the interaction read the ledger part needs. The path and the paging of the interaction read are Not specified in the source documents (GAP-0695; ASM-1242).
- RWB-PLT-E1042-CON and RWB-P3-E1042-CON (parameters), RWB-PLT-E1043-CON and RWB-P3-E1043-CON (reference data), RWB-PLT-E1047-CON (event and topic naming), RWB-PLT-E1044-CON (Flyway sequence), RWB-PLT-E1027-CON (decision record) and RWB-PLT-N001-CON (gateway-bff composite route) are done.
- The rwb-case login (DP-02) holds SELECT on schema `rwb_case` and no privilege on another schema. The login name is Not specified in the source documents (GAP-0692; ASM-1239).
- The user holds a role with Case record R and the case is in the user's scope.

### 4. Flow

1. Case owner: opens SCR-03 for case RW-2026-000801 and selects the Timeline panel.
2. gateway-bff: checks the session in Redis, takes the short-lived JWT through ACE Common sign-in and checks the coarse permission, then calls rwb-case.
3. rwb-case TimelineController: checks Case record R and the scope through the authorise guard; a case outside the scope returns 404 and never 403.
4. rwb-case TimelineQueryService: calls, in parallel and one hop each, the assignment read in `rwb_case`, the rwb-decision decision-record query, the rwb-source-data interaction read and the rwb-document documents-by-case operation; each has a 2 s budget and a GET retry once with jitter.
5. rwb-case TimelineMapper: maps every record to a TimelineItem with at, type, summary, by, reference and, for a transfer, reasonCode, fromQueueCode, toQueueCode and ruleId; "by" holds the person, or the rule ID with its version.
6. rwb-case TimelineQueryService: sorts by time, then by the type order of parameter `timeline.type.order`, then by record ID, and returns the page with the total of the merged set.
7. rwb-case SectionGuard: a source that fails or exceeds its budget sets that section to a failed state with MSG-P3-023 and leaves the other items in the page; the response stays 200.
8. TimelinePanel: shows each item with an icon for its type and the time; a new case shows one "Case created" item with the entry rule version.
9. Case owner: opens a transfer item; the panel shows the reason label, the from and to queue and owner, and the rule version.
10. TimelinePanel: pages by 50 with the total, and shows MSG-P3-023 in place of the section that failed.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The decision-record query does not answer | The other items show; the panel shows the section message for "Decisions" | MSG-P3-023 | AC3 |
| X2 | The case has only its creation record | One item "Case created" shows with the entry rule and version | None | AC4 |
| X3 | Two events have the same time | Fixed order by type, then record ID; the order is stable on every opening | None | AC5 |
| X4 | The case has more than 50 events | Paged by the page-size parameter; the total of the merged set shows | None | AC6 |
| X5 | The case is outside the user's scope | 404; no item shows | MSG-P4-003 | AC7 |
| X6 | A role without Case record R opens the timeline | Refused with 403 | MSG-P4-002 | AC8; Access test TC-E1-035-08 |
| X7 | The document hub does not answer | The items show without documents; the section message names "Documents" | MSG-P3-023 | AC3 pattern |
| X8 | The interaction read does not answer | The items show without contacts; the section message names "Contacts" | MSG-P3-023 | AC3 pattern |
| X9 | A transfer record has no closed previous assignment | The from queue and the from owner show as empty; the item and its reason still show | None | AC2 pattern |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads records that RWB-P3-E1018 to RWB-P3-E1028 write; adds one operation and one panel |
| Negotiable | The type order, the icons and the item layout are data and design choices |
| Valuable | A new owner sees the case history in one place, with who or which rule caused each event |
| Estimable | One operation, one merge service, three contract clients, one panel |
| Small | Fits two weeks (DOR-RWB-P3-E1035-APP-15) |
| Testable | Every criterion has a test case in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Case record view v1.1 with documents and history timeline

  Background:
    Given case owner U-81 owns case RW-2026-000801

  Scenario: AC1 Timeline order (legacy RWB-E1-035 AC1)
    Given case RW-2026-000801 has a rule transfer at 2026-12-02 08:10 by row "TRF-007" version "TRF-2026.11"
    Given documents "Demand letter" stored at 2026-12-02 10:30 and "Title deed" at 2026-12-03 09:00
    Given a status change from "ASSIGNED" to "IN_PROGRESS" at 2026-12-03 11:15 by U-81
    Given the rwb-decision contract mock returns the transfer decision record at 2026-12-02 08:10 with rule "TRF-007" and version "TRF-2026.11"
    Given the rwb-document contract mock returns "Demand letter" stored at 2026-12-02 10:30 and "Title deed" at 2026-12-03 09:00
    When the timeline opens
    Then the four events show in the order transfer, demand letter, title deed, status change
    Then the transfer shows "TRF-007" with version "TRF-2026.11" and the status change shows U-81

  Scenario: AC2 Transfer reason (legacy RWB-E1-035 AC2)
    Given a manual transfer at 2026-12-04 14:00 by team manager U-71 with transfer reason "R04"
    Given the rwb-decision contract mock returns the transfer decision record at 2026-12-04 14:00 by U-71 with version "TRF-2026.11"
    When the event is opened
    Then the reason "R04 Owner absent", the from owner, the to owner and the rule version "TRF-2026.11" are shown

  Scenario: AC3 Decision log unavailable (legacy RWB-E1-035 AC3)
    Given the decision log query does not answer within 3 seconds
    Given the rwb-decision contract mock times out on every decision-record query
    When the timeline opens
    Then the interactions, documents and assignments show in time order
    Then the panel shows MSG-P3-023 for "Decisions"

  Scenario: AC4 A new case shows only its creation (legacy RWB-E1-035 AC4)
    Given case RW-2026-000802 was created on 2026-12-02 and its only record is the creation entry in the decision log
    Given the rwb-decision contract mock returns one creation record for case RW-2026-000802 dated 2026-12-02 with its entry rule version
    When the timeline opens
    Then one item shows with type "Case created", time 2026-12-02 and the entry rule version

  Scenario: AC5 Events at the same time (legacy RWB-E1-035 AC5)
    Given an assignment and a decision log entry both at 2026-12-02 07:00:00
    Given the rwb-decision contract mock returns the decision record at 2026-12-02 07:00:00
    When the timeline opens
    Then the decision log entry shows before the assignment, by the fixed type order
    Then the order is the same on every opening

  Scenario: AC6 More than 50 events (legacy RWB-E1-035 AC6)
    Given case RW-2026-000803 has 132 events
    Given the rwb-decision and rwb-document contract mocks answer for case RW-2026-000803
    When the timeline opens
    Then the first page shows the 50 most recent events and total 132
    Then the third page shows 32 events

  Scenario: AC7 Case outside the scope (legacy RWB-E1-035 AC7)
    Given case RW-2026-000804 belongs to team "LIT-BKK" and U-81 has scope Own
    Given the rwb-access contract mock returns scope Own for U-81
    When U-81 calls the timeline for RW-2026-000804
    Then the response is 404 with MSG-P4-003

  Scenario: AC8 A role without Case record R is refused (new, D-RCV-60)
    Given a user whose role does not include Case record R
    When the user opens the timeline for case RW-2026-000801
    Then the response is 403 with MSG-P4-002

  Scenario: AC9 One failed document source degrades only the documents section (new, D-RCV-60)
    Given the rwb-document contract mock times out on every document query
    When the timeline opens
    Then the response is 200 with the interactions and decisions in time order
    Then the panel shows MSG-P3-023 for "Documents"

  Scenario: AC10 A call without a valid session is refused with 401 and a call without the right with 403 (new, D-RCV-60)
    Given a call to the timeline of case RW-2026-000801 without a valid session
    When the timeline is called
    Then the response is 401
    Given a call to the timeline of case RW-2026-000801 by a user whose role does not include Case record R
    When the timeline is called
    Then the response is 403
```

All seven legacy criteria are owned here and copied unchanged, each with its origin tag; the added Given lines name the contract mock that stands in for the two sources rwb-case no longer reads itself: the decision records of rwb-decision and the documents of rwb-document. The ledger rows likewise arrive through the rwb-source-data contract (DP-18). No value in a legacy line is changed.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Events show in time order; equal times follow the type order decision, status change, assignment, transfer, contact, document, then record ID | FSD A2.45; FEAT-ACA-12 |
| BR2 | An event caused by a rule shows the rule ID and version; an event by a person shows the person | REQ-CWC-016 |
| BR3 | A manual transfer shows its transfer reason | REQ-WKM-003; RWB-E1-021 |
| BR4 | Only cases in the caller's scope open | CTL-09 |
| BR5 | Personal fields in a contact summary follow the masking rules | REQ-ACA-005; DL26 |
| BR6 | The timeline reads in under 2 seconds at the ledger's 2031 size | NFR-070 |
| BR7 | The type order and the section timeout are parameters, never constants in code; the values in force are read on every request through the parameters contract | DP-06; legacy §13 |
| BR8 | A transfer item takes its to-queue from `assignment.queue_id` and its from-queue and from-owner from the closed previous assignment row of the same case; its rule version comes from the decision record of the transfer, never from a column | TSD P3 v3 assignment (DF-WRK-013, DF-WRK-016, DF-WRK-039, DF-WRK-040); ASM-3633 |
| BR9 | A case state change and the creation item are read as the decision records of the case; rwb-case adds no status-history table and keeps no second copy of the history | ASM-3632; GAP-2210 |
| BR10 | One failed source degrades one section and never the page: the response stays 200 with the section state, and the MSG-P3-023 text names the section | §5 X1, X7, X8; MSG-P3-023 |
| BR11 | The panel reads only what the caller may see: the scope filter is applied before the merge, and an out-of-scope case is 404 with no item | CTL-09; REQ-ACA-009 |

### 9. State transitions

None. This story does not change a case status. It reads the records of past changes: the assignment rows of `rwb_case` and the decision records of the case. The events that move a case are published by other rwb-case stories on topic `rwb.case.events.v1`; this story publishes and consumes none of them.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN | Reads the timeline of own cases (Case record R) |
| RW-TEAMMGR | Reads the timeline of team cases |
| RW-CONDUCT, RW-AUDIT | Read the timeline of every case |
| RW-REFADM | No Case record right; refused with MSG-P4-002 |
| The rwb-case login (DP-02) | Reads schema `rwb_case` only. The login name is Not specified in the source documents (GAP-0692; ASM-1239) |
| rwb-decision | Owns the decision records and the central ledger; answers the decision-record query |
| rwb-source-data | Owns the interaction ledger; answers the interaction read |
| rwb-document | Owns the documents; answers the documents-by-case operation |
| rwb-access | Owns the roles, the scope and the masking policy; answers the authorise and masking calls through the guard |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-WRK-009 | assignment | id | Read |
| DF-WRK-010 | assignment | case_id | Read |
| DF-WRK-012 | assignment | assignee_user_id | Read |
| DF-WRK-013 | assignment | assigned_at | Read |
| DF-WRK-014 | assignment | ended_at | Read |
| DF-WRK-015 | assignment | reason | Read |
| DF-WRK-016 | assignment | rule_id | Read |
| DF-WRK-039 | assignment | queue_id | Read |
| DF-WRK-040 | assignment | transfer_reason_code | Read |
| DF-INT-002 | interaction | case_id | Read through the rwb-source-data interaction read (DP-18) |
| DF-INT-004 | interaction | occurred_at | Read through the rwb-source-data interaction read (DP-18) |
| DF-INT-005 | interaction | channel | Read through the rwb-source-data interaction read (DP-18) |
| DF-INT-006 | interaction | direction | Read through the rwb-source-data interaction read (DP-18) |
| DF-INT-008 | interaction | contact_result | Read through the rwb-source-data interaction read (DP-18) |
| DF-INT-011 | interaction | summary | Read through the rwb-source-data interaction read (DP-18) |
| DF-DOC-001 | document | id | Read through the rwb-document contract |
| DF-DOC-004 | document | document_type | Read through the rwb-document contract |
| DF-DOC-005 | document | source | Read through the rwb-document contract |
| DF-DEC-002 | decision record | case_id | Read through the rwb-decision decision-record query (C RWB-P7-E1027-CON) |
| DF-DEC-003 | decision record | decision_code | Read through the rwb-decision decision-record query (C RWB-P7-E1027-CON) |
| DF-DEC-004 | decision record | rule_id | Read through the rwb-decision decision-record query (C RWB-P7-E1027-CON) |
| DF-DEC-005 | decision record | rule_version | Read through the rwb-decision decision-record query (C RWB-P7-E1027-CON) |
| DF-DEC-010 | decision record | approver_user_id | Read through the rwb-decision decision-record query (C RWB-P7-E1027-CON) |
| DF-DEC-012 | decision record | final_call | Read through the rwb-decision decision-record query (C RWB-P7-E1027-CON) |
| DF-DEC-016 | decision record | decided_at | Read through the rwb-decision decision-record query (C RWB-P7-E1027-CON) |

Field IDs are those in the Logical Data Model and Data Dictionary v9. No field in this story is written, and no copy of a source record is stored: the ledger, the document list and the decision records are read through their owners' contracts on every request (DP-01, DP-18).

### 12. Contract

#### 12.1 REST operations provided

| Operation | Purpose | Owner | Read or write |
|---|---|---|---|
| GET /api/recovery/case/v1/cases/{caseId}/timeline | The paged case timeline: decision records, assignments and transfers, contacts from the ledger and documents, ordered by BR1, with the item detail of a transfer and the state of each section | rwb-case (P3) | Read |

This is the v1.1 behaviour of the operation first published by RWB-P3-E1023-CON: the path, the query parameters `type`, `from`, `to`, `page` and `size` and the status codes are unchanged, and the item gains the detail fields and the section state (ASM-3636). The panel is served to SCR-03 as the gateway-bff composite route of RWB-PLT-N001-CON (DP-19).

#### 12.2 REST operations consumed

| Operation | Owner | Use in this story |
|---|---|---|
| The decision-record query of the rwb-decision contract (C RWB-P7-E1027-CON) | rwb-decision (P7) | The decision items, the case state changes and the creation item. Path and filter are Not specified in the source documents (GAP-2210; ASM-3635) |
| The interaction read of the rwb-source-data contract (DP-18) | rwb-source-data (P1) | The contact items of the ledger. Path and paging are Not specified in the source documents (GAP-0695; ASM-1242) |
| GET /api/recovery/document/v1/cases/{id}/documents | rwb-document (P5) | The document items |
| POST /api/recovery/access/v1/authorise | rwb-access (P4) | Case record R and the scope, through the guard of the service template (ASM-3637) |
| GET /api/recovery/case/v1/admin/parameters (own service) | rwb-case (P3) | `timeline.type.order`, `caserecord.section.timeout.ms` and the page size (DP-06) |
| GET /api/recovery/case/v1/admin/lists/{listCode} (own service) | rwb-case (P3) | LOV-TRANSFER-REASON, LOV-DOC-TYPE, LOV-CHANNEL labels (DP-07) |

#### 12.3 Events published

None. The panel publishes no case event. The AC-READ access record goes to the rwb-access access log through its contract, not to topic `rwb.case.events.v1` (DP-14 keeps the service topic name for the stories that publish).

#### 12.4 Events consumed

None. The panel reads on open and subscribes to no topic in this story.

#### 12.5 Workflows and activities

None. The read is synchronous REST and starts, signals and queries no workflow. CaseWorkflow (parent, one per case, task queue `rwb-case`) owns the case state the timeline shows; this story only reads the decision records it leaves.

#### 12.6 Schedules

None.

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| assignment | rwb_case | P3 | The assignment and transfer items: assignee, assigned_at, ended_at, reason, rule_id, queue_id, transfer_reason_code |
| recovery_case | rwb_case | P3 | case_no and the current status for the item header |
| queue | rwb_case | P3 | The queue code and the queue name of the from and to queue of a transfer |
| lov_value | rwb_case | P3 | Labels for the transfer reason, document type and channel codes |
| reference_row | rwb_case | P3 | LOV-TRANSFER-REASON, LOV-DOC-TYPE, LOV-CHANNEL |
| reference_version | rwb_case | P3 | The version in force on the read date |
| parameter_catalog | rwb_case | P3 | `timeline.type.order`, `caserecord.section.timeout.ms`, the page size |
| parameter_value | rwb_case | P3 | The values in force on the read date |

The interaction ledger, the documents and the decision records are read through their owners' contracts, never through a table (DP-01, DP-18). The service also owns case_account, case_party, case_entry_exclusion, task, queue_member and queue_measure; this story touches none of them.

#### 12.8 Contract fakes

| Fake | Operations | Owner | Used for |
|---|---|---|---|
| rwb-decision fake | The decision-record query by case | P7 (C RWB-P7-E1027-CON) | AC1, AC2, AC3, AC4, AC5, AC6 |
| rwb-document fake | Documents by case | P5 | AC1, AC6, X7 |
| rwb-source-data fake | The interaction read | P1 (DP-18) | AC1 pattern, AC3, X8 |
| rwb-access fake | Authorise and the masking policy | P4 | AC7, TC-E1-035-08 |
| gateway-bff composite route stub | The SCR-03 route | edge (RWB-PLT-N001-CON) | AC1 to AC7 on the screen path |
| rwb-case read fake | The timeline operation of RWB-P3-E1035-CON | P3 | The contract tests of the sibling story |

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | Yes. One read operation provided under `/api/recovery/case/v1`; three contracts consumed one hop each, 2 s timeout, GET retried once with jitter, breaker per downstream |
| Kafka | None. The panel publishes and consumes no event |
| Temporal | None. No workflow is started, signalled or queried |
| File | None. Documents arrive through the rwb-document contract, not as a file read |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.case`, module `timeline`; the screen module is served by the gateway-bff composite route of RWB-PLT-N001-CON and holds no server code of its own. The package name is the one the Service Template Specification v1 gives for service rwb-case in its P3 row: the story copies it and no segment is renamed or invented here (CG-ALL-3717; R-00756).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TimelineController | Controller | GET /cases/{caseId}/timeline with the guard, the query parameters and the problem response |
| TimelineQueryService | Service | Fans out to the three contracts and the assignment read, merges, sorts by BR1 and pages with the total |
| TimelineMapper | Service | One mapper per source; rule ID and version, or the person, into "by"; the transfer detail fields |
| AssignmentRepository | Repository | The assignments of a case ordered by assigned_at, with the closed previous row for the from queue and owner (DF-WRK-013, DF-WRK-039) |
| DecisionRecordClient | Client | The decision-record query of rwb-decision; 2 s budget, gets the case state changes and the creation item |
| LedgerClient | Client | The interaction read of rwb-source-data (DP-18) |
| DocumentClient | Client | The documents-by-case operation of rwb-document |
| SectionGuard | Component | Per-source budget, failure capture and the section state with MSG-P3-023 |
| ParameterReader | Component | `timeline.type.order`, `caserecord.section.timeout.ms` and the page size through the parameters contract (DP-06) |
| TimelinePanel, TimelineItemDetail, SectionMessage | Screen component | SCR-03 timeline panel, item detail for a transfer, section message |

**Pattern application**

| DP code | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Database**

- Reads assignment, recovery_case, queue, lov_value, reference_row, reference_version, parameter_catalog and parameter_value in schema `rwb_case` only, through the rwb-case login (DP-02).
- No migration. The tables and the Flyway sequence come from RWB-P3-E1018-CON and RWB-PLT-E1044-CON; the assignment read uses the index on `assignment(case_id, assigned_at)` that the DB story creates.
- No index and no read outside `rwb_case`; the ledger read is a contract call.

**Configuration and reference data**

- Parameter `timeline.type.order` (legacy §13) with the BR1 order as its value; `caserecord.section.timeout.ms` = 3000 (legacy assumed; DL11); the page size with the legacy default of 50.
- Reference data LOV-TRANSFER-REASON (R01 to R06), LOV-DOC-TYPE and LOV-CHANNEL through the reference-data contract (DP-07).

**Build steps**

1. AssignmentRepository and the transfer item detail from the closed previous row; tests AC1, AC2.
2. Mappers for the decision record, the ledger row and the document; tests AC1, AC4.
3. Merge, type order from the parameter and the record-ID tie break; tests AC1, AC5.
4. Paging with the total of the merged set; test AC6.
5. SectionGuard with the per-source budget and the partial page; tests AC3, X7, X8.
6. Scope check through the guard and the 404 path; test AC7.
7. TimelinePanel, item icons and the transfer detail; test AC2.
8. Performance test with 500 events; BR6; and the access test.

**Feature flag.** `rwb.p3.timeline` (legacy). Off: SCR-03 hides the Timeline panel and the operation returns 404.

**Done when.** The tests in section 16 pass and the timeline of a case with 500 events reads in under 2 seconds in SIT (NFR-070).

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session or an expired session | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the scope | This case is not in your scope. |
| MSG-P3-023 | One source does not answer | {section} cannot be shown now. The rest of the case is shown. |
| MSG-P3-024 | The panel has nothing to show | Nothing is recorded in {section} yet. |

Validation: `caseId` must be a case identifier; `page` is 0 or more and `size` 1 to 100, and a value outside the range is 400 with no data; `from` and `to` are optional date-times and `from` after `to` is 400. A case that is unknown, out of scope or behind the flag returns 404, never 403, so the panel leaks nothing about the case. Every error is the service problem response of TSD P3 v3 T2.1 carrying the MSG code and the trace ID.

### 15. Screens and states

SCR-03 Case record gains the Timeline panel, served as the gateway-bff composite route of RWB-PLT-N001-CON (DP-19). Loading: skeleton rows with the section headings. Read only: items in time order with type icon, summary, by and time; a new case shows its creation item; a transfer opens its detail with reason, from and to queue and owner, and the rule version. Empty (not in Screen Specifications v1; Not specified in the source documents (CG-ALL-3718)): a case with no item shows MSG-P3-024 for the panel. Error (not in Screen Specifications v1; Not specified in the source documents (CG-ALL-3718)): MSG-P3-023 for the section that failed and MSG-P4-003 out of scope; the panel never blocks the rest of the screen. No access (not in Screen Specifications v1; Not specified in the source documents (CG-ALL-3718)): MSG-P4-002 without the right. The full timeline screen with filters, SCR-04, comes in Epic 2 (RWB-P3-E2016-APP). SCR-04 states: Loading: skeleton rows with the section headings, as SCR-03. Empty, error and no access: not in Screen Specifications v1; Not specified in the source documents (CG-ALL-3719), so no SCR-04 state beyond loading is claimed in this story.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-035-08 | Access, AC8 | Component | RW-REFADM calls GET /cases/{caseId}/timeline and is refused with MSG-P4-002 |
| TC-E1-035-09 | Contract operations, events and activities of section 12 | Component | Not specified in the source documents (DOR-RWB-P3-E1035-APP-12) |
| TC-E1-035-10 | Boundary of the tables of section 12.7 (ASM-3438) | Component | Not specified in the source documents (DOR-RWB-P3-E1035-APP-12) |
| TC-E1-035-01 | AC1, BR1, BR2 | End to end | Transfer, two documents and a status change |
| TC-E1-035-02 | AC2, BR3 | End to end | Manual transfer with R04 |
| TC-E1-035-03 | AC3 | End to end | Decision log query timing out |
| TC-E1-035-04 | AC4 | End to end | Case with only its creation entry |
| TC-E1-035-05 | AC5, BR1 | End to end | Two records at 07:00:00 |
| TC-E1-035-06 | AC6 | End to end | 132 events |
| TC-E1-035-07 | AC7, BR4 | End to end | Case of another team |
| TC-E1-035-11 | AC10 | Component | Not specified in the source documents (NEWAC-RWB-P3-E1035-APP-AC10) |
| TC-E1-035-12 | AC9, BR10 | Component | Document query times out |
| TC-E1-035-13 | BR5, BR6, BR7, BR8, BR9, BR11 | Component | Not specified in the source documents (NEWAC-RWB-P3-E1035-APP-AC9) |

The legacy TC IDs, their Covers and their Data are kept unchanged; the legacy Level System maps to End to end and Access maps to Component. No ITG copy of a TC exists for this key, because no integration story owns a criterion here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the type order, the timeout, the page size and every label are data, read through the parameters and reference-data contracts.
- No personal data in logs, tests or prompts; contact summaries follow masking by role and test parties are synthetic. No PII in events, workflow inputs or logs.
- No read of another service's tables: documents through rwb-document, decision records through rwb-decision, ledger rows through rwb-source-data (DP-01, DP-18).
- No call chains: the panel asks each owner one hop, in parallel, with a 2 s timeout and a breaker per downstream.
- The timeline never writes; it shows records as they were written, and the AC-READ access record is the only record the read produces.
- A failed source degrades one section and never the page.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-016 | Every workflow event with its rule ID and version | Epic 1, 3.3; Program, 5.3 | FEAT-ACA-12 | 06 Take over and own the case | None | TC-E1-035-01, TC-E1-035-02, TC-E1-035-05 |
| REQ-OCC-007 | Contact history and documents on the case view | Epic 1, 3.6; Program, 5.6 | FEAT-ACA-12 | 06 Take over and own the case | None | TC-E1-035-03, TC-E1-035-04, TC-E1-035-06, TC-E1-035-07 |
| REQ-WKM-003 | A manual transfer carries its reason | Not specified in the source documents (GAP-2210; ASM-3634) | FEAT-ACA-12 | 06 Take over and own the case | BR3 | TC-E1-035-02 |
| REQ-ACA-005 | Personal data masked by role | Not specified in the source documents (GAP-2210; ASM-3634) | FEAT-ACA-12 | 06 Take over and own the case | BR5 | TC-E1-035-01, TC-E1-035-03 |

| Trace | Reference |
|---|---|
| Legacy key | RWB-E1-035, disposition Split (rework) |
| Contract story | RWB-P3-E1035-CON (v1.1 timeline item, partial-result envelope, fakes) |
| Contract version | Not specified in the source documents (DOR-RWB-P3-E1035-APP-23) |
| Build dependency | RWB-P3-E1023-APP (SCR-03 read-only case record and the published timeline operation) |
| Contract dependencies | RWB-P7-E1027-CON (decision-record query) |
| Pattern rows | DP-01, DP-03, DP-06, DP-07, DP-11, DP-13, DP-14, DP-15, DP-18, DP-19 |
| Epic design | Not specified in the source documents (DOR-RWB-P3-E1035-APP-14) |
| Gaps and assumptions | GAP-2210, GAP-0692, GAP-0695; ASM-3632, -2, -3, -4, -6, ASM-1239, ASM-1242 |
| Open decisions | DL11, DL26; ASM-0553, ASM-0703, ASM-1051, ASM-1104, ASM-0247, ASM-0264, ASM-0275, ASM-0355 |
| Database login | rwb-case login per DP-02; name taken from RWB-PLT-DB when issued; grants SELECT, INSERT and UPDATE on schema rwb_case only |
| Timeline order and paging | Default order occurred_at descending; page size taken from a parameter |

### 19. Out of scope

- The full timeline screen SCR-04 with filters and queue history (RWB-P3-E2016-APP, legacy RWB-E2-016).
- The full case record view with collateral, decisions and timers (Epic 2, FEAT-WKM-08).
- Communications and notices on the timeline (Epic 2, P6).
- The read-only case header, the accounts, the parties and the contact history panel (RWB-P3-E1023-APP).
- Writing an entry to the interaction ledger; the ledger is written by rwb-source-data (DP-18).
- The transfer itself and its reason codes (RWB-P3-E1021-APP and RWB-P3-E1021-CON).
