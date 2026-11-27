# RWB-S4-E5006-CON Recover a missing or lost document - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5006-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | P5, P8 and P10 contract stories (GAP-1737) |
| Integration dependencies | None |
| External dependencies | None |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-S4-E5006-CON-14) |
| Size | Not specified in the source documents (DOR-RWB-S4-E5006-CON-16) |
| Contract version | v1 (the path version of /api/recovery/litigation/v1 and of the consumed /api/recovery/document/v1 paths) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (FEAT-LIT-06; REQ-S4-002; L3 process 08 Litigate and enforce) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the pack-recovery step of rwb-litigation, split from RWB-E5-006. It fixes the two legal-action operations the legacy story names on `/api/recovery/litigation/v1` (DP-13), the recovery element and the outcome vocabulary `DOCUMENT_UNRECOVERABLE` and `PRESCRIPTION_WARNING` of R-LIT-19 and R-LIT-20 with `DOCUMENT_RETRIEVED` as the hand-back value of the sibling R-LIT-18, the `Idempotency-Key` rule and the error envelope, the consumed checklist and case-document reads of rwb-document (P5), the case-move answer of rwb-case and the decision-record element of DP-03. The document stays with rwb-document and no `document` property is declared here (GAP-2760; ASM-4594); the recovery element, the reason list and the case-move operation name have no source specification and are carried with the placeholder (GAP-2761; ASM-4595); the CCMS path has no owner in the target (GAP-2764; ASM-4598). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S4-E5006-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 11 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the pack-recovery step of rwb-litigation — the two legal-action operations on `/api/recovery/litigation/v1`, the recovery element and its outcome vocabulary, the `Idempotency-Key` rule and the error envelope, the consumed checklist and case-document facts of rwb-document, the case-move answer of rwb-case, the decision-record element, the tables and the fakes**, so that **the app story, the screen and the tests of this legacy key build against one fixed, testable contract on Day 1 and a document type, an outcome value, a reason or an answer shape can never drift between rwb-litigation, rwb-document and rwb-case without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy step of RWB-E5-006 crossed three boundaries at once: an officer screen, a document row of the pack, and a case state. The target splits them: the document, the checklist item and the custody of the file are rwb-document's (P5), the case of record and its route states stay with rwb-case (P3), and the pack-recovery decision and the legal action it repairs stay with rwb-litigation (S4). Each boundary is now a contract that another team builds against, so each has to be fixed before the app story starts: the two operations, the recovery element, the outcome vocabulary of the three rules, the facts the P5 contract answers, the case-move answer and the record of the decision.

The baseline also fixes the naming that the checks require: schema `rwb_litigation`, base `/api/recovery/litigation/v1`, topic `rwb.litigation.events.v1` with retry and `.dlt` topics, task queue `rwb-litigation` and Java package `th.co.scb.ace.workbench.recovery.litigation` (Architecture v5 slide 41 notes). It records that rwb-litigation holds no `v_ace_*` grant and no grant on `rwb_document` or any other `rwb_*` schema (Architecture v5 slides 29 and 41), so DP-05 is declared as a prohibition and the document facts are consumed on the owner's contract only. It records that the three catalogue events of the service — `LawsuitFiled`, `JudgmentRecorded` and `AuctionResult` — belong to the filing, the judgment and the auction result, so this baseline declares no event (GAP-2763; ASM-4597).

Three points are carried as gaps and assumptions rather than decided quietly: the three consumed contracts of the step have no C row and the plan's contract row is None (GAP-2760), the recovery element, the reason list of R-LIT-19 and the fields that would hold them have no field list in any source (GAP-2761), and the CCMS path of the FSD integration points has no owner in the target (GAP-2764). The boundary with the sibling story is fixed too: the defect check and its re-run on a supplied item are RWB-S4-E5005-APP's, so this baseline fixes only the unrecoverable and prescription outcomes and the hand-back value of R-LIT-18.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `legal_action` and `hearing` are S4's, `document` and `document_checklist_item` are P5's, `recovery_case` is P3's, `decision_log_entry` and `rule_row` are P7's. This document never declares another service's operation as provided.
- The two P5 operations are the published surface of their owner stories: `GET /cases/{caseId}/document-checklist` (API-P5-008) of RWB-P5-E1040-APP and `GET /cases/{caseId}/documents` (API-P5-002) of RWB-P5-E1026-APP. No P5 contract story carries either as a baseline, so both are class C dependencies in fact and the contract-dependency row here names P5, P8 and P10 (GAP-1737).
- The case-move answer of rwb-case is fixed here as a shape only; no source names a published operation that moves a case state on behalf of a stage, and the name is Not specified in the source documents (GAP-2760; ASM-4594).
- The LITIGATION rule package, its rows for R-LIT-18, R-LIT-19 and R-LIT-20 and the Head of Litigation approval are governed in rwb-decision (P7); this baseline names them and declares none of them. R-LIT-18 is evaluated by RWB-S4-E5005-APP and its outcome value is declared here only as the hand-back of a supplied item.
- The `legal_action` and `hearing` tables and their columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-litigation for this step: the two operations with their request and answer elements, the recovery element, the rights and the seven error responses.
2. Fix the recovery element: the case reference, the legal action reference, the checklist item by its `LOV-DOC-TYPE` document type, the outcome value, the reason where the item is unrecoverable, the rule ID, the package version and the decided-at time.
3. Fix the consumed document facts of the P5 contract: the checklist read with its version and item counts, and the case document page, and mark the fields the sources do not give with the placeholder.
4. Fix the case-move answer of rwb-case: the move `PACK_VERIFIED`, the rule ID, the version and the decided-at time, with no case row read or written here, and record that `PACK_ASSEMBLY` is the sibling story's move.
5. Record the decision-record element of DP-03 on `rwb.decision-record.v1`, written before the case-move answer.
6. Record the closed vocabulary of the outcome values and of the hand-back, and the rule that no list value is a constant of the code.
7. Publish the contract tables of section 12 and the five contract fakes.
8. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a `v_ace_*` read and of a `document` or `recovery_case` write, and the drift between a fake and the document.
9. Tag the baseline and hand it to RWB-S4-E5006-APP, SCR-19 and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body or a request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC7 |
| X4 | The consumed document fact or the case-move answer has a field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC4 |
| X5 | An outcome value outside the ones the rules name appears in the document or in an example | The vocabulary test fails the build | None | AC1, AC8 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `document` row or a `recovery_case` row | The review fails the baseline; the boundary test fails the build | None | AC8 |
| X7 | A POST is repeated with the same `Idempotency-Key` | The stored answer is returned and no second effect is described | None | AC2, AC5 |
| X8 | The rights of an operation are not the ones TSD S4 T-A.1 declares | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published P5 document surfaces and the rwb-case answer only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the operations, the outcome values, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S4-E5006-APP, SCR-19 and the wave 3 harness on Day 1, and the rwb-document and rwb-case teams on the same day |
| Estimable | One OpenAPI document, one AsyncAPI fragment that declares no event, nine contract tables, five fakes and four new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the pack-recovery step of rwb-litigation

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of legal_action and hearing is S4, of document and document_checklist_item is P5 and of recovery_case is P3
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The two legal-action operations are declared with the recovery element and the outcome vocabulary (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-litigation is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /cases/{caseId}/legal-actions with the LegalAction answer of status 201 and GET /legal-actions/{legalActionId} with the LegalAction answer of status 200, both under the base /api/recovery/litigation/v1 and owned by rwb-litigation
    Then the recovery answer declares the outcome against the rule vocabulary with the values DOCUMENT_UNRECOVERABLE and PRESCRIPTION_WARNING of R-LIT-19 and R-LIT-20, and DOCUMENT_RETRIEVED of R-LIT-18 as the hand-back to RWB-S4-E5005-APP
    Then every other property of the LegalAction element is copied from the baseline of the legal action and is not redefined here
    Then the document type of the checklist item is declared against LOV-DOC-TYPE and the action type against LOV-LEGAL-TYPE, with no list value written in the document as a constant of the consumer

  Scenario: AC2 The recovery element and its answer are fixed (new, D-RCV-60)
    Given the recovery section of the baseline
    When it is compared with the pack-recovery step of RWB-S4-E5006-APP
    Then the recovery element carries the case reference, the legal action reference, the checklist item by its LOV-DOC-TYPE document type, the outcome value and the reason where the outcome is DOCUMENT_UNRECOVERABLE
    Then its answer carries the same item, the outcome, the rule ID, the package version in force, the case move the rule names and the decided-at time, and no case state
    Then the POST declares the Idempotency-Key header and its stored answer, and the GET declares neither
    Then a request whose outcome is DOCUMENT_UNRECOVERABLE and which carries no reason is declared invalid
    Then the element names of the recovery element and of its reason that no source gives are Not specified in the source documents (GAP-2761; ASM-4595) and the document marks them so

  Scenario: AC3 The consumed document facts of rwb-document are declared and the document stays there (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with API-P5-008 and API-P5-002 of P5 rwb-document
    Then the case checklist is declared as consumed from P5, with its checklist version and each item with its document type against LOV-DOC-TYPE, its required flag and its present count
    Then the documents of the case are declared as consumed from P5, paged with type, page and size, each with its identifier, its document type and its stored date, and no field value and no content
    Then the document declares no document property, no storage reference, no retention class and no write-once flag, and no write of a document row from rwb-litigation
    Then the retrieval request of a missing item is named as rwb-document's and is not declared as an operation of this service
    Then every call on the two rows is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The case-move answer is declared and the case row is never written here (new, D-RCV-60)
    Given the case boundary of the baseline
    When it is compared with rwb-case as the owner of recovery_case and of the route states
    Then the case move is declared as an answer to rwb-case with the move PACK_VERIFIED, the rule ID, the package version and the decided-at time
    Then the move PACK_ASSEMBLY is named as RWB-S4-E5005-APP's and not as a move of this step
    Then the document declares no recovery_case property, no case route-state column and no write of a case row from rwb-litigation
    Then the answer carries the stage outcome that the parent CaseWorkflow applies, and the operation name of a REST case-move call for another caller is Not specified in the source documents (GAP-2760; ASM-4594)
    Then the states PACK_ASSEMBLY, PACK_DEFECT_HOLD and PACK_VERIFIED are named as the case of record's and are read from its answer only

  Scenario: AC5 The Idempotency-Key rule, the error envelope and the rights are fixed (new, D-RCV-60)
    Given the error and access sections of the baseline
    When they are compared with TSD S4 T-A.1 and T-A.2 and with TSD S4 T6.1
    Then the operations answer 400 for a malformed request, 401, 403 with MSG-P4-002, 404, 409 on a closed, withdrawn or wrong-state action, 422 with MSG-GEN-001 and 503 when a downstream does not answer, each with one envelope and one message ID per condition
    Then POST /cases/{caseId}/legal-actions declares Litigation right C and GET /legal-actions/{legalActionId} declares Litigation right R, each with the scope applied
    Then RW-LITOFF holds Litigation CRUA, RW-ENFORCE holds CRU, RW-LEGAL and RW-PRODHEAD and RW-HEADLIT hold RA, PT-LAWFIRM holds RU and every other role of TSD S4 T6.1 holds R
    Then a repeated POST with the same Idempotency-Key returns the stored answer and describes no second effect

  Scenario: AC6 The decision-record element is declared and written before the change (new, D-RCV-60)
    Given the decision section of the baseline
    When it is compared with the local decision-record library of DP-03
    Then one decision record is declared per rule outcome with the case reference, the legal action reference, the document type of the item, the outcome, the reason where the item is unrecoverable, the rule ID, the package version in force and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before the case-move answer, and a failed write leaves the case unchanged with MSG-P7-003
    Then the document declares no event of its own for the record and no second topic for this capability
    Then the record carries IDs, codes, dates and a rule version only

  Scenario: AC7 The five contract fakes answer the document (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-document checklist fake answers the checklist of case "RC-2026-000606" at its version with one item of LOV-DOC-TYPE missing, a checklist with every item present, a case with no checklist and no answer beyond 2 s
    Then the rwb-document document-page fake answers the stored documents of the case paged, with the item absent and with the item present after retrieval
    Then the rwb-case fake answers the case state PACK_DEFECT_HOLD and an accepted and a refused move
    Then the rwb-decision rule-package fake answers the LITIGATION package at its version with R-LIT-18, R-LIT-19 and R-LIT-20 and one approval answer
    Then the decision-record library stub answers a healthy chain and a stopped chain
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC8 The naming baseline and the no-v_ace_ boundary are fixed and no cross-schema read is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_litigation, the login is rwb_litigation, the topic is rwb.litigation.events.v1, the queue is rwb-litigation and the Java package is th.co.scb.ace.workbench.recovery.litigation
    Then the tables named as owned are legal_action read only and the library objects decision_record and idempotency_key, and document, document_checklist_item, recovery_case, decision_log_entry, rule_row and hearing are named as other owners' or another story's and are consumed only through their contracts
    Then the document declares no read of a v_ace_* view and no grant on rwb_document, rwb_case or any other rwb_* schema, and the boundary test fails a build that adds one
    Then the document declares no event published, no event consumed and no Schedule for this step, and the absence test fails a build that adds one
```

These eight criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S4-E5006-APP and they copy no criterion of the legacy story, whose two criteria stay with the app story word for word.

Scenario: AC9 Every business rule BR1 to BR12 of section 8 is covered by a criterion of this story or by a guardrail test (new, D-RCV-60)

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The pack-recovery decision and the legal action it repairs are rwb-litigation's, and the contract declares their elements on the two operations only | Architecture v5 slide 41; Ownership Map (legal_action and hearing owner S4); TSD S4 T-A.1 | AC1, AC2; TC-E5-006-01, TC-S4-E5006-CON-01 |
| BR2 | The decision record is declared as an element written before the case-move answer, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S4 T2; legacy RWB-E5-006 AC1 and AC2 | AC6; TC-E5-006-04, TC-S4-E5006-CON-04 |
| BR3 | The document stays with rwb-document: the contract declares the checklist read and the case document page as consumed, names the retrieval request as P5's, declares no `document` property and describes no custody, retention or write-once fact of rwb-litigation; the recovery outcome is carried on the P5 contract and publishes no event here (GAP-2763) | Ownership Map (`document` owner P5); Architecture v5 slide 41; GAP-2760 | AC3; TC-S4-E5006-CON-03 |
| BR4 | The case move is answered and not written: the contract declares the answer that carries `PACK_VERIFIED` and declares no `recovery_case` property and no case row write; `PACK_ASSEMBLY` is the sibling story's move | Ownership Map (`recovery_case` owner P3); Architecture v5 slide 41; GAP-2760 | AC4; TC-S4-E5006-CON-03 |
| BR5 | No ACE view and no ACE table is read: this service holds no `v_ace_*` grant and no grant on `rwb_document` or `rwb_case` | DP-05; Architecture v5 slides 29 and 41 | AC8; TC-S4-E5006-CON-04 |
| BR6 | A POST declares the `Idempotency-Key` and stores its answer; a GET declares none | Architecture v5 slide 11; TSD S4 T-A.2 | AC5; TC-E5-006-02, TC-S4-E5006-CON-02 |
| BR7 | The vocabulary is closed: the outcome values are those of R-LIT-19 and R-LIT-20 and the hand-back value is R-LIT-18's, and `LOV-DOC-TYPE`, `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS` are published as enumerated reference values, never as constants of the code | Business Rules and Routing Logic v4; TSD S4 T3.2; BR-S4-006 (FSD S4 A2.6.3.1) | AC1, AC2; TC-E5-006-01, TC-S4-E5006-CON-01 |
| BR8 | No personal data in a schema, an example or a fake: identifiers, a document type code, a reason code, dates and a rule version only | Architecture v5 slide 42 notes; Template and Rules v1 §R7.2 (s17) | AC8; TC-S4-E5006-CON-04 |
| BR9 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 | AC1, AC8; TC-S4-E5006-CON-01, TC-S4-E5006-CON-04 |
| BR10 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) | AC1; TC-S4-E5006-CON-01 |
| BR11 | The document lists only operations owned by rwb-litigation; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-11 | AC1; TC-S4-E5006-CON-01 |
| BR12 | The rule rows of R-LIT-19 and R-LIT-20 and the Head of Litigation approval are governed in rwb-decision and named here, never declared here; the defect check and its re-run are RWB-S4-E5005-APP's and are not restated | Business Rules and Routing Logic v4; GAP-2760 | AC8; TC-S4-E5006-CON-04 |

### 9. State transitions

The lifecycle of this document, not of a case:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the vocabulary, the consumed rows and the fakes are described | In review |
| In review | Consumer sign-off | The app story, SCR-19, the wave 3 harness and the rwb-document, rwb-case and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new error code | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or an outcome value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence test of AC8 fails: a `v_ace_*` view, a `document` or `recovery_case` property, a second topic or a Schedule | In review |

The route states the document describes are the case of record's: `PACK_ASSEMBLY`, `PACK_DEFECT_HOLD` and `PACK_VERIFIED` are read from the rwb-case answer, and this baseline fixes only the one move the two rules name and moves no case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-litigation | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes |
| Consuming teams (the app story, SCR-19, the wave 3 harness and the owners of rwb-document, rwb-case, rwb-decision, rwb-access and rwb-source-data) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme of the document is named "the rwb-litigation login (DP-02)" and is not part of this baseline.

The rwb-access authorise check that guards each operation of the document is Not specified in the source documents (DOR-RWB-S4-E5006-CON-6).

### 11. Data

The contract baseline declares shapes, not business values.

| Item | BR Field ID | Content |
|---|---|---|
| LegalAction element | DF-LEG-001 to DF-LEG-014 | The columns of DF-LEG-001 to DF-LEG-014: `id`, `case_id`, `law_firm_id`, `action_type`, `lawsuit_no`, `black_case_no`, `red_case_no`, `court_name`, `claim_amount`, `filed_date`, `judgment_date`, `judgment_amount`, `lit_status` and `status` |
| Recovery element | Not specified in the source documents (DOR-RWB-S4-E5006-CON-7) | The case reference, the legal action reference, the checklist item by its `document_type` against `LOV-DOC-TYPE` (DF-DOC-004), the outcome, the reason where the item is unrecoverable, the rule ID, the package version and the decided-at time; the element names that no source gives are Not specified in the source documents (GAP-2761; ASM-4595) |
| Decision record | DF-DEC-001 to DF-DEC-018 | DF-DEC-001 to DF-DEC-018 through the local library, written before the case-move answer (DP-03) |
| Document facts | DF-DOC-001 to DF-DOC-011 | DF-DOC-001 to DF-DOC-011 of `document` in `rwb_document`, read only through API-P5-008 and API-P5-002 and never written, copied or joined here |
| Case facts | DF-CAS-001 to DF-CAS-023 | DF-CAS-001 to DF-CAS-023 of `recovery_case` in `rwb_case`, read from the P3 answer only |
| ACE facts | DF-ACE-001 to DF-ACE-054 | DF-ACE-001 to DF-ACE-054, not read: this service holds no `v_ace_*` grant (DP-05) |
| Reason of an unrecoverable item | Not specified in the source documents (DOR-RWB-S4-E5006-CON-7) | The list and the element names: Not specified in the source documents (GAP-2761; ASM-4595) |
| Reference data | DF-DOC-004 (LOV-DOC-TYPE); LOV-LEGAL-TYPE and LOV-LEGAL-STATUS: Not specified in the source documents (DOR-RWB-S4-E5006-CON-7) | `LOV-DOC-TYPE`, `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS` published as enumerated reference values under DP-06 and DP-07; the parameters are Not specified in the source documents (DOR-RWB-S4-E5006-CON-20) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC1 and the optionality rules of AC2 and BR10. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/legal-actions` | LegalActionRequest in, LegalAction of status 201 out, with the recovery element and the action type of `LOV-LEGAL-TYPE` (API-S4-002) | Litigation, right C, scope applied | `Idempotency-Key` header required; the answer is stored |
| GET | `/legal-actions/{legalActionId}` | LegalAction of status 200 out with its action type, its status, its pack and the recovery answer (API-S4-003) | Litigation, right R, scope applied | Not applicable |

The two operations answer 400, 401, 403, 404, 409, 422 and 503, each with the error envelope and one message ID of section 14. The operation IDs are those of TSD S4 T-A.1; the paths are those of the target base and not the monolith form. API-S4-004 `PATCH /legal-actions/{legalActionId}` and API-S4-005 `POST /legal-actions/{legalActionId}/hearings` belong to the sibling stories of this service and are not declared by this baseline.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | `/api/recovery/document/v1/cases/{caseId}/document-checklist` (API-P5-008 of `RWB-P5-E1040-APP`) | P5 rwb-document | The checklist of the case type with its version and each item with its document type against `LOV-DOC-TYPE`, its required flag and its present count; faked |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` (API-P5-002 of `RWB-P5-E1026-APP`) | P5 rwb-document | The documents stored on the case, paged with `type`, `page` and `size`: identifier, document type, stored date; the file and the retention are P5's, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2760; ASM-4594)) | rwb-case (P3) | P3 rwb-case | The move of the case of record to `PACK_VERIFIED` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The three rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-2760 with ASM-4594. The retrieval request of a missing item is rwb-document's and its hub's and is not declared here. The CCMS path of the FSD integration points is not declared because no source assigns it an owner in the target (GAP-2764; ASM-4598). The pack, the court fee and the agent call of the FSD integration points are carried as contract dependencies on the P5, P8 and P10 contract stories, built against their published fakes; no direct call and no second writer is introduced here (GAP-1737).

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and its three catalogue events `LawsuitFiled`, `JudgmentRecorded` and `AuctionResult` belong to the stories that own the filing, the judgment and the auction result. This baseline declares none of them, adds no outbox row and widens no topic; the decision record is relayed by the library of DP-03 on `rwb.decision-record.v1` and is not an event of this service. No event for a recovered, re-created or unrecoverable document exists in the catalogue, and the assignment is recorded (GAP-2763; ASM-4597).

#### 12.4 Events consumed

None. The S4 IN row of Architecture v5 slide 19 lists `NoticeDelivered` and `PartnerResultSubmitted`, which belong to the notice and partner-result stories of this service, and the catalogue gives no document event to rwb-litigation. The document facts therefore arrive on the P5 contract of 12.2 and the case state on the rwb-case answer; this baseline declares no consumer group, no subscription and no inbox of its own.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-litigation` | The stage that hosts the pack-recovery step; its input, its signals and its outcome for the parent are declared, not built |
| `recoverMissingDocument` | Activity, the one pack-recovery step | `rwb-litigation` | The case, the legal action and the checklist item in; the rule ID with its package version, the outcome, the reason, the action of the rule and the case move out |

The activity name is a target design choice and is fixed by no source document. The checklist read and the case document page are P5's operations and are declared here as another owner's, never as this service's; the defect list check and its re-run are the sibling step of RWB-S4-E5005-APP and are signalled to, not declared as this step's. No timer is declared, because the 10 working days and the prescription date are durable timers of the journey's sibling stories (GAP-2761; ASM-4595). No activity is registered by this story.

Workflow ID form: Not specified in the source documents (CG-ALL-9130). Start rule (start or signalWithStart) and duplicate-start policy: Not specified in the source documents (CG-ALL-9130). The catalog row states the start condition as: 'Litigation route approved (R-LIT-01), or a restructure or settlement plan breaks (R-LIT-02)'.

#### 12.6 Schedules

None. The step starts from the parent `CaseWorkflow` when the pack stage finds a missing item; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table, and no Job of Architecture v5 slide 44 is owned or moved here.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | The action, its action type and its status; read by the two operations; no column written by this step |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated POST and the answer it holds |

`document` and `document_checklist_item` (P5), `recovery_case` (P3), `decision_log_entry` and `rule_row` (P7) and `hearing` (S4, the sibling stories') are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-document checklist fake (API-P5-008) | The checklist of case `RC-2026-000606` at its version with one item of `LOV-DOC-TYPE` missing; a checklist with every item present; a case with no checklist; no answer beyond 2 s | AC1, AC3, AC7 |
| rwb-document document-page fake (API-P5-002) | The stored documents of case `RC-2026-000606` paged, with the item absent and with the item present after retrieval; no answer beyond 2 s | AC3, AC7 |
| rwb-case case-move fake | The case state `PACK_DEFECT_HOLD`; the move `PACK_VERIFIED` accepted; a move refused | AC2, AC4, AC7 |
| rwb-decision rule-package fake | The LITIGATION package at its version in force with R-LIT-18, R-LIT-19 and R-LIT-20, and one approval answer | AC6, AC7 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC6, AC7 |

The fakes are test-only and are replaced by the real services in SIT. The case-move answer is derived from the published documents and carries the placeholder until its owner confirms it (GAP-2760; ASM-4594).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The create and read of the legal action on `/api/recovery/litigation/v1`; the checklist read, the case document page and the case-move answer; one hop, 2 s |
| Kafka | None declared | No event published and none consumed by this step; the decision record is the library's on `rwb.decision-record.v1` |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `LitigationWorkflow` and `recoverMissingDocument` on `rwb-litigation`; no Schedule |
| File | None | No file is read, built or delivered here; the stored file is P5's |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no document, no case, no decision and no rule package. What it publishes is one OpenAPI 3.1 document, one AsyncAPI fragment that declares no event, nine contract tables and five fakes.

**Deliverables.** The additive document `openapi/rwb-litigation-v1.yaml` for this step, the recovery element, the vocabulary of `LOV-DOC-TYPE`, `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS` as published enumerations, the contract README rows for the consumed rows and their placeholders, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step and the element the baseline declares. DP-13 moves the base and nothing else. DP-19 is behind SCR-19, whose screen model is the edge contract's. DP-05 is declared as a prohibition: the document declares no `v_ace_*` read and no grant on any schema of another service, because rwb-litigation holds none (Architecture v5 slides 29 and 41). DP-09 is not in the pattern set of this key, which is why no event is declared in 12.3 or 12.4.

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, while the plan's build list for this story is None; this baseline builds against their fakes until those platform contract stories publish. The three consumed rows are non-blocking C dependencies carried in §12.2 (GAP-2760; ASM-4594); the metadata row carries the FSD contract dependencies (GAP-1737). The two P5 reads are named after the P5 contract story that publishes them, and the rwb-case owner confirms the case-move answer when its contract story is written.

**Build steps**

1. Write the two operations and validate the additive rule of AC1 in the pipeline.
2. Write the recovery element of AC2 with the placeholder on the names the sources do not give.
3. Record the two P5 consumed rows of AC3 with their owner, their budget and the boundary of the retrieval request.
4. Record the case-move answer of AC4 and the absence test for a `recovery_case` property.
5. Record the error envelope, the rights and the `Idempotency-Key` rule of AC5.
6. Record the decision-record element of AC6 and validate it against the library schema.
7. Publish the five fakes of AC7 and the drift test.
8. Record the naming baseline and the boundary of AC8, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the ten contract tests pass, the five fakes answer every consumed path and the drift test is green, and the app story, SCR-19 and the wave 3 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the litigation pack at filing, which is the filing story of this service, so no path of this step raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key. It names the expiry of the claim on the case, which is the prescription fact of this service, so no path of this step raises it | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Litigation right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the case-move answer | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five message IDs are contract elements and the text is the legacy wording, copied unchanged; no message is reworded and no new one is added. No source gives the wording of a retrieval failure on the P5 side, so that path answers the platform error envelope and carries no message of its own (GAP-2761; ASM-4595).

### 15. Screens and states

The contract serves SCR-19 Litigation workspace in its `PACK_ASSEMBLY`, `PACK_DEFECT_HOLD` and `PACK_VERIFIED` states through the gateway-bff composite route (DP-19). Its empty, loading, error and no access states are Not specified in the source documents (CG-ALL-9133). The route calls rwb-litigation for the legal action and the recovery answer, rwb-document for the checklist and the case documents, and rwb-case for the case and its route state; this baseline fixes the rwb-litigation answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. SCR-20 Enforcement workspace is listed by the legacy story and is served by the sibling stories' answers; this baseline adds nothing to it. Its empty, loading, error and no access states are Not specified in the source documents (CG-ALL-9134). The refusal and failure states the app story shows — refused, not on hold, no reason, not recorded — read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-006-01 | AC1, AC2 | Contract | Case `RC-2026-000606`; the contract half answers the two operations, the recovery element and the outcome values |
| TC-E5-006-02 | AC2, AC5 | Contract | An unrecoverable outcome with and without a reason; the contract half answers the invalid request and the `Idempotency-Key` of the POST |
| TC-E5-006-03 | AC5, AC8 | Contract | A role without the Litigation right and a malformed request; the contract half answers the 403 with MSG-P4-002 and the 400 of the envelope |
| TC-E5-006-04 | AC6, AC8 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the naming and boundary rows |
| TC-S4-E5006-CON-01 | AC1 | Contract | The document validates; the two operations, the base, the recovery element and the three outcome values are present, and no document or case property is added |
| TC-S4-E5006-CON-02 | AC2, AC5 | Contract | The recovery element and its answer validate; the `Idempotency-Key` rule and the seven error responses with one message ID per condition |
| TC-S4-E5006-CON-03 | AC3, AC4 | Contract | The two P5 consumed rows and the case-move answer validate with their placeholder fields marked and one hop with a 2 s budget |
| TC-S4-E5006-CON-04 | AC6, AC7, AC8 | Contract | The decision-record element validates against the library schema; the five fakes match the document and a drifted fake fails the build; the absence test for a `v_ace_*` read, a `document` or `recovery_case` property, a second topic and a Schedule |
| TC-S4-E5006-CON-05 | AC6, AC8 | Contract | Each table of 12.7 is checked against its owner and contracted use: legal_action, decision_record and idempotency_key validate, and a table owned by another service or a new table fails the build |
| TC-S4-E5006-CON-06 | AC9 | Contract | Not specified in the source documents (NEWAC-RWB-S4-E5006-CON-AC9) |

The four legacy cases are the legacy cases of RWB-E5-006 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S4-E5006-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The four cases `TC-S4-E5006-CON-01` to `-04` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the working-day timers, the 90-day warning, the reason set, the lists and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, a document type code, a reason code, dates and a rule version only; every example is synthetic.
- The document stays with rwb-document and the case with rwb-case: the document declares no `document` property, no storage reference, no retention class, no `recovery_case` property and no case row write (BR3, BR4).
- ACE data only through the owner's contract: the document declares no `v_ace_*` view and no grant on `rwb_document`, `rwb_case` or any other `rwb_*` schema, and the boundary test fails a build that adds one (DP-05).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-litigation; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- The defect check and its re-run are not restated: a supplied item is the sibling story's outcome and this baseline fixes only the hand-back value (BR12).
- No retired element is reintroduced: the absence test of AC8 fails a build that declares a `v_ace_*` read, a second topic, a Schedule, a Quartz row or a shared job table.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S4-002 | A litigation pack is assembled and checked against the document checklist, and missing documents are requested (FSD S4 requirements served; Business Requirements Program v5); the legacy story master carries no requirement ID and the key is mapped to this requirement of the module (GAP-2762; ASM-4596) | The two operations, the recovery element, the two P5 consumed rows and the case-move answer | TC-E5-006-01, TC-S4-E5006-CON-01, TC-S4-E5006-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows with their budget and breaker | TC-S4-E5006-CON-02, TC-S4-E5006-CON-03 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-006, disposition Split (rework) |
| Legacy criteria | AC1 and AC2 of the legacy story, owned word for word by RWB-S4-E5006-APP; this baseline copies none of them |
| Test cases | The four legacy cases as the contract half, and the four new contract cases TC-S4-E5006-CON-01 to -04 |
| Feature and screens | FEAT-LIT-06, SCR-19 Litigation workspace and SCR-20 Enforcement workspace |
| Rules | R-LIT-19 and R-LIT-20, named from the Business Rules and Routing Logic v4 and governed in rwb-decision; R-LIT-18 is RWB-S4-E5005-APP's |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the two operations, the evaluation of R-LIT-19 and R-LIT-20, the decision record and the case-move answer: RWB-S4-E5006-APP.
- The document, the checklist per case type, the checklist item, the retrieval request, the intake and the OCR text, the custody of the file, the retention class and the write-once rule: rwb-document (P5), whose contract this baseline declares as consumed and faked. **The document stays with rwb-document and no part of this baseline moves it** (GAP-2760; ASM-4594).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose case-move answer this baseline declares as consumed and faked.
- The defect list check and its re-run on a supplied item, and the move to `PACK_ASSEMBLY`: RWB-S4-E5005-APP, whose outcome value this baseline only declares.
- The assembly of the pack (FEAT-LIT-04), the verification and filing (FEAT-LIT-07), the notice path and the firm instruction: the sibling stories of this service.
- The authoring, testing, approval and versioning of the LITIGATION package and of R-LIT-19 and R-LIT-20, and the Head of Litigation approval: rwb-decision (P7).
- The CCMS path of the FSD integration points: no source assigns it an owner in the target (GAP-2764; ASM-4598).
- The ACE account, customer and batch facts and the freshness of a data product: rwb-source-data (P1).
- The gateway-bff composite route and the screen field list of SCR-19 and SCR-20: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
