# RWB-S4-E5017-CON Trace assets for enforcement - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5017-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the enforcement asset-trace step of rwb-litigation, split from RWB-E5-017. It fixes the two legal-action operations on `/api/recovery/litigation/v1` (DP-13), the trace request and answer elements, the `CIVIL_CASE` action type and the statuses the step reads and writes, the ACE asset and batch-status read through rwb-source-data (DP-05), the external search through rwb-integration, the trace plan of rwb-agent, the case-move answer of rwb-case, the rule package of rwb-decision, the `Idempotency-Key` rule, the error envelope, the rights and the decision-record element of DP-03. The trace adds no table and no column, the enforcement decision stays with the sibling stories, and the five consumed rows carry no C row in the plan and no operation name in any source (GAP-2815 to GAP-2818; ASM-4659 to ASM-4664). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S4-E5017-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the enforcement asset-trace step of rwb-litigation — the two legal-action operations on `/api/recovery/litigation/v1`, the trace request and answer elements, the action-type and status vocabulary, the five consumed rows for the ACE assets and batch status, the external search, the trace plan, the case move and the rule package, the `Idempotency-Key` rule, the error envelope and the rights, the decision-record element, the tables and the fakes**, so that **the app story, SCR-19, SCR-20 and the tests of this legacy key build against one fixed, testable contract on Day 1, and an asset field, a source name, a state or an answer shape can never drift between rwb-litigation, rwb-source-data, rwb-integration, rwb-agent, rwb-case and rwb-decision without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy step of RWB-E5-017 crossed four boundaries at once: an unattended process holding the `recovery` schema and the `v_ace_npa_asset` view, a bureau call, a registry and insurer search, and a case state. The target splits them: the ACE assets and the batch status are rwb-source-data's (P1), the bureau, registry and insurer adapters are rwb-integration's (P2), the trace plan is rwb-agent's (P10), the case of record is rwb-case's (P3), the rule rows are rwb-decision's (P7), and the litigation stage, the legal action and the decision record stay with rwb-litigation (S4). Each boundary is a contract another team builds against, so each has to be fixed before the app story starts.

The baseline also fixes the naming the checks require: schema `rwb_litigation`, base `/api/recovery/litigation/v1`, topic `rwb.litigation.events.v1` with retry and `.dlt` topics, task queue `rwb-litigation` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.litigation` (context pack, service and naming rules). It records that rwb-litigation owns two tables, `legal_action` and `hearing`, five REST operations and one workflow, and no event and no job at all (context pack, ownership rows), so this baseline declares no event and no Schedule.

Three points are carried as gaps and assumptions rather than decided quietly: **the ACE read**, because `v_ace_npa_asset` and `v_ace_batch_status` are views the architecture gives to rwb-source-data and DP-05 allows either the owner's contract or the service's own view, and no view is granted to S4 (GAP-2815; ASM-4659); **the external search and the plan**, because NCB, the registries, the insurers and the model gateway appear in no dependency row and no operation name (GAP-2816; ASM-4660); and **the trace result**, because neither table of this service carries an asset, a trace date or a source, so the result is a decision record and a read model and the enforcement decision is a sibling story's (GAP-2818; ASM-4663).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `legal_action` and `hearing` are S4's, `v_ace_npa_asset` and `v_ace_batch_status` are read through P1, `recovery_case` is P3's, `decision_log_entry` and `rule_row` are P7's, `document` is P5's. This document never declares another service's operation as provided.
- The five consumed rows of 12.2 name five owners whose contracts are published; none of the five is in this story's contract-dependency row, which is None, and the absence is recorded (GAP-2815, GAP-2816; ASM-4659, ASM-4660).
- The operation names and the element lists of the five consumed rows are Not specified in the source documents: the TSD S4 T5.2 names the published Java interfaces P3, P7, P4, P5 and P6 with no operation, and T-A.1 lists five S4 operations only.
- The LITIGATION package, its rule rows for R-LIT-50 and R-LIT-52 and the 10 and 5 working-day timers are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The `legal_action` table and its columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-litigation for this step: the two operations with their request and answer elements, the action type and status vocabulary, the rights and the seven error responses.
2. Fix the trace elements: the request that carries the case, the legal action, the trace reference and the four sources, and the answer that carries the traced assets, the source of each asset, the batch status, the stage, the rule ID, the package version and the decided-at time.
3. Fix the boundary: the step reads the action and writes no column, adds no asset table and no trace column, and declares the enforcement decision as the sibling stories'.
4. Fix the five consumed rows and mark the fields the sources do not give with the placeholder.
5. Record the decision-record element of DP-03 on `rwb.decision-record.v1`, written before the stage changes.
6. Record the closed vocabulary and the rule that no value is a constant of the code.
7. Publish the contract tables of section 12 and the six contract fakes.
8. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of an asset, `recovery_case` or `rule_row` property, and the drift between a fake and the document.
9. Tag the baseline and hand it to RWB-S4-E5017-APP, SCR-19, SCR-20 and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body or a request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list or an operation name the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC6 |
| X5 | A value outside `LOV-LEGAL-TYPE` or `LOV-LEGAL-STATUS` appears, or an asset field is declared on `legal_action` | The vocabulary and the absence test fail the build | None | AC1, AC2, AC7 |
| X6 | The document declares another service's operation as provided, a `recovery_case` row, a `rule_row` property or a `v_ace_*` view it does not own | The review fails the baseline; the boundary test fails the build | None | AC3, AC7 |
| X7 | A POST is repeated with the same `Idempotency-Key` | The stored answer is returned and no second effect is described | None | AC4 |
| X8 | The rights of an operation are not the ones TSD S4 T-A.1 declares | The access test fails the build | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner contracts of rwb-source-data, rwb-integration, rwb-agent, rwb-case and rwb-decision only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the operations, the vocabulary, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S4-E5017-APP, SCR-19, SCR-20 and the wave 3 harness on Day 1, and the rwb-source-data, rwb-integration and rwb-agent teams on the same day |
| Estimable | One OpenAPI document, one AsyncAPI fragment, nine contract tables, six fakes and four new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the enforcement asset-trace step of rwb-litigation

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of legal_action and hearing is S4, of the ACE asset and batch views is P1 and of recovery_case is P3
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The two legal-action operations are declared with the action-type and status vocabulary (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-litigation is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /cases/{caseId}/legal-actions with the LegalAction answer of status 201 and GET /legal-actions/{legalActionId} with the LegalAction answer of status 200, both under the base /api/recovery/litigation/v1 and owned by rwb-litigation
    Then action_type is declared against LOV-LEGAL-TYPE with the values NOTICE, CIVIL_CASE, APPEAL, ENFORCEMENT, BANKRUPTCY_PETITION and LED_AUCTION, and the action of the judgment this step traces against is CIVIL_CASE
    Then status is declared against LOV-LEGAL-STATUS with the values OPEN, FILED, JUDGMENT, ENFORCING, CLOSED and WITHDRAWN, and the step reads the status and writes none
    Then no property is added to the LegalAction element for an asset, a trace date, a trace source or an enforcement decision
    Then every other property of the element is copied from the baseline of the legal action and is not redefined here

  Scenario: AC2 The trace request and answer elements are fixed and no trace column is added (new, D-RCV-60)
    Given the trace sections of the baseline
    When they are compared with the enforcement step of RWB-S4-E5017-APP
    Then the request element carries the case reference, the legal action reference, the trace reference, the four sources (NCB, internal data, registries, insurers), the trace plan version and the rule package version in force
    Then the answer element carries the stage ASSET_TRACE or ENFORCEMENT_DECISION, the traced assets with asset_ref, asset_key, asset_code, transfer_in_type, from_segment and book_value, the source of each asset, the batch status and its date, the rule ID, the package version and the decided-at time
    Then the document states that the trace result is carried by the decision record and the answer and that no asset, trace date or source column is added to legal_action or hearing
    Then the document states that the enforcement decision, the writ, the deferral and the petition are the sibling stories' and declares no property for them
    Then the POST declares the Idempotency-Key header and its stored answer, and the GET declares none
    Then the field names the sources do not give are Not specified in the source documents (GAP-2818; ASM-4663) and the document marks them so

  Scenario: AC3 The five consumed rows are declared and their effects stay with their owners (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership rows and with the contracts of P1, P2, P10, P3 and P7
    Then the ACE asset rows of v_ace_npa_asset and the batch status of v_ace_batch_status are declared as consumed from P1 rwb-source-data, with the product, the batch date and the stale condition of VR-S4-017-1, and the document declares no view grant and no ACE table
    Then the NCB, registry and insurer answers are declared as consumed from P2 rwb-integration, one call per source, and the document declares no adapter, no credential and no file
    Then the trace plan with its sources and their order is declared as consumed from P10 rwb-agent, and the document declares no model call and no source order of its own
    Then the case move carrying ENFORCEMENT_OPENED, ASSET_TRACE or ENFORCEMENT_DECISION is declared as consumed and answered with rwb-case, and the document declares no recovery_case property
    Then the LITIGATION rule package with R-LIT-50 and R-LIT-52 at its version in force is declared as consumed from P7 rwb-decision
    Then the operation names of the five rows are Not specified in the source documents (GAP-2815, GAP-2816; ASM-4659, ASM-4660) and the rows carry the placeholder
    Then every call on the five rows is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The Idempotency-Key rule, the error envelope and the rights are fixed (new, D-RCV-60)
    Given the error and access sections of the baseline
    When they are compared with TSD S4 T-A.1, T-A.2 and T6.1
    Then the operations answer 400 for a malformed request, 401, 403 with MSG-P4-002, 404, 409 on a closed, withdrawn or wrong-stage action, 422 with MSG-GEN-001 and 503 when a downstream or the rule package does not answer, each with one envelope and one message ID per condition
    Then POST /cases/{caseId}/legal-actions declares Litigation right C and GET /legal-actions/{legalActionId} declares Litigation right R, each with the scope applied
    Then RW-LITOFF holds Litigation CRUA, RW-ENFORCE holds CRU, RW-HEADLIT and RW-PRODHEAD and RW-LEGAL hold RA, PT-LAWFIRM holds RU and every other role of TSD S4 T6.1 holds R
    Then the document states that the unattended trace runs under the rwb-litigation service identity with no person right and adds no right for it (GAP-2817; ASM-4662)
    Then a repeated POST with the same Idempotency-Key returns the stored answer and describes no second effect

  Scenario: AC5 The decision-record element and the stale-product message are declared (new, D-RCV-60)
    Given the decision section of the baseline
    When it is compared with the local decision-record library of DP-03 and with VR-S4-017-1
    Then one decision record is declared per rule outcome with the case reference, the legal action reference, the rule ID, the package version in force, the sources searched, the answer of each source, the traced assets, the outcome and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before the stage changes, and a failed write leaves the stage unchanged with MSG-P7-003
    Then MSG-P1-001 is declared with the product and the date it carries, and the document states that the stale condition is answered by P1 and never judged here
    Then the document declares no event of its own for the record and no second topic for this capability

  Scenario: AC6 The six contract fakes answer the document (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-source-data fake answers the ACE asset rows of case "RC-2026-001717", a current batch status and a stale product with its date
    Then the rwb-integration fake answers the NCB, registry and insurer answers of the case, an empty answer per source and an answer beyond 2 s
    Then the rwb-agent plan fake answers the trace plan with its four sources and their order
    Then the rwb-case fake answers the case states JUDGMENT_RECORDED and ASSET_TRACE and the moves ENFORCEMENT_OPENED, ASSET_TRACE and ENFORCEMENT_DECISION, with one move refused
    Then the rwb-decision rule-package fake answers the LITIGATION package at its version with R-LIT-50 and R-LIT-52
    Then the decision-record library stub answers a healthy chain and a stopped chain, and the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the ownership boundary are fixed and nothing else is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_litigation, the login is rwb_litigation, the topic is rwb.litigation.events.v1, the queue is rwb-litigation and the Java package is th.co.scb.ace.workbench.recovery.litigation
    Then the tables named as owned are legal_action and the library objects decision_record and idempotency_key, and v_ace_npa_asset, v_ace_batch_status, recovery_case, rule_row, decision_log_entry, document and hearing are named as other owners' or another story's and are consumed only through their contracts
    Then the document declares no event published, no event consumed and no Schedule for this step, and the absence test fails a build that adds one
    Then the document declares no read of a v_ace_* view, no grant on rwb_case or rwb_decision and no asset, trace date or source column, and the boundary and absence tests fail a build that adds one
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S4-E5017-APP and they copy no criterion of the legacy story, whose four criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The trace step, the stage states `ENFORCEMENT_OPENED`, `ASSET_TRACE` and `ENFORCEMENT_DECISION`, and the legal action are rwb-litigation's; the contract declares their vocabulary and their shapes on `legal_action` only | FSD S4 A2.17; TSD S4 T4; Ownership Map (legal_action and hearing owner S4) |
| BR2 | The decision record is declared as an element written before the stage changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S4 T2; legacy RWB-E5-017 AC1 and AC4 |
| BR3 | ACE data stays with rwb-source-data: the contract declares the asset and batch-status read as consumed, declares no `v_ace_*` grant and no ACE table | DP-05; VR-S4-017-1; GAP-2815 |
| BR4 | The external search stays with rwb-integration: the contract declares the bureau, registry and insurer answers as consumed and declares no adapter, credential or file | FSD S4 A2.17.2; GAP-2816 |
| BR5 | The trace plan is the agent's: the contract declares it as consumed and fixes no source order, no cost and no model call of its own | FSD S4 A2.17.2 (integration points NCB, Model gateway); GAP-2816 |
| BR6 | The case move is answered and not written: the contract declares the answer that carries the move and declares no `recovery_case` property and no case row write | Ownership Map (recovery_case owner P3); GAP-2818 |
| BR7 | The trace adds no table and no column: the result is the decision record and the answer, and no asset, trace date, source or enforcement-decision property is declared on `legal_action` or `hearing` | TSD S4 T3.1; GAP-2818 |
| BR8 | The unattended step carries no person right: the two operations declare C and R only, and no right is added for the trace itself | FSD S4 A2.17.3.3; TSD S4 T6.1; GAP-2817 |
| BR9 | A POST declares the `Idempotency-Key` and stores its answer; a GET declares none | TSD S4 T-A.2 |
| BR10 | The vocabulary is closed: `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS` are published as enumerated values and no state name or list value is a constant of the code | TSD S4 T3.2; BR-S4-017 (FSD S4 A2.17.3.1) |
| BR11 | No personal data in a schema, an example or a fake: identifiers, asset references, amounts, dates, list values and a rule version only | Template and Rules v1 §R7.2 (s17) |
| BR12 | One REST base, one topic, one queue and one login per service; the document never declares another service's base, topic or view as its own, and a schema change is additive within major version 1 | DP-13, DP-14; Template and Rules §R4; DP-11 |

### 9. State transitions

The lifecycle of this document, not of a legal action:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the trace elements, the consumed rows and the fakes are described | In review |
| In review | Consumer sign-off | The app story, SCR-19, SCR-20, the wave 3 harness and the rwb-source-data, rwb-integration, rwb-agent, rwb-case and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new error code | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a list value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence test of AC7 fails: an asset or `recovery_case` property, a `v_ace_*` grant, a second topic or a Schedule | In review |

The stage machine of `LitigationWorkflow` that the document describes is the app story's: `JUDGMENT_RECORDED` → `ASSET_TRACE` under R-LIT-50, → `ENFORCEMENT_DECISION` under R-LIT-52, and this baseline fixes the vocabulary and the shapes and moves nothing.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-litigation | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes |
| Consuming teams (the app story, SCR-19, SCR-20, the wave 3 harness and the owners of rwb-source-data, rwb-integration, rwb-agent, rwb-case, rwb-decision, rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme of the document is named "the rwb-litigation login (DP-02)" and is not part of this baseline. No approver of the DoA matrix and no person is a party to this document: the step is unattended and the enforcement decision is a sibling story's (BR8).

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| LegalAction element | The columns of DF-LEG-001 to DF-LEG-014: `id`, `case_id`, `law_firm_id`, `action_type`, `lawsuit_no`, `black_case_no`, `red_case_no`, `court_name`, `claim_amount`, `filed_date`, `judgment_date`, `judgment_amount`, `lit_status` and `status` |
| Trace request | The case reference, the legal action reference, the trace reference, the four sources, the trace plan version and the rule package version: the field names Not specified in the source documents (GAP-2818; ASM-4663) |
| Trace answer | The stage, the traced assets with `asset_ref`, `asset_key`, `asset_code`, `transfer_in_type`, `from_segment` and `book_value` (DF-ACE-208 to DF-ACE-219), the source of each asset, the batch status and its date, the rule ID, the package version and the decided-at time |
| Asset view | `v_ace_npa_asset` and `v_ace_batch_status` of P1, read through the owner's contract only and never queried as a view (GAP-2815; ASM-4659) |
| Case | DF-CAS-001 to DF-CAS-023 of `recovery_case` in `rwb_case`, answered by P3 with the move and never written here |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the stage changes (DP-03) |
| Rules | DF-REF-001 to DF-REF-015 of `rule_row` in `rwb_decision`, consumed through the package in force; R-LIT-50 and R-LIT-52 and their timers are governed there |
| Not written here | `hearing` (S4, the sibling stories'), `document` (P5), `decision_log_entry` and `rule_row` (P7) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC1 and the optionality rule of BR12. **No new table, no new column and no migration** is declared by this story: an asset, a trace date, a source and an enforcement decision have no home in `rwb_litigation` (BR7).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/legal-actions` | LegalActionRequest in, LegalAction of status 201 out, with the action type of `LOV-LEGAL-TYPE` (API-S4-002) | Litigation, right C, scope applied | `Idempotency-Key` header required; the answer is stored |
| GET | `/legal-actions/{legalActionId}` | LegalAction of status 200 out with its court facts, its judgment facts and its status (API-S4-003) | Litigation, right R, scope applied | Not applicable |

The two operations answer 400, 401, 403, 404, 409, 422 and 503, each with the error envelope and one message ID of section 14. The operation IDs are those of TSD S4 T-A.1; the paths are those of the target base and not the monolith form. API-S4-004 `PATCH /legal-actions/{legalActionId}` records a filing, a judgment or an enforcement step and belongs to the sibling stories, and API-S4-005 `POST /legal-actions/{legalActionId}/hearings` and API-S4-001 `POST /notices/{noticeId}/approve` belong to the hearing and notice stories; none of the three is declared by this baseline.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The ACE asset and batch-status read (operation name Not specified in the source documents (GAP-2815; ASM-4659)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The asset rows of `v_ace_npa_asset` and the batch status of the product for VR-S4-017-1; the view, its ingestion and the stale condition are P1's; faked |
| The bureau, registry and insurer search (operation name Not specified in the source documents (GAP-2816; ASM-4660)) | `/api/recovery/integration/v1` | P2 rwb-integration | The NCB, registry and insurer answers for the debtor, one call per source; the adapters are P2's; faked |
| The trace plan (operation name Not specified in the source documents (GAP-2816; ASM-4660)) | `/api/recovery/agent/v1` | P10 rwb-agent | The sources to search and their order, from FEAT-AGT-01; read, never computed here; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2818; ASM-4663)) | rwb-case (P3) | P3 rwb-case | The move `ENFORCEMENT_OPENED`, `ASSET_TRACE` or `ENFORCEMENT_DECISION` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The rule package in force (operation name Not specified in the source documents) | `/api/recovery/decision/v1` | P7 rwb-decision | The LITIGATION package at its version with R-LIT-50 and R-LIT-52; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The five rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-2815 and GAP-2816 with ASM-4659 and ASM-4660. The base of each consumed row is the owner's and is named here only to show that it is not this service's.

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and the ownership rows of this service list no event at all (context pack, ownership rows). DP-09 is not in the pattern set of this key: this baseline declares no event, adds no outbox row and widens no topic, and the decision record is relayed by the library of DP-03 on `rwb.decision-record.v1` and is not an event of this service.

#### 12.4 Events consumed

None. The ownership rows list no consumed event either, so the judgment answer arrives on the rwb-case contract of 12.2 and the four source answers arrive on their owners' contracts (GAP-2817; ASM-4661). This baseline declares no consumer group, no subscription and no inbox of its own, and the absence test of AC7 fails a build that adds one.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-litigation` in namespace `rwb-recovery` | The stage that hosts the trace step; its signals, its 10 and 5 working-day timers and its outcome for the parent are declared, not built |
| `traceAssets` | Activity, the opening and tracing step | `rwb-litigation` | The case, the legal action and the trace plan in; the source answers, the rule ID with its package version, the traced assets and the case move out |
| `presentEnforcementDecision` | Activity, the presentation step | `rwb-litigation` | The traced assets in; the enforcement decision view, the decision record and the case move out |

No model call and no external adapter exist in this service: the plan is P10's answer and the search is P2's. The activity names are target design choices and the trigger of the step is read as the judgment answer, because the legacy story says the trigger arrives while R-LIT-50 names a recorded judgment (GAP-2817; ASM-4661). No activity is registered by this story.

#### 12.6 Schedules

None. The step runs from the judgment answer and the source answers; the 10 and 5 working-day task timers of R-LIT-50 and R-LIT-52 are durable timers of the workflow. This baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table, and the ownership rows of this service list no job.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | The civil-case action of the judgment, its court facts and its status; read by the two operations and **not written** on the trace path (BR7) |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated POST and the answer it holds |

`v_ace_npa_asset` and `v_ace_batch_status` (P1), `recovery_case` (P3), `decision_log_entry` and `rule_row` (P7), `document` (P5) and `hearing` (S4, the sibling stories') are not owned by this baseline; it names them only as answers or a later story's table, and no foreign key leaves the schema (DP-01). **No table holds a traced asset, a trace date or a source**, and the baseline declares none.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data asset fake | The ACE asset rows of case `RC-2026-001717`, a current batch status and a stale product with its date | AC2, AC3, AC5, AC6 |
| rwb-integration search fake | The NCB, registry and insurer answers of the case, an empty answer per source and an answer beyond 2 s | AC2, AC3, AC6 |
| rwb-agent plan fake | The trace plan with its four sources and their order for case `RC-2026-001717` | AC2, AC3, AC6 |
| rwb-case case-move fake | The case states `JUDGMENT_RECORDED` and `ASSET_TRACE`; the moves `ENFORCEMENT_OPENED`, `ASSET_TRACE` and `ENFORCEMENT_DECISION` accepted, and one refused | AC2, AC3, AC6 |
| rwb-decision rule-package fake | The LITIGATION package at its version in force with R-LIT-50 and R-LIT-52 | AC3, AC5, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC5, AC6 |
| gateway-bff composite route fake | The merged SCR-19 and SCR-20 answer for case `RC-2026-001717`, with the address facts and the traced assets read once | AC2 |

The fakes are test-only and are replaced by the real services in SIT. The operation names and the element lists of the five consumed rows are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2815, GAP-2816; ASM-4659, ASM-4660).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 5 consumed | The create and read of the legal action on `/api/recovery/litigation/v1`; the ACE asset and batch read, the external search, the trace plan, the case-move answer and the rule package; one hop, 2 s |
| Kafka | None declared | No event published and none consumed by this step; the decision record is the library's on `rwb.decision-record.v1` |
| Temporal | 1 workflow and 2 activities declared, 0 registered | `LitigationWorkflow`, `traceAssets` and `presentEnforcementDecision` on `rwb-litigation`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no legal action, no case, no source answer and no rule package. What it publishes is one OpenAPI 3.1 document, one AsyncAPI fragment that declares no event, nine contract tables and six fakes.

**Deliverables.** The additive document `openapi/rwb-litigation-v1.yaml` for this step, the trace request and answer elements, the vocabulary of `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS` as published enumerations, the contract README rows for the five consumed rows and their placeholders, and the six WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-13 moves the base and nothing else. DP-03 is declared as the element and the transaction rule, not as a build. DP-05 is declared as the owner's read, because the architecture gives the views to rwb-source-data and grants none to S4 (GAP-2815; ASM-4659). DP-19 is behind SCR-19 and SCR-20, whose screen model is the edge contract's. DP-09, DP-16 and DP-20 are not in the pattern set of this key, which is why no event is declared, why the external search is a consumed row rather than a baseline of this service, and why the plan is consumed from P10.

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, while the plan's build list for this story is None; this baseline builds against their fakes until those platform contract stories publish. The five consumed rows are C dependencies in fact and not in the metadata row (GAP-2815, GAP-2816; ASM-4659, ASM-4660).

**Build steps**

1. Write the two operations and validate the additive rule of AC1 in the pipeline.
2. Write the trace request and answer elements of AC2 with the placeholder on the fields the sources do not give, and the statement that no asset, trace date or source column is added.
3. Record the five consumed rows of AC3 with their owner, their budget and their placeholders.
4. Record the error envelope, the rights and the `Idempotency-Key` rule of AC4, including the absence of a person right for the unattended trace.
5. Record the decision-record element and the stale-product message of AC5 and validate them against the library schema.
6. Publish the six fakes of AC6 and the drift test.
7. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the seven contract tests pass, the six fakes answer every consumed path and the drift test is green, and the app story, SCR-19, SCR-20 and the wave 3 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the litigation pack, which is the pack story of this service, so no path of this step raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key. It names the expiry of the claim on the case, which is the prescription story of this service, so no path of this step raises it | The claim on this case expires on {date}. File before then. |
| MSG-P1-001 | The data product behind the ACE asset read is stale after a late or failed batch (VR-S4-017-1) | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Litigation right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the stage changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The six message IDs are contract elements and the text is the legacy, FSD and platform wording, copied unchanged; no message is reworded and no new one is added. VR-S4-017-1 is the only validation rule of this key and it names the stale product, which is answered by P1 and reported here; the pack and prescription messages belong to the pack and prescription stories of this service.

### 15. Screens and states

The contract serves SCR-19 Litigation workspace in its judgment state and SCR-20 Enforcement workspace in its requested state through the gateway-bff composite route (DP-19). The route calls rwb-litigation for the legal action, the stage outcome and the traced assets, rwb-case for the case and its route state, rwb-integration for the source answers and rwb-decision for the rule package; this baseline fixes the rwb-litigation answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The states this step adds — traced, nothing found, stale data, not recorded, refused — read the messages of section 14 on the same route. The legacy screen table gives SCR-20 the states requested, seized, auctioned and closed; the trace adds no state to that list, and seized, auctioned and closed belong to the writ, auction and proceeds stories.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-017-01 | AC1, AC2 | Contract | Case `RC-2026-001717` and action `LA-2026-001717`; the contract half answers the two operations, the `CIVIL_CASE` action type, the statuses and the trace elements |
| TC-E5-017-02 | AC2, AC3 | Contract | The judgment recorded and the four sources; the contract half answers the trace request and answer and the P1 and P5 consumed rows |
| TC-E5-017-03 | AC2, AC3 | Contract | One traced asset and the enforcement decision; the contract half answers the asset elements, the case move to `ENFORCEMENT_DECISION` and the no-column statement |
| TC-E5-017-04 | AC5 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the record element |
| TC-E5-017-05 | AC4, AC7 | Contract | A role without the Litigation right and a malformed request; the contract half answers the 403 with MSG-P4-002, the 400 of the envelope and the absence of a person right for the trace |
| TC-E5-017-06 | AC5, AC6 | Contract | A forced decision-record failure and a drifted fake; the contract half answers the stopped chain and fails the build on the drift |
| TC-S4-E5017-CON-01 | AC1, AC2 | Contract | The document validates; the two operations, the base, the six action types, the six status values, the trace elements and the unchanged action are present, and no asset or trace column is added |
| TC-S4-E5017-CON-02 | AC2, AC4 | Contract | The trace request and answer validate; the `Idempotency-Key` rule and the seven error responses with one message ID per condition |
| TC-S4-E5017-CON-03 | AC3 | Contract | The five consumed rows validate with their owner, their placeholder fields and one hop with a 2 s budget |
| TC-S4-E5017-CON-04 | AC5, AC6, AC7 | Contract | The record element validates against the library schema; the six fakes match the document and a drifted fake fails the build; the absence test for an asset or `recovery_case` property, a held list value, a second topic and a Schedule |

The six legacy cases are the legacy cases of RWB-E5-017 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S4-E5017-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The four cases `TC-S4-E5017-CON-01` to `-04` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the 10 and 5 working-day timers, the four sources, the lists and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, asset references, amounts, dates, list values and a rule version only; every example is synthetic.
- ACE data stays with rwb-source-data: the document declares no `v_ace_*` grant and no ACE table, and the boundary test fails a build that adds one (BR3).
- The external search stays with rwb-integration and the plan with rwb-agent: the document declares no adapter, credential, file, model call or source order of its own (BR4, BR5).
- The case stays with rwb-case: the document declares no `recovery_case` property and no case row write (BR6).
- The trace adds no table and no column: no asset, trace date, source or enforcement-decision property is declared on `legal_action` or `hearing` (BR7).
- No person right for the unattended trace: the two operations declare C and R only, and no right is added for the trace itself (BR8).
- One base, one topic, one queue and one login per service; a document that names another service's base, topic or view as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-litigation; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence test of AC7 fails a build that declares an event, a Schedule, a Quartz row or a shared job table.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S4-007 | Enforcement after judgment has one named owner from judgment to the end of enforcement; the contract fixes the trace elements, the four sources and the case move on which the rule is evaluated (FSD S4 Requirements served); the legacy story master carries no requirement id | The two operations, the trace elements, the five consumed rows and the case move | TC-E5-017-01, TC-E5-017-02, TC-S4-E5017-CON-01, TC-S4-E5017-CON-02 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed rows with their budget and breaker | TC-S4-E5017-CON-03 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-017, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by RWB-S4-E5017-APP; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the four new contract cases TC-S4-E5017-CON-01 to -04 |
| Feature and screens | FEAT-LIT-17, SCR-19 Litigation workspace and SCR-20 Enforcement workspace |
| Rules | R-LIT-50 and R-LIT-52, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the two operations, the evaluation of R-LIT-50 and R-LIT-52, the decision record, the trace presentation and the case-move answer: RWB-S4-E5017-APP.
- The ACE views, their ingestion, the data product and the stale condition: rwb-source-data (P1), whose contract this baseline declares as consumed and faked (GAP-2815; ASM-4659).
- The NCB, registry and insurer adapters, their credentials and their files: rwb-integration (P2), whose contract this baseline declares as consumed and faked (GAP-2816; ASM-4660).
- The trace plan and the model that produces it: rwb-agent (P10), whose contract this baseline declares as consumed and faked.
- The case of record, its route state and the parent `CaseWorkflow`: rwb-case (P3), whose case-move answer this baseline declares as consumed and faked.
- The enforcement decision itself — the writ and seizure (R-LIT-54), the deferral (R-LIT-53 to R-LIT-57), the petition (R-LIT-58 to R-LIT-60) and the auction ladder (R-LIT-63 to R-LIT-67): the sibling stories of this service. **This baseline fixes the traced assets and the stage and decides nothing** (GAP-2818; ASM-4663).
- The creation of the legal action, its pack, the filing, the hearing calendar and the judgment: the sibling stories of this service.
- The authoring, testing, approval and versioning of the LITIGATION package and of the rule rows of R-LIT-50 and R-LIT-52, and their timers: rwb-decision (P7).
- The enforcement pack and its documents: rwb-document (P5).
- The rights, roles, scope and masking data themselves, and the gateway-bff composite route and the screen field list of SCR-19 and SCR-20: rwb-access and RWB-PLT-N001-CON.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
