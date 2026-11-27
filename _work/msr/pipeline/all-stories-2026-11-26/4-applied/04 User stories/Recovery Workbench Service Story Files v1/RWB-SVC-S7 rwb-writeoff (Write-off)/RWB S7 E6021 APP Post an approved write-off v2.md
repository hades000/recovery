# RWB-S7-E6021-APP Post an approved write-off

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S7-E6021-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-021 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S7-I |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S7-E6021-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the app story of the posting feature of rwb-writeoff, split from RWB-E6-021 (FEAT-WOF-09). It keeps two of the legacy criteria word for word with their origin tag — AC2, the pack the posting is built from under R-WO-05, and AC4, the record discipline — and it builds the pack-prepared branch of `WriteOffWorkflow` on task queue `rwb-writeoff`, which reads the balance, the provision carried, the route history, the legal and asset state and the residual of a proposed write-off on the rwb-source-data contract (DP-05), records the outcome through the local decision-record library before `write_off` changes (DP-03), moves the WRITEOFF state to `PACK_PREPARED` in schema `rwb_writeoff`, answers the case move, and serves its SCR-27 fragment on the base `/api/recovery/writeoff/v1` (DP-13) behind the gateway-bff composite route (DP-19). The ALS and general-ledger posting itself, the re-post and the provision release — legacy AC1 and AC3 — are RWB-ITG-E6021-ITG's, and the plan's C and X rows are empty while the step consumes rwb-source-data and reads the pack document facts, so the absence is recorded as GAP-3033 with ASM-5067 to -9. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S7-E6021-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As the **Credit Administration officer**, I want **the Workbench to post the write-off to ALS and the general ledger and release the provision**, so that **write-offs follow the criteria and the committee's decision**.

The story is the app half of that sentence. It owns:

- the two legacy criteria of the key that this story keeps, AC2 and AC4, copied verbatim with their origin tag, and the rule, messages and screen they depend on;
- the pack-prepared branch of `WriteOffWorkflow` on task queue `rwb-writeoff` in namespace `rwb-recovery`, the stage child of `CaseWorkflow` owned by rwb-case (context pack workflow row `WriteOffWorkflow`; Temporal and Drools Design slide 13, "Write-off · rwb-writeoff · WO 51");
- the evaluation of R-WO-05 of the WO package on the pack built for the posting track, with balance, provision carried, route history, legal and asset state and residual asserted before the stage may move (Business Rules and Routing Logic v4 D9; FSD S7 A2.9.3.1);
- the read of the account balance and the provision carried, of the asset facts and of the route history on the rwb-source-data contract, one hop with a 2 s budget and a breaker, because only rwb-source-data holds the `recovery.v_ace_*` views (DP-05);
- the WRITEOFF transition of `write_off.state` from `POPULATION_PROPOSED` to `PACK_PREPARED`, and the write of `write_off.decision_log_id`, in schema `rwb_writeoff`;
- the local decision record of the outcome, written through RWB-PLT-E1027-CON before the row changes (DP-03), which is what legacy AC2's second `Then` and AC4 require;
- the answer to rwb-case for the case move `PACK_PREPARED`, with the rule ID and its version, and the prepared posting pack that the ALS and GL crossing consumes;
- the read-only SCR-27 fragment of the write-off stage in its proposed and pack-prepared states, through the gateway-bff composite route (DP-19).

It does not own: the published shapes of the `write_off` element, the POSTING state vocabulary, the consumed rows, the rights, the error set and the fakes, which are RWB-S7-E6021-CON; the crossing to ALS and the general ledger, the posting reference, the rejection and the re-post under R-WO-21 to R-WO-23 and R-WO-44, and the provision release, which are RWB-ITG-E6021-ITG's with legacy AC1 and AC3; the assembly of the pack itself, which is RWB-S7-E6015-APP's under the same rule row; the eligibility scan, the tax criteria and JOB-16, which are RWB-S7-E6013-APP and RWB-S7-E6014-APP's; the committee decision act and API-S7-002, which are RWB-S7-E6018-APP's to -E6020-APP's; the case of record, its route states and the case-move answer, which are rwb-case's (P3); the ACE account, asset and ledger facts, which are rwb-source-data's (P1); the rule package and the ledger, which are rwb-decision's (P7); the posting documents, which are rwb-document's (P5); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

Legacy RWB-E6-021 gave the Workbench one step that posted an approved write-off to ALS and the general ledger, released the provision and recorded the decision. The FSD keeps the objective unchanged — "Posts the write-off to ALS and the general ledger and releases the provision" (FSD S7 A2.9.1) — against the module metric "write-off packs accepted first time, rising each month", measured on the decision log and the Workbench records and reviewed monthly. The problem is unchanged too: write-off populations are assembled by hand each month.

What D-RCV-60 changes is where the posting is built and where the money crossing happens:

- **the write-off stage is this service's.** `write_off` is S7's only table, in `rwb_writeoff` (context pack ownership row `write_off`; TSD S7 T3.1, DF-FIN-010 to DF-FIN-020), so the stage state, the record reference and the amount posted are written here and nowhere else.
- **the money crossing is not this service's.** The connection matrix gives S7 one REST edge, to rwb-source-data, and one Temporal edge to rwb-payment; the module TSD publishes no external interface at all (TSD S7 T5.1, all None). The ALS and general-ledger crossing, the posting reference, the rejection and the re-post therefore need the real systems on both sides and sit on the wave 4 harness, which is why the plan split legacy AC1 and AC3 to RWB-ITG-E6021-ITG (GAP-3033; ASM-5070).
- **the pack is prepared here, not by hand.** The posting can only be built from a pack that carries the balance, the provision carried, the route history, the legal and asset state and the residual, and every one of those five facts belongs to an owner: the balance, the provision and the asset facts are ACE data read on the rwb-source-data contract (DP-05), the route history is the interaction ledger, which the default ruling gives to rwb-source-data (DP-18). This story asserts the five facts before the stage moves, and it reads no `v_ace_*` view and holds no ACE grant (ASM-5072).
- **the pack assembly itself is another story's.** RWB-S7-E6015-APP builds the pack under the same R-WO-05 row that FSD A2.9 also lists, and R-WO-05 is one rule with one outcome: this story applies it on the posting track, asserts the pack content, records the outcome and moves the state, and it writes no second pack builder, no second document reference and no second agent run (ASM-5068).
- **the ledger stays with its owner.** DP-03 keeps a local record in the caller's transaction and rwb-decision keeps the central ledger on `rwb.decision-record.v1`; `write_off.decision_log_id` carries the record this service writes (ASM-5040).
- **the step publishes nothing.** The service's single event EV-24 `WriteOffApproved` is the committee's approval (RWB-S7-E6018-APP); a posting that has not yet crossed to ALS has no approved event of its own (ASM-5069).

The binding values are unchanged and are not written in code: the posting window, the month-end close window, the retry limit, the reference data behind the pack and the rule row itself are rows of the package, of parameters and of reference data, read with their version.

The delivery is the plan's: this key is EP06 and therefore wave 4, and rwb-writeoff is created in wave 4 (Architecture v5), so the two agree and the release 30 April 2027 is copied unchanged and marked tentative (ASM-5035).

### 3. Preconditions

- RWB-S7-E6021-CON is published: the `write_off` element, the WRITEOFF state vocabulary including the POSTING values, the consumed rwb-case and rwb-source-data rows, the rights, the error set and the fakes are baselined and handed to this story.
- The rwb-source-data contract is available for the fake: the account balance and the provision carried (`v_ace_account`), the asset facts (`v_ace_npa_asset`) and the route history from the interaction ledger. No source publishes the operation names, so they are Not specified in the source documents (GAP-3033; ASM-5067, ASM-5072).
- The rwb-case contract is available for the fake: the case reference and the stage state (`GET /cases/{caseId}` family) and the case-move answer. The connection matrix shows no REST edge from S7 to P3, so the case facts also arrive in the stage workflow's input from the parent `CaseWorkflow` and the outcome is answered on the same boundary (ASM-5037).
- The rwb-decision WO package read is available for the fake: R-WO-05 at its version in force with the reference data the pack reads; the operation name is Not specified in the source documents (GAP-3033; ASM-5067).
- RWB-S7-E6015-APP has published the pack element and the pack document reference of the same service, so this story asserts the pack instead of building it (ASM-5068).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-27 Write-off proposal reaches this service through the gateway-bff composite route, one hop (DP-19).
- `write_off` exists in schema `rwb_writeoff` from the DB story of this service, with the columns of DF-FIN-010 to DF-FIN-020 and the standard record columns of TSD S7 T3.0; this story adds no table, no column and no migration.
- The service runs as its own login on schema `rwb_writeoff`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case.recovery_case`, `rwb_decision.rule_row` or a `v_ace_account` read is refused by the database and fails the boundary test (DP-01, DP-02).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S7-E6021-CON when its tests pass.

### 4. Flow

1. The committee approves the write-off and the case sits in `APPROVED` on the write-off stage; the posting track opens on the month-end close window that R-WO-20 names, and RWB-S7-E6021-APP builds the pack the posting is made from. That window and its timer belong to the harness and to the package, not to this step (ASM-5070).
2. The pack-prepared branch of `WriteOffWorkflow` on queue `rwb-writeoff` receives the case and the write-off reference from the parent `CaseWorkflow` and reads the `write_off` row in `rwb_writeoff`: the case reference, the amount, the tax criteria flag and the committee date.
3. `SourceDataClient` reads, one hop with a 2 s budget and a breaker, the account balance and the provision carried, the asset facts and the route history of the case on the rwb-source-data contract. No component of this service reads a `v_ace_*` view (DP-05).
4. `RulePackageClient` loads the WO package version in force from rwb-decision; `WriteOffPackEvaluator` applies R-WO-05 to the five pack facts and computes the residual the rule names.
5. Where a fact is absent or stale, the step holds: it writes nothing, reports the missing element or the stale date to the parent, and the case stays where it is (X4, X6).
6. `WriteOffDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**, with the case reference, the write-off reference, the rule ID and its version, the inputs reference, the five pack facts and the outcome. A failed write stops the step with nothing changed (DP-03; legacy AC2 and AC4).
7. `WriteOffPackWriter` updates the `write_off` row in one `rwb_writeoff` transaction with the record, the idempotency row and the optimistic lock of `version`: `state` becomes `PACK_PREPARED` and `decision_log_id` (DF-FIN-012) holds the identifier the library returns. `posted_date` (DF-FIN-016) and the GL columns are not written by this step; they are written once ALS and the general ledger answer (ASM-5070).
8. `CaseMoveAnswer` answers rwb-case with the move `PACK_PREPARED`, the rule ID, the version and the decided-at time, and hands the prepared pack to the posting track; rwb-case writes the case of record.
9. A repeated pack for the same write-off, rule and version writes nothing, answers no second move and counts the repeat.
10. SCR-27 Write-off proposal in its proposed and pack-prepared states reads the stage through the gateway-bff composite route, next to the case route state of rwb-case and the decision records of this service (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing is written: no state, no record reference and no case-move answer leaves the service | MSG-P7-003 | AC4, TC-E6-021-04, TC-E6-021-06 |
| X2 | The role does not hold the Write-off and posting right of the read or of the act | 403 before any read or write, and the screen fragment refuses the action | MSG-P4-002 | AC2, TC-E6-021-05 |
| X3 | The write-off is not in `POPULATION_PROPOSED`, or has already left the population | 409 and nothing is written; a case that has already moved is not re-packed | None | AC2 |
| X4 | The tax criteria version is absent, or an ACE data product of the pack is stale after a late or failed ACE batch | The step holds, writes nothing and reports the version or the date it waits on; the branch resumes on the next fresh answer | MSG-S7-001, MSG-P1-001 | AC2, TC-E6-021-02 |
| X5 | A required pack fact is absent: the balance, the provision carried, the route history, the legal state, the asset state or the residual | Nothing is written and the missing element is reported to the parent; the case stays in `POPULATION_PROPOSED` | MSG-GEN-001 | AC2 |
| X6 | The rwb-source-data, rwb-case or rwb-decision contract does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and no move is answered, and the caller sees 503 | None | AC2 |
| X7 | The same pack arrives twice for the same write-off, rule and version | One record, one update and one case-move answer; the repeat is counted | None | AC2 |
| X8 | A component, a statement or a test reaches another service's schema, a queue table or a `v_ace_*` view | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR6 |

X1 and X2 are the exception paths of RWB-E6-021 carried onto the split, X3 to X7 are the paths the rule package, the freshness and the call types add, and X8 is the DP-01, DP-02 boundary. The posting window, the close window, the retry limit and the reference data behind the pack are values in force in the package and in parameters, so none is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S7-E6021-CON, the rwb-source-data, rwb-case and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P1, P3 or P7 |
| Negotiable | The activity name, the decision code and the shape of the stage outcome are this story's choice; the rule, the messages, the screen, the state values and the `write_off` columns are fixed |
| Valuable | A proposed write-off becomes a prepared posting pack with its five facts and its decision recorded, so no pack is built by hand and the share accepted first time is measurable |
| Estimable | One workflow branch, one evaluator, three clients, one record write, one row update, one case-move answer and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on a synthetic write-off and synthetic source-data answers through the contract fakes, plus the failed-record and access cases |

### 7. Acceptance criteria

```gherkin
Feature: Post an approved write-off

  Background:
    Given write-off "WO-2027-000321" carries case "RC-2027-000721" of the write-off stage
    Given the WO rule package is in force at its version and carries R-WO-05
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC2 Rule R-WO-05 (legacy RWB-E6-021 AC2)
    Given the rwb-source-data contract mock returns the balance and the provision carried of the account of case "RC-2027-000721"
    Given the rwb-source-data contract mock returns the route history, the legal state and the asset state of case "RC-2027-000721"
    Given the rwb-decision contract mock returns the WO package in force with R-WO-05
    Given a case in state POPULATION_PROPOSED
    When pack built
    Then write-off agent prepares the pack: balance, provision carried, route history, legal and asset state, residual
    Then the case moves to PACK_PREPARED

  Scenario: AC4 Not recorded (legacy RWB-E6-021 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The two criteria are the legacy criteria of RWB-E6-021 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the legacy wording of `pack built` and `the action is taken` all stand. The cross-service parts are mocked, so AC2 carries three `Given the <service> contract mock returns <x>` lines before its legacy `Given`; those three lines are the only additions, and every value of the legacy `Then` — balance, provision carried, route history, legal and asset state, residual — is kept. What the legacy lines describe now happens in three places: rwb-source-data owns the balance, the provision carried, the asset facts and the route history, rwb-decision owns the WO package and R-WO-05, and this story asserts the five pack facts, records the decision and writes `state` and `decision_log_id` on the `write_off` row. Legacy AC2 says "the case moves to PACK_PREPARED": the case route state is rwb-case's and is answered, while the named value is also the WRITEOFF state this service writes on `write_off.state` (ASM-5037). AC2's "decision log" in AC4 is read as the local decision record of DP-03 written before the row changes, plus the ledger entry rwb-decision writes (ASM-5040).

Legacy AC1 (the ALS and general-ledger posting and the provision release) and legacy AC3 (the re-post after a rejection) are not owned here: the plan gives them to RWB-ITG-E6021-ITG, because both need the real systems on the far side and the connection matrix gives this service no external edge. This story builds the pack and the record those criteria consume.

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-WO-05 | Write-off | D9 | POPULATION_PROPOSED | PACK_BUILT | Any | Write-off agent prepares the pack: balance, provision carried, route history, legal and asset state, residual | PACK_PREPARED | Write-off team | Agent Runtime, Document Hub | 3 working days |

The row is the row of the Business Rules and Routing Logic v4, copied character for character, and it is the row of the WRITEOFF machine of TSD S7 T4. Its owner column is a role of the business and not a service: the agent run and the document index are rwb-agent's and rwb-document's and are consumed, the case move is answered to rwb-case, and the 3-day timer is read as a package value. R-WO-20 to R-WO-23, R-WO-25 and R-WO-44 — the posting task, the posting reference, the rejection, the re-post and the provision release — are the rows of RWB-ITG-E6021-ITG and are named here only as the consumers of the prepared pack (ASM-5070).

| ID | Rule | Source |
|---|---|---|
| BR1 | The write-off stage state and the record reference are this service's: `state` and `decision_log_id` are columns of `write_off` in `rwb_writeoff`, and no other service writes them | Context pack ownership row `write_off`; TSD S7 T3.1 (DF-FIN-012, T3.0 `state`); DP-01 |
| BR2 | The decision is recorded before the `write_off` row changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S7 T2 ("writes the decision log entry before any change"); legacy RWB-E6-021 AC2 and AC4 |
| BR3 | The case, its route states and the case move stay with rwb-case: this service reads the state, answers the move and writes no `recovery_case` row | Context pack ownership rows; legacy Data table `recovery_case`; ASM-5037 |
| BR4 | The balance, the provision carried, the asset facts and the route history are read on the rwb-source-data contract; this service holds no `v_ace_*` grant and reads no ACE table or view | DP-05, DP-01, DP-02; context pack naming rules; ASM-5072 |
| BR5 | The rule package, its version and the ledger stay with rwb-decision: this service reads the package in force and writes its local decision record, and no rule row and no ledger entry of its own | DP-03; ASM-5067, ASM-5040 |
| BR6 | No cross-schema join and no foreign key leaves `rwb_writeoff`; the case reference and the account reference are identifiers of other services' facts | DP-01, DP-02; TSD S7 T3.3 |
| BR7 | Only the pack-prepared outcome is written here: `posted_date`, `gl_product`, `responsibility_center`, `cost_center` and `recovered_after` keep their values until the posting crossing and the post charge-off stories write them | TSD S7 T3.1; FSD S7 A2.9.3.1; ASM-5070 |
| BR8 | Every value a business person may change is reference data, parameters or a rule row read with its version: the posting and close windows, the retry limit, the pack reference data and the state list | FSD S7 A2.9.3.1 BR-S7-009; Template and Rules v1 §R3 default rulings; ASM-5071 |
| BR9 | The pack is asserted, not rebuilt: the five facts are read and checked, and a second pack builder, a second document index and a second agent run are refused by the review | FSD S7 A2.3.3.1 and A2.9.3.1 (the same R-WO-05 row); ASM-5068 |
| BR10 | The same pack twice, or the same `Idempotency-Key` twice, writes once and answers the case move once | TSD S7 T-A.2; Architecture v5 slide 11 |
| BR11 | No person name, contact value or identity number enters `rwb_writeoff`, the decision record, a log or a workflow input | Template and Rules v1 §R7.2 (s17); context pack naming rule on PII |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR3). What this story writes is the WRITEOFF state of the `write_off` row.

| From (WRITEOFF, `write_off.state`) | Event | Condition | To |
|---|---|---|---|
| `POPULATION_PROPOSED` | `PACK_BUILT` under R-WO-05 | the balance, the provision carried, the route history, the legal and asset state and the residual are present | `PACK_PREPARED`, with the record reference written and the case move answered |
| Any state the rule does not name | Any pack | X3 | Unchanged, and the reason is reported to the parent |
| `PACK_PREPARED` and later | Any pack | — | Not written here: `WITH_COMMITTEE`, `APPROVED`, `POSTING_PENDING`, `POSTED`, `POSTING_REJECTED`, `WRITEOFF_EXCEPTION` and `PROVISION_RELEASED` belong to the committee, posting and integration stories |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The pack arrives for a write-off in `POPULATION_PROPOSED` | The package in force is loaded | Evaluating |
| Evaluating | R-WO-05 fires | The five pack facts are present and fresh | Applying |
| Applying | The record, the `write_off` row and the case move are written | The transaction commits | Waiting for the next pack |
| Applying | The record write or the transaction fails | X1 | Waiting, nothing changed |

The 27 states of the WRITEOFF machine are those of TSD S7 T4; `SCAN_DUE`, `SCAN_HELD`, `POPULATION_PROPOSED`, `PACK_PREPARED`, `PACK_INCOMPLETE`, `WITH_COMMITTEE`, `APPROVED`, `POSTING_PENDING`, `POSTED`, `POSTING_REJECTED` and `PROVISION_RELEASED` are the ones this key's stories read or write, and the values T4 does not print carry the placeholder (ASM-5037).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-WRITEOFF, write-off team member | Write-off and posting CRU in TSD S7 T6.1: reads the stage and the pack facts; the C right it holds is exercised on the scan story |
| RW-CREDITAD, Credit Administration officer | Write-off and posting CRUA: reads the stage and the prepared pack; the A right is exercised on API-S7-002 at RWB-S7-E6018-APP |
| RW-WOCOMM, write-off committee member | Write-off and posting RA: reads the stage and the prepared pack; the approval is API-S7-002's |
| RW-PRODHEAD, product head, and RW-FINANCE, Finance and CFO delegate | Write-off and posting RA: read the stage, the prepared pack and its provision carried |
| RW-FRAUD, RW-DEBTSALE, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Write-off and posting R: read only, in scope |
| SY-CASEWF, SY-RULES, SY-AGENT, SY-DATALOAD | Write-off and posting R and U as T6.1 gives them: the service identities run the step and are subject to the same checks |
| rwb-writeoff service identity | Runs the branch, evaluates R-WO-05, writes the record and the `write_off` row and answers the case move; no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S7 T6.1 and the two rows of the legacy Permission checks table, and nothing wider: the legacy table gives the A right to RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE and the C right to RW-WRITEOFF and RW-CREDITAD, which is what T6.1's RA, CRUA and CRU rows say. No role of this story holds an operation right, because the pack-prepared branch is unattended and every act on the population and the committee is taken on the operations of other stories of this service (ASM-5071). FSD S7 A2.9.3.3 names "None; runs unattended" as the primary user and "Credit Administration officer" as the other user, which is the reading used here. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard of the access service is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-FIN-010 | write_off (S7, `rwb_writeoff`) | id | Read, the write-off reference the record and the answer carry |
| DF-FIN-011 | write_off (S7, `rwb_writeoff`) | case_id | Read, the case reference the source read and the move carry |
| DF-FIN-012 | write_off (S7, `rwb_writeoff`) | decision_log_id | Write, the identifier the local decision-record library returns (ASM-5040) |
| DF-FIN-013 | write_off (S7, `rwb_writeoff`) | amount | Read, the amount the pack and the record carry |
| DF-FIN-014 | write_off (S7, `rwb_writeoff`) | tax_criteria_met | Read, the tax criteria result of RWB-S7-E6014-APP; it gates the pack (VR-S7-009-1) |
| DF-FIN-015 | write_off (S7, `rwb_writeoff`) | committee_date | Read, the approval date the pack carries; written by RWB-S7-E6018-APP |
| DF-FIN-016 | write_off (S7, `rwb_writeoff`) | posted_date | Not written here: it is written once ALS and the general ledger answer (ASM-5070) |
| DF-FIN-017, DF-FIN-018, DF-FIN-019, DF-FIN-020 | write_off (S7, `rwb_writeoff`) | responsibility_center, cost_center, gl_product, recovered_after | Not written here: the posting crossing and the post charge-off stories write them |
| Standard columns | write_off (S7, `rwb_writeoff`) | `state`, `version`, `updated_at`, `updated_by`, `created_at`, `created_by`, `is_active` | Write `state`, `updated_at`, `updated_by` and the optimistic lock of `version` on the update |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_writeoff`) | rule id, rule version, inputs reference, the five pack facts, outcome, decided at | Write through the local library, before the `write_off` row changes |
| DF-ACE-001 to DF-ACE-042 | v_ace_account (P1 rwb-source-data) | account_key, account_code, total_balance and the rest | Not read as a view: the balance and the provision carried arrive on the rwb-source-data contract (GAP-3033; ASM-5072) |
| DF-ACE-208 to DF-ACE-219 | v_ace_npa_asset (P1 rwb-source-data) | asset_ref, asset_key, asset_code, book_value and the rest | Not read as a view: the asset facts arrive on the rwb-source-data contract (ASM-5072) |
| DF-INT-001 to DF-INT-013 | interaction (P1 rwb-source-data, ledger owner) | id, case_id, person_key, occurred_at, channel, direction and the rest | Not read as a table: the route history arrives on the rwb-source-data contract (DP-18; ASM-5067) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and the rest | Not read as a table: the case reference and the state arrive on the rwb-case read and in the stage input, and the move is answered (ASM-5037) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (P7) | id, case_id, decision_code, rule_id, rule_version and the rest | Not written here: rwb-decision writes the ledger entry (ASM-5040) |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, from_state, event_code and the rest | Not read as a table: the rule row is governed in rwb-decision and loaded here as the package in force |

Field IDs are those of TSD S7 T3.1 and the Logical Data Model and Data Dictionary v9. **No new table, no new column and no migration**: `write_off` arrives with the DB story of this service, this story writes two of its existing columns, and `decision_record`, `idempotency_key` and `outbox_event` are platform library objects created in `rwb_writeoff` by the library's own migration (DP-03). The legacy Data table lists six entities; five of them are other services' and are consumed on their contracts as the rows above state.

**No personal data.** The rows this story writes carry identifiers, an amount, a code and a rule version. No name, address, contact value or identity number enters `rwb_writeoff`, the decision record, a log or a workflow input, and the fixture data of the tests is synthetic.

### 12. Contract

#### 12.1 REST operations provided

None. Owner rwb-writeoff (S7); base `/api/recovery/writeoff/v1` (DP-13). The two operations of this legacy key are declared by other stories of the same service: `POST /write-off-scans` (API-S7-001, Write-off and posting right C) is RWB-S7-E6013-APP's, and `POST /write-offs/{writeOffId}/committee-decision` (API-S7-002, right A) is RWB-S7-E6018-APP's with the reject and defer outcomes at RWB-S7-E6019-APP and RWB-S7-E6020-APP. The pack-prepared branch is a workflow step on the arrival of the pack, so this story provides no operation; a build that declares one here fails the absence test of the contract (GAP-3033; ASM-5071). No read of the stage is published either: SCR-27 shows it through the gateway-bff composite route, and the operation behind the list is Not specified in the source documents (GAP-3033; ASM-5071).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case reference and the stage state; read only, faked. The connection matrix shows no REST edge from S7 to P3, so the same facts also arrive in the stage input from the parent `CaseWorkflow` (ASM-5037) |
| The account and asset read (operation name Not specified in the source documents (GAP-3033; ASM-5067)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The balance and the provision carried of the account, and the asset facts of the case; faked |
| The route-history read of the interaction ledger (operation name Not specified in the source documents (GAP-3033; ASM-5067)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The route history of the case; the ledger is rwb-source-data's under the default ruling (DP-18); faked |
| The read of the WO rule package version in force (operation name Not specified in the source documents (GAP-3033; ASM-5067)) | `/api/recovery/decision/v1` | P7 rwb-decision | The package version and the row R-WO-05 with the reference data the pack reads; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter, a breaker per downstream and no retry of its own (ADR-020). The four rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-3033 with ASM-5067. The pack document index and the agent run that build the pack are read inside RWB-S7-E6015-APP and are not consumed here (ASM-5068).

#### 12.3 Events published

None. The service owns event EV-24 `WriteOffApproved` on topic `rwb.writeoff.events.v1`, and it is the committee's approval, which RWB-S7-E6018-APP publishes. The stage moves to `PACK_PREPARED`, which no event of the catalogue names, so this step writes no outbox row, holds no producer of its own and fails the absence test if it adds an event (DP-09 is not in this story's pattern set; ASM-5069).

#### 12.4 Events consumed

None. No source gives rwb-writeoff a consumed event for this step: the pack arrives from RWB-S7-E6015-APP inside the same service and the account, asset and case facts arrive on their owners' contracts. This story holds no consumer group, no subscription and no inbox row of its own, and a build that adds one fails the absence test (ASM-5069).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case per stage, the stage child of `CaseWorkflow` | `rwb-writeoff` in namespace `rwb-recovery` | Input: the case, the write-off, the amount, the tax criteria flag, the committee date and the package in force; signals: the pack and the source-data answer |
| The pack-prepared branch of `WriteOffWorkflow` | Workflow branch, the step from the pack to `PACK_PREPARED` | `rwb-writeoff` | Applies R-WO-05, writes the record and the row and reports the stage outcome to the parent |
| `prepareWriteOffPackForPosting` | Activity, the one step of this story | `rwb-writeoff` | The case, the write-off, the source-data answer and the package answer in; the rule ID with its version, the state, the record reference and the case move out, in one transaction |

No child workflow of this service and no approval workflow exists in this step: the committee's act is the `ApprovalWorkflow` of the kit on the P7 queue, started by RWB-S7-E6018-APP. The activity name is a target design choice of this story and is fixed by no source document; the trigger is read as the arrival of the pack for a write-off in `POPULATION_PROPOSED`, because the FSD declares the scan as the module's only background event (FSD S7 A2.9.4.4). The rwb-decision package read is reached as an activity on that owner's queue, as the connection matrix row S7 gives it, and is not a REST call of this story.

#### 12.6 Schedules

None. The branch runs from the pack and owns no Temporal Schedule, no Quartz row and no shared job table. JOB-16, the monthly write-off scan on the third working day on the ACE batch-complete record for ALS, is RWB-S7-E6013-APP's. The month-end close window and the posting window of R-WO-20 are timer values of the package and are read by the posting track, which is RWB-ITG-E6021-ITG's; they are not a Schedule of this service, and their calendar and cadence are Not specified in the source documents (GAP-3033; ASM-5070).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of the balance on a case; this story updates `state` and `decision_log_id` |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated pack and the outcome it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | Created in this schema by the library and used by the stories that publish; this step writes no row of it (12.3) |

Not owned and never read as a table: `recovery_case` (P3), `rule_row` and `decision_log_entry` (P7), `interaction`, `account_ext` and every `v_ace_*` view (P1), `document` (P5), `notice` (P6), `posting` and `proceeds` (P8 and S9). No foreign key leaves the schema and `write_off.case_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data account and asset fake | The balance and the provision carried of `RC-2027-000721`, the asset facts, a stale product with its date, and an account with no answer beyond 2 s | AC2, X4, X5, X6 |
| rwb-source-data ledger fake | The route history of the case, and a case with no route history | AC2, X5 |
| rwb-case state fake | The states `POPULATION_PROPOSED` and `PACK_PREPARED` of case `RC-2027-000721`; a case in a state the rule does not name | AC2, X3 |
| rwb-case case-move fake | The move `PACK_PREPARED` accepted, and a move refused because the case is not in the state the rule expects | AC2, X3 |
| rwb-decision rule-package fake | The WO package at its version in force with R-WO-05 and its reference data | AC2 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-27 answer for write-off `WO-2027-000321`, with the write-off facts of this service read once | AC2 |

The fakes are test-only and are replaced by the real services in SIT. The unpublished names of the source-data and package reads are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-3033; ASM-5067).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 4 consumed | The rwb-case state read, the rwb-source-data account-and-asset read and ledger read, and the rwb-decision package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `WriteOffApproved` (EV-24) is the approval story's; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow, 1 branch, 1 activity | `WriteOffWorkflow` and its pack-prepared branch on `rwb-writeoff`, with its `prepareWriteOffPackForPosting` activity; no Schedule and no child workflow |
| File | None | No file is read, built or delivered here; the ALS and general-ledger crossing is the integration story's and the pack documents are rwb-document's (P5) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.writeoff`, module `posting`, Java package `th.co.scb.ace.workbench.recovery.writeoff.posting`; front end `src/modules/recovery/writeoff/WriteOffPack.tsx`, the fragment SCR-27 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | the monolith API base | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the `write_off` update commit together or not at all, and the failed write is MSG-P7-003. DP-05 is the whole of the legacy marker in this story: the legacy Data table names `v_ace_account`, `v_ace_npa_asset` and `interaction`, and the target reads all three on rwb-source-data's contract, because only that service holds the `recovery.v_ace_*` views and this service holds no ACE grant. DP-13 moves the base of the key's two operations, neither of which this story provides, so it adds no element here. DP-19 is how SCR-27 reaches this service, one hop through the gateway, and this story fixes the fragment only. No other pattern is claimed: the case, the source data and the package are consumed contracts and the ALS crossing is the harness's, so DP-09, DP-10, DP-11, DP-16 and DP-20 stay off this table and their absence from the plan's rows is recorded in the registers (GAP-3033; ASM-5067, ASM-5069, ASM-5070).

**Dependencies the table adds and the plan does not hold.** The pattern table adds the two H rows the plan already carries, `RWB-PLT-E1027-CON` and `RWB-PLT-N001-CON`. DP-05 adds no row by the table's own rule, yet the story reads rwb-source-data's contract, and the four consumed rows are class C dependencies in fact while the plan's C and X rows are None, so the story builds against their documents and fakes on Day 1 and the absence is recorded (GAP-3033; ASM-5067).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `WriteOffWorkflow` pack-prepared branch | Workflow | Waits for the pack, loads the package in force, applies R-WO-05 and reports the outcome to the parent |
| `prepareWriteOffPackForPosting` | Activity | The one step: read the case and the write-off, read the pack facts, evaluate the rule, write the record and the row and answer the case move |
| `WriteOffPackEvaluator` | Service | The rule evaluation against the WO package version in force, with the residual and the reference data read as package values |
| `SourceDataClient` | Client | The account, asset and ledger reads of rwb-source-data; one hop, 2 s, breaker |
| `CaseStateClient` | Client | The case state read and the case-move answer of rwb-case; one hop, 2 s, breaker |
| `RulePackageClient` | Client | The WO package version in force of rwb-decision; one hop, 2 s, breaker |
| `WriteOffDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID and the version before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `WriteOffPackWriter` | Repository | Updates `state` and `decision_log_id` in one `rwb_writeoff` transaction, with the idempotency row and the optimistic lock |
| `WriteOffPackController` | Controller | The read behind the SCR-27 fragment, the capability area and right, the scope and the problem mapping of 400, 401, 403, 404 and 503 |
| `WriteOffPack` | React component | Shows the stage, the five pack facts and the pack-prepared state on SCR-27, read only, with the refusal and failed-record states |

**Database and migrations.** No Flyway file. `write_off` arrives with the DB story of this service, and the decision record, the idempotency key and the outbox are library objects created in `rwb_writeoff` by the library's migration (DP-03). No column is added: `state` is the standard record column of TSD S7 T3.0 and `decision_log_id` is DF-FIN-012.

**Configuration and reference data.**

- The pack reference data behind R-WO-05 and the state list of the WRITEOFF machine, read as package values and reference data at their version, never as constants.
- The posting and month-end close windows and the retry limit of the posting track, read as parameters of the package; their values and cadence are Not specified in the source documents (GAP-3033; ASM-5070).
- The capability area "Write-off and posting" and its rights are access rows of rwb-access, read through the guard; the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The pack-prepared branch of `WriteOffWorkflow` and its input record, registered on `rwb-writeoff` as the stage child of `CaseWorkflow`, with the pack as its trigger.
2. `SourceDataClient` against its fake, with the account, asset and ledger reads, the 2 s budget and the stale and missing paths (AC2, X4, X5, X6).
3. `CaseStateClient` against its fake, with the state read and the move answer (AC2, X3).
4. `RulePackageClient` and `WriteOffPackEvaluator` over the WO package, with R-WO-05 and the no-fire path (AC2).
5. `WriteOffDecisionRecordWriter` against the library stub, with the failed-write path (AC4, X1).
6. `WriteOffPackWriter` with the one transaction, the two columns, the idempotency row and the optimistic lock (AC2, X7).
7. `CaseMoveAnswer` and the parent signal, with the `PACK_PREPARED` move (AC2).
8. The read behind the SCR-27 fragment, with the rights, the scope and the problem mapping (AC2).
9. `WriteOffPack` and the screen fragment through the composite route fake (AC2).
10. The boundary test: no statement outside `rwb_writeoff`, no `v_ace_*` read, no write to `rwb_case`, `rwb_decision`, `rwb_source_data` or a queue table (X8, BR3, BR4, BR6).

**Feature flag.** `rwb.writeoff.posting-pack-v1`, read as a flag of the platform library; off means the branch holds the pack, writes nothing and answers no move, and the other stories of the service are unaffected.

**Done when.** The tests of section 16 pass, the branch runs from a synthetic pack in SIT, R-WO-05 produces its record, its state and its answer, a repeated pack writes once, a forced record failure changes nothing, no `recovery_case`, `rule_row`, `interaction` or `v_ace_*` read exists in the build, and SCR-27 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | Carried from the legacy message set of this key. It names the tax criteria version, which is the scan's gate (R-WO-03) and RWB-S7-E6013-APP's path, so no path of this story raises it; the tax criteria flag it reads is the gate of the pack (VR-S7-009-1) | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | A required field of the pack or of a consumed request is absent or invalid (X5) | Enter {field}. |
| MSG-P4-002 | A role without the Write-off and posting right reads the stage or tries the act (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the `write_off` row changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | A pack fact is stale after a late or failed ACE batch (X4), and the freshness arrives on the rwb-source-data answer | {product} is from {date}. Today's ACE batch has not arrived. |

The first four message IDs are those of the legacy message set of this key, and MSG-P1-001 is the message of VR-S7-009-1 in FSD S7 A2.9.3.1; the text is the legacy and FSD wording, copied unchanged, and no message is reworded or added.

### 15. Screens and states

SCR-27 Write-off proposal — "the monthly population, the pack per case and removals with reasons", first in E6 (FSD S7 Screens) — is the screen of this step, in its scan, proposed, in-committee and approved states on the legacy screen table. It is served through the gateway-bff composite route (DP-19): the route calls this service for the write-off row, its stage state and the five pack facts, rwb-case for the case and its route state, and rwb-decision for the decision records. This story fixes the write-off answer and the screen fragment; the composite route specification and the screen field list belong to RWB-PLT-N001-CON, and the population operation behind the list is a placeholder (ASM-5071).

The states this story produces are the stage state of the write-off on SCR-27 — pack prepared with the five facts and the decision record — and the states it shows: refused with MSG-P4-002, not recorded with MSG-P7-003, held as stale with MSG-P1-001, and held with the missing element of MSG-GEN-001. The in-committee and approved states belong to the committee decision stories of this service, and the posted, rejected and provision-released states belong to the posting track and its integration story.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-021-01 | AC1 (RWB-ITG-E6021-ITG) | Integration | The posting of write-off `WO-2027-000321` to ALS and the general ledger and the provision release; carried with the integration story that owns the criterion, and the app half is the prepared pack asserted in TC-E6-021-02 |
| TC-E6-021-02 | AC2 | Integration | Case `RC-2027-000721` at `POPULATION_PROPOSED`; the five pack facts on the rwb-source-data fakes, the `PACK_PREPARED` state, the record and the move asserted |
| TC-E6-021-03 | AC3 (RWB-ITG-E6021-ITG) | Integration | The re-post of a rejected posting under R-WO-23 and R-WO-44; carried with the integration story that owns the criterion |
| TC-E6-021-04 | AC4 | Component | The decision-record stub stopped; nothing written, no move answered and MSG-P7-003 shown |
| TC-E6-021-05 | Access | Component | A role without the Write-off and posting right; 403 with MSG-P4-002 and no read |
| TC-E6-021-06 | Principle 5 | Component | A forced decision log write failure at the moment of the row update; no column changed and no move answered |

The six legacy cases are the legacy cases of RWB-E6-021 in their legacy order, with the Level column added. TC-E6-021-02 and -03 map to `Integration` because they cross the rwb-source-data, rwb-case and rwb-decision boundaries, and -01 and -03 name the integration story that owns their criterion, so the same legacy case is proved once against the real systems and once against this service's half. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; no `-ITG` copy is written here, and the cross-service journey of the key belongs to the wave 4 harness.

### 17. Guardrails

- No business value in code: the posting and close windows, the retry limit, the pack reference data, the state list and the rule row stay data, reference data or the rule package, never a constant, a default or a branch of the build.
- No personal data in `rwb_writeoff`, in a workflow input or in a log: identifiers, an amount, a code and a rule version only, and every fixture is synthetic.
- The ACE data only through an owner's contract: this service holds no `v_ace_*` grant and reads no ACE table or view, and a build that adds one fails the boundary test (DP-01, DP-02, DP-05).
- The case and its route states stay with rwb-case, the account, asset and ledger facts with rwb-source-data, and the package and the ledger with rwb-decision: no `recovery_case` row, no `interaction` row, no rule row and no ledger entry is written here (BR3, BR4, BR5).
- The pack is asserted, not rebuilt: a second pack builder, a second document index or a second agent run fails the review (BR9).
- The ALS and general-ledger crossing, the re-post and the provision release stay with RWB-ITG-E6021-ITG: this step declares no file, no interface and no posting reference (ASM-5070).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no second event on the topic and no approval or queue table of this service's own.
- The decision is recorded before the change and the record and the update commit together; a build that writes the row first fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S7-002 | The committee pack is prepared from case and provision data with no manual assembly (Must, E6); this story asserts the five pack facts on the owners' contracts and builds no second pack | The pack-prepared branch and the `SourceDataClient` reads | TC-E6-021-02 |
| REQ-S7-005 | Approved write-offs post to the core system and the general ledger, the provision is released, and completeness is published (Must, E6); this story owns the app half — the pack the posting is built from and the record that gates it — and the crossing itself is RWB-ITG-E6021-ITG's (GAP-3033; ASM-5070) | The record written before the row change, the `PACK_PREPARED` state and the case move | TC-E6-021-01, TC-E6-021-04 |
| ADR-013 | 19 services inside ACE | rwb-writeoff as the owner of the write-off row and its stage state | TC-E6-021-02 |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-E6-021-06 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget | TC-E6-021-02 |
| ADR-022 | Local decision record plus central ledger | The decision record written before the change, with the ledger entry in P7 | TC-E6-021-04, TC-E6-021-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-021, disposition Split (rework) |
| Legacy criteria | AC2 and AC4, owned word for word by this story; AC1 and AC3 owned by RWB-ITG-E6021-ITG |
| Test cases | TC-E6-021-01 to TC-E6-021-06 |
| Feature and screens | FEAT-WOF-09 Post an approved write-off, SCR-27 Write-off proposal |
| Rules | R-WO-05, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes of the `write_off` element, the state vocabulary, the consumed rows, the rights, the error set and the fakes: RWB-S7-E6021-CON.
- The ALS and general-ledger posting, the posting reference, the rejection and the re-post under R-WO-20 to R-WO-23 and R-WO-44, the provision release under R-WO-25 and the completeness publication, with legacy AC1 and AC3: RWB-ITG-E6021-ITG (ASM-5070).
- The assembly of the pack, its document index and its agent run under the same R-WO-05 row: RWB-S7-E6015-APP (ASM-5068).
- The monthly eligibility scan, the tax criteria and JOB-16, and API-S7-001: RWB-S7-E6013-APP and RWB-S7-E6014-APP.
- The removal of a case by the team, the committee decision act API-S7-002, the approve, reject and defer outcomes and the escalation R-WO-12: RWB-S7-E6016-APP and RWB-S7-E6018-APP to RWB-S7-E6020-APP.
- The case of record, its route states and its move: rwb-case (P3), whose answers this story consumes and fakes (ASM-5037).
- The account balance, the provision carried, the asset facts, the route history and the `interaction` ledger: rwb-source-data (P1) (ASM-5067, ASM-5072).
- The WO rule package, its version and the ledger: rwb-decision (P7) (ASM-5067, ASM-5040).
- The posting documents and their custody: rwb-document (P5); the notices to customers: rwb-comms (P6); the payment posting of a recovery after charge-off: rwb-payment (P8).
- The gateway-bff composite route and the screen field list of SCR-27: RWB-PLT-N001-CON and the edge stories.
- The provisioning feed to Finance, the reconciliation of the approved and posted populations and the exception loop: RWB-E6-022 to RWB-E6-024 (FEAT-WOF-10 to -12).
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
