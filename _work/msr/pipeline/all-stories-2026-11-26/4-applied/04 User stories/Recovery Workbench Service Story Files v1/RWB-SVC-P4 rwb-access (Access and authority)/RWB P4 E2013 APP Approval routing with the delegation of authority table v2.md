# RWB-P4-E2013-APP Approval routing with the delegation of authority table

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E2013-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP08, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P4-AI |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P7-E2013-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-APD-001, REQ-APD-003, REQ-APD-004, REQ-APD-005, REQ-APD-007, REQ-APD-008, REQ-APD-009, REQ-APD-010, REQ-APD-011) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-013 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-E2013-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **approver, and the access service that holds the delegation of authority table as data**, I want **the delegation table answered as one lookup that names the lowest level whose row covers the decision, the row and the delegation version, and the authority of the person in front of me decided against that level**, so that **no screen and no service has to read a limit row of its own, every approval in the Workbench follows the versioned delegation table, and the audit trail shows the level, the row and the version that were used**.

Inside `rwb-access` this is the delegation-of-authority capability of the legacy story RWB-E2-013:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- Two deliverables, and nothing else: the lookup `GET /api/recovery/access/v1/doa-limits`, which answers level, delegation row, delegation version, holder, substitute and outcome for one decision and one date; and the approver-authority decision behind the existing `POST /api/recovery/access/v1/authorise`, which answers whether the caller holds the A letter in the decision's capability area and is the holder or substitute of the required level, or holds the route role.
- The approval record, the approval routing workflow (`ApprovalWorkflow` of the kit), the approval endpoints, the case status, the decision task, the service level timer, the escalation, the queue screen SCR-10 and the central decision log entry stay in `rwb-decision` (P7). This story runs no workflow and opens no case state.
- Loading, approving and rolling back a delegation version stay in `rwb-access` under RWB-P4-E1038-APP. This story reads the table and never writes a row of it.
- Every lookup and every authority decision appends one entry to the access log, and the access log of the target is a decision-record entry of the local library of DP-03, not a separate access-log table.

### 2. Business rationale

Approval and authority governance is an audit finding: approvals today are given by e-mail, sometimes above the approver's limit or by the person who prepared the decision. The delegation of authority table is the control that answers the question, but only if the answer is one service's answer and not a copy of the table on every screen. Legacy RWB-E2-013 read the table through the in-process `DelegationOfAuthority` interface of the monolith and checked authority through `RecoveryAccessGuard`; in the target both of those become `rwb-access`'s contract, so `rwb-decision` can route an approval and can accept or refuse an approver without ever holding a limit row.

This story meets REQ-APD-001, REQ-APD-003, REQ-APD-004, REQ-APD-005, REQ-APD-007, REQ-APD-008, REQ-APD-009, REQ-APD-010 and REQ-APD-011 on the delegation side: the level, the delegation row and the version that routed a decision are the level, the row and the version that the lookup answered, and the authority check is the A letter in the decision's capability area plus the holder, the substitute or the route role. It puts controls CTL-04, CTL-05 and CTL-07 within reach of `rwb-decision` and supports the measure decisions within the delegation of authority: target 100 percent.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P7-E2013-CON | The published approval contract: the approval resource with its level, limit version and status, the approver-authority request the router sends to `rwb-access`, and the contract fakes. The routing behaviour, the approval record and the endpoints are that contract's and that story's |
| RWB-P4-E1038-APP (same service, its own story) | The `delegation_limit` table, its migration, the load of version DOA-2026.11 with 218 rows (109 MORTGAGE and 109 SSME), the approval of a version and its rollback. This story reads the table; it creates no row and no version |
| RWB-P4-E1037-CON (same service, its own contract story) | The authorise contract, the role and permission tables behind the A letter, and the ADR refusal shape with MSG-P4-002. This story adds the DoA sub-check to that operation; it adds no path |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the access-log entry of every lookup and every decision |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06), for the route role parameter of a decision with no amount limit; read by `rwb-decision`, not by this story |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the reference-data contract of `rwb-case` (DP-07): LOV-APPROVAL-LEVEL, LOV-PRODUCT, LOV-CAPABILITY and LOV-DECISION with the version in force |
| RWB-PLT-E1037-CON | The guard library that carries this service's authorise answer to the other services (DP-08) |
| RWB-PLT-TE006-CON | The outbox and inbox library with CloudEvents (DP-09) |
| RWB-PLT-E1071-CON | The workflow kit in namespace `rwb-recovery` (DP-10); this story starts no workflow, and `ApprovalWorkflow` runs on `rwb-decision` |
| RWB-PLT-E1044-CON | The per-service Flyway sequence and migration conventions (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19); no screen of this story is served through it |

Business preconditions carried from RWB-E2-013:

- Delegation version DOA-2026.11 is in force and the lookup returns the lowest covering level (legacy RWB-E1-038); holders and substitutes are named test users in SIT and UAT (DL18).
- Item 2.1.1 at level L4 is two rows: principal 300,000,000.00 with loss up to 45.00 percent and maximum loss 150,000,000.00, and principal 50,000,000.00 with no loss limit.
- The delegation levels are L1 to L6, Board of Directors to Recovery executive, department level, per the delegation of authority matrix.
- Approval route parameters exist for each decision with no amount limit; for D7.1 notices `rwb.approval.route.D7.1.role`=RW-LITOFF. Under the R-PREC default ruling these are parameter rows of `rwb-case`, read by `rwb-decision` through the parameters contract of DP-06; this story does not own them, and it answers `NO_AMOUNT_LIMIT` without a level and without a role.
- The scope of the `rwb-decision` service identity inside `rwb-access` (which rights it holds, and in which areas) is Not specified in the source documents (GAP-0930; ASM-1654).

### 4. Flow

1. `rwb-decision` (P7), in `ApprovalWorkflow` or in its routing service, reads the decision, the regulation item, the product group, the amounts (`principal`, `lossPct`, `lossAmount`, `pricePctFmv`), the related-party flag and the routing date, and calls `GET /api/recovery/access/v1/doa-limits` on `rwb-access` with `decisionCode`, `regulationItem`, `productGroup`, `principal`, `lossPct`, `lossAmount`, `pricePctFmv`, `relatedParty` and `onDate`.
2. `DoaLimitController` validates the query: `decisionCode`, `regulationItem`, `productGroup` and `onDate` are required; an empty one is 422 with MSG-GEN-001 naming the field; an unknown product group or approval level is 422 against the reference lists of DP-07, which are read with the version in force and never written in code.
3. `DoaLimitLookupService` resolves the delegation version in force on `onDate`: the rows whose `valid_from` is not after the date and whose `valid_to` is empty or not before it. Several versions may be readable at once; exactly one is in force for the date asked.
4. The service selects the lowest covering row of the decision and the regulation item for the product group: the row whose `principal_limit` is not below the principal, or is empty, and whose `loss_pct_limit` is not below the loss percentage, or is empty, and whose `max_loss_amount` is not below the loss amount, or is empty, and whose `min_price_pct_fmv` is not above the sale price percentage, or is empty. The level of that row is the answer. Where the related-party flag is true and the decision carries the related-party condition, the L1 row is the answer.
5. The service answers `COVERED` with `level`, `delegationLimitId`, `limitVersion`, `holderUserId` and `substituteUserId`. The row and the version are answered together, so the caller can write both against the approval and keep them after a later version is approved (BR1).
6. Where the covering row has neither `holder_user_id` nor `substitute_user_id`, the service answers the next level up at once, with outcome `NO_HOLDER`, and records the level that was skipped for want of a holder (BR8). No caller ever receives a level with nobody on it.
7. Where no row of the version covers the decision and the product, the service answers `NOT_COVERED` with no level, no row and no holder (BR11). The hold of the item, the case status and the incident with MSG-P7-010 are `rwb-decision`'s.
8. Where the decision carries no amount limit (D7.1 notices and the other decisions of the same kind), the service answers `NO_AMOUNT_LIMIT` with no level, no row and no holder (BR2). The route role comes from the parameter rows of `rwb-case`, which `rwb-decision` reads; this story neither holds nor returns it.
9. Authority decision, behind the existing `POST /api/recovery/access/v1/authorise` with the DoA check in the request: the handler resolves the calling role and the person references, reads the permission row of the caller's role in the decision's capability area (LOV-CAPABILITY), and answers that the caller holds the A letter (BR3). Where the caller holds A, the handler compares the caller's level, or the caller as the holder or substitute of the required level, or the caller's route role, with the required level that `rwb-decision` named. A caller with A at the required level, as its substitute, or holding the route role, is allowed.
10. Authority decision, refusals: a caller without the A letter in the area is refused with 403 and MSG-P4-002; a caller with A but a level below the required level is refused with 403 carrying `requiredLevel`, and `rwb-decision` returns MSG-P7-001 to the approver, so the level is named and no silent approval is possible (BR3, AC8).
11. Every lookup and every authority decision appends one entry to the access log before the answer leaves the service: a decision-record entry of the local library of DP-03 with the decision code (`AC-READ` for an answered lookup or an allowed authority decision and `AC-DENY` for a refusal), the caller reference, the version read, the level answered or the reason refused, and the time. The entry carries no name, no e-mail address and no personal field (BR13).
12. Where the record cannot be written the answer is not returned: the call fails with 503 and MSG-P7-003 and nothing is answered, because an access-log entry that is missing cannot be reconstructed later (legacy RWB-E1-039; FSD P4 v3 A2.7).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A required query field is empty | 422, no lookup is made and no record is written | MSG-GEN-001 | AC1 |
| X2 | A product group, approval level or decision code is not in the reference lists | 422 naming the field, nothing answered | MSG-GEN-001 | AC1 |
| X3 | No row of the version in force covers the decision and the product | `NOT_COVERED`, no level, no row, no holder; the hold and the incident are `rwb-decision`'s | MSG-P7-010 (produced by `rwb-decision`) | AC4 |
| X4 | The decision carries no amount limit | `NO_AMOUNT_LIMIT`, no level, no row, no holder; the route role is `rwb-case`'s parameter | None | AC6 |
| X5 | The covering row has no holder and no substitute | The next level up is answered at once with `NO_HOLDER`, so no caller waits on nobody | MSG-P7-011 (produced by `rwb-decision`) | AC3 |
| X6 | The caller holds no A letter in the decision's capability area | 403, no authority granted, one refusal entry with decision code "AC-DENY" | MSG-P4-002 | AC7 |
| X7 | The caller holds A but a level below the required level | 403 carrying `requiredLevel`; `rwb-decision` tells the approver the level and sends the item there | MSG-P7-001 (produced by `rwb-decision`) | AC8 |
| X8 | The request names a required level that no row of the version in force holds | `NOT_COVERED` is not assumed: the answer names the level and no holder, and the test fails loudly rather than granting authority | None | AC3, AC8 |
| X9 | The decision record cannot be written | 503 and no answer; the lookup and the decision are not given | MSG-P7-003 | AC9 |
| X10 | The same lookup arrives twice with the same parameters | Both are answered; each writes its own access-log entry, because a read is an event and not a state change | None | AC9 |

No exception path of this story changes an approval, a case or a task: this service answers and records, and the state machine is `rwb-decision`'s and `rwb-case`'s.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the approval contract of RWB-P7-E2013-CON and the fakes; the `delegation_limit` table and the SIT fixture DOA-2026.11 are RWB-P4-E1038-APP's, and the read-only repository is the only coupling |
| Negotiable | Levels, limits, holders, substitutes, product groups, regulation items and versions are rows; the lists are reference data; no value is fixed in this story |
| Valuable | One lookup and one authority decision replace a per-screen copy of the table and a guard that every module re-implemented |
| Estimable | One read endpoint, one extended operation behind the existing authorise path, one repository, one record appender, one contract-fake run |
| Small | Fits two weeks with its tests; there is no screen, no workflow and no migration of its own |
| Testable | Each owned criterion has a test case in section 16, and the approval side is stubbed in the contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Approval routing with the delegation of authority table

  Background:
    Given the environment is SIT
    Given delegation version "DOA-2026.11" is in force from 30 November 2026 with 218 rows, 109 for MORTGAGE and 109 for SSME
    Given test holder "U-9201" holds level "L6" for MORTGAGE, "U-9202" holds "L5" and "U-9203" holds "L4", all holding RW-PRODHEAD with the A letter in Treatment and offer
    Given test user "U-9205" is the substitute of "U-9201"

  Scenario: AC1 The lookup answers the lowest covering level (new, D-RCV-60)
    Given decision D6.4 carries regulation item "2.1.1" and product group "MORTGAGE"
    When the rwb-decision service identity calls GET /api/recovery/access/v1/doa-limits with decisionCode "D6.4", regulationItem "2.1.1", productGroup "MORTGAGE", principal 2,400,000.00, lossPct 20.00, lossAmount 480,000.00 and onDate 15 December 2026
    Then the response is 200 with level "L6", limitVersion "DOA-2026.11", holderUserId "U-9201", substituteUserId "U-9205" and outcome "COVERED"
    Then delegationLimitId is the id of the item 2.1.1 row at L6 that the version holds
    Then one decision-record entry is written with decision code "AC-READ", the row, the version and the level, and no personal data

  Scenario: AC2 An item keeps the delegation version it was routed under (new, D-RCV-60)
    Given delegation version "DOA-2026.11" is in force until 31 December 2026 and version "DOA-2027.01" is in force from 1 January 2027 and moves that amount for D6.4 item 2.1.1 MORTGAGE to "L5"
    When the lookup is asked for the same amounts on 2 January 2027
    Then the response names level "L5", holder "U-9202" and limitVersion "DOA-2027.01"
    Then a lookup for the same amounts on 15 December 2026 still names level "L6" and "DOA-2026.11"
    Then the rows of "DOA-2026.11" stay readable with valid_to 31 December 2026, and an item routed under "DOA-2026.11" keeps that version in its approval record

  Scenario: AC3 A level with no holder passes the item one level up (new, D-RCV-60)
    Given the L6 row for SSME has no holder and no substitute
    Given the rwb-decision contract mock returns approval "A-2" for D6.4 item 2.1.1, SSME, principal 1,000,000.00, loss 10.00 percent routed to the L5 holder at once
    When the lookup is asked for D6.4 item 2.1.1, SSME, principal 1,000,000.00 and lossPct 10.00 on 15 December 2026
    Then the response is 200 with level "L5", the L5 delegationLimitId, limitVersion "DOA-2026.11", the L5 holder and outcome "NO_HOLDER"
    Then the entry records that L6 was skipped because it has no holder and no substitute, and no caller receives L6

  Scenario: AC4 A product that no row covers is not covered (new, D-RCV-60)
    Given "DOA-2026.11" holds no row for product group "HIRE_PURCHASE"
    Given the rwb-decision contract mock returns approval "A-3" for D6.4 item 2.1.1, HIRE_PURCHASE, principal 900,000.00 held with no limit
    When the lookup is asked for D6.4 item 2.1.1, HIRE_PURCHASE and principal 900,000.00 on 15 December 2026
    Then the response is 200 with outcome "NOT_COVERED" and no level, no delegationLimitId and no holderUserId
    Then the hold of the item, the case status and the incident with MSG-P7-010 are not produced here

  Scenario: AC5 A related-party write-off answers the Board level (new, D-RCV-60)
    Given "DOA-2026.11" is in force with a row for decision D9.2, regulation item "2.1.10", product group "SSME" at level "L1"
    When the lookup is asked for D9.2 item 2.1.10, SSME, principal 300,000.00 and relatedParty true on 15 December 2026
    Then the response is 200 with level "L1" and outcome "RELATED_PARTY"
    Then the entry records the related-party flag, the item and the version, and no name

  Scenario: AC6 A decision with no amount limit answers no level (new, D-RCV-60)
    Given decision D7.1 has no amount limit and its route role "RW-LITOFF" is the parameter row "rwb.approval.route.D7.1.role" of rwb-case, which this story does not own
    Given the rwb-decision contract mock returns approval "A-1" for case "RW-2026-000123" with decision D7.1, area "LITIGATION", route role RW-LITOFF and due at 09:00 on 15 December 2026
    When the lookup is asked for D7.1 with no principal, no loss and no price on 14 December 2026
    Then the response is 200 with outcome "NO_AMOUNT_LIMIT" and no level, no delegationLimitId and no holderUserId
    Then no route role and no capability area is answered by this lookup

  Scenario: AC7 A caller without the A letter is refused (new, D-RCV-60)
    Given test user "U-9210" holds RW-RESTRUCT and holds no A letter in the capability area "LITIGATION"
    When "U-9210" is checked through POST /api/recovery/access/v1/authorise for decision D7.1, area "LITIGATION" and route role RW-LITOFF
    Then the response is 403 with message MSG-P4-002 and no authority is granted
    Then one entry is written with decision code "AC-DENY", user reference "U-9210", area "LITIGATION" and right "A"

  Scenario: AC8 A caller below the required level is refused with the level (new, D-RCV-60)
    Given test user "U-9203" holds the A letter in Treatment and offer and is the holder of "L4" for MORTGAGE
    Given the rwb-decision contract mock returns approval "A-4" for D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00 with required level "L6"
    When "U-9203" is checked through POST /api/recovery/access/v1/authorise for approval "A-4" at the required level "L6"
    Then the authorise answer refuses with authorised false, requiredLevel "L6" and no authority granted
    Then rwb-decision turns that refusal into its 403 with MSG-P7-001 for the approver
    Then one entry is written with decision code "AC-DENY", the required level and the level the caller holds

  Scenario: AC9 Every lookup and decision writes one access-log entry (new, D-RCV-60)
    Given the decision-record store is available and its hash chain verifies
    When one lookup and one authority decision complete
    Then two decision-record entries are appended, each with the decision code, the caller reference, the version read, the outcome and the time
    Then neither entry carries a name, an e-mail address or any personal field, and each is appended before the answer is returned
    Then when the record cannot be written the call returns 503 with message MSG-P7-003 and no answer
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A decision with delegation rows routes to the lowest level whose row covers it on the routing date; the item keeps that delegation version | REQ-APD-001; REQ-APD-010; RWB-E1-038; Delegation of authority matrix, rule 9 |
| BR2 | A decision with no amount limit is answered with no level by the lookup; the route role named in its route parameters decides it | Parameters rwb.approval.route.*; DL22 |
| BR3 | The approver must hold the A letter in the decision's capability area and be the holder or substitute of the required level, or hold the route role | Permission matrix; Key sheet: A works within the delegation table; CTL-04 |
| BR8 | A level with no holder and no substitute passes the item one level up at once | REQ-APD-011 |
| BR9 | Levels L1 to L3 are committee levels; the lookup answers the level and its recording holder, and the resolution, its reference and the members present are recorded in `rwb-decision` | REQ-APD-008; doa.txt, Levels sheet |
| BR11 | A decision that no limit covers is answered `NOT_COVERED`; the hold of the item and the incident are `rwb-decision`'s | Delegation of authority matrix, rule 8 |
| BR13 | Every lookup and every authority decision appends one access-log entry in the same transaction as the answer, with no personal data; an answer that cannot be recorded is not returned | Principle 5; R-UNI-39; FSD P4 v3 A2.7 |
| BR14 | No business value in code: levels, limits, holders, substitutes, product groups, regulation items and versions are rows of `delegation_limit`, and the lists are reference data with a version | BR-P4-006; FSD P4 v3 A2.6 |

Target-service statements that make the rules hold in `rwb-access`:

- BR4, BR5, BR6, BR7, BR10 and BR12 of the legacy story are executed in `rwb-decision` on the answer this service gives: the preparer rule, the message above the limit, the reason rules, the escalation, the limit and version written with every approval, and the record of the outcome. This story owns the lookup and the authority answer only.

- BR1 and BR11 are one query over `delegation_limit` with the date and the amounts as predicates; the version is a column of the row, so the answer cannot name a row and a version that do not belong together.
- BR2 is the absence of a delegation row for the decision code: the lookup does not invent a level, and it does not read the `rwb-case` parameter that names the route role, because that parameter is another service's.
- BR3 is the permission row of the caller's role in the decision's capability area plus the level comparison; the request carries the required level or the route role from `rwb-decision`, so the decision is made against the level that will actually approve.
- BR8 is a second pass of the same query, from the level above the covering row, when the covering row has no holder and no substitute.
- BR9 is the level value alone: the committee's resolution and members present are approvals of `rwb-decision`, and this service answers the level and its recording holder.
- BR13 is the record appender of DP-03 inside the transaction that produces the answer; there is no separate access-log table in `rwb_access`, so the access log and the decision log are queried together (legacy FEAT-ACA-08).
- BR14 is checked by test: a new level, product group or regulation item is a row and a list value, and the build changes nothing.

### 9. State transitions

This service holds no case, task or approval state. The states it answers are the outcomes of a lookup and of an authority decision, and the lifecycle of a delegation version, which RWB-P4-E1038-APP writes.

| From | Event | Condition | To |
|---|---|---|---|
| Version in force | Lookup with `onDate` inside `valid_from` to `valid_to` | A row covers the decision, the product and the amounts | Version answered, outcome `COVERED` |
| Version in force | Lookup, covering row with no holder and no substitute | The next level up has a holder | Version answered, outcome `NO_HOLDER` |
| Version in force | Lookup, related-party flag true | The version holds the related-party row | Version answered, outcome `RELATED_PARTY` |
| Version in force | Lookup, no row for the product | None | Outcome `NOT_COVERED`, no level |
| Version in force | Lookup, decision with no amount limit | None | Outcome `NO_AMOUNT_LIMIT`, no level |
| Version in force | A new version is approved and becomes in force on a later date | A lookup is dated on or after that date | The new version answers; the older version stays readable for its own dates |
| Routed item | A new version is approved | The item was routed before | The item keeps its level and version; a new lookup answers with the new version |

| Command | Condition | Outcome |
|---|---|---|
| Authority decision | A letter in the area, and the caller is the holder or substitute of the required level, or holds the route role | `AUTHORISED`, one access-log entry with decision code "AC-READ" |
| Authority decision | No A letter in the area | `REFUSED` 403, MSG-P4-002, one entry with decision code "AC-DENY" |
| Authority decision | A letter in the area, and the caller's level is below the required level | `REFUSED` 403 with `requiredLevel`, MSG-P7-001 at the caller, one entry with decision code "AC-DENY" |

The approval record moves WAITING to APPROVED, REFUSED, RETURNED or to the next level on escalation in `rwb-decision`; this story holds no copy of it and changes no state of it.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The `rwb-decision` service identity | Call `GET /api/recovery/access/v1/doa-limits` with the Approval check R right, and pass the required level or route role to the authority decision. The exact scope of this identity is Not specified in the source documents (GAP-0930; ASM-1654) |
| The service identities of the other services | Call the authority decision behind `POST /api/recovery/access/v1/authorise` under their own cached permission read (DP-08), as the guard library already does |
| Holders and substitutes of levels L1 to L6 | Are answered as holders or substitutes of the required level; they do not read the table directly |
| Route roles, for example RW-LITOFF for D7.1 | Are accepted for an item that carries no amount limit, because the route role is the authority for that item |
| RW-COE, RW-RISK, RW-REFADM, RW-SECADM | Load, approve, roll back and administer the delegation versions in RWB-P4-E1038-APP; this story gives them no write path |
| RW-AUDIT | Reads the access-log entries through the decision log of `rwb-decision`; it calls no operation of this story |
| `rwb-access` itself | Reads `delegation_limit`, `role` and `permission` in its own schema and writes no row of them in this story |

The refusal shape is 403 with an RFC 9457 problem response and `messageId` set, MSG-P4-002 for an absent right and MSG-P7-001, with `requiredLevel` set, for an insufficient level. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-E1037-CON.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-016 | `delegation_limit` | id | Read |
| DF-REF-017 | `delegation_limit` | decision_code | Read |
| DF-REF-018 | `delegation_limit` | approval_level | Read |
| DF-REF-019 | `delegation_limit` | product_group | Read |
| DF-REF-020 | `delegation_limit` | principal_limit | Read |
| DF-REF-021 | `delegation_limit` | loss_pct_limit | Read |
| DF-REF-022 | `delegation_limit` | min_price_pct_fmv | Read |
| DF-REF-023 | `delegation_limit` | holder_user_id | Read |
| DF-REF-024 | `delegation_limit` | substitute_user_id | Read |
| DF-REF-025 | `delegation_limit` | valid_from | Read |
| DF-REF-026 | `delegation_limit` | valid_to | Read |
| DF-REF-055 | `delegation_limit` | limit_version | Read |
| DF-REF-056 | `delegation_limit` | regulation_item | Read |
| DF-REF-057 | `delegation_limit` | applies_when | Read |
| DF-REF-058 | `delegation_limit` | max_loss_amount | Read |
| DF-REF-059 | `delegation_limit` | max_delay_count | Read |
| DF-REF-060 | `delegation_limit` | min_price_pct_principal | Read |
| DF-REF-061 | `delegation_limit` | min_received_pct | Read |
| DF-REF-062 | `delegation_limit` | max_term_years | Read |
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read |
| DF-REF-159 to DF-REF-184 | `reference_version`, `reference_row` of `rwb-case` | LOV-APPROVAL-LEVEL, LOV-PRODUCT, LOV-CAPABILITY and LOV-DECISION versions in force | Read through the reference-data contract |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the access-log entry of a lookup and of a decision | Write |
| (outbox) | outbox library table in `rwb_access` | the record row and the `AccessPolicyChanged` row | Write |
| (inbox) | `processed_event` | none: this story consumes no event | None |

No row of `delegation_limit` is written in this story: the table, its load and its versions are RWB-P4-E1038-APP's. No row of `approval`, `decision_log_entry`, `case` or `task` is read or written: `approval` and `decision_log_entry` are `rwb-decision`'s (P7) and the case and its task are `rwb-case`'s (P3), and their fields DF-DEC-032 to DF-DEC-053 arrive in the approval contract, not by a schema read (DP-01). Field IDs are those in the Logical Data Model and Data Dictionary v9; `lov_value` is reference data of P3 under the ownership ruling and is read through DP-07, not from `rwb_access`.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| GET | `/api/recovery/access/v1/doa-limits` | P4 `rwb-access` | Query: `decisionCode`, `regulationItem`, `productGroup`, `principal`, `lossPct`, `lossAmount`, `pricePctFmv`, `relatedParty`, `onDate` | `level`, `delegationLimitId`, `limitVersion`, `holderUserId`, `substituteUserId`, `outcome` (COVERED, NO_HOLDER, NOT_COVERED, NO_AMOUNT_LIMIT, RELATED_PARTY) | 401; 403 Approval check R (MSG-P4-002); 422 missing or unknown query field (MSG-GEN-001); 503 record not written (MSG-P7-003) | Approval check R, for the `rwb-decision` service identity and the other service identities that route an approval | Not applicable, read only; no Idempotency-Key |

The operation is the one that Architecture v5 slide 14 names for `rwb-access` (`GET /doa-limits`) under the base `/api/recovery/access/v1` of DP-13. It is absent from Recovery Workbench API Specification v4, which is the lower-precedence document and is corrected by this story's contract (GAP-0928; ASM-1652). Its request and response field set is Not specified in the source documents (GAP-0929; ASM-1653): the fields above are the ones this story needs, and the contract review confirms or renames them before the endpoint is frozen.

The authority decision is not a new path. It sits behind the existing `POST /api/recovery/access/v1/authorise` of RWB-P4-E1037-CON, whose request already carries role, scope and DoA, and it adds the DoA part of the answer: `requiredLevel`, `routeRole`, `decisionCode` and the amounts in the request, and `authorised`, `requiredLevel` and `outcome` in the answer. That operation and the existing `GET /api/recovery/access/v1/me/permissions` and the masking-policies read are the service baseline's, and this story changes no other operation.

#### 12.2 REST operations consumed

None. This story calls no REST operation. The parameter rows that name a route role are read in process through the client library of DP-06 and the reference lists through the client library of DP-07, and the approval facts arrive in the request of `rwb-decision`, not by a call back to it.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 | roleCode or limitVersion | the changed policy reference: the table, the version and the change kind, with no personal data |
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | the hash-chained access-log entry of a lookup or of an authority decision |

CloudEvents 1.0 envelope; neither payload carries a name, an e-mail address or a personal field. The event `rwb.access.DoaLimitChanged.v1` is not published by this story: the DoA table itself is loaded, approved and rolled back by RWB-P4-E1038-APP, and that story publishes the change of a delegation version. The access-log entry is the decision-record entry of DP-03 (ASM-1655), so the access log and the decision log are the same append-only chain.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 (events: none), and this story adds no subscription. The permission caches that other services refresh on `rwb.access.AccessPolicyChanged.v1` are their concern, not this story's.

#### 12.5 Workflows and activities

None. `ApprovalWorkflow` of the workflow kit stays in `rwb-decision` and is template RWB-P7-E2013-APP's; this story starts no workflow, signals no workflow and registers no activity on the `rwb-access` queue. The queue `rwb-access` exists for the service's Schedule work, and the six-monthly access review list (JOB-18) is not part of this story.

#### 12.6 Schedules

None for this story. The six-monthly access review list (JOB-18) is a Schedule of `rwb-access` and belongs to the service's own story, not to the delegation lookup.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `delegation_limit` | P4 (`rwb_access`) | Read only: the version in force, the covering row, the holder and the substitute. Created and loaded by RWB-P4-E1038-APP |
| `role` | P4 (`rwb_access`) | Read only: the caller's role and its class |
| `permission` | P4 (`rwb_access`) | Read only: the A letter of the caller's role in the decision's capability area |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | The outbox row of the record and of `AccessPolicyChanged`; no inbox row is written because no event is consumed (DP-09) |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written: the central ledger entry is `rwb-decision`'s and the local record goes on `rwb.decision-record.v1` |

`lov_value` and the reference tables are reference data of P3 under the ownership ruling and are read through DP-07; no table of another service is read and no foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-decision approval WireMock | RWB-P7-E2013-CON | Approval "A-1" of AC6 with decision D7.1, area LITIGATION, route role RW-LITOFF and due 09:00 on 15 December 2026; approval "A-2" of AC3 routed to L5 with reason NO_HOLDER; approval "A-3" of AC4 held with no limit; approval "A-4" of AC8 with required level L6 |
| decision-record fake | RWB-PLT-E1027-CON | The record append, the hash chain check and the forced failure of AC9 |
| authorise and guard fake | RWB-PLT-E1037-CON, RWB-P4-E1037-CON | The permission answer behind the A letter, including the refusal for a role without it |
| reference-data fake | RWB-P3-E1043-CON | LOV-APPROVAL-LEVEL (L1 to L6), LOV-PRODUCT (MORTGAGE, SSME, HIRE_PURCHASE), LOV-CAPABILITY and LOV-DECISION with their versions |
| parameters fake | RWB-P3-E1042-CON | The route parameter row `rwb.approval.route.D7.1.role`=RW-LITOFF, read by `rwb-decision`, so AC6 can prove that this lookup answers no role |
| delegation fixture | RWB-P4-E1038-APP | DOA-2026.11 with 218 rows, its two item 2.1.1 L4 rows, the SSME L6 row with no holder and the D9.2 item 2.1.10 L1 row; and DOA-2027.01 for AC2 |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 1 new (`GET /doa-limits`), plus the DoA part of the existing `POST /authorise`; consumed 0 | Base `/api/recovery/access/v1` |
| Kafka | Published 2 event types; consumed 0 | `rwb.access.events.v1` and `rwb.decision-record.v1` |
| Temporal | 0 workflows, 0 activities | `ApprovalWorkflow` and the escalation timer are `rwb-decision`'s |
| File | None | No file input or output |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/doa`, Java package `th.co.scb.ace.workbench.recovery.access.doa`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the in-process `DelegationOfAuthority.lowestLevel` call (DP-11: a REST contract with a mock, one hop and a 2 s timeout, with the caller caching the answer) and the `RecoveryAccessGuard` right check (DP-08: this service's own authorise contract). DP-10 and DP-19 are carried by the legacy key and their work sits with the P7 slice — `ApprovalWorkflow` and the escalation timer on `rwb-decision`, and the approval queue screen SCR-10 through gateway-bff. This story starts no workflow and serves no screen.

This secondary slice adds no new build dependency of its own (metadata "Depends on (build)" is None): the libraries, the per-service Flyway baseline, the workflow kit, the outbox and the gateway route are already build dependencies of the P4 service's own stories, in particular RWB-P4-E1037-CON and RWB-P4-E1038-APP, and this story builds against the published contracts and their fakes.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DoaLimitController | Controller | `GET /doa-limits`: query validation, error mapping to RFC 9457 problem responses, `requiredLevel` on a refused authority decision |
| DoaLimitLookupService | Service | Version in force for the date, lowest covering row, no-holder pass-up, related-party row, `NOT_COVERED` and `NO_AMOUNT_LIMIT` outcomes |
| DoaAuthorityService | Service | BR3: the A letter in the decision's capability area, the holder, the substitute and the route role; the refusal with the required level |
| DoaLimitRepository | Repository | Read-only queries over `delegation_limit` in schema `rwb_access`, with the date window and the amount predicates; no write method |
| PermissionReader | Service | The `role` and `permission` rows of the caller, and the decision's capability area, in the same schema |
| LevelCatalog | Service | LOV-APPROVAL-LEVEL, LOV-PRODUCT, LOV-CAPABILITY and LOV-DECISION through the reference-data contract of DP-07; no Java enum of levels or products |
| AccessLogWriter | Service | The decision-record entry of a lookup and of a decision, in the transaction that produces the answer, with the outbox row (DP-03, DP-09) |

**Database and migrations**

- This story creates no table and owns no Flyway version of its own. `delegation_limit`, `role` and `permission` are created, indexed and loaded by RWB-P4-E1038-APP and RWB-P4-E1037-CON in the per-service sequence of DP-15, and this story reads them through the repository.
- The read predicates are `decision_code`, `regulation_item`, `product_group`, `approval_level`, the four amount columns and the `valid_from`/`valid_to` window. If the SIT query plan needs an index that the creating story does not have, the index is added to that story's migration, not to a new one here.
- No write statement exists in the repository: the class exposes no save, update or delete, so a lookup can never change a limit row.
- The outbox row and the record row commit in one transaction with nothing else to write; a failure rolls them back and the answer is not returned (MSG-P7-003).

**Configuration and reference data**

- LOV-APPROVAL-LEVEL (`L1` to `L6`), LOV-PRODUCT (`MORTGAGE`, `SSME`, `HIRE_PURCHASE` and the other groups the file carries), LOV-CAPABILITY and LOV-DECISION are read through the reference-data contract of DP-07 with the version in force (RWB-P3-E1043-CON); no level, product group or capability area is a constant in code.
- The route role parameter of a decision with no amount limit (`rwb.approval.route.<code>.role`) is a parameter row of `rwb-case`, read by `rwb-decision` through DP-06. This story neither reads it nor holds a default.
- The delegation versions, their rows, holders and substitutes are rows of `delegation_limit` in `rwb_access`; DOA-2026.11 is the version in force in SIT and is loaded by RWB-P4-E1038-APP.

**Build steps**

1. `DoaLimitRepository` with the read-only queries and the date window; test that the lowest covering row is the answer for the D6.4 case of AC1 and that the repository has no write method.
2. `DoaLimitLookupService`: `COVERED`, `NO_HOLDER`, `RELATED_PARTY`, `NOT_COVERED` and `NO_AMOUNT_LIMIT`; tests for AC1, AC3, AC4, AC5 and AC6.
3. `LevelCatalog` over the reference-data contract; test that a new level or product group value is accepted as data with no code change (BR14).
4. Version resolution and the two-version test of AC2 on a fixed clock: the date decides the version, and the older rows stay readable.
5. `DoaAuthorityService` behind the existing authorise path: the A letter, the level comparison, the substitute and the route role; tests for AC7 and AC8, including the `requiredLevel` in the refusal.
6. `AccessLogWriter` with the record append and the outbox row in one transaction; tests for AC9 and for the 503 when the record cannot be written.
7. The contract-fake run of the lookup and of the authority decision in isolation, so the story builds before the approval story exists in the environment.
8. The denial test through the guard library for a role without Approval check R, and the service-identity test of s10.

**Feature switch.** The lookup is a read path and carries no switch of its own. The DoA table's release and rollback are controlled by RWB-P4-E1038-APP through its versioned rows and approval, and the service-level feature flag of RWB-P4-E1037-CON governs the service baseline; this story adds no flag and removes nothing when a limit row is rolled back, because the lookup always answers the version in force.

**Done when.** The tests in section 16 pass; the lookup answers level, row and version for the D6.4 case of AC1 in SIT; a level with no holder passes up with `NO_HOLDER`; `HIRE_PURCHASE` answers `NOT_COVERED`; a D7.1 notice answers `NO_AMOUNT_LIMIT` with no level; a caller without the A letter is refused with MSG-P4-002 and a caller below the level is refused with the required level; and every lookup and every decision leaves one access-log entry in the decision record chain.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-GEN-001 | A required query field is empty or a code is not in its list | Enter {field}. | This story, on the lookup |
| MSG-P4-002 | The caller holds no A letter in the decision's capability area, or no Approval check R | You cannot {action} here. Your role does not include it. | This story, on the authority decision |
| MSG-P7-001 | The caller holds A but a level below the required level | This needs approval at level {level}. It has been sent to {approver}. | This story returns the 403 with `requiredLevel`; `rwb-decision` returns the text to the approver |
| MSG-P7-003 | The access-log entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the lookup and on the decision |
| MSG-P7-010 | No limit covers the decision and product | No approval limit covers {decision} for {product}. The item is held and Risk has been told. | `rwb-decision`, from this story's `NOT_COVERED` answer |
| MSG-P7-011 | A level passed the item up for want of a holder | {decision} on case {caseNo} passed its service level and is now with you for approval. | `rwb-decision`, from this story's `NO_HOLDER` answer |

Every error from this service is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. The 403 of an insufficient level also carries `requiredLevel`, so the caller can name the level without a second lookup.

### 15. Screens and states

No screen is built in this story. The lookup and the authority decision are consumed by `rwb-decision` and by the other services' guards; the screens that show their answers belong to other stories.

| Screen | State | Where it is |
|---|---|---|
| SCR-10 Approval queue | Loading, list, empty | `rwb-decision` (RWB-P7-E2013-APP); shows the level and the limit version this lookup answered |
| DoA table load and approval | Loaded, approved, rolled back | `rwb-access` (RWB-P4-E1038-APP) |
| Access audit query | List over a period | `rwb-access` (legacy RWB-E1-039; the access-log story) |

The gateway-bff composite route of DP-19 is not used by this story: no screen calls the lookup directly, and the approver's screen calls `rwb-decision`, which calls this service in one hop with a 2 s timeout and caches the answer.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-013-01 | AC6, BR2 | Component | Synthetic demand notice under R-LIT-03 with no amount limit |
| TC-E2-013-02 | AC2, AC8, BR1 | Contract | Approval timer breached at 09:00 next day; the escalation re-checks the new level on the same version |
| TC-E2-013-03 | AC2, BR1 | Contract | Delegation versions DOA-2026.11 and DOA-2027.01 |
| TC-E2-013-04 | AC1, AC5, BR1 | Component | D6.4 Mortgage at 2.4 million baht, and the related-party write-off that answers L1 with reason RELATED_PARTY |
| TC-E2-013-05 | AC1, AC7, BR3 | Component | L6 holder approving |
| TC-E2-013-06 | AC7, BR3 | Contract | Preparer who is also a substitute; the preparer check is the contract fake's and the A check is this story's |
| TC-E2-013-07 | AC8, BR3 | Component | Principal changed to 120 million baht, answered at L5 |
| TC-E2-013-08 | AC8, BR3 | Contract | Refuse without and with a reason; the reason rule is the contract fake's |
| TC-E2-013-09 | AC8, BR3 | Contract | Return with a question; the return rule is the contract fake's |
| TC-E2-013-10 | AC8, BR3 | Contract | Change without a reason code; the coded-reason rule is the contract fake's |
| TC-E2-013-11 | AC3, BR8 | Component | SSME L6 row with no holder |
| TC-E2-013-12 | AC1, BR9 | Component | L3 committee level with its recording holder; resolution PARC-2026-14 is recorded in rwb-decision |
| TC-E2-013-13 | AC1, BR3 | Contract | Holder and substitute at once; one authority answer each, the winner is rwb-decision's |
| TC-E2-013-14 | AC4, BR11 | Component | Hire purchase with no delegation rows |
| TC-E2-013-15 | AC7, BR3 | Component | A role without the right is refused with MSG-P4-002 |
| TC-E2-013-16 | AC9, BR13 | NFR | The decision-record write forced to fail during a lookup and during a decision |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to Component or Contract as the row shows, Access to Component and Resilience to NFR. The whole legacy set is kept because the DoA side of the key carries it; the tests whose rule lives in `rwb-decision` (preparer, refusal reason, return, coded reason, committee resolution, concurrency) use this story's authority answer and the contract fake for the rest. The ITG copy of the whole set is RWB-ITG-E2013-ITG and is not written here, so no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in code: levels, limits, holders, substitutes, product groups, regulation items and versions are rows of `delegation_limit`, and the lists are reference data with a version (BR14). A test proves that a new level or product group needs no build.
- No personal data anywhere: the lookup and the decision carry user references, decision codes, amounts and versions; the access-log entry and both event payloads carry no name, no e-mail address and no personal field, and no test data or prompt holds one.
- No read of another service's tables (DP-01): `approval` and `decision_log_entry` are `rwb-decision`'s, the case and its task are `rwb-case`'s, and no foreign key crosses a schema. The delegation table is read in `rwb_access` only.
- ACE data only through the owner's contract or its own `v_ace_*` views: this story reads no ACE data at all; the group-to-role mapping is `rwb-access`'s own concern in RWB-E1-022.
- One writer for a delegation version: only RWB-P4-E1038-APP writes `delegation_limit`. This story's repository has no write method, so a lookup cannot change a limit.
- No answer without its record: the access-log entry commits with the answer, and the answer is withheld with MSG-P7-003 when it cannot be written (BR13).
- The lookup is read-only and idempotent; the authority decision is a pure function of the rows, the lists and the request, so a retry answers the same and writes a second entry, as a read must.
- A refused caller learns the required level and nothing else: no limit amount, no holder and no substitute is returned in a refusal, so the refusal cannot be used to map the delegation table.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-APD-001 | Route to the approver named by the delegation table | Epic 2, 3.7 | FEAT-APD-01, FEAT-APD-10 | 17 Run the decision center | BR1, BR2 | TC-E2-013-01, TC-E2-013-04 |
| REQ-APD-003 | Accept, change, reject or return, each recorded | Epic 2, 3.7 | FEAT-APD-02, FEAT-APD-03, FEAT-APD-04 | 17 Run the decision center | BR3, BR13 | TC-E2-013-05, TC-E2-013-08, TC-E2-013-09 |
| REQ-APD-004 | Above the limit refused and raised, no silent approval | Epic 2, 3.7 | FEAT-APD-05 | 17 Run the decision center | BR3, BR8 | TC-E2-013-06, TC-E2-013-07 |
| REQ-APD-005 | Override needs a coded reason | Epic 2, 3.7 | FEAT-APD-07 | 17 Run the decision center | BR3, BR13 | TC-E2-013-10 |
| REQ-APD-007 | Unanswered approval escalates to the named role | Epic 2, 3.7 | FEAT-APD-06 | 17 Run the decision center | BR3, BR8 | TC-E2-013-02 |
| REQ-APD-008 | Committee decision recorded with members present | Epic 2, 3.7 | FEAT-APD-07 | 17 Run the decision center | BR9 | TC-E2-013-12 |
| REQ-APD-009 | Limit, rule version and approver written with every approval | Epic 2, 3.7 | FEAT-APD-11 | 17 Run the decision center | BR13, BR14 | TC-E2-013-05, TC-E2-013-13, TC-E2-013-16 |
| REQ-APD-010 | Open items keep the delegation version they were decided under | Epic 2, 3.7 | FEAT-APD-10 | 17 Run the decision center | BR1 | TC-E2-013-03, TC-E2-013-14 |
| REQ-APD-011 | Routing escalates rather than stalls with no person in a role | Epic 2, 3.7 | FEAT-APD-06 | 17 Run the decision center | BR8 | TC-E2-013-11 |

| Legacy reference | Where it is kept |
|---|---|
| Delegation version DOA-2026.11 with 218 rows, item 2.1.1 L4 as two rows, item 2.1.10 L1 on the related-party flag | Sections 3, 7, 12.8, 13 |
| Lowest covering level and the version kept with the item | Sections 4, 7, 8, 9 |
| No holder and no substitute passes one level up | Sections 4, 5, 7, 8 |
| No limit covers the decision; no amount limit routes to the route role | Sections 4, 5, 7, 8, 12.1 |
| A letter in the decision's capability area plus level or route role | Sections 4, 7, 8, 10 |
| MSG-P4-002, MSG-P7-001, MSG-P7-003, MSG-P7-010, MSG-P7-011, MSG-GEN-001 | Section 14, exception paths |
| Rule IDs R-UNI-39 and CTL-04, CTL-05, CTL-07 | Sections 2, 8, 17 |
| Legacy key RWB-E2-013, story RWB-P4-E2013-APP, contract RWB-P7-E2013-CON | Metadata, sections 3, 12 |
| Field IDs DF-REF-016 to DF-REF-062, DF-REF-034 to DF-REF-044 | Section 11 |

### 19. Out of scope

- The `rwb-decision` slices RWB-P7-E2013-APP and RWB-P7-E2013-CON: `ApprovalWorkflow`, the approval record, the approve, refuse and return endpoints, the approval queue SCR-10, the escalation and the central decision log entry.
- The `rwb-case` slice RWB-P3-E2013-APP: the case status `WAITING_APPROVAL`, the decision task and the service level timer projection on the case.
- The DoA table itself — its migration, its load of DOA-2026.11, the approval of a version and the rollback — under RWB-P4-E1038-APP. This story reads the table and publishes no `DoaLimitChanged`.
- The integration harness RWB-ITG-E2013-ITG and the `-ITG` copies of the test cases.
- The committee pack screen SCR-12 with each member's vote (Epic 4).
- The monthly override report (Epic 8, FEAT-ADM-08) and the reporting of approvals in `rwb-reporting`.
- The route role parameters and the capability area per decision code, which are `rwb-case` parameter rows under the R-PREC default ruling.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
