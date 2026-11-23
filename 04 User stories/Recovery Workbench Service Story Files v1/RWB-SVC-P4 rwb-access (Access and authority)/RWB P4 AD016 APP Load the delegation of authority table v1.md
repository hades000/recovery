# RWB-P4-AD016-APP Load the delegation of authority table

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-AD016-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-016 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP07, DP13, DP19 |
| Parallel lane | L-P4-J |
| Ready to start | After RWB-P4-E1038-APP |
| Depends on (build) | RWB-P4-AD016-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-N001-CON, RWB-P4-E1038-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-016 for rwb-access, which owns the delegation of authority table. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **reference data administrator, with the Risk and model risk officer who approves the version and the access service that answers the approval router**, I want **the delegation of authority table loaded as a dated version, approved by Risk and answered as one lookup by decision, regulation item, product and amount**, so that **approval levels, limits, holders and substitutes change by a data load with effective dates, a wrong file changes nothing, and no code change is needed to route an approval by the regulation**.

Inside `rwb-access` this is the load, approval and lookup journey of the legacy story RWB-AD-016:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- **The split, stated plainly.** The table `delegation_limit` (DF-REF-016 to DF-REF-026, DF-REF-055 to DF-REF-062), its Flyway migration in `rwb_access`, the version window, the difference report, the rollback and the version read are **RWB-P4-E1038-APP's**, which is wave 1 and a build dependency of this story. This story is the legacy RWB-AD-016 journey that sits on that table: the DoA load as the administrator makes it, the whole-file refusal that stores nothing, the approval by Risk with the four-eyes control, and the **lookup answer** the approval router reads.
- **Four operations provided**: `POST /api/recovery/access/v1/admin/doa-loads` (multipart file, query `table` = `delegation_limit` and `validFrom`, `Idempotency-Key` required); `POST /api/recovery/access/v1/admin/doa-loads/{loadId}/approve`; `GET /api/recovery/access/v1/admin/doa-loads/{loadId}` (the load, its row count, version label, validFrom and state); and `GET /api/recovery/access/v1/doa-limits`, the lookup that answers the level, the `delegation_limit` id and the limit version for one decision, regulation item, product and dated amount, or `NOT_COVERED` with an incident reference.
- **Whole file or nothing.** The load validates every row before it stores one: every decision code, approval level and product is a value of LOV-DECISION, LOV-APPROVAL-LEVEL and LOV-PRODUCT in force; every row carries its limit version and its regulation item; no two rows repeat decision, regulation item, product, level and limits; a level's principal limit that rises above the level beneath it is refused as a falling limit; an unknown decision code is refused. Any failure answers MSG-P1-002 naming the check and the row, stores no row, and leaves the version in force in force.
- **Two authorities, two letters.** The load is the C letter in Reference data (RW-REFADM, RW-COE); the approval is the A letter in Rules and parameters (RW-RISK only). The loader can never approve, and a role without the A letter answers 403 with MSG-P4-002.
- **Data**: the rows of `delegation_limit` and their `valid_from`/`valid_to`; one decision-record entry of the DP-03 library per approval or refusal; one `rwb.access.DoaLimitChanged.v1` on `rwb.access.events.v1` through the outbox after the approval commits.
- **The screens.** SCR-41 Delegation of authority is served through the gateway-bff composite route of DP-19 (versions, load, approval). SCR-39 Rules and parameters belongs to the rule-version key RWB-AD-011 and is not served here.

### 2. Business rationale

The delegation of authority is the table that says who may approve what, by decision, product and amount, and it is the one table in the recovery module whose change is a board-level control: the regulation states the limits, Risk approves a version, and every approval taken afterwards has to be checked against the version in force on its date. In the monolith the table was loaded through a generic reference-load endpoint, approved through a rule-version endpoint that named a different right, and read in process by a router that kept its own copy. Nobody could say from the record which version a decision was checked against.

The target keeps the regulation in rows and changes the custody and the journey. `rwb-access` holds `delegation_limit` in its own schema (Architecture v5 slides 14 and 41), RWB-P4-E1038-APP builds the table, its window and its rollback, and this story delivers what the legacy key actually asks for: one file loaded whole, one approval by the risk function, one dated lookup that answers with the version it used, one refusal that changes nothing, and one incident when no limit covers a request. The legacy criteria are met word for word: limits by decision, level, product and amount (AC1), and a decision with no limit at any level that goes to the next level up with an incident naming the missing limit (AC2).

This story meets REQ-ACA-004 (the delegation of authority table held as reference data, setting every approval limit), REQ-APD-010 (a delegation change is versioned, approved and dated, and open items keep the version they were decided under), REQ-APD-001 (a decision that needs approval is routed to the approver the table names for that decision, product and amount), REQ-DRI-010 (thresholds, limits and names are configuration rows with a version, changed without a code release) and REQ-ACA-013 (the administration screens for roles, permissions and delegation exist). It applies R-UNI-38 (a new version applies from its effective date, and open work keeps the version it was decided under) and R-UNI-39 (an action that cannot be recorded does not proceed), and it follows the same approve-and-date discipline the Drools rule packages follow: a version is approved by a second person and takes effect on a date, not on the day it was approved.

The lookup is the half that makes the table worth having. Every approval in the other eighteen services — a settlement, a write-off, a debt sale, a litigation step — is routed by asking this one question with a date on it, and the answer carries the version, so an auditor can always see why a case went to a given approver. A request no limit covers is not silently approved at the lowest level: it answers `NOT_COVERED`, names the decision and the product, and an incident goes to Risk.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E1038-APP (same service, its own story, wave 1) | The `delegation_limit` table and its migration in `rwb_access`, the version window, the difference report, the rollback and the four paths of the table store. This story builds the DoA load-and-approve journey and the lookup on that table and duplicates no column |
| RWB-P4-AD016-CON (same service, its own contract story) | The published OpenAPI 3.1 document of the four operations, the `DoaLoad`, `DoaLoadAnswer` and `DoaLimitAnswer` schemas, the `NOT_COVERED` and `RELATED_PARTY` answers, the error envelope and the fakes this story builds against |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): one entry per approval and per refusal |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the approver-role parameter read with the version in force |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the reference-data contract of `rwb-case` (DP-07): LOV-DECISION, LOV-APPROVAL-LEVEL and LOV-PRODUCT with the version in force |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) that serves SCR-41 Delegation of authority to the browser |
| RWB-P4-E1037-CON (same service, its own contract story) | The per-service login (DP-02) and the authorise answer behind a right, with the RFC 9457 refusal shape and MSG-P4-002 |

Business preconditions carried from RWB-AD-016, the P4 specifications and the Drools design:

- The version in force in SIT is "DOA-2026.11", built from the regulation, with 95 limits and 218 stored rows (FSD P4 v3 A2.6 AC-P4-006-01).
- LOV-DECISION, LOV-APPROVAL-LEVEL (L1 to L6) and LOV-PRODUCT (MORTGAGE, HIRE_PURCHASE, SSME, UNSECURED) are reference-data rows of `rwb-case` read through DP-07, never rows of `rwb_access` and never a Java enum (TSD P4 v3 T3.2; ASM-0071).
- The holder and substitute of each level are not yet named (DL18), so the rows load with `holder_user_id` and `substitute_user_id` empty in production and with named test users in SIT and UAT.
- The approver of a version is Risk and model risk officer (RW-RISK) through the A letter in Rules and parameters, and the loader is the reference data administrator through the C letter in Reference data: two people by construction (legacy permission table; FSD P4 v3 A2.6 AC-EXC-P4-006-02; TSD P4 v3 T6.1).
- The file format of the delegation workbook (sheet names, column order) and the enumerated regulation item list are Not specified in the source documents (GAP-0834, GAP-0835; ASM-1535, ASM-1536); the values used in the criteria are the FSD's own.

### 4. Flow

1. The reference data administrator opens SCR-41 Delegation of authority through the gateway-bff composite route of DP-19. The route calls `GET /api/recovery/access/v1/admin/doa-loads/{loadId}` for a load and this service's version read for the list; the browser calls no service directly.
2. The administrator converts the regulation matrix to the load file and calls `POST /api/recovery/access/v1/admin/doa-loads` with the multipart file, query `table` = `delegation_limit`, query `validFrom` (for example "2026-11-30"), the version label in the file, and an `Idempotency-Key`.
3. `DoaLoadController` validates the call: `table` must be `delegation_limit`, which is the only table this path accepts; `validFrom` and the version label are required, and an empty one is 422 with MSG-GEN-001 naming the field; a version label already loaded is 409 with MSG-GEN-004; a missing `Idempotency-Key` is 422. A repeated key answers the stored answer of the first call and writes no second row and no second entry.
4. `DoaFileValidator` validates the file whole and never row by row. Every row must carry a decision code in LOV-DECISION, an approval level in LOV-APPROVAL-LEVEL, a product in LOV-PRODUCT, its regulation item and its limit version, all read with the version in force through DP-07. No two rows may repeat decision, regulation item, product, level and limits. A level's principal limit that rises above the principal limit of the level beneath it for the same decision and item is a falling limit. An unknown decision code is refused as an unknown code (GAP-0835; ASM-1536).
5. Any single failure refuses the load in full: 422 with MSG-P1-002 naming the check and the row, no row stored, no decision-record entry, and the version in force unchanged. The version in force keeps its `valid_to` as it was, so no approval already routed can lose its limit because a bad file arrived.
6. On pass, the loader stores all rows of the version in one transaction with the same `limit_version`, `valid_from` and state `LOADED`, and answers 201 with the load id, the row count (218 for "DOA-2026.11"), the version label, `validFrom` and the state. The insert and the window arithmetic are the table's, which RWB-P4-E1038-APP builds; this story owns the journey and its checks (GAP-0833; ASM-1534).
7. `GET /api/recovery/access/v1/admin/doa-loads/{loadId}` answers the load with its row count, its version label, `validFrom` and its state, so the administrator and Risk read the same object before the approval.
8. Risk and model risk officer (RW-RISK) reviews the difference report and calls `POST /api/recovery/access/v1/admin/doa-loads/{loadId}/approve` with an `Idempotency-Key`. `PermissionReader` resolves the caller's A letter in Rules and parameters from the `role` and `permission` rows of `rwb_access`; a caller with no role row is 403 with MSG-P4-001, a caller without the A letter is 403 with MSG-P4-002 and nothing is approved.
9. `FourEyesRule` compares the load's author reference with the approver reference of the caller. The loader is refused with MSG-P7-002 and the load stays `LOADED`. The approver role is also read from the parameter of DP-06 with the version in force, so a change of approver is a data change and never a release (GAP-0836; ASM-1537).
10. On pass, one transaction moves the version to `APPROVED`, sets `valid_to` of the rows of the version before to the day before this `valid_from`, appends one decision-record entry of the DP-03 library with decision code `AC-VERS`, the version label, the `valid_from`, the approver reference and the row count, and writes the outbox row. Where the record cannot be written the transaction rolls back, the call answers 503 with MSG-P7-003 and the load stays `LOADED`: an approval that cannot be recorded does not take effect (legacy TC-AD-016-04).
11. After the commit, the outbox relay publishes `rwb.access.DoaLimitChanged.v1` on `rwb.access.events.v1`, keyed on the limit version, carrying the version, the table, the change kind, `validFrom`, `validTo` and the row count, and no personal data (GAP-0841; ASM-1542). A failed transaction publishes nothing.
12. The approval router, and every service that routes an approval, calls `GET /api/recovery/access/v1/doa-limits` with the decision code, the regulation item, the product, the principal, the loss percentage and the loss amount, and the date it is deciding on. `DoaLimitLookup` reads the rows of `rwb_access` whose window contains that date and answers the lowest level, from L6 up to L1, whose limit covers the request, with the `delegation_limit` id and the limit version. No row at any level answers `NOT_COVERED` with the message MSG-P7-010 naming the decision and the product and an incident reference to the RW-RISK queue; a write-off for a related party answers L1 with reason `RELATED_PARTY` whatever the amount.
13. The older version stays readable at its own dates: after "DOA-2027.01" comes into force on "2027-01-01", the rows of "DOA-2026.11" keep `valid_to` "2026-12-31" and a lookup dated 31 December 2026 still answers from "DOA-2026.11". No decision taken under the older version is re-decided.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A row repeats decision, regulation item, product, level and limits, or a level's principal limit rises above the level beneath it | The load is refused in full, the row is named, nothing is stored and the version in force stays | MSG-P1-002 | AC4 |
| X2 | A row carries a decision code, an approval level or a product outside its list in force, or a required field is empty | The load is refused in full with the row and the check named | MSG-P1-002, MSG-GEN-001 | AC4 |
| X3 | The version label is already loaded | 409, nothing stored, the stored version untouched | MSG-GEN-004 | AC3 |
| X4 | The person who loaded the version approves it | 403, the load stays `LOADED`, one `AC-DENY` entry with both references | MSG-P7-002 | AC5 |
| X5 | A caller without the A letter in Rules and parameters approves, for example RW-PRODHEAD | 403 before the handler runs, nothing approved, one `AC-DENY` entry | MSG-P4-002 | AC5 |
| X6 | A caller holds no role row at all in `rwb_access` | 403 with no entry, because there is no area to record against | MSG-P4-001 | AC5 |
| X7 | The decision-record entry cannot be written during an approval | The transaction rolls back, the load stays `LOADED`, the version in force stays in force, and no event is published | MSG-P7-003 | AC6 |
| X8 | The approver calls twice with one `Idempotency-Key`, or the gateway repeats the call | The second call answers the stored answer of the first and writes no second entry | None | AC3 |
| X9 | The reference-data or the parameter read is unavailable while a load arrives | 503, nothing stored, the load is retried under the same key | MSG-GEN-006 | AC3 |
| X10 | A lookup finds no row for the decision and the product at any level, for example HIRE_PURCHASE before the chapter 8 limits arrive | The answer is `NOT_COVERED` with MSG-P7-010 naming the decision and the product and an incident reference to the RW-RISK queue; nothing is approved at a default level | MSG-P7-010 | AC9 |
| X11 | A write-off is for a director, a senior executive, a major shareholder or a related party | The answer is L1 with reason `RELATED_PARTY` whatever the amount | None | AC10 |
| X12 | The lookup date falls on the last day of a version or the first day of its successor | The version whose window contains that date answers; `valid_to` of the older version is the day before the newer `valid_from` | None | AC8 |
| X13 | A request's principal is above every level's principal limit | The answer is the level the regulation gives for that amount, or `NOT_COVERED` where the regulation gives none for the product | None | AC9 |

No exception path of this story writes a case, a task or an approval record: this service holds the DoA table and the answer about it, and the state machine of an approval is `rwb-decision`'s.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P4-AD016-CON, the platform contracts and RWB-P4-E1038-APP's table; the router that calls the lookup is another service and shares only the published answer |
| Negotiable | Limits, levels, products, regulation items, holders, substitutes and version labels are rows; the lists are reference data with a version; the approver is a right and a parameter row; no value is fixed in this story |
| Valuable | One approved, dated version of the regulation and one dated answer replace a table every module copied and a limit that lived in a document |
| Estimable | Four operations, one whole-file validator, one approval gate, one lookup, one record appender, one event, one screen route and one contract-fake run |
| Small | Fits two weeks with its tests; it creates no table, no workflow and no case state |
| Testable | Each of the eleven criteria has a test case in section 16, and the refused file, the loader, the missing limit and the related-party answer are stubbed in the fakes |

### 7. Acceptance criteria

```gherkin
Feature: Load the delegation of authority table

  Background:
    Given the environment is SIT
    Given test user "U-3101" holds RW-REFADM with the C letter in Reference data
    Given test user "U-3102" holds RW-RISK with the A letter in Rules and parameters
    Given test user "U-3103" holds RW-PRODHEAD with no A letter in Rules and parameters

  Scenario: AC1 Limits loaded (legacy RWB-AD-016 AC1)
    Given the approval-router contract mock returns level L6, the row of item 2.1.1 at L6 and version "DOA-2026.11" from 30 November 2026
    Given limits by decision, level, product and amount
    When Risk approves the version
    Then approvals check against it from its date

  Scenario: AC2 Missing limit (legacy RWB-AD-016 AC2)
    Given the approval-router contract mock returns "NOT_COVERED" for decision D6.4, item 2.1.1, product HIRE_PURCHASE, principal 900,000.00
    Given a decision with no limit at any level
    When it is submitted
    Then it goes to the next level up and an incident names the missing limit

  Scenario: AC3 The load stores the version whole and answers the load (new, D-RCV-60)
    Given the delegation of authority file "DOA-2026.11", with 95 limits
    When "U-3101" loads it with table "delegation_limit" and validFrom "2026-11-30" and "U-3102" approves it
    Then 218 rows are stored: 109 decision and limit rows for MORTGAGE and 109 for SSME
    Then every row has a decision code, an approval level and a product, and no two rows repeat the same decision, regulation item, product, level and limits
    Then item 2.1.1 at level L4 is stored as two rows: principal 300,000,000.00 with loss up to 45.00 percent and maximum loss 150,000,000.00, and principal 50,000,000.00 with no loss limit
    Then GET /api/recovery/access/v1/admin/doa-loads/{loadId} returns the load with row count 218, version "DOA-2026.11", validFrom "2026-11-30" and state "LOADED" before the approval and "APPROVED" after it
    Then one decision-record entry records the approval with version "DOA-2026.11" and its valid-from date

  Scenario: AC4 A file with an error is refused whole (new, D-RCV-60)
    Given file "DOA-2026.12" gives item 2.1.1 at L5 a principal limit of 400,000,000.00, above the 300,000,000.00 of L4
    Given it gives one row the decision code "D6.9"
    When "U-3101" loads it
    Then the load is refused with message MSG-P1-002 naming the falling limit and the unknown decision code
    Then no row of "DOA-2026.12" is stored and "DOA-2026.11" stays in force

  Scenario: AC5 The loader cannot approve and only Risk may (new, D-RCV-60)
    Given load "DOA-2027.01" was loaded by "U-3101"
    When "U-3101" calls approve on it
    Then the call is refused with message MSG-P7-002 and the load stays "LOADED"
    Then when test user "U-3103" holding RW-PRODHEAD calls approve on it the call is refused with status 403 and message MSG-P4-002

  Scenario: AC6 An approval that cannot be recorded does not take effect (new, D-RCV-60)
    Given the decision log store is unavailable
    When "U-3102" approves load "DOA-2027.01"
    Then the call returns status 503 with message MSG-P7-003 and the load stays "LOADED"
    Then "DOA-2026.11" stays in force and no event is published on rwb.access.events.v1

  Scenario: AC7 The lookup answers the level, the row and the version for a dated request (new, D-RCV-60)
    Given "DOA-2026.11" is in force
    When the router asks GET /api/recovery/access/v1/doa-limits for decision D6.4, item 2.1.1, product MORTGAGE, principal 2,400,000.00, loss 20.00 percent and loss amount 480,000.00 on 15 December 2026
    Then the lookup returns level L6, the row ID of item 2.1.1 at L6 and version "DOA-2026.11"

  Scenario: AC8 A change closes the previous version on the day before and keeps it readable (new, D-RCV-60)
    Given "DOA-2026.11" is in force
    Given file "DOA-2027.01" adds a row for item 2.1.5 at level L5 with principal up to 10,000,000.00, validFrom "2027-01-01"
    When "U-3101" loads it and "U-3102" approves it
    Then the rows of "DOA-2026.11" stay readable with valid_to "2026-12-31"
    Then a lookup for D6.6, item 2.1.5, MORTGAGE, principal 8,000,000.00 dated 2 January 2027 returns L5 and version "DOA-2027.01"
    Then one decision-record entry records the approval of "DOA-2027.01" with its valid from date

  Scenario: AC9 No limit covers the request (new, D-RCV-60)
    Given "DOA-2026.11" holds no row for product HIRE_PURCHASE
    When the router asks who may approve decision D6.4, item 2.1.1, for HIRE_PURCHASE, principal 900,000.00
    Then the lookup returns "NOT_COVERED"
    Then an incident is raised to the RW-RISK queue with message MSG-P7-010 naming D6.4 and HIRE_PURCHASE
    Then nothing is approved at a default level

  Scenario: AC10 A write-off for a related party answers the Board level (new, D-RCV-60)
    Given "DOA-2026.11" is in force
    When the router asks who may approve decision D9.2, item 2.1.10, criteria met, product SSME, principal 300,000.00, with related party flag true
    Then the lookup returns level L1 with reason "RELATED_PARTY"

  Scenario: AC11 The change is published once the approval commits (new, D-RCV-60)
    Given "DOA-2027.01" is approved and its transaction has committed
    Then one rwb.access.DoaLimitChanged.v1 is published on rwb.access.events.v1 keyed on the limit version
    Then its payload carries the version, the table "delegation_limit", the change kind, validFrom "2027-01-01", validTo and the row count, and no personal data
    Then a load that was refused or rolled back publishes nothing
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The load path accepts one table only, `delegation_limit`, and validates the file whole: every decision code, level and product from its list in force, every limit version and regulation item present, no repeated tuple of decision, regulation item, product, level and limits, and no falling principal limit from L6 up to L1 | Legacy RWB-AD-016; FSD P4 v3 A2.6 AC-P4-006-01 and AC-EXC-P4-006-01; TSD P4 v3 T3.1 |
| BR2 | Any failed check refuses the load in full with MSG-P1-002 naming the check and the row; no row of the refused version is stored and the version in force stays in force | Legacy RWB-AD-016; FSD P4 v3 A2.6 AC-EXC-P4-006-01 |
| BR3 | The load needs the C letter in Reference data; the approval needs the A letter in Rules and parameters, held in the matrix by RW-RISK; the letter is read from the `role` and `permission` rows and never from a role name in code | Legacy RWB-AD-016 Permission checks; TSD P4 v3 T6.1; REQ-ACA-003; FSD P4 v3 A2.6 AC-EXC-P4-006-02 |
| BR4 | The approver must not be the load's author; the same person may not load and approve, and the approver role is also read from the parameter of DP-06 with the version in force | Legacy RWB-AD-016 Permission checks; MSG-P7-002; DP-06; GAP-0836 |
| BR5 | An approved version takes effect from its `valid_from` date; on approval the rows of the version before get `valid_to` set to the day before, and those rows stay readable at their own dates | Legacy RWB-AD-016 AC1; FSD P4 v3 A2.6 AC-ALT-P4-006-02; R-UNI-38 |
| BR6 | One decision-record entry of the DP-03 library is appended per approval and per refusal, with decision code `AC-VERS` or `AC-DENY`, the version, the `valid_from`, the caller reference and no personal data | Principle 5; DP-03; TSD P4 v3 T6.3 |
| BR7 | No approval takes effect without its record: where the entry cannot be written the transaction rolls back, the call answers 503 with MSG-P7-003 and the load stays `LOADED` | R-UNI-39; FSD P4 v3 A2.6 AC-EXC-P4-006-03 |
| BR8 | The lookup answers the lowest level, from L6 up to L1, whose row for the decision, regulation item and product covers the request on its date, and returns the `delegation_limit` id and the limit version with it | FSD P4 v3 A2.6 AC-ALT-P4-006-01; TSD P4 v3 T3.1; LOV-APPROVAL-LEVEL |
| BR9 | A decision and product that no row covers answers `NOT_COVERED` with MSG-P7-010 naming the decision and the product and an incident reference to the RW-RISK queue; nothing is approved at a default level | Legacy RWB-AD-016 AC2; FSD P4 v3 A2.6 AC-EXC-P4-006-04 |
| BR10 | A write-off for a director, a senior executive, a major shareholder or a related party answers L1 with reason `RELATED_PARTY` whatever the amount | FSD P4 v3 A2.6 AC-EXC-P4-006-05; the item 2.1.10 L1 row of RWB-P4-E1038-APP |
| BR11 | A version change publishes `rwb.access.DoaLimitChanged.v1` on `rwb.access.events.v1` through the outbox after the commit, and a refused or rolled-back change publishes nothing | Architecture v5 slide 43; DP-09 outbox rule; GAP-0841 |
| BR12 | Every write operation carries `Idempotency-Key`; a repeated key answers the stored answer and writes no second row and no second entry | Architecture v5 slide 11 |
| BR13 | No value a business person may change is written in code: levels, limits, products, regulation items, versions, holders and substitutes are rows, the lists are reference data with a version, and the approver is a right and a parameter row | FSD P4 v3 A2.6 BR-P4-006; REQ-DRI-010 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 and BR2 are one validator over the whole file before any insert, so a refused file leaves the table exactly as the version in force left it; the validator reads the three lists through the reference-data client of DP-07 and holds no enum of its own.
- BR3 is two reads of the service's own `role` and `permission` rows; the capability area and the letters are data, so a change of approver is a `permission` row and not a build.
- BR4 is one comparison of two references plus the parameter read of DP-06; both are decided before the transaction opens.
- BR5 is the window arithmetic on `valid_from` and `valid_to`: the previous version is closed on the day before and never edited afterwards.
- BR6 and BR7 are the record appender of DP-03 inside the same transaction as the state change, which is why the failure of X7 leaves the load `LOADED` rather than `APPROVED`.
- BR8 to BR10 are the lookup: one indexed read on `decision_code`, `regulation_item`, `product_group`, `approval_level` and `valid_from`, ordered from L6 up, with the related-party condition applied before the amount test.
- BR11 is the outbox row written in the transaction and published by the relay after the commit, so a consumer never sees a version that did not commit.
- BR13 is checked by test: a new decision code, level, product or regulation item is a row and a list value, and the build changes nothing.

### 9. State transitions

This service holds the lifecycle of a delegation version and the window of its rows; it holds no case, task or approval state.

| From | Event | Condition | To |
|---|---|---|---|
| (none) | Load of a file that passes the whole-file validation | Every code is a list value, no repeated tuple, no falling limit | `LOADED`, rows stored, the version in force still in force |
| (none) | Load of a file that fails validation, or a version label that exists | Any check fails, or the label is already loaded | Nothing stored, the version in force stays |
| `LOADED` | Approval by the A letter in Rules and parameters, not the loader, record written | The transaction commits | `APPROVED`; the previous version's rows get `valid_to` on the day before |
| `LOADED` | Approval by the loader | The author and the approver are the same reference | Stays `LOADED`, one `AC-DENY` entry |
| `LOADED` | Approval by a role without the A letter | No A in Rules and parameters | Stays `LOADED`, 403, one `AC-DENY` entry |
| `LOADED` | Approval whose record cannot be written | The record write fails | Stays `LOADED`, 503, no state change |
| `APPROVED` | Its `valid_from` arrives | A lookup is dated on or after `valid_from` | In force for its dates; the older version readable for its own |
| In force | A successor is approved | The successor's `valid_from` is later | Rows keep `valid_to` on the day before the successor; superseded but readable |

| Command | Condition | Outcome |
|---|---|---|
| Load | C letter in Reference data, file passes whole | 201, version `LOADED`, row count and difference report answered |
| Load | Any check fails | 422 MSG-P1-002, nothing stored |
| Approve | A letter in Rules and parameters, not the loader, record commits | 200, version `APPROVED`, one `AC-VERS` entry, one event after the commit |
| Approve | Loader, or no A letter, or record fails | Refused, version `LOADED`, one `AC-DENY` entry where a record can be written |
| Lookup | Rows cover the request on the date | 200 with the level, the row id and the limit version |
| Lookup | No row at any level | `NOT_COVERED` with MSG-P7-010 and the incident reference |
| Lookup | A related-party write-off | L1 with reason `RELATED_PARTY` |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-REFADM Reference data administrator | Loads a delegation version (C letter in Reference data). Approves none |
| RW-COE Center of excellence analyst | Holds C in Reference data in TSD P4 v3 T6.1, so it may prepare and load a version; it holds no A in Rules and parameters and approves none |
| RW-RISK Risk and model risk officer | Approves a version: the only role with the A letter in Rules and parameters (TSD P4 v3 T6.1), and the role the parameter of DP-06 names |
| RW-PRODHEAD Product head | Agrees the limits for a product with Risk before the load; holds no A in Rules and parameters, so an approval answers 403 with MSG-P4-002 |
| RW-AUDIT Internal audit | Reads the versions and the approvals through the decision-record chain and the version read; it writes nothing |
| The approval router and the other service identities | Call `GET /api/recovery/access/v1/doa-limits` under the R letter in Reference data; they hold no write path to the table |
| `rwb-access` itself | Writes `delegation_limit`, the decision-record entry and the outbox row; reads `role`, `permission` and its own ACE view for the caller's staff reference |
| The gateway-bff route | Calls this service once per screen read for SCR-41; it holds no right of its own |

The refusal shape is 403 with an RFC 9457 problem response and `messageId` set: MSG-P4-002 for an absent letter, MSG-P4-001 for an absent role, MSG-P7-002 for the loader approving its own load. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-E1037-CON.

Levels L1 to L6 are Board of Directors, Executive Committee, Problem Asset Resolution Committee or Management Committee, Head of Recovery at function level, Recovery executive at division level and Recovery executive at department level; the mapping is the regulation's and its holders are not yet named (DL18).

### 11. Data

| BR Field ID | Table | Field | Read or write |
|---|---|---|---|
| DF-REF-016 to DF-REF-026 | `delegation_limit` in `rwb_access` | id, decision_code, approval_level, product_group, principal_limit, loss_pct_limit, min_price_pct_fmv, holder_user_id, substitute_user_id, valid_from, valid_to | Write through the load, read by the lookup |
| DF-REF-055 to DF-REF-062 | `delegation_limit` in `rwb_access` | limit_version, regulation_item, applies_when, max_loss_amount, max_delay_count, min_price_pct_principal, min_received_pct, max_term_years | Write through the load, read by the lookup |
| DF-REF-034 to DF-REF-039 | `role` in `rwb_access` | id, role_code, role_name, role_class, default_scope, entra_group | Read |
| DF-REF-040 to DF-REF-044 | `permission` in `rwb_access` | id, role_id, capability_area, letters, matrix_version | Read |
| DF-REF-027 to DF-REF-033 | `lov_value` of `rwb-case` | LOV-DECISION, LOV-APPROVAL-LEVEL and LOV-PRODUCT with the version in force | Read through DP-07, never written |
| (parameter) | `parameter_value` of `rwb-case` | the approver-role parameter of the table, read with the version in force | Read through DP-06 |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the `AC-VERS` and `AC-DENY` entry of an approval or a refusal | Write |
| (outbox) | outbox library table in `rwb_access` | the record row and the `DoaLimitChanged` row of a committed change | Write |
| (idempotency) | `idempotency_key` in `rwb_access` | the stored answer of each load and approve call | Write |
| (inbox) | `processed_event` | none: this story consumes no event | None |

No row of `decision_log_entry` or of `approval` (P7) and no case, task or queue row (P3) is read or written. `lov_value`, `reference_row`, `reference_version`, `parameter_catalog` and `parameter_value` are P3's under the Ownership Map and are read through DP-07 and DP-06, never from `rwb_access`. The caller's staff reference and group resolve through `v_ace_iam_group`, a read of the service's own ACE view (DP-05), and the holders and substitutes are stored as user references only: no name, no e-mail address and no personal field appears in a row, a log line or an event.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/access/v1` (DP-13). Owner P4 `rwb-access`.

| Method | Path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|
| POST | `/admin/doa-loads` | Multipart: file; query `table` = `delegation_limit`, `validFrom`, version label | `DoaLoad`: `loadId`, `table`, `limitVersion`, `validFrom`, `state`, `rowCount`, difference report | 401 MSG-P4-001; 403 MSG-P4-002; 409 MSG-GEN-004; 422 MSG-P1-002 or MSG-GEN-001; 503 MSG-GEN-006 | Reference data, right C, scope applied | `Idempotency-Key` required; a repeat answers the stored answer |
| POST | `/admin/doa-loads/{loadId}/approve` | None | `DoaVersion`: `limitVersion`, `validFrom`, `validTo`, `state`, `rowCount`, `approverReference` | 401 MSG-P4-001; 403 MSG-P4-002 or MSG-P7-002; 404 MSG-P4-003; 409 MSG-GEN-004; 503 MSG-P7-003 | Rules and parameters, right A, scope applied | `Idempotency-Key` required |
| GET | `/admin/doa-loads/{loadId}` | None | `DoaLoadAnswer`: `loadId`, `limitVersion`, `validFrom`, `state`, `rowCount`, `authorReference`, `approverReference` | 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 503 | Reference data, right R, scope applied | Not applicable, read only |
| GET | `/doa-limits` | Query: `decisionCode`, `regulationItem`, `productGroup`, `principal`, `lossPct`, `lossAmount`, `asOf` | `DoaLimitAnswer`: `status` (`COVERED` or `NOT_COVERED`), `approvalLevel`, `delegationLimitId`, `limitVersion`, `reason`, `incidentReference`, `asOf` | 401 MSG-P4-001; 403 MSG-P4-002; 422 MSG-GEN-001; 503 | Reference data, right R, scope applied | Not applicable, read only |

The legacy story named the approval path `/admin/rule-versions/{versionId}/approve` with the right "Rules and parameters A" and the load path `/admin/reference-loads` with "Reference data C", both under the single monolith base that DP-13 replaces; TSD P4 v3 appendix T-A carries the generic reference-load paths as API-P4-005 and API-P4-006, and the ownership map rules them P3 `rwb-case`'s because the reference store is P3's (ASM-0041). No approved source therefore gives a DoA-specific path: the paths of this table are the ones RWB-P4-E1038-APP introduces, and this story serves the load-and-approve journey and the lookup on them (GAP-0833; ASM-1534). The lookup path is the ownership map's `GET /doa-limits` for P4 (GAP-0842; ASM-1543).

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (own) | The C letter in Reference data and the A letter in Rules and parameters for the caller, with the MSG-P4-002 refusal shape |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 `rwb-case` | LOV-DECISION, LOV-APPROVAL-LEVEL and LOV-PRODUCT with the version in force, read through the reference-data client of DP-07 |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case` | The approver-role parameter of the table, read with the version in force through DP-06 |

None of the three is declared as provided by this story, and none is called twice in one load or one approval.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.access.DoaLimitChanged.v1` | `rwb.access.events.v1` | P4 | limitVersion | limitVersion, table `delegation_limit`, the change kind (approved), validFrom, validTo, rowCount, and no personal data |

The event is written to the outbox in the same transaction as the approval and published by the relay after the commit, so it is never seen for a version that did not commit. Its shape is proposed here and confirmed at contract review (GAP-0841; ASM-1542). The service also appends a decision-record entry of the DP-03 library, whose `DecisionRecorded` message travels on the shared topic `rwb.decision-record.v1`; it is the library's message and not this service's own event, and section 12.9 counts it.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 (events: none), and this story adds no subscription.

#### 12.5 Workflows and activities

None. The load and the approval are two calls with a human decision between them, not a workflow: the legacy story has no timer, no escalation and no saga, and the lookup is one synchronous read.

#### 12.6 Schedules

None for this story. The six-monthly access review list (JOB-18) is a Temporal Schedule of `rwb-access` and belongs to the service's own story.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `delegation_limit` | P4 (`rwb_access`) | Written through the load path and read by the lookup; created and migrated by RWB-P4-E1038-APP, which is the only writer of a version window |
| `role`, `permission` | P4 (`rwb_access`) | Read only: the caller's C letter in Reference data and A letter in Rules and parameters. Created by RWB-P4-E1037-CON |
| `outbox_event`, `idempotency_key`, `processed_event` | PLT library, created in `rwb_access` | The record row and the `DoaLimitChanged` row, and the stored answer under `Idempotency-Key`; no inbox row is written because no event is consumed (DP-09) |
| decision record (local library objects) | PLT library, created in `rwb_access` | The `AC-VERS` and `AC-DENY` entries and their hash chain (DP-03) |
| `lov_value`, `reference_row`, `reference_version` | P3 (`rwb_case`) | Not owned and not read from the schema: read through the reference-data contract of DP-07 |
| `parameter_catalog`, `parameter_value` | P3 (`rwb_case`) | Not owned and not read from the schema: the approver role arrives through DP-06 |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written: the central ledger is `rwb-decision`'s |

No foreign key crosses a schema and no SQL statement of this story names a table of another service (DP-01). `delegation_limit` keeps no reference to a case, a role or a list row: its codes are values of lists, exactly as the regulation is written.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| parameters fake | RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The approver-role parameter read with the version in force, and the forced unavailability of X9 |
| reference-data fake | RWB-PLT-E1043-CON, RWB-P3-E1043-CON | LOV-DECISION with "D6.9" absent and D6.4, D6.6 and D9.2 present; LOV-APPROVAL-LEVEL L1 to L6; LOV-PRODUCT with MORTGAGE, HIRE_PURCHASE, SSME and UNSECURED, each with its version |
| decision-record fake | RWB-PLT-E1027-CON | The `AC-VERS` and `AC-DENY` append, the hash-chain check and the forced failure of AC6 |
| authorise fake | RWB-P4-E1037-CON | The C letter for "U-3101", the A letter for "U-3102", the MSG-P4-002 refusal for "U-3103" and the MSG-P4-001 answer for a caller with no role |
| table fixture fake | RWB-P4-E1038-APP | The rows of "DOA-2026.11" seeded for the lookup: item 2.1.1 at L4 as two rows, item 2.1.10 at L1 with `RELATED_PARTY`, and no HIRE_PURCHASE row |
| approval-router fake | RWB-P4-AD016-CON | The request the router sends to `GET /doa-limits`: D6.4 item 2.1.1 MORTGAGE at 2,400,000.00 and 20.00 percent on 15 December 2026; D6.6 item 2.1.5 on 2 January 2027; D6.4 for HIRE_PURCHASE at 900,000.00; D9.2 item 2.1.10 SSME related party |
| gateway-bff route fake | RWB-PLT-N001-CON | The SCR-41 composite route: the version list, one load and the four states waiting, loaded, approved and refused |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 4 (3 write, 1 read on the base, plus the read-only lookup); consumed 3 | Four operations on `/api/recovery/access/v1`; the authorise call, the list read and the parameter read; one hop, 2 s timeout |
| Kafka | Published 1 event type; consumed 0 | `rwb.access.DoaLimitChanged.v1` on `rwb.access.events.v1`, plus the library's `DecisionRecorded` message on `rwb.decision-record.v1` |
| Temporal | 0 workflows, 0 activities | The `rwb-access` queue serves JOB-18 and other stories |
| File | 1 inbound | The delegation of authority file, multipart on `POST /admin/doa-loads`; no file output |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/doa`, Java package `th.co.scb.ace.workbench.recovery.access.doa`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the generic reference-load endpoint of the monolith (DP-13: this service's own base under `/api/recovery/access/v1`), the in-process `DelegationOfAuthority` call inside the monolith (the lookup is one REST answer, one hop and 2 s, cached on the caller's side), the reading of the monolith permission table (DP-05: the service's own `role` and `permission` rows and `v_ace_iam_group` for the caller's reference), the LOV enums compiled into the loader (DP-07: three lists read with the version in force), the approve-and-date discipline kept by a second write (DP-03: the decision-record entry in the same transaction), and the ace-web screen (DP-19: the SCR-41 composite route). DP-06 carries the approver-role parameter, so a change of approver is a data change.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DoaLoadController | Controller | The four operations, the `Idempotency-Key` check, the RFC 9457 error mapping and `messageId` on every refusal |
| DoaFileValidator | Service | BR1 and BR2: the whole-file check against the three lists, the repeated tuple, the falling limit and the unknown decision code, with the row named |
| DoaApprovalService | Service | The approval: the authority, the state check, the window arithmetic, the record and the answer |
| PermissionReader | Service | The caller's C letter in Reference data and A letter in Rules and parameters, from `role` and `permission` |
| ApproverRoleReader | Service | The approver role from the parameter of DP-06, read with the version in force |
| FourEyesRule | Service | BR4: the load's author reference against the approver reference |
| DoaLimitLookup | Service | BR8 to BR10: the dated read from L6 up, the related-party condition and the `NOT_COVERED` answer with its incident reference |
| DecisionRecordWriter | Service | The `AC-VERS` and `AC-DENY` entry in the transaction that produces the answer, with the outbox row |
| DoaLimitChangedPublisher | Service | The `rwb.access.DoaLimitChanged.v1` outbox row after a committed approval |
| IdempotencyStore | Service | The stored answer per key, so a repeat answers the first call and writes no second entry |

**Database and migrations**

- This story creates no table. `delegation_limit` and its index belong to RWB-P4-E1038-APP's migration in the per-service Flyway sequence of DP-15; `role` and `permission` belong to RWB-P4-E1037-CON; the outbox, idempotency and decision-record rows are library objects created in the `rwb_access` baseline.
- The only writes are the rows of a loaded version, the version window on approval, the decision-record row and its outbox row, and the `idempotency_key` row, each in one local transaction per call.
- Where SIT needs an index for the dated lookup beyond the table's own lookup index, the index is added to RWB-P4-E1038-APP's migration and not to a new one here.

**Configuration and reference data**

- "DOA-2026.11" is the version in force in SIT: 95 limits, 218 rows, 109 for MORTGAGE and 109 for SSME, item 2.1.1 at L4 as the two-row pair and item 2.1.10 at L1 on the related-party flag. "DOA-2027.01" is the change fixture of AC8.
- The approver role is the parameter row read through DP-06; RW-RISK holds the A letter in Rules and parameters in the matrix, so the right and the parameter agree in SIT (GAP-0836; ASM-1537). No role name is a Java constant.
- LOV-DECISION, LOV-APPROVAL-LEVEL and LOV-PRODUCT are read through DP-07 with the version in force; a new decision code is a row and a list value.
- The holders and substitutes load empty in production and as named test users in SIT and UAT (DL18).

**Build steps**

1. `DoaLoadController` with the four paths, the query `table` = `delegation_limit`, the `Idempotency-Key` requirement and the error envelope; contract test against RWB-P4-AD016-CON.
2. `DoaFileValidator`: the three list reads through DP-07, the repeated tuple, the falling limit from L6 up and the unknown decision code, with the row named in MSG-P1-002; tests for AC3 and AC4 and for a file that fails two checks at once.
3. The all-or-nothing insert and the answer of the load with its row count, and the load read of `GET /admin/doa-loads/{loadId}`; tests for the 218 rows, the item 2.1.1 pair and the 409 of an existing version label.
4. `PermissionReader` and `ApproverRoleReader`: the C letter for the load, the A letter for the approval and the 403 for RW-PRODHEAD; tests for AC5 and X6.
5. `FourEyesRule`: the loader refused with MSG-P7-002 before the transaction; tests for AC5.
6. The approval transaction with the window arithmetic, the `AC-VERS` entry, the outbox row and the forced failure of AC6; tests for AC3, AC6 and AC8.
7. `DoaLimitLookup`: the dated read from L6 up, the related-party condition, `NOT_COVERED` with MSG-P7-010 and the incident reference; tests for AC7, AC9, AC10 and X12.
8. `DoaLimitChangedPublisher`: one event per committed approval, none on a refusal or a rollback; test for AC11.
9. The idempotency store: one entry per load and per approval on a repeated key; test for X8.
10. The SCR-41 composite route against the gateway-bff fake, with the four states, and the contract-fake run of the four operations in isolation.

**Feature switch.** `rwb.access.delegation-table`, owned by RWB-P4-E1038-APP. Off, the table holds no version in force, this story's operations are not served, and the lookup answers `NOT_COVERED`; on is the state SIT and UAT run in. The lookup is not behind a second flag: an answer that could be switched off would leave every approval route with no limit to check.

**Done when.** The tests in section 16 pass; "DOA-2026.11" is in force in SIT with 218 rows reconciling to the 95 limits; the item 2.1.1 L4 pair and the item 2.1.10 L1 row are answered at their dates; a file with a falling limit or an unknown decision code is refused whole with nothing stored; the loader is refused with MSG-P7-002 and RW-PRODHEAD with MSG-P4-002; an approval whose record cannot be written answers 503 with MSG-P7-003 and the load stays `LOADED`; the lookup answers L6, `NOT_COVERED` and `RELATED_PARTY` as AC7, AC9 and AC10 state; and `rwb.access.DoaLimitChanged.v1` is published once per committed approval.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The caller holds no Recovery Workbench role row | You have no Recovery Workbench role. Ask your team manager to request one. | This story, on the load and the approval |
| MSG-P4-002 | The caller holds no C letter for a load, or no A letter in Rules and parameters for an approval | You cannot {action} here. Your role does not include it. | This story, on the load, the approval and the lookup |
| MSG-P4-003 | The load reference is unknown to the caller or outside its scope | This case is not in your scope. | This story, on the load read and the approval |
| MSG-GEN-001 | A required field is empty or carries a value outside its list | Enter {field}. | This story, on the load, the approval and the lookup |
| MSG-GEN-004 | The version label exists, the load is not `LOADED`, or the window has closed | Someone else changed this record. Reload it to see their change. | This story, on the load and the approval |
| MSG-GEN-006 | The reference-data read, the parameter read or the store is unavailable | The service is busy. Try again in a few minutes. | This story, on the load |
| MSG-P1-002 | The delegation file fails a check | The {source} load for {date} was refused: {check}. The previous load is still in use. | This story, on the load |
| MSG-P7-002 | The loader approves its own load | You prepared this decision, so you cannot approve it. | This story, on the approval |
| MSG-P7-003 | The decision-record entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the approval and the load |
| MSG-P7-010 | No limit covers the decision and the product | No approval limit covers {decision} for {product}. The item is held and Risk has been told. | This story, in the `NOT_COVERED` answer; the incident itself is the routing side's (GAP-0838; ASM-1539) |

Every error is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. MSG-P1-002 and MSG-P7-010 are messages of the source-data and decision catalogues and are kept word for word rather than renumbered, because the legacy criterion and the FSD use those ids (GAP-0837; ASM-1538).

### 15. Screens and states

One screen, SCR-41 Delegation of authority, served through the gateway-bff composite route of DP-19. The route calls the version read and this service's load read; the browser calls no service directly and holds no right of its own.

| Screen | State | Where it is |
|---|---|---|
| SCR-41 Delegation of authority | Waiting: a load in `LOADED` with its row count, version label and valid-from date | `rwb-access` through gateway-bff; this story answers the load read |
| SCR-41 Delegation of authority | Approved: the version `APPROVED` from its valid-from date, with the approver reference and the time | Same route; the answer of the approve call |
| SCR-41 Delegation of authority | Refused: MSG-P1-002 for a refused file, MSG-P7-002 for the loader, MSG-P4-002 for a role without the letter, each with nothing changed | Same route; the refusal of the load or the approval |
| SCR-41 Delegation of authority | Not covered: `NOT_COVERED` with the decision, the product and the incident reference, shown to the administrator and to Risk | Same route; the lookup answer |
| SCR-41 Delegation of authority | Empty: no version loaded for the table | Same route; the empty version list |

SCR-39 Rules and parameters is not served by this story: the rule-version load and its approval are RWB-AD-011's. The composite route specification, the screen field list and the masking of any field on SCR-41 are the platform story's (RWB-PLT-N001-CON); this story fixes the operations the route calls.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-016-01 | AC1, AC3, BR1, BR5, BR6 | Contract | "DOA-2026.11" with 95 limits loaded by "U-3101" and approved by "U-3102"; 218 rows, 109 MORTGAGE and 109 SSME; the item 2.1.1 L4 pair; the answer of the load read before and after the approval |
| TC-AD-016-02 | AC2, AC9, BR8, BR9 | Contract | No row for HIRE_PURCHASE; the lookup for D6.4 item 2.1.1 at principal 900,000.00 answers `NOT_COVERED` with MSG-P7-010 naming D6.4 and HIRE_PURCHASE and an incident reference |
| TC-AD-016-03 | AC5, BR3, BR4 | Component | "U-3101" approving its own load is refused with MSG-P7-002; "U-3103" holding RW-PRODHEAD is refused 403 with MSG-P4-002; a caller with no role row is refused with MSG-P4-001 |
| TC-AD-016-04 | AC6, BR7 | NFR | The decision-record write forced to fail during an approval: 503 with MSG-P7-003, the load stays `LOADED`, the version in force stays and no event is published |
| TC-AD-016-05 | AC4, BR1, BR2 | Component | "DOA-2026.12" with item 2.1.1 at L5 at 400,000,000.00 above the 300,000,000.00 of L4 and one row with decision code "D6.9": refused with MSG-P1-002 naming both, nothing stored, "DOA-2026.11" in force |
| TC-AD-016-06 | AC7, AC8, BR5, BR8 | Component | D6.4 item 2.1.1 MORTGAGE at 2,400,000.00 and 20.00 percent on 15 December 2026 answers L6; after "DOA-2027.01" is in force on 1 January 2027, D6.6 item 2.1.5 at 8,000,000.00 dated 2 January 2027 answers L5 and "DOA-2027.01", and "DOA-2026.11" keeps valid_to "2026-12-31" |
| TC-AD-016-07 | AC10, BR10 | Component | D9.2 item 2.1.10 SSME at 300,000.00 with the related party flag true answers L1 with reason "RELATED_PARTY" |
| TC-AD-016-08 | AC11, BR11 | Component | One approved version publishes one `rwb.access.DoaLimitChanged.v1` keyed on the version with the payload of section 12.3; a refused load and a failed approval publish nothing |
| TC-AD-016-09 | AC3, BR12 | Component | The same load and the same approval sent twice under one `Idempotency-Key` answer the first answer and write one row set, one entry and one event |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to Contract, Access to Component and Principle 5 to NFR. The four legacy cases are kept because the legacy key carries them: TC-AD-016-01 and TC-AD-016-02 cover the two legacy criteria, TC-AD-016-03 the access refusal and TC-AD-016-04 the forced record failure. The integration copy of the whole set is not written here, so no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in code: levels, limits, products, regulation items, version labels, holders and substitutes are rows; the three lists are reference data with a version; the approver is a right and a parameter row (BR13). A test proves that a new decision code, level or product needs no build.
- No personal data anywhere: the load, the approval, the lookup answer and the event carry user references, decision codes, amounts and versions. Holders and substitutes are stored as user references, and no name, e-mail address or personal field appears in a log, an event payload, a test or a prompt (DP-05).
- No read of another service's tables (DP-01): `lov_value`, `reference_row`, `reference_version` and the parameter rows arrive through DP-07 and DP-06, and the decision record is the local library's chain of DP-03.
- One writer of the table: only RWB-P4-E1038-APP's loader inserts a version and moves a window. This story adds no second writer, so a load can never be stored under two owners.
- Whole file or nothing: no partial load exists, and a refused file leaves the version in force untouched, so no approval already routed can lose its limit (BR2).
- No answer without its record: the version state and the decision-record entry commit together, and an approval that cannot be recorded does not take effect (BR7).
- A version already approved is never edited: a change is a new version, and the older rows stay readable at their own dates (BR5).
- The lookup answers what it may and nothing more: one level, one row id, one version, or `NOT_COVERED` with the incident reference; it returns no other decision's rows, so an answer cannot be used to map the table.
- No limit is converted or rounded at load or at read time; amounts are stored in baht with two decimals.
- The screen is served through the gateway-bff route of DP-19 and calls no service directly; the browser holds no token with a Rules and parameters right of its own.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-004 | The delegation of authority table is held as reference data and sets every approval limit | Epic 1, 3.4; Program access | FEAT-ACA-06 | 17 Run the decision center | BR1, BR2, BR5, BR8, BR13 | TC-AD-016-01, TC-AD-016-05, TC-AD-016-06 |
| REQ-APD-010 | A change to the delegation of authority table is versioned, approved and dated, and open items keep the version they were decided under | Epic 2, 3.7 | FEAT-ADM-03 | 17 Run the decision center | BR5, BR6, BR7 | TC-AD-016-01, TC-AD-016-04, TC-AD-016-06 |
| REQ-APD-001 | A decision that needs approval is routed to the approver the table names for that decision, product and amount | Epic 2, 3.7 | FEAT-ACA-06 | 17 Run the decision center | BR8, BR9, BR10 | TC-AD-016-02, TC-AD-016-06, TC-AD-016-07 |
| REQ-DRI-010 | A parameter catalog and a configuration service hold every threshold, limit and name, versioned, changed without a code release | Epic 1; Program 5.4 reference data | FEAT-ACA-03, FEAT-ACA-06 | 12 Administer reference data | BR3, BR12, BR13 | TC-AD-016-01, TC-AD-016-09 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator | Epic 8 administration | FEAT-ADM-01 | 12 Administer reference data | BR3, BR13 | TC-AD-016-03, TC-AD-016-05 |

| Legacy reference | Where it is kept |
|---|---|
| Legacy criteria AC1 and AC2 of RWB-AD-016, word for word with their origin tags | Section 7, TC-AD-016-01 and TC-AD-016-02 |
| The version "DOA-2026.11" with 95 limits and 218 rows, the item 2.1.1 L4 pair and the item 2.1.10 L1 row | Sections 3, 4, 7, 12.8, 13 |
| The whole-file refusal with MSG-P1-002, the falling limit and the unknown decision code | Sections 4, 5, 7, 8, 14 |
| The loader cannot approve, MSG-P7-002, and the 403 with MSG-P4-002 for RW-PRODHEAD | Sections 4, 5, 7, 8, 10, 14 |
| The dated lookup with the level, the row id and the version, `NOT_COVERED` with MSG-P7-010 and the related-party L1 answer | Sections 4, 5, 7, 8, 12.1 |
| The decision log entry of an approval and the 503 with MSG-P7-003 on an unwritable record | Sections 4, 5, 7, 8, 14 |
| SCR-41 Delegation of authority and SCR-39 Rules and parameters | Sections 1, 15, 19 |
| Permission checks "Rules and parameters A: RW-RISK" and "Reference data C: RW-COE, RW-REFADM" | Sections 8, 10, 14 |
| Test cases TC-AD-016-01 to TC-AD-016-04 | Section 16 |
| Rule IDs R-UNI-38 and R-UNI-39 | Sections 2, 8, 14, 17 |
| Field IDs DF-REF-016 to DF-REF-026, DF-REF-055 to DF-REF-062, DF-REF-034 to DF-REF-044 | Section 11 |
| DL18 holders and substitutes | Sections 3, 10, 13 |

### 19. Out of scope

- The `delegation_limit` table, its migration, its index, the version window, the difference report, the rollback and the version read: RWB-P4-E1038-APP. This story loads, approves and answers on that table and adds no column and no second writer.
- The routing of an approval to the holder of the level, the approval record, the queue, the escalation and the central decision log entry: `rwb-decision` (P7), with `ApprovalWorkflow`.
- The case status, the decision task and the service level timer projection: `rwb-case` (P3).
- The router side of the lookup — which case, which stage and which date is asked — and the story that owns the routing journey (RWB-P4-E2013-APP, legacy RWB-E2-013); this story answers the question and publishes the answer's contract (GAP-0842).
- The rule-version load, its approval and the SCR-39 screen (RWB-AD-011).
- The reference-data and parameter store itself, its lists and their versions: `rwb-case` (P3) through DP-06 and DP-07.
- Names of holders and substitutes, and the chapter 8 limits for hire purchase and unsecured loans: Risk with the product heads, DL18.
- The base contract of the four operations as a service-wide document; that is RWB-P4-AD016-CON's, and this story implements against it.
- The cross-service journey harness and its evidence; no `-ITG` story is split from this legacy key here.
- The Helm chart, the Kafka subscription values, the dashboards, the alerts and the runbook of this capability (an OPS story of this legacy key).
