# RWB-P7-E6028-APP Sell a post charge-off population

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- Decision-record event type name corrected to `rwb.decision.DecisionRecorded.v1`; topic `rwb.decision-record.v1` unchanged (RD-P1-008).

| Item | Value |
|---|---|
| Story key | RWB-P7-E6028-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 4 |
| Business epic | EP06 |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P7-E6028-APP-14); confirm against the epic design record |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-028 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-P7-AQ |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P7-E6028-APP-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-S7-E6028-CON |
| Integration dependencies | None |
| Contract fake library version | Not specified in the source documents (DOR-RWB-P7-E6028-APP-22) |
| Contract version | Not specified in the source documents (DOR-RWB-P7-E6028-APP-23); the operations sit on the `/api/recovery/decision/v1` path |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-008 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E6-028 as the `rwb-decision` slice — the `approval` item of a write-off pack whose amount sits above the write-off committee limit and its routing level read from the delegation answer, the approve, return and refuse of that item, the registry rows of rules R-WO-12 and R-WO-32, and the central decision ledger entry of both rules with the two ledger reads. The scan, the pack, the committee, the posting and the sale itself stay with RWB-S7-E6028-APP and the debt sale route. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P7-E6028-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 21 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

### 1. Story

As a **product head (RW-PRODHEAD) chairing the credit approval committee with Risk**, I want **the write-off packs whose amount sits above the write-off committee limit to reach me as approval items at the delegation level the delegation answer gives, with the level, the delegation row and its version written on the item and on the decision record, and with my approve, return or refuse recorded once against the rule that routed the pack**, so that **no charged-off population can be sold on an authority the committee never held, and the bank can show afterwards which rule, which level and which limit version allowed each pack through**.

Inside `rwb-decision` this is the approval-and-record slice of the legacy story RWB-E6-028:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, shared topic `rwb.decision-record.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`.
- Three deliverables and nothing else. **First**, the `approval` row of a write-off pack whose limit is exceeded: raised by the write-off story of this key (RWB-S7-E6028-APP), routed here to the level the delegation answer names, and carried through the states of LOV-APPROVAL-STATUS, approved, returned or refused here. **Second**, the decision records of rule R-WO-12 and of rule R-WO-32: the routing record this service writes when it raises the item, and the central ledger entry of the write-off's own record of R-WO-12 (a case in PACK_PREPARED whose limit is exceeded routes to the credit approval committee and moves to ESCALATED_TO_CREDIT_COMMITTEE) and of R-WO-32 (a case in PLACEMENT_DECIDED with sale selected moves to SOLD_POST_CHARGEOFF), collected from `rwb.decision-record.v1` into `rwb_decision.decision_log_entry`, plus the two rule rows in the registry that make each entry's rule id and version resolvable. **Third**, the two reads `GET /approvals` and `GET /decision-log` under the Decision log right and the caller's scope.
- The routing level is read, never computed. The level, the delegation row and the version of the delegation table in force arrive in the answer of the P4 `rwb-access` delegation-limit contract on the business date, and this service stores them on the approval (`approval_level`, `delegation_limit_id`, `limit_version`) and on the record. No delegation row, no limit value, no DoA item and no role is copied into `rwb_decision` and no limit is re-computed here (DP-01; Ownership Map `delegation_limit` to P4).
- The records are written through the decision-record path of DP-03 and never through another service's table. The record, its chain link and the outbox row commit together or not at all (R-UNI-39), and no row of the ledger is ever updated or deleted (REQ-DRI-002).
- Not this story, stated once and meant everywhere below: the write-off scan and its population, the committee pack of three working days, the committee agenda and the meeting, the posting to ALS and the general ledger, the provision release, the finance feed and the debt-sale lot (RWB-S7-E6028-APP for the write-off half and S6 `rwb-debtsale` for the lot); the delegation table, the role model, the scope, the masking policy and the authorise answer (P4 `rwb-access`); the case status, the case read and the timers (P3 `rwb-case`); the screen SCR-27 Write-off proposal (RWB-S7-E6028-APP and the Epic 8 screen stories); and the cross-service proof of the whole journey (RWB-ITG-E6028-ITG).
- The database login used by the capability is the per-service login of DP-02. Its name is Not specified in the source documents (GAP-1311; ASM-2272); this story uses the phrase "the `rwb-decision` login (DP-02)" and never the shared monolith login.
- The legacy behaviour carried into the decision service is unchanged in substance: one approval item per pack whose limit is exceeded, routed by the rule and not by a screen, the limit exceeded read as the write-off committee limit that rule R-WO-12 names, the same four legacy messages MSG-S7-001, MSG-GEN-001, MSG-P4-002 and MSG-P7-003, and the same refusal of the whole action when the record cannot be written.

### 2. Business rationale

Rule R-WO-12 is short and its consequence is long: a pack of charged-off accounts whose amount sits above the write-off committee limit is routed to the credit approval committee chaired by the product head with Risk, and the case moves to ESCALATED_TO_CREDIT_COMMITTEE. Rule R-WO-32 then hands the charged-off population to the debt sale route and moves the case to SOLD_POST_CHARGEOFF. Between the two rules sits the whole authority of the sale: a population that reaches the buyer without the committee's approval was sold on an authority nobody granted, and R-WO-13 and R-WO-15 close the loop from the other side by requiring the final call, the approver and the limit applied to be recorded. REQ-S7-003 asks that the committee decision to approve, reject or defer is recorded against each account, and REQ-S7-006 asks that the post charge-off treatment, sale included, is set by rule; the two are unenforceable without an approval item that carries the level it was routed at and a decision record that names the rule and the version behind it.

Under Architecture v5 the approval item and the central ledger are `rwb-decision`'s (slides 14, 20, 27, 28 and 41: approvals, central decision ledger and DMN model registry; `ApprovalRequested` and `ApprovalDecided` on `rwb.decision.events.v1`). The realignment changes the mechanism and not the business rule:

1. The decision table that used to be read in process becomes a governed rule package with a version, and the two rows that matter here — R-WO-12 and R-WO-32 — are catalogue rows of this service's registry, so the rule id and the rule version on every entry resolve to a row a business person approved (slide 27; the routing logic of Business Rules and Routing Logic v4, route set Write-off, decision D9).
2. The delegation limit that used to be a table in the module's own schema is `rwb-access`'s versioned table, read at the moment of the decision and recorded with its version (slide 41; TSD P7 v2 A2.24). This service asks and stores the answer; it holds no limit and computes none.
3. The decision log that used to be written synchronously in one place becomes a local record written by the service that acts, hash-linked to the record before it, and a central ledger collected by this service on `rwb.decision-record.v1` within five minutes, with strict mode only at the four points of no return (slide 28; DP-03; ADR-022).
4. Every path is on the owner's base `/api/recovery/decision/v1` (DP-13), and the approval queue and the decision-log query are reached through the gateway-bff composite route the screens use (DP-19).
5. No service reads another service's tables: the case arrives on the P3 read, the delegation answer and the right on P4's operations, the write-off's own record on the shared topic, and the lot never arrives at all (DP-01).

This story carries the decision-record half of REQ-S7-003 and NFR-034 ("every action carries the rule version applied and the approver who allowed it") for this key: the approval item holds identifiers, a code, a level, a version, an amount and a user reference, and the record holds a rule id, a rule version, a final call and an approver, and no name, e-mail address, mobile number, national identity number or account number.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-S7-E6028-CON | The published write-off contract: the raise of an approval for a pack whose amount sits above the write-off committee limit, the answer that carries the approval reference back, and the record of R-WO-12 and of R-WO-32 that `rwb-writeoff` publishes on `rwb.decision-record.v1`. The request and answer shape of the raise is Not specified in the source documents (GAP-1311; ASM-2321); until the contract lands the P7 slice is built against its fake |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the append, the hash link, the chain sequence and the outbox row in one transaction |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) through which the approval queue and the decision-log query are reached; this story adds no route |
| The delegation answer and the authorise answer of `rwb-access` (P4) | The level, the delegation row id and the version of the delegation table in force for one decision, one regulation item, one product group, one amount and one business date; and the right and the scope of the caller on the reads and on the three decisions. Both are consumed on their published contracts or their fakes, are not rows of the metadata, and are carried in GAP-1312 |
| The case read of `rwb-case` (P3) | The owner, team, region and product group the scope filter of the two reads is applied to, and the status and stage S7's own story asserts; this story reads and changes none of them |

Business preconditions carried from RWB-E6-028 and from the sources of this key:

- The write-off committee limit and the tax criteria are not values of this story: the limit test is rule R-WO-12's, applied by `rwb-writeoff`, and the tax criteria hold the scan before any population exists (R-WO-03, MSG-S7-001). This service never sees the limit value and never compares an amount with it.
- The routing level is a value of LOV-APPROVAL-LEVEL, L1 to L6 (TSD P7 v2 T3.2), read from the P4 answer with the version of the delegation table in force on the business date. FSD P7 v3 A2.15 and A2.24 carry `DOA-2026.11` as an example version and `L6` as an example level; this story introduces neither and stores what the answer returns.
- The approval status is a value of LOV-APPROVAL-STATUS — WAITING, HELD_NO_LIMIT, APPROVED, REFUSED, RETURNED (TSD P7 v2 T3.2) — and the capability area of the item is WRITE_OFF_AND_POSTING, a value of LOV-CAPABILITY (TSD P7 v2 T3.2).
- The item is in the queue of the role the routing names, and it is not shown to the person who prepared it (FSD P7 v3 A2.15 row AC-P7-015-01 and A2.16 exception AC-EXC-P7-016-02).
- The rule package in force holds R-WO-12 and R-WO-32 with the row values of Business Rules and Routing Logic v4, so each entry's rule id and rule version resolve to a registry row; the version label of the package in force is Not specified in the source documents (GAP-1311; ASM-2323).
- The order of the legacy story's own criteria is unchanged: the pack is routed before it is approved, and the sale follows the approval, never the other way round (R-WO-12 then R-WO-32; FSD P7 v3 A2.15 and A2.16).
- No build dependency. Day 1, against the write-off fake and the two platform contracts, which are platform CON stories and block nothing.
- The hand-over of a charged-off population to the debt sale route (R-WO-32 where the placement type is sale; R-WO-50 and R-WO-51 closing on the buyer's settlement and remittance) is carried here as product behaviour with the population, the route and the approval recorded; the call type and the direction between this service and S6 rwb-debtsale are an open question with the S6 owner, to be closed before the wave 4 system test (GAP-1799).
- The two platform H dependencies, RWB-PLT-E1027-CON (DP-03) and RWB-PLT-N001-CON (DP-19), are non-blocking platform contracts of wave 0; the four consumed contracts of the delegation answer, the authorise answer, the case read and the reference-data lists are published contracts of P3 and P4, built against their fakes; the metadata rows are left as the plan gives them (GAP-1312).

### 4. Flow

1. `rwb-writeoff` (S7): the committee step of a pack reaches PACK_PREPARED and the amount of the pack sits above the write-off committee limit, so rule R-WO-12 sends the pack to the credit approval committee; `rwb-writeoff` calls the raise of this service, one hop with a 2 s timeout and a breaker, carrying the case reference, the write-off as the source item, the amount, the product group, the capability area WRITE_OFF_AND_POSTING, the rule id R-WO-12 and its rule version, and its idempotency key. The exact request shape is Not specified in the source documents (GAP-1311; ASM-2321).
2. `rwb-decision` `ApprovalRaiseController`: validates the shape, the idempotency key and the presence of the source item; a request with no source reference or no amount is refused with 422 and MSG-GEN-001 naming the field, and nothing is written (X1).
3. `rwb-decision` `ApprovalValidationService`: reads the decision code, the capability area, the approval level list and the approval status list as reference data with the version in force, and refuses a code, a capability area or a status that is not a value of its list with 422 and MSG-P7-009 naming the field; the text of MSG-P7-009 is Not specified in the source documents (GAP-1311; ASM-2321).
4. `rwb-decision` `DoaLimitClient`: calls the P4 delegation answer for decision D9, the regulation item of the pack, the product group, the amount and the business date, and takes the level, the delegation row id and the limit version from the answer. It re-computes nothing, holds no limit value and keeps no copy of the delegation table (DP-01).
5. No row of the delegation table covers the decision: the approval is stored with status HELD_NO_LIMIT, the case stays where `rwb-writeoff` has it, an incident is raised to RW-RISK with MSG-P7-010, and the answer is the held approval. The text of MSG-P7-010 is Not specified in the source documents (GAP-1311; ASM-2321).
6. A row covers the decision: `rwb-decision` `ApprovalRaiseService` writes, in one `RecordAndApply` transaction in `rwb_decision`, the routing `decision_log_entry` (the case, the decision code D9, rule id R-WO-12, its rule version, an inputs reference holding the amount, the product group and the delegation answer, the recommendation holding the level, the row and the version, the final call of the routing, the service identity as actor, the decided time, the previous hash, the entry hash and the chain sequence), the `approval` row with status WAITING and the routing details copied from the answer, and the outbox rows of the routing record and of the approval request.
7. The transaction commits and the controller answers 201 with the approval reference, the level, the delegation row, the limit version, the due time and the record reference; `rwb-writeoff` stores the approval reference and commits its own state change to ESCALATED_TO_CREDIT_COMMITTEE together with its own local record of R-WO-12 (RWB-S7-E6028-APP).
8. `rwb-decision` `DecisionRecordOutbox`: the relay publishes `rwb.decision.ApprovalRequested.v1` on `rwb.decision.events.v1` for the gateway-bff inbox and `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` for the ledger consumers, both in CloudEvents 1.0 with the record id and the case id as the key.
9. `rwb-decision` `LedgerIngestConsumer`: consumes `DecisionRecorded` from `rwb-writeoff` — the R-WO-12 record of the state change and the R-WO-32 record of the sale selection — deduplicates on the event id through the inbox, and appends one `decision_log_entry` per record with the next chain sequence and the previous hash of the head, in one transaction with its own outbox row where the event has to be relayed on.
10. An approver at the routed level opens `GET /api/recovery/decision/v1/approvals` and sees the item with the decision, the product, the amount, the level, the limit version and its age; the page is filtered to the caller's level and scope and never shows the caller an item they prepared (FSD P7 v3 A2.15 and A2.23).
11. `POST /api/recovery/decision/v1/approvals/{approvalId}/approve`: the guard answers the Decision log right and the capability area; the preparer is refused with 409 and MSG-P7-002 (X2); the approval must be WAITING or the call answers 409 (X3); and the approve writes, in one transaction, the record of the decision (the case, the code, rule R-WO-12 and its version, the inputs reference, the recommendation, the approver, the approval level, final call APPROVED, the decided time, the hashes and the sequence), the approval status APPROVED with its `decision_log_id` set to the new record, and the outbox rows of `DecisionRecorded` and `ApprovalDecided`. A failure of the record rolls everything back and answers 503 with MSG-P7-003 (X6).
12. `POST /approvals/{approvalId}/return` and `POST /approvals/{approvalId}/refuse` do the same with status RETURNED and REFUSED and a reason that is required; a missing reason is 422 with MSG-GEN-001 naming the field `reason` (X4, X5).
13. Readers with the Decision log right and the case in scope read the ledger with `GET /api/recovery/decision/v1/decision-log?caseId=…` and one record with `GET /api/recovery/decision/v1/decision-log/{entryId}`, and see the two R-WO entries of the case — the routing record of this service and the write-off's own record — each with its rule id, its rule version, its final call, its approver and its hashes, in chain order (X7, X8).
14. Nothing in this story changes the case, the pack, the committee, the sale or the lot: the case moves only because `rwb-writeoff` moves it, and the ledger is the only thing this service adds to the population.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The raise arrives with no source item, no amount or a malformed body | Refused with 422 before anything is read or written; no approval, no record, no sequence consumed | MSG-GEN-001 | AC1 |
| X2 | The approver prepared the decision | Refused with 409 and the approval stays WAITING; no record and no status change | MSG-P7-002 | AC4, TC-E6-028-05 |
| X3 | The approve, return or refuse arrives for an item that is no longer WAITING, or two decisions arrive at once | The first commits, the second is refused with 409 and the optimistic lock; one record and one final call exist | MSG-GEN-004 | AC3 |
| X4 | A return carries no reason | Refused with 422 and MSG-GEN-001 naming `reason`; nothing written | MSG-GEN-001 | AC5 |
| X5 | A refuse carries no reason | Refused with 422 and MSG-GEN-001 naming `reason`; nothing written | MSG-GEN-001 | AC5 |
| X6 | The record cannot be written: the library fails, the insert fails or the connection is lost | The whole transaction rolls back; the approval keeps WAITING, no `DecisionRecorded` and no `ApprovalDecided` is written, no chain sequence is consumed, and the incident is raised under R-UNI-39 | MSG-P7-003 | AC7, TC-E6-028-04, TC-E6-028-06 |
| X7 | The caller holds no Decision log right, or no right in the capability area | 403 with MSG-P4-002 and nothing returned | MSG-P4-002 | AC2, TC-E6-028-05 |
| X8 | The case of the item or of the record is outside the caller's scope | The item is not listed and the single read answers 404 with MSG-P4-003; nothing is returned | MSG-P4-003 | AC2 |
| X9 | No row of the delegation table covers the decision | The approval is stored with status HELD_NO_LIMIT and an incident is raised to RW-RISK; the case does not move | MSG-P7-010 | AC6, TC-E6-028-02 |
| X10 | A `DecisionRecorded` of the same event id arrives twice, or the same record is replayed | The inbox absorbs the repeat; the ledger holds one entry with one chain sequence | None to a user | AC8, TC-E6-028-03 |
| X11 | A `DecisionRecorded` arrives for a record whose rule id is not in the registry of this service | The entry is appended with the rule id it carries and the ingest raises a registry gap to RW-COE; nothing is refused and nothing is invented | None to a user | AC8 |

No approval row is ever deleted and no ledger row is ever updated: a wrong record is corrected by a new record that names the one it corrects in `corrects_entry_id`, so the ledger stays append only (REQ-DRI-002). The approval item keeps the state a decision put it in; a re-opened pack is a new item raised by `rwb-writeoff` and not a resurrection of the old one.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the write-off contract of RWB-S7-E6028-CON, the decision-record library, the gateway-bff route and the P4 and P3 answers and their fakes; no write-off behaviour, no pack, no committee, no posting, no lot and no delegation rule is rebuilt here |
| Negotiable | The code and list values, the level and the version, the amounts and the message texts are reference data, the delegation answer or the message standard; the story fixes only the one-item-per-pack rule, the read-not-computed level, the one-record-per-decision rule, the chain and the fail-closed behaviour |
| Valuable | No charged-off population can be sold on an approval the committee never gave, and the authority behind each sold pack is readable afterwards with its rule and its limit version |
| Estimable | One controller set, one raise service, one DoA client, one decision service, one chain writer, one ingest consumer, three reads, one migration |
| Small | Fits one sprint with its tests; it is the approval-and-ledger slice of the legacy key |
| Testable | Each of the eight criteria in section 7 runs as an automated test against the contract fakes, the delegation fake and the decision-record library, with a fixed clock and a seeded chain |
| Not this story | The write-off scan, the pack, the committee agenda, the posting, the provision release, the finance feed and the debt-sale lot are RWB-S7-E6028-APP and S6's; the delegation table, the role model and the scope are P4's; SCR-27 is S7's and the Epic 8 screen stories'; the cross-service proof is RWB-ITG-E6028-ITG's |

### 7. Acceptance criteria

```gherkin
Feature: Sell a post charge-off population — the rwb-decision approval and decision-record slice

  Background:
    Given the environment is SIT
    Given the rwb-writeoff contract mock returns write-off "WO-SYN-000730" for case "RW-2027-000730" of product group "MORTGAGE" at PACK_PREPARED, with the amount above the write-off committee limit under rule "R-WO-12" version in force
    Given the rwb-access contract mock returns the delegation answer for decision "D9" with level "L6", delegation row "DL-2.1.10-L6" and limit version "DOA-2026.11"
    Given product head "approver.user01" holds the Decision log right A for capability area "WRITE_OFF_AND_POSTING" at level "L6"

  Scenario: AC1 An above-limit pack raises one approval at the level the delegation answer gives (new, D-RCV-60)
    Given rwb-writeoff sends the raise for write-off "WO-SYN-000730" of case "RW-2027-000730" with source type, source reference, amount and rule "R-WO-12"
    When rwb-decision raises the approval
    Then one approval exists with status "WAITING", capability area "WRITE_OFF_AND_POSTING", level "L6", delegation row "DL-2.1.10-L6", limit version "DOA-2026.11" and the amount of the pack
    Then one routing decision record exists for the case with rule id "R-WO-12", its rule version and the level, row and version of the delegation answer as its recommendation
    Then the raise answer carries the approval reference and the record reference and rwb-writeoff stores both
    Then rwb-decision computed no limit and holds no delegation row

  Scenario: AC2 The approval queue is filtered to the caller and to the level (new, D-RCV-60)
    Given three approvals exist at levels "L6", "L5" and "L6", the third prepared by "approver.user01"
    Given the rwb-case contract mock returns case "RW-2027-000731" in team "HP-NE" outside the scope of "approver.user01"
    When "approver.user01" sends GET /api/recovery/decision/v1/approvals
    Then the page holds the "L6" item prepared by another role, with its amount, level, limit version and age
    Then it holds no "L5" item, no item prepared by "approver.user01" and no item of case "RW-2027-000731"
    Then a caller holding no Decision log right is refused with 403 and MSG-P4-002, and an item of case "RW-2027-000731" read singly is 404 with MSG-P4-003

  Scenario: AC3 An approval inside the limit records the final call, the approver and the level (new, D-RCV-60)
    Given the approval of case "RW-2027-000730" is "WAITING" at level "L6"
    When "approver.user01" approves it with one Idempotency-Key
    Then the answer is 200 with the record reference and the status "APPROVED"
    Then one decision record exists with rule id "R-WO-12", its rule version, final call "APPROVED", the approver, approval level "L6" and the limit version "DOA-2026.11"
    Then the approval carries that record as its decision log reference and the ledger chain holds one new link
    Then a repeat of the same call with the same Idempotency-Key answers the first record and adds no second entry and no second link

  Scenario: AC4 The preparer cannot approve their own pack (new, D-RCV-60)
    Given the approval of case "RW-2027-000730" was prepared by "approver.user01" and is "WAITING"
    When "approver.user01" approves it
    Then the answer is 409 with MSG-P7-002
    Then the approval stays "WAITING" and no decision record is written for the attempt

  Scenario: AC5 A return and a refuse need a reason (new, D-RCV-60)
    Given the approval of case "RW-2027-000730" is "WAITING" and held by "approver.user01"
    When "approver.user01" returns it with no reason and then refuses it with no reason
    Then each answer is 422 with MSG-GEN-001 naming the field "reason"
    Then no status changes and no decision record is written
    When "approver.user01" refuses it with the reason "Tax criteria version not published at the meeting"
    Then the approval is "REFUSED", one decision record exists with final call "REFUSED" and that reason, and rwb-writeoff reads the refusal on its own contract

  Scenario: AC6 A decision no limit covers is held, not routed (new, D-RCV-60)
    Given the rwb-access contract mock returns no delegation row for decision "D9" of product group "HIRE_PURCHASE"
    When rwb-writeoff sends the raise for write-off "WO-SYN-000731" of case "RW-2027-000731"
    Then the approval is stored with status "HELD_NO_LIMIT"
    Then no routing decision record carries a level and no approval is queued for a role
    Then an incident is raised to RW-RISK with MSG-P7-010

  Scenario: AC7 The record cannot be written and nothing else moves (new, D-RCV-60)
    Given the approval of case "RW-2027-000730" is "WAITING" at level "L6"
    Given the decision-record library refuses the append and raises its unavailable condition
    When "approver.user01" approves it
    Then the answer is 503 with MSG-P7-003
    Then the approval stays "WAITING", no decision record and no outbox row exists for the attempt, and the chain stands at its last entry
    Then an incident is raised under R-UNI-39 to the platform administration role

  Scenario: AC8 The R-WO-32 record is collected once and read back with its rule version (new, D-RCV-60)
    Given rwb-writeoff publishes rwb.decision.DecisionRecorded.v1 for case "RW-2027-000730" with rule id "R-WO-32", its rule version, final call "SOLD_POST_CHARGEOFF" and one event id
    When rwb-decision consumes the event and the same event id is delivered again
    Then one ledger entry exists for that record, with rule id "R-WO-32", its rule version and the next chain sequence
    Then GET /api/recovery/decision/v1/decision-log for the case returns the routing record of rule "R-WO-12" and the record of rule "R-WO-32" in chain order
    Then the single read of each entry carries its final call, its approver where it has one, its decided time, its previous hash and its entry hash

  Scenario: AC9 The approval, the record, the event and the log carry no personal data and reach no case, task, timer or delegation row (new, D-RCV-60)
    Given the approval of case "RW-2027-000730" is "WAITING" at level "L6"
    When "approver.user01" approves it
    Then the approval, the decision record, the outbox row and the log line hold only case and write-off identifiers, a decision code, a rule id and version, a level, an amount, a status, a reason and a user reference
    Then no write reaches a case, task, timer or delegation row

  Scenario: AC10 A call without a valid credential is refused with 401 on each provided operation (new, D-RCV-60)
    Given no valid credential is sent with the call
    When the caller sends a call to each provided operation of this service
    Then each answer is 401 and nothing is read or written
```

These ten criteria are new for the `rwb-decision` slice of RWB-E6-028 and are the approval and ledger criteria of the key; the legacy values they use are the values of the key — the write-off committee limit test of rule R-WO-12, the escalation state ESCALATED_TO_CREDIT_COMMITTEE, the sale state SOLD_POST_CHARGEOFF, rule R-WO-32, the write-off and posting capability area with right A held by RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE, the four legacy messages and the decision code domain D9 — and no new business value is introduced. `acs` is empty for this story: no legacy criterion is owned verbatim here, because legacy AC1 opens the sale, legacy AC2 reads the escalation of the case, legacy AC3 reads the sale state and legacy AC4 reads the not-recorded path at the write-off, and all four belong to RWB-S7-E6028-APP. The level, the delegation row and the limit version are values of the P4 answer on the business date; `DOA-2026.11` and `L6` in the Background and the scenarios are the example values of FSD P7 v3 A2.15 and A2.24 and are read as the answer, never as a constant of this service.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One approval item per write-off pack whose amount sits above the write-off committee limit; the item is raised by the write-off story of this key and carried here through the states of LOV-APPROVAL-STATUS | R-WO-12; TSD P7 v2 T3.1 `approval`, T3.2 LOV-APPROVAL-STATUS; legacy AC2 |
| BR2 | The level, the delegation row and the version of the delegation table are read from the P4 answer on the business date and written on the approval and on the record; no limit is computed here and no delegation row is copied. The legacy "limit exceeded" of rule R-WO-12 is read as the write-off committee limit the rule names — the test is `rwb-writeoff`'s — and the level is the answer's, which is ASM-2322 | TSD P7 v2 A2.24 and T3.1 DF-DEC-038 to DF-DEC-040; FSD P7 v3 A2.15 and A2.24; Ownership Map `delegation_limit` to P4; DP-01 |
| BR3 | A decision that no delegation row covers is stored with status HELD_NO_LIMIT, is queued for no role and raises an incident with MSG-P7-010; it is never routed on a guessed level | FSD P7 v3 A2.15 AC-EXC-P7-015-06 and A2.24 AC-EXC-P7-024-11; TSD P7 v2 T3.2 |
| BR4 | The routing of a pack writes exactly one decision record, naming rule R-WO-12, its rule version and the delegation answer, in the same transaction as the approval row and without which neither exists | FSD P7 v3 A2.15 AC-P7-015-01; TSD P7 v2 T2 ("writes the decision log entry before any change"); R-UNI-39; DP-03 |
| BR5 | The approver cannot be the preparer; the attempt is refused with 409 and MSG-P7-002 and the item stays WAITING | FSD P7 v3 A2.16 AC-EXC-P7-016-02; VR-P7-016-2; legacy section "Permission checks" |
| BR6 | An approve records the final call, the approver, the approval level and the limit applied, and releases the item; the case is released by `rwb-writeoff` and not here | R-WO-13; R-WO-15; REQ-S7-003; TSD P7 v2 T3.1 DF-DEC-010 to DF-DEC-012 |
| BR7 | A return and a refuse require a reason of at most 1,000 characters written as the override reason; a missing reason is refused with 422 and MSG-GEN-001 naming the field | TSD P7 v2 T-A.2 API-P7-004 and API-P7-005; T3.1 DF-DEC-013; FSD P7 v3 A2.18; legacy MSG-GEN-001 |
| BR8 | Every action of this story writes its record once, in the same transaction as the status it records, and an action whose record cannot be written does not happen | REQ-DRI-005; R-UNI-39; FSD P7 v3 A2.5 VR-P7-005-2; MSG-P7-003; DP-03 |
| BR9 | The record is append only and hash chained: an entry hash over its canonical form, a previous hash equal to the entry hash before it, a sequence number never reused, no update and no delete; a wrong record is corrected by a new record naming the one it corrects | REQ-DRI-002; REQ-DRI-003; TSD P7 v2 T3.1 DF-DEC-017, DF-DEC-018, DF-DEC-028, DF-DEC-029 |
| BR10 | The record of rule R-WO-12 and the record of rule R-WO-32 written by `rwb-writeoff` are collected once into the central ledger from `rwb.decision-record.v1`, deduplicated on the event id, with the target of five minutes and strict mode only at the four points of no return. One escalation therefore leaves two entries in the ledger — the routing record this service writes and the write-off's own record of the state change — and neither is a duplicate of the other, which is ASM-2324 and GAP-1313 | Architecture v5 slides 20 and 28; DP-03; R-WO-12; R-WO-32; ADR-022 |
| BR11 | The two rule rows of R-WO-12 and R-WO-32 are registry rows of this service, carrying the route set, the from state, the event code, the condition, the action, the to state, the owner, the systems and the timer of the routing logic, with the rule version in force | Architecture v5 slide 27; Temporal design slide 15 T6; Business Rules and Routing Logic v4 rows R-WO-12 and R-WO-32; TSD P7 v2 T3.1 `rule_row` |
| BR12 | The approval read and the three decisions are served under the Decision log right A and the caller's scope, and the two ledger reads under the read right R; the approval operations also require the write-off and posting capability area, and both are required in the authorise answer; this service holds no role, no scope and no masking rule of its own | TSD P7 v2 T-A.1 and T6.2; FSD P7 v3 T6.1 (read right only) and A2.23; the authorise dependency is carried in GAP-1312 and the role holders in GAP-1314 |
| BR13 | No personal data in the approval, the record, the event, the trail or the logs: case and write-off identifiers, a decision code, a rule id and version, a level, an amount, a status, a reason and a user reference only; the P2 personal-data classing of each field of this list is checked before build | Template and Rules §R7.2 s17; Architecture v5 slides 42 and 43 |
| BR14 | This story moves no case, sets no task and no timer, and holds no copy of a write-off, a case or a delegation row; the split of write-off states between the write-off stage record and the case state is an open question with the P3 owner (GAP-1800) | Architecture v5 slide 41; DP-01; the case is P3's and the write-off is S7's |

### 9. State transitions

The states below are the states of the approval item of this story and of its records. The case states PACK_PREPARED, ESCALATED_TO_CREDIT_COMMITTEE, PLACEMENT_DECIDED and SOLD_POST_CHARGEOFF are `rwb-writeoff`'s and are named only so the boundary is visible.

| From | Event | Condition | To |
|---|---|---|---|
| Absent | A raise arrives for a pack above the write-off committee limit and a delegation row covers it | The record, the approval and the outbox rows commit in one transaction | WAITING, with the level, the delegation row, the limit version and one routing record |
| Absent | A raise arrives and no delegation row covers the decision | The DoA client answers that nothing covers the decision | HELD_NO_LIMIT, with no role queue and an incident carrying MSG-P7-010 |
| Absent | A raise arrives with no source item or no amount | The validation refuses the request | Absent: 422 and MSG-GEN-001 naming the field |
| WAITING | Approve by a caller at the item's level who is not the preparer | The record and the status commit together | APPROVED, with the final call, the approver, the level, the limit version and one record |
| WAITING | Return with a reason | The record and the status commit together | RETURNED, with the reason as the override reason |
| WAITING | Refuse with a reason | The record and the status commit together | REFUSED, with the reason as the override reason |
| WAITING | Approve, return or refuse by the preparer | The preparer rule refuses the call | WAITING: 409 and MSG-P7-002, nothing written |
| WAITING | Approve, return or refuse without a reason where one is needed | The validation refuses the call | WAITING: 422 and MSG-GEN-001 naming `reason` |
| WAITING | The record cannot be written | The transaction rolls back | WAITING: 503 and MSG-P7-003, the chain at its last entry |
| WAITING | A second decision arrives at the same moment | The first commits and the optimistic lock refuses the second | The state the first decision set: 409 and MSG-GEN-004 for the second, one record only |
| HELD_NO_LIMIT | A delegation row is published for the decision and the item is raised again | A new item is raised by `rwb-writeoff` | A new item at the level of the answer; the held item stays as it was |
| Any decided state | A later approve, return or refuse arrives | The item is no longer WAITING | Unchanged: 409 and MSG-GEN-004 |
| Absent record | A `DecisionRecorded` arrives on the shared topic | The inbox has not seen the event id | Appended with the next chain sequence and the head's previous hash |
| Appended record | The same event id arrives again | The inbox holds the id | Appended: unchanged, one entry and one sequence |
| Appended record | A wrong record must be corrected | A person decides the correction | Appended: a new record with `corrects_entry_id` naming the wrong one; the wrong one stays |

The approval leaves WAITING only through one of the three decisions of this story, and the escalation of an overdue item — the move of the same item to a higher role with `escalation_level` raised and a new due time — is the escalation path of FSD P7 v3 A2.20 and not this story. The case states are S7's: this story neither sets them nor reads them as its own.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PRODHEAD, the product head (Mortgage, HP, SSME) | Chairs the credit approval committee with Risk, reads the item at their level and approves, returns or refuses it; holds Write-off and posting A under the legacy permission table and the Decision log right on the approval operations |
| RW-CREDCOMM, the credit approval committee member | Holds the right the escalated item is routed to under R-WO-12 and decides it; the legacy permission table does not list RW-CREDCOMM against Write-off and posting A, which is GAP-1314 |
| RW-CREDITAD, RW-WOCOMM and RW-FINANCE | Hold Write-off and posting A under the legacy permission table and read and decide the items routed to them; the committee's own routing for the inside-limit pack under R-WO-11 is not this story |
| RW-RISK, the risk and model risk officer | Receives the HELD_NO_LIMIT incident with MSG-P7-010 and reads the record of the item |
| RW-AUDIT and RW-TRIBE | Read the approval and the ledger under the Decision log right R, as TSD P7 v2 T6.1 fixes it; they take no decision |
| SY-DECLOG and SY-CASEWF | Append the record of a decision on behalf of a service, one hop, under the service identity; they hold no user right and write nothing else |
| The `rwb-decision` service identity | Writes its own `approval`, `decision_log_entry` and outbox rows, and reads the delegation answer and the case read (the `rwb-decision` login, DP-02) |
| `rwb-access` (P4) | Owns the delegation table, the role model, the scope and the authorise answer; this story applies the two answers and changes neither |
| `rwb-writeoff` (S7) | Owns the scan, the pack, the committee, the case states, the posting and the local records of R-WO-12 and R-WO-32; it raises the item and this story routes, records and serves it |

The authorisation decision is `rwb-access`'s and is consumed as the answers the operations declare; the refusal shape stays 403 with MSG-P4-002 and 404 with MSG-P4-003. The right that guards the approval operations is read as the Decision log right A of TSD P7 v2 T-A.1 together with the capability area WRITE_OFF_AND_POSTING of the approval row; the reading of the FSD P7 v3 T6.1 column as the read right only, and of RW-CREDCOMM as a holder of the capability right the legacy table does not list, is ASM-2326 and GAP-1314. The database login is per service (DP-02) and its name is Not specified in the source documents (GAP-1311; ASM-2272).

### 11. Data

| BR Field ID | Entity in `rwb_decision` | Field | Read or write |
|---|---|---|---|
| DF-DEC-032 | `approval` | id | Write |
| DF-DEC-033 | `approval` | case_id | Write |
| DF-DEC-034 | `approval` | decision_code | Write, the code D9 of the write-off decision, read as a value of LOV-DECISION |
| DF-DEC-035 | `approval` | regulation_item | Write, the item of the pack as the write-off carries it |
| DF-DEC-036 | `approval` | capability_area | Write, WRITE_OFF_AND_POSTING of LOV-CAPABILITY |
| DF-DEC-037 | `approval` | route_role_code | Write, the role the routing names, as the answer and the rule row give it |
| DF-DEC-038 | `approval` | approval_level | Write, the level of the P4 answer, a value of LOV-APPROVAL-LEVEL |
| DF-DEC-039 | `approval` | delegation_limit_id | Write, the row id of the P4 answer |
| DF-DEC-040 | `approval` | limit_version | Write, the version of the delegation table in force, from the P4 answer |
| DF-DEC-041 | `approval` | product_group | Write, a value of LOV-PRODUCT |
| DF-DEC-042 | `approval` | amount | Write, the amount of the pack as the write-off sends it; the limit test is not repeated here |
| DF-DEC-043 | `approval` | terms | Write, the pack facts the routing needs, where the write-off sends them |
| DF-DEC-044 | `approval` | prepared_by | Write, the user reference of the raise |
| DF-DEC-045 | `approval` | assigned_user_id | Write when the routing names a holder, empty otherwise |
| DF-DEC-046 | `approval` | status | Write, a value of LOV-APPROVAL-STATUS |
| DF-DEC-047 | `approval` | due_at | Write, the due time the routing sets |
| DF-DEC-048 | `approval` | escalation_level | Write; the base value the item starts at is Not specified in the source documents (GAP-1311; ASM-2321) |
| DF-DEC-049, DF-DEC-050 | `approval` | source_type, source_ref | Write, the kind and the reference of the write-off the item is for; the value set of `source_type` is Not specified in the source documents (GAP-1311; ASM-2321) |
| DF-DEC-051, DF-DEC-052 | `approval` | rule_id, rule_version | Write, R-WO-12 and its rule version for the write-off item |
| DF-DEC-053 | `approval` | decision_log_id | Write on a decision, the record of the final call |
| DF-DEC-001 | `decision_log_entry` | id | Write |
| DF-DEC-002 | `decision_log_entry` | case_id | Write |
| DF-DEC-003 | `decision_log_entry` | decision_code | Write, a value of LOV-DECISION; the code of the escalation and of the sale selection is Not specified in the source documents (GAP-1311; ASM-2323) and is read as reference data, never as a constant |
| DF-DEC-004, DF-DEC-005 | `decision_log_entry` | rule_id, rule_version | Write, R-WO-12 on the routing record and on the R-WO-12 record, R-WO-32 on the sale-selection record |
| DF-DEC-006, DF-DEC-007 | `decision_log_entry` | model_version, agent_version | Not written by this story |
| DF-DEC-008 | `decision_log_entry` | inputs_ref | Write, the reference of the inputs snapshot with the amount, the product group and the delegation answer |
| DF-DEC-009 | `decision_log_entry` | recommendation | Write, the level, the delegation row and the limit version of the answer, and the rule result where one exists |
| DF-DEC-010 | `decision_log_entry` | approver_user_id | Write on a decision; empty on a routing record |
| DF-DEC-011 | `decision_log_entry` | approval_level | Write on a decision, the level applied |
| DF-DEC-012 | `decision_log_entry` | final_call | Write; the value set of a routing record and of a decision is Not specified in the source documents (GAP-1311; ASM-2321) and the values APPROVED, RETURNED and REFUSED are read as reference data |
| DF-DEC-013 | `decision_log_entry` | override_reason | Write on a return and on a refuse, at most 1,000 characters |
| DF-DEC-014, DF-DEC-015 | `decision_log_entry` | actions, outcome | Write where the decision carries them |
| DF-DEC-016 | `decision_log_entry` | decided_at | Write |
| DF-DEC-017, DF-DEC-018 | `decision_log_entry` | prev_hash, entry_hash | Write |
| DF-DEC-028 | `decision_log_entry` | chain_seq | Write |
| DF-DEC-029 | `decision_log_entry` | corrects_entry_id | Write only on a record that corrects an earlier one |
| DF-DEC-030 | `decision_log_entry` | actor_user_id | Write, the approver reference or the service identity |
| DF-DEC-031 | `decision_log_entry` | idempotency_key | Write, the idempotency key of the raise or of the decision; the key of an ingested record is the event id |
| DF-DEC-001 to DF-DEC-031 | `decision_log_entry` | all fields | Read through `GET /decision-log` and `GET /decision-log/{entryId}` |
| DF-DEC-032 to DF-DEC-053 | `approval` | all fields | Read through `GET /approvals` and `GET /approvals/{approvalId}` |
| DF-REF-001 to DF-REF-015 | `rule_row` | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | Write for the two rows of R-WO-12 and R-WO-32; read by the ingest to resolve an entry's rule and version |
| DF-CAS-001, DF-CAS-003, DF-CAS-009, DF-CAS-011, DF-CAS-012 | `recovery_case` | id, product_group, owner_user_id, team_code, region_code | Read through the P3 case read, for the scope filter only |
| (delegation answer) | `delegation_limit` (P4) | the level, the row id and the version | Read through the P4 answer; no row is copied and no field identifier is restated here |
| (outbox), (inbox), `idempotency_key` | library objects in `rwb_decision` | the event rows of the two records and of the two approval events, the processed event ids, the stored answer of a repeated call | Write |

No row of `write_off`, of `debt_sale_lot`, of `debt_sale_account`, of `recovery_case`, of `delegation_limit`, of `role`, of `permission` or of `masking_rule` is copied into `rwb_decision`: the write-off arrives on its contract and its records on the shared topic, the case on the P3 read, and the delegation and the right on P4's answers. Field IDs are those in the Logical Data Model and Data Dictionary v9.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-decision` (P7); base `/api/recovery/decision/v1`. API-P7-002, API-P7-003, API-P7-004, API-P7-005, API-P7-006, API-P7-007 and API-P7-008 are the operations of TSD P7 v2 T-A.1; the raise on the same collection is the write path this slice needs so that the write-off story can hand the item over without writing a foreign table, and it is Not specified in the source documents (GAP-1311; ASM-2321). The field set of `ApprovalPage`, `ApprovalDetail`, `ApprovalAction`, `DecisionLogPage` and `DecisionLogEntry` is named by T-A.2 without being written out and is Not specified in the source documents (GAP-1311; ASM-2321).

| ID | Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|---|
| (raise) | POST | `/approvals` | Raise one approval for a write-off pack whose limit is exceeded: validate, route on the delegation answer, write the routing record and the item in one transaction, answer 201 (Not specified in the source documents (GAP-1311; ASM-2321)) | Service identity only, SY-DECLOG and `rwb-writeoff`; one hop with a 2 s timeout | Idempotency-Key header, stored on the approval |
| API-P7-002 | GET | `/approvals` | List the decisions waiting for the caller's level | Decision log, right A, scope applied | Not applicable, read only |
| API-P7-008 | GET | `/approvals/{approvalId}` | Read one approval with its routing details | Decision log, right A, scope applied | Not applicable, read only |
| API-P7-003 | POST | `/approvals/{approvalId}/approve` | Approve inside the caller's limit and answer the record | Decision log, right A, scope applied | Idempotency-Key header |
| API-P7-004 | POST | `/approvals/{approvalId}/return` | Return the item to the preparer with a reason | Decision log, right A, scope applied | Idempotency-Key header |
| API-P7-005 | POST | `/approvals/{approvalId}/refuse` | Refuse the item with a reason and answer the record | Decision log, right A, scope applied | Idempotency-Key header |
| API-P7-006 | GET | `/decision-log` | Search the ledger by case, decision, rule, approver and date | Decision log, right R, scope applied | Not applicable, read only |
| API-P7-007 | GET | `/decision-log/{entryId}` | Read one record with its inputs and versions | Decision log, right R, scope applied | Not applicable, read only |

Errors: 401 no session (message ID Not specified in the source documents (CG-ALL-7458)); 403 the caller holds no Decision log right (MSG-P4-002); 404 the item, the record or the case is absent or out of scope (MSG-P4-003); 409 the approver prepared the item (MSG-P7-002) or the item is no longer WAITING (MSG-GEN-004); 422 a reason is missing (MSG-GEN-001) or a code, a capability area or a status is not a value of its list (MSG-P7-009); 503 the record was not written (MSG-P7-003). Every error is an RFC 9457 problem response with `messageId` set.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/access/v1/doa-limits` | P4 `rwb-access` | The delegation answer for one decision, regulation item, product group, amount and business date: the level, the delegation row id and the version in force. The path is the one Architecture v5 slide 14 names for P4; the Ownership Map publishes no row for it and its request and answer shape is Not specified in the source documents (GAP-1311; ASM-2321); faked, one hop with a 2 s timeout and a breaker |
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` | The right and the scope of the caller behind the four reads and the three decisions; faked, cached |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 `rwb-case` | The owner, team, region and product group the scope filter is applied to; faked, one hop |

The three operations are the P4 and P3 rows of Architecture v5 slides 14 and 41 and of the Ownership Map. The Ownership Map publishes `GET /me/session` for P4 and no row for the authorise and delegation paths, so both are consumed against their published contracts or their fakes and the dependency is carried in GAP-1312. DP-08, which would add the guard library and the authorise contract as named dependencies, is not among the patterns of this key.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision.ApprovalRequested.v1` | `rwb.decision.events.v1` | P7, published by this service | approvalId | approval ID, case ID, amount, level |
| `rwb.decision.ApprovalDecided.v1` | `rwb.decision.events.v1` | P7, published by this service | approvalId | Not specified in the source documents (CG-ALL-7460) |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7, published by this service | entryId | record ID, case ID, decision code, rule id, rule version, final call, approval level, decided at, chain sequence, entry hash |

`ApprovalRequested` and `ApprovalDecided` are the two events Architecture v5 slides 14 and 42 give to `rwb.decision.events.v1`, with the gateway-bff inbox as the consumer of the first. Each is written to the outbox in the same transaction as the row it announces, relayed in the CloudEvents 1.0 envelope, and carries no name, e-mail address, mobile number, national identification number or account number.

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | Produced by all 19 services, here by `rwb-writeoff` for R-WO-12 and R-WO-32 | CloudEvents 1.0 binary mode, key caseId, one event per local append; consumed idempotently into the central ledger, deduplicated on the event id through the inbox, with the five-minute completeness target of Architecture v5 slide 28 |

The three events of the catalogue that concern the item — `ApprovalRequested`, `ApprovalDecided` and `DecisionRecorded` — are on two topics, and this service consumes only its own ledger feed; a record this service writes goes into `decision_log_entry` inside its own transaction and its event, if it comes back, is dropped by the inbox as already stored.

#### 12.5 Workflows and activities

None of this story's own. The raise and the three decisions are synchronous operations inside one unit of work, and the two reads are queries. `rwb-decision` holds `ApprovalWorkflow` of the workflow kit as Architecture v5 slide 14 names it, and the kit is the workflow-platform story's (DP-10 is not among the patterns of this key); this story starts no workflow, signals none and registers no activity on the `rwb-decision` queue. The escalation of an overdue item, which would be the timer that raises `escalation_level`, is FSD P7 v3 A2.20's path and the escalation slice's.

#### 12.6 Schedules

None. JOB-13 at 01:00 is the legacy decision-log copy and is now the continuous Kafka ingest this story's consumer is part of, so no Schedule is registered for it; JOB-14 at 02:00 is the chain check of the decision-log store slice of this service; JOB-20 at 00:01 is the rule promote of the registry slice; and JOB-16 at the third working day is `rwb-writeoff`'s and starts the population this story never runs (Architecture v5 slide 44). This story adds no cadence and polls nothing.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `approval` | P7 (`rwb_decision`) | The item: the case, the code, the capability area, the routing role, the level, the delegation row and its version, the product group, the amount, the source item, the status, the due time, the rule and the record reference |
| `decision_log_entry` | P7 (`rwb_decision`) | The routing record and the record of each decision of this story, and the central entry of each record collected from `rwb-writeoff`; written once and read |
| `rule_row` | P7 (`rwb_decision`) | The two rows of R-WO-12 and R-WO-32 in the registry, with their route set, states, event, condition, action, owner, systems and timer |
| outbox library table and `processed_event` | PLT library, created in `rwb_decision` | The `ApprovalRequested`, `ApprovalDecided` and `DecisionRecorded` rows, and the processed event ids of the ingest (DP-09) |
| `idempotency_key` | PLT library, created in `rwb_decision` | The stored answer of a repeated raise and of a repeated decision |

Not owned and never read by this story: `write_off` (S7; its four entity groups are the scan result, the committee decision per account, the posting attempts and the recovery, placement and closure records), `debt_sale_lot` and `debt_sale_account` (S6), `recovery_case`, `task`, `timer` and `queue` (P3), `delegation_limit`, `role`, `permission` and `masking_rule` (P4), `lov_value` and `parameter_catalog` (P3). The delegation answer, the case and the right arrive on their contracts; no foreign key crosses a schema and no row of another service is copied (DP-01). The `approval` and `decision_log_entry` baselines belong to the slices that created them — the approvals slice of this service for `approval` (legacy RWB-E2-013) and the decision-log store slice for the ledger (legacy RWB-E1-008) — and this story adds only its keys and indexes.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-writeoff contract fake | RWB-S7-E6028-CON | The raise of the pack of case `RW-2027-000730` above the limit under R-WO-12; the raise of `RW-2027-000731` of product group HIRE_PURCHASE; the `DecisionRecorded` of the R-WO-12 state change and of the R-WO-32 sale selection with their rule versions and one event id, replayed once; the request journal for the idempotency assertions |
| rwb-access fake | The P4 delegation and authorise answers | The answer of level `L6`, row `DL-2.1.10-L6` and version `DOA-2026.11`; the answer that nothing covers HIRE_PURCHASE for D9; the allow answer on the Decision log right A for `approver.user01` and the refusal for a role without it (MSG-P4-002); the refusal of the out-of-scope case (MSG-P4-003) |
| rwb-case fake | The P3 case read | Case `RW-2027-000730` in scope with product group MORTGAGE; case `RW-2027-000731` in team `HP-NE` outside the scope |
| decision-record fake | RWB-PLT-E1027-CON | The append of the local record, the chain sequence allocation and the hash link; the chain verifier over a seeded ledger; a forced failure and an unavailable condition for AC7 |

Each fake is replaced by the real service as its contract lands, without a change to the criteria: the write-off fake stands until RWB-S7-E6028-CON and RWB-S7-E6028-APP land, and every flow is asserted against the published contract and its fake in the meantime.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 8, consumed 3 | The raise, the two approval reads and the three decisions, and the two ledger reads provided; the delegation answer, the authorise call and the case read consumed, one hop each with the 2 s timeout |
| Kafka | Published 3 event types, consumed 1 | `rwb.decision.ApprovalRequested.v1` and `rwb.decision.ApprovalDecided.v1` on `rwb.decision.events.v1`, `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`; `DecisionRecorded` consumed for the ledger |
| Temporal | None | No workflow, no activity and no Schedule registered; `ApprovalWorkflow` and the Schedules of the service belong to other slices |
| File | None | No file input and no file output; the daily ledger seal is the store slice's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `approval/writeoffsale`, Java package `th.co.scb.ace.workbench.recovery.decision.writeoffsale`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | The monolith REST base | `/api/recovery/decision/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the core of the slice: the legacy `DecisionLogWriter` of the monolith becomes the local decision-record library of this service, which writes the record, the hash link and the outbox row in one transaction and publishes on `rwb.decision-record.v1`, so the routing of R-WO-12, the approval of the committee and the two write-off records of R-WO-12 and R-WO-32 each have one entry in a ledger this service owns. DP-13 puts the eight operations on `/api/recovery/decision/v1`. DP-19 is the composite route through which the approval queue and the decision-log query are reached by the screens; this story adds no route and serves no screen of its own.

The two platform H dependencies of the table — H RWB-PLT-E1027-CON and H RWB-PLT-N001-CON — are not in the metadata rows of this story, which name None and RWB-S7-E6028-CON; they are the dependencies the DP table adds and they are recorded in GAP-1312 and ASM-2325. Both are platform CON stories of wave 0, so neither blocks the build and **Ready to start stays Day 1**. The same row carries the two consumed operations that no pattern names, the P4 delegation answer and the P4 authorise call, and the P3 case read the scope filter is applied to.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ApprovalRaiseController | Controller | `POST /approvals` with the shape and idempotency validation, the 201 answer and the problem mapping for 401, 409, 422 and 503 |
| ApprovalController | Controller | `GET /approvals` and `GET /approvals/{approvalId}` with the guard, the level filter, the scope and the page |
| ApprovalDecisionController | Controller | `POST /approvals/{approvalId}/approve`, `/return` and `/refuse` with the guard, the preparer rule, the reason rule and the answers of T-A.2 |
| DecisionLogQueryController | Controller | `GET /decision-log` and `GET /decision-log/{entryId}` with the guard, the filters, the scope and the page |
| ApprovalValidationService | Service | The code, capability area, level and status lists read as reference data, and the refusals with MSG-P7-009 |
| DoaLimitClient | Adapter | The P4 delegation answer, one hop with a 2 s timeout and a breaker; returns the level, the row id and the version in force and never a computed limit |
| ApprovalRaiseService | Service | One transaction: the routing record, the `approval` row and the outbox rows, or nothing; maps the no-limit answer to HELD_NO_LIMIT and MSG-P7-010 |
| ApprovalDecisionService | Service | One transaction: the record of the decision, the status and the `decision_log_id`, and the outbox rows; maps the failure to 503 with MSG-P7-003 |
| ChainWriter | Service | Reads the head of the chain under the append lock, computes the entry hash over the canonical form, and builds the previous hash and the sequence number |
| LedgerIngestConsumer | Consumer | The `DecisionRecorded` consumer: inbox dedupe on the event id, one append per record, the registry check that raises a gap and never invents a row |
| LedgerQueryService | Service | The ledger page and the single entry, with the scope filter applied to the case read |
| AccessCheckClient | Client | The authorise answer behind the four reads and the three decisions, with the cached decision of the right |
| CaseScopeClient | Client | The P3 case read that gives the owner, team, region and product group of the scope filter |
| RuleRowRegistryService | Service | Writes and reads the two registry rows of R-WO-12 and R-WO-32, and resolves an entry's rule id and version |
| ApprovalOutbox | Library use | The three outbox rows in the same transaction as the rows they announce (DP-03) |

**Database and migrations**

- Writes `approval`, `decision_log_entry`, `rule_row` and the outbox, inbox and idempotency objects of the library, all in schema `rwb_decision`; reads no other schema.
- The `approval` baseline belongs to the approvals slice of this service (legacy RWB-E2-013) and the `decision_log_entry` baseline, its append-only trigger and its grants belong to the decision-log store slice (legacy RWB-E1-008); this story rebuilds neither.
- Migration in this story, in the per-service Flyway sequence: `V6028_1__approval_writeoff_sale.sql` adds the unique key `ux_approval_source ON approval (case_id, decision_code, source_type, source_ref)` so one pack gives one item, the index `ix_approval_status_level ON approval (status, approval_level, due_at)` for the level read of `GET /approvals`, the index `ix_declog_case_decided ON decision_log_entry (case_id, decided_at DESC)` for the ledger read of one case, the unique key `ux_declog_ingest ON decision_log_entry (idempotency_key) WHERE idempotency_key IS NOT NULL` for the ingest, and the unique key `ux_rule_row_version ON rule_row (rule_id, rule_version)`.
- No row is updated and no row is deleted by this story on the ledger; the update path of the store does not exist and the delete path does not exist. The approval row is updated only by the three decisions, under the optimistic lock of the version column.

**Configuration and reference data**

- LOV-DECISION, LOV-CAPABILITY, LOV-APPROVAL-LEVEL, LOV-APPROVAL-STATUS and LOV-PRODUCT are read with the version in force; the default ruling puts reference data with `rwb-case` (P3) and this story consumes the list values and never carries them as constants. No pattern of this key adds the reference-data contract as a named dependency, so the list values are read against the published contract or its fake and the dependency is carried in GAP-1312.
- The delegation table, its rows, its version label and its item numbering are `rwb-access`'s; this story stores what the answer returns.
- The due time of an item, the base value of `escalation_level` and the page size of the two reads are parameters or values of their owners and are Not specified in the source documents (GAP-1311; ASM-2321); the story writes no default for them.
- The `rwb-decision` login of DP-02, the flyway user and the outbox relay identity are environment configuration and not values of this story.

**Build steps**

1. The migration `V6028_1__approval_writeoff_sale.sql`; test that a second item for the same pack and a repeated ingest of one event id are refused by the constraints (BR1, BR10).
2. `DoaLimitClient` over the P4 answer with the timeout and the breaker, and the HELD_NO_LIMIT path; tests for AC1 and AC6 (X9).
3. `ChainWriter` and `RuleRowRegistryService`; test the seeded chain of 100 records, the first record with the previous hash of 64 zeros, and the resolution of R-WO-12 and R-WO-32 (AC1, AC8).
4. `ApprovalRaiseService` and the fail-closed raise transaction; tests for AC1 and X1.
5. `ApprovalController`, `ApprovalDecisionController` and `ApprovalDecisionService`; tests for AC2, AC3, AC4, AC5 and AC7 (X2 to X7).
6. `LedgerIngestConsumer` with the inbox dedupe, the registry gap and the chain append; tests for AC8 (X10, X11).
7. `DecisionLogQueryController` and `LedgerQueryService` with the authorise answer and the scope filter; tests for AC2 and AC8.
8. The idempotency path: a repeated raise and a repeated decision return the first answer and consume no second sequence; tests for AC3.
9. The privacy test: the approval, the records, the three event payloads and the log entries carry no name, e-mail address, mobile number, national identity number or account number.

**Done when.** The tests in section 16 pass, the contract tests of RWB-S7-E6028-CON stay green, and a SIT day shows one approval item per above-limit pack at the level of the delegation answer with its row and version, an approve, return and refuse that each write one record and one status, a pack whose decision no limit covers held with MSG-P7-010, no status change and no record when the record cannot be written, one ledger entry per write-off record of R-WO-12 and R-WO-32 with its rule version, and no personal data in any item, record, event or log.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P7-003 | The decision record of the item cannot be written, so the raise or the decision does not happen | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the raise and on the three decisions |
| MSG-P7-002 | The approver prepared the item | You prepared this decision, so you cannot approve it. | This story, on the three decisions, as 409 |
| MSG-P7-001 | The delegation answer of the business date places the item above the caller's level | This needs approval at level {level}. It has been sent to {approver}. | This story, on a decision whose terms moved the level (FSD P7 v3 A2.15 VR-P7-015-1); the change of terms itself is A2.17's and out of scope |
| MSG-P7-009 | A decision code, a capability area, a status or a level is not a value of its list | Not specified in the source documents (GAP-1311; ASM-2321) | This story, on the validation; the FSD names only the identifier and the field |
| MSG-P7-010 | No row of the delegation table covers the decision | Not specified in the source documents (GAP-1311; ASM-2321) | This story, on the HELD_NO_LIMIT path, as an incident to RW-RISK |
| MSG-GEN-001 | A raise has no source item or no amount, or a return or a refuse has no reason | Enter {field}. | This story, on the validation of the raise and of the three decisions |
| MSG-GEN-004 | The item is no longer WAITING, or two decisions arrive at once | Someone else changed this record. Reload it to see their change. | This story, on the optimistic lock of the item |
| MSG-P4-002 | The caller holds no Decision log right or no right in the capability area | You cannot {action} here. Your role does not include it. | This story, through the authorise answer |
| MSG-P4-003 | The item or the case is outside the caller's scope | This case is not in your scope. | This story, through the authorise answer and the case read |
| MSG-S7-001 | The scan is on hold until Finance publishes the tax criteria | The scan is on hold until Finance publishes the tax criteria. | `rwb-writeoff`, on the scan; this story produces no population until it clears and holds no text of it |

MSG-S7-001, MSG-GEN-001, MSG-P4-002 and MSG-P7-003 are copied unchanged from the legacy story RWB-E6-028 section "Validation and messages"; MSG-P7-001, MSG-P7-002, MSG-P7-009 and MSG-P7-010 are the message identifiers FSD P7 v3 A2.15, A2.16 and A2.5 name, and the texts of MSG-P7-009, MSG-P7-010 and MSG-P7-011 are not written out in any source this story may read, so the placeholder stands for those. Thai text for each message follows decision DL10, which is open and assumed under ASM-2250, ASM-2357, ASM-2377 and ASM-2863.

### 15. Screens and states

No screen is built in this story. SCR-27 Write-off proposal with its states — scan, proposed, in committee, approved — is the legacy screen of RWB-E6-028 and belongs to RWB-S7-E6028-APP and the Epic 8 screen stories; the approval queue screen and the decision-log query screen that read this story's operations are their own slices of this service, and the composite route of DP-19 is used and not extended.

| Where | State | What the reader sees |
|---|---|---|
| `POST /approvals` | 201 Raised | The approval reference and the record reference, with the level, the delegation row, the limit version and the due time |
| `POST /approvals` | 201 Held | An item at HELD_NO_LIMIT, an incident with MSG-P7-010, no role queue and no level |
| `GET /approvals` | One page | The items of the caller's level and scope with decision, product, amount, level, limit version and age; never an item the caller prepared |
| `GET /approvals/{approvalId}` | One item | The routing details: level, delegation row, limit version, due time, status, source item and record reference |
| `POST /approvals/{approvalId}/approve` | 200 APPROVED | The record reference, the final call, the approver and the level applied |
| `POST /approvals/{approvalId}/return`, `/refuse` | 200 RETURNED or REFUSED | The approval with its status, its reason and its record reference |
| `POST /approvals/{approvalId}/approve` | 409 or 422 | MSG-P7-002 for the preparer, MSG-GEN-004 for an item no longer WAITING, MSG-GEN-001 for a missing reason, and nothing written |
| `POST /approvals`, the three decisions | 503 | MSG-P7-003 and nothing written; the item stays where it was |
| `GET /decision-log`, `GET /decision-log/{entryId}` | One page or one entry | The routing record of R-WO-12, the record of each decision and the collected records of R-WO-12 and R-WO-32, with rule id, rule version, final call, approver, decided time and the two hashes |
| `GET /approvals`, `GET /decision-log` | 403 or 404 | MSG-P4-002 for a role without the right, MSG-P4-003 for an item or a case out of scope |

The states of the approval item are the five values of LOV-APPROVAL-STATUS; the four legacy screen states are S7's and are not restated as this item's. The empty, loading, error and no access states of SCR-27 are Not specified in the source documents (CG-ALL-7468), because Screen Specifications v1 gives none of them. The escalation of an overdue item is carried inside WAITING through escalation_level, not as a sixth status, and is the escalation slice's (GAP-1311).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-028-01 | AC1, AC2, AC3, BR1, BR2, BR4, BR6, BR12 | Component | The raise, the level read and the approve of the pack of case `RW-2027-000730`, with the delegation answer at level `L6`, row `DL-2.1.10-L6` and version `DOA-2026.11` |
| TC-E6-028-02 | AC1, AC6, BR2, BR3 | Contract | The P4 delegation answer as the only source of the level, and the answer that covers nothing for HIRE_PURCHASE, with the item held at HELD_NO_LIMIT and MSG-P7-010 |
| TC-E6-028-03 | AC8, BR10, BR11 | Contract | The `DecisionRecorded` of R-WO-32 on `rwb.decision-record.v1`, delivered twice with one event id, and the registry resolution of the rule id and version |
| TC-E6-028-04 | AC5, AC7, BR7, BR8 | Component | A return and a refuse without a reason, and the decision-record library failing on an approve; 422 with MSG-GEN-001 and 503 with MSG-P7-003, nothing written |
| TC-E6-028-05 | AC2, AC4, BR5, BR12 | Component | A caller without the Decision log right, an item of the out-of-scope case `RW-2027-000731`, and `approver.user01` approving an item they prepared |
| TC-E6-028-06 | AC7, BR8, BR9 | NFR | The decision-record write forced to fail on an approve; no status change, no record, no outbox row, no sequence consumed and the chain at its last entry |
| TC-E6-028-07 | BR7, BR8 | Component | A return reason at the 1,000-character limit of BR7 accepted and one character over it refused, with each record written once in `decision_log_entry` and `approval` |
| TC-E6-028-08 | AC9, BR13, BR14 | Component | The approval, the decision record, the outbox row and the log line of case `RW-2027-000730` checked for personal data fields, and any write to the case, task, timer or delegation row |
| TC-E6-028-09 | AC10 | Component | A call to each provided operation with no valid credential, answered 401 with nothing read or written |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The legacy TC-E6-028-01 to TC-E6-028-06 are the six tests of the legacy key; this slice keeps their identifiers for the approval and ledger half and the `-ITG` copies of the same identifiers are RWB-ITG-E6028-ITG and are not written here. The legacy level System maps to Component or Contract as the rows show, Access to Component and Resilience to NFR. The write-off read and the write-off sale operation do not exist in the sources, so the population is asserted through the case read, the decision log and DP-09; the synthetic keys, amounts, business date, committee limit and gate of the debt sale handover harness are held as configuration and agreed at the wave 4 entry check (GAP-0458).

### 17. Guardrails

- No business value in code: the decision code, the capability area, the level list, the status list, the product list, the final calls, the message texts, the due time and the escalation base are reference-data rows, message-standard rows or values of an owner's answer; nothing of them is a constant here.
- No limit is computed and no delegation row is copied: the level, the row and the version arrive from P4 at the moment of the decision and are stored as they arrive (DP-01, TSD P7 v2 A2.24).
- No personal data in the approval, the record, the event payload, the trail, the tests or the logs: case and write-off identifiers, a decision code, a rule id and version, a level, an amount, a status, a reason and a user reference only.
- No read of another service's tables: the write-off arrives on its contract and its records on the shared topic, the case on the P3 read, the delegation and the right on P4's answers; no `write_off`, `recovery_case`, `delegation_limit`, `role` or `permission` row is copied into `rwb_decision`.
- ACE data only through the owner's contract or `v_ace_*` views: this story reads no ACE data at all.
- No record without its event and no event without its record: each record, its chain link and its outbox row commit in one transaction, and a failure changes nothing (R-UNI-39).
- Append only and hash chained: no update path and no delete path exist on the ledger, the sequence number is never reused, and a wrong record is corrected by a new record naming the one it corrects (REQ-DRI-002).
- One item per pack and one record per decision: the unique key of the source and the idempotency key make a second item and a second record impossible, and a repeated call returns the first answer.
- One base, one topic, one queue: `/api/recovery/decision/v1`, `rwb.decision.events.v1` and the `rwb-decision` queue in namespace `rwb-recovery`, with the shared topic `rwb.decision-record.v1` for the record event (DP-13).
- One hop and 2 s on every call, with a breaker per downstream; a missing delegation answer never produces an item on a guessed level.
- The record path is never gated by a feature flag and never skipped for speed: an approval without its record is a defect, not a degraded mode.
- This story moves no case, starts no workflow and registers no Schedule: the scan, the pack, the committee, the posting and the sale stay with their owners.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S7-003 | The committee decision to approve, reject or defer is recorded against each account | Business Requirements Program, section 5.14 | FEAT-WOF-16; legacy FEAT-WOF-16 | 06 Take over and own the case | R-WO-12, R-WO-13, R-WO-15 | TC-E6-028-01, TC-E6-028-02 |
| REQ-S7-006 | Post charge-off treatment is set by rule, including the sale of a charged-off population | Business Requirements Program, section 5.14 | FEAT-WOF-16; legacy FEAT-WOF-16 | 06 Take over and own the case | R-WO-29, R-WO-32 | TC-E6-028-03 |
| NFR-034 | Every action carries the rule version applied and the approver who allowed it | TSD P7 v2 T7 | FEAT-DRI-04; legacy FEAT-WOF-16 | 06 Take over and own the case | R-WO-12, R-WO-32 | TC-E6-028-01, TC-E6-028-03 |
| NFR-033 | Every decision is reproducible from the log, including the versions and the inputs used | TSD P7 v2 T7 | FEAT-DRI-01, FEAT-DRI-03 | 06 Take over and own the case | R-WO-12, R-WO-32 | TC-E6-028-03, TC-E6-028-06 |

| Legacy reference | Where it is kept |
|---|---|
| One approval where the limit requires it, on the way to the sale | Sections 1, 2, 4, 7 (AC1, AC3), 8 (BR1, BR6) |
| Rule R-WO-12 and the escalation to the credit approval committee | Sections 1, 4, 7 (AC1, AC6), 8 (BR2, BR3, BR4), 9 |
| Rule R-WO-32 and the sale of the charged-off population | Sections 1, 7 (AC8), 8 (BR10, BR11), 9, 11 |
| MSG-P7-003 and the block when the record cannot be written | Sections 5 (X6), 7 (AC7), 8 (BR8), 14 |
| MSG-P4-002 and the right in the write-off and posting capability area | Sections 5 (X7), 7 (AC2), 10, 14 |
| MSG-S7-001 and the scan that holds the population | Section 14; the scan is S7's and section 19 |
| The screen SCR-27 Write-off proposal and its four states | Section 15; S7's and the Epic 8 screen stories' |
| Legacy test cases TC-E6-028-01 to TC-E6-028-06 | Section 16 |
| Legacy key RWB-E6-028, story RWB-P7-E6028-APP, contract RWB-S7-E6028-CON | Metadata, sections 3 and 12 |
| Decoupling patterns DP03, DP13, DP19 | Metadata, section 13 |

The other slices of the key answer the rest: RWB-S7-E6028-CON the write-off contract and the shape of the raise; RWB-S7-E6028-APP the scan, the pack, the committee, the case states, the posting and the local records of R-WO-12 and R-WO-32; S6 `rwb-debtsale` the lot, its accounts and the transfer; RWB-ITG-E6028-ITG the cross-service harness and the `-ITG` copies of the test cases.

### 19. Out of scope

- The approval letters, the sale itself and the population: the write-off scan JOB-16 and its tax criteria hold, the committee pack of three working days, the committee agenda and meeting, the committee decision operation of `rwb-writeoff`, the escalation state on the case, the posting to ALS and the general ledger, the provision release, the finance feed and the post charge-off placement decision — RWB-S7-E6028-APP and RWB-S7-E6028-CON.
- The debt sale route: the lot, its accounts, the data room, the buyer qualification, the bids, the award, the data transfer, the derecognition and the general ledger posting of the sale — S6 `rwb-debtsale` and its own stories, with `POST /api/recovery/debtsale/v1/debt-sale-lots` as the operation RWB-ITG-E6028-ITG calls.
- The delegation table, the DoA item numbering, the level holders and substitutes, the role model, the scope, the masking policy and the authorise answer: P4 `rwb-access`; this story consumes the delegation and authorise answers and holds no rule of either.
- The case record, the case status, the case list, the timers and the placement timer: P3 `rwb-case`.
- SCR-27 Write-off proposal and its four states: RWB-S7-E6028-APP and the Epic 8 screen stories; the approval queue and decision-log screens are the other slices of this service.
- The escalation of an overdue item, the change of a recommendation before approval and the coded override: FSD P7 v3 A2.17, A2.19, A2.20 and A2.21, and their slices of this service.
- The decision-log store of this service — the append-only trigger, the grants, the chain verifier and the chain check JOB-14 at 02:00: the store slice (legacy RWB-E1-008) and the service baseline.
- The rule package registry beyond the two rows of R-WO-12 and R-WO-32 — the authoring, the dry run, the four-eyes approval, the promotion JOB-20 and the rollback: RWB-P7-E2042-APP and the registry slice.
- The daily ledger seal to immutable storage and the lake copy: the seal is the store slice's and the lake is removed (DP-17).
- The cross-service proof of the whole journey and the `-ITG` copies of the test cases: RWB-ITG-E6028-ITG.
- The two platform H stories RWB-PLT-E1027-CON and RWB-PLT-N001-CON, the DB, INF and OPS stories of this key, the Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability.

The names of the level holders and substitutes and the parameter values of the delegation table are data of their owners, and no date is changed by this story: the release 30 April 2027 is copied unchanged and stays tentative.
