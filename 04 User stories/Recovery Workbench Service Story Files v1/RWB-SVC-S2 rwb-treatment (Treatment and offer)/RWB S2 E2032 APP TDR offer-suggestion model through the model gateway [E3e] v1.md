# RWB-S2-E2032-APP TDR offer-suggestion model through the model gateway [E3e]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-032 for rwb-treatment (S2). This is the treatment-side slice of the legacy key: the stage asks the agent-run operation of `RWB-P10-E2032-CON` for a TDR offer suggestion through one REST hop on `/api/recovery/treatment/v1` (DP-11, DP-13), waits at most 60 s and falls back to the rule result of the `RESTRUCTURE` package in force, stores the answer on the treatment row as a proposal with the model, prompt and policy version it came from, and writes its local decision record in the same transaction through the RWB-PLT-E1027-CON library with the outbox row (DP-03, DP-09). The model, the prompt, the guardrails, the run and the evaluation stay with P10 rwb-agent; SCR-15 is reached through the gateway-bff composite route (DP-19). The legacy acceptance criteria AC1 to AC8 belong to `RWB-P10-E2032-APP`; this story writes eight criteria of its own. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E2032-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-032 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP11, DP13, DP19 |
| Parallel lane | L-S2-K |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P10-E2032-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to REQ-CHO-006, REQ-DRI-001) |
| Status | Draft (realignment v1) |

### 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **`TreatmentWorkflow` of rwb-treatment to ask the agent-run operation of `RWB-P10-E2032-CON` for a TDR offer suggestion for the case facts it already holds, to store the answer on the treatment row as a proposal with the model, the prompt and the policy version it came from, to fall back to the rule result of the `RESTRUCTURE` package in force when the agent is slow or unavailable, and to record the suggestion and every officer override in the local decision record in the same transaction**, so that **the treatment record holds what was suggested next to what the officer offered, and every suggestion can be explained afterwards by the model and prompt version that produced it**.

This is the treatment-side slice of legacy RWB-E2-032. It owns:

- the use of the suggestion on the treatment side: the `suggestTdrOffer` activity of `TreatmentWorkflow`, the child of `CaseWorkflow` on task queue `rwb-treatment` in namespace `rwb-recovery`, which asks the suggestion operation for the facts of the treatment it is running and waits at most 60 s for the answer (Architecture v5 slides 16 and 18; Temporal and Drools Design slides 12 and 13);
- the proposal on the `treatment` row of `rwb_treatment`: the suggested terms, the model code and version, the prompt version, the policy version, the agent run id, the decision record id and the confidence, written as a proposal and never as an approved amount (DF-TRT-001, DF-TRT-002, DF-TRT-004, DF-TRT-007, DF-TRT-009);
- the fallback to the rule result of the `RESTRUCTURE` package in force when the answer does not arrive inside the wait, when the answer carries no suggestion, or when the agent refuses the call (R-UNI-32);
- the local decision record of every suggestion and of every officer override, written through the RWB-PLT-E1027-CON library inside the caller's transaction, with the rule ID and the package version on the fallback, hash-linked and published on `rwb.decision-record.v1` (DP-03), together with the outbox row (DP-09);
- the parameter value of the suggestion wait and the reference-data lists LOV-PROPOSER and LOV-TREATMENT read at their version (DP-06, DP-07);
- one REST operation on base `/api/recovery/treatment/v1` that returns the proposal of a treatment (DP-13), reached by SCR-15 through the gateway-bff composite route (DP-19);
- the boundary: ACE facts only through the owner's contract or the `v_ace_*` views (DP-05), and no table of another service read or joined (DP-01).

It does not own: the model, the prompt, the guardrails, the run, the evaluation and the human-feedback record, which are P10 rwb-agent's (`RWB-P10-E2032-APP` and the contract `RWB-P10-E2032-CON`); the rule packages, their rows and their versions, which are P7 rwb-decision's; the settlement offer, the below-floor approval and the TDR plan, which are `RWB-S2-E3002-APP`, `RWB-S2-E3003-APP` and `RWB-S2-E3004-APP`; the case status, `CaseWorkflow` and the case table, which are rwb-case's (P3); the roles, rights and scope data, which are rwb-access's (P4); the gateway-bff composite route and the layout, which are the platform edge story's.

### 2. Business rationale

The legacy story put a suggestion on the treatment record through an interface inside the monolith: `ModelSuggestionClient.suggestOffer` returned an `OfferSuggestion` record, the decision log was written by the in-process `DecisionLogWriter`, the agent run was a table of the same `recovery` schema, and the P3 treatment service called all of it in one process. Its business objective is unchanged and is the one that matters here: the restructuring officer builds each restructure offer by hand from the balance, the arrears and the payment history, and a recorded suggestion next to the officer's offer lets the case be explained afterwards — what was recommended, by which model, at which policy version, and what the officer did with it (REQ-CHO-006, REQ-DRI-001).

What D-RCV-60 changes is where the answer comes from and who owns it. The suggestion is no longer produced by a component of the treatment module: it is a run of rwb-agent, reached by one REST operation on `/api/recovery/agent/v1` with one hop and a client budget (DP-11, DP-13; Architecture v5 slide 16; ADR-020), and the run, the prompt, the guardrail and the evaluation are rows of `rwb_agent` (Architecture v5 slide 41). The treatment service therefore holds a proposal and not a model: it sends the facts it owns, stores the answer it receives, and never reaches the Enterprise AI endpoint itself. That single ruling is what keeps one gateway, one prompt store and one model inventory in the platform, and it is why nothing in section 11 of this story is an `agent_run` write.

The second change is the fallback. The design gives every stage the same safety: an agent that is slow or unavailable does not stop the case, because after 60 seconds the rule result is used and the decision record says so (Architecture v5 slide 16; Temporal and Drools Design slide 27; R-UNI-32). Here the rule result is the answer of the `RESTRUCTURE` package version in force, which this stage already evaluates for its own steps, so the officer sees a proposal either way: the model's, or the rule's, and the record names which one.

The third change is the material action. The suggestion is advice, and the target keeps the officer's decision where the legacy put it: the officer builds and submits the offer, and the approval of an offer below the floor or outside the band is the approval story's (legacy BR7; FSD S2 A2.3 and A2.4). The architecture note on agent risk is explicit — a human decides every material action, and the prompts, the outputs and the model versions are logged (Architecture v5 slide 44) — so this story writes a proposal, a flag and a record, and it never writes an approved amount, an offer state or a booking.

Serves REQ-CHO-006 and REQ-DRI-001: a treatment record holds what was suggested next to what was offered, and the decision carries the model, the agent and the prompt version that produced it. No business value is invented or moved: the model code, the version, the policy version, the mode, the review date, the terms and the messages are the values the legacy story, the FSD and the design already carry, read in force.

### 3. Preconditions

- `RWB-P10-E2032-CON` is published: the suggestion operation on base `/api/recovery/agent/v1`, whose path below the base is Not specified in the source documents (GAP-0634; ASM-0977), its eight answer members `agentRunId`, `decisionLogEntryId`, `modelCode`, `modelVersion`, `installments`, `monthlyAmountThb`, `interestRate` and `confidence`, its request members case ID, treatment ID and the idempotency key `TDR_OFFER:<treatmentId>`, its refusals 200 with no suggestion and MSG-P10-007, 503 with MSG-P7-003 and 409 for a repeat that returns the stored answer, its one hop with the 2 s client budget of DP-11, and the rwb-agent fake. This story builds against that contract and its fake and never against `rwb_agent`.
- The platform libraries are in place as the wave 0 service-template capability: the decision-record writer of RWB-PLT-E1027-CON with `DecisionRecordWriter.record(DecisionRecord)` declared `@Transactional(propagation = MANDATORY)`, the outbox and inbox library of RWB-PLT-TE006-CON, the parameters client of RWB-PLT-E1042-CON, the reference-data client of RWB-PLT-E1043-CON and the composite route of RWB-PLT-N001-CON (ASM-3098).
- The `rwb_treatment` schema and login exist from the platform database story, and this service's Flyway sequence is at the version that carries the library tables; this story adds the proposal columns of the `treatment` row on the same sequence and never edits an applied migration (DP-15).
- The workflow kit is in place on task queue `rwb-treatment` in namespace `rwb-recovery`, and `CaseWorkflow` of rwb-case starts this stage as a child on that queue with parent close policy ABANDON (Temporal and Drools Design slide 13).
- The `RESTRUCTURE` package is in force for the business date, announced by rwb-decision on `rwb.decision.RulePackageInForce.v1`, and the embedded Drools runtime of the service template evaluates it; the package, its rows and its version stay rwb-decision's and this story stores no rule text (DP-04 capability of the template; ASM-3098).
- The parameter value of the suggestion wait and the lists LOV-PROPOSER with AGENT, RULE and PERSON, and LOV-TREATMENT with its eleven values, are in force and are read as data with their version; neither the 60 seconds nor any member of either list is written in code (BR-S2-001; TSD S2 T3.2).
- Treatment "T-1001" of case "RW-2026-001001" is open in state Draft, opened by `RWB-S2-E3001-APP`, and its treatment type is RESTRUCTURE (legacy sections 3 and 4).
- No approval is needed to build against a Draft contract baseline, and an APP story with only contract dependencies starts on Day 1 with the C dependency of RWB-P10-E2032-CON never blocking (§R5.7).

### 4. Flow

1. `TreatmentWorkflow` is running on queue `rwb-treatment` for case "RW-2026-001001" with treatment "T-1001" open and in state Draft, having reached the offer step of the restructure route.
2. The workflow reads the `RESTRUCTURE` package version in force from the package signal and the parameter value of the suggestion wait from the parameters contract, and confirms that the treatment type of the row is RESTRUCTURE before it asks anything: on any other type the step makes no call (legacy BR6, AC8 of `RWB-P10-E2032-APP`).
3. `suggestTdrOffer` activity builds the request from the facts the stage holds: the case ID, the treatment ID, the route, the band and the plan terms as identifiers and amounts, the idempotency key `TDR_OFFER:T-1001`, the model code and the output schema `tdr-offer-v1` as the contract declares them. No name, no account number, no address and no document text leaves the service (section 17; ASM-3097).
4. The activity calls the suggestion operation of `RWB-P10-E2032-CON` once, with one hop and the 2 s client budget of DP-11 (ASM-3095).
5. The workflow waits at most 60 s for the answer and records the waiting period as a durable timer, so a worker restart does not lose the wait (R-UNI-32; Architecture v5 slide 16; ASM-3096).
6. On an answer that carries a suggestion, the activity builds the proposal from the eight members of the contract: the terms as identifiers and amounts, the model code and version, the confidence, the agent run id and the decision record id.
7. `recordSuggestion` activity writes, in one `rwb_treatment` transaction: the proposal on the `treatment` row of "T-1001" with the model version, the prompt version, the policy version and the run id it came from, the local `decision_record` row through `DecisionRecordWriter.record` with decision "D5", final call "SUGGESTION_RECORDED", the suggestion as the recommendation and the facts it was asked with as the inputs reference, the outbox row and the idempotency row of the key.
8. On a wait of 60 s without an answer, on an answer of 200 with no suggestion and MSG-P10-007, or on a refusal of 503 with MSG-P7-003, the activity takes the rule result of the `RESTRUCTURE` package version in force, records it as the proposal with the rule ID and the package version in place of the model version, sets the fallback fact on the proposal and on the decision record, and the stage continues on its next step (R-UNI-32; MSG-P10-007).
9. The activity returns the proposal and the decision record id to the stage; the stage reports the target state of the rule that its offer step takes — AWAITING_CREDIT_APPROVAL when the suggested terms fall outside the band, as R-RES-10 does — to the parent `CaseWorkflow`, which moves the case status. This service writes no case table (DP-01).
10. The officer reads the proposal on SCR-15 through the gateway-bff composite route, which composes the case read of rwb-case, the treatment read of this service and the proposal read of 12.1 in one hop each (DP-19).
11. When the officer overrides the suggestion, the override is written by the offer story of this service, and this story writes the second decision record that names the proposal it overrode — the agent run id, the model version and the suggested terms — in its inputs and marks the first proposal overridden, in one transaction with the same outbox row rule.
12. A repeated request with the same key `TDR_OFFER:T-1001` is answered with the stored suggestion or the stored proposal, writes no second proposal, no second record and no second outbox row, and makes no second model call (R-UNI-40; 409 of the contract).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The answer does not arrive inside the 60 s wait | The rule result of the `RESTRUCTURE` package in force is used, the fallback fact is recorded on the proposal and on the decision record, and the stage continues (R-UNI-32) | MSG-P10-007 | AC2 |
| X2 | The answer is 200 with no suggestion because the model is not in service | No model terms are stored; the rule result is used as X1 and SCR-15 shows the same message | MSG-P10-007 | AC2, AC6 |
| X3 | The agent refuses with 503 because the decision record could not be written on its side | No proposal is written, the treatment row and its state are unchanged, and the activity fails to the workflow, which retries it on the platform policy — 1 s initial interval, back-off 2, 10 attempts | MSG-P7-003 | AC6 |
| X4 | The 2 s client budget of the one hop is exceeded | The call is abandoned at the caller, no proposal is written from it, and the wait of X1 runs to its end and falls back to the rule result (DP-11) | MSG-P10-007 | AC2 |
| X5 | The local decision record cannot be written | The transaction rolls back: no proposal, no outbox row, no idempotency row; the user sees MSG-P7-003 and the call is retried with the same key | MSG-P7-003 | AC1, section 17 |
| X6 | The same key arrives twice | The first proposal is returned, the repeat is counted, and no second model call is made (R-UNI-40) | None | AC5 |
| X7 | The treatment type is not RESTRUCTURE | No call, no proposal and no record; the step moves on with the offer as today | None | AC1 |
| X8 | No `RESTRUCTURE` version is in force for the business date | No call is made and no proposal is written; the stage ends with the package refusal it received and the case keeps its status | MSG-P7-003 | Section 12.4 |
| X9 | A role without Treatment and offer R asks for the proposal | 403 with the guard library's answer, and the service log records the role and the operation, never a personal field | MSG-P4-002 | AC6, section 10 |
| X10 | A class, a statement or a test reaches an `rwb_agent`, `rwb_decision` or `rwb_case` table or a `v_ace_*` view directly | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17 |

X1 to X3 are the fallback and refusal paths of the legacy story carried onto the split; X4 is the client budget of DP-11, which the one hop adds; X5 and X6 are the record and repeat rules of the legacy (R-UNI-39, R-UNI-40); X7 and X8 are the type guard and the package refusal the workflow model adds; X9 is the guard's answer; X10 is the schema boundary. A refusal under X9 writes nothing at all, because the guard runs before the transaction opens.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against the RWB-P10-E2032-CON fake, the record-writer fake, the parameters and reference-data fakes and the composite-route fake; needs no live rwb-agent, no model and no Enterprise AI endpoint |
| Negotiable | The activity and operation names of this slice, the column names of the proposal and the shape of the override record are this story's choice; the terms, the versions, the lists, the rights and the messages are fixed |
| Valuable | The officer sees a recorded suggestion next to the offer, the record says which model and prompt produced it, and a slow agent never stops the case |
| Estimable | One activity pair, one proposal on one row, one read operation, one library adapter, one migration and one panel behind a route |
| Small | Fits two weeks with its tests, as a secondary slice of the legacy key |
| Testable | Each of the eight criteria of section 7 is one automated test; the agent, the package, the writer and the route are stubbed |

### 7. Acceptance criteria

```gherkin
Feature: TDR offer-suggestion model through the model gateway — the rwb-treatment use

  Background:
    Given restructure treatment "T-1001" is open on case "RW-2026-001001" in state Draft
    Given the account has principal outstanding 1,250,000.00 baht and 120 days past due
    Given the RESTRUCTURE package in force is the version rwb-decision announces on rwb.decision.RulePackageInForce.v1

  Scenario: AC1 A suggestion is stored as a proposal with its versions and nothing is approved (new, D-RCV-60)
    Given the rwb-agent contract mock returns for treatment "T-1001" a suggestion with model code "TDR_OFFER", model version "TDR-OFFER-1.0", 84 installments of 18,900.00 baht, an agentRunId, a decisionLogEntryId and a confidence, under policy "TDR_OFFER" version "P2" in mode "L1"
    When "suggestTdrOffer" asks for the suggestion for treatment "T-1001" with the key "TDR_OFFER:T-1001"
    Then treatment "T-1001" holds one proposal carrying the 84 installments of 18,900.00 baht, model code "TDR_OFFER", model version "TDR-OFFER-1.0", policy version "P2", the prompt version whose source is Not specified in the source documents (GAP-1882; ASM-3094) and the agent run id of the answer
    Then DF-TRT-007 offer_amount stays empty, the treatment state stays Draft and no amount is approved by this write
    Then one decision record with decision "D5", final call "SUGGESTION_RECORDED" and the suggestion as its recommendation is written with the proposal in one transaction, and its outbox row is written with them

  Scenario: AC2 The 60 s wait ends and the rule result is used (new, D-RCV-60)
    Given the rwb-agent contract mock does not answer inside the 60 s wait, the model staying silent for 61 seconds
    And the RESTRUCTURE package in force holds the row that answers the plan terms for a restructure treatment
    When "suggestTdrOffer" waits for 60 s and receives no suggestion
    Then the proposal records the terms of the rule result with the row ID and the package version in force, and records that the suggestion was not available
    Then MSG-P10-007 is shown for treatment "T-1001" and no model term is stored
    Then the stage continues on its next step and reports RESUME_STATE, the target state of R-UNI-32, while the treatment state stays Draft

  Scenario: AC3 A suggestion outside the band is flagged and routed to approval (new, D-RCV-60)
    Given the rwb-agent contract mock returns for treatment "T-1001" a suggestion of 84 installments of 18,900.00 baht with model version "TDR-OFFER-1.0"
    And the RESTRUCTURE package in force answers that the suggested terms fall outside the band the plan may move within, the band itself being Not specified in the source documents (GAP-1882; ASM-3094)
    When "suggestTdrOffer" stores the proposal on treatment "T-1001"
    Then the proposal is flagged outside the band and the stage takes the R-RES-10 branch of its offer step, reporting AWAITING_CREDIT_APPROVAL to its parent
    Then DF-TRT-007 offer_amount stays empty, no offer leaves the Workbench and the approval itself stays with RWB-S2-E3003-APP

  Scenario: AC4 An officer override is recorded with the suggestion it overrode (new, D-RCV-60)
    Given treatment "T-1001" holds a proposal from a suggestion with model version "TDR-OFFER-1.0" and an agent run id
    When the restructuring officer (RW-RESTRUCT) overrides the suggestion with the plan terms the officer enters
    Then a second decision record carries the proposal it overrode — the agent run id, the model version "TDR-OFFER-1.0" and the suggested terms — in its inputs and the officer's terms as its recommendation
    Then the first proposal is marked overridden, treatment "T-1001" holds one live proposal, and the offer terms themselves are written by RWB-S2-E3002-APP and RWB-S2-E3004-APP

  Scenario: AC5 The same key asked twice writes once (new, D-RCV-60)
    Given treatment "T-1001" holds a proposal from a suggestion asked with the key "TDR_OFFER:T-1001"
    When "suggestTdrOffer" asks again for treatment "T-1001" with the key "TDR_OFFER:T-1001" and the rwb-agent contract mock answers 409 with the stored suggestion
    Then the stored proposal is returned and no second proposal, no second decision record and no second outbox row is written
    Then no model call is made for the repeat and the repeat is counted

  Scenario: AC6 A refusal leaves the treatment unchanged and the workflow retries (new, D-RCV-60)
    Given the rwb-agent contract mock refuses the suggestion for treatment "T-1001" with status 503 and MSG-P7-003
    When "suggestTdrOffer" asks for the suggestion
    Then treatment "T-1001" keeps no proposal, its state stays Draft, DF-TRT-007 stays empty and no decision record is written here
    Then the activity fails to the workflow with the refusal and the workflow retries it on the platform policy, 1 s initial interval with back-off 2 and 10 attempts
    Then a role without Treatment and offer R asking for the proposal is refused with 403 and MSG-P4-002 and nothing changes

  Scenario: AC7 No personal data in the request, the answer, the event or the log (new, D-RCV-60)
    Given the facts this service sends are the case ID "RW-2026-001001", the treatment ID "T-1001", the route, the band and the plan terms as identifiers and amounts
    When "suggestTdrOffer" asks for the suggestion and stores the proposal
    Then the request, the answer, the proposal, the decision record and the outbox row carry no name, no account number, no national identifier, no address and no document text
    Then the case ID and the treatment ID are the only identifiers they carry, and a synthetic name placed in the case facts appears in no request field, no response field, no record, no event payload and no log line

  Scenario: AC8 The proposal shows on SCR-15 through the composite route (new, D-RCV-60)
    Given the gateway-bff composite route serves SCR-15 Settlement offer for case "RW-2026-001001" from the case read of rwb-case, the treatment read of this service and the proposal read, one hop each
    Given treatment "T-1001" holds a proposal of 84 installments of 18,900.00 baht with model version "TDR-OFFER-1.0" and policy version "P2"
    When the restructuring officer (RW-RESTRUCT) opens SCR-15
    Then SCR-15 shows the proposal with its model code, model version, policy version and the suggested terms, marked as a proposal and not as an approved offer
    Then SCR-15 shows MSG-P10-007 when no proposal is available, and the officer edits the offer fields as before
    Then no screen calls this service directly and the browser reaches it only through gateway-bff
```

The eight criteria are new under D-RCV-60 and test only the treatment-side deliverable of this story: the proposal on the `treatment` row, the 60 s wait and its fallback to the rule result, the out-of-band flag, the override record, the write-once key, the refusal path, the personal-data boundary and the screen read. The eight legacy criteria AC1 to AC8 of RWB-E2-032 — the exposure of the model, the mode OFF path, the logged record, the timeout, the schema failure, the unrecorded decision, the repeated request and the non-restructure type — belong to `RWB-P10-E2032-APP`, are written there word for word with their origin tags, and are not restated here (ASM-3094). The shape of the operation, its eight answer members, its refusal codes and its fake are `RWB-P10-E2032-CON`'s; the cross-service proof of the suggestion across rwb-treatment and rwb-agent is the wave 2 integration harness's and no criterion of this story claims it.

Three readings of the sources are stated here rather than hidden in the code. The treatment side of the suggestion is not described by any source — the legacy story describes the agent side end to end and the TSD gives `treatment` no column for a suggestion, a model version or a prompt version — so the proposal, its columns and its values are this story's design and are carried as a gap with its assumption (GAP-1882; ASM-3094). The one hop carries the 2 s client budget of DP-11 while the agent call keeps the policy timeout of 60 seconds, and no source reconciles the two waits, so both are declared and either breach falls back to the rule result (ASM-3095, ASM-3096; GAP-0634). The band the suggested terms are tested against is a row value of the `RESTRUCTURE` package and is not restated as a number here (GAP-1882; ASM-3094). The conflict between the operation list of Architecture v5 slide 16 and the in-process client of the legacy section 12 is carried as `GAP-1883`.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The model is reached only through the agent-run operation of `RWB-P10-E2032-CON`; this service embeds no model client, calls no Enterprise AI endpoint and reads no `rwb_agent` row | Legacy RWB-E2-032 BR1; DP-11; Architecture v5 slides 16 and 41 (GAP-1883) |
| BR2 | The suggestion is asked only for a treatment whose type is RESTRUCTURE; any other type makes no call and returns no proposal | Legacy RWB-E2-032 BR6; DF-TRT-004; TSD S2 T3.2 |
| BR3 | The proposal is advice: it never writes the approved amount, the offer terms, the offer state or a booking; the officer builds and submits the offer and decides it | Legacy RWB-E2-032 BR7; Architecture v5 slide 44 agent-risk note; FSD S2 A2.3 and A2.4 |
| BR4 | A suggestion is kept only with the model code, the model version, the prompt version and the policy version that produced it; a proposal without them is not written | REQ-DRI-001; legacy RWB-E2-032 AC3 (GAP-1882; ASM-3094) |
| BR5 | A model answer that is not there inside the wait, an answer that carries no suggestion or a refusal gives the rule result of the `RESTRUCTURE` package version in force, recorded with the fallback fact, and the stage continues | Legacy RWB-E2-032 BR4; R-UNI-32; Architecture v5 slide 16; Temporal and Drools Design slide 27 |
| BR6 | The suggestion and every override are recorded before they are returned: the proposal, the local decision record and the outbox row are one transaction, and a failed record rolls the call back with MSG-P7-003 | Legacy RWB-E2-032 BR3; R-UNI-39; DP-03 |
| BR7 | One proposal per treatment per key `TDR_OFFER:<treatmentId>`: a repeat returns the stored answer and writes nothing | Legacy RWB-E2-032 BR5; R-UNI-40 |
| BR8 | The case status stays rwb-case's and the treatment state stays this service's own `state` column: the stage reports the target state of the rule it took and the parent moves the case | ASM-3062; DP-01 |
| BR9 | No value a business person may change is written in code: the band, the wait, the model code and version, the prompt version, the policy version and the lists are values in force read with their version | BR-S2-001; BR-S2-004; TSD S2 T3.2 (DP-06, DP-07) |
| BR10 | A role reads the proposal only with Treatment and offer R, and the right is declared and not re-implemented: the check is the platform guard library's | TSD S2 T6.1; DP-08 as a template capability (ASM-3098) |
| BR11 | ACE data is never read here: the facts of the request are the treatment's own and, were an ACE fact needed, it would come through the contract of rwb-source-data or a `v_ace_*` view granted to this schema | DP-05; Architecture v5 slide 41; `ownership.json` |
| R-UNI-32 | The agent or the model does not answer inside the timeout of 60 seconds: fall back to the rule result and continue, and record the fallback on the decision | Business Rules and Routing Logic v4 (R-UNI-32); Temporal and Drools Design slide 27 |
| R-UNI-39 | The decision cannot be written: block the action and raise an incident, and no action proceeds unlogged | Business Rules and Routing Logic v4 (R-UNI-39); legacy RWB-E2-032 BR3 |
| R-UNI-40 | The same event arrives twice with the same key: ignore the second and record the idempotency hit | Business Rules and Routing Logic v4 (R-UNI-40); legacy RWB-E2-032 BR5 |
| R-RES-10 | A case in WITH_FCR_OFFICER with OFFER_PREPARED and `offer outside the range or deviation_flag = Y` routes the offer to credit approval; its target state is AWAITING_CREDIT_APPROVAL | TSD S2 T4; FSD S2 A2.4; BR3 |

**Where each rule lives in the target.** BR1 and BR2 are the `suggestTdrOffer` activity and the contract's request. BR3 is the absence of any write to DF-TRT-007, DF-TRT-009 and the treatment `state` in this story's components, asserted by a build check and by AC1. BR4 and BR5 are the proposal builder and the fallback branch of the activity. BR6 is `recordSuggestion` and the library. BR7 is the idempotency key and the inbox. BR8 is the stage outcome and the parent workflow. BR9 is the parameters and reference-data reads and the package read. BR10 is the contract's `security` section and the guard. BR11 is the schema grant and the boundary test. R-UNI-32 is the 60 s wait and the rule branch. R-UNI-39 is the rollback of X5. R-UNI-40 is the 409 path of AC5. R-RES-10 is the target state the stage reports when the proposal is outside the band.

### 9. State transitions

None of the rows below is a case status or the `treatment.state` of this service. The case status is moved by the parent `CaseWorkflow` on rwb-case from the outcome the stage reports (ASM-3062; DP-01), and `treatment.state` stays Draft through this story, because a suggestion approves nothing and books nothing.

| From (proposal state on the treatment row) | Event | Condition | Reported target state |
|---|---|---|---|
| none | SUGGESTION_RECEIVED | The answer carries a suggestion inside the band | None reported; the offer step stays with the officer |
| none | SUGGESTION_RECEIVED | The answer carries a suggestion outside the band | AWAITING_CREDIT_APPROVAL, the target of R-RES-10 |
| none | AGENT_SLOW or AGENT_REFUSED | No answer inside the 60 s wait, no suggestion, or a refusal | RESUME_STATE, the target of R-UNI-32 |
| SUGGESTED | OFFICER_OVERRIDE | The officer enters different plan terms | None reported; the second record names the proposal it overrode |
| SUGGESTED, OVERRIDDEN | REPEAT_REQUEST | The same key `TDR_OFFER:<treatmentId>` asks again | None; the stored proposal is returned |

The proposal has its own lifecycle in the proposal columns of the `treatment` row — proposed, overridden, replaced by the rule result — and their names are this story's design, Not specified in the source documents (GAP-1882; ASM-3094). The stage execution itself is RUNNING, COMPLETED or FAILED in the workflow history, and a failed execution is retried on the platform policy, 1 s initial interval with back-off 2 and 10 attempts, with a package refusal non-retryable.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The rwb-treatment squad, service identity of `rwb_treatment` | Runs the activity, writes the proposal, the decision record and the outbox rows, calls the agent contract |
| RW-RESTRUCT, restructuring officer (CRUA) | Reads the proposal on SCR-15, overrides it, builds and submits the offer; the primary role of the story |
| RW-CASEOWN, case owner (CRU) | Reads the proposal on SCR-15 for cases in scope |
| RW-SPECIAL, hardship and vulnerability specialist (CRU) | Reads the proposal on cases in scope |
| RW-TEAMMGR, team manager (R); RW-PRODHEAD, product head (RA); RW-CREDCOMM, credit approval committee member (RA) | Read the proposal; the approval of an offer outside the band is RWB-S2-E3003-APP's |
| The other reading roles of TSD S2 T6.1 — RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-GUARANT, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE (R) | Read the treatment and its proposal on cases in scope |
| SY-CASEWF, SY-RULES, SY-AGENT (R) | Read as service identities through the same checks |
| rwb-agent (P10) | Owns the operation, the model, the prompt, the guardrail, the run, the evaluation and the human-feedback record; answers the one hop |
| rwb-decision (P7) | Owns the `RESTRUCTURE` package, its rows and its version, and publishes `RulePackageInForce` |
| rwb-access (P4) | Owns the rights, the roles and the scope data the guard library answers with |
| No delegation of authority level applies | The story proposes; it approves nothing and books nothing |

No credential and no personal name appears in the request, the row, the record, the workflow input or the logs. Where a person must be identified the row carries a user identifier, never a name, and the masking of the personal fields of the case is the platform edge's.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Read: the treatment the proposal belongs to |
| DF-TRT-002 | treatment | case_id | Read: carried as the case ID of the request |
| DF-TRT-003 | treatment | decision_log_id | Not rewritten here: the record ID of the open stays, and the proposal carries its own record ID with the proposal |
| DF-TRT-004 | treatment | treatment_type | Read: the model is asked only when the value is RESTRUCTURE (BR2) |
| DF-TRT-005 | treatment | proposed_by | Not rewritten here: `RWB-S2-E3001-APP` writes it at open, and the proposer of the proposal is carried with the proposal from LOV-PROPOSER |
| DF-TRT-006 | treatment | proposed_at | Not rewritten here: the business time of the proposal is carried with the proposal |
| DF-TRT-007 | treatment | offer_amount | Read, never written here: it stays empty until `RWB-S2-E3002-APP` writes the offer |
| DF-TRT-009 | treatment | installments | Read, never written here: the suggested count is a proposal value and the plan count is `RWB-S2-E3004-APP`'s |
| DF-TRT-031 | treatment | installment_amount | Not written here: the plan story writes the count that becomes the plan |
| DF-TRT-032 | treatment | installments_paid | Not written here: the open writes zero and the plan story carries it |
| DF-DEC-001 to DF-DEC-018 | decision_record (local, in `rwb_treatment`) | all fields through `DecisionRecordWriter.record` | Write, in the same transaction (DP-03) |
| The proposal columns of the `treatment` row | treatment | the suggested terms as identifiers and amounts, the model code, the model version, the prompt version, the policy version, the agent run id, the decision record id, the confidence, the out-of-band flag and the proposal state | Write: names and types Not specified in the source documents (GAP-1882; ASM-3094) |
| DF-AGT-004, DF-AGT-005, DF-AGT-036, DF-AGT-040, DF-AGT-049, DF-AGT-058 | agent_policy, agent_run (`rwb_agent`, owner P10) | the model code, the model version, the run ID and the record ID of the suggestion | Not read and not written here: they arrive as the eight answer members of `RWB-P10-E2032-CON` (`agentRunId`, `modelCode`, `modelVersion`, `decisionLogEntryId`) and are stored on the proposal |
| DF-ACC-009, DF-ACE-020, DF-ACE-018, DF-ACE-025, DF-ACE-045, DF-ACE-046 | v_ace_account, v_ace_payment (`rwb_source_data`, owner P1) | the balance, the arrears and the payments of the legacy inputs | Not read here: the masked inputs snapshot is assembled by P10 rwb-agent behind its own contract (DP-05), and this service sends the facts of the treatment only |
| DF-CAS-001 to DF-CAS-023 | recovery_case (`rwb_case`, owner P3) | the case and its status | Not read and not written: the status arrives as the case signal the parent forwards |

`treatment` is the only table this story touches, and it adds no table: it adds the proposal columns of section 13 to the row `RWB-S2-E3001-APP` created, and writes the `decision_record` through the library in the same schema. The eight answer members are the only P10 identifiers this story sees, they arrive on the contract's answer, and no `agent_policy`, `agent_run`, `agent_prompt` or `agent_evaluation` row is read or written (DP-01; Architecture v5 slide 41; `ownership.json`). No foreign key crosses a schema and no row of another service's table is joined.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). This story supplies one read of the proposal; the treatment create and read of `RWB-S2-E3001-CON` and the offer operations of `RWB-S2-E3002-CON` and `RWB-S2-E3004-CON` are unchanged by it.

| Method | Path | Request and response | Access | Idempotency |
|---|---|---|---|---|
| GET | Below the base, the segment of the proposal read Not specified in the source documents (GAP-1882; ASM-3094) | `Treatment` id in the path, the proposal out: the suggested terms, the model code, the model version, the prompt version, the policy version, the agent run id, the decision record id, the confidence, the out-of-band flag and the proposal state, or the fallback fact and its rule ID and package version | Treatment and offer R, scope applied, through the guard library | Not applicable |

The errors are 401, 403, 404 and 503 with the RFC 9457 problem body; 403 carries MSG-P4-002 and 404 carries MSG-P4-003. The proposal read declares no offer body, no approval envelope and no plan body: those belong to the sibling contracts of this epic.

#### 12.2 REST operations consumed

| Method | Operation | Owner | Use |
|---|---|---|---|
| POST | The suggestion operation of `RWB-P10-E2032-CON`, path below `/api/recovery/agent/v1` Not specified in the source documents (GAP-0634; ASM-0977) | P10 rwb-agent | One suggestion for one treatment, answered with the eight legacy members; refusals 200 with no suggestion and MSG-P10-007, 503 with MSG-P7-003, 409 for a repeat |
| GET | The parameters read of the RWB-P3-E1042-CON contract, operation Not specified in the source documents (GAP-1882; ASM-3094) | P3 rwb-case | The suggestion wait in force, whose value the design fixes at 60 seconds (R-UNI-32) |
| GET | The reference-data read of the RWB-P3-E1043-CON contract, operation Not specified in the source documents (GAP-1882; ASM-3094) | P3 rwb-case | LOV-PROPOSER and LOV-TREATMENT at their version in force |

Every call is one hop with the 2 s client budget of DP-11 (ADR-020). The agent call is the one hop of this story that may take the agent's policy timeout of 60 seconds, and the exception is recorded with its assumption (ASM-3095, ASM-3096; ASM-0978). The model itself is reached only by rwb-agent, on the Enterprise AI private endpoint, and this service holds no external call (X section 19).

#### 12.3 Events published

The topic of the service is `rwb.treatment.events.v1` with event names `rwb.treatment.<Event>.v1` (DP-14); `TreatmentApproved` and `TreatmentClosed` belong to `RWB-S2-E3003-APP` and `RWB-S2-E3004-APP`, and this story publishes neither. The only event of this story is the one the library writes inside the transaction: `DecisionRecorded` on `rwb.decision-record.v1`, once per proposal and once per override, with no personal data in its payload (DP-03, DP-09; Architecture v5 slides 20 and 42).

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` (EV-30) | `rwb.decision.events.v1` | P7 rwb-decision | Announces the `RESTRUCTURE` package version in force; the stage stamps it on the fallback record and reads the band from it |
| CaseEvent (EV-29), the case signal | no topic: the case router and the parent `CaseWorkflow` of rwb-case | P3 rwb-case | Carries the route and the case facts the stage evaluates; forwarded by the parent |

`rwb.agent.AgentRunCompleted.v1` (EV-28) is not consumed here: its consumers are rwb-decision, rwb-document and rwb-deviation (Architecture v5 slide 43), and the suggestion answer already carries the run ID, the model version and the record ID this story stores. The package event is consumed through the inbox of the outbox library, so a redelivery starts no second swap; the case signal is a Temporal signal forwarded by the parent and is not a Kafka subscription of this service.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow` | Workflow, the stage child of `CaseWorkflow`, one execution per case and stage | `rwb-treatment` in namespace `rwb-recovery` | The offer step takes the suggestion as its input and reports the target state of section 9 |
| `suggestTdrOffer` | Activity | `rwb-treatment` | Input: case ID, treatment ID, the treatment type, the route, the band, the plan terms and the key `TDR_OFFER:<treatmentId>`; output: the proposal or the fallback result, with the decision record ID; one REST hop and one 60 s wait |
| `recordSuggestion` | Activity | `rwb-treatment` | One transaction: the proposal on the treatment row, the local decision record, the outbox row and the idempotency row (the `RecordAndApply` shape of the design) |

The activity names outside the design's `TreatmentWorkflow` are this story's design and are fixed by no source document (GAP-1882; ASM-3094). The package evaluation of the fallback is the embedded Drools runtime's, inside `suggestTdrOffer`, and adds no activity of its own.

#### 12.6 Schedules

None. The suggestion is request-driven, the stage is started by the parent `CaseWorkflow`, and the Arch v5 job map names no job for an agent suggestion (Architecture v5 slide 44). The 60 s wait is a durable timer inside the workflow execution, not a Schedule.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | Adds the proposal columns of section 13 to the row of `RWB-S2-E3001-APP` and writes them; DF-TRT-001, DF-TRT-002 and DF-TRT-004 are read |
| `decision_record` | `rwb_treatment` | PLT library object applied in this schema | Written through `DecisionRecordWriter.record` in the caller's transaction; the central `decision_log_entry` is P7's and is never touched |
| outbox, inbox, idempotency | `rwb_treatment` | PLT library objects | The service template's and not restated here (ASM-3098) |

No `agent_run`, `agent_policy`, `agent_prompt`, `agent_evaluation`, `rule_package`, `rule_row` or `recovery_case` table is created, read or joined (DP-01, `ownership.json`).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P10-E2032-CON agent fake | The suggestion operation of 12.2 | A suggestion with the eight members and model version "TDR-OFFER-1.0"; a 200 with no suggestion and MSG-P10-007; a 503 with MSG-P7-003; a 409 returning the stored suggestion; a silent stub for 61 seconds |
| RWB-PLT-E1027-CON writer fake | `DecisionRecordWriter.record` | An accepted record with chain sequence and entry hash; a refusal with MSG-P7-009; an unavailable store raising MSG-P7-003 |
| RWB-PLT-E1042-CON and RWB-PLT-E1043-CON fakes | The parameters and reference-data reads | The suggestion wait of 60 seconds; LOV-PROPOSER with AGENT, RULE and PERSON; LOV-TREATMENT with its eleven values |
| RWB-PLT-N001-CON composite-route fake | SCR-15 | The composed case read, treatment read and proposal read in one hop each |
| RESTRUCTURE package fixture | The fallback | Version in force with the row that answers the plan terms and the band, and a case whose type is SETTLEMENT for the type guard |
| RWB-S2-E3001-CON treatment fake | The treatment row of the stage | Treatment "T-1001" open in state Draft on case "RW-2026-001001" |

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 1 operation on `/api/recovery/treatment/v1` | 3 operations (agent suggestion, parameters, reference data) | OpenAPI 3.1; one hop each, 2 s client budget; browser traffic through gateway-bff (DP-19) |
| Kafka | 1 event through the library (`DecisionRecorded`) | 1 event (`rwb.decision.RulePackageInForce.v1`) | Own topic `rwb.treatment.events.v1` used by the sibling stories; inbox dedupe by cloud event id |
| Temporal | None | `TreatmentWorkflow` and 2 activities on `rwb-treatment` | Namespace `rwb-recovery`; one child per case; one 60 s durable timer; no Schedule |
| File | None | None | No file is read or written |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, modules `stage` and `treatment`, with the published types in `...treatment.api`. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>`, "recovery schema" | Owner's schema `rwb_treatment`; the proposal is a column set of the service's own `treatment` row and no `rwb_agent`, `rwb_decision` or `rwb_case` table is read | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library in `rwb_treatment` and the shared topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | ACE facts only through the owner's contract or the service's own ACE views; this story sends the treatment's own facts and reads no ACE view | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library, for the suggestion wait in force | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case, for LOV-PROPOSER and LOV-TREATMENT | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; the owner's topic and CloudEvents; the record's event leaves through the outbox row | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout, replacing `ModelSuggestionClient.suggestOffer` | none (C from the legacy dependency: RWB-P10-E2032-CON) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/treatment/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route for SCR-15 | H RWB-PLT-N001-CON |

DP-11 is the pattern the story is built on: the in-process `ModelSuggestionClient.suggestOffer` of the legacy becomes one operation of another service, faked on Day 1, and the treatment side never embeds the agent. DP-03 and DP-09 are the record and its event in one transaction; DP-01 and DP-05 are the two boundaries that keep another service's data out; DP-06 and DP-07 are the two reads that keep the wait and the lists out of code; DP-13 is the base and DP-19 the only route the screen uses. The platform contracts that the table names — RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON and RWB-PLT-N001-CON — are the wave 0 service-template capability here, which is why the story carries no H build dependency and only the C dependency of the key; the default is recorded (ASM-3098). The embedded Drools runtime and the package read are the template's and add no dependency of their own.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `TreatmentWorkflow` | Workflow | Runs the offer step, calls `suggestTdrOffer` with its facts, waits at most 60 s, takes the rule branch, reports the target state of section 9 to the parent |
| `suggestTdrOffer` | Activity | Builds the request, makes the one hop, maps the eight members, runs the fallback, calls the record activity |
| `recordSuggestion` | Activity | One transaction: the proposal columns, the decision record, the outbox row and the idempotency row |
| `TdrProposalBuilder` | Service | Maps the eight answer members to the proposal, keeps the model, prompt and policy versions, and refuses a proposal without them (BR4) |
| `TdrFallbackResolver` | Service | Takes the rule result of the `RESTRUCTURE` package in force, with the row ID and the package version, and sets the fallback fact |
| `OfferSuggestionController` | Controller | The proposal read of 12.1, the problem body and the guard |
| `ProposalRepository` | Repository | Reads and writes the proposal columns of `treatment` in `rwb_treatment` only |
| `DecisionRecordAdapter` | Library adapter | Calls `DecisionRecordWriter.record` with decision "D5", final call "SUGGESTION_RECORDED", the suggestion and the facts it was asked with (DP-03) |
| `Migrations` | Migration | The proposal columns and their constraints on the per-service Flyway sequence (DP-15) |

**Database.** The proposal columns are added to `treatment` in `rwb_treatment` on the service's own sequence, on the primary key `id`, with the standard columns of TSD S2 T3.0 unchanged — `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`. The suggested count is an integer and the suggested monthly amount a numeric(18,2), matching the physical types TSD S2 T3.1 gives DF-TRT-009 and DF-TRT-031; the confidence is a numeric whose precision is Not specified in the source documents (GAP-1882; ASM-3094); the agent run id and the decision record id are cross references with no foreign key into another schema; the model code, the model version, the prompt version, the policy version and the proposal state are bounded text. No column of another service's table is copied and no foreign key crosses a schema (DP-01).

**Configuration and reference data.** The suggestion wait is the parameter value in force, whose value the design fixes at 60 seconds (R-UNI-32; Architecture v5 slide 16); LOV-PROPOSER and LOV-TREATMENT are values in force read with their version and no member is a constant (BR-S2-001; BR9). The `RESTRUCTURE` package, its band and its rows are rwb-decision's and arrive on `RulePackageInForce`; the story stores no rule text and no band number. The model code "TDR_OFFER", the model version "TDR-OFFER-1.0", the policy version "P2", the mode "L1" and the review date 2027-02-28 are rows of `agent_policy` on P10's side and reach this story only through the answer and the contract; none of them is a constant of this service. The right and the capability area are rwb-access data, and the story declares the right only.

**Build steps**

1. The Flyway version with the proposal columns, their constraints and the migration test against the treatment DDL template (AC1).
2. `OfferSuggestionController` and `ProposalRepository` for the proposal read, with the problem body and the guard (AC8).
3. `TdrProposalBuilder` and `DecisionRecordAdapter`, with the version guard of BR4 and the rollback path of X5 (AC1, AC4).
4. `suggestTdrOffer` against the agent fake: the happy path, the 409 repeat, the 503 refusal and the 61-second silent stub (AC1, AC5, AC6).
5. `TdrFallbackResolver` and the 60 s durable timer, with the rule branch and the `RESUME_STATE` outcome (AC2).
6. The band test and the out-of-band flag, with the `AWAITING_CREDIT_APPROVAL` report of R-RES-10 (AC3).
7. The override record and the marking of the first proposal, against the offer story's patch path (AC4).
8. The property test of AC7 over the request, the answer, the record, the event payload and the logs; the boundary test of section 17.
9. The SCR-15 panel through the composite-route fake, with the fallback message (AC8).

**Feature flag.** `rwb.treatment.tdr-suggestion`. Off: the offer step makes no call, writes no proposal and continues as today.

**Done when.** The tests of section 16 pass, the RWB-P10-E2032-CON contract tests stay green, a synthetic suggestion stores one proposal with its model, prompt and policy version and writes its record in the same transaction in SIT, a silent agent falls back to the rule result of the package in force and the stage continues, a repeated key writes nothing, a forced record failure leaves no proposal and no outbox row, and SCR-15 shows the proposal through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-007 | No suggestion: the model is not in service, the call timed out, the gateway answered an error or the schema check failed | No offer suggestion is available for this treatment. The TDR model is not in service. |
| MSG-P7-003 | The decision record cannot be written, here or on the agent side | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | The record is refused for a missing or invalid field | The decision record was refused: {field} is missing or not valid. |
| MSG-P4-002 | A role without the right for the operation | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The treatment named does not exist in scope | The record was not found or is not in your scope. |
| MSG-GEN-001 | A required field of the request is missing | Enter {field}. |

MSG-P10-007, MSG-P7-003 and MSG-P4-002 are the three legacy texts carried unchanged. MSG-P10-007 is the agent contract's answer and is shown on SCR-15 as it arrives; MSG-P7-003 and MSG-P7-009 are the library's and are declared by RWB-PLT-E1027-CON; MSG-P4-002 and MSG-P4-003 are the guard's; MSG-GEN-001 is used for a missing field before the transaction opens. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | States | What this story puts on it |
|---|---|---|
| SCR-15 Settlement offer | Draft; below floor; approved; sent; accepted | The proposal with its model code, model version, prompt version, policy version and suggested terms, marked as a proposal; the out-of-band flag; MSG-P10-007 when no proposal is available |
| SCR-14 Treatment record | Draft; submitted; approved; booked; broken | Read only: the treatment and its state, as `RWB-S2-E3001-APP` serves them; this story puts no suggestion area on it |

Both screens are served by the gateway-bff composite route, which composes the case read of rwb-case, the treatment read and the proposal read of this service in one hop each, read only (DP-19); the browser calls no owner service directly. The legacy story placed the suggestion area on SCR-14, and the FSD S2 screen list gives SCR-15 the offer range, the floor and the gap to the floor, so the proposal is shown on SCR-15 and SCR-14 stays read only; that placement is this story's default and is recorded with its assumption (ASM-3099). The screen field list, the composite route specification and the layout belong to the platform edge story and the screen owners, and this story fixes the service side of the answer only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-032-09 | Access | Component | RW-RESTRUCT calls the admin run read through the agent contract; refused with MSG-P4-002 |
| TC-E2-032-01 | AC1, BR1, BR3 | End to end | Treatment T-1001, stub answer 84 installments of 18,900.00 baht |
| TC-E2-032-02 | AC2, BR2 | End to end | Policy TDR_OFFER P1 mode OFF, review date 2027-02-28 |
| TC-E2-032-03 | AC3 | End to end | Suggestion recorded on T-1001 |
| TC-E2-032-04 | AC4, BR4 | End to end | Stub silent for 61 seconds |
| TC-E2-032-05 | AC5, BR4 | End to end | Answer with installments -12 |
| TC-E2-032-06 | AC6, BR3 | End to end | Decision log writer fails |
| TC-E2-032-07 | AC7, BR5 | End to end | Second request for T-1001 |
| TC-E2-032-08 | AC8, BR6 | End to end | Treatment T-1002 of type SETTLEMENT |
| TC-E2-032-10 | Principle 5 | Component | Decision log write forced to fail after the model answers; no suggestion; MSG-P7-003 |
| TC-S2-E2032-APP-01 | AC1, AC4 | Component | The proposal with its model, prompt and policy version, the empty DF-TRT-007 and the override record that names the suggestion it overrode |
| TC-S2-E2032-APP-02 | AC2, AC3 | Component | The 60 s wait with the rule result of the RESTRUCTURE package in force, and the out-of-band flag that reports AWAITING_CREDIT_APPROVAL |
| TC-S2-E2032-APP-03 | AC5, AC6 | Component | The repeated key TDR_OFFER:T-1001 answered 409, and the 503 refusal that leaves the row unchanged and retries |
| TC-S2-E2032-APP-04 | AC7, AC8 | End to end | A synthetic name in the case facts appearing in no request field, response field, record, event payload or log line, and the proposal on SCR-15 through the composite route |

The ten legacy test case IDs, their Covers and their Data are kept in the order the legacy key lists them and character for character; the legacy level "System" maps to "End to end" and the "Access" and "Resilience" cases to "Component", as in the other stories of this run. They are carried here because the legacy key's test set is one set, while the criteria they prove on the agent side belong to `RWB-P10-E2032-APP` (ASM-3094); where a case exercises the treatment side of the answer, the agent fake of section 12.8 stands behind it. The four `TC-S2-E2032-APP` cases are new under D-RCV-60 and cover the eight criteria of section 7. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 2 integration harness and are not listed here.

### 17. Guardrails

- No value that a business person may change is written in code: the band, the wait of 60 seconds, the model code and version, the prompt version, the policy version, the mode and the lists are values in force read with their version (BR-S2-001; BR9).
- No personal data in the request, the log, the test or the prompt: the request carries the case ID, the treatment ID, the route, the band and the plan terms as identifiers and amounts, and a name, an account number, a national identifier, an address or a document text is never sent, stored, logged or put on an event (AC7; ASM-3097; Architecture v5 slide 44).
- The suggestion is never written into the offer fields, the approved amount, the treatment state or a booking: it is a proposal on the row, and the officer decides (BR3; Architecture v5 slide 44 agent-risk note).
- No read of another service's tables: the run, the policy, the prompt and the evaluation stay in `rwb_agent`, the package and its rows in `rwb_decision`, the case in `rwb_case`, and `rwb_treatment` holds no foreign key into another schema (DP-01; `ownership.json`).
- ACE data only through the owner's contract or the `v_ace_*` views: this story reads no ACE view, and the masked inputs snapshot of the legacy is assembled by rwb-agent behind its own contract (DP-05).
- The decision record is written in the same transaction as the proposal, and a failed write rolls the whole call back with MSG-P7-003 (DP-03; R-UNI-39).
- The central ledger is never written or read here: `decision_log_entry` belongs to P7 and is reached only through `rwb.decision-record.v1` (DP-03).
- An applied migration is never edited: a correction to the proposal columns is a new version on the service sequence (DP-15).
- No right is re-implemented: the capability area and the right are declared, and the guard library answers (DP-08 as a template capability).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-006 | A treatment record holds every offer's type, terms, approval and outcome | Business Requirements Program v4, section 5.3 | FEAT-AGT-10 | 7.3 Negotiate settlement or deed in lieu | R-UNI-32, R-UNI-40 | TC-E2-032-01 to TC-E2-032-08, TC-E2-032-10, TC-S2-E2032-APP-01 to TC-S2-E2032-APP-04 |
| REQ-DRI-001 | Every decision records the rule, model, agent and prompt versions | Business Requirements Program v4, section 5.7 | FEAT-AGT-10 | 7.3 Negotiate settlement or deed in lieu | R-UNI-39 | TC-E2-032-01, TC-E2-032-03, TC-E2-032-06, TC-E2-032-09, TC-E2-032-10, TC-S2-E2032-APP-01, TC-S2-E2032-APP-03 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P10-E2032-CON | Contract | C: the suggestion operation, its eight answer members, its refusal codes, its 2 s client budget and its fake |
| RWB-P10-E2032-APP | App development | The primary slice: the model run, the prompt, the guardrail, the evaluation and the legacy criteria AC1 to AC8 |
| RWB-S2-E3001-APP | App development | Sibling: the treatment row this story adds the proposal columns to, and the stage this activity runs in |
| RWB-S2-E3002-APP; RWB-S2-E3003-APP; RWB-S2-E3004-APP | App development | Siblings: the settlement offer, the below-floor approval and the TDR plan, which own the offer terms and the approval |
| RWB-PLT-E1027-CON; RWB-PLT-TE006-CON; RWB-PLT-E1042-CON; RWB-PLT-E1043-CON; RWB-PLT-N001-CON | Contract | The wave 0 service-template capability this story is built on (ASM-3098) |
| RWB-ITG-W2 | Integration | The cross-service proof of the suggestion against the live agent and the live package, held by the wave 2 harness |

### 19. Out of scope

- The model, the prompt, the guardrails, the run, the evaluation and the human-feedback record, and the legacy criteria AC1 to AC8: `RWB-P10-E2032-APP` and `RWB-P10-E2032-CON`.
- The operation path, the request and answer members of the suggestion, its refusal codes and its fake: `RWB-P10-E2032-CON` (GAP-0634).
- The model, the prompt and the policy rows of `rwb_agent`, and the Enterprise AI private endpoint INT-23: P10 rwb-agent and the infrastructure story of the key.
- The `RESTRUCTURE` package, its rows, its band and its version: rwb-decision (P7).
- The settlement offer and its range, the below-floor approval and the TDR plan: `RWB-S2-E3002-APP`, `RWB-S2-E3003-APP`, `RWB-S2-E3004-APP`.
- The case status, `CaseWorkflow` and the case signal: rwb-case (P3).
- The rights, the roles and the scope data, and the guard library that answers them: rwb-access (P4) and the platform library stories.
- The gateway-bff composite route, the screen field list and the layout: the platform edge story and the screen owners.
- The proposal column names and types, the prompt-version source and the operation segment of the proposal read: Not specified in the source documents (GAP-1882; ASM-3094).
- The real cross-service proof of the suggestion against the live agent and the live package: the wave 2 integration harness.
- The deployment of this build: chart values, the queue and topic provisioning, the flag, dashboards and the runbook.
