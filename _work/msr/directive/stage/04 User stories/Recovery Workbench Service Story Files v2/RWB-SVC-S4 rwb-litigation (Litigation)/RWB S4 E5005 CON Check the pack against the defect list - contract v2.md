# RWB-S4-E5005-CON Check the pack against the defect list - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5005-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-005 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement (DOR-RWB-S4-E5005-CON-16) |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | `/api/recovery/litigation/v1` (v1) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the pack-defect check of rwb-litigation, split from RWB-E5-005. It fixes the two legal-action operations on `/api/recovery/litigation/v1` (DP-13), the pack element that carries the checklist version, the item states and the missing items, the outcome element and the case move, the `Idempotency-Key` rule and the error envelope, the consumed checklist and case-document reads of rwb-document (P5), the case answer of rwb-case and the decision-record element of DP-03. The defect list is read as the document checklist of FEAT-DCM-16 (GAP-2758; ASM-4588); the three consumed rows are class C in fact while the plan's C row is None (GAP-2758; ASM-4589); the element names, the activity name and the trigger have no source specification and are carried with the placeholder (GAP-2759; ASM-4592). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S4-E5005-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 8 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Not specified in the source documents (DOR-RWB-S4-E5005-CON-1)**, I want **the published contract baseline of the pack-defect check of rwb-litigation — the two legal-action operations on `/api/recovery/litigation/v1`, the pack element with the checklist version, the item states and the missing items, the outcome element, the case-move answer, the `Idempotency-Key` rule, the error envelope and the rights, the consumed checklist and document facts of rwb-document, the case answer of rwb-case, the decision-record element, the tables and the fakes**, so that **the app story, the screens and the tests of this legacy key build against one fixed, testable contract on Day 1 and a checklist version, an item state, a document type or an answer shape can never drift between rwb-litigation, rwb-document and rwb-case without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy step of RWB-E5-005 crossed three boundaries at once: an officer screen, a set of documents and a checklist, and a case state. The target splits them: the checklist per case type and the documents are rwb-document (P5) under FEAT-DCM-16 and its store, the case of record and its pack states stay with rwb-case (P3), and the legal action, the pack outcome and the decision stay with rwb-litigation (S4). Each boundary is now a contract that another team builds against, so each has to be fixed before the app story starts: the item states of the checklist answer, the missing-item list, the outcome element, the case answer and the record of the decision.

The baseline also fixes the naming that the checks require: schema `rwb_litigation`, base `/api/recovery/litigation/v1`, topic `rwb.litigation.events.v1` with retry and `.dlt` topics, task queue `rwb-litigation` and Java package `th.co.scb.ace.workbench.recovery.litigation` (Architecture v5 slide 41 notes). It records that rwb-litigation holds no `v_ace_*` grant and no grant on `rwb_document` or `rwb_case`, so no fact of the checklist, the documents or the case is read as a table and DP-05 is not in the pattern set of this key.

Three points are carried as the working read of an assumption rather than decided quietly: that the "known defect list" of the legacy story is the document checklist of FEAT-DCM-16, because that feature states that it is the source the pack checks read (FSD P5 A2.16, R-LIT-16 and R-LIT-17) although no source uses the two names as one (GAP-2758; ASM-4588); that neither story publishes or consumes an event, because DP-09 is not in the pattern set and the S4 IN row lists no document event (GAP-2759; ASM-4590); and that the element names, the activity name and the missing-item shape that no source fixes are this run's design and carry the placeholder (GAP-2759; ASM-4592).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `legal_action` and `hearing` are S4's, `document`, `document_checklist_item` and `case_document_check` are P5's, `recovery_case` is P3's, `rule_row` and `decision_log_entry` are P7's. This document never declares another service's operation as provided.
- The two consumed rwb-document operations are the published surface of their owner stories: `GET /cases/{caseId}/document-checklist` (API-P5-008) of RWB-P5-E1040-APP and `GET /cases/{caseId}/documents` (API-P5-002) of RWB-P5-E1026-APP. No P5 contract story carries either as a baseline, so both are class C dependencies of this key in fact while the row of this story is None, and the absence is recorded (GAP-2758; ASM-4589).
- The case answer of rwb-case is fixed here as a shape only; no source names a published operation that moves a case state on behalf of a stage, and the name is Not specified in the source documents (GAP-2758; ASM-4589).
- The LITIGATION rule package, its rule rows for R-LIT-16, R-LIT-17, R-LIT-18 and R-LIT-32 and its D7 approval limit are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The `legal_action` and `hearing` tables and their columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7), and the missing approval of the FSD, the TSD and the realigned story is recorded as an assumption of this run (GAP-2759; ASM-4593).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-litigation for this step: the two operations with their request and answer elements, the pack element, the outcome element, the rights and the six error responses.
2. Fix the pack element: the checklist version in force, the stage code, the items with their document type, label, required flag and presence, the missing items and the outcome of the last check, with no checklist row and no document row of the hub restated as a property of this service.
3. Fix the outcome element and the case answer: the rule ID, the package version, the missing item count, the decided-at time and the move `PACK_DEFECT_HOLD` or `PACK_ASSEMBLY`.
4. Fix the consumed checklist read and the consumed case document page of rwb-document, mark the fields the sources do not give with the placeholder and declare one paging rule.
5. Record the decision-record element of DP-03 on `rwb.decision-record.v1`, written before the case answer.
6. Record the closed vocabulary of the item state and the reuse of `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS`, and the rule that no value is a constant of the code.
7. Publish the contract tables of section 12 and the six contract fakes.
8. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a `v_ace_*` read and of a document, checklist or case write, and the drift between a fake and the document.
9. Tag the baseline and hand it to RWB-S4-E5005-APP, the screens and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body or a request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC5 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC6 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | The consumed checklist or document answer has a field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC2, AC6 |
| X5 | A value outside `LOV-LEGAL-TYPE`, `LOV-LEGAL-STATUS` or the item state appears in the document or in an example | The vocabulary test fails the build | None | AC1, AC5 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a checklist row, a document row or a `recovery_case` row | The review fails the baseline; the boundary test fails the build | None | AC6 |
| X7 | A POST is repeated with the same `Idempotency-Key` | The stored answer is returned and no second effect is described | None | AC5 |
| X8 | The rights of an operation are not the ones TSD S4 T-A.1 declares | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published app surfaces of rwb-document and rwb-case only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the operations, the lists, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S4-E5005-APP, the two screens and the wave 3 harness on Day 1, and the rwb-document and rwb-case teams on the same day |
| Estimable | One OpenAPI document, one AsyncAPI fragment, nine contract tables, six fakes and four new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the pack-defect check of rwb-litigation

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of legal_action and hearing is S4, of document and document_checklist_item is P5 and of recovery_case is P3
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The two legal-action operations and the pack element are declared (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-litigation is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /cases/{caseId}/legal-actions with the LegalAction answer of status 201 and GET /legal-actions/{legalActionId} with the LegalAction answer of status 200, both under the base /api/recovery/litigation/v1 and owned by rwb-litigation
    Then the LegalAction element carries a pack property with the checklist version, the stage code, the items and the missing items, and the outcome property with the rule ID, the package version, the missing item count and the decided-at time
    Then action_type is declared against LOV-LEGAL-TYPE and status against LOV-LEGAL-STATUS, and every other property of the element is copied from the baseline of the legal action and is not redefined here
    Then the document declares no checklist row, no document row and no case route-state property

  Scenario: AC2 The consumed checklist and case document facts of rwb-document are declared (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with API-P5-008 and API-P5-002 of rwb-document
    Then the checklist of a case type is declared as consumed from P5 rwb-document with the checklist version, the stage code, and each item with its document type, label, required flag and present count
    Then the documents of the case are declared as consumed from P5 rwb-document with the case reference, the page, the size and the total, and each document with its identifier, its document type and its stored date, and no field value and no content
    Then the field names of the two rows that no source gives are Not specified in the source documents (GAP-2759; ASM-4592) and the rows carry the placeholder
    Then every call on the two rows is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC3 The outcome element and the case-move answer are declared and the case row is never written here (new, D-RCV-60)
    Given the outcome and case boundary of the baseline
    When they are compared with rwb-case as the owner of recovery_case and of the route states
    Then the case move is declared as an answer to rwb-case with the move PACK_DEFECT_HOLD or PACK_ASSEMBLY, the rule ID, the package version, the missing item count and the decided-at time
    Then the document declares no recovery_case property, no route-state column and no write of a case row from rwb-litigation
    Then the states PACK_ASSEMBLY, PACK_DEFECT_HOLD, PACK_VERIFIED and FILING_REJECTED are named as the case of record's and are read from its answer only
    Then the operation name of a REST case-move call for another caller is Not specified in the source documents (GAP-2758; ASM-4589)

  Scenario: AC4 The decision-record element is declared and written before the case answer (new, D-RCV-60)
    Given the decision section of the baseline
    When it is compared with the local decision-record library of DP-03
    Then one decision record is declared per rule outcome with the case reference, the legal action reference, the rule ID, the package version in force, the checklist version, the inputs reference, the missing item count, the outcome and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before the case answer, and a failed write leaves the step unchanged with MSG-P7-003
    Then the document declares no event of its own for the record and no second topic for this capability
    Then the record carries IDs, codes, counts, dates and a rule version only

  Scenario: AC5 The Idempotency-Key rule, the error envelope and the rights are fixed (new, D-RCV-60)
    Given the error and access sections of the baseline
    When they are compared with TSD S4 T-A.1, T-A.2 and T6.1
    Then the operations answer 400 for a malformed request, 401, 403 with MSG-P4-002, 404, 409 on a closed or withdrawn action, 422 with MSG-GEN-001 and with MSG-S4-001 on a held pack, and 503 when a downstream does not answer, each with one envelope and one message ID per condition
    Then POST /cases/{caseId}/legal-actions declares Litigation right C and GET /legal-actions/{legalActionId} declares Litigation right R, each with the scope applied
    Then RW-LITOFF holds Litigation CRUA, RW-ENFORCE holds CRU, RW-LEGAL, RW-PRODHEAD and RW-HEADLIT hold RA, PT-LAWFIRM holds RU and every other role of TSD S4 T6.1 holds R
    Then a repeated POST with the same Idempotency-Key returns the stored answer and describes no second effect

  Scenario: AC6 The six contract fakes answer the document, the naming baseline holds and no cross-schema read is declared (new, D-RCV-60)
    Given the fakes and the naming section of the baseline
    When the nine sub-tables and the fakes are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the rwb-document checklist fake answers version CHK-2026.11 for case RC-2026-000705 with a present and a missing required item, and answers an empty checklist
    Then the rwb-document document-page fake answers the stored documents of the case paged, including the missing item after retrieval
    Then the rwb-case fake answers the case states PACK_ASSEMBLY, PACK_DEFECT_HOLD and FILING_REJECTED and an accepted and a refused move, the rwb-decision fake answers the LITIGATION package at its version, and the decision-record stub answers a healthy and a stopped chain
    Then the drift test compares every fake with the document and fails the build on any difference
    Then the schema is rwb_litigation, the topic is rwb.litigation.events.v1, the queue is rwb-litigation and the Java package is th.co.scb.ace.workbench.recovery.litigation
    Then the tables named as owned are legal_action and the library objects decision_record and idempotency_key, and document, document_checklist_item, case_document_check, recovery_case, rule_row and decision_log_entry are named as other owners' and are consumed only through their contracts
    Then the document declares no v_ace_* read, no grant on another rwb_* schema, no event published, no event consumed and no Schedule, and the absence test fails a build that adds one
```

These six criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S4-E5005-APP and they copy no criterion of the legacy story, whose four criteria stay with the app story word for word.

Scenario: AC7 Each business rule BR1 to BR12 has a criterion or a boundary test (new, D-RCV-60)

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The legal action, the pack outcome and the decision are rwb-litigation's, and the contract declares their element, status and outcome on `legal_action` only | Architecture v5 slide 41; Ownership Map (legal_action and hearing owner S4); TSD S4 T3.1 |
| BR2 | The defect list is the checklist of rwb-document and is declared as a consumed fact, never as a property of this service and never as a stored copy | FEAT-DCM-16 (FSD P5 A2.16); RWB-P5-E1040-APP section 12; GAP-2758 |
| BR3 | The decision record is declared as an element written before the case answer, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S4 T2; legacy RWB-E5-005 AC1 and AC4 |
| BR4 | The case move is answered and not written: the contract declares the answer that carries `PACK_DEFECT_HOLD` or `PACK_ASSEMBLY` and declares no `recovery_case` property and no case row write | Ownership Map (recovery_case owner P3); Architecture v5 slide 41; GAP-2758 |
| BR5 | No ACE view and no ACE table is read: the service holds no `v_ace_*` grant, and the legacy data row of this key lists no ACE fact | Architecture v5 slide 29; DP-05 (not applied) |
| BR6 | A POST declares the `Idempotency-Key` and stores its answer; a GET declares none | Architecture v5 slide 11; TSD S4 T-A.2 |
| BR7 | The vocabulary is closed: `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS` are published as enumerated values, the item state is an enumerated value of the answer, and no state name or list value is a constant of the code | TSD S4 T3.2; BR-S4-005 (FSD S4 A2.5.3.1) |
| BR8 | No personal data in a schema, an example or a fake: identifiers, type codes, counts, dates, list values and a rule version only | Architecture v5 slide 42 notes; Template and Rules v1 §R7.2 (s17) |
| BR9 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR10 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR11 | The document lists only operations owned by rwb-litigation; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-11 |
| BR12 | The rule rows of R-LIT-16, R-LIT-17, R-LIT-18 and R-LIT-32 and the D7 approval limit are governed in rwb-decision and named here, never declared here | Business Rules and Routing Logic v4; TSD S4 T4 |

Rule coverage: BR1 by AC1 (TC-E5-005-01, TC-S4-E5005-CON-01); BR2 by AC2 (TC-E5-005-02, TC-S4-E5005-CON-02); BR3 by AC4 and AC6 (TC-S4-E5005-CON-03, TC-E5-005-06); BR4 by AC3 (TC-E5-005-03, TC-S4-E5005-CON-02); BR5 by AC6 (TC-S4-E5005-CON-04); BR6 by AC1 (TC-S4-E5005-CON-01); BR7 by AC1 (TC-S4-E5005-CON-01); BR8 by AC1 (TC-S4-E5005-CON-01); BR9 by AC6 (TC-S4-E5005-CON-04); BR10 by AC1 (TC-S4-E5005-CON-06); BR11 by AC1 and AC6 (TC-S4-E5005-CON-01, TC-S4-E5005-CON-04); BR12 by AC2 and AC3 (TC-E5-005-02, TC-E5-005-03).

### 9. State transitions

The lifecycle of this document, not of a case:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the pack and outcome elements, the consumed rows and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the two screens, the wave 3 harness and the rwb-document, rwb-case and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new error code | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a list value or an item state changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence test of AC6 fails: a `v_ace_*` view, a checklist, document or `recovery_case` property, a second topic or a Schedule | In review |

The status machine of `legal_action` that the document describes is the app story's, and this baseline fixes the vocabulary and the pack element's values and moves no case and no action.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-litigation | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes |
| Consuming teams (the app story, the screens, the wave 3 harness and the owners of rwb-document, rwb-case, rwb-decision and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme of the document is named "the rwb-litigation login (DP-02)" and is not part of this baseline.

Every operation of `/api/recovery/litigation/v1` calls the rwb-access authorise check (DP-08) before it acts. That check is consumed from rwb-access and is named here only, never declared as a rule of this service. Screens SCR-19 and SCR-20 of P3 are not declared by this contract; their empty, loading, error and no-access states belong to RWB-S4-E5005-APP. The no-access outcome of this contract is the 403 response of AC5.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| LegalAction element | The columns of DF-LEG-001 to DF-LEG-014: `id`, `case_id`, `law_firm_id`, `action_type`, `lawsuit_no`, `black_case_no`, `red_case_no`, `court_name`, `claim_amount`, `filed_date`, `judgment_date`, `judgment_amount`, `lit_status` and `status` | BR1 |
| Pack element | The checklist version, the stage code, the items and the missing items of the case, carried on the answer and stored nowhere here; the checklist version is DF-REF-234 to DF-REF-243 of `document_checklist_item` (P5) | BR4 |
| Item state | Present or missing per required item, derived from `presentCount` of the P5 answer; the value set of the state is an element name of this baseline (GAP-2759; ASM-4592) | BR7 |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the case answer (DP-03) | BR3 |
| Case documents | DF-DOC-001 to DF-DOC-011 of `document` in `rwb_document`, read only through API-P5-002 and never written, copied or joined here | BR11 |
| Case of record | DF-CAS-001 to DF-CAS-023 of `recovery_case` in `rwb_case`, read only through the case answer | BR4 |
| Not written here | `document`, `document_checklist_item`, `case_document_check` (P5), `recovery_case` (P3), `decision_log_entry` and `rule_row` (P7) | BR4 |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC1 and the optionality rule of BR10. **No new table, no new column and no migration** is declared by this story.

The business key `case_id` of `legal_action` is a varchar(255) column that carries the business key of the case, with no foreign key: the case lives in `rwb_case`, so no cross-schema reference is stored (DP-01; ADR-014). The field name is kept from the FSD.

Reference data read: the enumerated values `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS` (BR7) and the checklist rows of `document_checklist_item` (DF-REF-234 to DF-REF-243, read through API-P5-008). The reference-data contract of DP-06 and DP-07 applies to these reads. The parameter keys read are Not specified in the source documents (DOR-RWB-S4-E5005-CON-20).

The defect list is the document checklist of FEAT-DCM-16, read through API-P5-008 of rwb-document (P5). The case documents are read through API-P5-002 and the case of record through the rwb-case answer. The three consumed reads are described as consumed and faked here (BR2, BR11). The class and dependency rows stay as the plan gives them; step D1 decides whether they become C dependencies of this key or a baseline of the P5 defect-list story is raised.

The step starts from the case stage that the parent CaseWorkflow forwards to the litigation child on task queue rwb-litigation (PACK_ASSEMBLY, PACK_DEFECT_HOLD, FILING_REJECTED). No event and no Schedule is declared, because DP-09 is not in the pattern set of this key. The trigger, the item-state and missing-item elements and the REQ-S4-002 trace are confirmed at step D1 (GAP-2759; ASM-4592).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/legal-actions` | LegalActionRequest in, LegalAction of status 201 out with its pack element (API-S4-002) | Litigation, right C, scope applied | `Idempotency-Key` header required; the answer is stored |
| GET | `/legal-actions/{legalActionId}` | LegalAction of status 200 out with its pack element, the items and the missing items (API-S4-003) | Litigation, right R, scope applied | Not applicable |

The two operations answer 400, 401, 403, 404, 409, 422 and 503, each with the error envelope and one message ID of section 14. The operation IDs are those of TSD S4 T-A.1; the paths are those of the target base and not the monolith form. API-S4-004 `PATCH /legal-actions/{legalActionId}`, API-S4-005 `POST /legal-actions/{legalActionId}/hearings` and API-S4-001 `POST /notices/{noticeId}/approve` belong to the filing, hearing and notice stories of this service and are not declared by this baseline.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | `/api/recovery/document/v1/cases/{caseId}/document-checklist` (API-P5-008) | P5 rwb-document | The checklist of the case type: the checklist version, the stage code, and each item with its document type, label, required flag and present count; faked |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` (API-P5-002) | P5 rwb-document | The documents stored on the case, paged with `type`, `page` and `size`: identifier, document type, stored date; no field value and no content; faked |
| The case read and the case-move answer (operation name Not specified in the source documents (GAP-2758; ASM-4589)) | rwb-case (P3) | P3 rwb-case | The case reference and the route state, and the move of the case of record to `PACK_DEFECT_HOLD` or `PACK_ASSEMBLY` with the rule ID and its version; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The three rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-2758 with ASM-4589. The two P5 rows are published by the app stories of the hub and no P5 contract story carries them as a baseline, which is the same gap.

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and its catalogue events `LawsuitFiled`, `JudgmentRecorded` and `AuctionResult` belong to the stories that own the filing, the judgment and the auction result. This baseline declares none of them, adds no outbox row and widens no topic; the decision record is relayed by the library of DP-03 on `rwb.decision-record.v1` and is not an event of this service.

#### 12.4 Events consumed

None. The step is started by the case stage the parent `CaseWorkflow` forwards, and DP-09 is not in the pattern set of this key; the S4 IN row of Architecture v5 slide 19 lists only `NoticeDelivered` and `PartnerResultSubmitted`, and the `DocumentStored` event of rwb-document has its consumers elsewhere (GAP-2759; ASM-4590). This baseline therefore declares no consumer group, no subscription and no inbox of its own, and the absence test fails a build that adds one.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-litigation` | The stage that hosts the pack-defect step; its signals and its outcome for the parent are declared, not built. Workflow ID form: Not specified in the source documents (CG-ALL-9107). Start rule: start on the catalog trigger 'Litigation route approved (R-LIT-01), or a restructure or settlement plan breaks (R-LIT-02)'; duplicate-start policy: Not specified in the source documents (CG-ALL-9107) |
| `checkPackDefects` | Activity, the one pack-defect check step | `rwb-litigation` | The case and the legal action in; the rule ID with its package version, the checklist version, the missing items and the case move out. Not in Temporal Catalog v1 Activities (CG-ALL-9108) |

The activity name is a target design choice and the trigger of the step is read as the case stage forwarded by the parent, because the legacy story says the step runs unattended while the FSD declares no background event (GAP-2759; ASM-4590). No activity is registered by this story.

#### 12.6 Schedules

None. The step runs from the case stage signal the parent forwards; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table, and no Job of Architecture v5 slide 44 is owned or moved here.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | The action and its case reference, action type and status; read by the two operations and written by no part of this step |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated POST and the answer it holds |

`document`, `document_checklist_item` and `case_document_check` (P5), `recovery_case` (P3), `decision_log_entry` and `rule_row` (P7) and `hearing` (S4, the sibling stories') are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-document checklist fake (API-P5-008) | The checklist of case `RC-2026-000705` at version `CHK-2026.11` with a present and a missing required item; an empty checklist for a stage with no rows; no answer beyond 2 s | AC1, AC2, AC6 |
| rwb-document document-page fake (API-P5-002) | The stored documents of case `RC-2026-000705` paged, including the missing item after retrieval; a page with no document of a required type | AC2, AC6 |
| rwb-case case fake and case-move answer | The case states `PACK_ASSEMBLY`, `PACK_DEFECT_HOLD` and `FILING_REJECTED`; the moves `PACK_DEFECT_HOLD` and `PACK_ASSEMBLY` accepted, and a move refused | AC3, AC6 |
| rwb-decision rule-package fake | The LITIGATION package at its version in force with R-LIT-16, R-LIT-17, R-LIT-18 and R-LIT-32 | AC4, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC4, AC6 |
| gateway-bff composite route fake | The merged SCR-19 answer for case `RC-2026-000705`, with the pack facts of this service read once | AC1, AC6 |

The fakes are test-only and are replaced by the real services in SIT. The case-move answer and the element names the sources do not fix are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2758, GAP-2759; ASM-4589, ASM-4592).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The create and read of the legal action with its pack on `/api/recovery/litigation/v1`; the checklist and the case document page of rwb-document, and the rwb-case read and move answer; one hop, 2 s |
| Kafka | None declared | No event published and none consumed by this step; the decision record is the library's on `rwb.decision-record.v1` |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `LitigationWorkflow` and `checkPackDefects` on `rwb-litigation`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no case, no legal action, no document and no rule package. What it publishes is one OpenAPI 3.1 document, one AsyncAPI fragment that declares no event, nine contract tables and six fakes.

**Deliverables.** The additive document `openapi/rwb-litigation-v1.yaml` for this step, the pack, item-state and outcome elements, the vocabulary of `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS` as published enumerations, the contract README rows for the consumed rows and their placeholders, and the six WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-13 moves the base and nothing else. DP-19 is behind SCR-19 and SCR-20, whose screen model is the edge contract's. DP-03 is the element rule: the record is written before the answer. DP-09 is not in the pattern set of this key, which is why no event is declared in 12.3 or 12.4, and DP-05 is not either, because this service holds no `v_ace_*` grant.

**Dependencies the table adds and the plan does not hold.** The pattern table adds exactly the two H rows the plan already carries, `RWB-PLT-E1027-CON` and `RWB-PLT-N001-CON`, so no H row is missing. The three consumed rows are class C in fact and the plan's C row is None (GAP-2758; ASM-4589).

**Build steps**

1. Write the two operations and validate the additive rule of AC1 in the pipeline.
2. Write the pack, item-state and outcome elements of AC1 with the placeholder on the fields the sources do not give.
3. Record the two P5 consumed rows of AC2 with their owner, their paging rule, their budget and their placeholders.
4. Record the case answer of AC3 and the absence test for a `recovery_case` property.
5. Record the decision-record element of AC4 and validate it against the library schema.
6. Record the error envelope, the rights and the `Idempotency-Key` rule of AC5.
7. Publish the six fakes of AC6 and the drift and absence tests.
8. Tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the contract tests pass, the six fakes answer every consumed path and the drift test is green, and the app story, the screens and the wave 3 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | A required item of the checklist version in force is not among the documents of the case; the app story raises it on a held pack, and this baseline declares it on the 422 of the held pack | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key. It names the expiry of the claim on the case, which the prescription rules of the sibling stories raise, so no path of this step raises it | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Litigation right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the case answer | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added.

### 15. Screens and states

The contract serves SCR-19 Litigation workspace in its pack, instructed, filed, hearing and judgment states and SCR-20 Enforcement workspace in its requested, seized, auctioned and closed states, all through the gateway-bff composite route (DP-19). The route calls rwb-litigation for the legal action and its pack element, rwb-document for the checklist version, the items and the documents, and rwb-case for the case and its route state; this baseline fixes the rwb-litigation answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The held, empty and failure states the app story shows — pack held, no checklist, not recorded, refused — read the messages of section 14 on the same route. SCR-19 empty, loading, error and no access states: Not specified in the source documents (CG-ALL-9111). SCR-20 empty, loading, error and no access states: Not specified in the source documents (CG-ALL-9112).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-005-01 | AC1 | Contract | Check the pack against the defect list; the contract half answers the two operations, the pack element and the outcome element |
| TC-E5-005-02 | AC2 | Contract | Rule R-LIT-18; the contract half answers the consumed checklist row and the re-run shape |
| TC-E5-005-03 | AC3 | Contract | Rule R-LIT-32; the contract half answers the case answer and the re-filing move |
| TC-E5-005-04 | AC4 | Contract | Not recorded; the contract half answers the decision-record element and the MSG-P7-003 condition |
| TC-E5-005-05 | AC5 | Contract | A role without the right is refused with MSG-P4-002; the contract half answers the rights and the 403 |
| TC-E5-005-06 | AC6 | Contract | A forced decision record write failure stops the action with MSG-P7-003; the contract half answers the fake and the absence tests |
| TC-S4-E5005-CON-01 | AC1, AC5 | Contract | The document validates; the two operations, the pack and outcome elements, the two lists and the seven error responses are present |
| TC-S4-E5005-CON-02 | AC2, AC3 | Contract | The two P5 rows and the case answer validate with their placeholder fields marked and one hop with a 2 s budget |
| TC-S4-E5005-CON-03 | AC4 | Contract | The decision-record element validates against the library schema, with the checklist version and the missing item count |
| TC-S4-E5005-CON-04 | AC6 | Contract | The six fakes match the document and a drifted fake fails the build; the absence test for a `v_ace_*` read, a checklist, document or `recovery_case` property, a second topic and a Schedule |
| TC-S4-E5005-CON-05 | AC1, AC4 | Contract | Boundary of the three §12.7 tables, legal_action, decision_record and idempotency_key: each validates with its declared columns, and a column outside the declared set is refused |
| TC-S4-E5005-CON-06 | AC1 | Contract | A change to a declared shape is additive within major version 1, and a breaking change needs a new major version (BR10) |
| TC-S4-E5005-CON-07 | AC7 | Contract | Each rule BR1 to BR12 is checked by its criterion or boundary test; proposed test: Not specified in the source documents (NEWAC-RWB-S4-E5005-CON-AC7) |

The six legacy cases are the legacy cases of RWB-E5-005 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S4-E5005-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The four cases `TC-S4-E5005-CON-01` to `-04` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the checklist items, their required flag and order, the lists and the rule rows stay reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, type codes, counts, dates, list values and a rule version only; every example is synthetic.
- The checklist stays with rwb-document and the case with rwb-case: the document declares no checklist property, no document-row property, no `recovery_case` property and no case row write (BR2, BR4).
- ACE data only through the owner's contract: the document declares no `v_ace_*` view and no grant on another `rwb_*` schema, and the boundary test fails a build that adds one.
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-litigation; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence test of AC6 fails a build that declares a `v_ace_*` read, an event, a second topic, a Schedule, a Quartz row or a shared job table.
- The error envelope, the `Idempotency-Key` rule and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S4-002 | A litigation pack is assembled and checked against the document checklist, and missing documents are requested; the contract fixes the pack element, the checklist and document rows and the case answer on which the rule is evaluated (FSD S4 Requirements served; Business Requirements Program v5); the legacy story master carries no requirement ID and the plan's requirement row for this key is empty (GAP-2759; ASM-4591) | The two operations, the pack and outcome elements, the two P5 consumed rows and the case answer | TC-E5-005-01, TC-S4-E5005-CON-01, TC-S4-E5005-CON-02 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows with their budget and breaker | TC-S4-E5005-CON-02 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-005, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by RWB-S4-E5005-APP; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the four new contract cases TC-S4-E5005-CON-01 to -04 |
| Feature and screens | FEAT-LIT-05, FEAT-DCM-16, SCR-19 Litigation workspace and SCR-20 Enforcement workspace |
| Rules | R-LIT-16, R-LIT-17, R-LIT-18 and R-LIT-32, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the two operations, the evaluation of R-LIT-16, R-LIT-17, R-LIT-18 and R-LIT-32, the decision record and the case answer: RWB-S4-E5005-APP.
- The document checklist per case type, the stored documents, the retrieval request and the CCMS exchange: rwb-document (P5), FEAT-DCM-16 and its stories. **The defect list is the hub's checklist, and no part of this baseline copies it** (GAP-2758; ASM-4588).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose case answer this baseline declares as consumed and faked.
- The assembly of the pack, the verification and approval of the filing, the law firm instruction, the court filing, the hearing calendar and the judgment: the sibling stories of this service.
- The authoring, testing, approval and versioning of the LITIGATION package and of the rule rows of the four rules, and the D7 approval limit: rwb-decision (P7).
- The ACE account and batch facts and the interaction ledger: rwb-source-data (P1); this key reads none of them.
- The gateway-bff composite route and the screen field list of SCR-19 and SCR-20: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
