# RWB-S6-E6003-CON Bar a buyer that fails qualification - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E6003-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-003 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Not set; the squad sizes the story at refinement |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | API Specification v5 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the remediation and bar step of rwb-debtsale, split from RWB-E6-003. It fixes the bar element and the answer shape it appears in (DP-13), the release and panel-request elements and their closed lists, the six consumed rows for the rwb-partner panel read and suspension request, the rwb-case state read and move answer, the rwb-access right and the rwb-decision package, the window of R-DS-40 as a workflow timer, the decision-record element of DP-03, the rights, the error envelope, the fakes and the absence tests. TSD S6 T-A publishes no bar operation, so the baseline declares no operation as provided and records the two legacy endpoint rows as RWB-S6-E6005-APP's and RWB-S6-E5026-APP's. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S6-E6003-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (12 resolved, 15 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the remediation and bar step of rwb-debtsale - the bar element and the answer shape it appears in, the release and panel-request elements with their closed lists, the six consumed rows, the window element, the decision-record element, the rights, the error envelope and the fakes**, so that **the app story, SCR-26 Award, the data room, the re-offer at the award and the wave 4 harness build against one fixed, testable contract on Day 1, and a buyer fact, a move name, a lot status or an answer shape can never drift between rwb-debtsale, rwb-partner, rwb-case, rwb-access, rwb-decision and the award story without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy bar of RWB-E6-003 crossed four boundaries at once: a partner panel, a buyer's licence and KYC facts, a case state and a decision log. The target splits them: rwb-partner owns the panel and the evidence, rwb-case owns the case and its route states, rwb-access owns the right, rwb-decision owns the package in force and its ledger, and rwb-debtsale owns the lot and its release. Each boundary is now a contract another team builds against, so each has to be fixed before the app story starts: the bar and release elements, the panel request, the closed lists, the state and move vocabulary, the window and the record of the decision.

The baseline also fixes the naming the checks require: schema `rwb_debtsale`, login `rwb_debtsale`, base `/api/recovery/debtsale/v1`, topic `rwb.debtsale.events.v1` with its retry and `.dlt` topics, task queue `rwb-debtsale` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.debtsale` (context pack S6).

Four points are carried as gaps and assumptions rather than decided quietly. The plan's C row for this slice is None while the step needs six consumed rows (GAP-2987). TSD S6 appendix T-A publishes no bar or panel operation, so the baseline declares none and records the two legacy endpoint rows as its siblings' (GAP-2987). The `panel_status` vocabulary and the operation names of the panel read and the suspension request are published by no source, so they carry the placeholder. And the lot status value taken at the release, and the next qualified bidder to whom the lot is released, are named by no source either: the release value carries the placeholder and the re-offer stays with R-DS-28 at the award story (GAP-2987).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the context pack and the Ownership Map only: `debt_sale_lot` and `debt_sale_account` are S6's, `recovery_case` and `timer` are P3's, `role` and `permission` are P4's, `decision_log_entry` and `rule_row` are P7's, `notice` is P6's, and the partner panel and the buyer's evidence are S9's. This document never declares another service's table or operation as its own.
- The rwb-partner panel contract, the rwb-case state and move rows, the rwb-access authorise contract and the rwb-decision package row are published with their fakes; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-2987; ASM-4920).
- The Debt sale rule package and its rows R-DS-14, R-DS-16, R-DS-40 and R-DS-41 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- `debt_sale_lot` and `debt_sale_account` arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 fragment of rwb-debtsale for this step: the bar element and the answer shape it is embedded in, with the rights and the error responses, and no operation of its own (GAP-2987; ASM-4922).
2. Fix the release and panel-request elements: the lot reference, the buyer partner reference, the buyer class, the lot status at the release, the panel request with its reason and rule reference, the bar state, the rule ID with its version and the decided-at time.
3. Fix the six consumed rows, marking the fields the sources do not give with `Not specified in the source documents (GAP-2987)`.
4. Record the window element of R-DS-40: a durable workflow timer at the package's 10-working-day target, with no Schedule and no Quartz row.
5. Record the decision-record element of DP-03, written before the lot row changes.
6. Record the closed vocabulary of the lists, the state and move names, the naming baseline and the rule that no value is a constant of the code.
7. Record that the buyer is an organisation, that no person field is a property of any element, example or fake, and that the evidence is a reference of its owners.
8. Publish the contract tables of section 12 and the fakes of 12.8.
9. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a provided operation, the absence of a `partner` or `recovery_case` property, the drift between a fake and the document, and the absence of published and consumed events.
10. Tag the baseline and hand it to RWB-S6-E6003-APP, the award story's re-offer, SCR-26 Award, the data room and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request or a response body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC6 |
| X2 | A property is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC5 |
| X5 | A value outside `LOV-BUYER-CLASS`, `LOV-LOT-STATUS`, `LOV-SEGMENT` or `LOV-PUTBACK` appears in the document or in an example | The vocabulary test fails the build | None | AC2 |
| X6 | The document declares a provided operation, a `partner` or `recovery_case` property, a case-row write or a `decision_log_entry` column | The review fails the baseline and the boundary test fails the build | None | AC3, AC4, AC6 |
| X7 | The document declares a published or a consumed event, a second topic, a Schedule or a Quartz row | The absence test fails the build | None | AC6 |
| X8 | A person field appears in any element, example or fake | The schema test and the review fail the baseline | None | AC2, AC6 |
| X9 | The rights of a surface are not the ones TSD S6 T6.1 declares | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack and the published owner contracts of rwb-partner, rwb-case, rwb-access and rwb-decision only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the element set, the lists, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S6-E6003-APP, the award story's re-offer, SCR-26 Award, the data room and the wave 4 harness on Day 1 |
| Estimable | One OpenAPI fragment, nine contract tables, eight fakes and five new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the remediation and bar step of rwb-debtsale

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of debt_sale_lot and debt_sale_account is S6, of recovery_case is P3, of role is P4, of decision_log_entry and rule_row is P7, and of the partner panel is S9
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The bar element and its answer shape are declared with their errors (new, D-RCV-60)
    Given the OpenAPI 3.1 fragment of rwb-debtsale for this step is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the bar element with the lot reference, the buyer partner reference, the bar state, the rule ID with its version and the decided-at time, and it declares no operation of its own
    Then it records that the element is embedded in the answer of the lot read API-S6-002 and in the answer of the data room read API-S6-004, which are a sibling story's and RWB-S6-E5026-APP's, and that it narrows neither answer
    Then the answers 400, 401, 403, 404, 409, 422 and 503 are declared with one envelope and one message ID per condition
    Then every other property of the answers is copied from the baseline that owns the operation and is not redefined here

  Scenario: AC2 The release and panel-request elements and their closed lists are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S6 T3.1, T3.2 and the rule rows R-DS-40 and R-DS-41
    Then the Release element declares the lot reference, the buyer partner reference, the buyer class, the lot status at the release and the account set of the lot, and its lot status is declared against LOV-LOT-STATUS
    Then the value taken from LOV-LOT-STATUS at the release is Not specified in the source documents (GAP-2987; ASM-4924) and the element requires it where the source is silent about the value only
    Then the PanelRequest element declares the buyer partner reference, the reason of R-DS-41 and the rule ID with its version, and it declares no panel status value because the vocabulary is the owner's
    Then buyer_class is declared against LOV-BUYER-CLASS with the values AMC and NON_AMC, segment against LOV-SEGMENT with RETAIL, SSME and CORPORATE, and put_back_status against LOV-PUTBACK with NONE, CLAIMED, ACCEPTED and REJECTED
    Then the panel status values active and suspended are named as the values the rules test and the full list is Not specified in the source documents (GAP-2987; ASM-4921)
    Then no property carries a person name, an identity number, a date of birth or a contact value, and the schema test fails any element, example or fake that adds one

  Scenario: AC3 The rwb-partner panel rows are declared as consumed and never as owned (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with rwb-partner as the owner of the panel and of the buyer's evidence
    Then the panel read is declared with the partner reference, the licence expiry, the KYC status, the panel status and the buyer class
    Then the panel suspension request is declared with the partner reference, the reason and the rule ID with its version, and the answer carries the applied state
    Then the operation names of both rows are Not specified in the source documents (GAP-2987; ASM-4921) and each row carries the placeholder
    Then the document declares no partner, partner_user or evidence table property, no NDA storage and no grant on rwb_partner
    Then each call is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The rwb-case state and move rows are declared with their two moves (new, D-RCV-60)
    Given the consumed rows and the state section of the baseline
    When they are compared with rwb-case as the owner of recovery_case and with TSD S6 T4
    Then the case state read and the case-move answer are declared as consumed, with the case reference, the route state and the move BACK_TO_CASE_LIST or BUYER_PENDING_KYC carrying the rule ID and its version
    Then the operation name of the case-move answer is Not specified in the source documents (GAP-2987; ASM-4920) and the row carries the placeholder
    Then the document declares no recovery_case property, no case route-state column and no write of a case row from rwb-debtsale
    Then the route states named are DATA_ROOM_OPEN, BUYER_PENDING_KYC, BUYER_REJECTED and BACK_TO_CASE_LIST, and no other state of the DEBTSALE machine is declared by this step
    Then R-DS-14 and R-DS-16 are named as the qualification story's evaluation whose answers open this window, and no criterion of this baseline evaluates them

  Scenario: AC5 The window, the rule package and the rwb-access rights are fixed (new, D-RCV-60)
    Given the window and the access sections of the baseline
    When they are compared with R-DS-40, R-DS-41 and TSD S6 T6.1
    Then the window is declared as a durable workflow timer at the package's 10-working-day target, read from the package in force and started from the rejection's decided-at time, and no Schedule, Quartz row or shared job table is declared
    Then the Debt sale package read is declared as consumed from P7 rwb-decision, with the package version in force and the rule rows R-DS-14, R-DS-16, R-DS-40 and R-DS-41 named and not declared
    Then the capability areas Debt sale and Partner portal with their rights are declared as consumed from P4 rwb-access, with RW-HEADASL RA, RW-DEBTSALE CRUA, RW-PRODHEAD RA, PT-BUYER RU scoped to its own lot and the SY-* identities R as TSD S6 T6.1 gives them
    Then the authorise operation name is Not specified in the source documents (GAP-2987; ASM-4920) and the row carries the placeholder
    Then a refused caller answers 403 with MSG-P4-002, and a repeated timer fire or request with the same Idempotency-Key describes no second effect

  Scenario: AC6 The decision-record element, the fakes and the naming baseline answer the document (new, D-RCV-60)
    Given the decision section, the fakes and the naming section of the baseline
    When each is compared with the library schema, with the element it serves and with the nine sub-tables
    Then one decision record is declared per rule outcome with the case reference, the lot reference, the buyer partner reference, the rule ID, the package version in force, the inputs reference, the outcome, the reason, the case move and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before the lot row changes, and a failed write leaves the lot unchanged with MSG-P7-003
    Then the rwb-partner fake answers an expired licence with the panel status suspended, a licence in date with the panel status active, no evidence inside the window, evidence inside the window and a refused suspension, and no answer beyond 2 s
    Then the rwb-case fake answers the four route states of AC4 with an accepted and a refused move, the rwb-access fake answers the two capability areas with and without the right, the rwb-decision fake answers the package at its version, and the decision-record stub answers a healthy and a stopped chain
    Then the schema is rwb_debtsale, the login is rwb_debtsale, the base is /api/recovery/debtsale/v1, the topic is rwb.debtsale.events.v1, the queue is rwb-debtsale and the Java package is th.co.scb.ace.workbench.recovery.debtsale
    Then 12.1 is None and records that TSD S6 T-A publishes no bar operation and that the award path API-S6-003 and the data room read API-S6-004 are RWB-S6-E6005-APP's and RWB-S6-E5026-APP's
    Then the document declares no published event and no consumed event for this step, and the absence tests fail a build that adds one
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S6-E6003-APP and they copy no criterion of the legacy story, whose four criteria stay with the app story word for word.

Scenario: AC7 The contract answers each rule of section 8 with the element, shape or absence it names (new, D-RCV-60)

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The lot release is rwb-debtsale's, and the contract declares its fields, its lists and its required flags on the release element only | Architecture v5 slide 4; TSD S6 T3.1 and T3.2 |
| BR2 | The decision record is declared as an element written before the lot row changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S6 T2; legacy RWB-E6-003 AC1 and AC4 |
| BR3 | The panel and the buyer's evidence stay with rwb-partner: the contract declares the panel read and the suspension request as consumed, and declares no partner property and no NDA storage | Architecture v5 slides 4 and 13; GAP-2987 |
| BR4 | The case move is answered and not written: the contract declares the state read and the two moves, and declares no `recovery_case` property | Architecture v5 slides 3 and 13; GAP-2987 |
| BR5 | This baseline declares no provided operation: the step runs behind the lot read, the data room read and the award operation of its siblings | TSD S6 T-A.1; GAP-2987 |
| BR6 | A POST declares the `Idempotency-Key` and stores its answer; the surfaces this step serves are reads and the panel request is declared on its owner's operation | Architecture v5 slide 11; TSD S6 T-A.2 |
| BR7 | The vocabulary is closed: `LOV-BUYER-CLASS`, `LOV-LOT-STATUS`, `LOV-SEGMENT` and `LOV-PUTBACK` are published enumerations and no list value is a constant of the code | TSD S6 T3.2; FSD S6 BR-S6-007 |
| BR8 | No personal data in a schema, an example or a fake: the buyer is a partner organisation and no name, identity number, date of birth, address or contact value is declared | Template and Rules v1 §R7.2 (s17); FSD S6 A2.3 |
| BR9 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13; Template and Rules §R4 |
| BR10 | A schema change is additive within major version 1; a breaking change, including a change to a move name or a list value, is a new major version | Architecture v5 slide 11 (BACKWARD compatibility) |
| BR11 | The rule rows of R-DS-14, R-DS-16, R-DS-40 and R-DS-41, the 10-working-day window and the licence and panel conditions are governed in rwb-decision and named here, never declared here | Business Rules and Routing Logic v4; GAP-2987 |
| BR12 | The window is a workflow timer and never a Schedule: the baseline declares no `JOB-nn` row, no shared job table and no batch table | DP-10 shape; ASM-4923 |
| BR13 | The release of the lot and the re-offer of R-DS-28 meet at the lot status only; the baseline declares the release value as a placeholder and the selection of the next bidder as the award story's | R-DS-41 and R-DS-28; GAP-2987; ASM-4924 |

### 9. State transitions

The lifecycle of this document, not of a lot:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The elements, the lists, the six consumed rows, the window and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the award story's re-offer, SCR-26 Award, the data room, the wave 4 harness and the rwb-partner, rwb-case, rwb-access and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional reason code | Baselined |
| Baselined | Breaking change | A property, a move name or a list value is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests fail: a provided operation, a `partner` property, a `recovery_case` property, an event, a Schedule or a person field | In review |

The remediation state machine the document describes is the app story's: a rejected buyer's lot moves to re-opened or barred and the case is answered. This baseline fixes the vocabulary of those states and moves no lot.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-debtsale | Owns the OpenAPI fragment and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the rows the baseline consumes, including the absent bar operation and the panel request |
| Consuming teams (the app story, the award story's re-offer, SCR-26 Award, the data room, the wave 4 harness and the owners of rwb-partner, rwb-case, rwb-access and rwb-decision) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake, and that the buyer is an organisation |

The per-service login behind the security scheme of the document is named "the rwb_debtsale login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | BR Field ID | Content |
|---|---|---|
| Bar element | Not specified in the source documents (DOR-RWB-S6-E6003-CON-7) | The lot reference, the buyer partner reference, the bar state, the rule ID with its version and the decided-at time |
| Release element | Not specified in the source documents (DOR-RWB-S6-E6003-CON-7) | The lot properties of DF-SAL-020 to DF-SAL-030 with `buyer_partner_id` (DF-SAL-025), `buyer_class` (DF-SAL-026) and `status` (DF-SAL-030) as the columns the release writes; the account set of DF-SAL-031 to DF-SAL-037 is referenced; the release value of the lot status carries the placeholder (GAP-2987; ASM-4924) |
| PanelRequest element | Not specified in the source documents (DOR-RWB-S6-E6003-CON-7) | The buyer partner reference, the reason of R-DS-41 and the rule ID with its version; the applied state in the answer; the list of the applied states is Not specified in the source documents (GAP-2987; ASM-4921) |
| Lists | Not specified in the source documents (DOR-RWB-S6-E6003-CON-7) | `LOV-BUYER-CLASS` (`AMC`, `NON_AMC`), `LOV-LOT-STATUS` (`BUILDING`, `OFFERED`, `AWARDED`, `TRANSFERRED`, `CLOSED`), `LOV-SEGMENT` (`RETAIL`, `SSME`, `CORPORATE`) and `LOV-PUTBACK` (`NONE`, `CLAIMED`, `ACCEPTED`, `REJECTED`), published as enumerations and read at their version; the reference-data contract is DP-06 and DP-07, and the parameters read are Not specified in the source documents (DOR-RWB-S6-E6003-CON-20) |
| Window | Not specified in the source documents (DOR-RWB-S6-E6003-CON-7) | One timer element per lot at the package's 10-working-day target, started from the rejection's decided-at time, declared as a durable workflow timer (AC5) |
| Decision record | Not specified in the source documents (DOR-RWB-S6-E6003-CON-7) | DF-DEC-001 to DF-DEC-018 through the local library, written before the lot row changes (DP-03) |
| Buyer facts | Not specified in the source documents (DOR-RWB-S6-E6003-CON-7) | The partner reference, the licence expiry, the KYC status and the panel status, of S9 rwb-partner, read only through the owner's contract and never copied or joined here |
| Not declared here | Not specified in the source documents (DOR-RWB-S6-E6003-CON-7) | `recovery_case` and `timer` (P3), `partner`, `partner_user` and the evidence tables (S9), `role` and `permission` (P4), `document` (P5), `notice` (P6), `decision_log_entry` and `rule_row` (P7), `proceeds` (P8) and every `v_ace_*` view (P1) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC2 and the additive rule of BR10. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

None of its own. TSD S6 appendix T-A publishes five operations for the module: API-S6-001 `POST /debt-sale-lots` (C), API-S6-002 `GET /debt-sale-lots/{lotId}` (R), API-S6-003 `POST /debt-sale-lots/{lotId}/award` (A), API-S6-004 `GET /partner/data-room/{lotId}` (Partner portal R) and API-S6-005 `POST /partner/data-room/{lotId}/bids` (Partner portal C), and none of them is a bar, remediation or panel operation. The two endpoint rows of the legacy story are API-S6-003 and API-S6-004; they are RWB-S6-E6005-APP's and RWB-S6-E5026-APP's, and API-S6-005 belongs to the take-bids story. This baseline therefore declares no operation as provided, records the sibling rows by name, and fixes only the bar element and the answer shape it is embedded in. The absence is recorded as GAP-2987 with ASM-4922.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The buyer's licence, KYC and panel facts (operation name Not specified in the source documents (GAP-2987; ASM-4921)) | `/api/recovery/partner/v1` | S9 rwb-partner | The licence expiry, `kyc_status`, `panel_status` and buyer class; faked |
| The panel suspension request (operation name Not specified in the source documents (GAP-2987; ASM-4921)) | `/api/recovery/partner/v1` | S9 rwb-partner | The removal of the buyer from the panel with the reason and the rule reference, and the applied state in the answer; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state, the case reference and the lot link; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2987; ASM-4920)) | rwb-case (P3) | P3 rwb-case | The move `BACK_TO_CASE_LIST` or `BUYER_PENDING_KYC` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The authorise call and the capability area read (operation name Not specified in the source documents (GAP-2987; ASM-4920)) | `/api/recovery/access/v1` | P4 rwb-access | The capability areas "Debt sale" and "Partner portal", the right of the caller and the scope of its own lot; faked |
| The rule package in force (read) | `/api/recovery/decision/v1` | P7 rwb-decision | The Debt sale package at its version with R-DS-14, R-DS-16, R-DS-40 and R-DS-41, and its 10-working-day window; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The six rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-2987 with ASM-4920.

#### 12.3 Events published

None. Architecture v5 slide 19 OUT gives rwb-debtsale the topic `rwb.debtsale.events.v1` with `LotAwarded` (event 23, consumers rwb-case and rwb-payment) and `AccountsTransferred` (consumers rwb-case and rwb-reporting). `LotAwarded` is RWB-S6-E6005-APP's and `AccountsTransferred` is RWB-S6-E6007-APP's; this step produces neither, so the baseline declares no event of its own, no outbox row and no producer, and the absence test of AC6 fails a build that adds one.

#### 12.4 Events consumed

None. Architecture v5 slide 19 IN gives rwb-debtsale the event `ProceedsMatched` (event 25), which belongs to RWB-S6-E6011-APP, and no event of the module carries a breach report, a piece of evidence or a window expiry. This baseline therefore declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step, and the absence test of AC6 fails a build that adds one.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per lot, the child of `CaseWorkflow` on rwb-case (P3), a saga with pivot = transfer; started on the monthly sale cycle opening or a residual from disposal (R-DS-01); workflow ID form Not specified in the source documents (CG-ALL-10511); duplicate-start policy Not specified in the source documents (CG-ALL-10511) | `rwb-debtsale` | The stage that hosts the remediation branch and its durable window; its signals and its outcome for the parent are declared, not built |
| `assessRemediation` | Activity, the R-DS-40 outcome | `rwb-debtsale` | The case, the lot and the evidence in; the rule ID with its version, the record and the `BUYER_PENDING_KYC` answer out |
| `barBuyer` | Activity, the R-DS-41 outcome | `rwb-debtsale` | The case, the lot and the buyer in; the record, the panel request, the lot release and the `BACK_TO_CASE_LIST` answer out |

No child workflow for the case and none for the money exists in this service. The two activity names are a target design choice and the trigger is read as the window timer and the breach report for a lot, because the FSD declares no background event for the feature (FSD S6 A2.7.4.4). No activity is registered by this story, the qualification step that receives the re-opened check is RWB-S6-E6002-APP's, and the re-offer of the lot is the award story's.

#### 12.6 Schedules

None. The window is a durable workflow timer inside `DebtSaleWorkflow`; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table, and no Job of Architecture v5 slide 44 is owned or moved here (ASM-4923).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot, its buyer reference, its buyer class and its status; the three columns the release writes |
| debt_sale_account | S6 (`rwb_debtsale`) | The account set of the lot the release returns to the case list; read only by this step |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the repeated timer fire, breach report or answer and the answer it holds |
| outbox_event | PLT library, created in `rwb_debtsale` | The library object the service's sibling stories relay their events through; this step declares no row |

`partner` and `partner_user` (S9), `recovery_case` and `timer` (P3), `role` and `permission` (P4), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `proceeds` (P8) and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-partner panel and buyer fake | The organisation `PTR-2026-000031` with an expired licence and the panel status suspended, with a licence in date and the panel status active, with no evidence inside the window and with evidence inside it; a refused suspension; no answer beyond 2 s | AC2, AC3, AC6 |
| rwb-case state and move fake | The states `DATA_ROOM_OPEN`, `BUYER_PENDING_KYC`, `BUYER_REJECTED` and `BACK_TO_CASE_LIST` of case `RC-2026-000842`; an accepted move and a refused move for each of the two move names | AC4, AC6 |
| rwb-access authorise fake | The capability areas "Debt sale" and "Partner portal" with their rights for the TSD S6 T6.1 roles; a caller without the right | AC5, AC6 |
| rwb-decision rule-package fake | The Debt sale package at its version in force with R-DS-14, R-DS-16, R-DS-40 and R-DS-41 and the 10-working-day window | AC5, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC6 |
| Temporal test server with time skipping | The window advanced without waiting, and a window that has not ended | AC5, AC6 |
| gateway-bff composite route fake | The merged SCR-26 Award and PRT-05 Data room answer for lot `LOT-2026-000042` and case `RC-2026-000842`, carrying the bar element once | AC1, AC6 |
| Award re-offer consumer fake | The lot status read by R-DS-28 after a release, with the placeholder value recorded | AC2, AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-partner panel read and suspension request, the rwb-case move answer and the rwb-access authorise call are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2987; ASM-4921).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 6 consumed | The rwb-partner panel read and suspension request, the rwb-case state read and move answer, the rwb-access authorise call and the rwb-decision package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `LotAwarded` and `AccountsTransferred` are sibling stories' and `ProceedsMatched` is the remittance story's |
| Temporal | 1 workflow and 2 activities declared, 0 registered | `DebtSaleWorkflow` with `assessRemediation` and `barBuyer` on `rwb-debtsale`, and one durable timer; no Schedule |
| File | None | No file is read, built or delivered here; the evidence is the partner's and the sale documents are rwb-document's |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no lot, no case, no partner record and no rule package. What it publishes is one OpenAPI 3.1 fragment, nine contract tables, eight fakes and five new contract tests.

**Deliverables.** The additive fragment `openapi/rwb-debtsale-v1.yaml` for the bar element, the `Release`, `PanelRequest` and `BarElement` schemas, the vocabulary of the four lists and of the four route states as published enumerations, the contract README rows for the six consumed rows and their placeholders, and the eight mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule the element describes: the record, the panel request and the lot release commit together or not at all. DP-13 moves the base and nothing else. DP-19 is behind SCR-26 Award and the data room, whose screen model is the edge contract's.

**Dependencies the table adds and the plan does not hold.** The pattern table adds the two H rows the plan already carries for this key, `RWB-PLT-E1027-CON` and `RWB-PLT-N001-CON`. It leaves out the six consumed rows, which are C dependencies in fact and not in the metadata, and the DP-08 guard, which the step uses and the pattern set does not carry (GAP-2987; ASM-4920).

**Build steps**

1. Write the bar element and the answer shape of AC1, with the no-provided-operation record, and validate the additive rule in the pipeline.
2. Write the `Release` and `PanelRequest` elements, their required flags and the four lists of AC2, with the placeholder on the release value and the panel vocabulary.
3. Record the two rwb-partner rows of AC3 with their owner, budget and placeholders.
4. Record the rwb-case rows of AC4, the two move names and the state vocabulary.
5. Record the window element, the rwb-decision package and the rwb-access rights of AC5.
6. Record the decision-record element of AC6 and validate it against the library schema.
7. Publish the eight fakes of AC6 and the drift test.
8. Record the naming baseline, the boundary and the absences of AC6, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI fragment validates in the pipeline, the five contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the award story's re-offer, SCR-26 Award, the data room and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | Carried from the legacy message set of this key. It names an open deviation on an account, which is the eligibility story's, so no path of this step raises it | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role or the partner identity lacks the Debt sale or the Partner portal right the surface declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the lot row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE data product of the case is stale after a late or failed batch (VR-S6-007-1); the check is the owner's and this service holds no ACE batch status read | {product} is from {date}. Today's load has not arrived. |

The five message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged, except MSG-P1-001, whose text is copied from the Error and Message Standard v4; no message is reworded and no new one is added.

### 15. Screens and states

The contract serves SCR-26 Award in its open, closed, awarded and transferred states and PRT-05 Data room in its data room, bid and qualified-buyer states, all read only, through the gateway-bff composite route (DP-19). The route calls rwb-debtsale for the lot and the bar element, rwb-case for the case and its route state and rwb-partner for the buyer organisation; this baseline fixes the bar element only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The states this baseline names are `BUYER_PENDING_KYC`, `BUYER_REJECTED` and `BACK_TO_CASE_LIST` on the case and the release value of the lot status, which carries the placeholder (GAP-2987; ASM-4924). The refusal, not-recorded and stale-data states the app story shows read the messages of section 14.

SCR-26 Award has four screen states that this story names and the contract does not carry: the empty state, the loading state, the error state and the no-access state. The messages and field lists of these four states are Not specified in the source documents (CG-ALL-10516); they belong to RWB-PLT-N001-CON, the edge story that owns the composite route. The empty, loading, error and no-access states of SCR-26 are not in Screen Specifications v1: Not specified in the source documents (CG-ALL-10516).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-003-01 | AC1, AC2 | Contract | Lot `LOT-2026-000042` and buyer `PTR-2026-000031`; the contract half answers the bar element, the release element and the lists |
| TC-E6-003-02 | AC4 | Contract | Case `RC-2026-000842` at `BUYER_REJECTED`; the contract half answers the `BACK_TO_CASE_LIST` move shape and the state vocabulary |
| TC-E6-003-03 | AC4 | Contract | Case `RC-2026-000842` at `DATA_ROOM_OPEN`; the contract half answers the `BUYER_PENDING_KYC` move shape and the re-opened path |
| TC-E6-003-04 | AC6 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the decision-record element |
| TC-E6-003-05 | AC5 | Contract | RW-HEADASL holds RA and PT-BUYER holds RU scoped; the contract half answers the rights of the two capability areas |
| TC-E6-003-06 | AC5, AC6 | Contract | A window advanced and a window not ended under time skipping; the contract half answers the timer element and the absence tests |
| TC-S6-E6003-CON-01 | AC1, AC2 | Contract | The fragment validates; the bar and release elements, the seven error answers and the no-provided-operation record are present |
| TC-S6-E6003-CON-02 | AC2, AC3 | Contract | The `Release` and `PanelRequest` elements validate with their properties, required flags and the four closed lists |
| TC-S6-E6003-CON-03 | AC3, AC4 | Contract | The two rwb-partner rows and the two rwb-case rows with their placeholders and move names; the no-`partner` and no-`recovery_case` boundary |
| TC-S6-E6003-CON-04 | AC5, AC6 | Contract | The window, the rwb-decision and rwb-access rows, the eight fakes and the drift test; the absence of an event, a second topic and a Schedule |
| TC-S6-E6003-CON-05 | §12.7 tables (ASM-3438) | Contract | The five tables of §12.7 with their owners and contracted uses; no foreign key leaves the schema (DP-01) |
| TC-S6-E6003-CON-06 | AC7, BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13 | Contract | Each rule row of §8 checked against the contract: the element, the answer shape or the absence it names |

The six legacy cases are the legacy cases of RWB-E6-003 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S6-E6003-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The four cases `TC-S6-E6003-CON-01` to `-04` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 4 harness and none is written here.

### 17. Guardrails

- No business value in the contract: the 10-working-day window, the licence and panel conditions, the lists and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: the buyer is a partner organisation and no name, identity number, date of birth, address or contact value is declared; every example is synthetic.
- The panel and the evidence stay with rwb-partner and the case with rwb-case: the document declares no `partner` property, no `recovery_case` property and no case row write (BR3, BR4).
- The money stays with rwb-payment and the ledger with rwb-decision: the document declares no posting, no balance and no `decision_log_entry` column.
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13).
- No operation of a sibling is claimed: API-S6-003 and API-S6-004 are named as the surfaces the step runs behind, never as provided here (GAP-2987; ASM-4922).
- No retired element is reintroduced: the absence tests fail a build that declares a published or consumed event, a second topic, a Schedule, a Quartz row or a shared job table (ASM-4923).
- The error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S6-005 | A buyer who fails the check is given a remediation window and is removed from the panel if it is not met; the contract fixes the element, the rows, the window and the lists on which the bar is built (FSD S6 requirements served); the split plan carries no requirement id for this slice (GAP-2987; ASM-4920) | The bar element, the `Release` and `PanelRequest` elements, the window and the six consumed rows | TC-E6-003-01, TC-S6-E6003-CON-01, TC-S6-E6003-CON-02, TC-S6-E6003-CON-04 |
| REQ-S6-004 | Buyers pass a know your customer, licensing and eligibility check before they bid; the contract fixes the state and move vocabulary of the window that check opens | The four route states and the two move names | TC-E6-003-02, TC-E6-003-03, TC-S6-E6003-CON-03 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The recorded absence of an event of this step and the library object the siblings use | TC-S6-E6003-CON-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The six consumed rows with their budget and breaker | TC-S6-E6003-CON-01, TC-S6-E6003-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element written before the lot changes | TC-E6-003-04, TC-S6-E6003-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-003, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by RWB-S6-E6003-APP; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the four new contract cases TC-S6-E6003-CON-01 to -04 |
| Feature and screens | FEAT-DBS-07 Bar a buyer that fails qualification, SCR-26 Award and PRT-05 Data room |
| Rules | R-DS-14, R-DS-16, R-DS-40 and R-DS-41, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (outbox and CloudEvents), ADR-020 (contract-first REST), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the element, the window, the evaluation of R-DS-40 and R-DS-41, the record, the panel request, the lot release and the two moves: RWB-S6-E6003-APP.
- The award operation API-S6-003, its `DecisionLogEntry` answer and the re-offer to the next qualified bidder under R-DS-28: RWB-S6-E6005-APP (GAP-2987; ASM-4924).
- The data room read API-S6-004 and its `DataRoom` answer: RWB-S6-E5026-APP.
- The bid submission operation API-S6-005 and the bidding window: the take-bids story of this service.
- The qualification of a buyer, R-DS-14, R-DS-15, R-DS-16 and R-DS-18: RWB-S6-E6002-APP, whose answers open this window.
- The buyer panel, its `panel_status` values, the partner users and the evidence: rwb-partner (S9) (GAP-2987; ASM-4921).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose state and move answer this baseline declares as consumed and faked.
- The capability areas, the rights and the scope rows, and the authorise call: rwb-access (P4).
- The authoring, testing, approval and versioning of the Debt sale package and of R-DS-14, R-DS-16, R-DS-40 and R-DS-41: rwb-decision (P7).
- The sale agreement and the customer notices: rwb-document (P5) and rwb-comms (P6).
- The gateway-bff composite route and the screen field list of SCR-26 and PRT-05: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
