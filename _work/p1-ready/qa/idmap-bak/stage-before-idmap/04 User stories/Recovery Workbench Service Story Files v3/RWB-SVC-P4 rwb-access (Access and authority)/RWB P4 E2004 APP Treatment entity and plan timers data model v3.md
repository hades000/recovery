# RWB-P4-E2004-APP Treatment entity and plan timers data model

**Version 3 changes.**

- MSG-P4-001 carries the English text of Error and Message Standard v6 (RD-P1-004).

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E2004-APP |
| Readiness decisions | RD-P1-004 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P4-AF |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P4-E2004-APP-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E2004-CON |
| Platform prerequisites (delivery, not per-story blockers) | Platform contracts of the patterns DP03, DP06, DP07, DP09 and DP19 (Template and Rules v1 R5.5); the platform H rows and self-referential C rows that the patterns listed under Patterns applied add are held by the platform and contract stories and are not repeated on this line; the story stays Day 1 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-CHO-006, REQ-CHO-007, REQ-RDF-014, REQ-CWC-011) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-004 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E2004-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 31 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **restructuring officer (RW-RESTRUCT), a case owner (RW-CASEOWN) and the access service that holds the role matrix and the delegation of authority table**, I want **the access decision for the treatment record and for the plan timers behind the authorise contract, the delegation lookup for the approval the treatment carries, the scope answer for the case the treatment hangs on, and one access entry per decision**, so that **the right role reads the treatment and its timers, a role without the right is refused with one message, an approval level the delegation table does not cover is never allowed, and every look at the treatment and at a plan timer is recorded once with the IDs and the field IDs only**.

Inside `rwb-access` this is the treatment-and-plan-timer slice of the legacy story RWB-E2-004:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- Five deliverables, and nothing else: (a) the authorise decisions for the treatment record read and for the plan-timer read behind `POST /api/recovery/access/v1/authorise` — Treatment and offer R, and CRUA where the role holds it, for `RW-RESTRUCT`; Treatment and offer CRU and Case record R for `RW-CASEOWN`; Case record R for the timer read; and a refusal with MSG-P4-002 for a role without Treatment and offer R, which is the legacy refusal of `RW-PHONECOL` (TC-E2-004-15); (b) the delegation-of-authority lookup behind `GET /api/recovery/access/v1/doa-limits` for the decision code and the product of the approval the treatment carries, read only from `delegation_limit` at the limit version in force, so the approval level written on the treatment can be checked against the approver's limit and a level the table does not cover is answered `NOT_COVERED` rather than allowed; (c) the scope answer for the case the treatment and its timers hang on, taken from the case attributes carried in the request and never from a `rwb_case` row; (d) one access entry per decision, appended through the decision-record library with its outbox row (DP-03, DP-09) and relayed as `DecisionRecorded` on `rwb.decision-record.v1` (EV-08); (e) the masking answer for the treatment fields and the timer fields.
- The treatment row, the `TreatmentRecords` interface, the timer rows, the plan rules R-RES-25 and R-RES-27, the route moves and the START, PAUSE and EXPIRE of a plan timer stay in `rwb-treatment` (RWB-S2-E2004-APP) and `rwb-case` (RWB-P3-E2004-APP), and the DP04 treatment extract stays with the reporting work of this legacy key. The DoA table load and its versions stay in `rwb-access` under RWB-P4-E1038-APP, and the approval router stays under RWB-P4-E2013-APP. This story reads the table and writes no row of it.
- The plan timer is a durable Temporal timer inside `TreatmentWorkflow` and `CaseWorkflow`; `TreatmentRecords.recordApproved`, the `changedSince` extract step and `TimerScheduler` are not built here. `JOB-05`, the Quartz timer check of the legacy story, is retired in the target (Architecture v5 slide 44).

### 2. Business rationale

A restructure, a settlement or a deed in lieu is agreed with terms, an approval level and a first due date, and the plan then runs on a clock: an installment falls due and, when a payment is missed, a cure period starts. The legacy story gave that record and that clock one story and one team; in the target the treatment and its timers belong to `rwb-treatment` and the case projection to `rwb-case`, and the right to look at them, the scope of the case, the authority of the approver and the record of the look belong to `rwb-access` — Recovery roles as data, scope, the masking policy, the DoA table and the access log (Architecture v5 slide 41), answered to every other service through the cached authorise call of slide 14.

Without this slice the treatment screen and the timer panel would each carry their own copy of who may read a treatment, the delegation of authority table would be read by whoever needed a level, and no service would know that a role without Treatment and offer R was refused. The legacy key owns that refusal once: `RW-PHONECOL` reads the treatment, is refused with MSG-P4-002 and one refusal entry is written (TC-E2-004-15), and the legacy authority line states that the approval itself is made at the level set by the delegation of authority (doa.txt, item 2.1.1, levels 1 to 6) before the story runs.

This story meets REQ-CHO-006, REQ-CHO-007 and REQ-CWC-011 on the access side — every treatment has one record whose read is decided for the right role, its plan timers are read under the same scope test, and the warning before a due date is shown only to a role that may read the timer — and it supports REQ-RDF-014 by making the treatment data product readable only through the reporting right of the reporting role. It keeps R-UNI-39 (a decision that cannot be recorded does not proceed) and gives NFR-042 (every read logged) its entry for this capability.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P3-E2004-CON | The `rwb-case` contract of this legacy key: the case resource with its owner, queue, team and route state, the timer resource behind `GET /cases/{caseId}/timers`, and its fixtures. It is used as a fixture only; this story calls no `rwb-case` operation at run time |
| RWB-P4-E1037-CON (same service) | The authorise contract of `rwb-access`: the `POST /api/recovery/access/v1/authorise` request and answer, the `GET /api/recovery/access/v1/me/permissions` resolved view, the masking read and the ADR refusal shape with MSG-P4-002. This story fills the treatment and timer decisions of that operation and adds no path to it |
| RWB-P4-E1038-APP (same service) | The `delegation_limit` table, its migration and the load of version DOA-2026.11 with 218 rows (109 MORTGAGE and 109 SSME), the approval of a version and the rollback. This story reads the table and writes no row of it |
| RWB-P4-E1037-APP and RWB-P4-AD002-APP (same service) | The `role`, `permission`, `masking_rule` and `role_conflict` tables and the policy pack loaded as data at matrix version PM-2026.12 |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the access entry of every decision |
| RWB-PLT-TE006-CON | The outbox and inbox library with CloudEvents (DP-09) |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06), for the decision-cache lifetime |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the reference-data contract of `rwb-case` (DP-07): LOV-CAPABILITY, LOV-APPROVAL-LEVEL, LOV-DECISION, LOV-PRODUCT and LOV-SCOPE with the version in force |
| RWB-PLT-E1047-CON | The topic naming library (DP-14) |
| RWB-PLT-E1044-CON | The per-service Flyway sequence and migration conventions (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route that serves SCR-14 and SCR-03 (DP-19) |

Business preconditions carried from RWB-E2-004:

- Case `RW-2026-000201` with product group `MORTGAGE` and route state `BOOKED_IN_ALS_NLEADS`; the treatment of the case carries approval level `L4`, decision log entry `DLE-9001` and offer amount `850000.00`; its first payment falls due on `2026-12-31`.
- Package `RESTRUCTURE` version `RES-2026.12` is in force with rows R-RES-25 and R-RES-27; the rows are evaluated in `rwb-case`, and this story evaluates no rule.
- Delegation version `DOA-2026.11` is in force from 30 November 2026; item 2.1.1 at level `L4` is two rows — principal 300,000,000.00 with loss up to 45.00 percent and maximum loss 150,000,000.00, and principal 50,000,000.00 with no loss limit. The approval the treatment carries is decision `D6.4` (and `D6.6` where the plan is a deed in lieu), regulation item 2.1.1, product `MORTGAGE`.
- The policy pack in force is matrix version PM-2026.12 (FSD P4 A2.4): Treatment and offer R for `RW-RESTRUCT` and CRUA where the role holds it, Treatment and offer CRU and Case record R for `RW-CASEOWN`, Case record R for the timer read, and no Treatment and offer row for `RW-PHONECOL`. The TSD P4 RBAC matrix tabulates only Rules and parameters, Reference data and Platform administration, so these two capability areas are read from the pack and confirmed with the matrix owner (GAP-0917; ASM-1639).
- The caller sends the case attributes the scope test needs — the case ID, its owner, its queue and its team — inside the authorise request; the request and answer field names are Not specified in the source documents (GAP-0917; ASM-1639).
- The treatment and timer field IDs the screens show arrive in the request; the exact per-screen field list is Not specified in the source documents (GAP-0920; ASM-1642).
- The login is the `rwb-access` login (DP-02), fixed once in the platform DB story of DP-02 and referenced here rather than repeated. Its name, grants and schema owner are Not specified in the source documents (GAP-0921; ASM-1643).

### 4. Flow

1. gateway-bff, `rwb-case` or `rwb-treatment` holds an action for this capability: a read of the treatment record on SCR-14 Treatment record, a read of the timer panel on SCR-03 Case record, or the authority of an approval that carries a level.
2. The caller sends `POST /api/recovery/access/v1/authorise` with the caller identity from the session, the capability area, the right, the treatment reference, the case reference, the case attributes for the scope test, the treatment or timer field IDs the screen will show and, where the decision is an approval, the approval level written on the treatment together with the decision code, the regulation item, the product group and the amounts.
3. `rwb-access`: the decision is served from the decision cache when the same identity, area, right, treatment reference, case reference and field list is already held under the matrix version in force; otherwise it is decided.
4. `rwb-access`: the caller's roles are read from `role`, and the letters of the area from `permission` at the matrix version in force (PM-2026.12); the letters are unioned across the roles the caller holds, and no role code, area or letter is written in code.
5. `rwb-access`: the scope test runs on the attributes carried in the request — OWN compares the case owner with the caller, TEAM the queue's team, REGION the team's region, ALL no test. No `rwb_case` row is read and no `rwb-case` operation is called, so the timer read is decided from the request alone (DP-01, DP-11).
6. `rwb-access`: an area with no letter, or a role with no permission row at all, is refused with 403 and MSG-P4-002, before any treatment or timer field is returned (default deny). A case that does not exist, or that sits outside the caller's scope, is answered 404 with MSG-P4-003 and no case data.
7. `rwb-access`: the masking answer is read from `masking_rule` at the masking version in force for the field IDs the caller names. The treatment record shows amounts, dates and IDs (the offer amount `850000.00`, the approval level, the booked date, the treatment and case IDs) and the timer shows a due date (`2026-12-31`) and its type (`INSTALLMENT_DUE`, `CURE_PERIOD`); no personal field is on either list, so no masking row applies and nothing is unmasked by this decision.
8. Where the decision is the authority of an approval, `rwb-access` calls its own delegation lookup `GET /api/recovery/access/v1/doa-limits` with the decision code (`D6.4` or `D6.6`), the regulation item (`2.1.1`), the product group (`MORTGAGE`), the principal, the loss percentage and the loss amount, and the approval date.
9. `DoaLimitLookupService` resolves the limit version in force on that date from the `valid_from` and `valid_to` of the rows, and selects the lowest level whose row covers the decision, the item, the product and the amounts. It answers the level, the delegation row ID, the limit version (`DOA-2026.11`), the holder and the substitute, with outcome `COVERED`.
10. The approval level written on the treatment (`L4`) is compared with the level the lookup answered. A level at or below the answer is within the approver's limit. A level the version in force does not cover — no row for the product, or an amount above every covering row — is answered `NOT_COVERED` with no level, and the authority decision refuses: the approval is not allowed, and no level is guessed.
11. `rwb-access`: one access entry is written for the decision, first, in the same transaction as the answer, with decision code `AC-READ` or `AC-DENY`, the actor, the case ID, the treatment ID where the decision names one, the area, the right, the field IDs and the time. The entry holds no amount, no due date and no personal field.
12. `rwb-access`: the entry is written through the decision-record library with its hash link and its outbox row, and the outbox relay publishes `DecisionRecorded` (EV-08) on `rwb.decision-record.v1` for the central ledger in `rwb-decision`. If that write fails the answer is 503 with MSG-P7-003 and nothing is returned (R-UNI-39).
13. The caller receives the decision with the decision code, the matrix version, the masking answer, the scope result and, where it asked for it, the delegation level and version; the screen shows the treatment or the timer panel, or the approver is told the level is not covered.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The area holds no letter, or the role has no permission row at all | Default deny; no treatment and no timer field is returned, and the treatment is unchanged | MSG-P4-002 | AC2 |
| X2 | The case does not exist, or sits outside the caller's scope | 404 with no case data, no treatment ID and no amount in the answer or the entry | MSG-P4-003 | AC6 |
| X3 | The request carries no owner, queue or team attribute for a scope test that needs one | No allow is decided from a partial answer; the caller retries with the attribute | MSG-P4-003 | AC8 |
| X4 | The limit version holds no row for the product, or no row covers the amount | `NOT_COVERED` with no level; the authority decision refuses and the approval is not allowed | None; the incident with MSG-P7-010 is `rwb-decision`'s | AC5 |
| X5 | The approval level on the treatment is above the level the lookup answered | The authority decision refuses, naming the level the table answered; no silent approval | MSG-P7-001 (produced by `rwb-decision`) | AC5 |
| X6 | The access entry cannot be written | 503 and no answer; nothing is shown and no case data is returned | MSG-P7-003 | AC7 |
| X7 | No masking row covers a field ID the caller names | Nothing is unmasked; the answer keeps the field masked as the default | None | AC7 |
| X8 | The same read is asked for twice | Both are answered from the cache under the same version; a new decision writes its own entry, because a read is an event and not a state change | None | AC7 |
| X9 | The policy pack in force has no row for the area on the business date | Default deny, never a default allow; the gap is alerted to RW-PLATADM | MSG-P4-002 | AC2 |
| X10 | A timer that has not started is asked for on the timer panel | The read is decided; the timer list comes from the `rwb-case` fixture, and no timer is created, paused or expired here | None | AC8 |

No exception path of this story moves a treatment, a case or a timer: this service answers and records, and the treatment state, the route state and the clock are `rwb-treatment`'s and `rwb-case`'s.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the `rwb_access` baseline, the authorise contract of RWB-P4-E1037-CON and the RWB-P3-E2004-CON fixture; the treatment and timer answers are contract fakes |
| Negotiable | Roles, areas, letters, scope values, DoA rows and versions, the masking rows and the cache lifetime are data rows and parameters; the story fixes the decision path |
| Valuable | Every look at a treatment and at a plan timer is decided once for the right role, refused with one message where the right is absent, and recorded once |
| Estimable | Two decisions behind one operation, one read-only lookup, one scope evaluator, one masking read, one entry writer and one cache |
| Small | Fits one sprint with its tests, as a secondary slice of the legacy key |
| Testable | Every criterion in section 7 is one automated test against a fixture, with a controlled clock where a date decides the limit version |

### 7. Acceptance criteria

```gherkin
Feature: Treatment entity and plan timers — access decisions, the delegation lookup and the access entries

  Background:
    Given the policy pack version "PM-2026.12" is in force with TREATMENT_AND_OFFER R for "RW-RESTRUCT", TREATMENT_AND_OFFER CRU and CASE_RECORD R for "RW-CASEOWN", CASE_RECORD R for the timer read, and no TREATMENT_AND_OFFER row for "RW-PHONECOL"
    Given delegation version "DOA-2026.11" is in force from 30 November 2026 and holds the item 2.1.1 row at level "L4" with principal 300,000,000.00, loss up to 45.00 percent and maximum loss 150,000,000.00
    Given case "RW-2026-000201" with product group "MORTGAGE" and route state "BOOKED_IN_ALS_NLEADS"
    Given decision log entry "DLE-9001" records the approval of a restructure at level "L4"
    Given package "RESTRUCTURE" version "RES-2026.12" is in force with rows R-RES-25 and R-RES-27

  Scenario: AC1 The treatment record read is allowed for the restructuring officer (new, D-RCV-60)
    Given the caller holds role "RW-RESTRUCT" with scope "OWN" and owns case "RW-2026-000201"
    When the caller asks POST /api/recovery/access/v1/authorise for capability area "TREATMENT_AND_OFFER", right "R", treatment "TRT-SYN-0201" on case "RW-2026-000201" and the field IDs of the treatment record
    Then the answer grants the read with decision code "AC-READ" and matrix version "PM-2026.12"
    And the delegation lookup for decision D6.4, item 2.1.1, product "MORTGAGE" on the approval date answers level "L4" against version "DOA-2026.11", so the level "L4" written on the treatment is within the approver's limit
    And one access entry is written with decision code "AC-READ", the actor, case "RW-2026-000201", the treatment ID, area "TREATMENT_AND_OFFER", right "R" and the field IDs

  Scenario: AC2 A role without Treatment and offer R is refused (new, D-RCV-60)
    Given the caller holds only role "RW-PHONECOL" and the pack holds no TREATMENT_AND_OFFER row for it
    When the caller asks POST /api/recovery/access/v1/authorise for area "TREATMENT_AND_OFFER", right "R" and treatment "TRT-SYN-0201" on case "RW-2026-000201"
    Then the call is refused with status 403 and message MSG-P4-002 for action "read the treatment"
    And no treatment field is returned and the treatment is unchanged
    And one entry is written with decision code "AC-DENY", area "TREATMENT_AND_OFFER", right "R" and result "REFUSED"

  Scenario: AC3 The case owner reads the treatment and the timer (new, D-RCV-60)
    Given the caller holds role "RW-CASEOWN" with scope "TEAM" and case "RW-2026-000201" sits on a queue of the caller's team
    When the caller asks POST /api/recovery/access/v1/authorise for area "TREATMENT_AND_OFFER", right "R" and treatment "TRT-SYN-0201"
    And the caller asks for area "CASE_RECORD", right "R" and the timer panel of case "RW-2026-000201" with timer types "INSTALLMENT_DUE" and "CURE_PERIOD"
    Then both answers grant the read with decision code "AC-READ" and matrix version "PM-2026.12"
    And two access entries are written, one for the treatment read and one for the timer read

  Scenario: AC4 The delegation lookup answers the level the treatment carries (new, D-RCV-60)
    Given the SIT fixture of RWB-P4-E1038-APP holds the lower-level rows of item 2.1.1 below principal 300,000,000.00
    When the rwb-decision service identity calls GET /api/recovery/access/v1/doa-limits with decisionCode "D6.4", regulationItem "2.1.1", productGroup "MORTGAGE", principal 300,000,000.00, lossPct 20.00, lossAmount 60,000,000.00 and onDate 15 December 2026
    Then the response is 200 with level "L4", limitVersion "DOA-2026.11", the delegation row ID of the item 2.1.1 L4 row and outcome "COVERED"
    Then the approval level "L4" written on the treatment is checked against that answer and is within the limit, so the authority decision allows the approval

  Scenario: AC5 A level above the limit is not covered and the approval is not allowed (new, D-RCV-60)
    Given delegation version "DOA-2026.11" holds no row for product group "HIRE_PURCHASE"
    Given the treatment on case "RW-2026-000202" carries approval level "L4" and product group "HIRE_PURCHASE"
    When the delegation lookup is asked for decision D6.4, item 2.1.1, "HIRE_PURCHASE", principal 900,000.00 and onDate 15 December 2026
    Then the response is 200 with outcome "NOT_COVERED" and no level, no delegation row and no holder
    Then the authority decision behind POST /api/recovery/access/v1/authorise refuses the approver with outcome "NOT_COVERED" and no level, so the approval is not allowed
    Then the hold of the item and the incident with MSG-P7-010 are rwb-decision's, and this story produces neither

  Scenario: AC6 A case outside the caller's scope is not returned (new, D-RCV-60)
    Given the caller holds role "RW-RESTRUCT" with scope "OWN" and does not own case "RW-2026-000999"
    When the caller asks POST /api/recovery/access/v1/authorise for area "TREATMENT_AND_OFFER", right "R" and treatment "TRT-SYN-0999" on case "RW-2026-000999"
    Then the answer is status 404 with message MSG-P4-003 and carries no case data, no treatment ID and no amount
    And one entry is written with decision code "AC-DENY", area "TREATMENT_AND_OFFER", right "R" and case "RW-2026-000999"

  Scenario: AC7 The entry carries the treatment ID and the field IDs only (new, D-RCV-60)
    Given the caller holds role "RW-RESTRUCT" with scope "OWN" and reads the treatment of case "RW-2026-000201" with the offer amount 850000.00 and the first due date 2026-12-31
    When the read of the treatment record and the read of the timer panel are decided
    Then the treatment entry carries case "RW-2026-000201", the treatment ID, area "TREATMENT_AND_OFFER", right "R" and the field IDs
    And the timer entry carries case "RW-2026-000201", the treatment ID, area "CASE_RECORD", right "R" and the field IDs
    And neither entry holds the offer amount 850000.00, the due date 2026-12-31, a name, an address, an identity number or an account number
    And both entries are appended through the decision-record library and relayed on "rwb.decision-record.v1" as DecisionRecorded

  Scenario: AC8 The timer read is decided from the request and reads no case row (new, D-RCV-60)
    Given the caller holds role "RW-CASEOWN" with scope "OWN" and the request carries the owner, the queue and the team of case "RW-2026-000201"
    Given the rwb-case contract mock returns the timer list of case "RW-2026-000201" with an "INSTALLMENT_DUE" timer due 2026-12-31 and a "CURE_PERIOD" timer, as a fixture only
    When the timer read for case "RW-2026-000201" is decided
    Then the decision is taken from the attributes in the request, and no row of rwb_case is read, no rwb-case operation is called and no v_ace_* view is read
    And a request that carries no owner attribute decides no allow and answers MSG-P4-003
    And no timer is started, paused or expired here, because the plan timer is a durable timer inside TreatmentWorkflow and CaseWorkflow

  Scenario: AC9 A role, area and right are read from the pack and never from code (new, D-RCV-60)
    Given the policy pack version "PM-2026.12" holds a TREATMENT_AND_OFFER row with right "R" for role "RW-RESTRUCT"
    And the caller holds role "RW-RESTRUCT" with scope "OWN" and owns case "RW-2026-000201"
    When the caller asks POST /api/recovery/access/v1/authorise for area "TREATMENT_AND_OFFER", right "R" and treatment "TRT-SYN-0201" on case "RW-2026-000201"
    Then the answer is decided from the matrix version in force, with decision code "AC-READ" as in AC1
    And no role code, area, letter or scope value is written in code: a change of the pack row changes the answer without a code change

  Scenario: AC10 A call without a valid credential is answered 401 (new, D-RCV-60)
    Given the caller presents no valid credential
    When the caller asks POST /api/recovery/access/v1/authorise for area "TREATMENT_AND_OFFER", right "R" and treatment "TRT-SYN-0201" on case "RW-2026-000201"
    Then the answer is status 401 and carries no treatment field, no case data and no amount
    And the same status 401 is answered for GET /api/recovery/access/v1/doa-limits
```

The ten criteria above are new and test only this deliverable: the treatment and timer decisions behind the authorise contract, the delegation lookup, the scope answer and the access entries. The legacy criteria of RWB-E2-004 are owned elsewhere: AC1 to AC14 of the legacy story are carried by `rwb-treatment` (RWB-S2-E2004-APP), `rwb-case` (RWB-P3-E2004-APP) and `rwb-source-data` (the DP04 extract); the legacy refusal of `RW-PHONECOL` with MSG-P4-002 (TC-E2-004-15) and the legacy authority line are answered here, by AC1, AC2, AC4 and AC5.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The access decision for a treatment and for a plan timer is served only by `rwb-access`, on the authorise contract, from the matrix version in force; every other service and every agent asks it before a read (DP-08) | Architecture v5 slides 14 and 41; DP-08 |
| BR2 | Roles, capability areas, letters, scope values, the masking rows, the DoA rows and the limit versions are data with their version; no role code, area, letter, scope value or level is written in code | FSD P4 A2.3, A2.4, A2.6; BR-P4-004; BR-P4-006; TSD P4 T3.2 |
| BR3 | A capability area with no letter, and a role with no permission row, are refused (default deny), never allowed by default | FSD P4 A2.4; VR-P4-004-1 |
| BR4 | The scope of a treatment or a timer read is decided from the case attributes carried in the request; a missing attribute never decides an allow | FSD P4 A2.14; DP-11 |
| BR5 | A case outside the caller's scope is answered as not found with MSG-P4-003 and returns no case data | FSD P4 A2.14 AC-EXC-P4-014-01 |
| BR6 | The delegation lookup answers the lowest level whose row covers the decision, the regulation item, the product and the amounts, with the row and the limit version in force on the approval date | FSD P4 A2.6 AC-ALT-P4-006-01; RWB-E1-038 |
| BR7 | The approval level written on the treatment is checked against that answer; a level the version in force does not cover is answered `NOT_COVERED` with no level, and the approval is never allowed on a guess | FSD P4 A2.6 AC-EXC-P4-006-04; Architecture v5 slide 14 |
| BR8 | Every decision, allowed or refused, writes one access entry with decision code `AC-READ` or `AC-DENY`, the actor, the case ID, the treatment ID where the decision names one, the area, the right, the field IDs and the time | FSD P4 A2.7 |
| BR9 | The access entry is a decision-record entry written through the local decision-record library and relayed as `DecisionRecorded` on `rwb.decision-record.v1`; it is never a new Kafka event and never a new topic (DP-03, EV-08) | FSD P4 A2.8; Architecture v5 slide 42 (08 DecisionRecorded) |
| BR10 | A decision that cannot be recorded does not proceed: 503 with MSG-P7-003 and nothing returned | R-UNI-39; FSD P4 AC-EXC-P4-007-03 |
| BR11 | No masking row is needed for this capability: the treatment record shows amounts, dates and IDs and the timer shows a due date; no personal field is on either, and the masking answer is still read per field ID | FSD P4 A2.5; TSD P4 T3.1 (`masking_rule`) |
| BR12 | The clock is not this service's: a plan timer is a durable Temporal timer inside `TreatmentWorkflow` and `CaseWorkflow`, and JOB-05 is retired; this story starts, pauses and expires no timer | Architecture v5 slides 42 and 44; Temporal and Drools design, durable timers |
| BR13 | The plan rules R-RES-25 and R-RES-27 of package `RESTRUCTURE` version `RES-2026.12` are evaluated in `rwb-case`; this story reads no rule, no package and no DRL source | DP-04; Arch v5 slides 14 and 41 |
| BR14 | No row of `delegation_limit` is written here, and no row of `treatment`, `timer` or `rwb_case` is read: the owner's contract or the request carries every fact | DP-01; TSD P4 T4 |

Target-service statements that make the rules hold in `rwb-access`:

- Legacy BR11, the authority of the approval, is answered here as the delegation lookup plus the level comparison of BR6 and BR7; the legacy statement that a plan timer goes only through `TimerScheduler` is not this service's, and `JOB-05` is retired in the target (BR12).
- BR1 and BR3 are the permission rows of the caller's roles in the area; the union across roles is taken, so a second role can only add a letter, never take one away.
- BR4 is the scope evaluator over the request attributes: OWN, TEAM, REGION and ALL are LOV-SCOPE values, and no case row is read (DP-01). This is also how the timer read is decided, so the timer panel needs no `rwb-case` call for its decision.
- BR6 and BR7 are one read over `delegation_limit` with the date window and the amount predicates, then one comparison; the version is a column of the row, so the answer can never name a row and a version that do not belong together.
- BR8 and BR9 are the record appender of DP-03 inside the transaction that produces the answer; there is no separate access-log table in `rwb_access`, so access and decisions are queried together.
- BR11 is proven by a test that lists the field IDs of the treatment record and of the timer panel and asserts that `masking_rule` holds no row for any of them and that none is a personal field.
- BR13 is the absence of any rule read: the treatment's approval and its plan rows reach this service only as facts in the request.

Rule coverage: BR1 by AC1, AC2 and AC3 (TC-E2-004-01, TC-E2-004-02); BR2 by AC9 (TC-E2-004-21); BR3 by AC2 (TC-E2-004-15); BR4 by AC3, AC6 and AC8 (TC-E2-004-02, TC-E2-004-07); BR5 by AC6 (TC-E2-004-07); BR6 by AC4 (TC-E2-004-01); BR7 by AC5 (TC-E2-004-17, TC-E2-004-20); BR8 by AC2, AC6 and AC7 (TC-E2-004-03, TC-E2-004-08, TC-E2-004-15); BR9 by AC7 (TC-E2-004-18); BR10 by AC7 (TC-E2-004-09); BR11 by AC7 (TC-E2-004-03); BR12 by AC8 (TC-E2-004-02, TC-E2-004-14); BR13 by AC1 (TC-E2-004-13); BR14 by AC8 (TC-E2-004-19).

### 9. State transitions

This service holds no treatment, timer, case or approval state. The states it answers are the outcomes of a decision and of a lookup.

| From | Event | Condition | To |
|---|---|---|---|
| permission row in force at PM-2026.12 | AccessPolicyChanged | A new matrix version is loaded, approved and in force | permission row in force at the new version; the cached decision under the old version is dropped |
| no letter for the area, or no permission row | an authorise request | The area and the right are asked for | refused, `AC-DENY`, one entry written |
| letter held | an authorise request for a treatment or a timer read | The case is outside the caller's scope | 404 MSG-P4-003, `AC-DENY`, one entry written |
| limit version in force on the approval date | a delegation lookup | A row covers the decision, the item, the product and the amounts | `COVERED`, the level, the row and the version answered |
| limit version in force on the approval date | a delegation lookup | No row covers the product or the amount | `NOT_COVERED`, no level, the approval not allowed |
| a new limit version approved with a later valid-from date | a delegation lookup | The lookup is dated on or after that date | the new version answers; the older rows stay readable for their own dates |

| Command | Condition | Outcome |
|---|---|---|
| Treatment or timer read | Letter for the area, and the case attributes inside the caller's scope | `AUTHORISED`, `AC-READ`, one entry with the treatment ID and the field IDs |
| Treatment or timer read | No letter for the area | `REFUSED` 403, MSG-P4-002, one entry with `AC-DENY` |
| Treatment or timer read | Letter held, case outside the scope | `REFUSED` 404, MSG-P4-003, one entry with `AC-DENY` |
| Authority of an approval | The level on the treatment is at or below the level the lookup answered | `AUTHORISED`, `AC-READ`, the level and the version on the answer |
| Authority of an approval | No row covers the decision, the product or the amount | `REFUSED`, outcome `NOT_COVERED`, no level, the approval not allowed |

The treatment state, the case route state and the timer status move in `rwb-treatment` and `rwb-case`; this story reads none of them and changes none of them. A delegation version moves LOADED to APPROVED to IN_FORCE to SUPERSEDED or ROLLED_BACK under RWB-P4-E1038-APP (TSD P4 T3.2 LOV-VERSION-STATUS); this story only reads the version in force.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The `rwb-access` service identity (the `rwb-access` login, DP-02) | Serves the decision, reads the matrix, the masking rows and the delegation rows, and writes the access entry and its outbox row |
| The decision-record library identity | Appends the access entry with its hash link and relays it on `rwb.decision-record.v1` (Decision log C, DP-03) |
| RW-RESTRUCT, restructuring officer | Treatment and offer R, and CRUA where the role holds it: reads the treatment record and its terms on SCR-14 |
| RW-CASEOWN, case owner | Treatment and offer CRU and Case record R: reads the treatment and the timer panel on SCR-14 and SCR-03 |
| RW-PHONECOL, phone collector | No Treatment and offer row: the treatment read is refused with MSG-P4-002 (legacy TC-E2-004-15) |
| RW-BIANAL, reporting and BI analyst | Reads the treatment data product under the reporting right of the reporting role; this story decides no reporting read |
| The `rwb-decision` service identity | Calls `GET /api/recovery/access/v1/doa-limits` with the decision, the item, the product and the amounts; the exact scope of this identity is Not specified in the source documents (GAP-0917; ASM-1639) |
| `rwb-access` itself | Reads `role`, `permission`, `masking_rule` and `delegation_limit` in its own schema and writes no row of them in this story |

The approval itself is made at the level set by the delegation of authority (doa.txt, item 2.1.1, levels 1 to 6) before this story runs; this story answers which level the table covers for the decision, the product and the amounts, and refuses a level it does not cover.

The refusal shape is 403 with an RFC 9457 problem response and `messageId` set: MSG-P4-002 for an absent right and MSG-P4-003 for a case outside the scope. No amount, no holder and no substitute is returned in a refusal, so a refusal cannot be used to map the delegation table.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-038 | `role` | id, role_code, role_name, role_class, default_scope; entra_group (Not specified in the source documents (DOR-RWB-P4-E2004-APP-7)) | Read |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read |
| DF-REF-198 to DF-REF-204 | `masking_rule` | role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read |
| DF-REF-016 to DF-REF-026 and DF-REF-055 to DF-REF-062 | `delegation_limit` | decision_code, approval_level, product_group, principal_limit, loss_pct_limit, max_loss_amount, holder_user_id, substitute_user_id, valid_from, valid_to, limit_version, regulation_item | Read |
| DF-TRT-001 to DF-TRT-014 | treatment (named in the authorise request through the `rwb-treatment` contract) | the treatment record fields the read shows, including the approval level and the offer amount | Not read and not written; named as field IDs |
| DF-TRT-029 | treatment | first_due_date | Not read and not written; named as a field ID |
| DF-WRK-027 to DF-WRK-036 | timer (named in the request through the `rwb-case` contract) | the timer fields the panel shows, including its due date and its type | Not read and not written; named as field IDs |
| DF-WRK-042 | timer | treatment_id | Not read and not written; named as a field ID |
| DF-CAS-001 | case attributes carried in the request (`rwb-case` owns the case) | id | Read from the request; nothing copied |
| (case owner, queue and team) | case attributes carried in the request | the scope attributes; their field IDs are Not specified in the source documents (GAP-0917; ASM-1639) | Read from the request; nothing copied |
| DF-DEC-001 to DF-DEC-018 and DF-DEC-028 to DF-DEC-031 | access entry (local decision record) | decision code, actor, case ID, actions (area, right, field IDs, result), decided at, hash chain, idempotency key | Write |

No treatment row, no timer row, no `rwb_case` row and no ACE row is copied into `rwb_access`: the treatment and timer facts arrive with the authorise request as field IDs and a treatment reference, and the case attributes for the scope test arrive on each decision. The entry holds IDs and field IDs only: no offer amount, no due date, no account number and no personal field. Field IDs are those in the Logical Data Model and Data Dictionary v9. This story owns the DDL, keys, constraints, indexes, dictionary rows and Flyway baseline of the five rwb_access tables (role, permission, role_conflict, masking_rule and delegation_limit); RWB-P4-E1037-CON keeps the contract stub and creates no table, and any sibling reference to the rwb_access baseline names the version this story applies.

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Owner | Purpose | Request | Response | Errors | Idempotency |
|---|---|---|---|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` | Decide a role's read of a treatment record or a plan timer, and the authority of an approval, with the masking answer and the access entry | Caller identity from the session, capability area, right, treatment reference, case reference, the case attributes for the scope test, the field IDs, and for an approval the approval level with the decision code, the regulation item, the product group and the amounts | Decision code (`AC-READ` or `AC-DENY`), matrix version, the masking answer per field ID, the scope result, the entry reference and, for an approval, the level, the delegation row, the limit version and the outcome | 401 (MSG-P4-001); 403 no letter (MSG-P4-002); 404 case absent or out of scope (MSG-P4-003); 422 missing field (MSG-GEN-001); 503 entry not written (MSG-P7-003) | Idempotent by identity, area, right, treatment reference, case reference and field list within the cache window |
| GET | `/api/recovery/access/v1/doa-limits` | P4 `rwb-access` | Answer the level, the delegation row and the limit version for one decision on one date | Query: `decisionCode`, `regulationItem`, `productGroup`, `principal`, `lossPct`, `lossAmount`, `onDate` | `level`, `delegationLimitId`, `limitVersion`, `holderUserId`, `substituteUserId`, `outcome` (`COVERED`, `NOT_COVERED`, `NO_HOLDER`, `NO_AMOUNT_LIMIT`, `RELATED_PARTY`) | 401; 403 Reference data R (MSG-P4-002), the area and right the DoA read declares; 422 missing or unknown query field (MSG-GEN-001); 503 entry not written (MSG-P7-003) | Not applicable, read only |
| GET | `/api/recovery/access/v1/me/permissions` | P4 `rwb-access` | The caller's resolved roles, scope, matrix version and letters per capability area | None | Session permission view | 401; 503 | Not applicable |

Both `POST /authorise` and `GET /me/permissions` are the service baseline's operations under RWB-P4-E1037-CON; this story fills their treatment and timer decisions and changes no other operation. `GET /doa-limits` is the operation Architecture v5 slide 14 names for `rwb-access`, under the base `/api/recovery/access/v1` of DP-13; it is absent from the TSD P4 appendix T-A, whose endpoint inventory has no DoA path at all, and its request and answer field set is Not specified in the source documents (GAP-0918; ASM-1640). The authorise request and answer field set is likewise Not specified in the source documents (GAP-0917; ASM-1639), and the contract review confirms or renames it before the endpoint is frozen.

The authority part of `POST /authorise` is not a new path: it adds the approval level, the decision code, the regulation item, the product group and the amounts to the existing request, and the level, the delegation row, the limit version and the outcome to the existing answer. The DoA table's own load, verify, approve and rollback endpoints (API-P4-005, API-P4-006, API-P4-009 and API-P4-010 of TSD P4 T-A.1) are RWB-P4-E1038-APP's and are not touched here.

#### 12.2 REST operations consumed

None. The treatment and the case attributes travel in the authorise request, and the timer list of the `rwb-case` contract and the treatment record of the `rwb-treatment` contract are fixtures only: this story calls no operation of either service at run time, so the one hop and the 2 s budget of DP-11 apply to the inbound call alone. The reference lists and the cache lifetime reach this service through the client libraries of DP-06 and DP-07, not by a call per decision.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7, written through the local library of DP-03 | caseId, or the actor for an entry with no case | decision code, area, right, field IDs, matrix version, treatment ID, record reference, decided at |

One event type only. `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoaLimitChanged.v1` belong to the stories that put a policy version or a limit version in force (RWB-P4-AD002-APP and RWB-P4-E1038-APP); this story publishes neither, because it writes no policy row and no limit row. The event is written to the outbox in the same transaction as the answer and relayed with the CloudEvents 1.0 envelope; it carries no name, no e-mail address, no amount, no due date and no personal field (DP-09).

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 (events: none) and this story adds no subscription. The permission caches that other services refresh on `rwb.access.AccessPolicyChanged.v1`, and the treatment and timer facts those services hold, are their concern: this story reads neither `rwb.treatment.TreatmentApproved.v1` nor `rwb.case.events.v1`.

#### 12.5 Workflows and activities

None. The plan timers are durable timers inside `TreatmentWorkflow` in `rwb-treatment` and `CaseWorkflow` in `rwb-case`; this story starts no workflow, signals no workflow and registers no activity on the `rwb-access` queue. `TimerDue` (EV-18) is retired as a Kafka event (Architecture v5 slide 42) and is observed on the workflow history of the case, not here.

#### 12.6 Schedules

None. `JOB-05` Timer check is retired: the 5-minute timer check is replaced by durable timers inside each workflow (Architecture v5 slide 44), and this story holds no Schedule of its own. The six-monthly access review list (`JOB-18`) is a Schedule of `rwb-access` and belongs to RWB-P4-AD008-APP.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | Read only: the caller's roles and their class and default scope |
| `permission` | P4 (`rwb_access`) | Read only: the letters of the area at the matrix version in force |
| `masking_rule` | P4 (`rwb_access`) | Read only: the masking answer per field ID; no row covers a treatment or timer field |
| `delegation_limit` | P4 (`rwb_access`) | Read only: the version in force, the covering row, the holder and the substitute. Created and loaded by RWB-P4-E1038-APP |
| access entry (local decision record) | P4 rows in `rwb_access`, written through the decision-record library of DP-03 | One entry per decision, `AC-READ` or `AC-DENY` |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | The outbox row of the entry; no inbox row is written because no event is consumed (DP-09) |

`treatment`, `timer` and `case` are not this service's tables and are not read, not copied and not joined: the treatment and timer field IDs arrive in the request and the case attributes arrive with it, so no foreign key crosses a schema (DP-01). `lov_value` and the reference tables are reference data read through DP-07.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| `rwb-case` contract mock (RWB-P3-E2004-CON) | The `rwb-case` contract of this legacy key | Case `RW-2026-000201` with owner, queue, team, product group `MORTGAGE` and route state `BOOKED_IN_ALS_NLEADS`; the timer list behind `GET /cases/{caseId}/timers` with an `INSTALLMENT_DUE` timer due `2026-12-31` and a `CURE_PERIOD` timer; case `RW-2026-000999` outside the caller's scope |
| `rwb-treatment` fixture | The treatment facts the request names | Treatment `TRT-SYN-0201` on case `RW-2026-000201`, approval level `L4`, decision log entry `DLE-9001`, offer amount `850000.00`, first due date `2026-12-31`; the treatment of case `RW-2026-000202` with product group `HIRE_PURCHASE` |
| authorise and masking fake (RWB-P4-E1037-CON, RWB-PLT-E1037-CON) | The authorise contract and the guard library | A granted case, a refused role, the masking read and the problem mapping for 401, 403, 404 and 503 |
| decision-record fake (RWB-PLT-E1027-CON) | DP-03 | A healthy chain and outbox, and a stopped chain for the 503 path |
| reference-data fake (RWB-P3-E1043-CON) | DP-07 | LOV-CAPABILITY, LOV-APPROVAL-LEVEL (`L1` to `L6`), LOV-DECISION (`D6.4`, `D6.6`), LOV-PRODUCT and LOV-SCOPE with their versions |
| parameters fake (RWB-P3-E1042-CON) | DP-06 | The decision-cache lifetime |
| delegation fixture (RWB-P4-E1038-APP) | The DoA table | DOA-2026.11 with 218 rows, the two item 2.1.1 L4 rows, the lower-level rows of item 2.1.1 and the absent HIRE_PURCHASE rows |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 3 (`POST /authorise`, `GET /doa-limits`, `GET /me/permissions`), consumed 0 | Base `/api/recovery/access/v1`; no new path beyond the three, and no outbound call |
| Kafka | Published 1 event type (`DecisionRecorded`), consumed 0 | `rwb.decision-record.v1` only |
| Temporal | 0 workflows, 0 activities | The plan timers are durable timers in `rwb-treatment` and `rwb-case` |
| File | None | This story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/treatment`, Java package `th.co.scb.ace.workbench.recovery.access.treatment`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-10 applies as a statement that the clock is not this service's: the plan timer is a durable Temporal timer in `rwb-treatment` and `rwb-case`, and `JOB-05` is retired. DP-14 applies to the topic names this service publishes and consumes (none consumed here). DP-04 and DP-05 apply as prohibitions: this service evaluates no rule and reads no ACE view, so the treatment and the timer reach it as facts in the request only. DP-19 is carried by the legacy key and its work sits with the screens of SCR-14 and SCR-03 through gateway-bff. The screen states of SCR-14 and SCR-03 (empty, loading, error and no access) are served through the gateway-bff composite route; the wording and layout of each state are Not specified in the source documents (DOR-RWB-P4-E2004-APP-10).

This secondary slice adds no new build dependency of its own (metadata "Depends on (build)" is None): the platform contract libraries, the per-service Flyway baseline, the workflow kit, the outbox and the gateway route already arrive with the P4 service baseline and its own stories, in particular RWB-P4-E1037-CON, RWB-P4-E1037-APP and RWB-P4-E1038-APP, and this story builds against the published contracts and their fakes, at contract version v1 (the `/v1` segment of the rwb-access operations).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TreatmentAuthoriseController | Controller | The treatment and timer decisions and the authority part of `POST /authorise`; validation and the problem mapping for 401, 403, 404, 422 and 503 |
| TreatmentAccessService | Service | Unions the letters across the caller's roles for `TREATMENT_AND_OFFER` and `CASE_RECORD`, applies the scope test, decides `AC-READ` or `AC-DENY` and orders the entry write before the answer |
| TreatmentScopeEvaluator | Service | Compares the case owner, queue and team carried in the request with the role's default scope; refuses an allow when an attribute is missing; owns the timer read's scope answer |
| PlanTimerAccessService | Service | The timer-panel decision: Case record R on the case the timer list belongs to, from the request attributes only |
| DoaLimitController | Controller | `GET /doa-limits`: query validation, the version window and the problem mapping |
| DoaLimitLookupService | Service | Version in force for the approval date, lowest covering row, `NOT_COVERED`, and the level comparison against the approval level the treatment carries |
| DoaLimitRepository | Repository | Read-only queries over `delegation_limit`, with the date window and the amount predicates; no write method |
| PermissionReader | Service | The `role` and `permission` rows of the caller at the matrix version in force |
| MaskingReader | Service | The masking answer per field ID from `masking_rule`, and the proof that no treatment or timer field is personal |
| AccessEntryWriter | Service | The access entry through the decision-record library, first in the transaction, with its outbox row (DP-03, DP-09) |
| PolicyCache | Cache | Holds a decision under the matrix version and the limit version it was decided on; drops it on a version change |
| AccessCatalog | Service | LOV-CAPABILITY, LOV-SCOPE, LOV-APPROVAL-LEVEL, LOV-DECISION and LOV-PRODUCT through the reference-data contract of DP-07; no area, scope or level in Java |

**Database and migrations**

- Reads `role`, `permission`, `masking_rule` and `delegation_limit` in schema `rwb_access`; writes the access entry of the decision-record library and the outbox row.
- Migration in this story: `V2004_1__treatment_access_decision.sql` adds the index on `permission (capability_area, matrix_version, role_id)` used by the two decisions and the index on the access entry (actor, decided_at) used by the access-log search. The tables arrive with the `rwb_access` baseline; no column is added for a treatment, a timer or a case fact.
- No row of `role`, `permission` or `masking_rule` is written here (the pack is RWB-P4-AD002-APP's) and no row of `delegation_limit` is written here (the DoA versions are RWB-P4-E1038-APP's). The repository has no save, update or delete method, so a lookup cannot change a limit.

**Configuration and reference data**

- The policy pack slice in force at matrix version PM-2026.12: Treatment and offer R for `RW-RESTRUCT` and CRUA where the role holds it, Treatment and offer CRU and Case record R for `RW-CASEOWN`, Case record R for the timer read, and no Treatment and offer row for `RW-PHONECOL` (GAP-0917; ASM-1639).
- Delegation version `DOA-2026.11` in force from 30 November 2026, with item 2.1.1 at `L4` as the two rows named in section 3. The version that governs a decision is the version in force on the approval date, read from the row's `valid_from` and `valid_to`; the version in force in each environment is not a document value (GAP-0919; ASM-1641).
- No masking row for the treatment fields or the timer field IDs: none is a personal field, and the test of section 7 AC7 proves it.
- The decision-cache lifetime is a parameter read through the parameters contract (DP-06); its value is Not specified in the source documents (GAP-0917; ASM-1639).
- The per-screen field list of SCR-14 and SCR-03 is Not specified in the source documents (GAP-0920; ASM-1642), so the service accepts the field IDs in the request rather than fixing them in code.

**Build steps**

1. `PermissionReader` and `TreatmentAuthoriseController` over the matrix version in force, with a test per letter set; AC1 and AC2.
2. `TreatmentAccessService` with the letter union and the default-deny path; AC2 and the AC-EXC-P4-004-06 shape of the pack.
3. `TreatmentScopeEvaluator` over the request attributes, with the not-found, the missing-attribute and the no-partial-allow tests; AC6 and AC8.
4. `PlanTimerAccessService` for the timer panel: Case record R, the timer types and the due date named as field IDs, and no read of another service's schema; AC3 and AC8.
5. `MaskingReader` with the masking version, the no-row answer and the test that lists the treatment and timer field IDs and asserts that none is personal; AC7.
6. `DoaLimitRepository` and `DoaLimitLookupService`: the version in force, the lowest covering row, the item 2.1.1 `L4` answer and `NOT_COVERED`; AC4 and AC5. The repository test asserts that it exposes no write method.
7. `DoaLimitController` on `GET /doa-limits` and the level comparison against the approval level on the treatment; AC1, AC4 and AC5.
8. `AccessEntryWriter` and `PolicyCache`: the entry before the answer, the `AC-READ` and `AC-DENY` codes, the version-keyed cache and the 503 when the record cannot be written; AC7 and the record path of section 5.
9. The contract-fake run of the treatment, timer and DoA answers in isolation, so the story builds before `rwb-treatment` and `rwb-case` are live.
10. The denial test through the guard library for a role without Reference data R on the DoA read, and the service-identity test of section 10.

**Feature switch.** `rwb.access.treatment-authorise`, read as a parameter through the parameters contract. Off: the treatment and timer decisions are refused closed and the caller is told the capability is not open, never allowed by default. The DoA read is a read path and adds no switch of its own; the limit version in force governs it.

**Done when.** The tests in section 16 pass; the treatment record read is granted for `RW-RESTRUCT` and refused with MSG-P4-002 for `RW-PHONECOL` in SIT; the timer panel read is decided for `RW-CASEOWN` from the request attributes with no read of another service's schema; the lookup answers level `L4`, the row and `DOA-2026.11` for item 2.1.1 `MORTGAGE` and answers `NOT_COVERED` for `HIRE_PURCHASE`; a case outside the scope answers MSG-P4-003; and every decision leaves one access entry with the treatment ID and the field IDs and no amount and no due date.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | No Workbench role on the token | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. | This story, on both decisions |
| MSG-P4-002 | The area holds no letter for the caller's roles, or the role has no permission row | You cannot {action} here. Your role does not include it. | This story, on the treatment and timer decisions and on the DoA read (**legacy RWB-E2-004 section 14**) |
| MSG-P4-003 | The case is absent or outside the caller's scope, or a scope attribute is missing | This case is not in your scope. | This story, on the treatment and timer decisions |
| MSG-GEN-001 | A required field is empty, or a code is not in its list | Enter {field}. | This story, on the DoA query |
| MSG-P7-003 | The access entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on both decisions and on the DoA read |
| MSG-P7-001 | The approval level on the treatment is above the level the lookup answered | This needs approval at level {level}. It has been sent to {approver}. | This story returns the refusal with the level; `rwb-decision` returns the text to the approver |
| MSG-P7-010 | No limit covers the decision and the product | No approval limit covers {decision} for {product}. The item is held and Risk has been told. | `rwb-decision`, from this story's `NOT_COVERED` answer |

For MSG-P4-002 in this story, {action} names the action the caller tried — for example "read the treatment" or "read the plan timers" — and never a case fact. No message of this story names an amount, a due date or a personal field; MSG-P7-010 is raised and owned by `rwb-decision` and is copied here because the answer that triggers it is this story's.

### 15. Screens and states

SCR-14 Treatment record: the officer asks for the treatment of the case and sees its terms, its approval level (`L4`), its booked date and its outcome; the decision for that read comes from this story. SCR-03 Case record, timer panel: the case owner sees the `INSTALLMENT_DUE` timer due `2026-12-31` and, after a missed payment, the `CURE_PERIOD` timer; the decision for that read comes from this story, and the timer list itself is `rwb-case`'s.

| Screen | State | Where it is |
|---|---|---|
| SCR-14 Treatment record | Loading, approved, booked, refused; empty, error and no access: Not specified in the source documents (CG-ALL-5167) | gateway-bff composite route; the treatment is `rwb-treatment`'s, the decision is this story's |
| SCR-03 Case record (timer panel) | Loading, list, empty, refused; error and no access: Not specified in the source documents (CG-ALL-5166) | gateway-bff composite route; the timers are `rwb-case`'s, the decision is this story's |
| The approval a treatment carries | Covered, not covered, above the limit | `rwb-decision` (RWB-P4-E2013-APP) shows the level and the limit version this lookup answered |

Both screens are served by the gateway-bff composite route (DP-19), which calls `rwb-case` for the case and the timer list, `rwb-treatment` for the treatment and `rwb-access` for the decision, one hop each, and merges the answers into the screen model. The screen fields, the field-level masking of the composite route and the route specification are Not specified in the source documents (GAP-0920; ASM-1642). No screen is built in this story, and neither screen shows a personal field for this capability, so nothing is masked by this decision.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-004-01 | AC1, AC4, AC7 | End to end | Restructure, 36 installments, 850000.00 baht, entry DLE-9001: the treatment record read is authorised for RW-RESTRUCT, the delegation lookup answers L4, and the entry names the treatment ID and the field IDs only |
| TC-E2-004-02 | AC3, AC8 | End to end | First due date 2026-12-31 and an INSTALLMENT_DUE timer: the timer panel read is authorised for RW-CASEOWN from the request attributes, and no timer is started, paused or expired here |
| TC-E2-004-03 | AC7 | End to end | Ten treatments over three products, two booked: the access entries carry IDs and field IDs only, and no amount reaches the record |
| TC-E2-004-04 | AC1, AC7 | End to end | Restructure with no first due date: the read decision is taken on the treatment that exists, and the refusal of the record itself is rwb-treatment's |
| TC-E2-004-05 | AC1 | End to end | Unknown decision log entry DLE-0000: the entry is carried as an ID on the request, and its existence is rwb-treatment's and rwb-decision's check, not this story's |
| TC-E2-004-06 | AC1 | End to end | First due date one day before the proposal: the read decision is unaffected, and the date check is rwb-treatment's |
| TC-E2-004-07 | AC6, AC8 | End to end | Case in route state WITH_FCR_OFFICER: the read decision does not depend on the route state, and a case outside the caller's scope answers MSG-P4-003 |
| TC-E2-004-08 | AC7 | End to end | The same read asked for twice: the second is served from the cache under the same version, and a new decision writes its own entry because a read is an event |
| TC-E2-004-09 | AC7 | End to end | Decision-record store stopped in the test container: the answer is 503 MSG-P7-003, nothing is returned, and the entry count is unchanged |
| TC-E2-004-10 | AC7 | End to end | JOB-15 forced to fail on 2026-12-02: the DP04 extract is rwb-source-data's and rwb-reporting's, and this story decides no extract read |
| TC-E2-004-11 | AC6 | End to end | Closed case: the read decision answers on the scope, and the refusal of the record with MSG-P3-005 is rwb-case's |
| TC-E2-004-12 | AC3, AC8 | End to end | PaymentMissed for due date 2026-12-31: the CURE_PERIOD timer is read on the panel under the same scope test, and the cure period itself is rwb-case's |
| TC-E2-004-13 | AC1 | End to end | No RESTRUCTURE version in force on 2026-12-01: the in-force check is rwb-decision's and rwb-case's, and this story reads no rule |
| TC-E2-004-14 | AC8 | End to end | A component that inserts into the timer table without TimerScheduler: the boundary belongs to rwb-case, and this story adds no timer write at all |
| TC-E2-004-15 | AC2 | Component | RW-PHONECOL (no Treatment and offer right) reads the treatment; refused with MSG-P4-002 and one entry with AC-DENY and result REFUSED |
| TC-E2-004-16 | AC7 | NFR | The decision-log-first path: this story writes the access entry first and withholds the answer when it cannot be written; the timer-start ordering is rwb-case's and rwb-treatment's |
| TC-E2-004-17 | AC5 | Component | Item 2.1.1 with product group HIRE_PURCHASE: the lookup answers NOT_COVERED, as the lookup of TC-E2-004-01 answers L4 for MORTGAGE |
| TC-E2-004-18 | §12.1, §12.3 | Contract | The operations of section 12.1 and the event of section 12.3 are checked against the rwb-access contract and the Kafka catalog: the event type is rwb.decision.DecisionRecorded.v1 on topic rwb.decision-record.v1 |
| TC-E2-004-19 | §12.7 (ASM-3438) | Component | Each table of section 12.7 is read through rwb_access only: the repository exposes no write method on delegation_limit, and no treatment, timer or case table is read |
| TC-E2-004-20 | AC5 | Component | Item 2.1.1 with product group HIRE_PURCHASE and approval level L4: the authorise answer refuses the approver with NOT_COVERED, the approval is not allowed, and no hold or incident is written here |
| TC-E2-004-21 | AC9 | Component | The pack row for RW-RESTRUCT changed in a test copy of the pack: the authorise answer follows the row with no code change, as AC1 does |
| TC-E2-004-22 | AC10 | Component | A call to POST /api/recovery/access/v1/authorise or GET /api/recovery/access/v1/doa-limits with no valid credential: the answer is 401 and no treatment field, case data or amount is returned |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to End to end, Access to Component and Resilience to NFR as the rows show. Every legacy test case of this key is listed above with the one slice of its behaviour this story answers: the treatment record, the plan timers, the rules, the DP04 extract and the route moves belong to the other slices of this legacy key (RWB-S2-E2004-APP and RWB-P3-E2004-APP, with the extract step outside this service), and this story answers the access decision, the delegation lookup, the scope answer and the access entry. The `-ITG` copies of these cases are not here: they belong to RWB-ITG-E2004-ITG, which proves the same values end to end across `rwb-treatment`, `rwb-case`, `rwb-decision` and `rwb-access`.

### 17. Guardrails

- No business value in code: roles, capability areas, letters, scope values, the masking rows, the DoA rows, the approval levels and the limit versions are data rows and parameters read with the version in force. No role code, area, letter, scope value or level appears in Java, and a test proves that a new level or product group needs no build.
- No personal data in events, logs, tests or prompts. This story writes case IDs, treatment IDs and field IDs only; the access entry never carries a name, an address, an identity number, an account number, an amount or a due date, and the test data is synthetic (`TRT-SYN-0201`, `RW-2026-000201`, `850000.00`).
- ACE data only through the owner's contract or the owner's `v_ace_*` views: this story reads neither. The case attributes arrive in the authorise request and the group-to-role mapping belongs to the sign-in stories of `rwb-access`.
- No cross-schema read: `rwb_access` holds no foreign key into another schema and no copy of a treatment, a timer or a case row (DP-01). `role`, `permission`, `masking_rule` and `delegation_limit` are this service's own data.
- One writer per table: only RWB-P4-E1038-APP writes `delegation_limit`, and only RWB-P4-AD002-APP writes the pack. This story's repository has no write method and the DoA read cannot change a limit.
- No answer without its record: the access entry commits with the answer, and the answer is withheld with MSG-P7-003 when it cannot be written (BR10).
- The clock is not this service's: no timer is started, paused, resumed or expired here, `JOB-05` is retired, and no Quartz table is written (BR12, DP-10).
- The two decisions are read-only and idempotent; the DoA lookup is a pure function of the rows, the lists and the query, so a retry answers the same and writes a second entry, as a read must.
- A refused caller learns nothing about the table: a refusal carries the message and, for an insufficient level, the level, never a limit amount, a holder or a substitute.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-006 | A treatment record for every offer with type, terms, approval and outcome, read only by a role that holds the right | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-CHO-06 | 7.3 Negotiate settlement or deed in lieu | R-RES-25 | TC-E2-004-01, TC-E2-004-04 to TC-E2-004-07, TC-E2-004-13, TC-E2-004-15 |
| REQ-CHO-007 | Plan timers run from the treatment; a read of the plan is decided for the right role and the right scope | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-CHO-06 | 7.3 Negotiate settlement or deed in lieu | R-RES-25, R-RES-27, R-UNI-39, R-UNI-40 | TC-E2-004-02, TC-E2-004-08, TC-E2-004-09, TC-E2-004-12, TC-E2-004-14, TC-E2-004-16 |
| REQ-RDF-014 | The treatment data product is read only under the reporting right, and no personal field reaches it | Business Requirements Epic 2, section 4; Program, section 5.1 | FEAT-CHO-06 | 7.3 Negotiate settlement or deed in lieu | None | TC-E2-004-03, TC-E2-004-10 |
| REQ-CWC-011 | The warning before a due date reaches only a role that may read the timer | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-CWC-11 | 7.3 Negotiate settlement or deed in lieu | R-RES-25 | TC-E2-004-02, TC-E2-004-12 |

The supporting features of the policy pack are FEAT-ACA-04 (role to permission matrix as data), FEAT-ACA-05 (mask PDPA fields by role), FEAT-ACA-06 (the DoA table as reference data) and FEAT-ACA-07 (every access event to the access log); this slice answers them only for the treatment and plan-timer capability and changes neither the matrix, nor the masking design, nor the DoA table.

| Legacy reference | Where it is kept |
|---|---|
| Case `RW-2026-000201`, product group `MORTGAGE`, approval level `L4`, decision log entry `DLE-9001`, offer amount `850000.00`, first due date `2026-12-31` | Metadata, sections 3, 7, 12.8 |
| Package `RESTRUCTURE` version `RES-2026.12` with rows R-RES-25 and R-RES-27, evaluated in `rwb-case` | Sections 3, 7, 8 (BR13), 19 |
| Timer types `INSTALLMENT_DUE` and `CURE_PERIOD` | Sections 4, 7, 9, 12.8, 15, 16 |
| Delegation of authority item 2.1.1, levels 1 to 6, and the authority line of the legacy story | Sections 3, 4, 8, 9, 10 |
| The `RW-PHONECOL` refusal with MSG-P4-002 (TC-E2-004-15) and MSG-P4-003 | Sections 3, 7 (AC2, AC6), 10, 14, 16 |
| Legacy BR11, the timer port and `JOB-05`, retired in the target | Sections 1, 4, 8 (BR12), 12.5, 12.6, 17 |
| Legacy `GET /treatments/{treatmentId}` and `GET /cases/{caseId}/timers`, now the owner services' paths | Sections 1, 11, 12.1, 12.8, 15 |
| Legacy key RWB-E2-004, story RWB-P4-E2004-APP, contract RWB-P3-E2004-CON | Metadata, sections 3, 12 |
| Field IDs DF-REF-016 to DF-REF-062, DF-REF-198 to DF-REF-204, DF-TRT-001 to DF-TRT-029, DF-WRK-027 to DF-WRK-042 | Section 11 |

### 19. Out of scope

- The treatment row, the `TreatmentRecords` interface, the plan rules R-RES-25 and R-RES-27 and the route moves to `PLAN_RUNNING` and `PLAN_CURE_PERIOD`: `rwb-treatment` (RWB-S2-E2004-APP) and `rwb-case` (RWB-P3-E2004-APP). The DP04 treatment extract is the reporting work of this legacy key and is not this story's.
- The timer rows, the timer list behind `GET /cases/{caseId}/timers` and the durable timers inside `TreatmentWorkflow` and `CaseWorkflow`: `rwb-case` (RWB-P3-E2004-APP) and `rwb-treatment` (RWB-S2-E2004-APP). No timer is started, paused or expired here.
- The DoA table itself — its migration, its load of `DOA-2026.11`, the approval of a version and its rollback — under RWB-P4-E1038-APP; and the approval router, `ApprovalWorkflow` and the approval record under RWB-P4-E2013-APP.
- The machine-readable API document of `delegation_limit` (API Specification P4) and the change report of a DoA version.
- The treatment policy bands per product (FEAT-ADM-04, Epic 8) and the movement of an approval limit (FEAT-ADM-03, Epic 8; FSD P4 A2.19).
- The end-to-end proof of these values across the four services: RWB-ITG-E2004-ITG and the `-ITG` copies of the test cases.
- The policy pack loader and the masking design: RWB-P4-AD002-APP and RWB-P4-E1037-APP; the sign-in path and the group-to-role mapping: RWB-P4-E1022-APP and RWB-P4-AD001-APP.
- The access-log search screen, the break-glass grant and the six-monthly access review list (JOB-18): RWB-P4-AD007-APP, RWB-P4-AD006-APP and RWB-P4-AD008-APP.
- The `rwb_access` schema baseline, the per-service login, the topic and queue provisioning, the dashboards, the alerts and the runbook of this capability: the service baseline and the OPS story of this legacy key.
