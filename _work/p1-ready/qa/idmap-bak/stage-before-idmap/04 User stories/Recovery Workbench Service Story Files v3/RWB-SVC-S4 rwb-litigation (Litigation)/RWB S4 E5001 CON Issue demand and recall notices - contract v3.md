# RWB-S4-E5001-CON Issue demand and recall notices - contract

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5001-CON |
| Readiness decisions | RD-P1-001, RD-P1-004 |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Notice slice | The notice contract, its fake and its schema, published before wave 2 (GAP-1741); the rest of the capability is built in wave 3 against the same contract |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-001 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement; not specified in the source documents (DOR-RWB-S4-E5001-CON-16) |
| Contract version | v1 on `/api/recovery/litigation/v1` (served) and on `/api/recovery/comms/v1` (consumed) |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | Consumed, non-blocking C rows: the P6 notice generate and send (operation name: Not specified in the source documents (GAP-2743)); the rwb-case stage answer (name: Not specified in the source documents (GAP-2743)) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Version 3 changes**

- D-RCV-60 P1 developer readiness (RD-P1 register). Aligned the notices contract Problem codes and replay counting with the application story.


**Change log.** D-RCV-60, 22 November 2026: contract baseline of the notice step of rwb-litigation, split from RWB-E5-001. It fixes the three legal-action and notice operations on `/api/recovery/litigation/v1` (DP-13), the `NOTICE` action type and the stage vocabulary of the notice step, the create, read and approve shapes, the `Idempotency-Key` rule and the error envelope, the consumed notice fact of rwb-comms (P6) and the stage answer of rwb-case, and the decision-record element of DP-03. The notice row, the templates and the WIN dispatch stay with rwb-comms (GAP-2743; ASM-4558); the consumed operation names and the case answer have no source specification and carry the placeholder (GAP-2743; ASM-4559); the requirement trace and the approval gate are resolved by assumption (ASM-4561, ASM-4562). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S4-E5001-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 13 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the notice step of rwb-litigation — the legal-action and notice operations on `/api/recovery/litigation/v1`, the `NOTICE` action type and the notice stage vocabulary, the create, read and approve shapes, the `Idempotency-Key` rule, the error envelope and the rights, the consumed notice fact of rwb-comms, the stage answer of rwb-case, the decision-record element, the tables and the fakes**, so that **the app story, the screen and the tests of this legacy key build against one fixed, testable contract on Day 1 and an action type, a stage name, a notice state or an answer shape can never drift between rwb-litigation, rwb-comms and rwb-case without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy notice step of RWB-E5-001 crossed three boundaries at once: the notice and its template, the litigation stage and the decision record. The target splits them: the notice row, the template, the rendering, the D7.1 approval and the WIN dispatch stay with rwb-comms (P6), which TSD S4 T5.2 names as "P6 for notices" and whose FSD module scope is "letters, notices, SMS, LINE, proof of delivery" with the dispatch job JOB-10; the case of record and its route state stay with rwb-case (P3); the `NOTICE` legal action and its stage stay with rwb-litigation (S4). Each boundary is now a contract another team builds against, so each has to be fixed before the app story starts.

The baseline also fixes the naming the checks require: schema `rwb_litigation`, base `/api/recovery/litigation/v1`, topic `rwb.litigation.events.v1` with retry and `.dlt` topics, task queue `rwb-litigation` and Java package `th.co.scb.ace.workbench.recovery.litigation` (Architecture v5 slide 41 notes). It records that the service holds no grant on another `rwb_*` schema and no `v_ace_*` grant (Architecture v5 slide 29), so the notice and the template are consumed on the owner's contract only and never copied into `rwb_litigation`. No view and no ACE table is read by this service: source data comes only through the rwb-source-data contract (P1); its contract fields, the LIT view names and the freshness response are Not specified in the source documents (GAP-1736).

Four points are carried as a gap and its assumptions rather than decided quietly: the owner of the notice row and of the template rows while `POST /notices/{noticeId}/approve` is an operation of this service (ASM-4558, ASM-4560), the name of the consumed P6 operations and of the case answer (ASM-4558, ASM-4559), the reading of "no person in the path" against the built D7.1 approval (ASM-4561), and the requirement trace, because the legacy master carries no requirement row (ASM-4562).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `legal_action` and `hearing` are S4's; `notice` and `template` are outside S4's rows and the notice service is named as their owner (GAP-2743; ASM-4558); `recovery_case` is P3's; `decision_log_entry` and `rule_row` are P7's; `document` is P5's.
- The rwb-comms (P6) notice contract is published, so the consumed row of 12.2 names a real owner document; it is not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-2743; ASM-4558).
- The stage answer of rwb-case is fixed here as a shape only; no source names a published operation that moves a case state on behalf of a stage, and the name is Not specified in the source documents (GAP-2743; ASM-4559).
- The LITIGATION rule package and its row for R-LIT-03 are governed in rwb-decision (P7); this baseline names them and declares none of them (ASM-4561).
- The `legal_action` table and its columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-litigation for this step: the three operations with their request and answer elements, the `NOTICE` action type, the stage vocabulary, the rights and the seven error responses.
2. Fix the shape of the create: the `LegalActionRequest` element, the action type `NOTICE` of `LOV-LEGAL-TYPE`, the case reference, the claim amount and the `Idempotency-Key` rule.
3. Fix the shape of the approval: `POST /notices/{noticeId}/approve` with no request body, the notice reference and its state in the answer, and the decision record that goes with it.
4. Fix the consumed notice fact of the P6 contract — the notice reference, the notice type, the template code and version, the template status and the notice state — and mark the fields the sources do not give with the placeholder.
5. Fix the stage answer of rwb-case: the move, the rule ID, the version and the decided-at time, with no case row read or written here.
6. Record the decision-record element of DP-03 on `rwb.decision-record.v1`, written before the legal action or the notice changes.
7. Record the closed vocabulary of the action type and the stage names, and the rule that no value is a constant of the code.
8. Publish the contract tables of section 12 and the five contract fakes.
9. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a notice, template or `v_ace_*` read and of a `recovery_case` write, and the drift between a fake and the document.
10. Tag the baseline and hand it to RWB-S4-E5001-APP, the screen and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body or a request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC7 |
| X4 | The consumed notice fact or the stage answer has a field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC4 |
| X5 | A value outside `LOV-LEGAL-TYPE` or the stage vocabulary appears in the document or in an example | The vocabulary test fails the build | None | AC1, AC8 |
| X6 | The document declares another service's operation as provided, a `notice` property, a `template` property, a `v_ace_*` view or a `recovery_case` row | The review fails the baseline; the boundary test fails the build | None | AC8 |
| X7 | A POST is repeated with the same `Idempotency-Key` | The stored answer is returned and no second effect is described | None | AC2, AC5 |
| X8 | The rights of an operation are not the ones TSD S4 T-A.1 declares | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner contracts of rwb-comms and rwb-case only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the operations, the action type, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S4-E5001-APP, SCR-18 and the wave 3 harness on Day 1, and the rwb-comms and rwb-case teams on the same day |
| Estimable | One OpenAPI document, one AsyncAPI fragment, nine contract tables, five fakes and four new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the notice step of rwb-litigation

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of legal_action is S4, of notice and template is the notice service and of recovery_case is P3
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The legal-action and notice operations are declared with the NOTICE action type and the notice stage vocabulary (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-litigation is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /cases/{caseId}/legal-actions with the LegalAction answer of status 201, GET /legal-actions/{legalActionId} with the LegalAction answer of status 200 and POST /notices/{noticeId}/approve with the NoticeApproval answer of status 200, all under the base /api/recovery/litigation/v1 and owned by rwb-litigation
    Then action_type is declared against LOV-LEGAL-TYPE with the values NOTICE, CIVIL_CASE, APPEAL, ENFORCEMENT, BANKRUPTCY_PETITION and LED_AUCTION, and the action type of this step is NOTICE
    Then the stage names NOTICE_GENERATED, NOTICE_DISPATCHED, NOTICE_BLOCKED and NOTICE_UNSERVED are published as an enumeration of the stage element and not as a column of legal_action
    Then the approve operation answers the notice reference and its state as the notice service returns them, and declares no notice property of its own
    Then every other property of the LegalAction element is copied from the baseline of the legal action and is not redefined here

  Scenario: AC2 The create, read and approve shapes are fixed with the Idempotency-Key rule (new, D-RCV-60)
    Given the request and answer sections of the baseline
    When they are compared with the notice step of RWB-S4-E5001-APP
    Then the create takes a LegalActionRequest that carries the case reference, the action type NOTICE, the claim amount and the Law firm reference where it is known, and answers a LegalAction of status 201
    Then the read answers a LegalAction of status 200 with its action type, its claim amount and its status
    Then the approve takes no request body and answers the notice reference, the notice state and the decision reference of the approval
    Then the two POST operations declare the Idempotency-Key header and its stored answer, and the GET declares none
    Then the field names of LegalActionRequest and of NoticeApproval that no source gives are Not specified in the source documents (GAP-2743; ASM-4558) and the document marks them so

  Scenario: AC3 The consumed notice fact of rwb-comms is declared and the notice stays there (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the notice scope and the dispatch run of the FSD P6 module
    Then the generate and send of a demand or recall notice is declared as consumed from the notice service, with the case reference, the notice type, the template code and version, the addressee role, the legal action reference and the notice state
    Then the operation name of the row is Not specified in the source documents (GAP-2743; ASM-4558) and the row carries the placeholder
    Then the document declares no notice property, no template property, no barcode, no sent date and no dispatch job of rwb-litigation
    Then every call on the row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The stage answer is declared and the case row is never written here (new, D-RCV-60)
    Given the case boundary of the baseline
    When it is compared with rwb-case as the owner of recovery_case and of the route state
    Then the stage move is declared as an answer to rwb-case with the move NOTICE_DISPATCHED, the rule ID, the package version, the template version, the notice reference and the decided-at time
    Then the document declares no recovery_case property, no case route-state column and no write of a case row from rwb-litigation
    Then the answer carries the stage outcome that the parent CaseWorkflow applies, and the operation name of a REST case-move call for another caller is Not specified in the source documents (GAP-2743; ASM-4559)
    Then the states NOTICE_GENERATED and NOTICE_DISPATCHED are named as the stage of this service and answered to the case, and the notice states Generated, Approved, Sent, Delivered and Unserved are named as the notice service's

  Scenario: AC5 The Idempotency-Key rule, the error envelope and the rights are fixed (new, D-RCV-60)
    Given the error and access sections of the baseline
    When they are compared with TSD S4 T-A.1 and T-A.2 and with TSD S4 T6.1
    Then the operations answer 400 for a malformed request, 401, 403 with MSG-P4-002, 404 MSG-P4-003, 409 MSG-P3-005 on a wrong-type action or stage, 422 MSG-GEN-001 and 503 MSG-GEN-006 when a downstream does not answer, each with one envelope and one message ID per condition
    Then POST /cases/{caseId}/legal-actions declares Litigation right C, GET /legal-actions/{legalActionId} declares Litigation right R and POST /notices/{noticeId}/approve declares Litigation right A, each with the scope applied
    Then RW-LITOFF holds Litigation CRUA, RW-LEGAL, RW-PRODHEAD and RW-HEADLIT hold RA, RW-ENFORCE holds CRU, PT-LAWFIRM holds RU and every other role of TSD S4 T6.1 holds R
    Then a repeated POST with the same Idempotency-Key returns the stored answer and describes no second effect
    Then a replay is not counted again, a missing, blank or non-UUID key returns 400 MSG-PLT-N009-03, a conflicting or in-flight key returns 409 MSG-PLT-N009-05 and an unavailable key store returns 503 MSG-PLT-N009-06

  Scenario: AC6 The decision-record element is declared and written before the change (new, D-RCV-60)
    Given the decision section of the baseline
    When it is compared with the local decision-record library of DP-03
    Then one decision record is declared per rule outcome with the case reference, the legal action reference, the rule ID, the package version in force, the template version, the inputs reference, the outcome, the stage move and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before the legal action or the notice changes, and a failed write leaves both unchanged with MSG-P7-003
    Then the document declares no event of its own for the record and no second topic for this capability
    Then the record carries identifiers, codes, dates, an amount and a rule version only

  Scenario: AC7 The five contract fakes answer the document (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-comms notice fake answers the notice generated from template "DEMAND-MTG" at its Legal-approved version with status "current" for case "RC-2026-000501", its notice reference, the state "Approved" or "Sent", a template status "withdrawn" and no answer beyond 2 s
    Then the rwb-case stage fake answers the case route state NOTICE_GENERATED, an accepted move to NOTICE_DISPATCHED and a refused move
    Then the rwb-decision rule-package fake answers the LITIGATION package at its version with R-LIT-03 and one approval answer
    Then the decision-record library stub answers a healthy chain and a stopped chain
    Then the gateway-bff composite route fake answers the merged SCR-18 model for case "RC-2026-000501"
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC8 The naming baseline and the schema boundary are fixed and no cross-schema read is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_litigation, the login is rwb_litigation, the topic is rwb.litigation.events.v1, the queue is rwb-litigation and the Java package is th.co.scb.ace.workbench.recovery.litigation
    Then the tables named as owned are legal_action and the library objects decision_record and idempotency_key, and notice, template, recovery_case, decision_log_entry, rule_row, document and hearing are named as other owners' or another story's and are consumed only through their contracts
    Then the document declares no read of a v_ace_* view and no grant on rwb_comms or any other rwb_* schema, and the boundary test fails a build that adds one
    Then the document declares no event published, no event consumed and no Schedule for this step, and the absence test fails a build that adds one

  Scenario: AC9 Each business rule BR1 to BR12 of section 8 is covered by a test case (new, D-RCV-60)
    Given the business rules BR1 to BR12 of section 8
    When the test case coverage of section 8 is compared with the test cases of section 16
    Then each of BR1 to BR12 is named by at least one test case of section 16 and the coverage line of section 8 names the same test cases
    Then the test case of this criterion is TC-S4-E5001-CON-06, and its test content is Not specified in the source documents (NEWAC-RWB-S4-E5001-CON-AC9)
```

These eight criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S4-E5001-APP and they copy no criterion of the legacy story, whose three criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The `NOTICE` legal action is rwb-litigation's, and the contract declares its action type and its columns on `legal_action` only | Architecture v5 slide 41; Ownership Map (legal_action owner S4); TSD S4 T3.1 and T3.2 |
| BR2 | The decision record is declared as an element written before the legal action or the notice changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S4 T2; legacy RWB-E5-001 AC1 and AC3 |
| BR3 | The notice and the template stay with rwb-comms: the contract declares the notice generate and send as consumed, declares no notice or template property, and describes no rendering and no dispatch of rwb-litigation | TSD S4 T5.2; FSD P6 v3; GAP-2743 |
| BR4 | The stage move is answered and not written: the contract declares the answer that carries `NOTICE_DISPATCHED` and declares no `recovery_case` property and no case row write | Ownership Map (recovery_case owner P3); Architecture v5 slide 19; GAP-2743 |
| BR5 | No ACE view and no ACE table is read: the notice and the template are consumed on the owner's contract, and the service holds no `v_ace_*` grant | DP-01; Architecture v5 slide 29 |
| BR6 | A POST declares the `Idempotency-Key` and stores its answer; a GET declares none | Architecture v5 slide 11; TSD S4 T-A.2 |
| BR7 | The vocabulary is closed: `LOV-LEGAL-TYPE` and the notice stage names are published as enumerations and no state name or list value is a constant of the code | TSD S4 T3.2 and T4; BR-S4-001 (FSD S4 A2.1.3.1) |
| BR8 | No personal data in a schema, an example or a fake: identifiers, an amount, dates, list values and a rule version only | Architecture v5 slide 42 notes; Template and Rules v1 §R7.2 (s17) |
| BR9 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR10 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 42 notes |
| BR11 | The document lists only operations owned by rwb-litigation; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-11 |
| BR12 | The rule row of R-LIT-03 and the notice types and template statuses are governed in rwb-decision and in the notice service and named here, never declared here | ASM-4561; Business Rules and Routing Logic v4 |

Test case coverage of the rules of this section: BR1 and BR7 by TC-S4-E5001-CON-01; BR2 by TC-E5-001-05 and TC-S4-E5001-CON-03; BR3, BR4 and BR5 by TC-S4-E5001-CON-02; BR6, BR8, BR9, BR10, BR11 and BR12 by TC-S4-E5001-CON-05; the boundary of the §12.7 tables by TC-S4-E5001-CON-04.

### 9. State transitions

The lifecycle of this document, not of a legal action:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The three operations, the vocabulary, the consumed rows and the fakes are described | In review |
| In review | Consumer sign-off | The app story, SCR-18, the wave 3 harness and the rwb-comms, rwb-case and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new error code | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or the action type or a stage name changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence test of AC8 fails: a notice or template property, a `v_ace_*` view, a `recovery_case` property, a second topic or a Schedule | In review |

The stage machine the document describes is the app story's: `NOTICE_GENERATED` to `NOTICE_DISPATCHED` under R-LIT-03 of the LITIGATION machine of TSD S4 T4, and this baseline fixes the names and moves no stage.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-litigation | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes |
| Consuming teams (the app story, SCR-18, the wave 3 harness and the owners of rwb-comms, rwb-case, rwb-decision and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme of the document is named "the rwb-litigation login (DP-02)" and is not part of this baseline.

The authorisation of each operation is the rwb-access authorise check (DP-08); the name of that check in the rwb-access contract is Not specified in the source documents (DOR-RWB-S4-E5001-CON-6).

The empty, loading, error and no-access states of SCR-18 are not specified in the source documents (DOR-RWB-S4-E5001-CON-10). The no-access state is the 403 with MSG-P4-002 of TC-E5-001-04.

### 11. Data

The contract baseline declares shapes, not business values.

| BR Field ID | Item | Content |
|---|---|---|
| DF-LEG-001 to DF-LEG-014 | LegalAction element | The columns of DF-LEG-001 to DF-LEG-014: `id`, `case_id`, `law_firm_id`, `action_type`, `lawsuit_no`, `black_case_no`, `red_case_no`, `court_name`, `claim_amount`, `filed_date`, `judgment_date`, `judgment_amount`, `lit_status` and `status`; this step fixes `action_type` to `NOTICE` |
| Not specified in the source documents (DOR-RWB-S4-E5001-CON-7) | Stage element | `NOTICE_GENERATED`, `NOTICE_DISPATCHED`, `NOTICE_BLOCKED`, `NOTICE_UNSERVED` of the LITIGATION machine (TSD S4 T4); a name of the workflow's stage, not a column |
| DF-DEC-001 to DF-DEC-018 | Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the action changes (DP-03) |
| DF-LEG-015 to DF-LEG-023 | Notice | DF-LEG-015 to DF-LEG-023 of the notice service, read only through its contract and never written, copied or joined here (GAP-2743; ASM-4558) |
| DF-REF-045 to DF-REF-051 | Template | DF-REF-045 to DF-REF-051, read only through the notice contract; owner Not specified in the source documents (GAP-2743; ASM-4560) |
| DF-ACE-001 to DF-ACE-054 | ACE facts | DF-ACE-001 to DF-ACE-054, not read: this service holds no `v_ace_*` grant (DP-05 is absent from the pattern set and the boundary is absolute) |
| Not specified in the source documents (DOR-RWB-S4-E5001-CON-7) | Not written here | `recovery_case` (P3), `document` (P5), `decision_log_entry` and `rule_row` (P7), `hearing` (S4, a sibling story's) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC1 and the optionality rule of BR10. **No new table, no new column and no migration** is declared by this story.

The reference data this step reads is the closed list `LOV-LEGAL-TYPE` and the notice stage names (BR7), and the template statuses read through the notice contract. Their reference-data contract is DP-06; the parameters they read are Not specified in the source documents (DOR-RWB-S4-E5001-CON-20).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/legal-actions` | LegalActionRequest in, LegalAction of status 201 out, with the action type `NOTICE` (API-S4-002) | Litigation, right C, scope applied | `Idempotency-Key` header required; the answer is stored |
| GET | `/legal-actions/{legalActionId}` | LegalAction of status 200 out with its action type and status (API-S4-003) | Litigation, right R, scope applied | Not applicable |
| POST | `/notices/{noticeId}/approve` | No request body, the NoticeApproval answer of status 200 with the notice reference and its state (API-S4-001) | Litigation, right A, scope applied | `Idempotency-Key` header required; the answer is stored |

The three operations answer 400, 401, 403, 404, 409, 422 and 503, each with the error envelope and one message ID of section 14.
The shared Problem uses messageCode and traceId. Apply the 404, 409 and 503 codes and the POST key errors of AC5. The operation IDs are those of TSD S4 T-A.1; the paths are those of the target base and not the monolith form. API-S4-004 `PATCH /legal-actions/{legalActionId}` and API-S4-005 `POST /legal-actions/{legalActionId}/hearings` belong to the filing, judgment and hearing stories of this service and are not declared as this baseline's scope, though they share the document. The notice row behind API-S4-001 is the notice service's and is named as such (GAP-2743; ASM-4558).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The generate and send operation of the notice contract (operation name Not specified in the source documents (GAP-2743; ASM-4558)) | `/api/recovery/comms/v1` | P6 rwb-comms | The demand or recall notice generated from the named template version and sent on the dispatch run: the case reference, the notice type, the template code and version, the addressee role and the legal action reference in; the notice reference and its state out; faked |
| The stage answer (operation name Not specified in the source documents (GAP-2743; ASM-4559)) | rwb-case (P3) | P3 rwb-case | The move of the case of record to `NOTICE_DISPATCHED` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). Both rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-2743 with ASM-4558 and ASM-4559.

The notice ownership split (GAP-1740): this service decides that a notice is due, approves it and owns the notice period; rwb-comms owns the template, the merge fields, the delivery and the proof of delivery, and returns the served result (event name: Not specified in the source documents (GAP-1740)). The notice period starts from the delivery time that rwb-comms returns (field name: Not specified in the source documents (GAP-1740)), and the notice state on the case is written by this service only.

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and its three catalogue events `LawsuitFiled`, `JudgmentRecorded` and `AuctionResult` belong to the stories that own the filing, the judgment and the auction result. This baseline declares none of them, adds no outbox row and widens no topic; the decision record is relayed by the library of DP-03 on `rwb.decision-record.v1` and is not an event of this service.

#### 12.4 Events consumed

None. The one notice fact on the S4 IN row of Architecture v5 slide 19 is `NoticeDelivered`, which is the proof of delivery and belongs to the sibling story of this legacy family; with DP-09 outside this story's pattern set, no consumer group, no subscription and no inbox is declared, and the notice fact of 12.2 arrives synchronously (GAP-2743; ASM-4563).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-litigation` | The stage that hosts the notice step; its inputs, its signals, its one durable timer of 1 working day and its outcome for the parent are declared, not built |
| `issueDemandAndRecallNotices` | Activity, the one notice step | `rwb-litigation` | The case and the legal action in; the rule ID with its package version, the template version, the notice reference and the stage move out |

The activity name is a target design choice and the trigger of the step is read as the opening of the litigation stage for route R4, which is the event `ROUTE_APPROVED` of R-LIT-01, because the legacy story says the step runs with no person in the path while the FSD declares no background event (GAP-2743; ASM-4561). No activity is registered by this story. The workflow ID form and the duplicate-start policy of `LitigationWorkflow` are not specified in the source documents (DOR-RWB-S4-E5001-CON-8). Its start rule is the catalog trigger of Temporal Catalog v1: 'Litigation route approved (R-LIT-01), or a restructure or settlement plan breaks (R-LIT-02)'. The start mode (start or signalWithStart) is Not specified in the source documents (DOR-RWB-S4-E5001-CON-8). The activity `issueDemandAndRecallNotices` is not in Temporal Catalog v1; that catalog entry is a cross-document change. The rule set of this story is the thirty-two R-LIT rules the FSD names; the other forty-seven are authoring work for the litigation rule package, whose package code, version label and owner are Not specified in the source documents (GAP-1742).

#### 12.6 Schedules

None. The dispatch run JOB-10 at 16:00 is the notice service's; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table, and no Job of Architecture v5 slide 44 is owned or moved here.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | The `NOTICE` action, its action type and its columns; the table the create and the read serve |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated POST and the answer it holds |

`notice` and `template` (rwb-comms), `recovery_case` (P3), `document` (P5), `decision_log_entry` and `rule_row` (P7) and `hearing` (S4, a sibling story's) are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-comms notice fake | The notice generated from template `DEMAND-MTG` at its Legal-approved version with status `current` for case `RC-2026-000501`, its notice reference and the state `Approved` or `Sent`; a template status `withdrawn`; no answer beyond 2 s | AC1, AC2, AC3, AC7 |
| rwb-case stage fake | The case route state `NOTICE_GENERATED`; an accepted move to `NOTICE_DISPATCHED` and a refused move | AC2, AC4, AC7 |
| rwb-decision rule-package fake | The LITIGATION package at its version in force with R-LIT-03 and one approval answer | AC6, AC7 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC6, AC7 |
| gateway-bff composite route fake | The merged SCR-18 answer for case `RC-2026-000501`, with the notice facts read once | AC1, AC7 |

The fakes are test-only and are replaced by the real services in SIT. The operation name of the notice row, the notice reference shape and the stage answer are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2743; ASM-4558, ASM-4559).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 2 consumed | The create, read and notice approval on `/api/recovery/litigation/v1`; the notice generate and send of rwb-comms and the stage answer of rwb-case; one hop, 2 s |
| Kafka | None declared | No event published and none consumed by this step; the decision record is the library's on `rwb.decision-record.v1` |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `LitigationWorkflow` and `issueDemandAndRecallNotices` on `rwb-litigation`, with one durable timer; no Schedule |
| File | None | No file is read, built or delivered here; the WIN file of the dispatch run is the notice service's |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no legal action, no notice, no case and no rule package. What it publishes is one OpenAPI 3.1 document, one AsyncAPI fragment that declares no event, nine contract tables and five fakes.

**Deliverables.** The additive document `openapi/rwb-litigation-v1.yaml` for this step, the `LegalActionRequest` and `NoticeApproval` elements, the stage enumeration, the vocabulary of `LOV-LEGAL-TYPE` as a published enumeration, the contract README rows for the consumed rows and their placeholders, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-13 moves the base and nothing else. DP-19 is behind SCR-18, whose screen model is the edge contract's. DP-03 is the transaction rule the document declares. DP-01 is stated as the schema boundary, and DP-09 is not in the pattern set of this key, which is why no event is declared in 12.3 or 12.4. The template fact is consumed on the notice contract because DP-07 is not in the pattern set of this key either (GAP-2743; ASM-4560).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, while the plan's build list for this story is None; this baseline builds against their fakes until those platform contract stories publish. The notice contract and the case answer are C dependencies in fact and not in the metadata row (GAP-2743; ASM-4558, ASM-4559).

**Build steps**

1. Write the three operations and validate the additive rule of AC1 in the pipeline.
2. Write the `LegalActionRequest`, `NoticeApproval` and stage elements of AC2 with the placeholder on the fields the sources do not give.
3. Record the consumed notice row of AC3 with its owner, its budget and its placeholder.
4. Record the stage answer of AC4 and the absence test for a `recovery_case` property and a notice property.
5. Record the error envelope, the rights and the `Idempotency-Key` rule of AC5.
6. Record the decision-record element of AC6 and validate it against the library schema.
7. Publish the five fakes of AC7 and the drift test.
8. Record the naming baseline and the boundary of AC8, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the eight contract tests pass, the five fakes answer every consumed path and the drift test is green, and the app story, SCR-18 and the wave 3 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the litigation pack, which is the pack story of this service, so no path of this step raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key. It names the expiry of the claim on the case, which is the prescription fact of this service, so no path of this step raises it | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Litigation right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the legal action or the notice changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P6-003 | The template was withdrawn after generation and the notice is held; the text is the notice service's and is declared here because the hold state of SCR-18 displays it | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P1-001 | The data product of the source is stale after a late or failed ACE batch, which is VR-S4-001-1 of the FSD; the check is the owner's and this service holds no ACE batch status read | {product} is from {date}. Today's ACE batch has not arrived. |

The seven message IDs are contract elements and the text of the first five is the legacy and FSD wording, copied unchanged; MSG-P6-003 is the notice service's hold message and MSG-P1-001 is carried because it is in the message set of this feature, and no path of this service raises either. No message is reworded and no new one is added (GAP-2743; ASM-4560).

### 15. Screens and states

The contract serves SCR-18 Notice approval in its generated, approved, sent, delivered and unserved states, all through the gateway-bff composite route (DP-19). The route calls rwb-litigation for the legal action and the rule outcome, rwb-comms for the notice, its template version and its state, and rwb-case for the case of record and its route state; this baseline fixes the rwb-litigation answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The route of SCR-19 litigation workspace and SCR-20 enforcement workspace, and this service's part of each, are Not specified in the source documents (GAP-1747); the owner cell of the three screens is not decided here. The hold, refusal and failure states the app story shows — blocked, not recorded, refused, stale data — read the messages of section 14 on the same route. The empty, loading, error and no access states of SCR-18 are Not specified in the source documents (CG-ALL-9011); Screen Specifications v1 does not give them.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-001-01 | AC1, AC2 | Contract | The demand and recall notice of case `RC-2026-000501`; the contract half answers the three operations, the action type and the shapes |
| TC-E5-001-02 | AC1, AC3 | Contract | Template `DEMAND-MTG` at its Legal-approved version with status `current`; the contract half answers the notice stage enumeration and the consumed notice row |
| TC-E5-001-03 | AC4, AC6 | Contract | The stage move to `NOTICE_DISPATCHED` and the decision-record element; the contract half answers the stage answer and the record element |
| TC-E5-001-04 | AC5, AC8 | Contract | A role without the Litigation right and a malformed request; the contract half answers the 403 with MSG-P4-002 and the 400 of the envelope |
| TC-E5-001-05 | AC5, AC6 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the rights of AC5 |
| TC-S4-E5001-CON-01 | AC1, AC2 | Contract | The document validates; the three operations, the base, the six action types, the four stage names and the shapes are present, and no notice or template property is added |
| TC-S4-E5001-CON-02 | AC3, AC5, AC8 | Contract | The consumed notice row and the stage answer validate with their placeholder fields marked and one hop with a 2 s budget; the absence test for a notice property, a `v_ace_*` read, a second topic and a Schedule |
| TC-S4-E5001-CON-03 | AC6, AC7 | Contract | The decision-record element validates against the library schema; the five fakes match the document and a drifted fake fails the build |
| TC-S4-E5001-CON-04 | AC2 | Contract | The three tables of §12.7 at their owners, legal_action, decision_record and idempotency_key; the contract half answers that no foreign key leaves the schema and that no table outside §12.7 is declared (ASM-3438) |
| TC-S4-E5001-CON-05 | AC1, AC2 | Contract | Each POST declares `Idempotency-Key` and each GET declares none (BR6); no personal data in a schema, example or fake (BR8); one base, topic, queue and login (BR9); a breaking change is a new major version (BR10); only rwb-litigation operations are listed (BR11); the rule row and notice types are not declared here (BR12) |
| TC-S4-E5001-CON-06 | AC9 | Contract | Not specified in the source documents (NEWAC-RWB-S4-E5001-CON-AC9) |

The five legacy cases are the legacy cases of RWB-E5-001 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S4-E5001-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The six new cases are the contract tests of the baseline. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the template statuses, the notice types, the stage names, the lists and the rule row stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, an amount, dates, list values and a rule version only; every example is synthetic and the addressee is a role.
- The notice stays with rwb-comms and the case with rwb-case: the document declares no notice property, no template property, no `recovery_case` property and no case row write (BR3, BR4).
- ACE data only through the owner's contract: the document declares no `v_ace_*` view and no grant on `rwb_comms` or any other `rwb_*` schema, and the boundary test fails a build that adds one (DP-01).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-litigation; a consumed operation is described as consumed and faked, never as provided (DP-11).
- No retired element is reintroduced: the absence test of AC8 fails a build that declares a notice property, a `v_ace_*` read, a second topic, a Schedule, a Quartz row or a shared job table.
- The error envelope, the `Idempotency-Key` rule and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S4-001 | Demand and recall notices are generated by rule, approved, dispatched, and their notice periods are timed; the contract fixes the notice a case requests and the stage it moves to (FSD S4 requirements served; Business Requirements Program v5); the legacy story master carries no requirement ID (GAP-2743; ASM-4562) | The three operations, the `NOTICE` action type, the stage enumeration, the consumed notice row and the stage answer | TC-E5-001-01, TC-E5-001-02, TC-S4-E5001-CON-01, TC-S4-E5001-CON-02 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two consumed rows with their budget and breaker | TC-S4-E5001-CON-02 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-001, disposition Split (rework) |
| Legacy criteria | AC1 to AC3 of the legacy story, owned word for word by RWB-S4-E5001-APP; this baseline copies none of them |
| Test cases | The five legacy cases as the contract half, and the three new contract cases TC-S4-E5001-CON-01 to -03 |
| Feature and screen | FEAT-LIT-01, SCR-18 Notice approval |
| Rules | R-LIT-03, named from the Business Rules and Routing Logic v4 and governed in rwb-decision (ASM-4561) |
| Decoupling patterns | DP03, DP13, DP19, with DP-01 as the schema boundary |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the three operations, the evaluation of R-LIT-03, the decision record, the notice request and the stage answer: RWB-S4-E5001-APP.
- The notice row, the templates, the rendering, the D7.1 approval and the dispatch run with the WIN file: rwb-comms (P6) and rwb-decision (P7). **The notice is generated, approved and dispatched by rwb-comms, and no part of this baseline moves it** (GAP-2743; ASM-4558).
- The case of record, its route state and the parent `CaseWorkflow`: rwb-case (P3), whose stage answer this baseline declares as consumed and faked (ASM-4559).
- The proof of delivery, the notice period and its timer, the pack, the filing, the hearings and the judgment: the sibling stories of this service, including RWB-S4-E5002-APP and RWB-S4-E5011-APP.
- The authoring, testing, approval and versioning of the LITIGATION package and of the row of R-LIT-03, and the approval matrix and delegation of authority: rwb-decision (P7) (ASM-4561).
- The template reference data and the freshness of the data product: the reference-data owner and rwb-source-data (P1) (GAP-2743; ASM-4560).
- The document of the notice pack, its custody and its retention: rwb-document (P5).
- The gateway-bff composite route and the screen field list of SCR-18: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
