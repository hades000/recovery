# RWB-S4-E5007-CON Verify the pack and approve filing - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5007-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the pack verification and filing approval of rwb-litigation, split from RWB-E5-007. It fixes the three legal-action operations on `/api/recovery/litigation/v1` (DP-13), the pack action types of `LOV-LEGAL-TYPE` and the status vocabulary of `LOV-LEGAL-STATUS`, the verification and authorisation shapes, the template-withdrawn hold, the case route fact and the task, the decision-record element of DP-03, the error envelope, the `Idempotency-Key` rule and the fakes. The pack itself and its defect list are rwb-document's and the notice is rwb-comms's (GAP-2765; ASM-4599); the element names and field lists no source gives are carried with the placeholder (GAP-2770; ASM-4604); the notice approval operation API-S4-001 is first in E2 and is not declared here (GAP-2771; ASM-4605). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S4-E5007-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the pack verification and filing approval of rwb-litigation — the three legal-action operations on `/api/recovery/litigation/v1` with the pack action types, the verification and authorisation elements, the template-withdrawn hold and the case route fact, the decision-record element, the error envelope, the rights and the fakes**, so that **the app story, the screens and the tests of this legacy key build against one fixed, testable contract on Day 1, and a list value, a status value, an element or an answer shape can never drift between rwb-litigation, rwb-document, rwb-comms, rwb-case and rwb-decision without a failing build**.

The baseline owns one surface and declares the rest as consumed:

- the OpenAPI 3.1 document of the three operations of TSD S4 T-A on base `/api/recovery/litigation/v1`: API-S4-002 create, API-S4-003 read and API-S4-004 patch (DP-13);
- the closed vocabulary of `action_type`, `status`, `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS` (TSD S4 T3.2);
- the `LegalAction`, `LegalActionRequest` and `LegalActionUpdate` elements of TSD S4 T3.1 DF-LEG-001 to DF-LEG-014, plus the verification and authorisation properties the app story needs and no source names (GAP-2770);
- the element that carries the pack and defect-list reference, the element that carries the case route fact and the task raise, and the element that carries the D7 approval answer — declared, never owned;
- the decision-record element of DP-03 on the shared `rwb.decision-record.v1`, written before the change;
- the contract tables 12.1 to 12.9 and the fakes of 12.8.

It declares no pack document, no notice, no case row and no approval item as its own, and it publishes no event (DP-09 is not in this key's pattern set). The notice approval operation `POST /notices/{noticeId}/approve` (API-S4-001) is named by the legacy endpoint block of RWB-E5-007 but is first in E2, so it belongs to the notice story of this service and stays out of this baseline (GAP-2771; ASM-4605).

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy step of RWB-E5-007 crossed four boundaries at once: an officer screen, a pack and its defect list, a notice and its template, a case state with a task and a timer, and a decision log entry. The target splits them: the pack and the defect list are rwb-document's (P5), the notice and its template are rwb-comms's (P6), the case, its task and its timers are rwb-case's (P3), and the delegation table and the ledger are rwb-decision's (P7). Only the legal action of the pack and its rule answers stay with rwb-litigation (S4).

Each boundary is now a contract another team builds against, so each has to be fixed before the app story starts: the pack action types and the status vocabulary, the shape of the verification and of the authorisation, the shape of the hold and of the route fact, the shape of the D7 approval answer, and the record of the decision. The baseline also fixes the naming the checks require: schema `rwb_litigation`, base `/api/recovery/litigation/v1`, topic `rwb.litigation.events.v1` with retry and `.dlt` topics, task queue `rwb-litigation` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.litigation` (Architecture v5 slide 41 notes).

Three points are carried as gaps and assumptions rather than decided quietly: no source gives the element names and field lists of the verification, the authorisation and the route fact (GAP-2770; ASM-4604); the notice approval operation of the legacy endpoint block is first in E2 and its ownership here is unsettled (GAP-2771; ASM-4605); and no source publishes the pack element or states which document owns it (GAP-2765; ASM-4599).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `legal_action` and `hearing` are S4's; `document` is P5's, the notice and its template are P6's, `recovery_case`, `task` and `timer` are P3's, `decision_log_entry`, `rule_row` and the approval item are P7's. This document never declares another service's operation as provided.
- LOV-LEGAL-TYPE and LOV-LEGAL-STATUS are read as values in force on the reference data of rwb-case (`RWB-P3-E1043-CON`). DP-07 is not in this story's pattern set and the read carries no dependency row (GAP-2765; ASM-4599).
- The pack read of rwb-document, the notice and template-status read of rwb-comms, the case answer and route fact of rwb-case and the approval item of rwb-decision (`RWB-P7-E2013-CON`) are published and faked. None is in this story's contract-dependency row, which is None, and no source names their operations; the absence is recorded (GAP-2765, GAP-2771; ASM-4599, ASM-4605).
- The LITIGATION rule package, its rows for R-LIT-04, R-LIT-11, R-LIT-16, R-LIT-21 and R-LIT-23 and its D7 limit are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The `legal_action` and `hearing` tables and their columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules section R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-litigation for this step: the three operations with their request and answer elements, the action types, the status values, the rights and the six error responses.
2. Fix the pack action types: `NOTICE` and `CIVIL_CASE` of `LOV-LEGAL-TYPE`, and the status vocabulary of `LOV-LEGAL-STATUS` with the note that no value names a verification or an authorisation.
3. Fix the verification element and the authorisation element: the pack reference, the defect-list result reference, the checklist version, the approval code, the rule ID and the package version.
4. Fix the consumed shapes: the pack and defect-list answer of rwb-document, the notice and template-status answer of rwb-comms, the case answer with its route fact and task raise, and the D7 approval answer of rwb-decision, each marked with the placeholder where no source gives a field list.
5. Record the decision-record element of DP-03 on `rwb.decision-record.v1`, written before the legal action changes.
6. Record the closed vocabulary and the rule that no value is a constant of the code.
7. Publish the contract tables of section 12 and the five contract fakes.
8. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a `v_ace_*` read and of a `document`, `notice`, `recovery_case` or `task` write, and the drift between a fake and the document.
9. Tag the baseline and hand it to `RWB-S4-E5007-APP`, the two screens and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request or a response body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A property is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed answer has a field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC2, AC3 |
| X5 | A value outside `LOV-LEGAL-TYPE` or `LOV-LEGAL-STATUS` appears in the document or in an example | The vocabulary test fails the build | None | AC1, AC7 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `document`, `notice`, `recovery_case`, `task` or `timer` property | The review fails the baseline and the boundary test fails the build | None | AC7 |
| X7 | A POST or a PATCH is repeated with the same `Idempotency-Key` | The stored answer is returned and no second effect is described | None | AC2, AC5 |
| X8 | The rights of an operation are not the ones TSD S4 T-A.1 and the legacy permission block declare | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner contracts of rwb-document, rwb-comms, rwb-case and rwb-decision only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the operations, the vocabulary, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks `RWB-S4-E5007-APP`, the two screens and the wave 3 harness on Day 1, and the rwb-document, rwb-comms, rwb-case and rwb-decision teams on the same day |
| Estimable | One OpenAPI document, one AsyncAPI fragment that declares no event, nine contract tables, five fakes and four new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the pack verification and filing approval of rwb-litigation

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of legal_action and hearing is S4, of document is P5, of the notice is P6, of recovery_case, task and timer is P3 and of the approval item is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The three legal-action operations are declared on the per-service base with the pack action types and the status vocabulary (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-litigation is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /cases/{caseId}/legal-actions with the LegalAction answer of status 201, GET /legal-actions/{legalActionId} with the LegalAction answer of status 200 and PATCH /legal-actions/{legalActionId} with the LegalAction answer of status 200, all under the base /api/recovery/litigation/v1 and owned by rwb-litigation
    Then action_type is declared against LOV-LEGAL-TYPE with the values NOTICE, CIVIL_CASE, APPEAL, ENFORCEMENT, BANKRUPTCY_PETITION and LED_AUCTION, and the two action types of this step are NOTICE and CIVIL_CASE
    Then status is declared against LOV-LEGAL-STATUS with the values OPEN, FILED, JUDGMENT, ENFORCING, CLOSED and WITHDRAWN, and the document states that no value of the list names a pack verification or a filing authorisation
    Then no property is added to the LegalAction element for a pack state, a checklist or an approval, and every other property of the element is copied from the legal action of TSD S4 T3.1

  Scenario: AC2 The verification and authorisation elements are fixed and the pack facts stay with rwb-document (new, D-RCV-60)
    Given the verification and authorisation sections of the baseline
    When they are compared with the pack step of RWB-S4-E5007-APP
    Then the verification is carried on PATCH /legal-actions/{legalActionId} with an element that carries the pack reference, the defect-list result reference, the checklist version, the rule ID R-LIT-16, the package version in force and the outcome
    Then the authorisation is carried on the same operation with an element that carries the approval code, the rule ID R-LIT-16 with its version, the pack reference and the decided-at time
    Then the pack reference, the document list, the checklist version and the missing items are declared as the answer of rwb-document and are never declared as a property of this service's tables
    Then the field names of the two elements that no source gives are Not specified in the source documents (GAP-2770; ASM-4604) and the document marks them so
    Then the POST declares the Idempotency-Key header and its stored answer, and the GET declares none, and the PATCH declares the header with its stored answer

  Scenario: AC3 The template-withdrawn hold, the route fact and the task raise are declared as consumed and never written here (new, D-RCV-60)
    Given the hold and case sections of the baseline
    When they are compared with the owners of the notice and of the case
    Then the template status is declared as consumed from P6 rwb-comms with the notice reference, the status value current or withdrawn and the template version
    Then the case route fact is declared as an answer to P3 rwb-case with the case reference, the route fact NOTICE_BLOCKED, PACK_ASSEMBLY, PACK_VERIFIED or PACK_APPROVED, the rule ID, the package version and the decided-at time
    Then the task raise of R-LIT-04 is declared with the case reference, the task code, the route fact and the rule that raised it, and is answered by rwb-case
    Then the document declares no notice property, no recovery_case, task or timer property and no write of one of those rows from rwb-litigation
    Then the operation names of the hold, the route fact and the task raise are Not specified in the source documents (GAP-2765; ASM-4599) and every call is one hop with a 2 s budget and a breaker (DP-11, ADR-020)

  Scenario: AC4 The decision-record element is declared and written before the change (new, D-RCV-60)
    Given the decision section of the baseline
    When it is compared with the local decision-record library of DP-03
    Then one decision record is declared per rule outcome with the case reference, the legal action reference, the rule ID, the package version in force, the inputs reference, the outcome, the case route fact and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before the legal action changes, and a failed write leaves the action unchanged with MSG-P7-003
    Then the document declares no event of its own for the record and no second topic for this capability
    Then the record carries IDs, codes, dates and a rule version only

  Scenario: AC5 The Idempotency-Key rule, the error envelope and the rights are fixed (new, D-RCV-60)
    Given the error and access sections of the baseline
    When they are compared with TSD S4 T-A.1, T-A.2 and T6.1 and with the legacy permission block of RWB-E5-007
    Then the operations answer 400 for a malformed request, 401, 403 with MSG-P4-002, 404, 409 on a status or a case state that refuses the step, 422 with MSG-GEN-001 and 503 when a downstream does not answer, each with one envelope and one message ID per condition
    Then POST /cases/{caseId}/legal-actions declares Litigation right C, GET /legal-actions/{legalActionId} declares Litigation right R and PATCH /legal-actions/{legalActionId} declares Litigation right U, each with the scope applied
    Then RW-LITOFF holds Litigation CRUA and C, RW-ENFORCE holds CRU and C, RW-LEGAL, RW-PRODHEAD and RW-HEADLIT hold RA, and every other role of TSD S4 T6.1 holds R
    Then a repeated POST or PATCH with the same Idempotency-Key returns the stored answer and describes no second effect

  Scenario: AC6 The five contract fakes answer the document (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-document pack fake answers the pack of 2026-12-09 for case "RC-2026-000704" with every defect list item present for action "LA-2026-000704", a pack with one missing item, and no answer beyond 2 s
    Then the rwb-comms notice fake answers notice "NT-2026-000704" with template status current and withdrawn, each with its template version
    Then the rwb-case fake answers the case states NOTICE_GENERATED, NOTICE_UNSERVED and PACK_ASSEMBLY, an accepted and a refused route fact, and an accepted and a refused task raise
    Then the rwb-decision approval fake answers the D7 item granted, refused with a reason, and delayed
    Then the decision-record library stub answers a healthy chain and a stopped chain
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and no cross-schema read is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_litigation, the login is rwb_litigation, the topic is rwb.litigation.events.v1, the queue is rwb-litigation and the Java package is th.co.scb.ace.workbench.recovery.litigation
    Then the tables named as owned are legal_action and the library objects decision_record and idempotency_key, and document, notice, recovery_case, task, timer, decision_log_entry, rule_row and hearing are named as other owners' or another story's and are consumed only through their contracts
    Then the document declares no read of a v_ace_* view and no grant on another rwb_* schema, and the boundary test fails a build that adds one
    Then the document declares no event published, no event consumed and no Schedule for this step, and the absence test fails a build that adds one
    Then the notice approval operation POST /notices/{noticeId}/approve is not declared as provided here, because it is first in E2 (GAP-2771; ASM-4605)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by `RWB-S4-E5007-APP` and they copy no criterion of the legacy story, whose four criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The legal action of the pack is rwb-litigation's, and the contract declares its action types, status values and pack elements on `legal_action` only | Architecture v5 slide 41; Ownership Map (`legal_action` and `hearing` owner S4); TSD S4 T3.1, T3.2 |
| BR2 | The decision record is declared as an element written before the legal action changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S4 T2; legacy RWB-E5-007 AC1 and AC4 |
| BR3 | The pack stays with rwb-document: the contract declares the pack and defect list as consumed, declares no `document` property and describes no document write of rwb-litigation | Ownership Map (`document` owner P5); Architecture v5 slide 4; GAP-2765; ASM-4599 |
| BR4 | The notice, its template status, the case, its task and its timers are answered and not written: the contract declares the answers and declares no property of those objects | Ownership Map (`recovery_case`, `task`, `timer` owner P3; the notice P6); FSD S4 existing capability check |
| BR5 | A POST and a PATCH declare the `Idempotency-Key` and store their answer; a GET declares none | Architecture v5 slide 11; TSD S4 T-A.2 |
| BR6 | The vocabulary is closed: `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS` are published as enumerated values, no status value names a verification or an authorisation, and no value is a constant of the code | TSD S4 T3.2; BR-S4-007 (FSD S4 A2.7.3.1); GAP-2770 |
| BR7 | No personal data in a schema, an example or a fake: identifiers, amounts, dates, list values and a rule version only | Architecture v5 slide 42 notes; Template and Rules section R7.2 (s17) |
| BR8 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules section R4 |
| BR9 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR10 | The document lists only operations owned by rwb-litigation; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-11 |
| BR11 | The notice approval operation of the legacy endpoint block is first in E2 and is not declared by this baseline | TSD S4 T-A.1 (API-S4-001 first in E2); GAP-2771; ASM-4605 |
| BR12 | The rule rows of R-LIT-04, R-LIT-11, R-LIT-16, R-LIT-21 and R-LIT-23 and the D7 limit are governed in rwb-decision and named here, never declared here | Business Rules and Routing Logic v4; GAP-2765 |

### 9. State transitions

The lifecycle of this document, not of a legal action:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The three operations, the vocabulary, the consumed answers and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the two screens, the wave 3 harness and the rwb-document, rwb-comms, rwb-case and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new error code | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or an action type or status value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence test of AC7 fails: a `v_ace_*` view, a `document`, `notice`, `recovery_case`, `task` or `timer` property, a second topic or a Schedule | In review |

The status machine of `legal_action` that the document describes is the app story's: `LOV-LEGAL-STATUS` is OPEN, FILED, JUDGMENT, ENFORCING, CLOSED and WITHDRAWN, this baseline fixes the vocabulary and names no verification or authorisation value, and it moves no action (GAP-2770; ASM-4604).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-litigation | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes |
| Consuming teams (the app story, the screens, the wave 3 harness and the owners of rwb-document, rwb-comms, rwb-case, rwb-decision, rwb-access and rwb-source-data) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme of the document is named "the rwb-litigation login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| LegalAction element | The columns of DF-LEG-001 to DF-LEG-014: `id`, `case_id`, `law_firm_id`, `action_type`, `lawsuit_no`, `black_case_no`, `red_case_no`, `court_name`, `claim_amount`, `filed_date`, `judgment_date`, `judgment_amount`, `lit_status` and `status` |
| Pack action and status | `action_type` takes `NOTICE` or `CIVIL_CASE` of LOV-LEGAL-TYPE; `status` takes the six values of LOV-LEGAL-STATUS and no value names a verification or an authorisation |
| Verification and authorisation | Carried on the elements of AC2; their property names and field lists are Not specified in the source documents (GAP-2770; ASM-4604) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the action changes (DP-03) |
| Pack and defect list | The document list, the checklist version and the missing items of rwb-document (P5), read only through the owner and never copied or joined here |
| Notices | DF-LEG-015 to DF-LEG-023 of the notice in `rwb_comms` (P6), read only through the owner |
| ACE facts | Documents and notices only, and this service holds no `v_ace_*` grant (DP-05) |
| Not written here | `recovery_case`, `task` and `timer` (P3), `document` (P5), the notice (P6), `decision_log_entry`, `rule_row` and the approval item (P7); the notes of the three are answers of their owners or a later story's table |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC1 and the optionality rule of BR9. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/legal-actions` | LegalActionRequest in, LegalAction of status 201 out, with `action_type` of `LOV-LEGAL-TYPE` and the decision record of the create (API-S4-002) | Litigation, right C, scope applied | `Idempotency-Key` header required; the answer is stored |
| GET | `/legal-actions/{legalActionId}` | LegalAction of status 200 out with its pack reference, its facts and its status (API-S4-003) | Litigation, right R, scope applied | Not applicable |
| PATCH | `/legal-actions/{legalActionId}` | LegalActionUpdate in, LegalAction out, carrying the verification or the authorisation element of AC2 (API-S4-004) | Litigation, right U, scope applied | `Idempotency-Key` header required; the answer is stored |

The three operations answer 400, 401, 403, 404, 409, 422 and 503, each with the error envelope and one message ID of section 14. The operation IDs are those of TSD S4 T-A.1; the paths are those of the target base and not the monolith form. API-S4-001 `POST /notices/{noticeId}/approve` is first in E2 and is not declared here (BR11); API-S4-005 `POST /legal-actions/{legalActionId}/hearings` belongs to the hearing story of this service.

#### 12.2 REST operations consumed

| Method and path | Owner | Use in the baseline |
|---|---|---|
| The pack and defect-list read (operation name Not specified in the source documents (GAP-2765; ASM-4599)) | P5 rwb-document | The pack reference, the document list, the checklist version and the missing items; the element and its owner document are Not specified in the source documents (GAP-2765; ASM-4599); faked |
| The notice and template-status read (operation name Not specified in the source documents (GAP-2765; ASM-4599)) | P6 rwb-comms | The notice reference, the template status `current` or `withdrawn` and the template version of R-LIT-04; faked |
| The case answer, the route fact and the task raise (operation names Not specified in the source documents (GAP-2765; ASM-4599)) | P3 rwb-case | The case state, the route facts `NOTICE_BLOCKED`, `PACK_ASSEMBLY`, `PACK_VERIFIED` and `PACK_APPROVED`, and the task of R-LIT-04; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The approval item of `RWB-P7-E2013-CON`, base `/api/recovery/decision/v1` | P7 rwb-decision | The D7 approval of the substituted service or the filing under R-LIT-11, granted, refused or delayed; the delegation level and the clock are the approval's; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). None of the four is in this story's contract-dependency row, which is None, and every absence is recorded (GAP-2765, GAP-2771; ASM-4599, ASM-4605).

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and its catalogue events `LawsuitFiled`, `JudgmentRecorded` and `AuctionResult` belong to the stories that own the filing, the judgment and the auction result. This baseline declares none of them, adds no outbox row and widens no topic; the decision record is relayed by the library of DP-03 on `rwb.decision-record.v1` and is not an event of this service.

#### 12.4 Events consumed

None. The template withdrawal of R-LIT-04 and the prescription warning of R-LIT-11 arrive as synchronous answers of the comms and case contracts, and DP-09 is not in this key's pattern set; so this baseline declares no consumer group, no subscription and no inbox of its own, and the prescription clock is the case's (GAP-2765; ASM-4599).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-litigation` in namespace `rwb-recovery` | The stage that hosts the pack step; its signals and its outcome for the parent are declared, not built |
| `verifyPack` | Activity, the one pack verification step | `rwb-litigation` | The case and the legal action in; the rule ID with its package version, the outcome and the case route fact out |
| `authoriseFiling` | Activity, the one authorisation step | `rwb-litigation` | The approval code, the rule ID with its version, the `PACK_APPROVED` route fact and the decided-at time out |

`prescriptionApproval` is rwb-decision's child workflow on queue `rwb-decision` and is declared here as another owner's; no child workflow of this service holds the prescription clock or the D7 limit. The activity names are target design choices and no activity is registered by this story.

#### 12.6 Schedules

None. The pack step runs from the officer's act and from the case answer; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table, and no Job of Architecture v5 slide 44 is owned or moved here.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | The action, its action type, its facts and its status; the table the three operations read and the verification and authorisation write |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked decision record of each rule answer (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated POST or PATCH and the answer it holds |

`document` (P5), the notice (P6), `recovery_case`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and the approval item (P7) and `hearing` (S4, the sibling stories') are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-document pack fake | The pack of 2026-12-09 for case `RC-2026-000704` with every defect list item present for action `LA-2026-000704`; a pack with one missing item; no answer beyond 2 s | AC2, AC3, AC6 |
| rwb-comms notice fake | Notice `NT-2026-000704` with template status `current` and `withdrawn`, each with its template version | AC3, AC6 |
| rwb-case case fake | The case states `NOTICE_GENERATED`, `NOTICE_UNSERVED` and `PACK_ASSEMBLY`; an accepted and a refused route fact; an accepted and a refused task raise | AC3, AC6 |
| rwb-decision approval fake | The D7 item granted, refused with a reason, and delayed beyond 2 s | AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC4, AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names, the element names and the field lists that no source gives are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2765, GAP-2770; ASM-4599, ASM-4604).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 4 consumed | The create, read and patch of the legal action on `/api/recovery/litigation/v1`; the pack, notice, case and approval answers; one hop, 2 s |
| Kafka | None declared | No event published and none consumed by this step; the decision record is the library's on `rwb.decision-record.v1` |
| Temporal | 1 workflow and 2 activities declared, 0 registered | `LitigationWorkflow`, `verifyPack` and `authoriseFiling` on `rwb-litigation`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no legal action, no case, no task, no notice and no rule package. What it publishes is one OpenAPI 3.1 document, one AsyncAPI fragment that declares no event, nine contract tables and five fakes.

**Deliverables.** The additive document `openapi/rwb-litigation-v1.yaml` for this step, the verification and authorisation elements, the vocabulary of `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS` as published enumerations, the contract README rows for the consumed answers and their placeholders, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-13 moves the base and nothing else; DP-19 is behind SCR-18 and SCR-19, whose screen model is the edge contract's; DP-03 declares the record element and no payload of this service. DP-09 is not in the pattern set of this key, which is why no event is declared in 12.3 or 12.4.

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, while the plan's build list for this story is None; this baseline builds against their fakes until those platform contract stories publish. The four consumed owners have no C row and the absence is recorded (GAP-2765; ASM-4599).

**Build steps**

1. Write the three operations and validate the additive rule of AC1 in the pipeline.
2. Write the verification and authorisation elements of AC2 with the placeholder on the fields the sources do not give.
3. Record the consumed pack, notice, case and approval rows of AC3 with their owner, their budget and their placeholders.
4. Record the decision-record element of AC4 and validate it against the library schema.
5. Record the error envelope, the rights and the `Idempotency-Key` rule of AC5.
6. Publish the five fakes of AC6 and the drift test.
7. Record the naming baseline and the boundary of AC7, including the exclusion of API-S4-001, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the seven contract tests pass, the five fakes answer every consumed path and the drift test is green, and the app story, the two screens and the wave 3 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the litigation pack, which the app story raises on the document answer, so no path of this baseline raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key. It names the expiry of the claim on the case, which is the prescription fact of the case of record, so no path of this step raises it | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Litigation right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the legal action changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. The two carried messages are in the message set of this feature and no path of the baseline raises them.

### 15. Screens and states

The contract serves SCR-18 Notice approval in its generated, approved, sent, delivered and unserved states and SCR-19 Litigation workspace in its pack, instructed, filed, hearing and judgment states, all through the gateway-bff composite route (DP-19). The route calls rwb-litigation for the legal action, the verification and the authorisation, rwb-document for the pack and its defect list, rwb-comms for the notice and its template status and rwb-case for the case and its route state; this baseline fixes the rwb-litigation answers only, and the composite route specification and the screen field list belong to `RWB-PLT-N001-CON`. The refusal, hold, not-recorded and failure states the app story shows read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-007-01 | AC1, AC2 | Contract | Case `RC-2026-000704` and action `LA-2026-000704`; the contract half answers the three operations, the pack action types, the status vocabulary and the two elements |
| TC-E5-007-02 | AC2, AC5 | Contract | Action `LA-2026-000704` at `OPEN`; the contract half answers the validation and the authorisation elements and the `Idempotency-Key` of the POST and the PATCH |
| TC-E5-007-03 | AC3 | Contract | Case `RC-2026-000704` at `NOTICE_GENERATED` with notice `NT-2026-000704` template status `withdrawn`; the contract half answers the hold, the route fact and the task raise with their placeholders |
| TC-E5-007-04 | AC4, AC6 | Contract | The decision-record stub stopped and a refused approval; the contract half answers the MSG-P7-003 path and the five fakes of AC6 |
| TC-E5-007-05 | AC5, AC7 | Contract | A role without the Litigation right and a malformed request; the contract half answers the 403 with MSG-P4-002 and the 400 of the envelope, and the absence test for a `v_ace_*` read, a `document`, notice, case or task property, a second topic and a Schedule |
| TC-E5-007-06 | AC6, AC7 | Contract | The five fakes compared with the document, a drifted fake failing the build, and the exclusion of API-S4-001 from the provided set |
| TC-S4-E5007-CON-01 | AC1 | Contract | The document validates; the three operations, the base, the six action types, the six status values and the pack action types are present, and no pack or approval property is added |
| TC-S4-E5007-CON-02 | AC2, AC5 | Contract | The verification and authorisation elements validate; the `Idempotency-Key` rule and the seven error responses with one message ID per condition |
| TC-S4-E5007-CON-03 | AC3, AC4, AC6, AC7 | Contract | The four consumed rows and the decision-record element validate with their placeholder fields; the five fakes match the document; the absence test and the API-S4-001 exclusion pass |

The six legacy cases are the legacy cases of RWB-E5-007 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by `RWB-S4-E5007-APP`. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The three cases `TC-S4-E5007-CON-01` to `-03` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the checklist rows, the 90-day threshold, the D7 limit, the lists and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, amounts, dates, list values and a rule version only; every example is synthetic.
- The pack stays with rwb-document and the notice with rwb-comms: the document declares no `document` property, no notice property, no document write and no dispatch (BR3, BR4).
- The case, its task and its timers are answered and not written: the document declares no `recovery_case`, `task` or `timer` property (BR4).
- ACE data only through the owner's contract: the document declares no `v_ace_*` view and no grant on another `rwb_*` schema, and the boundary test fails a build that adds one (DP-05).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-litigation; a consumed operation is described as consumed and faked, never as provided, and API-S4-001 is not in the provided set (DP-01, DP-11, BR11).
- The error envelope, the `Idempotency-Key` rule and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S4-003 | The litigation officer verifies the pack against the defect list before filing is approved; the contract fixes the action types, the verification and authorisation elements and the answers on which the rule is evaluated (FSD S4 requirements served; the legacy master carries no requirement ID (GAP-2769; ASM-4603)) | The three operations, the vocabulary, the two elements and the four consumed rows | TC-E5-007-01, TC-E5-007-03, TC-S4-E5007-CON-01, TC-S4-E5007-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-S4-E5007-CON-02, TC-S4-E5007-CON-03 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-007, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by `RWB-S4-E5007-APP`; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the three new contract cases TC-S4-E5007-CON-01 to -03 |
| Feature and screens | FEAT-LIT-07, SCR-18 Notice approval and SCR-19 Litigation workspace |
| Rules | R-LIT-04, R-LIT-11, R-LIT-16, R-LIT-21 and R-LIT-23, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the three operations, the evaluation of R-LIT-04, R-LIT-11, R-LIT-16 and R-LIT-21, the decision record and the authorisation: `RWB-S4-E5007-APP`.
- The pack, its documents, its checklist and the defect list, and the message MSG-S4-001 as an authored message: rwb-document (P5) (GAP-2765; ASM-4599).
- The notice, its template, its dispatch and the notice approval operation API-S4-001: rwb-comms (P6) and the E2 notice story of this service (GAP-2771; ASM-4605).
- The case of record, its route states, the task and the timers: rwb-case (P3).
- The approval item at D7, the delegation of authority table and its clock, and the rule rows of the five rules: rwb-decision (P7), `RWB-P7-E2013-CON`.
- The firm selection and the instruction of R-LIT-23: `RWB-S4-E5008-APP` and rwb-partner (S9).
- The filing itself, the hearings, the judgment and the enforcement steps: the sibling stories of this service, including API-S4-005.
- The ACE account and batch facts and the reference data themselves: rwb-source-data (P1), rwb-case (P3) and rwb-access (P4).
- The gateway-bff composite route and the screen field list of SCR-18 and SCR-19: `RWB-PLT-N001-CON` and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
