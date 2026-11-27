# RWB-S2-E3002-APP Offer a settlement inside the range

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: application slice split from RWB-E3-002 for rwb-treatment. The four legacy acceptance criteria are kept word for word with their origin tag and now run on the settlement branch of `TreatmentWorkflow` on task queue `rwb-treatment`, reached through the gateway-bff composite route (DP-19) and the base `/api/recovery/treatment/v1` (DP-13); the one `recovery` schema becomes `rwb_treatment` and no other service's table is read (DP-01); the legacy `DecisionLogWriter` write to the shared `decision_log_entry` becomes the local decision record of RWB-PLT-E1027-CON written in the same transaction as the change (DP-03); the offer operation, its body and the range and floor facts have no source specification and are declared as the working read of the assumption (GAP-1870; ASM-3066); the offer operation is published as `/offer` under the source precedence rule while the TSD form `/submit` is recorded as superseded and not published (GAP-1871; ASM-3067). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S2-E3002-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3002-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S2-M |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S2-E3002-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **restructuring officer (FCR)**, I want **to build and send a settlement offer inside the calculated range from one screen, with the terms of the draft saved as I go, the below-floor case sent for approval, the offer validity shown and the whole decision recorded in the same transaction**, so that **restructures and settlements reach booking in days instead of the 23 to 26 days they take today, and no offer leaves the Workbench that the rule set did not evaluate**.

This is the application slice of legacy RWB-E3-002. It owns:

- all four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages, screens and data rows they depend on;
- the settlement branch of `TreatmentWorkflow` on task queue `rwb-treatment` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` owned by rwb-case, with the activities `buildSettlementOffer`, `checkFloor` and `recordAndApply` (Architecture v5 slide 18; Temporal and Drools Design slides 13 and 18);
- `POST /treatments/{treatmentId}/offer` and `PATCH /treatments/{treatmentId}` on base `/api/recovery/treatment/v1`, under capability area "Treatment and offer" with right U and an `Idempotency-Key` on the offer (DP-13; TSD S2 T-A.1 API-S2-003 and API-S2-004, with the operation name of Architecture v5 slide 18);
- the below-floor check against the floor in force, the offer validity check and the stale-payoff warning, with MSG-S2-001, MSG-S2-003 and MSG-S2-002;
- the local decision record of the offer, written through RWB-PLT-E1027-CON in the same transaction as the `treatment` row (DP-03);
- the writer of the settlement columns of `treatment` in schema `rwb_treatment`, and the stage outcome the parent `CaseWorkflow` uses to move the case status.

It does not own: the published shape of the two operations, the request and response elements, the error set and the fakes, which are RWB-S2-E3002-CON; the approval of a below-floor offer and its approval matrix, which are RWB-S2-E3003-APP and RWB-S2-E3003-CON; the creation of the treatment record and the treatment read, which are RWB-S2-E3001-APP; the TDR plan body, which is RWB-S2-E3004-APP; the affordability pre-assessment through ACE, which is RWB-S2-E3005-APP; the case and its status, which are rwb-case's; the payoff and the range calculation, which are S1 rwb-valuation's (FEAT-VAL-06); the decision-record library, which is RWB-PLT-E1027-APP; the gateway-bff composite route, which is RWB-PLT-N001-CON; and the deployment of this build, which is the wave 2 integration harness and the platform DevOps stories.

### 2. Business rationale

Legacy RWB-E3-002 gave the restructuring officer one screen on which to build and send a settlement offer inside the range that the payoff calculation produced. The functional specification keeps the objective and its metric — a restructure turnaround of 5 days, measured on the decision log and the Workbench records, reviewed monthly, against the 23 to 26 days the process takes today — and the program keeps both halves of the rule: REQ-S2-004 states that settlement terms are negotiated inside a rule-set range and that anything outside the range needs approval, and REQ-S2-002 states that an offer carries a validity period and that expiry returns the case to the status it came from. The legacy guardrail BR-S2-002 stands unchanged: no value a business person may change is written in code; it is read from reference data with its version.

What D-RCV-60 changes is where the offer is built, what it is written to and how the range reaches it. In the monolith the screen, the offer columns and the decision log row sat in one `recovery` schema and the range and the floor were read in the same process. In the target:

- the settlement branch of `TreatmentWorkflow` runs on task queue `rwb-treatment` in namespace `rwb-recovery` as the stage child of `CaseWorkflow`, so the case keeps one parent workflow from entry to closure and the stage runs where its rules and data live (Architecture v5 slide 18; Temporal and Drools Design slides 13 and 18);
- the offer and its draft terms are written to `treatment` in `rwb_treatment` (DP-01), reached through the gateway-bff composite route (DP-19) and the base `/api/recovery/treatment/v1` (DP-13);
- the decision is recorded through the local decision-record library in the same transaction as the change (DP-03), because `decision_log_entry` is P7's ledger and no service reads or writes it;
- the range, the floor and the payoff are facts on the route decision signal that rwb-case forwards, calculated by S1 rwb-valuation under FEAT-VAL-06, and nothing about them is copied into `rwb_treatment` (GAP-1870; ASM-3066);
- the setup of the case — pick-up by an officer and the return of the calculated plan after the affordability check — is reported to the parent workflow, which owns and moves the case status, because rwb-case owns the case and its CMMN state (ASM-3062).

No business value moves. The range bounds, the floor, the approval matrix and the offer clocks stay values in force in the owner's data. The offer validity of 14 days of the Temporal and Drools Design slide 18, and the 2 working days of an officer review in the same source, are read from reference data with their version and never written in code (BR-S2-002).

### 3. Preconditions

- RWB-S2-E3002-CON is published: the two operations, the `SettlementOffer` and `TreatmentUpdate` elements, the request-context facts `rangeLow`, `rangeHigh` and `floor`, the response flag `belowFloor`, the error set, the `Idempotency-Key` rule, the compatibility rule and the fakes are baselined and handed to this story. The element contents have no source specification and are published as the working read (GAP-1870; ASM-3066), and the operation is published as `/offer` while the TSD form `/submit` is recorded as superseded (GAP-1871; ASM-3067).
- RWB-PLT-E1027-CON is published with its writer fake: `DecisionRecordWriter.record(DecisionRecord)` runs with `@Transactional(propagation = MANDATORY)`, refuses with MSG-P7-009 and fails with MSG-P7-003, so the offer and its record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-14 and SCR-15 reach this service through the gateway-bff composite route, one hop each, and no screen calls a service directly (DP-19).
- The route decision signal is available: the parent `CaseWorkflow` forwards the case status change to the running stage, and the signal that starts the settlement stage carries the route, the payoff with its date, `rangeLow`, `rangeHigh` and `floor` as calculated by S1 rwb-valuation (FEAT-VAL-06). Where the S1 contract fixes the field names of that payload, they are copied from it; no source document fixes them here (GAP-1870; ASM-3066).
- The case status is not this service's: the stage reports an outcome and the parent moves the status, so no case table is read or written here (DP-01; ASM-3062).
- The embedded Drools runtime and the SETTLEMENT rule package are the service template's wave-0 capability, and the package version in force arrives on `rwb.decision.RulePackageInForce.v1`; this story names the package and its version and adds no build dependency of its own (ASM-3063).
- The access guard, the outbox and inbox library and the workflow kit are service-template capabilities; this story declares the capability area "Treatment and offer", the right U and the call types and adds no build dependency of its own (ASM-3064).
- The per-service Flyway sequence of rwb-treatment carries `treatment` with DF-TRT-001 to DF-TRT-033 and the library object `decision_record`; this story adds no table and never edits an applied migration.
- The treatment row the offer patches is the one RWB-S2-E3001-APP creates; this story's tests insert their own fixture rows, and the Work Package records no wait on that sibling because the H list is `RWB-S2-E3002-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON` only.
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S2-E3002-CON when its tests pass.

### 4. Flow

1. rwb-case's `CaseWorkflow` receives the case status change through the case router and forwards it to the running `TreatmentWorkflow` child on queue `rwb-treatment` as a signal; the stage never calls rwb-case (Temporal and Drools Design slide 13, the four steps receive, ask, record and apply, wait).
2. The settlement stage holds the facts it was started with: the route R2, the payoff and its date, `rangeLow`, `rangeHigh` and `floor` from the S1 calculation, and the rule package in force. Nothing is copied into `rwb_treatment` (GAP-1870; ASM-3066).
3. Restructuring officer or case owner: opens SCR-15 Settlement offer for the case through the gateway-bff composite route, which answers from `GET /treatments/{treatmentId}` of RWB-S2-E3001-CON (DP-19).
4. The officer edits the draft terms and calls `PATCH /treatments/{treatmentId}` with `TreatmentUpdate` under right U; `buildSettlementOffer` validates the fields, resolves the case through the signal and writes the draft columns of `treatment`.
5. `checkFloor` evaluates the SETTLEMENT package in the version in force: an amount at or below the floor raises `belowFloor` with MSG-S2-001 and the offer moves to the below-floor state of SCR-15, where the approval path of RWB-S2-E3003-APP takes it; an amount above the floor keeps the offer inside the range (R-SET-04, R-SET-05).
6. The officer submits the offer with `POST /treatments/{treatmentId}/offer`, carrying `SettlementOffer` and an `Idempotency-Key`; a repeat of the same key returns the first answer and stores no second row.
7. `checkFloor` also tests the payoff date against the freshness limit: an older payoff raises MSG-S2-002 and a new figure is requested, and the offer is not moved out of the draft state.
8. `recordAndApply` assembles the `DecisionRecord` — the decision code of the settlement offer event, the case, the rule ID with the package version, the recommendation, the final call and the actor — and writes it through `DecisionRecordWriter.record` in the caller's transaction, then writes the `treatment` row in the same transaction (DP-03).
9. The stage publishes nothing: the offer is reported to the parent `CaseWorkflow`, which moves the case status, and the service events of rwb-treatment stay with the stories that own them (DP-01; ASM-3062).
10. On the prepared offer the stage reports the outcome of R-RES-07 or R-RES-04 so the parent moves the case to WITH_FCR_OFFICER; the officer sees the calculated plan, the range, the floor, the haircut and the validity date on SCR-15.
11. The offer carries its validity: `valid_until` is written on the draft and the officer sees MSG-S2-003 with the date the offer to the customer ends (REQ-S2-002).
12. A counter-offer outside the range returns the case to the officer under R-RES-15, and a deviated offer is routed under R-RES-10 or R-SET-05 by the sibling approval story.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The role does not hold right U on "Treatment and offer" | 403 before any read or write; the refusal is the guard library's and is logged by it | MSG-P4-002 | AC1, TC-E3-002-05 |
| X2 | The decision record cannot be written | `recordAndApply` throws before the `treatment` row is written and the transaction rolls back; nothing changes | MSG-P7-003 | AC4, TC-E3-002-06 |
| X3 | The decision record is refused for a missing or invalid field | Nothing is written and the field is named in the service log and the incident | MSG-P7-009 | AC4 |
| X4 | The offer amount is at or below the floor in force | The offer is stored in the below-floor state with `belowFloor` true and the gap to the floor, and the approval path of the sibling story takes it | MSG-S2-001 | AC1, Section 8 |
| X5 | The payoff date carried on the signal is older than the freshness limit | The warning is shown and a fresh payoff is requested; the offer stays in the draft state | MSG-S2-002 | AC1 |
| X6 | The validity date is absent or not in the future | The request is refused with 422 and the field is named | MSG-GEN-001 | AC1 |
| X7 | The same `Idempotency-Key` is presented twice | The first answer is returned and no second `treatment` row and no second decision record are written | None | AC1 |
| X8 | The case is not at a status the settlement stage accepts | The signal is recorded and the stage waits; no offer is written and the parent keeps the status | None | AC2, AC3 |
| X9 | The rule package in force is not the one the offer was built on | The stage re-evaluates the offer against the package named on `rwb.decision.RulePackageInForce.v1` and records the version it used | None | AC1 |

X1 to X4 are the exception paths of RWB-E3-002 carried onto the split, X5 to X7 are the paths the settlement offer adds, and X8 and X9 belong to the parent-and-child workflow model of the target. The floor of X4 and the freshness limit of X5 are values in force, so neither is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published offer contract, the decision-record library and the gateway route with their fakes, on the tables of its own schema, and needs no live rwb-case, no live rwb-valuation and no live rwb-decision to start |
| Negotiable | The activity names, the decision code per offer event and the shape of the stage outcome are this story's choice; the rules, the messages, the screens and the two operations are fixed |
| Valuable | The officer builds and sends the offer from one screen inside days, and every offer and every draft change carries the rule version it was evaluated with |
| Estimable | One workflow branch, three activities, two operations, one repository and one record write |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic treatments and route facts through the contract fakes, plus the two component cases of the access answer and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Offer a settlement inside the range

  Scenario: AC1 Offer a settlement inside the range (legacy RWB-E3-002 AC1)
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the officer build and send a settlement offer within the calculated range
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-RES-07 (legacy RWB-E3-002 AC2)
    Given the rwb-case contract mock returns case status AFFORDABILITY_IN_ACE
    Given a case in state AFFORDABILITY_IN_ACE
    When affordability passed
    Then return the calculated plan to the officer and build the offer
    Then the case moves to WITH_FCR_OFFICER

  Scenario: AC3 Rule R-RES-04 (legacy RWB-E3-002 AC3)
    Given the rwb-case contract mock returns case status IN_FCR_QUEUE
    Given a case in state IN_FCR_QUEUE
    When case picked up
    Then assign the case to a restructuring officer and start the offer clock
    Then the case moves to WITH_FCR_OFFICER

  Scenario: AC4 Not recorded (legacy RWB-E3-002 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Target reading.** Every line and every value above is the legacy line and the legacy value, unchanged, including the repetition of `Then` and the legacy wording of `the action is taken` and `the decision log cannot be written`; what changes is where it runs, who produces the fact and how it is reached. The screen of AC1 and the offer of AC1 and AC2 are SCR-15 Settlement offer, reached through the gateway-bff composite route of DP-19 and published by RWB-PLT-N001-CON on base `/api/recovery/treatment/v1` (DP-13); the officer works on the settlement branch of `TreatmentWorkflow` on task queue `rwb-treatment` in namespace `rwb-recovery`, the stage child of `CaseWorkflow` of rwb-case, with the three activities `buildSettlementOffer`, `checkFloor` and `recordAndApply` (Architecture v5 slide 18, "TMP TreatmentWorkflow · settlement and DIL sagas"; Temporal and Drools Design slide 13, "a parent per case, a child per stage", and slide 18, "Runs in rwb-treatment / TreatmentWorkflow"). "The calculated range" and "the floor" are not columns of `rwb_treatment`: they arrive as facts on the route decision signal that the parent forwards, calculated by S1 rwb-valuation under FEAT-VAL-06, and the offer body carries them for the length of one request and one decision record (GAP-1870; ASM-3066). The operation the officer uses is `POST /treatments/{treatmentId}/offer` under right U with an `Idempotency-Key`, the operation name of Architecture v5 slide 18, because the source precedence of §R3 puts the catalogue slides above the Technical Specifications; API Specification v4 and TSD S2 T-A.1 API-S2-004 name `POST /treatments/{treatmentId}/submit` for the same purpose and that form is not published (GAP-1871; ASM-3067). "The decision log" of AC1 and AC4 is the local decision record of `decision_record` in `rwb_treatment`, written through RWB-PLT-E1027-CON with `@Transactional(propagation = MANDATORY)` in the same transaction as the `treatment` row (DP-03); `decision_log_entry` is P7's central ledger and is never written or read here (DP-01). "The rule version" is the version label of the SETTLEMENT package in force on `rwb.decision.RulePackageInForce.v1` (EV-30), and the package and its runtime are the service template's, not a build dependency of this story (ASM-3063). "The case moves to WITH_FCR_OFFICER" in AC2 and AC3 is the parent's move: the stage reports the outcome of R-RES-07 and R-RES-04 and the parent `CaseWorkflow` changes the status, because rwb-case owns the case and its CMMN state and this service writes no case table (ASM-3062). The case status the mock returns in AC2 and AC3 is the status the parent forwards on the signal; it is a test double of that signal and adds no contract dependency. "The action is taken" in AC4 is the offer submission or the draft change, and the access answer of AC1, of the Access case and of every other call is the guard library's on the capability area "Treatment and offer" with right U (ASM-3064).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A settlement offer is negotiated inside the range the payoff calculation produced; an amount inside the range goes to the customer and an amount below the floor goes to the approver with the gap to the floor | REQ-S2-004; R-SET-04, R-SET-05 |
| BR2 | An offer to a customer carries a validity period, and expiry returns the case to the status it came from | REQ-S2-002; R-RES-09, R-RES-18; Temporal and Drools Design slide 18, "Offer 14 days" |
| BR3 | A case picked up by an officer is assigned to that officer and the offer clock starts; the case then sits with the officer | R-RES-04; R-RES-07 |
| BR4 | A counter-offer outside the current range returns the case to the officer with the counter-offer and the gap | R-RES-15 |
| BR5 | A payoff older than the freshness limit is not used for an offer: the warning is shown and a fresh figure is requested | R-SET-03; MSG-S2-002 |
| BR6 | The decision is recorded with the rule version before or with the change; if it cannot be recorded, nothing changes | REQ-DRI-005; DP-03; MSG-P7-003 |
| BR7 | No value a business person may change is written in code; it is read from reference data with its version | BR-S2-002 |
| BR8 | The range, the floor and the below-floor answer are facts of the request and of the decision record, never columns of `rwb_treatment` and never a copy of S1's calculation | GAP-1870; ASM-3066; DP-01 |

**Where each rule lives in the target.** BR1 and BR4 are the `checkFloor` activity against the SETTLEMENT package, with the range bounds and the floor taken from the request context; the approval of a below-floor offer is RWB-S2-E3003-APP's. BR2 is `valid_until` on the draft and the validity message of the screen, and the expiry transition of the case belongs to the parent. BR3 and BR4 are the two rule outcomes of the legacy criteria, reported to the parent `CaseWorkflow`, which owns the status change (ASM-3062). BR5 is the freshness test of the activity; the freshness limit is a reference value. BR6 is the `MANDATORY` transaction of the library, so the `treatment` row and the `decision_record` row commit together or not at all (DP-03). BR7 is the reason the range, the floor and the clocks are not constants of this build. BR8 is the reason no range, floor or validity column is added to `rwb_treatment`: storing them would copy another service's facts into this schema (DP-01).

### 9. State transitions

The case status is rwb-case's and is not changed by this story: the settlement stage reports an outcome and the parent `CaseWorkflow` moves the case (ASM-3062). What this story does own is the state of the `treatment` row and the state of the stage execution.

| From | Event | Condition | To |
|---|---|---|---|
| no stage child for the case | case signal forwarded by the parent `CaseWorkflow` | The route is R2 and the case status is one the settlement stage accepts | `TreatmentWorkflow` settlement branch running |
| running | case status AFFORDABILITY_IN_ACE with AFFORDABILITY_PASSED | R-RES-07 condition holds | Stage reports WITH_FCR_OFFICER; the parent moves the case |
| running | case status IN_FCR_QUEUE with CASE_PICKED_UP | R-RES-04 condition holds | Stage reports WITH_FCR_OFFICER; the parent moves the case |
| running | case status the settlement stage does not accept | X8 | Stage waits on the next signal; no offer is written |

| `treatment.state` | Event | Condition | To |
|---|---|---|---|
| Draft | draft terms changed | `PATCH /treatments/{treatmentId}`, right U | Draft |
| Draft | offer submitted | `belowFloor` false and the validity date present | Approved |
| Draft | offer submitted | `belowFloor` true | Below floor |
| Below floor | approval decided | The approval path of RWB-S2-E3003-APP | Approved or Draft |
| Approved | offer sent to the customer | The offer channel of the sibling story | Sent |
| Sent | customer accepts | The signature path of the sibling story | Accepted |

The four `treatment.state` values are the states of SCR-15 in the legacy story; `submitted`, `booked` and `broken` are SCR-14 states and belong to the treatment stories that own them. The stage execution itself moves from running to waiting on each signal and ends when the parent closes the stage, and the rule package version the offer was evaluated with is on the decision record and never on the treatment row.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery squad (RW-TRIBE) | Writes the settlement branch of the workflow, the three activities, the two operations and the repository |
| RW-RESTRUCT, restructuring officer (FCR) | Builds, edits and submits the offer; holds right CRUA, so the right C, R, U and A of the area |
| RW-CASEOWN, case owner | Builds, edits and submits the offer; holds CRU |
| RW-SPECIAL, hardship and vulnerability specialist | Builds, edits and submits the offer; holds CRU |
| RW-GUARANT, guarantee officer | Builds, edits and submits the offer; holds CRU |
| RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Read the treatment and the offer; right R only |
| RW-PRODHEAD, RW-CREDCOMM | Read, and approve through the approval path of the sibling story; right RA |
| SY-CASEWF, SY-RULES, SY-AGENT | Read as service identities, subject to the same checks |
| The approval of a below-floor offer | Not this story: RWB-S2-E3003-APP holds the matrix and the levels of TSD S2 T6.1 |
| The case status | Not this story: rwb-case owns it and the parent `CaseWorkflow` moves it |

The rights above are those of TSD S2 T6.1, and the check itself is the platform guard library's: this story declares the capability area "Treatment and offer" and the right U and calls the guard, and it owns no check of its own. No credential and no personal name appears in the request, the payloads or the logs, which carry case IDs, treatment IDs, amounts, dates, codes and rule versions only.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-002 | treatment | case_id | Read |
| DF-TRT-003 | treatment | decision_log_id | Write: the entry id returned by `DecisionRecordWriter.record` |
| DF-TRT-004 | treatment | treatment_type | Read: SETTLEMENT |
| DF-TRT-005 | treatment | proposed_by | Write |
| DF-TRT-006 | treatment | proposed_at | Write |
| DF-TRT-007 | treatment | offer_amount | Write |
| DF-TRT-008 | treatment | haircut_amount | Write |
| DF-TRT-009 | treatment | installments | Read |
| DF-TRT-010 | treatment | valid_until | Write |
| DF-TRT-011 | treatment | approval_level | Read: set by the approval path of RWB-S2-E3003-APP |
| DF-TRT-013 | treatment | outcome | Read |
| DF-TRT-014 | treatment | outcome_at | Read |
| T3.0 `state`, `version`, `updated_at`, `updated_by` | treatment | standard record columns | Write |
| DF-DEC-001 to DF-DEC-018 | decision_record | the record fields of the library | Write through RWB-PLT-E1027-CON |
| Not a column: `rangeLow`, `rangeHigh`, `floor`, `belowFloor`, `deviationFlag` | route decision signal | the request context facts | Read only, for the length of the request and of the decision record |

`treatment` is the only business table this story writes, in schema `rwb_treatment` and through this service's own login (DP-01). The `decision_record` row is a library object of RWB-PLT-E1027-CON created in the same schema and written in the caller's transaction; `decision_log_entry` is P7's and is neither written nor read. The range, the floor and the below-floor answer are not columns: no source document gives them a place in `rwb_treatment`, and storing them would copy the S1 calculation into this service (GAP-1870; ASM-3066). The contracts, the settlement and deed-in-lieu agreements and the plan timers that Architecture v5 slide 41 names in `rwb_treatment` have no field list in the TSD and belong to the sibling stories, not to this one.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). This story supplies the behaviour behind two operations whose shapes are declared by RWB-S2-E3002-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/treatments/{treatmentId}/offer` | `SettlementOffer` in, the offer and its `belowFloor` flag out | Treatment and offer, right U | `Idempotency-Key` header required |
| PATCH | `/treatments/{treatmentId}` | `TreatmentUpdate` in, the treatment out | Treatment and offer, right U | Not applicable |

The errors are 401, 403 with MSG-P4-002, 404, 409 on a state conflict, 422 with MSG-GEN-001 for a missing or invalid field, and 503 when the rule package or the library does not answer. The operation is `/offer` and not `/submit`: Architecture v5 slide 18 names `POST /treatments/{id}/offer` as the rwb-treatment IN operation, and the source precedence of §R3 puts the catalogue slides above the Technical Specifications, so API Specification v4 and TSD S2 T-A.1 API-S2-004 name a path that is not published (GAP-1870, GAP-1871; ASM-3066, ASM-3067). The field list of `SettlementOffer` and `TreatmentUpdate` is the working read of the contract story and is not restated here.

#### 12.2 REST operations consumed

None. The range, the floor and the payoff arrive on the route decision signal that the parent `CaseWorkflow` forwards, and the case status arrives the same way, so this story calls no service (ASM-3062). The two operations the screen uses to reach the treatment read belong to RWB-S2-E3001-CON, and the decision record is called in process inside the caller's transaction (DP-03). This is why the Work Package records no C dependency for this story.

#### 12.3 Events published

None. The topic of the service is `rwb.treatment.events.v1` with event names `rwb.treatment.<Event>.v1` (DP-14), and its two events `TreatmentApproved` and `TreatmentClosed` belong to the stories that own the approval and the closure. This story writes no outbox row and announces no event of its own; the offer is reported to the parent `CaseWorkflow` as a stage outcome.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` (EV-30) | `rwb.decision.events.v1` | P7 rwb-decision | The SETTLEMENT package version in force, so the offer is evaluated and recorded with the version it used |
| `rwb.deviation.DeviationRaised.v1` (EV-06) | `rwb.deviation.events.v1` | S8 rwb-deviation | A deviation raised on the case, so a deviated offer is routed under R-RES-10 or R-SET-05 by the sibling story and the stage does not send it |

Both events reach this service as an event and are consumed through the inbox of the outbox library, deduplicated by cloud event id, so a redelivery changes nothing. The case status change is not an event of this table: it arrives as the signal the parent forwards (ASM-3062), and `rwb.payment.TreatmentBooked.v1` (EV-11) and `rwb.payment.PaymentMissed.v1` (EV-12) are available to the service for the booking and plan stories.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow` (settlement branch) | Workflow, one execution per case per stage, the child of `CaseWorkflow` | `rwb-treatment` in namespace `rwb-recovery` | Input: the case, the route R2 and the route facts including `rangeLow`, `rangeHigh`, `floor` and the payoff with its date; signals: the case status forwarded by the parent, the rule package in force and the deviation |
| `buildSettlementOffer` | Activity | `rwb-treatment` | The draft terms or the offer in, the validated `treatment` columns out |
| `checkFloor` | Activity | `rwb-treatment` | The amount, the range and the floor in; `belowFloor`, the gap to the floor and the payoff freshness out |
| `recordAndApply` | Activity | `rwb-treatment` | The `DecisionRecord` and the `treatment` row written in one transaction through RWB-PLT-E1027-CON, and the stage outcome for the parent |

The stage is the settlement branch of the one `TreatmentWorkflow` that Architecture v5 slide 18 names, and the parent-and-child model with the four steps of receive, ask, record and apply, wait is the one of the Temporal and Drools Design slides 13 and 18. The activity names are a target design choice of this story and are fixed by no source document. A workflow class never calls the decision-record library directly: the call is made inside `recordAndApply`, so a replay reuses the recorded decision.

#### 12.6 Schedules

None. The stage runs from the signal the parent forwards and from the officer's calls, and owns no Temporal Schedule and no legacy Quartz job. The offer clock and the plan timers are durable timers inside the workflow, and the schedules of the service belong to the plan stories.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 rwb-treatment | Written by this story for the settlement columns of DF-TRT-001 to DF-TRT-014 and the standard record columns; created by the per-service Flyway sequence and never re-created here |
| `decision_record` | `rwb_treatment` | PLT, library object | Not written directly: the row is written by RWB-PLT-E1027-CON in the caller's transaction (DP-03) |

No table of another service is read and no foreign key crosses a schema (DP-01). `decision_log_entry` in `rwb_decision` is P7's and is named here only. No range, floor, below-floor or validity-state column is added to `treatment`: the range and the floor have no place in this schema (GAP-1870; ASM-3066).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-S2-E3002-CON offer fake | The two operations, the request context facts and the error set | An offer inside the range with `belowFloor` false; an offer below the floor with `belowFloor` true and the gap; a repeated `Idempotency-Key` returning the first answer; 422 for a missing validity date; 403 for a role without right U |
| RWB-PLT-E1027-CON writer fake | The decision record | An accepted record with chain sequence and entry hash; a refusal with MSG-P7-009 and the field; a failed write raising MSG-P7-003; a call with no transaction refused before any write |
| RWB-PLT-N001-CON route fake | The gateway-bff composite route | A composite answer for SCR-15 that joins the treatment read and the route facts; a refused route for a role without the right |
| rwb-case case-status mock | The signal the parent forwards, used by AC2 and AC3 | A case at AFFORDABILITY_IN_ACE and a case at IN_FCR_QUEUE; a case status the settlement stage does not accept. Test-only, adds no contract dependency (ASM-3062) |
| Route fact fixture | The facts of the S1 calculation on the signal | One case with payoff 1,200,000.00 baht, `rangeLow` 780,000.00, `rangeHigh` 900,000.00 and a floor of 720,000.00; the same case with a payoff date older than the freshness limit |

The offer, writer and route fakes are the published contracts of those stories; the case-status mock and the route fact fixture stand in for the signal of the parent and for the S1 calculation, which have no published contract of their own here (GAP-1870; ASM-3066).

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 operations on `/api/recovery/treatment/v1` | None | OpenAPI 3.1; the two shapes are declared by RWB-S2-E3002-CON |
| Kafka | None | 2 events (`rwb.decision.RulePackageInForce.v1`, `rwb.deviation.DeviationRaised.v1`) | Own topic unused by this story; inbox dedupe by cloud event id |
| Temporal | None | `TreatmentWorkflow` settlement branch and 3 activities on `rwb-treatment` | Namespace `rwb-recovery`; stage child of `CaseWorkflow`; no Schedule |
| File | None | None | No file is read or written |
| Nexus and ACE Common | None | None | The restructure calculator of the stopgap route is not called by the settlement offer; the range arrives on the signal |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, modules `settlement` and `web`, with the published types in `...treatment.api`. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the offer: the record and the `treatment` row commit together, and a failed record leaves nothing behind. DP-13 moves the base of the two operations and nothing else. DP-19 is how SCR-14 and SCR-15 reach this service, one hop through the gateway, so no screen reads a table and no screen calls another service.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `TreatmentWorkflow` settlement branch | Workflow | One execution per case per stage; the route facts, the case signal, the package in force and the stage outcome |
| `buildSettlementOffer` | Activity | Validation of the draft terms and of the offer, and the `treatment` columns of the settlement |
| `checkFloor` | Activity | The range and floor evaluation of the SETTLEMENT package, the `belowFloor` answer, the gap to the floor and the payoff freshness |
| `recordAndApply` | Activity | The `DecisionRecord` and the `treatment` row in one transaction through RWB-PLT-E1027-CON |
| `SettlementOfferController` | Controller | The two operations, the right U check through the guard, the `Idempotency-Key` and the error mapping |
| `TreatmentRepository` | Repository | The settlement columns of `treatment` in schema `rwb_treatment`, with the optimistic lock of the `version` column |
| `StageOutcomeReporter` | Signal reporter | The outcome the parent `CaseWorkflow` uses to move the case status; it reports, it never changes a case row |

**Database.** `treatment` holds the settlement columns of DF-TRT-001 to DF-TRT-014 and the standard record columns of T3.0, with the optimistic lock on `version`. The range, the floor and the below-floor answer are not columns and are not created: they belong to the request context and to the decision record (GAP-1870; ASM-3066). `decision_record` is the library object applied by the per-service Flyway sequence, and this story writes it only through the library.

**Configuration and reference data.** The capability area "Treatment and offer" and right U are access rows of rwb-access, read through its guard. The offer validity, the officer review clock and the payoff freshness limit are values in force in reference data, read with their version and never written in code (BR-S2-002; the 14 days of the offer clock come from the Temporal and Drools Design slide 18). The SETTLEMENT package and its version come from `rwb.decision.RulePackageInForce.v1` and are never configured here.

**Build steps**

1. The settlement branch of `TreatmentWorkflow` and its input record, registered on `rwb-treatment` as the stage child of `CaseWorkflow`, with the case signal and the route facts (AC2, AC3).
2. `buildSettlementOffer` against the offer fake, with `TreatmentUpdate` and the validation of the validity date (AC1).
3. `checkFloor` against the SETTLEMENT package, with the inside-range answer, the below-floor answer, the gap to the floor and the payoff freshness (AC1).
4. `recordAndApply` with the `DecisionRecord`, the `MANDATORY` transaction and the `treatment` row, plus the failed-write path (AC4).
5. The two operations with the guard check, the `Idempotency-Key` and the error mapping of section 12.1 (AC1).
6. `StageOutcomeReporter` and the parent signal, with the two rule outcomes of AC2 and AC3.
7. Tests for AC1 to AC4 against the fakes and the route fact fixture, plus the two component cases of section 16.

**Feature flag.** `rwb.treatment.settlement-offer`.

**Done when.** The tests in section 16 pass, the stage runs from a synthetic case signal in SIT, an offer inside the range is stored with `belowFloor` false and an offer below the floor with the gap to the floor, a repeated `Idempotency-Key` stores one row, the decision record and the `treatment` row commit or roll back together, the parent moves the case on the two rule outcomes, and SCR-15 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S2-001 | The offer amount is below the floor in force | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-002 | The payoff carried on the signal is older than the freshness limit | The payoff is from {date}. A new figure has been requested. |
| MSG-S2-003 | The offer carries its validity date | The offer to the customer ends on {date}. |
| MSG-GEN-001 | A required field is absent or invalid, the validity date among them | Enter {field}. |
| MSG-P4-002 | The role does not hold right U on the capability area | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | The decision record is refused for a field | The decision record was refused: {field} is missing or not valid. |

The seven texts are the legacy texts carried unchanged, and no message identifier is added or renamed. MSG-S2-001 carries the floor in force and MSG-S2-002 and MSG-S2-003 carry a date, so no message holds a constant. MSG-P4-002 is the access answer of the guard library, and MSG-P7-003 and MSG-P7-009 are raised by RWB-PLT-E1027-CON and shown by this story. Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-14 Treatment record (Draft; submitted; approved; booked; broken) and SCR-15 Settlement offer (Draft; below floor; approved; sent; accepted) are the two legacy screens of this story and keep their state lists unchanged. SCR-15 is where the officer reads the calculated range, the floor, the offer amount, the haircut, the validity date and the gap to the floor, and where the below-floor state routes the offer to the approval path of RWB-S2-E3003-APP. Both screens reach the service through the gateway-bff composite route, one hop each, and the route joins the treatment read with the route facts (DP-19); the screen field list and the composite route specification belong to the platform edge story and the screen owners, and this story fixes the service side of the answer only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-002-01 | AC1 | End to end | Offer a settlement inside the range |
| TC-E3-002-02 | AC2 | End to end | Rule R-RES-07 |
| TC-E3-002-03 | AC3 | End to end | Rule R-RES-04 |
| TC-E3-002-04 | AC4 | End to end | Not recorded |
| TC-E3-002-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E3-002-06 | Principle 5 | Component | A forced decision log write failure stops the action with MSG-P7-003 |

The six legacy test case IDs, their Covers and their Data are kept in order and character for character; the legacy level "System" maps to "End to end" and "Access" and "Principle 5" map to "Component", as in the other stories of this run. The offer fake, the decision-record writer fake and the route fact fixture of section 12.8 stand behind every case, and the case-status mock supplies the two statuses of AC2 and AC3. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 2 integration harness and are not listed here.

### 17. Guardrails

- No value that a business person may change is written in code: the range bounds, the floor, the offer validity, the officer review clock and the approval levels are values in force in reference data, read with their version (BR-S2-002).
- No personal data in logs, events, workflow inputs, prompts or the fixture: the rows carry case IDs, treatment IDs, amounts, dates, codes and rule versions only, and the test data is synthetic.
- No read of another service's table: the case status and the route facts arrive as a signal, the treatment facts are this service's own, and `decision_log_entry` is P7's and is never touched (DP-01).
- No range, floor or below-floor column and no copy of the S1 calculation in `rwb_treatment`; a schema change that adds one fails the guardrail test (DP-01; ASM-3066).
- ACE data only through the owner's contract or the `v_ace_*` views, and this service reads neither: no ACE view is opened by the settlement offer.
- No event of this story and no outbox row: the offer is reported to the parent, so a replay of the stage produces no second message.
- The decision record and the `treatment` row commit in one transaction through the `MANDATORY` rule of the library; an action that commits without its record is a build failure, not a defect (DP-03).
- An applied migration is never edited: any correction to the `treatment` table is a new version on the service sequence.
- No screen calls a service directly and no screen reads a table: SCR-14 and SCR-15 go through the gateway-bff composite route (DP-19).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-004 | Settlement terms are negotiated inside a rule-set range, and anything outside the range needs approval | Program 5.9 | FEAT-TRT-02 | 07 Route, settle and claim | R-RES-04, R-RES-07, R-RES-15, R-SET-05 | TC-E3-002-01, TC-E3-002-02, TC-E3-002-03 |
| REQ-S2-002 | An offer to a customer carries a validity period, and expiry returns the case to the status it came from | Program 5.9 | FEAT-TRT-02 | 07 Route, settle and claim | R-RES-09, R-RES-18; BR2 | TC-E3-002-01, TC-E3-002-05, TC-E3-002-06 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3002-CON | Contract | H: declares the offer surface, the `SettlementOffer` and `TreatmentUpdate` elements, the request context facts, the `belowFloor` flag, the error set and the fakes |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record writer called in the caller's transaction with the `MANDATORY` rule |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route that SCR-14 and SCR-15 use |
| RWB-S2-E3001-APP, RWB-S2-E3001-CON | App development, Contract | Sibling: creates the treatment record and publishes the treatment read this story patches and answers from; no build dependency is recorded |
| RWB-S2-E3003-APP, RWB-S2-E3003-CON | App development, Contract | Sibling: the approval of a below-floor offer and the approval matrix the below-floor state routes into |
| RWB-S2-E3004-APP | App development | Sibling: the TDR plan body, which this story does not declare |
| RWB-S2-E3005-APP | App development | Sibling: the affordability pre-assessment through ACE, which produces the plan AC2 returns to the officer |
| S1 rwb-valuation | Service, wave 3 | The payoff and the range calculation of FEAT-VAL-06, whose facts arrive on the route decision signal |
| rwb-case (P3) | Service, wave 1 | Owns the case, its status and the parent `CaseWorkflow`; the stage reports and never moves the status |
| rwb-deviation (S8) | Service, wave 2 | Owns `rwb.deviation.DeviationRaised.v1`, consumed here so a deviated offer is routed by the sibling story |
| Wave 2 integration harness | Integration | I: the cross-service proof of the same legacy key against the live owners, with the `-ITG` copies of the six test cases |

### 19. Out of scope

- The published shape of the two operations, the elements, the request context facts, the error set and the fakes: RWB-S2-E3002-CON.
- The approval of an offer below the floor, its matrix, its levels and its decision: RWB-S2-E3003-APP and RWB-S2-E3003-CON.
- The creation of the treatment record, the treatment read and the treatment resource body: RWB-S2-E3001-APP and RWB-S2-E3001-CON.
- The TDR plan body, its installments and its plan body declaration: RWB-S2-E3004-APP and RWB-S2-E3004-CON.
- The affordability pre-assessment through ACE and its answer: RWB-S2-E3005-APP.
- The case, its CMMN status, the parent `CaseWorkflow`, the case signal and the case router: rwb-case (P3), so no case table is read or written here (ASM-3062).
- The payoff, the range bounds and the floor as calculations: S1 rwb-valuation and FEAT-VAL-06; this story consumes them as facts on the signal and copies none of them (GAP-1870; ASM-3066).
- The decision-record library, its chain, its envelope and the central ledger of P7: RWB-PLT-E1027-CON, RWB-PLT-E1027-APP and RWB-P7-E1027-APP.
- The SETTLEMENT rule package, its authoring, its approval and its promotion: P7 rwb-decision, with the embedded runtime as a service-template capability (ASM-3063).
- The gateway-bff composite route and the screen field list of SCR-14 and SCR-15: RWB-PLT-N001-CON and the screen owners.
- The contracts, the settlement and deed-in-lieu agreements and the plan timers that Architecture v5 slide 41 places in `rwb_treatment`: their field lists have no source and their stories are the plan and booking ones, not this one.
- The offer expiry transition of the case, the counter-offer handling of the case and the sending of the offer letter: the parent workflow, the sibling stories and rwb-comms.
- The deployment, the flag switch and the runbook: the platform DevOps stories of wave 2; the real cross-service proof: the wave 2 integration harness.
