# RWB-S7-E6015-APP Prepare the write-off pack

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S7-E6015-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S7-C |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S7-E6015-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the pack slice of RWB-E6-015 in rwb-writeoff. The three legacy criteria are kept word for word with their origin tag; the step evaluates R-WO-05 of the WO route set against the package version in force, assembles the pack from the case facts and route history of rwb-case, the balance and the legal and asset state of the rwb-source-data data products (DP-05), the document index of rwb-document and the write-off agent run of rwb-agent, registers the pack document in rwb-document, writes the `write_off` row and the local decision record before it changes (DP-03) and answers rwb-case for the move `PACK_PREPARED`, on base `/api/recovery/writeoff/v1` behind the gateway-bff composite route (DP-13, DP-19). DP-20 is absent although R-WO-05 names the Agent Runtime and the connection-matrix cell S7 to P10 is empty; DP-09 is absent although the service owns topic `rwb.writeoff.events.v1` with event `EV-24`; the plan's C row is None while the step consumes six owners' rows; `provision_carried`, `residual` and `pack_document_id` have no column in `write_off`; and SCR-27 needs a pack read the Ownership Map does not carry. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **write-off team member (RW-WRITEOFF)**, I want **the Workbench to assemble the committee pack from the case facts, the documents and the recovery history**, so that **write-offs follow the criteria and the committee's decision**.

This is the pack slice of legacy RWB-E6-015. It owns:

- the three legacy criteria (AC1, AC2, AC3), copied verbatim with their origin tag, and the rules, messages and screen they depend on;
- one step of `WriteOffWorkflow` on task queue `rwb-writeoff` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` and as the step between the scan of R-WO-01 and the committee routing of R-WO-11 (Temporal and Drools Design slide 5, S7 "monthly scan, posting"; slide 12, saga runner and DoA approvals for S7; slide 13);
- the evaluation of R-WO-05 against the WO package version in force, on the case in `POPULATION_PROPOSED` (FSD S7 A2.3; TSD S7 T4);
- the pack content: the balance, the provision carried, the route history, the legal and asset state and the residual of the case (legacy AC2; FSD S7 A2.3.3.1), assembled from the rwb-case case facts and route history, the rwb-source-data balance and asset state, the rwb-document index and the rwb-agent run;
- the pack document, registered in rwb-document and referenced from the pack, and the `write_off` row of the case in `rwb_writeoff` with the pack amount;
- the local decision record of the outcome, written through RWB-PLT-E1027-CON before the row changes (DP-03), with the rule ID, the package version and the case move;
- the answer to rwb-case for `PACK_PREPARED`, with the rule and its version;
- the pack-prepared state of SCR-27 Write-off proposal behind the gateway-bff composite route (DP-13, DP-19).

It does not own: the published shape of the pack element, of the `write_off` columns and of the consumed rows, the lists, the error set and the fakes, which are RWB-S7-E6015-CON; the monthly scan and its population (RWB-S7-E6013-APP), the tax criteria (RWB-S7-E6014-APP), the removal of a case from the population (RWB-S7-E6016-APP), the routing to the committee and the meeting with R-WO-09, R-WO-10 and R-WO-11 (RWB-S7-E6017-APP), the committee decision with `POST /write-offs/{writeOffId}/committee-decision` (RWB-S7-E6018-APP), the posting (RWB-S7-E6020-APP), the exception loop, the retention closure and the post charge-off recovery; the case of record, its route states and the parent `CaseWorkflow`, which are rwb-case (P3); the ACE data products, which are rwb-source-data's (P1); the documents, which are rwb-document's (P5); the agent run, which is rwb-agent's (P10); the WO package, which is rwb-decision's (P7); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

The feature objective, the problem and the metric are unchanged from the legacy story and the module FSD: the Workbench assembles the committee pack from the case facts, the documents and the recovery history (FSD S7 A2.3.1), because write-off populations are assembled by hand each month (FSD S7 A1.3), and the share of packs accepted first time is measured on the decision log and the Workbench records, rising each month, reviewed monthly (FSD S7 A2.3.1). The requirement is REQ-S7-002, "The committee pack is prepared from case and provision data with no manual assembly" (FSD S7 Requirements served). What D-RCV-60 changes is who owns the facts of the pack and who writes the row.

- **The pack is this service's.** `write_off` is S7's single table in `rwb_writeoff` (context pack, ownership rows owned by S7; TSD S7 T3.1), so the pack amount and the decision reference are recorded here and nowhere else.
- **The case stays with rwb-case.** `recovery_case`, the route state `POPULATION_PROPOSED` and the target `PACK_PREPARED` are P3's; this step reads the facts, the route history and the recovery history and answers the move, and no source names a payment or proceeds row for the recovery history of the pack (ASM-5020, ASM-5027).
- **The ACE facts stay with rwb-source-data.** The legacy Data table names `v_ace_account` (DF-ACE-001 to DF-ACE-042) and `v_ace_npa_asset` (DF-ACE-208 to DF-ACE-219); in the target only rwb-source-data holds the 30 `recovery.v_ace_*` views, so the balance and the legal and asset state arrive on the owner's data-product contract and no `v_ace_*` grant is requested here (DP-05; ASM-5020).
- **The documents stay with rwb-document.** The legacy Data table names `document` (DF-DOC-001 to DF-DOC-011); this step reads the index and registers the pack document, and copies no document field into `rwb_writeoff` (ASM-5023).
- **The pack is prepared by the agent.** R-WO-05 reads "Write-off agent prepares the pack", its Systems column names the Agent Runtime and the Document Hub, and legacy AC2 says the same. The run is consumed on rwb-agent's contract; DP-20 is not in this key's pattern set and the matrix cell S7 to P10 is empty, so the row is recorded rather than added to the metadata (ASM-5022).
- **The package is read, not embedded.** The WO route set is 51 rules over 27 states (TSD S7 T4), authored and approved in rwb-decision; DP-04 is not in this key's pattern set, so the package arrives on its read with the version in force and the version is recorded with the outcome (ASM-5021).
- **The decision is recorded first**, in the same transaction as the `write_off` row, which is what legacy AC1 asked for and legacy AC3 tested.
- **The pack has elements with no column.** `provision_carried`, `residual` and the pack document reference are named by R-WO-05, R-WO-09 and legacy AC2, and no field of TSD S7 T3.1 carries them: they live in the pack element and the row carries the amount (ASM-5023).

No business value moves: the pack elements, the rule, the zone of the three working days and the states are values of the package and of reference data, read with their version and never written in code.

### 3. Preconditions

- RWB-S7-E6015-CON is published: the pack element, the `write_off` columns DF-FIN-010 to DF-FIN-020, the consumed rows, the message set, the absence rules and the fakes are baselined and handed to this story.
- The rwb-case case-facts and route-history read is published with its fake, and so is the case-move answer, so the case can be packed on Day 1; both operation names are Not specified in the source documents (GAP-3021; ASM-5020).
- The rwb-source-data data-product contract that carries the balance and the asset state is published with its fake, with the as-of date of each product; its operation name is Not specified in the source documents (GAP-3021; ASM-5020). The row is not in this story's contract-dependency list, which is None.
- The rwb-document index read and the pack document registration are published with their fakes; their operation names are Not specified in the source documents (GAP-3021; ASM-5023).
- The rwb-agent write-off pack run is published with its fake; its operation name is Not specified in the source documents (GAP-3021; ASM-5022), and DP-20 is absent from the pattern set of this key.
- The rwb-decision rule-package read is published with its fake and answers the WO package at its version in force, with R-WO-05 among its 51 rules over 27 states; its operation name is Not specified in the source documents (GAP-3021; ASM-5021).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision record is written in the caller's transaction, and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-27 reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `write_off` exists in schema `rwb_writeoff` from the DB story of this service, with the columns of DF-FIN-010 to DF-FIN-020 and the standard record columns of TSD S7 T3.0; this story adds no table, no column and no migration.
- The tax criteria version in force is published by the tax criteria step; a pack without one is a missing value (GAP-3021; ASM-5024).
- The service runs as its own login on schema `rwb_writeoff`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_account` or `rwb_case` is refused by the database and fails the boundary test (ASM-5020).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S7-E6015-CON when its tests pass.

### 4. Flow

1. The monthly scan of R-WO-01 has produced the population and the tax criteria step has recorded its result, so the case is in `POPULATION_PROPOSED`; the parent `CaseWorkflow` forwards the stage signal and the pack step of `WriteOffWorkflow` on queue `rwb-writeoff` starts (FSD S7 A2.3.2 step 1).
2. The step reads the package version in force from rwb-decision, with the WO route set, its 51 rules over 27 states and the three-working-day zone R-WO-05 carries, one hop with a 2 s budget and a breaker (ASM-5021).
3. The step reads the case facts and the route history on the rwb-case contract: the case reference, the case number, the product group, the stage code, the state, the recovery history of the case and the route history the pack needs; read only, never a `recovery_case` row (ASM-5020).
4. The step reads the balance of the case and the legal and asset state of its collateral on the rwb-source-data data products, with the as-of date of each. A product that is stale holds the step and nothing is written (DP-05; ASM-5020).
5. The step reads the document index of the case on the rwb-document contract: the document reference, the type, the source and the storage reference, read only and without content (ASM-5023).
6. The step asks for the pack content on the rwb-agent contract, with the case facts, the route history, the balance, the provision carried, the legal and asset state, the residual and the document index as its input, and a service identity subject to the same role checks as a person (R-WO-05; TSD S7 T6.2; ASM-5022).
7. `RuleEvaluator` evaluates R-WO-05 on the case with the package in force: where the case is in `POPULATION_PROPOSED` and the pack content is complete, the rule answers the action, the target `PACK_PREPARED`, the rule ID and its version. Where no rule fires, the step changes nothing and reports the reason to the parent (FSD S7 A2.3.3.1).
8. The pack keeps the elements R-WO-05 names — the balance, the provision carried, the route history, the legal and asset state and the residual — with the tax criteria version the pack was built on; the amount written off is the balance the pack carries (ASM-5023, ASM-5024).
9. `WriteOffDecisionRecordWriter` writes one decision record per case through the local decision-record library, **before any change**: the case reference, the rule ID with the package version, the inputs reference with the as-of dates of the data products, the pack reference, the outcome and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC3).
10. `PackDocumentWriter` registers the pack document in rwb-document with the case reference, the pack reference and the type, and receives the document reference the pack carries; the document itself stays in the document hub (ASM-5023).
11. `WriteOffWriter` writes the `write_off` row of the case in one `rwb_writeoff` transaction with the decision record and the idempotency row: `case_id`, `decision_log_id`, `amount` and the standard columns of §11; `committee_date`, `posted_date`, `responsibility_center`, `cost_center`, `gl_product` and `recovered_after` stay empty, because they belong to the committee story and the posting story (ASM-5024).
12. `CaseMoveAnswer` answers rwb-case with `PACK_PREPARED`, the rule ID, the version and the decided-at time. rwb-case writes the `recovery_case` row; this service writes neither the row nor the state.
13. A repeated signal for the same case, pack and package version writes no second pack, no second document and no second record, sends no second answer and counts the repeat; SCR-27 shows the pack in its prepared state from this service through the gateway-bff composite route, next to the case state of rwb-case (DP-19; GAP-3021).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no `write_off` row, no pack document reference and no case-move answer leaves the service | MSG-P7-003 | AC3, TC-E6-015-03, TC-E6-015-05 |
| X2 | The role does not hold the Write-off and posting right of the action | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | TC-E6-015-04 |
| X3 | The case is not in `POPULATION_PROPOSED`, or has left the population since it was read | 409 and nothing is written for that case; a case that has already moved is not re-packed | None | AC2 |
| X4 | The tax criteria version is absent, or an ACE data product is stale after a late or failed batch | The step holds, writes nothing and shows the version or the date it waits on; the pack resumes on the next fresh answer | MSG-S7-001 | AC1, X5 |
| X5 | The rwb-case, rwb-source-data, rwb-document, rwb-agent or rwb-decision contract does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own schedule; nothing is written and no move is answered; the caller sees 503 with the platform error envelope | None | AC1, X4 |
| X6 | The pack content is incomplete: a pack element, the provision carried or the document index is absent | Nothing is written and the reason is reported to the parent with the missing element; the case stays in `POPULATION_PROPOSED` | MSG-GEN-001 | AC1 |
| X7 | A repeated signal for the same case, pack and package version | One row, one document reference, one record and one answer per case; the repeat is counted | None | AC1 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row, a `document` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR3, BR4, BR5 |

X1 to X3 are the legacy exception paths carried onto the slice — the failed record is AC3, the role check and the wrong state are the two exception flows of FSD S7 A2.3.4.3; X4 to X7 are the paths the target call types and the once-per-pack signal add; X8 is the ACE and schema boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S7-E6015-CON, the rwb-case, rwb-source-data, rwb-document, rwb-agent and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P1, P3, P5, P7 or P10 |
| Negotiable | The activity name, the decision code, the shape of the pack element and the state value of the row are this story's choice; the rule, the messages, the screen, the columns and the states are fixed |
| Valuable | The pack is assembled by rule with its decision recorded, so no pack is built by hand and the share accepted first time is measurable |
| Estimable | One workflow step, one evaluator, one record write, one row writer, one document registration, one case-move answer, six clients and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on a synthetic case and synthetic data products through the contract fakes, plus the access and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Prepare the write-off pack

  Background:
    Given case "RC-2026-000715" is one of 180 cases in state "POPULATION_PROPOSED" on the write-off population of the monthly scan
    Given the WO rule package is in force at its version and carries R-WO-05
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Prepare the write-off pack (legacy RWB-E6-015 AC1)
    Given the rwb-case contract mock returns the case facts, the route history and the recovery history of "RC-2026-000715"
    Given the rwb-source-data contract mock returns the balance of "RC-2026-000715" and the legal and asset state of its collateral with as-of date "2026-11-30"
    Given the rwb-document contract mock returns the document index of "RC-2026-000715"
    Given the rwb-agent contract mock returns the pack content of "RC-2026-000715"
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then assembles the committee pack from the case facts, the documents and the recovery history
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-WO-05 (legacy RWB-E6-015 AC2)
    Given the rwb-case contract mock returns the case state "POPULATION_PROPOSED" for "RC-2026-000715" and accepts the move "PACK_PREPARED"
    Given a case in state POPULATION_PROPOSED
    When pack built
    Then write-off agent prepares the pack: balance, provision carried, route history, legal and asset state, residual
    Then the case moves to PACK_PREPARED

  Scenario: AC3 Not recorded (legacy RWB-E6-015 AC3)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The three criteria are the legacy criteria of RWB-E6-015 word for word, with their origin tag added and nothing else changed: the repeated `Then`, the wording of `its trigger arrives`, `pack built`, `the action is taken` and `the decision log cannot be written` all stand. The cross-service parts are mocked, so AC1 carries four and AC2 one `Given the <service> contract mock returns <x>` line, and those are the only additions. What the legacy lines describe happens in six places now: rwb-case answers the case facts, the route history, the recovery history and the move; rwb-source-data answers the balance and the asset state that the FSD and the legacy Data table named as `v_ace_account` and `v_ace_npa_asset`; rwb-document answers the index; rwb-agent assembles the content; rwb-decision holds the package at its version; and this story evaluates the rule, writes the record, the row and the document reference and answers the move. The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_writeoff`, with the central `decision_log_entry` ledger of rwb-decision behind it. Two points are recorded rather than smoothed over: AC1 reads as the outcome of the feature while AC2 reads the rule at the case, so one step produces both; and the pack elements `provision_carried`, `residual` and the pack document have no column in `write_off`, so they live in the pack element of RWB-S7-E6015-CON (ASM-5023).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-WO-05 | Write-off | D9 | POPULATION_PROPOSED | PACK_BUILT | Any | Write-off agent prepares the pack: balance, provision carried, route history, legal and asset state, residual | PACK_PREPARED | Write-off team | Agent Runtime, Document Hub | 3 working days |

The row is the row of the Business Rules and Routing Logic v4, copied character for character. Its owner and systems columns name a business role and business systems, not services: in the target the "Agent Runtime" is rwb-agent (P10), the "Document Hub" is rwb-document (P5), the pack is written to `rwb_writeoff` and the case move is written by rwb-case on this story's answer. R-WO-03, R-WO-09, R-WO-10 and R-WO-11 sit beside it at `SCAN_DUE`, `PACK_PREPARED` and `PACK_INCOMPLETE` and belong to the scan story and the routing story; R-WO-06, the open deviation that holds a case out of the population, is tested by the scan and the removal stories, not here.

| ID | Rule | Source |
|---|---|---|
| BR1 | The pack is this service's: `write_off` is a row of `rwb_writeoff`, and no other service writes it | Context pack ownership rows (table `write_off`); TSD S7 T3.1; FSD S7 A2.3.2 |
| BR2 | The decision is recorded before the `write_off` row changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S7 T2 ("writes the decision log entry before any change"); legacy AC1 and AC3 |
| BR3 | The ACE facts stay with rwb-source-data: this story reads no `v_ace_*` view and no ACE table, and takes the balance and the asset state on the owner's data-product contract with their as-of dates | DP-05; FSD S7 A2.3.2; legacy Data table rows DF-ACE-001 to DF-ACE-042 and DF-ACE-208 to DF-ACE-219; ASM-5020 |
| BR4 | The case move is answered and not written: `recovery_case`, `POPULATION_PROPOSED` and `PACK_PREPARED` are rwb-case's | ASM-5020; TSD S7 T4 |
| BR5 | The documents stay with rwb-document: the index is read and the pack document is registered, and no `document` field is copied into `rwb_writeoff` | TSD S7 T3.1; legacy Data table row `document` DF-DOC-001 to DF-DOC-011; ASM-5023 |
| BR6 | No cross-schema join and no foreign key leaves `rwb_writeoff`; `case_id` and `decision_log_id` are identifiers of another service's fact | DP-01; TSD S7 T3.3 |
| BR7 | Every value a business person may change is reference data or a rule row read with its version: the pack elements, the rule, the three-working-day zone and the state vocabulary | FSD S7 BR-S7-003; legacy Guardrails; TSD S7 T3.2 |
| BR8 | The tax criteria version the pack was built on is read and recorded; a pack without it is held with VR-S7-003-1 and MSG-S7-001 and nothing is written | FSD S7 A2.3.3.1; ASM-5024 |
| BR9 | The same signal twice for the same case, pack and package version writes one row, one document reference, one record and one answer | TSD S7 T-A.2; FSD S7 A2.3.4.4 |
| BR10 | No person name, address, contact value or identity number enters `rwb_writeoff`, the pack element, the decision record, a log or a workflow input; `primary_person_key` is P3's and is never copied | Template and Rules §R7.2 (s17); TSD S7 T6.2 |
| BR11 | The pack step owns no posting and no committee decision: `POST /write-offs/{writeOffId}/committee-decision` is RWB-S7-E6018-APP's and the posting is RWB-S7-E6020-APP's | FSD S7 A2.6, A2.9; TSD S7 T-A.1 |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it (BR4). What this story owns is the state of the `write_off` row and the state of the step.

| From (`write_off.state`) | Event | Condition | To |
|---|---|---|---|
| None, no row | A pack built under R-WO-05 | the case is in `POPULATION_PROPOSED` and the pack content is complete | A row in `PACK_PREPARED`, with the answer `PACK_PREPARED` |
| None, no row | A pack whose content is incomplete | X6 | No row, no record and no answer |
| PACK_PREPARED | The committee routing of R-WO-11 | amount inside the write-off committee limit | `WITH_COMMITTEE`, by RWB-S7-E6017-APP |
| PACK_PREPARED | The pack check of R-WO-09 | `provision_carried` or the pack document absent | `PACK_INCOMPLETE`, by RWB-S7-E6017-APP |
| PACK_PREPARED | The committee decision of R-WO-15 | approved inside the delegation | `APPROVED`, by RWB-S7-E6018-APP |
| PACK_PREPARED | A repeated signal for the same case, pack and package version | X7 | Unchanged, the repeat is counted |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The scan has moved the case to `POPULATION_PROPOSED` | The package in force is read | Reading |
| Reading | The case facts, the data products, the index and the pack content are answered | The rule answers | Evaluating |
| Evaluating | R-WO-05 fires on the case | The decision record is written | Applying |
| Applying | The document reference, the row and the answer are written | The transaction commits | Waiting for the committee routing |
| Applying | The record write or the transaction fails | X1 | Waiting, nothing changed |
| Reading | The tax criteria version is absent or a data product is stale | X4 | Held, until a fresh answer |

The route states are those of the WRITEOFF machine of TSD S7 T4 and live on the case of record; the row carries the target state of the rule so that the row and the case agree on SCR-27, which is this story's design choice and not a business value. `PACK_INCOMPLETE`, `WITH_COMMITTEE`, `APPROVED` and the posting states are the later stories'.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-WRITEOFF, write-off team member | Write-off and posting CRU in TSD S7 T6.1: the primary role, building a pack, reading it and re-running a pack |
| RW-CREDITAD, Credit Administration officer | Write-off and posting CRUA: reads the pack and re-runs it |
| RW-PRODHEAD, product head; RW-WOCOMM, write-off committee member; RW-FINANCE, Finance and CFO delegate | Write-off and posting RA: read the pack in scope and act through the committee path of RWB-S7-E6018-APP |
| RW-FRAUD, RW-DEBTSALE, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Write-off and posting R: read only, in scope |
| SY-CASEWF, SY-RULES, SY-AGENT, SY-DATALOAD | Write-off and posting R as the matrix gives it: the service identities run the step and are subject to the same checks |
| rwb-writeoff service identity | Runs the step, reads the case, the data products, the index, the pack content and the package, writes the record, the document reference and the row and answers the move; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S7 T6.1 and the two rights of the legacy permission table — A for RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE, C for RW-WRITEOFF and RW-CREDITAD — and nothing wider. The FSD says the feature "runs unattended" with the write-off team member as also-user (FSD S7 A2.3.3.3), and both statements hold: the step runs under the service identity with no officer task on the happy path, and the team member is the primary role when a person acts on SCR-27 or re-runs a pack. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the access guard is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-FIN-010 | write_off (S7, `rwb_writeoff`) | id | Write, the pack reference of the row and the answer |
| DF-FIN-011 | write_off (S7, `rwb_writeoff`) | case_id | Write, from the case of the pack |
| DF-FIN-012 | write_off (S7, `rwb_writeoff`) | decision_log_id | Write, the local decision record of the pack |
| DF-FIN-013 | write_off (S7, `rwb_writeoff`) | amount | Write, the balance the pack carries |
| DF-FIN-014 | write_off (S7, `rwb_writeoff`) | tax_criteria_met | Read, written by the tax criteria step (ASM-5024) |
| DF-FIN-015 | write_off (S7, `rwb_writeoff`) | committee_date | Not written here: RWB-S7-E6018-APP |
| DF-FIN-016 | write_off (S7, `rwb_writeoff`) | posted_date | Not written here: the posting story |
| DF-FIN-017 | write_off (S7, `rwb_writeoff`) | responsibility_center | Not written here: the posting story |
| DF-FIN-018 | write_off (S7, `rwb_writeoff`) | cost_center | Not written here: the posting story |
| DF-FIN-019 | write_off (S7, `rwb_writeoff`) | gl_product | Not written here: the posting story |
| DF-FIN-020 | write_off (S7, `rwb_writeoff`) | recovered_after | Not written here: the post charge-off recovery story |
| Standard columns | write_off (S7, `rwb_writeoff`) | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` | Write, with `state` at `PACK_PREPARED` and the optimistic lock of `version` |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_writeoff`) | rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before the row changes |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table and not written: the case facts, the route history and the state arrive on the rwb-case contract |
| DF-ACE-001 to DF-ACE-042 | `v_ace_account` (P1) | account_key, account_code, account_status, contract_no, product_category_efs, total_balance and 36 more | Not read: no `v_ace_*` grant; the balance arrives on the rwb-source-data product |
| DF-ACE-208 to DF-ACE-219 | `v_ace_npa_asset` (P1) | asset_ref, asset_key, asset_code, transfer_in_type, from_segment, book_value and 6 more | Not read: no `v_ace_*` grant; the legal and asset state arrive on the rwb-source-data product |
| DF-DOC-001 to DF-DOC-011 | document (P5) | id, case_id, person_key, document_type, source, storage_ref and 5 more | Not read as a table: the index arrives on the rwb-document contract and the pack document is registered there |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read here: R-WO-05 arrives on the package read with its version |
| Pack elements with no column | `provision_carried`, `residual`, the pack document reference | Read from the pack content and the document registration, written in the pack element; the column is Not specified in the source documents (GAP-3021; ASM-5023) |

Field IDs are those of TSD S7 T3.1 and the Logical Data Model and Data Dictionary; the ACE, document and ledger rows are the rows the legacy Data table lists, with their owners changed to P1, P5 and P7 by the target. **No new table, no new column and no migration**: `write_off` arrives with the DB story of this service, this story writes four of its existing columns, and `decision_record` and `idempotency_key` are library objects created in `rwb_writeoff` by the library's own migration (DP-03). `outbox_event` also sits in the schema as a library object, and this step writes no row to it because it publishes no event (§12.3).

**No personal data.** The row carries identifiers, an amount, a boolean, dates, list values and a rule version. No name, address, contact value or identity number enters `rwb_writeoff`, the pack element, the record, a log or a workflow input, and the fixtures are synthetic. `primary_person_key` is P3's and is never copied here.

### 12. Contract

#### 12.1 REST operations provided

None. This legacy key owns no REST operation: the pack is prepared unattended by the stage step and answers the case, and SCR-27 reads it through the gateway-bff composite route. The two operations the legacy story lists belong elsewhere under the Ownership Map: `POST monolith-base/write-off-scans` is API-S7-001, declared on `/api/recovery/writeoff/v1` by RWB-S7-E6013-CON under DP-13, and `POST monolith-base/write-offs/{writeOffId}/committee-decision` is API-S7-002, declared by RWB-S7-E6018-CON. The Ownership Map gives rwb-writeoff exactly those two operations and no write-off read, so the read SCR-27 needs carries a placeholder (GAP-3021; ASM-5026).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The case-facts and route-history read (operation name Not specified in the source documents (GAP-3021; ASM-5020)) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, case number, product group, stage code, state, recovery history and route history of the pack; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3021; ASM-5020)) | rwb-case (P3) | P3 rwb-case | The move `PACK_PREPARED` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The balance and asset-state data-product read (operation name Not specified in the source documents (GAP-3021; ASM-5020)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The balance of the case and the legal and asset state of its collateral, with the as-of date of each product (DP-05); faked |
| The document-index read (operation name Not specified in the source documents (GAP-3021; ASM-5023)) | `/api/recovery/document/v1` | P5 rwb-document | The documents of the case: reference, type, source and storage reference, without content; faked |
| The pack document registration (operation name Not specified in the source documents (GAP-3021; ASM-5023)) | `/api/recovery/document/v1` | P5 rwb-document | The pack document of the case, answered with the document reference the pack carries; faked |
| The write-off pack run (operation name Not specified in the source documents (GAP-3021; ASM-5022)) | `/api/recovery/agent/v1` | P10 rwb-agent | The pack content: balance, provision carried, route history, legal and asset state and residual; faked |
| The rule-package read in force (operation name Not specified in the source documents (GAP-3021; ASM-5021)) | `/api/recovery/decision/v1` | P7 rwb-decision | The WO package at its version, with R-WO-05 among its 51 rules over 27 states; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The seven rows are contract dependencies of class C that the plan does not carry, because this story's C row is None; the absence is recorded (GAP-3021). The one Temporal call the connection matrix gives S7 towards P7 is not tied to a named operation by any source and this step makes no such call (§12.5).

#### 12.3 Events published

None. The service publishes on `rwb.writeoff.events.v1` and owns event `EV-24`, which TSD S7 T5.3 names `WriteOffApproved`; neither belongs to this step, because the pack approves nothing and changes no book: `EV-24` is the committee approval's, in RWB-S7-E6018-APP. This story therefore declares no event, no producer group and no outbox row of its own, and a build that publishes one fails the absence test. The topic carries the retry and `.dlt` topics of the platform (DP-14), and the outbox and inbox library that relays it is the DP-09 dependency the plan does not carry for this key (ASM-5025; GAP-3021).

#### 12.4 Events consumed

None. The service subscribes to rwb-payment's events in the recovery-after-charge-off steps (context pack connection matrix, row S7: Temporal and events to P8), and none of them belongs to the pack: no recovery exists before the write-off is posted. This story therefore holds no consumer group, no subscription and no inbox row, and a build that adds one fails the absence test. The trigger of the step is the case signal the parent forwards after the scan and the tax criteria, and the FSD declares a monthly scan background event and no other (FSD S7 A2.3.4.4).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case, the child of `CaseWorkflow`, saga steps for the committee and the posting, continues-as-new at each stage end | `rwb-writeoff` in namespace `rwb-recovery` | Input: the case reference, the population reference, the cut-off date and the package in force; signals: the case facts and state, the data products, the index, the pack content and the committee answer. This step sits before the committee, so it needs no compensation |
| `prepareWriteOffPack` | Activity, the one pack step | `rwb-writeoff` | The case reference, the cut-off date and the package in force in; the pack element, the rule ID with its package version, the document reference, the row reference and the case move out, with the record and the row written in one transaction |

No child workflow for the case and none for the money exists in this service, and this step registers no activity on another queue: the evaluation runs inside `prepareWriteOffPack` on the WO package read from rwb-decision, which is where ADR-017 places the rule models and DP-04 the evaluation. The activity name is a target design choice fixed by no source document. The connection matrix gives S7 one Temporal call to P7 and no source names its operation; this story does not use it and records the gap (GAP-3021; ASM-5021).

#### 12.6 Schedules

None. The step runs from the case signal the parent forwards after the monthly population is built, and owns no Temporal Schedule and no legacy Quartz job. The monthly clock is JOB-16, the write-off scan of the service, and it belongs to RWB-S7-E6013-APP; the three-working-day zone of R-WO-05 is a commercial zone of the rule and not a Schedule.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of the case; this story writes the row and the columns of §11 |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated signal and the answer it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | Present as a library object; this step writes no row to it (§12.3) |

Not owned and never read as a table: `recovery_case` and `timer` (P3), every `v_ace_*` view (P1), `document` (P5), `notice` (P6), `proceeds` (P8), `decision_log_entry` and `rule_row` (P7). No foreign key leaves the schema and `case_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-facts and route-history fake | The facts, the route history and the recovery history of `RC-2026-000715`, with the state `POPULATION_PROPOSED`; a case that has left the population | AC1, AC2, X3 |
| rwb-case case-move fake | The move `PACK_PREPARED` accepted for `RC-2026-000715`; a move refused because the case is not in the expected state | AC2, X3 |
| rwb-source-data data-product fake | The balance and the legal and asset state of the case with as-of date `2026-11-30`; a stale product with its date; no answer beyond 2 s | AC1, X4, X5 |
| rwb-document fake | The index of the case and the registration of the pack document, answered with a document reference | AC1, X6 |
| rwb-agent pack-run fake | The pack content of `RC-2026-000715` with its five elements; an incomplete content; no answer beyond 2 s | AC1, AC2, X5, X6 |
| rwb-decision rule-package fake | The WO package at its version in force with R-WO-05, the three-working-day zone and the state vocabulary | AC1, AC2 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC3, X1 |
| gateway-bff composite route fake | The merged SCR-27 answer for `RC-2026-000715`, in its pack-prepared state | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the six consumed rows carry the placeholder until their owners confirm them (GAP-3021).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 7 consumed | The case read and the case-move answer, the balance and asset-state read, the document index and the pack registration, the agent run and the package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `EV-24` `WriteOffApproved` belongs to the approval story and no event is consumed here (§12.3, §12.4) |
| Temporal | 1 workflow and 1 activity | `WriteOffWorkflow` and `prepareWriteOffPack` on `rwb-writeoff`; no Schedule, and no activity on the `rwb-decision` queue from this step |
| File | None | No file is read, built or delivered here; the pack document is a document of rwb-document |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.writeoff`, module `pack`; front end `src/modules/recovery/writeoff/WriteOffPack.tsx`, the fragment SCR-27 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract, with no `v_ace_*` grant in this service | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the `write_off` row commit together or not at all. DP-05 is why the legacy `v_ace_account` and `v_ace_npa_asset` rows become a contract read of rwb-source-data and no view grant, and it adds no row by its own table. DP-13 fixes the base of the service's two operations and touches nothing this step provides, because it provides none. DP-19 is how SCR-27 reaches this service, one hop through the gateway. These four are the whole pattern set of the key and the story adds no fifth: DP-20 (the agent client), DP-04 (the embedded Drools kit) and DP-09 (the outbox and inbox library) are real dependencies of this step that the plan does not hold, and they are recorded in the registers instead of the metadata table (GAP-3021; ASM-5021, ASM-5022, ASM-5025).

**Dependencies the tables add and the plan does not hold.** The seven consumed rows are class C dependencies in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1. The agent client of DP-20 would add `C RWB-P10-TE013-CON`, and the run is consumed as a contract call without that row. The Drools kit of DP-04 would add `RWB-PLT-E1072-CON` and `RWB-P7-E1073-CON`; the package is read as data and evaluated in this service's activity, so no kit is declared. The outbox library of DP-09 would add `RWB-PLT-TE006-CON` and is needed only by the stories that publish. The plan's H row stands unchanged.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `WriteOffWorkflow` pack branch | Workflow | Waits for the case signal, reads the package in force and reports the outcome to the parent |
| `prepareWriteOffPack` | Activity | Reads the case, the products, the index and the pack content, evaluates R-WO-05, writes the record, the document reference and the row, answers the move |
| `RuleEvaluator` | Service | The R-WO-05 evaluation over the package in force, with the state test, the completeness test and the no-fire path |
| `WriteOffDecisionRecordWriter` | Library adapter | Writes the record with the rule ID and the version before any change, hash-linked; refuses the step when the write fails |
| `PackDocumentWriter` | Client | Registers the pack document in rwb-document and holds the returned reference |
| `WriteOffWriter` | Repository | Writes the `write_off` row in one `rwb_writeoff` transaction with the idempotency row and the optimistic lock |
| `CaseFactsClient` | Client | The case-facts, route-history and state read of rwb-case, one hop, 2 s, breaker |
| `SourceDataProductClient` | Client | The balance and asset-state read of rwb-source-data with the as-of dates and the stale path |
| `DocumentIndexClient` | Client | The document-index read of rwb-document |
| `AgentPackClient` | Client | The write-off pack run of rwb-agent with its service identity and the incomplete-content path |
| `RulePackageClient` | Client | The package read of rwb-decision at its version in force |
| `CaseMoveAnswer` | Client | The `PACK_PREPARED` move to rwb-case, one answer per case |
| `WriteOffPackController` | Controller | The capability area and right of the two operations of the service that read the pack, the problem mapping and the read-only answer |
| `WriteOffPack` | React component | Shows the pack and its elements on SCR-27, read only, with the refusal, not-recorded and stale-data states |

**Database and migrations.** No Flyway file. `write_off` arrives with the DB story of this service, and the record and idempotency key are library objects created in `rwb_writeoff` by the library's migration (DP-03). No column is added for the provision carried, the residual, the pack document, the case or the rule row: those are pack elements and rows of their owners and are referenced, not copied.

**Configuration and reference data.**

- The pack elements, the three-working-day zone and the state vocabulary: rule rows of the WO package with their version, never written in code (ASM-5021).
- The tax criteria version in force: a versioned data row read with the pack (ASM-5024).
- The capability area "Write-off and posting" and its rights: access rows of rwb-access, read through the guard.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020; the flag `rwb.writeoff.pack-v1` is a flag of the platform library.

**Build steps**

1. The pack branch of `WriteOffWorkflow` and its input record, registered on `rwb-writeoff` as the stage child of `CaseWorkflow`, with the case signal as its trigger.
2. `CaseFactsClient`, `SourceDataProductClient`, `DocumentIndexClient`, `AgentPackClient` and `RulePackageClient` against their fakes, with the 2 s budget, the breaker, the as-of dates, the stale path, the incomplete-content path and the no-answer path (AC1, AC2, X4, X5, X6).
3. `RuleEvaluator` over the package, with R-WO-05, the state test and the no-fire path (AC1, AC2).
4. `WriteOffDecisionRecordWriter` against the stub, with the failed-write path (AC1, AC3, X1).
5. `PackDocumentWriter` with the registration and the returned reference (AC1, X6).
6. `WriteOffWriter` with the one transaction, the row, the columns of §11, the idempotency row and the optimistic lock (AC1, X7).
7. `CaseMoveAnswer` with the `PACK_PREPARED` move and the refused move (AC2, X3).
8. `WriteOffPackController` with the rights, the problem mapping and the read-only answer, and `WriteOffPack` on SCR-27 through the composite route fake (AC1).
9. The boundary test: no statement outside `rwb_writeoff`, no `v_ace_*` read, no write to `rwb_case`, `rwb_document`, `rwb_agent` or `rwb_decision` (X8, BR3, BR4, BR5).

**Feature flag.** `rwb.writeoff.pack-v1`; off means the step holds the case in `POPULATION_PROPOSED`, writes nothing and answers no move, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic population in SIT, R-WO-05 builds the pack with its five elements, the row and the document reference are written with the record, a repeated signal writes once, a forced record failure changes nothing, no `recovery_case`, `document` or `v_ace_*` read exists in the build, and SCR-27 answers through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | The tax criteria version is absent when the pack is built (X4, VR-S7-003-1) | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | A required field of the request or of the pack content is absent or invalid (X5, X6) | Enter {field}. |
| MSG-P4-002 | A role without the Write-off and posting right acts on the pack (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the row changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are those of the legacy message set and of FSD S7 A2.3.3.1, and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-S7-001 is the wording of VR-S7-003-1, which the FSD gives to this feature as well as to the scan.

### 15. Screens and states

SCR-27 Write-off proposal, in its loading state and its pack-prepared state, is served through the gateway-bff composite route (DP-19). The route calls rwb-writeoff for the pack and its elements, rwb-case for the case and its route state and rwb-document for the pack document; this story fixes the rwb-writeoff answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The state this story produces is the "proposed" state of the legacy screen table — the pack of the case with its five elements, the balance, the provision carried, the route history, the legal and asset state and the residual, on a row at `PACK_PREPARED`. The legacy table gives the states "Scan; proposed; in committee; approved": the scan state is RWB-S7-E6013-APP's, the in-committee state is RWB-S7-E6017-APP's and RWB-S7-E6018-APP's, and the approved state is RWB-S7-E6018-APP's. The refusal, not-recorded and stale-data states read the messages of section 14. The read of the pack on this screen has no operation in the Ownership Map and carries a placeholder (GAP-3021; ASM-5026).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-015-01 | AC1 | Component | The 180-case population with the case, the products, the index and the pack content on the fakes; the pack element, the row, the document reference, the record and the answer asserted |
| TC-E6-015-02 | AC2 | Component | Case `RC-2026-000715` at `POPULATION_PROPOSED`; the pack built by the agent run and the `PACK_PREPARED` move asserted on the fake |
| TC-E6-015-03 | AC3 | Component | The decision-record stub stopped; nothing written and MSG-P7-003 shown |
| TC-E6-015-04 | Access | Component | A role without the Write-off and posting right; 403 with MSG-P4-002 and no read |
| TC-E6-015-05 | Principle 5 | Component | A forced decision log write failure inside the transaction; no `write_off` row, no document reference and no answer |

The five legacy cases are those of RWB-E6-015 in their legacy order, with the Level column added: every case is tested on the fakes, so every case is `Component`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in code: the pack elements, the rule, the three-working-day zone, the state vocabulary and the tax criteria version stay data, reference data or the rule package, never a constant, a default or a branch.
- No personal data in `rwb_writeoff`, in the pack element, in a workflow input or in a log: identifiers, an amount, a boolean, dates, list values and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (BR3).
- The case stays with rwb-case and the documents with rwb-document: no `recovery_case` row, no case route-state write and no `document` field copied here (BR4, BR5).
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no event published by this step and no `v_ace_*` view read.
- The decision is recorded before the change; a build that writes the `write_off` row outside the record's transaction fails the review (DP-03).
- The pack is assembled, never keyed: no pack field is typed in by a person on the happy path, and a run that needs a manual entry fails the acceptance test.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S7-002 | The committee pack is prepared from case and provision data with no manual assembly (FSD S7 Requirements served); TSD S7 T8 maps the same id to FEAT-WOF-01 and the conflict is recorded (GAP-3021) | The pack step, the pack element, the row and the case move | TC-E6-015-01, TC-E6-015-02, TC-E6-015-05 |
| ADR-013 | 19 services inside ACE | rwb-writeoff as the owner of `write_off` | TC-E6-015-01 |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-E6-015-01 |
| ADR-017 | Embedded Drools per service; rule registry in rwb-decision | The R-WO-05 evaluation on the package read | TC-E6-015-01, TC-E6-015-02 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The seven consumed rows with their budget and breaker | TC-E6-015-01, TC-E6-015-02 |
| ADR-022 | Local decision record plus central ledger | The record written before the change | TC-E6-015-03, TC-E6-015-05 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-015, disposition Split (rework); feature FEAT-WOF-03, depends on FEAT-WOF-01 |
| Legacy criteria | AC1, AC2 and AC3, owned word for word by this story |
| Source text | Legacy RWB-E6-015; FSD S7 Write-off and recovery v3 A2.3, A1.3, Requirements served and Screens; TSD S7 Write-off and recovery v2 T2, T3, T4, T5.3, T6 and T-A; Business Rules and Routing Logic v4 row R-WO-05 |
| Test cases | TC-E6-015-01 to TC-E6-015-05 |
| Feature and screens | FEAT-WOF-03, SCR-27 Write-off proposal |
| Rules | R-WO-05, governed in rwb-decision; R-WO-09, R-WO-10 and R-WO-11 are RWB-S7-E6017-APP's |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-017, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the pack element, of the `write_off` columns, of the consumed rows and of the fakes: RWB-S7-E6015-CON.
- The monthly scan and the population (RWB-S7-E6013-APP) and the tax criteria (RWB-S7-E6014-APP), whose result this step reads.
- The removal of a case from the population, R-WO-06 and R-WO-07: RWB-S7-E6016-APP.
- The routing to the committee, the meeting, the pack check of R-WO-09 and the routing of R-WO-10 and R-WO-11: RWB-S7-E6017-APP.
- The committee decision, R-WO-15, `POST /write-offs/{writeOffId}/committee-decision` and `EV-24` `WriteOffApproved`: RWB-S7-E6018-APP.
- The posting, the provision release, the Finance feed, the reconciliation and the exception loop: the later S7 stories, with the money in rwb-payment (P8) and the ledger in rwb-decision (P7).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3). The ACE data products: rwb-source-data (P1). The documents: rwb-document (P5). The agent run: rwb-agent (P10). The WO package: rwb-decision (P7).
- The gateway-bff composite route, the screen field list of SCR-27 and the write-off read the map does not carry: RWB-PLT-N001-CON (ASM-5026).
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
