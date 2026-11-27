# RWB-S7-E6022-APP Send provision inputs to Finance

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S7-E6022-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-022 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S7-J |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S7-E6022-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the Finance feed slice of RWB-E6-022 in rwb-writeoff. The three legacy criteria the plan gives this slice (AC1, AC2 and AC3) are kept word for word with their origin tags; the step applies R-WO-26 to send the provision inputs and the tax file to Finance from `PROVISION_RELEASED` to `FINANCE_FEED_SENT`, with R-WO-27 on a rejected file and R-WO-28 on the accepted re-send, records each outcome through the local decision-record library before anything leaves (DP-03), builds the inputs from the service's own `write_off` rows and the tax criteria version in force, reads the case state on rwb-case's contract and answers the case move, and reads the feed state on SCR-27 behind the gateway-bff composite route on base `/api/recovery/writeoff/v1` (DP-13, DP-19). It provides no operation of its own, because TSD S7 appendix T-A publishes only the scan and the committee decision, which are sibling stories'; the plan's C row is None while four consumed surfaces exist, and the transport, layout and acceptance codes of the Finance provision feed are named by no source in the read set. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S7-E6022-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As the **finance and CFO delegate**, I want **the Workbench to produce the provision file Finance needs from the posted population**, so that **write-offs follow the criteria and the committee's decision** — in the target, as the Finance feed step of `rwb-writeoff`, which takes each case whose provision has been released, builds the provision inputs and the tax file, records the decision, sends them to the Finance provision feed and answers the case move.

This is the Finance feed slice of legacy RWB-E6-022 (FEAT-WOF-10, module S7 Write-off and recovery, priority Must, depends on FEAT-WOF-09). It owns:

- the three legacy acceptance criteria AC1, AC2 and AC3 of the key, copied verbatim with their origin tags (section 7);
- the `prepareFinanceFeed` step of `WriteOffWorkflow` on task queue `rwb-writeoff` in namespace `rwb-recovery`: R-WO-26 "Send the provision inputs and the tax file to Finance", from `PROVISION_RELEASED` to `FINANCE_FEED_SENT`, at the month-end close;
- the `sendFinanceFeed` step: the handover of the feed, R-WO-27 "Retry the feed and raise a task after the retry limit", which holds a rejected file at `FINANCE_FEED_REJECTED`, and R-WO-28 "Record the tax file reference", which returns the case to `FINANCE_FEED_SENT` once the re-sent feed is accepted;
- the provision input record set, built from the posted population of this service's own `write_off` rows (DF-FIN-010 to DF-FIN-020) with the case reference, and the tax file, built from the `tax_criteria_met` flag of each posted row and the tax criteria version in force;
- the local decision record of every outcome — case reference, write-off reference, rule ID, package version, inputs as-of date, feed reference, acceptance code, tax file reference and case move — written through RWB-PLT-E1027-CON before anything leaves (DP-03), with MSG-P7-003 when it cannot be written (legacy AC3);
- the case state read and the case move `FINANCE_FEED_SENT`, `FINANCE_FEED_REJECTED` or `FINANCE_FEED_SENT` after retry answered to rwb-case, the tax criteria version read as reference data and the WO rule set read at its version in force on rwb-decision's contract;
- the feed state on SCR-27 Write-off proposal, served behind the gateway-bff composite route (DP-19), from this service's own reads on base `/api/recovery/writeoff/v1` (DP-13).

It does not own: the published shape of the feed elements, the state and item vocabulary, the consumed rows, the rights, the error envelope and the fakes, which are RWB-S7-E6022-CON; the posting of the write-off and the provision release of R-WO-25, which are RWB-S7-E6021-APP and produce the state this step starts from; the monthly scan and the eligibility rules, which are RWB-S7-E6013-APP; the tax criteria test of each proposed account, which is RWB-S7-E6014-APP and writes the `tax_criteria_met` flag read here; the reconciliation of the approved and posted populations, which is RWB-S7-E6023-APP; the write-off exception loop, which is RWB-S7-E6024-APP; the case of record and its route states, which are rwb-case (P3); the account and ALS facts, which are rwb-source-data's (P1); the rule package and the central ledger, which are rwb-decision's (P7); the Finance provision feed itself, its transport, layout, acceptance codes and retry schedule, which are Finance's; and the deployment of this build, which is the operations story of the key.

### 2. Business rationale

The provision Finance needs exists only once the write-off is posted and the provision is released, and a provision input that is rebuilt by hand each month is a control nobody can prove. The legacy feature produced the file in process against the `recovery` schema, with no seam between the posted population, the case state, the decision log and Finance's feed. The objective, the problem and the metric are unchanged: produces the provision file Finance needs from the posted population (FSD S7 A2.10.1; FEAT-WOF-10), because write-off populations are assembled by hand each month (FSD S7 A1.3), with the metric "Write-off packs accepted first time", rising each month, measured on the decision log and the Workbench records, reviewed monthly (FSD S7 A2.10.1).

What D-RCV-60 changes is who owns each part of the sentence.

- **The posted population is this service's.** `write_off` is S7's only table in `rwb_writeoff` (context pack ownership rows; TSD S7 T3.1), so the population, its amount, its tax flag, its committee and posting dates and its cost centres are read here and no other service reads them; the case, the pack document and the ledger stay with P3, P5 and P7 (ASM-5074).
- **The case stays with rwb-case.** `recovery_case` and the route states `PROVISION_RELEASED`, `FINANCE_FEED_SENT` and `FINANCE_FEED_REJECTED` are P3's, so the step answers the move with the rule and its version and writes no case row.
- **The tax criteria version is reference data, never a constant.** R-WO-03 gives it the systems column "Reference data, Finance provision feed" and VR-S7-010-1 holds the scan with MSG-S7-001 while no version is published, so the version in force is read with its version and the tax file is built against it.
- **The decision is recorded first**, in the same transaction that keeps the feed outcome, which is what legacy AC3 tests: a feed that cannot be recorded changes nothing and leaves nothing with Finance (DP-03; ADR-022).
- **The feed is Finance's.** The provision file layout, the tax file layout, the transport, the acceptance codes and the retry schedule are named by no source in the read set, and Architecture v5 slide 13 gives rwb-writeoff no call to rwb-integration and no file cell while R-WO-26 names the Finance provision feed, so the conflict is recorded and the step builds and validates the feed instead of inventing a channel (GAP-3035; ASM-5076).
- **The feed status has no column of its own.** TSD S7 T3.1 gives DF-FIN-010 to DF-FIN-020 and none of them is a feed status, a feed reference, an acceptance code or a tax file reference, so the decision record and the case state carry them (GAP-3035; ASM-5080).

No business value is invented: the provision file layout, the tax file layout, the acceptance and rejection codes, the retry limit and the Finance address are named by no source in the read set and stay unstated with the placeholder and the recorded gap and assumptions (GAP-3035; ASM-5073, ASM-5076).

### 3. Preconditions

- RWB-S7-E6022-CON is published: the provision-input and tax-file elements, the finance-feed item and its result set, the state and item vocabulary, the four consumed rows, the rights, the error envelope and the fakes. This story adds no shape of its own.
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction, and a failed write stops the step with MSG-P7-003, so the record and the outcome commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-27 Write-off proposal reaches this service and rwb-case through the gateway-bff composite route, one hop, read only (DP-19).
- The posting of R-WO-25 is complete for the population: each case stands at `PROVISION_RELEASED` and its released amount is held in the posting story's decision record. RWB-S7-E6021-APP writes that state; this story only reads it.
- `write_off` exists in schema `rwb_writeoff` from the DB story of this service, with the columns of DF-FIN-010 to DF-FIN-020 and the standard record columns of TSD S7 T3.0, populated by the scan, the committee and the posting stories; this story adds no table, no column and no migration.
- rwb-case answers the case state and accepts the move, with the case reference, the write-off link and the route state; the operation name of the case-move answer is Not specified in the source documents (GAP-3035; ASM-5073).
- The tax criteria version in force is answered as reference data, with its version and its effective date; the operation name of the reference-data read is Not specified in the source documents (GAP-3035; ASM-5075).
- rwb-decision answers the WO rule set at its version in force with R-WO-25 to R-WO-28 among its 51 rules over 27 states; the operation name of the package read is Not specified in the source documents (GAP-3035; ASM-5073).
- The Finance provision feed answers an accepted feed, a rejected feed and no answer inside the timeout through its published interface; its transport, address, layout, acceptance codes and retry schedule are Not specified in the source documents (GAP-3035; ASM-5076).
- The service runs as its own login on schema `rwb_writeoff`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case` or on `recovery.v_ace_account` is refused by the database and fails the boundary test.
- No approval is needed to build against a Draft contract baseline; the baseline is tagged by RWB-S7-E6022-CON when its tests pass. No approved baseline exists for the key — FSD S7 v3 and TSD S7 v2 stand at "In review" — so the story proceeds in Draft (realignment v1) and the release 30 April 2027 is copied unchanged and marked tentative (ASM-5081).

### 4. Flow

1. The posting story completes the provision release: the case stands at `PROVISION_RELEASED` under R-WO-25 and the released amount is in its decision record. The parent `CaseWorkflow` forwards the move to the `WriteOffWorkflow` child of the case on queue `rwb-writeoff` (Temporal and Drools Design slide 13).
2. At the month-end close the `prepareFinanceFeed` step of `WriteOffWorkflow` receives its trigger `FINANCE_FEED_RUN` and reads the version of the WO rule set in force on rwb-decision's contract, one hop with a 2 s budget and a breaker.
3. `PostedPopulationReader` reads the posted population of the business date from `write_off`: the write-off reference, the case reference, the amount, the tax criteria flag, the committee date, the posting date, the responsibility centre, the cost centre, the GL product and the amount recovered after charge-off.
4. `CaseStateReader` reads the case state and the write-off link on rwb-case's contract. A case that is not at `PROVISION_RELEASED`, or has left the population since it was read, is skipped with nothing written, and the run log names it.
5. `TaxCriteriaReader` reads the tax criteria version in force as reference data. Where no version is in force the step holds with VR-S7-010-1 and MSG-S7-001 and writes nothing (R-WO-03).
6. `FinanceFeedBuilder` builds the provision input set from the population rows and the released amount, and the tax file from the `tax_criteria_met` flag of each row against the version in force. The layouts are rows of the Finance feed configuration, never constants of this service (GAP-3035; ASM-5076).
7. `WriteOffDecisionRecordWriter` writes one decision record for the run and one per case outcome through the local decision-record library, **before anything leaves**: the case reference, the write-off reference, the rule ID with its package version, the inputs as-of date, the tax criteria version, the feed reference, the outcome and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC3).
8. `FinanceFeedSender` hands the two items to the Finance provision feed through its published interface with a manifest — feed reference, business date, provision input set, tax file, record reference and an `Idempotency-Key` — and receives the feed reference and the acceptance code.
9. Where the feed is accepted, R-WO-26 applies: the step writes its own record with the feed reference and the acceptance code and **answers the case move `FINANCE_FEED_SENT`**. rwb-case writes the case row; this service writes neither the row nor the state.
10. Where the feed rejects the file, R-WO-27 holds the case: the rejection code and the feed reference are written to the record, the two-working-day task is raised for the Credit Administration officer, the case move `FINANCE_FEED_REJECTED` is answered, and no second feed is sent until the retry limit is reached.
11. Where a re-sent feed is accepted, R-WO-28 applies: the step records the tax file reference, writes its record naming R-WO-28 and the previous feed reference, and answers the case move `FINANCE_FEED_SENT`.
12. A repeated trigger for the same business date, population and package version writes no second record, sends no second feed and answers no second move; the `Idempotency-Key` answers the feed that exists.
13. The step hands the next stage over: once a feed is accepted, `finance_feed_status` is `accepted` and R-WO-29 decides the post charge-off treatment in the story that owns it. This story neither starts nor waits for that step.
14. SCR-27 Write-off proposal shows the write-off in its scan, proposed, in-committee and approved readings, and the feed outcome for the Finance and CFO delegate: the write-off and its feed outcome from this service, the case state from rwb-case, merged by the gateway-bff composite route, one hop, read only (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes and nothing leaves: no record, no feed, no case move; an incident is raised | MSG-P7-003 | AC3, TC-E6-022-03, TC-E6-022-05 |
| X2 | A caller without the Write-off and posting right reads the feed outcome | 403 before any read; nothing changes and no record is written | MSG-P4-002 | TC-E6-022-04 |
| X3 | No tax criteria version is in force | The step holds the case at `PROVISION_RELEASED`, writes nothing and raises the hold; the run resumes when Finance publishes the version | MSG-S7-001 | VR-S7-010-1, X8 |
| X4 | The case is not at `PROVISION_RELEASED` when the run arrives, or has left the population since it was read | 409 for that case and nothing is written for it; a case that has already moved is not fed twice | None | X7 |
| X5 | rwb-case, rwb-decision or the reference-data read does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own schedule; nothing is written and no move is answered; the caller sees 503 with the platform error envelope | None | X4 |
| X6 | The Finance provision feed rejects the file | R-WO-27 records the rejection code, answers `FINANCE_FEED_REJECTED` and raises the two-working-day task; the retry limit is the feed row's | Not specified in the source documents (GAP-3035; ASM-5076) | X7, R-WO-27 |
| X7 | The same business date, population and package version arrive twice, or the same `Idempotency-Key` twice | One record, one feed and one answer per case; the repeat is counted and the key answers the feed that exists | None | X7 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR5, BR8 |
| X9 | The Finance feed row has changed since the last run, or no row is in force at the business date | The next feed obeys the new version, or no feed is built and the cases stay at `PROVISION_RELEASED` with the refusal in the run log | MSG-GEN-001 | X9 |

X1 is the legacy exception path carried onto this slice (legacy AC3), X2 to X5 and X7 are the paths the target call types add, X6 is the feed's own rejection path under R-WO-27, and X8 and X9 are the boundary and the feed-configuration paths.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S7-E6022-CON, the rwb-case, rwb-decision and reference-data fakes, the Finance feed fake and the decision-record stub, on its own schema, and needs no live P1, P3, P7 or Finance |
| Negotiable | The activity names, the decision code per rule and the shape of the stage outcome are this story's choice; the rules, the messages, the states and the four consumed surfaces are fixed |
| Valuable | The provision inputs and the tax file reach Finance from the posted population once, with the record that proves it, so the provision release is provably closed out |
| Estimable | Two workflow steps, one population reader, one builder, one sender, one record write, one case-move answer and one read-only screen reading |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | AC1 and AC2 run on the fakes with the feed fake accepting and rejecting; AC3 runs with the record stub stopped; the hold, the rejection and the re-send are each one component case |

### 7. Acceptance criteria

```gherkin
Feature: Send provision inputs to Finance

  Scenario: AC1 Send provision inputs to Finance (legacy RWB-E6-022 AC1)
    Given the rwb-case contract mock returns the posted population at PROVISION_RELEASED
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then produces the provision file Finance needs from the posted population
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-WO-26 (legacy RWB-E6-022 AC2)
    Given the rwb-case contract mock returns the case at PROVISION_RELEASED and accepts the move to FINANCE_FEED_SENT
    Given a case in state PROVISION_RELEASED
    When finance feed run
    Then send the provision inputs and the tax file to Finance
    Then the case moves to FINANCE_FEED_SENT

  Scenario: AC3 Not recorded (legacy RWB-E6-022 AC3)
    Given the Finance provision feed mock returns an accepted feed with its reference
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The three criteria are the three criteria of RWB-E6-022, word for word, with their origin tags added and nothing else changed: "the data and the rule version this feature needs", "its trigger arrives", "produces the provision file Finance needs from the posted population", "a case in state PROVISION_RELEASED", "finance feed run", "send the provision inputs and the tax file to Finance", "the case moves to FINANCE_FEED_SENT", "the decision log cannot be written", "the action is taken", "nothing changes" and "the user sees MSG-P7-003" all stand. The single leading `Given` of each scenario is the only addition, and it names the cross-service part the criterion leaves open — the case state and the move of rwb-case, and the Finance feed at the exit. The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_writeoff`, with the central `decision_log_entry` ledger of rwb-decision behind it.

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-WO-25 | Write-off | D9 | POSTED | PROVISION_RELEASE_RUN | provision_carried present | Release the provision carried and record the released amount | PROVISION_RELEASED | Workbench | Rules component, ALS core and GL | None |
| R-WO-26 | Write-off | D9 | PROVISION_RELEASED | FINANCE_FEED_RUN | Any | Send the provision inputs and the tax file to Finance | FINANCE_FEED_SENT | Credit Administration | Finance provision feed | month-end close |
| R-WO-27 | Write-off | D9 | FINANCE_FEED_SENT | FINANCE_REJECTED_FILE | finance_feed_status = rejected | Retry the feed and raise a task after the retry limit | FINANCE_FEED_REJECTED | Credit Administration | Finance provision feed | 2 working days |
| R-WO-28 | Write-off | D9 | FINANCE_FEED_REJECTED | FEED_ACCEPTED_ON_RETRY | finance_feed_status = accepted | Record the tax file reference | FINANCE_FEED_SENT | Credit Administration | Finance provision feed | None |

The four rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner and systems columns name business roles and systems, not services: "Finance provision feed" is Finance's feed, "Rules component" is the embedded Drools kit fed by rwb-decision (P7), "ALS core and GL" is the ledger interface, and "Workbench" is this service. R-WO-25 is tabled only because it produces the state this step starts from; it belongs to RWB-S7-E6021-APP. R-WO-29, which decides the post charge-off treatment once the feed is accepted, belongs to the story that owns that treatment and is not this step's.

| ID | Rule | Source |
|---|---|---|
| BR1 | The provision inputs and the tax file leave to Finance as two items of the Finance provision feed, built from data and the feed configuration; this service writes no Finance file of its own layout and holds no direct Finance endpoint | R-WO-26 (Systems column); ASM-5076 |
| BR2 | The decision is recorded before anything leaves, with the rule ID and the package version in force; a failed write changes nothing, leaves no feed and answers no move, and the caller sees MSG-P7-003 | DP-03; TSD S7 T2; legacy AC3 |
| BR3 | The posted population is this service's `write_off` rows only: no other service reads them and this step reads no other service's table; `recovery_case`, `document`, `decision_log_entry` and `rule_row` are not copied here | DP-01; TSD S7 T3.1; ASM-5074 |
| BR4 | The case move is answered and not written: `recovery_case` and the states `PROVISION_RELEASED`, `FINANCE_FEED_SENT` and `FINANCE_FEED_REJECTED` are rwb-case's | ASM-5073; TSD S7 T4 |
| BR5 | The tax criteria version is reference data read with its version; where none is in force the step holds with VR-S7-010-1 and MSG-S7-001 and writes nothing | R-WO-03; FSD S7 A2.10.3.1 |
| BR6 | No value a business person may change is written in code: the feed layout, the tax file layout, the acceptance and rejection codes, the retry limit, the month-end close and the rule rows are data or configuration read with their version | FSD S7 BR-S7-010; legacy Guardrails |
| BR7 | One feed per business date and population, and one re-send per cleared rejection: a rejection is held at `FINANCE_FEED_REJECTED` under R-WO-27 and only an accepted re-send returns the case under R-WO-28 | R-WO-27; R-WO-28 |
| BR8 | The feed status, the feed reference, the acceptance code and the tax file reference are held in the decision record and in the case state, because no column of this service's table carries them; this story adds no column | GAP-3035; ASM-5080 |
| BR9 | The month-end close of R-WO-26 is a durable timer of `WriteOffWorkflow` and not a Schedule; the service's one job row is the scan's | R-WO-26 (Timer column); context pack, jobs 1 (JOB-16); ASM-5078 |
| BR10 | No person name, address, contact value or identity number enters `rwb_writeoff`, the record, a feed item, a log or a workflow input; the population carries references, amounts, dates and codes only | Template and Rules §R7.2 (s17); TSD S7 T6.2 |
| BR11 | The same business date, population and package version twice, or the same `Idempotency-Key` twice, produces one record, one feed and one answer per case | TSD S7 T-A.2; R-UNI-40 |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it (BR4). What this story owns is the state of its two steps and the feed.

| From (case route state) | Event | Condition | To | Rule |
|---|---|---|---|---|
| POSTED | PROVISION_RELEASE_RUN | provision_carried present | PROVISION_RELEASED | R-WO-25, RWB-S7-E6021-APP |
| PROVISION_RELEASED | FINANCE_FEED_RUN | Any, at the month-end close | FINANCE_FEED_SENT | R-WO-26 |
| FINANCE_FEED_SENT | FINANCE_REJECTED_FILE | finance_feed_status = rejected | FINANCE_FEED_REJECTED | R-WO-27 |
| FINANCE_FEED_REJECTED | FEED_ACCEPTED_ON_RETRY | finance_feed_status = accepted | FINANCE_FEED_SENT | R-WO-28 |
| FINANCE_FEED_SENT | POST_CHARGEOFF_RULE_RUN | finance_feed_status = accepted | PLACEMENT_DECIDED | R-WO-29, the post charge-off story |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The provision release completes | The package in force is read | Preparing the feed |
| Preparing the feed | R-WO-26 fires at the month-end close and the tax criteria version is in force | The record is written | Sending the feed |
| Sending the feed | The feed is accepted | The record with the feed reference is written | Waiting for the next business date |
| Sending the feed | The feed rejects the file | R-WO-27 | Held at `FINANCE_FEED_REJECTED`, task open |
| Held | A re-sent feed is accepted | R-WO-28 | Sending the feed, one new feed |
| Preparing or sending | The record write, the feed or a consumed read fails | X1, X3, X5 | Waiting, nothing changed |

The route states are those of the WRITEOFF machine of TSD S7 T4, with 51 rules over 27 states, and they live on the case of record. This baseline fixes the vocabulary of the four states between `POSTED` and `FINANCE_FEED_SENT` and moves no case itself.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-writeoff service identity, login on schema `rwb_writeoff` (DP-02) | Runs the feed under the service identity with no officer task on the happy path; holds the primary use of the feature (FSD S7 A2.10.3.3 "None; runs unattended") |
| Finance and CFO delegate, RW-FINANCE | Write-off and posting RA in TSD S7 T6.1: reads the posted population, the feed outcome and the tax file reference on SCR-27; the also-user of FSD S7 A2.10.3.3 |
| Credit Administration officer, RW-CREDITAD | Write-off and posting CRUA: reads the feed outcome and works the two-working-day task of R-WO-27 |
| Write-off committee member, RW-WOCOMM; product head, RW-PRODHEAD | Write-off and posting RA: read the outcome inside their scope |
| Write-off team member, RW-WRITEOFF | Write-off and posting CRU: reads the outcome inside the scope |
| RW-FRAUD, RW-DEBTSALE, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Write-off and posting R: read only, in scope |
| SY-CASEWF, SY-RULES, SY-AGENT | Write-off and posting R as the matrix gives it; the service identities run the step and are subject to the same checks |
| SY-DATALOAD | Write-off and posting U: the ACE load path, not this step |

The rights are the rows of TSD S7 T6.1 and nothing wider. The legacy permission table gives right A of "Write-off and posting" to RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE and right C to RW-WRITEOFF and RW-CREDITAD; those two rights sit on the scan and the committee-decision operations, which are sibling stories', and this step declares no operation and no right of its own. R-WO-26 and R-WO-27 name "Credit Administration" in their owner column, which is the business owner of the decision and not an operator right: the feed and the re-send run unattended and the officer reads the outcome and works the task (ASM-5079). DP-08 is not in this story's pattern set: the capability area and the right are declared per operation by the service template, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-FIN-010 to DF-FIN-020 | write_off (S7, `rwb_writeoff`) | the write-off, its case, its decision-log link, its `amount`, its `tax_criteria_met`, its `committee_date`, its `posted_date`, its `responsibility_center`, its `cost_center`, its `gl_product` and its `recovered_after` | Read: the posted population of the business date; no column changes at this step |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_writeoff`) | the rule ID, the package version, the tax criteria version, the inputs as-of date, the feed reference, the acceptance code, the tax file reference, the outcome and the decided-at time | Write through the local library, before anything leaves |
| Standard columns | write_off (S7, `rwb_writeoff`) | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` | Read; the optimistic lock is not taken because no column changes |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table and not written: the state arrives on the rwb-case contract and the move is answered |
| DF-DOC-001 to DF-DOC-011 | document (P5) | id, case_id, person_key, document_type, source, storage_ref and 5 more | Not read by this step: the pack document is the pack story's; where the tax file is stored is Not specified in the source documents (GAP-3035; ASM-5076) |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read as a table: the package arrives on rwb-decision's contract |
| DF-DEC ledger | decision_log_entry (P7) | the central ledger entry | Not written here: the local record is this service's and the library relays it |
| No row | The tax criteria version | the version in force, its effective date and the tax criteria it carries | Read as reference data through rwb-case's reference-data contract, with its version (ASM-5075) |

Field IDs are those of TSD S7 T3.1 and the Logical Data Model and Data Dictionary, and the case, document and ledger rows are the rows the legacy Data table lists, with their owners changed to P3, P5 and P7 by the target. **No new table, no new column and no migration**: the one table arrives with the DB story of this service, and this story writes no business column of it — its outcome is the record, the feed item and the case move. The missing feed-status, feed-reference, acceptance-code and tax-file-reference columns are recorded (GAP-3035; ASM-5080). `decision_record`, `idempotency_key` and `outbox_event` are library objects created in `rwb_writeoff` by the library's migration (DP-03); this step writes no outbox row because it publishes no event (§12.3).

**No personal data.** The records, the feed items and the manifests carry references, codes, amounts, dates, a boolean, a version and an acceptance code. No name, address, contact value or identity number enters `rwb_writeoff`, a record, a feed item, a log or a workflow input, and every fixture is synthetic. `primary_person_key` is P3's and is never copied here.

### 12. Contract

#### 12.1 REST operations provided

None of its own. TSD S7 appendix T-A publishes two operations for the module: API-S7-001 `POST /write-off-scans` (right C, request ScanRequest, response WriteOffScan) and API-S7-002 `POST /write-offs/{writeOffId}/committee-decision` (right A, request CommitteeDecision, response DecisionLogEntry), and neither is a Finance feed operation. The two endpoint rows of the legacy story are those same two operations, whose shapes are the scan story's and the committee story's (RWB-S7-E6013-APP, RWB-S7-E6018-APP); this story adds no operation and redefines neither. The feed outcome is read from the case state of rwb-case and from the record of this service behind the composite route (§15). The absence is recorded as GAP-3035 with ASM-5079.

#### 12.2 REST operations consumed

| Operation | Base | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, its route state, its write-off link and its business date; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3035; ASM-5073)) | rwb-case (P3) | P3 rwb-case | The moves `FINANCE_FEED_SENT` and `FINANCE_FEED_REJECTED` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent applies; faked |
| The rule package in force (read) | `/api/recovery/decision/v1` | P7 rwb-decision | The WO rule set at its version with R-WO-25 to R-WO-28; faked |
| The reference-data read (operation name Not specified in the source documents (GAP-3035; ASM-5075)) | `/api/recovery/case/v1` | P3 rwb-case | The tax criteria version in force, its effective date and its criteria; faked |
| The Finance provision feed (interface values Not specified in the source documents (GAP-3035; ASM-5076)) | Finance provision feed, outside the 19 services | Finance | The provision input set and the tax file in; the feed reference and the acceptance code out; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four reads and the feed call are contract dependencies of class C that the plan does not carry, because this story's C row is None; the absence is recorded (GAP-3035; ASM-5073).

#### 12.3 Events published

None. The service publishes on `rwb.writeoff.events.v1` and the catalogue holds one event of this service, `WriteOffApproved` (EV-24, payload `writeOffId`, `caseId`, `amount`, consumer "Posting"), which is the approval story's and not this step's. No finance-feed or provision event exists in the catalogue, so this story declares no event, no producer group and no outbox row of its own, and a build that publishes one fails the absence test. The local decision record travels on the shared `rwb.decision-record.v1` through the library of RWB-PLT-E1027-CON, not through this story's topic (ASM-5077).

#### 12.4 Events consumed

None. The connection matrix gives rwb-writeoff listeners on rwb-payment's and rwb-source-data's events, which belong to the post charge-off payment story and the scan (`AceDataReady`, EV-26, whose consumers include the write-off scan JOB-16). The step starts from the provision release of R-WO-25 and the month-end timer of R-WO-26, so it holds no consumer group, no subscription and no inbox row, and a build that adds one fails the absence test (ASM-5077).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case, the child of `CaseWorkflow`, which continues-as-new across the committee, posting, Finance feed and post charge-off window | `rwb-writeoff` in namespace `rwb-recovery` | Input: the case, the write-off, the business date and the package in force; this step sits after the posting, so no compensation is declared for it |
| `prepareFinanceFeed` | Activity, the R-WO-26 step | `rwb-writeoff` | The business date, the population and the package in force in; the provision input set, the tax file, the rule ID, the package version, the record id and the `FINANCE_FEED_SENT` move out |
| `sendFinanceFeed` | Activity, the R-WO-27 and R-WO-28 step | `rwb-writeoff` | The feed items and the manifest in; the feed reference, the acceptance code, the tax file reference, the record id and the `FINANCE_FEED_SENT` or `FINANCE_FEED_REJECTED` move out |

No child workflow for the case and none for the money exists in this service. The activity names are target design choices fixed by no source document; the retry is 1 s initial interval, back-off 2, 10 attempts, and a rule that is not in force is non-retryable. The service's one job row, JOB-16, is the monthly scan's and is RWB-S7-E6013-APP's.

#### 12.6 Schedules

None. R-WO-26 carries "month-end close" in its timer column and the service's one job row is the scan's (context pack, jobs 1, JOB-16), so the wait is a durable timer inside `WriteOffWorkflow` on `rwb-writeoff` and not a Temporal Schedule. No Quartz row, no shared job table and no batch table is declared or moved here (ASM-5078).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off, its population and its GL-facing columns; read at this step, which changes no column |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked record of each rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the business date, the population and each feed |
| outbox_event | PLT library, created in `rwb_writeoff` | Present as a library object; this step writes no row to it (§12.3) |

Not owned and never read as a table: `recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), `document` (P5), every `v_ace_*` view (P1), and the Finance feed tables and files. No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case state and move fake | Cases `RC-2026-000842` and its siblings at `PROVISION_RELEASED`; an accepted move and a refused move for `FINANCE_FEED_SENT` and `FINANCE_FEED_REJECTED`; a case at `POSTED` and a case that has left the population | AC1, AC2, X4 |
| rwb-decision rule-package fake | The WO rule set at its version in force with R-WO-25 to R-WO-28 | AC1, AC2 |
| Reference-data fake of rwb-case | The tax criteria version in force with its effective date; a state with no version in force | AC1, X3 |
| Finance provision feed fake | One feed accepted with its reference and acceptance code; one file rejected with its code; a re-send accepted with the tax file reference; no answer beyond 2 s | AC2, X6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC3, TC-E6-022-05 |
| Authorise stub of the service template | Right R held and not held | TC-E6-022-04 |
| gateway-bff composite route fake | The merged SCR-27 answer for write-off `WO-2026-000042`: the write-off, its feed outcome and the case state | AC1 |

The fakes are test-only and are replaced by the real services and the real Finance interface in SIT. The operation names and the feed's transport, layout, acceptance codes and retry schedule carry the placeholder until their owners confirm them (GAP-3035; ASM-5073, ASM-5076).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 4 consumed | The rwb-case state read and move answer, the rwb-decision package read, the rwb-case reference-data read; one hop, 2 s; plus the Finance feed call |
| Kafka | 0 published, 0 consumed | `WriteOffApproved` (EV-24) is the approval story's and `AceDataReady` (EV-26) is the scan's |
| Temporal | 1 workflow and 2 activities | `WriteOffWorkflow`, `prepareFinanceFeed` and `sendFinanceFeed` on `rwb-writeoff`; no Schedule |
| File | 1 built by this story | The provision input set and the tax file are file items of the Finance feed; their layout is the feed's row and carries the placeholder |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.writeoff`, module `financefeed`; front end `src/modules/recovery/writeoff/WriteOffProposal.tsx`, the fragment SCR-27 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of both steps: the record and the feed commit together or not at all. DP-13 fixes the base of the service and this story adds no operation of its own to it. DP-19 carries SCR-27, whose readings this step does not change. The two H rows of the table are the ones the metadata carries, and no DP row of this key adds a contract dependency: the four reads and the feed call are class C in fact while the plan's C row is None (GAP-3035; ASM-5073). DP-07 is not in this key's pattern set although the tax criteria version is reference data, and DP-16 is not either although R-WO-26 names an external feed; both are recorded (ASM-5075, ASM-5076).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `WriteOffWorkflow` Finance feed branch | Workflow | Waits for the provision release and the month-end close, reads the package in force, runs the two steps and reports the outcome to the parent |
| `prepareFinanceFeed` | Activity | Reads the population, the case state and the tax criteria version, evaluates R-WO-26, writes the record and builds the two items |
| `sendFinanceFeed` | Activity | Hands the items over, applies R-WO-27 and R-WO-28, writes the record and answers the move |
| `PostedPopulationReader` | Repository adapter | The `write_off` rows of the business date, with their GL-facing columns |
| `FinanceFeedBuilder` | Service | The provision input set and the tax file, from data and never from a constant |
| `FinanceFeedSender` | Client | The feed call, the manifest, the key, the feed reference and the acceptance code |
| `CaseStateReader` and `CaseMoveAnswer` | Client | The state read and the `FINANCE_FEED_SENT` and `FINANCE_FEED_REJECTED` answers to rwb-case |
| `RulePackageClient` and `TaxCriteriaReader` | Client | The package in force of rwb-decision and the reference-data read of the tax criteria version |
| `WriteOffDecisionRecordWriter` | Library adapter | The record with the rule ID, the version, the feed reference and the codes, written before anything leaves |
| `WriteOffProposal` | React component | Shows the write-off and its feed outcome on SCR-27, read only, with the refused, rejected, held and stale readings |

**Database and migrations.** No Flyway file. `write_off` arrives with the DB story of this service, and the record, the idempotency key and the outbox are library objects created in `rwb_writeoff` by the library's migration (DP-03). No column is added for the feed status, the feed reference, the acceptance code or the tax file reference: those are recorded in the decision record (BR8; ASM-5080).

**Configuration and reference data.**

- The tax criteria version in force, read as reference data and never as a constant (BR5; ASM-5075).
- The feed layout, the tax file layout, the transport, the address, the acceptance and rejection codes, the retry limit and the month-end close: rows of the Finance feed configuration, read per run (GAP-3035; ASM-5076).
- The rules R-WO-25 to R-WO-28: rule rows of the package with their version, never written in code.
- The capability area "Write-off and posting" and its rights: access rows of rwb-access, read through the guard.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020.

**Build steps**

1. The Finance feed branch of `WriteOffWorkflow` and its input record, registered on `rwb-writeoff`, with the provision release as its trigger.
2. `PostedPopulationReader`, `CaseStateReader`, `RulePackageClient` and `TaxCriteriaReader` against their fakes, with the 2 s budget, the breaker and the hold of X3.
3. `FinanceFeedBuilder` with the two items from the feed configuration rows, and the no-constant test on every value.
4. `WriteOffDecisionRecordWriter` against the stub, in the same transaction as the feed, with the failed-write path (AC3, X1).
5. `FinanceFeedSender` with the manifest, the key and the acceptance code, then R-WO-26, the R-WO-27 hold with the two-working-day task and the R-WO-28 re-send (X6).
6. The repeat guard on the business date, the population and the key (X7), and the feed-configuration read (X9).
7. SCR-27 through the composite route fake, and the boundary test: no statement outside `rwb_writeoff`, no `v_ace_*` read, no write to `rwb_case` or `rwb_decision` (X8).

**Feature flag.** `rwb.writeoff.finance-feed-v1`, a flag of the platform library; off means the step holds the case at `PROVISION_RELEASED`, writes nothing and sends no feed, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, a SIT run builds and sends the feed for a posted population once, holds a rejected file at `FINANCE_FEED_REJECTED` and re-sends it after the correction, a forced record failure changes nothing and sends no feed, a repeated trigger writes once, and no `recovery_case` row and no `v_ace_*` read exists in the build.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | No tax criteria version is in force when the run arrives (VR-S7-010-1; X3) | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | A required field of the population row or of the feed manifest is absent or invalid, or no feed row is in force at the business date (X9) | Enter {field}. |
| MSG-P4-002 | A role without the Write-off and posting right reads the feed outcome (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before anything leaves (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| None | The Finance feed rejects the file (X6); the acceptance and rejection code and its text are the feed's row | Not specified in the source documents (GAP-3035; ASM-5076) |

The four named IDs are those of the legacy message set of RWB-E6-022 and of FSD S7 A2.10.3.1, and their text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is invented. MSG-S7-001 is the scan's message in R-WO-03 and is raised here because the tax criteria version gates the tax file.

### 15. Screens and states

SCR-27 Write-off proposal, in its scan, proposed, in-committee and approved readings, is served through the gateway-bff composite route (DP-19). The route calls rwb-writeoff for the write-off and its feed outcome and rwb-case for the case and its route state; this story fixes the rwb-writeoff answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

| State of SCR-27 | What it shows | Where it comes from |
|---|---|---|
| Scan and proposed | The population of the cut-off date and the write-off per case, awaiting the pack | The scan story; `POPULATION_PROPOSED` of rwb-case |
| In committee | The pack and the committee route of the case | The pack and committee stories; `WITH_COMMITTEE` of rwb-case |
| Approved | The final call, the limit applied and the posting state | The committee story; `APPROVED` of rwb-case |
| Provision released, feed pending | The write-off, its amount, its tax flag and the month-end close it waits for | This service; `PROVISION_RELEASED` of rwb-case |
| Feed sent | The feed reference, the acceptance code and the tax file reference | This service; `FINANCE_FEED_SENT` of rwb-case |
| Feed rejected and held | The rejection code and the two-working-day task of R-WO-27 | This service; `FINANCE_FEED_REJECTED` of rwb-case |
| Refused, not recorded, no tax criteria version | The messages of section 14 | This service and the reference data |

The legacy screen table gives SCR-27 with the states "Scan; proposed; in committee; approved"; the first three belong to the earlier stories of the module, the fourth to the committee story, and this story adds the three readings a feed produces on the same screen. The legacy table gives no screen for the feed, so no screen is invented.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-022-01 | AC1: the provision file is produced from the posted population and the result is recorded with the rule version | Component | Write-offs `WO-2026-000042` and `WO-2026-000043` posted; the case fake at `PROVISION_RELEASED`; the tax criteria version `2026-12`; the record asserted |
| TC-E6-022-02 | AC2: R-WO-26 sends the provision inputs and the tax file and moves the case to `FINANCE_FEED_SENT` | Component | Case `RC-2026-000842` at `PROVISION_RELEASED`; the package in force; the feed accepted; the move asserted on the fake |
| TC-E6-022-03 | AC3: the record cannot be written, so nothing changes, nothing leaves and the user sees MSG-P7-003 | Component | The record stub stopped; no feed, no reference, no move |
| TC-E6-022-04 | Access: a role without the right is refused with MSG-P4-002 | Component | A caller without Write-off and posting R on the write-off read; no read and no record |
| TC-E6-022-05 | Principle 5: a forced decision log write failure stops the action with MSG-P7-003 and sends no feed | NFR | The record store stopped during a business date; the run is repeated after recovery and writes once |

The five legacy cases are those of RWB-E6-022 in their legacy order, with the Level column added: every case is proved on the fakes, so every case is `Component`, except the forced-failure case which is `NFR`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID. No `-ITG` copy is written by this story: the key is not split to an integration story by the plan, and the cross-service evidence of AC1 and AC2 is the component proof on the four fakes.

### 17. Guardrails

- No business value in code: the feed layout, the tax file layout, the acceptance and rejection codes, the retry limit, the month-end close, the tax criteria version and the rule rows stay data, reference data or configuration, never a constant, a default or a branch.
- No personal data in a record, a feed item, a workflow input or a log: references, codes, amounts, dates, a boolean, a version and an acceptance code only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test.
- Nothing leaves except through the Finance provision feed row: no direct Finance endpoint, no letter, no email and no second channel built here (BR1).
- The case stays with rwb-case: no `recovery_case` row, no case route-state column and no case write here (BR4).
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- The record precedes the feed and both or neither; a build that sends a feed outside the record's transaction fails the review (DP-03; BR2).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no event published by this step and no `v_ace_account` view read.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S7-005 | Approved write-offs post to the core system and the general ledger, the provision is released, and completeness is published (FSD S7 Requirements served, E6); the split plan carries no requirement id for this slice (GAP-3035) | The Finance feed step, its two items and the case moves | TC-E6-022-01, TC-E6-022-02 |
| FEAT-WOF-10 | Send provision inputs to Finance, System, runs unattended, systems ALS and GL, depends on FEAT-WOF-09 (Epics 3 to 8 Specification v3) | The whole slice | All |
| ADR-013 | 19 services inside ACE | rwb-writeoff as the owner of the write-off and the step | TC-E6-022-01 |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-E6-022-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-E6-022-01, TC-E6-022-02 |
| ADR-022 | Local decision record plus central ledger | The record written before anything leaves | TC-E6-022-03, TC-E6-022-05 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-022, disposition Split (rework); feature FEAT-WOF-10; module S7 Write-off and recovery; release 30 April 2027 (tentative) |
| Legacy criteria | AC1, AC2 and AC3 owned word for word by this story |
| Source text | Legacy RWB-E6-022; FSD S7 Write-off and recovery v3 A2.10, A1.3 and Requirements served; TSD S7 Write-off and recovery v2 T3, T4, T5, T6, T-A and T-B; Business Rules and Routing Logic v4 rows R-WO-25 to R-WO-28; Event and Messaging Design v5 EV-24 and EV-26; Epics 3 to 8 Specification v3 row FEAT-WOF-10 |
| Test cases | TC-E6-022-01 to TC-E6-022-05 |
| Feature and screens | FEAT-WOF-10, SCR-27 Write-off proposal |
| Rules | R-WO-26, with R-WO-27 and R-WO-28 on the feed's rejection path and R-WO-25 as the precondition, governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes of the feed elements, the vocabulary, the consumed rows, the rights, the error envelope and the fakes: RWB-S7-E6022-CON.
- The posting of the write-off, the provision release of R-WO-25 and the recording of the released amount: RWB-S7-E6021-APP.
- The monthly eligibility scan and R-WO-01 to R-WO-04, with JOB-16: RWB-S7-E6013-APP.
- The tax criteria test of each proposed account and the writing of `tax_criteria_met`: RWB-S7-E6014-APP.
- The pack, the committee route, the approve, reject and defer decisions and the removal of a case: RWB-S7-E6015-APP to RWB-S7-E6020-APP.
- The reconciliation of the approved and posted populations and the write-off exception loop of R-WO-24, R-WO-42 and R-WO-43: RWB-S7-E6023-APP and RWB-S7-E6024-APP.
- The post charge-off treatment of R-WO-29 and later, and the closing of the case: the post charge-off stories of this service.
- The Finance provision feed itself — its transport, address, layout, acceptance codes, retry schedule and exception queue: Finance.
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3).
- The rule package, its rows and versions, and the central decision ledger: rwb-decision (P7).
- The account and ALS facts and the freshness of a data product: rwb-source-data (P1).
- The rights, the scopes and the masking: rwb-access (P4) and the guard of the service template.
- The composite route and the field list of SCR-27: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
