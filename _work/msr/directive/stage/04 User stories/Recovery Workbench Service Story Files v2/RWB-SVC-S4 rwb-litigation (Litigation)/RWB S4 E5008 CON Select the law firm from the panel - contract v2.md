# RWB-S4-E5008-CON Select the law firm from the panel - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5008-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-S4-E5008-CON-16); the squad sizes it at refinement |
| Contract version | v1, the version of the base `/api/recovery/litigation/v1` |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped; traces to REQ-S4-004 and FEAT-LIT-08; the legacy master carries no requirement ID) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the firm-selection step of rwb-litigation, split from RWB-E5-008. It fixes the three legal-action operations on `/api/recovery/litigation/v1` (DP-13), the `law_firm_id` element of `LegalAction` and `LegalActionUpdate` and the closed vocabularies of `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS`, the consumed panel and decline reads of rwb-partner (S9), the case-move answer of rwb-case, the `Idempotency-Key` rule and the error envelope, and the decision-record element of DP-03. The panel is answered by rwb-partner and this contract declares no `partner` property (GAP-2773, GAP-2778; ASM-4607, ASM-4612); `PartnerResultSubmitted` is not consumed here (GAP-2774; ASM-4608); the score, capacity, court coverage and conflict fields and the operation names have no source specification and are carried with the placeholder. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S4-E5008-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 12 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead of rwb-litigation (S4)**, I want **the published contract baseline of the firm-selection step — the base `/api/recovery/litigation/v1` with API-S4-002 create, API-S4-003 read and API-S4-004 patch, the `LegalAction`, `LegalActionRequest` and `LegalActionUpdate` schemas with the `law_firm_id` element and no panel property, the two closed vocabularies of `action_type` and `status`, the consumed panel and decline reads of rwb-partner, the case-move answer to rwb-case, the `Idempotency-Key` rule, the error envelope, the declared right of each operation, the decision-record element, the tables and the fakes**, so that **RWB-S4-E5008-APP, the screens and the wave 3 harness build against one frozen, testable shape on Day 1 and a firm reference, a status value, a panel field or an answer shape can never drift between rwb-litigation, rwb-partner and rwb-case without a failing build**.

It owns the shapes and nothing that moves: the selection, the write of the firm, the decision record, the case-move answer and the re-selection are `RWB-S4-E5008-APP`'s; the panel, the scorecard, the capacity, the court coverage, the conflict status and the decline are rwb-partner's (S9) and `RWB-S4-E5009-APP`'s instruction; the case of record and its route states are rwb-case's (P3); the rule rows and the package version are rwb-decision's (P7).

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy step of RWB-E5-008 crossed three boundaries at once: a panel row, a case route state and a decision log row, all in one `recovery` schema and one process. The target splits them: the panel is rwb-partner's (S9), the case of record and the route states `FIRM_SELECTION` and `FIRM_DECLINED` stay with rwb-case (P3), and the legal action and the selected firm stay with rwb-litigation (S4). Each boundary is now a contract that another team builds against, so each has to be fixed before the app story starts: the `law_firm_id` element, the closed vocabularies, the panel read, the decline read and the case-move answer.

The baseline also fixes the naming that the checks require: schema `rwb_litigation`, base `/api/recovery/litigation/v1`, topic `rwb.litigation.events.v1` with retry and `.dlt` topics, task queue `rwb-litigation` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.litigation` (Architecture v5 slide 41 notes). It records that rwb-litigation holds no `v_ace_*` grant and no grant on `rwb_partner` (Architecture v5 slide 29), so DP-05 is declared as a prohibition and the panel and score facts are consumed on the owner's contract only. It records that `PartnerResultSubmitted` is an event of rwb-partner whose consumer row lists rwb-litigation while DP-09 is not in this key's pattern set, so this contract declares no consumed event and the decline arrives synchronously.

Three points are carried as gaps and assumptions rather than decided quietly: the plan gives the panel read, the decline read and the case-move answer no C row and no contract story (GAP-2773), the score, capacity, court coverage and conflict fields of a panel firm have no field list anywhere and the legacy `v_ace_score` read has no grant here (GAP-2778), and the rule rows of R-LIT-23 and R-LIT-27 with their weights, thresholds and window are governed in rwb-decision and named here only (GAP-2777).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `legal_action` and `hearing` are S4's, `partner` and `partner_instruction` are S9's, `recovery_case` is P3's, `decision_log_entry` and `rule_row` are P7's, `document` is P5's. This document never declares another service's operation as provided.
- The panel list operation of rwb-partner (API-S9-001 `GET /partners` "List partners with panel status and score", on base `/api/recovery/partner/v1`) and the instruction read that answers a decline (API-S9-003 and API-S9-004 of the partner set) are published, so the consumed rows of 12.2 name a real owner document; no plan slice gives them a story key and neither is in this story's contract-dependency row, which is None, so the absence is recorded (GAP-2773; ASM-4607).
- The case-move answer of rwb-case is fixed here as a shape only; no source names a published operation that moves a case state on behalf of a stage, and the name is Not specified in the source documents (GAP-2773; ASM-4607).
- The LITIGATION rule package, its rule rows for R-LIT-23 and R-LIT-27, its scorecard weights, capacity test, court coverage set, conflict check and 2-working-day window are governed in rwb-decision (P7); this baseline names them and declares none of them (GAP-2777; ASM-4611).
- The `legal_action` table and its columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-litigation for this step: the three operations with their request and answer elements, the closed vocabularies, the `law_firm_id` element, the rights and the six error responses.
2. Fix the firm element: `law_firm_id` (DF-LEG-003) on `LegalAction` and `LegalActionUpdate` as an identifier of the S9 partner, optional, with no panel property and no score property added to `legal_action`.
3. Fix the consumed panel read of rwb-partner and its facts — panel status, type, contract end, score, capacity, court coverage and conflict status — and mark the fields the sources do not give with the placeholder.
4. Fix the consumed decline read and the case-move answer of rwb-case: the move `FIRM_SELECTION` or `FIRM_DECLINED`, the rule ID, the version and the decided-at time, with no case row read or written here.
5. Record the decision-record element of DP-03 on `rwb.decision-record.v1`, written before the legal action changes.
6. Record the closed vocabulary of the action types and the action status, and the rule that no value is a constant of the code.
7. Publish the contract tables of section 12 and the five contract fakes.
8. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a `v_ace_*` read and of a `partner` or `recovery_case` property, and the drift between a fake and the document.
9. Tag the baseline and hand it to RWB-S4-E5008-APP, the screens and the wave 3 harness.
10. Trigger: the pack-approved fact for a case in PACK_VERIFIED is evaluated in one activity selectPanelFirm of LitigationWorkflow on queue rwb-litigation under the service identity, with no officer task on the happy path; the litigation officer acts on SCR-19 and on the re-selection path.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body or a request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC7 |
| X4 | The consumed panel read, the decline read or the case-move answer has a field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC2, AC3, AC4 |
| X5 | A value outside `LOV-LEGAL-TYPE` or `LOV-LEGAL-STATUS` appears in the document or in an example | The vocabulary test fails the build | None | AC1, AC8 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `partner` row or a `recovery_case` row | The review fails the baseline; the boundary test fails the build | None | AC8 |
| X7 | A POST is repeated with the same `Idempotency-Key` | The stored answer is returned and no second effect is described | None | AC2, AC5 |
| X8 | The rights of an operation are not the ones TSD S4 T-A.1 declares | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner documents of rwb-partner and rwb-case only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the operations, the vocabularies, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S4-E5008-APP, the screen and the wave 3 harness on Day 1, and the rwb-partner and rwb-case teams on the same day |
| Estimable | One OpenAPI document, one AsyncAPI fragment, nine contract tables, five fakes and four new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the firm-selection step of rwb-litigation

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of legal_action is S4, of partner and partner_instruction is S9 and of recovery_case is P3
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The three legal-action operations are declared with the firm element and the closed vocabularies (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-litigation is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /cases/{caseId}/legal-actions with the LegalAction answer of status 201, GET /legal-actions/{legalActionId} with the LegalAction answer of status 200 and PATCH /legal-actions/{legalActionId} with the LegalAction answer of status 200, all under the base /api/recovery/litigation/v1 and owned by rwb-litigation
    Then law_firm_id is declared on LegalAction and on LegalActionUpdate as an optional identifier of the S9 partner, and court_name is declared on LegalAction for the court coverage test
    Then action_type is declared against LOV-LEGAL-TYPE with the values NOTICE, CIVIL_CASE, APPEAL, ENFORCEMENT, BANKRUPTCY_PETITION and LED_AUCTION, and status is declared against LOV-LEGAL-STATUS with the values OPEN, FILED, JUDGMENT, ENFORCING, CLOSED and WITHDRAWN
    Then no property is added to the LegalAction element for a panel, a panel status, a score, a capacity, a court coverage set, a conflict status or a case state, and every other property of the element is copied from the baseline of the legal action and is not redefined here

  Scenario: AC2 The selection and re-selection shapes are fixed on the patch (new, D-RCV-60)
    Given the selection sections of the baseline
    When they are compared with the firm-selection step of RWB-S4-E5008-APP
    Then the selection is PATCH /legal-actions/{legalActionId} with a LegalActionUpdate that carries law_firm_id, the case reference, the rule ID, the package version in force and the outcome code
    Then its answer is a LegalAction that carries the same law_firm_id, the rule ID, the package version and the decided-at time, and no case state
    Then the re-selection of R-LIT-27 uses the same element and the same operation, and the document declares that status is not moved by a selection or a re-selection
    Then the POST declares the Idempotency-Key header and its stored answer, and the GET and the PATCH declare none
    Then the field names of LegalActionUpdate beyond the facts the sources give are Not specified in the source documents (GAP-2778; ASM-4612) and the document marks them so

  Scenario: AC3 The consumed panel and decline reads of rwb-partner are declared and the panel stays there (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with API-S9-001, API-S9-003 and API-S9-004 of the partner set, and with the Ownership Map
    Then the panel list is declared as consumed from S9 rwb-partner with the partner reference, the partner code, the partner type, the panel status, the contract end, the score, the capacity, the court coverage and the conflict status of each firm
    Then the instruction read that answers a decline is declared as consumed from S9 rwb-partner, and the instruction itself is named as RWB-S4-E5009-APP's and rwb-partner's
    Then the operation names of the two rows and the field list of the score, capacity, court coverage and conflict facts are Not specified in the source documents (GAP-2773, GAP-2778; ASM-4607, ASM-4612) and the rows carry the placeholder
    Then the document declares no partner property, no partner_instruction property and no write of a partner row from rwb-litigation
    Then every call on the two rows is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The case-move answer is declared and the case row is never written here (new, D-RCV-60)
    Given the case boundary of the baseline
    When it is compared with rwb-case as the owner of recovery_case and of the route states
    Then the case move is declared as an answer to rwb-case with the move FIRM_SELECTION or FIRM_DECLINED, the rule ID, the package version and the decided-at time
    Then the document declares no recovery_case property, no case route-state column and no write of a case row from rwb-litigation
    Then the answer carries the stage outcome that the parent CaseWorkflow applies, and the operation name of a REST case-move call for another caller is Not specified in the source documents (GAP-2773; ASM-4607)
    Then the states PACK_VERIFIED, FIRM_SELECTION, FIRM_INSTRUCTED and FIRM_DECLINED are named as the case of record's and are read from its answer only

  Scenario: AC5 The Idempotency-Key rule, the error envelope and the rights are fixed (new, D-RCV-60)
    Given the error and access sections of the baseline
    When they are compared with TSD S4 T-A.1 and T-A.2 and with TSD S4 T6.1
    Then the operations answer 400 for a malformed request, 401, 403 with MSG-P4-002, 404, 409 on a closed, withdrawn or wrong-type action, 422 with MSG-GEN-001 and 503 when a downstream does not answer, each with one envelope and one message ID per condition
    Then POST /cases/{caseId}/legal-actions declares Litigation right C, GET /legal-actions/{legalActionId} declares Litigation right R and PATCH /legal-actions/{legalActionId} declares Litigation right U, each with the scope applied
    Then RW-LITOFF holds Litigation CRUA, RW-ENFORCE holds CRU, RW-LEGAL and RW-PRODHEAD and RW-HEADLIT hold RA, PT-LAWFIRM holds RU and every other role of TSD S4 T6.1 holds R
    Then the feature runs unattended under the service identity, and that identity is subject to the same declared rights
    Then a repeated POST with the same Idempotency-Key returns the stored answer and describes no second effect

  Scenario: AC6 The decision-record element is declared and written before the change (new, D-RCV-60)
    Given the decision section of the baseline
    When it is compared with the local decision-record library of DP-03
    Then one decision record is declared per selection and per re-selection with the case reference, the legal action reference, the rule ID, the package version in force, the ranked shortlist reference, the selected firm, the outcome, the case move and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before the legal action changes, and a failed write leaves the action unchanged with MSG-P7-003
    Then the document declares no event of its own for the record and no second topic for this capability
    Then the record carries identifiers, codes, scores, dates and a rule version only

  Scenario: AC7 The five contract fakes answer the document (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-partner panel fake answers the panel for case "RC-2026-000805" with a firm that covers the court and has capacity, a firm that fails the conflict check, a firm that fails the capacity test, no firm that covers the court, and no answer beyond 2 s
    Then the rwb-partner instruction fake answers the instruction of "LA-2026-000805" declined with the next firm on the scorecard, an instruction accepted inside the window, and a refusal for a firm outside the panel
    Then the rwb-case fake answers the case states PACK_VERIFIED and FIRM_INSTRUCTED and an accepted and a refused case move
    Then the rwb-decision rule-package fake answers the LITIGATION package at its version with R-LIT-23 and R-LIT-27, and the earlier version of the package
    Then the decision-record library stub answers a healthy chain and a stopped chain
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC8 The naming baseline and the boundary are fixed and no cross-schema read is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_litigation, the login is rwb_litigation, the topic is rwb.litigation.events.v1, the queue is rwb-litigation and the Java package is th.co.scb.ace.workbench.recovery.litigation
    Then the tables named as owned are legal_action and the library objects decision_record and idempotency_key, and partner, partner_instruction, recovery_case, proceeds, decision_log_entry, rule_row, document and hearing are named as other owners' or another story's and are consumed only through their contracts
    Then the document declares no read of a v_ace_* view and no grant on rwb_partner or rwb_case or any other rwb_* schema, and the boundary test fails a build that adds one
    Then the document declares no event published, no event consumed and no Schedule for this step, and the absence test fails a build that adds one
    Then the decision level D7 of R-LIT-23 and R-LIT-27, their weights, thresholds and window are named as rwb-decision's and declared nowhere in the document
```

These nine criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S4-E5008-APP and they copy no criterion of the legacy story, whose four criteria stay with the app story word for word.

Scenario: AC9 Each business rule BR1 to BR12 of section 8 is answered by a test in section 16, or by a guardrail or boundary test where the rule is an architecture constraint (new, D-RCV-60)

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The legal action and the selected firm are rwb-litigation's, and the contract declares `law_firm_id`, the vocabularies and the outcome fields on `legal_action` only | Architecture v5 slide 41; Ownership Map (legal_action owner S4); TSD S4 T3.1 and T3.2 |
| BR2 | The decision record is declared as an element written before the legal action changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S4 T2; legacy RWB-E5-008 AC1 and AC4 |
| BR3 | The panel stays with rwb-partner: the contract declares the panel and the decline as consumed, declares no `partner` or `partner_instruction` property, and describes no score, panel status or conflict write of rwb-litigation | Ownership Map (partner and partner_instruction owner S9); TSD S9 T3.1 and API-S9-001; GAP-2778 |
| BR4 | The case move is answered and not written: the contract declares the answer that carries `FIRM_SELECTION` or `FIRM_DECLINED` and declares no `recovery_case` property and no case row write | Ownership Map (recovery_case owner P3); Architecture v5 slide 41; GAP-2773 |
| BR5 | No ACE view and no ACE table is read: the panel and score facts are consumed on the owner's contract, and the service holds no `v_ace_*` grant | DP-05; Architecture v5 slides 29 and 41 |
| BR6 | A POST declares the `Idempotency-Key` and stores its answer; a GET and a PATCH declare none | Architecture v5 slide 11; TSD S4 T-A.2 |
| BR7 | The vocabulary is closed: `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS` are published as enumerated values and no state name, list value, weight, threshold or window is a constant of the code or a schema default | TSD S4 T3.2; BR-S4-008 (FSD S4 A2.8.3.1) |
| BR8 | No personal data in a schema, an example or a fake: identifiers, codes, scores, dates, list values and a rule version only | Architecture v5 slide 42 notes; Template and Rules v1 §R7.2 (s17) |
| BR9 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR10 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR11 | The document lists only operations owned by rwb-litigation; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-11 |
| BR12 | The rule rows of R-LIT-23 and R-LIT-27, their weights, thresholds, court set, conflict check and window, and the D7 decision level are governed in rwb-decision and named here, never declared here; until rwb-decision publishes them, the package is loaded on a rule-package-in-force signal whose name is Not specified in the source documents (GAP-2777), and its values are carried as data, never as constants | GAP-2777; ASM-4611; Business Rules and Routing Logic v4 |

**Rule coverage.** BR1 and BR7: AC1 and AC2 (TC-S4-E5008-CON-01 and TC-S4-E5008-CON-02); BR2: AC6 (TC-E5-008-05, TC-E5-008-06 and TC-S4-E5008-CON-04); BR3 and BR4: AC3 and AC4 (TC-S4-E5008-CON-03); BR5 and BR11: AC3, AC7 and AC8 (TC-S4-E5008-CON-03 and -04); BR6: AC5 (TC-S4-E5008-CON-02); BR8, BR9 and BR12: AC8 (TC-S4-E5008-CON-04); BR10: AC1 (TC-S4-E5008-CON-01).

### 9. State transitions

The lifecycle of this document, not of a legal action:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The three operations, the vocabularies, the firm element, the consumed rows and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the screen, the wave 3 harness and the rwb-partner, rwb-case and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new error code | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a list value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence test of AC8 fails: a `v_ace_*` view, a `partner` or `recovery_case` property, a second topic or a Schedule | In review |

The status machine of `legal_action` that the document describes is the app story's: `LOV-LEGAL-STATUS` is OPEN, FILED, JUDGMENT, ENFORCING, CLOSED and WITHDRAWN, and a selection or a re-selection writes `law_firm_id` and moves no status; this baseline fixes the vocabulary and moves no action and no case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-litigation | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes |
| Consuming teams (the app story, the screen, the wave 3 harness and the owners of rwb-partner, rwb-case, rwb-decision, rwb-access and rwb-source-data) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme of the document is named "the rwb-litigation login (DP-02)" and is not part of this baseline.

The rights of the three operations are checked by the rwb-access authorise check of DP-08; the call and its operation name are Not specified in the source documents (DOR-RWB-S4-E5008-CON-6).

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| LegalAction element | The columns of DF-LEG-001 to DF-LEG-014: `id`, `case_id`, `law_firm_id`, `action_type`, `lawsuit_no`, `black_case_no`, `red_case_no`, `court_name`, `claim_amount`, `filed_date`, `judgment_date`, `judgment_amount`, `lit_status` and `status` | DF-LEG-001 to DF-LEG-014 |
| Firm element | `law_firm_id` (DF-LEG-003), an identifier of the S9 partner, optional on the action and on the update; no other property is added for a selection | DF-LEG-003 |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the action changes (DP-03) | DF-DEC-001 to DF-DEC-018 |
| Partner | DF-PRT-001 to DF-PRT-007 of `partner` in `rwb_partner`, read only through the S9 owner and never written, copied or joined here | DF-PRT-001 to DF-PRT-007 |
| Partner instruction | DF-PRT-008 to DF-PRT-016 of `partner_instruction` in `rwb_partner`, read only through the S9 owner, and the instruction itself is `RWB-S4-E5009-APP`'s | DF-PRT-008 to DF-PRT-016 |
| ACE score facts | DF-ACE-270 to DF-ACE-279 of `v_ace_score`, not read: this service holds no `v_ace_*` grant (DP-05) | DF-ACE-270 to DF-ACE-279 |
| Not written here | `recovery_case` (P3), `document` (P5), `decision_log_entry` and `rule_row` (P7), `hearing` (S4, the sibling stories') | Not specified in the source documents (DOR-RWB-S4-E5008-CON-7) |
| Panel facts | The score, the capacity, the court coverage and the conflict status of a firm: Not specified in the source documents (GAP-2778; ASM-4612) | Not specified in the source documents (DOR-RWB-S4-E5008-CON-7) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabularies of AC1 and the optionality rule of BR10. **No new table, no new column and no migration** is declared by this story.

Reference data: the vocabularies above are read under the reference-data contract of DP-06 and DP-07; the parameters read are Not specified in the source documents (DOR-RWB-S4-E5008-CON-20).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/legal-actions` | LegalActionRequest in, LegalAction of status 201 out, with the action type of `LOV-LEGAL-TYPE` (API-S4-002) | Litigation, right C, scope applied | `Idempotency-Key` header required; the answer is stored |
| GET | `/legal-actions/{legalActionId}` | LegalAction of status 200 out with `law_firm_id`, `court_name` and `status` (API-S4-003) | Litigation, right R, scope applied | Not applicable |
| PATCH | `/legal-actions/{legalActionId}` | LegalActionUpdate in, LegalAction out with the selected firm (API-S4-004) | Litigation, right U, scope applied | Idempotency-Key header required |

The three operations answer 400, 401, 403, 404, 409, 422 and 503, each with the error envelope and one message ID of section 14. The operation IDs are those of TSD S4 T-A.1; the paths are those of the target base and not the monolith form. API-S4-001 `POST /notices/{noticeId}/approve` and API-S4-005 `POST /legal-actions/{legalActionId}/hearings` belong to the notice and hearing stories of this service and are not declared by this baseline.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The panel list operation, API-S9-001 `GET /partners` (operation name of the S9 contract Not specified in the source documents (GAP-2773; ASM-4607)) | `/api/recovery/partner/v1/partners` | S9 rwb-partner | The panel of firms with the partner reference, code, type, panel status, contract end, score, capacity, court coverage and conflict status; faked |
| The instruction read that answers a decline, API-S9-003 and API-S9-004 of the partner set (operation name Not specified in the source documents (GAP-2773; ASM-4607)) | `/api/recovery/partner/v1` | S9 rwb-partner | The decline of the instruction of the case, which is the fact of R-LIT-27; the instruction, its pack and its clock are `RWB-S4-E5009-APP`'s and the partner stories'; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2773; ASM-4607)) | rwb-case (P3) | P3 rwb-case | The move of the case of record to `FIRM_SELECTION` or `FIRM_DECLINED` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). None of the three is a contract dependency of this story, whose C row is None, and the panel and decline rows additionally have no contract story in the plan; the absence is recorded as GAP-2773 with ASM-4607.

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and its three catalogue events `LawsuitFiled`, `JudgmentRecorded` and `AuctionResult` belong to the stories that own the filing, the judgment and the auction result. This baseline declares none of them, adds no outbox row and widens no topic; the decision record is relayed by the library of DP-03 on `rwb.decision-record.v1` and is not an event of this service.

#### 12.4 Events consumed

None. `PartnerResultSubmitted` is produced by rwb-partner on `rwb.partner.events.v1` and its consumer row lists rwb-litigation, rwb-asset and rwb-case, but DP-09 is not in the pattern set of this key, the S4 IN row of Architecture v5 slide 19 names the event without assigning it to this step, and no source states that a decline of an instruction is its trigger (GAP-2774; ASM-4608). The decline therefore arrives on the rwb-partner contract of 12.2 and the case state on the rwb-case answer; this baseline declares no consumer group, no subscription and no inbox of its own, and the trigger of the step is a workflow step rather than an event (GAP-2775; ASM-4609).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-litigation` | The stage that hosts the firm-selection step; its signals and its outcome for the parent are declared, not built |
| `selectPanelFirm` | Activity, the one firm-selection step | `rwb-litigation` | The case and the legal action in; the rule ID with its package version, the selected firm, the ranked shortlist and the case move out |

`issueInstruction` is rwb-partner's activity on queue `rwb-partner` and is declared here as another owner's, never as this service's. The activity name is a target design choice, and the trigger of the step is read as the arrival of the pack-approved fact for a case in `PACK_VERIFIED`, because the legacy story says the step runs unattended while the FSD declares no background event (GAP-2775; ASM-4609). No activity is registered by this story.

Workflow ID form of `LitigationWorkflow`: Not specified in the source documents (CG-ALL-9178). Start rule and duplicate-start policy: Not specified in the source documents (CG-ALL-9178). The catalog trigger reads: 'Litigation route approved (R-LIT-01), or a restructure or settlement plan breaks (R-LIT-02)'.

#### 12.6 Schedules

None. The step runs from the pack-approved fact and from the decline the partner contract answers, and the 2-working-day window of R-LIT-27 is a durable timer of the step, not a Schedule; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table, and no Job of Architecture v5 slide 44 is owned or moved here.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | The action, its court, its selected firm and its status; the table the three operations read and the firm write patches |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked decision record of the selection and of the decline (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated POST and the answer it holds |

`partner` and `partner_instruction` (S9), `recovery_case` (P3), `decision_log_entry` and `rule_row` (P7), `document` (P5) and `hearing` (S4, the sibling stories') are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-partner panel fake (API-S9-001) | The panel for case `RC-2026-000805`: a firm that covers the court and has capacity, a firm that fails the conflict check, a firm that fails the capacity test, no firm that covers the court, and no answer beyond 2 s | AC1, AC3, AC7 |
| rwb-partner instruction fake | The instruction of `LA-2026-000805` declined with the next firm on the scorecard; an instruction accepted inside the window; a refusal for a firm outside the panel | AC3, AC7 |
| rwb-case case-move fake | The case states `PACK_VERIFIED` and `FIRM_INSTRUCTED`; an accepted move and a refused move | AC4, AC7 |
| rwb-decision rule-package fake | The LITIGATION package at its version in force with R-LIT-23 and R-LIT-27, and the earlier version of the package | AC6, AC7 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC6, AC7 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the three consumed rows, the panel facts and the case-move answer are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2773, GAP-2778; ASM-4607, ASM-4612).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 3 consumed | The create, read and patch of the legal action on `/api/recovery/litigation/v1`; the panel read and the decline read of rwb-partner, and the case-move answer; one hop, 2 s |
| Kafka | None declared | No event published and none consumed by this step; the decision record is the library's on `rwb.decision-record.v1` |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `LitigationWorkflow` and `selectPanelFirm` on `rwb-litigation`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no legal action, no case, no panel row and no rule package. What it publishes is one OpenAPI 3.1 document, one AsyncAPI fragment that declares no event, nine contract tables and five fakes.

**Deliverables.** The additive document `openapi/rwb-litigation-v1.yaml` for this step, the `law_firm_id` element on `LegalAction` and `LegalActionUpdate`, the vocabularies of `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS` as published enumerations, the contract README rows for the consumed rows and their placeholders, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is declared as a prohibition here: the document declares no `v_ace_*` read and no grant on the S9 owner's schema, because rwb-litigation holds neither (Architecture v5 slides 29 and 41; GAP-2778; ASM-4612). DP-13 moves the base and nothing else. DP-19 is behind SCR-19, whose screen model is the edge contract's. DP-09 is not in the pattern set of this key, which is why no event is declared in 12.3 or 12.4. The decline is read on the rwb-partner contract and not as an event; a consumed event row is added only if the solution architect adds rwb-litigation as a consumer of `PartnerResultSubmitted`, and that adds one consumed event row, one inbox subscription, one fake and one AC clause, with no schema change.

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, while the plan's build list for this story is None; this baseline builds against their fakes until those platform contract stories publish. The panel read, the decline read and the case-move answer are C dependencies in fact and not in the metadata row, and no plan slice gives the two partner rows a contract story key (GAP-2773; ASM-4607). This story and the app story name the panel list of rwb-partner (API-S9-001), the decline reads of rwb-partner (API-S9-003 and API-S9-004) and the case-move answer of rwb-case as consumed rows, build against their published documents and fakes on Day 1 with a call budget and a breaker, the budget Not specified in the source documents (GAP-2773), and step D1 decides whether a C row and a partner contract story are added to the plan; no metadata row is changed by this baseline.

**Build steps**

1. Write the three operations and validate the additive rule of AC1 in the pipeline.
2. Write the `law_firm_id` element of AC2 with the placeholder on the fields the sources do not give.
3. Record the two rwb-partner consumed rows and the panel facts of AC3 with their owner, their budget and their placeholders.
4. Record the case-move answer of AC4 and the absence test for a `recovery_case` property.
5. Record the error envelope, the rights and the `Idempotency-Key` rule of AC5.
6. Record the decision-record element of AC6 and validate it against the library schema.
7. Publish the five fakes of AC7 and the drift test.
8. Record the naming baseline and the boundary of AC8, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the eight contract tests pass, the five fakes answer every consumed path and the drift test is green, and the app story, the screen and the wave 3 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the litigation pack, which is the pack story of this service, so no path of this step raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key. It names the expiry of the claim on the case, which is the prescription fact of this service, so no path of this step raises it | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Litigation right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the legal action changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The data product of the source is stale after a late or failed ACE batch, which is VR-S4-008-1 of the FSD; the check is the owner's and this service holds no ACE batch status read | {product} is from {date}. Today's load has not arrived. |

The six message IDs are contract elements and the text is the legacy wording, copied unchanged, except MSG-P1-001, whose text is copied from Error and Message Standard v4 (CG-ALL-9180); no message is reworded and no new one is added. MSG-P1-001 is carried because it is in the message set of this feature, and no path of this service raises it (GAP-2779; ASM-4613).

### 15. Screens and states

The contract serves SCR-19 Litigation workspace in its pack, selected, declined, instructed, filed, hearing and judgment states, through the gateway-bff composite route (DP-19). The route calls rwb-litigation for the legal action and the selected firm, rwb-case for the case and its route state and rwb-partner for the panel and the instruction; this baseline fixes the rwb-litigation answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The refusal and failure states the app story shows — not recorded, refused, stale data — read the messages of section 14 on the same route. The empty, loading and error states of SCR-19 are Not specified in the source documents (DOR-RWB-S4-E5008-CON-10; CG-ALL-9182); the no access state is the refusal of MSG-P4-002 on the same route. MSG-P1-001 is shown on SCR-19 where the owner reports staleness.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-008-01 | AC1, AC2 | Contract | The panel for case `RC-2026-000805`; the contract half answers the three operations, the firm element and the vocabularies |
| TC-E5-008-02 | AC2, AC5 | Contract | Action `LA-2026-000805` with no firm; the contract half answers the patch of `law_firm_id` under R-LIT-23, the rights and the `Idempotency-Key` of the POST |
| TC-E5-008-03 | AC2, AC3 | Contract | The instruction declined with the next firm on the scorecard; the contract half answers the re-selection on the same element and the two rwb-partner consumed rows |
| TC-E5-008-04 | AC5, AC8 | Contract | A role without the Litigation right and a malformed request; the contract half answers the 403 with MSG-P4-002 and the 400 of the envelope |
| TC-E5-008-05 | AC5, AC6 | Contract | RW-LITOFF holds CRUA and RW-ENFORCE holds CRU; the contract half answers the rights of AC5 and the decision-record element of AC6 |
| TC-E5-008-06 | AC6, AC7 | Contract | The decision-record stub stopped and a panel with no firm that covers the court; the contract half answers the MSG-P7-003 path and the fakes of AC7 |
| TC-S4-E5008-CON-01 | AC1 | Contract | The document validates; the three operations, the base, the `law_firm_id` element, the six action types and the six status values are present, and no panel or case property is added |
| TC-S4-E5008-CON-02 | AC2, AC5 | Contract | The `LegalActionUpdate` and case-move elements validate; the `Idempotency-Key` rule and the seven error responses with one message ID per condition |
| TC-S4-E5008-CON-03 | AC3, AC4 | Contract | The two rwb-partner consumed rows and the case-move answer validate with their placeholder fields marked and one hop with a 2 s budget |
| TC-S4-E5008-CON-04 | AC6, AC7, AC8 | Contract | The decision-record element validates against the library schema; the five fakes match the document and a drifted fake fails the build; the absence test for a `v_ace_*` read, a `partner` or `recovery_case` property, a second topic and a Schedule |
| TC-S4-E5008-CON-05 | AC8 | Contract | The three tables of 12.7 (`legal_action`, `decision_record`, `idempotency_key`) are answered by the contract; no table of `partner`, `partner_instruction`, `recovery_case`, `decision_log_entry`, `rule_row`, `document` or `hearing` is declared as owned |
| TC-S4-E5008-CON-06 | AC9 | Contract | Not specified in the source documents (NEWAC-RWB-S4-E5008-CON-AC9); the rule coverage line of section 8 names the case for each of BR1 to BR12 |

The six legacy cases are the legacy cases of RWB-E5-008 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S4-E5008-APP. The legacy table carries no level column, and the artefact under test is the contract, so every row maps to `Contract`. The six cases `TC-S4-E5008-CON-01` to `-06` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the scorecard weights, the capacity test, the court coverage set, the conflict check, the 2-working-day window, the D7 level and the lists stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, codes, scores, dates, list values and a rule version only; every example is synthetic.
- The panel stays with rwb-partner and the case with rwb-case: the document declares no `partner`, `partner_instruction` or `recovery_case` property, no panel write and no case row write (BR3, BR4).
- ACE data only through the owner's contract: the document declares no `v_ace_*` view and no grant on `rwb_partner`, `rwb_case` or any other `rwb_*` schema, and the boundary test fails a build that adds one (DP-05).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-litigation; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence test of AC8 fails a build that declares a `v_ace_*` read, a second topic, a Schedule, a Quartz row or a shared job table.
- The error envelope, the `Idempotency-Key` rule and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S4-004 | A law firm is selected from the panel by rule using panel performance, and instructed through the partner portal; the contract fixes the firm element, the panel read and the case-move answer on which the rule is evaluated (FSD S4 requirements served; Business Requirements Program v5); the legacy story master carries no requirement ID (GAP-2776; ASM-4610) | The three operations, the `law_firm_id` element, the vocabularies, the two rwb-partner consumed rows and the case-move answer | TC-E5-008-01, TC-E5-008-03, TC-S4-E5008-CON-01, TC-S4-E5008-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows with their budget and breaker | TC-S4-E5008-CON-02, TC-S4-E5008-CON-03 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-008, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by RWB-S4-E5008-APP; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the four new contract cases TC-S4-E5008-CON-01 to -04 |
| Feature and screen | FEAT-LIT-08, SCR-19 Litigation workspace |
| Rules | R-LIT-23 and R-LIT-27, named from the Business Rules and Routing Logic v4 and governed in rwb-decision (GAP-2777) |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the three operations, the evaluation of R-LIT-23 and R-LIT-27, the decision record, the firm write and the case-move answer: RWB-S4-E5008-APP.
- The panel, the scorecard, the capacity, the court coverage, the conflict check and the decline record: rwb-partner (S9), its panel and instruction operations and its own stories. **The panel is answered by rwb-partner, and no part of this baseline moves it** (GAP-2773, GAP-2778; ASM-4607, ASM-4612).
- The issue of the instruction, its pack and its clock: `RWB-S4-E5009-APP` and rwb-partner.
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose case-move answer this baseline declares as consumed and faked.
- The escalation of R-LIT-25 and the nomination and panel-widening paths of R-LIT-26: the sibling stories of this service.
- The authoring, testing, approval and versioning of the LITIGATION package, of the rule rows of R-LIT-23 and R-LIT-27 and of their weights, thresholds and window, and the D7 decision level: rwb-decision (P7) (GAP-2777; ASM-4611).
- The pack and its documents, the ACE score and batch facts, the freshness of the data product and the interaction ledger: rwb-document (P5) and rwb-source-data (P1).
- The gateway-bff composite route and the screen field list of SCR-19: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
