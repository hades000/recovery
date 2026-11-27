# RWB-P3-E2014-APP Approval screen for D7.1 demand and recall notices

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2014-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-014 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP19 |
| Parallel lane | L-P3-AG |
| Ready to start | Day 1 |
| Size | Not set in this story; Not specified in the source documents (DOR-RWB-P3-E2014-APP-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-P7-E2014-CON, RWB-P1-E1015-CON, RWB-P3-E1018-CON; P6 notice generate and send and the rwb-case stage answer as non-blocking C rows, IDs Not specified in the source documents (GAP-2742) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (no FR mapped to REQ-APD-002, REQ-APD-006) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-014 for rwb-case, secondary slice. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P3-E2014-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 43 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF), legal counsel (RW-LEGAL) and head of litigation (RW-HEADLIT) who decide a D7.1 demand or recall notice, and the case owner (RW-CASEOWN) who must act on the outcome**, I want **rwb-case to serve the case facts behind the approval screen — case number, product group, stage, route, status, owner and entry date, the balance and arrears facts each with its as-of date and its age in days, and only for a case my role may read in my scope — and to raise one redress task on the case in the case owner's queue when a notice is refused or returned**, so that **the approver decides on facts that carry their own dates, and a refused notice becomes work somebody owes instead of a message somebody read**.

This is the secondary `rwb-case` slice of legacy RWB-E2-014. It owns no legacy criterion; AC1 to AC10 stay with `rwb-decision` (RWB-P7-E2014-APP) for the approval and with `rwb-access` (RWB-P4-E2014-APP) for the rights.

- Service `rwb-case`, schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1`, task queue `rwb-case` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.case`.
- Contract version: the rwb-case OpenAPI contract (`rwb-case.yaml`) and AsyncAPI contract (`rwb-case.asyncapi.yaml`) at version 5.0.0 of Recovery Workbench API Specification v5; the REST base and the topic are the v1 contract.
- It delivers three things: the case-facts projection of the case read behind the panel, with one `inputAsOf` element per input carrying its business date and age in days; the case-side right and scope answer taken from the `rwb-access` authorise contract before a field is rendered; and the outcome — one redress task on the case from `rwb.decision.ApprovalRefused.v1` or `rwb.decision.ApprovalReturned.v1`, assigned to the case owner with the reason or question, plus its trace on the case timeline.
- It builds no screen and moves no case status. SCR-10, SCR-11 and SCR-18 are `rwb-decision`'s and are composed by gateway-bff; the notice, its template version and the three notice operations are `rwb-comms`'s; the approval, the decision entry and the input age limits are `rwb-decision`'s; the access decision and the masking are `rwb-access`'s; the ACE balance, arrears and contact facts and the interaction ledger are `rwb-source-data`'s. The status move out of `WAITING_APPROVAL` and the resume state of the routing rule are RWB-P3-E2013-APP's.
- The two outcome event names are Not specified in the source documents (GAP-2216; ASM-3643): the catalogue lists `ApprovalRequested` and the decision record, so this slice names one event per outcome and confirms the names against RWB-P7-E2014-CON.
- The redress task's code, element type, assignment reason, due time and its notice and approval references are Not specified in the source documents (GAP-2216; ASM-3644); the story names the task by the notice it comes from and reads every other value from reference data.

The legacy values are unchanged: case `RW-2026-000123`, product `MORTGAGE`, approval `A-0201`, notice `N-0201`, template `DEMAND-MTG` version 2, rule `R-LIT-03` version `LIT-2026.12`, prepared by `U-9211`, decided on 14 December 2026, the total balance of business date 13 December 2026 and of 11 December 2026 when it is 3 days old, and the refusal reason "Addressee is a guarantor; a guarantor notice is needed".

### 2. Business rationale

A demand fee notice sent on a stale balance is a Bank of Thailand finding, and a refusal nobody acts on is the same finding one step later: the notice is blocked, the case sits, and the reason lives in a screen nobody reopens. The legacy story read the case, the balance, the approval and the queue in one process, so the age of a fact and the task of a refused notice were free. In the target that transaction is gone: `rwb-case` owns the case and its tasks in `rwb_case`, `rwb-source-data` owns the ACE facts with their business dates, `rwb-access` owns the right and the scope, `rwb-decision` owns the approval and the age limits, and gateway-bff composes the screen from the owners one hop each (Architecture v5 slides 10, 14 and 17).

The two things the case service alone can guarantee are therefore this slice's value: the panel tells the truth about how old each fact is, and a refused or returned notice becomes a task on the case with an owner and a reason. Neither can be lost to a service that is not built yet, and neither depends on the approval being live on the same day.

It serves REQ-APD-002 (the approver sees the inputs used, with their dates, on one screen) and REQ-APD-006 (demand and recall notices are approved through approval routing, and a refusal returns the case to its owner) on the case side, and supports CTL-14 (only an approved notice is dispatched, so the refusal must be visible) and CTL-05 (the preparer cannot decide, which `rwb-decision` enforces). The measure is notices sent with an approval entry, target 100 percent; the case-side measure this slice adds is every refused notice with a redress task on its case.

The realignment changes the mechanism and not the rule: the in-process case read and `RecoveryAccessGuard` become the published case contract on `/api/recovery/case/v1` (DP-13, DP-11) and the cached authorise answer of `rwb-access` (DP-08 as consumed); the ACE facts come from `rwb-source-data`'s reads with `data_as_of` (DP-05); and the refusal task becomes one `task` row and one `assignment` row in `rwb_case`, written in one transaction with the local decision record of DP-03 from an outcome read through the inbox of DP-09.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P7-E2014-CON | The published screen contract tested here: the case facts field list, the `inputAsOf` element with `inputCode`, `businessDate` and `ageDays`, the input codes `TOTAL_BALANCE` and `POSTAL_ADDRESS`, the screen states and the fakes. The field-level shape is Not specified in the source documents (GAP-2216; ASM-3645) |
| The `rwb_case` baseline | `recovery_case`, `task`, `assignment`, `reference_version`, `reference_row`, `parameter_catalog`, `parameter_value`, and the outbox, inbox and idempotency objects, with the per-service Flyway sequence of DP-15 running in `rwb_case` |
| The case contract of the service | `GET /cases/{caseId}` (API-P3-002) and `GET /cases/{caseId}/timeline` (API-P3-003) published on `/api/recovery/case/v1` with their shapes and errors; the projection this story adds narrows the case answer under that contract |
| The `rwb-access` authorise contract | `POST /api/recovery/access/v1/authorise` with the cached right and scope answer, the refusal MSG-P4-002 and the out-of-scope answer MSG-P4-003. This contract carries no C row in this key and its request and answer shape is Not specified in the source documents (GAP-2216; ASM-3648) |
| The `rwb-source-data` contract | The account and customer reads with `data_as_of` and the freshness read for the business date in force (DP-05, RWB-P1-E1015-CON); how the postal address input's business date is read is Not specified in the source documents (GAP-2216; ASM-3646) |
| The `rwb-decision` outcome events | One event per outcome on `rwb.decision.events.v1` carrying the approval, the notice, the case, the final call, the reason or question and the record reference; names Not specified (GAP-2216; ASM-3643) |
| The decision-record library | `rwb.decision-record.v1` and DP-03, so the task raise is written, chained and published in one transaction with the task and the assignment |
| Reference data and parameters | LOV-ELEMENT, LOV-TASK-STATUS, LOV-ROLE and LOV-ASSIGN-REASON with the version in force through DP-07, and the case-side switch through DP-06; the age limits stay `rwb-decision`'s rows |
| The gateway-bff composite route | The DP-19 route that carries the case read, the authorise call and the timeline read to this base path, one hop and 2 s per downstream (DP-11) |
| Test users in SIT | `U-9211` holds `RW-LEGAL` and prepared `N-0201`; `U-9212` and `U-9214` hold `RW-LITOFF`; `U-9213` holds `RW-HEADLIT`; `U-9215` holds `RW-CASEOWN` and owns the case; `U-9216` holds `RW-AUDIT` with scope `ALL`; `U-9217` holds `RW-PHONECOL` with no Litigation and no Case record right |

Carried business preconditions:

- Case `RW-2026-000123` exists with product group `MORTGAGE`, status `WAITING_APPROVAL` while `A-0201` waits, an owner, a stage, a route and an entry date.
- The total balance is an ACE fact with a business date: 13 December 2026 in the background and 11 December 2026 for the stale case, 3 days old on 14 December 2026 against the 1 day limit `rwb-decision` holds.
- The limits `rwb.decision.input-age-days.TOTAL_BALANCE` = 1 and `rwb.decision.input-age-days.POSTAL_ADDRESS` = 30 (assumed, owner RW-COE; DL22) are `rwb-decision`'s parameter rows; this story neither reads nor compares them.
- A D7.1 notice carries no amount limit, so no `delegation_limit` row is read on this path and the panel shows no limit.
- Open decisions: DL10 (assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863) and DL22 (assumptions ASM-1162, ASM-1304, ASM-2217, ASM-2569) are still open, and each has an assumption.

### 4. Flow

1. Litigation officer: opens SCR-10 Approval queue through the gateway-bff route and selects the D7.1 item of approval `A-0201` for notice `N-0201` on case `RW-2026-000123`.
2. gateway-bff: composes SCR-11 with the SCR-18 panel and calls `GET /api/recovery/case/v1/cases/{caseId}` on this service, one hop, with the caller's session and a 2 s budget (DP-19, DP-11).
3. `AuthoriseCheck`: calls `POST /api/recovery/access/v1/authorise` with the caller, the area `Case record`, right `R` and the case as the object, and holds the answer for the life of the cache entry.
4. `AuthoriseCheck`: refuses with 403 MSG-P4-002 when the answer carries no right, and with 404 MSG-P4-003 when the case is outside the scope; no case fact is read or returned on a refusal.
5. `CaseFactsProjection`: reads `recovery_case` by ID and returns the case number, product group, stage code, route state, route code, status, owner reference and entry date, with days past due at entry, total outstanding at entry and exposure band.
6. `SourceDataClient`: reads the account read for the current total balance and days past due with `data_as_of`, and the customer read for the contact fact the postal address input comes from; the address value itself is never read, echoed or cached here (DP-05).
7. `InputAgeService`: for each input, computes the age in days from that input's business date to the ACE business date in force (the freshness read) and returns one `inputAsOf` element with `inputCode`, `businessDate` and `ageDays`; the only codes are `TOTAL_BALANCE` and `POSTAL_ADDRESS`.
8. The answer carries the case facts and `inputAsOf` only: no approval status, no notice body, no template code, no rule version and no limit, because those are other owners' facts and the route merges them from their own answers.
9. `rwb-decision`: the officer refuses `A-0201` with the legacy reason, or returns it with a question; the approval, its decision entry and the notice hold stay `rwb-decision`'s and `rwb-comms`'s.
10. `rwb-decision`: publishes the refusal or return event on `rwb.decision.events.v1` with the approval, the notice, the case, the final call, the reason or question and the record reference (GAP-2216; ASM-3643).
11. `NoticeOutcomeListener`: reads the event into the inbox of DP-09, deduplicates by event ID (R-UNI-40) and calls `signalWithStart` on `CaseWorkflow` with workflow ID equal to the case ID, on task queue `rwb-case`.
12. `raiseRedressTask`, one `RecordAndApply` transaction in `rwb_case`: reads the element type, task status and role values through DP-07; writes the `task` row with the task code for a notice redress, the notice and approval references, status OPEN, `owner_role` and the due time of the reference row; writes one `assignment` row naming `recovery_case.owner_user_id`; writes the local decision record of DP-03 with the approval, the notice, the final call and the reason code; writes the outbox row (GAP-2216; ASM-3644).
13. The case status is not written here: RWB-P3-E2013-APP moves the case and writes the resume state of its routing rule from the same outcome.
14. Case owner (`U-9215`): sees the redress task in the work list with the reason or question and the notice reference; the task carries no notice body and no address.
15. Any caller with Case record R in scope: opens SCR-04 and sees the outcome as the decision item of `rwb-decision`'s ledger read and the task item of `task`, newest first, with the final call, the reason code and the time and no notice content.
16. A repeat of the same event is dropped by the inbox; a closed case records the event and raises no task; a transaction that cannot write the record changes nothing and the event stays on the topic for redelivery.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The caller holds no Case record right | 403 before any fact is read; the answer names the action and the area and carries no case fact | MSG-P4-002 | AC3 |
| X2 | The case is outside the caller's scope | 404; no case number, product, balance or owner is returned and the case is not read | MSG-P4-003 | AC3 |
| X3 | The account or customer read does not answer inside 2 s | The panel serves the case facts it has and marks that input's date and age as unavailable; no fact is shown as current | MSG-GEN-006 | AC2 |
| X4 | The data product answers with an older business date | The as-of date and the age in days are returned as they are; the refusal of the approval is `rwb-decision`'s | MSG-P7-006 (P7) | AC2 |
| X5 | The refusal or return event arrives twice | One task; the second delivery is recorded in the inbox and raises nothing | None | AC6 |
| X6 | The event arrives for a closed case | No task and no status change; the mismatch is recorded on the activity with the case and event IDs | None | AC8 |
| X7 | The local decision record cannot be written | Nothing changes: no task, no assignment, no outbox row; the event is redelivered | MSG-P7-003 | AC8 |
| X8 | A stale case version at commit | MSG-GEN-004 and a retry; no second task is raised | MSG-GEN-004 | AC6 |
| X9 | The authorise contract does not answer | The read is refused as unavailable and no fact is returned from an unanswered check | MSG-GEN-006 | AC3 |
| X10 | The notice reference is missing from the event | The task is raised without a notice reference, the gap is recorded, and no reason is dropped | None | AC4 |
| X11 | The readiness of a fact is unknown because its business date is absent | The input is answered as unavailable, never as current | None | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against the published RWB-P7-E2014-CON and the case, access, source-data and decision contracts with their fakes; the approval and the notice are facts of the event, never a table read |
| Negotiable | The task code, element type, role, assignment reason and due time are data; the story fixes only the facts projection, the age rule and the one-task rule |
| Valuable | The approver sees how old every fact is, and every refused notice becomes a task with an owner and a reason |
| Estimable | One projection with an input-age list, one authorise call, one listener, one activity, one task and assignment write, one index migration |
| Small | Fits one week with its tests and within two weeks, because the screen, the approval, the notice and the access decision belong to other stories |
| Testable | Each criterion is one test case in section 16; the approval, notice and access facts come from the contract mocks |

### 7. Acceptance criteria

```gherkin
Feature: Case facts and the refused-notice redress task behind the D7.1 approval screen

  Background:
    Given the environment is SIT
    Given case "RW-2026-000123" exists with product group "MORTGAGE", status "WAITING_APPROVAL", stage "LITIGATION", route "R6", an owner and entry date 1 December 2026
    Given test user "U-9212" holds RW-LITOFF, "U-9215" holds RW-CASEOWN and owns the case, "U-9216" holds RW-AUDIT with scope "ALL" and "U-9217" holds RW-PHONECOL
    Given the rwb-access contract mock returns allowed for area "Case record", right "R" and case "RW-2026-000123" in scope
    Given the rwb-decision contract mock returns approval "A-0201" of notice "N-0201" for case "RW-2026-000123", waiting for role RW-LITOFF
    Given the rwb-source-data contract mock returns the total balance with data_as_of 13 December 2026 and the ACE business date in force 14 December 2026

  Scenario: AC1 The panel is served the case facts of the case (new, D-RCV-60)
    Given the rwb-access contract mock returns allowed for area "Case record", right "R"
    When "U-9212" opens "A-0201" and the composite route calls GET /api/recovery/case/v1/cases/RW-2026-000123
    Then the answer carries case number "RW-2026-000123", product group "MORTGAGE", stage "LITIGATION", route "R6", route state and status "WAITING_APPROVAL"
    Then the answer carries the case owner reference, entry date 1 December 2026, days past due at entry, total outstanding at entry and the exposure band
    Then the answer carries no approval status, no notice body, no template code, no rule version and no input age limit

  Scenario: AC2 Every fact carries its as-of date and its age in days (new, D-RCV-60)
    Given the rwb-source-data contract mock returns the total balance with data_as_of 13 December 2026
    When the case facts panel is read on 14 December 2026
    Then the total balance is answered with as-of date 13 December 2026 and age 1 day
    Then the postal address input is answered with its own business date and its age in days and with no value of the address
    When the rwb-source-data contract mock returns the total balance with data_as_of 11 December 2026
    Then the total balance is answered with as-of date 11 December 2026 and age 3 days
    Then no limit and no stale flag is computed or returned by this service

  Scenario: AC3 The case right and the case scope gate the panel (new, D-RCV-60)
    Given the rwb-access contract mock returns refused for area "Case record", right "R" for "U-9217"
    When "U-9217" asks the case facts panel of case "RW-2026-000123"
    Then the call is refused with status 403 and message MSG-P4-002 for area "Case record"
    Then the answer carries no case number, no product group, no balance, no arrears fact and no owner
    Given the rwb-access contract mock returns allowed for area "Case record", right "R" and the case outside the caller's scope
    When "U-9217" asks the case facts panel again
    Then the call answers 404 with message MSG-P4-003 and reads no case row

  Scenario: AC4 A refused notice raises one redress task in the case owner's queue (new, D-RCV-60)
    Given the rwb-decision contract mock publishes rwb.decision.ApprovalRefused.v1 for approval "A-0201", notice "N-0201" and case "RW-2026-000123" with final call "REFUSED" and reason "Addressee is a guarantor; a guarantor notice is needed"
    When the case router reads the event at 10:05 on 14 December 2026
    Then one task exists on case "RW-2026-000123" with notice reference "N-0201", approval reference "A-0201", status "OPEN" and an element type from the reference list
    Then one assignment row names "U-9215" as the assignee of that task, taken from the case owner of the case
    Then the task carries the reason "Addressee is a guarantor; a guarantor notice is needed" and appears in the work list of "U-9215"
    Then the case status is unchanged and the local decision record names the approval, the notice and final call "REFUSED"

  Scenario: AC5 A returned notice raises the same task with the question (new, D-RCV-60)
    Given the rwb-decision contract mock publishes rwb.decision.ApprovalReturned.v1 for approval "A-0201", notice "N-0201" and case "RW-2026-000123" with final call "RETURNED" and the question "Attach the latest income statement"
    When the case router reads the event
    Then one task exists on case "RW-2026-000123" for notice "N-0201" with status "OPEN" and is assigned to "U-9215"
    Then the task carries the question "Attach the latest income statement"
    Then the case status is unchanged and no second task and no second assignment row is written

  Scenario: AC6 One outcome raises one task, however often the event arrives (new, D-RCV-60)
    Given a redress task already exists on case "RW-2026-000123" for notice "N-0201" from the same event
    When the same event is delivered again with the same event ID
    Then no second task and no second assignment row is written
    Then the inbox holds one processed row for the event and the repeat is counted
    When a stale case version is met at commit
    Then the activity answers MSG-GEN-004 and retries, and the case still has exactly one open redress task

  Scenario: AC7 The case timeline shows the outcome with no notice content (new, D-RCV-60)
    Given a redress task exists on case "RW-2026-000123" for notice "N-0201"
    Given the rwb-decision contract mock returns the decision entry of "A-0201" with final call "REFUSED" and the reason code for the case
    When "U-9215" opens the case timeline of "RW-2026-000123"
    Then the timeline shows the decision item of "A-0201" with its final call and time, newest first, before the task item
    Then the timeline shows the task item with the task code, the status and the notice reference
    Then neither item carries a notice body, a template content, an addressee or a value of the postal address

  Scenario: AC8 A task that cannot be recorded does not exist (new, D-RCV-60)
    Given the rwb-decision contract mock publishes an outcome event for case "RW-2026-000999" in status "CLOSED"
    When the case router reads the event
    Then no task is raised on that case, its status is unchanged, and the mismatch is recorded with the case and event IDs
    Given the decision-record library is stopped and the event arrives for case "RW-2026-000123"
    When the activity runs
    Then no task, no assignment row and no outbox row is written and the case carries MSG-P7-003
    Then the event is redelivered and the task is raised once when the library answers

  Scenario: AC9 No business value is written in code and no postal address value leaves the service (new, D-RCV-60)
    Given the rwb-decision contract mock publishes rwb.decision.ApprovalRefused.v1 for approval "A-0201", notice "N-0201" and case "RW-2026-000123" with final call "REFUSED"
    When the case router reads the event
    Then the task code, element type, task status, owner role, assignment reason and due time are read from reference data with the version in force
    Then the panel, the task, the record and the timeline item carry the postal address field and no value of it
    Given the rwb-decision contract mock publishes an outcome event for case "RW-2026-000999" in status "CLOSED"
    When the case router reads the event
    Then no task is raised on that case and the mismatch is recorded

  Scenario: AC10 The provided operations answer 401 without a valid credential (new, D-RCV-60)
    Given the caller holds no valid credential
    When the composite route calls GET /api/recovery/case/v1/cases/RW-2026-000123
    Then the call is refused with status 401
    Then the answer carries no case fact

  Scenario: AC11 A retried or timed-out activity raises no second task (new, D-RCV-60)
    Given the rwb-decision contract mock publishes rwb.decision.ApprovalRefused.v1 for approval "A-0201", notice "N-0201" and case "RW-2026-000123" with final call "REFUSED"
    When the activity is retried after a stale case version is met at commit
    Then the activity retries and the case still has exactly one open redress task
    When the activity times out before its commit
    Then no task, no assignment row and no outbox row is written and the event is redelivered

  Scenario: AC12 A consumed call that fails or does not answer is refused and reads no fact (new, D-RCV-60)
    Given the rwb-access contract mock does not answer for area "Case record", right "R" and case "RW-2026-000123"
    When "U-9212" opens the case facts panel of case "RW-2026-000123"
    Then the call is refused and no case fact is read
    Given the rwb-source-data contract mock fails for the total balance of case "RW-2026-000123"
    When "U-9212" opens the case facts panel of case "RW-2026-000123"
    Then the answer carries no total balance and the failure is recorded with the case and the call
```

These criteria are the ones this slice owns; it owns no legacy AC, and legacy AC1 to AC10 are carried by `rwb-decision` (RWB-P7-E2014-APP) and `rwb-access` (RWB-P4-E2014-APP). Every value above is a legacy value of RWB-E2-014: the case, product, notice and approval, the balance of 13 December 2026 and of 11 December 2026 for the stale case, 14 December 2026 as the decision date, the refusal reason, the return question and the roles. The ages 1 day and 3 days are counted in calendar days from the input's business date to the ACE business date in force.

The projection field list, the `inputAsOf` element and the way the task is named are Not specified in the source documents (GAP-2216; ASM-3645) and (GAP-2216; ASM-3644); none of them is a business value and they are renamed at the contract review if the published contract differs.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The facts the D7.1 panel shows are `rwb_case` facts of this service and the balance and arrears facts of `rwb-source-data`'s contract; the notice, the approval, the rule version and the template version are other owners' facts and are never read or repeated here | REQ-APD-002; legacy s11; DP-01, DP-05 |
| BR2 | Every fact the panel shows carries the date it is true for, and every input carries its business date and its age in days counted from that date to the ACE business date in force; no fact of an older date is shown as current | REQ-APD-002; FSD P3 v4 A2.45; legacy AC5 ages |
| BR3 | Opening the case facts of a notice for approval needs Case record right R and the case in the caller's scope, answered by the `rwb-access` authorise contract; no right is 403 MSG-P4-002 and out of scope is 404 MSG-P4-003 before any fact is read | Legacy s10; FSD P3 v4 A2.45 AC-EXC-P3-045-03; TSD P3 v3 T6.1; DP-08 |
| BR4 | A refused demand or recall notice raises one task on its case, owned by the case owner, holding the reason and the notice reference, so the refusal becomes work and not a message | Legacy BR7 and AC3; REQ-APD-006; FEAT-APD-04 |
| BR5 | A returned notice raises the same task with the approver's question, and neither a refusal nor a return moves the case status in this story | Legacy AC9; RWB-P3-E2013-APP owns the status move |
| BR6 | One outcome raises one task: the event is deduplicated by event ID in the inbox, and a repeated delivery raises nothing | R-UNI-40; TSD P3 v3 T2.4 |
| BR7 | The outcome appears on the case timeline as the decision item of `rwb-decision`'s ledger read and the task item of `task`, newest first, and neither item carries a notice body, template content, an addressee or an address value | REQ-OCC-008; legacy AC3 and s17; NFR-040 |
| BR8 | A task raise that cannot be recorded does not take effect: task, assignment, local record and outbox row commit in one transaction, and a failure leaves the case unchanged and the event on the topic | Principle 5; R-UNI-39; DP-03 |
| BR9 | No business value is written in code: the task code, element type, task status, owner role, assignment reason and due time are reference data read with the version in force | FSD P3 v4 A2.45; DP-07; Template and Rules R7.2 s17 |
| BR10 | No personal data leaves this service: the panel, the task, the record and the timeline item carry the case number, codes, amounts and dates; the postal address is named as a field and never read as a value | Legacy s17; NFR-040 |
| BR11 | A closed case takes no redress task, and an outcome for a case that cannot take work is recorded as a mismatch rather than dropped in silence | FSD P3 v4 A2.3 VR-P3-003-1; R-UNI-20 |

How the rules hold in `rwb-case`:

- BR1 and BR2 are a read of `recovery_case` plus one call to the account and customer reads of `rwb-source-data` with `data_as_of`; the answer carries no field of `notice`, `approval`, `template` or `decision_log_entry`, and `InputAgeService` returns the business date as the read gives it with the difference in calendar days to the business date in force, and no limit and no stale flag.
- BR3 is one call to the authorise contract with a refusal by default: an unanswered or unparseable answer is a refusal, never an allow.
- BR4 and BR5 are one `task` row with `owner_role` and one `assignment` row naming `recovery_case.owner_user_id`; a case with no owner falls back to the case owner role, so a task is never invisible to everybody.
- BR6 is the inbox of DP-09 keyed by event ID plus a partial unique index that makes a second open task for one notice impossible.
- BR7 is the timeline read of API-P3-003, composing decision items from `rwb-decision`'s ledger read and task items from `task`; this story writes no ledger row, because the ledger is `rwb-source-data`'s under DP-18 (GAP-2216; ASM-3647).
- BR8, BR9, BR10 and BR11 are one `RecordAndApply` transaction with the record written last, the DP-07 read with the version in the record and no Java enum of task codes or statuses, a check on the answer and the record that the address is named `POSTAL_ADDRESS` and never valued, and a status check against LOV-CASE-STATUS read through DP-07.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| No task | The refusal or return event | The case is open and the event ID is new | One task OPEN, assigned to the case owner |
| Task OPEN | The case owner opens the task | None | Task IN_PROGRESS |
| Task IN_PROGRESS | The case owner completes it with an outcome | The outcome is a reference outcome | Task DONE with `completed_at` and `outcome_code` |
| Task OPEN or IN_PROGRESS | The case closes before the task is done | The case reaches a closed status | Task CANCELED with the reason |
| Task OPEN | The same event arrives again | The event ID is in the inbox | Unchanged; no second task |
| Any | The record cannot be written | None | Unchanged; MSG-P7-003; redelivery |

The task statuses are the LOV-TASK-STATUS values `OPEN`, `IN_PROGRESS`, `DONE` and `CANCELED`, read with the version in force through DP-07.

| From | Event | Condition | To |
|---|---|---|---|
| `CaseWorkflow` running | The outcome arrives through the case router | The event ID is new | `raiseRedressTask` scheduled |
| `raiseRedressTask` committed | Task, assignment, record and outbox written | None | Waiting on the next signal or stage |
| Waiting | Stage ends or 28 days pass | None | Continue-As-New with the same workflow ID |

The case status is in neither table: the move out of `WAITING_APPROVAL` and the resume state of the routing rule are RWB-P3-E2013-APP's.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF Litigation officer | Reads the case facts panel of a D7.1 notice for approval (Case record R, in scope); decides nothing here, because the approval is `rwb-decision`'s |
| RW-LEGAL Legal counsel | The same case read on the same notice, from the same answer |
| RW-HEADLIT Head of Litigation | The same case read on an item escalated to RW-HEADLIT |
| RW-CASEOWN Case owner | Reads the case facts (Case record R in scope) and receives the redress task of a refused or returned notice with its reason or question |
| RW-AUDIT Internal audit | Reads the case facts and the timeline with scope `ALL`, and the approval and ledger through `rwb-decision` |
| RW-PHONECOL and any role without Case record R | Refused with 403 and MSG-P4-002; no case fact is returned |
| SY-CASEWF, the `rwb-case` service identity | Consumes the outcome events, raises the task and the assignment, writes the local record and the outbox row |
| SY-DECLOG, the decision-record library identity | Writes the local record of the task raise and publishes it on `rwb.decision-record.v1` |

The access decision is `rwb-access`'s and is consumed on its authorise contract as the cached answer of DP-08; this story holds no permission, masking or delegation row. The preparer rule is not here: `rwb-decision` refuses the preparer with 409 and MSG-P7-002 before any outcome event exists, so a refused preparer raises no task in this service.

### 11. Data

| BR Field ID | Table in `rwb_case`, or owner | Field | Read or write |
|---|---|---|---|
| DF-CAS-002 | `recovery_case` | case_no | Read |
| DF-CAS-003 | `recovery_case` | product_group | Read |
| DF-CAS-005 | `recovery_case` | status | Read |
| DF-CAS-006 | `recovery_case` | stage_code | Read |
| DF-CAS-007 | `recovery_case` | route_state | Read |
| DF-CAS-008 | `recovery_case` | route_code | Read |
| DF-CAS-009 | `recovery_case` | owner_user_id | Read (assignee of the redress task) |
| DF-CAS-013 | `recovery_case` | entry_date | Read |
| DF-CAS-014 | `recovery_case` | dpd_at_entry | Read |
| DF-CAS-015 | `recovery_case` | exposure_band | Read |
| DF-CAS-016 | `recovery_case` | total_outstanding_at_entry | Read |
| DF-CAS-017 | `recovery_case` | prescription_date | Read |
| DF-CAS-001 and `version` | `recovery_case` | id, optimistic lock version | Read |
| DF-WRK-017 to DF-WRK-026 | `task` | task_code, element_type, owner_role, status, due_at, completed_at, outcome_code, case_id | Write (the redress task) |
| DF-WRK-009 to DF-WRK-016 | `assignment` | case_id, task_id, assignee_user_id, assigned_at, reason | Write (the assignee) |
| DF-ACE-020 | account read, `rwb-source-data` contract (DP-05) | total_balance and days past due with `data_as_of` | Read through the contract |
| DF-ACE-078 | customer read, `rwb-source-data` contract (DP-05) | the postal address input: its business date only; the value is never read, echoed or cached | Read as a date only |
| DF-REF-132 to DF-REF-184 | `parameter_catalog`, `parameter_value`, `reference_row`, `reference_version` | LOV-ELEMENT, LOV-TASK-STATUS, LOV-ROLE, LOV-ASSIGN-REASON and the case-side switch, version in force | Read through DP-06 and DP-07 |
| DF-DEC-001 to DF-DEC-018 | local decision record (DP-03) | decision code, actor, case and notice references, final call, reason code, time | Write |
| (inbox) | `processed_event` | event_id, consumer, processed_at | Write |
| (outbox) | outbox table in `rwb_case` | the record row and the notification row | Write |
| (idempotency) | `idempotency_key` | the stored answer of a repeated case read | Write |

No row of `notice`, `template` or `approval` is read or copied: the notice and approval references arrive in the outcome event and are stored as references on the task, and their content stays in `rwb-comms` and `rwb_decision`. The interaction ledger is `rwb-source-data`'s under DP-18 and this story writes no ledger row (GAP-2216; ASM-3647). The task's own naming is Not specified in the source documents (GAP-2216; ASM-3644). Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

None new. The facts projection is served through the existing case operations of owner P3 `rwb-case` on base `/api/recovery/case/v1`; this story adds no path, no query parameter and no error code.

| ID | Method | Path | Purpose in this story | Authorization | Errors |
|---|---|---|---|---|---|
| API-P3-002 | GET | `/api/recovery/case/v1/cases/{caseId}` | One case with the facts projection and `inputAsOf[]`: `caseNo`, `productGroup`, `stageCode`, `routeState`, `routeCode`, `status`, `ownerRef`, `entryDate`, `dpdAtEntry`, `totalOutstandingAtEntry`, `exposureBand`, `prescriptionDate`, `inputAsOf[]` | Case record R, scope applied through the authorise contract | 401; 403 MSG-P4-002; 404 MSG-P4-003; 503 MSG-GEN-006 |
| API-P3-003 | GET | `/api/recovery/case/v1/cases/{caseId}/timeline` | The outcome as a decision item and a task item, newest first, with type, actor, time and reference | Case record R, scope applied | 401; 403 MSG-P4-002; 404 MSG-P4-003; 503 MSG-GEN-006 |

Each `inputAsOf` element is `inputCode`, `businessDate` and `ageDays`, one element per input, with the two codes `TOTAL_BALANCE` and `POSTAL_ADDRESS` and no other. The route's `inputFacts` element takes `businessDate` and `ageDays` from this answer and `limitDays` and `stale` from `rwb-decision`'s answer, so no limit is computed twice. The field-level type and order of the projection are Not specified in the source documents (GAP-2216; ASM-3645). The work list of a case owner is served by the existing `GET /api/recovery/case/v1/me/tasks` operation and the queue views by RWB-P3-E2011-APP.

#### 12.2 REST operations consumed

| Method and path | Owner | Use in this story |
|---|---|---|
| POST `/api/recovery/access/v1/authorise` | P4 `rwb-access`, RWB-P4-E1037-CON | The Case record right and the scope of the caller for the case, before any fact is read; the contract carries no C row in this key and its shape is Not specified in the source documents (GAP-2216; ASM-3648) |
| GET `/api/recovery/source-data/v1/accounts/{accountId}` | P1 `rwb-source-data`, DP-05 | The current total balance and days past due of the primary account with `data_as_of`, one hop, 2 s |
| GET `/api/recovery/source-data/v1/customers/{customerId}` | P1 `rwb-source-data`, DP-05 | The contact fact the postal address input comes from: its business date only. Which field carries that date is Not specified in the source documents (GAP-2216; ASM-3646) |
| GET `/api/recovery/source-data/v1/data-products/freshness` | P1 `rwb-source-data`, RWB-P1-E1015-CON | The ACE business date in force, against which each input's age is counted |
| GET `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 `rwb-decision` | The decision items of the case for the timeline read: final call, reason code, approver reference, time. No approval, notice or template content is read |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (DP-11, ADR-020). No row reads a table of another service, and this story adds no `v_ace_*` read of its own (GAP-2216; ASM-3646).

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | caseId | the hash-chained record of the task raise: decision code, actor, case, notice and approval references, final call, reason code, time |

CloudEvents 1.0 envelope with identifiers, codes and dates and no personal data and no notice content; written to the outbox in the same transaction as the task and the assignment and relayed by the library (DP-03, DP-09). This slice publishes nothing on `rwb.case.events.v1`: the status move that would publish `rwb.case.CaseStateChanged.v1` is RWB-P3-E2013-APP's.

#### 12.4 Events consumed

| Event | Topic | Owner | Handler |
|---|---|---|---|
| `rwb.decision.ApprovalRefused.v1` | `rwb.decision.events.v1` | P7 | Case router, inbox dedupe by event ID, `signalWithStart` of `CaseWorkflow`, then `raiseRedressTask` |
| `rwb.decision.ApprovalReturned.v1` | `rwb.decision.events.v1` | P7 | The same path, with the approver's question on the task |

Both names are Not specified in the source documents (GAP-2216; ASM-3643): one event per outcome keeps a refusal and a return apart; a rename is a contract change of RWB-P7-E2014-CON and changes nothing in this story's behaviour. `ApprovalRequested` is RWB-P3-E2013-APP's and is not consumed here.

#### 12.5 Workflows and activities

| Name | Kind | Queue | Note |
|---|---|---|---|
| `CaseWorkflow` | Parent workflow, one per case, workflow ID = case ID | `rwb-case` | The case service's existing workflow; this story registers one activity on it and starts no workflow of its own |
| `raiseRedressTask` | Activity | `rwb-case` | Status and reference checks, task and assignment write, the local record and the outbox in one transaction |
| `RecordAndApply` | Activity, from the kit | `rwb-case` | Writes the record and the outbox rows with the task write in one transaction |

The activity input is the case reference, the notice reference, the approval reference, the final call and the reason or question; it carries no notice body, no addressee and no personal data.

#### 12.6 Schedules

None. This story adds no Schedule and reads no scheduler table: the task due time comes from the reference row of its task code, and the case clocks are this service's own `timer` rows read by `GET /cases/{caseId}/timers` (DP-10).

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `recovery_case` | P3 (`rwb_case`) | The case facts, the owner reference and the optimistic lock version; read only, no status write |
| `task` | P3 (`rwb_case`) | The redress task of a refused or returned notice |
| `assignment` | P3 (`rwb_case`) | The one assignee row naming the case owner for that task |
| `lov_value`, `reference_row`, `reference_version` | P3 (`rwb_case`) | Element type, task status, role and assignment reason lists, read through DP-07 |
| `parameter_catalog`, `parameter_value` | P3 (`rwb_case`) | The case-side switch, read through DP-06 |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, in `rwb_case` | Outbox, inbox and idempotency objects (DP-09) |

`notice`, `template` and `merge_field` are P6's, `approval` and `decision_log_entry` are P7's, `permission`, `masking_rule` and `delegation_limit` are P4's, `interaction` is P1's and `document` is P5's; none is read and no foreign key crosses a schema (DP-01). The task holds the notice and approval references as values.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-decision outcome WireMock | RWB-P7-E2014-CON | `ApprovalRefused` for `A-0201` and `N-0201` on case `RW-2026-000123` with final call `REFUSED` and the guarantor reason; `ApprovalReturned` with the question "Attach the latest income statement"; a repeat of each with the same event ID; an outcome for the closed case `RW-2026-000999`; the decision-log read with the decision item of `A-0201` |
| rwb-access authorise fake | RWB-P4-E1037-CON | Allowed for `RW-LITOFF`, `RW-LEGAL`, `RW-HEADLIT`, `RW-CASEOWN` and `RW-AUDIT`; refused for `RW-PHONECOL`; the out-of-scope answer; an unanswered call beyond 2 s |
| rwb-source-data fake | RWB-P1-E1015-CON and the account and customer reads | The total balance with `data_as_of` 2026-12-13 for the background and 2026-12-11 for the stale case; the days past due; the customer read's business date; the freshness row of ACE business date 2026-12-14; a delayed answer |
| decision-record fake | RWB-PLT-E1027-CON | A healthy chain and outbox, and a stopped library for AC8 |
| gateway-bff route fake | RWB-PLT-N001-CON | The composite route carrying the case read, the authorise call and the timeline read, so the panel's own calls can be asserted |

The fakes use the legacy values of RWB-E2-014 section 7 unchanged, so component and integration assertions read the same fixtures.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 0 new (2 existing case operations used), consumed 5 | API-P3-002 and API-P3-003 on `/api/recovery/case/v1`; the authorise, the two source-data reads, the freshness read and the decision-log read consumed, one hop and 2 s each |
| Kafka | Published 1 through the library, consumed 2 | `rwb.decision-record.v1` published; the two `rwb-decision` outcome events consumed from `rwb.decision.events.v1`; nothing published on `rwb.case.events.v1` |
| Temporal | 1 existing workflow, 1 new activity | `CaseWorkflow` with `raiseRedressTask` and the kit's `RecordAndApply` |
| File | None | No file is read or written; the notice PDF is a document reference held by `rwb-comms` and `rwb-document` |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `case/noticefacts`, Java package `th.co.scb.ace.workbench.recovery.case.noticefacts`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

Instances in this slice: DP-01 is the read of `recovery_case` and the writes to `task` and `assignment`; DP-03 is the local record of the task raise; DP-05 is the balance, arrears and contact business dates read on the `rwb-source-data` contract and never from a `v_ace_*` view; DP-06 is the case-side switch; DP-07 is the LOV-ELEMENT, LOV-TASK-STATUS, LOV-ROLE and LOV-ASSIGN-REASON read; DP-09 is the inbox, the outbox and the idempotency key; DP-10 is the existing `CaseWorkflow` that receives the outcome, with no Schedule; DP-11 is the authorise call and the three source-data calls with mocks and the 2 s budget; DP-13 is the base path; DP-19 is the composite route.

DP-08 is relied on without being declared: the authorise answer is consumed on the `rwb-access` contract as one hop (DP-11) and this story adds no guard library and no permission row (GAP-2216; ASM-3648). The metadata H row is None because the platform contracts the DP rows name — the decision-record, parameters, reference-data, outbox and inbox, workflow-kit and composite-route contracts — are pulled by the `rwb-case` baseline stories this slice builds on; the slice is therefore Day 1 and builds against RWB-P7-E2014-CON and its fakes.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseFactsController | REST controller | The facts projection and `inputAsOf[]` on API-P3-002 and the problem responses with their message IDs |
| CaseFactsProjection | Service | The case facts and arrears facts of `recovery_case`, the owner reference and the version lock |
| InputAgeService | Service | One `inputAsOf` element per input: business date from the read and age in calendar days to the business date in force; no limit and no stale flag |
| SourceDataClient | Adapter | The account and customer reads and the freshness read, one hop, 2 s, breaker, GET retried once with jitter |
| AuthoriseCheck | Client | The Case record right and the scope answer of `rwb-access`, cached, refusing closed |
| NoticeOutcomeListener | Kafka consumer with the inbox | The refusal and return events, deduplicated by event ID, `signalWithStart` on `CaseWorkflow` |
| RaiseRedressTaskActivity | Temporal activity | Status and reference checks, task and assignment write, local record and outbox in one transaction |
| RedressTaskService | Service | The task code and due time from reference data, the one open task per notice, the assignee taken from the case owner |
| TimelineOutcomeAssembler | Service | The decision item of `rwb-decision`'s ledger read and the task item of `task` on API-P3-003, newest first, with no notice content |

**Database and migrations.** Reads `recovery_case`; writes `task`, `assignment`, the local record, the inbox and the outbox. No case update. Constraint: partial unique index `ux_task_open_notice_redress ON task (case_id, notice_ref) WHERE notice_ref IS NOT NULL AND status IN ('OPEN','IN_PROGRESS')` (BR6). Column: `task.notice_ref`, because TSD P3 v3 T3.1 gives `task` no column for the notice, and its name and type are Not specified in the source documents (GAP-2216; ASM-3644). Index `ix_task_case_status ON task (case_id, status)` for the work list and the timeline. Migration `V2014_1__case_notice_redress_task.sql` in the per-service Flyway sequence (DP-15).

**Configuration and reference data.** LOV-ELEMENT, LOV-TASK-STATUS, LOV-ROLE and LOV-ASSIGN-REASON through DP-07 (RWB-P3-E1043-CON), so no task code, element type, role or due time is a constant (GAP-2216; ASM-3644). The case-side switch is a parameter row through DP-06 (RWB-P3-E1042-CON): off means the listener does not subscribe, no task is raised, and the panel still answers. The age limits stay `rwb-decision`'s rows; this story reads none and compares none. The legacy flag `rwb.decision.notice-approval` is not read here.

**Build steps.**

1. `CaseFactsProjection` and `CaseFactsController` with the facts and arrears projection under API-P3-002, and the absence of approval, notice and rule fields; AC1.
2. `SourceDataClient` and `InputAgeService` with the two input codes, the business date and the age in calendar days; AC2 with 13 and 11 December 2026, and the unanswered read (X3, X11).
3. `AuthoriseCheck` with the right, the scope, the refusal by default and the cache; AC3 with `RW-PHONECOL` and an out-of-scope case, and the unanswered call (X9).
4. `NoticeOutcomeListener` with the inbox, the dedupe and `signalWithStart`; AC6 and the repeat.
5. `RaiseRedressTaskActivity` and `RedressTaskService` for a refusal and a return, with the assignment to the case owner; AC4, AC5 and the closed case of AC8.
6. The decision-record failure path, with the record written last; AC8.
7. `TimelineOutcomeAssembler` against the decision-log fake with the no-notice-content assertion; AC7.
8. The contract-fake run of both events in isolation and the drift test against RWB-P7-E2014-CON, so the slice builds before the approval story is live.

**Done when.** The tests in section 16 pass; every fact is answered with its as-of date and every input with its business date and age in days and nothing else; a caller without Case record R is refused before a fact is read; every refused or returned notice has exactly one open redress task on its case, assigned to the case owner, with the reason or question and its local record; the outcome shows on the timeline with no notice content; and a repeated event raises nothing.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-002 | The caller's role does not carry Case record right R | You cannot {action} here. Your role does not include it. | This story, on the case read behind the authorise answer |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. | This story, on the case read |
| MSG-GEN-006 | A consumed call does not answer in time | {system} is not available. Your request is queued and will be retried. | This story, on the source-data and ledger calls |
| MSG-GEN-004 | The case changed while the outcome was applied | Someone else changed this record. Reload it to see their change. | This story, on the version check |
| MSG-P7-003 | The local decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the record writer |
| MSG-P7-006 | An input is past its age limit | {input} is {days} days old, past its limit. Refresh it before you decide. | `rwb-decision`, never this story |
| MSG-P7-002 | A preparer tries to decide | You prepared this decision, so you cannot approve it. | `rwb-decision`, never this story |

The {action} value names the action and nothing else — here "open the case facts of a D7.1 notice" — and the problem response carries the capability area in its `detail` beside the message ID, so a refusal is diagnosable without a case fact. Every error is an RFC 9457 problem response with `messageId` set and `instance` naming the request; the event path answers no caller and records the error on the activity, letting the retry policy act. Thai text for each message follows DL10.

### 15. Screens and states

No screen is built here. The screens are `rwb-decision`'s and the platform route's, and reach this service through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON).

| Screen | State | What this story supplies |
|---|---|---|
| SCR-11 Decision screen | Ready | The case facts with their as-of dates, the arrears facts, the owner, the entry date and the two input ages in days |
| SCR-11 Decision screen | Stale input | The as-of date and the age in days of the stale input; the state and the limit come from `rwb-decision` |
| SCR-11 Decision screen | Decided | No field of this story changes; the decided state is `rwb-decision`'s |
| SCR-11 Decision screen | Empty | Not specified in the source documents (CG-ALL-4201) |
| SCR-11 Decision screen | Loading | Not specified in the source documents (CG-ALL-4201) |
| SCR-11 Decision screen | Error | Not specified in the source documents (CG-ALL-4201) |
| SCR-11 Decision screen | No access | Not specified in the source documents (CG-ALL-4201) |
| SCR-18 Notice approval | Generated | The case number behind the panel header, and nothing of the notice |
| SCR-18 Notice approval | Empty | Not specified in the source documents (CG-ALL-4202) |
| SCR-18 Notice approval | Loading | Not specified in the source documents (CG-ALL-4202) |
| SCR-18 Notice approval | Error | Not specified in the source documents (CG-ALL-4202) |
| SCR-18 Notice approval | No access | Not specified in the source documents (CG-ALL-4202) |
| SCR-04 Case timeline | Loaded | The outcome as the decision item of `rwb-decision`'s ledger and the task item of `task`, newest first |
| SCR-04 Case timeline | Empty | Not specified in the source documents (CG-ALL-4200) |
| SCR-04 Case timeline | Loading | Loading state as set in Screen Specifications v1 section SCR-04 |
| SCR-04 Case timeline | Error | Not specified in the source documents (CG-ALL-4200) |
| SCR-04 Case timeline | No access | Not specified in the source documents (CG-ALL-4200) |
| SCR-01 My work and the case owner's queue view | Loaded | The redress task of a refused or returned notice, with the reason or question and the notice reference |
| SCR-01 My work and the case owner's queue view | Empty | Not specified in the source documents (CG-ALL-4199) |
| SCR-01 My work and the case owner's queue view | Loading | Not specified in the source documents (CG-ALL-4199) |
| SCR-01 My work and the case owner's queue view | Error | Not specified in the source documents (CG-ALL-4199) |
| SCR-01 My work and the case owner's queue view | No access | Not specified in the source documents (CG-ALL-4199) |

The panel layout, the masked rendering of the postal address and the composite route's field list are Not specified in the source documents (GAP-2216; ASM-3645); the panel and the queue screens are RWB-P7-E2014-APP and RWB-P3-E2011-APP, and this story changes no screen behaviour, field order or mask. The route's own overlay states loading, temporarily unavailable and session expired are not panel states of this story; they are carried by the route as RWB-P7-E2014-CON AC4 states.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-014-01 | AC1, AC4, BR1, BR3 | End to end | Synthetic demand notice `N-0201` on case `RW-2026-000123` with approval `A-0201`; the panel facts are asserted and an approval raises no redress task |
| TC-E2-014-02 | AC1, AC2, BR1 | Component | Variant `DEMAND-MTG-B` and reason `TEMPLATE_VARIANT`; the case facts and input dates are unchanged and the variant is `rwb-decision`'s fact |
| TC-E2-014-03 | AC4, AC5, AC7, BR4, BR5, BR7 | End to end | A refusal with the guarantor reason and a return with the question "Attach the latest income statement": one task each in the case owner's queue and one task item on the timeline |
| TC-E2-014-04 | AC3, AC4, BR3 | Contract | Preparer `U-9211` holding `RW-LEGAL`; the 409 is `rwb-decision`'s, no outcome event exists, no task is raised and the case read is authorised as usual |
| TC-E2-014-05 | AC2, BR2 | Component | Total balance with `data_as_of` 2026-12-11 read on 2026-12-14: as-of date and age 3 days; the 1 day limit is `rwb-decision`'s |
| TC-E2-014-06 | AC1, AC2, BR1 | Component | Template `DEMAND-MTG` version 2 withdrawn at 09:30 on 14 December 2026; the case facts are unchanged and no field of the notice is read |
| TC-E2-014-07 | AC4, AC6, BR6 | Contract | Refusal with an empty reason refused with 422 by `rwb-decision`; no outcome event, no task, no record |
| TC-E2-014-08 | AC4, AC6, BR6 | Contract | Variant change with no reason code refused with 422 by `rwb-decision`; no outcome event, no task, no record |
| TC-E2-014-09 | AC6, AC7, BR6, BR7 | Component | `U-9214` decides at 10:01 and `U-9212` at 10:02; the inbox applies one outcome once and one task and one timeline item exist |
| TC-E2-014-10 | AC1, AC2, AC3, BR1, BR2 | End to end | Screen open for `N-0201`: case number, product `MORTGAGE`, the balance of 13 December 2026 with age 1 day, the arrears facts, the owner and the entry date, and no notice content |
| TC-E2-014-11 | AC3, BR3 | Component | `U-9217` without Case record right and an out-of-scope case: 403 MSG-P4-002 and 404 MSG-P4-003, with no case fact in either answer |
| TC-E2-014-12 | AC8, AC6, BR8 | NFR | The decision-record library stopped and an outcome for the closed case `RW-2026-000999`; nothing is written, the case carries MSG-P7-003 and the event is redelivered |
| TC-E2-014-13 | BR1, BR9, BR10 | Component | Not specified in the source documents (ASM-3438): boundary values for each table of section 12.7 that this story reads or writes |
| TC-E2-014-14 | BR9, BR10, BR11 | Component | Closed case `RW-2026-000999` as in TC-E2-014-12; the task code, status and role are read from reference data with the version in force, and no postal address value is in the panel or the task |
| TC-E2-014-15 | AC9, BR9, BR10, BR11 | Component | Refused notice `N-0201` on case `RW-2026-000123` as in AC9; the task code, element type, status, role, reason and due time are read from reference data, and the postal address is named and never valued |
| TC-E2-014-16 | AC10, BR3 | Contract | Caller without a valid credential calls GET /api/recovery/case/v1/cases/RW-2026-000123; 401 is answered and no case fact is in the answer |
| TC-E2-014-17 | AC11, BR6, BR8 | NFR | Activity retried after a stale case version and activity timed out before commit on the refusal of `N-0201`; at most one open task, and no task, assignment or outbox row from the timed-out attempt |
| TC-E2-014-18 | AC12, BR3 | Contract | rwb-access does not answer and rwb-source-data fails for the total balance; no case fact is answered and the failure is recorded |

The first twelve cases keep their legacy order and legacy data and each asserts only this slice's facts, refusal and task; TC-E2-014-13 to TC-E2-014-18 are this story's own cases for the table boundary, for BR9 to BR11 and for AC9 to AC12. Legacy level System maps to End to end, Access to Component and Resilience to NFR. No `-ITG` copy is used here: the integration copy is RWB-ITG-E2014-ITG, whose `TC-E2-014-01-ITG` to `TC-E2-014-12-ITG` prove the same facts across `rwb-case`, `rwb-decision`, `rwb-comms` and `rwb-access` with real services. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the task code, element type, task status, owner role, assignment reason, due time and the two input codes are data rows read with the version in force; the Java code holds no task code, element type, status or role literal (BR9).
- No personal data in logs, events, records, workflow history, tests or prompts: the panel, the task, the record and the timeline item carry the case number, codes, amounts and dates; the postal address is named `POSTAL_ADDRESS` and only its business date and age are returned, and a test scans the task text and the record for any part of the synthetic address (BR10).
- No read of another service's tables and no cross-schema read (DP-01): `notice`, `template`, `approval`, `decision_log_entry`, `permission`, `masking_rule`, `delegation_limit`, `interaction` and `document` are never queried here.
- ACE data only through the owner's contract (DP-05, ADR-010): the balance, arrears and contact facts arrive on `rwb-source-data`'s reads with `data_as_of`, and this story adds no `v_ace_*` read (GAP-2216; ASM-3646).
- A fact is never shown as current without its date: an input whose business date is unknown is answered as unavailable and the panel marks it (BR2).
- The authorise answer is required before any fact is read and fails closed: a missing, unparseable or unanswered answer is a refusal, never an allow (BR3).
- The task, the assignment, the local record and the outbox row commit in one transaction, and a task that cannot be recorded does not exist (BR8, R-UNI-39).
- One hop and 2 s on every call; a timeout never shows a stale fact as current and never raises a task twice (DP-11).
- The case status and the resume state of the routing rule are not written here, so this slice cannot put a case in a state its rules did not name.
- Every example is synthetic; no production payload is copied into a test, a fake or a message.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-APD-002 | Recommendation, reasons, inputs and limit on one screen | Business Requirements Epic 2, 3.7; Business Requirements Program, 5.7 | FEAT-APD-08 | 8.1 Prepare pre-litigation | BR1, BR2, BR9, BR10 | TC-E2-014-01, TC-E2-014-02, TC-E2-014-05, TC-E2-014-06, TC-E2-014-10, TC-E2-014-13, TC-E2-014-14 |
| REQ-APD-006 | Demand and recall notices approved through approval routing | Business Requirements Epic 2, 3.7; Business Requirements Program, 5.7 | FEAT-APD-08 | 8.1 Prepare pre-litigation | BR3, BR4, BR5, BR6, BR7, BR8, BR11 | TC-E2-014-01, TC-E2-014-03, TC-E2-014-04, TC-E2-014-07, TC-E2-014-08, TC-E2-014-09, TC-E2-014-11, TC-E2-014-12, TC-E2-014-14 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E2-014, disposition Split (rework), secondary slice |
| Legacy criteria owned here | None; legacy AC1 to AC10 are carried by RWB-P7-E2014-APP and RWB-P4-E2014-APP |
| Values kept from the legacy story | Case `RW-2026-000123`, product `MORTGAGE`, approval `A-0201`, notice `N-0201`, the balance of 13 and 11 December 2026 with ages 1 and 3 days, the refusal reason, the return question, decided 14 December 2026 |
| Test cases | TC-E2-014-01 to TC-E2-014-14: the first twelve in the legacy order with their legacy data, each asserting only this slice; TC-E2-014-13 and TC-E2-014-14 are this story's own; the `-ITG` copies are RWB-ITG-E2014-ITG's |
| Decoupling patterns | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-016 (reusable Temporal layer), ADR-019 (edge: gateway-bff), ADR-020 (contract-first REST, one hop, 2 s), ADR-022 (local decision record plus central ledger) |
| Rules | R-LIT-03, R-LIT-04, R-UNI-39, R-UNI-40, VR-P3-003-1 |
| Requirement trace | Not specified in the source documents (GAP-2742) |

The feature mapping is read as FSD P3 declares it for the case record view (FEAT-WKM-08) and as the legacy story declares it for the notice approval (FEAT-APD-08); TSD P3 v3 maps no requirement of this legacy key, so FEAT-APD-08 is taken from the legacy story and the BRD. The limit REQ-APD-002 asks for is not on this panel: a D7.1 notice carries no amount limit and the case panel shows none, which is the reading RWB-P7-E2014-APP records for the same requirement.

### 19. Out of scope

- The approval and its decision: SCR-10, SCR-11, the SCR-18 panel, the approve, change, refuse and return operations, the decision entry and the preparer check (RWB-P7-E2014-APP, RWB-P7-E2014-CON).
- The notice, its template version, the notice PDF and the approve, regenerate and hold operations of the notice (RWB-P6-E1052-CON and the `rwb-comms` app story).
- The access decision itself: the permission and masking rows, the policy pack and the delegation table (RWB-P4-E2014-APP, RWB-P4-AD002-APP, RWB-P4-AD004-APP).
- The rule evaluation, the rule package and version, the input age limits and the stale-input state (RWB-P7-E2014-APP and the `rwb-decision` rule stories).
- The screen layout, field order, mask rendering and the composite route itself (RWB-P7-E2014-CON, RWB-PLT-N001-APP).
- The case status move out of `WAITING_APPROVAL` and the resume state of its routing rule (RWB-P3-E2013-APP).
- The full case record view and the timeline read as a whole (RWB-P3-E2016-APP, RWB-P3-E1023-APP) and the interaction ledger behind it (`rwb-source-data`, DP-18).
- The delegation of authority lookup for limit-based approvals and delegation item 2.1.3 (RWB-P3-E2013-APP), which a D7.1 notice does not use.
- The integration harness RWB-ITG-E2014-ITG and its `-ITG` copies, dispatch to WIN and proof of delivery (RWB-P6-E2021-APP), and the deployment, dashboards and run book of this capability (an OPS story of this key).
