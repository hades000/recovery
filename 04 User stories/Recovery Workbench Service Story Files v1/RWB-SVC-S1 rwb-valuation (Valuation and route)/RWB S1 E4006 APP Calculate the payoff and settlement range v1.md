# RWB-S1-E4006-APP Calculate the payoff and settlement range

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S1-E4006-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-valuation |
| Service epic | RWB-SVC-S1 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S1-F |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S1-E4006-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S1 rwb-valuation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-006 split out for rwb-valuation. The two legacy criteria this story owns are copied word for word with their origin tag. The payoff is read from the ACE balances of the account on the rwb-source-data contract or on this service's own SELECT-only view (DP-05) and is not copied anywhere; the settlement range and the floor come from the rule set in force at its version; the result is written to the local decision record with the rule id and version before the answer leaves (DP-03); the answer travels on `POST /cases/{caseId}/route` on base `/api/recovery/valuation/v1` (DP-13) and reaches SCR-13 Route decision through the gateway-bff composite route (DP-19). No source gives S1 a table for the payoff, the range or the floor (GAP-2615; ASM-4317), publishes the names of the two reads (GAP-2616; ASM-4318), fixes the source of the balances or the composition of the payoff (GAP-2617; ASM-4319) or fixes the freshness limit and the floor method (GAP-2618; ASM-4320); the trigger set is FSD wording with no event and no job behind it (GAP-2619; ASM-4321). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner**, I want **the Workbench to work out the payoff from the balances ACE holds for the account and the settlement range from the rules, with the floor applied**, so that **the route is chosen on expected return with reasons**.

This is the application slice of legacy RWB-E4-006. It owns:

- the legacy criteria AC1 and AC2 of the key, copied verbatim, and the rules, messages, screens and tests they carry;
- the calculation step inside `RouteDecisionWorkflow` on task queue `rwb-valuation`: the payoff at the ACE batch date and the settlement range with the floor applied, computed per assessment, never stored as a constant;
- the read of `total_balance`, `past_due_amount` and `collections_fee` of each account of the case from the ACE account data product, one hop, 2 s, read only, with no `v_ace_*` copy and no balance of this service (DP-05);
- the read of the settlement route set in force, with the range bounds, the floor and the rule id and version (DF-REF-001 to DF-REF-015, owner P7);
- the local decision record of the step, written through RWB-PLT-E1027-CON in the caller's transaction before the answer is composed (DP-03);
- the calculation elements of the answer of `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`, whose shape is baselined by RWB-S1-E4006-CON (DP-13);
- the states of SCR-13 Route decision that the calculation produces, reached through the gateway-bff composite route (DP-19).

It does not own: the route recommendation and its reasons, which are FEAT-VAL-07 and its story; the approval and the case move, which are the route-decision submission slice of RWB-E4-005 (RWB-S1-E4005-APP) and rwb-case; the offer built inside the range, which is rwb-treatment's (S2) on R-SET-04 and the settlement stories; the ACE balances and their freshness, which are rwb-source-data's (P1); the rule package, its approval and the central ledger, which are rwb-decision's (P7); the roles and scopes behind the right, which are rwb-access's (P4); the composite route and the screen field list, which are RWB-PLT-N001-CON; the fresh-payoff request to EAPI and the interfaces behind it, which are rwb-integration's (P2).

### 2. Business rationale

The route of a case is a decision about money, and it can only be taken on expected return if two numbers are on the table: what the bank will collect if it calls the account now, and how far it may go in a settlement without breaching the floor. Today both numbers sit in an officer's account plan, read from ALS through the Workbench's own copies of the account, and the range is looked up by hand. D-RCV-60 puts the balances where they already are — ACE, through the contract of rwb-source-data or this service's own SELECT-only view (DP-05) — and puts the range and the floor where the bank governs them: in the rule set in force, read with its version.

The three things the target changes, and nothing else:

- **the balances are read, not held.** This service keeps no loan account copy and no balance (ADR-010, D-RCV-35 U1); the payoff is computed from `total_balance`, `past_due_amount` and `collections_fee` at the ACE batch date and is not persisted as a second fact.
- **the range is governed data.** The bounds and the floor are values in force with a version, referenced by identifier and never written in code (BR-S1-006); a change of limit is a release of the rule set, not a build.
- **the decision is on record.** The payoff, its as-at date, the range and the floor are recorded with the rule id and version in the caller's transaction, and a calculation that cannot be recorded does not proceed (DP-03).

Two boundaries are recorded rather than assumed. No source gives S1 a table for the payoff, the range or the floor: the ownership rows give S1 no table, TSD S1 T3.1 declares only `valuation` and `score`, and the legacy data table names `v_ace_account`, `treatment`, `decision_log_entry` and `rule_row`, none of which is this service's (GAP-2615; ASM-4317). And the FSD's phrase "payoff from ALS" and the legacy story's "from v_ace_account" are the same read after the ACE re-base, while the composition of the payoff out of the three balances is published by no source (GAP-2617; ASM-4319).

Serves the route decision of EP04 in wave 3 on release 28 February 2027 (tentative). No business value is invented: the amounts of AC1, the messages and the rights are the values the legacy story and the FSD already carry.

### 3. Preconditions

- RWB-S1-E4006-CON is published: base `/api/recovery/valuation/v1`, the calculation elements of `POST /cases/{caseId}/route`, the error set, the `Idempotency-Key` header and the fakes. This story builds against that baseline and never against a sibling service.
- RWB-PLT-E1027-CON is published: the decision-record writer with `@Transactional(propagation = MANDATORY)`, its refusal and failure messages, and the `decision_record` DDL template applied in `rwb_valuation` (DP-03).
- RWB-PLT-N001-CON is published: the composite route that serves SCR-13 from the case read and this service's answer, one hop each, read only (DP-19).
- The `rwb_valuation` schema and its login exist from the platform database story; SELECT on the ACE account data product — the rwb-source-data contract or `recovery.v_ace_account` and `recovery.v_ace_batch_status` — is granted and on nothing else (ASM-4318, ASM-4319).
- The settlement route set — R-SET-01, R-SET-02, R-SET-03, R-SET-04 and R-SET-05 — is in force with its rule id and version for the business date, and the range bounds and the floor are values of that set (Business Rules and Routing Logic v4; GAP-2618; ASM-4320).
- The freshness limit of `payoff_as_at` and the batch-date rule of the ACE data product are reference values in force for the business date; they are read, never constant (VR-S1-006-1; BR-S1-006).
- FSD S1 and TSD S1 carry status "In review" and no approval is needed to build against a Draft baseline; the split proceeds at status Draft (ASM-4323).
- The story has only CON build dependencies, so it is Day 1 by rule (§R5.7 rule 8).

### 4. Flow

1. The case owner opens SCR-13 Route decision for a case and prepares the route decision; the browser calls `POST /cases/{caseId}/route` on the service base through gateway-bff (DP-13, DP-19).
2. The guard resolves right U in the capability area Treatment and offer from the contract's `security` declaration and applies the scope (TSD S1 T6.1).
3. The freshness gate runs: VR-S1-006-1 reads `v_ace_batch_status` for the account product and, when the product is from an earlier date, the step stops with MSG-P1-001 and writes nothing.
4. The service resolves the accounts of the case and reads `account_key`, `account_code`, `account_status`, `total_balance`, `past_due_amount` and `collections_fee` for each account at the ACE batch date through the rwb-source-data contract (DP-05).
5. The payoff is computed by the calculation in force from those three balances; the formula, the fee inclusion and the rounding are governed values read with their version and are not written in code (BR-S1-006; GAP-2617; ASM-4319).
6. `payoff_as_at` is stamped from the ACE batch date of the data product. When it is older than the freshness limit, R-SET-03 blocks the step and a fresh payoff is requested through rwb-integration (P2); this service writes nothing on that path.
7. The settlement route set in force is read with its rule id and version, and the range bounds and the floor are taken from it; the floor is applied to the range so that no offered amount below it leaves this step unflagged (R-SET-01, R-SET-05).
8. One transaction opens: the local `decision_record` is written with the rule id, the rule version, the payoff, `payoff_as_at`, the range bounds, the floor and the facts reference, and the request's idempotency row is written in the same transaction (DP-03).
9. The transaction commits and the answer to the caller carries the payoff, its as-at date, the two range bounds, the floor, the rule version and the state; a missing payoff or a missing floor holds the calculation as UNMATCHED_EXCEPTION, names the missing field and raises a task for the case owner (R-SET-25).
10. A repeated request with the same `Idempotency-Key` returns the first answer and writes no second record.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without right U in Treatment and offer, or a case outside the scope | 403 before any read; the refusal is the guard library's answer and the log carries the role and the operation, never a personal field | MSG-P4-002 | Section 10; TC-E4-006-03 |
| X2 | The account data product is stale for the business date | The step stops before a balance is used: nothing is calculated, nothing is written | MSG-P1-001 | TC-S1-E4006-APP-02 |
| X3 | The decision record cannot be written | The transaction rolls back: no record, no idempotency row, no answer; the caller may retry with the same key | MSG-P7-003 | AC2; TC-E4-006-02, TC-E4-006-04 |
| X4 | The account of the case has no row in the ACE account product | No payoff is computed, the range is not offered, and the screen states that no balance is held; nothing is invented | None | R-SET-25; TC-S1-E4006-APP-01 |
| X5 | `payoff_as_at` is older than the freshness limit | R-SET-03 blocks the calculation at PAYOFF_AND_RANGE_SET and a fresh payoff is requested through rwb-integration; this service writes nothing | None | TC-S1-E4006-APP-02 |
| X6 | The rule set in force carries no floor, or no range for the route set | The calculation holds as UNMATCHED_EXCEPTION, names the missing value and raises a task for the case owner (R-SET-25) | MSG-GEN-001 | TC-S1-E4006-APP-01 |
| X7 | A required element of the request is absent or outside its list | 422 with MSG-GEN-001 naming the field; the transaction never opens | MSG-GEN-001 | Section 12.1 |
| X8 | The rwb-source-data read or the rule read does not answer inside 2 s | 503 with the platform problem body; nothing is written and the workflow retries on its own schedule | None | Section 12.2 |

X1 to X3 are the legacy paths carried onto the split: X1 is the permission check of the legacy story, X2 the freshness rule the FSD gives the feature, X3 legacy AC2. X4 to X8 are the paths the read of two contracts adds. A refusal under X1, X2 or X7 writes nothing, because the guard, the gate and the validator run before the transaction opens.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against the RWB-S1-E4006-CON fake, the decision-record writer fake and the composite-route fake, with a balance fixture and a rule-set fixture; needs no live ACE, rwb-decision or rwb-case |
| Negotiable | The component names, the internal method boundary and the shape of the calculation object are this story's choice; the operation, the element names of the routing workbook, the messages and the rights are fixed |
| Valuable | The officer sees the payoff and the range with the floor before choosing a route, and the bank can prove which rule version produced them |
| Estimable | One calculation, two reads, one library adapter, one transaction, one answer and one freshness gate |
| Small | Fits two weeks with its tests |
| Testable | Each criterion and each exception path is one automated test on fixtures and fakes; the two reads are contract-level |

### 7. Acceptance criteria

```gherkin
Feature: Calculate the payoff and settlement range

  Background:
    Given the rwb-decision contract mock returns the settlement route set in force with its rule id and rule version
    Given account "A-0001" belongs to case "RC-2026-000401" and the ACE account data product is fresh at the business date

  Scenario: AC1 Calculate the payoff and settlement range (legacy RWB-E4-006 AC1)
    Given the rwb-source-data contract mock returns total balance 1240000, past due amount 86000 and collections fee 4500 for account "A-0001" at the ACE batch date 2026-12-14
    Given v_ace_account holds total balance 1240000, past due amount 86000 and collections fee 4500 for account "A-0001" at the ACE batch date 2026-12-14
    When the case owner prepares the route decision
    Then the Workbench works out the payoff from the balances in v_ace_account and the settlement range from the rules, with the floor applied
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E4-006 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Target reading.** Both criteria are the legacy criteria of RWB-E4-006 word for word, with their origin tag added and nothing else changed: the repeated `Then`, `v_ace_account`, `the case owner prepares the route decision` and `the action is taken` all stand. The cross-service part of AC1 is mocked, so AC1 carries one `Given the rwb-source-data contract mock returns <x>` line holding the legacy amounts unchanged, and that added line is the only addition to the criterion. AC2 needs none, because the decision-record library is local. What the legacy lines describe happens in four places in the target: the balances are ACE's and arrive on the rwb-source-data contract or this service's own view, read only (DP-05); the range and the floor are the settlement route set at its version (R-SET-01, R-SET-05); "the decision log" is the local `decision_record` written through RWB-PLT-E1027-CON in the same transaction (DP-03), with the central `decision_log_entry` ledger of rwb-decision behind it; and the answer is served on `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1` (DP-13), composed into SCR-13 by the gateway-bff composite route (DP-19). The word "system" in AC1 is kept: the calculation is unattended, as FSD S1 A2.6.3.3 states.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The payoff is computed from the balances ACE holds for the account and is never read from a copy, a staging table or a balance of this service | legacy RWB-E4-006 story; D-RCV-35 U1; ADR-010; DP-05 |
| BR2 | The three balances used are `total_balance`, `past_due_amount` and `collections_fee` at the ACE batch date; no other balance is added and no balance is stored | legacy RWB-E4-006 AC1; Physical Schema v6 DF-ACE-020, DF-ACE-022 and DF-ACE-024 |
| BR3 | The settlement range and the floor are values of the rule set in force, read with the rule id and version; the floor is applied to the range and no amount below it leaves unflagged | legacy RWB-E4-006 AC1; R-SET-01, R-SET-05; BR-S1-006 |
| BR4 | A stale account data product stops the step with MSG-P1-001 and nothing is calculated | VR-S1-006-1; FSD S1 A2.6.3.1 |
| BR5 | `payoff_as_at` older than the freshness limit blocks the calculation and a fresh payoff is requested through rwb-integration | R-SET-02, R-SET-03 |
| BR6 | A missing payoff or a missing floor holds the calculation as UNMATCHED_EXCEPTION, names the missing field and raises a task for the case owner | R-SET-25 |
| BR7 | The result is recorded in the local decision record with the rule id and version before the answer is composed, and a result that cannot be recorded does not proceed | legacy RWB-E4-006 AC1, AC2; DP-03; REQ-S1-004 |
| BR8 | No value a business person may change is written in code: the formula, the range bounds, the floor, the freshness limit and the lists are values in force read with their version | BR-S1-006; FSD S1 A2.6.3.1 |
| BR9 | The step needs right U in the capability area Treatment and offer; the check is the platform guard library's and no role list is written here | TSD S1 T6.1; legacy permission checks |
| BR10 | This service writes no case table, no treatment row and no rule row, and reads no table of another service | DP-01; GAP-2615 |

**Where each rule lives in the target.** BR1 and BR2 are the `AccountBalanceReadClient` and the absence of any account repository. BR3, BR5 and BR6 are the rule-set adapter and the three named conditions of the settlement route set. BR4 is the freshness gate in front of the read. BR7 is the `DecisionRecordAdapter` and the one transaction. BR8 is the reference-data reads and the Drools runtime of the service template. BR9 is the contract's `security` section and the guard library. BR10 is the schema boundary and the absence of a cross-schema key.

### 9. State transitions

No case status is owned here; the case and its route state are moved by `CaseWorkflow` on rwb-case and by the route-decision submission slice of RWB-E4-005. The only lifecycle this story writes is the calculation and its record.

| Object | From | Event | Condition | To |
|---|---|---|---|---|
| Calculation | absent | the route decision is prepared | the account product is fresh and the rule set is in force | payoff and range calculated, `payoff_as_at` stamped |
| Calculation | calculated | the result is recorded | the decision record is written in the same transaction | recorded with the rule id and version, and answered |
| Calculation | calculated | the record cannot be written | X3 | nothing written, the transaction rolled back, MSG-P7-003 |
| Calculation | absent | the account product is stale | X2 | stays absent with MSG-P1-001 |
| Calculation | calculated | `payoff_as_at` is older than the freshness limit | R-SET-03 | blocked at PAYOFF_AND_RANGE_SET, no range offered, a fresh payoff requested |
| Calculation | calculated | the payoff or the floor is missing | R-SET-25 | UNMATCHED_EXCEPTION with the missing field named and a task raised |
| Calculation | recorded | the route is approved as settlement and the offer is prepared | R-SET-04, R-SET-05 | re-read for the offer step; the re-read is rwb-treatment's call and not this story's write |

The calculation carries no `state` of its own beyond the standard record lifecycle of the decision record (TSD S1 T3.0). It has no workflow state machine: it either commits its one transaction or writes nothing.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The rwb-valuation squad, service identity of `rwb_valuation` | Runs the calculation on the case's behalf; holds SELECT on the ACE account product only |
| RW-CASEOWN, case owner (right U) | Prepares the route decision of a case in scope and thereby triggers the calculation |
| RW-RESTRUCT, restructuring officer; RW-SPECIAL, hardship and vulnerability specialist; RW-GUARANT, guarantee officer (right U) | The same right in the same capability area, on the cases in scope |
| RW-TEAMMGR, RW-PRODHEAD, RW-CREDCOMM, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE (right R) | Read the payoff, the range and the floor on SCR-13; they trigger nothing here |
| SY-CASEWF, SY-RULES, SY-AGENT | Read as service identities through the same checks |
| rwb-source-data (P1) | Owns the ACE account data product, its freshness and the `v_ace_*` views it grants |
| rwb-decision (P7) | Owns the settlement route set, its approval, its version and the central ledger |
| rwb-access (P4) | Owns the roles, the rights and the scope data the guard answers with |
| rwb-integration (P2) | Owns the fresh-payoff request to EAPI that R-SET-03 asks for |
| No delegation of authority level applies | The story calculates and records; it approves nothing and moves no case |

No credential and no personal name appears in the request, the record, the workflow input or the logs. The account is held as its ACE business key and never as a customer identifier.

### 11. Data

| BR Field ID | Entity | Fields | Read or write |
|---|---|---|---|
| DF-ACE-001 to DF-ACE-042 | `recovery.v_ace_account` (ACE data; view owned by rwb-source-data) | account_key, account_code, account_status, contract_no, product_category_efs, total_balance and 36 more, as the legacy data row lists them | Read only, SELECT |
| DF-ACE-020, DF-ACE-022, DF-ACE-024 | `recovery.v_ace_account` | total_balance, past_due_amount, collections_fee | Read only: the three balances of the payoff |
| DF-ACE-001 to DF-ACE-005, DF-ACE-006, DF-ACE-011 | `recovery.v_ace_account` | account_key, account_code, account_name, account_status, account_status_date, contract_no, product_category_efs | Read only: the account of the case and its scope |
| `v_ace_batch_status` (no DF id in the legacy story) | `recovery.v_ace_batch_status` (view owned by rwb-source-data) | the product and its date | Read only: the freshness gate VR-S1-006-1 and the `payoff_as_at` stamp |
| DF-REF-001 to DF-REF-015 | `rule_row` (`rwb_decision`, owner P7) | rule_id, rule_version, route_set, from_state, event_code and 11 more | Not read directly: the evaluated package returns the rule id, the version, the range bounds and the floor |
| DF-DEC-001 to DF-DEC-018 | `decision_record` (local, in `rwb_valuation`) and `decision_log_entry` (`rwb_decision`, owner P7) | all fields of the record | Write the local record through the library in the same transaction; the central ledger is sealed by P7 |
| DF-TRT-001 to DF-TRT-014 | `treatment` (`rwb_treatment`, owner S2) | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | Named by its owner and not written here: the treatment record is opened by the settlement route after approval |

The payoff, the range and the floor are held in this story only as the outcome of the local decision record and as elements of the answer; no table of this service holds them, because the ownership rows give S1 no table and TSD S1 T3.1 declares no payoff, range or floor table (GAP-2615; ASM-4317). No foreign key points into a view, no column of another service's table is joined, and no balance is copied into `rwb_valuation` (DP-01). **No personal data** appears in the record, the answer or the logs.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-valuation (S1); base `/api/recovery/valuation/v1` (DP-13). This story supplies the calculation part of the route answer; the published shape, the error set and the fakes are declared by RWB-S1-E4006-CON.

| Method | Path | Request and response | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/route` | `RouteRequest` in, `Approval` out (TSD S1 T-A.2); the answer carries the payoff, `payoff_as_at`, `settlement_range_low`, `settlement_range_high`, `floor_price`, the rule id, the rule version and the calculation state | Treatment and offer U, scope applied, through the guard library | `Idempotency-Key` header required |

The element names of the range, the floor and the as-at date are the names the routing workbook uses; the element name of the payoff amount itself is Not specified in the source documents (GAP-2620; ASM-4322). No second operation is claimed: the FSD lists one endpoint for the feature and it is the route operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The account and balance data-product read (operation name Not specified in the source documents (GAP-2616; ASM-4318)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | `total_balance`, `past_due_amount` and `collections_fee` of each account of the case at the ACE batch date, with the product date; faked |
| The freshness read (operation name Not specified in the source documents (GAP-2616; ASM-4318)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The account product and its batch date for VR-S1-006-1; faked |
| The rule-set-in-force read (operation name Not specified in the source documents (GAP-2616; ASM-4318)) | `/api/recovery/decision/v1` | P7 rwb-decision | The settlement route set at its version, with the range bounds, the floor and the rule id; faked |
| `GET /cases/{caseId}` family | `/api/recovery/case/v1` | P3 rwb-case | The case and its account set, to resolve the accounts to read; faked |
| `POST /authorise` | `/api/recovery/access/v1` | P4 rwb-access | The capability area, the right and the scope of the caller; faked |

Each row is one hop, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). This story has no C dependency, so every row is built against its fake.

#### 12.3 Events published

None. The ownership rows give rwb-valuation no event: the topic `rwb.valuation.events.v1` exists with its `.retry` and `.dlt` under the naming rule, but this story declares no event, no event name and no outbox row on it. The only publication of the step is the decision record, which the library of DP-03 sends to `rwb.decision-record.v1`, and that is the library's publication and not an event of this service.

#### 12.4 Events consumed

None. FSD S1 A2.6.2 step 1 names the trigger set as "a completed ACE batch, an event or a timer" and no source publishes an event name for any of them; the ownership rows give S1 no job and no event, so the calculation runs inside the route-decision command and its freshness is proved by VR-S1-006-1 (GAP-2619; ASM-4321).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `RouteDecisionWorkflow` | Workflow, one execution per case per assessment, continues-as-new | `rwb-valuation` in namespace `rwb-recovery` | Input: the case, the account set and the rule set in force; signals: the freshness answer of the account product and the rule version |
| `calculatePayoffAndRange` | Activity | `rwb-valuation` | The account set and the business date in; the payoff, `payoff_as_at`, the range bounds, the floor, the rule id and version and the decision record out, in one transaction |
| `readAccountBalances` | Activity | `rwb-valuation` | The account keys in; the three balances and the product date out; no write |

The activity names are a design choice of this story; the baseline RWB-S1-E4006-CON carries them so that the workflow history stays stable across the two documents.

#### 12.6 Schedules

None. The ownership rows give S1 no job, and this story declares no Temporal Schedule and no legacy Quartz job. The phrase "a completed ACE batch, an event or a timer" would be a Schedule of this service if a source named one, and none does (GAP-2619; ASM-4321).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| None | S1 declares no payoff, range or floor table | The ownership rows give S1 no table and TSD S1 T3.1 declares only `valuation` and `score`; the outcome lives in the decision record (GAP-2615; ASM-4317) |
| decision_record | PLT library, created in `rwb_valuation` | The local decision record of DP-03, declared through RWB-PLT-E1027-CON |
| idempotency_key | PLT library, created in `rwb_valuation` | The key of the repeated command and the answer it holds |

No migration, index or column is added by this story, and no table of another owner is declared: `v_ace_account` and `v_ace_batch_status` (P1), `rule_row`, `decision_log_entry` and `approval` (P7), `treatment` (S2) and `recovery_case` and `timer` (P3) are named by their owners.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data account and balance fake | Account `A-0001` of case `RC-2026-000401` with total balance 1240000, past due amount 86000 and collections fee 4500 at ACE batch date 2026-12-14; an account with no row; no answer beyond 2 s | AC1, X4 |
| rwb-source-data freshness fake | The account product at the business date, and the same product from an earlier date | X2, TC-S1-E4006-APP-02 |
| rwb-decision rule-set fake | The settlement route set in force with its rule id and version, its range bounds and its floor; a set with no floor and a set with no range | AC1, X5, X6 |
| rwb-case account-set fake | Case `RC-2026-000401` with account `A-0001`; a case in another state | AC1 |
| rwb-access authorise fake | Treatment and offer, right U accepted and refused | X1 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC2 |
| gateway-bff composite route fake | The merged SCR-13 answer for case `RC-2026-000401`, with the payoff, the range and the floor read once | AC1 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 5 consumed | `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`; the rwb-source-data account and freshness rows, the rwb-decision rule-set row, the rwb-case row and the rwb-access row; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this service and no subscription; the decision record reaches `rwb.decision-record.v1` through the library of DP-03 |
| Temporal | 1 workflow and 2 activities | `RouteDecisionWorkflow`, `calculatePayoffAndRange` and `readAccountBalances` on `rwb-valuation`; no Schedule |
| File | None | The step reads contracts only; the fresh-payoff request of R-SET-03 is rwb-integration's |

### 13. Solution plan

**Build steps.**

1. `PayoffCalculator`: the payoff from `total_balance`, `past_due_amount` and `collections_fee` by the calculation in force, with the formula, the inclusion and the rounding read from governed values (BR2, BR8).
2. `RangeResolver`: the settlement route set in force, the range bounds, the floor and the rule id and version; a missing floor or range raises UNMATCHED_EXCEPTION (BR3, BR6).
3. `FreshnessGate`: VR-S1-006-1 on the account product and the `payoff_as_at` limit of R-SET-03 (BR4, BR5).
4. `AccountBalanceReadClient`, `RuleSetClient` and the rwb-case and rwb-access clients on the contract and its fake (section 12.2).
5. `DecisionRecordAdapter` on RWB-PLT-E1027-CON in the same transaction as the answer (BR7).
6. `calculatePayoffAndRange` and `readAccountBalances` as activities of `RouteDecisionWorkflow` (section 12.5).
7. The calculation elements of the answer and their state, and SCR-13 through the composite route fake (section 12.1).
8. The idempotency row and the repeat answer (section 9).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Done when.** AC1 and AC2 pass on the fakes, the boundary and freshness tests pass, the record carries the rule id and version, and the answer holds the payoff, its as-of date, the two range bounds and the floor with no constant in code.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A role without the Treatment and offer right calls the operation | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required element of `RouteRequest` is absent or invalid, or a governed value the calculation needs is missing | Enter {field}. |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE account data product is stale after a late or failed batch (VR-S1-006-1) | {product} is from {date}. Today's ACE batch has not arrived. |

The four message IDs are those of the legacy story and of FSD S1 A2.6.3.1, copied unchanged. No message text is written in this story beyond these rows.

### 15. Screens and states

The calculation feeds SCR-13 Route decision through the gateway-bff composite route (DP-19).

| Screen | States | What the screen shows from this step |
|---|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted | The payoff and its as-at date, the range bounds, the floor, the rule version, and the calculation state: calculated, blocked on a stale product, or an unmatched exception naming the missing value |

No screen is built here: the field list, the merge order and the states of the composite route are RWB-PLT-N001-CON, and the recommendation and override elements are the sibling stories'.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-006-01 | AC1: the payoff from the three balances, the range with the floor and the record with its rule version | Component | Case `RC-2026-000401`, account `A-0001`, total balance 1240000, past due amount 86000, collections fee 4500, ACE batch date 2026-12-14, the settlement set in force |
| TC-E4-006-02 | AC2: the decision log cannot be written | Component | The decision-record stub stopped; nothing written, no answer, MSG-P7-003 |
| TC-E4-006-03 | Access: a role without the right | Component | A role without Treatment and offer U; 403 with MSG-P4-002 and no read |
| TC-E4-006-04 | Principle 5: a forced decision-log write failure | NFR | A forced failure at the moment of the record; no record, no answer and no event |
| TC-S1-E4006-APP-01 | The boundary and the unmatched path: no balance copy, no foreign schema write, no event, and a missing floor or range holds as UNMATCHED_EXCEPTION | Component | The build scan, an outbox that must stay empty, and a rule set with no floor |
| TC-S1-E4006-APP-02 | Freshness: a stale account product stops with MSG-P1-001 and a `payoff_as_at` older than the limit blocks under R-SET-03 | Component | The freshness fake in both states and the `payoff_as_at` limit in force |

The four legacy case IDs are the legacy cases of RWB-E4-006 in their legacy order, with the Level column added; TC-E4-006-01 is Component because the calculation is tested on its fakes. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in code: the formula, the range bounds, the floor, the freshness limit and the lists are read with their version and never written as a constant, a default or a fixture in production code (BR-S1-006).
- No personal data in events, workflow inputs or logs: the account is an ACE business key, and the payoff, the range and the floor are amounts and codes only.
- ACE data only through the owner's contract or the service's own `v_ace_*` view, SELECT only, with no copy and no cross-schema key (DP-05, DP-01).
- The case stays with rwb-case, the rule set and the ledger with rwb-decision, and the treatment record with rwb-treatment: none is declared here.
- One base, one topic, one queue and one login per service; no document or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element returns: no monolith base `/api/recovery/v1`, no account copy table, no Quartz row, no Schedule and no data-lake extract (DP-17).
- A calculation that cannot be recorded does not proceed (BR7).

### 18. Traceability

| Source | Reference | Used in |
|---|---|---|
| Legacy story | RWB-E4-006, disposition Split (rework); AC1 and AC2 are owned by this story, verbatim; TC-E4-006-01 to -04 map onto this deliverable | 1, 5, 7, 14, 16 |
| Feature | FEAT-VAL-06 Calculate the payoff and settlement range, module S1, epic E4, depends on FEAT-DRI-07 | 1, 2, 3 |
| FSD S1 v3 | A2.6.1 intent and metric; A2.6.2 steps and integration points ALS and GL and the Rules component; A2.6.3.1 VR-S1-006-1 and BR-S1-006; A2.6.3.3 roles; A2.6.4.1 AC-S1-006-01 and A2.6.4.3 AC-EXC-S1-006-01 and -02; REQ-S1-004; SCR-13 | 2, 3, 5, 8, 12, 15 |
| TSD S1 v2 | T2 components; T3.0 standard columns; T3.1 `valuation` and `score`; T5.2 cross-module interfaces; T6.1 rights; T-A.1 and T-A.2 API-S1-001 | 3, 10, 11, 12 |
| Epics 3 to 8 Specification v3 | E4 S1 FEAT-VAL-06 row; FEAT-VAL-07 depends on it; FEAT-TRT-02 depends on it | 1, 3 |
| Routing logic v4 | R-SET-01, R-SET-02, R-SET-03, R-SET-04 and R-SET-05 (D6.4); R-SET-25 | 3, 8, 9 |
| Logical data model and Physical Schema | DF-ACE-001 to DF-ACE-042 and DF-ACE-020, DF-ACE-022, DF-ACE-024; DF-DEC-001 to DF-DEC-018; DF-REF-001 to DF-REF-015; DF-TRT-001 to DF-TRT-014 | 11 |
| Patterns | DP-03, DP-05, DP-13, DP-19 (Template and Rules v1 §R5.5) | 13 |
| Gaps and assumptions | GAP-2615 to -5; ASM-4317 to -5 and -7 | 1, 3, 5, 7, 11, 12, 13 |
| Decisions | ADR-010, ADR-013, ADR-014, ADR-020, ADR-022; D-RCV-35 U1; D-RCV-60 | all |

### 19. Out of scope

- The route recommendation, its reasons and the alternatives: FEAT-VAL-07 and its story; the route agent, which is rwb-agent's (P10).
- The approval of the route, the override reason and the case move: the route-decision submission slice of RWB-E4-005 and rwb-case (P3).
- The offer built inside the range, the counter-offer and the settlement letter: rwb-treatment (S2) on R-SET-04 and the settlement stories.
- The ACE balances, their batch date and their freshness: rwb-source-data (P1); the load and the correction of ASL and GL data are outside the Workbench.
- The settlement route set, its range bounds, its floor, its approval and its version: rwb-decision (P7); the values are read, not fixed, here.
- The fresh-payoff request to EAPI and the interface behind it: rwb-integration (P2) on R-SET-03.
- The roles, scopes and masking behind the right: rwb-access (P4) and the guard of the service template.
- The composite route, the merge order and the field list of SCR-13: RWB-PLT-N001-CON and the edge stories.
- The decision-record library's own schema and migration: RWB-PLT-E1027-CON.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
- The deployment, the flag, the dashboards, the alerts and the runbook of this capability: the operations story of this legacy key.
