# RWB-S3-E4017-APP Notify guarantors and co-borrowers

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E4-017 for rwb-guarantee (S3, Guarantee). The demand leaves the monolith's in-process call out of `recovery_svc` and becomes the notice branch of `GuaranteeClaimWorkflow`, the stage child that `CaseWorkflow` starts on task queue `rwb-guarantee` (DP-12); each demand is issued through the workflow kit's Notify template as an activity on the queue `rwb-comms`, which owns the approved template, the channel and the proof of delivery, because Architecture v5 slide 13 gives S3 no REST line to P6 and the Ownership Map gives S3 no event to publish (DP-09 in reverse, DP-11); the notice clock becomes a durable Temporal timer inside that workflow instead of a `timer` row; the local decision record is written in the same transaction as the notice outcome through RWB-PLT-E1027-CON (DP-03); the claim operations the officer and the notice use sit on base `/api/recovery/guarantee/v1` (DP-13); the ACE customer facts the legacy send read for the letter are not read here (DP-05); SCR-17 is reached through the gateway-bff composite route (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S3-E4017-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (25 resolved, 19 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S3-E4017-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-guarantee |
| Service epic | RWB-SVC-S3 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement (DOR-RWB-S3-E4017-APP-16) |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S3-F |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S3-E4017-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Contract version | Not specified in the source documents (DOR-RWB-S3-E4017-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S3 rwb-guarantee v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **case owner**, I want **the Workbench to send the demand to every guarantor and co-borrower on the case, from the approved template**, so that **no guarantee claim misses its deadline**.

This is the application slice of legacy RWB-E4-017. It owns:

- both legacy acceptance criteria of the story, copied verbatim with their origin tag, and the data rows, the messages and the rule they rest on — R-GUA-06 of the GUARANTEE set, which is the notice rule the routing workbook gives this feature;
- the notice branch of `GuaranteeClaimWorkflow` on task queue `rwb-guarantee` in namespace `rwb-recovery` — the stage child that rwb-case's `CaseWorkflow` starts for a guarantee claim, with the four steps of every stage: receive the signal, ask Drools, record and apply in one transaction, then wait (DP-12; Architecture v5 slide 13; Temporal and Drools Design slide 13);
- the demand itself: on `DEADLINE_TIMER_RUNNING` with `GUARANTOR_NOTICE_DUE`, when `guarantee_type` is a personal guarantor, a co-borrower or a corporate guarantor, R-GUA-06 issues the D6.6 guarantor notice from the approved template and the stage moves to `GUARANTOR_NOTICE` (Routing Logic v4 R-GUA-06; FSD S3 A2.5.2);
- the addressee set: every party on the case whose role is a guarantor or a co-borrower, taken from the case signal as party keys and never by reading `case_party` (DP-01; ASM-4525);
- the dispatch: one Notify activity per addressee on the queue `rwb-comms` through the workflow kit's Notify template, with the `GuarantorNotice` payload of RWB-S3-E4017-CON; rwb-comms selects the approved template for the product and the notice type, resolves the name and the address, issues the letter through WIN and keeps the document in the Document Hub, and answers accepted or refused; this service publishes no event because the Ownership Map gives S3 none (ASM-4524);
- the notice clock: the durable Temporal timer that runs the notice period by product from the instant the stage entered `DEADLINE_TIMER_RUNNING`, with the length read as a value in force (ASM-4526);
- the local decision record of the notice cycle — template, addressees, instant, rule id, rule version — written in the same transaction as the stage outcome through the library of RWB-PLT-E1027-CON, because `guarantee_claim` has no notice column (DP-03; GAP-2725);
- the stage outcome of R-GUA-06 reported to the parent `CaseWorkflow`, which moves the case status (ASM-4525; DP-01);
- the DP-05 boundary: no `v_ace_*` view is read for the addressee, because the customer facts of the legacy data table belong to rwb-comms' path and to rwb-source-data (ASM-4524).

It does not own: the `GuarantorNotice` element, the template rule, the activity input, the versioning rule and the fakes, which are RWB-S3-E4017-CON; the claim entity, its fields and the claim create and update operations, which are RWB-S3-E4013-APP and RWB-S3-E4013-CON; the claim deadline, the claim submission and the tracking states, which are RWB-S3-E4013-APP, RWB-S3-E4014-APP and RWB-S3-E4015-APP; the guarantor's answer, the negotiation and the refusal paths R-GUA-28 to R-GUA-32, which are RWB-S3-E4018-APP; the case, the party and the case clock, which are rwb-case's (DP-01); the template, the channel, the consent check and the proof of delivery, which are rwb-comms' (P6); the letter file WIN (INT-14), which is rwb-integration's (P2); the decision-record library, which is RWB-PLT-E1027-CON; SCR-17 and its composite route, which are the platform edge story and the screen owners (DP-19); and the real cross-service proof, which is the wave 3 integration harness.

### 2. Business rationale

The module is measured by one number, and the FSD states it twice: claims filed inside the deadline, 100 percent, read from the decision log and the Workbench records, reviewed monthly (FSD S3 A2.1.1 and A2.5.1). The problem the module exists to fix is stated in one line: guarantee and TCG claims are late because deadlines are not tracked (FSD S3 A1.3). The demand to the guarantors and the co-borrowers is the step that starts the clock the guarantor answers against, and the requirement is exact: guarantor and co-borrower notices are generated by rule and sent on the same path as customer notices (REQ-S3-004, FSD S3 "Requirements served").

Three facts of the legacy story move, and each one is a decoupling, not a rewrite. The first is the dispatch. The legacy send called the notification path from inside one deployable, and its integration points are recorded as "WIN, Workbench" with no contract and no channel (FSD S3 A2.5.2). Architecture v5 slide 13 gives S3 a Temporal line and an event subscription to rwb-comms and no REST line at all, and the Ownership Map gives S3 zero published events, so the target can only send the demand as a Temporal activity on the owner's queue; making it an event would mean inventing an event this service does not own (ASM-4524). The second is the addressee. The legacy data table lists `v_ace_customer` and `case_party` because the monolith filled the letter from them; in the target the 30 `recovery.v_ace_*` views are read only by rwb-source-data and `case_party` is rwb-case's, so the parties arrive as keys on the case signal and the name and the address are resolved where the letter is built (Architecture v5 slide 8; DP-01, DP-05; ASM-4525). The third is the clock. The legacy wait is a `timer` row; the target clock is a durable Temporal timer inside the stage workflow, and the catalogue retires `TimerDue` for exactly that reason (Architecture v5 slide 42, event 18; ASM-4526).

No business value moves. The template stays "the approved template", the notice period stays "notice period by product" as the routing workbook states it, and every message text is the legacy text carried unchanged (BR-S3-005; MSG-GEN-001, MSG-P4-002, MSG-P7-003). The one state the legacy story names for this step, `GUARANTOR_NOTICE`, is new vocabulary that SCR-17's five states do not carry; it is reported to the parent as an outcome and is not drawn on the screen by this story (GAP-2725).

### 3. Preconditions

- RWB-S3-E4017-CON is published: the `GuarantorNotice` element and its properties, the approved-template rule, the activity input on the queue `rwb-comms`, the notice-period key and the fakes are baselined and handed to this story.
- RWB-PLT-E1027-CON is published: `DecisionRecordWriter.record(DecisionRecord)` with `@Transactional(propagation = MANDATORY)`, the refusal MSG-P7-009, the failure MSG-P7-003, and the DDL template of `decision_record` applied by this service's own Flyway sequence in `rwb_guarantee` (DP-03, DP-15).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-17, one hop per call (DP-19).
- The per-service Flyway sequence of rwb-guarantee carries `guarantee_claim` with the eight fields of TSD S3 T3.1 (DF-TRT-015 to DF-TRT-022) and the seven standard columns of T3.0, and the `rwb_guarantee` login holds rights in that schema only (DP-01, DP-02).
- The GUARANTEE package is in force: `GuaranteeClaimWorkflow` exists for a case whose route decision opened a guarantee claim, the package and its version arrive with the case signal, and the embedded Drools runtime is the service template's capability, so this story adds no build dependency for it (ASM-4525).
- `GuaranteeClaimWorkflow` and the claim operations are RWB-S3-E4013-APP's and RWB-S3-E4013-CON's; until they are built the claim facts and the party keys arrive from their workflow-state fixture and no term is assumed.
- The notice period by product is a value in force; the routing workbook carries it in its service-level column only and no parameter key is defined for it (GAP-2725; ASM-4526).
- The party roles that make an addressee are read as reference data through rwb-case's reference-data contract, not as a constant list; the three values R-GUA-06 names are the rule's condition and are never a local literal (GAP-2725; ASM-4525).
- The outbox and inbox library, the workflow kit and the access guard are the service template's, and the capability area and the right are declared here and checked there (ASM-4525).
- No approval is needed to build against a Draft contract baseline; this story runs in Draft (realignment v1) until RWB-S3-E4017-CON is tagged.

### 4. Flow

1. rwb-case's `CaseWorkflow` starts `GuaranteeClaimWorkflow` as its child on task queue `rwb-guarantee` when the route decision on the case opens a guarantee claim; the parent forwards the case event to the running child as a signal and never calls the service directly (DP-12; Temporal and Drools Design slide 13, notes).
2. Step 1, receive: the workflow takes the case status, the claim facts of `guarantee_claim`, the party keys with their roles and the GUARANTEE package version from the signal. It reads no `recovery_case`, `case_party` or `timer` row (DP-01; ASM-4525).
3. The notice clock is armed when the stage reports that it has entered `DEADLINE_TIMER_RUNNING` — the move R-GUA-01 makes and RWB-S3-E4013-APP owns — with the notice period by product as its length. The clock is a durable Temporal timer, cancelled by any earlier stage end (ASM-4526; DP-10).
4. The clock fires `GUARANTOR_NOTICE_DUE`. Step 2, ask Drools: `EvaluateRules` runs the GUARANTEE package in force; R-GUA-06 fires on `DEADLINE_TIMER_RUNNING` when `guarantee_type` is a personal guarantor, a co-borrower or a corporate guarantor, and answers `GUARANTOR_NOTICE` — issue the D6.6 guarantor notice with proof of delivery (Routing Logic v4 R-GUA-06; TSD S3 T4).
5. `resolveAddressees` activity: the party keys of the signal are filtered by role into the addressee set — every guarantor and every co-borrower on the case, one entry per party — and nothing else is read. A case with no addressee in that set takes the rule's negative answer and does not enter the notice state (ASM-4524, ASM-4525).
6. `notifyGuarantor` activity, once per addressee, on the queue `rwb-comms` through the kit's Notify template: the payload is the `GuarantorNotice` of RWB-S3-E4017-CON — case reference, claim reference, party reference, party role, notice type, template code, claim deadline and notice due date. rwb-comms checks that the template is current for the product and the notice type, resolves the name and the address, issues the letter through WIN and keeps the document in the Document Hub, and answers accepted with its dispatch reference or refused with a reason code (RWB-S3-E4017-CON; ASM-4524).
7. `recordAndApply` activity, one transaction: the decision record is written through `DecisionRecordWriter.record(DecisionRecord)` with `MANDATORY` so it joins this transaction and opens none, carrying the rule id, the rule version, the template code, the addressee count and the dispatch references; no `guarantee_claim` row is changed, because the table has no column for the notice (DF-TRT-015 to DF-TRT-022; GAP-2725; DP-03).
8. The stage outcome of R-GUA-06 is reported to the parent, which moves the case to `GUARANTOR_NOTICE`; the workflow arms the notice-period timer that the guarantor's answer runs against, and the answer itself — R-GUA-28, R-GUA-29 and R-GUA-30 — is RWB-S3-E4018-APP's (ASM-4525).
9. A refused dispatch on one addressee does not roll back the others: the refusal is recorded with its reason code on the decision record, the remaining addressees are issued, and the officer sees the refused addressee named on SCR-17. A refused dispatch on every addressee leaves the stage in `DEADLINE_TIMER_RUNNING` and no notice-period timer is armed (ASM-4524).
10. Step 4, wait: the workflow waits on the next case signal or on the notice-period timer, and Continue-As-New keeps the run inside the platform's history limit (Temporal and Drools Design slide 13, History).
11. A repeat of the same notice cycle answers the first result: one activity per addressee, one decision record and one notice-period timer, never a second of each; the workflow ID and the `Idempotency-Key` of the claim operation carry the identity.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without the right U or C in capability area Treatment and offer calls the notice form of the claim | 403 before any read of the claim; the refusal is the guard library's and is logged by it | MSG-P4-002 | AC3, TC-E4-017-03, TC-E4-017-05 |
| X2 | A notice fact is incomplete: no addressee, no template code or no notice due date | The notice cycle is refused before any dispatch, with the field named; nothing changes | MSG-GEN-001 | AC4, TC-E4-017-01, TC-S3-E4017-CON-01, TC-E4-017-06 |
| X3 | The decision record cannot be written | The apply step rolls back, no dispatch is recorded, the notice-period timer is not armed and the user sees MSG-P7-003 | MSG-P7-003 | AC2, TC-E4-017-02, TC-E4-017-04 |
| X4 | A record field is refused by the library | Nothing changes and the field is named; no demand leaves | MSG-P7-009 | AC5, TC-S3-E4017-CON-04, TC-E4-017-07 |
| X5 | rwb-comms answers refused for one addressee — the template is not current, or the party cannot be reached | The refusal is recorded with its reason code, the other addressees are issued, and the refused addressee is named on SCR-17; no message identifier exists for this path in the source documents (GAP-2725) | Not specified in the source documents (GAP-2725; ASM-4524) | AC6, TC-S3-E4017-CON-03, TC-E4-017-08 |
| X6 | rwb-comms answers refused for every addressee | No notice-period timer is armed, the stage stays in `DEADLINE_TIMER_RUNNING` and the officer is told the state did not move | Not specified in the source documents (GAP-2725; ASM-4524) | AC7, TC-S3-E4017-CON-03, TC-E4-017-09 |
| X7 | A data product the notice rests on is stale after a late or failed ACE batch | The notice is held and the product and its date are named | MSG-P1-001 | AC8, TC-S3-E4017-CON-02, TC-E4-017-10 |
| X8 | The same notice cycle is retried, or a consumer redelivers the signal | One activity per addressee, one decision record and one timer: the workflow answers the first result | None | AC9, TC-E4-017-01, TC-E4-017-11 |

X1, X3 and X8 are the exception paths of RWB-E4-017 carried onto the split; X2, X4, X5, X6 and X7 are the paths that the published element, the `MANDATORY` record, the owner's answer and the FSD's stale-data rule add (GAP-2725; ASM-4524).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-S3-E4017-CON, RWB-PLT-E1027-CON and RWB-PLT-N001-CON with their fakes, on `guarantee_claim` in its own schema; needs no live rwb-case, no live rwb-comms and no live ACE to start |
| Negotiable | The activity names, the timer field names and the log fields are this story's choice; the rule, the `MANDATORY` record, the no-event rule and the no-personal-data rule are fixed |
| Valuable | Every guarantor and co-borrower on the case receives the demand from the approved template, and a notice date exists that the officer and the record can both prove |
| Estimable | One workflow branch, four activities, one controller method, one repository and one timer |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion runs on synthetic claims, party keys and case signals through the contract fakes, plus one component test of the dispatch and the access answer |

### 7. Acceptance criteria

```gherkin
Feature: Notify guarantors and co-borrowers

  Scenario: AC1 Notify guarantors and co-borrowers (legacy RWB-E4-017 AC1)
    Given the rwb-comms contract mock returns a notice accepted for every addressee
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then sends the demand to every guarantor and co-borrower on the case, from the approved template
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E4-017 AC2)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 Role without the right is refused (X1) (new, D-RCV-60)
    Given a role without the right U or C in capability area Treatment and offer
    When it calls the notice form of the claim
    Then the request is refused with 403 before any read of the claim
    Then the user sees MSG-P4-002

  Scenario: AC4 Incomplete notice fact is refused before dispatch (X2) (new, D-RCV-60)
    Given a notice cycle with no addressee, no template code or no notice due date
    When the notice cycle starts
    Then it is refused before any dispatch with the missing field named
    Then the user sees MSG-GEN-001 and nothing changes

  Scenario: AC5 Record field refused by the library (X4) (new, D-RCV-60)
    Given the record library refuses a field of the decision record
    When the notice outcome is applied
    Then nothing changes and the field is named
    Then no demand leaves and the refusal is logged with MSG-P7-009

  Scenario: AC6 Refused for one addressee (X5, BR4) (new, D-RCV-60)
    Given rwb-comms answers refused for one addressee because the template is not current or the party cannot be reached
    When the dispatch set completes
    Then the refusal is recorded with its reason code on the decision record
    Then the other addressees are issued
    Then the refused addressee is named on SCR-17

  Scenario: AC7 Refused for every addressee (X6) (new, D-RCV-60)
    Given rwb-comms answers refused for every addressee
    When the dispatch set completes
    Then no notice-period timer is armed
    Then the stage stays in DEADLINE_TIMER_RUNNING
    Then the officer is told the state did not move

  Scenario: AC8 Stale data product holds the notice (X7, BR11) (new, D-RCV-60)
    Given a data product the notice rests on is stale after a late or failed ACE batch
    When the notice cycle is run
    Then the notice is held
    Then the user sees MSG-P1-001 naming the product and its date

  Scenario: AC9 Retried cycle answers the first result (X8) (new, D-RCV-60)
    Given a notice cycle has already run for a case
    When the same cycle is retried or the signal is redelivered
    Then one activity per addressee, one decision record and one timer exist
    Then the workflow answers the first result

  Scenario: AC10 Rule fires and one dispatch per addressee (BR1, BR2) (new, D-RCV-60)
    Given the stage reports DEADLINE_TIMER_RUNNING with GUARANTOR_NOTICE_DUE
    And guarantee_type is a personal guarantor, a co-borrower or a corporate guarantor
    When R-GUA-06 fires
    Then one notice is dispatched per addressee on the queue rwb-comms
    Then the stage moves to GUARANTOR_NOTICE

  Scenario: AC11 No move without a qualifying type or addressee (BR1, BR3) (new, D-RCV-60)
    Given guarantee_type is not one of the three, or no addressee is found among the parties of the case signal
    When R-GUA-06 is evaluated
    Then the stage does not move and the answer is recorded
    Then only parties whose role is a guarantor or a co-borrower are addressees

  Scenario: AC12 Template is the current approved one (BR4) (new, D-RCV-60)
    Given the template code and the notice type are passed to rwb-comms
    When the notice is dispatched
    Then this service passes no wording, no name and no address
    Then rwb-comms checks that the template is current for the product and the notice type

  Scenario: AC13 Notice values come from the values in force (BR5) (new, D-RCV-60)
    Given the notice period by product, the notice type list, the party roles and the template code are in force
    When the notice cycle is built
    Then each value is read from the parameters, the rule package or the reference data
    Then no period, role list or template code appears as a literal

  Scenario: AC14 Notice clock is a durable timer (BR6) (new, D-RCV-60)
    Given the stage reports DEADLINE_TIMER_RUNNING
    When the notice clock is armed
    Then a durable Temporal timer is armed inside GuaranteeClaimWorkflow
    Then the timer is cancelled by any earlier stage end and no timer row is written

  Scenario: AC15 Notice recorded in one transaction (BR7, BR8) (new, D-RCV-60)
    Given the notice outcome is applied
    When the decision record is written
    Then the record holds the rule id, the rule version, the template code, the addressee count and the dispatch references
    Then the record is written in the same transaction as the stage outcome and no guarantee_claim column changes

  Scenario: AC16 Case status and events are not moved here (BR9, BR10) (new, D-RCV-60)
    Given the stage reports the outcome of R-GUA-06
    When the outcome is reported
    Then the outcome goes to the parent CaseWorkflow and the stage writes no case status
    Then no event for the demand is published on rwb.guarantee.events.v1

  Scenario: AC17 No personal value crosses the boundary (BR12) (new, D-RCV-60)
    Given a notice cycle runs for an addressee
    When the workflow input, the activity payload and the log are written
    Then they carry party references and codes only
    Then no name or address appears in them

  Scenario: AC18 Provided operation error answers (401, 403, 404) (new, D-RCV-60)
    Given a provided operation of the guarantee claim API is called
    When the call is refused
    Then the answer carries status 401, 403 or 404

  Scenario: AC19 Replay of a write with the same idempotency key answers the first result (new, D-RCV-60)
    Given a write to the claim carries an idempotency key already used
    When the same write is replayed with that key
    Then the first result is answered and no second write is made

  Scenario: AC20 Retried or timed-out activity follows the retry policy (new, D-RCV-60)
    Given an activity of the stage is retried or times out
    When the retry or the timeout occurs
    Then the retry follows the policy of section 12.5
    Then no retry is made on a refused record

  Scenario: AC21 Disallowed status change is refused (new, D-RCV-60)
    Given a status change the model does not allow is requested
    When the change is submitted
    Then it is refused and the stage does not move
```

**Target reading.** Every legacy line and every legacy value above is kept character for character except the decision-log wording, which becomes decision record (CG-ALL-8909), including the repeated `Then` of the legacy form; what changes is where it runs, who owns the fact and how it is reached. The trigger of AC1 is the `GUARANTOR_NOTICE_DUE` event of the stage's own durable clock, which fires R-GUA-06 on `DEADLINE_TIMER_RUNNING`; the addressees are the parties of the case signal whose role is a guarantor or a co-borrower, and "every" means one dispatch per addressee, so a case with three addressees produces three (ASM-4524, ASM-4525). "The approved template" is the template rwb-comms holds as current for the product and the notice type: this service passes the notice type and the template code and never the wording, the name or the address (BR4; GAP-2725). The demand leaves as a Notify activity on the queue `rwb-comms` through the workflow kit, because Architecture v5 slide 13 gives S3 a Temporal line to P6 and no REST line, and the Ownership Map gives S3 no event to publish; the `rwb-comms contract mock` line above stands for that activity's accepted answer in the test and not for a REST call (ASM-4524). The `timer` row of the legacy data table is replaced by the durable notice-period timer inside `GuaranteeClaimWorkflow`, armed in the same apply step that reports the state move, and the period is the value in force the routing workbook calls "notice period by product" (ASM-4526). The decision record of AC1 and AC2 is the local `decision_record` written through `DecisionRecordWriter.record(DecisionRecord)` with `@Transactional(propagation = MANDATORY)`, refusing with MSG-P7-009 and failing with MSG-P7-003; `decision_log_entry` is P7's central ledger and is neither written nor read here (DP-03, DP-01). The case move to `GUARANTOR_NOTICE` is reported to the parent `CaseWorkflow`, which applies it; the stage writes no case status (ASM-4525; DP-01).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | On `DEADLINE_TIMER_RUNNING` with `GUARANTOR_NOTICE_DUE`, when `guarantee_type` is a personal guarantor, a co-borrower or a corporate guarantor, the D6.6 guarantor notice is issued with proof of delivery and the stage moves to `GUARANTOR_NOTICE` | Routing Logic v4 R-GUA-06; TSD S3 T4 R-GUA-06; FSD S3 A2.5.2 |
| BR2 | The demand goes to every guarantor and every co-borrower on the case, one dispatch per party, from the approved template | FSD S3 A2.5.2; legacy RWB-E4-017 AC1 |
| BR3 | The addressees are the parties of the case signal whose role is a guarantor or a co-borrower; `case_party` is rwb-case's and is never read here | DP-01; ASM-4525 |
| BR4 | The template must be approved and current for the product and the notice type; this service passes the notice type and the template code, and rwb-comms holds the wording, the channel and the proof of delivery | FSD S3 A2.5.2; R-GUA-06; ASM-4524 |
| BR5 | A notice fact is never a constant: the notice period by product, the notice type list, the party roles and the template code are values in force read from the parameters, the rule package and the reference data | FSD S3 A2.5.3.1 BR-S3-005; ASM-4526 |
| BR6 | The notice clock is a durable Temporal timer inside `GuaranteeClaimWorkflow`, armed when the stage reports `DEADLINE_TIMER_RUNNING` and cancelled by any earlier stage end; no `timer` row and no Schedule | Architecture v5 slide 42 event 18; Temporal and Drools Design slide 13; ASM-4526 |
| BR7 | The notice cycle is recorded in the local `decision_record` in the same transaction as the stage outcome, with the rule id, the rule version, the template code, the addressee count and the dispatch references, or nothing is recorded and the officer is told the action was not taken | ADR-022; DP-03; FSD S3 A2.5.4.3 |
| BR8 | `guarantee_claim` carries no notice column: the notice date, the template and the dispatch references live on the decision record, and a correction becomes a new decision record | TSD S3 T3.1 DF-TRT-015 to DF-TRT-022; GAP-2725 |
| BR9 | The case status and the case-level clock are not rwb-guarantee's to move: the stage reports the outcome of R-GUA-06 to the parent `CaseWorkflow` | ASM-4525; DP-01 |
| BR10 | This service publishes no event for the demand: the dispatch is a Temporal activity on the queue `rwb-comms`, and `rwb.guarantee.events.v1` carries no notice event because the Ownership Map gives S3 none | Ownership Map; Architecture v5 slide 13; ASM-4524 |
| BR11 | A data product the notice rests on that is stale after a late or failed ACE batch holds the notice and names the product and its date | FSD S3 A2.5.3.1 VR-S3-005-1 |
| BR12 | Nothing that identifies a person crosses the workflow input, the activity payload or the log: the payload carries party references and codes only, and the name and the address are resolved by rwb-comms | Template and Rules §R7.2 s17; DP-09; ASM-4524 |

**Where each rule lives in the target.** BR1 and BR2 are the rule outcome and the loop over addressees: the GUARANTEE package decides the first, the stage iterates the second, and AC1 asserts the dispatch set. BR3 and BR12 are the boundary with the letter: the party key is the only handle this service holds. BR4 is why the wording of the demand is nowhere in this code. BR5 is why no period, no role list and no template code appears as a literal. BR6 replaces the `timer` row with the workflow's clock. BR7 and BR8 are the record rule and the reason the notice lives on the record rather than on the claim. BR9 is the boundary with rwb-case and BR10 is the decision not to invent an event. BR11 is the FSD's stale-data rule of this feature.

### 9. State transitions

The case status is rwb-case's (DP-01; ASM-4525). This story reports one outcome of the GUARANTEE set and changes the state of its own `GuaranteeClaimWorkflow` execution and of its durable notice clock.

| From | Rule and event | Condition | To (reported to the parent) |
|---|---|---|---|
| `DEADLINE_TIMER_RUNNING` | R-GUA-06, `GUARANTOR_NOTICE_DUE` | `guarantee_type` is a personal guarantor, a co-borrower or a corporate guarantor, and at least one addressee is found | `GUARANTOR_NOTICE`; one demand per addressee and the notice-period timer armed |
| `DEADLINE_TIMER_RUNNING` | R-GUA-06, `GUARANTOR_NOTICE_DUE` | `guarantee_type` is not one of the three, or no addressee is found | No move; the stage stays and the answer is recorded |
| `DEADLINE_TIMER_RUNNING` | R-GUA-06, `GUARANTOR_NOTICE_DUE` | Every dispatch is refused by the owner | No move; the refusals are recorded and the officer is told the state did not move |
| `GUARANTOR_NOTICE` | R-GUA-28, R-GUA-29, R-GUA-30 | The guarantor settles, refuses or disputes | Out of scope: RWB-S3-E4018-APP and the parent's move |

| Workflow state | Meaning |
|---|---|
| RUNNING, waiting on the case signal | The stage is open and the notice clock has not fired |
| RUNNING, waiting on the notice-period timer | The demands were issued and the guarantor's answer is awaited |
| COMPLETED | The stage ended: the claim was submitted, the notice path ended, or the case left the guarantee route |
| FAILED | The record write or the notice validation failed and the apply step rolled back |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Primary user of the claim and of the demand; rights C, R and U of capability area Treatment and offer and CRU in the module matrix (TSD S3 T6.1; FSD S3 A2.5.3.3) |
| RW-GUARANT, guarantee officer | Also uses the claim and the demand, rights C, R and U and CRU |
| RW-RESTRUCT, RW-SPECIAL | Use the claim and the demand, rights C, R and U; RW-RESTRUCT holds CRUA |
| RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE, SY-CASEWF, SY-RULES, SY-AGENT | Read only, right R |
| RW-PRODHEAD, RW-CREDCOMM | Read and approve, rights R and A; no approval is taken in this story |
| The recovery squad (RW-TRIBE) | Writes the workflow branch, the four activities, the controller method, the repository and the timer |
| rwb-case (P3) | Owns the case, the party, the case status and the case clock; answers the signal this stage receives |
| rwb-comms (P6) | Owns the approved template, the channel, the addressee resolution and the proof of delivery that turn the activity into the demand the guarantor receives |
| rwb-integration (P2) | Owns the WIN letter file (INT-14) the notice is sent through |
| rwb-document (P5) | Owns the document copy of the issued notice |
| rwb-decision (P7) | Owns the rule package registry and the rule versions |
| The platform workflow owner | Owns the `rwb-guarantee` task queue, the namespace and the worker registration |
| No delegation of authority level applies | The story issues a notice a rule already requires; it takes no credit and no settlement decision |

The access check is the platform guard library's and is declared here as the capability area and the right only (ASM-4525; TSD S3 T6.1). No credential and no personal name appears in the workflow input, the activity payloads or the logs, which carry case IDs, claim IDs, party references, codes and dates only.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-015 | guarantee_claim | id | Read |
| DF-TRT-016 | guarantee_claim | case_id | Read |
| DF-TRT-017 | guarantee_claim | claim_type | Read |
| DF-TRT-018 | guarantee_claim | claim_deadline | Read |
| DF-TRT-019 | guarantee_claim | claimed_amount | Read |
| DF-TRT-020 | guarantee_claim | filed_at | Read |
| DF-TRT-021 | guarantee_claim | paid_amount | Not used by the notice |
| DF-TRT-022 | guarantee_claim | status | Read |
| DF-DEC-001 to DF-DEC-018 | decision_record | the local record shape declared by RWB-PLT-E1027-CON, carrying the notice facts | Write |
| DF-CAS-001 to DF-CAS-023 | recovery_case | the case status, read from the case signal only | Read (from the signal) |
| DF-CAS-030 to DF-CAS-035 | case_party | the party reference and its role, read from the case signal only | Read (from the signal) |
| DF-WRK-027 to DF-WRK-036 | timer | Not used: the notice clock is a durable Temporal timer | Not read or written |
| DF-ACE-055 to DF-ACE-074 | v_ace_customer | Not used: the name and the address are resolved by rwb-comms, and no ACE view is read here | Not read or written |

The notice writes no business column, and that is deliberate: TSD S3 T3.1 gives `guarantee_claim` eight fields and none of them is a notice date, a template code, an addressee or a dispatch reference, so the notice cycle is recorded on the `decision_record` through the library and never by a repository of this story (GAP-2725; BR8; DP-03). `recovery_case`, `case_party` and `timer` are P3's: the case status and the parties arrive on the signal and the clock is Temporal's, so no row of those three tables is read or written (Ownership Map; ASM-4525). `v_ace_customer` is named in the legacy data table and is not read here: the 30 `recovery.v_ace_*` views are read only by rwb-source-data, and the addressee is the letter owner's concern (ASM-4524; DP-05). Field identifiers are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-guarantee (S3); base `/api/recovery/guarantee/v1` (DP-13). This story supplies the notice behaviour of the claim update operation and the `GuarantorNotice` payload that RWB-S3-E4017-CON declares; the operation, its envelope, its `GuaranteeClaim` response and its error set are declared by the service's guarantee-claim contract, RWB-S3-E4013-CON, and are named here, not redeclared.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| PATCH | `/guarantee-claims/{claimId}` (the notice form) | Request `GuarantorNotice` of RWB-S3-E4017-CON — `claimId`, `caseId`, `partyRef`, `partyRole`, `noticeType`, `templateCode` and the notice due date; response `GuaranteeClaim` of RWB-S3-E4013-CON; the operation, the envelope and the error set are RWB-S3-E4013-CON's | Treatment and offer, right U, scope applied | `Idempotency-Key` header |
| POST | `/cases/{caseId}/guarantee-claims` | `GuaranteeClaimRequest` of RWB-S3-E4013-CON; named only, because the notice branch opens no claim | Treatment and offer, right C, scope applied | `Idempotency-Key` header |

Both paths and both rights are the legacy story's endpoint table and permission table carried onto the split; the only change is the base, which is the service's own under DP-13 (GAP-2725; ASM-4527). The errors are 400 or 422 with MSG-GEN-001 and the field name, 403 with MSG-P4-002, 404, 409, 503, and MSG-P7-003 and MSG-P7-009 on the record path; the envelope texts are RWB-S3-E4013-CON's and are not restated here.

#### 12.2 REST operations consumed

None. This story calls no service over REST in its own name: the demand leaves as a Temporal activity on the queue `rwb-comms` (12.5), the case status and the parties arrive on the case signal the parent forwards, and the decision record is written in process inside this transaction and calls nothing (DP-03; ASM-4524, ASM-4525). The `rwb-comms contract mock` line of AC1 is the test-only stand-in for that activity's answer and adds no consumed operation, which is why the contract dependencies of this story are None.

#### 12.3 Events published

None. The Ownership Map gives S3 no published event, and no source names a notice event for `rwb.guarantee.events.v1`; the demand is therefore dispatched by a Temporal activity on the owner's queue and not by an event of this service, which is also why no consumer outside the workflow is created here (Ownership Map; Architecture v5 slide 13; ASM-4524). The local decision record is written in the same transaction as the stage outcome through the library, and the shared topic `rwb.decision-record.v1` is the library's, not an event of this story (DP-03).

#### 12.4 Events consumed

None. The guarantee claim's triggers reach the stage as signals forwarded by the parent `CaseWorkflow`, including the GUARANTEE package version in force, and the notice clock is the workflow's own durable timer. Architecture v5 slide 13 shows S3 listening to rwb-comms and rwb-payment events for the claim and the payment tracking paths — the proof of delivery and the claim payment — and those subscriptions belong to RWB-S3-E4015-APP and RWB-S3-E4018-APP, not to the notice cycle of this story (ASM-4524).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `GuaranteeClaimWorkflow` | Workflow, the stage child of `CaseWorkflow`, one execution per case and stage, with the four steps receive, evaluate, record and apply, wait | `rwb-guarantee` | Input: case ID, stage, claim ID, claim facts, party keys and roles, case status, rule package version; holds the addressee set, the template code, the dispatch references and the durable notice timer; output: the outcome of R-GUA-06 and the addressee count |
| `EvaluateRules` | Activity | `rwb-guarantee` | The GUARANTEE package and its version in force; the rule answer for `GUARANTOR_NOTICE_DUE` |
| `resolveAddressees` | Activity | `rwb-guarantee` | The party keys and their roles from the signal; the addressee set, one entry per party, and the empty answer with its reason |
| `notifyGuarantor` | Activity, invoked as the workflow kit's Notify template | `rwb-comms` | The `GuarantorNotice` payload of RWB-S3-E4017-CON; the accepted answer with its dispatch reference or the refused answer with its reason code |
| `recordAndApply` | Activity | `rwb-guarantee` | One transaction: the decision record through the library and the stage outcome reported to the parent; it writes no `guarantee_claim` column |
| Durable notice timer inside `GuaranteeClaimWorkflow` (not a separate workflow) | Timer | `rwb-guarantee` | The durable notice-period timer from the state entry to the notice due date, with the period in force |

The workflow is the stage child named by Architecture v5 slide 13 and the Temporal and Drools Design slide 13 for rwb-guarantee; the activity names are this story's design choice and are fixed by no source document (GAP-2725; ASM-4526). Workflow ID form and start rule: Not specified in the source documents (CG-ALL-8902); the catalog row gives only the start trigger, a guarantee found at takeover and the claim deadline timer starting (R-GUA-01). The `notifyGuarantor` activity is the kit's Notify template with no business term in its interface, and the business terms ride in the payload the owner's contract types (Temporal and Drools Design slide 12, L3 and L4; ASM-4524). The retry policy is the workflow kit's: 1 s initial interval, back-off 2, 10 attempts, and no retry on a refused record (Temporal and Drools Design slide 14).

#### 12.6 Schedules

None. The stage is started by the parent `CaseWorkflow` and advanced by signals and by its own durable timer; it owns no Temporal Schedule and no legacy Quartz job. The notice period is a durable timer and not a Schedule, which is why no schedule entry and no polling job exists for it (ASM-4526; DP-10).

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `guarantee_claim` | `rwb_guarantee` | S3 | Read only, with the eight fields of TSD S3 T3.1; the notice adds no column and changes no row |
| `decision_record` | `rwb_guarantee` | PLT, a library object | Written through `DecisionRecordWriter.record(...)` in the same transaction; the shape and the DDL template are RWB-PLT-E1027-CON's (DP-03) |
| `decision_log_entry` | `rwb_decision` | P7 | Never read and never written here; the central ledger is P7's (DP-01) |
| `timer`, `recovery_case`, `case_party` | `rwb_case` | P3 | Never read and never written here; the state move is the parent's, the parties arrive on the signal and the clock is Temporal's (ASM-4525) |

No table of another service is read and no foreign key crosses a schema (DP-01). The template, the issued letter, its addressee and its proof of delivery are rwb-comms' and rwb-document's and are not stored here; the notice cycle leaves the claim reference, the addressee count and the dispatch references behind, and nothing else (BR4, BR12).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-S3-E4017-CON notice fake | The `GuarantorNotice` element, the template rule and the notice-period key | A complete payload; a payload missing the addressee or the notice due date; a payload carrying a personal field, which is refused; an accepted answer with its dispatch reference; a refused answer with its reason code |
| RWB-PLT-E1027-CON decision-record fake | The record write | An accepted record with a chain sequence and an entry hash; a refusal with MSG-P7-009 and the field; a failure with MSG-P7-003; the absence of any row after a rollback |
| rwb-comms activity stub | The `notifyGuarantor` activity on the queue `rwb-comms` and the `rwb-comms contract mock` line of AC1 | One accepted answer per addressee; a refusal on one addressee of three; a refusal on all three; a redelivery of the same request identity |
| rwb-case case-signal mock | The case status, the party keys and their roles on the forwarded signal | A case with three addressees; a case whose parties hold no guarantor or co-borrower role; `DEADLINE_TIMER_RUNNING` as the status of AC1 |
| RWB-PLT-N001-CON route fake | The composite route of SCR-17 | The two hops of the claim screen, including the refused addressee line |

The notice and decision-record fakes are the published contracts of those two stories, the activity stub is test-only and stands for rwb-comms' side until the integration harness proves it live, and the route fake is the platform edge contract's (GAP-2725; ASM-4524).

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 operations on `/api/recovery/guarantee/v1`, both declared by RWB-S3-E4013-CON | None | OpenAPI 3.1; the controller validates and maps errors to problem responses |
| Kafka | None | None | This service publishes no event and subscribes to none for the notice cycle; the local record rides the library's topic (DP-03) |
| Temporal | None | `GuaranteeClaimWorkflow` with 4 activities and one durable timer on `rwb-guarantee`, of which `notifyGuarantor` runs on `rwb-comms` | Namespace `rwb-recovery`; one durable timer; no Schedule |
| File | None | None | The WIN letter file (INT-14) is rwb-integration's and rwb-comms' path; no file is read or written here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.guarantee`, modules `notice` and `claim`, with the published types in `...guarantee.api` (DP-13, DP-14). Service base `/api/recovery/guarantee/v1`, schema `rwb_guarantee`, topic `rwb.guarantee.events.v1`, task queue `rwb-guarantee` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views; this story reads none, because the addressee is resolved by rwb-comms | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule the notice is built on: the record and the stage outcome are one commit or none is. DP-05 is applied by removal: the legacy send read `v_ace_customer` in process, and in the target no ACE view is read by this service because the views belong to rwb-source-data and the letter belongs to rwb-comms (BR12; ASM-4524). DP-13 fixes the base of the two claim operations, and DP-19 is the route by which the officer reaches SCR-17. The in-process call of the legacy send is carried by DP-11's rule — one hop and a 2 s timeout — in its Temporal form, because Architecture v5 slide 13 makes the rwb-comms call a Temporal one and not REST (ASM-4524). The other patterns of the service — the owner schema, the workflow kit, the topic naming — are service-template capabilities and add no dependency of this story.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `GuaranteeClaimWorkflow` (notice branch) | Workflow | The four steps, the notice state, the addressee loop, the durable timer and the outcome report to the parent |
| `EvaluateRules` | Activity | Runs the GUARANTEE package in force and maps the `GUARANTOR_NOTICE_DUE` answer (BR1) |
| `resolveAddressees` | Activity | Filters the party keys by role into the addressee set (BR2, BR3) |
| `notifyGuarantor` | Activity | One Notify call per addressee on the queue `rwb-comms` with the `GuarantorNotice` payload (BR4) |
| `recordAndApply` | Activity | One transaction: the decision record and the stage outcome (BR7, BR8) |
| `GuaranteeClaimController` | Controller | The notice form of the claim update and the claim read, with the access right and the error map (12.1) |
| `GuaranteeClaimRepository` | Repository | Reads the claim facts in `rwb_guarantee` and writes no notice column (BR8) |
| `NoticeTimer` | Workflow timer | The durable notice-period clock from the state entry to the notice due date (BR6) |
| `Migrations` | Migration | The `guarantee_claim` table where the claim story leaves it to this one, and no notice column (DP-15) |

**Database.** `guarantee_claim` holds the eight fields of TSD S3 T3.1 and the seven standard columns of T3.0. No notice-date, template, addressee or dispatch-reference column exists, so the notice cycle is recorded on `decision_record`, which the library applies in `rwb_guarantee` through this service's own Flyway sequence (GAP-2725; BR8). There is no `timer` row for the clock, because the clock is a durable timer inside the workflow (ASM-4526).

**Configuration and reference data.** The notice period by product is a value in force — the routing workbook gives it as "Notice period by product" in the service-level column — and is read as a parameter and rule-package value, never as a constant (BR5; ASM-4526). The notice type, the party role and the template code lists are reference data read through rwb-case's contract; the template itself is rwb-comms' and is addressed by code. The capability area "Treatment and offer" and the rights C and U are the access rows of the platform guard library, not constants of this story.

**Build steps**

1. The Flyway version that carries `guarantee_claim` where the claim story leaves it to this one and the library's `decision_record`, with no notice column (GAP-2725; DP-15).
2. `GuaranteeClaimWorkflow`'s notice branch and its input record, registered on `rwb-guarantee`, with the four steps and the outcome report to the parent (BR9).
3. The `EvaluateRules` call with the GUARANTEE package version from the signal and the R-GUA-06 answer mapping (BR1).
4. `resolveAddressees` with the role filter and the empty answer (BR2, BR3).
5. `notifyGuarantor` with the `GuarantorNotice` payload, one call per addressee, and the accepted and refused answers (BR4, BR12).
6. `recordAndApply` with the `MANDATORY` record write and the stage outcome (AC1, AC2).
7. The durable notice timer, its arming on `DEADLINE_TIMER_RUNNING` and its cancellation on an earlier stage end (BR6).
8. The controller for the notice form of the claim update and the claim read, with the access right and the error map (12.1).
9. Tests for AC1 and AC2 against the fakes and the three-addressee fixture.

**Feature flag.** `rwb.guarantee.guarantor-notice`.

**Done when.** The tests in section 16 pass, `GuaranteeClaimWorkflow` starts for a synthetic guarantee case and reports R-GUA-06, one demand leaves per addressee through the activity stub with no personal value in the payload, one `decision_record` holds the template, the addressee count and the dispatch references in one commit, the notice timer is armed from the value in force, a forced record failure leaves nothing behind with MSG-P7-003, and SCR-17 shows the notice state and any refused addressee through the composite route in SIT, with its empty, loading, error and no access states (content: Not specified in the source documents (DOR-RWB-S3-E4017-APP-10)).

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A notice fact is missing or outside its type or domain | Enter {field}. |
| MSG-P4-002 | A role without the right in Treatment and offer calls the notice form of the claim | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | The record is refused for a missing or invalid field (log and incident, not the screen) | The decision record was refused: {field} is missing or not valid. |
| MSG-P1-001 | A data product the notice rests on is stale after a late or failed ACE batch | {product} is from {date}. Today's load has not arrived. |

The five texts are the legacy and FSD texts carried unchanged, except MSG-P1-001, which takes the Error and Message Standard v4 text: MSG-GEN-001, MSG-P4-002 and MSG-P7-003 are the legacy story's validation table, MSG-P1-001 is VR-S3-005-1 of the FSD, and MSG-P7-009 and MSG-P7-003 are the record library's (RWB-PLT-E1027-CON; FSD S3 A2.5.3.1). No message identifier is invented for the refused-dispatch path, which the source documents leave unnamed (GAP-2725). Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-17 Guarantee claim carries the five states the legacy story names — Not due; due; submitted; paid; refused — and shows the claim, the deadline and the checklist. The notice cycle adds a fact and no state to that screen: the officer sees that the demand was issued, to how many addressees, from which template code, and which addressee was refused, and the field list belongs to the screen owners and the platform edge story (DP-19; RWB-PLT-N001-CON). The state `GUARANTOR_NOTICE` that R-GUA-06 moves the stage to is not one of the screen's five and is not drawn by this story; the mapping of the stage vocabulary onto the screen states is not specified in the source documents (GAP-2725; ASM-4525). The empty, loading, error and no access states of SCR-17 are not specified in the source documents (CG-ALL-8910).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-017-01 | AC1 | End to end | Notify guarantors and co-borrowers |
| TC-E4-017-02 | AC2 | End to end | Not recorded |
| TC-E4-017-03 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E4-017-05 | AC3 | Component | A role without the right U or C is refused with 403 before any read |
| TC-E4-017-06 | AC4 | Component | An incomplete notice fact is refused before dispatch with MSG-GEN-001 |
| TC-E4-017-07 | AC5 | Component | A record field refused by the library changes nothing and sends no demand |
| TC-E4-017-08 | AC6 | Integration | One addressee refused: the others are issued and the refusal is recorded |
| TC-E4-017-09 | AC7 | Integration | Every addressee refused: no timer is armed and the stage stays in DEADLINE_TIMER_RUNNING |
| TC-E4-017-10 | AC8 | Component | A stale data product holds the notice and names the product and its date |
| TC-E4-017-11 | AC9 | Component | A retried notice cycle answers the first result |
| TC-E4-017-12 | AC10 | End to end | R-GUA-06 fires for each addressee and the stage moves to GUARANTOR_NOTICE |
| TC-E4-017-13 | AC11 | Component | No move without a qualifying type or addressee |
| TC-E4-017-14 | AC12 | Integration | The template code and notice type are passed and no wording is passed |
| TC-E4-017-15 | AC13 | Component | Notice values are read from parameters, the rule package and reference data |
| TC-E4-017-16 | AC14 | Component | The notice clock is a durable timer inside the workflow |
| TC-E4-017-17 | AC15 | Component | The decision record holds the notice facts in one commit |
| TC-E4-017-18 | AC16 | Component | The outcome goes to the parent and no demand event is published |
| TC-E4-017-19 | AC17 | Component | No personal value crosses the workflow input, payload or log |
| TC-E4-017-04 | Principle 5 | Component | A forced decision record write failure stops the action with MSG-P7-003 |
| TC-E4-017-24 | Section 12 contract | Component | Not specified in the source documents (DOR-RWB-S3-E4017-APP-12) |
| TC-E4-017-25 | Section 12.7 boundary (ASM-3438) | Component | Not specified in the source documents (DOR-RWB-S3-E4017-APP-12) |
| TC-E4-017-20 | AC18 | Component | Not specified in the source documents (NEWAC-RWB-S3-E4017-APP-AC11) |
| TC-E4-017-21 | AC19 | Component | Not specified in the source documents (NEWAC-RWB-S3-E4017-APP-AC12) |
| TC-E4-017-22 | AC20 | Component | Not specified in the source documents (NEWAC-RWB-S3-E4017-APP-AC13) |
| TC-E4-017-23 | AC21 | Component | Not specified in the source documents (NEWAC-RWB-S3-E4017-APP-AC14) |

The four legacy test case IDs, their Covers and their Data are kept in order and character for character. The legacy level "System" maps to "End to end" for the two criteria and to "Component" for the Access and Principle 5 cases, as in the other stories of this run. Where the legacy Covers names `Access`, the criterion is the published answer of the platform guard library on the claim update; where it names `Principle 5`, the criterion is the `MANDATORY` record write of RWB-PLT-E1027-CON rolling the apply step back. The notice fake, the decision-record fake, the rwb-comms activity stub, the case-signal mock and the route fake of section 12.8 stand behind every case. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 3 integration harness and are not listed here.

### 17. Guardrails

- No business value in code: the notice period by product, the notice due date, the template code and the party roles are values in force read from the parameters, the rule package and the reference data, never constants (BR5).
- No personal data in logs, workflow inputs, activity payloads or the fixture: the payload carries party references, codes and dates, and the name and the address are resolved by rwb-comms (BR12; Template and Rules §R7.2 s17).
- No read of another service's table: the case status and the parties arrive on the forwarded signal, and `recovery_case`, `case_party` and `timer` are never named in SQL (DP-01; BR3).
- No read of an ACE view and no copied customer fact: `v_ace_customer` is retired from this path and the views stay with rwb-source-data (DP-05; BR12).
- No event invented: `rwb.guarantee.events.v1` carries no notice event, because the service owns none, and the dispatch is the kit's Notify activity on the queue `rwb-comms` (BR10; ASM-4524).
- The decision record is written in the same transaction as the stage outcome, with `MANDATORY`; a forced failure leaves nothing behind and shows MSG-P7-003 (DP-03; BR7).
- The notice clock is a durable timer inside `GuaranteeClaimWorkflow`: no `timer` row, no polling job and no Schedule (BR6).
- One demand per addressee per notice cycle: a retry answers the first result and never sends the same demand twice (BR2; ASM-4524).
- An applied migration is never edited: a correction to the claim table or to the record link is a new version on the service sequence (DP-15).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S3-004 | Guarantor and co-borrower notices are generated by rule and sent on the same path as customer notices | Program BRD; Epic 4 BRD v1 (this run) | FEAT-GUA-05 | D6.5, D6.6 | R-GUA-06 | TC-E4-017-01, TC-E4-017-03 |
| REQ-S3-001 | A guarantee claim is prepared from case data and submitted inside the guarantor's deadline | Program BRD; Epic 4 BRD v1 (this run) | FEAT-GUA-05 | D6.5, D6.6 | R-GUA-06 | TC-E4-017-01, TC-E4-017-02 |
| REQ-S3-002 | Claim status, payment and any shortfall are recorded on the case | Program BRD; Epic 4 BRD v1 (this run) | FEAT-GUA-05 | D6.5, D6.6 | R-GUA-06 | TC-E4-017-04 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S3-E4017-CON | Contract | H: declares the `GuarantorNotice` element, the template rule, the activity input, the notice-period key and the fakes |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library and its `MANDATORY` transaction rule |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route of SCR-17 |
| RWB-S3-E4013-APP, RWB-S3-E4013-CON | App development, Contract | The claim entity, its fields and the create and update operations this story's paths belong to |
| RWB-S3-E4014-APP, RWB-S3-E4015-APP | App development | The claim submission, the tracking states and the proof-of-delivery read of the same feature family |
| RWB-S3-E4018-APP | App development | R-GUA-28 to R-GUA-32, the guarantor's answer and the negotiation that follows this notice |
| rwb-case (P3) | App development | The `CaseWorkflow` parent, the case status, the party and the case clock |
| rwb-comms (P6) | App development | The approved template, the channel, the addressee resolution and the proof of delivery |
| rwb-integration (P2), rwb-document (P5) | App development | The WIN letter file (INT-14) and the document copy of the issued notice |
| The wave 3 integration harness | Integration | I: the cross-service proof of the same legacy key against the live owners |

**Open decisions.** Open decision DL10 is still open and applies to this story. It is a business decision, so this story does not close it. Its assumptions are ASM-2250, ASM-2357, ASM-2377 and ASM-2863, each confirmed.

### 19. Out of scope

- The `GuarantorNotice` element, the template rule, the activity input, the versioning rule and the fakes: RWB-S3-E4017-CON.
- The claim entity, its other fields and the claim create and update operations: RWB-S3-E4013-APP and RWB-S3-E4013-CON.
- The claim preparation, the TCG submission and the claim tracking states: RWB-S3-E4013-APP, RWB-S3-E4014-APP and RWB-S3-E4015-APP.
- The guarantor's answer, the negotiation, the refusal and the dispute paths R-GUA-28 to R-GUA-32: RWB-S3-E4018-APP.
- The approved template, its wording, the consented channel, the addressee resolution and the proof of delivery: rwb-comms (P6).
- The WIN letter file (INT-14) and the document copy of the notice: rwb-integration (P2) and rwb-document (P5), through their own contracts.
- The case, the party, the case status, the case clock and every row of `recovery_case`, `case_party` and `timer`: rwb-case (P3).
- The decision-record library, its DDL template and the central ledger: RWB-PLT-E1027-CON and P7 rwb-decision.
- SCR-17, its field list and the gateway-bff composite route: the platform edge story and the screen owners (DP-19).
- The real cross-service proof of the demand, the template answer and the letter: the wave 3 integration harness.
