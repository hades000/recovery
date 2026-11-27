# RWB-P3-E2001-APP EFS hand-over with full history

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2001-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-001 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP18, DP19 |
| Parallel lane | L-P3-X |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2001-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-032) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-001 for rwb-case. The ACE read, the hand-over adapter and the freshness stamp stay with rwb-integration and rwb-source-data; this story keeps the create-or-link of the case in `rwb_case`, the EFS history on the case through the interaction ledger, the local decision record, the outbox event and the composite-route screens. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P3-E2001-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the case created from the ACE record of the ALS hand-over the morning after the account reaches 90 days past due, or the account linked to the open case of the same customer and product group, with the EFS contact and promise history on the case timeline**, so that **the case starts on the first morning after day 90 and I can see what happened before day 90 without asking for a spreadsheet**.

### 2. Business rationale

Accounts move from collections to recovery by a weekly transfer today and the case starts without its collection history. ACE ingests the ALS hand-over and the EFS action history instead (D-RCV-35 U1), so the Workbench loads no source file and holds no copy of an ACE record.

In the target the journey is cut across services. rwb-integration reads the ACE records, holds the freshness of the data products and publishes AceDataReady (EV-26) and AceDataLate (EV-27); rwb-source-data owns the interaction ledger (default ruling, DP-18) and the `v_ace_*` views (DP-05). This story owns the case of record: it consumes the hand-over page of the rwb-integration contract (DP-11, built against RWB-P2-E2001-CON and its fake), writes the case and its account link in `rwb_case` (DP-01), appends the EFS history of the collection period to the ledger through the rwb-source-data contract keyed on `efs_record_key` (DP-18), writes the local decision record with the ENTRY rule and the business date (DP-03), and publishes CaseCreated (EV-01) from its outbox in the same transaction (DP-09). The morning step is an event-started workflow on task queue `rwb-case`, with the 09:00 cut-off as a durable timer and no Quartz row (DP-10). The threshold, the product map, the copied action codes and the cut-off are rows and parameters (DP-06, DP-07), and the case list and timeline are composed at the edge (DP-19).

Retiring the in-process call is the realignment work (ASM-3719): the legacy `AccountQuery.findAtOrAboveDpd`, `EfsHistoryQuery.forAccount`, `CaseCreation.createOrLink`, `InteractionLedger.appendEfsHistory` and `HandoverRun.run` interfaces become a published P2 contract on one side, a P1 ledger contract on the other and one `rwb_case` transaction with its outbox rows in the middle.

It meets REQ-DRI-013, REQ-CHO-001, REQ-CHO-005 and REQ-RDF-003 for the case side, and it carries the legacy measure: CTL-01 and REC-01 (accounts at 90 days past due against open cases, zero unexplained). It owns no legacy acceptance criterion, because the eight criteria of RWB-E2-001 are exercised across services by the integration story; the ten criteria in section 7 are new for this service change and keep every legacy value.

### 3. Preconditions

- RWB-P2-E2001-CON is published: the hand-over candidate page and the EFS history page of the rwb-integration service (fields, errors, contract fake), on base `/api/recovery/integration/v1`. This story builds against that contract and its fake and never against the ACE database.
- The rwb-source-data contract is published for the interaction ledger append, the business-key break of REC-05 and the ACE source views that P1 owns; their paths and payloads are Not specified in the source documents (GAP-2259; ASM-3725).
- The `rwb_case` baseline and the case of record exist from the Epic 1 story RWB-P3-E1018-APP: `recovery_case`, `case_account`, `case_entry_exclusion`, the parameter and reference tables and the outbox table.
- Parameter `case.entry.dpd_threshold` = 90 is in force (DL16) and `handover.hold_until` = 09:00.
- The product code to product group map (LOV-PRODUCT-CODE to LOV-PRODUCT) is loaded as versioned reference data of rwb-case (DL17).
- The EFS action codes copied at hand-over are rows of `efs_ledger_outcome` (DL29).
- The local decision-record library and the shared topic `rwb.decision-record.v1` are published by the platform contract story of DP-03; the outbox and inbox library by DP-09, and the workflow kit by DP-10. Those H dependencies are held by the platform stories and are not repeated in the metadata rows (GAP-2261; ASM-3723).
- The rwb-case login holds SELECT on no ACE view: the hand-over data arrives through the P2 and P1 contracts only (DP-01, DP-05).

### 4. Flow

1. rwb-source-data publishes AceDataReady (EV-26) for the ALS source when both ALS and EFS carry business date D; the rwb-case case router consumes it through its inbox and starts DailyCaseRun on task queue `rwb-case`, workflow ID `case-entry-{D}`. A second event for D returns the running execution and starts nothing.
2. When the cut-off `handover.hold_until` (09:00) passes with no EV-26, AceDataLate (EV-27) starts DailyCaseRun in holding mode: no case is created, the data steward is alerted with MSG-P2-007, and the workflow waits for the next EV-26.
3. EntryStep reads the hand-over candidate page for business date D through the rwb-integration contract in the `readCandidates` activity: one hop, 2 s timeout, breaker per downstream (DP-11). The page carries `account_key`, `person_key`, product code, `days_past_due`, `total_balance` and `data_as_of` of the accounts at or above the threshold with no open case link.
4. For each candidate the step runs `IdempotencyGuard.firstTime("handover", account_key + ":" + D)`; a repeat is skipped and counted, so a redelivered EV-26 writes nothing.
5. HandoverGroupBuilder groups the candidates by `person_key` and product group, using the product code map read through the reference-data contract of rwb-case (DP-07); a candidate whose `person_key` has no customer row is held on the REC-05 business-key break and tried on the next business date.
6. CreateOrLinkCase activity: in one `rwb_case` transaction the service writes the local decision record with the ENTRY rule and the business date in its inputs snapshot (DP-03), then creates the case with status `NEW`, a case number `RW-YYYY-NNNNNN` from the rwb-case sequence and entry date D+1, or links the account to the customer's open case for the product group with `linked_from` D+1 and `is_primary` false. A failed record write rolls the transaction back and the account is retried.
7. The same transaction inserts `rwb.case.CaseCreated.v1` (EV-01) with case ID, case number, product group and business date into the outbox; the relay publishes it on `rwb.case.events.v1` (DP-09). A link raises no event, because the case status does not change.
8. AppendEfsHistory activity calls the rwb-source-data ledger contract once per created or linked case with the EFS rows of the collection period returned by the contract: source system EFS, the action code, `contact_at`, the promise date and amount. Each entry carries `efs_record_key`, so a row the daily EFS read already wrote is skipped.
9. The step writes the run summary (accounts read, cases created, accounts linked, repeats, held) and the gap dates, and hands the REC-01 result to rwb-source-data, which owns `reconciliation_result`. JOB-03 allocation follows in the rwb-case allocation step (RWB-P3-E1020-APP).
10. The case owner opens SCR-02 Case list and SCR-04 Case timeline through the gateway-bff composite route, which calls rwb-case and rwb-source-data in parallel, one hop each, and merges the answers (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The same business date is run twice, or EV-26 is redelivered | No second case, no second link and no second ledger entry; the repeat is counted in the run summary (R-UNI-40) | None | AC2 |
| X2 | The ACE batch for ALS and business date D is not complete by the cut-off | DailyCaseRun holds; no case is created from an earlier business date; the data steward is alerted; cases are created on the next complete business date | MSG-P1-001, MSG-P2-007 | AC5 |
| X3 | The candidate's person_key has no row in the customer data | No case is created; the REC-05 business-key break names `account_key` and the person_key for the data steward; the account is tried on the next business date | None | AC4 |
| X4 | The local decision-record write fails | The transaction rolls back; no case exists; the failure is counted and an incident is raised (R-UNI-39); the account is retried | MSG-P7-003 | AC6 |
| X5 | The customer already has an open case for the product group | The account is linked to that case; no new case and no event | None | AC3 |
| X6 | A second start or a rerun for a business date whose workflow runs | The running execution is returned and nothing starts; a rerun request answers 409 with MSG-P2-006 through the operation recorded as Not specified in the source documents (GAP-2258; ASM-3722) | MSG-P2-006 | AC7 |
| X7 | The rwb-integration contract does not answer within 2 s, or the rwb-source-data ledger call times out | The step fails for that page and retries with the next EV-26 or the scheduled retry; no partial case is left, because the case write and its outbox row are one transaction | MSG-GEN-006 | AC6 |
| X8 | A role without the Case record right, or a case outside the caller's scope, reads the timeline | Refused; nothing is returned and nothing is written | MSG-P4-002, MSG-P4-003 | AC8 |
| X9 | A ledger row already written by the daily EFS read | The append skips it on `efs_record_key`; the timeline shows it once | None | AC9 |

The REC-05 break of X3 and the REC-01 result of step 9 live in `reconciliation_result`, owned by rwb-source-data; the operation by which rwb-case hands them over is Not specified in the source documents (GAP-2259; ASM-3725).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against the RWB-P2-E2001-CON fake and the platform kits; no work order sits inside another team's lane |
| Negotiable | Threshold, cut-off, product map, copied action codes and the feature parameter are rows; the story fixes the behaviour |
| Valuable | Each case starts the morning after day 90 with its collection history, and no case is built from a stale business date |
| Estimable | One workflow, one step, two read activities, one transaction, one ledger call and one composite screen |
| Small | Fits two weeks with its tests |
| Testable | Each of the ten criteria of section 7 is one automated test; every cross-service answer is stubbed in a contract fake |

### 7. Acceptance criteria

```gherkin
Feature: EFS hand-over with full history

  Background:
    Given parameter "case.entry.dpd_threshold" is 90
    Given parameter "handover.hold_until" is 09:00
    Given the rwb-integration contract mock answers the hand-over candidates for business date 2026-12-14

  Scenario: AC1 Case created from the ACE data with its EFS history (new, D-RCV-60)
    Given the rwb-integration contract mock returns account "A-0001" for customer "C-0001", product group "MORTGAGE", 90 days past due at business date 2026-12-14
    Given the rwb-integration contract mock returns 14 contact rows and 2 promise rows of the EFS history for "A-0001" in its collection period
    Given the rwb-source-data contract mock accepts the ledger append and returns its entry references
    When the entry step of DailyCaseRun runs on 2026-12-15
    Then one case exists with status "NEW", product_group "MORTGAGE", entry_date 2026-12-15 and days past due at entry 90
    Then case_account holds "A-0001" as the primary account with linked_from 2026-12-15
    Then the 16 EFS entries are appended through the ledger contract with source system "EFS" and the action code of each row
    Then no interaction row and no copy of an EFS row is written in rwb_case
    Then the decision record of the creation names the ENTRY rule and business date 2026-12-14 in its inputs snapshot
    Then rwb.case.CaseCreated.v1 is published with business date 2026-12-14
    Then the case row, the ledger append key and the outbox row commit in one rwb_case transaction

  Scenario: AC2 Repeat run (new, D-RCV-60)
    Given the run for business date 2026-12-14 created the case for "A-0001"
    When AceDataReady for business date 2026-12-14 is consumed again and the entry step runs
    Then no second case is created and no interaction entry is added
    Then the run summary shows 1 repeat for "A-0001"

  Scenario: AC3 Account linked to the open case (new, D-RCV-60)
    Given customer "C-0002" has open case "RW-2026-000210" for product group "SSME"
    Given the rwb-integration contract mock returns account "A-0002" of "C-0002", product group "SSME", 90 days past due on 2026-12-14
    When the entry step runs
    Then no new case is created
    Then "A-0002" is linked to "RW-2026-000210" with linked from 2026-12-15 and is primary false
    Then the status of "RW-2026-000210" is unchanged and no CaseCreated is published

  Scenario: AC4 Customer not in the ACE customer data (new, D-RCV-60)
    Given the rwb-integration contract mock returns account "A-0003" at 90 days past due with a person_key that has no customer row
    When the entry step runs
    Then no case is created for "A-0003"
    Then the REC-05 business-key break lists "A-0003" and its person_key for the data steward
    Then "A-0003" is tried again on the next business date
    Then no case row and no decision record exist for "A-0003"

  Scenario: AC5 Cases created on the next good batch (new, D-RCV-60)
    Given no entry run ran for business date 2026-12-15
    Given the rwb-integration contract mock answers the hand-over for business date 2026-12-16 completed at 05:15 on 2026-12-17
    When AceDataReady for 2026-12-16 starts the entry step on 2026-12-17
    Then no case is created from the data of 2026-12-14
    Then accounts that reached 90 days past due on 2026-12-15 or 2026-12-16 get cases with entry date 2026-12-17
    Then the run summary names the gap date 2026-12-15

  Scenario: AC6 Decision record write fails (new, D-RCV-60)
    Given the local decision-record store is unavailable
    When the entry step runs for "A-0004"
    Then the transaction rolls back and no case is created for "A-0004"
    Then the run summary carries message MSG-P7-003 and an incident is raised
    Then "A-0004" is taken in the next run and gets one case and exactly one decision record

  Scenario: AC7 Second start or rerun is refused (new, D-RCV-60)
    Given DailyCaseRun is running for business date 2026-12-14
    When AceDataReady for business date 2026-12-14 is consumed again
    Then the running execution is returned and no second execution starts
    Then no second case is created and the run summary counts one repeat
    When a platform administrator requests a rerun of the entry run for 2026-12-14
    Then the response is 409 with message MSG-P2-006

  Scenario: AC8 The history read is refused without the right or outside the scope (new, D-RCV-60)
    Given user "U-5001" holds RW-REFADM, which has no Case record right
    Given the rwb-access contract mock returns no Case record right for role "RW-REFADM"
    When "U-5001" calls GET /cases/{caseId}/timeline for case "RW-2026-000123"
    Then the call is refused with status 403 and message MSG-P4-002
    Given a case owner whose scope is "Own" and case "RW-2026-000210" owned by another person
    When that case owner calls the same operation for it
    Then the response is 404 with message MSG-P4-003
    Then the read writes nothing

  Scenario: AC9 A ledger row already written is skipped (new, D-RCV-60)
    Given the ledger already holds the entry for efs_record_key "EFS-0001" written by the daily EFS read
    When the entry step appends the history of "A-0001"
    Then the row for "EFS-0001" is skipped on its key and counted once
    Then the timeline of the case shows that entry once

  Scenario: AC10 The new case and its history on the screens (new, D-RCV-60)
    Given the gateway-bff composite route serves the case list and the case timeline
    Given the case "RW-2026-000123" created for "A-0001" with its 16 EFS entries
    When the case owner opens SCR-02 Case list and SCR-04 Case timeline
    Then the case row shows the case number "RW-2026-000123" and status "New"
    Then the timeline shows the 16 entries with source "EFS" and the action code of each row
    And the browser calls one composite route per screen and no owner service directly
```

AC1 to AC10 are new for the rwb-case slice (ASM-3720): the eight legacy criteria of RWB-E2-001 are exercised across services by the integration story and the app slices of rwb-integration and rwb-source-data, so this story owns no legacy acceptance criterion and copies none. Every legacy value is kept (the accounts, the dates, the 14 contact rows and 2 promise rows, the 16 entries, the case numbers, the gap date and the message codes).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A case enters at 90 days past due | DL16; parameter case.entry.dpd_threshold |
| BR2 | One case per customer per product group; a further account of the same customer and product group is linked to the open case | DL17; FEAT-CWC-02; REQ-CHO-005 |
| BR3 | The hand-over set is read through the rwb-integration contract for the ACE business date; rwb-case reads no ACE view and loads no source file | D-RCV-35 U1; ADR-010; DP-05; DP-11 |
| BR4 | No case is created from a business date whose ACE batch is not complete | FEAT-CHO-05; CTL-02; DP-10 |
| BR5 | The EFS contact and promise history of the collection period is appended to the interaction ledger with source system EFS, one entry per efs_record_key, and the ledger is owned by rwb-source-data | DL29; LOV-SOURCE; REQ-CHO-001; DP-18 |
| BR6 | A repeat hand-over for the same account and business date is ignored and counted | R-UNI-40 |
| BR7 | A decision that cannot be written to the decision record does not proceed: the record, the case row and the outbox row are one transaction | Principle 5; R-UNI-39; DP-03 |
| BR8 | An account whose person_key has no customer row is held on the REC-05 business-key break and tried on the next business date | REC-05; DQ-040; D-RCV-35 U2 |
| BR9 | The case number is `RW-YYYY-NNNNNN` from the rwb-case sequence and is never reused | FEAT-CWC-01; DF-CAS-002 |
| BR10 | The threshold, the product map, the copied action codes and the cut-off are rows and parameters with a version, never code | Principle 1; DP-06; DP-07 |
| BR11 | rwb-case writes only its own schema and holds no foreign key into another schema; a case link is a business key of 255 characters | DP-01; FSD P3 A1.5 |
| BR12 | CaseCreated is written to the outbox in the transaction that writes the case and is relayed with the CloudEvents envelope; a link raises no event | DP-09; EV-01 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| No case | `rwb.case.CaseCreated.v1` (EV-01) from the entry step | days_past_due at or above the threshold and no open case for the customer and product group | New |
| New, Assigned, In progress or any Waiting | Account linked by the entry step | Open case for the customer and product group | Status unchanged |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-case service identity (the rwb-case login, DP-02) | Runs the entry step; reads the hand-over through the rwb-integration contract; writes the case, the account link and the outbox row |
| DailyCaseRun and its activities | Hold the cut-off timer, drive the creates and links, and write the run summary |
| Decision-record library identity | Writes the local decision record and its outbox row (Decision log C) |
| RW-CASEOWN, case owner | Reads the case and its EFS history once allocated (Case record R) |
| RW-DATASTEW, data steward | Receives the held-run alert and reads the REC-05 break (Platform administration R) |
| RW-PLATADM, platform administrator | Requests a rerun of a business date (Platform administration U); refused with MSG-P2-006 while the run is in flight |
| RW-REFADM, RW-COE | Own the product map, the copied action codes and the parameters; hold no Case record right |

The per-service login name is Not specified in the source documents (GAP-2259; ASM-3725); the story names it "the rwb-case login (DP-02)" until it is agreed.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-002 | recovery_case | case_no | Write |
| DF-CAS-003 | recovery_case | product_group | Write |
| DF-CAS-004 | recovery_case | primary_person_key | Write |
| DF-CAS-005 | recovery_case | status | Write |
| DF-CAS-013 | recovery_case | entry_date | Write |
| DF-CAS-014 | recovery_case | dpd_at_entry | Write |
| DF-CAS-016 | recovery_case | total_outstanding_at_entry | Write |
| DF-CAS-025 to DF-CAS-028 | case_account | case_id, account_key, is_primary, linked_from | Write |
| DF-INT-002, DF-INT-004 to DF-INT-010, DF-INT-013, DF-INT-018 | interaction (rwb_source_data) | case_id, occurred_at, channel, direction, action_code, contact_result, promise_amount, promise_date, source_system, idempotency_key | Write through the rwb-source-data ledger contract only |
| DF-ACE-001, DF-ACE-008, DF-ACE-018, DF-ACE-020, DF-ACE-036 | Hand-over candidate page (rwb-integration) | account_key, product_key, days_past_due, total_balance, data_as_of | Read from the contract, never from a view |
| DF-ACE-056 | Hand-over candidate page (rwb-integration) | person_key | Read from the contract |
| DF-ACE-108, DF-ACE-111, DF-ACE-114, DF-ACE-119, DF-ACE-122, DF-ACE-123 | EFS history page (rwb-integration) | efs_record_key, action_code, contact_at, is_ptp, promise_date, promise_amount | Read from the contract |
| DF-REF-132 to DF-REF-158 | parameter_catalog, parameter_value | `case.entry.dpd_threshold`, `handover.hold_until` and their versions in force | Read |
| DF-REF-159 to DF-REF-184 | reference_version, reference_row | The product code map version and the `efs_ledger_outcome` rows | Read |
| DF-DEC-001 to DF-DEC-018 | decision record (local library) | all fields | Write locally; the central entry is sealed by rwb-decision |
| DF-OPS-118 to DF-OPS-129, DF-OPS-178 to DF-OPS-183 | reconciliation_result, processed_event (rwb_source_data) | all fields | Write through the rwb-source-data contract |

Field IDs are those in the Logical Data Model and Data Dictionary v9. The hand-over rows are read through the published P2 contract and are never read from an ACE table; `rwb_case` holds no copy of them, and the ledger entries are written by their owner, rwb-source-data (DP-01, DP-05, DP-18). The case link to ACE is the business key `account_key` with no foreign key (FSD P3 A1.5).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases/{caseId}/timeline` | The case history with query filters `type`, `from` and `to`; the EFS entries appended through the ledger contract are shown with source system "EFS" and their action codes | Case record R, scope applied | Not applicable: the call writes nothing |

Errors: 401 no session (MSG-P4-001), 403 no Case record R (MSG-P4-002), 404 not found or out of scope (MSG-P4-003), 503 ledger or case store down. `GET /cases/{caseId}` and `GET /cases` exist from RWB-P3-E1018-APP and RWB-P3-E1002-APP and are unchanged; the full case record view with the timeline is completed by RWB-P3-E2016-APP.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | Not specified in the source documents (GAP-2259; ASM-3725) | rwb-integration (P2) | The hand-over candidate page for business date D from RWB-P2-E2001-CON and its fake: account_key, person_key, product code, days_past_due, total_balance, data_as_of | One hop, 2 s |
| GET | Not specified in the source documents (GAP-2259; ASM-3725) | rwb-integration (P2) | The EFS contact and promise rows of an account for its collection period: efs_record_key, action_code, contact_at, is_ptp, promise_date, promise_amount | One hop, 2 s |
| POST | Not specified in the source documents (GAP-2259; ASM-3725) | rwb-source-data (P1) | Append the EFS history to the interaction ledger, keyed on efs_record_key (DP-18) | One hop, 2 s |
| POST | Not specified in the source documents (GAP-2259; ASM-3725) | rwb-source-data (P1) | The REC-05 business-key break and the REC-01 run result for an account with no customer row | One hop, 2 s |
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | The Case record right and the scope before the timeline read, cached by the guard library | One hop, 2 s |

The four P1/P2 resources replace the legacy published interfaces `AccountQuery.findAtOrAboveDpd`, `EfsHistoryQuery.forAccount`, `InteractionLedger.appendEfsHistory` and the REC-05 break write; their per-service paths and payloads are fixed by RWB-P2-E2001-CON and the rwb-source-data contract stories and are not in the source documents.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.case.CaseCreated.v1` (EV-01) | `rwb.case.events.v1` | P3 | caseId | caseId, caseNo, productGroup, personKey, businessDate, accountKeys, entryDate, dpdAtEntry |
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 owns the type and the central ledger; every service writes its own record | caseId | decision record reference, rule ID of the ENTRY rule, rule version, business date |

Both are written to the outbox in the same transaction as the case row and relayed with the CloudEvents envelope. No name, account number, amount or identity number is carried in any payload; the person key is a business key, not personal data (DP-09).

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Handler |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` (EV-26) | `rwb.source-data.events.v1` | P1 | Case router: inbox dedupe on business date, `signalWithStart` of DailyCaseRun with workflow ID `case-entry-{D}` |
| `rwb.source-data.AceDataLate.v1` (EV-27) | `rwb.source-data.events.v1` | P1 | Case router: starts or signals DailyCaseRun in holding mode, raises MSG-P2-007 to the data steward and creates no case |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| DailyCaseRun | Workflow (event-started from EV-26 or EV-27, workflow ID `case-entry-{businessDate}`) | `rwb-case` | Owns the cut-off timer, the entry step, the run summary and the held state |
| EntryStep | Step of DailyCaseRun | `rwb-case` | Groups the candidates, applies the idempotency key and drives the creates, the links and the history |
| readCandidates | Activity | `rwb-case` | Calls the rwb-integration candidate page with the 2 s timeout and the breaker |
| readEfsHistory | Activity | `rwb-case` | Calls the rwb-integration EFS history page for one account |
| CreateOrLinkCase | Activity | `rwb-case` | Writes the decision record, the case or the link and the outbox row in one transaction |
| AppendEfsHistory | Activity | `rwb-case` | Calls the rwb-source-data ledger append with the EFS rows and the keys |
| recordRunSummary | Activity | `rwb-case` | Writes the counts and the gap dates and hands the REC-01 result to rwb-source-data |

#### 12.6 Schedules

None new. The legacy JOB-02 Quartz trigger becomes the event-started DailyCaseRun workflow; the 09:00 cut-off of `handover.hold_until` is a durable timer inside the workflow, and no Schedule row and no five-minute timer check is created by this story (DP-10).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| recovery_case | P3 (rwb_case) | The case row: case number, product group, primary person key, status, entry date, days past due at entry and total outstanding at entry |
| case_account | P3 (rwb_case) | The account link: `account_key`, `is_primary`, `linked_from`; no foreign key into ACE |
| parameter_catalog, parameter_value | P3 (rwb_case) | `case.entry.dpd_threshold`, `handover.hold_until` and their versions |
| reference_version, reference_row | P3 (rwb_case) | The product code map version and the `efs_ledger_outcome` rows |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | Outbox, inbox and idempotency objects (DP-09) |

`interaction` is not a table of this story: the ledger is owned by rwb-source-data (DP-18; ASM-3721), and the ownership conflict between that ruling and the P3 data model is recorded as GAP-2260. `reconciliation_result` is owned by rwb-source-data. `decision_log_entry` is owned by rwb-decision and is written only through its contract. rwb-case reads no table of another service and holds no foreign key across services (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-integration WireMock | The P2 contract of RWB-P2-E2001-CON | The candidate page of 2026-12-14 with "A-0001"; "A-0002" of "C-0002"; "A-0003" with no customer row; the page of 2026-12-16 completed at 05:15 on 2026-12-17; the EFS history with 14 contact rows and 2 promise rows; the row "EFS-0001"; a delay beyond 2 s |
| rwb-source-data WireMock | The P1 contract | The ledger append accepting 16 entries and returning their references; the duplicate key "EFS-0001"; the REC-05 break; the REC-01 result |
| rwb-access WireMock | The P4 contract | `POST /authorise` granting Case record R, refusing it for RW-REFADM and excluding a case from an Own scope |
| gateway-bff composite route (WireMock) | The DP-19 routes of SCR-02 and SCR-04 | The merged case row and the merged timeline of AC10 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 5 consumed | The timeline read provided; the P2 candidate page and EFS history, the P1 ledger append and break, and the P4 authorise consumed; one hop, 2 s |
| Kafka | 2 published, 2 consumed | `rwb.case.events.v1` and `rwb.decision-record.v1` published; `rwb.source-data.events.v1` consumed for EV-26 and EV-27 |
| Temporal | 1 workflow, 6 activities | DailyCaseRun; readCandidates, readEfsHistory, CreateOrLinkCase, AppendEfsHistory, recordRunSummary and the cut-off timer |
| File | None | This story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `handover`, Java package `th.co.scb.ace.workbench.recovery.case.handover`; the screens are the existing SCR-02 and SCR-04 modules composed at the edge.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_case`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H dependencies this table adds are held by the platform and service contract stories and are not repeated in the metadata rows, which carry only the contract dependency of the legacy read (GAP-2261; ASM-3723). DP-05 resolves to the P2 and P1 contracts, never to an ACE view: the views are read by rwb-source-data only. DP-18 resolves to one contract and no ledger table in `rwb_case`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DailyCaseRunWorkflow | Workflow | Holds the cut-off timer, runs the entry step once per business date and keeps the held state |
| EntryStep | Step | Reads the candidates, applies the idempotency key, groups and drives the creates, links and history |
| HandoverGroupBuilder | Service | Groups candidates by person key and product group with the product map read through the reference-data contract |
| CaseCreationService | Service | Creates the case with the sequence number or links the account, inside one transaction with the decision record and the outbox row |
| HandoverRepository | Repository | Reads and writes `recovery_case` and `case_account` in schema `rwb_case` only |
| HandoverClient | Client | Calls the rwb-integration candidate and EFS history resources with one hop, the 2 s timeout and a breaker |
| LedgerClient | Client | Calls the rwb-source-data ledger append with the EFS rows and their keys; owns no ledger table |
| RunSummaryWriter | Service | Writes the counts, the gap dates and the REC-01 result through the rwb-source-data contract |
| DecisionRecordWriter | Library adapter | Writes the local decision record with the ENTRY rule and the business date, hash-linked, in the same transaction (DP-03) |
| CaseCreatedRelay | Library adapter | Relays `rwb.case.CaseCreated.v1` from the outbox with the CloudEvents envelope (DP-09) |
| TimelineController | Controller | `GET /cases/{caseId}/timeline` with the access check, the scope and the EFS source filter |

**Database and migrations**

- Migration `V2001_1__handover_index.sql` adds two indexes in `rwb_case`: `ix_case_account_open ON case_account (account_key) WHERE linked_to IS NULL` and `ix_recovery_case_open_group ON recovery_case (primary_person_key, product_group) WHERE closed_date IS NULL`, for the open-case lookup of BR2.
- No new table: the case, the account link, the parameters, the reference tables and the outbox table already exist in `rwb_case`. The ledger and the reconciliation tables belong to rwb-source-data.
- The migration runs in the rwb-case Flyway sequence of the service's own schema (DP-15); no other schema is touched.

**Configuration and reference data**

- Parameter `case.entry.dpd_threshold` = 90 (RW-COE, DL16) and `handover.hold_until` = 09:00 (RW-COE), read through the parameters contract of rwb-case.
- Product code to product group map (RW-REFADM, DL17) as versioned reference rows of rwb-case; `efs_ledger_outcome` rows for the copied action codes (RW-DATASTEW, DL29).
- The legacy feature flag `rwb.integration.efs-handover` is kept as the legacy reference; in the target the switch is a parameter row read through the parameters contract, and off means the step creates no case and the timeline reads the ledger only.

**Build steps**

1. HandoverClient against the RWB-P2-E2001-CON fake, with the 2 s timeout and the breaker; tests for AC1 and AC5.
2. HandoverGroupBuilder and the product map read through the reference-data contract; tests for AC1 and AC3.
3. CaseCreationService with the sequence number, the open-case lookup and the link; tests for AC1, AC3 and AC4.
4. The idempotency key and the inbox dedupe on account and business date; test for AC2.
5. DecisionRecordWriter, the outbox row and the relay; tests for AC1 and AC6.
6. LedgerClient with the EFS rows and the `efs_record_key` skip; tests for AC1 and AC9.
7. RunSummaryWriter with the counts, the gap dates and the REC-05 break; tests for AC4 and AC5.
8. DailyCaseRun with the cut-off timer, the held mode and the duplicate-start rule; test for AC7.
9. TimelineController with the access check, the scope and the EFS filter; test for AC8.
10. Contract-fake run of the composite routes of SCR-02 and SCR-04; test for AC10.

**Done when.** The tests in section 16 pass, the RWB-P2-E2001-CON contract tests stay green, REC-01 for SIT business date 2026-12-14 shows zero unexplained difference, and no case in the run was built from a business date whose batch was not complete.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | Data product stale after an incomplete ACE batch | {product} is from {date}. Today's load has not arrived. |
| MSG-P2-007 | Case creation held for an incomplete ACE batch | Case creation for {date} is held until a load passes its checks. {count} accounts are waiting. |
| MSG-P7-003 | Decision record write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P2-006 | Rerun while the entry run is in flight | {job} is already running. Wait until it ends before you run it again. |
| MSG-P4-002 | A role without the Case record right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the caller's scope | This case is not in your scope. |
| MSG-GEN-006 | rwb-integration or rwb-source-data unavailable | {system} is not available. Your request is queued and will be retried. |

For MSG-GEN-006, {system} is "rwb-integration" when the hand-over read fails and "rwb-source-data" when the ledger append or the break write fails.

### 15. Screens and states

SCR-02 Case list (states loading, list) shows the new case with its case number, status "New", product group and entry date. SCR-04 Case timeline (states loading, filtered) shows the EFS entries with source "EFS" and their action codes, filtered by type and period. SCR-45 Data quality (states loading, list, read only) shows the held runs and the REC-05 break to the data steward.

All three are served by the gateway-bff composite route, which calls rwb-case and rwb-source-data in parallel, one hop each, and merges the answers into the screen model; the browser never calls an owner service directly (DP-19). The screen fields, the masking of personal fields and the merge order are Not specified in the source documents (GAP-2262; ASM-3726); the full case record view and its timeline remain with RWB-P3-E2016-APP.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-001-01 | AC1, AC9, BR1, BR3, BR5 | Component | rwb-integration stub with "A-0001" and 14 contact rows plus 2 promise rows |
| TC-E2-001-02 | AC2, BR6 | Component | Same business date run twice, EV-26 redelivered |
| TC-E2-001-03 | AC5, BR4 | Component | No complete batch for 2026-12-15; the page of 2026-12-16 arrives on 2026-12-17 |
| TC-E2-001-04 | AC3, BR2 | Component | Customer "C-0002" with an open "SSME" case RW-2026-000210 |
| TC-E2-001-05 | AC4, BR8 | Component | Account "A-0003" whose person_key has no customer row |
| TC-E2-001-06 | AC5, BR4 | Component | Good batch on 2026-12-17 after the missed day 2026-12-15 |
| TC-E2-001-07 | AC6, BR7 | Component | Decision-record store stopped |
| TC-E2-001-08 | AC7 | Component | DailyCaseRun running for 2026-12-14; second event and rerun request |
| TC-E2-001-09 | AC8 | Contract | RW-REFADM calls `GET /cases/{caseId}/timeline`; refused with MSG-P4-002 |
| TC-E2-001-10 | AC6, BR7 | NFR | Decision-record write forced to fail across 50 synthetic accounts; no case exists without its record |

The legacy levels map System to Component, Access to Contract and Resilience to NFR (ASM-3724), because the cross-service behaviour of this key is proved by the integration story. The `-ITG` copy of each case is held by the integration story of wave 2. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the threshold, the product map, the copied action codes and the cut-off are rows or parameters with a version.
- No personal data in logs, tests, events or workflow history: logs hold case IDs, business dates and person keys only, never names, account numbers, amounts or identity numbers; workflow payloads pass the payload codec.
- No read of ACE tables and no ACE view in rwb-case: the hand-over comes from the rwb-integration contract and the ledger from rwb-source-data (DP-01, DP-05, DP-18).
- The decision record is written before the case row moves, in one transaction with it; a failed write rolls the whole create or link back (R-UNI-39).
- Every outbound event is written to the outbox in the same transaction as the case row and carries IDs and facts only (DP-09).
- No case is built from a business date whose ACE batch is not complete, and a held run never falls back to an earlier date silently.
- The ledger append is idempotent on `efs_record_key` and no ledger row is copied into `rwb_case`.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-013 | Hand-over arrives in the daily ALS batch | Program 5.2; Epic 2 3.2 | FEAT-CHO-01 | 6.1 Take over the case at 90 days past due | R-UNI-40 | TC-E2-001-01, TC-E2-001-02 |
| REQ-CHO-001 | Case with full contact and promise history | Program 5.3; Epic 2 3.2 | FEAT-CHO-01 | 6.1 | None | TC-E2-001-01, TC-E2-001-05 |
| REQ-CHO-005 | Workbench is the system of record for case state after hand-over | Program 5.3; Epic 2 3.2 | FEAT-CHO-04 | 6.1 | R-UNI-39 | TC-E2-001-04, TC-E2-001-07, TC-E2-001-10 |
| REQ-RDF-003 | EFS history transfers to the case | Program 5.1; Epic 2 3.2 | FEAT-CHO-05 | 6.1 | None | TC-E2-001-03, TC-E2-001-06, TC-E2-001-08 |
| D-RCV-60 DP-18 | The interaction ledger is owned by rwb-source-data; this service appends through its contract and keeps no ledger table | Decision log, D-RCV-60; Template and Rules §R5.5 | FEAT-CHO-01 | 6.1 | BR5 | TC-E2-001-01, TC-E2-001-10 |
| D-RCV-60 DP-10 | The JOB-02 trigger and the 09:00 cut-off are workflow and durable-timer behaviour, not a Quartz row | Template and Rules §R5.5; Arch v5 slide 44 | FEAT-CHO-05 | 6.1 | BR4 | TC-E2-001-03, TC-E2-001-08 |

### 19. Out of scope

- The ACE read, the hand-over adapter, the freshness stamp and the ingestion of the ALS and EFS data (RWB-P2-E2001-APP and RWB-P2-E2001-CON; rwb-source-data stories).
- The interaction ledger store and writer: under DP-18 it is owned by rwb-source-data; the ownership conflict is GAP-2260.
- Allocation of the new case by queue and owner (RWB-P3-E1020-APP; legacy RWB-E1-020).
- The ACE plan status on the case (RWB-P3-E2002-APP).
- The daily reconciliation and the REC-01 and REC-05 break lists themselves, and the `reconciliation_result` table (rwb-source-data; legacy RWB-E1-011).
- The case number sequence and the case of record as a whole (RWB-P3-E1018-APP).
- The case list row set and its filters (RWB-P3-E1002-APP), the full case record view and the timeline screens (RWB-P3-E2016-APP), and the manual ledger entry from the case (RWB-P3-E2034-APP).
- A same-day hand-over event (DL06).
- The deployment of this capability: chart values, topic and queue provisioning, dashboards and the runbook.
