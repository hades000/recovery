# RWB-P3-E2016-APP Full case record view with the history timeline

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2016-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Contract version | v1 (REST base /api/recovery/case/v1) |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-016 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P3-E2016-APP-16); the fit to two weeks is Not specified in the source documents (DOR-RWB-P3-E2016-APP-15) |
| Patterns applied | DP01, DP03, DP06, DP07, DP11, DP13, DP14, DP19 |
| Parallel lane | L-P3-AD |
| Ready to start | After RWB-P3-E2015-APP, RWB-P3-E2012-APP |
| Depends on (build) | RWB-P3-E2016-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-N001-CON, RWB-P3-E2015-APP, RWB-P3-E2012-APP, RWB-P3-E1035-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-012, FR-P3-019, FR-P3-021, FR-P3-023, FR-P3-030) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-016 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P3-E2016-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 17 cross-document, 5 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the case record view to show every action, decision, transfer, letter, document, contact and timer event of my case on one timeline with type and date filters and a paged answer, and the queue history with the reason for each move, read from rwb-case and from the decision log, document, notice and interaction-ledger contracts**, so that **I read the whole case in one place, inside the 2-second wait, with no service reading another service's schema and no item that my role may not see**.

### 2. Business rationale

A case lives for months or years and passes through several teams, partners and courts. Today a new owner reads email threads and spreadsheets to learn what happened. This story puts the decision log entries, assignments and transfers, contacts, notices, documents and timer events of a case on one timeline, filtered by type and date, with a queue history that shows every queue and owner and the reason for each move. It meets REQ-WKM-008 and REQ-OCC-008. The measure is that a case history with 30 events reads in under 2 seconds (NFR-009) and stays under 2 seconds at the 2031 data size (NFR-070).

In the target the same journey is cut across services and the read is composed from owners rather than from one schema. rwb-case holds the case, its `assignment`, `queue`, `timer` and `recovery_case` rows (DP-01). The decision items come from the central decision ledger of rwb-decision (P7), the document items from the metadata of rwb-document (P5), the notice items from rwb-comms (P6), the contact items from the interaction ledger owned by rwb-source-data (P1) under the default ruling and DP-18, and the rights and the mask from rwb-access (P4). The legacy in-process calls `DecisionLogQuery.forCase`, `DocumentQuery.forCase` and `NoticeQuery.forCase` become REST calls on the owners' bases, one hop, with a 2 s timeout and a breaker per downstream (DP-11), built against the contract fakes on Day 1.

Retiring the monolith surface is the realignment work. The legacy endpoint `GET /cases/{caseId}/timeline` on the shared base moves to `/api/recovery/case/v1` (DP-13), the page size limits and the per-source timeout become parameter rows read through the parameters contract instead of configuration in code (DP-06), the type and reason labels come from the reference-data contract with their version in force (DP-07), and the case screen is composed at the edge by gateway-bff, which calls rwb-case and the other owners in parallel and merges the answers (DP-19). No topic is published by this read; the event naming rule of DP-14 is respected in that the story declares no topic of its own.

Two values of the target are not settled by the sources and are carried as register rows: the owner-side read path of the case's interaction-ledger entries, because the interaction API is claimed by both P3 and P1 in the Ownership Map (GAP-0716; ASM-1263), and the Ownership Map row of the case-scoped notice list that Architecture v5 slide 17 gives rwb-comms (GAP-0717; ASM-1264). The story builds against the P1, P5, P6, P7 and P4 contract fakes and is proven end to end by RWB-ITG-E2016-ITG.

### 3. Preconditions

- RWB-P3-E2016-CON is published: the operation shape of `GET /cases/{caseId}/timeline`, the `TimelinePage` and `TimelineItem` components with the seven type values, the error mapping, the nine contract tables and the fakes of P1, P4, P5, P6 and P7.
- RWB-PLT-E1027-CON is published: the local decision-record library, the record reference shape and the shared topic `rwb.decision-record.v1` (DP-03). The decision item carries the ledger entry ID as its reference; this story writes no record.
- RWB-PLT-E1042-CON and RWB-P3-E1042-CON are published: the parameters contract and its client library, so the source timeout and the page size limits are rows and not constants (DP-06).
- RWB-PLT-E1043-CON and RWB-P3-E1043-CON are published: the reference-data contract, with LOV-ASSIGN-REASON and LOV-TRANSFER-REASON and the type labels loaded and versioned (DP-07).
- RWB-PLT-E1047-CON is published: the naming library, so no topic or base is chosen locally (DP-14).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves the case screen and composes the timeline answer with the case answer (DP-19).
- RWB-P3-E2015-APP is done: the clocks and deviations panels on SCR-03, whose timer rows this story reads on the same screen.
- RWB-P3-E2012-APP is done: every new assignment carries its queue and its transfer reason code, so a queue-history item can show from queue, to queue, reason code and rule ID.
- RWB-P3-E1035-CON is published: the case record view v1.1 contract, whose timeline answer this story extends with the paging, the queue history, the four extra item fields and `unavailableSources[]`, so no field of v1.1 is removed and a v1.1 consumer keeps working.
- The decision log, document, notice and interaction-ledger contracts are consumed and faked; the case-scoped interaction read is built against the P1 fake while its path is settled (GAP-0716; ASM-1263), and the case-scoped notice list is read under the P6 contract against the P6 fake (GAP-0717; ASM-1264).
- The roles of section 10 hold Case record R with the case in scope, and Decision log R, Documents R and Litigation R for the item types they may read, all answered by rwb-access.
- The login is the rwb-case login (DP-02): Not specified in the source documents (GAP-0675; ASM-1222).

### 4. Flow

1. Case owner: opens SCR-04 Case timeline from SCR-03 Case record. The browser calls the gateway-bff composite route and never an owner service directly (DP-19).
2. gateway-bff: calls `GET /api/recovery/case/v1/cases/{caseId}` and `GET /api/recovery/case/v1/cases/{caseId}/timeline` on rwb-case, one hop each, and merges the two answers into the screen model.
3. rwb-case: applies the access check through rwb-access (`POST /api/recovery/access/v1/authorise`), which returns Case record R, the scope and the item-type rights Decision log R, Documents R and Litigation R; a missing Case record R is a 403 and a case outside the scope is a 404.
4. rwb-case: reads the case's own records from `rwb_case` — `assignment` with `queue_code`, `recovery_case` and `timer` — for the date range, using the case indexes only.
5. rwb-case: in parallel, and only for the item types the caller may read, calls the owners' operations of section 12.2: the ledgers of P7 by case, P5 by case, P6 by case, and P1 for the interaction ledger; each call runs in an activity-free request thread with one hop, a 2 s timeout taken from the parameter `timeline.source-timeout-ms`, and a breaker per downstream.
6. rwb-case: maps every record to a `TimelineItem` with `at`, `type`, `summary`, `by`, `reference`, and, for an assignment or a transfer, `reasonCode`, `fromQueueCode`, `toQueueCode` and `ruleId`; the summary is built from codes and labels, never from free text of another service.
7. rwb-case: drops the item types the caller may not read without an error (decision items without Decision log R, document items without Documents R, notice items without Litigation R), masks each contact summary by role through the ACE common masking path with the masking policy read from rwb-access, merges the remaining items newest first with the source sequence kept on a tie, and returns one page with `page`, `size`, `total` and `unavailableSources[]`.
8. rwb-case: on a source that times out or has its breaker open, adds one entry to `unavailableSources[]` with MSG-GEN-006 for that source and returns the other items; the call itself does not fail.
9. Case owner: filters by type and by date; the front end repeats the call with `type`, `from` and `to` and shows the answer in state Filtered. A page beyond the last returns an empty `items[]` with the same `total`.
10. Case owner: opens Queue history; the front end calls the same operation with `type=ASSIGNMENT,TRANSFER` and shows from queue, to queue, from owner, to owner, reason code and rule ID for each move, with the allocation as the oldest entry.
11. Case owner: opens a decision item; the front end opens the entry through `GET /api/recovery/decision/v1/decision-log/{entryId}` on the P7 contract, which is the reference the item already carries.
12. Screen states of SCR-03 Case record and SCR-04 Case timeline: loading while the timeline call runs (loading text not specified in the source documents, DOR-RWB-P3-E2016-APP-10); empty when `items[]` is empty; error when the call returns 422 or 503, showing the message ID of the response and keeping the page; no access when the call returns 403 (MSG-P4-002), with no items shown.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A source module does not answer within 2 seconds, or its breaker is open | The other items show; one entry per missing source names it in `unavailableSources[]`; the call returns 200 | MSG-GEN-006 | AC6 |
| X2 | The caller lacks Decision log R, Documents R or Litigation R | Those item types are left out without an error and without a gap in the other items | None | AC5 |
| X3 | Date from is after date to | Refused before any source is called; nothing is read and nothing is written | MSG-GEN-003 | AC7 |
| X4 | No item matches the filter | An empty page with total 0 and the empty sentence on the screen | MSG-P3-019 | AC8 |
| X5 | An assignment written before RWB-E2-012 has no queue | The move shows with "Queue not recorded" and its reason, and the run continues | None | AC9 |
| X6 | The case is outside the caller's scope | Not found; nothing is returned and nothing is written | MSG-P4-003 | AC10 |
| X7 | Page size is outside 1 to 200, or not an integer | Refused before any source is called, with the field and its bounds | MSG-GEN-002 | AC7, AC11 |
| X8 | The item count of a case exceeds one page | The first page returns with `total` and `page` and the caller pages; the order is stable across the pages of one query | None | AC11 |
| X9 | The caller holds no Case record R | Refused with 403 on the service call and on the composite route; the answer carries the refusal, not an empty timeline | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads what other stories write; builds on Day 1 against the case contract and the P1, P4, P5, P6 and P7 contract fakes. The queue on the assignment comes from RWB-P3-E2012-APP and the timer projection from RWB-P3-E1035-CON |
| Negotiable | Item wording, the filter layout and the summary text can change; the sources, the rights and the ordering are fixed |
| Valuable | A new owner reads the case without asking the previous one, and no team waits for another team's release to see the history |
| Estimable | One endpoint, one merge service, one rights filter, five consumed contracts, one screen with two states and a queue-history tab |
| Small | Fits one iteration with its tests |
| Testable | API tests with seeded `rwb_case` rows and stubbed contracts; one load test at 4,000 items; no test reaches another schema |

### 7. Acceptance criteria

```gherkin
Feature: Full case record view with the history timeline

  Background:
    Given the business date is 2026-12-20
    Given user "U-CO-01" holds RW-CASEOWN and owns case "RW-2026-000601"

  Scenario: AC1 Timeline (legacy RWB-E2-016 AC1)
    Given case "RW-2026-000601" has 30 events: 4 assignments, 3 transfers, 8 contacts, 6 decision log entries, 2 notices, 5 documents and 2 timer events
    Given the rwb-source-data contract mock returns the 8 contacts of the case with the same values, all kept
    Given the rwb-decision contract mock returns the 6 decision log entries of the case with the same values, all kept
    Given the rwb-document contract mock returns the 5 documents of the case with the same values, all kept
    Given the rwb-comms contract mock returns the 2 notices of the case with the same values, all kept
    When "U-CO-01" opens the case timeline
    Then the 30 items show newest first, each with type, actor and time
    Then the first page loads within 2 seconds at the 95th percentile over 20 runs

  Scenario: AC2 Filter (legacy RWB-E2-016 AC2)
    Given the filter set to "DECISION"
    Given the rwb-decision contract mock returns the 6 decision log entries of the case with the same values, all kept
    When the timeline refreshes
    Then only the 6 decision items show
    Then each carries its decision log entry ID and opens that entry

  Scenario: AC3 Queue history (legacy RWB-E2-016 AC3)
    Given case "RW-2026-000601" was allocated to "MTG-BKK-CO" on 2026-11-30 and transferred three times: to "LIT-BKK-01" with reason "R05" on 2026-12-05, to "MTG-BKK-CO" with reason "R06" on 2026-12-08 and to "LIT-BKK-02" with reason "R01" on 2026-12-12
    When "U-CO-01" opens queue history
    Then the three moves show newest first with from queue, to queue, from owner, to owner, reason code and rule ID
    Then the allocation on 2026-11-30 shows as the first entry with reason "ALLOCATION"

  Scenario: AC4 Date filter (legacy RWB-E2-016 AC4)
    Given the filter from 2026-12-05 to 2026-12-08
    When the timeline refreshes
    Then only items dated 2026-12-05 to 2026-12-08 inclusive show

  Scenario: AC5 Items the role may not read (legacy RWB-E2-016 AC5)
    Given user "U-PC-01" holds RW-PHONECOL with case "RW-2026-000601" in scope
    Given the rwb-access contract mock returns Case record R and Documents R for "RW-PHONECOL" without Decision log R and without Litigation R, all kept
    Given the rwb-document contract mock returns the 5 documents of the case with the same values, all kept
    When "U-PC-01" opens the case timeline
    Then no decision item and no notice item shows
    Then contacts, assignments, transfers, documents and timer events show

  Scenario: AC6 A source does not answer (legacy RWB-E2-016 AC6)
    Given the document query does not answer within 2 seconds
    Given the rwb-document contract mock returns no answer within 2 seconds, all kept
    When "U-CO-01" opens the case timeline
    Then the 25 items from the other sources show
    Then a notice shows MSG-GEN-006 naming "Document hub"

  Scenario: AC7 Dates in the wrong order (legacy RWB-E2-016 AC7)
    When "U-CO-01" sets the filter from 2026-12-10 to 2026-12-01
    Then the system refuses the request with MSG-GEN-003 naming "to" and "from"

  Scenario: AC8 Nothing matches (legacy RWB-E2-016 AC8)
    Given the filter set to "NOTICE" and the dates 2026-11-01 to 2026-11-15
    Given the rwb-comms contract mock returns no notice of the case in that range, all kept
    When the timeline refreshes
    Then the screen shows MSG-P3-019

  Scenario: AC9 Assignment written before the queue was recorded (legacy RWB-E2-016 AC9)
    Given case "RW-2026-000602" has an assignment from 2026-11-30 with no queue recorded
    When "U-CO-01" opens its queue history
    Then the move shows with "Queue not recorded" and its reason "ALLOCATION"

  Scenario: AC10 Case outside scope (legacy RWB-E2-016 AC10)
    Given case "RW-2026-000603" belongs to team "SME-NTH" and "U-CO-01" has scope Own in team "MTG-BKK"
    Given the rwb-access contract mock returns no scope for "U-CO-01" over team "SME-NTH", all kept
    When "U-CO-01" opens its timeline
    Then the system does not find the response with MSG-P4-003

  Scenario: AC11 Large history (legacy RWB-E2-016 AC11)
    Given case "RW-2026-000604" has 4,000 timeline items
    When "U-CO-01" opens the case timeline with page size 50
    Then the first 50 items show within 2 seconds
    Then the total shows 4,000

  Scenario: AC12 Masking, owner reads and labels (BR6, BR11, BR12, BR14) (new, D-RCV-60)
    Given the rwb-source-data contract mock returns the contacts of the case, with the count Not specified in the source documents (NEWAC-RWB-P3-E2016-APP-AC12)
    When a user with the Case record right opens the case timeline
    Then the contact summaries are masked for the role and no unmasked summary is returned or logged
    Then the case timeline reads no table of another service and writes no row
    Then the type and reason labels come from the reference data with the version in force

  Scenario: AC13 Error answers of the provided operations (new, D-RCV-60)
    Given the error mapping of RWB-P3-E2016-CON is in force
    When a request to the case timeline is refused for a missing login, for a role without the right, or for a case that is not found
    Then the answer carries the status code of the error mapping, 401, 403 or 404, and no item is returned

  Scenario: AC14 A status change the model does not allow is refused (NEWAC-RWB-P3-E2016-APP-AC14) (new, D-RCV-60)
    Given the case holds a status from which the status model does not allow the requested change
    When a user with the Case record right requests that status change on the case
    Then the system refuses the change with the error mapping of RWB-P3-E2016-CON
    Then the case keeps its current status
```

Four mechanism moves sit behind these criteria and change no value of them. First, the contact items are built in rwb-case from the interaction ledger, which the Ownership Map gives to rwb-source-data (ASM-0067, DP-18), so the ledger is read one hop away through the P1 contract and never from an `interaction` table in `rwb_case`; the owner-side path and the base are contested by the two rulings of the map (GAP-0716; ASM-1263). Second, the decision, document and notice items come from the P7, P5 and P6 contracts in place of the legacy in-process queries, each with one hop, the 2 s timeout of the parameter and a breaker, which is why each cross-service Given above is paired with its contract mock. Third, the case-scoped notice list is given by Architecture v5 slide 17 to rwb-comms and has no row in the Ownership Map API section (GAP-0717; ASM-1264). Fourth, queue history is the same operation with `type=ASSIGNMENT,TRANSFER`, so AC3 opens no second endpoint and no second contract. Nothing is projected: the items are merged on the read, so a source that is down removes its own items and nothing else.

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
| BR8 | Paging is part of the operation: `page` starts at 0, `size` starts at 50 and is limited to 1 to 200; a value outside the bounds is refused with MSG-GEN-002 before any source is called | Template and Rules §R5.5 DP-06; legacy contract |
| BR9 | The same query repeated returns the same page, and two items at the same instant keep the source sequence, so a caller may page a long history without a lost or a doubled item | events.txt Rules (ordering); BR2 |
| BR10 | `unavailableSources[]` carries one entry with MSG-GEN-006 for each source that timed out or whose breaker is open, and the remaining items still return with 200 | NFR-008; MSG-GEN-006 |
| BR11 | The timeline reads `recovery_case`, `assignment`, `queue` and `timer` in `rwb_case` and the owners' contracts; it never reads another service's table, and `interaction` is not a table of this service | DP-01; DP-18; ASM-0067; ADR-010 |
| BR12 | The role mask of a contact summary is applied through the ACE common masking path with the policy read from rwb-access; the unmasked summary is never returned and never logged | CTL-11; DL26 |
| BR13 | The call writes nothing: no row, no decision record, no event and no workflow state, and a refusal writes nothing either | Legacy solution plan; Template and Rules §R7.2 s17 |
| BR14 | The source timeout and the page size bounds are parameter rows read through the parameters contract, and the type and reason labels come from the reference data with the version in force; the summary wording of a document timeline item is Not specified in the source documents (GAP-1061) | DP-06; DP-07; legacy solution plan |
| BR15 | A type value outside the seven of the contract is refused with MSG-GEN-002 and is never ignored, so a filter that is meant to narrow the answer can never widen it | Legacy contract; BR8 |

### 9. State transitions

None. This story does not change a case status and does not move a case. It reads records only, writes no row, raises no event and starts no workflow.

| Observed fact | Written by | Appears as |
|---|---|---|
| Case allocated to a queue | rwb-case allocation (RWB-P3-E1020-APP) | The oldest queue-history entry with reason ALLOCATION |
| Case transferred with a reason code | rwb-case transfer (RWB-P3-E1021-APP) | A later queue-history entry with from and to queue, from and to owner, reason code and rule ID |
| Decision recorded | rwb-decision ledger through the local decision-record library | A decision item with the ledger entry ID as its reference |
| Document attached | rwb-document metadata | A document item, left out without Documents R |
| Notice sent | rwb-comms notice | A notice item, left out without Litigation R |
| Timer started or breached | rwb-case timer projection | A timer item with its type, start and status |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Reads the timeline and queue history (Case record R; Decision log R; Documents R; Litigation R) |
| RW-TEAMMGR, team manager | Reads the timeline and queue history (Case record R; Decision log R) |
| RW-PHONECOL, phone collector | Reads the timeline without decisions and notices (Case record R; Documents R) |
| RW-CONDUCT, conduct and QA officer | Reads every item (R in all areas) |
| RW-AUDIT, internal audit | Reads every item (R in all areas); changes nothing |
| rwb-case service identity (the rwb-case login, DP-02) | Applies the access check, reads the `rwb_case` rows and calls the P1, P5, P6 and P7 contracts one hop away; writes nothing |
| gateway-bff (the platform edge) | Calls the case and timeline operations and merges the two answers for the screen; holds no copy of the items |
| RW-REFADM and every role without Case record R | Refused on the operation with MSG-P4-002 |

The per-service login name is Not specified in the source documents (GAP-0675; ASM-1222); the story names it "the rwb-case login (DP-02)" until it is agreed.

### 11. Data

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
| DF-INT-002 | interaction | case_id | Read through P1's ledger contract |
| DF-INT-004 | interaction | occurred_at | Read through P1's ledger contract |
| DF-INT-005 | interaction | channel | Read through P1's ledger contract |
| DF-INT-006 | interaction | direction | Read through P1's ledger contract |
| DF-INT-008 | interaction | contact_result | Read through P1's ledger contract |
| DF-INT-011 | interaction | summary | Read through P1's ledger contract, masked by role |
| DF-WRK-030 | timer | timer_type | Read |
| DF-WRK-031 | timer | started_at | Read |
| DF-WRK-035 | timer | status | Read |
| DF-DEC-001 | decision_log_entry | id | Read through the owner's contract (P7 rwb-decision) |
| DF-DEC-003 | decision_log_entry | decision_code | Read through the owner's contract (P7 rwb-decision) |
| DF-DEC-004 | decision_log_entry | rule_id | Read through the owner's contract (P7 rwb-decision) |
| DF-DEC-012 | decision_log_entry | final_call | Read through the owner's contract (P7 rwb-decision) |
| DF-DEC-016 | decision_log_entry | decided_at | Read through the owner's contract (P7 rwb-decision) |
| DF-DOC-001 | document | id | Read through the owner's contract (P5 rwb-document) |
| DF-DOC-004 | document | document_type | Read through the owner's contract (P5 rwb-document) |
| DF-DOC-005 | document | source | Read through the owner's contract (P5 rwb-document) |
| DF-LEG-015 | notice | id | Read through the owner's contract (P6 rwb-comms) |
| DF-LEG-018 | notice | notice_type | Read through the owner's contract (P6 rwb-comms) |
| DF-LEG-019 | notice | sent_date | Read through the owner's contract (P6 rwb-comms) |
| DF-LEG-022 | notice | delivery_status | Read through the owner's contract (P6 rwb-comms) |
| DF-REF-132 to DF-REF-158 | parameter_catalog, parameter_value | `timeline.source-timeout-ms`, the page size default and the page size maximum, with their versions in force | Read |
| DF-REF-159 to DF-REF-184 | reference_version, reference_row | LOV-ASSIGN-REASON and LOV-TRANSFER-REASON versions and their rows, and the type labels | Read |

Field IDs are those in the Logical Data Model and Data Dictionary v9. The `interaction` rows keep their legacy field IDs; the table is owned by rwb-source-data (ASM-0067, DP-18), so this story reads the six fields through the P1 contract and holds no copy of them. The decision, document and notice rows are read through the P7, P5 and P6 contracts and are never joined into `rwb_case`. A contact summary is masked before it leaves the service (BR12). The `summary` of an item is built from codes and labels and is never a free-text note of another service.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases/{caseId}/timeline` | One page of the case timeline: `items[]` newest first, `page`, `size`, `total`, `unavailableSources[]`; query `type` (comma separated DECISION, ASSIGNMENT, TRANSFER, INTERACTION, NOTICE, DOCUMENT, TIMER), `from` (date), `to` (date), `page` (integer, default 0), `size` (integer, default 50, 1 to 200) | Case record R, scope applied; item types filtered by Decision log R, Documents R and Litigation R | Not applicable: the call writes nothing |
| GET | `/cases/{caseId}/timeline` | Queue history: the same operation with the type filter fixed, so each item carries from queue, to queue, from owner, to owner, `reasonCode` and `ruleId`; no second path is published | As above | Not applicable |

`TimelinePage` fields: `items[]` of `TimelineItem`, `page`, `size`, `total`, `unavailableSources[]`. `TimelineItem` fields: `at`, `type`, `summary`, `by`, `reference`, `reasonCode`, `fromQueueCode`, `toQueueCode`, `ruleId`; `reference` is the decision log entry ID, the document ID, the notice ID, the assignment ID or the timer ID of its source. `unavailableSources[]` entries carry `system` and `messageId` (MSG-GEN-006) per missing source.

Errors: 401 no session (MSG-P4-001); 403 no Case record R (MSG-P4-002); 404 unknown or out of scope (MSG-P4-003); 422 `to` before `from` (MSG-GEN-003), a `size` outside 1 to 200 or a `type` outside the seven (MSG-GEN-002); 503 the case store is down (MSG-GEN-006, Error and Message Standard v4; whether its text fits a read is Not specified in the source documents (CG-ALL-4240)). A downstream that is down is not a 5xx of this operation: it is an `unavailableSources[]` entry with 200 (BR10).

The interaction operation that TSD P3 v3 records as API-P3-014 is owned by rwb-source-data under the Ownership Map (`GET /cases/{caseId}/interactions`, owner P1; ASM-0038), while the table ruling keeps the case timeline and interaction API with rwb-case (ASM-0067). This story therefore serves the timeline, which carries the contact items, and reads the ledger one hop away as consumed in 12.2; the owner-side path is the open point (GAP-0716; ASM-1263).

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout of `timeline.source-timeout-ms` and a breaker per downstream apply to every row.

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | rwb-decision (P7) | The ledger entries of the case in the date range, for the decision items: `id`, `decisionCode`, `ruleId`, `finalCall`, `decidedAt` | One hop, 2 s, breaker |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | rwb-decision (P7) | One ledger entry when the case owner opens a decision item | One hop, 2 s, breaker |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | rwb-document (P5) | The document metadata of the case in the date range, for the document items: `id`, `documentType`, `source` | One hop, 2 s, breaker |
| GET | `/api/recovery/comms/v1/cases/{caseId}/notices` | rwb-comms (P6) | The case-scoped notice list, for the notice items: `id`, `noticeType`, `sentDate`, `deliveryStatus`; the path is Architecture v5 slide 17 and has no Ownership Map row (GAP-0717; ASM-1264) | One hop, 2 s, breaker |
| GET | `/api/recovery/comms/v1/notices/{noticeId}` | rwb-comms (P6) | One notice when a notice item is opened | One hop, 2 s, breaker |
| GET | Not specified in the source documents (GAP-0716; ASM-1263) | rwb-source-data (P1) | The case's interaction-ledger entries for the contact items: `occurredAt`, `channel`, `direction`, `contactResult`, `summary` | One hop, 2 s, breaker |
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | Case record R, the scope and the item-type rights Decision log R, Documents R and Litigation R, cached by the guard library | One hop, 2 s, breaker |
| GET | `/api/recovery/access/v1/masking-policies` | rwb-access (P4) | The masking policy the ACE common masking path applies to a contact summary by role (CTL-11, DL26) | One hop, 2 s, cached |

The masking path is the operation Architecture v5 slide 14 gives rwb-access (`/masking-policies`); the Ownership Map API section has no row for it, so its path is taken from that slide and confirmed in the rwb-access contract baseline (RWB-P4-E1037-CON). No other service is called, and the timeline never calls a downstream of a downstream.

#### 12.3 Events published

None. The timeline is a read: it writes no row and raises no event, so it has no outbox row and no topic of its own. The decision-record reference it shows is written by the local decision-record library of the story that took the decision (DP-03), and the record itself is sealed in the central ledger by rwb-decision.

#### 12.4 Events consumed

None. The facts that become a timeline item arrive in rwb-case through the case router of the stories that move the case; the timeline holds no projection and no inbox, so it consumes nothing and its answer is always the current state of its sources. A stale item is therefore impossible, and a missing source is visible in `unavailableSources[]` rather than frozen into a table.

#### 12.5 Workflows and activities

None added. The timeline is served inside the request; it starts no workflow, adds no activity and holds no timer. The assignment and timer rows it reads are written by the activities of CaseWorkflow and of the allocation and transfer stories, which own them.

#### 12.6 Schedules

None. The legacy five-minute timer check (JOB-05) is retired and the clocks are durable timers inside the workflow (Architecture v5 slide 44); this story creates no Schedule and no Quartz row, and a read needs none.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| recovery_case | P3 (rwb_case) | Case facts of the timeline: case ID and team |
| assignment | P3 (rwb_case) | The assignment and transfer items, with queue, reason, reason code and rule ID |
| queue | P3 (rwb_case) | The queue code of a move |
| timer | P3 (rwb_case) | The timer items: type, start and status |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | Present in the schema; this story writes none of them |

`interaction` is not a table of this contract: it is owned by rwb-source-data (ASM-0067, DP-18) and is read through the P1 contract. No table of another service is named and no foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-decision WireMock | The P7 contract | The 6 entries of RW-2026-000601 with their IDs and decided times; one entry by ID; an empty answer for the November range |
| rwb-document WireMock | The P5 contract | The 5 documents of the case; an empty answer; a delayed answer beyond 2 s for AC6 |
| rwb-comms WireMock | The P6 contract | The 2 notices of the case with type, sent date and delivery status; an empty answer for the November range; one notice by ID |
| rwb-source-data WireMock | The P1 contract | The 8 contacts of the case ledger with channel, direction, contact result and a summary that must come back masked |
| rwb-access WireMock | The P4 contract | Allow RW-CASEOWN in scope with all four rights; allow RW-PHONECOL with Case record R and Documents R only; refuse a role without Case record R with MSG-P4-002; refuse SME-NTH for a team MTG-BKK scope with MSG-P4-003; the masking policy of the caller's role |
| gateway-bff composite route (WireMock) | The DP-19 route of the case record | The merged case and timeline answer, and the refusal answer that must not be an empty timeline |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 8 consumed | The timeline operation provided (queue history is the same operation); the P7 ledger queries, the P5 documents, the P6 notice list and notice, the P1 ledger read and the P4 authorise and masking policy consumed; one hop, 2 s, breaker |
| Kafka | None | The story publishes and consumes no event (12.3, 12.4) |
| Temporal | None | No workflow and no activity added; the rows it reads are written by the case workflow's activities |
| File | None | No document content is read: only metadata, through the P5 contract |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `timeline`, Java package `th.co.scb.ace.workbench.recovery.case.timeline`; front end folder `src/modules/recovery/case/timeline` with `CaseTimelinePage.tsx` and `QueueHistoryTab.tsx`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; here the decision item carries the record reference and the story writes no record | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-14 applies as a prohibition as well as a rule: the story publishes no topic, and no legacy `rwb.casewf.` or `rwb.p3.` topic name appears in it. The H and C dependencies of this table are held by the platform and service contract stories and are not repeated in the metadata rows, which carry the in-lane stories and the contract story of this key.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TimelineService | Service | Applies the rights filter, calls the sources in parallel, merges, sorts, pages and builds `unavailableSources[]` |
| TimelineItemMapper | Service | Maps an assignment, a transfer, a timer, a contact, a decision, a document and a notice to `TimelineItem`, with summaries built from codes and labels |
| ItemRightsFilter | Service | Drops the item types the caller may not read, silently and without a gap in the other items (BR3) |
| AssignmentHistoryRepository | Repository | Reads `assignment` with its `queue_code` for a case and a date range, using the case index |
| TimerHistoryRepository | Repository | Reads `timer` for a case and a date range, using the case index |
| CaseFactsRepository | Repository | Reads the case ID and team from `recovery_case` for the access check and the answer |
| LedgerClient | Client | Calls the P1 interaction-ledger read and returns the contact facts, or a timeout |
| DecisionLogClient | Client | Calls the P7 ledger by case and by entry ID |
| DocumentClient | Client | Calls the P5 case document list |
| NoticeClient | Client | Calls the P6 case notice list and the notice by ID |
| AccessCheckClient | Client | Calls the P4 authorise operation and the masking policy, both cached by the guard library |
| MaskingAdapter | Library adapter | Applies the role mask to a contact summary through the ACE common masking path (CTL-11, DL26) |
| SourceCallGuard | Component | Wraps each downstream call with the parameter timeout, a breaker and bulkhead, and turns a failure into an `unavailableSources[]` entry |
| CaseTimelineController | Controller | The timeline operation, the query and page validation, and the error mapping |
| CaseTimelinePage | React component | SCR-04 with the Loading, Filtered and Empty states, the type and date filters and the source notice |
| QueueHistoryTab | React component | The queue-history view on SCR-04, calling the same operation with the fixed type filter |

**Database and migrations**

- Reads `recovery_case`, `assignment`, `queue` and `timer` in schema `rwb_case`. No new table and no new column: the timeline is a read.
- Migration `V2016_1__timeline_indexes.sql` adds `ix_assignment_case_assigned_at ON assignment (case_id, assigned_at)` and `ix_timer_case_started_at ON timer (case_id, started_at)`, each read with its date column sorted descending, so a page of the newest items is read without a sort of the whole case.
- The migration runs in the rwb-case Flyway sequence of the service's own schema (DP-15, held by the rwb_case DB story); no other schema is touched and no index is created on another service's table.

**Configuration and reference data**

- Parameter `timeline.source-timeout-ms` = 2000, `timeline.page-size-default` = 50 and `timeline.page-size-max` = 200, through the parameters contract (DP-06). The breaker and bulkhead settings are the resilience library's platform defaults and are not business values, so no number for them is fixed here.
- LOV-ASSIGN-REASON, LOV-TRANSFER-REASON and the seven type labels, through the reference-data contract with the version in force (DP-07). The type list is a list value, not a Java enum.
- The masking policy of a role, read from rwb-access; the mask itself is applied by the ACE common masking path.

**Build steps**

1. `AssignmentHistoryRepository`, `TimerHistoryRepository` and `CaseFactsRepository` with the two indexes; unit tests for each item type and for the "Queue not recorded" case of AC9.
2. `TimelineItemMapper` with codes and labels, and the ordering with the source sequence on a tie; tests for AC1 and AC3.
3. `SourceCallGuard` and the five clients, each against its contract fake, with the parameter timeout, a breaker and the `unavailableSources[]` entry; tests for AC6 and AC3.
4. `ItemRightsFilter` and `MaskingAdapter`; tests for AC5 and for the mask of a contact summary.
5. Paging, the type and date filters and the validation of `to` before `from`, of `size` and of `type`; tests for AC4, AC7, AC8 and AC11.
6. `CaseTimelineController` with the error mapping and the access check; test for AC10 and the 403 of X9.
7. `CaseTimelinePage` with the three states and `QueueHistoryTab` on the same operation; the composite-route contract test with gateway-bff.
8. The 4,000-item load test at page size 50 over 20 runs, and the query plan check that the page uses the two case indexes only.
9. Contract-fake run of every consumed answer in isolation, so the story builds before P1, P5, P6, P7 and P4 land.

**Feature switch.** The legacy flag name `rwb.p3.full-timeline` is kept as the legacy reference. In the target the switch is a parameter read through the parameters contract: off means SCR-03 shows the timeline of RWB-E1-035 and the operation answers the same earlier view.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P3-E2016-CON stay green, the 4,000-item case returns its first 50 items inside 2 s at the 95th percentile over 20 runs, and no item of a type the caller may not read appears in any answer.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-019 | No item matches the filter | Nothing on this case matches the filter. |
| MSG-GEN-006 | A source module does not answer in time | {system} is not available. Your request is queued and will be retried. |
| MSG-GEN-003 | Date to is before date from | {field} cannot be before {other}. |
| MSG-GEN-002 | Page size outside 1 to 200, or a type outside the seven | {field} must be between {min} and {max}. |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. |
| MSG-P4-002 | A role without Case record R opens the timeline | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | No session (401, section 12.1) | Not specified in the source documents (DOR-RWB-P3-E2016-APP-9) |

For MSG-GEN-006 in this story, {system} is the display name of the missing source as the screen shows it, "Document hub" for rwb-document, "Decision log" for rwb-decision, "Notice hub" for rwb-comms and "Interaction ledger" for rwb-source-data. For MSG-GEN-003 the fields are "to" and "from"; for MSG-GEN-002 the field is "size" or "type". MSG-P3-019 is new in the legacy story and keeps its text. Thai text follows DL10. Open decisions DL10 (assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863) and DL26 (assumptions ASM-0247, ASM-0264, ASM-0275, ASM-0355) apply and remain open; each assumption is accepted and used as stated.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-04 Case timeline | Loading | Sees skeleton rows while the composite route answers |
| SCR-04 Case timeline | Filtered | Filters by type and date; pages through a long history; opens a decision, a document or a notice; reads the queue history |
| SCR-04 Case timeline | Empty | Reads MSG-P3-019 when nothing matches, with the filters still shown |
| SCR-04 Case timeline | Error | Not specified in the source documents (CG-ALL-4247) |
| SCR-04 Case timeline | No access | Not specified in the source documents (CG-ALL-4247) |
| SCR-03 Case record | Read only | Opens the timeline from the record |
| SCR-03 Case record | Loading | Not specified in the source documents (CG-ALL-4246) |
| SCR-03 Case record | Empty | Not specified in the source documents (CG-ALL-4246) |
| SCR-03 Case record | Error | Not specified in the source documents (CG-ALL-4246) |
| SCR-03 Case record | No access | Not specified in the source documents (CG-ALL-4246) |

Both screens are served by the gateway-bff composite route, which calls rwb-case and the other owners in parallel, one hop each, and merges the answers into the screen model (DP-19). The browser calls one composite route and no owner service directly. The route path, the screen field list, the field-level masking of the screen model and the merge order are Not specified in the source documents (GAP-0674; ASM-1221); the route itself is owned by RWB-PLT-N001-CON and the full read-only case view with its other sections remains with RWB-P3-E1023-APP.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-016-01 | AC1, BR1, BR2 | End to end | 30 items over seven types; 20 timed runs |
| TC-E2-016-02 | AC2, BR5 | End to end | Filter DECISION over the AC1 case |
| TC-E2-016-03 | AC3, BR4 | End to end | One allocation and three transfers with reasons R05, R06, R01 |
| TC-E2-016-04 | AC4 | End to end | Date filter 2026-12-05 to 2026-12-08 |
| TC-E2-016-05 | AC5, BR3 | End to end | RW-PHONECOL on the AC1 case |
| TC-E2-016-06 | AC6, BR7, BR10 | End to end | Stubbed rwb-document query delayed 3 seconds |
| TC-E2-016-07 | AC7, BR8, BR15 | End to end | From 2026-12-10, to 2026-12-01; then size 500; then type "CONTACT" |
| TC-E2-016-08 | AC8 | End to end | NOTICE filter in November |
| TC-E2-016-09 | AC9 | End to end | Assignment with no queue |
| TC-E2-016-10 | AC10 | End to end | Case of team SME-NTH |
| TC-E2-016-11 | AC11, BR9 | End to end | 4,000 synthetic items, page size 50 |
| TC-E2-016-12 | Access, BR13 | Component | RW-REFADM (no Case record right) calls the timeline; refused with MSG-P4-002 |
| TC-E2-016-13 | Contract of section 12 | Contract | Operations of section 12.1 and the consumed operations of section 12.2 |
| TC-E2-016-14 | Boundary of section 12.7, ASM-3438 | Component | Boundary rows of each table of section 12.7 |
| TC-E2-016-15 | AC12, BR6, BR11, BR12, BR14 | Component | Not specified in the source documents (NEWAC-RWB-P3-E2016-APP-AC12) |
| TC-E2-016-16 | AC13 | Contract | Not specified in the source documents (NEWAC-RWB-P3-E2016-APP-AC13) |
| TC-E2-016-17 | AC14 | Component | Not specified in the source documents (NEWAC-RWB-P3-E2016-APP-AC14) |

The legacy levels map System to End to end and Access to Component, because this story carries the whole read and the cross-service journeys of the key are asserted again by RWB-ITG-E2016-ITG, which holds the `-ITG` copy of each case. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the type list, the labels, the reason codes, the timeout and the page size bounds are rows and parameters (BR14).
- No personal data in logs, tests or prompts. Summaries are built from codes; a contact summary is masked by role, never logged and never returned unmasked; test data is synthetic and no production case, party, notice or document is copied.
- No read of another service's tables: decisions, documents, notices and contacts come only through the P7, P5, P6 and P1 contracts, and `interaction` is not a table of `rwb_case` (BR11, DP-01, DP-18).
- No ACE view is read: the timeline needs no ACE data, and only rwb-source-data reads the `recovery.v_ace_*` views (ADR-010).
- One hop, no chaining: the timeline never calls a downstream of a downstream, and the breaker and bulkhead are per downstream (DP-11).
- The timeline never writes: it does not copy another service's records into `rwb_case`, does not project the history and raises no event (BR13).
- A role without a right sees fewer items, never an error and never another role's items (BR3, BR12).
- The case number and the case ID on the screen come from the case contract, never from a copy.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-008 | Queue and transfer history visible on the case | Business Requirements Epic 2, sections 3.3 and 4; Program, section 5.3 | FEAT-WKM-08, FEAT-WKM-09 | 06 Take over and own the case | R-UNI-24; CTL-09; CTL-11 | TC-E2-016-01 to TC-E2-016-14 |
| REQ-OCC-008 | History timeline of every state change, transfer, contact, document and decision | Business Requirements Epic 2, sections 3.3 and 4 | FEAT-WKM-08, FEAT-WKM-09 | 06 Take over and own the case; All recovery processes | None | TC-E2-016-01, TC-E2-016-04 |
| REQ-CWC-016 | Every allocation, assignment, transfer and timer event is logged with the rule ID and the rule version that caused it | Business Requirements Epic 1, section 4 | FEAT-WKM-09 | 06 Take over and own the case | BR4 | TC-E2-016-03 |
| REQ-DRI-002 | The decision log is append only; a correction is a new record naming the one it corrects | Business Requirements Epic 1, section 4 | FEAT-WKM-08 | 06 Take over and own the case | BR5; R-UNI-24 | TC-E2-016-02 |
| REQ-WKM-014 | The next action is visible on the case record and in every queue view | Business Requirements Epic 2, section 4 | FEAT-WKM-08 | 06 Take over and own the case | None | None (out of scope, section 19) |

### 19. Out of scope

- The next action on the case and in every queue view (REQ-WKM-014, RWB-E2-035).
- The clocks and deviations panels (RWB-P3-E2015-APP).
- The decision log query screen for audit (SCR-38, P7).
- The accounts, parties and collateral sections of the record view (RWB-E1-023, P4 FEAT-ACA-12).
- The document metadata, its intake and its content (RWB-P5-E2016-APP and the P5 stories); this story reads metadata only.
- The decision, notice and interaction-ledger contracts themselves, their schemas and their fakes as artefacts (the P7, P6 and P1 CON stories).
- The gateway-bff composite route, its path and its merge order (RWB-PLT-N001-CON).
- The rights, roles, scope and masking policy data themselves (the P4 access stories).
- The deployment of this capability: chart values, topic and queue provisioning, dashboards and the runbook (RWB-P3-E2016-OPS).
