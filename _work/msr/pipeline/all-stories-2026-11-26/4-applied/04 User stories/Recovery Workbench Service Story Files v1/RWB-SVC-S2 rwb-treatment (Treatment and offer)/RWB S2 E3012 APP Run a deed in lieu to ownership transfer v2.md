# RWB-S2-E3012-APP Run a deed in lieu to ownership transfer

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E3-012 for rwb-treatment. The deed-in-lieu journey leaves the monolith's S2 service in the one `recovery` schema and becomes the deed-in-lieu stage of `TreatmentWorkflow` on this service's own task queue, driving R-DIL-16, R-DIL-18, R-DIL-22, R-DIL-23 to R-DIL-26 and R-DIL-28 with the title hold of R-DIL-29, the AMIS record, the debt settlement and the registration release requested through their owners and returned as facts, the treatment facts written on the treatment row in the same transaction as the local decision record (DP-03), the ACE customer and NPA-asset facts read as facts (DP-05), the screens SCR-14 and SCR-16 reached through the gateway-bff composite route (DP-19), and `rwb.treatment.TreatmentApproved.v1` published on the treatment topic when the offer goes to the customer. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S2-E3012-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3012-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-012 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S2-W |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S2-E3012-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **recovery developer (RW-TRIBE)**, I want **the deed-in-lieu stage of `TreatmentWorkflow` on task queue `rwb-treatment` — the release of the offer with its document set and its validity timer (R-DIL-16), the customer acceptance and the field inspection (R-DIL-18, R-DIL-22), the asset-unlock decision and its approver path (R-DIL-23 to R-DIL-26), the transfer completion that records the asset, settles the debt and releases the registration (R-DIL-28) with the title hold of R-DIL-29, and the local decision record written in the same transaction — with the case status and the AMIS record carried by their owners, the customer and NPA-asset facts arriving as facts, every outcome reported to the parent `CaseWorkflow`, and `rwb.treatment.TreatmentApproved.v1` published on the treatment topic when the offer goes to the customer**, so that **a deed in lieu reaches the asset record in days instead of weeks, the transfer is provable with the rule version that made it, and no case table, no asset table and no ACE view is read or written by this service**.

This is the application slice of legacy RWB-E3-012. It owns:

- the four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages and data rows they depend on;
- the deed-in-lieu stage of `TreatmentWorkflow`, the stage child of `CaseWorkflow` on rwb-case, with the seven activities `generateOfferDocuments`, `scheduleInspection`, `recordInspection`, `decideAssetUnlock`, `completeTransfer`, `recordAndApply` and `publishApproved`;
- the `ApprovalWorkflow` child of the workflow kit on rwb-decision's queue for the approver release of R-DIL-24 and R-DIL-25, and the mapping of its answer onto the treatment;
- the treatment columns that hold the deed-in-lieu facts — `transferPrice`, `inspectionOutcome`, `unlockDecision`, `assetRef` and `transferredAt` — in schema `rwb_treatment`;
- the local decision record written through RWB-PLT-E1027-CON in the same transaction as the treatment change (DP-03);
- the request for the AMIS record, the debt settlement and the registration release through their owners, and the facts that come back for the treatment;
- the entry of the stage and the screen path of SCR-14 and SCR-16 through the gateway-bff composite route (DP-19).

It does not own: the published element set of the deed-in-lieu treatment, the event reference and the fakes, which are RWB-S2-E3012-CON; the treatment record itself and the offer operation, which are RWB-S2-E3001-APP and RWB-S2-E3002-APP; the below-floor second signature of the transfer price, which is RWB-S2-E3003-APP; the encumbrance and early-valuation check, which is FEAT-TRT-13; the document templates and the document hub, which are rwb-document and FEAT-TRT-18; the asset record, the AMIS interface and the core-bank settlement, which are rwb-asset and rwb-integration; the buy-back rental of FEAT-TRT-16; the case status, the case table and the task of the approver, which stay rwb-case's and rwb-decision's; and the deployment, dashboards and alerts, which are this legacy key's DevOps story.

### 2. Business rationale

A deed in lieu takes 26 days today against a 12-day target, and the case is tracked by hand across the offer, the inspection, the documents and the Land Office or SCIS step (Business Requirements Program, section 5.9; FSD S2 A2.12.1). The step that costs the days is not a decision: it is a chain of four handoffs — the offer to the customer, the field inspection, the asset unlock, and the transfer that must reach AMIS, ALS and the registration system before the asset is on the books. FEAT-TRT-12 asks for that chain to run end to end in the Workbench, and REQ-S2-007 and REQ-S2-008 ask that the asset be unlocked by rule and that the booked terms, the settled accounts and the released collateral be posted to their systems of record without re-keying; REQ-S2-006 asks that the documents come from templates.

The monolith answered it in one process: the S2 service moved `recovery_case.status` itself, wrote `decision_log_entry` in the same schema, read `v_ace_customer` and `v_ace_npa_asset` directly, wrote `document` rows, and called AMIS, ALS and SCIS in the same transaction boundary. In the 19-service target each of those facts has a different owner. The case status is rwb-case's and reaches the stage on the case signal the parent forwards (ASM-4388). The decision record is the platform library's, written locally in this service's schema (DP-03). The ACE customer and NPA-asset facts are rwb-source-data's, and the connection matrix gives rwb-treatment no link to rwb-source-data at all, so they arrive as facts on the case signal and no `v_ace_*` view is read here (DP-05; ASM-4389). The AMIS record, the debt settlement and the registration release are rwb-integration's and rwb-asset's, and they return as facts (ASM-4390). The documents are rwb-document's and the notice is rwb-comms' (ASM-4391).

What the business keeps is the rule, not the code. R-DIL-16 generates the documents and puts the offer to the customer when the second signature is given or the price is inside the floor; R-DIL-18 schedules the inspection before the transfer for a mortgage with a wet-ink signature; R-DIL-22 runs the asset unlock on the inspection; R-DIL-23 releases about 95% of cases without a person and R-DIL-24 sends the rest to the approver with a summary; R-DIL-28 records the asset in AMIS, settles the debt and releases the registration for HP; R-DIL-29 holds the transfer when the title is not clean, on a ten-working-day clock. The state names, the clocks, the reason codes and the product conditions are values in force of their owners, never constants (BR-S2-012).

Serves REQ-S2-006, REQ-S2-007 and REQ-S2-008. No business value moves into code.

### 3. Preconditions

- RWB-S2-E3012-CON is published: the deed-in-lieu element set (`transferPrice`, `inspectionOutcome`, `unlockDecision`, `assetRef`, `transferredAt`), the reuse of the `rwb.treatment.TreatmentApproved.v1` envelope, the rule that no table is created for the inspection or the transfer, the compatibility rule and the fakes (H).
- RWB-PLT-E1027-CON is published (DP-03): `DecisionRecordWriter.record(DecisionRecord)` with propagation `MANDATORY`, the refusal `DecisionLogRecordInvalidException` with MSG-P7-009 and its field, and `DecisionLogUnavailableException` with MSG-P7-003 (H).
- RWB-PLT-N001-CON is published (DP-19): the gateway-bff composite route that carries SCR-14 and SCR-16, one hop (H).
- RWB-S2-E3001-APP is done: `treatment` exists in schema `rwb_treatment` with DF-TRT-001 to DF-TRT-033, and its own migration sequence is the only place a column is added.
- RWB-S2-E3002-APP and RWB-S2-E3003-APP are done for the deed-in-lieu form: the offer surface, the transfer price and the below-floor second signature exist, so R-DIL-13, R-DIL-15 and R-DIL-16 have a price to offer.
- `rwb.decision.RulePackageInForce.v1` (EV-30) is consumed and the DEEDINLIEU package is in force with its version label, evaluated by the embedded Drools runtime (ASM-4392).
- The workflow kit and the outbox and inbox library are service-template capabilities (ASM-4392): the stage child, the `ApprovalWorkflow` child, the timers, the signal handling and the outbox are taken from the kit.
- The access guard is the platform guard library's; this story declares the capability area "Treatment and offer" and the rights the stage exercises — U for the officer and RA for the approver — with the roles TSD S2 T6.1 lists.
- The customer and NPA-asset facts are on the case signal; no `v_ace_*` view is read here (DP-05; ASM-4389). The AMIS, ALS and registration answers come back as facts from rwb-integration and rwb-asset (ASM-4390).
- The document set, the customer notice and the field-inspection capture are requested from rwb-document and rwb-comms through the workflow kit; the templates are FEAT-TRT-18's (ASM-4391).
- The product condition, the inspection and hold clocks, the unlock thresholds, the state names and the reason codes are values in force of their owners; this story holds no copy of any of them.
- No approval of this story is needed to build against a Draft contract baseline; RWB-S2-E3012-CON tags the version when its tests pass.

### 4. Flow

1. The parent `CaseWorkflow` on rwb-case forwards the case signal to the running `TreatmentWorkflow` child on `rwb-treatment`; the signal carries the case status, the product, the collateral and the customer and NPA-asset facts, and the status stays rwb-case's (ASM-4388; ASM-4389).
2. The stage holds a treatment of type DEED_IN_LIEU in TRANSFER_PRICE_SET with a transfer price set (R-DIL-13), or in AWAITING_SECOND_SIGNATURE when the price is below the floor (R-DIL-15).
3. `generateOfferDocuments` (R-DIL-16, on the second signature or on an inside-floor price of R-DIL-14): requests the deed-in-lieu document set on rwb-document's queue, asks rwb-comms for the customer notice through the workflow kit, writes the treatment's `valid_until`, starts the offer validity timer, writes the decision record, and `publishApproved` writes the outbox row for `rwb.treatment.TreatmentApproved.v1` (EV-10). The case reaches OFFER_WITH_CUSTOMER_DIL.
4. Customer acceptance arrives as a fact on the case signal (R-DIL-18); `scheduleInspection` reports the inspection need to the parent, which raises the field task in rwb-case, and the checklist and photographs land in rwb-document (ASM-4388; ASM-4391).
5. `recordInspection` (R-DIL-22): the completed checklist arrives as a fact; the treatment takes `inspectionOutcome` and the stage runs the asset-unlock rule.
6. `decideAssetUnlock` (R-DIL-23 to R-DIL-26): AUTO_UNLOCK_PASSED releases the asset for transfer with no person; AUTO_UNLOCK_FAILED starts the kit's `ApprovalWorkflow` child on rwb-decision's queue with the agent summary, and APPROVER_RELEASED or APPROVER_REFUSED decides the case. The treatment takes `unlockDecision`.
7. `completeTransfer` (R-DIL-28 for HP, R-DIL-27 for a mortgage): requests the asset record in AMIS and the asset on books in rwb-asset, and the debt settlement and registration release behind them; the answers return as facts on the workflow, and the treatment takes `assetRef`. A title or registration check that fails holds the transfer (R-DIL-29) on a ten-working-day clock, and a registry the answer does not name goes to UNMATCHED_EXCEPTION (R-DIL-36).
8. `recordAndApply`, one transaction: the treatment row takes `transferPrice`, `inspectionOutcome`, `unlockDecision`, `assetRef` and `transferredAt`; the decision record is written through `DecisionRecordWriter.record` (decision code D6.4, the rule ID and the rule version of the package that routed the answer, the recommendation, the final call, the outcome and the time); the outbox row is written in the same transaction.
9. The stage reports the rule outcome — ASSET_ON_BOOKS from R-DIL-28 or R-DIL-27 — to the parent; the parent moves the case status and rwb-asset and rwb-case act on it. This service publishes no transfer event: the catalogue names one event for the service, EV-10, and no source names one for the transfer (GAP-2672; ASM-4393).
10. A redelivered case signal or a repeated facts answer answers the open step and starts no second child or second request: the rejection and the workflow ID of this treatment carry the idempotency. The offer expiry timer (R-DIL-21) and the hold clock of R-DIL-29 are workflow timers of the stage, so a restart loses nothing.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without right U records the inspection or the transfer, or a role without RA answers the unlock | 403 from the guard; the refusal is logged and nothing changes | MSG-P4-002 | AC1, TC-E3-012-05 |
| X2 | The decision record cannot be written | The transaction rolls back: no treatment column, no outbox row, no status report to the parent | MSG-P7-003 | AC4, TC-E3-012-06 |
| X3 | The record is refused for a missing field | The transaction rolls back and the field is named in the service log and the incident | MSG-P7-009 | AC4 |
| X4 | The offer validity passes with no acceptance | The stage reports the expiry to the parent, which returns the case with reason `offer_expired`; no upload and no transfer request | None | AC1 |
| X5 | The inspection is incomplete or the checklist is missing a capture | The stage holds the case at WITH_FIELD_INSPECTION and names the missing item; no unlock is run | MSG-GEN-001 | AC1 |
| X6 | The unlock rule fails and the approver refuses | The stage reports the refusal to the parent, which returns the case with reason `unlock_refused` | None | AC1 |
| X7 | The transfer price or the offer date is stale when the documents are requested | The stage asks for a new figure and holds the document request | MSG-S2-002 | AC1 |
| X8 | The title or the registration check fails at transfer | The transfer is held, a task is raised to clear the title, and the ten-working-day clock of R-DIL-29 runs | None | AC2 |
| X9 | The registry the answer names is unknown, or AMIS does not answer inside the step | The stage goes to UNMATCHED_EXCEPTION with the missing field, or retries the request on the kit's policy and holds the case; no treatment fact is written on a partial answer | None | AC2 |

X1 to X4 are the exception paths of RWB-E3-012 carried onto the split; X5 to X9 are the paths of the target. The exception flows the FSD records for FEAT-TRT-12 — a role without the right and an unrecordable decision — are AC-EXC-S2-012-01 and AC-EXC-S2-012-02 and are X1 and X2 (FSD S2 A2.12.4.3).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published element set and fakes of RWB-S2-E3012-CON, the decision-record contract and the gateway route; no live rwb-case, rwb-document, rwb-asset or rwb-integration is needed to start, and the case status, the ACE facts and the AMIS answer arrive on mocks |
| Negotiable | The activity names, the shape of the treatment's five extra columns and the request bodies are this story's choice; the rules, the clocks and the reason codes are fixed by their owners' data |
| Valuable | A deed in lieu runs from the offer to the asset record with no hand-carried step, and the transfer is provable |
| Estimable | One stage, seven activities, one child workflow call, five treatment columns and one event |
| Small | Finished inside three weeks with its tests |
| Testable | Each criterion runs on synthetic treatments, offers and inspections through the contract fakes, plus one component test of the guard and the stage entry |

### 7. Acceptance criteria

```gherkin
Feature: Run a deed in lieu to ownership transfer

  Scenario: AC1 Run a deed in lieu to ownership transfer (legacy RWB-E3-012 AC1)
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then takes the deed in lieu from offer through inspection, documents and transfer to the asset record
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIL-28 (legacy RWB-E3-012 AC2)
    Given the rwb-case contract mock returns case status AWAITING_TRANSFER
    Given a case in state AWAITING_TRANSFER
    When transfer completed
    Then record the asset in AMIS, settle the debt and release the registration
    Then the case moves to ASSET_ON_BOOKS

  Scenario: AC3 Rule R-DIL-16 (legacy RWB-E3-012 AC3)
    Given the rwb-case contract mock returns case status AWAITING_SECOND_SIGNATURE
    Given a case in state AWAITING_SECOND_SIGNATURE
    When second signature given
    Then generate the documents and put the offer to the customer
    Then the case moves to OFFER_WITH_CUSTOMER_DIL

  Scenario: AC4 Not recorded (legacy RWB-E3-012 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Target reading.** Every one of the four criteria keeps its wording and its values; what changes is where each step runs, who owns each fact and how the answer is proved. The journey is no longer a set of steps of the monolith's S2 service in the one `recovery` schema: it is the deed-in-lieu stage of `TreatmentWorkflow`, the stage child of `CaseWorkflow` on rwb-case, on task queue `rwb-treatment` in namespace `rwb-recovery`, one parent per case and one child per stage (Temporal and Drools Design slides 13 and 18; ASM-4388). "The user acts on the screen" in AC1 is the restructuring officer on SCR-16 through the gateway-bff composite route (DP-19), and the result recorded "with the rule version" is the local decision record written through RWB-PLT-E1027-CON in the same transaction as the treatment change (DP-03); `decision_log_entry` is P7's ledger and is neither written nor read here. The statuses of AC2 and AC3 — AWAITING_TRANSFER, AWAITING_SECOND_SIGNATURE, ASSET_ON_BOOKS, OFFER_WITH_CUSTOMER_DIL — stay rwb-case's, which is why the two added Given lines are answered by the rwb-case contract mock standing in for the case signal: the stage reports the rule outcome and the parent moves the status (ASM-4388). "Record the asset in AMIS, settle the debt and release the registration" of AC2 is the request the `completeTransfer` activity makes to rwb-asset and rwb-integration and the facts it receives back on the workflow, R-DIL-28 being the HP branch whose registration sits in SCIS; no AMIS call, no ALS posting and no registry call is made from this service (ASM-4390; GAP-2672). "Generate the documents and put the offer to the customer" of AC3 is the document set requested on rwb-document's queue plus the notice asked of rwb-comms, with the validity date on the treatment and the offer timer in the workflow (ASM-4391). R-DIL-16, R-DIL-18, R-DIL-22, R-DIL-23 to R-DIL-26 and R-DIL-28 are evaluated by the embedded Drools runtime against the package version in force announced by `rwb.decision.RulePackageInForce.v1`, and that version is written with every answer (ASM-4392). The customer and NPA-asset facts that AC1 and AC2 need — the owner, the product, the collateral, the registration — arrive on the case signal as facts of rwb-source-data's read, because the connection matrix gives this service no call to rwb-source-data and slide 8 grants the `recovery.v_ace_*` views to rwb-source-data alone (DP-05; ASM-4389).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A given second signature or a transfer price inside the floor generates the documents and puts the offer to the customer, with the validity date on the treatment and the offer timer running, and moves the case to OFFER_WITH_CUSTOMER_DIL | R-DIL-14; R-DIL-16 |
| BR2 | The collateral inspection is scheduled before the transfer where the product and the signature basis require it, and the case reaches WITH_FIELD_INSPECTION | R-DIL-18; FSD S2 A2.12.3.1 |
| BR3 | The asset unlock runs on the completed inspection: it passes about 95% of cases with no person, and a failure goes to the approver with a summary | R-DIL-23; R-DIL-24; R-DIL-25; R-DIL-26 |
| BR4 | The transfer records the asset in AMIS, settles the debt and releases the registration for the product branch of the case, and the case reaches ASSET_ON_BOOKS | R-DIL-27; R-DIL-28 |
| BR5 | A title or registration check that fails at transfer holds the transfer, raises a task and runs a ten-working-day clock; an unknown registry goes to UNMATCHED_EXCEPTION with the missing field named | R-DIL-29; R-DIL-30; R-DIL-31; R-DIL-36; R-DIL-37 |
| BR6 | No value a business person may change is written in code: the product conditions, the clocks, the unlock thresholds, the state names and the reason codes are read as values in force with their version | BR-S2-012; FSD S2 A2.12.3.1 |
| BR7 | The deed-in-lieu facts are held on the treatment row as `transferPrice`, `inspectionOutcome`, `unlockDecision`, `assetRef` and `transferredAt`, and no table is created for the inspection or the transfer | GAP-2672; ASM-4393; TSD S2 T3.1 |
| BR8 | A step whose decision cannot be recorded does not take effect: the record joins the caller's transaction and a failed append rolls everything back | R-UNI-39; RWB-PLT-E1027-CON; Principle 5 |
| BR9 | The case status, the case task, the asset record, the AMIS interface and the documents stay with their owners; this stage requests them and writes none of them | DP-01; ASM-4388; ASM-4390; ASM-4391 |

**Where each rule lives in the target.** BR1 and BR2 are `generateOfferDocuments` and `scheduleInspection`: the validity date, the offer clock and the inspection trigger are values in force of rwb-case's reference data and the product rules, read and never copied (BR6). BR3 is `decideAssetUnlock`, which runs the unlock rule locally and starts the kit's `ApprovalWorkflow` child on rwb-decision's queue for the exception (ASM-4392). BR4 and BR5 are `completeTransfer`: the request to rwb-asset and rwb-integration, the facts that come back, and the hold with its clock. BR6 is served by reading every value from its owner; the only fixed strings in this story are the element and event names of its contract. BR7 is the five treatment columns and the absence of an inspection or transfer table. BR8 is `recordAndApply`: the treatment update, the decision record and the outbox row sit in one transaction, and `DecisionLogUnavailableException` (MSG-P7-003) and `DecisionLogRecordInvalidException` (MSG-P7-009) roll it back. BR9 is the signal contract with the parent and the request contract with rwb-asset, rwb-integration, rwb-document and rwb-comms (DP-01).

### 9. State transitions

None of the states below is this service's to change (ASM-4388). The stage evaluates the rule, records the outcome and reports it to the parent `CaseWorkflow`, and the parent moves the case status in rwb-case. The table lists the deed-in-lieu route of TSD S2 T4 as the stage asserts it, which is what AC2 and AC3 name.

| From (case status, rwb-case's) | Event | Condition | To (case status, rwb-case's) | Rule |
|---|---|---|---|---|
| TRANSFER_PRICE_SET | PRICE_INSIDE_FLOOR | `transfer_price >= floor_price` | OFFER_WITH_CUSTOMER_DIL | R-DIL-14 |
| TRANSFER_PRICE_SET | PRICE_BELOW_FLOOR | `transfer_price < floor_price` | AWAITING_SECOND_SIGNATURE | R-DIL-15 |
| AWAITING_SECOND_SIGNATURE | SECOND_SIGNATURE_GIVEN | `final_call = approved` | OFFER_WITH_CUSTOMER_DIL | R-DIL-16 |
| AWAITING_SECOND_SIGNATURE | SECOND_SIGNATURE_REFUSED | `final_call = rejected` | RETURNED_TO_ROUTE_DIL with reason `price_below_floor` | R-DIL-17 |
| OFFER_WITH_CUSTOMER_DIL | CUSTOMER_ACCEPTED | acceptance recorded and a signature basis exists | WITH_FIELD_INSPECTION | R-DIL-18 |
| OFFER_WITH_CUSTOMER_DIL | OFFER_EXPIRED | offer validity passed | RETURNED_TO_ROUTE_DIL with reason `offer_expired` | R-DIL-21 |
| WITH_FIELD_INSPECTION | INSPECTION_COMPLETED | checklist, photographs and bills captured | ASSET_UNLOCK_DECISION | R-DIL-22 |
| ASSET_UNLOCK_DECISION | AUTO_UNLOCK_PASSED | unlock rule passes | AWAITING_TRANSFER | R-DIL-23 |
| ASSET_UNLOCK_DECISION | AUTO_UNLOCK_FAILED | unlock rule fails | AWAITING_APPROVER_SUMMARY | R-DIL-24 |
| AWAITING_APPROVER_SUMMARY | APPROVER_RELEASED | `final_call = approved` | AWAITING_TRANSFER | R-DIL-25 |
| AWAITING_TRANSFER | TRANSFER_COMPLETED | registration or ownership transfer confirmed | ASSET_ON_BOOKS | R-DIL-27; R-DIL-28 |
| AWAITING_TRANSFER | TITLE_NOT_CLEAN | title or registration check fails | TITLE_NOT_CLEAN, held on the clock | R-DIL-29 |
| TITLE_NOT_CLEAN | TITLE_CLEARED | check passes | AWAITING_TRANSFER | R-DIL-30 |
| AWAITING_TRANSFER | TRANSFER_COMPLETED | the registry is not one the answer names | UNMATCHED_EXCEPTION | R-DIL-36 |

Two states of the stage's own object are visible in the outcome: the treatment's `unlockDecision` is empty until the unlock has decided and carries the rule's answer after it, and the treatment carries no state machine of its own beyond the LOV-TRT-OUTCOME values that later steps write.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery squad (RW-TRIBE) | Writes the stage, the seven activities, the child-workflow call and the five treatment columns |
| RW-RESTRUCT, restructuring officer (FCR) | Runs the deed-in-lieu journey on SCR-16, records the acceptance and the transfer facts; holds CRUA in "Treatment and offer" |
| RW-CASEOWN, RW-GUARANT, RW-SPECIAL | Hold C, R and U in "Treatment and offer" and may progress a case; they do not release the asset |
| RW-PRODHEAD, RW-CREDCOMM | Hold RA and answer the unlock where the matrix names them |
| RW-HEADNPA, Head of NPA | The role R-DIL-24 and R-DIL-25 name as the owner of the unlock exception |
| The field officer, in the field app | Captures the checklist, the photographs and the bills; the capture is rwb-document's and the task is rwb-case's |
| RW-AUDIT, RW-COE | Read the recorded decision and the treatment outcome; they change nothing |
| rwb-case (P3) | Owns the case status, the case task and the clock the stage reads as a value |
| rwb-decision (P7) | Owns the `approval` record, the `ApprovalWorkflow` on its own queue and the rule packages and their versions |
| rwb-asset (S5), rwb-integration (P2) | Own the asset record, the AMIS interface, the debt settlement and the registration release |
| rwb-document (P5), rwb-comms (P6) | Own the document set, the templates and the customer notice |
| rwb-source-data (P1) | Owns the ACE customer and NPA-asset read that reaches this stage as facts |
| No delegation of authority level applies to this story | The story builds the stage; the level that applies is a data value of the approver's row, never a decision of this code |

No credential, personal name or email address appears in the workflow input, the activity payloads, the event or the logs, which carry treatment and case identifiers, codes, amounts, versions and timestamps only.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-002 | treatment | case_id | Read |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-005 | treatment | proposed_by | Read |
| DF-TRT-006 | treatment | proposed_at | Read |
| DF-TRT-007 | treatment | offer_amount | Read; carries the transfer price on this path |
| DF-TRT-010 | treatment | valid_until | Write at R-DIL-16 |
| DF-TRT-011 | treatment | approval_level | Read |
| DF-TRT-013 | treatment | outcome | Read |
| DF-TRT-014 | treatment | outcome_at | Read |
| (no field ID) | treatment | transferPrice, inspectionOutcome, unlockDecision, assetRef, transferredAt | Write |
| DF-DEC-001 to DF-DEC-018 | decision_record (library object in `rwb_treatment`) | id, case_id, decision_code, rule_id, rule_version, model_version, idempotency_key, approval_level, final_call, outcome, decided_at, chain_seq, entry_hash and the rest | Write through `DecisionRecordWriter` |
| DF-ACE-055 to DF-ACE-074 | v_ace_customer (`rwb_source_data`'s read) | person_key, cif_no, first_name, last_name, date_of_birth and the rest | Read as facts on the case signal, never from the view |
| DF-ACE-208 to DF-ACE-219 | v_ace_npa_asset (`rwb_source_data`'s read) | asset_ref, asset_key, asset_code, transfer_in_type, from_segment, book_value and the rest | Read as facts on the case signal, never from the view |
| DF-REF-001 to DF-REF-015 | rule_row (`rwb_decision`) | rule_id, rule_version, from_state, event_code, condition, target state | Read as the evaluated package, never from the table |

`treatment` is this service's table and the only one this story writes, together with the library's `decision_record` and the outbox in the same schema (DP-01; DP-03). The five deed-in-lieu columns carry no field ID and no column definition in the TSD, which lists DF-TRT-001 to DF-TRT-033 and has no transfer price, no inspection and no asset reference: their names and types are the working read of the gap and the assumption below. `recovery_case`, `assignment`, `document` and the two `v_ace_*` views belong to rwb-case, rwb-case, rwb-document and rwb-source-data: the case facts and the asset facts arrive on the case signal, the documents are requested and not written, and no ACE view is named in a statement of this service (DP-05). Field IDs are those of the Logical Data Model and Data Dictionary. The element names, their types and the treatment's holding of them are Not specified in the source documents (GAP-2672; ASM-4393).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). This story declares no operation of its own: the stage is entered from the treatment the sibling stories publish and operates. The treatment resource and the read are RWB-S2-E3001-CON's (`POST /cases/{caseId}/treatments`, `GET /treatments/{treatmentId}`), and the draft-terms change and the offer are RWB-S2-E3002-CON's (`PATCH /treatments/{treatmentId}`, `POST /treatments/{treatmentId}/offer`, the latter superseding the `/submit` form of API Specification v4 and TSD S2 T-A.1 API-S2-004 under the source precedence of Template and Rules §R3).

| Element this story reads from the treatment | Source | Use |
|---|---|---|
| The stored terms, the treatment reference and `belowFloor` with the floor and the gap | RWB-S2-E3002-CON | The price the offer is built on and the branch that decides whether a second signature is needed |
| `transferPrice`, `inspectionOutcome`, `unlockDecision`, `assetRef`, `transferredAt` on the treatment | RWB-S2-E3012-CON | The deed-in-lieu facts this stage writes and the screens read |
| The treatment element of a read | RWB-S2-E3001-CON | The stage entry: the treatment exists and belongs to the case |

#### 12.2 REST operations consumed

None. The case status, the customer facts and the NPA-asset facts arrive on the case signal the parent `CaseWorkflow` forwards, which is the only way a case fact reaches this service (ASM-4388; ASM-4389). The document set, the customer notice, the asset record, the AMIS interface and the debt settlement are reached through Temporal on their owners' queues, because route services reach shared capabilities through Temporal and never REST (Architecture v5 slide 13 note; ASM-4390; ASM-4391). The approval is a child workflow of the kit on rwb-decision's queue. The Work Package lists no contract dependency for this story, and none is added.

#### 12.3 Events published

| Event | Topic | Key | Payload carries | Purpose |
|---|---|---|---|---|
| `rwb.treatment.TreatmentApproved.v1` | `rwb.treatment.events.v1` | `caseId` | The ten fields of the service envelope — treatmentId, caseId, treatmentType (DEED_IN_LIEU on this path), offerAmount (the transfer price), approvalLevel, approverRole, finalCall, decidedAt, ruleId, ruleVersion — with `approvalLevel` and `approverRole` present only where the price went below the floor | EV-10: tells rwb-comms to issue the offer documents and rwb-payment to expect the settlement of the debt (Architecture v5 slide 42 row 10) |

| Envelope element | Value |
|---|---|
| Mode | CloudEvents 1.0, binary mode |
| ce_specversion | 1.0 |
| ce_type | rwb.treatment.TreatmentApproved.v1 |
| ce_source | rwb-treatment |
| ce_subject | The case ID of the approved treatment |
| ce_id and traceparent | The event identifier and the W3C trace context of the transaction that wrote it |
| Payload | Identifiers and figures only; no personal data, no free text and no document content |

The envelope is the one RWB-S2-E3003-CON fixes for the service and this story publishes it at R-DIL-16, in the same transaction as the treatment change and the decision record, through the outbox relay (DP-03; ASM-4392). One event exists for this service and this path; the transfer completion of R-DIL-28 is announced by no event of this service, because the catalogue names none — a gap recorded below and closed by the case signal to the parent. The names follow Template and Rules §R4 and the topic is the service's own. The payload has no published shape and the field list is Not specified in the source documents (GAP-2672; ASM-4393).

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | P7 rwb-decision | EV-30: names the DEEDINLIEU package version in force, which the stage evaluates and writes into the decision record; a version is swapped in at the next event and no restart is needed |

Consumed through the inbox of the outbox library, so a redelivery of EV-30 is deduplicated by the cloud event id. The other events this service subscribes to — `rwb.payment.TreatmentBooked.v1` (EV-11), `rwb.payment.PaymentMissed.v1` (EV-12) and `rwb.deviation.DeviationRaised.v1` (EV-06) — are consumed by other stages of `TreatmentWorkflow` and not by this one.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow` | Workflow, the stage child of `CaseWorkflow` (rwb-case), one execution per case and stage, continue-as-new at the stage end | `rwb-treatment` in namespace `rwb-recovery` | Input: case ID, stage, case status, product, treatment ID and the case and asset facts; the stage outcome returned to the parent; search attributes CaseId and Stage |
| `ApprovalWorkflow` | Child workflow of the workflow kit, started on rwb-decision's queue | `rwb-decision` | Input: case, treatment, decision code D6.4, capability area, product group, amount and the agent summary; output: level, limit version, status, final call, approver reference and decided-at time |
| `generateOfferDocuments` | Activity | `rwb-treatment` | The treatment and the document set requested on rwb-document's queue, the notice on rwb-comms', the validity date; idempotent by treatment and request |
| `scheduleInspection` | Activity | `rwb-treatment` | The inspection need reported to the parent and the document references of the checklist |
| `recordInspection` | Activity | `rwb-treatment` | The completed checklist fact; the treatment's `inspectionOutcome` |
| `decideAssetUnlock` | Activity | `rwb-treatment` | The unlock rule's answer and, on failure, the `ApprovalWorkflow` child and its answer; the treatment's `unlockDecision` |
| `completeTransfer` | Activity | `rwb-treatment` | The request for the asset record, the debt settlement and the registration release, and the facts that return; the treatment's `assetRef` |
| `recordAndApply` | Activity | `rwb-treatment` | One transaction: the five treatment columns, the decision record through RWB-PLT-E1027-CON and the outbox row |
| `publishApproved` | Activity | `rwb-treatment` | The approved treatment and its facts; the outbox row the relay publishes as `TreatmentApproved` |

DP-03, DP-05, DP-13 and DP-19 are the patterns this story applies; the workflow and activity names are a target design choice fixed by no source document, and the stage model itself is the workflow kit's. The retry policy is the kit's, and the clocks of the route — the offer validity, the title hold and the appraisal of the sibling story — are values in force that the stage reads and never sets.

#### 12.6 Schedules

None. The stage is signal-started inside `TreatmentWorkflow` and owns no Temporal Schedule and no legacy Quartz job. The offer validity, the ten-working-day title hold and the inspection clock are workflow timers of this stage, so they survive a worker restart and a release.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | Updated by `recordAndApply`: `valid_until` (DF-TRT-010), `transferPrice`, `inspectionOutcome`, `unlockDecision`, `assetRef` and `transferredAt`; no row is inserted here |
| `decision_record` | `rwb_treatment` | PLT (library object, written through RWB-PLT-E1027-CON) | Written in the same transaction as the treatment update (DP-03) |
| `outbox` | `rwb_treatment` | S2, from the service template | Written in the same transaction; the relay publishes `TreatmentApproved` |
| `asset` | `rwb_asset` | S5 | Not written and not read: the asset record is requested and its reference returns as a fact |
| `document` | `rwb_document` | P5 | Not written and not read: the document set is requested and its references return as facts |
| `recovery_case`, `assignment` | `rwb_case` | P3 | Not written and not read: the status, the task and the facts arrive on the case signal |
| `v_ace_customer`, `v_ace_npa_asset` | ACE views, `rwb_source_data`'s read | P1 | Never named in a statement of this service (DP-05) |

No new table is created for the inspection or the transfer, and no foreign key crosses a schema (DP-01). `decision_log_entry` is P7's ledger and is named here only.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-S2-E3012-CON deed-in-lieu fake | The five treatment elements and the envelope reuse | A treatment at each deed-in-lieu state with its price, its inspection outcome, its unlock decision and its asset reference; a treatment with no inspection and one with no transfer |
| RWB-PLT-E1027-CON decision-record fake | The record write | An accepted record with chain sequence and entry hash; a refusal with MSG-P7-009 and the field; an unavailable writer with MSG-P7-003 |
| RWB-PLT-N001-CON gateway route fake | The composite route of SCR-14 and SCR-16 | A granted right U for the officer and RA for the approver; a refused answer; a scope miss |
| rwb-case case-status mock | The two added Given lines of AC2 and AC3 and the facts of the stage entry | Case status AWAITING_TRANSFER, AWAITING_SECOND_SIGNATURE and ASSET_ON_BOOKS on the signal, the product and the NPA-asset facts, and the status the parent reports back |
| rwb-asset and rwb-integration answer fake | The asset record, the AMIS reference, the debt settlement and the registration release | A transfer accepted with an asset reference; a title check that fails; a registry the answer does not name; a timeout |
| rwb-document and rwb-comms request fake | The document set and the notice | A document set accepted with its references; a missing template; a notice accepted |
| `ApprovalWorkflow` fake | The child workflow of the kit | An approver release at the level the matrix names; a refusal; HELD_NO_LIMIT; a timeout |
| Deed-in-lieu value fixture | The values in force | The product conditions, the unlock thresholds, the clocks and the reason codes `offer_expired`, `unlock_refused`, `title_not_clean` of their owners |

The element, decision-record and gateway fakes are the published contracts of those stories; the case-status mock stands in for the signal, which is the only way a case fact reaches this service (ASM-4388); the asset and document fakes stand in for the Temporal calls to their owners (ASM-4390; ASM-4391).

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0: the stage declares no operation | 0 | The treatment resource, the draft-terms change and the offer are sibling CON stories, reached through gateway-bff (DP-19) |
| Kafka | 1 event (`rwb.treatment.TreatmentApproved.v1`) on `rwb.treatment.events.v1` | 1 event (`rwb.decision.RulePackageInForce.v1`) | CloudEvents 1.0 binary mode, key `caseId`, outbox and inbox of the service template |
| Temporal | 1 stage workflow and 7 activities | 1 child workflow (`ApprovalWorkflow`) on rwb-decision's queue; activities on rwb-document, rwb-comms, rwb-asset and rwb-integration | Namespace `rwb-recovery`; no Schedule |
| File | None | None | No file is read or written; the field captures are documents of rwb-document |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, modules `deed-in-lieu` and `treatment`, with the published types in `...treatment.api`. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | ACE data read through rwb-source-data's contract or the service's own ACE views; here the facts arrive on the case signal and no view is named | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the record of each step inside the same transaction; DP-05 is the customer and NPA-asset read that comes to this stage as facts, because the connection matrix gives rwb-treatment no call to rwb-source-data and the views are granted to rwb-source-data alone (ASM-4389); DP-13 fixes the service base on which the sibling operations answer; DP-19 is the route by which SCR-14 and SCR-16 reach this service. The ownership rule of DP-01 is applied in prose and in the SQL: `recovery_case`, `asset`, `document` and the two views are never named in a statement of this service.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `TreatmentWorkflow` (deed-in-lieu stage) | Workflow | The offer release, the inspection, the unlock, the transfer, the outcome report and the record |
| `generateOfferDocuments` | Activity | The document and notice requests, the validity date and the offer timer |
| `scheduleInspection`, `recordInspection` | Activities | The inspection need, the checklist fact and the treatment's inspection outcome |
| `decideAssetUnlock` | Activity | The unlock rule and the `ApprovalWorkflow` child for the exception |
| `completeTransfer` | Activity | The asset, AMIS, settlement and registration requests and the facts that return |
| `recordAndApply` | Activity | The five treatment columns, the decision record and the outbox row in one transaction |
| `publishApproved` | Activity | The `TreatmentApproved` outbox row |
| `DeedInLieuHandler` | Handler | The stage entry from the case signal: the price, the state and the facts mapped onto the stage input |
| `TreatmentRepository` | Repository | The update of `treatment` by ID, with the optimistic-lock version of the row |

**Database.** `treatment` already holds DF-TRT-001 to DF-TRT-033. This story adds `transferPrice`, `inspectionOutcome`, `unlockDecision`, `assetRef` and `transferredAt` on the service's own migration sequence and creates no table: the inspection and the transfer have none of their own (GAP-2672; ASM-4393). `decision_record` is the library object of RWB-PLT-E1027-CON in the same schema.

**Configuration and reference data.** The product conditions of R-DIL-18 and R-DIL-28, the unlock thresholds, the offer and title clocks, the state names and the reason codes `offer_expired`, `unlock_refused` and `title_not_clean` are values in force of their owners and are read, never set here (BR6). The package version arrives through `rwb.decision.RulePackageInForce.v1`. The capability area and the rights are the guard library's data.

**Build steps**

1. The migration that adds the five deed-in-lieu columns to `treatment` on the service sequence, with no new table.
2. `generateOfferDocuments` against the document, notice and envelope fakes, with the validity date and the offer timer (AC1, AC3).
3. `scheduleInspection` and `recordInspection` against the inspection fixtures, complete and incomplete (AC1).
4. `decideAssetUnlock` against the unlock fixture and the `ApprovalWorkflow` fake, with the pass, the release, the refusal, HELD_NO_LIMIT and the timeout (AC1).
5. `completeTransfer` against the asset and integration answers, with the accepted transfer, the title hold, the unknown registry and the timeout (AC2).
6. `recordAndApply` with the treatment update, the decision record through the fake and the outbox row, and the rollback on MSG-P7-003 and MSG-P7-009 (AC4).
7. The stage entry and the guard, with the case signal, a role without right U and a role without RA (AC1, TC-E3-012-05).
8. The outcome report to the parent and the two mocked case statuses (AC2, AC3).
9. Tests for AC1 to AC4 against the fakes and the fixtures.

**Feature flag.** `rwb.treatment.deed-in-lieu`.

**Done when.** The tests in section 16 pass, a synthetic deed in lieu walks from TRANSFER_PRICE_SET to ASSET_ON_BOOKS in SIT with the document set, the inspection, the unlock and the transfer facts recorded on the treatment, `TreatmentApproved` appears on `rwb.treatment.events.v1` once at the offer release and not on a refusal, a forced record failure leaves the treatment unchanged with MSG-P7-003, and SCR-16 shows the stage, the inspection outcome and the asset reference through the gateway-bff route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S2-001 | The transfer price is below the floor of its case and has been routed for approval | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-002 | The payoff or the figure behind the offer is older than the freshness limit | The payoff is from {date}. A new figure has been requested. |
| MSG-S2-003 | The offer to the customer carries its end date | The offer to the customer ends on {date}. |
| MSG-GEN-001 | A required field of the inspection or the transfer is missing | Enter {field}. |
| MSG-P4-002 | The role does not hold the right the action needs in "Treatment and offer" | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | The record is refused for a missing or invalid field (service log and incident, not shown to the customer) | The decision record was refused: {field} is missing or not valid. |

The six legacy texts are carried unchanged; MSG-P7-009 comes with the decision-record contract of RWB-PLT-E1027-CON. MSG-S2-001 and MSG-S2-002 are raised by the branch of RWB-S2-E3003-APP and are listed because the legacy story carried them. Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-16 Deed in lieu: states Checks, appraisal, approved, transferred; this story owns the step from approved to transferred — the offer release, the inspection outcome, the unlock answer and the asset reference — and shows the deed-in-lieu facts of section 12.1. SCR-14 Treatment record (states Draft, submitted, approved, booked, broken) shows the treatment and its outcome. Both reach this service through the gateway-bff composite route (DP-19), which calls rwb-treatment and the screen's other owners in parallel, one hop each; the officer's action on SCR-16 is an update of the treatment through the surface of RWB-S2-E3002-CON, and the stage learns it on the case signal. The screen field list and the composite route specification belong to the platform edge story and the screen owners; this story fixes the service side only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-012-01 | AC1 | End to end | A deed-in-lieu treatment with a price, a document set, an inspection and an unlock answer; the officer acts on SCR-16 and the decision record carries the rule version |
| TC-E3-012-02 | AC2 | End to end | Case status AWAITING_TRANSFER on the case signal mock; the transfer completes for HP; the asset record, the debt settlement and the registration release return as facts and the case reaches ASSET_ON_BOOKS |
| TC-E3-012-03 | AC3 | End to end | Case status AWAITING_SECOND_SIGNATURE on the case signal mock; the second signature is given; the documents are generated, the offer goes to the customer and the case reaches OFFER_WITH_CUSTOMER_DIL |
| TC-E3-012-04 | AC4 | End to end | The decision-record fake refuses the write; nothing changes and MSG-P7-003 is shown |
| TC-E3-012-05 | Access | Component | RW-CASEOWN acts without right U and a role without RA answers the unlock; refused with MSG-P4-002 and nothing changes |
| TC-E3-012-06 | Principle 5 | Component | A forced decision-record write failure stops the action with MSG-P7-003; the treatment row, the outbox and the parent report are unchanged |

The six legacy test case IDs, their Covers and their Data are kept in order and character for character; the legacy level "System" maps to "End to end" and "Access" to "Component", as in the other stories of this run. The contract fakes of section 12.8 stand behind every case, and the `ApprovalWorkflow`, asset and document fakes replace the child workflow and the calls to their owners. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies belong to the wave 2 integration harness, RWB-ITG-W2, and are not listed here.

### 17. Guardrails

- No business value in code: the product conditions, the unlock thresholds, the clocks, the state names and the reason codes are values in force of their owners, read with their version, never constants (BR6).
- No personal data in logs, events, workflow inputs or the fixture: the stage carries treatment and case identifiers, codes, amounts, versions and timestamps; test data is synthetic and no customer field is copied.
- No read of another service's table and no read of an ACE view: the case and asset facts arrive on the case signal, the asset record and the documents are requested, and no `v_ace_*` view is named in a statement of this service (DP-01; DP-05; ASM-4389).
- No write outside the transaction that records the change: the treatment update, the decision record and the outbox row commit together or not at all (DP-03; BR8).
- The decision is written before the change takes effect, and a refused or unavailable record leaves the case exactly as it was, which is what R-UNI-39 and Principle 5 require.
- The rule version and the approver level are written with every answer, so an auditor can see why an asset was released or held.
- No case status and no case task is written: the parent moves the status and raises the task on the stage outcome (ASM-4388).
- One event only, and no event on a refusal or a hold: rwb-comms and rwb-payment hear only of an approved deed in lieu (EV-10).
- No credential, no secret and no document content appears in code, configuration, a prompt or an event payload.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-006 | The credit application, contract and mortgage documents for a deed in lieu are generated from templates | Business Requirements Program, section 5.9 | FEAT-TRT-12 | 07 Route, settle and claim | R-DIL-16 | TC-E3-012-01, TC-E3-012-03 |
| REQ-S2-007 | An asset accepted under a deed in lieu is unlocked as a non performing asset by rule, with exceptions summarized for the approver | Business Requirements Program, section 5.9 | FEAT-TRT-12 | 07 Route, settle and claim | R-DIL-22; R-DIL-23; R-DIL-24; R-DIL-25 | TC-E3-012-01 |
| REQ-S2-008 | Booked terms, settled accounts and released collateral are posted to their systems of record without re-keying | Business Requirements Program, section 5.9 | FEAT-TRT-12 | 07 Route, settle and claim | R-DIL-27; R-DIL-28; R-DIL-29 | TC-E3-012-02 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3012-CON | Contract | H: declares the deed-in-lieu element set, the event reference, the no-new-table rule and the fakes this story builds against |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library, its `MANDATORY` rule and its two exceptions (DP-03) |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route of SCR-14 and SCR-16 (DP-19) |
| RWB-S2-E3001-APP, RWB-S2-E3002-APP | App development | Same lane, earlier: the treatment record and the offer surface the stage stands on |
| RWB-S2-E3003-APP | App development | Same lane: the below-floor second signature of R-DIL-15 and the R-DIL-16 release on the below-floor path |
| RWB-ITG-W2 | Integration | I: the cross-service proof of the same legacy key against rwb-case, rwb-asset, rwb-document and rwb-integration; not this story's |

### 19. Out of scope

- The published element set, the event reference, the compatibility rule and the fakes: RWB-S2-E3012-CON.
- The treatment record, its creation, its fields DF-TRT-001 to DF-TRT-033 and its own migration: RWB-S2-E3001-APP and RWB-S2-E3001-CON.
- The offer surface `POST /treatments/{treatmentId}/offer`, the draft-terms change and the settlement range: RWB-S2-E3002-APP and RWB-S2-E3002-CON.
- The below-floor second signature and the transfer price comparison against the floor: RWB-S2-E3003-APP and RWB-S2-E3003-CON.
- The encumbrance and eligibility check before negotiation, the early valuation and the appraisal order: FEAT-TRT-13 and the sibling stories of this service.
- The document templates, the document hub, the e-signature and the customer notice: rwb-document, rwb-comms and FEAT-TRT-18.
- The asset record, the asset list, the AMIS interface, the core-bank settlement, the registration release in SCIS and the Land Office path: rwb-asset and rwb-integration, through their own contracts.
- The buy-back rental, the auto-debit and the arrears follow-up of FEAT-TRT-16: the sibling stories of this service and rwb-payment.
- The case status, the case table, the task of the inspector and the task of the approver: rwb-case, RWB-P3-E1018 and its contract; the status reaches this service on the case signal only.
- The `approval` record, the `ApprovalWorkflow` and the rule package registry: rwb-decision.
- The topic, its ACLs, the retry topics and the dead-letter topic: the event platform and the platform infrastructure stories.
- The deployment, the flag, the dashboards and the alerts of this build: this legacy key's DevOps story.
- The real cross-service proof against the live rwb-case, rwb-asset, rwb-document and rwb-integration: the wave 2 integration harness.
