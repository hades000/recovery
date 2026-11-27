# RWB-S4-E5015-APP Pay court fees and legal expenses

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5015-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Feature | FEAT-LIT-15 Pay court fees and legal expenses |
| Rules | R-LIT-30; R-LIT-41 to R-LIT-43 |
| Module measure | litigation turnaround, 6 days |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S4-P |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S4-E5015-APP-16) |
| Contract version | /v1 path only; the contract version is not specified in the source documents (DOR-RWB-S4-E5015-APP-23) |
| Depends on (build) | RWB-S4-E5015-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | Document contract (P5, the Workbench document hub), payment contract (P8, rwb-payment), agent contract (P10, model gateway) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: app slice split from RWB-E5-015 for rwb-litigation (S4). The fee decision of a legal action is taken on the legal-action operations of base `/api/recovery/litigation/v1` (DP-13); one decision record is written through the local decision-record library before the spend is approved, rejected or paid (DP-03); the fee is paid and posted by rwb-payment (P8) and never here (GAP-2806; ASM-4646); the schedule the fee is checked against is a versioned reference row read on rwb-case (GAP-2807; ASM-4647); the filing rule of legacy AC2 is built by `RWB-S4-E5010-APP` and `RWB-S4-E5011-APP` and only asserted here (GAP-2808; ASM-4648); the approval is the P7 approval child workflow with the D7.4 limit (GAP-2809; ASM-4649); the two workspaces read the spend state through the gateway-bff composite route (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S4-E5015-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (25 resolved, 14 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer or enforcement owner (RW-LITOFF, RW-ENFORCE)**, I want **the court fee or legal expense of a legal action checked against the fee schedule in force, routed to the approver inside the D7.4 limit, recorded with one decision record and then paid against the case by the service that owns the money**, so that **a filing, a hearing or an enforcement step is never held up by a fee nobody checked or a spend nobody approved, and the money, the case and the rules stay with the services that own them**.

This story owns the spend decision of a legal action and the fact that pays it:

- the evaluation of R-LIT-41, R-LIT-42 and R-LIT-43 of the LITIGATION route set — route the fee to the approver inside the D7.4 limit, raise and pay the approved fee against the case, record the reason of a rejected spend — with the rule rows at their version in force (Business Rules and Routing Logic v4);
- the one decision record each evaluation writes through the local decision-record library **before** the spend moves, on the shared topic `rwb.decision-record.v1` (DP-03);
- the check of the fee against the fee schedule in force and against the D7.4 limit, both read as versioned values of their owners and never as a constant of the code (GAP-2807; GAP-2809);
- the legal action the fee hangs on, opened on `POST /cases/{caseId}/legal-actions` (API-S4-002) and read on `GET /legal-actions/{legalActionId}` (API-S4-003) on base `/api/recovery/litigation/v1` (DP-13; TSD S4 T-A.1, T-A.2);
- the spend facts the workspace shows: the fee reference, the fee type, the amount, the value date, the approver, the rule ID with its version, the approval state and the payment reference the owner returns.

It owns nothing else. The money — the payment, its posting against the case and the general ledger entry — is rwb-payment's (P8): R-LIT-42's "raise the fee and post it against the case" names ALS core and GL as its systems, and this service holds no fee table, no fee column and no posting (GAP-2806; ASM-4646). `recovery_case` and its route states are rwb-case's (P3); the rule rows and the approval are rwb-decision's (P7); the fee receipt is rwb-document's (P5); the firm's expense claim arrives on the rwb-partner contract (S9). The court case number and the hearing timers of legacy AC2 are written by the filing and hearing stories of this same service and are only asserted here (GAP-2808; ASM-4648).

### 2. Business rationale

The legacy feature is one sentence — "Checks the fee against the schedule, routes it for approval where needed and pays it" (FSD S4 A2.15.1) — and the legacy story gives it one process, one `recovery` schema and one decision log entry written together with the case row and the timer row. Its problem statement is the reason it exists: "Litigation takes 21 days to file; packs are incomplete and law firm progress is not tracked", and the module measure it carries is "litigation turnaround, 6 days" (FSD S4 A2.15.1). Its stated prerequisite is FEAT-PAY-05 and its integration points are "Partner portal, ALS and GL" (FSD S4 A2.15.2).

The target cuts the step three ways, and the cuts are stated rather than assumed. The decision to spend is litigation's: an officer of this service routes the fee, the rule decides whether the D7.4 limit is crossed, and the decision record is written here before anything moves (DP-03; R-LIT-41 to R-LIT-43). The money is not: no column of `legal_action` or `hearing` carries a fee, an amount to pay or a posting (TSD S4 T3.1), the service owns two tables and five operations and none of them touches money (context pack ownership rows), so the payment and the posting against the case are consumed on rwb-payment (P8), whose module is Payments and posting. The schedule and the limit are not: "the schedule" of the legacy sentence is a fee schedule with a version, and the D7.4 limit is a delegation limit of the authority matrix, so both are read from their owners and neither becomes a constant (BR-S4-015; VR-S4-015-1).

Two further consequences are written down. First, the legacy criterion AC2 of this key carries R-LIT-30, the filing rule, whose effects — the court case number on the legal action and the hearing timers — are built by `RWB-S4-E5010-APP` and `RWB-S4-E5011-APP` under the same rule row. This story keeps the criterion word for word and proves the post-condition against those two stories' surfaces; it adds no second writer of `black_case_no` and no second timer (GAP-2808; ASM-4648). Second, the approval is not a local state: TSD S4 T5.2.2 names the approval as a Temporal child workflow of rwb-decision (P7), so it is declared, consumed and faked, not rebuilt here (GAP-2809; ASM-4649).

It serves FEAT-LIT-15 "Pay court fees and legal expenses" (FSD S4 A2.15), it carries the module measure by making every fee one decision record plus one owner's payment reference, and it holds the legacy prerequisite FEAT-PAY-05 through the consumed payment contract. The three legacy criteria AC1 to AC3 belong to this story and are copied word for word in section 7. No requirement identifier is given for this key by any source read: TSD S4 T8 maps REQ-S4-001 to REQ-S4-010 to FEAT-LIT-01 only (GAP-2810; ASM-4650).

### 3. Preconditions

- `RWB-S4-E5015-CON` is published: the two operations of this key on `/api/recovery/litigation/v1`, the `LegalActionRequest` and `LegalAction` elements, the `Idempotency-Key` rule, the error envelope, the consumed rows with their placeholders and the fakes. It is the first build dependency of this story, so the story starts on Day 1.
- The `legal_action` and `hearing` tables exist in schema `rwb_litigation` with DF-LEG-001 to DF-LEG-014 and DF-LEG-024 to DF-LEG-029 of TSD S4 T3.1 and the standard columns of T3.0. This story creates no table, no column and no migration; no fee column exists on either table (GAP-2806).
- The legal action exists and is `FILED` or later in LOV-LEGAL-STATUS (`OPEN`, `FILED`, `JUDGMENT`, `ENFORCING`, `CLOSED`, `WITHDRAWN`): it is opened on API-S4-002 and moved to `FILED` by the filing story of this service.
- The local decision-record library and the shared record format of DP-03 are live (`RWB-PLT-E1027-CON`), and the record is relayed on `rwb.decision-record.v1`.
- `LitigationWorkflow` runs on task queue `rwb-litigation` in namespace `rwb-recovery` as a child of `CaseWorkflow`, and it hosts the spend step of the stage (context pack workflow row).
- The fee schedule in force, its version and the fee types are read as reference data of rwb-case, operation `Not specified in the source documents (GAP-2807; ASM-4647)`; they are consumed and faked, not built.
- The D7.4 approval limit and the approver's delegation limit are read on the authorise contract of rwb-access, operation `Not specified in the source documents (GAP-2809; ASM-4649)`.
- The LITIGATION rule package at its version in force with R-LIT-30 and R-LIT-41 to R-LIT-43, and the approval child workflow, are consumed on rwb-decision (P7), operations `Not specified in the source documents (GAP-2809; ASM-4649)`.
- The payment and posting of the approved spend, and the payment reference it returns, are consumed on rwb-payment (P8), operation `Not specified in the source documents (GAP-2806; ASM-4646)`.
- The fee receipt and the firm's expense claim are consumed on rwb-partner (S9) and rwb-document (P5), operations `Not specified in the source documents (GAP-2806; ASM-4646)`.
- The gateway-bff composite route `RWB-PLT-N001-CON` serves SCR-20 and SCR-18, so the spend panel is readable from Day 1 (DP-19).
- The caller holds a Workbench role with a Litigation right on the operation it calls (TSD S4 T6.1): RW-LITOFF holds CRUA, RW-ENFORCE holds CRU, RW-LEGAL and RW-PRODHEAD and RW-HEADLIT hold RA, PT-LAWFIRM holds RU and SY-DATALOAD holds U.
- The service runs as its own login on schema `rwb_litigation` (DP-01, DP-02); it holds no grant on another `rwb_*` schema and no `v_ace_*` grant.

### 4. Flow

1. A court fee or a legal expense falls due on an action: the firm's receipt and expense claim arrive on the rwb-partner contract (S9) and the receipt document reference on the rwb-document contract (P5), and the spend step of `LitigationWorkflow` starts. Nothing is polled from an ACE view (operation names not specified: GAP-2806, ASM-4646).
2. The officer opens SCR-20 Enforcement workspace or SCR-18 Notice approval through the gateway-bff composite route (DP-19) and reads the action and its spend panel on `GET /legal-actions/{legalActionId}`: court fields, `claim_amount`, the status, and the open spend with its fee type and value date.
3. Where the action has to be opened first, it is created on `POST /cases/{caseId}/legal-actions` with `LegalActionRequest`; the `Idempotency-Key` header is required and its answer is stored.
4. `LegalSpendValidator` checks the legal-action reference and its status, the fee type against the schedule in force, the presence of the amount and the value date, the currency, the caller's scope and the receipt reference. A failed check answers 404, 409 or 422 and nothing is written.
5. `FeeScheduleChecker` compares the claimed fee with the schedule row in force for that fee type and court level and reports a variance; a fee above the schedule is routed, never silently reduced, and the comparison carries the schedule version.
6. `SpendDecisionWriter` evaluates R-LIT-41 with the rule rows at their version in force and writes one decision record through the local library **before** the spend moves: rule ID, version in force, inputs reference, the fee, the limit test and the answer (DP-03; legacy AC1).
7. `SpendApprovalClient` sends the spend to the P7 approval child workflow with the case, the action, the fee, the schedule version and the D7.4 limit test; the approver signs within their delegated authority read on rwb-access, and the answer is `APPROVED` or `REJECTED` with a reason (GAP-2809; ASM-4649).
8. On `APPROVED`, R-LIT-42 raises the fee: `LegalSpendPayer` asks rwb-payment to pay and post the approved spend against the case, with the case reference, the action reference, the fee reference, the amount, the value date and the approval reference, and stores the payment reference the owner returns. No balance, no posting and no ledger entry is written here (GAP-2806; ASM-4646).
9. On `REJECTED`, R-LIT-43 records the reason and returns the case without the spend: the decision record carries the rejection, the action and its `lit_status` are unchanged, and the officer sees the reason.
10. A repeated pay request with the same `Idempotency-Key`, or a repeat for the same fee reference, returns the stored payment reference and posts nothing twice; the repeat is counted under R-UNI-40.
11. The spend panel shows the fee, the schedule version, the approver, the approval state, the rule ID with its version and the payment reference; a failed or delayed payment leaves the spend `APPROVED` and the panel says so.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The request carries no amount, no fee type or no value date, or the fee type is not in the schedule | 422; no decision record and no payment | MSG-GEN-001 | AC1 |
| X2 | The legal-action ID names no row inside the caller's scope | 404; an out-of-scope action cannot be told from a missing one | None | AC1 |
| X3 | The action is `CLOSED` or `WITHDRAWN`, or the same fee reference is already paid | 409; nothing changes and the stored answer is returned | None | AC1 |
| X4 | The fee exceeds the schedule row for its fee type and court level | The variance is reported and the spend is still routed to the approver; it is never auto-approved and never silently reduced | MSG-S4-002 (only where the claim also runs past its warning window) | AC1 |
| X5 | A role without the Litigation right routes, approves, reads or pays a fee | Refused before any read or write; no decision record | MSG-P4-002 | AC1 |
| X6 | The local decision-record write fails | The transaction writes nothing: no approval request, no payment, no fact | MSG-P7-003 | AC3 |
| X7 | The approval child workflow does not answer inside its window, or the approver rejects | The spend stays `PENDING` or moves to `REJECTED` with its reason; no payment is sent | None | AC1 |
| X8 | The rwb-payment call does not answer inside 2 s or its breaker is open | The spend stays `APPROVED` with the retry marker; the panel says the payment is not confirmed; the workflow retries per policy | None | AC1 |
| X9 | A statement or a test reaches another `rwb_*` schema, a `v_ace_*` view or an ACE table | The grant refuses the statement and the boundary test fails the build | None (pipeline log) | BR6; AC4 |
| X10 | The court fee or expense is withdrawn or refunded by the court after payment | The refund is recorded by rwb-payment as its own fact; this service records the decision and shows the owner's value | None | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against `RWB-S4-E5015-CON`, the decision-record library, the composite route and the fakes of rwb-payment, rwb-decision, rwb-case, rwb-access, rwb-document and rwb-partner; no C dependency blocks the build |
| Negotiable | The fee schedule values, the D7.4 limit and the approval window are versioned reference or rule rows; the story fixes the shape and the behaviour, not the values |
| Valuable | Every court fee and legal expense of a case that runs for years carries its schedule check, its approver, its decision record and the owner's payment reference |
| Estimable | Two operations, one validator, one schedule check, three rule evaluations, one library write, two clients and one consumed child workflow, two durable steps in the stage workflow, one read-only workspace fragment |
| Small | Fits one sprint with its tests, as the fee slice of the legacy key |
| Testable | Each criterion of section 7 is one end-to-end test with the cross-service answers stubbed in the contract fakes; the contract half is tested in `RWB-S4-E5015-CON` |

### 7. Acceptance criteria

```gherkin
Feature: Pay court fees and legal expenses, in rwb-litigation

  Background:
    Given the legal action "LA-2026-001215" exists on case "RC-2026-001215" with status "FILED"
    Given the rule rows of the LITIGATION route set are in force at their version, and the fee schedule and the fee types of the case are read with their version in force
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Pay court fees and legal expenses (legacy RWB-E5-015 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-payment contract mock returns the payment reference of the approved fee of case "RC-2026-001215"
    Given the rwb-decision contract mock returns the rule rows of R-LIT-41, R-LIT-42 and R-LIT-43 at their version in force, the D7.4 limit and the approval answer
    Given the rwb-case contract mock returns the fee schedule in force, its version and the fee type of the claim
    When its trigger arrives
    Then checks the fee against the schedule, routes it for approval where needed and pays it
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Rule R-LIT-30 (legacy RWB-E5-015 AC2)
    Given a case in state FIRM_INSTRUCTED
    Given the rwb-case contract mock returns the case of record in state FIRM_INSTRUCTED
    When case filed
    Then write the court case number to the Legal Action and set the hearing timers
    Then the case moves to FILED_IN_COURT

  Scenario: AC3 Not recorded (legacy RWB-E5-015 AC3)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC4 A statement or a test reaches another `rwb_*` schema, a `v_ace_*` view or an ACE table is refused and fails the build (new, D-RCV-60)
    Given a statement or a test reads another `rwb_*` schema, a `v_ace_*` view or an ACE table
    When the statement runs under the rwb-litigation grant
    Then the grant refuses the statement and the boundary test fails the build

  Scenario: AC5 Each business rule of section 8 has a criterion or a guardrail test (new, D-RCV-60)
    Given the business rules BR1 to BR10 of section 8
    When the build runs
    Then every rule is covered by a criterion, or by a guardrail or boundary test when it is an architecture constraint

  Scenario: AC6 The provided operations answer 401, 403 and 404 where the case requires them (new, D-RCV-60)
    Given a request without a valid login, a request by a role without the Litigation right and a legal-action ID outside the caller's scope
    When the provided operations receive each request
    Then they answer 401, 403 and 404 respectively

  Scenario: AC7 A replay of a write with the same `Idempotency-Key` pays once and returns the stored reference (new, D-RCV-60)
    Given a write with an `Idempotency-Key` has been accepted and its fee is paid
    When the same request with the same `Idempotency-Key` is replayed
    Then no second payment is made and the stored reference is returned

  Scenario: AC8 A retried or timed-out activity leaves the spend in its stored state (new, D-RCV-60)
    Given the rwb-payment call does not answer inside 2 s
    When the activity times out and the workflow retries it per policy
    Then the spend stays `APPROVED` with the retry marker and the panel says the payment is not confirmed

  Scenario: AC9 A consumed call that fails or does not answer leaves the spend unchanged (new, D-RCV-60)
    Given the approval child workflow does not answer inside its window, or the rwb-payment breaker is open
    When the call fails or does not answer
    Then the spend stays `PENDING` or `APPROVED` as stored and this service sends no payment

  Scenario: AC10 A status change the model does not allow is refused and nothing changes (new, D-RCV-60)
    Given a legal action with a status the status model does not allow to change
    When a status change that the status model does not allow is requested
    Then the change is refused with the code Not specified in the source documents (NEWAC-RWB-S4-E5015-APP-AC10) and nothing changes
```

The three scenarios are the legacy criteria word for word, with the cross-service reads the target adds stated as mock Givens: the payment reference is rwb-payment's, the rule rows, the D7.4 limit and the approval are rwb-decision's, the fee schedule is rwb-case's and the case state of AC2 is rwb-case's. Nothing in the legacy wording is changed, reordered or narrowed. AC2's two effects — the court case number on `legal_action.black_case_no` and the hearing timers on `LitigationWorkflow` — are built by `RWB-S4-E5010-APP` and `RWB-S4-E5011-APP` under the same rule row, so this story proves the post-condition and writes neither again (GAP-2808; ASM-4648).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The spend decision of a legal action is this service's; the payment, the posting against the case and the ledger entry are rwb-payment's and are consumed, never written here | Context pack ownership rows (2 tables, 5 operations, no money); TSD S4 T3.1; GAP-2806 |
| BR2 | The fee is checked against the schedule in force for its fee type and court level, with the schedule version carried on the decision; a variance is routed to the approver, never auto-approved and never silently reduced | FSD S4 A2.15.1; GAP-2807 |
| BR3 | R-LIT-41 routes the fee to the approver inside the D7.4 limit, R-LIT-42 raises and pays the approved fee against the case, R-LIT-43 records the reason of a rejected spend; the rule rows and their version are read from rwb-decision | Business Rules and Routing Logic v4 (R-LIT-41 to R-LIT-43); GAP-2809 |
| BR4 | The decision record is written before the spend is approved, rejected or paid, through the local library on `rwb.decision-record.v1`; a failed write changes nothing | DP-03; TSD S4 T2; legacy AC1 and AC3 |
| BR5 | The approval is the P7 approval child workflow; the approver's delegation limit is read on rwb-access and the limit value is never a constant of the code | TSD S4 T5.2.2; GAP-2809 |
| BR6 | No value a business person may change is written in code: the fee schedule, the fee types, the D7.4 limit, the approval window and every LOV value are reference or rule rows with a version | FSD S4 A2.15.3.1 (BR-S4-015); principle 1 |
| BR7 | The stale marker of a source product is shown with MSG-P1-001 and blocks no spend; the batch-status check is the owner's | FSD S4 A2.15.3.1 (VR-S4-015-1) |
| BR8 | A repeated request with the same `Idempotency-Key` or for the same fee reference pays once and returns the stored reference | TSD S4 T-A.2; R-UNI-40 |
| BR9 | No personal data in a log, a workflow input, a fixture or a prompt; the record carries references, dates, amounts, codes and a rule version only | Template and Rules §R7.2 (s17); FSD S4 A2.15 |
| BR10 | One REST base, one topic, one queue and one login per service; no ACE view and no other `rwb_*` schema is read, and this service never chains a call to a third service on behalf of a screen | DP-01, DP-13, DP-14; ADR-020 |

### 9. State transitions

The transition table is TSD S4 T4 and the Business Rules and Routing Logic v4; this story owns the spend rows of it and answers the rest to rwb-case.

| From | Event | Condition | To | Rule |
|---|---|---|---|---|
| IN_HEARING | Fee due | a court fee or legal expense falls due | LEGAL_SPEND_APPROVAL | R-LIT-41 |
| LEGAL_SPEND_APPROVAL | Fee approved | inside the D7.4 limit, or the committee approves above it | IN_HEARING | R-LIT-42 |
| LEGAL_SPEND_APPROVAL | Fee rejected | the approver rejects the spend | IN_HEARING | R-LIT-43 |
| FIRM_INSTRUCTED | Case filed | the firm uploads the receipt and the court case number | FILED_IN_COURT | R-LIT-30 (asserted here; built by `RWB-S4-E5010-APP`) |

The case state itself is written by rwb-case on this service's answer: the stage outcome carries the state name, the rule ID and the package version, and this service writes no `recovery_case` row. `LEGAL_SPEND_APPROVAL` and `IN_HEARING` are case route states, not values of LOV-LEGAL-STATUS, and neither is added to the closed list LOV-LEGAL-STATUS (GAP-2808; ASM-4648). The action's own `status` follows LOV-LEGAL-STATUS (`OPEN`, `FILED`, `JUDGMENT`, `ENFORCING`, `CLOSED`, `WITHDRAWN`) and is unchanged by a spend (TSD S4 T3.2).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Litigation officer (RW-LITOFF) | Route a fee, read the spend panel, record a reason on a rejected spend, recreate a withdrawn claim |
| Enforcement owner (RW-ENFORCE) | Route and read the spend of an enforcement action (CRU) |
| Legal counsel, product head, head of litigation (RW-LEGAL, RW-PRODHEAD, RW-HEADLIT) | Read the spend and approve it inside the D7.4 limit where the approval route names them (RA) |
| Approver at D7.4 | Decides the spend inside the delegated limit; above it the committee decides, as R-LIT-41 to R-LIT-42 state |
| Partner and agency manager (RW-AGENCYMG), law firm user (PT-LAWFIRM) | Read the spend of the instructed firm's actions; the firm submits its expense claim through the portal, not into this service |
| Rules and agent identities (SY-RULES, SY-AGENT) | Read the rule answer under a service identity, never approve and never pay |
| Tech lead of rwb-litigation | Owns the implementation and the build steps of section 13 |
| Architect of the platform library and of the edge | Own the decision-record library, the envelope and the composite route this story consumes |

### 11. Data

| Entity | Fields | Owner | Use in this story | BR Field ID |
|---|---|---|---|---|
| legal_action | DF-LEG-001 to DF-LEG-014: id, case_id, law_firm_id, action_type, lawsuit_no, black_case_no, red_case_no, court_name, claim_amount, filed_date, judgment_date, judgment_amount, lit_status, status | S4 `rwb_litigation` | Read for the action, its amount, its court and its status; `black_case_no` and `filed_date` are AC2's post-condition and are written by the filing story | Not specified in the source documents (DOR-RWB-S4-E5015-APP-7) |
| hearing | DF-LEG-024 to DF-LEG-029 | S4 `rwb_litigation` | Read for the hearing the spend belongs to; no timer row is written | Not specified in the source documents (DOR-RWB-S4-E5015-APP-7) |
| decision_record | DF-DEC-001 to DF-DEC-018 shape, through the local library | PLT library in `rwb_litigation` | One record per spend decision (DP-03) | Not specified in the source documents (DOR-RWB-S4-E5015-APP-7) |
| idempotency_key | The key of a repeated create or pay request | PLT library in `rwb_litigation` | Stores the answer of a repeated request | Not specified in the source documents (DOR-RWB-S4-E5015-APP-7) |
| recovery_case, timer, task | DF-WRK-027 to DF-WRK-036 for the timer | P3 rwb-case | Read through the case read and answer only | Not specified in the source documents (DOR-RWB-S4-E5015-APP-7) |
| rule_row, decision_log_entry | DF-REF-001 to DF-REF-015; DF-DEC-001 to DF-DEC-018 | P7 rwb-decision | Read at the version in force (GAP-2809) | Not specified in the source documents (DOR-RWB-S4-E5015-APP-7) |
| Fee schedule and fee types | No field list in any source for this key | P3 rwb-case reference data | Read as the schedule the fee is checked against (GAP-2807) | Not specified in the source documents (DOR-RWB-S4-E5015-APP-7) |
| Payment and posting rows | No field list in any source for this key | P8 rwb-payment | Read and requested as the payment reference (GAP-2806) | Not specified in the source documents (DOR-RWB-S4-E5015-APP-7) |
| document, partner expense claim | DF-DOC-001 to DF-DOC-011 for the receipt document | P5 rwb-document; S9 rwb-partner | Read as the receipt and the claim behind the fee (GAP-2806) | Not specified in the source documents (DOR-RWB-S4-E5015-APP-7) |

The standard columns of TSD S4 T3.0 (`is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`) apply to the two owned tables. **No fee table, no fee column and no migration** is declared by this story: the durable effect of a spend here is the decision record, the idempotency row and the stage answer (GAP-2806; ASM-4646).

Reference data read here: the fee schedule and the fee types from the rwb-case reference data, and the rule rows R-LIT-41 to R-LIT-43 and the D7.4 limit from rwb-decision, read at their version in force through the reference-data contract of DP-06 and DP-07; the parameter keys of that contract are Not specified in the source documents (DOR-RWB-S4-E5015-APP-20). The spend states LEGAL_SPEND_APPROVAL and IN_HEARING are case route states read from the rwb-case answer; they are not values of LOV-LEGAL-STATUS and no LOV value is invented for them (GAP-2808; ASM-4648).

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Purpose | Access | Contract element |
|---|---|---|---|---|
| POST | `/cases/{caseId}/legal-actions` | Open a legal action and its pack, the action a fee hangs on (API-S4-002) | Litigation C | `LegalActionRequest` in, `LegalAction` out, status 201; `Idempotency-Key` required, the stored answer returned on a repeat |
| GET | `/legal-actions/{legalActionId}` | Read the action with its pack, instruction, hearings, judgment and spend panel (API-S4-003) | Litigation R | `LegalAction` out |

Base `/api/recovery/litigation/v1` (DP-13). The other three operations of the service — `POST /notices/{noticeId}/approve` (API-S4-001), `PATCH /legal-actions/{legalActionId}` (API-S4-004) and `POST /legal-actions/{legalActionId}/hearings` (API-S4-005) — belong to the notice, filing and hearing stories of this service and are not provided by this story. No operation of this story carries an amount to pay: a spend has no path of its own, because the sources give the fee no column and no resource (GAP-2806; ASM-4646).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use here |
|---|---|---|---|
| `Not specified in the source documents (GAP-2806; ASM-4646)` | `/api/recovery/payment/v1` | P8 rwb-payment | Pay and post the approved fee against the case; returns the payment reference and its value date; faked |
| `Not specified in the source documents (GAP-2807; ASM-4647)` | `/api/recovery/case/v1` | P3 rwb-case | The fee schedule and the fee types in force with their version, and the case state and product group; faked |
| `Not specified in the source documents (GAP-2809; ASM-4649)` | `/api/recovery/decision/v1` | P7 rwb-decision | The LITIGATION package at its version in force with R-LIT-30 and R-LIT-41 to R-LIT-43; faked |
| `Not specified in the source documents (GAP-2809; ASM-4649)` | `/api/recovery/access/v1` | P4 rwb-access | The authorise answer and the D7.4 delegation limit of the approver; faked |

Every row is one hop with a 2 s timeout, a breaker per downstream and a GET retried once with jitter (ADR-020). None of the four is a dependency row of this key; each is a C dependency in fact and the absence is recorded as GAP-2806, GAP-2807 and GAP-2809.

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14); its two catalogue events `JudgmentRecorded` and `AuctionResult` (TSD S4 T5.2.1) belong to the judgment and auction stories, and the ownership rows of this service publish zero events. DP-09 is outside this key's pattern set, so no outbox row and no producer is added here. The decision record leaves on `rwb.decision-record.v1` through the library of DP-03 and is not an event of this service.

#### 12.4 Events consumed

None. `FEE_DUE`, `FEE_APPROVED` and `FEE_REJECTED` are the event names of the state machine in the Business Rules and Routing Logic v4, not Kafka subscriptions: the two events this service consumes, `NoticeDelivered` (EV-15) and `PartnerResultSubmitted` (EV-21), belong to the notice and partner stories (TSD S4 T5.2.2). The service holds no consumer group and no inbox for this step, and the fee claim, the schedule, the rule rows and the payment answer arrive on the contracts of 12.2 and 12.5 (GAP-2806; ASM-4646).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, child of `CaseWorkflow`, continues-as-new | `rwb-litigation` | Hosts the spend step; its signals and its stage outcome are declared, not built. Workflow ID form and start rule: Not specified in the source documents (CG-ALL-9362) |
| `recordSpendDecision` | Activity | `rwb-litigation` | The fee and the schedule row in; the decision record, the rule ID with its version and the limit test out |
| `requestSpendApproval` | Activity | `rwb-litigation` | The spend in; the approval answer, the approver and the reason out |
| `payLegalSpend` | Activity | `rwb-litigation` | The approved spend in; the payment reference, its value date and its state out |
| Approval (P7 rwb-decision) | Temporal child workflow, **consumed** | `rwb-decision` | The approval of TSD S4 T5.2.2, declared as another owner's and never registered here |

The three activity names are target design choices fixed by no source; the consumed child workflow is the row TSD S4 T5.2.2 gives. `postProceeds` and the ledger entry are rwb-payment's activities on queue `rwb-payment` and are another owner's. No Schedule and no Quartz row is introduced (context pack ownership rows: Jobs 0).

#### 12.6 Schedules

None. The step starts from the arrival of a fee claim and from the time the approval waits, which are workflow steps of `LitigationWorkflow`, not a Schedule: no Temporal Schedule, no Quartz row, no shared job table and no batch window is declared here. The filing clock of R-LIT-30 is armed by the filing story of this service and no clock is armed by this story (GAP-2808; ASM-4648).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | Read for the action, its amount, its court and its status; written by the filing, judgment and enforcement stories |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked record of every spend decision (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of a repeated create or pay request |

`hearing` is this service's and another story's table. `recovery_case`, `timer` and `task` (P3), `rule_row` and `decision_log_entry` (P7), `document` (P5), the partner claim (S9), the fee schedule (P3 reference data) and the payment and posting rows (P8) are not owned here, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-payment pay-and-post fake | The payment reference of the approved fee of case `RC-2026-001215` with its value date and state, a refused payment and an answer beyond 2 s; no amount is fixed by any source (GAP-2806) | AC1 |
| rwb-case reference and case fake | The fee schedule in force with its version and the fee types, another version, and the case state `FIRM_INSTRUCTED` with the product group | AC1, AC2 |
| rwb-decision rule-package fake | The LITIGATION package at its version with R-LIT-30 and R-LIT-41 to R-LIT-43, and a second version | AC1, AC2 |
| rwb-decision approval child workflow fake | An `APPROVED` answer with its approver and an `APPROVED` answer above the limit refused for the committee, and a `REJECTED` answer with a reason | AC1 |
| rwb-access authorise and limit fake | The authorise answer for the roles of section 10, and the D7.4 delegation limit of the approver | AC1 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain that answers MSG-P7-003 | AC1, AC3 |
| gateway-bff composite route fake | The merged SCR-20 and SCR-18 model of case `RC-2026-001215` with its spend panel | AC1 |

The fakes are test-only and are replaced by the owners' services in SIT. The schedule values, the D7.4 limit and the approval window are reference or rule values and are never fixed in a fake beyond the shape the documents give (GAP-2807, GAP-2809).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The legal-action create and read provided; the payment, the schedule and case read, the rule package and the authorise read consumed; one hop, 2 s |
| Kafka | None | No event published and none consumed; the decision record is the library's on `rwb.decision-record.v1` |
| Temporal | 1 workflow, 3 activities, 1 consumed child workflow | `LitigationWorkflow`, `recordSpendDecision`, `requestSpendApproval`, `payLegalSpend`, and the P7 Approval child workflow; no Schedule |
| File | None | No file is read or written by this story; the fee receipt is a document reference of P5 |

### 13. Solution plan

**Deliverables.** The two operations on the base of DP-13 with their validator and error envelope, `FeeScheduleChecker`, the evaluation of R-LIT-41 to R-LIT-43 and the decision-record writer of DP-03, the approval and payment clients with their breakers, the three workflow activities, the `legal_action` and idempotency reads, and the SCR-20 and SCR-18 spend panel behind the composite route of DP-19.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/litigation/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-04 is applied in behaviour but not in the pattern set: the three rules are evaluated with the embedded Drools kit against the rule package of rwb-decision, which is a consumed contract without a dependency row (GAP-2809). DP-06, DP-07, DP-08 and DP-11 are outside the set although the story reads the schedule, the LOV values, the delegation limit and four owners' answers; each read travels on the owner's contract and the absence of the dependency rows is recorded (GAP-2807, GAP-2809).

**Build steps**

1. Publish the two operations of 12.1 against the CON, with the validator, the error envelope and the `Idempotency-Key` rule.
2. Write the decision-record writer and prove the "nothing changes" rule of AC3 on a stopped chain.
3. Write `FeeScheduleChecker` and the R-LIT-41 evaluation, and record the schedule version with the limit test on every decision.
4. Write the approval client for the P7 child workflow and the `PENDING`, `APPROVED` and `REJECTED` paths of R-LIT-42 and R-LIT-43.
5. Write the payment client with its 2 s budget, its breaker and its stored reference, and prove a repeated key pays once.
6. Write the three activities and host the spend step in `LitigationWorkflow`.
7. Assert AC2 against the filing and hearing stories' surfaces: `black_case_no` on the action and the hearing timers, with no second writer and no second timer.
8. Finish the boundary tests: no read of another `rwb_*` schema, no `v_ace_*` view, no fee, posting, balance or case row written here.

**Done when.** The three legacy criteria pass end to end against the fakes, a repeated key pays once, the spend panel shows the owner's payment reference with its stale and pending markers, and the boundary tests are green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | The pack of the action is incomplete, which is the pack story's path; no path of this story raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | The claim on the case is inside its warning window, as the case read reports it, while the fee is routed | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field is absent or invalid, or the fee type is not in the schedule | Enter {field}. |
| MSG-P4-002 | The role lacks the Litigation right the operation or the spend step declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the spend moves | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The source product of a consumed read is stale after a late or failed ACE batch | {product} is from {date}. Today's load has not arrived. |

The six message IDs are the legacy set of this key and the FSD wording; the text of MSG-P1-001 is copied from the Error and Message Standard v4, and no other message is reworded and no new one is added. MSG-P1-001 is carried because it is VR-S4-015-1 of the feature, and the batch-status check itself is the owner's, not this service's.

### 15. Screens and states

| Screen | States |
|---|---|
| SCR-20 Enforcement workspace | Requested; seized; auctioned; closed; empty, loading, error and no access: Not specified in the source documents (CG-ALL-9370) |
| SCR-18 Notice approval | Generated; approved; sent; delivered; unserved; empty, loading, error and no access: Not specified in the source documents (CG-ALL-9369) |

Both screens read the spend panel — the fee, the schedule version, the approver, the approval state and the payment reference — through the gateway-bff composite route (DP-19), next to the case route state of rwb-case and the legal action of this service. The pending, rejected, refused and stale states read the messages of section 14 on the same route. The composite route specification and the screen field list belong to `RWB-PLT-N001-CON`; no screenshot or field list for a fee panel exists in any source read here (GAP-2806; ASM-4646).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-015-01 | AC1 | End to end | Pay court fees and legal expenses |
| TC-E5-015-02 | AC2 | Component | Rule R-LIT-30 |
| TC-E5-015-03 | AC3 | Component | Not recorded |
| TC-E5-015-04 | AC1 (access path) | Component | A role without the right is refused with MSG-P4-002 |
| TC-E5-015-05 | AC3 (forced failure) | NFR | A forced decision record write failure stops the action with MSG-P7-003 |
| TC-E5-015-06 | §12 operations, events and activities (no AC) | Contract | Not specified in the source documents (DOR-RWB-S4-E5015-APP-12) |
| TC-E5-015-07 | §12.7 tables (ASM-3438) | Component | Not specified in the source documents (DOR-RWB-S4-E5015-APP-12) |
| TC-E5-015-08 | AC4 | NFR | Not specified in the source documents (NEWAC-RWB-S4-E5015-APP-AC4) |
| TC-E5-015-09 | AC5 | Component | Not specified in the source documents (NEWAC-RWB-S4-E5015-APP-AC5) |
| TC-E5-015-10 | AC6 | Contract | Not specified in the source documents (NEWAC-RWB-S4-E5015-APP-AC6) |
| TC-E5-015-11 | AC7 | Component | Not specified in the source documents (NEWAC-RWB-S4-E5015-APP-AC7) |
| TC-E5-015-12 | AC8 | Component | Not specified in the source documents (NEWAC-RWB-S4-E5015-APP-AC8) |
| TC-E5-015-13 | AC9 | Component | Not specified in the source documents (NEWAC-RWB-S4-E5015-APP-AC9) |
| TC-E5-015-14 | AC10 | Component | Not specified in the source documents (NEWAC-RWB-S4-E5015-APP-AC10) |

The five legacy test case IDs, their Covers and their Data are kept in order and character for character; the legacy table carries no level column, so the case that exercises the whole step maps to `End to end`, the filing post-condition and the not-recorded case to `Component`, and the forced failure of Principle 5 to `NFR`. The access and forced-failure cases test the same two criteria from their own angle, which is why they are listed against AC1 and AC3. The fakes and the stub of 12.8 stand behind every case, and the fixture data — case `RC-2026-001215`, legal action `LA-2026-001215`, a filing fee on 2026-11-30 and an enforcement expense in 2027 — is synthetic. The full test, with its Given, When and Then, is not yet in Recovery Workbench Test Cases v8.xlsx; it is to be added to the next Test Cases version, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness and are not listed here.

### 17. Guardrails

- No business value in code: the fee schedule, the fee types, the D7.4 limit, the approval window and the message texts are values of reference or rule rows with a version; no amount, percentage, day count or list value appears in Java.
- No personal data in logs, workflow inputs, fixtures or prompts: references, dates, amounts, codes and a rule version only, and every fixture is synthetic.
- The money stays with rwb-payment: no fee row, no posting, no ledger entry and no balance is written here; the payment is requested and its reference stored (BR1).
- The case stays with rwb-case: no `recovery_case` row, no route state, no `timer` row and no `task` row is written here; the stage outcome is answered with the rule and its version.
- ACE data only through the owner's contract: no component reads a `v_ace_*` view or an ACE table, and the service holds no such grant (DP-05 applied as a prohibition).
- No read of another service's tables and no cross-schema join: `recovery_case`, `rule_row`, `decision_log_entry`, `document`, the partner claim, the fee schedule and the payment rows are reached only through their owners' contracts (DP-01).
- Every spend decision is preceded by its decision record; a failed write leaves the spend untouched and the user sees MSG-P7-003.

### 18. Traceability

| Requirement ID | Requirement (short) | How this story satisfies it | Test cases | Feature | L3 process |
|---|---|---|---|---|---|
| FEAT-LIT-15 | Pay court fees and legal expenses (FSD S4 A2.15); no requirement ID is given for this key by the legacy master or TSD S4 T8 (GAP-2810; ASM-4650) | The two operations, the schedule check, the approval, the payment request and the decision record | TC-E5-015-01, TC-E5-015-03 | Pay court fees and legal expenses | Not specified in the source documents (DOR-RWB-S4-E5015-APP-2) |
| R-LIT-41, R-LIT-42, R-LIT-43 | Fee due, approved and rejected (Business Rules and Routing Logic v4) | The routing at the D7.4 limit, the payment of the approved fee and the reason of a rejection | TC-E5-015-01, TC-E5-015-05 | Pay court fees and legal expenses | Not specified in the source documents (DOR-RWB-S4-E5015-APP-2) |
| R-LIT-30 | Filing: court case number on the action and hearing timers set (asserted only) | The post-condition of AC2 proved against the filing and hearing stories' surfaces | TC-E5-015-02 | Pay court fees and legal expenses | Not specified in the source documents (DOR-RWB-S4-E5015-APP-2) |
| BR-S4-015, VR-S4-015-1 | No value in code; the stale marker of a source product | Reference and rule rows with a version, and the stale marker with MSG-P1-001 | TC-E5-015-04, TC-E5-015-05 | Pay court fees and legal expenses | Not specified in the source documents (DOR-RWB-S4-E5015-APP-2) |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-015, disposition Split (rework) |
| Legacy criteria | AC1, AC2 and AC3, owned word for word by this story |
| Legacy screens | SCR-20 Enforcement workspace; SCR-18 Notice approval |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-016 (Temporal and durable workflow steps), ADR-020 (contract-first REST, one hop, 2 s), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The payment, the posting against the case, the balance and the general ledger entry: rwb-payment (P8), `RWB-P8-*` contracts consumed on 12.2 (GAP-2806; ASM-4646).
- The fee schedule, its versions and the fee types: the reference-data owner of rwb-case, consumed on 12.2 (GAP-2807).
- The D7.4 limit, the committee path above it, the roles and the scope: rwb-access (P4) and rwb-decision (P7), consumed and faked (GAP-2809).
- The authoring, testing, approval and versioning of the LITIGATION package and of R-LIT-30 and R-LIT-41 to R-LIT-43: rwb-decision (P7).
- The filing, the court case number, the hearing timers and the judgment: `RWB-S4-E5010-APP`, `RWB-S4-E5011-APP` and the judgment story of this service (GAP-2808).
- The fee receipt document and the firm's expense claim in the portal: rwb-document (P5) and rwb-partner (S9).
- The case of record, its route states, the case clock and the officer task: rwb-case (P3).
- The rights, roles, scope and masking data, and the composite route and screen field list of SCR-20 and SCR-18: rwb-access (P4) and `RWB-PLT-N001-CON`.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this key.
