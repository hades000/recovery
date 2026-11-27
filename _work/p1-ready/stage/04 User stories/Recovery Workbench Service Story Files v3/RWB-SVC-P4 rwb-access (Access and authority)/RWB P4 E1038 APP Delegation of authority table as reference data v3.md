# RWB-P4-E1038-APP Delegation of authority table as reference data

**Version 3 changes.**

- MSG-GEN-006 carries the English text of Error and Message Standard v6 (RD-P1-004).

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E1038-APP |
| Readiness decisions | RD-P1-004 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-038 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P4-E1038-APP-16); squad sizes at refinement |
| Patterns applied | DP01, DP03, DP04, DP06, DP07, DP08, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P4-J |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-P4-E1037-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P7-E1027-CON |
| Contract version | Not specified in the source documents (DOR-RWB-P4-E1038-APP-23); the contract path is /api/recovery/access/v1 |
| Contract fake library version | Not specified in the source documents (DOR-RWB-P4-E1038-APP-22) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (FR-P4-012, FR-P4-020, FR-P4-021, FR-P4-022, FR-P4-038) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: realigned from RWB-E1-038 for `rwb-access`, which becomes the only writer of the delegation of authority table. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E1038-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 19 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Risk and model risk officer (RW-RISK)**, I want **the delegation of authority (which approval level may approve which decision, by product, principal amount and second condition) held as a versioned table that the approval router reads**, so that **approval limits change by an approved data load and every approval can be checked against the limit that applied on its date**.

Inside `rwb-access` this is the delegation-of-authority reference-data capability of the legacy story RWB-E1-038, and it is the **only writer** of the table:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- **What this story owns.** The `delegation_limit` table and its per-service Flyway migration in `rwb_access` (DP-01, DP-15); the load of a delegation version and its whole-file validation; the approval of a version with the four-eyes control and the approver role read from a parameter; the version window `valid_from`/`valid_to`; the rollback of a version; the parameter and reference-data reads the load needs (DP-06, DP-07); the authority check behind the load and the approval (DP-08); one access-log entry per approval or refusal (DP-03); and the `rwb.access.DoaLimitChanged.v1` event that tells the other services a version moved.
- **What this story does not own.** The lookup that the approval router calls — level, row and version for one decision and one date — is RWB-P4-E2013-APP's `GET /api/recovery/access/v1/doa-limits`, and it only reads the rows this story writes. The approval record, `ApprovalWorkflow`, the approval endpoints, the case status, the decision task, the escalation and the central decision log entry are `rwb-decision`'s (P7). The rule-package governance of the same authorise-and-date discipline is RWB-P4-E2041-APP and RWB-P4-E2042-APP.
- **The legacy story is moved, not reworked.** Its nine acceptance criteria are carried word for word with the legacy story's numbering; what changes is the transport (four REST operations of this service in place of the monolith reference-load endpoints and the in-process `DelegationOfAuthority` interface) and the schema (one table owned by one service in `rwb_access`). No business value of the legacy story changes.
- **Reference data, not code.** Levels L1 to L6, products, decision codes and regulation items are rows of `delegation_limit` and values of reference lists read through DP-07; the approver role is a parameter read through DP-06. No limit, level, product or role is written in code.

### 2. Business rationale

Approval and authority governance is an audit finding, and limits today sit in the bank regulation and in people's heads. The legacy story loads the 95 limits of Regulation 540031 as amended by Regulation 690070 (chapter 2 for problem loans, chapter 3 for assets held for sale) as versioned rows and gives the approval router one lookup that returns the lowest approval level whose limit covers a decision, with the version used. In the target the table is still the same regulation in rows, but it belongs to one service: `rwb-access` writes it, `rwb-decision` and every approver read it through the contract, and no service keeps a copy of a limit or reads another service's table (DP-01, DP-11).

The target change is therefore a change of custody, not of policy. In the monolith the DoA matrix was a table of the recovery schema, loaded through a generic reference-load endpoint and read in process by `DelegationOfAuthority`. In the target the table is `rwb_access.delegation_limit`, loaded and approved through this service's own operations, and read only through the lookup `GET /api/recovery/access/v1/doa-limits` on the Ownership Map path or the `rwb-access` authorise operation. The version window, the approve-and-date discipline and the four-eyes rule are kept exactly as the legacy story states them, and the same discipline is what the Drools rule packages follow (DP-04): a version is approved by a second person and takes effect on a date, not on the day it was approved.

This story meets REQ-ACA-004 (the delegation of authority table as reference data, setting every limit) and REQ-APD-010 (delegation changes versioned, approved and dated, and open items keep their version). It is the data behind control CTL-04 and supports the measure decisions within the delegation of authority: target 100 percent.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-PLT-E1044-CON | The per-service Flyway sequence and migration conventions (DP-15) that carry `delegation_limit` into `rwb_access` |
| RWB-PLT-E1027-CON, RWB-P7-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the `AC-VERS` entry of an approved version and the `AC-DENY` entry of a refusal |
| RWB-PLT-E1072-CON | The embedded Drools kit (DP-04). This story evaluates no rule; the kit is the build dependency the legacy key carries, because the DoA table follows the approve-and-date discipline of the rule packages and the router that reads it evaluates rules in its own service |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the approver-role parameter `rwb.refload.approver.delegation_limit` |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the reference-data contract of `rwb-case` (DP-07): LOV-DECISION, LOV-APPROVAL-LEVEL and LOV-PRODUCT with the version in force |
| RWB-PLT-E1037-CON, RWB-P4-E1037-CON | The guard library and this service's own authorise contract (DP-08): the role and permission rows behind the Reference data right, with the RFC 9457 refusal shape and MSG-P4-002 |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19). No screen of this story is served through it; it is carried because the delegation version read will be shown in the Epic 8 administration console (SCR-41) |

Business preconditions carried from RWB-E1-038:

- The reference-data load and rollback of the monolith are now this service's own operations, because the Ownership Map gives the generic reference-load path to `rwb-case` and `delegation_limit` to `rwb-access` (GAP-0970; ASM-1704).
- LOV-DECISION holds D5, D6.4, D6.5, D6.6, D7.1, D7.4, D7.5, D8.2, D8.3, D8.4, D9.2 and D9.3; LOV-APPROVAL-LEVEL holds L1 to L6; LOV-PRODUCT holds MORTGAGE, HIRE_PURCHASE, SSME and UNSECURED. Under the R-PREC default ruling these are reference-data rows of `rwb-case`, read through DP-07, not rows of `rwb_access`.
- The parameter `rwb.refload.approver.delegation_limit=RW-RISK` exists in the parameter catalog of `rwb-case`, read through DP-06.
- The holder and substitute of each level are not yet named (DL18); rows load with `holder_user_id` and `substitute_user_id` empty in PROD and with named test users in SIT and UAT.
- The version in force in SIT is DOA-2026.11: 218 rows, 109 for MORTGAGE and 109 for SSME, with item 2.1.1 at L4 as two rows and item 2.1.10 at L1 on the related-party flag.
- The rollback of a version is in this story's scope, and no legacy acceptance criterion covers it (GAP-0971; ASM-1705).

### 4. Flow

1. Reference data administrator (RW-REFADM) converts the Delegation of authority matrix to the load file: one row per limit and decision code, for MORTGAGE and SSME, amounts converted from THB million to baht, "No limit" to an empty value, "Up to X%" to `loss_pct_limit`, "At least X%" against fair market value to `min_price_pct_fmv`, "Once" and "Twice" to `max_delay_count`.
2. RW-REFADM calls `POST /api/recovery/access/v1/admin/doa-loads` with the file, `table` = `delegation_limit`, `validFrom` and the version name, for example DOA-2026.11, and an `Idempotency-Key`. The path is this service's own, because the generic reference-load path of the monolith is `rwb-case`'s under the Ownership Map (GAP-0970; ASM-1704).
3. `DoaLoadController` validates the call: `table` must be `delegation_limit`, which is the only table this path accepts; `validFrom` and the version name are required, and an empty one is 422 with MSG-GEN-001 naming the field; a version name already loaded is 409 with MSG-GEN-004; a missing `Idempotency-Key` is 422. A repeated key answers the stored answer of the first call and writes no second row.
4. `DoaLimitLoader` validates the file whole, never row by row: every decision code, approval level and product must be a value of the reference lists in force (LOV-DECISION, LOV-APPROVAL-LEVEL, LOV-PRODUCT, read through DP-07 and never written in code); every required field must be present; no two rows may repeat the same decision, regulation item, product, level and limits; and no level's highest principal limit may fall from L6 up to L1. Any failure refuses the load in full with 422 and MSG-P1-002 naming the check and the row, and stores no row.
5. On pass, `DoaLimitLoader` inserts all rows of the version in one transaction with the same `limit_version`, `valid_from` and status Loaded, and answers 201 with the load, the row count (218 for DOA-2026.11) and the difference report against the version in force: rows added, rows removed and rows changed, by decision, regulation item, product, level and limit.
6. Risk and model risk officer (RW-RISK) reviews the difference report and calls `POST /api/recovery/access/v1/admin/doa-loads/{loadId}/approve`.
7. `FourEyesRule` and `ApproverRoleReader` check the approval: the approver reference of the caller must differ from the load's author reference, or the call is refused with MSG-P7-002; and the caller must hold the role the parameter `rwb.refload.approver.delegation_limit` names, or the call is refused with 403 and MSG-P4-002. The authority is the parameter role, not the Reference data A letter that the legacy contract document declares and no role holds.
8. On pass, `DoaVersionService` approves in one transaction: the rows of the new version move from Loaded to Approved; `valid_to` of the rows of the previous version is set to the day before the new `valid_from`; one decision-record entry of the DP-03 library is appended with decision code `AC-VERS`, the version, `valid_from`, the approver reference and no case; and the outbox row is written. An approval that cannot be recorded does not take effect: the transaction rolls back, the call returns 503 with MSG-P7-003 and the version stays Loaded.
9. After the commit, the outbox relay publishes `rwb.access.DoaLimitChanged.v1` on `rwb.access.events.v1`, keyed on the delegation version, so the other services refresh their cached reference view. The event carries the version, the table, the change kind and the two dates, and no personal data (GAP-0972; ASM-1706). The outbox row is written through the library created in `rwb_access`; the library's own contract is a service-baseline dependency rather than a row of this story's metadata (GAP-0973; ASM-1707).
10. `POST /api/recovery/access/v1/admin/doa-loads/{loadId}/rollback` is the inverse of the approval, one call: the caller must hold the same approver role, the same four-eyes rule applies, the window of the rolled-back version and of the version before it is reversed, one `AC-VERS` entry records the rollback and the event is published. Only a version inside its own window may be rolled back; an approved version whose `valid_to` has passed is history and is never reopened (GAP-0971; ASM-1705).
11. `GET /api/recovery/access/v1/admin/doa-versions` reads the versions with their state, `valid_from`, `valid_to`, row count, author and approver reference for RW-AUDIT and for the administration console. It is read only and carries the Reference data R right.
12. Every refusal of an approval or a rollback appends one decision-record entry with decision code `AC-DENY`, the version, the caller reference and the reason refused, and no personal data. A refusal of a load file at validation writes no record, because no row of that version was ever accepted and the legacy story stores nothing.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A file repeats a decision, regulation item, product, level and condition, or a level's highest principal limit falls below a lower level's | The load is refused in full; the version in force stays | MSG-P1-002 | AC4 |
| X2 | A file holds an unknown decision code, level or product, or a required field is empty | The load is refused in full | MSG-P1-002 | AC4 |
| X3 | The person who loaded the version approves it | Refused; the version stays Loaded; one AC-DENY entry with both references | MSG-P7-002 | AC5 |
| X4 | A role other than the parameter's approver role approves | Refused with 403; one AC-DENY entry with the area and the right | MSG-P4-002 | AC5 |
| X5 | The decision-record write for the approval fails | The version is not approved and stays Loaded; the transaction rolls back | MSG-P7-003 | AC6 |
| X6 | A lookup finds no row for the decision and product, for example hire purchase before the chapter 8 limits arrive | The lookup answers `NOT_COVERED` (RWB-P4-E2013-APP) and `rwb-decision` raises the incident to RW-RISK; this story supplies the rows and no incident path of its own | MSG-P7-010 (produced by `rwb-decision`) | AC7 |
| X7 | A lookup date falls on the last day of the old version or the first day of the new one | The version valid on that date is used, because `valid_to` of the old version is the day before `valid_from` of the new one | None | AC8 |
| X8 | A write-off is for a director, senior executive, major shareholder or related party | The L1 row of item 2.1.10 is stored with the related-party condition, so the lookup answers L1 whatever the amount | None | AC9 |
| X9 | The version name already exists | 409, nothing stored | MSG-GEN-004 | AC1 |
| X10 | A rollback is called on a version whose window has already closed | 409, nothing changed; an approved version that has expired is never reopened | MSG-GEN-004 | AC10 |
| X11 | A rollback is called by a caller other than the approver role, or by the version's loader | 403 with MSG-P4-002, or MSG-P7-002 for the loader; one AC-DENY entry | MSG-P4-002, MSG-P7-002 | AC11 |
| X12 | The reference-data or parameter read is unavailable when a load arrives | 503, nothing stored; the load is retried under the same `Idempotency-Key` | MSG-GEN-006 | AC1 |

No exception path of this story changes a case, a task or an approval: this service writes the delegation table and the versions, and the state machine of an approval is `rwb-decision`'s.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the platform contract stories, the parameter and reference-data contracts and its own authorise operation; the lookup that consumes the table is RWB-P4-E2013-APP's and the two stories share only the table |
| Negotiable | Limits, levels, products, regulation items, conditions, holders, substitutes and versions are rows; the approver role is a parameter; no value is fixed in code |
| Valuable | One approved, dated, four-eyes version of the regulation replaces a table that every module copied and a limit that lived in a document |
| Estimable | One migration, one loader, one approval gate, one rollback, one version read, one record appender, one event |
| Small | Fits two weeks with its tests; there is no screen, no workflow and no case state |
| Testable | Each of the nine owned criteria has a test case in section 16, and the lookup half of AC2, AC7, AC8 and AC9 is exercised against the published lookup contract and its fake |

### 7. Acceptance criteria

```gherkin
Feature: Delegation of authority table as reference data

  Background:
    Given the environment is SIT
    Given test user "U-3101" holds RW-REFADM and test user "U-3102" holds RW-RISK

  Scenario: AC1 Table loaded (legacy RWB-E1-038 AC1)
    Given the delegation of authority file "DOA-2026.11" built from Regulation 540031 as amended by Regulation 690070, with 95 limits
    When "U-3101" loads it with table "delegation_limit" and validFrom "2026-11-30" and "U-3102" approves it
    Then the system stores 218 rows : 109 decision and limit rows for MORTGAGE and 109 for SSME
    Then every row has a decision code, an approval level and a product, and no two rows repeat the same decision, regulation item, product, level and limits
    Then the system stores item 2.1.1 at level L4 as two rows: principal 300,000,000.00 with loss up to 45.00 percent and maximum loss 150,000,000.00, and principal 50,000,000.00 with no loss limit

  Scenario: AC2 Lookup (legacy RWB-E1-038 AC2)
    Given "DOA-2026.11" is in force
    When the router asks who may approve decision D6.4, item 2.1.1, product MORTGAGE, principal 2,400,000.00, loss 20.00 percent and loss amount 480,000.00 on 15 December 2026
    Then the lookup returns level L6, the row ID of item 2.1.1 at L6 (Not specified in the source documents (ACR-RWB-P4-E1038-APP-AC2)) and version "DOA-2026.11"

  Scenario: AC3 Change (legacy RWB-E1-038 AC3)
    Given "DOA-2026.11" is in force
    Given file "DOA-2027.01" adds a row for item 2.1.5 at level L5 with principal up to 10,000,000.00, validFrom "2027-01-01"
    When "U-3101" loads it and "U-3102" approves it
    Then the rows of "DOA-2026.11" stay readable with valid_to "2026-12-31"
    Then a lookup for D6.6, item 2.1.5, MORTGAGE, principal 8,000,000.00 dated 2 January 2027 returns L5 and version "DOA-2027.01"
    Then one decision log entry records the approval of "DOA-2027.01" with its valid from date

  Scenario: AC4 A file with an error is refused in full (legacy RWB-E1-038 AC4)
    Given file "DOA-2026.12" gives item 2.1.1 at L5 a principal limit of 400,000,000.00, above the 300,000,000.00 of L4
    Given it gives one row the decision code "D6.9"
    When "U-3101" loads it
    Then the system refuses the load with message MSG-P1-002 naming the falling limit and the unknown decision code
    Then the system stores no row of "DOA-2026.12" and "DOA-2026.11" stays in force

  Scenario: AC5 The loader cannot approve and only Risk may (legacy RWB-E1-038 AC5)
    Given load "DOA-2027.01" was loaded by "U-3101"
    When "U-3101" calls approve on it
    Then the system refuses the call with message MSG-P7-002
    Then when test user "U-3103" holding RW-PRODHEAD calls approve on it
    Then the system refuses the call with status 403 and message MSG-P4-002

  Scenario: AC6 An approval that cannot be recorded does not take effect (legacy RWB-E1-038 AC6)
    Given the decision log store is unavailable
    When "U-3102" approves load "DOA-2027.01"
    Then the call returns status 503 with message MSG-P7-003 and the load stays "Loaded"

  Scenario: AC7 No limit covers the request (legacy RWB-E1-038 AC7)
    Given "DOA-2026.11" holds no row for product HIRE_PURCHASE
    When the router asks who may approve decision D6.4, item 2.1.1, for HIRE_PURCHASE, principal 900,000.00
    Then the lookup returns "NOT_COVERED"
    Then the system raises an incident to the RW-RISK queue with message MSG-P7-010 naming D6.4 and HIRE_PURCHASE

  Scenario: AC8 The version valid on the decision date is used (legacy RWB-E1-038 AC8)
    Given "DOA-2026.11" is valid to 31 December 2026 and "DOA-2027.01" from 1 January 2027
    When the router looks up D6.6, item 2.1.5, MORTGAGE, principal 8,000,000.00 dated 31 December 2026 and again dated 1 January 2027
    Then the first lookup returns L4 and "DOA-2026.11"
    Then the second returns L5 and "DOA-2027.01"

  Scenario: AC9 A write-off for a related party goes to the Board (legacy RWB-E1-038 AC9)
    Given "DOA-2026.11" is in force
    When the router asks who may approve decision D9.2, item 2.1.10, criteria met, product SSME, principal 300,000.00, with related party flag true
    Then the lookup returns level L1 with reason "RELATED_PARTY" as a coded value on the answer, read from the row whose applies_when condition is the related-party one; the condition text stays in the row only

  Scenario: AC10 A rollback is refused when the window has closed (new, D-RCV-60)
    Given "DOA-2026.11" is approved and its window has closed
    When "U-3102" calls rollback on it
    Then the system refuses the call with status 409 and message MSG-GEN-004, nothing changes and the version is not reopened

  Scenario: AC11 A rollback by a caller other than the approver, or by the loader, is refused and writes one AC-DENY entry (X11) (new, D-RCV-60)
    Given "DOA-2027.01" was loaded by "U-3101"
    When "U-3101" calls rollback on it
    Then the system refuses the call with message MSG-P7-002 and writes one AC-DENY entry
    Then when test user "U-3103" holding RW-PRODHEAD calls rollback on it
    Then the system refuses the call with status 403 and message MSG-P4-002 and writes one AC-DENY entry

  Scenario: AC12 A call without a valid credential is refused with 401 and a call on a version that does not exist with 404 (new, D-RCV-60)
    When a caller without a valid credential calls a provided operation of rwb_access
    Then the call returns status 401 and nothing is stored
    When "U-3101" calls rollback on a version name that does not exist
    Then the call returns status 404 and nothing changes
```

The nine criteria are carried word for word from RWB-E1-038 with their numbering. Two halves are now in different services and neither criterion is split: the **data half** — the rows, the version, the window, the item 2.1.1 pair and the item 2.1.10 L1 row — is this story's and is proved by section 16 against `rwb_access`; the **lookup half** of AC2, AC7, AC8 and AC9 is RWB-P4-E2013-APP's `GET /api/recovery/access/v1/doa-limits` reading these rows, and the incident of AC7 is `rwb-decision`'s. AC1, AC3, AC4, AC5 and AC6 are this story's end to end. AC10 is added for the rollback exception X10 and AC11 for X11; both are this story's end to end and carry no legacy criterion. AC12 covers the 401 and 404 answers of the provided operations and carries no legacy criterion.

- **AC13.** The delay rule holds: a delay of legal action, of seizure or of an auction is within a level's limit only while the count of delays on the case, including this one, is not above the level's max_delay_count (BR6).
- **AC14.** No value a business person may change is written in code: levels, limits, conditions, products, regulation items, holders, substitutes and versions are rows, and a new decision code, level or product is a row and a list value that needs no code change (BR11).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Limits are held as the regulation states them: principal limit in baht, loss as a percentage, maximum loss in baht, payment or price against fair market value, and price against principal outstanding; an empty limit means no limit | delegation_limit fields DF-REF-020 to DF-REF-022; Delegation of authority matrix, Key sheet |
| BR2 | Where a level has two rows, the approval is within limit if either row is met | Delegation of authority matrix, How it applies, rule 3 |
| BR3 | The lowest level, from L6 up to L1, with a row for the decision code and regulation item valid on the decision date that covers the request is the level returned | LOV-APPROVAL-LEVEL; FEAT-APD-10 |
| BR4 | A decision that no limit covers goes to the next level up; a decision and product with no row at any level returns NOT_COVERED and raises an incident | Delegation of authority matrix, How it applies, rule 8 |
| BR5 | A write-off for a director, senior executive, major shareholder or related party goes to the Board (L1) | Delegation of authority matrix, How it applies, rule 6 |
| BR6 | A delay of legal action, of seizure or of an auction is within a level's limit only while the count of delays on the case, including this one, is not above the level's delay count | Delegation of authority matrix, How it applies, rule 4; items 2.1.3 and 2.1.6 |
| BR7 | A decision keeps the version it was approved under; a new version applies from its valid from date | Delegation of authority matrix, How it applies, rule 9; R-UNI-38; REQ-APD-010 |
| BR8 | A limit change is a data load approved by Risk, never by its loader | Delegation of authority matrix, How it applies, rule 11; CTL-08; separation of duty, reference data administrator and Risk |
| BR9 | Hire purchase and unsecured limits follow chapter 8 of credit approval regulation 450032 and load when supplied | Delegation of authority matrix, How it applies, rule 7; DL18 (open decision; assumptions ASM-2569, ASM-2839, ASM-2859, ASM-2883) |
| BR10 | A version approval that cannot be written to the decision log does not take effect | Principle 5; R-UNI-39 |
| BR11 | No value a business person may change is written in code: levels, limits, conditions, products, regulation items, holders, substitutes and versions are rows, the lists are reference data with a version and the approver role is a parameter | BR-P4-006; FSD P4 v3 A2.6 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 and BR2 are columns of `delegation_limit` and the two item 2.1.1 rows of the same level; the table stores baht with two decimals and never converts or rounds at read time.
- BR3, BR4, BR5 and BR6 are execution rules of the lookup, and the lookup is RWB-P4-E2013-APP's. This story stores what those rules need: the regulation item on every row, the two `applies_when` values of item 2.1.10, `max_delay_count`, `min_price_pct_principal`, `min_received_pct` and `max_term_years`.
- BR7 is the `valid_from`/`valid_to` window: an approval closes the previous version on the day before the new `valid_from`, and the rows stay readable, so a dated lookup and an item routed under an older version both keep their version.
- BR8 is the four-eyes rule plus the approver-role parameter; the loader's reference is stored with the load and compared with the approver's.
- BR9 is data: the chapter 8 rows load when the matrix supplies them, and their absence is the `NOT_COVERED` answer of AC7, not a code path.
- BR10 is the transaction: the decision-record entry and the version state commit together, and a failure leaves the version Loaded.
- BR11 is checked by test: a new decision code, level or product is a row and a list value, and the build changes nothing.

### 9. State transitions

This service holds no case, task or approval state. It holds the lifecycle of a delegation version and the window of its rows.

| From | Event | Condition | To |
|---|---|---|---|
| (none) | Load of a file that passes whole-file validation | Every code is a list value, no repeated tuple, no level's limit falls | Version Loaded, rows stored, previous version still in force |
| (none) | Load of a file that fails validation or names an existing version | Any check fails, or the version name exists | Nothing stored; the version in force stays |
| Loaded | Approval by the parameter's approver role, not the loader | The decision-record entry is written | Version Approved; previous version's `valid_to` set to the day before the new `valid_from` |
| Loaded | Approval by the loader, by another role, or with an unwritable record | Four eyes fails, role fails, or the record fails | Version stays Loaded |
| Approved, inside its window | Rollback by the parameter's approver role | The previous version exists and the version is inside its window | Window reversed, rollback recorded, version no longer in force |
| Approved, window closed | Rollback | The version has expired | Refused; history is not reopened |
| Approved | Its `valid_from` arrives | A lookup is dated on or after `valid_from` | In force for its dates; older versions readable for theirs |

| Command | Condition | Outcome |
|---|---|---|
| Load | Caller holds the Reference data C right and the file passes | 201, version Loaded, difference report answered |
| Approve | Caller holds the parameter's approver role, is not the loader, and the record commits | 200, version Approved, one `AC-VERS` entry |
| Approve | Caller is the loader, or holds another role, or the record fails | Refused, version Loaded, one `AC-DENY` entry except when nothing can be recorded |
| Rollback | Caller holds the parameter's approver role, is not the loader, and the version is inside its window | 200, window reversed, one `AC-VERS` entry |
| Read versions | Caller holds the Reference data R right | 200, the versions with their states and windows |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-REFADM Reference data administrator | Prepares and loads a delegation version (Reference data C). Approves none |
| RW-RISK Risk and model risk officer | Approves and rolls back a delegation version; the approver role is the parameter `rwb.refload.approver.delegation_limit`, never a role written in code |
| RW-PRODHEAD Product head | Agrees the limits for their product with Risk before the load; may not approve the load |
| Risk with the product heads | Name the holder and substitute of each level (DL18) |
| Approval levels L1 to L6 | Board of Directors, Executive Committee, Problem Asset Resolution Committee or Management Committee, Head of Recovery at function level, Recovery executive at division level, Recovery executive at department level. Levels L1 to L3 approve by committee resolution recorded in the decision log; L4 to L6 approve in the Workbench |
| RW-AUDIT Internal audit | Reads every version and its approval entry through `GET /api/recovery/access/v1/admin/doa-versions`; it writes nothing |
| SY-RULES Drools evaluator, and the other service identities | Call the lookup of RWB-P4-E2013-APP under the Approval check R right; they hold no write path to this table |
| `rwb-access` itself | Writes `delegation_limit`, its version rows and its outbox rows; reads `role` and `permission` in its own schema for the Reference data right |

The refusal shape is 403 with an RFC 9457 problem response and `messageId` set, MSG-P4-002 for a missing right and MSG-P7-002 for the loader approving its own load. FSD P4 v3 A2.6.3.3 names the Security administrator as the primary actor of the DoA feature; the loader and the approver here are the legacy story's and the parameter's, and the FSD role table is read as the generic feature-role table (GAP-0974; ASM-1708). The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-E1037-CON.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-016 | `delegation_limit` | id | Write, read |
| DF-REF-017 | `delegation_limit` | decision_code | Write, read |
| DF-REF-018 | `delegation_limit` | approval_level | Write, read |
| DF-REF-019 | `delegation_limit` | product_group | Write, read |
| DF-REF-020 | `delegation_limit` | principal_limit | Write, read |
| DF-REF-021 | `delegation_limit` | loss_pct_limit | Write, read |
| DF-REF-022 | `delegation_limit` | min_price_pct_fmv | Write, read |
| DF-REF-023 | `delegation_limit` | holder_user_id | Write, read |
| DF-REF-024 | `delegation_limit` | substitute_user_id | Write, read |
| DF-REF-025 | `delegation_limit` | valid_from | Write, read |
| DF-REF-026 | `delegation_limit` | valid_to | Write, read |
| DF-REF-055 | `delegation_limit` | limit_version | Write, read |
| DF-REF-056 | `delegation_limit` | regulation_item | Write, read |
| DF-REF-057 | `delegation_limit` | applies_when | Write, read |
| DF-REF-058 | `delegation_limit` | max_loss_amount | Write, read |
| DF-REF-059 | `delegation_limit` | max_delay_count | Write, read |
| DF-REF-060 | `delegation_limit` | min_price_pct_principal | Write, read |
| DF-REF-061 | `delegation_limit` | min_received_pct | Write, read |
| DF-REF-062 | `delegation_limit` | max_term_years | Write, read |
| (standard record columns) | `delegation_limit` | is_active, state, version, created_at, created_by, updated_at, updated_by | Write, read |
| DF-REF-159 to DF-REF-184 | `reference_version`, `reference_row` of `rwb-case` | LOV-DECISION, LOV-APPROVAL-LEVEL and LOV-PRODUCT with the version in force | Read through the reference-data contract (DP-07) |
| (parameter) | `parameter_value` of `rwb-case` | `rwb.refload.approver.delegation_limit` | Read through the parameters contract (DP-06) |
| DF-REF-034 to DF-REF-044 | `role`, `permission` of `rwb_access` | the caller's Reference data letters | Read |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the `AC-VERS` and `AC-DENY` entries of a version | Write |
| (outbox) | outbox library table in `rwb_access` | the record row and the `DoaLimitChanged` row | Write |
| (inbox) | `processed_event` | none: this story consumes no event | None |

No row of `decision_log_entry`, `approval`, `case` or `task` is read or written: `decision_log_entry` and `approval` are `rwb-decision`'s (P7) and the case and its task are `rwb-case`'s (P3), and nothing of this story needs them. `lov_value`, `reference_version`, `reference_row`, `parameter_catalog` and `parameter_value` are reference data and parameters of P3 under the Ownership Map and are read through DP-07 and DP-06, not from `rwb_access`. Field IDs are those in the Logical Data Model and Data Dictionary v9; TSD P4 v3 T3.1 is the field list of `delegation_limit`.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| POST | `/api/recovery/access/v1/admin/doa-loads` | P4 `rwb-access` | Multipart: file, `table` = `delegation_limit`, `validFrom`, `limitVersion` | 201 `DoaLoad`: id, table, limitVersion, validFrom, status "Loaded", rowCount, differenceReport | 401; 403 no Reference data C (MSG-P4-002); 409 version name exists (MSG-GEN-004); 422 validation failed (MSG-P1-002, MSG-GEN-001); 503 reference read or store unavailable (MSG-GEN-006) | Reference data, right C | `Idempotency-Key` required |
| POST | `/api/recovery/access/v1/admin/doa-loads/{loadId}/approve` | P4 `rwb-access` | None | 200 `DoaVersion`: limitVersion, validFrom, validTo, status "Approved", rowCount, approverReference | 401; 403 not the parameter's approver role (MSG-P4-002); 404 load outside the role's scope (MSG-P4-003); 409 caller loaded it (MSG-P7-002) or load not "Loaded" (MSG-GEN-004); 503 decision record not written (MSG-P7-003) | The approver role named by the parameter `rwb.refload.approver.delegation_limit`, checked instead of the Reference data A letter that no role holds | `Idempotency-Key` required |
| POST | `/api/recovery/access/v1/admin/doa-loads/{loadId}/rollback` | P4 `rwb-access` | `RollbackRequest`: reason | 200 `DoaVersion` of the version restored | 401; 403 not the approver role (MSG-P4-002) or caller loaded it (MSG-P7-002); 404; 409 window closed or no earlier version (MSG-GEN-004); 503 decision record not written (MSG-P7-003) | The approver role named by the parameter, plus Reference data U | `Idempotency-Key` required |
| GET | `/api/recovery/access/v1/admin/doa-versions` | P4 `rwb-access` | Query: table, state, from, to, page, size | `DoaVersion[]`: limitVersion, validFrom, validTo, status, rowCount, authorReference, approverReference | 401; 403 no Reference data R (MSG-P4-002); 422 unknown query field (MSG-GEN-001); 503 | Reference data, right R | Not applicable, read only |

The four paths are this service's own, because the generic reference-load operations the monolith names are `rwb-case`'s under the Ownership Map and `delegation_limit` is P4's table (GAP-0970; ASM-1704). The `DoaLoad`, `DoaVersion`, `DifferenceReport` and `RollbackRequest` shapes are proposed by this story and confirmed or renamed at contract review; the OpenAPI 3.1 document of RWB-P4-E1037-CON carries them. The lookup `GET /api/recovery/access/v1/doa-limits` is **not** in this table: it is served once by `rwb-access` on the Ownership Map path; its answer over the DoA table is RWB-P4-AD016-APP's, and RWB-P4-E2013-APP owns only the routing that consumes the answer and holds no second copy of the path. This story only supplies the rows. The lookup division is still to be confirmed at contract review. The generic reference-load and rule-version paths stay P3's and P7's and are not reused for the DoA table; RWB-P4-AD016-APP builds the load-and-approve journey and the lookup on these four paths and declares none of them.

#### 12.2 REST operations consumed

None. This story calls no REST operation. The approver role is read in process through the parameters client library of DP-06 and the three lists through the reference-data client library of DP-07, each with a 2 s cached read; the role and permission rows are read in its own schema through RWB-P4-E1037-CON's contract.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.access.DoaLimitChanged.v1` | `rwb.access.events.v1` | P4 | limitVersion | limitVersion, table `delegation_limit`, the change kind (loaded, approved, rolled back), validFrom, validTo, rowCount, and no personal data |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | the hash-chained `AC-VERS` or `AC-DENY` entry of a version |

CloudEvents 1.0 envelope; neither payload carries a name, an e-mail address or a personal field, and the holder and substitute are user references. The event is published by the outbox relay after the transaction commits, so a consumer never sees a version that did not commit. Its payload and key are proposed here (GAP-0972; ASM-1706) and the outbox row is written through the library created in `rwb_access` (GAP-0973; ASM-1707).

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 (events: none), and this story adds no subscription. The rule packages of RWB-P4-E2042-APP and the access-policy cache are other capabilities of the same service.

#### 12.5 Workflows and activities

None. This story starts no workflow, signals no workflow and registers no activity on the `rwb-access` queue. The load and the approval are two calls with a human decision between them, not a workflow: the legacy story has no timer, no escalation and no saga, and a workflow would add a state that nobody owns.

#### 12.6 Schedules

None for this story. The six-monthly access review list (JOB-18) is a Temporal Schedule of `rwb-access` and belongs to the service's own story.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `delegation_limit` | P4 (`rwb_access`) | Created, indexed and written: the rows of each version, the window, the holders and the substitutes. Read by RWB-P4-E2013-APP and by nothing else |
| `role`, `permission` | P4 (`rwb_access`) | Read only: the caller's Reference data letters. Created by RWB-P4-E1037-CON |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | The outbox row of the record and of `DoaLimitChanged`, and the stored answer under `Idempotency-Key`; no inbox row is written because no event is consumed (DP-09) |
| `lov_value`, `reference_version`, `reference_row` | P3 (`rwb_case`) | Not created and not read directly: the lists arrive through DP-07 |
| `parameter_catalog`, `parameter_value` | P3 (`rwb_case`) | Not created and not read directly: the approver role arrives through DP-06 |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written: the central ledger entry is `rwb-decision`'s and the local record goes on `rwb.decision-record.v1` |

No foreign key crosses a schema (DP-01). `delegation_limit` keeps no reference to a case, a role or a list row: its codes are values of lists, not foreign keys, exactly as the regulation is written.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| parameters fake | RWB-PLT-E1042-CON, RWB-P3-E1042-CON | `rwb.refload.approver.delegation_limit` = RW-RISK, and the forced unavailability of X12 |
| reference-data fake | RWB-PLT-E1043-CON, RWB-P3-E1043-CON | LOV-DECISION with D6.9 absent, LOV-APPROVAL-LEVEL (L1 to L6), LOV-PRODUCT (MORTGAGE, SSME, HIRE_PURCHASE), each with its version |
| decision-record fake | RWB-PLT-E1027-CON, RWB-P7-E1027-CON | The record append, the hash-chain check and the forced failure of AC6 |
| authorise and guard fake | RWB-PLT-E1037-CON, RWB-P4-E1037-CON | The Reference data C, A and U answers, and the refusal of a role without the right |
| embedded Drools kit fake | RWB-PLT-E1072-CON | None: this story evaluates no rule. The kit is listed because the legacy key carries it and the router evaluates rules against these rows in its own service |
| Flyway conventions | RWB-PLT-E1044-CON | None as a fake: the migration sequence and the naming of the `rwb_access` baseline are the convention this story follows |
| gateway-bff route fake | RWB-PLT-N001-CON | None: no screen of this story. The route is listed because the Epic 8 administration console (SCR-41) will read the versions through it |
| lookup contract fake | RWB-P4-E2013-APP | The lookup answer for AC2, AC7, AC8 and AC9, seeded from this story's fixture DOA-2026.11 and DOA-2027.01 |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 4 (3 write, 1 read); consumed 0 | Base `/api/recovery/access/v1` |
| Kafka | Published 2 event types; consumed 0 | `rwb.access.events.v1` and `rwb.decision-record.v1` |
| Temporal | 0 workflows, 0 activities | The `rwb-access` queue serves JOB-18 and other stories |
| File | 1 inbound | The delegation of authority load file, multipart on `POST /admin/doa-loads`; no file output |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/doa`, Java package `th.co.scb.ace.workbench.recovery.access.doa`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

How each pattern lands in this slice:

- **DP-01 and DP-15** are the same act: `delegation_limit` moves from the monolith recovery schema to `rwb_access` in this service's own Flyway sequence, and no other schema is read. The legacy table's columns are kept and the eight regulation columns of DF-REF-055 to DF-REF-062 are added.
- **DP-03** is the access log: the `AC-VERS` entry of an approved version, the `AC-VERS` entry of a rollback and the `AC-DENY` entry of a refusal are decision-record entries of the local library, so the access log and the decision log are one append-only chain and there is no separate access-log table in `rwb_access`.
- **DP-04** is carried, not applied: this story evaluates no rule. The build dependency on the embedded kit is here because the DoA table follows the approve-and-date discipline of the Drools packages (Temporal and Drools design slide 6) and because the router that reads these rows evaluates rules in its own service. `RWB-P7-E1073-CON` is not a dependency of this story: no rule package is loaded or evaluated here, and the rule packages of the legacy key are RWB-P4-E2041-APP's and RWB-P4-E2042-APP's.
- **DP-06** is one parameter: the approver role of the table. It is read with the version in force and never written in code, which is what lets AC5 refuse RW-PRODHEAD without a release.
- **DP-07** is three lists: LOV-DECISION, LOV-APPROVAL-LEVEL and LOV-PRODUCT. The loader validates a file against them and stores no enum, so a new decision code is a row and a list value.
- **DP-08** is the Reference data right behind the load, the version read and the rollback; the approver role is checked in addition, because the legacy contract declares a Reference data A letter that no role holds.
- **DP-11** is the legacy in-process `DelegationOfAuthority.lowestLevel` call: in the target it is a REST call to RWB-P4-E2013-APP's lookup, one hop, 2 s timeout and a cached answer on the caller's side. This story publishes the rows that call reads and answers nothing itself.
- **DP-13** is the base `/api/recovery/access/v1` for the four operations.
- **DP-19** is carried: no screen of this story, and the Epic 8 administration console (SCR-41) will read the versions through the gateway-bff composite route.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DoaLoadController | Controller | The four operations: request validation, `Idempotency-Key`, RFC 9457 problem responses |
| DoaLimitLoader | Service | Whole-file validation against the lists of DP-07, the repeated-tuple check, the falling-limit check from L6 to L1, and the insert of one version in one transaction |
| DoaDifferenceReport | Service | The difference report of a load against the version in force: rows added, removed and changed |
| FourEyesRule | Service | The load's author reference against the approver reference; a service-identity author may be approved by a person |
| ApproverRoleReader | Service | The approver role from `rwb.refload.approver.delegation_limit` through DP-06; no role in code |
| DoaVersionService | Service | Approval, previous-version close, rollback and the window arithmetic on `valid_from`/`valid_to` |
| DelegationLimitRepository | Repository | Writes and reads `delegation_limit` in `rwb_access`; the only class in the service with a write method on the table |
| AccessLogWriter | Service | The `AC-VERS` and `AC-DENY` decision-record entries and their outbox rows, in the transaction that produces the answer |
| DoaLimitChangedPublisher | Service | The `rwb.access.DoaLimitChanged.v1` outbox row after a load, an approval or a rollback |

**Database and migrations**

- One migration in the `rwb_access` sequence of DP-15, with the legacy stem `V_E1_038`: `delegation_limit` with DF-REF-016 to DF-REF-026 and DF-REF-055 to DF-REF-062, the standard record columns of TSD P4 v3 T3.0, and the lookup index `ix_delegation_lookup` on (`decision_code`, `regulation_item`, `product_group`, `approval_level`, `valid_from`) where `is_active`.
- The eight added columns are `limit_version varchar(20) not null`, `regulation_item varchar(10) not null`, `applies_when varchar(40)`, `max_loss_amount numeric(18,2)`, `max_delay_count integer`, `min_price_pct_principal numeric(5,2)`, `min_received_pct numeric(5,2)` and `max_term_years numeric(4,1)`.
- The version window is data, not a second table: one version is the set of rows that share `limit_version` and `valid_from`, and its window is the shared `valid_from` and `valid_to`. The index is built for the lookup of RWB-P4-E2013-APP, which is the only reader on the hot path.
- `delegation_limit` is never updated except to move a version's state and its `valid_to`; a limit change is always a new version, so an approved version's rows are never edited (BR7).
- The write path is one transaction per call: rows or state, the decision-record entry and the outbox row commit together or not at all.

**Configuration and reference data**

- DOA-2026.11 (RW-REFADM loads, RW-RISK approves) is the version in force in SIT: 218 rows, 109 for MORTGAGE and 109 for SSME, item 2.1.1 at L4 as two rows, item 2.1.10 at L1 on the related-party flag. DOA-2027.01 is the change fixture of AC3 and AC8.
- `applies_when` values `WO_CRITERIA_MET` and `WO_CRITERIA_NOT_MET` for the two write-off rows of item 2.1.10, loaded with the version.
- The approver role is the parameter `rwb.refload.approver.delegation_limit=RW-RISK`, read through DP-06. No role name is written in code.
- LOV-DECISION, LOV-APPROVAL-LEVEL and LOV-PRODUCT are read through DP-07 with the version in force; the loader rejects a value that is not in the list in force and names the row.
- Holders and substitutes load empty in PROD and as named test users in SIT and UAT (DL18).

**Build steps**

1. The migration and the index of `delegation_limit` in the `rwb_access` sequence; a test that the table, its columns and the index exist and that a duplicate tuple is refused by a unique constraint.
2. `DoaLimitLoader`: whole-file validation, the repeated-tuple check, the falling-limit check from L6 to L1 and the all-or-nothing insert; tests for AC1 and AC4.
3. `DoaDifferenceReport` against the version in force; a test that a load with no difference answers an empty report.
4. `ApproverRoleReader` over DP-06 and `FourEyesRule`; tests for AC5, including a service-identity author approved by a person.
5. `DoaVersionService`: approval, previous-version close and the window arithmetic; the transaction with the record and the outbox row; tests for AC3 and AC6.
6. The rollback of a version and its refusal when the window has closed (GAP-0971; ASM-1705).
7. `DoaLimitChangedPublisher` and the outbox row; a test that no event is published when the transaction rolls back (GAP-0972; ASM-1706).
8. The contract-fake run of the four operations in isolation, the version read for RW-AUDIT, and the seeded fixture that lets RWB-P4-E2013-APP prove AC2, AC7, AC8 and AC9 against this story's rows.

**Feature switch.** `rwb.access.delegation-table`. Off, the four operations are not served and the table holds no version in force, so a lookup answers `NOT_COVERED` and no approval can be routed by limit. On is the state SIT and UAT run in. A rollback is the switch for one version, not for the capability.

**Done when.** The tests in section 16 pass; DOA-2026.11 is in force in SIT with 218 rows reconciling to the 95 limits of the matrix; the item 2.1.1 L4 pair and the item 2.1.10 L1 row are readable at their dates; a file with a falling limit or an unknown decision code is refused whole; the loader cannot approve its own load and another role cannot approve at all; an approval whose record cannot be written leaves the version Loaded; a change closes the previous version on the day before its successor; and `rwb.access.DoaLimitChanged.v1` is published on the outbox relay after each committed change.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P1-002 | The delegation file fails validation | The {source} load for {date} was refused: {check}. The previous load is still in use. | This story, on the load |
| MSG-P7-002 | The loader approves their own load | You prepared this decision, so you cannot approve it. | This story, on the approve and on the rollback |
| MSG-P4-002 | A role other than the parameter's approver role approves, or the caller lacks the right | You cannot {action} here. Your role does not include it. | This story |
| MSG-P7-003 | The approval or the rollback cannot be written to the decision log | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story |
| MSG-P7-010 | No limit covers a decision and product | No approval limit covers {decision} for {product}. The item is held and Risk has been told. | `rwb-decision`, from the `NOT_COVERED` answer of RWB-P4-E2013-APP; this story stores the rows and produces no incident |
| MSG-GEN-004 | A second approve of an approved load, an existing version name, or a rollback on a closed window | Someone else changed this record. Reload it to see their change. | This story |
| MSG-GEN-001 | A required field is empty or names a value outside its list | Enter {field}. | This story |
| MSG-P4-003 | A record outside the role's scope | This case is not in your scope. | This story |
| MSG-GEN-006 | A system of record is unavailable | {system} is not available. Try again in a few minutes. | This story |

Every error is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. Thai text for each message follows DL10; the proposed Thai for MSG-P7-010 is unchanged from the legacy additions file. Open decision DL10 rests on assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863.

### 15. Screens and states

No screen is built in this story. Delegation versions arrive by file load until SCR-41 Delegation of authority comes in Epic 8 (RWB-P4-E8008-APP). RW-RISK sees the difference report returned by the load and the approval result; RW-AUDIT reads the versions through `GET /api/recovery/access/v1/admin/doa-versions`.

| Screen | State | Where it is |
|---|---|---|
| DoA table load and approval | Loaded, approved, rolled back | `rwb-access` (this story); the operations are called by the reference-data console and by RW-RISK |
| SCR-41 Delegation of authority | List of versions, one version's rows, a limit change in progress; empty, loading, error and no access: Not specified in the source documents (CG-ALL-5021) | Epic 8 (RWB-P4-E8008-APP), read through `GET /api/recovery/access/v1/admin/doa-versions` and the gateway-bff composite route of DP-19 |
| Access audit query | List over a period | `rwb-access` (legacy RWB-E1-039); the access-log story |

The gateway-bff composite route of DP-19 is not used by this story: the four operations are called by an administrator's console call or by RW-RISK directly, and no screen of the legacy key is served in wave 1.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-038-01 | AC1, BR1, BR2 | Component | Delegation file DOA-2026.11 from the 95 matrix limits, loaded and approved in SIT |
| TC-E1-038-02 | AC2, BR3 | Contract | D6.4 Mortgage request at 2.4 million baht principal and 20 percent loss, against the lookup contract fake seeded from this story's fixture |
| TC-E1-038-03 | AC3, BR7 | Integration | Versions DOA-2026.11 and DOA-2027.01 with the window closed on the day before the successor's valid from |
| TC-E1-038-04 | AC4, BR1 | Component | File with a falling limit and an unknown decision code |
| TC-E1-038-05 | AC5, BR8 | Component | Approve by the loader, then by RW-PRODHEAD |
| TC-E1-038-06 | AC6, BR10 | Component | Decision log store switched off in the test double |
| TC-E1-038-07 | AC7, BR4, BR9 | Contract | Hire purchase request with no rows, answered by the lookup contract fake from this story's fixture |
| TC-E1-038-08 | AC8, BR7 | Integration | Lookups on 31 December 2026 and 1 January 2027 against the two seeded versions |
| TC-E1-038-09 | AC9, BR5 | Contract | D9.2 request with the related party flag, answered from the item 2.1.10 L1 row |
| TC-E1-038-10 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E1-038-11 | Principle 5 | NFR | The decision log write forced to fail during an approval |
| TC-E1-038-12 | BR1 | Component | Boundary rows of each table of section 12.7 (ASM-3438) |
| TC-E1-038-13 | AC13, BR6 | Contract | Delay count on a case equal to the level's max_delay_count, then one above it, against the lookup contract fake seeded from this story's fixture |
| TC-E1-038-14 | AC14, BR11 | Component | A new decision code, level and product added as rows and list values, with no code change |
| TC-E1-038-15 | AC11 | Component | Rollback by the loader, then by RW-PRODHEAD, on a version within its window |
| TC-E1-038-16 | AC12 | Component | A call without a valid credential, and a rollback on a version name that does not exist |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to Component or Contract as the row shows, Access to Component and Resilience to NFR. The four tests whose answer is the lookup (TC-E1-038-02, -07, -08, -09) run against the published lookup contract of RWB-P4-E2013-APP and its fake, seeded from this story's fixture, because the lookup implementation is that story's and the data is this one's; the seven tests of the table, the load, the approval, the refusal and the record run against `rwb_access` directly. The whole legacy set is kept because the legacy key carries it. The ITG copy of the whole set is an integration-harness story and is not written here, so no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in code: levels, limits, conditions, products, regulation items, holders, substitutes and versions are rows; the lists are reference data with a version; the approver role is a parameter (BR11). A test proves that a new decision code, level or product needs no build.
- No personal data anywhere: the load, the approval and the events carry user references, decision codes, amounts and versions. Holders and substitutes are stored as user references, and no name, e-mail address or personal field appears in a log, an event payload, a test or a prompt.
- No read of another service's tables (DP-01): the reference lists and the parameter arrive through DP-07 and DP-06, the access log is the local record of DP-03, and no foreign key crosses a schema.
- One writer: only this story writes `delegation_limit`. RWB-P4-E2013-APP's repository has no write method, and no other service holds a limit row.
- No answer without its record: the version state and the decision-record entry commit together, and an approval that cannot be recorded does not take effect (BR10).
- A version already approved is never edited: a change is a new version, and a rollback moves the window and writes a new entry rather than deleting a row.
- No limit is converted or rounded at load or at read time; amounts are stored in baht with two decimals.
- The load path accepts one table only: `delegation_limit`. A file naming another table is refused, so this service cannot become a second, silent reference-data loader for `rwb-case`'s lists.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-004 | Delegation of authority table as reference data, setting every limit | Epic 1, 3.4 | FEAT-ACA-06 | 17 Run the decision center | BR1, BR2, BR3, BR4, BR5, BR6, BR8, BR9, BR10, BR11 | TC-E1-038-01, TC-E1-038-02, TC-E1-038-04, TC-E1-038-05, TC-E1-038-06, TC-E1-038-07, TC-E1-038-09, TC-E1-038-10, TC-E1-038-12, TC-E1-038-13, TC-E1-038-14 |
| REQ-APD-010 | Delegation changes versioned, approved and dated; open items keep their version | Epic 2, 3.7 | FEAT-APD-10 | 17 Run the decision center | BR7, BR10 | TC-E1-038-03, TC-E1-038-08, TC-E1-038-11 |

| Legacy reference | Where it is kept |
|---|---|
| Version DOA-2026.11 with 218 rows, 95 matrix limits, item 2.1.1 L4 as two rows, item 2.1.10 L1 on the related-party flag | Sections 3, 7, 12.8, 13 |
| Load whole-file validation, the repeated-tuple rule and the falling-limit rule | Sections 4, 5, 7, 8, 13 |
| Four eyes and the approver role from a parameter | Sections 4, 5, 7, 8, 10, 12.1 |
| Version window, previous-version close and the dated lookup | Sections 4, 8, 9, 12.1 |
| MSG-P1-002, MSG-P7-002, MSG-P4-002, MSG-P7-003, MSG-P7-010, MSG-GEN-001, MSG-GEN-004 | Section 14, exception paths |
| Rule IDs R-UNI-38, R-UNI-39, CTL-04, CTL-08, Principle 5 | Sections 2, 8, 17 |
| Legacy key RWB-E1-038, story RWB-P4-E1038-APP, lookup RWB-P4-E2013-APP | Metadata, sections 1, 3, 12 |
| Field IDs DF-REF-016 to DF-REF-026 and DF-REF-055 to DF-REF-062 | Section 11 |
| DL18 holders and substitutes, DL10 Thai messages | Sections 3, 10, 13, 14 |

### 19. Out of scope

- The lookup the router calls — level, row, version, holder and substitute for one decision and one date — and the authority answer behind `POST /api/recovery/access/v1/authorise`: RWB-P4-E2013-APP. This story writes the rows that story reads and answers no lookup.
- The routing of an approval to the holder of the level, the queue, the escalation, the approval record and the central decision log entry: `rwb-decision` (P7).
- The case status, the decision task and the service level timer projection: `rwb-case` (P3).
- Names of holders and substitutes, and the chapter 8 limits for hire purchase and unsecured loans: Risk with the product heads, DL18.
- The rule packages of the legacy key and their governance: RWB-P4-E2041-APP and RWB-P4-E2042-APP.
- The reference-data and parameter store itself, its lists and its versions: `rwb-case` (P3) through DP-06 and DP-07.
- The Delegation of authority screen SCR-41 and moving a limit through screens: Epic 8 (RWB-P4-E8008-APP).
- The integration harness and the `-ITG` copies of the test cases.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
