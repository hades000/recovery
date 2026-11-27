# RWB-P2-E2006-APP Credit approval pack for NLEADS

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P2-E2006-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP11, DP15, DP19 |
| Parallel lane | L-P2-A |
| Ready to start | After RWB-P2-E1007-APP |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P2-E1007-APP |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P3-E2004-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (no FR mapped to REQ-CHO-008, REQ-CHO-006, REQ-RDF-009) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-006 for rwb-integration. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P2-E2006-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the credit approval pack for an approved restructure plan assembled on the integration base from the case, the plan terms, the account, collateral and valuation facts, the NLEADS decision, the checklist documents and the required approval level, all read through their owners' contracts, and the NLEADS reference and result accepted through the same base**, so that **a plan reaches credit without the case facts being re-keyed, and the result is recorded and sent on to the case and the treatment by the services that own them**.

The legacy story put the pack, the result, the decision log entry, the four NLEADS columns on the treatment and the case move on two P2 Integration endpoints. Under D-RCV-60 the work is split by owner. The case-side pack facts, the route state, the queue move and the case-side decision record are rwb-case's, carried by RWB-P3-E2006-APP. The four treatment columns `nleads_ref`, `credit_result`, `credit_result_reason` and `credit_result_at` and the treatment state are rwb-treatment's, carried by the S2 story of this legacy key. The delegation of authority table is rwb-access's, and the approval routing and the approval workflow are the P4 and P7 stories. The accessibility of the pack and the NLEADS submission step is what stays with rwb-integration: the two treatment-scoped operations of the integration base that the Ownership Map keeps with P2, `GET /treatments/{treatmentId}/credit-pack` and `POST /treatments/{treatmentId}/credit-result`.

### 2. Business rationale

A restructure outside the approved range goes to credit approval (R-RES-10), which the bank decides in NLEADS. NLEADS has no interface to the Workbench (INT-26), and ACE ingests the NLEADS decision overnight: only rwb-source-data reads the thirty read-only ACE views, and every other service reads ACE facts through its contract (DP-05, ADR-010). Officers therefore still re-key the case facts and the plan terms into NLEADS today, and the credit result never reaches the case record. This story answers the integration half of that problem: one credit approval pack assembled field by field from the services that own the facts, and one result operation that accepts what NLEADS returned, records it, and hands it to the case and the treatment. It meets REQ-CHO-008 and REQ-CHO-006 and applies REQ-RDF-009, because every input of the pack carries its age and every accepted result records the freshness of the data it used.

**What the split changes, and why it changes here.**

- **DP-01.** `rwb_integration` holds no copy of a case, a treatment, an account or a document, and no foreign key into another schema. The pack is composed at request time from contracts, so nothing is cached and nothing goes stale in a table.
- **DP-03.** The `DecisionLogWriter` of the monolith becomes the local decision-record library: one record with decision "D5", the final call, the NLEADS reference in the actions, the approval level and the freshness of the data used, written in `rwb_integration` in the same local transaction as the acceptance, and published as `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` for the central ledger in rwb-decision. A decision that cannot be recorded does not proceed (R-UNI-39; CTL-06).
- **DP-05.** `AceSourceQuery` and the `v_ace_*` reads disappear from this slice. The accounts, the collateral, the latest appraisal, the ACE business date and the NLEADS decision behind `v_ace_credit_decision` are read through the rwb-source-data contract; this service reads no view at all.
- **DP-07.** The NLEADS pack checklist is reference data of rwb-case. This story reads the checklist rows through the rwb-case reference-data contract with the version in force, so no document type is written in code.
- **DP-11.** The in-process calls to `DelegationQuery`, `CaseEvents`, `TreatmentQuery`, `TreatmentCommands` and `CaseDocuments` become REST contracts with fakes, one hop, and a 2 s timeout each.
- **DP-15.** One Flyway sequence in `rwb_integration` for the library tables this story uses; no new business table.
- **DP-19.** The pack and the result are reached from SCR-14 through the gateway-bff composite route of RWB-PLT-N001-CON, never by the browser calling the service directly.

The two operations are the legacy contract shape, kept for the integration base: the CreditPack field set and the CreditResult request that the P2 contract published. The case-side story serves SCR-14 from the case record and carries the route state and the queue; this story keeps the frozen integration-base shape for the NLEADS submission step and the legacy consumers of the pack, and both compose the shared values from the same four contracts, so the two answers agree on those fields. That the same pack is now composed twice, once case-side and once integration-side, is recorded as a gap and an assumption, not hidden.

### 3. Preconditions

- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03). The library writes the record and publishes `rwb.decision-record.DecisionRecorded.v1` on the service's behalf.
- RWB-PLT-E1043-CON and RWB-P3-E1043-CON are published: the reference-data contract of rwb-case, which carries the NLEADS pack checklist rows with the version in force (DP-07).
- RWB-PLT-E1044-CON is published: the per-service Flyway sequence and the migration conventions of `rwb_integration` (DP-15).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-14 and declares the two integration-base operations (DP-19).
- RWB-P2-E1007-APP is delivered: the integration base, its controller conventions, its problem-response mapping, its contract-client and idempotency handling.
- RWB-P3-E2004-CON is published: the treatment contract story of the case fold, which fixes the plan-terms read and the credit-result record that this story calls. Its published form and the S2 treatment build are the two sides of the same contract.
- The case is in route state AWAITING_CREDIT_APPROVAL with an open RESTRUCTURE treatment, and its ACE plan status is APPROVED (RWB-E2-002).
- The NLEADS pack checklist is loaded as reference data of rwb-case (DL19; the items the legacy story assumes are CREDIT_APPLICATION, ID_COPY, TITLE_DEED, LATEST_APPRAISAL and INCOME_PROOF), with the version in force.
- The delegation rows for item 2.1.1 are loaded in rwb-access (DL18) and are read through its `GET /doa-limits` contract, never from a table of this service.
- The input age limit for balances in a credit pack is 1 business day (assumed in the legacy story under DL22), read as a reference row.
- The person holds RW-RESTRUCT or RW-CASEOWN with the case in scope.
- The feature switch `rwb.integration.nleads-pack` is the legacy reference for the switch; the switch itself is a feature flag of the platform flag library.
- The login is the rwb-integration login (DP-02): Not specified in the source documents (GAP-0663; ASM-1099).

### 4. Flow

1. Restructuring officer: opens SCR-14 Treatment record through gateway-bff and selects the credit approval pack.
2. gateway-bff: calls the composite route, which reads the case-side pack on rwb-case and the integration-base pack on `GET /api/recovery/integration/v1/treatments/{treatmentId}/credit-pack`, one hop each, and merges the answers into the screen model (DP-19).
3. rwb-integration: checks the Treatment and offer right through the rwb-access authorise contract, cached per session, and the case scope; a refusal ends the request before any read.
4. rwb-integration: reads the treatment through the rwb-treatment contract: the case reference, the treatment type, the state, the offer amount, the haircut amount, the installments and the valid-until date.
5. rwb-integration: reads the case through the rwb-case contract: the case number, the product group, the route state and the linked accounts, by business key only.
6. rwb-integration: reads each linked account and each collateral, with the latest appraisal and the ACE business date behind each input, through the rwb-source-data contract (DP-05).
7. rwb-integration: reads the NLEADS decision behind the treatment's plan through the rwb-source-data contract over `v_ace_credit_decision`; the view is never read here.
8. rwb-integration: reads the NLEADS pack checklist rows through the rwb-case reference-data contract with the version in force, and the documents on the case through the rwb-document contract; each checklist row becomes present with its link, or missing.
9. rwb-integration: reads the required approval level for decision D5, the product group and the amount under item 2.1.1 through the rwb-access delegation contract, with the delegation version in force.
10. rwb-integration: attaches the age of every input against its limit, and its message; an input past its limit is returned with its age and MSG-P7-006 (REQ-RDF-009).
11. rwb-integration: returns CreditPack: case number, product group, the accounts with balances as of the ACE business date, the collateral with its latest appraisal, the plan terms, the required level, the checklist documents with a link or as missing, and the messages. No field needs to be typed by the officer.
12. Restructuring officer: submits the plan in NLEADS, receives the reference, and later the result.
13. Restructuring officer: records the NLEADS reference, the result, the approval level, the result date and, for a refusal, the reason through `POST /api/recovery/integration/v1/treatments/{treatmentId}/credit-result`, under `Idempotency-Key` and `If-Match`.
14. rwb-integration: validates the reference shape, the result value, the approval level against the level the delegation contract returns, the result date, the reason when the result is REFUSED, the case state through the rwb-case contract, that no result is recorded yet through the rwb-treatment contract, and the treatment version. A failure returns its problem and nothing changes.
15. rwb-integration: writes the decision record with decision "D5", the final call, the NLEADS reference in the actions, the approval level, the delegation version and the freshness of the data used, in the same local transaction as the acceptance of the result and the outbox row; the library publishes DecisionRecorded on `rwb.decision-record.v1`. A failed record write rolls back the acceptance and blocks the action (MSG-P7-003).
16. rwb-integration: records the reference, the result, the reason, the approval level and the result date through the rwb-treatment contract; rwb-treatment writes its four columns and moves the treatment state to APPROVED or REFUSED.
17. rwb-integration: raises CREDIT_APPROVED or CREDIT_DECLINED to the rwb-case contract, and rwb-case moves the route state by R-RES-11 or R-RES-12 and R-RES-14 with its own decision record and its queue move.
18. rwb-integration: answers 200 with the treatment as rwb-treatment returns it, and stores the response against the `Idempotency-Key`. A repeat with the same key replays the stored answer and writes no second record; a different key on a treatment that already holds a result returns 409 with MSG-P2-010.
19. If a remote call fails after the record is committed, the answer is 502 or 503 with MSG-GEN-006, the committed record keeps the accepted result and the pending action, and the same `Idempotency-Key` resumes the two remote steps so the officer never writes a second record.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A checklist document is not on the case | The pack shows the item as missing and the other items as present | MSG-P2-009 | AC4; the case-side pack shows it too |
| X2 | A balance in the pack is older than its age limit | The pack shows the input age in days | MSG-P7-006 | AC5 |
| X3 | Reference empty, or a refusal without a reason | Refused; nothing changes | MSG-GEN-001 | AC6 |
| X4 | Result date after today | Refused; nothing changes | MSG-GEN-002 | AC6 |
| X5 | The NLEADS approval level is below the level the plan needs | Refused; nothing changes | MSG-P2-018 | AC7 |
| X6 | A result is already recorded on the treatment | Refused; no second decision record | MSG-P2-010 | AC8 |
| X7 | The case is not in AWAITING_CREDIT_APPROVAL or the treatment is not a restructure | Refused; nothing changes | MSG-P3-005 | AC9 |
| X8 | The treatment changed between read and write | Refused; nothing changes | MSG-GEN-004 | AC10 |
| X9 | The decision record cannot be written | Nothing changes and no remote call is made; an incident is raised | MSG-P7-003 | AC11 |
| X10 | A role without the Treatment and offer right opens the pack or records a result | Refused before any read or write; nothing changes | MSG-P4-002 | TC-E2-006-12 |
| X11 | rwb-source-data, rwb-treatment, rwb-document, rwb-access or rwb-case does not answer inside the REST budget | One hop, 2 s timeout; a pack section returns the source message for that section, and a result is refused with nothing written | MSG-GEN-006 | AC1, AC11 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published contracts: the decision-record library, the reference-data contract, the migration conventions, the edge route and the integration base. The source-data, treatment, document, case and access answers come from their contract fakes |
| Negotiable | The checklist rows, the age limit and the delegation levels are data values in their owners' tables; the story fixes only the behaviour |
| Valuable | Removes the re-keying into NLEADS and puts the credit result on the case and the treatment through the services that own them |
| Estimable | Two operations, one query path, one validated result path, one library integration, one contract-fake run |
| Small | Fits two weeks with its tests |
| Testable | Each owned criterion has a test case in section 16; every cross-service answer is stubbed |

### 7. Acceptance criteria

```gherkin
Feature: Credit approval pack for NLEADS

  Background:
    Given case "RW-2026-000610" is in route state "AWAITING_CREDIT_APPROVAL"
    Given treatment "TRT-SYN-0610" of type "RESTRUCTURE" has offer amount 2,400,000.00 baht, haircut 0.00 baht and 84 installments
    Given the ACE plan status of the case is "APPROVED"
    Given the plan needs approval at level "L6" or higher under item 2.1.1

  Scenario: AC1 Pack prepared (legacy RWB-E2-006 AC1)
    Given an approved restructure plan on treatment "TRT-SYN-0610"
    Given the rwb-treatment contract mock returns treatment "TRT-SYN-0610" with reference "NL-SYN-000610" and state "APPROVED"
    Given the rwb-source-data contract mock returns 2 accounts with balances as of 2026-12-14 and 1 collateral with its latest appraisal
    Given the rwb-case contract mock returns case "RW-2026-000610" with product group "MORTGAGE" and route state "AWAITING_CREDIT_APPROVAL"
    Given the rwb-case reference-data contract mock returns the 5 checklist rows in force
    Given the rwb-access contract mock returns required approval level "L6" for item 2.1.1
    Given the rwb-document contract mock returns a link for each of the 5 checklist documents
    When the officer opens the credit approval pack on 2026-12-15
    Then the pack holds case number "RW-2026-000610", product group "MORTGAGE", 2 accounts with balances as of 2026-12-14 and 1 collateral with its latest appraisal
    Then the pack holds the plan terms: offer amount 2,400,000.00 baht, haircut 0.00 baht, 84 installments, valid until 2026-12-29
    Then the pack lists the 5 checklist documents with a link to each one on the case
    Then the system shows the required approval level "L6"
    Then no field in the pack needs to be typed by the officer

  Scenario: AC2 Result recorded (legacy RWB-E2-006 AC2)
    Given the officer has submitted the pack in NLEADS
    Given the rwb-source-data contract mock returns NLEADS reference "NL-SYN-000610", result "APPROVED", approval level "L5" and result date 2026-12-17
    Given the rwb-treatment contract mock returns treatment "TRT-SYN-0610" with reference "NL-SYN-000610" and state "APPROVED"
    Given the rwb-case contract mock returns route state "OFFER_WITH_CUSTOMER" for case "RW-2026-000610"
    When the officer records NLEADS reference "NL-SYN-000610", result "APPROVED", approval level "L5" and result date 2026-12-17
    Then the treatment carries the reference "NL-SYN-000610" and its state is "APPROVED"
    Then a decision log entry with decision "D5" and final call "approved" holds the NLEADS reference
    Then the route state moves to "OFFER_WITH_CUSTOMER" by R-RES-11

  Scenario: AC3 Refused (legacy RWB-E2-006 AC3)
    Given NLEADS refuses the plan with reason "Income does not cover 84 installments"
    Given the rwb-source-data contract mock returns NLEADS reference "NL-SYN-000611", result "REFUSED" and reason "Income does not cover 84 installments"
    Given the rwb-treatment contract mock returns treatment "TRT-SYN-0610" with reference "NL-SYN-000611", state "REFUSED" and the reason
    Given the rwb-case contract mock returns route state "DECLINED_BY_CREDIT" and then "BACK_TO_ROUTE_DECISION" for case "RW-2026-000610"
    When the officer records reference "NL-SYN-000611", result "REFUSED" and the reason
    Then the treatment state is "REFUSED" and the treatment shows the reason
    Then the route state moves to "DECLINED_BY_CREDIT" by R-RES-12 and then to "BACK_TO_ROUTE_DECISION" by R-RES-14
    Then the case is in the case owner's queue

  Scenario: AC4 Missing checklist document (legacy RWB-E2-006 AC4)
    Given the case holds no document of type "INCOME_PROOF"
    Given the rwb-document contract mock returns 4 of the 5 checklist documents and no "INCOME_PROOF"
    When the officer opens the pack
    Then the pack shows "INCOME_PROOF" as missing with message MSG-P2-009
    Then the other 4 documents show as present

  Scenario: AC5 Stale balance (legacy RWB-E2-006 AC5)
    Given the last account load for the case is for business date 2026-12-12 and today is 2026-12-15
    Given the rwb-source-data contract mock returns balances as of 2026-12-12 and business date 2026-12-15 on the freshness read
    When the officer opens the pack
    Then each balance shows message MSG-P7-006 with 3 days

  Scenario: AC6 Invalid input (legacy RWB-E2-006 AC6)
    When the officer records result "REFUSED" with reference "NL-SYN-000612" and an empty reason
    Then the response is 422 with message MSG-GEN-001 for field "reason"
    Then a result with result date 2026-12-31 on 2026-12-17 returns 422 with message MSG-GEN-002
    Then the treatment does not change

  Scenario: AC7 Approval level below the required level (legacy RWB-E2-006 AC7)
    Given the rwb-access contract mock returns the required approval level the plan carries under item 2.1.1
    When the officer records result "APPROVED" with approval level "L6" for a plan that needs level "L5"
    Then the response is 409 with message MSG-P2-018
    Then the treatment does not change

  Scenario: AC8 Result recorded twice (legacy RWB-E2-006 AC8)
    Given the treatment holds result "APPROVED" with reference "NL-SYN-000610" recorded on 2026-12-17
    Given the rwb-treatment contract mock returns that recorded result on the treatment read
    When the officer records a result again
    Then the response is 409 with message MSG-P2-010
    Then the system writes no second decision log entry

  Scenario: AC9 Case not awaiting credit approval (legacy RWB-E2-006 AC9)
    Given case "RW-2026-000620" is in route state "PLAN_RUNNING"
    Given the rwb-case contract mock returns route state "PLAN_RUNNING" for case "RW-2026-000620"
    Given the rwb-treatment contract mock returns a "RESTRUCTURE" treatment for case "RW-2026-000620"
    When the officer records a result for its treatment
    Then the response is 409 with message MSG-P3-005

  Scenario: AC10 Two officers record at once (legacy RWB-E2-006 AC10)
    Given two officers read treatment "TRT-SYN-0610" at version 3
    Given the rwb-treatment contract mock holds treatment version 3
    When both record a result with If-Match version 3
    Then the system saves one result
    Then the system refuses the other with 409 and message MSG-GEN-004

  Scenario: AC11 Decision log write fails (legacy RWB-E2-006 AC11)
    Given the decision log store is unavailable
    Given the rwb-treatment and rwb-case contract mocks record that no call is made
    When the officer records result "APPROVED" with reference "NL-SYN-000613" and approval level "L5"
    Then the response is 503 with message MSG-P7-003
    Then the treatment and the route state do not change
    Then the system raises an incident
```

The eleven criteria are copied unchanged from the legacy story, values included, with the cross-service parts replaced by a contract-mock Given. **AC1, AC4 and AC5 are proved here**, because the pack is assembled from the four contracts and the checklist rows and the input ages are this operation's output. **AC2, AC3, AC6, AC7, AC8, AC9 and AC10 are proved here at Component level** against the contract fakes: the validation, the level comparison, the one-result rule, the version check and the decision record are this operation's, while the treatment state and the four columns are rwb-treatment's and are proved in the S2 story of this legacy key, and the route state, the queue move and the case-side decision record are rwb-case's and are proved in RWB-P3-E2006-APP. **AC11 is proved here** in the sense that matters: the record write fails before any remote call is made, so the treatment and the route state cannot have changed; the case-side and treatment-side proofs that they did not change are the P3 and S2 stories'. The delegation of the approval routing itself, and the versions of the delegation rows, are the P4 and P7 stories'.

The values are kept exactly as the legacy has them, including the level "L5" that AC2 records against a plan the Background puts at "L6" or higher, and the level "L6" that AC7 refuses for a plan that needs "L5". The two statements are inconsistent in the legacy story; both are copied unchanged and the inconsistency is recorded, not repaired here (GAP-0663; ASM-1163).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A restructure outside the approved range or with a deviation goes to credit approval | R-RES-10 |
| BR2 | Credit approval releases the offer to the customer with a 14-day validity | R-RES-11 |
| BR3 | A credit refusal records the reason, then returns the case to the route decision for the case owner | R-RES-12, R-RES-14 |
| BR4 | NLEADS has no interface: the officer submits in NLEADS, ACE ingests the decision, and the decision is read only through the rwb-source-data contract over `v_ace_credit_decision` | INT-26; DL12; DP-05; ADR-010 |
| BR5 | The approval level must be at or above the level the delegation of authority sets for the decision, the product and the amount, read through the rwb-access contract with the version in force and recorded with the decision | doa.txt item 2.1.1; CTL-04; DL18 |
| BR6 | The pack documents are the rows of the NLEADS pack checklist of rwb-case, with the version in force; a row with no document on the case is shown as missing | Document types reference table; DL19; DP-07 |
| BR7 | An input past its age limit is shown with its age, and an accepted result records the freshness of the data it used | MSG-P7-006; REQ-RDF-009 |
| BR8 | A decision that cannot be written to the decision record does not proceed, and no remote change is attempted | Principle 5; R-UNI-39; CTL-06; DP-03 |
| BR9 | A restructure covers every account of the customer in the case, so the pack carries every linked account and adds none | CTL-26 |
| BR10 | One credit result per treatment: a second result is refused and writes no second decision record | Legacy RWB-E2-006 AC8 and X6 |
| BR11 | The integration base holds no copy of a case, a treatment, an account or a document, and no foreign key into another schema; the pack is composed at request time from the owners' contracts | DP-01; D-RCV-35 U4; ADR-010 |
| BR12 | The treatment columns and the treatment state are written only by rwb-treatment, and the route state and the queue only by rwb-case; this story asks for both and writes neither | Arch v5 slide 41; DP-01 |
| BR13 | The pack and the result are reached only through the gateway-bff composite route of SCR-14, never directly from the browser | DP-19 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| AWAITING_CREDIT_APPROVAL | CREDIT_APPROVED | final_call = approved | OFFER_WITH_CUSTOMER |
| AWAITING_CREDIT_APPROVAL | CREDIT_DECLINED | final_call = rejected | DECLINED_BY_CREDIT |
| DECLINED_BY_CREDIT | DECLINE_RECORDED | Any | BACK_TO_ROUTE_DECISION |

The three moves are `recovery_case.route_state` writes of rwb-case, asked for by the CREDIT_APPROVED or CREDIT_DECLINED raise of step 17 and proved in RWB-P3-E2006-APP. The treatment state moves from SUBMITTED to APPROVED or REFUSED in rwb-treatment, through the contract call of step 16 and proved in the S2 story of this legacy key. The state this slice owns is the lifecycle of its own decision record: a record is written once per accepted result with decision "D5", its final call and its actions, and a retry with the same `Idempotency-Key` reuses it instead of writing a second one.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, restructuring officer | Opens the pack and records the result (Treatment and offer, CRUA) |
| RW-CASEOWN, case owner | Opens the pack and records the result on cases in scope (Treatment and offer, CRU) |
| RW-CREDCOMM, RW-PRODHEAD | Read the pack and the result (Treatment and offer, RA); they approve in NLEADS, not in this story |
| rwb-case, through its contract | Receives CREDIT_APPROVED or CREDIT_DECLINED with the reference and the final call; owns the route state, the queue and its own decision record |
| rwb-treatment, through its contract | Records the four NLEADS columns and moves the treatment state; owns the treatment record |
| rwb-access, through its contracts | Answers the Treatment and offer right, and the required approval level with the delegation version in force |
| rwb-source-data, through its contract | Supplies the account, collateral, valuation, freshness and NLEADS credit-decision facts; it is the only reader of the ACE views |
| Decision-record library identity | Writes the local decision record in `rwb_integration` and publishes DecisionRecorded on `rwb.decision-record.v1` (Decision log, C) |
| Approval levels L1 to L6 | As in doa.txt item 2.1.1, recorded from NLEADS |

The service runs as the rwb-integration login (DP-02). The login name is Not specified in the source documents (GAP-0663; ASM-1099).

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-002 | recovery_case, through the rwb-case contract | case_no | Read |
| DF-CAS-003 | recovery_case, through the rwb-case contract | product_group | Read |
| DF-CAS-007 | recovery_case, through the rwb-case contract | route_state | Read; written by rwb-case (P3 story) |
| DF-ACE-002 | v_ace_account, through the rwb-source-data contract | account_code | Read |
| DF-ACC-009 | v_ace_account, through the rwb-source-data contract | principal_outstanding | Read |
| DF-ACC-010 | v_ace_account, through the rwb-source-data contract | interest_outstanding | Read |
| DF-ACE-020 | v_ace_account, through the rwb-source-data contract | total_balance | Read |
| DF-ACE-018 | v_ace_account, through the rwb-source-data contract | days_past_due | Read |
| DF-ACE-036 | v_ace_account, through the rwb-source-data contract | data_as_of | Read |
| DF-ACE-091 | v_ace_collateral, through the rwb-source-data contract | collateral_no | Read |
| DF-ACE-097 | v_ace_collateral, through the rwb-source-data contract | collateral_type | Read |
| DF-ACE-191 | v_ace_valuation, through the rwb-source-data contract | appraised_value | Read |
| DF-ACE-193 | v_ace_valuation, through the rwb-source-data contract | appraisal_date | Read |
| DF-DOC-001 | document, through the rwb-document contract | id | Read |
| DF-DOC-004 | document, through the rwb-document contract | document_type | Read |
| DF-TRT-001 | treatment, through the rwb-treatment contract | id | Read |
| DF-TRT-003 | treatment, through the rwb-treatment contract | decision_log_id | Read here; written by rwb-treatment (S2 story) |
| DF-TRT-004 | treatment, through the rwb-treatment contract | treatment_type | Read |
| DF-TRT-007 | treatment, through the rwb-treatment contract | offer_amount | Read |
| DF-TRT-008 | treatment, through the rwb-treatment contract | haircut_amount | Read |
| DF-TRT-009 | treatment, through the rwb-treatment contract | installments | Read |
| DF-TRT-010 | treatment, through the rwb-treatment contract | valid_until | Read |
| DF-TRT-011 | treatment, through the rwb-treatment contract | approval_level | Read here; written by rwb-treatment (S2 story) |
| DF-TRT-023 | treatment, through the rwb-treatment contract | nleads_ref | Read here; written by rwb-treatment (S2 story) |
| DF-TRT-024 | treatment, through the rwb-treatment contract | credit_result | Read here; written by rwb-treatment (S2 story) |
| DF-TRT-025 | treatment, through the rwb-treatment contract | credit_result_reason | Read here; written by rwb-treatment (S2 story) |
| DF-TRT-026 | treatment, through the rwb-treatment contract | credit_result_at | Read here; written by rwb-treatment (S2 story) |
| Standard column | treatment, through the rwb-treatment contract | state | Read here; written by rwb-treatment (S2 story) |
| DF-DEC-001 to DF-DEC-018 | decision_record (library table in `rwb_integration`) | all fields, including decision code, final call, actions, approval level, rule version and freshness | Write |
| DF-REF-159 to DF-REF-184 | reference_row, through the rwb-case reference-data contract | The NLEADS pack checklist rows and the version in force | Read |

Field IDs are those in the Logical Data Model and Data Dictionary v9. No ACE row, no case row and no treatment row is copied into `rwb_integration`: the service links to them by business key (`account_key`, `treatmentId`) with no foreign key (DP-01, BR11). The NLEADS decision facts of `v_ace_credit_decision` are read through the rwb-source-data contract and are not stored here; what the decision record carries is the reference ACE ingested and the freshness of the read. The only write of this slice is the decision record and its outbox row.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/integration/v1`; owner rwb-integration (P2).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/treatments/{treatmentId}/credit-pack` | The credit approval pack for submission in NLEADS: case number, product group, the accounts with balances and business date, the collateral with its latest appraisal, the plan terms, the required approval level, the checklist documents with a link or as missing, the input ages and the messages | Treatment and offer R, scope applied | Not applicable, read only |
| POST | `/treatments/{treatmentId}/credit-result` | Accepts the NLEADS reference, result, approval level, result date and reason, writes the decision record with decision "D5" in the same local transaction, then records the result through rwb-treatment and raises CREDIT_APPROVED or CREDIT_DECLINED to rwb-case | Treatment and offer U, scope applied | `Idempotency-Key` required with `If-Match`; one result per treatment, a repeat with the same key replays the stored answer, a different key on a recorded treatment returns 409 |

Response fields of the GET follow the legacy CreditPack shape: `caseNo`, `productGroup`, `accounts` (`accountNo`, `principal`, `interest`, `totalBalance`, `daysPastDue`, `dataAsOf`, `ageDays`), `collateral` (`collateralNo`, `type`, `appraisedValue`, `appraisalDate`), `terms` (`offerAmount`, `haircutAmount`, `installments`, `validUntil`), `requiredLevel`, `documents` (`type`, `documentId` or `missing`), `messages`. The request fields of the POST follow the legacy CreditResult shape: `nleadsRef` (1 to 30 letters, digits and dashes; format assumed until SCB IT confirms, DL12), `result` (APPROVED or REFUSED), `approvalLevel` (L1 to L6), `resultDate`, `reason` (1 to 1,000 characters, required when REFUSED), with the header `If-Match`; the 200 answer is the treatment as rwb-treatment returns it, with the decision-record reference.

Errors: 401 no session (MSG-P4-001); 403 no Treatment and offer right (MSG-P4-002); 404 not found or out of scope (MSG-P4-003); 409 state (MSG-P3-005), already recorded (MSG-P2-010), level too low (MSG-P2-018) or version (MSG-GEN-004); 422 (MSG-GEN-001, MSG-GEN-002); 502 or 503 a source interface unavailable (MSG-GEN-006), and 503 a failed decision record (MSG-P7-003).

The two operations are the ones the Ownership Map keeps with rwb-integration, at the legacy treatment-scoped paths under the integration base of DP-13. Their placement against the integration-base catalogue and the retirement entry of the technical specification are recorded as a conflict; the JSON field names of the request and the response are Not specified in the source documents (GAP-0663; ASM-1160).

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | rwb-treatment (S2) | The case reference, the treatment type and state, the plan terms, the recorded result and the version | One hop, 2 s (DP-11) |
| PATCH | `/api/recovery/treatment/v1/treatments/{treatmentId}` | rwb-treatment (S2) | Records the reference, the result, the reason, the approval level and the result date, and moves the treatment state | One hop, 2 s (DP-11) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | rwb-case (P3) | The case number, the product group, the route state and the linked accounts | One hop, 2 s (DP-11) |
| POST | `/api/recovery/case/v1/cases/{caseId}/actions` | rwb-case (P3) | Raises CREDIT_APPROVED or CREDIT_DECLINED with the reference, the final call and the freshness | One hop, 2 s (DP-11) |
| GET | `/api/recovery/source-data/v1/accounts/{id}` | rwb-source-data (P1) | The balance, arrears and `data_as_of` of each linked account | One hop, 2 s (DP-11) |
| GET | `/api/recovery/source-data/v1/collateral/{id}` | rwb-source-data (P1) | The collateral and its latest appraisal | One hop, 2 s (DP-11) |
| GET | `/api/recovery/source-data/v1/freshness` | rwb-source-data (P1) | The ACE business date and batch state behind each input (REQ-RDF-009) | One hop, 2 s (DP-11) |
| The NLEADS credit-decision read of the rwb-source-data contract | rwb-source-data (P1) | The reference, result, approval level, result date and reason behind the recorded result, over `v_ace_credit_decision` | One hop, 2 s (DP-11) |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | rwb-document (P5) | The checklist documents and their links | One hop, 2 s (DP-11) |
| GET | `/api/recovery/access/v1/doa-limits` | rwb-access (P4) | The required approval level for decision D5, the product group and the amount under item 2.1.1, with the version in force | One hop, 2 s (DP-11) |
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | Role, scope and right check before a read or a write | One hop, 2 s (DP-11) |
| The reference-data read of the rwb-case contract (RWB-P3-E1043-CON) | rwb-case (P3) | The NLEADS pack checklist rows with the version in force | One hop, 2 s (DP-11) |

The NLEADS credit-decision operation name and field shape are Not specified in the source documents (GAP-0663; ASM-1159). The operation that records the credit result on the treatment, and the JSON field names of that contract, are Not specified in the source documents (GAP-0663; ASM-1160). The path of the reference-data read is Not specified in the source documents (GAP-0663; ASM-1164). The case action that carries CREDIT_APPROVED and CREDIT_DECLINED is the case action operation of RWB-P3-E2006-APP, because this slice publishes no business event; its request shape is Not specified in the source documents (GAP-0663; ASM-1161).

#### 12.3 Events published

None on `rwb.integration.events.v1` by this story's own work: FileDelivered and FileFailed are the outbound-file events of the integration base, RWB-P2-E1007-APP. The decision-record library publishes `rwb.decision-record.DecisionRecorded.v1` (EV-08) on `rwb.decision-record.v1` from the same transaction as the acceptance, with the decision code "D5", the final call, the NLEADS reference in the actions, the approval level, the delegation version and the freshness of the data used (DP-03, H RWB-PLT-E1027-CON).

#### 12.4 Events consumed

None. The NLEADS decision arrives as ACE data and is read through the rwb-source-data contract at the officer's request; this story subscribes to no topic and consumes no case event.

#### 12.5 Workflows and activities

None. This story starts no workflow and adds no activity; the Temporal worker and the integration-base activities are RWB-P2-E1007-APP's. The officer-driven pair of operations is synchronous REST, one hop per contract.

#### 12.6 Schedules

None. The credit approval is officer-driven; no Schedule and no timer is created by this story.

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| decision_record | rwb_integration | PLT library, created in rwb_integration | The local record of the accepted NLEADS result, written in the same transaction as the acceptance (DP-03) |
| idempotency_key | rwb_integration | PLT library, created in rwb_integration | The stored response of a POST sent with an `Idempotency-Key` |
| outbox_event, outbox_delivery | rwb_integration | PLT library, created in rwb_integration | The rows the decision-record library writes and the relay publishes on its behalf |

This story adds no business table. `interface_config`, `outbound_item` and `job_catalog` stay the integration base's and are untouched here. rwb-integration reads no table of another service, holds no foreign key across services, and reads no ACE view (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-source-data WireMock | The P1 contract | `GET /accounts/{id}`, `GET /collateral/{id}`, `GET /freshness` and the NLEADS credit-decision read, with the fixtures of AC1, AC2, AC3 and the 2026-12-12 balances of AC5 |
| rwb-treatment WireMock | The S2 contract | `GET /treatments/{treatmentId}` for the plan terms, the recorded result states of AC2 and AC3 and version 3 of AC10; `PATCH /treatments/{treatmentId}` for the accepted result, the refusal and the version conflict |
| rwb-case WireMock | The P3 contract and its reference data | `GET /cases/{caseId}`, `POST /cases/{caseId}/actions`, and the reference-data read returning the five checklist rows with the version in force |
| rwb-document WireMock | The P5 contract | `GET /cases/{caseId}/documents` presenting the five checklist documents with links, and the four-of-five answer of AC4 |
| rwb-access WireMock | The P4 contract | `GET /doa-limits` returning level "L6" for item 2.1.1, and `POST /authorise` granting and refusing the Treatment and offer right |
| Decision-record library stub | RWB-PLT-E1027-CON | A committed record, and the unavailable-store case of AC11 that must leave the two remote fakes uncalled |
| gateway-bff composite route stub | The edge route of RWB-PLT-N001-CON | The SCR-14 route that reaches the two integration-base operations (AC1) |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 11 named consumed plus the NLEADS credit-decision read and the reference-data read | Pack and result provided; treatment, case, source-data, document, delegation and authorise consumed; one hop, 2 s timeout each, GET retried once with jitter |
| Kafka | None published by this service's own work, 1 published by the decision-record library | `rwb.decision-record.v1` carries DecisionRecorded on the service's behalf (DP-03); `rwb.integration.events.v1` is not used by this slice |
| Temporal | None | No workflow, no activity, no signal, no Schedule |
| File | None | This story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.integration`, module `nleads`, Java package `th.co.scb.ace.workbench.recovery.integration.nleads`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views; this service has no view of its own | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

RWB-P3-E1043-CON is another service's contract story, so it sits in the contract-dependency row, not the build row; RWB-P3-E2004-CON is the second contract this slice builds against.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CreditPackController | Controller | `GET /treatments/{treatmentId}/credit-pack` and `POST /treatments/{treatmentId}/credit-result`; request and header validation; problem responses |
| CreditPackService | Service | Composes the pack from the rwb-case, rwb-treatment, rwb-source-data, rwb-document and rwb-access contracts; checklist rows; input age and messages |
| CreditResultService | Service | Validates the reference, the result, the level, the date, the reason, the case state, the one-result rule and the version; writes the decision record first; records the result; raises the case event |
| CreditResultValidator | Service | The field and cross-field rules of the CreditResult shape, with one message per field |
| DecisionRecordWriter | Library client | Calls the local decision-record library with decision "D5", the final call, the actions, the level, the delegation version and the freshness; a failure fails the transaction (DP-03) |
| TreatmentClient | Client | The plan-terms read, the recorded-result read and the result record on the rwb-treatment contract, with `If-Match` |
| CaseClient | Client | The case read and the CREDIT_APPROVED or CREDIT_DECLINED raise on the rwb-case contract |
| SourceDataClient | Client | Accounts, collateral, freshness and the NLEADS credit-decision read (DP-05) |
| DocumentClient | Client | The checklist documents; a failure marks the document section, not the pack |
| ChecklistCatalog | Service | Reads the NLEADS pack checklist rows through the reference-data contract; no document type in code (DP-07) |
| DoaLimitClient | Client | The required level of item 2.1.1 with the version in force |
| AccessCheckClient | Client | The authorise contract, cached per session, before a read or a write |

**Database and migrations**

- One migration in the rwb-integration sequence: `V2006_1__credit_result_record.sql` adds the partial index on `decision_record (decision_code, created_at)` and on `decision_record (case_id, decision_code)` that the one-result and ledger reads use, and includes the library tables `decision_record`, `idempotency_key`, `outbox_event` and `outbox_delivery` in `rwb_integration` (DP-15).
- No new business table and no new column on anything but the library tables. The four NLEADS columns are on the treatment and are rwb-treatment's, added by the S2 story of this legacy key.
- The one-result rule is enforced by the treatment state read through the rwb-treatment contract plus the decision-record check inside the local transaction; no unique table is added (BR10).

**Configuration and reference data**

- The NLEADS pack checklist stays reference data of rwb-case and is read through its contract with the version in force (DL19); the five items the legacy story assumes are CREDIT_APPLICATION, ID_COPY, TITLE_DEED, LATEST_APPRAISAL and INCOME_PROOF.
- The balance age limit of 1 business day (assumed in the legacy story under DL22) is read as a reference row, not written in code.
- The delegation rows for item 2.1.1 stay in rwb-access (DL18) and are read through its contract; this service holds no copy.
- The feature switch keeps the legacy name `rwb.integration.nleads-pack` as the legacy reference. In the target it is a feature flag of the platform flag library; off refuses the POST with MSG-GEN-006 while nothing is written, and hides the pack from the composite route.

**Build steps**

1. CreditPackService and CreditPackController against the contract stubs, one test per pack section; AC1, AC4.
2. SourceDataClient over the rwb-source-data contract for accounts, collateral, freshness and the NLEADS credit-decision read; AC1, AC2, AC3.
3. TreatmentClient and CaseClient over their contracts, with the plan-terms read, the recorded-result read, the case read and the raise; AC2, AC3, AC9.
4. DocumentClient and ChecklistCatalog over their contracts, with the per-section degradation and the missing-row message; AC1, AC4.
5. The input age and its message in CreditPackService, from the freshness read and the age-limit row; AC5.
6. CreditResultValidator: reference, result, level, date and reason; AC6, AC7.
7. The case-state, one-result and version checks; AC8, AC9, AC10.
8. DecisionRecordWriter before any remote change, with the rollback path and the incident; AC11.
9. The record call on the rwb-treatment contract, then the raise on the rwb-case contract, then the stored response against the `Idempotency-Key`; AC2, AC3, AC10.
10. The contract-fake run of every cross-service answer in isolation, so the story builds before the other services exist.
11. The composite-route stub run, so SCR-14 can be shown reaching both providers.

**Done when.** The tests in section 16 pass, every accepted result names decision "D5" and the freshness of the data it used, the pack is assembled from contracts alone with no ACE view and no foreign table, a failed decision record leaves both remote fakes uncalled, and the contract tests of RWB-PLT-E1027-CON, RWB-P3-E1043-CON and RWB-P3-E2004-CON stay green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-009 | A checklist document is missing from the pack | The credit approval pack is missing {item}. Add it to the case before you submit in NLEADS. |
| MSG-P7-006 | An input is past its age limit | {input} is {days} days old, past its limit. Refresh it before you decide. |
| MSG-GEN-001 | Reference or refusal reason empty | Enter {field}. |
| MSG-GEN-002 | Result date after today | {field} must be between {min} and {max}. |
| MSG-P2-018 | NLEADS approval level below the required level | The NLEADS approval is at level {level}. This plan needs level {required} or higher. |
| MSG-P2-010 | Result already recorded | The NLEADS result for this treatment was recorded on {date}. |
| MSG-P3-005 | Case not awaiting credit approval | This case cannot move to {state} from {current}. |
| MSG-GEN-004 | Treatment changed by someone else | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role without the right | You cannot {action} here. Your role does not include it. |
| MSG-GEN-006 | A source contract did not answer | {source} could not be read. Try again in a few minutes. |

MSG-P3-005 names the target route state and the current one only. MSG-P7-003 is raised after the local transaction has rolled back, and the incident carries the case reference, the decision code and the failure class, never a personal value. MSG-GEN-006 names the section or the step, never the payload.

### 15. Screens and states

SCR-14 Treatment record, credit approval panel. In state submitted the officer opens the pack, copies each field into NLEADS and opens each document link; a missing item and a stale input show their own message. The officer records the result in the result form; the panel moves to state approved, or shows the refusal reason while the case leaves the officer's view for the case owner's queue. This story supplies the values of the panel through the two operations; the panel and its field-level behaviour are the screen work of RWB-P3-E2006-APP, which serves the case-side pack.

The screen is reached through the gateway-bff composite route, which calls the case-side pack and this story's pack in parallel, one hop each, and merges the answers into the screen model (DP-19). The route specification, the merge rule between the two pack answers and the field-level masking are Not specified in the source documents (GAP-0663; ASM-1166).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-006-12 | Access | Component | RW-PHONECOL calls the result operation; refused with MSG-P4-002 |
| TC-E2-006-01 | AC1, BR6, BR9 | End to end | Synthetic case with 2 accounts, 1 collateral and 5 checklist documents |
| TC-E2-006-02 | AC2, BR2 | End to end | Result APPROVED at level L5 |
| TC-E2-006-03 | AC3, BR3 | End to end | Result REFUSED with a reason |
| TC-E2-006-04 | AC4, BR6 | End to end | No INCOME_PROOF document |
| TC-E2-006-05 | AC5, BR7 | End to end | Account load of 2026-12-12 |
| TC-E2-006-06 | AC6 | End to end | Empty reason; result date in the future |
| TC-E2-006-07 | AC7, BR5 | End to end | Level L6 for a plan that needs L5 |
| TC-E2-006-08 | AC8 | End to end | Result recorded twice |
| TC-E2-006-09 | AC9, BR1 | End to end | Case in PLAN_RUNNING |
| TC-E2-006-10 | AC10 | End to end | Two results with If-Match version 3 |
| TC-E2-006-11 | AC11, BR8 | End to end | Decision log store stopped during a result |
| TC-E2-006-13 | Principle 5 | NFR | Decision log write forced to fail; treatment and route state unchanged; MSG-P7-003 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end, Access to Component and Resilience to NFR.

This story runs TC-E2-006-01 to TC-E2-006-10 and TC-E2-006-12 against its two operations with the contract fakes: the pack tests at Component level, the result tests at Component level with the treatment and case answers stubbed, and the access test at its own endpoint. TC-E2-006-11 and TC-E2-006-13 are cited for the legacy key: the blocking half is proved here, because a failed decision record leaves the treatment and case fakes uncalled, and the End-to-end and NFR proof that the treatment and the route state do not change is RWB-P3-E2006-APP's and the S2 story's. The approval routing of the level behind BR5 is the P4 and P7 stories'.

The values of TC-E2-006-02 and TC-E2-006-07 are kept exactly as the legacy has them, level "L5" for an approval and level "L6" refused for a plan that needs "L5", although the Background of the criteria sets the plan at "L6" or higher.

### 17. Guardrails

- No business value in code: the checklist rows, the age limit and the delegation levels are data rows of their owners; the story fixes only the behaviour.
- No personal data in logs, tests, workflow history or prompts. The pack reads `account_key`, `person_key` and amounts only; the refusal reason is free text and is written to the decision record, never to application logs.
- No read of another service's tables and no ACE view: account, collateral, valuation, freshness and NLEADS credit-decision facts come only through the rwb-source-data contract; plan terms and the result record only through the rwb-treatment contract; the case only through the rwb-case contract; documents only through the rwb-document contract; the required level only through the rwb-access contract (DP-01, DP-05).
- `rwb_integration` holds no foreign key into another schema; the service links to ACE, the case and the treatment by business key only.
- The decision record is written before any remote change; a failure blocks the action and raises an incident (R-UNI-39).
- No call to NLEADS from the Workbench: the officer submits in NLEADS and ACE ingests the decision.
- The treatment columns and the state are written only by rwb-treatment, and the route state, the queue and the owner only by rwb-case; this story asks for both and writes neither.
- The service runs as the rwb-integration login and reaches the two operations only through the gateway-bff composite route.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-008 | A plan submitted for credit approval is recorded on the case | Epic 2, 3.2; Program, 5.3 | FEAT-CHO-07 | 7.3 Negotiate settlement or deed in lieu | R-RES-10, R-RES-11, R-RES-12, R-RES-14, R-UNI-39 | TC-E2-006-02, TC-E2-006-03, TC-E2-006-06 to TC-E2-006-11, TC-E2-006-13 |
| REQ-CHO-006 | The treatment holds its type, terms, approval and outcome | Epic 2, 3.2; Program, 5.3 | FEAT-CHO-07 | 7.3 Negotiate settlement or deed in lieu | None | TC-E2-006-01, TC-E2-006-04, TC-E2-006-05, TC-E2-006-12 |
| REQ-RDF-009 | Every data product carries a freshness stamp, and every decision records the freshness of the data it used | Program, 5.3 | FEAT-CHO-07 | 7.3 Negotiate settlement or deed in lieu | R-UNI-39 | TC-E2-006-01, TC-E2-006-05, TC-E2-006-11 |

### 19. Out of scope

- The case-side credit approval pack, the route state, the queue move and the case-side decision record: carried by RWB-P3-E2006-APP.
- The four NLEADS columns on the treatment, its APPROVED or REFUSED state and the treatment record screen: carried by the S2 story of this legacy key.
- The delegation table itself, its versions and the approval workflow in rwb-decision: the P4 and P7 stories; this story only reads the level through their contracts.
- The panel and the result form on SCR-14, and their field-level behaviour: RWB-P3-E2006-APP.
- The integration base, its Temporal worker, its outbound-file adapters and its topic: RWB-P2-E1007-APP.
- Generating a credit application document from a template: RWB-E2-026.
- Booking the plan in NLEADS and ALS and its confirmation: RWB-E2-007 and Epic 3 (R-RES-21, R-RES-22).
- Approval inside the Workbench for decisions within the delegation: RWB-E2-013.
- Any direct read of an ACE view, and any call to NLEADS.
