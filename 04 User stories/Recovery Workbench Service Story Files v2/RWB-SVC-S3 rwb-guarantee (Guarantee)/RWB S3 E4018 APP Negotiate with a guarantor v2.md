# RWB-S3-E4018-APP Negotiate with a guarantor

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: application slice split from RWB-E4-018 for rwb-guarantee. The four legacy acceptance criteria are kept word for word with their origin tag and now run on `GuaranteeClaimWorkflow` on task queue `rwb-guarantee` in namespace `rwb-recovery`, reached through the gateway-bff composite route (DP-19) and the base `/api/recovery/guarantee/v1` (DP-13); the one `recovery` schema becomes `rwb_guarantee` and no other service's table is read (DP-01); the legacy `DecisionLogWriter` write to the shared `decision_log_entry` becomes the local decision record of RWB-PLT-E1027-CON written in the same transaction as the change (DP-03); the legacy `AceSourceQuery` read of `v_ace_customer` is dropped, because the negotiation and the subrogation record need the claim and the party reference and no personal field (DP-05); the state the legacy story moves on the case becomes the GUARANTEE state of TSD S3 T4 reported to the parent `CaseWorkflow` as a stage outcome; the negotiation range, the outcome vocabulary, the TCG-share column and the payment event are named by no S3 source and are carried as the working read of an assumption (GAP-2728, GAP-2729; ASM-4529 to ASM-4535). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S3-E4018-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 12 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S3-E4018-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-guarantee |
| Service epic | RWB-SVC-S3 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S3-G |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S3-E4018-APP-16) |
| Depends on (build) | RWB-S3-E4018-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Contract version | Path /v1 only (base `/api/recovery/guarantee/v1`); contract version Not specified in the source documents (DOR-RWB-S3-E4018-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S3 rwb-guarantee v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **case owner**, I want **to negotiate with a guarantor inside the approved range on the guarantee claim of the case and to have the outcome recorded against the claim and the TCG share kept for every later recovery**, so that **no guarantee claim misses its deadline and no subrogation position is lost after the TCG pays**.

This is the application slice of legacy RWB-E4-018. It owns:

- all four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages, screen and data rows they depend on;
- `GuaranteeClaimWorkflow` on task queue `rwb-guarantee` in namespace `rwb-recovery`, as the guarantee stage child of `CaseWorkflow` owned by rwb-case, with the activities `evaluateNegotiation`, `applyOutcome` and `recordAndApply` (context pack: one workflow; Architecture v5 slide 18 "Guarantee claim · GUA 32"; Temporal and Drools Design slide 13);
- the behaviour behind `PATCH /guarantee-claims/{claimId}` on base `/api/recovery/guarantee/v1`, under capability area "Treatment and offer" with right U (DP-13; TSD S3 T-A.1 API-S3-002);
- the negotiation outcome against the claim: R-GUA-23 and R-GUA-24 to `SUBROGATION_POSITION` and R-GUA-29 to `RESIDUAL_TO_ROUTE`, evaluated in the GUA package version in force;
- the local decision record of the negotiation, written through RWB-PLT-E1027-CON in the same transaction as the `guarantee_claim` row (DP-03);
- the writer of `guarantee_claim` in schema `rwb_guarantee` and the stage outcome the parent uses to move the case.

It does not own: the published shape of the two operations, the elements, the error set and the fakes, which are RWB-S3-E4018-CON; the preparation and filing of the claim and the balance claim, which are the claim-preparation slices of FEAT-GUA-01, FEAT-GUA-02 and FEAT-GUA-03; the demand to the guarantor and its expiry, which are the FEAT-GUA-05 slice; the closing of the guarantee and the case, which are FEAT-GUA-07 (legacy RWB-E4-019); the case status, which is rwb-case's; the decision-record library, which is RWB-PLT-E1027-APP; the gateway-bff composite route, which is RWB-PLT-N001-CON; and the deployment, which is the wave 3 integration harness and the platform DevOps stories.

### 2. Business rationale

Guarantee and TCG claims are late because deadlines are not tracked (FSD S3 A1.3), and the position a guarantor may reclaim after payment is lost because nothing records it. The functional specification keeps the objective and its metric — claims filed inside the deadline at 100 percent, measured on the decision log and the Workbench records, reviewed monthly — and REQ-S3-005 states that a guarantor who answers a demand enters the same treatment paths as a borrower. The legacy guardrail BR-S3-006 stands unchanged: no value a business person may change is written in code; it is read from reference data with its version.

What D-RCV-60 changes is where the negotiation is decided, what it is written to and who owns the state:

- the guarantee stage is `GuaranteeClaimWorkflow` on task queue `rwb-guarantee`, the child of `CaseWorkflow` of rwb-case, so the case keeps one parent workflow from entry to closure and the stage runs where its rules and data live (Temporal and Drools Design slide 13);
- the outcome is written to `guarantee_claim` in `rwb_guarantee` (DP-01), reached through the gateway-bff composite route (DP-19) and the base `/api/recovery/guarantee/v1` (DP-13);
- the decision is recorded through the local decision-record library in the same transaction as the change (DP-03), because `decision_log_entry` is P7's ledger and no service writes it;
- the state the legacy story moves — `SUBROGATION_POSITION` — is the GUARANTEE state of TSD S3 T4 and belongs to this claim, while the case status stays with rwb-case: the stage reports an outcome and the parent moves the case (ASM-4530);
- the legacy read of `v_ace_customer` is not carried: the negotiation and the share need the claim, the party reference and the range, not the customer's personal fields, and the ACE views are read by rwb-source-data (DP-05; ASM-4532).

No business value moves. The approved range, the notice expiry and the rule package stay values in force in the owner's data, read with their version and never written in code (BR-S3-006).

### 3. Preconditions

- RWB-S3-E4018-CON is published: the two operation entries on `/api/recovery/guarantee/v1`, the `GuaranteeClaimRequest`, `GuaranteeClaim` and `GuaranteeClaimUpdate` elements, the negotiation facts declared context-only, the error set, the idempotency rule and the fakes. The negotiation body has no source specification and is published as the working read (GAP-2730; ASM-4529).
- RWB-PLT-E1027-CON is published with its writer fake: `DecisionRecordWriter.record(DecisionRecord)` runs with `@Transactional(propagation = MANDATORY)`, refuses with MSG-P7-009 and fails with MSG-P7-003, so the claim row and its record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-17 Guarantee claim is reached through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19). The service publishes no read operation of its own, so the route composes the case read of rwb-case with the claim the stage holds (GAP-2730; ASM-4533).
- The signal the parent forwards carries the case, the claim reference, the GUARANTEE state, the guaranteed amount and the approved range as request context; the range, its unit and the identity of the list it comes from are named by no S3 source (GAP-2728; ASM-4529).
- The embedded Drools runtime and the GUA package (32 rules, TSD S3 T4) are the service template's capability, and the package version in force arrives on `rwb.decision.RulePackageInForce.v1`; this story names the package and adds no build dependency of its own (ASM-4534).
- The access guard, the outbox and inbox library and the workflow kit are service-template capabilities; this story declares capability area "Treatment and offer" and the rights C and U and adds no build dependency of its own.
- The per-service Flyway sequence of rwb-guarantee carries `guarantee_claim` with DF-TRT-015 to DF-TRT-022 and the library object `decision_record`; this story adds the TCG-share column and never edits an applied migration (GAP-2728; ASM-4535).
- No ACE view is opened by this story: `case_party`, `assignment` and `timer` are rwb-case's, and `v_ace_customer` is rwb-source-data's (DP-05; ASM-4532).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S3-E4018-CON when its tests pass.

### 4. Flow

1. rwb-case's `CaseWorkflow` receives the case change through the case router and signals the running guarantee child on queue `rwb-guarantee`; the stage never calls rwb-case (Temporal and Drools Design slide 13, the four steps receive, ask, record and apply, wait).
2. The stage holds the facts it was started with: the case, the claim reference, the GUARANTEE state — `CLAIM_PAID` or `CLAIM_PART_PAID` — the guaranteed amount, the approved range as context and the package in force. Nothing about the range is copied into `rwb_guarantee` (ASM-4529).
3. Case owner or guarantee officer opens SCR-17 Guarantee claim through the gateway-bff composite route and reads the claim, the deadline and the checklist (DP-19).
4. The officer records the negotiation outcome with `PATCH /guarantee-claims/{claimId}` carrying `GuaranteeClaimUpdate` under right U; `evaluateNegotiation` validates the fields and applies the range check.
5. An outcome inside the approved range is accepted; an outcome outside the range is refused with 422 naming the field, because the rule that would authorise it is named by no S3 source (GAP-2728; ASM-4529).
6. `evaluateNegotiation` evaluates the GUA package in the version in force: on `SUBROGATION_DUE` with the claim at `CLAIM_PAID` it selects R-GUA-23, at `CLAIM_PART_PAID` it selects R-GUA-24, and on `GUARANTOR_REFUSED` it selects R-GUA-29.
7. A guarantor who refuses or does not answer by the notice expiry records the refusal and the stage reports `RESIDUAL_TO_ROUTE` under R-GUA-29, so the parent returns the case to the route decision.
8. `applyOutcome` writes the claim result on `guarantee_claim` — `status` from LOV-CLAIM-STATUS, `state` from the GUARANTEE set, `paid_amount` and the TCG share — and keeps the range used on the decision record only.
9. `recordAndApply` assembles the `DecisionRecord` — the decision code, the case, the claim, the rule ID with the package version, the recommendation, the final call and the actor — and writes it through `DecisionRecordWriter.record` in the caller's transaction, then the `guarantee_claim` row in the same transaction (DP-03).
10. The stage publishes nothing: the outcome is reported to the parent `CaseWorkflow`, which moves the case and, for the subrogation, keeps the TCG share against the case for all future recoveries, because the case is rwb-case's record (ASM-4530).
11. A payment that arrives for the claim reaches the stage as the next signal the parent forwards; the event that carries it and any subscription of this service to it are named by no source (GAP-2728; ASM-4531).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The role does not hold right U on "Treatment and offer" | 403 before any read or write; the refusal is the guard library's and is logged by it | MSG-P4-002 | AC1, TC-E4-018-05 |
| X2 | The decision record cannot be written | `recordAndApply` throws before the `guarantee_claim` row is written and the transaction rolls back; nothing changes | MSG-P7-003 | AC4, TC-E4-018-06 |
| X3 | The decision record is refused for a missing or invalid field | Nothing is written and the field is named in the service log and the incident | MSG-P7-009 | AC4 |
| X4 | The negotiation outcome is outside the approved range | The request is refused with 422 and the field is named; no claim row changes and the range used is not recorded | MSG-GEN-001 | AC1 |
| X5 | A required field of the negotiation is absent | The request is refused with 422 and the field is named | MSG-GEN-001 | AC1 |
| X6 | The claim is not at a GUARANTEE state the stage accepts | The signal is recorded and the stage waits; no outcome is written and the parent keeps the case status | None | AC2, AC3 |
| X7 | The package in force is not the one the outcome was built on | The stage re-evaluates against the package named on `rwb.decision.RulePackageInForce.v1` and records the version it used | None | AC1 |
| X8 | The guarantor refuses, or the notice expires with no answer | The refusal is recorded and the stage reports `RESIDUAL_TO_ROUTE` under R-GUA-29 | None | AC5, TC-E4-018-09 |

X1 to X5 are the exception paths of RWB-E4-018 carried onto the split, X6 and X7 belong to the parent-and-child workflow model of the target, and X8 is the refusal rule the functional specification lists next to the two subrogation rules. The range of X4 and the notice expiry of X8 are values in force, so neither is a constant of this story.

Screen states of SCR-17 Guarantee claim: the empty state, the loading state and the error state are Not specified in the source documents (DOR-RWB-S3-E4018-APP-10); the no access state is X1, refused with MSG-P4-002 before any read or write.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published contract, the decision-record library and the gateway route with their fakes, on the tables of its own schema, and needs no live rwb-case, no live P7 and no live payment to start |
| Negotiable | The activity names, the decision code per outcome, the shape of the stage outcome and the share column are this story's choice; the rules, the messages, the screen and the two operations are fixed |
| Valuable | The officer records the negotiation and the TCG share in days, and every outcome carries the rule version it was evaluated with |
| Estimable | One workflow branch, three activities, one operation, one repository and one record write |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic claims and range facts through the contract fakes, plus the two component cases of the access answer and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Negotiate with a guarantor

  Scenario: AC1 Negotiate with a guarantor (legacy RWB-E4-018 AC1)
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the case owner negotiate within the range and record the outcome against the claim and the party reference of the case
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Rule R-GUA-23 (legacy RWB-E4-018 AC2)
    Given the rwb-case contract mock returns case status CLAIM_PAID
    Given a case in state CLAIM_PAID
    When subrogation due
    Then record the TCG share against the case for all future recoveries
    Then the claim moves to SUBROGATION_POSITION and the stage reports the outcome to the parent case

  Scenario: AC3 Rule R-GUA-24 (legacy RWB-E4-018 AC3)
    Given the rwb-case contract mock returns case status CLAIM_PART_PAID
    Given a case in state CLAIM_PART_PAID
    When subrogation due
    Then record the TCG share against the case for all future recoveries
    Then the claim moves to SUBROGATION_POSITION and the stage reports the outcome to the parent case

  Scenario: AC4 Not recorded (legacy RWB-E4-018 AC4)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 The guarantor refuses, or the notice expires with no answer (new, D-RCV-60)
    Given the guarantor refuses, or the notice expires with no answer
    When the stage takes the guarantor answer
    Then the refusal is recorded
    Then the stage reports RESIDUAL_TO_ROUTE under R-GUA-29

  Scenario: AC6 A status change the model does not allow is refused (new, D-RCV-60)
    Given the claim is at a GUARANTEE state the stage does not accept
    When the stage takes the signal
    Then the status change is refused
    Then no outcome is written

  Scenario: AC7 Each business rule of section 8 applies as written (new, D-RCV-60)
    Given the business rules BR1 to BR8 of section 8 are in place
    When the stage takes a negotiation outcome or a guarantor answer
    Then the rule of section 8 that matches the outcome applies
    Then a rule that does not match is not applied

  Scenario: AC8 An error answer of the provided operations is 401, 403 or 404 (new, D-RCV-60)
    Given a request the operation refuses with status 401, 403 or 404 under the contract
    When the operation is called
    Then the service answers with the status the contract gives

  Scenario: AC9 A write replayed with the same idempotency key is not applied twice (new, D-RCV-60)
    Given a write request carries an idempotency key the service has already processed
    When the operation is called again with the same idempotency key
    Then the service returns the result of the first call
    Then no second decision record is written and no second outcome is applied

  Scenario: AC10 A retried or timed-out activity writes no outcome twice (new, D-RCV-60)
    Given an activity of GuaranteeClaimWorkflow is retried or times out
    When the activity runs again or the timeout is reached
    Then the activity runs again without writing a second outcome
    Then no decision record is written twice
```

**Target reading.** Every line and every value above is the legacy line and the legacy value, unchanged, including the repetition of `Then` and the legacy wording of `the action is taken` and `the decision log cannot be written`, where the term is now `decision record` in AC1, AC4 and TC-E4-018-06; what changes is where it runs, who produces the fact and how it is reached. The screen of AC1 is SCR-17 Guarantee claim, reached through the gateway-bff composite route of DP-19 on base `/api/recovery/guarantee/v1` (DP-13); the officer works on `GuaranteeClaimWorkflow` on task queue `rwb-guarantee` in namespace `rwb-recovery`, the guarantee stage child of `CaseWorkflow` of rwb-case, with the three activities `evaluateNegotiation`, `applyOutcome` and `recordAndApply` (Architecture v5 slide 18, "Guarantee claim · GUA 32"; Temporal and Drools Design slide 13). "The range" arrives as a context fact on the stage signal and is never a column: no S3 source defines its bounds, its unit or the list it comes from (GAP-2728; ASM-4529). "The outcome against the customer" is recorded against the claim and the party reference of the case, because the statement of the functional specification reads "the party" for the same feature and the difference is recorded, not resolved, here (GAP-2729; ASM-4530). "The decision log" of AC1 and AC4 is the local decision record of `decision_record` in `rwb_guarantee`, written through RWB-PLT-E1027-CON with `@Transactional(propagation = MANDATORY)` in the same transaction as the `guarantee_claim` row, so a failed record leaves nothing behind (DP-03). `CLAIM_PAID`, `CLAIM_PART_PAID` and `SUBROGATION_POSITION` of AC2 and AC3 are the GUARANTEE states of TSD S3 T4, reached inside the stage; the case status is rwb-case's and the stage reports the outcome, so the two `Given` lines name the state the mock and the claim carry (ASM-4530). "The TCG share ... for all future recoveries" is kept on the claim row for the length of the claim and reported to the parent in the stage outcome so that the case carries it, because the case is rwb-case's record and this service writes no case row.

### 8. Business rules

Open decision DL10 applies to this story and remains open; each of its assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 is confirmed by the programme directive, and this story does not close the decision.

| ID | Rule | Source |
|---|---|---|
| BR1 | The guarantor negotiation is recorded against the claim inside the approved range; an outcome outside the range is refused and nothing is written | R-GUA-28 "inside the approved range"; FSD S3 A2.6; GAP-2728; ASM-4529 |
| BR2 | When the TCG holds a share of every later recovery and the claim is at `CLAIM_PAID`, the share is recorded against the case and the claim moves to `SUBROGATION_POSITION` | R-GUA-23; REQ-S3-005 |
| BR3 | When the TCG holds a share of every later recovery and the claim is at `CLAIM_PART_PAID`, the same share is recorded and the claim moves to `SUBROGATION_POSITION` | R-GUA-24; REQ-S3-005 |
| BR4 | When the guarantor refuses, or does not reply by the notice expiry, the refusal is recorded and the case returns to the route decision | R-GUA-29 |
| BR5 | The decision is recorded with the rule version in the same transaction as the change; if it cannot be recorded, nothing changes and the user sees MSG-P7-003 | DP-03; MSG-P7-003 |
| BR6 | A required field of the negotiation is refused with MSG-GEN-001 and the field name | VR-S3-006-1; MSG-GEN-001 |
| BR7 | No value a business person may change is written in code; it is read from reference data with its version through DP-06 and DP-07; the parameters are the approved range and the notice expiry, whose parameter keys are Not specified in the source documents (DOR-RWB-S3-E4018-APP-20) | BR-S3-006 |
| BR8 | The approved range and the notice expiry are facts of the request and of the decision record, never columns of `rwb_guarantee` | GAP-2728; ASM-4529; DP-01 |

**Where each rule lives in the target.** BR1 is the range check of `evaluateNegotiation`, with the bounds taken from the request context and no rule identifier available in any source. BR2 and BR3 are the two subrogation branches of the same activity, selected by the GUARANTEE state the stage holds. BR4 is the refusal branch of the activity and the `RESIDUAL_TO_ROUTE` outcome the stage reports. BR5 is the `MANDATORY` transaction of the library, so the claim row and the record row commit together or not at all. BR6 is the field validation of the two operations. BR7 is the reason the range, the expiry and the package are not constants of this build. BR8 is the reason no range or expiry column is added: storing them would copy another owner's facts into this schema.

### 9. State transitions

The case status is rwb-case's and is not changed by this story: the stage reports an outcome and the parent `CaseWorkflow` moves the case (ASM-4530). What this story owns is the `guarantee_claim` row and the execution of the stage.

| From | Event | Condition | To | Rule |
|---|---|---|---|---|
| `CLAIM_PAID` | SUBROGATION_DUE | The TCG holds a share of every later recovery | `SUBROGATION_POSITION` | R-GUA-23 |
| `CLAIM_PART_PAID` | SUBROGATION_DUE | The same share condition | `SUBROGATION_POSITION` | R-GUA-24 |
| `GUARANTOR_NOTICE` | GUARANTOR_REFUSED | The guarantor refuses or the notice expires with no answer | `RESIDUAL_TO_ROUTE` | R-GUA-29 |
| any accepted GUARANTEE state | the officer records an outcome outside the approved range | X4 | no change | None |

| `guarantee_claim.state` | Event | To |
|---|---|---|
| `CLAIM_PAID` or `CLAIM_PART_PAID` | The stage reports `SUBROGATION_POSITION` | `SUBROGATION_POSITION` |
| `GUARANTOR_NOTICE` | The stage reports the refusal | `RESIDUAL_TO_ROUTE` |

`state` carries the GUARANTEE state of TSD S3 T4 (the 17-state set, 32 rules) and `status` carries LOV-CLAIM-STATUS — `PREPARING`, `FILED`, `DEFECT`, `PAID`, `REJECTED` — so the two vocabularies are kept apart and the screen labels of SCR-17 — Not due, due, submitted, paid, refused — are the screen's own (GAP-2729; ASM-4530). `SUBROGATION_POSITION` to `RESIDUAL_TO_ROUTE` under R-GUA-25 and the closing of the guarantee under R-GUA-26 belong to FEAT-GUA-07 and are not this story's.

`SUBROGATION_POSITION` and `RESIDUAL_TO_ROUTE` are values of `guarantee_claim.state` (the GUARANTEE set of TSD S3 T4). This story does not add them to LOV-CLAIM-STATUS, which it only reads (DOR-RWB-S3-E4018-APP-5).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery squad (RW-TRIBE) | Writes the guarantee stage, the three activities, the operation and the repository |
| RW-CASEOWN, case owner | Records the negotiation and the outcome; holds CRU, so right C, R and U |
| RW-GUARANT, guarantee officer | Records the negotiation and the outcome; holds CRU |
| RW-RESTRUCT, restructuring officer (FCR) | Records the negotiation and the outcome; holds CRUA |
| RW-SPECIAL, hardship and vulnerability specialist | Records the negotiation and the outcome; holds CRU |
| RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL | Read the claim; right R only |
| RW-PRODHEAD, RW-CREDCOMM | Read, and approve where another story's matrix requires it; right RA |
| SY-CASEWF, SY-RULES, SY-AGENT | Read as service identities, subject to the same checks |
| The case status and the case-level storage of the TCG share | Not this story: rwb-case owns them and the parent moves and keeps them |
| The closing of the guarantee, the balance claim and the demand notice | Not this story: FEAT-GUA-07, FEAT-GUA-02 and FEAT-GUA-05 slices |

The rights above are those of TSD S3 T6.1 and of the permission table of the legacy story, and the check itself is the platform guard library's: this story declares capability area "Treatment and offer" and rights C and U and calls the guard, and it owns no check of its own. No credential and no personal name appears in the request, the payloads or the logs, which carry case IDs, claim IDs, amounts, dates, codes and rule versions only.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-015 | guarantee_claim | id | Read |
| DF-TRT-016 | guarantee_claim | case_id | Read |
| DF-TRT-017 | guarantee_claim | claim_type | Read: TCG, CREDIT_LIFE_INSURANCE, MORTGAGE_INSURANCE, COLLATERAL_INSURANCE |
| DF-TRT-018 | guarantee_claim | claim_deadline | Read |
| DF-TRT-019 | guarantee_claim | claimed_amount | Read |
| DF-TRT-020 | guarantee_claim | filed_at | Read |
| DF-TRT-021 | guarantee_claim | paid_amount | Write: the amount the TCG paid |
| DF-TRT-022 | guarantee_claim | status | Write: LOV-CLAIM-STATUS |
| T3.0 `state` | guarantee_claim | the GUARANTEE state of TSD S3 T4 | Write |
| T3.0 `version`, `updated_at`, `updated_by` | guarantee_claim | standard record columns | Write |
| Not a field: `subrogationShare` | guarantee_claim | the TCG share kept for later recoveries | Write, on a column this story adds |
| DF-DEC-001 to DF-DEC-018 | decision_record | the record fields of the library | Write through RWB-PLT-E1027-CON |
| Not a column: the approved range and its bounds | stage signal | the request context facts | Read only, for the length of the request and of the record |

`guarantee_claim` is the only business table this story writes, in schema `rwb_guarantee` and through this service's own login (DP-01). The `decision_record` row is a library object applied by the per-service Flyway sequence and written through RWB-PLT-E1027-CON in the caller's transaction; `decision_log_entry` in `rwb_decision` is P7's and is neither written nor read. The TCG share has no field identifier and no column in TSD S3 T3.1, which stops at DF-TRT-022, so its name, type and unit are Not specified in the source documents (GAP-2728; GAP-2730; ASM-4535). No table of another service is read: `recovery_case`, `case_party`, `assignment` and `timer` of the legacy data table are rwb-case's, and `v_ace_customer` is read by rwb-source-data (DP-05).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-guarantee (S3); base `/api/recovery/guarantee/v1` (DP-13). The service publishes two operations; this story supplies the behaviour of the second and the contract publishes both.

| Method | Path | Documented shape | Access | Idempotency | This story |
|---|---|---|---|---|---|
| PATCH | `/guarantee-claims/{claimId}` | `GuaranteeClaimUpdate` in, `GuaranteeClaim` out | Treatment and offer, right U | Not applicable (TSD S3 T-A.2) | Supplied here |
| POST | `/cases/{caseId}/guarantee-claims` | `GuaranteeClaimRequest` in, `GuaranteeClaim` out | Treatment and offer, right C | `Idempotency-Key` header (TSD S3 T-A.2) | Published by the contract; behaviour of the claim-preparation slice |

The errors are 401, 403 with MSG-P4-002, 404, 409 on a state conflict, 422 with MSG-GEN-001 for a missing, invalid or out-of-range field, and 503 when the package or the library does not answer; the set is the one TSD S3 T-A.2 lists. The service publishes no read operation, so SCR-17 is composed by the gateway-bff route from the case read of rwb-case and the claim the stage holds (GAP-2730; ASM-4533). The field list of `GuaranteeClaimUpdate` is the working read of the contract story and is not restated here.

#### 12.2 REST operations consumed

None. Nothing is called over REST: the case, its status, the claim reference and the approved range arrive on the signal the parent `CaseWorkflow` forwards, and the decision record is called in process inside the caller's transaction (DP-03). This is why the Work Package records no C dependency for this story.

#### 12.3 Events published

None. The topic of the service is `rwb.guarantee.events.v1` with event names `rwb.guarantee.<Event>.v1` (DP-14), and the ownership rows of S3 give the service no event: the outcome is reported to the parent `CaseWorkflow` as a stage outcome, so a replay of the stage produces no second message and no outbox row is written.

#### 12.4 Events consumed

None. No subscription is declared. The payment that triggers a subrogation and the refusal that triggers `RESIDUAL_TO_ROUTE` reach the stage as signals the parent forwards, and the event that would carry a guarantee payment is named by no source, so the form of the subscription is Not specified in the source documents (GAP-2728; ASM-4531). If the service must subscribe, the event name and the subscription belong to the payment story and to the event catalogue.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `GuaranteeClaimWorkflow` | Workflow, one execution per case per guarantee stage, the child of `CaseWorkflow` | `rwb-guarantee` in namespace `rwb-recovery` | Workflow ID form: Not specified in the source documents (CG-ALL-8922); start: a guarantee is found at takeover and the claim deadline timer starts (R-GUA-01); duplicate-start policy: Not specified in the source documents (CG-ALL-8922). Input: the case, the claim reference, the GUARANTEE state, the guaranteed amount and the approved range as context; signals: the case status forwarded by the parent, the rule package in force |
| `evaluateNegotiation` | Activity | `rwb-guarantee` | The negotiation outcome, the range and the claim state in; the selected rule, the range answer and the GUARANTEE event out |
| `applyOutcome` | Activity | `rwb-guarantee` | The `guarantee_claim` columns of the outcome — `status`, `state`, `paid_amount` and the TCG share |
| `recordAndApply` | Activity | `rwb-guarantee` | The `DecisionRecord` and the `guarantee_claim` row written in one transaction through RWB-PLT-E1027-CON, and the stage outcome for the parent |

The workflow is the one the context pack owns for S3 and the one Architecture v5 slide 13 names as the guarantee child, and the parent-and-child model with the four steps of receive, ask, record and apply, wait is the one of the Temporal and Drools Design slides 12 and 13. The activity names are a target design choice of this story and are fixed by no source document. A workflow class never calls the record library directly: the call is made inside `recordAndApply`, so a replay reuses the recorded decision.

#### 12.6 Schedules

None. The ownership rows give S3 no job: the stage runs from the signal the parent forwards and from the officer's call, and the claim deadline and the notice expiry are durable timers inside the workflow and not Temporal Schedules. The deadline timer of R-GUA-01 and the notice timer of R-GUA-06 are set by the claim-preparation and notice slices on the same workflow.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `guarantee_claim` | `rwb_guarantee` | S3 rwb-guarantee | Written by this story for DF-TRT-015 to DF-TRT-022, the `state` value of TSD S3 T4, the TCG share and the standard columns of T3.0; created by the per-service Flyway sequence and never re-created here |
| `decision_record` | `rwb_guarantee` | PLT, library object | Not written directly: the row is written by RWB-PLT-E1027-CON in the caller's transaction (DP-03) |

`guarantee_claim` is the single table the ownership rows give S3, and it holds the eight fields of TSD S3 T3.1 plus the standard columns of T3.0. No table of another service is read and no foreign key crosses a schema (DP-01); `recovery_case` and `case_party` are rwb-case's and are named here only. No range, expiry or notice column is added: those facts belong to the request context and to the decision record.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-S3-E4018-CON claim fake | The two operations, the elements and the error set | A `PATCH` answering a `SUBROGATION_POSITION` outcome and a `RESIDUAL_TO_ROUTE` refusal; a repeated `Idempotency-Key` on the `POST`; 422 for a missing or out-of-range field; 403 for a role without right U |
| RWB-PLT-E1027-CON writer fake | The decision record | An accepted record with chain sequence and entry hash; a refusal with MSG-P7-009 and the field; a failed write raising MSG-P7-003; a call with no transaction refused before any write |
| RWB-PLT-N001-CON route fake | The gateway-bff composite route of SCR-17 | A composite answer that joins the case read of rwb-case with the claim the stage holds; a refused route for a role without the right |
| rwb-case status mock | The signal the parent forwards, used by AC2 and AC3 | A case at `CLAIM_PAID` and a case at `CLAIM_PART_PAID`; a GUARANTEE state the stage does not accept. Test-only; adds no contract dependency |
| Range fixture | The context fact of the approved range | One claim with its range on the signal and one outcome outside it. The bounds are synthetic because no source states them (GAP-2728; ASM-4529) |

The claim, writer and route fakes are the published contracts of those stories; the case-status mock and the range fixture stand in for the signal of the parent, which has no published contract of its own here.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 operations on `/api/recovery/guarantee/v1` | None | One hop from the BFF, 2 s timeout; the two shapes are declared by RWB-S3-E4018-CON |
| Kafka | None | None | The topic `rwb.guarantee.events.v1` is named and unused; the service owns no event (DP-14) |
| Temporal | None | `GuaranteeClaimWorkflow` and 3 activities on `rwb-guarantee` | Namespace `rwb-recovery`; guarantee stage child of `CaseWorkflow`; no Schedule |
| File | None | None | No file is read or written |
| SQL view | None | None | No `v_ace_*` view is opened by this story (DP-05) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.guarantee`, modules `negotiation` and `web`, with the published types in `...guarantee.api`. Service base `/api/recovery/guarantee/v1`, schema `rwb_guarantee`, topic `rwb.guarantee.events.v1`, task queue `rwb-guarantee` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the negotiation: the record and the claim row commit together, and a failed record leaves nothing behind. DP-05 is applied as a removal: no `AceSourceQuery` and no `v_ace_*` read remains in this build, because the negotiation needs the claim, the party reference and the range (ASM-4532). DP-13 moves the base of the two operations and nothing else. DP-19 is how SCR-17 reaches the service, one hop through the gateway, so no screen reads a table and no screen calls another service.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `GuaranteeClaimWorkflow` guarantee stage | Workflow | One execution per case per guarantee stage; the claim facts, the case signal, the package in force and the stage outcome |
| `evaluateNegotiation` | Activity | Field validation, the range check and the two subrogation rules of the GUA package with the version in force |
| `applyOutcome` | Activity | The `guarantee_claim` columns of the outcome, including the TCG share |
| `recordAndApply` | Activity | The `DecisionRecord` and the claim row in one transaction through RWB-PLT-E1027-CON |
| `GuaranteeClaimController` | Controller | The `PATCH` operation, the right U check through the guard and the error mapping |
| `GuaranteeClaimRepository` | Repository | The claim columns and the TCG share in `rwb_guarantee`, with the optimistic lock of `version` |
| `StageOutcomeReporter` | Signal reporter | The outcome the parent `CaseWorkflow` uses to move the case and to keep the share; it reports, it never writes a case row |

**Database.** `guarantee_claim` holds DF-TRT-015 to DF-TRT-022, the `state` value of TSD S3 T4, the standard columns of T3.0 with the optimistic lock on `version`, and the TCG-share column this story adds, whose name, type and unit are Not specified in the source documents (GAP-2728; ASM-4535). The range and the notice expiry are not columns. `decision_record` is the library object applied by the per-service Flyway sequence, and this story writes it only through the library.

**Configuration and reference data.** Capability area "Treatment and offer" and rights C and U are access rows of rwb-access, read through its guard. The approved range, the notice expiry and the guarantee scheme values are values in force with their version, read at run time and never written in code (BR-S3-006). The GUA package and its version come from `rwb.decision.RulePackageInForce.v1` and are never configured here.

**Build steps**

1. The guarantee stage of `GuaranteeClaimWorkflow` and its input record, registered on `rwb-guarantee` as the child of `CaseWorkflow`, with the case signal and the claim facts (AC2, AC3).
2. `evaluateNegotiation` with the field validation, the range check and the two subrogation rules, against the claim fake (AC1, AC2, AC3).
3. `applyOutcome` with the claim columns and the TCG share, plus the refusal branch of R-GUA-29.
4. `recordAndApply` with the `DecisionRecord`, the `MANDATORY` transaction and the claim row, plus the failed-write path (AC4).
5. The `PATCH` operation with the guard check and the error mapping of section 12.1 (AC1).
6. `StageOutcomeReporter` and the parent signal, with the subrogation outcome and the share.
7. Tests for AC1 to AC4 against the fakes and the range fixture, plus the two component cases of section 16.

**Feature flag.** `rwb.guarantee.guarantor-negotiation`.

**Done when.** The tests in section 16 pass, the stage runs from a synthetic case signal in SIT, an in-range outcome writes the claim with its share and its GUARANTEE state, an out-of-range outcome writes nothing, a failed record write rolls the claim row back, the parent receives the `SUBROGATION_POSITION` or `RESIDUAL_TO_ROUTE` outcome, and SCR-17 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of the negotiation is absent or invalid, the range among them | Enter {field}. |
| MSG-P4-002 | The role does not hold right U on the capability area | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | The decision record is refused for a field | The decision record was refused: {field} is missing or not valid. |

The first three texts are the legacy texts of RWB-E4-018 carried unchanged, and MSG-P7-009 is the library's answer, raised by RWB-PLT-E1027-CON and shown by this story. No message holds a constant: MSG-GEN-001 carries the field name, MSG-P4-002 the action and MSG-P7-009 the refused field. The entry format of each message in a published catalogue is Not specified in the source documents (GAP-2730; ASM-4533). Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-17 Guarantee claim is the legacy screen of this story and keeps its state list unchanged: Not due; due; submitted; paid; refused. The empty, loading, error and no access states are absent from Screen Specifications v1 and are Not specified in the source documents (CG-ALL-8928); the no access behaviour is X1 of section 5. It is where the officer reads the claim, the claim deadline, the scheme checklist and the claim result, and where the negotiation outcome is recorded; it reaches the service through the gateway-bff composite route, one hop, which joins the case read of rwb-case with the claim the stage holds (DP-19; ASM-4533). The screen labels are the screen's own and are not the stored `status` of LOV-CLAIM-STATUS or the GUARANTEE `state` of TSD S3 T4, whose mapping is a working read owned by the screen owners (GAP-2729; ASM-4530). The screen field list and the composite route specification belong to the platform edge story and the screen owners; this story fixes the service side of the answer only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-018-01 | AC1 | End to end | Negotiate with a guarantor |
| TC-E4-018-02 | AC2 | End to end | Rule R-GUA-23 |
| TC-E4-018-03 | AC3 | End to end | Rule R-GUA-24 |
| TC-E4-018-04 | AC4 | End to end | Not recorded |
| TC-E4-018-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E4-018-06 | Principle 5 | Component | A forced decision record write failure stops the action with MSG-P7-003 |
| TC-E4-018-07 | Section 12 (operations, events and activities) | Contract | Operations, events and activities of section 12 |
| TC-E4-018-08 | Section 12.7 (ASM-3438) | Component | Each table of section 12.7 at its boundary |
| TC-E4-018-09 | AC5, BR4 | End to end | The guarantor refuses, or the notice expires with no answer |
| TC-E4-018-10 | BR1 | Component | An outcome inside and an outcome outside the approved range |
| TC-E4-018-11 | BR2, BR3 | Component | Share recorded and claim moved at CLAIM_PAID and CLAIM_PART_PAID |
| TC-E4-018-12 | BR5 | Component | Claim row and decision record commit together or not at all |
| TC-E4-018-13 | BR6, X5 | Component | A required negotiation field absent, refused with MSG-GEN-001 |
| TC-E4-018-14 | BR7 | Component | Business-changeable values read from reference data with version |
| TC-E4-018-15 | BR8 | Component | No range, expiry or notice column in rwb_guarantee |
| TC-E4-018-16 | AC6 | Component | A claim at a GUARANTEE state the stage does not accept; the status change is refused and no outcome is written |
| TC-E4-018-17 | AC7, BR1 to BR8 | Component | Each rule of section 8 applied and checked by its own case above |
| TC-E4-018-18 | AC8 | Contract | A request the operation refuses with 401, 403 or 404 under TSD S3 T-A.2 |
| TC-E4-018-19 | AC9 | Component | Not specified in the source documents (NEWAC-RWB-S3-E4018-APP-AC8) |
| TC-E4-018-20 | AC10 | Component | Not specified in the source documents (NEWAC-RWB-S3-E4018-APP-AC9) |

The six legacy test case IDs, their Covers and their Data are kept in order and character for character; the legacy level "System" maps to "End to end" and "Access" and "Principle 5" map to "Component", as in the other stories of this run. The claim fake, the decision-record writer fake and the range fixture of section 12.8 stand behind every case, and the case-status mock supplies the two states of AC2 and AC3. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 3 integration harness and are not listed here.

### 17. Guardrails

- No value that a business person may change is written in code: the approved range, the notice expiry and the scheme values are values in force in reference data, read with their version (BR-S3-006).
- No personal data in logs, events, workflow inputs, prompts or the fixture: the rows carry case IDs, claim IDs, amounts, dates, codes and rule versions only, and the test data is synthetic.
- No read of another service's table: the case status, the party reference and the range arrive as a signal, the claim facts are this service's own, and `decision_log_entry` is P7's and is never touched (DP-01).
- ACE data only through the owner's contract or the `v_ace_*` views, and this story opens neither: the legacy `v_ace_customer` read is removed (DP-05; ASM-4532).
- No range, expiry or notice column in `rwb_guarantee`; a schema change that adds one fails the guardrail test (DP-01; ASM-4529).
- No event of this story and no outbox row: the outcome is reported to the parent, so a replay of the stage produces no second message.
- The decision record and the claim row commit in one transaction through the `MANDATORY` rule of the library; an action that commits without its record is a build failure, not a defect (DP-03).
- An applied migration is never edited: the TCG-share column and any correction are a new version on the service sequence.
- No screen calls a service directly and no screen reads a table: SCR-17 goes through the gateway-bff composite route (DP-19).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S3-005 | A guarantor who answers a demand enters the same treatment paths as a borrower | Epic 4 BRD, S3 module | FEAT-GUA-06 | D6.5, D6.6 Guarantee claim | R-GUA-23, R-GUA-24, R-GUA-29; BR1 to BR4 | TC-E4-018-01, TC-E4-018-02, TC-E4-018-03 |
| REQ-S3-003 | A guarantee payment that clears the balance closes the case and records the subrogation position | Epic 4 BRD, S3 module | FEAT-GUA-06 (the recording half; the closing half is FEAT-GUA-07) | D6.5, D6.6 Guarantee claim | R-GUA-23, R-GUA-24 | TC-E4-018-02, TC-E4-018-03 |
| Legacy test set RWB-E4-018 | TC-E4-018-01 to TC-E4-018-06 | Epic 4 BRD, S3 module | FEAT-GUA-06 | D6.5, D6.6 Guarantee claim | R-GUA-23, R-GUA-24, R-GUA-29 | TC-E4-018-04, TC-E4-018-05, TC-E4-018-06 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S3-E4018-CON | Contract | H: declares the two operations, the elements, the context-only negotiation facts, the error set and the fakes |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record writer called in the caller's transaction with the `MANDATORY` rule |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route that SCR-17 uses |
| The claim-preparation slices of FEAT-GUA-01, FEAT-GUA-02 and FEAT-GUA-03 | App development | Sibling: creates and files the claim this story patches and records the balance claim; no build dependency is recorded |
| The FEAT-GUA-05 slice | App development | Sibling: the demand to the guarantor and its expiry, which start the refusal path of R-GUA-29 |
| FEAT-GUA-07 slice (legacy RWB-E4-019) | App development | Sibling: closes the guarantee and the case under R-GUA-26 and returns the residual under R-GUA-25 |
| rwb-case (P3) | Service, wave 1 | Owns the case, its status, the party reference and the case-level keeping of the TCG share; the stage reports and never moves the status |
| P7 rwb-decision | Service, wave 1 | Owns `rwb.decision.RulePackageInForce.v1` and the GUA package registry |
| rwb-source-data (P1) | Service, wave 1 | Owns the ACE views; this story opens none of them (DP-05) |
| rwb-payment (P8) | Service, wave 2 | Produces the guarantee payment that triggers a subrogation; the event name is not fixed here |
| Wave 3 integration harness | Integration | I: the cross-service proof of the same legacy key against the live owners, with the `-ITG` copies of the six test cases |

### 19. Out of scope

- The published shape of the two operations, the elements, the context-only facts, the error set and the fakes: RWB-S3-E4018-CON.
- The preparation, the checklist and the filing of the claim, and the balance claim under R-GUA-21: the claim-preparation slices of FEAT-GUA-01, FEAT-GUA-02 and FEAT-GUA-03.
- The demand to the guarantor and co-borrowers, its template and its expiry under R-GUA-06: the FEAT-GUA-05 slice.
- Closing the guarantee and the case under R-GUA-26, and returning the residual under R-GUA-25 and R-GUA-19: the FEAT-GUA-07 slice (legacy RWB-E4-019).
- The insurance claim on a collateral event under FEAT-GUA-08: its own slice.
- The case, its status, the party reference, the parent `CaseWorkflow`, the case router and the case-level keeping of the TCG share: rwb-case (P3).
- The decision-record library, its chain, its envelope and the central ledger of P7: RWB-PLT-E1027-CON and RWB-PLT-E1027-APP.
- The GUA rule package, its authoring, its approval and its promotion: P7 rwb-decision, with the embedded runtime as a service-template capability.
- The gateway-bff composite route and the screen field list of SCR-17: RWB-PLT-N001-CON and the screen owners.
- The ACE views and the customer, account and payment data behind them: rwb-source-data (P1), which this story does not call (DP-05).
- The event that carries a guarantee payment and any subscription to it: the payment story and the event catalogue (GAP-2728; ASM-4531).
- The deployment, the flag switch and the runbook: the platform DevOps stories of wave 3; the real cross-service proof: the wave 3 integration harness.
