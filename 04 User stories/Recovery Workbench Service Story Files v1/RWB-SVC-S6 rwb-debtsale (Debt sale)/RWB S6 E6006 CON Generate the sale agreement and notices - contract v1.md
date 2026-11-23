# RWB-S6-E6006-CON Generate the sale agreement and notices - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E6006-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the agreement-and-notices step of rwb-debtsale, split from RWB-E6-006. It fixes the `SaleAgreement` and `SaleNotice` elements, the award-time answer of the lot on base `/api/recovery/debtsale/v1` (DP-13), the closed lists, the consumed rwb-document, rwb-comms, rwb-source-data, rwb-case and rwb-decision rows with their placeholders, the decision-record element with its references (DP-03), the rights, the fakes and the absence tests. The award operation API-S6-003 is RWB-S6-E6005-APP's and is declared here as not provided; the plan's C row is None although the step consumes five services, and no S6 extract exists in the extract folder (GAP-2996, -2, -7; ASM-4943, -2, -7). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the agreement-and-notices step of rwb-debtsale — the `SaleAgreement` and `SaleNotice` elements, the award-time answer of the lot, the closed lists, the consumed rwb-document, rwb-comms, rwb-source-data, rwb-case and rwb-decision rows, the decision-record element with its references, the rights, the tables and the fakes**, so that **the app story, the award screen and the wave 4 harness build against one fixed, testable contract on Day 1 and an agreement field, a notice field, a list value, a consumed shape or an answer can never drift between rwb-debtsale, rwb-document, rwb-comms, rwb-source-data, rwb-case and rwb-decision without a failing build**.

The baseline is deliberately narrow: it declares no operation of this service, describes the two elements this step produces through their owners, fixes the award-time answer of the lot that an existing story owns, and declares the five boundaries the step crosses.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy agreement and notices of RWB-E6-006 crossed five boundaries at once — the customer data of an ACE view, the document of the case, a notice record, the decision log and the case state — all inside one process and one `recovery` schema. The target splits them: rwb-document owns the agreement, its template and its custody; rwb-comms owns the notices, the conduct check and the WIN despatch; rwb-source-data owns the customer fact; rwb-case owns the case and its route states; rwb-decision owns the rule package and the ledger; rwb-debtsale owns the awarded lot and the decision record. Each boundary is now a contract another team builds against, so each has to be fixed before the app story starts: the `SaleAgreement` and `SaleNotice` elements and their lists, the award-time fields of the lot, the consumed document, notice, customer, case and package rows, the record of the decision with its references, and the rights.

The baseline also fixes the naming that the checks require: schema `rwb_debtsale`, login `rwb_debtsale`, base `/api/recovery/debtsale/v1`, topic `rwb.debtsale.events.v1` with its retry and `.dlt` topics, task queue `rwb-debtsale` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.debtsale` (Template and Rules §R4; Architecture v5 slide 42 notes). It records that rwb-debtsale holds no grant on `rwb_document`, `rwb_comms`, `rwb_source_data`, `rwb_case` or `rwb_decision`, and no `v_ace_*` grant, so all six are consumed on their owners' contracts only.

Four points are carried as gaps and assumptions rather than decided quietly: the plan's C row is None while the step consumes five services and five of the consumed operations have no published name (GAP-2996), the legacy endpoint row of the award belongs to RWB-S6-E6005-APP while the award effect is this step's (GAP-2997), the lot carries no column for the agreement or notice references (GAP-2998), and the addressee the notices need is the ACE customer fact that only rwb-source-data may read (GAP-2999).

The wave and the date are the plan's and the legacy epic's: this key is EP06 and therefore wave 4 with release 30 April 2027, while rwb-debtsale is created in wave 3, so one service delivers in two waves and two releases and the date is copied unchanged and marked tentative (GAP-3001; ASM-4948).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `debt_sale_lot` and `debt_sale_account` are S6's, `document` is P5's, `notice` is P6's, `recovery_case` is P3's, `rule_row` and `decision_log_entry` are P7's, and every `v_ace_*` view is P1's. This document never declares another service's table or operation as its own.
- The rwb-document generation contract, the rwb-comms notice contract, the rwb-source-data customer read, the rwb-case state read and move answer and the rwb-decision package read are published with their fakes; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-2996; ASM-4943).
- The DS rule package and its row R-DS-23, the 54 percent cap, the notice types and the templates are governed in rwb-decision, rwb-comms and rwb-document; this baseline names them and declares none of them.
- The `debt_sale_lot` and `debt_sale_account` tables and their columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- The `SaleAgreement` and `SaleNotice` elements have no operation of this service to be declared on; they ride on the answers of rwb-document and rwb-comms and on the award-time answer of the lot, whose shape is RWB-S6-E6001-CON's and is referenced, not redefined (GAP-2997; ASM-4944).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the additive fragment of the OpenAPI 3.1 document of rwb-debtsale for this step: the two elements, the award-time properties they reference on the lot answer, and the error envelope of the read they are shown on.
2. Fix the `SaleAgreement` element: the lot and case references, the buyer reference, the signing date, the template reference and version, the document reference and the sealing state, and the absence of any customer property.
3. Fix the `SaleNotice` element: the account and case references, the notice type against its list, the template reference and version, the document reference, the `sent_date`, the `barcode` and the delivery state, with the addressee named as consumed and never echoed.
4. Fix the award-time properties of the lot answer: `signing_date` and `status` against `LOV-LOT-STATUS`, as the reference to the shape RWB-S6-E6001-CON baselines.
5. Fix the consumed rows: the rwb-document generation, the rwb-comms notice issue, the rwb-source-data addressee read, the rwb-case state read and move answer, and the rwb-decision package read, each with the placeholder where no name is published.
6. Record the decision-record element of DP-03, written before the lot row changes, carrying the agreement and notice references.
7. Publish the contract tables of section 12, the rights of the read and the fakes of 12.8.
8. Add the contract tests: schema validation, the additive rule, the vocabulary, the element shapes, the no-addressee rule, the error envelope, the rights, the drift between a fake and the document, and the absence of a provided operation, of an event and of a foreign table.
9. Tag the baseline and hand it to RWB-S6-E6006-APP, the award screen and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body or a request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC7 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list or a name the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC4 |
| X5 | A value outside `LOV-LOT-STATUS`, `LOV-SEGMENT`, `LOV-BUYER-CLASS`, `LOV-PUTBACK` or the notice-type list appears in the document or in an example | The vocabulary test fails the build | None | AC2 |
| X6 | An element echoes a customer name, address, contact value or identity number | The no-personal-data test fails the build and the review refuses the baseline | None | AC2, AC6 |
| X7 | The document declares another service's operation as provided, a `document` property, a `notice` property or a `recovery_case` property | The review fails the baseline; the boundary test fails the build | None | AC1, AC7 |
| X8 | The document declares a published or consumed event, a second topic, a Schedule or a Quartz row | The absence test fails the build | None | AC7 |
| X9 | The rights of the read are not the ones TSD S6 T-A.1 and T6.1 declare | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner contracts of rwb-document, rwb-comms, rwb-source-data, rwb-case and rwb-decision only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the lists, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S6-E6006-APP, the award screen and the wave 4 harness on Day 1, and the rwb-document, rwb-comms, rwb-source-data, rwb-case and rwb-decision teams on the same day |
| Estimable | One OpenAPI fragment, nine contract tables, eight fakes and six new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the agreement-and-notices step of rwb-debtsale

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of debt_sale_lot and debt_sale_account is S6, of document is P5, of notice is P6, of recovery_case is P3 and of rule_row is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The baseline declares no operation of its own and records the award row of its sibling (new, D-RCV-60)
    Given the OpenAPI 3.1 fragment of rwb-debtsale for this step is published with this change
    When it is validated against the OpenAPI 3.1 schema and compared with TSD S6 T-A.1
    Then it validates with no error and is additive within major version 1
    Then it declares no operation as provided, and names API-S6-001, API-S6-002, API-S6-003, API-S6-004 and API-S6-005 as the five operations of the module with their owners
    Then it records that the award operation of the legacy Endpoints table is API-S6-003 on the base /api/recovery/debtsale/v1, that it is RWB-S6-E6005-APP's and that this step provides none
    Then the award-time answer the elements are shown on is the lot read API-S6-002 on base /api/recovery/debtsale/v1, referenced from RWB-S6-E6001-CON and not redefined here
    Then the answers 400, 401, 403, 404 and 503 of that read are declared with one envelope and one message ID per condition (GAP-2997; ASM-4944)

  Scenario: AC2 The SaleAgreement and SaleNotice elements and the closed lists are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S6 T3.1 and T3.2, FSD S6 A2.10 and the legacy Data table
    Then the SaleAgreement element declares the lot reference, the case reference, the buyer reference, the signing date, the template reference and version, the document reference and the sealing state, and declares no customer property
    Then the SaleNotice element declares the account and case references, the notice type against the notice-type list, the template reference and version, the document reference, the sent date, the barcode and the delivery state, and declares no addressee property
    Then the lot reference is declared against DF-SAL-020, the signing date against DF-SAL-027, the lot status against DF-SAL-030 with the values BUILDING, OFFERED, AWARDED, TRANSFERRED and CLOSED of LOV-LOT-STATUS, and the account reference against DF-SAL-032 of debt_sale_account
    Then the notice fields are declared from the legacy notice row DF-LEG-015 to DF-LEG-023 with their owner P6, and the notice types and the templates are declared as reference data of rwb-comms and rwb-document at their version, with the list values Not specified in the source documents (GAP-2999; ASM-4946)
    Then segment, buyer class and put-back status are declared against LOV-SEGMENT, LOV-BUYER-CLASS and LOV-PUTBACK with the values of TSD S6 T3.2
    Then the no-personal-data test refuses any customer name, address, contact value or identity number in an element, an example or a fake

  Scenario: AC3 The consumed document and comms rows are declared with their placeholders (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with Architecture v5 slide 41 and the Ownership Map rows of P5 and P6
    Then the agreement generation is declared as consumed from P5 rwb-document on the base /api/recovery/document/v1 with the template in force, the merged facts and the sealed document reference, and its operation name is Not specified in the source documents (GAP-2996; ASM-4943)
    Then the notice issue is declared as consumed from P6 rwb-comms on the base /api/recovery/comms/v1 with the notice type, the template and its version, the addressee and the issued notice with its sent date and barcode, and its operation name is Not specified in the source documents (GAP-2996; ASM-4943)
    Then the document element, the notice element, the template, the template version and the notice type are recorded as P5's, P6's and reference data, and no document table, notice table, template text or conduct rule is declared as this service's
    Then each row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The consumed customer, case and package rows are declared (new, D-RCV-60)
    Given the consumed rows of AC3 and the boundary of the baseline
    When they are compared with the Ownership Map rows of P1, P3 and P7
    Then the addressee fact is declared as consumed from P1 rwb-source-data with its as-of date and the masking policy in force, its operation name is Not specified in the source documents (GAP-2996; ASM-4943), and the baseline records that this service holds no v_ace_* grant and reads the view v_ace_customer named by the legacy Data table nowhere (GAP-2999; ASM-4946)
    Then the case state read is declared as consumed from P3 rwb-case on the GET /cases/{caseId} family with the states AWARD_PENDING, LOT_AWARDED and SETTLEMENT_PENDING, and the case-move answer with the move LOT_AWARDED and the rule ID with its version, its operation name being Not specified in the source documents (GAP-2996; ASM-4943)
    Then the DS rule package read is declared as consumed from P7 rwb-decision with R-DS-23, the 54 percent cap, the notice types and the templates, and its operation name is Not specified in the source documents (GAP-2996; ASM-4943)
    Then the baseline declares no recovery_case property, no rule row, no ledger entry and no write of a case row from rwb-debtsale

  Scenario: AC5 The rights and the scope are fixed on the read and on the step (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S6 T6.1, T-A.1 and the legacy permission rows
    Then the read of the awarded lot declares Debt sale right R with the scope applied, RW-DEBTSALE holds CRUA, RW-PRODHEAD and RW-HEADASL hold RA and every other role of T6.1 holds R
    Then the baseline records that the legacy A right of RW-DEBTSALE, RW-PRODHEAD and RW-HEADASL belongs to the award operation API-S6-003 of RWB-S6-E6005-APP, and that this step runs unattended as the FSD states, with the debt sale officer as an also-user
    Then the baseline records that the partner identity of PT-BUYER and PT-RAMC reads its own award through the partner gateway and never a customer fact and never a notice
    Then a repeated confirmation describes no second effect and the read declares no Idempotency-Key (GAP-2997; ASM-4944)

  Scenario: AC6 The decision-record element and the fakes answer the document (new, D-RCV-60)
    Given the decision section and the fakes of the baseline
    When each is compared with the library schema and with the operation or the element it serves
    Then one decision record is declared per rule outcome with the case reference, the lot reference, the rule ID, the package version in force, the inputs reference, the agreement reference, the notice references, the outcome, the case move and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before the lot row changes, and a failed write leaves the lot unchanged with MSG-P7-003
    Then the baseline records that the lot has no column for the agreement or the notice references and that the references live in the record and in the custody of their owners (GAP-2998; ASM-4945)
    Then the rwb-document fake answers a sealed agreement with a reference, a run with no reference and a failed run, the rwb-comms fake answers an issued notice set, a conduct stop and a run with no reference, and the rwb-source-data fake answers a masked addressee, an absent one and a stale one
    Then the rwb-case fake answers the three route states and an accepted and a refused move, the rwb-decision fake answers the package at its version, and the rwb-debtsale fake answers the awarded lot with its signing date, its status and its references
    Then the drift test compares every fake with the document and fails the build on any difference, and no fake carries a person name or an unmasked addressee

  Scenario: AC7 The naming baseline and the boundary are fixed and no event is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_debtsale, the login is rwb_debtsale, the base is /api/recovery/debtsale/v1, the topic is rwb.debtsale.events.v1, the queue is rwb-debtsale and the Java package is th.co.scb.ace.workbench.recovery.debtsale
    Then the tables named as owned are debt_sale_lot and debt_sale_account and the library objects decision_record, idempotency_key and outbox_event, and document, notice, recovery_case, timer, approval, decision_log_entry, rule_row, partner, proceeds and every v_ace_* view are named as other owners' and are consumed only through their contracts
    Then the document declares no published event and no consumed event, and names LotAwarded as the award story's, AccountsTransferred as the transfer story's and ProceedsMatched as the settlement story's
    Then the document declares no Schedule, no Quartz row and no shared job table, and no file of its own, the WIN daily letters file of INT-14 being rwb-comms's and rwb-integration's (GAP-3000; ASM-4947)
    Then the document records that the plan's C row is None although the step consumes five services, and that no S6 extract exists in the extract folder so FSD S6 v3 and TSD S6 v2 stand in (GAP-2996, GAP-3002; ASM-4943, ASM-4949)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S6-E6006-APP and they copy no criterion of the legacy story, whose three criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The awarded lot and its award-time columns are rwb-debtsale's, and the contract declares `signing_date` and `status` on the lot answer only, by reference to the shape RWB-S6-E6001-CON baselines | Architecture v5 slide 41; TSD S6 T3.1; Ownership Map `debt_sale_lot` |
| BR2 | The decision record is declared as an element written before the lot row changes, through the local library on the shared topic, carrying the agreement and notice references; a failed write changes nothing | DP-03; TSD S6 T2; legacy RWB-E6-006 AC1 and AC3 |
| BR3 | The agreement stays with rwb-document and the notices with rwb-comms: the contract declares both as consumed and declares no `document` property, no `notice` property, no template and no conduct rule | Architecture v5 slide 41 P5 and P6; GAP-2996 |
| BR4 | The addressee is consumed from rwb-source-data and is never echoed: the elements carry no customer property, and the read is one hop on that owner's contract (DP-05) | DP-05; Architecture v5 slides 29, 37 and 45; GAP-2999 |
| BR5 | The case move is answered and not written: the contract declares the state read and the move answer, and declares no `recovery_case` property | Ownership Map `recovery_case` owner P3; GAP-2996 |
| BR6 | The award operation and the price test stay with RWB-S6-E6005-APP: the contract declares no operation of this step and records the disposition of the legacy endpoint row | TSD S6 T-A.1 API-S6-003; GAP-2997 |
| BR7 | No event belongs to this step: the contract declares no published event and no consumed event | Architecture v5 slide 19 OUT and slide 43; GAP-2997 |
| BR8 | The vocabulary is closed: `LOV-LOT-STATUS`, `LOV-SEGMENT`, `LOV-BUYER-CLASS` and `LOV-PUTBACK` are published as enumerated values and no list value is a constant of the code; the notice-type list and the templates are reference data of their owners and are carried by reference | TSD S6 T3.2; FSD S6 BR-S6-010; GAP-2999 |
| BR9 | No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule version only, and no addressee value | Architecture v5 slide 42 notes; Template and Rules v1 §R7.2 (s17) |
| BR10 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own, and it declares no file of its own | DP-13, DP-14; Template and Rules §R4; GAP-3000 |
| BR11 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR12 | The document lists only operations owned by rwb-debtsale; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-11 |

### 9. State transitions

The lifecycle of this document, not of a lot:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two elements, the lot answer reference, the lists, the consumed rows, the rights and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the award screen, the wave 4 harness and the rwb-document, rwb-comms, rwb-source-data, rwb-case and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional notice delivery field | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a list value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC1, AC2 and AC7 fail: a provided operation, a `document` or `notice` property, an addressee property, an event or a Schedule | In review |

The route machine that the document describes is the app story's and rwb-case's: `AWARD_PENDING`, `LOT_AWARDED` and `SETTLEMENT_PENDING` are case route states, and `LOV-LOT-STATUS` is BUILDING, OFFERED, AWARDED, TRANSFERRED and CLOSED. This baseline fixes both vocabularies, declares no value for the agreement or the notices in the lot list, and moves no lot and no case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-debtsale | Owns the OpenAPI fragment and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes |
| Consuming teams (the app story, the award screen, the wave 4 harness and the owners of rwb-document, rwb-comms, rwb-source-data, rwb-case and rwb-decision) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field and no addressee value is declared in an answer, an element, an example or a fake |

The per-service login behind the security scheme of the document is named "the rwb-debtsale login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Agreement element | `SaleAgreement`: the lot reference DF-SAL-020, the case reference, the buyer reference DF-SAL-025, the signing date DF-SAL-027, the template reference and version, the document reference and the sealing state; no customer property |
| Notice element | `SaleNotice`: the account reference DF-SAL-033, the case reference, the notice type, the template reference and version, the document reference, the sent date, the barcode and the delivery state; no addressee property |
| Lot award-time fields | `signing_date` DF-SAL-027 and `status` DF-SAL-030 against `LOV-LOT-STATUS`; required flags and types are those of TSD S6 T3.1 and the answer shape is RWB-S6-E6001-CON's |
| Lists | `LOV-LOT-STATUS`, `LOV-SEGMENT`, `LOV-BUYER-CLASS` and `LOV-PUTBACK` published as enumerations and read as reference data at their version; the notice-type list and the template set are reference data of P6 and P5, carried by reference with the values Not specified in the source documents (GAP-2999; ASM-4946) |
| Legacy notice row | DF-LEG-015 to DF-LEG-023: id, case_id, document_id, notice_type, sent_date, barcode and 3 more, owned by P6 and consumed, never declared as this service's |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, with the agreement and notice references, written before the lot row changes (DP-03) |
| Consumed shapes | The document generation of P5, the notice issue of P6, the customer fact of P1, the case state and move of P3 and the package of P7, each declared as consumed and faked |
| Not declared here | `document` (P5), `notice` (P6), `recovery_case` and `timer` (P3), `approval`, `decision_log_entry` and `rule_row` (P7), `partner` (S9), `proceeds` (P8), every `v_ace_*` view (P1), and the award operation API-S6-003 (RWB-S6-E6005-APP) |
| Consumed fields with no source | The operation names of the document generation, the notice issue, the customer read, the case-move answer and the package read, and the notice-type and template values: Not specified in the source documents (GAP-2996, GAP-2999; ASM-4943, ASM-4946) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC2 and the no-addressee rule of BR4 and BR9. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

None of its own. TSD S6 appendix T-A publishes five operations for the module — API-S6-001 `POST /debt-sale-lots`, API-S6-002 `GET /debt-sale-lots/{lotId}`, API-S6-003 `POST /debt-sale-lots/{lotId}/award`, API-S6-004 `GET /partner/data-room/{lotId}` and API-S6-005 `POST /partner/data-room/{lotId}/bids` — and none of them is an agreement or a notice operation. The single endpoint row of the legacy RWB-E6-006 Endpoints table is API-S6-003; it is RWB-S6-E6005-APP's, it carries the A right, and this baseline records the disposition instead of claiming it. The elements this baseline fixes ride on the award-time answer of the lot read API-S6-002, whose shape is RWB-S6-E6001-CON's baseline and is referenced, not redefined; the absence is recorded as GAP-2997 with ASM-4944.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The generation of the sale agreement from the approved template (operation name Not specified in the source documents (GAP-2996; ASM-4943)) | `/api/recovery/document/v1` | P5 rwb-document | The template in force, the sealed agreement and its reference; faked |
| The issue of the customer notices (operation name Not specified in the source documents (GAP-2996; ASM-4943)) | `/api/recovery/comms/v1` | P6 rwb-comms | The notice type, the template and its version, the addressee, and the issued notice with its sent date and barcode; the conduct check and the WIN despatch sit behind it; faked |
| The masked addressee fact of a sold account (operation name Not specified in the source documents (GAP-2996; ASM-4943)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The addressee of the notice and its as-of date, masked under the policy in force; faked (DP-05) |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state, the case reference and the stage the lot belongs to; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2996; ASM-4943)) | rwb-case (P3) | P3 rwb-case | The move `LOT_AWARDED` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The read of the DS rule package version in force (operation name Not specified in the source documents (GAP-2996; ASM-4943)) | `/api/recovery/decision/v1` | P7 rwb-decision | The package version and the rows of R-DS-23 with the cap, the notice types and the templates; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The six rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-2996 with ASM-4943.

#### 12.3 Events published

None. Architecture v5 slide 19 OUT gives rwb-debtsale exactly two events, `LotAwarded` and `AccountsTransferred`; `LotAwarded` is RWB-S6-E6005-APP's and `AccountsTransferred` is RWB-S6-E6007-APP's. This baseline therefore declares no producer, no envelope and no outbox row of its own, and the absence test of AC7 fails a build that adds one.

#### 12.4 Events consumed

None. Architecture v5 slide 19 IN gives rwb-debtsale `ProceedsMatched`, which is the settlement fact of RWB-S6-E6011-APP's step, and the award confirmation of this step is a stage signal and not an event. This baseline declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per case per stage, the saga child of `CaseWorkflow`, pivot = transfer | `rwb-debtsale` in namespace `rwb-recovery` | The stage that hosts the R-DS-23 branch; its input, its signals and its outcome for the parent are declared, not built |
| The R-DS-23 branch of `DebtSaleWorkflow` | Workflow branch | `rwb-debtsale` | The step from the confirmed award to `LOT_AWARDED`: the confirmation in, the agreement and the notices requested, the record and the lot columns written, the stage outcome out |
| The document run of rwb-document | Activity on the owner's queue, owned and run by P5 | `rwb-document` (P5) | The template, the merged facts and the sealed document; started by this story, owned by P5 |
| `recordAwardAndIssueNotices` | Activity, the one step | `rwb-debtsale` | The case, the lot, the award and the two owner answers in; the rule ID with its package version, the two lot columns, the decision record and the case move out |

No child workflow for the case and none for the money exists in this service, and neither the agreement nor the notice is produced here: they are the owners' runs (BR3). The activity name is a target design choice and the trigger is read as the award confirmation for a case in `AWARD_PENDING`, because the FSD declares no background event for the feature (FSD S6 A2.10.4.4). No activity is registered by this story.

#### 12.6 Schedules

None. The step runs from the award confirmation; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table, and no Job of Architecture v5 slide 44 is owned or moved here.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot, its signing date, its status and its accounts; the row the award-time answer reads |
| debt_sale_account | S6 (`rwb_debtsale`) | The sold accounts a notice is raised for; read only by this step |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked decision record of the rule outcome, with the agreement and notice references (DP-03) |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the repeated confirmation and the outcome it holds |
| outbox_event | PLT library, created in `rwb_debtsale` | Created in this schema by the library for the stories that publish; no row of it belongs to this step |

`document` (P5), `notice` (P6), `recovery_case` and `timer` (P3), `approval`, `decision_log_entry` and `rule_row` (P7), `partner` (S9), `proceeds` (P8) and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers or references of their owners, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-document agreement fake | The sealed agreement of lot `LOT-2027-000041` with its reference, its template and its version; a run with no reference; a failed run; no answer beyond 2 s | AC2, AC3, AC6 |
| rwb-comms notice fake | An issued notice set with its types, sent dates and barcodes; a notice stopped by the conduct check; a run with no reference; no answer beyond 2 s | AC2, AC3, AC6 |
| rwb-source-data addressee fake | A masked addressee with its as-of date; an absent addressee; a stale fact; no answer beyond 2 s; no answer carrying an unmasked identifier | AC4, AC6 |
| rwb-case state and move fake | The states `AWARD_PENDING`, `LOT_AWARDED` and `SETTLEMENT_PENDING` of case `RC-2027-000611`; an accepted and a refused `LOT_AWARDED` move | AC4, AC6 |
| rwb-decision rule-package fake | The DS package at its version in force with R-DS-23, the cap, the notice types and the templates | AC4, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC6 |
| rwb-debtsale lot fake | The awarded lot `LOT-2027-000041` with its signing date, its status, its references and its accounts | AC1, AC2, AC6 |
| gateway-bff composite route fake | The merged SCR-26 answer for lot `LOT-2027-000041`, carrying the two elements once | AC1, AC6 |

The fakes are test-only and are replaced by the real services in SIT. The unpublished names of the document, comms, customer, case-move and package operations are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2996; ASM-4943).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 6 consumed | The rwb-document generation, the rwb-comms notice issue, the rwb-source-data addressee read, the rwb-case state read and move answer and the rwb-decision package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `LotAwarded` is the award story's, `AccountsTransferred` the transfer story's and `ProceedsMatched` the settlement story's; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow, 1 branch, 1 activity and 1 run on the P5 queue declared, 0 registered | `DebtSaleWorkflow`, its R-DS-23 branch and `recordAwardAndIssueNotices` on `rwb-debtsale`, and the document run on `rwb-document`; no Schedule |
| File | None of its own | The WIN daily letters file of INT-14 is produced and handed over by rwb-comms and rwb-integration on the notice despatch; this service reads and writes no file (GAP-3000) |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no lot, no case, no document, no notice and no rule package. What it publishes is one OpenAPI 3.1 fragment, nine contract tables, the rights of the read and eight fakes.

**Deliverables.** The additive fragment `openapi/rwb-debtsale-v1.yaml` for the two elements, the `SaleAgreement` and `SaleNotice` elements, the vocabulary of the four lists as published enumerations, the contract README rows for the six consumed rows and their placeholders, and the eight WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the element the baseline declares before the lot row changes, on the shared `rwb.decision-record.v1`, carrying the references. DP-05 is the customer fact, which the baseline declares as consumed from rwb-source-data and never as a view read or an element property. DP-13 moves the base and nothing else. DP-19 is behind SCR-26, whose screen model is the edge contract's, and this baseline fixes the rwb-debtsale answer only. No other pattern is claimed: the document, the notices, the customer fact, the case state and the package are consumed contracts, so DP-09 and DP-16 stay off this table and their absence from the plan's rows is recorded in the registers (GAP-2996).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan's build list for this key already carries. The six consumed rows are C dependencies in fact and not in the metadata row, and the document run also adds a Temporal dependency on the P5 queue that no row expresses (GAP-2996; ASM-4943).

**Build steps**

1. Write the fragment and validate the additive rule and the no-provided-operation record of AC1, with API-S6-003 named as another story's.
2. Write the `SaleAgreement` and `SaleNotice` elements, their required flags, the four lists and the no-addressee rule of AC2, with the unstated notice-type and template values recorded.
3. Record the rwb-document and rwb-comms rows of AC3 with their owners, their budget and their placeholders.
4. Record the rwb-source-data, rwb-case and rwb-decision rows of AC4, with the no-view rule and the placeholder.
5. Record the rights, the award operation disposition and the scope of AC5.
6. Record the decision-record element with its references of AC6 and validate it against the library schema.
7. Publish the eight fakes of AC6 and the drift test.
8. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI fragment validates in the pipeline, the six contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the award screen and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | Carried from the legacy message set of this key. It names an open deviation on an account, which is the exclusion path of RWB-S6-E5023-APP, so no path of this step raises it | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation (VR-S6-010-1) | Enter {field}. |
| MSG-P1-001 | The customer data product behind a notice is stale, or carries no addressee for a sold account (VR-S6-010-1) | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P4-002 | The role lacks the Debt sale right the read declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the lot row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four legacy message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; MSG-P1-001 is the stale-data message of VR-S6-010-1, which the FSD carries for every feature of the module. MSG-S6-001 is carried because it is in the message set of this feature, and the check itself belongs to the exclusion story of this service. No message is reworded and no new one is added.

### 15. Screens and states

The contract serves SCR-26 Award in its open, closed, awarded and transferred states, read only, through the gateway-bff composite route (DP-19). The route calls rwb-debtsale for the lot, its signing date, its status and its references, rwb-case for the case and its route state, and rwb-document and rwb-comms for the agreement and the notices the references point at; this baseline fixes the rwb-debtsale answer only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The refusal, not-recorded and stale-customer-data states the app story shows read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-006-01 | AC1, AC2 | Contract | The confirmed award of lot `LOT-2027-000041` for case `RC-2027-000611`; the contract half answers the read, the two elements and their fields |
| TC-E6-006-02 | AC2, AC3 | Contract | The award confirmation on a case at `AWARD_PENDING`; the contract half answers the agreement and notice shapes and the `LOT_AWARDED` move shape |
| TC-E6-006-03 | AC6 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the record element with its references |
| TC-E6-006-04 | AC5 | Contract | A role without the Debt sale right; the contract half answers the 403 with MSG-P4-002 and the rights of the read |
| TC-E6-006-05 | AC6, AC7 | Contract | A forced record failure and a forbidden element; the contract half answers the record path and the absence tests |
| TC-S6-E6006-CON-01 | AC1 | Contract | The fragment validates; no provided operation, the five module operations named with their owners, and the award row recorded as the sibling's |
| TC-S6-E6006-CON-02 | AC2 | Contract | The two elements validate with their properties, the four lists and the notice-type list by reference; no customer and no addressee property |
| TC-S6-E6006-CON-03 | AC3, AC4 | Contract | The six consumed rows and their placeholders; the no-view rule; the no-`document`, no-`notice` and no-`recovery_case` boundary |
| TC-S6-E6006-CON-04 | AC5 | Contract | RW-DEBTSALE holds CRUA, RW-PRODHEAD and RW-HEADASL hold RA and every other role holds R; the A right is recorded as the award story's |
| TC-S6-E6006-CON-05 | AC6 | Contract | The eight fakes match the document, no fake carries a person value, and a drifted fake fails the build |
| TC-S6-E6006-CON-06 | AC7 | Contract | The naming baseline; the absence test for an event, a second topic, a Schedule, a Quartz row and a file |

The five legacy cases are the legacy cases of RWB-E6-006 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S6-E6006-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The six cases `TC-S6-E6006-CON-01` to `-06` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID; no `-ITG` copy is written here, and the cross-service journey of the key belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: the 54 percent cap, the 45-day target, the notice types, the templates and their versions, the lists and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule version only; the addressee is consumed and never echoed, and every example is synthetic.
- The agreement and the notices stay with their owners: the document declares no `document` property, no `notice` property, no template text and no conduct rule (BR3).
- The case stays with rwb-case and the package with rwb-decision: the document declares no `recovery_case` property, no ledger property and no rule row (BR5).
- The award operation and the price test stay with RWB-S6-E6005-APP: the document declares no operation of this step and records the disposition (BR6).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-debtsale; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence tests fail a build that declares an event, a second topic, a Schedule, a Quartz row, a shared job table or a file of this service's own.
- The error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S6-006 | The award of a lot is approved and recorded with the price achieved against the reserve (Must, E6; FSD S6 requirements served). It is the nearest requirement row: no FSD requirement names the agreement or the notices, and TSD S6 T8 carries no row for FEAT-DBS-10 (GAP-2998; ASM-4945) | The award-time fields of the lot answer, the two elements and the six consumed rows | TC-E6-006-01, TC-E6-006-02, TC-S6-E6006-CON-01, TC-S6-E6006-CON-02 |
| ADR-014 | Schema and login per service | `rwb_debtsale` and its own login | TC-S6-E6006-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The six consumed rows with their budget and breaker | TC-S6-E6006-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element with its references and the ledger entry of P7 | TC-S6-E6006-CON-05 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-006, disposition Split (rework) |
| Legacy criteria | AC1, AC2 and AC3 of the legacy story, owned word for word by RWB-S6-E6006-APP; this baseline copies none of them |
| Test cases | The five legacy cases as the contract half, and the six new contract cases TC-S6-E6006-CON-01 to -06 |
| Feature and screens | FEAT-DBS-10, SCR-26 Award |
| Rules | R-DS-23, with R-DS-19 as its predecessor and R-DS-24 as its successor, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |
| Source text | FSD S6 Debt sale v3 A2.10, TSD S6 Debt sale v2 T3, T4, T5 and Appendix T-A, Business Rules and Routing Logic v4, the legacy story master of Epics 3 to 8 v3 and the Feature List v4 rows FEAT-OCC-01, -02, -05 and -07 |

### 19. Out of scope

- The behaviour behind the elements, the evaluation of R-DS-23, the decision record, the two lot columns and the case-move answer: RWB-S6-E6006-APP.
- The award operation API-S6-003, the price test R-DS-19 and the `LotAwarded` event: RWB-S6-E6005-APP (GAP-2997).
- The agreement's template, its generation, its custody and its retention: rwb-document (P5).
- The notices, their templates, the conduct check, the WIN despatch and the proof of delivery: rwb-comms (P6) and the P2 INT-14 file (GAP-3000).
- The customer fact and its masking policy: rwb-source-data (P1) and rwb-access (P4) (DP-05).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3).
- The rule package, its versioning, the approval chain and the ledger: rwb-decision (P7).
- The lot build, the estimate and the reserve: RWB-S6-E5024-APP; the eligible-account selection: RWB-S6-E5023-APP; the data room and the bids: RWB-S6-E5026-APP.
- The settlement term, the data transfer, derecognition and the general ledger posting: RWB-S6-E6007-APP and RWB-S6-E6008-APP.
- The gateway-bff composite route and the screen field list of SCR-26: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
