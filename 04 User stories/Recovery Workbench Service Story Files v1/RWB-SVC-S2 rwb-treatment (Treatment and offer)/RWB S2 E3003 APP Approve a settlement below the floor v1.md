# RWB-S2-E3003-APP Approve a settlement below the floor

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E3-003 for rwb-treatment. The below-floor approval leaves the monolith's S2 service in the one `recovery` schema and becomes the below-floor branch of `TreatmentWorkflow` on this service's own task queue, with the second signature taken through the workflow kit's `ApprovalWorkflow` started as a child on rwb-decision's queue, the delegation level and the floor read as values in force, the outcome written on the treatment row in the same transaction as the local decision record (DP-03), and `rwb.treatment.TreatmentApproved.v1` published on the treatment topic when the second signature is given. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3003-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-003 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S2-N |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S2-E3003-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **recovery developer (RW-TRIBE)**, I want **the below-floor approval of a settlement or a deed in lieu to run as the below-floor branch of `TreatmentWorkflow` on task queue `rwb-treatment` — the check of the offer or transfer price against the floor in force, the second-signature request carried by the workflow kit's `ApprovalWorkflow` started as a child on rwb-decision's queue with the gap to the floor and the delegation level read as values in force, the recording of the second signature or its refusal with the reason code `price_below_floor`, the rule outcomes R-DIL-15, R-DIL-17 and R-SET-05 reported to the parent `CaseWorkflow`, the local decision record written in the same transaction, and `rwb.treatment.TreatmentApproved.v1` published on the treatment topic when the second signature is given**, so that **a price below the floor reaches the approver or the committee the matrix names in days instead of weeks, the decision is provable with the rule version and the delegation version that made it, and no case status, no case table and no delegation table moves into this service**.

This is the application slice of legacy RWB-E3-003. It owns:

- the four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages and data rows they depend on;
- the below-floor branch of `TreatmentWorkflow`, the stage child of `CaseWorkflow` on rwb-case, with the four activities `checkFloor`, `requestSecondSignature`, `recordAndApply` and `publishApproved`;
- the `ApprovalWorkflow` child started on rwb-decision's queue with the request the workflow kit builds, and the mapping of its answer onto the treatment row;
- the treatment columns that hold the outcome — `approval_level` (DF-TRT-011) plus the final call, the approver role, the decided-at time and the reason code — in schema `rwb_treatment`;
- the local decision record written through RWB-PLT-E1027-CON in the same transaction as the treatment change (DP-03);
- the entry of the branch from the offer the officer prepares, re-tested by the stage against the floor in force, and the screen path of SCR-14 and SCR-15 through the gateway-bff composite route (DP-19).

It does not own: the published element set of the approved treatment, the event envelope and the fakes, which are RWB-S2-E3003-CON; the treatment record itself, which is RWB-S2-E3001-APP; the offer inside the range and the offer document sent to the customer, which are RWB-S2-E3002-APP; the case status and the case table, which stay rwb-case's and reach the stage on the case signal the parent forwards (ASM-3062); the approval record `approval`, the delegation table `delegation_limit` and the approval routing features, which are rwb-decision's and rwb-access's; the approval matrices themselves, which are data rows those services own; and the deployment, dashboards and alerts, which are this legacy key's DevOps story.

### 2. Business rationale

Epic 3 today takes 23 to 26 days per restructure, settlement or deed in lieu and is tracked by hand (FSD S2 A2.3.1). The long step is not the decision: it is the hand-carried approval. A price under the floor is negotiated in the Workbench, sent by mail or by hand to the person or the committee the matrix names, and comes back days later, so the offer clock and the customer wait. REQ-S2-004 asks that settlement terms be negotiated inside a rule-set range and that anything outside the range need approval; the FSD enters the same requirement as FEAT-TRT-03 and as the validation rule VR-S2-003-1 with MSG-S2-001.

The monolith answered this inside one process: the S2 service compared the offer to `floor_price`, called the approval routing of FEAT-APD-01 in the same connection, wrote `decision_log_entry` in the same transaction and moved the case status in the same table. In the 19-service target each of those four facts belongs to a different owner. The case status is rwb-case's and reachable only on the case signal that `CaseWorkflow` forwards to its stage child (ASM-3062). The approval is the workflow kit's `ApprovalWorkflow`, started as a child on rwb-decision's queue (Architecture v5 slide 18, "TMP Decision: child: approval"; Temporal and Drools Design slides 6 and 13), and the approval record `approval` is P7's. The delegation limit is rwb-access's `delegation_limit`, which the approval request carries as a value in force (ASM-3068; Ownership Map row `delegation_limit`, owner P4). The decision record is the platform library's, written locally in this service's schema (DP-03).

What the business keeps is the rule, not the code. R-SET-05 routes a settlement offer to the approver with the gap to the floor when `offer_amount < floor_price`, to AWAITING_APPROVAL_SET with a three-working-day clock. R-DIL-15 routes a transfer price for a second signature when `transfer_price < floor_price`, to AWAITING_SECOND_SIGNATURE with a three-working-day clock, and R-DIL-17 returns the case to the route decision with reason `price_below_floor` when `final_call = rejected`. The Temporal and Drools Design slide 6 shows why this matters: a settlement of THB 2,400,000 principal at a 20% loss routes to an L6 approver under delegation version DOA-2026.11 and to an L5 approver under DOA-2027.01 from 2 January 2027 — a change of table and date, no code change, no release, and the version used is written with the answer. That is exactly the value this story has to preserve while the code around it is split: the floor, the level, the limit and the reason code are values in force, never constants (BR-S2-003).

Serves REQ-S2-004 (settlement terms inside the rule-set range, anything outside needs approval) and, for the deed-in-lieu form, the same rule set's R-DIL-15 and R-DIL-17. No business value moves into code: the floor, the levels, the limits, the clock and the reason code stay data rows of their owners.

### 3. Preconditions

- RWB-S2-E3003-CON is published: the treatment element set of an approved below-floor price (`approvalLevel`, `approverRole`, `finalCall`, `decidedAt`, `reasonCode`), the `rwb.treatment.TreatmentApproved.v1` envelope on `rwb.treatment.events.v1`, the rule that no new table is created for the second signature, the compatibility rule and the fakes are baselined and handed to this story (H).
- RWB-PLT-E1027-CON is published (DP-03): `DecisionRecordWriter.record(DecisionRecord)` with propagation `MANDATORY`, the refusal `DecisionLogRecordInvalidException` with MSG-P7-009 and its field, and `DecisionLogUnavailableException` with MSG-P7-003 (H).
- RWB-PLT-N001-CON is published (DP-19): the gateway-bff composite route that carries SCR-14 and SCR-15, shows the approval item of rwb-decision and calls this service, one hop (H).
- RWB-S2-E3001-APP is done: `treatment` exists in schema `rwb_treatment` with DF-TRT-001 to DF-TRT-033, and its own migration sequence is the only place a column is added.
- RWB-S2-E3002-APP is done for the settlement form: the settlement range and the offer of the case are on the treatment, so there is an offer to compare with the floor; for the deed-in-lieu form the transfer price is set by R-DIL-13 before this branch can run.
- `rwb.decision.RulePackageInForce.v1` (EV-30) is consumed and the SETTLEMENT and DEEDINLIEU packages are in force, with their version labels and checksums, evaluated by the embedded Drools runtime (ASM-3063).
- The workflow kit and the outbox and inbox library are service-template capabilities (ASM-3064): the stage child, the `ApprovalWorkflow` child, the signal handling and the outbox are taken from the kit and are not built here.
- The access guard is the platform guard library's (ASM-3064); this story declares the capability area "Treatment and offer" and the rights the branch exercises — U for the officer who prepares the below-floor offer and RA for the approver who answers it — and the roles that hold them as TSD S2 T6.1 lists them.
- rwb-access owns `delegation_limit`, the DoA levels L1 to L6, their holders and substitutes, and the valid-from dates; rwb-decision's `ApprovalWorkflow` reads them for the routing date. How rwb-treatment learns the level and the limit, and which level a below-floor settlement takes, is not stated by any source document and is taken as the working read of ASM-3068 (GAP-1872).
- The floor in force, the three-working-day approval clock of R-SET-05 and R-DIL-15, and the reason codes `price_below_floor` and `below_floor_refused` are values in force of their owners; this story holds no copy of any of them.
- No approval of this story is needed to build against a Draft contract baseline; RWB-S2-E3003-CON tags the version when its tests pass.

### 4. Flow

1. The parent `CaseWorkflow` on rwb-case forwards the case signal to the running `TreatmentWorkflow` child on `rwb-treatment`; the signal carries the case status and the case facts the stage works with, and the status stays rwb-case's (EV-29; ASM-3062).
2. The stage holds a treatment of type SETTLEMENT in WITH_FCR_OFFICER_SET with an offer prepared, or of type DEED_IN_LIEU in TRANSFER_PRICE_SET with a transfer price set (R-DIL-13).
3. Restructuring officer or product head: prepares the offer or the transfer price on SCR-15 through the gateway-bff composite route; the guard checks capability area "Treatment and offer", right U, and the scope, and the offer answer carries `belowFloor`, the floor and `gapToFloor` (RWB-S2-E3002-CON).
4. `checkFloor` activity: reads the floor in force and compares it with the offer amount (R-SET-05) or the transfer price (R-DIL-15). At or above the floor the stage answers the inside-range path and this branch ends; below the floor it continues.
5. `requestSecondSignature` activity: computes the gap to the floor and starts the `ApprovalWorkflow` child on rwb-decision's queue with the treatment, the case, the amount, the gap and the decision code D6.4; the child routes to the level the `delegation_limit` row names for the product, the decision and the amount on the routing date, and returns its level, its limit version, its status and its final call as the child workflow's result (ASM-3068).
6. The stage reports the rule outcome to the parent: R-SET-05 with the AWAITING_APPROVAL_SET status for a settlement, R-DIL-15 with the AWAITING_SECOND_SIGNATURE status for a deed in lieu. The parent moves the case status; this service writes no case table.
7. `recordAndApply` activity, one transaction: the treatment row takes `approval_level`, the final call, the approver role, the decided-at time and the reason code; the decision record is written through `DecisionRecordWriter.record` (decision code D6.4, the rule ID and the rule version of the package that routed the answer, the delegation version in the inputs reference, the recommendation, the approver and the level, the final call, the outcome and the decided-at time); the outbox row is written in the same transaction.
8. On a given second signature: R-SET-06 releases the offer to the customer, R-DIL-16 generates the documents and puts the offer to the customer. `publishApproved` activity: the outbox relay publishes `rwb.treatment.TreatmentApproved.v1` on `rwb.treatment.events.v1` with key `caseId` (EV-10; consumers rwb-comms and rwb-payment).
9. On a refusal: R-SET-07 records the reason and the gap and the case reaches DECLINED_BY_APPROVER_SET, then R-SET-08 returns it to the route decision with reason `below_floor_refused`; for a deed in lieu R-DIL-17 returns it to RETURNED_TO_ROUTE_DIL with reason `price_below_floor`. No `TreatmentApproved` event is published.
10. A redelivered case signal, a retried activity or a second offer answer for the same treatment answers the open approval and starts no second child: the rejection and the workflow ID of this treatment carry the idempotency.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without right U prepares the below-floor offer, or a role without RA answers the approval | 403 from the guard on the offer operation; the refusal is logged and nothing changes; no approval item is raised for a role without RA | MSG-P4-002 | AC1, TC-E3-003-05 |
| X2 | The decision record cannot be written | The transaction rolls back: no treatment column, no outbox row, no status report to the parent, nothing changes | MSG-P7-003 | AC4, TC-E3-003-06 |
| X3 | The record is refused for a missing field | The transaction rolls back and the field is named in the service log and the incident | MSG-P7-009 | AC4 |
| X4 | The level the DoA row names has no holder and no substitute | The child workflow passes the item one level up at once and answers with the covering level; the treatment records that level | None | AC2 |
| X5 | No delegation row covers the decision, the product and the amount | The child answers HELD_NO_LIMIT and an incident is raised; the case does not move and the gap is shown on SCR-15 | None | AC2 |
| X6 | The floor in force is stale or missing for the case | The stage holds the branch, names the missing value and raises a task for the owner; no approval is requested with an unknown floor | MSG-GEN-001 | AC1 |
| X7 | The approval is refused | The refusal is recorded with its reason, the case is reported back to the route decision and no event is published | None | AC3, TC-E3-003-03 |
| X8 | The case signal arrives again, or a second offer answer arrives, while the approval is open | The open approval is answered and no second child is started; the first answer stands | None | AC1, AC2 |
| X9 | The approval child does not answer inside the clock | The escalation of the approval routing applies on rwb-decision's side and the case does not move; the stage keeps waiting | None | AC2 |

X1 to X4 and X7 are the exception paths of RWB-E3-003 carried onto the split: the access refusal, the record failure, the record refusal and the refusal of the second signature. X5, X6, X8 and X9 are the paths of the target: the DoA answer that covers nothing, the floor as a value in force that a business person may change, the workflow kit's idempotency, and the clock of R-SET-05 and R-DIL-15 which stays with the owner of the approval.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published element set and fakes of RWB-S2-E3003-CON, the decision-record contract and the gateway route; no live rwb-decision, rwb-access or rwb-case is needed to start, and the case status arrives on a mocked signal |
| Negotiable | The activity names, the input record of the child workflow and the shape of the treatment's four extra columns are this story's choice; the rules, the reason code, the floor and the three-working-day clock are fixed by their owners' data |
| Valuable | A price under the floor reaches the named approver or committee in days, with the level, the limit version and the rule version written into the record |
| Estimable | One stage branch, four activities, one child workflow call, four treatment columns, one operation branch and one event |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion runs on synthetic treatments, offers and floors through the contract fakes, plus one component test of the branch entry and the guard |

### 7. Acceptance criteria

```gherkin
Feature: Approve a settlement below the floor

  Scenario: AC1 Approve a settlement below the floor (legacy RWB-E3-003 AC1)
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then routes a settlement below the floor price to the approver or the committee named in the matrix
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIL-15 (legacy RWB-E3-003 AC2)
    Given the rwb-case contract mock returns case status TRANSFER_PRICE_SET
    Given a case in state TRANSFER_PRICE_SET
    When price below floor
    Then route the price for a second signature
    Then the case moves to AWAITING_SECOND_SIGNATURE

  Scenario: AC3 Rule R-DIL-17 (legacy RWB-E3-003 AC3)
    Given the rwb-case contract mock returns case status AWAITING_SECOND_SIGNATURE
    Given a case in state AWAITING_SECOND_SIGNATURE
    When second signature refused
    Then return the case to the route decision with reason price_below_floor
    Then the case moves to RETURNED_TO_ROUTE_DIL

  Scenario: AC4 Not recorded (legacy RWB-E3-003 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Target reading.** Every one of the four criteria keeps its wording and its values; what changes is where the step runs, who owns each fact and how the answer is proved. The step is no longer a step of the monolith's S2 service in the one `recovery` schema: it is the below-floor branch of `TreatmentWorkflow`, the stage child of `CaseWorkflow` on rwb-case, on task queue `rwb-treatment` in namespace `rwb-recovery` (Architecture v5 slide 18, "TMP  Decision: child: approval"; Temporal and Drools Design slide 13, a parent per case and a child per stage, and slide 18, "Settlement below floor → approval (R-SET-05)" and "Deed below floor: Head of NPA (R-DIL-15)"). "The user acts on the screen" in AC1 is the restructuring officer or the product head acting on SCR-15 in state below floor, reached through the gateway-bff composite route (DP-19), and the "approver or the committee named in the matrix" is the level the `delegation_limit` row names for the product, the decision and the amount on the routing date — L6 or L5 in the slide 6 example, under DOA-2026.11 or DOA-2027.01 — carried by the kit's `ApprovalWorkflow` child on rwb-decision's queue, with the gap to the floor on the request and no limit held here (ASM-3068). "The decision log" of AC1 and "the result ... with the rule version" are the local decision record written through RWB-PLT-E1027-CON in the same transaction as the treatment change (DP-03); `decision_log_entry` is P7's ledger and is neither written nor read here. The statuses of AC2 and AC3 — TRANSFER_PRICE_SET, AWAITING_SECOND_SIGNATURE, RETURNED_TO_ROUTE_DIL — stay rwb-case's: the two added Given lines are answered by the rwb-case contract mock standing in for the case signal, and this story reports the rule outcome to the parent `CaseWorkflow`, which moves the status, and writes no case table (ASM-3062). R-DIL-15, R-DIL-17 and R-SET-05 are evaluated by the embedded Drools runtime against the package version in force announced by `rwb.decision.RulePackageInForce.v1` (ASM-3063), and `price_below_floor` is the reason code in force, never a constant. AC4 is unchanged in words and stricter in reach: the record write joins the caller's transaction and opens none, so a failed append leaves the treatment row, the approval and the case exactly as they were. The guard behind the screen and the operation is the platform guard library's, and this story declares the capability area and the right only (ASM-3064), on the service base `/api/recovery/treatment/v1` (DP-13). The approved answer is announced as `rwb.treatment.TreatmentApproved.v1` on `rwb.treatment.events.v1` with key `caseId` to rwb-comms and rwb-payment (Architecture v5 slide 42 row 10), which no legacy line names because the monolith had no event of its own; the payload has no published shape and is the working read of ASM-3068 (GAP-1872).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A settlement offer below the floor price is routed to the approver with the gap to the floor and moves the case to AWAITING_APPROVAL_SET, with a three-working-day clock | R-SET-05; FSD S2 A2.3.3.1; VR-S2-003-1 |
| BR2 | A transfer price below the floor is routed for a second signature and moves the case to AWAITING_SECOND_SIGNATURE, with a three-working-day clock | R-DIL-15; FSD S2 A2.3.3.1 |
| BR3 | A refused second signature returns the case to the route decision with reason `price_below_floor`; a refused settlement approval records the reason and the gap and returns the case with reason `below_floor_refused` | R-DIL-17; R-SET-07; R-SET-08 |
| BR4 | A granted approval releases the offer to the customer (settlement) or generates the documents and puts the offer to the customer (deed in lieu) | R-SET-06; R-DIL-16 |
| BR5 | The approval routes to the level the delegation of authority names for the product, the decision and the amount on the routing date, and the level and the limit version are written with the answer | REQ-S2-004; Temporal and Drools Design slide 6; DoA 2.1.1 |
| BR6 | No value a business person may change is written in code: the floor, the levels, the limits, the clock and the reason codes are read as values in force with their version | BR-S2-003; FSD S2 A2.3.3.1 |
| BR7 | The approval outcome is recorded on the treatment row as `approval_level` plus the final call, the approver role, the decided-at time and the reason code, and no new table is created for it | GAP-1872; ASM-3068 |
| BR8 | A below-floor approval that cannot be recorded does not take effect: the record joins the caller's transaction and a failed append rolls everything back | R-UNI-39; RWB-PLT-E1027-CON; Principle 5 |
| BR9 | The case status is rwb-case's; this story reports the stage outcome to the parent workflow and writes no case table | DP-01; ASM-3062 |

**Where each rule lives in the target.** BR1 and BR2 are the `checkFloor` and `requestSecondSignature` activities and the R-SET-05 and R-DIL-15 outcomes the stage reports to the parent; the floor, the clock and the rule rows are values in force of rwb-case's reference data, S5's floor price and P7's rule catalogue, read and never copied (BR6). BR3 and BR4 are the same two activities on the refusal and the grant path: the reason code `price_below_floor` for the deed in lieu and `below_floor_refused` for the settlement are reference values in force, not string literals in code. BR5 is the request the kit's `ApprovalWorkflow` builds and the level and limit version it answers with; rwb-treatment never reads `delegation_limit` and holds no limit (ASM-3068). BR6 is served by reading every value from its owner; the only fixed strings in this story are the element and event names of its contract. BR7 is the four columns of the treatment and the absence of a second-signature table. BR8 is `recordAndApply`: the treatment update, the decision record and the outbox row sit in one transaction, and `DecisionLogUnavailableException` (MSG-P7-003) and `DecisionLogRecordInvalidException` (MSG-P7-009) roll it back. BR9 is the signal contract with the parent and the absolute rule that this service names no case table in SQL (DP-01).

### 9. State transitions

None of the states below is this service's to change (ASM-3062). The stage evaluates the rule, records the outcome and reports it to the parent `CaseWorkflow`, and the parent moves the case status in rwb-case. The table therefore lists what the stage asserts on the signal it returns and on the status the case reaches, which is what AC2 and AC3 name.

| From (case status, rwb-case's) | Event | Condition | To (case status, rwb-case's) | Rule |
|---|---|---|---|---|
| TRANSFER_PRICE_SET | PRICE_BELOW_FLOOR | `transfer_price < floor_price` | AWAITING_SECOND_SIGNATURE | R-DIL-15 |
| TRANSFER_PRICE_SET | PRICE_INSIDE_FLOOR | `transfer_price >= floor_price` | OFFER_WITH_CUSTOMER_DIL, inside-range path of the sibling story | R-DIL-14 |
| AWAITING_SECOND_SIGNATURE | SECOND_SIGNATURE_GIVEN | `final_call = approved` | OFFER_WITH_CUSTOMER_DIL | R-DIL-16 |
| AWAITING_SECOND_SIGNATURE | SECOND_SIGNATURE_REFUSED | `final_call = rejected` | RETURNED_TO_ROUTE_DIL with reason `price_below_floor` | R-DIL-17 |
| WITH_FCR_OFFICER_SET | OFFER_PREPARED | `offer_amount < floor_price` | AWAITING_APPROVAL_SET | R-SET-05 |
| AWAITING_APPROVAL_SET | APPROVAL_GRANTED | `final_call = approved` | OFFER_WITH_CUSTOMER_SET | R-SET-06 |
| AWAITING_APPROVAL_SET | APPROVAL_REFUSED | `final_call = rejected` | DECLINED_BY_APPROVER_SET | R-SET-07 |
| DECLINED_BY_APPROVER_SET | DECLINE_RECORDED | Any | RETURNED_TO_ROUTE_SET with reason `below_floor_refused` | R-SET-08 |

Two states of the stage's own object are visible in the outcome: the treatment's `approval_level` is empty while the approval is open and carries L1 to L6 when an approval has decided, and the treatment carries no state machine of its own beyond the LOV-TRT-OUTCOME values that later steps write.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery squad (RW-TRIBE) | Writes the stage branch, the four activities, the child-workflow call and the four treatment columns |
| RW-RESTRUCT, restructuring officer (FCR) | Prepares the below-floor offer or the transfer price and submits it; holds CRUA in "Treatment and offer"; may not approve what they prepared |
| RW-PRODHEAD, product head (Mortgage, HP, SSME) | Approves at the level the matrix names for their product; holds RA |
| RW-CREDCOMM, credit approval committee member | Approves at the level the matrix names as a committee member; holds RA; records the committee resolution reference |
| RW-HEADNPA, Head of NPA | The role R-DIL-15 names as the owner of the deed-in-lieu second signature |
| RW-CASEOWN, RW-GUARANT, RW-SPECIAL | Hold C, R and U in "Treatment and offer" and may read the approved treatment; they do not approve |
| RW-AUDIT, RW-COE | Read the recorded decision and the treatment outcome; they change nothing |
| rwb-decision (P7) | Owns the `approval` record, the `ApprovalWorkflow` on its own queue and the routing of the level; owns the rule packages and their versions |
| rwb-access (P4) | Owns `delegation_limit`, the levels L1 to L6, their holders, substitutes and valid-from dates |
| rwb-case (P3) | Owns the case status and moves it on the stage outcome the parent receives |
| No delegation of authority level applies to this story | The story builds the branch; the level that applies is a data value of the approver's row, never a decision of this code |

No credential, personal name or email address appears in the workflow input, the activity payloads, the event or the logs, which carry treatment and case identifiers, codes, levels, amounts, versions and timestamps only.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-002 | treatment | case_id | Read |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-005 | treatment | proposed_by | Read |
| DF-TRT-006 | treatment | proposed_at | Read |
| DF-TRT-007 | treatment | offer_amount | Read |
| DF-TRT-008 | treatment | haircut_amount | Read |
| DF-TRT-010 | treatment | valid_until | Read |
| DF-TRT-011 | treatment | approval_level | Write |
| DF-TRT-013 | treatment | outcome | Read |
| DF-TRT-014 | treatment | outcome_at | Read |
| (no field ID) | treatment | final_call | Write |
| (no field ID) | treatment | approver_role | Write |
| (no field ID) | treatment | decided_at | Write |
| (no field ID) | treatment | reason_code | Write |
| DF-DEC-001 to DF-DEC-018 | decision_record (library object in `rwb_treatment`) | id, case_id, decision_code, rule_id, rule_version, model_version, idempotency_key, approver_user_id, approval_level, final_call, outcome, decided_at, chain_seq, entry_hash and the rest | Write through `DecisionRecordWriter` |
| DF-REF-018 | delegation_limit (`rwb_access`) | approval_level | Read on the approval request, never from the table |
| DF-REF-001 to DF-REF-015 | rule_row (`rwb_decision`) | rule_id, rule_version, from_state, event_code, condition, target state | Read as the evaluated package, never from the table |

`treatment` is this service's table and the only one this story writes, together with the library's `decision_record` in the same schema (DP-03). The four outcome columns beyond `approval_level` carry no field ID and no column definition in the TSD, which lists DF-TRT-001 to DF-TRT-033 and stops at `approval_level` for the approval facts: their names and types are the working read of ASM-3068 and the gap stays open (GAP-1872). `recovery_case`, `assignment`, `decision_log_entry` and `rule_row` of the legacy data table belong to rwb-case, rwb-case, rwb-decision and rwb-decision: the case facts this story needs arrive on the case signal, the ledger is P7's and is neither written nor read here, and the rule rows arrive as the evaluated package of the service's Drools runtime. Field IDs are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). This story declares no operation of its own. The branch is entered when the officer prepares the offer or the transfer price on the offer operation `POST /treatments/{treatmentId}/offer`, whose surface and below-floor answer — `belowFloor`, the floor in force and `gapToFloor` — are RWB-S2-E3002-CON's. The second signature is answered in the approval item that gateway-bff shows from rwb-decision and reaches this stage as the child workflow's result, and the treatment with its approval element is read on the treatment read of RWB-S2-E3001-CON. No `/submit` form is published: API Specification v4 and TSD S2 T-A.1 API-S2-004 name one, and the source precedence of Template and Rules §R3 puts the Architecture v5 slide 18 form `/offer` first, which RWB-S2-E3002-CON records as superseded.

| Element this story reads from the offer answer | Source | Use |
|---|---|---|
| `belowFloor`, the floor in force, `gapToFloor` | RWB-S2-E3002-CON | The reason the officer sees on SCR-15; the branch re-tests the price with `checkFloor` and never trusts the flag as the trigger |
| The treatment reference and the stored terms | RWB-S2-E3001-CON | The offer amount or transfer price and the treatment the outcome is written to |

#### 12.2 REST operations consumed

None. This story calls no other service: the case status and the case facts arrive on the case signal forwarded by the parent `CaseWorkflow` (EV-29; ASM-3062), the approval is a child workflow of the kit on rwb-decision's queue and not a REST call (ASM-3068), the delegation level and limit are carried on that request, and the rule version arrives as an event. The offer operation of section 12.1 is this service's own and is called by the officer through gateway-bff, not by this story. The Work Package lists no contract dependency for this story, and none is added.

#### 12.3 Events published

| Event | Topic | Key | Payload carries | Purpose |
|---|---|---|---|---|
| `rwb.treatment.TreatmentApproved.v1` | `rwb.treatment.events.v1` | `caseId` | treatmentId, caseId, treatmentType, offerAmount, approvalLevel, approverRole, finalCall, decidedAt, ruleId, ruleVersion | EV-10: tells rwb-comms to issue the approved offer and rwb-payment to expect the settlement or the proceeds (Architecture v5 slide 42 row 10) |

| Envelope element | Value |
|---|---|
| Mode | CloudEvents 1.0, binary mode |
| ce_specversion | 1.0 |
| ce_type | rwb.treatment.TreatmentApproved.v1 |
| ce_source | rwb-treatment |
| ce_subject | The case ID of the approved treatment |
| ce_id and traceparent | The event identifier and the W3C trace context of the transaction that wrote it |
| Payload | Identifiers and facts only; no personal data, no free text and no document content |

The event is written to the outbox in the same transaction as the treatment change and the decision record, and the relay publishes it (ASM-3064). Its name follows the naming rule of Template and Rules §R4 and the topic is the service's own `rwb.treatment.events.v1`. The payload has no published shape: Architecture v5 slide 42 names the producer and the consumers, and the field list is the working read of ASM-3068 (GAP-1872). A refusal publishes nothing.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | P7 rwb-decision | EV-30: names the SETTLEMENT and DEEDINLIEU package versions in force, which the stage evaluates and writes into the decision record; a version is swapped in at the next event and no restart is needed (Temporal and Drools Design slide 15) |

Consumed through the inbox of the outbox library, so a redelivery of EV-30 is deduplicated by the cloud event id (ASM-3064). The other events this service subscribes to — `rwb.payment.TreatmentBooked.v1` (EV-11), `rwb.payment.PaymentMissed.v1` (EV-12) and `rwb.deviation.DeviationRaised.v1` (EV-06) — are consumed by other stages of `TreatmentWorkflow` and are not consumed by this branch.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow` | Workflow, the stage child of `CaseWorkflow` (rwb-case), one execution per case and stage, continue-as-new at the stage end | `rwb-treatment` in namespace `rwb-recovery` | Input from the parent signal: case ID, stage, case status, treatment ID; the stage outcome returned to the parent; search attributes CaseId and Stage |
| `ApprovalWorkflow` | Child workflow of the workflow kit, started on rwb-decision's queue | `rwb-decision` in namespace `rwb-recovery` | Input: case, treatment, decision code D6.4, capability area, product group, amount, gap to the floor, prepared-by reference; output: level, limit version, status, final call, approver reference, decided-at time |
| `checkFloor` | Activity | `rwb-treatment` | The offer amount or transfer price and the floor in force; inside or below, with the gap |
| `requestSecondSignature` | Activity | `rwb-treatment` | Starts the `ApprovalWorkflow` child with the request above and returns its answer; idempotent by treatment and approval reference |
| `recordAndApply` | Activity | `rwb-treatment` | One transaction: the four treatment columns plus `approval_level`, the decision record through RWB-PLT-E1027-CON, the outbox row |
| `publishApproved` | Activity | `rwb-treatment` | The approved treatment and its facts; the outbox row the relay publishes as `TreatmentApproved` |

DP-03, DP-13 and DP-19 are the patterns this story applies; the workflow and activity names are a target design choice fixed by no source document, and the stage model itself is the workflow kit's. The retry policy is the kit's; the approval clock of three working days belongs to R-SET-05 and R-DIL-15 and runs on rwb-decision's side.

#### 12.6 Schedules

None. The branch is event- and signal-started inside `TreatmentWorkflow`; it owns no Temporal Schedule and no legacy Quartz job. The approval clock and its escalation are the approval routing's, and the plan timers of a restructure are the sibling stories'.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | Updated by `recordAndApply`: `approval_level` (DF-TRT-011) and the four outcome columns `final_call`, `approver_role`, `decided_at` and `reason_code`; no row is inserted here |
| `decision_record` | `rwb_treatment` | PLT (library object, written through RWB-PLT-E1027-CON) | Written in the same transaction as the treatment update (DP-03) |
| `outbox` | `rwb_treatment` | S2, from the service template | Written in the same transaction; the relay publishes `TreatmentApproved` |
| `approval` | `rwb_decision` | P7 | Not written and not read: the answer arrives as the child workflow's result |
| `delegation_limit` | `rwb_access` | P4 | Not written and not read: the level and the limit arrive on the approval request |

No new table is created for the second signature, and no foreign key crosses a schema (DP-01). `decision_log_entry` is P7's ledger and is named here only.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-S2-E3003-CON treatment-approval fake | The treatment element set, the approval elements and the event envelope | An approved settlement and an approved deed in lieu with their level and final call; a refusal with reason `price_below_floor`; a record with no decision |
| RWB-PLT-E1027-CON decision-record fake | The record write | An accepted record with chain sequence and entry hash; a refusal with MSG-P7-009 and the field; an unavailable writer with MSG-P7-003 |
| RWB-PLT-N001-CON gateway route fake | The composite route of SCR-14 and SCR-15 and the approval item | A granted right U for the officer and RA for the approver; a refused answer for a role without them; a scope miss |
| rwb-case case-status mock | The two added Given lines of AC2 and AC3 | Case status TRANSFER_PRICE_SET and AWAITING_SECOND_SIGNATURE on the signal, and the status the parent reports back |
| `ApprovalWorkflow` fake | The child workflow of the kit | An approved answer at L6 under DOA-2026.11; an approved answer at L5 under DOA-2027.01; a refusal; HELD_NO_LIMIT; a timeout |
| Floor and reason-code fixture | The values in force | A floor of the case with an offer above and below it; the reason codes `price_below_floor` and `below_floor_refused` of their owners |

The treatment-approval, decision-record and gateway fakes are the published contracts of those stories; the case-status mock stands in for the signal, which is the only way a case status reaches this service (ASM-3062); the approval fake stands in for the kit's child workflow and answers with the DoA values of rwb-access, recorded with GAP-1872 and ASM-3068.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0: the branch declares no operation | 0 | The offer operation is RWB-S2-E3002-CON's and the treatment read RWB-S2-E3001-CON's; both are reached through gateway-bff (DP-19) |
| Kafka | 1 event (`rwb.treatment.TreatmentApproved.v1`) on `rwb.treatment.events.v1` | 1 event (`rwb.decision.RulePackageInForce.v1`) | CloudEvents 1.0 binary mode, key `caseId`, outbox and inbox of the service template |
| Temporal | 1 stage workflow and 4 activities | 1 child workflow (`ApprovalWorkflow`) on rwb-decision's queue | Namespace `rwb-recovery`; no Schedule |
| File | None | None | No file is read or written |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, modules `approval` and `treatment`, with the published types in `...treatment.api`. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the record of the approval inside the same transaction; DP-13 fixes the service base on which the offer operation and the treatment read of this service answer; DP-19 is the route by which SCR-14 and SCR-15 reach this service and the approval item. The ownership rule of DP-01 is applied in prose and in the SQL: `recovery_case`, `approval` and `delegation_limit` are never named in a statement of this service.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `TreatmentWorkflow` (below-floor branch) | Workflow | The floor check, the child workflow call, the outcome report to the parent, the record and the publish |
| `checkFloor` | Activity | The comparison of the offer or transfer price with the floor in force, and the gap |
| `requestSecondSignature` | Activity | The `ApprovalWorkflow` child on rwb-decision's queue and the mapping of its answer |
| `recordAndApply` | Activity | The treatment columns, the decision record and the outbox row in one transaction |
| `publishApproved` | Activity | The `TreatmentApproved` outbox row |
| `TreatmentApprovalHandler` | Handler | The branch entry from the offer answer: the re-test of the price, the child workflow call and the mapping of the answer |
| `TreatmentRepository` | Repository | The update of `treatment` by ID, with the optimistic-lock version of the row |

**Database.** `treatment` already holds DF-TRT-001 to DF-TRT-033. This story adds the four outcome columns `final_call`, `approver_role`, `decided_at` and `reason_code` on the service's own migration sequence, beside the existing `approval_level` (DF-TRT-011), and creates no table: the second signature has no table of its own (GAP-1872; ASM-3068). `decision_record` is the library object of RWB-PLT-E1027-CON in the same schema.

**Configuration and reference data.** The floor in force, the DoA levels and limits, the three-working-day clock of R-SET-05 and R-DIL-15, and the reason codes `price_below_floor` and `below_floor_refused` are values in force of their owners and are read, never set here (BR6). The rule package versions arrive through `rwb.decision.RulePackageInForce.v1`. The capability area and the right are the guard library's data.

**Build steps**

1. The migration that adds the four outcome columns to `treatment` on the service sequence, with no new table.
2. `checkFloor` against the floor fixture, with the below and inside answers and the gap (AC1, AC2).
3. `requestSecondSignature` against the `ApprovalWorkflow` fake, with the L6 and L5 answers, the refusal, HELD_NO_LIMIT and the timeout (AC1, AC2, AC3).
4. `recordAndApply` with the treatment update, the decision record through the fake and the outbox row, and the rollback on MSG-P7-003 and MSG-P7-009 (AC4).
5. `publishApproved` and the envelope against the schema fixture, with key `caseId` (AC1).
6. The branch entry and the guard, with a below-floor offer answer, an inside-range answer, a role without right U and a role without RA (AC1, TC-E3-003-05).
7. The outcome report to the parent and the two mocked case statuses (AC2, AC3).
8. Tests for AC1 to AC4 against the fakes and the fixtures.

**Feature flag.** `rwb.treatment.below-floor-approval`.

**Done when.** The tests in section 16 pass, a synthetic below-floor settlement and a synthetic below-floor transfer price each reach the approval child in SIT and come back with a level and a final call recorded on the treatment, `TreatmentApproved` appears on `rwb.treatment.events.v1` for a granted answer and not for a refusal, a forced record failure leaves the treatment unchanged with MSG-P7-003, and the approval block of SCR-14 shows the level, the final call and the reason code through the gateway-bff route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S2-001 | A settlement offer is below the floor and has been routed for approval | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-002 | The payoff of the case is older than the freshness limit | The payoff is from {date}. A new figure has been requested. |
| MSG-S2-003 | An offer to the customer carries its end date | The offer to the customer ends on {date}. |
| MSG-GEN-001 | A required field of the offer or the approval is missing | Enter {field}. |
| MSG-P4-002 | The role does not hold right U in "Treatment and offer" | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | The record is refused for a missing or invalid field (service log and incident, not shown to the customer) | The decision record was refused: {field} is missing or not valid. |

The seven texts are the legacy texts carried unchanged; MSG-P7-009 comes with the decision-record contract of RWB-PLT-E1027-CON and is not shown on a screen. MSG-S2-002 and MSG-S2-003 are raised by the offer of the sibling story and are listed here because the legacy story carried them; this story does not raise them. Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-14 Treatment record: states Draft, submitted, approved, booked, broken; this story shows the approval block of the record — level, approver role, final call, decided-at time and reason code — once an answer exists. SCR-15 Settlement offer: states Draft, below floor, approved, sent, accepted; the below-floor state is where this story starts, and the screen names the floor, the gap and the level the matrix requires. Both reach this service through the gateway-bff composite route (DP-19), which calls rwb-treatment and rwb-case in parallel, one hop each; the approver answers in the approval item that the route shows from rwb-decision, and the answer reaches this stage as the child workflow's result, not as a screen call of this service. The screen field list and the composite route specification belong to the platform edge story and the screen owners, and this story fixes the service side of the answer only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-003-01 | AC1 | End to end | A settlement offer below the floor of its case; the floor and the reason code in force; RW-PRODHEAD approves at the level the matrix names; the decision record carries the rule version |
| TC-E3-003-02 | AC2 | End to end | Case status TRANSFER_PRICE_SET on the case signal mock; `transfer_price < floor_price`; R-DIL-15 routes the price for a second signature and the case reaches AWAITING_SECOND_SIGNATURE |
| TC-E3-003-03 | AC3 | End to end | Case status AWAITING_SECOND_SIGNATURE on the case signal mock; the second signature is refused; the case returns to the route decision with reason `price_below_floor` and reaches RETURNED_TO_ROUTE_DIL |
| TC-E3-003-04 | AC4 | End to end | The decision-record fake refuses the write; nothing changes and MSG-P7-003 is shown |
| TC-E3-003-05 | Access | Component | RW-CASEOWN prepares a below-floor offer without right U and a role without RA answers the approval; refused with MSG-P4-002 and nothing changes |
| TC-E3-003-06 | Principle 5 | Component | A forced decision-record write failure stops the action with MSG-P7-003; the treatment row, the outbox and the parent report are unchanged |

The six legacy test case IDs, their Covers and their Data are kept in order and character for character; the legacy level "System" maps to "End to end" and "Access" to "Component", as in the other stories of this run. The contract fakes of section 12.8 stand behind every case, and the `ApprovalWorkflow` fake replaces the child workflow. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 2 integration harness, RWB-ITG-W2J01-ITG and the Epic 3 journey stories, and are not listed here.

### 17. Guardrails

- No business value in code: the floor, the DoA levels L1 to L6, the limits, the three-working-day clock and the reason codes `price_below_floor` and `below_floor_refused` are values in force of their owners, read with their version, never constants (BR6).
- No personal data in logs, events, workflow inputs or the fixture: the branch carries treatment and case identifiers, codes, levels, amounts, rule and delegation versions and timestamps; test data is synthetic and no customer field is copied.
- No read of another service's table: the case status and case facts arrive on the case signal, the approval answer arrives as the child workflow's result, and the delegation facts arrive on the approval request (DP-01; ASM-3062; ASM-3068).
- No write outside the transaction that records the change: the treatment update, the decision record and the outbox row commit together or not at all (DP-03; BR8).
- The decision is written before the change takes effect, and a refused or unavailable record leaves the case exactly as it was, which is what R-UNI-39 and Principle 5 require.
- The rule version, the delegation version and the level are written with every answer, so an auditor can see why a case went to a given approver (Temporal and Drools Design slide 6).
- No case status is written and no case table is named in SQL: the parent moves the status on the stage outcome this story returns (ASM-3062).
- No credential, no secret and no delegation limit appears in code, configuration, a prompt or the event payload.
- A refusal publishes no approval event: rwb-comms and rwb-payment hear only of an approved treatment (EV-10).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-004 | Settlement terms are negotiated inside a rule-set range, and anything outside the range needs approval | Business Requirements Program, section 5.9 | FEAT-TRT-03 | 07 Route, settle and claim | R-DIL-15; R-DIL-17; R-SET-05 | TC-E3-003-01 to TC-E3-003-06 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3003-CON | Contract | H: declares the treatment approval elements, the `TreatmentApproved` envelope, the no-new-table rule and the fakes this story builds against |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library, its `MANDATORY` rule and its two exceptions (DP-03) |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route of SCR-14 and SCR-15 and the approval item the answer arrives on (DP-19) |
| RWB-S2-E3001-APP | App development | Same lane, earlier stage: the treatment record and the service's own migration sequence |
| RWB-S2-E3002-APP | App development | Same lane: the settlement range and the inside-range offer, whose below-floor branch is this story |
| RWB-S2-E3004-CON, RWB-S2-E3004-APP | Contract, App development | Same service, no build dependency: the TDR plan whose affordability path uses the same approval routing |
| RWB-ITG-W2J01-ITG | Integration | I: the cross-service proof of the same legacy key against the live owners; not this story's |

### 19. Out of scope

- The published element set of the approved treatment, the `TreatmentApproved` envelope, the compatibility rule and the fakes: RWB-S2-E3003-CON.
- The treatment record, its creation, its fields DF-TRT-001 to DF-TRT-033 and its own migration: RWB-S2-E3001-APP and RWB-S2-E3001-CON.
- The settlement range, the payoff freshness and the offer inside the range, including `POST /treatments/{treatmentId}/offer`: RWB-S2-E3002-APP and RWB-S2-E3002-CON.
- The TDR plan and the affordability check that precedes it: RWB-S2-E3004-APP and RWB-S2-E3005-APP.
- The case status, the case table, the assignment and the task of the approver: rwb-case, RWB-P3-E1018 and its contract; the status reaches this service on the case signal only (ASM-3062).
- The approval record `approval`, the `ApprovalWorkflow` on rwb-decision's queue, the approval routing features of FEAT-APD-01, the rule package registry and the version promotion: rwb-decision, and the sibling stories of that service.
- The delegation of authority data, the levels L1 to L6, their holders, substitutes and valid-from dates: rwb-access and RWB-P4-E1038-APP; this story holds no limit and reads no DoA table (ASM-3068).
- The floor price of an asset, the settlement range values and the reason-code list as data rows: their owners, S5 rwb-asset, P3 rwb-case and P7 rwb-decision.
- The contract and deed-in-lieu documents generated after a granted second signature (R-DIL-16), the e-signature and the notice to the customer: rwb-document, rwb-comms and the sibling stories of this service.
- The deployment, the flag, the dashboards and the alerts of this build: this legacy key's DevOps story.
- The real cross-service proof of the approval against the live rwb-decision, rwb-access and rwb-case: the wave 2 integration harness.
