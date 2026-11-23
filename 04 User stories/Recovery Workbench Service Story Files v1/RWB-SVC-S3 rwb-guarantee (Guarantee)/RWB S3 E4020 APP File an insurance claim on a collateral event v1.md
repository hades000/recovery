# RWB-S3-E4020-APP File an insurance claim on a collateral event

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S3-E4020-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-guarantee |
| Service epic | RWB-SVC-S3 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-020 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S3-I |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S3-E4020-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S3 rwb-guarantee v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-020 split out for rwb-guarantee (S3). Both legacy criteria of the key, AC1 and AC2, are copied word for word with their origin tags, and the two cross-service parts of AC1 are mocked with one added `Given` line each: the collateral read of rwb-source-data and the case signal that carries the re-appraisal request. The claim becomes a `guarantee_claim` row of type `COLLATERAL_INSURANCE` filed from SCR-17 on base `/api/recovery/guarantee/v1` (DP-13) and reached through the gateway-bff composite route (DP-19); the collateral and appraisal facts are read through rwb-source-data's contract (DP-05); the claim row and the local decision record are written in one transaction (DP-03); and the re-appraisal is requested on the case signal to the parent `CaseWorkflow` of rwb-case, because Architecture v5 slide 13 gives S3 no REST edge to rwb-valuation and the SVAF order of the feature is FEAT-VAL-01. The service publishes no event, because the ownership rows give S3 none. No source gives the collateral-insurance claim a rule row, a deadline source, a claimed-amount source, an insurer interface or a map between the claim states and the X7 states (GAP-2736; ASM-4543). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner**, I want **to file the claim where collateral is stolen, written off or damaged, and trigger re-appraisal**, so that **no guarantee claim misses its deadline**.

This is the application slice of legacy RWB-E4-020. It owns:

- the two legacy criteria of the key, AC1 and AC2, copied verbatim with their origin tags, and the messages and the screen they name;
- the collateral-event branch of `GuaranteeClaimWorkflow`, the one workflow the ownership rows give S3, on task queue `rwb-guarantee` in namespace `rwb-recovery`, as a child of the case workflow, with the activities `readCollateralFacts`, `evaluateClaimRules`, `recordAndApply` and `reportCollateralEvent`;
- the creation of the claim row: `guarantee_claim` with `claim_type` taken from `LOV-CLAIM-TYPE` as `COLLATERAL_INSURANCE`, the claim deadline, the claimed amount and the status of the row, through `POST /cases/{caseId}/guarantee-claims` with right C (API-S3-001);
- the filing of that claim and the write of `filed_at` and `status = FILED` through `PATCH /guarantee-claims/{claimId}` with right U (API-S3-002), on the base `/api/recovery/guarantee/v1` (DP-13);
- the read of the collateral and appraisal facts of the case through rwb-source-data's contract, with no `v_ace_*` grant in `rwb_guarantee` (DP-05);
- the re-appraisal request, raised on the case signal to the parent `CaseWorkflow` of rwb-case so that the route stage can order the appraisal under FEAT-VAL-01;
- the claim row and the local decision record in one transaction, with the rule id and the rule version in force (DP-03);
- the claim slice of SCR-17 Guarantee claim this step produces, reached through the gateway-bff composite route (DP-19).

It does not own: the published shape of the claim resource, the element set, the error set, the versioning rule and the fakes, which are RWB-S3-E4020-CON; the preparation of a TCG claim and its checklist, which is FEAT-GUA-01 (legacy RWB-E4-013); the submission to the TCG portal, which is FEAT-GUA-02 (RWB-E4-014); the tracking of the claim to payment and the claim deadline timer, which are FEAT-GUA-03 (RWB-E4-015); the subrogation position, which is FEAT-GUA-04 (RWB-E4-016); guarantor notices and negotiation, which are FEAT-GUA-05 and FEAT-GUA-06 (RWB-E4-017 and RWB-E4-018); the close of the guarantee, which is FEAT-GUA-07 (RWB-E4-019); the X7 deviation flag, its pause and its states, which are rwb-deviation's and FEAT-DVF-07; the re-appraisal order and the SVAF exchange, which are rwb-valuation's and FEAT-VAL-01; the case, its states and the parent workflow, which are rwb-case's; the documents of the claim, which are rwb-document's; the rule rows and the package version, which are rwb-decision's; the roles and the scopes behind the rights, which are rwb-access's; the composite route and the SCR-17 field list, which are RWB-PLT-N001-CON; any interface to an insurer, which no source publishes; and the deployment of this build.

### 2. Business rationale

FSD S3 A2.8 states the feature in one line: files the claim where collateral is stolen, written off or damaged, and triggers re-appraisal. The module problem is unchanged, that guarantee and TCG claims are late because deadlines are not tracked, and so is the module measure: claims filed inside the deadline, 100 percent, read monthly from the decision log and the Workbench records. Two requirements carry it: REQ-S3-002, claim status, payment and any shortfall are recorded on the case, and REQ-S3-007, claims are filtered for eligibility before submission so that ineligible claims are not filed. The Epics 3 to 8 Specification v3 gives the feature as FEAT-GUA-08, kind user, primary role case owner, systems Workbench and SVAF, depends on FEAT-VAL-01.

Two other keys meet this one and neither is built here. FSD S8 A2.16 runs the X7 collateral event end to end — files the insurance claim, re-appraises the collateral and returns the case to the route decision — and names FEAT-GUA-08 as its prerequisite. Business Rules and Routing Logic v4 gives the same event as R-LIT-79: collateral stolen, damaged, written off, or the insurance lapsed, re-appraise and return the case to the route decision at D6, systems SVAF and Workbench, 10 working days; and as R-DEV-06: with the code in (X6, X7), the agent handles within policy and a person approves an insurance claim.

The monolith did this in one S3 process: it read `v_ace_collateral`, `v_ace_collateral_detail` and `v_ace_valuation` on its own connection, wrote `guarantee_claim`, `document` and `decision_log_entry` in the same schema and moved the case. In the 19-service target the same act touches four owners, and this story is what keeps them apart while the act stays the same.

- **the collateral and the appraisal are not this service's.** Slide 8 reserves the 30 `recovery.v_ace_*` views to rwb-source-data, and FEAT-VAL-01 orders the appraisal to SVAF and records its result through rwb-valuation. The facts arrive through rwb-source-data's contract and leave through the case signal; `rwb_guarantee` holds no `v_ace_*` grant and this story orders no appraisal (DP-05; GAP-2736).
- **the claim is this service's.** `guarantee_claim` is the one table the ownership rows give S3 and `LOV-CLAIM-TYPE` already holds the member `COLLATERAL_INSURANCE`, so a collateral-insurance claim needs no new entity, no new table and no new list (TSD S3 T3.1, T3.2).
- **the deviation is rwb-deviation's.** X7 is a deviation code of S8 with its own states, and this story raises no deviation row and moves no deviation state (FSD S8 A2.16.3.2).
- **the case stays with rwb-case.** The stage reports its outcome and the re-appraisal request to the parent workflow; the parent applies the case state and the clock, and this service writes no `recovery_case`, `task` or `timer` row (DP-01).
- **the decision is recorded first, and locally.** AC1 asks for the result to be written with the rule version, and AC2 is the rule that makes it trustworthy: when the record cannot be written nothing changes and the user sees MSG-P7-003. Under DP-03 the record is local and hash-linked and commits with the claim row (R-UNI-38, R-UNI-39).
- **nothing is published.** The ownership rows give S3 no event type, so no claim event is added to `rwb.guarantee.events.v1`; the outward facts are the claim answer, the case signal and the decision record, which the library sends to `rwb.decision-record.v1` (GAP-2736).

The claim is also a claim without a published rule. FSD S3 A2.8.3.1 states VR-S3-008-1 and BR-S3-008 only, and the 32 rows of the GUARANTEE set in Business Rules and Routing Logic v4 carry no collateral-insurance row; the branch therefore applies the two rows that exist, the reference data behind them and the person-approval condition of R-DEV-06, and it asserts no threshold, no window and no deadline that a source does not state (GAP-2736; ASM-4546).

### 3. Preconditions

- RWB-S3-E4020-CON is published: the collateral-event elements, the required set, the claim type and status list codes, the rights, the error envelope and the fakes are baselined and handed to this story (H).
- RWB-PLT-E1027-CON is published (DP-03): the local decision-record writer joins the caller's transaction and a failed write stops the step with MSG-P7-003 (H).
- RWB-PLT-N001-CON is published (DP-19): SCR-17 Guarantee claim reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (H).
- The service runs as its own login on schema `rwb_guarantee`, owns `guarantee_claim` and holds the library objects `decision_record` and `idempotency_key`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery_case`, `decision_log_entry`, `v_ace_collateral` or `v_ace_valuation` is refused by the database and fails the boundary test.
- `GuaranteeClaimWorkflow` runs as a child of the parent `CaseWorkflow` of rwb-case on `rwb-guarantee`, started when the case enters the guarantee stage or when the collateral event is signalled, and reports its stage outcome to the parent; the parent applies the case state, the clock and the re-appraisal order.
- The collateral and appraisal facts of the case are read through rwb-source-data's contract; the operation name, the request and the answer fields, the field identifiers of the three legacy views and the freshness rule are Not specified in the source documents (GAP-2736; ASM-4545).
- The rule package in force is consumed on `rwb.decision.RulePackageInForce.v1`; the version carried on the decision record is the row in force and no version number is asserted (R-UNI-38).
- The claim type `COLLATERAL_INSURANCE` and the claim status values are the members of `LOV-CLAIM-TYPE` and `LOV-CLAIM-STATUS` of TSD S3 T3.2, read as values in force with their version and never written in code (BR-S3-008).
- The claim deadline and the claimed amount have no published source for this claim type: `claim_deadline` and `claimed_amount` are required fields of `guarantee_claim` and the branch takes them from the filing officer and the appraisal of record (GAP-2736; ASM-4543).
- The capability area is Treatment and offer: right C on the create and right U on the filing for RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL and RW-GUARANT, the rows of the legacy permission table and of TSD S3 T6.1.
- No approval is needed to build against a Draft contract baseline; RWB-S3-E4020-CON tags the version when its tests pass (ASM-4548).

### 4. Flow

1. A collateral event is reported on a case that carries a guarantee or collateral insurance: collision, theft, damage, a write-off of the asset or a lapsed policy. The X7 deviation is rwb-deviation's and its flag arrives as a case fact; this story files the claim and never raises the deviation (ASM-4547).
2. `readCollateralFacts` reads the collateral of the case and its last appraisal through rwb-source-data's contract: the collateral key, the type, the value and the appraisal number, value and date; a missing or stale fact stops the branch and raises a task (GAP-2736; ASM-4545).
3. The case owner opens SCR-17 on the case through the gateway-bff composite route and chooses the collateral-insurance claim; the guard checks Treatment and offer right C and the scope before any read (DP-19; AC1).
4. `evaluateClaimRules` applies the VR-S3-008-1 and BR-S3-008 rows of FSD S3 A2.8 and the rule package in force: the claim type, the deadline, the claimed amount against the appraised value, the required documents and the person-approval condition of R-DEV-06 (AC1; GAP-2736).
5. `POST /cases/{caseId}/guarantee-claims` creates the `guarantee_claim` row: `claim_type` = `COLLATERAL_INSURANCE`, `claim_deadline`, `claimed_amount`, `status` = `PREPARING`, the collateral element and the appraisal reference; a repeated `Idempotency-Key` returns the first answer and creates no second claim (API-S3-001; DP-13).
6. The officer files the claim with the insurer outside the Workbench and records the filing; the branch takes the filing date as the business date, because no interface to an insurer is published (GAP-2736; ASM-4544).
7. `recordAndApply`, one transaction: `guarantee_claim` is updated with `filed_at`, `status` = `FILED`, the optimistic `version`, `updated_at` and `updated_by`; the decision record is written with the decision code, the rule id and the version in force, the claim, the collateral key, the appraisal number and the role of the officer; and the outbox row follows in the same transaction. A failed record write leaves the claim in `PREPARING` and shows MSG-P7-003 (AC1, AC2; DP-03).
8. `PATCH /guarantee-claims/{claimId}` answers the claim in its new state with its deadline, its amount, the collateral and the appraisal it was filed on; a stale `version` is refused with 409 and nothing is written (API-S3-002).
9. `reportCollateralEvent` reports the stage outcome to the parent `CaseWorkflow`: the claim is filed and the collateral needs re-appraisal. The parent applies the case state and asks the route stage to order the appraisal under FEAT-VAL-01; this service writes no case row and orders no appraisal (GAP-2736; ASM-4544).
10. A claim of the case that is already in `PREPARING` or `FILED` for the same collateral event is returned as it stands and no second row is created; a claim of another type on the same case is a separate row of the same table (TSD S3 T3.3).
11. The decision record reaches `rwb.decision-record.v1` through the library of DP-03, keyed by the case, with no personal data on it; this service publishes no event of its own (GAP-2736).
12. SCR-17 shows the claim, its deadline, the collateral, the appraisal it was filed on and the result, read through the composite route, read only (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written or is refused for a missing element | The transaction writes nothing, the claim stays in `PREPARING` and no filing is recorded | MSG-P7-003 | AC2, TC-E4-020-02, TC-E4-020-04 |
| X2 | The role does not hold right C or U of Treatment and offer, or the caller is out of scope | 403 before any read or write, and no record is written | MSG-P4-002 | TC-E4-020-03 |
| X3 | A required element of the claim, the collateral fact or the appraisal is absent or invalid | The branch does not run, nothing is written and the missing element is named | MSG-GEN-001 | TC-E4-020-01, TC-S3-E4020-APP-01 |
| X4 | The collateral of the case or its last appraisal is missing, stale or not readable through the owner's contract | The branch holds, names the missing fact and raises a task; no claim is created on an unread fact | None | TC-S3-E4020-APP-01 |
| X5 | The claim's `version` is stale, or the same create arrives twice with one `Idempotency-Key` | 409 with nothing written for a stale version; the first answer for a repeated key and no second claim | None | TC-S3-E4020-APP-02 |
| X6 | The case signal is not accepted by the parent, or the workflow is waiting and the record is behind | The claim stays filed and the re-appraisal request is reported again on the next signal; the claim is never re-filed by the retry | None | TC-S3-E4020-APP-02 |
| X7 | A component, a statement or a test reaches `recovery_case`, `v_ace_collateral`, `v_ace_valuation`, another service's schema or a `v_ace_*` view | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | TC-S3-E4020-APP-01, s17 |
| X8 | No rule row, deadline source, claimed-amount source or insurer interface is stated for this claim type | The branch applies the rows that exist, takes the value on the claim and calls no insurer; the gap stays open | Not specified in the source documents (GAP-2736; ASM-4543) | Sections 8, 11, 12 and 13 |

X1 and X2 are the exception paths the legacy key carries, in the words of FSD S3 A2.8.4.3; X3 and X5 to X7 are the paths the target call types, the idempotency rule and the schema boundary add; X4 and X8 are the boundary this key records, because the collateral facts and the insurer channel have no published shape.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S3-E4020-CON, the rwb-source-data read fake, the case-signal fake, the decision-record stub and the composite route fake, on its own schema, and needs no live P1, P3 or S1 |
| Negotiable | The activity names, the decision code and the layout of the claim fragment are this story's choice; the operation, the rights, the messages, the claim type and the screen are fixed |
| Valuable | A collateral event becomes a filed claim with its deadline and its record, and the collateral reaches re-appraisal without a person carrying the case between the two services |
| Estimable | One workflow branch, four activities, two operations, one record write, one case report and one screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each path runs on synthetic claims, collateral facts and appraisals through the contract fakes, plus the stopped record write, the repeated key, the stale version and a missing collateral fact |

### 7. Acceptance criteria

```gherkin
Feature: File an insurance claim on a collateral event

  Scenario: AC1 File an insurance claim on a collateral event (legacy RWB-E4-020 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-source-data contract mock returns the collateral of the case and its last appraisal
    Given the rwb-case contract mock returns the case signal accepted with the filed claim and the re-appraisal request
    When the user acts on the screen
    Then files the claim where collateral is stolen, written off or damaged, and triggers re-appraisal
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E4-020 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The two criteria are the legacy criteria of RWB-E4-020 word for word, with their origin tag added and nothing else changed: the legacy wording `the data and the rule version this feature needs are in place`, `the user acts on the screen` and `the decision log cannot be written` all stand, and no deadline, amount, threshold or version number is added. The two cross-service parts of AC1 are mocked and those two `Given` lines are the only additions: the collateral and appraisal fact is a read of rwb-source-data's contract, and the re-appraisal is a request on the case signal to rwb-case. AC2 needs none, because the decision record is local to this service. "The decision log" of AC1 and AC2 is the local decision record of DP-03 on its way to `rwb.decision-record.v1`; `decision_log_entry` stays P7's ledger and is neither written nor read here. Nothing in AC1 fixes what the claim deadline is, what the claimed amount must be or which insurer is called, because no source read for this key states them (GAP-2736; ASM-4543).

### 8. Business rules

| ID | Rule | Message |
|---|---|---|
| VR-S3-008-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S3-008 | No value a business person may change is written in code; it is read from reference data with its version | None |

| ID | Rule | Source |
|---|---|---|
| R-DEV-06 | X1 to X7, DEV_FLAGGED, OWNER_ASSIGNED, deviation_code in (X6,X7): agent handles within policy; a person approves an insurance claim. To DEV_WITH_OWNER | Business Rules and Routing Logic v4 |
| R-LIT-79 | Litigation, D7, DEVIATION_HOLD, X7_COLLATERAL_EVENT: collateral stolen, damaged, written off, or the insurance lapsed; re-appraise the collateral and return the case to the route decision at D6. To TO_TREATMENT, SVAF and Workbench, 10 working days | Business Rules and Routing Logic v4 |
| R-DEV-09 | X1 to X7, DEV_WITH_OWNER, DEVIATION_RESOLVED, deviation_code in (X1,X7): record the outcome; the same decision resumes. To DEV_RESOLVED | Business Rules and Routing Logic v4 |

The two FSD rows are copied character for character from FSD S3 A2.8.3.1 and are the only rule rows that module gives this feature. The three rows below them are referred to, not owned: R-DEV-06 is the person-approval condition the branch honours, R-LIT-79 names the same collateral event from the litigation route and the re-appraisal it orders, and R-DEV-09 records the X7 outcome in rwb-deviation. The 32 GUA rows of the workbook hold no collateral-insurance row, so no threshold, window or state of this branch is taken from them (GAP-2736; ASM-4546).

| ID | Rule | Source |
|---|---|---|
| BR1 | A collateral-insurance claim is a `guarantee_claim` row with `claim_type` = `COLLATERAL_INSURANCE`, filed from the collateral event of the case, and no new entity, table or list is created | TSD S3 T3.1, T3.2; FSD S3 A2.8.3.2 |
| BR2 | The claim type, the claim status, the deadline, the claimed amount and the document set are values with their version; no threshold, window, percentage or amount is a constant, a default or a branch of the build | BR-S3-008; FSD S3 A2.8.3.1 |
| BR3 | The claim row and the decision record commit in one transaction, with the rule id and the version in force; a failed write changes nothing and shows MSG-P7-003 | DP-03; R-UNI-38, R-UNI-39; AC2 |
| BR4 | The branch files one claim per collateral event of the case: a repeated command is caught by the `Idempotency-Key` and a repeated signal by the inbox key, and neither raises a second row | TSD S3 T-A.2; R-UNI-40 |
| BR5 | The collateral and appraisal facts are read through rwb-source-data's contract; `rwb_guarantee` holds no `v_ace_*` grant and no ACE table is read | DP-05; Architecture v5 slide 8; GAP-2736 |
| BR6 | The re-appraisal is requested on the case signal and ordered by the route stage under FEAT-VAL-01; this service calls no rwb-valuation operation, orders no appraisal and orders no SVAF exchange | Architecture v5 slide 13; ASM-4544 |
| BR7 | The case state, the case clock, the X7 deviation flag and its states are not written here: the stage reports its outcome and rwb-case and rwb-deviation own the rest | DP-01; FSD S8 A2.16.3.2 |
| BR8 | No call reaches an insurer, SVAF or the TCG for this claim: no interface to an insurer is published, and INT-29 is TCG only and not available today | TSD S3 T5.1; GAP-2736 |
| BR9 | No event is published and no Schedule is declared: the ownership rows give S3 no event type and no job, and the wait is a durable workflow timer or the next signal | context pack S3 ownership rows; GAP-2736 |
| BR10 | No person name, address, contact value or identity number enters `rwb_guarantee`, the decision record, a log or a workflow input; the parties are identifiers and the officer is a role | Template and Rules §R7.2 (s17) |

**Where each rule lives.** BR1 and BR2 are the create of the row and the list reads. BR3 is the activity `recordAndApply` and the library adapter behind it. BR4 is the `Idempotency-Key` rule of the POST and the inbox key of the consumer. BR5 is the client of the owner's contract and the boundary test of the build. BR6 and BR7 are the report to the parent workflow and the absence of any case or deviation write. BR8 and BR9 are the absences a build scan proves: no insurer client, no `v_ace_*` statement, no outbox row of a claim event and no Schedule. BR10 is the guardrail of the payloads and the logs.

### 9. State transitions

The case states and the deviation states below are not this story's: the stage reports its outcome and the owners apply it. What this story owns is the claim row and the two moves it makes on that row.

| From (claim row, `guarantee_claim.status`) | Event | Condition | To |
|---|---|---|---|
| none | Collateral event reported and the create accepted | Right C, the collateral fact and the appraisal are present | `PREPARING`, one row per collateral event (BR1, BR4) |
| `PREPARING` | Filing recorded by the officer | Right U, a valid deadline and claimed amount, the record written in the same transaction | `FILED`, with `filed_at` (AC1) |
| `PREPARING` | The record cannot be written | X1 | `PREPARING`, nothing filed (AC2) |
| `FILED` | The same create or signal arrives again | X5 | `FILED`, one row and no second record |
| `DEFECT`, `PAID`, `REJECTED` | Any event of this story | The row is not in a state this branch moves | Unchanged; the tracking, the rejection and the payment are FEAT-GUA-03 and FEAT-GUA-07 |

| Object (owner) | State named by the sources | This story |
|---|---|---|
| Case (rwb-case, P3) | `DEVIATION_HOLD` and `TO_TREATMENT` of R-LIT-79; `DEV_FLAGGED`, `DEV_WITH_OWNER`, `DEV_RESOLVED` and `DEV_REROUTE` of R-DEV-01 to R-DEV-22 (rwb-deviation, S8) | Reported, never written: the parent applies them from the stage outcome |
| Claim row (S3) | `PREPARING`, `FILED`, `DEFECT`, `PAID`, `REJECTED` of `LOV-CLAIM-STATUS` (TSD S3 T3.2) | Written: this story moves `PREPARING` to `FILED` and no further |

No source maps the five members of `LOV-CLAIM-STATUS` to the case or deviation states, so the two vocabularies are declared side by side and a filed claim is reported to the parent without a state name of its own (GAP-2736; ASM-4547). The `state` column of the row is varchar(40) with no check constraint, so a new row state is a data change and not a build change.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Treatment and offer CRU in TSD S3 T6.1 and the primary role of FSD S3 A2.8.3.3: opens SCR-17, creates the claim, records the filing and reads the result |
| RW-GUARANT, guarantee officer | Treatment and offer CRU: the "also uses" role of FSD S3 A2.8.3.3; reviews the claim and records the filing |
| RW-RESTRUCT (CRUA), RW-SPECIAL (CRU), the "hardship and vulnerability specialist" of FSD S3 A2.8.3.3 | Treatment and offer C and U of the legacy permission table: create and file the claim of the case in scope |
| RW-TEAMMGR (R), RW-COMPLAIN (R), RW-FRAUD (R), RW-LITOFF (R), RW-LEGAL (R), RW-CONDUCT (R), RW-PRODHEAD (RA), RW-CREDCOMM (RA), RW-RISK (R), RW-COE (R), RW-AUDIT (R), RW-BIANAL (R), RW-TRIBE (R) | TSD S3 T6.1 rows for the capability area: read the claim and its record in scope, and create or file nothing |
| SY-CASEWF, SY-RULES, SY-AGENT | Treatment and offer R: the service identities read the step and are subject to the same checks as people |
| rwb-guarantee service identity | Reads the collateral facts through the owner's contract, runs the four activities, writes the claim row and the decision record, reports the collateral event and answers the two operations; it holds no grant on another schema and no `v_ace_*` grant |
| rwb-case, rwb-valuation, rwb-deviation, rwb-document, rwb-decision, rwb-access | Hold the case, the appraisal, the deviation, the documents, the rules and the rights this story refers to and does not write |

The rights are the rows of TSD S3 T6.1 and of the legacy permission table of this key, and nothing wider. R-DEV-06 adds the condition that a person approves an insurance claim: the branch never files a claim from an agent or a rule alone, and the approval is the officer's recorded filing. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and checked by the platform guard, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-TRT-015 to DF-TRT-022 | `guarantee_claim` (S3) | id, case_id, claim_type, claim_deadline, claimed_amount, filed_at, paid_amount, status | Write: the whole row on the create, then `filed_at`, `status`, `version`, `updated_at` and `updated_by` on the filing; read the rest |
| DF-ACE-091 to DF-ACE-098 | `v_ace_collateral` (P1 via contract) | collateral_no, asset_key, account_key, collateral_value, collateral_type, register_date and 2 more | Read through rwb-source-data's contract; no `v_ace_*` grant here (BR5) |
| DF-ACE-196 to DF-ACE-207 | `v_ace_collateral_detail` (P1 via contract) | asset_key, title_doc_no, plot_no, area_text, province, lien_rank and 6 more | Read through the same contract; no grant here |
| DF-ACE-187 to DF-ACE-195 | `v_ace_valuation` (P1 via contract) | valuation_key, asset_key, appraisal_no, appraisal_type, appraised_value, appraisal_date and 3 more | Read through the same contract, for the appraisal the claim is filed on |
| DF-DOC-001 to DF-DOC-011 | `document` (P5) | id, case_id, person_key, document_type, source, storage_ref and 5 more | Not read or written as a table: the claim's document set is rwb-document's and is referenced by identifier |
| DF-WRK-027 to DF-WRK-036 | `timer` (P3) | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | Not read or written: the claim clock and the 10 working days of R-LIT-79 are rwb-case's |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_guarantee`) | decision code, rule id, rule version, inputs reference, claim, collateral key, appraisal number, decided at, decider role | Write, one record per filing, before the claim moves |
| No Field ID published | the collateral-event fact of the case (rwb-deviation, S8) | deviation_code, raised_at, raised_by, paused_state, handler_user_id, contact_stop, cleared_at of FSD S8 A2.16.3.2 | Not read or written: X7 is rwb-deviation's, and this story takes no deviation row |

Field IDs are those of the Logical Data Model and Data Dictionary v8, of TSD S3 T3.1 and of the legacy Data table of the key, with the owners changed by the target. **No new table and no new column**: `guarantee_claim` already sits in `rwb_guarantee` with its eight fields, the claim type is a member of the list in force, and the decision record and the idempotency key are library objects created in the schema by the library's migration (DP-03, DP-15). The collateral, the appraisal and the deadline have no field identifier in this service's schema and are carried as elements of the claim answer and of the record (GAP-2736; ASM-4543; ASM-4545).

**No personal data.** The rows this story reads and writes carry identifiers, codes, amounts, dates and versions. No name, address, contact value or identity number enters `rwb_guarantee`, the decision record, a log or a workflow input; the officer is a role on the record and the parties are identifiers on the case and on the collateral.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-guarantee (S3); base `/api/recovery/guarantee/v1` (DP-13). This story supplies the collateral-event branch of the two operations the legacy Endpoints table names, and their shape is baselined by RWB-S3-E4020-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/guarantee-claims` | `GuaranteeClaimRequest` with `caseId` from the path, `claimType` = `COLLATERAL_INSURANCE`, `claimDeadline`, `claimedAmount` and the collateral-element fields; 201 with `GuaranteeClaim` (API-S3-001) | Treatment and offer, right C, scope applied | `Idempotency-Key` required; a repeated key returns the first answer |
| PATCH | `/guarantee-claims/{claimId}` | `GuaranteeClaimUpdate` with `status` = `FILED` and `filedAt` after the officer records the filing; 200 with `GuaranteeClaim` (API-S3-002) | Treatment and offer, right U, scope applied | Not applicable in TSD S3 T-A.2; a stale `version` is refused with 409 |

The errors are 400 for a malformed request, 401 for an unauthenticated call, 403 with MSG-P4-002 for a role without the right, 404 for an unknown or out-of-scope claim or case, 409 for a stale `version` or a claim already in `FILED`, 422 with MSG-GEN-001 for an invalid element, and 503 when the decision library does not answer. The element set of the collateral event — the collateral key, the appraised value and the appraisal number — has no published field identifier and is the baseline's (GAP-2736; ASM-4549).

#### 12.2 REST operations consumed

| Operation | Owner | Use |
|---|---|---|
| The collateral and appraisal read (operation name Not specified in the source documents (GAP-2736; ASM-4545)) | P1 rwb-source-data | The collateral of the case, its type and value, and its last appraisal with the number, the value and the date; used by `readCollateralFacts` and by the claimed amount |

One consumed operation, one hop, 2 s timeout (DP-11). DP-05 adds no dependency, so the plan's class C row is empty and the client is built against the documented use and a fake; the operation, its request and answer and its error set are the owner's and are recorded once (GAP-2736). No other REST call is made: the re-appraisal is not a call of this service, rwb-valuation is reached through the case, and no insurer, SVAF or TCG interface exists to call (BR6, BR8).

#### 12.3 Events published

None. The ownership rows give rwb-guarantee no event type, so this story adds no name, no outbox row and no payload to `rwb.guarantee.events.v1`, and a build that publishes one here fails the absence test (BR9). The one publication of the step is the decision record, which the library of DP-03 sends to `rwb.decision-record.v1` in the transaction of the claim write.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` (EV-30 RulePackageInForce) | The rwb-decision topic, with `.retry` and `.dlt`; its topic name is not published for this key (GAP-2736) | P7 rwb-decision | The package code, the package version, the version id, the valid-from date and the approver role; the version the record carries and the version the claim rules are evaluated against |
| The X7 collateral event, when the case router signals it (event name Not specified in the source documents (GAP-2736; ASM-4547)) | Through rwb-case, not directly | P3 rwb-case | The fact that a collateral event is open on the case; it starts or signals the branch and is never a subscription of this service |

One subscription with the inbox of the platform event library: the package event is stored once by its key, and the workflow reads the version in force. Slide 13 gives S3 event subscriptions from P6 and P8 and none from another service, so this story declares one subscription to the rule package and takes the collateral event from the case signal rather than from a topic.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `GuaranteeClaimWorkflow` | Workflow, one child execution per case per guarantee stage, child of `CaseWorkflow`, continues-as-new | `rwb-guarantee` in namespace `rwb-recovery` | Input: the case, the claim, the rule version in force; signal: the collateral event of the case; reports the stage outcome and the re-appraisal request to the parent |
| `readCollateralFacts` | Activity, this story | `rwb-guarantee` | The case and the collateral key in; the collateral, its type and value, the last appraisal and the claimed amount out |
| `evaluateClaimRules` | Activity, this story | `rwb-guarantee` | The collateral fact, the claim type and the package version in; the rule rows that fired, their versions, the required documents and the approval flag out |
| `recordAndApply` | Activity, this story | `rwb-guarantee` | The claim create and the filing in; the claim row, the decision record and the outbox row out, in one transaction |
| `reportCollateralEvent` | Activity, this story | `rwb-guarantee` | The stage outcome and the re-appraisal request in; the parent signal accept out, with no case row written |

`GuaranteeClaimWorkflow` is the one workflow the ownership rows give S3, and these four activities are this branch's; the preparation, submission, tracking and subrogation activities are the sibling stories'. The activity names are a target design choice, fixed by the baseline so that the workflow history is stable.

#### 12.6 Schedules

None. The branch runs from a case signal inside the workflow and owns no Temporal Schedule and no legacy Quartz job, because the ownership rows give S3 no job. The 10 working days of R-LIT-79 and the claim clock are the workflow timers of rwb-case and rwb-valuation, not a Schedule of this story (BR7).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `guarantee_claim` | S3 | The one table of this service: insert the collateral-insurance row and update `filed_at`, `status`, `version`, `updated_at` and `updated_by` |
| `decision_record` | PLT library, created in `rwb_guarantee` | The local hash-linked decision record of DP-03, one per filing |
| `idempotency_key` | PLT library, created in `rwb_guarantee` | The key of the repeated create and the answer it holds |

Not owned and never read as a table: `recovery_case`, `case_party`, `assignment`, `task` and `timer` (P3), `deviation` (S8), `decision_log_entry` and `rule_row` (P7), `document` (P5), `valuation_ext` (S1) and every `v_ace_*` view (P1). No foreign key leaves `rwb_guarantee`: the case, the collateral and the appraisal are identifiers and values, not keys across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data collateral read fake | The collateral of case `RC-2027-000420` with its type and value, its last appraisal with number, value and date, a case with no appraisal, a stale answer and an unavailable service | AC1, X4, TC-S3-E4020-APP-01 |
| rwb-case case-signal fake | A case signal accepted with the filed claim and the re-appraisal request; a rejected signal; a case in `DEVIATION_HOLD` | AC1, X6, TC-S3-E4020-APP-02 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC2, X1 |
| rwb-decision package fake | A package in force with its version, and no package | AC1, TC-E4-020-01 |
| gateway-bff composite route fake | The merged SCR-17 answer for the claim, the collateral, the appraisal and the result, read once | TC-E4-020-01 |
| rwb-guarantee claim-resource fake (`RWB-S3-E4020-CON`) | A create in `PREPARING`, a filing in `FILED`, a repeated key, a stale `version` and a claim already filed | TC-E4-020-01, TC-S3-E4020-APP-02 |

The fakes are test-only and are replaced by the real services in SIT. The collateral operation and the case-signal element set are not published, so their fakes are built from the documents and carry the placeholder until the owners confirm them (GAP-2736; ASM-4544; ASM-4545).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 consumed | `POST /cases/{caseId}/guarantee-claims` and `PATCH /guarantee-claims/{claimId}` on `/api/recovery/guarantee/v1`; one read of rwb-source-data's contract; the screen reaches the service through gateway-bff (DP-19) |
| Kafka | 0 published, 1 consumed | `rwb.decision.RulePackageInForce.v1`; no event of this service; the decision record reaches `rwb.decision-record.v1` through the library of DP-03 |
| Temporal | 1 workflow and 4 activities | `GuaranteeClaimWorkflow`, `readCollateralFacts`, `evaluateClaimRules`, `recordAndApply` and `reportCollateralEvent` on `rwb-guarantee`, as a child of `CaseWorkflow`; no Schedule |
| File | None of this service | The claim writes no file; the insurer and SVAF are not called, and the appraisal order is rwb-valuation's (BR6, BR8) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.guarantee`, module `collateralevent`, Java package `th.co.scb.ace.workbench.recovery.guarantee.collateralevent`; front end `src/modules/recovery/guarantee/CollateralInsuranceClaim.tsx`, the fragment SCR-17 embeds.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the filing: the claim row and the record commit together or not at all. DP-05 is applied through the owner's contract rather than a grant: the three legacy views are read through rwb-source-data and `rwb_guarantee` holds no `v_ace_*` grant, so the alternative of the service's own views is not taken and no dependency is added. DP-13 moves the base of the two operations and keeps the monolith path out of the build. DP-19 is how SCR-17 reaches this service, one hop through the gateway. No other DP applies: no rule package is embedded here beyond the package in force (no DP-04 row), no event is published (no DP-09), no job runs (no DP-10) and no file crosses the act.

**Dependencies the tables add and the plan does not hold.** The collateral read is class C in kind and the plan's C row is empty, so the client is built against the documented use and a fake on Day 1 and the absence is recorded as GAP-2736 (ASM-4545). The re-appraisal is a case signal and not a call, so it adds no dependency at all (ASM-4544). The three H rows of the metadata are the contract of this key and the two platform contracts of DP-03 and DP-19; no other H row is added, so the lane stays at depth two.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `GuaranteeClaimWorkflow` collateral-event branch | Workflow | Waits for the collateral event, reads the facts, evaluates the rules, records the filing and reports the event with the re-appraisal request |
| `readCollateralFacts` | Activity | Reads the collateral and the last appraisal through the owner's contract and returns them with the claimed amount |
| `evaluateClaimRules` | Activity | Applies VR-S3-008-1, BR-S3-008 and the package in force, and returns the rule rows, their versions, the document set and the approval flag |
| `recordAndApply` | Activity | Inserts the claim row and updates the filing in one transaction with the record and the outbox row |
| `reportCollateralEvent` | Activity | Reports the stage outcome and the re-appraisal request to the parent `CaseWorkflow` |
| `CollateralReadClient` | Client | One hop to rwb-source-data with the 2 s timeout, the retry and the problem mapping |
| `PackageInForceConsumer` | Consumer | The inbox subscription on the rule-package event, keyed by the package and version |
| `GuaranteeClaimRepository` | Repository | Reads and writes `guarantee_claim` only, with the optimistic `version` |
| `ClaimRecordWriter` | Library adapter | Writes one record per filing, hash-linked, and refuses the step when the write fails (DP-03) |
| `CollateralClaimController` | Controller | The collateral-event slice of the two operations, its rights, its `version` check and the problem mapping |
| `CollateralInsuranceClaim` | React component | Shows the claim, its deadline, the collateral, the appraisal and the result on SCR-17, read only |

**Database and migrations.** No Flyway file. `rwb_guarantee` and its login arrive with the DB story of this service, `guarantee_claim` is already the service's table, and the decision record and the idempotency key are library objects created in the schema by the library's migration (DP-03, DP-15). No column is added for the collateral event, the collateral key or the appraisal: they are elements of the answer and of the record until the data owner names the fields (GAP-2736; ASM-4549).

**Configuration and reference data.**

- `LOV-CLAIM-TYPE` and `LOV-CLAIM-STATUS` with their identifiers, never enumerated in code (BR2).
- The claim deadline basis, the claimed-amount basis and the document set, as rows in force with their version (GAP-2736).
- The rule package in force and its version, read through the package event (R-UNI-38).
- The capability area Treatment and offer and its rights C and U, as access rows read through the guard.
- No insurer, SVAF or TCG endpoint, credential or file window: no interface is published (BR8).

**Build steps**

1. The collateral-event branch of `GuaranteeClaimWorkflow` and its input record, registered on `rwb-guarantee` as a child of the case workflow (AC1).
2. `CollateralReadClient` against the read fake, with the no-appraisal, the stale and the unavailable paths (X4).
3. `PackageInForceConsumer` and the version in force the record carries (AC1).
4. `readCollateralFacts` with the collateral, the appraisal and the claimed amount (AC1).
5. `evaluateClaimRules` with VR-S3-008-1, BR-S3-008 and the missing-rule path (X8).
6. `GuaranteeClaimRepository` and the optimistic `version`, with the stale-version and repeated-key refusals (X5).
7. `recordAndApply` and the record with the rule id and version, the claim, the collateral key and the appraisal number (AC1).
8. `ClaimRecordWriter` against the library stub, with the failed-write path (AC2, X1).
9. `reportCollateralEvent` and the case signal, with the rejected-signal and the open-deviation paths (AC1, X6).
10. `CollateralClaimController` with the rights, the `version` check and the problem mapping (TC-E4-020-03).
11. `CollateralInsuranceClaim` and SCR-17 through the composite route fake, and the boundary test: no statement outside `rwb_guarantee`, no `v_ace_*` read, no write to a foreign schema, no outbox row of a claim event (X7, BR5, BR9).

**Feature flag.** `rwb.guarantee.collateral-event-claim-v1`, read as a flag of the platform library; off means the collateral event reaches the case with no claim created, the stage raises a task and no claim deadline is set.

**Done when.** The tests of section 16 pass, a collateral event files exactly one claim and one record in SIT, a repeated key and a repeated signal file nothing twice, a stale version is refused, a forced record failure changes nothing and shows MSG-P7-003, the re-appraisal request reaches the case, no case or deviation row and no `v_ace_*` read exists in the build, and SCR-17 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required element of the claim, of the collateral fact or of the appraisal is absent or invalid (X3) | Enter {field}. |
| MSG-P4-002 | A role without right C or U of Treatment and offer calls the operation (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the filing is applied (X1, AC2) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The three message IDs and their text are the rows of the legacy Validation and messages table of this key, copied unchanged. FSD S3 A2.8.3.1 adds VR-S3-008-1 with MSG-GEN-001 in the same words. No message is reworded, no new one is added, and no message carries a deadline, an amount or an insurer reference. The 403 carries MSG-P4-002 and the 409 of a stale version or an already filed claim has no business text in any source (GAP-2736). Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-17 Guarantee claim is served through the gateway-bff composite route (DP-19), and this story fixes the collateral-insurance part of its answer and the states it can show.

| Screen | States | What this story sets |
|---|---|---|
| SCR-17 Guarantee claim | Not due; due; submitted; paid; refused | Loading while the claim, the collateral and the appraisal are read; due with the deadline, the appraised value and the document set; submitted with the filing date, the claim status `FILED` and the re-appraisal requested; held with the missing collateral fact or appraisal named; not recorded with MSG-P7-003; refused with MSG-P4-002 |

The legacy screen row of this key lists the five states and no state for a collateral event, so the event is shown inside the due and submitted states and SCR-17 needs no sixth state (GAP-2736). "Not due" and "paid" belong to the preparation and the payment stories of this service, and "refused" to the rejection path of FEAT-GUA-03. The screen's field list, its merge order and its other elements belong to RWB-PLT-N001-CON and to the sibling stories; the collateral, appraisal and filing elements are this story's and the baseline's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-020-01 | AC1: a collateral event files the claim and triggers re-appraisal; the result and the rule version are written | Component | Case `RC-2027-000420` with collateral `COL-2027-000420` and appraisal `APR-2027-0042`, a claim type of `COLLATERAL_INSURANCE`, a deadline and a claimed amount, and an accepted case signal |
| TC-E4-020-02 | AC2: the decision log cannot be written | Component | The decision-record stub stopped; the claim stays in `PREPARING`, nothing filed and MSG-P7-003 shown |
| TC-E4-020-03 | Access: a role without the right is refused with MSG-P4-002 | Component | A role without C of Treatment and offer on the create and without U on the filing, and an out-of-scope case; 403 before any read |
| TC-E4-020-04 | Principle 5: a forced decision log write failure stops the action | NFR | A forced failure at the moment of the claim write; no filing, no record and no case signal |
| TC-S3-E4020-APP-01 | The read edge: the collateral with no appraisal, a stale answer, an unavailable owner's contract, a missing element and the boundary scan | Component | A case with no appraisal, a stale read, a 503 from the owner, a claim with no deadline and the build scan of step 11 |
| TC-S3-E4020-APP-02 | The write edge: the repeated key, the repeated signal, the stale `version`, the claim already filed and the rejected case signal | Component | The same `Idempotency-Key` twice, the same case signal twice, a claim whose `version` has moved, a claim in `FILED` and a rejected parent signal |

The four legacy case IDs are the legacy cases of RWB-E4-020 in their legacy order, with the Level column added: TC-E4-020-01 and -02 cover the two criteria, -03 the access path and -04 the principle-5 failure. They are Component because the branch is tested on its fakes; the legacy wording of each case is kept in the Test Cases workbook, tab Story test cases. The two `TC-S3-E4020-APP-` cases are new and cover the parts no legacy case touches. The `-ITG` copies belong to the wave 3 harness, which owns the cross-service journey of this key; the X7 journey end to end is FEAT-DVF-07's.

### 17. Guardrails

- No business value in code: the deadline basis, the claimed-amount basis, the document set, the claim lists and the rule version stay rows read with their version, never a constant, a default or a branch of the build.
- No personal data in `rwb_guarantee`, in a workflow input, in an answer or in a log: identifiers, codes, amounts, dates and versions only, and the record names the officer's role and never the officer.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and the legacy reads of `v_ace_collateral`, `v_ace_collateral_detail` and `v_ace_valuation` are retired rather than moved (DP-05).
- The case, the deviation and the appraisal stay with their owners: no `recovery_case`, `assignment`, `task`, `timer` or `deviation` row is written, and no appraisal is ordered (BR6, BR7).
- A person approves an insurance claim: the branch never files from an agent or a rule alone (R-DEV-06).
- The claim is recorded before it moves and the fact is consumed once: a build that files a claim before its record, or twice for one event, fails the review (DP-03, BR3, BR4).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no monolith base `/api/recovery/v1`, no shared job table, no Quartz row, no direct ACE view read and no claim event published by this step.

### 18. Traceability

| Source | Reference | Used in |
|---|---|---|
| Legacy story | RWB-E4-020, disposition Split (rework); AC1 and AC2 owned word for word by this story; endpoints, screen, permissions, messages and the four cases | 1, 7, 10, 14, 15, 16 |
| Feature | FEAT-GUA-08 File an insurance claim on a collateral event, module S3, epic E4, kind user, primary role case owner, systems Workbench and SVAF, depends on FEAT-VAL-01 | 1, 2, 3 |
| Related features | FEAT-DVF-07 Run X7 collateral event end to end (S8, E7, prerequisite FEAT-GUA-08); FEAT-VAL-01 Order an appraisal when the last one is stale (S1) | 2, 4, 19 |
| FSD S3 v3 | A1.4 preconditions; A2.8.2 steps and integration points; A2.8.3.1 VR-S3-008-1 and BR-S3-008; A2.8.3.2 field catalog; A2.8.3.3 roles; A2.8.4.3 exception flows; REQ-S3-002 and REQ-S3-007; SCR-17 | 2, 3, 4, 8, 11, 14, 15 |
| FSD S8 v3 | A2.16.1 to A2.16.3.3 for the X7 collateral event, its field catalog and its roles | 2, 9 |
| TSD S3 v2 | T2 components; T3.0 standard columns; T3.1 `guarantee_claim`; T3.2 `LOV-CLAIM-TYPE` and `LOV-CLAIM-STATUS`; T3.3 relationships; T5.1 INT-29; T5.3 no event; T6.1 rights; T-A.1 and T-A.2 for API-S3-001 and API-S3-002 | 3, 9, 10, 11, 12 |
| Business Rules and Routing Logic v4 | R-DEV-06, R-DEV-09 and R-LIT-79 | 2, 8, 9 |
| Requirements | REQ-S3-002 and REQ-S3-007 of Business Requirements Program v4, section 5.10 | 2, 18 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S3-E4020-CON | Contract | H consumer: publishes the collateral-event elements, the required set, the rights, the error set and the fakes this story builds against |
| RWB-S3-E4013-APP, RWB-S3-E4014-APP | App development | Siblings: preparation and submission of the TCG claim; the same workflow and the same table, different branch |
| RWB-S3-E4015-APP, RWB-S3-E4016-APP | App development | Siblings: tracking to payment and the subrogation position; they read the claim this story creates |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library the filing writes through |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route SCR-17 uses |
| P1 rwb-source-data | Service | C in kind, no row: the collateral and appraisal read |
| P3 rwb-case | Service | The case of record, the parent workflow and the case signal |
| S1 rwb-valuation, S8 rwb-deviation | Services | The appraisal order of FEAT-VAL-01 and the X7 deviation of FEAT-DVF-07 |
| RWB-ITG-W3 | Integration | The end-to-end proof against the live owners, held by the wave 3 harness |

### 19. Out of scope

- The contract artefact — the document, the schemas, the DDL template, the error set, the versioning rule and the fakes: RWB-S3-E4020-CON.
- The X7 deviation end to end — the flag, the pause, the states and the return: rwb-deviation and FEAT-DVF-07.
- The appraisal itself — the order to SVAF, the value, the outlier flag and the acceptance: rwb-valuation and FEAT-VAL-01 to FEAT-VAL-04.
- The case, its states, the stage clock and the parent workflow: rwb-case (P3).
- The documents of the claim and their retention: rwb-document (P5).
- The central decision ledger, the `GUA` rule rows and their approval: rwb-decision (P7); the local record contract: RWB-PLT-E1027-CON.
- The roles, the rights and the scope data: rwb-access (P4).
- The gateway-bff composite route, the SCR-17 field list and the layout: RWB-PLT-N001-CON and the screen owner (DP-19).
- Any interface to an insurer, to SVAF or to the TCG for this claim: no source publishes one, and INT-29 is TCG only and not available today (GAP-2736).
- The tracking, the rejection, the payment and the subrogation position of this claim: FEAT-GUA-03, FEAT-GUA-04 and FEAT-GUA-07.
- The deployment of this build: the chart values, the schema and login, the topic and the flag.
- The real cross-service proof against the live owners: the wave 3 integration harness.
