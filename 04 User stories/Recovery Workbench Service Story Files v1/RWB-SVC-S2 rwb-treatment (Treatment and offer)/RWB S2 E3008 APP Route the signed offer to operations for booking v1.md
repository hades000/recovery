# RWB-S2-E3008-APP Route the signed offer to operations for booking

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E3-008 for rwb-treatment (S2, Treatment and offer). The signed-offer hand-over leaves the monolith's in-process stage of `rwb-case` and becomes the signed branch of `TreatmentWorkflow`, the stage child that `CaseWorkflow` starts on task queue `rwb-treatment` (DP-12); the customer's signature arrives on the forwarded case event instead of being read from a local table; the rule that routes the case (R-RES-16 or R-SET-10) is evaluated in the package in force and its outcome is handed back to the parent in one element published by RWB-S2-E3008-CON, so the case status, the operations queue and the task timer stay rwb-case's; the local decision record is written in the same transaction as the signature status through RWB-PLT-E1027-CON (DP-03); ACE customer and payment facts are not copied but reached through rwb-source-data or the service's own views where they are needed at all (DP-05); the screen read sits under base `/api/recovery/treatment/v1` (DP-13) through the gateway-bff composite route (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3008-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S2-S |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S2-E3008-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **restructuring officer (FCR)**, I want **the Workbench to move the case to operations when the customer signs inside the validity period**, so that **restructures and settlements reach booking in days**.

This is the application slice of legacy RWB-E3-008. It owns:

- all four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the data rows, the messages and the two rules they depend on;
- the signed branch of `TreatmentWorkflow` on task queue `rwb-treatment` in namespace `rwb-recovery` — the stage child that `CaseWorkflow` of rwb-case starts for a restructure or a settlement, run in the four steps of every stage: receive the signal, ask Drools, record and apply in one transaction, then finish (Temporal and Drools Design slide 11, one service shape with queue `rwb-treatment`; TSD S2 T0.1);
- the signature gate: `signed = Y and signature verified` for R-RES-16 and `signed = Y` for R-SET-10, with the signature fact taken from the forwarded case event and the outcome kept as `signature_status` (DF-TRT-030) of the treatment (TSD S2 T3.1, LOV-TRT-SIGNATURE);
- the hand-over: the outcome of the signed offer — the route to operations, the target case state and the settlement instruction request — built as the `SignedOfferHandover` element of RWB-S2-E3008-CON and returned to the parent `CaseWorkflow` as the stage result (ASM-4371, ASM-4373);
- the local decision record of the signed path, written with the rule ID and rule version in the same transaction as the signature status through the library of RWB-PLT-E1027-CON (DP-03);
- the read the officer sees, `GET /treatments/{treatmentId}` on base `/api/recovery/treatment/v1`, declared by RWB-S2-E3001-CON and reached through the gateway-bff composite route (DP-13, DP-19).

It does not own: the published shape of the hand-over element and its rules, which is RWB-S2-E3008-CON; the offer itself, its validity clock and its expiry, which are RWB-S2-E3002-APP, RWB-S2-E3004-APP and RWB-S2-E3007-APP; the return on no signature (R-RES-17 and R-RES-18), which is RWB-S2-E3009-APP; the booking to ALS and NLEADS, the plan schedule and the settlement booking (R-RES-21 to R-RES-25, R-SET-13), which are the booking stories; the case status, the operations queue and its timer, which are rwb-case's (DP-01; ASM-4373); the e-signature execution and the documents, which are rwb-document's; the payment posting, which is rwb-payment's; the decision-record library, which is RWB-PLT-E1027-CON and its APP story; the screens and their composite route, which are the platform edge story and the screen owners (DP-19); and the real cross-service proof, which is the wave 2 integration harness.

### 2. Business rationale

The FSD measures this feature by one number: restructure turnaround of 5 days, measured from the decision log and the Workbench records, reviewed monthly, against today's 23 to 26 days tracked by hand (FSD S2 v4, section A2.8.1). The signed offer is the moment the case stops waiting on the customer and starts moving to booking, and the rule that owns that moment gives it one working day (Business Rules and Routing Logic v4 rows R-RES-16 and R-SET-10, timer column). The feature is a system step with no person in the path — the FSD records its primary role as "None; runs unattended" — so the value is won by making the hand-over automatic, provable and impossible to half-complete.

In the monolith the hand-over was one write to `recovery_case.status` inside one process. Architecture v5 moves three of the four facts. The case and its state belong to rwb-case (DP-01; ASM-4373); the treatment, its signature status and its terms belong to rwb-treatment in schema `rwb_treatment` (TSD S2 T0.2, one table); and the rule that routes the case is data of the package in force, not a branch in code (BR-S2-008; FSD S2 A2.8.3.1). What is left to this story is the join: read the signature, ask the rules, record and hand over — in one transaction, so that a case is never in `WITH_OPS_BOOKING` with no record of why.

One requirement carries the business value: REQ-S2-003, that a signed offer routes to operations for booking and that an unsigned or declined offer returns the case to its prior status. Its second half is RWB-S2-E3009-APP's; its first half is this story, and it is unbuildable without one agreed shape for the hand-over, because the operations step, the settlement instruction and the parent's status move would otherwise each invent their own. Two systems of the legacy row — EasyApp e-signature and ALS through COLLINS — are outside the Workbench, so the story takes the signature as a fact brought in from outside and hands the booking to the story that books, and calls neither system itself.

### 3. Preconditions

- RWB-S2-E3008-CON is published: the `SignedOfferHandover` element, its required and optional properties, its mapping to the `treatment` field set of TSD S2 T3.1, the rule that the five request-context facts are recorded on the decision record and gain no column, the two `toState` values, the versioning rule and the fakes are baselined and handed to this story.
- `TreatmentWorkflow` exists for a case whose route decision is R1 (restructure) or R2 (settlement) — the stage child of `CaseWorkflow` on task queue `rwb-treatment`, its input, its four steps and its parent close policy are the treatment stories' and are reused here, not redeclared (TSD S2 T0.1 and T5.2.1; Temporal and Drools Design slide 11).
- `treatment` carries the 33 fields of TSD S2 T3.1 and the seven standard columns of T3.0 on the per-service Flyway sequence of rwb-treatment, `signature_status` (DF-TRT-030, LOV-TRT-SIGNATURE) among them, and the `rwb_treatment` login holds rights in that schema only (DP-01, DP-02, DP-15).
- RWB-PLT-E1027-CON is published: `DecisionRecordWriter.record(DecisionRecord)` with `@Transactional(propagation = MANDATORY)`, the refusal `MSG-P7-009`, the failure `MSG-P7-003`, and the DDL template of `decision_record` applied by this service's own Flyway sequence (DP-03, DP-15).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-14 and SCR-15, one hop per call (DP-19).
- The RESTRUCTURE and SETTLEMENT route sets are in force: the packages and their versions are the ones announced by `rwb.decision.RulePackageInForce.v1` (EV-30), the event the sibling stories of this service already consume, and the embedded Drools runtime is the service template's wave-0 capability (ASM-4372; Rules v4 header, hit policy Unique).
- The signature fact arrives on the case event the parent forwards; the e-signature step itself is rwb-document's and the signature's verification is part of that path, proven by the wave 2 integration harness, so this story adds no contract dependency of its own (ASM-4372; TSD S2 T5.2.2).
- The case status, the operations queue and the one-working-day task timer are rwb-case's; this story reports the hand-over and the parent applies it (ASM-4373; DP-01).
- The settlement instruction is raised from the hand-over by rwb-payment (P8) and the partner side (S9); no published operation names it, and the integration harness proves it (GAP-2661; ASM-4374).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S2-E3008-CON when its tests pass, and this story runs in Draft (realignment v1) until it does.

### 4. Flow

1. The offer is in force: the case is in `OFFER_WITH_CUSTOMER` for a restructure or in `OFFER_WITH_CUSTOMER_SET` for a settlement, and the offer clock of the offer stories runs to the validity date (Rules v4 rows R-RES-09, R-RES-11, R-SET-04, R-SET-06).
2. The customer signs through the e-signature path; the verified signature fact reaches the case router of rwb-case, which raises `CUSTOMER_SIGNED` and forwards it to the running stage child as a signal (ASM-4372; TSD S2 T5.2.2, contract generation and e-signature; FSD S2 A2.8.2, step 1 "Receives its trigger: a completed ACE batch, an event or a timer").
3. Step 1, receive: the workflow takes the case status, `signed`, the verification flag, the signature time and the treatment reference from the signal. It reads no case table and no `recovery_case` row (DP-01; ASM-4373).
4. The signature is resolved against the offer clock: a signature that arrives while the offer timer has not fired is this story's; one that arrives after it fired belongs to the no-signature path of RWB-S2-E3009-APP (R-RES-18) and the stage does not route to operations (Rules v4 row R-RES-18).
5. Step 2, ask Drools: the `EvaluateRules` activity runs the package in force at the version announced by EV-30, under 300 ms in the owning service (ASM-4372). On `OFFER_WITH_CUSTOMER` with `CUSTOMER_SIGNED`, R-RES-16 fires when `signed = Y and signature verified` and answers "Route the case to operations to complete the booking" with `WITH_OPS_BOOKING`. On `OFFER_WITH_CUSTOMER_SET` with `CUSTOMER_SIGNED`, R-SET-10 fires when `signed = Y` and answers "Route the case to operations and raise the payment instruction" with `WITH_OPS_SETTLEMENT` (Rules v4 rows R-RES-16, R-SET-10; TSD S2 T4).
6. Step 3, record and apply, in one transaction: `signature_status` is set to SIGNED (DF-TRT-030), the decision record is written through the library with the rule ID, the rule version and the facts of the signed offer, the `DecisionRecorded` event is written to this service's outbox by the library, and the `SignedOfferHandover` is built with `toState`, the route facts and the instruction flag (DP-03, DP-09; ASM-4371).
7. `buildSignedHandover` completes the element: the treatment and case identifiers, the treatment type, `signatureStatus`, `signedAt`, `validUntil`, `offerAmount`, `toState`, `paymentInstructionRequired`, `ruleId` and `ruleVersion` of RWB-S2-E3008-CON. The five facts without a column are carried here and recorded on the decision record only (ASM-4371).
8. Step 4, finish: the child completes with the hand-over as its result. The parent `CaseWorkflow` moves the case to `WITH_OPS_BOOKING` or `WITH_OPS_SETTLEMENT`, places it in the operations (booking) queue and starts the one-working-day timer of the rule; none of those three writes is this story's (ASM-4373; DP-01).
9. Settlement only: the instruction request flagged on the hand-over is what rwb-payment (P8) acts on when the agreement is booked (R-SET-13); no posting, no due date and no payment row is created here (GAP-2661; ASM-4374).
10. The officer sees the case leave the offer state on SCR-14 Treatment record or SCR-15 Settlement offer, read through the gateway-bff composite route in one hop per call, with `signature_status` shown as SIGNED (DP-19).
11. A repeat `CUSTOMER_SIGNED` for the same treatment — a redelivery of the signal or of the case event behind it — returns the first hand-over: one signature status, one decision record and one stage result, never a second of each (DP-09 inbox dedupe).
12. After the hand-over the case is with operations; R-RES-21 to R-RES-25 and R-SET-13 and beyond are the booking stories', and this stage ends.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without the right in capability area Treatment and offer reads the signed treatment | 403 before any read; the refusal is the guard library's and is logged by it | MSG-P4-002 | TC-E3-008-05 |
| X2 | `signed = N`, or no signature fact on the event | No rule of this story fires and the case stays in the offer state; the no-signature path is RWB-S2-E3009-APP's | None | Section 8, BR1 |
| X3 | The signature arrives after the offer timer fired | The stage does not route to operations; R-RES-18 of the no-signature story applies and the case leaves the offer state there | MSG-S2-003 | Section 8, BR1 |
| X4 | `signed = Y` but the signature is not verified, on a restructure | R-RES-16 does not fire, nothing is written and the case stays in `OFFER_WITH_CUSTOMER`; the officer resolves the signature with the document owner | Not specified in the source documents (GAP-2661; ASM-4372) | Section 8, BR2 |
| X5 | The decision record cannot be written | The transaction rolls back, `signature_status` is not stored, no hand-over is returned and the user sees MSG-P7-003 | MSG-P7-003 | AC4, TC-E3-008-04, TC-E3-008-06 |
| X6 | A record field is refused by the library | Nothing changes and the field is named; the case stays in the offer state | MSG-P7-009 | Section 12.8 |
| X7 | The hand-over does not satisfy RWB-S2-E3008-CON | The apply step fails its validation before the child completes and the workflow retries; no partial element leaves the stage | MSG-GEN-001 | TC-S2-E3008-CON-04 |
| X8 | The same signal is delivered twice | One signature status, one record and one hand-over; the first answer is returned | None | Section 4, step 11 |

X1, X5 and X2 are the exception paths of RWB-E3-008 carried onto the split; X3 is the boundary with the no-signature story, X4 is the verification line the legacy rule states but no source shapes, and X6 to X8 are the paths the published element and its `MANDATORY` record add (GAP-2661; ASM-4371).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-S2-E3008-CON, RWB-PLT-E1027-CON and RWB-PLT-N001-CON with their fakes, on `treatment` in its own schema; needs no live rwb-case, no live rwb-document and no live rwb-payment to start |
| Negotiable | The activity names, the signal handling of a late signature and the log fields are this story's choice; the two rules, the four legacy criteria, the element and the `MANDATORY` record are fixed |
| Valuable | A signature inside the validity period moves the case to operations in one working day with a provable record, which is the turnaround the FSD measures |
| Estimable | One workflow branch, three activities, one element build, one repository write and one test set |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion runs on synthetic treatments and case signals through the contract fakes, plus one component test of the read and the access answer |

### 7. Acceptance criteria

```gherkin
Feature: Route the signed offer to operations for booking

  Scenario: AC1 Route the signed offer to operations for booking (legacy RWB-E3-008 AC1)
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then moves the case to operations when the customer signs inside the validity period
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-RES-16 (legacy RWB-E3-008 AC2)
    Given the rwb-case contract mock returns case status OFFER_WITH_CUSTOMER
    Given a case in state OFFER_WITH_CUSTOMER
    When customer signed
    Then route the case to operations to complete the booking
    Then the case moves to WITH_OPS_BOOKING

  Scenario: AC3 Rule R-SET-10 (legacy RWB-E3-008 AC3)
    Given the rwb-case contract mock returns case status OFFER_WITH_CUSTOMER_SET
    Given a case in state OFFER_WITH_CUSTOMER_SET
    When customer signed
    Then route the case to operations and raise the payment instruction
    Then the case moves to WITH_OPS_SETTLEMENT

  Scenario: AC4 Not recorded (legacy RWB-E3-008 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Target reading.** Every legacy line and every legacy value above is kept character for character, including the legacy repetition of `Then`; what changes is where it runs, who owns the fact and how it is reached. The trigger of AC1 is the `CUSTOMER_SIGNED` case event forwarded by the parent `CaseWorkflow` as a signal; the FSD calls it "a completed ACE batch, an event or a timer" (FSD S2 A2.8.2, step 1) and the stage takes it as an event. The decision log of AC1 and AC4 is the local `decision_record` written through `DecisionRecordWriter.record(DecisionRecord)` with `@Transactional(propagation = MANDATORY)`, refusing with MSG-P7-009 and failing with MSG-P7-003; `decision_log_entry` is P7's central ledger and is neither written nor read here (DP-03, DP-01; TSD S2 T5.3). The case states of AC2 and AC3 are rwb-case's and reach the stage on the forwarded signal; the `rwb-case contract mock` line stands for the case-status answer on that signal, not for a REST call and not for a table read, and the status move itself is the parent's (ASM-4373). "Customer signed" of AC2 and AC3 is R-RES-16 and R-SET-10 of the packages in force, whose versions arrive on `rwb.decision.RulePackageInForce.v1` (EV-30); the verification clause of R-RES-16 (`and signature verified`) is the e-signature fact carried on the same event (ASM-4372; Rules v4 rows R-RES-16, R-SET-10; TSD S2 T4). "Route the case to operations" is the `SignedOfferHandover` returned to the parent with `toState` set to the rule's own target state; the queue, the task and the one-working-day timer are rwb-case's (ASM-4371, ASM-4373). "Raise the payment instruction" of AC3 is the `paymentInstructionRequired` fact of the hand-over, which rwb-payment acts on when the settlement is booked; no instruction operation is published by any source, so its shape is not invented here (GAP-2661; ASM-4374). Nothing is read from another service's table, and no ACE customer or payment fact is copied: the legacy data rows `v_ace_customer` and `v_ace_payment` are reached through rwb-source-data's contract or the service's own read-only views only if a later step needs them, and this slice needs neither (DP-05; TSD S2 T0.4).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | On `OFFER_WITH_CUSTOMER` with `CUSTOMER_SIGNED`, when `signed = Y and signature verified`, the case is routed to operations to complete the booking and the target state is `WITH_OPS_BOOKING` | TSD S2 T4 R-RES-16; Rules v4 R-RES-16; FSD S2 A2.8.3.1 |
| BR2 | On `OFFER_WITH_CUSTOMER_SET` with `CUSTOMER_SIGNED`, when `signed = Y`, the case is routed to operations and the payment instruction is raised, and the target state is `WITH_OPS_SETTLEMENT` | TSD S2 T4 R-SET-10; Rules v4 R-SET-10; FSD S2 A2.8.3.1 |
| BR3 | No value a business person may change is written in code: the two target states, the rule IDs, the rule versions and the one-working-day timer are read as values in force from the package and the parameters | FSD S2 A2.8.3.1 BR-S2-008; ASM-4372 |
| BR4 | The signature is kept as `signature_status` of the treatment, one of PENDING, SIGNED or NOT_SIGNED; this path writes SIGNED and no other value | TSD S2 T3.1 DF-TRT-030 and T3.2 LOV-TRT-SIGNATURE |
| BR5 | A signature that arrives after the offer validity date does not route the case to operations; expiry and decline are R-RES-18 and R-RES-17 of RWB-S2-E3009-APP | Rules v4 rows R-RES-17, R-RES-18; TSD S2 T4 |
| BR6 | The decision record is written in the same transaction as the signature status, or neither is stored and the action is not taken | ADR-022; DP-03; TSD S2 T0.3 DP-03 |
| BR7 | The case status, the operations queue and the task timer stay rwb-case's: the stage returns the hand-over and the parent applies it; no case table is read or written here | ASM-4373; DP-01 |
| BR8 | The hand-over is one element with one published shape, and the facts without a column are recorded on the decision record and never stored on `treatment` | RWB-S2-E3008-CON; ASM-4371 |
| BR9 | The signed path runs unattended: no person approves the route to operations, and the only human step is the customer's signature outside the Workbench | FSD S2 A2.8.3.3, primary role "None; runs unattended" |

**Where each rule lives in the target.** BR1 and BR2 are the two rule outcomes this workflow reports: the package decides them and the parent applies them, so AC2 and AC3 assert the hand-over element and the mock case status, not a local status write (ASM-4373). BR3 is the reason the two states, the rule IDs and the timer are read from the package and never written as constants. BR4 is the only business column this story writes. BR5 is the boundary with the no-signature story: the stage resolves the signature against the offer timer and hands nothing over once the timer has fired. BR6 is the `MANDATORY` propagation of the record write. BR7 and BR8 are the two boundaries of the split, with rwb-case and with the published element, and BR9 is why no approval step appears in the flow.

### 9. State transitions

None of this story's own: the case status is rwb-case's (DP-01; ASM-4373), and the `treatment` row's states (Draft, submitted, approved, booked, broken) are set by the treatment and booking stories. This story reports an outcome for each rule and changes the state of its own `TreatmentWorkflow` execution.

| From | Rule and event | Condition | To (reported to the parent) |
|---|---|---|---|
| `OFFER_WITH_CUSTOMER` | R-RES-16, `CUSTOMER_SIGNED` | `signed = Y and signature verified`, inside the validity period | `WITH_OPS_BOOKING`; `paymentInstructionRequired = false` |
| `OFFER_WITH_CUSTOMER_SET` | R-SET-10, `CUSTOMER_SIGNED` | `signed = Y`, inside the validity period | `WITH_OPS_SETTLEMENT`; `paymentInstructionRequired = true` |
| `OFFER_WITH_CUSTOMER` | none, `CUSTOMER_SIGNED` | `signed = Y` with the signature not verified | No hand-over; the case stays in the offer state (X4) |
| `OFFER_WITH_CUSTOMER` or `_SET` | none, late signature | The offer timer fired before the signature arrived | No hand-over; R-RES-18 belongs to RWB-S2-E3009-APP (X3) |
| `OFFER_WITH_CUSTOMER` or `_SET` | none, `signed = N` | No signature | No hand-over; R-RES-17 belongs to RWB-S2-E3009-APP (X2) |

| Workflow state | Meaning |
|---|---|
| RUNNING, waiting on the case signal | The stage is open and the offer is with the customer |
| RUNNING, applying | A signature arrived, the rule fired and the apply step is running |
| COMPLETED | The hand-over was returned; the parent owns everything after it |
| FAILED | The record write or the element validation failed and the apply step rolled back |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF, the case workflow module of rwb-case | Starts the stage child and forwards the `CUSTOMER_SIGNED` case event; holds the case status, the operations queue and the one-working-day timer (ASM-4373) |
| The service identity of the rwb-treatment worker | Runs the workflow and its three activities under the service's own identity (TSD S2 T6.2) |
| RW-RESTRUCT, restructuring officer (FCR) | Reads the signed treatment and its signature status on SCR-14 and SCR-15, right R in capability area Treatment and offer; signing itself is the customer's, outside the Workbench |
| RW-CASEOWN, case owner | Reads the same record, right R (TSD S2 T6.1) |
| RW-TEAMMGR, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE, SY-RULES, SY-AGENT | Read only, right R (TSD S2 T6.1) |
| rwb-document (P5) | Owns the e-signature execution and the documents of the offer, and the verification behind the fact this story receives (ASM-4372) |
| rwb-payment (P8) and rwb-partner (S9) | Act on the settlement instruction the hand-over flags; no instruction record is written here (ASM-4374) |
| The recovery squad (RW-TRIBE) | Writes the workflow branch, the three activities, the repository write and the tests |
| No delegation of authority level applies | The rule decides the route to operations and no person approves it (BR9) |

The access check itself is the platform guard library's and is declared here as the capability area and the right only (TSD S2 T6.1). No credential and no personal name appears in the workflow input, the activity payloads or the logs, which carry case IDs, treatment IDs, codes, states and dates only.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-002 | treatment | case_id | Read |
| DF-TRT-003 | treatment | decision_log_id | Write |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-007 | treatment | offer_amount | Read |
| DF-TRT-010 | treatment | valid_until | Read |
| DF-TRT-012 | treatment | booked_at | Read (left to the booking story) |
| DF-TRT-030 | treatment | signature_status | Write (SIGNED) |
| DF-DEC-001 to DF-DEC-018 | decision_record | the local record shape declared by RWB-PLT-E1027-CON | Write |
| DF-REF-001 to DF-REF-015 | rule_row | rule ID, rule version and the labels the evaluated rule reports | Read (through the package, not from its table) |
| DF-CAS-001 to DF-CAS-023 | recovery_case | the case status and the signed facts, read from the case signal only | Read (from the signal) |
| DF-WRK-009 to DF-WRK-016 | assignment | Not used: the operations queue and its task are rwb-case's | Not read or written |
| DF-PRT-008 to DF-PRT-016 | partner_instruction | Not used: the legacy row is S9's and this story writes no instruction | Not read or written |
| DF-ACE-043 to DF-ACE-054 | v_ace_payment | Not used: no payment fact is needed to route the signed offer | Not read or written |
| DF-ACE-055 to DF-ACE-074 | v_ace_customer | Not used: no customer fact is needed to route the signed offer | Not read or written |

`signature_status` is the only business column this story writes, and it is one of the 33 fields of TSD S2 T3.1 with its list LOV-TRT-SIGNATURE (PENDING, SIGNED, NOT_SIGNED). `decision_record` is written through the library and never by a repository of this story (DP-03, DP-01). The case, the assignment, the queue and the timer belong to rwb-case, and the partner instruction to S9, so no row of those tables is read or written here (Ownership Map; ASM-4373). The two ACE views the legacy story lists carry customer and payment facts that the routing rule does not need; where a later step does need one, it comes through rwb-source-data's contract or the service's own read-only view and is copied nowhere (DP-05; TSD S2 T0.4). Field identifiers are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). This story provides no operation of its own: the two rows of the legacy endpoint table are declared by RWB-S2-E3001-CON and named here, never redeclared.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/treatments` | `TreatmentRequest` in, `Treatment` out, declared by RWB-S2-E3001-CON; the treatment the signed offer belongs to is opened there, before this stage | Treatment and offer, right C, scope applied | `Idempotency-Key` header |
| GET | `/treatments/{treatmentId}` | `Treatment` of RWB-S2-E3001-CON, with `signatureStatus` (DF-TRT-030), `validUntil` (DF-TRT-010) and `bookedAt` (DF-TRT-012) | Treatment and offer, right R, scope applied | Not applicable |

The legacy story lists these two operations and nothing else; no source publishes a path for the signature or for the hand-over, so none is invented. The signature arrives on the case event and the hand-over is the result element of RWB-S2-E3008-CON (GAP-2661; ASM-4371). The error set of the read is RWB-S2-E3001-CON's: 401, 403 with MSG-P4-002, 404 and 503, and it is not restated here.

#### 12.2 REST operations consumed

None. This story calls no service in its own name. The signature fact arrives on the case signal the parent `CaseWorkflow` forwards, the case status arrives on the same signal, and the package version arrives on `rwb.decision.RulePackageInForce.v1` (ASM-4372, ASM-4373). The e-signature activity of rwb-document and the instruction path of rwb-payment are named as their owners' and are proven by the wave 2 integration harness; the Work Package fixes the contract dependencies of this story as None, and the `rwb-case contract mock` of AC2 and AC3 is a test-only stand-in for the signal answer (ASM-4374).

#### 12.3 Events published

None of this story's own. The service topic is `rwb.treatment.events.v1` with event names `rwb.treatment.<Event>.v1` (DP-14); its two service events, TreatmentApproved (EV-10) and TreatmentClosed, belong to the approval and closure stories (TSD S2 T5.3). The signed path writes no outbox row itself: the `DecisionRecorded` event on the shared topic `rwb.decision-record.v1` is written to this service's outbox by the decision-record library in the apply transaction, with that contract's envelope and key (DP-03, DP-09).

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` (EV-30) | `rwb.decision.events.v1` | P7 rwb-decision | Announces the RESTRUCTURE and SETTLEMENT packages and their versions; the workflow evaluates the version in force and stamps it on the hand-over's record (BR3) |

The event is consumed through the inbox of the outbox library, so a redelivery does not swap a package twice for one version. `CUSTOMER_SIGNED` is not a topic subscription of this story: it reaches the stage as the `CaseEvent` signal the parent forwards, after the case router of rwb-case has received the connected events of this service — TreatmentBooked (EV-11) and PaymentMissed (EV-12) on `rwb.payment.events.v1`, and DeviationRaised (EV-06) on `rwb.deviation.events.v1` (TSD S2 T5.2.2 and T5.3; ASM-4373).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow`, signed branch | Workflow, the stage child of `CaseWorkflow`, one execution per case and stage, with the four steps receive, evaluate, record and apply, finish | `rwb-treatment` in namespace `rwb-recovery` | Input: case ID, stage, route set, case status, `signed`, the verification flag and the signature time on the signal; output: the `SignedOfferHandover` of RWB-S2-E3008-CON |
| `EvaluateRules` | Activity (existing, reused) | `rwb-treatment` | The package in force, its version, the case state and `CUSTOMER_SIGNED`; the fired rule R-RES-16 or R-SET-10 with its target state |
| `buildSignedHandover` | Activity | `rwb-treatment` | The treatment and the rule answer; the eleven properties of the element, validated against RWB-S2-E3008-CON |
| `recordSignedOutcome` | Activity | `rwb-treatment` | One transaction: `signature_status` SIGNED, the decision record through the library with the rule ID and version, the outbox row of the record event, and the hand-over as the child's result |

The workflow is the stage child the TSD names for rwb-treatment, run on queue `rwb-treatment` (TSD S2 T0.1 and T5.2.1; Temporal and Drools Design slide 11); the two new activity names are this story's design choice and are fixed by no source document (GAP-2661; ASM-4371). The retry policy is the workflow kit's: 1 s initial interval, back-off 2, 10 attempts, and no retry on a refused record (ASM-4372). The stage owns no timer: the one-working-day follow-up of the rule is a case task timer of rwb-case (ASM-4373).

#### 12.6 Schedules

None. The stage is started by the parent `CaseWorkflow` and advanced by the case signal it forwards; it owns no Temporal Schedule and no legacy job, and the FSD's mention of a completed ACE batch as a possible trigger is rwb-source-data's overnight path, not a schedule of this service (FSD S2 A2.8.2; DP-10).

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | Created by the treatment story's Flyway version with the 33 fields of TSD S2 T3.1; this story writes `signature_status` inside `recordSignedOutcome` and creates no column |
| `decision_record` | `rwb_treatment` | PLT, a library object | Written through `DecisionRecordWriter.record(...)` in the same transaction; the shape and the DDL template are RWB-PLT-E1027-CON's (DP-03) |
| `decision_log_entry` | `rwb_decision` | P7 | Never read and never written here; the central ledger is P7's (DP-01) |
| `recovery_case`, `assignment`, `timer`, the operations queue | `rwb_case` | P3 | Never read and never written here; the case status arrives on the signal and the queue and its timer are the parent's (ASM-4373) |
| `partner_instruction` | `rwb_partner` | S9 | Never read and never written here; the legacy data row is S9's and the instruction is flagged on the hand-over only (ASM-4374) |

No table of another service is read and no foreign key crosses a schema (DP-01). The five facts without a column — `signedAt`, `toState`, `paymentInstructionRequired`, `ruleId` and `ruleVersion` — are recorded on the decision record and create no table and no column (GAP-2661; ASM-4371).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-S2-E3008-CON hand-over fake | The `SignedOfferHandover` element | A complete booking hand-over; a complete settlement hand-over with the instruction flag; an element missing a required property; an element with a `toState` the contract does not publish |
| RWB-PLT-E1027-CON decision-record fake | The record write | An accepted record with a chain sequence and an entry hash; a refusal with MSG-P7-009 and the field; a failure with MSG-P7-003; the outbox row present and absent after a rollback |
| rwb-case case-status mock | The case-status line of AC2 and AC3 | `OFFER_WITH_CUSTOMER` for AC2 and `OFFER_WITH_CUSTOMER_SET` for AC3, on the forwarded signal; no case table and no case REST call |
| RWB-PLT-N001-CON route fake | The composite route of SCR-14 and SCR-15 | The two screen reads of a signed treatment, one hop each |
| Signature fixture | The signature fact on the case event | `signed = Y` and verified; `signed = Y` and not verified; `signed = N`; a signature that arrives after the offer timer fired |

The hand-over and decision-record fakes are the published contracts of those two stories, the route fake is the platform edge contract's, and the signature fixture stands in for the e-signature path of rwb-document until the integration harness runs against it; the case-status mock is test-only and is the signal answer recorded with ASM-4373 (GAP-2661; ASM-4372).

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 operations on `/api/recovery/treatment/v1`, both declared by RWB-S2-E3001-CON | None | OpenAPI 3.1; the controller validates and maps errors to problem responses |
| Kafka | None of its own | 1 event (`rwb.decision.RulePackageInForce.v1`) | Own topic `rwb.treatment.events.v1` for the service's own events; inbox dedupe by cloud event id; the record event goes out through the library's outbox |
| Temporal | None | `TreatmentWorkflow`'s signed branch and 3 activities on `rwb-treatment` | Namespace `rwb-recovery`; no timer and no Schedule of this story |
| File | None | None | No file is read or written |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, modules `signed` and `handover`, with the published types in `...treatment.api` (DP-13, DP-14). Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule the signed path is built on: the signature status and the record are one commit or neither is. DP-05 is applied and empty: the two ACE views the legacy data table lists carry no fact the routing rule needs, and any later need is met through the owner's contract or a read-only view, never by a copy (TSD S2 T0.4). DP-13 fixes the base of the read, and DP-19 is the route by which the officer sees the result. The other patterns of the service — the owner schema, the workflow kit, the outbox and the embedded rules runtime — are service-template capabilities and add no dependency of this story (ASM-4372, ASM-4373).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `TreatmentWorkflow` (signed branch) | Workflow | The four steps, the signature gate, the offer-clock resolution and the hand-over result (BR1, BR2, BR5) |
| `EvaluateRules` | Activity | Runs the package in force and returns the fired rule and its target state (BR3) |
| `buildSignedHandover` | Activity | Builds and validates the eleven properties of the element (BR8) |
| `recordSignedOutcome` | Activity | One transaction: `signature_status`, the decision record, the outbox row and the result (BR6) |
| `TreatmentReadController` | Controller | The treatment read of the legacy row, with the access right and the error map (BR7) |
| `TreatmentRepository` | Repository | Reads the treatment and writes `signature_status` in `rwb_treatment` (DP-01) |
| `Migrations` | Migration | The `signature_status` field on the per-service sequence where it is missing, and no new column for the five facts (DP-15) |

**Database.** `treatment` holds `signature_status` (DF-TRT-030, varchar(12), LOV-TRT-SIGNATURE) with the seven standard columns of T3.0 (TSD S2 T3.1). No signed-at column, no route column and no instruction column exists: `signedAt`, `toState`, `paymentInstructionRequired`, `ruleId` and `ruleVersion` are request-context facts recorded on the decision record (BR8; GAP-2661; ASM-4371). `decision_record` is the library object applied by this service's own Flyway sequence in `rwb_treatment`.

**Configuration and reference data.** The two target states, the two rule IDs and the one-working-day timer are values in force of the RESTRUCTURE and SETTLEMENT packages and of the parameters, never constants (BR3; Rules v4 rows R-RES-16, R-SET-10). The package version arrives on EV-30. The treatment type and signature lists are reference data read through the owner's contract (DP-07 is a service-template capability, ASM-4372). The capability area "Treatment and offer" and the right R are access rows of the platform guard library, not constants of this story.

**Build steps**

1. The Flyway version that carries `signature_status` where it is missing, with no column for the five request-context facts (BR8, DP-15).
2. The signed branch of `TreatmentWorkflow` and its input record, registered on `rwb-treatment`, with the signature gate and the offer-clock resolution (BR1, BR5).
3. The `EvaluateRules` call with the package version from EV-30 and the R-RES-16 and R-SET-10 outcome mapping (BR2, BR3).
4. `buildSignedHandover` against the element of RWB-S2-E3008-CON, with the validation and the refusal of an unpublished `toState` (BR8).
5. `recordSignedOutcome` with `signature_status`, the `MANDATORY` record write and the outbox row (BR4, BR6).
6. The controller for the treatment read, with the access right and the error map (BR7).
7. Tests for AC1 to AC4 against the fakes and the signature fixture.
8. The target reading note of section 7 reviewed with the owners of rwb-case, rwb-document and rwb-payment before the contract freeze (ASM-4372, ASM-4373, ASM-4374).

**Feature flag.** `rwb.treatment.signed-offer-handover`.

**Done when.** The tests in section 16 pass, the stage starts for a synthetic restructure case and for a settlement case and returns a booking hand-over and a settlement hand-over respectively, `signature_status` and one `decision_record` are committed together, the five request-context facts appear on the record and in no column, a forced record failure leaves nothing behind with MSG-P7-003, a signature after the offer timer routes nothing, and SCR-14 shows the SIGNED status through the composite route in SIT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A role without the right in Treatment and offer reads the signed treatment | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | The hand-over fails its validation for a missing or out-of-domain property | Enter {field}. |
| MSG-P7-003 | The decision record cannot be written and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | The record is refused for a missing or invalid field (log and incident, not the screen) | The decision record was refused: {field} is missing or not valid. |
| MSG-S2-003 | The offer reaches its validity date before a signature arrives | The offer to the customer ends on {date}. |
| MSG-S2-001 | A settlement offer falls below the floor and goes for approval | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-002 | The payoff the offer rests on is older than the freshness rule | The payoff is from {date}. A new figure has been requested. |

The seven texts are the legacy texts carried unchanged; MSG-S2-001 and MSG-S2-002 are raised by the settlement and payoff paths of the sibling stories and are named here because the legacy story carries them, MSG-S2-003 is the offer clock's, MSG-GEN-001 is the field refusal of the element, MSG-P7-009 and MSG-P7-003 are the record library's, and MSG-P4-002 is the guard library's answer (RWB-PLT-E1027-CON; TSD S2 T6.1). Thai text for each message follows decision DL10. Where the verification line of R-RES-16 fails no message is published by any source (GAP-2661; ASM-4372).

### 15. Screens and states

SCR-14 Treatment record with the states Draft, submitted, approved, booked and broken, and SCR-15 Settlement offer with the states Draft, below floor, approved, sent and accepted, show the result of this story: the offer leaves the sent or approved state, `signature_status` reads SIGNED, and the case is with operations. Both are reached through the gateway-bff composite route, which calls rwb-case and rwb-treatment in parallel, one hop each (DP-19; RWB-PLT-N001-CON). The screen state lists of the legacy story name no operations state, so the operations step is shown through the case status the parent holds and not through a new screen state (GAP-2661; ASM-4373). The screen field list and the composite route specification belong to the platform edge story and the screen owners, and this story fixes the service side of the answer only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-008-01 | AC1 | End to end | Route the signed offer to operations for booking |
| TC-E3-008-02 | AC2 | End to end | Rule R-RES-16 |
| TC-E3-008-03 | AC3 | End to end | Rule R-SET-10 |
| TC-E3-008-04 | AC4 | End to end | Not recorded |
| TC-E3-008-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E3-008-06 | Principle 5 | Component | A forced decision log write failure stops the action with MSG-P7-003 |

The six legacy test case IDs, their Covers and their Data are kept in order and character for character. The legacy level "System" maps to "End to end" for the four criteria and to "Component" for the Access and Principle 5 cases, as in the other stories of this run. Where the legacy Covers names `Access`, the criterion is the published answer of the platform guard library on the treatment read; where it names `Principle 5`, the criterion is the `MANDATORY` record write of RWB-PLT-E1027-CON rolling the apply step back. The hand-over, decision-record and route fakes of section 12.8 stand behind every case, and the signature fixture supplies the four signature states. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 2 integration harness and are not listed here.

### 17. Guardrails

- No business value in code: the two target states, the two rule IDs, the rule versions and the one-working-day timer are values in force read from the package and the parameters, never constants (BR3).
- No personal data in logs, events, workflow inputs or the fixture: the rows carry case IDs, treatment IDs, codes, states and dates only; test data is synthetic and the case subject is never in a payload (DP-09).
- No read of another service's table: the case status and the signed facts arrive on the forwarded signal, the package version on its event, and `recovery_case`, `assignment`, `timer`, `partner_instruction` and `rule_row` are never named in SQL (DP-01, ASM-4373).
- No new column for a routing or instruction fact: `signedAt`, `toState`, `paymentInstructionRequired`, `ruleId` and `ruleVersion` are recorded on the decision record (BR8).
- The decision record is written in the same transaction as `signature_status`, with `MANDATORY`; a forced failure leaves nothing behind and shows MSG-P7-003 (DP-03, BR6).
- The stage owns no timer and no Schedule: the one-working-day follow-up is a task timer of rwb-case and the offer clock is the offer stories' (ASM-4373; DP-10).
- ACE data only through the owner's contract or the `v_ace_*` views, and only where a step needs it: this slice reads neither view (DP-05; TSD S2 T0.4).
- An applied migration is never edited: a correction to `signature_status` is a new version on the service sequence (DP-15).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-003 | A signed offer routes to operations for booking, and an unsigned or declined offer returns the case to its prior status | Program, 5.9 | FEAT-TRT-08 | 07 Route, settle and claim | R-RES-16; R-SET-10 | TC-E3-008-01, TC-E3-008-02, TC-E3-008-03, TC-E3-008-04, TC-E3-008-05, TC-E3-008-06 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3008-CON | Contract | H: declares the `SignedOfferHandover` element, its validation and its fakes |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library and its `MANDATORY` transaction rule |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route of SCR-14 and SCR-15 |
| RWB-S2-E3001-CON, RWB-S2-E3001-APP | Contract, App development | The treatment entity and the two operations of the legacy endpoint table; named, not redeclared |
| RWB-S2-E3002-APP, RWB-S2-E3004-APP, RWB-S2-E3007-APP | App development | The offer, its validity clock and its expiry, which this stage reads as facts on the signal |
| RWB-S2-E3009-APP | App development | The no-signature path (R-RES-17, R-RES-18), the other half of REQ-S2-003 |
| The booking stories of S2 (FEAT-TRT-10) | App development | R-RES-21 to R-RES-25 and R-SET-13: booking to ALS and NLEADS, the plan schedule and the settlement booking |
| RWB-P7-E1073-CON | Contract | The rule package registry that announces the two packages on EV-30 |
| rwb-document (P5), rwb-payment (P8), rwb-partner (S9) | App development | The e-signature execution and the settlement instruction the hand-over flags |
| rwb-case (P3) | App development | The `CaseWorkflow` parent, the case status, the operations queue and the task timer |
| The wave 2 integration harness | Integration | I: the cross-service proof of the same legacy key against the live owners |

### 19. Out of scope

- The published `SignedOfferHandover` element, its properties, its validation and its fakes: RWB-S2-E3008-CON.
- The treatment entity, its other fields, its states and the two operations of the legacy endpoint table: RWB-S2-E3001-APP and RWB-S2-E3001-CON.
- The offer, the offer clock, the counter-offer path and the below-floor approval: RWB-S2-E3002-APP, RWB-S2-E3003-APP, RWB-S2-E3004-APP and RWB-S2-E3007-APP.
- The return on no signature, on decline and on expiry (R-RES-17, R-RES-18, R-RES-20): RWB-S2-E3009-APP.
- Booking to ALS and NLEADS, the plan schedule and the settlement booking (R-RES-21 to R-RES-25, R-SET-13): the booking stories of S2.
- The e-signature execution, the offer documents and the signature verification itself: rwb-document (P5).
- The payment instruction record, the payment posting and the settlement due date: rwb-payment (P8) and rwb-partner (S9).
- The case status, the operations queue, the assignment and the task timer: rwb-case (P3), RWB-P3-E2004-APP and its contract.
- The decision-record library, its DDL template, its envelope and its exceptions: RWB-PLT-E1027-CON and RWB-PLT-E1027-APP; the central ledger: the P7 ledger story.
- SCR-14 and SCR-15, their field list and the gateway-bff composite route: the platform edge story and the screen owners (DP-19).
- The real cross-service proof of the signed route, the record and the instruction: the wave 2 integration harness.
