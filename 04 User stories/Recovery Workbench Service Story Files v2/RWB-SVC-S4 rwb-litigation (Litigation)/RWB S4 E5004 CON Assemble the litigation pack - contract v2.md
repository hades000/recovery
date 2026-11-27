# RWB-S4-E5004-CON Assemble the litigation pack - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5004-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Contract version | Major version 1, base `/api/recovery/litigation/v1` |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S4-E5004-CON-16) |
| Depends on (build) | None |
| Contract dependencies | P3, P5, P8 and P10 contract stories, built against their published fakes; the consumed reads API-P3-002, API-P5-002 and API-P5-008 are non-blocking |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E5-004 for rwb-litigation (S4). The legal action that carries the litigation pack is published on Day 1 on base `/api/recovery/litigation/v1` with API-S4-002, API-S4-003 and API-S4-004, the `legal_action` DDL template, the case-state and task hand-over shapes, the consumed document-index and case-facts shapes, the fakes and the drift test; the four legacy acceptance criteria stay with RWB-S4-E5004-APP and every criterion here is new. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S4-E5004-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (9 resolved, 15 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **contract owner of rwb-litigation (S4)**, I want **the published contract of the legal action that carries the litigation pack — the base `/api/recovery/litigation/v1` with API-S4-002 create, API-S4-003 read and API-S4-004 patch, the `LegalActionRequest`, `LegalAction` and `LegalActionUpdate` schemas with the court and filing fields and the pack item references, the `legal_action` DDL template with DF-LEG-001 to DF-LEG-014, the `Idempotency-Key` rule, the error envelope, the declared right of each operation, the case-state and task hand-over shapes, the consumed document-index and case-facts shapes, the fakes and the drift test** instead of the monolith's in-process controller and its one `recovery.legal_action` table, so that **RWB-S4-E5004-APP and every later litigation story build against one frozen, testable shape from Day 1, and a court field, a status value, a pack state or an error status can never drift between rwb-litigation, rwb-document and rwb-case without a failing build**.

This story owns the contract and nothing else:

- the OpenAPI 3.1 document of the legal action resource: the base, the three operations, the three object schemas, the problem schema, the security and the error set;
- the pack sub-shape of the read: the pack item references, the checklist reference and the two state facts the workspace reads, declared as read elements and never as columns;
- the `legal_action` DDL template with the columns and types of TSD S4 T3.1 and the standard columns of T3.0, applied in this service's own schema with no cross-schema key;
- the element naming rule (camelCase after the DF-LEG field identifiers), the required set and the enumeration rule that names a list code and no member list;
- the `Idempotency-Key` rule on the two write operations, the compatibility rule and the pinning rule;
- the shapes this service hands to rwb-case and the shapes it reads back, and the shapes it consumes from rwb-document and rwb-case;
- the fake set generated from the document, and the drift test every consuming build runs.

It does not build the pack. The composition, the two rule evaluations, the decision record, the task raise and the state announcement are `RWB-S4-E5004-APP`'s; the document index is rwb-document's; the case, its states and its tasks are rwb-case's. The document declares shapes and moves nothing.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020), and the litigation service has one base and one document for its legal actions. The legacy key RWB-E5-004 built the pack inside one process against one `recovery` schema, with the case, the documents, the notice, the task and the decision log entry all in reach. Three of those are now other services' rows and every one is reached on a published shape, so each shape has to be fixed before the app story starts: the three operations and their bodies, the court fields the pack writes, the pack items the read returns, the decision record the service writes in its own transaction, and the two state facts it hands over.

Two points are structural rather than stylistic. The pack has no table: the Ownership Map gives this service `legal_action` and `hearing` only, and TSD S4 T3.1 has the same two objects, so the pack is a composition over rwb-document's index and rwb-case's case facts and the document declares it as a read view and not as a row (GAP-2753; ASM-4583). And the pack states are not status values: LOV-LEGAL-STATUS has six members of which none is `PACK_ASSEMBLY`, `PACK_VERIFIED`, `NOTICE_BLOCKED` or `PACK_DEFECT_HOLD`, so the states that R-LIT-04, R-LIT-16, R-LIT-17 and R-LIT-21 move are states of the case of record; the document fixes the announcement shape and declares no seventh status (GAP-2754; ASM-4584).

The legacy endpoint block of the key names two operations: `POST monolith-base/notices/{noticeId}/approve` with right A, which is the notice stories' of this service, and `POST monolith-base/cases/{caseId}/legal-actions` with right C, which is this resource's. The pack has no operation of its own in any source, so the document publishes the legal action that carries it and not a second resource (GAP-2755; ASM-4585).

The baseline also fixes the naming the checks require: schema `rwb_litigation`, login `rwb_litigation`, base `/api/recovery/litigation/v1`, topic `rwb.litigation.events.v1` with retry and `.dlt` topics, event names `rwb.litigation.<Event>.v1`, task queue `rwb-litigation` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.litigation`. It keeps the operation IDs the TSD allocates, API-S4-002 create, API-S4-003 read and API-S4-004 patch.

It serves FEAT-LIT-04 "Assemble the litigation pack" through the shape of its legal action, and it traces to that feature until the Epics 3 to 8 PRD adds requirement identifiers, because the legacy master and the Epics 3 to 8 specification carry none for this key (GAP-2752; ASM-4582).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the event names and the package follow the platform rule and not a local choice.
- The platform error envelope and its `messageId` extension are the platform baseline; where this document narrows them it does so explicitly, and the envelope is reused and never redeclared.
- The reference lists of the legal action are read with their version: LOV-LEGAL-TYPE (`NOTICE`, `CIVIL_CASE`, `APPEAL`, `ENFORCEMENT`, `BANKRUPTCY_PETITION`, `LED_AUCTION`) and LOV-LEGAL-STATUS (`OPEN`, `FILED`, `JUDGMENT`, `ENFORCING`, `CLOSED`, `WITHDRAWN`) of TSD S4 T3.2. The document names the list codes and their members as the TSD enumerates them; the version in force is read at run time.
- The `legal_action` row is the TSD S4 T3.1 row, DF-LEG-001 to DF-LEG-014, plus the seven standard columns of T3.0. No field outside that row is declared, because no source gives one for the pack.
- The decision record is the local decision-record library's (`RWB-PLT-E1027-CON`); this document names the element it needs and fixes none of the library's fields.
- The document index of rwb-document is read on `GET /cases/{caseId}/documents` (API-P5-002) and `GET /cases/{caseId}/document-checklist` (API-P5-008), both built in Epic 1 (FEAT-DCM-02); the case facts on `GET /cases/{caseId}` (API-P3-002). The case-state and task operations have no published name and carry the placeholder (GAP-2751; ASM-4581).
- No build dependency: this story is Day 1 by rule (Template and Rules section R5.7 rule 1), and every consuming story of the service builds against it and its fake.

### 4. Flow

1. Draft the OpenAPI 3.1 document of the legal action resource on base `/api/recovery/litigation/v1`: API-S4-002, API-S4-003 and API-S4-004 with their request and answer bodies, their rights and their error sets.
2. Fix the `LegalAction` element set from DF-LEG-001 to DF-LEG-014 in camelCase, with the required set of TSD S4 T3.1 and the two list references of T3.2.
3. Fix the pack sub-shape of the read: the pack item references, the checklist reference and the two case-state facts, declared as read-only elements of the answer and not as columns of the row.
4. Write the `legal_action` DDL template with the columns, the physical types, the widths, the keys and the standard columns; carry the index set as a gap.
5. Write the decision-record element and the two hand-over shapes: the case-state announcement and the task raise to rwb-case, with the placeholder on the two operation names.
6. Write the two consumed shapes: the document index and the checklist of rwb-document, and the case facts of rwb-case.
7. Write the `Idempotency-Key` rule on the two write operations, the compatibility rule and the pinning rule.
8. Generate the fake set from the document and wire the drift test into the build of this story and of `RWB-S4-E5004-APP`.
9. Publish v1, record the pinned version of each consuming story, and hand the baseline to the sibling S4 stories and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | None | AC1 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC8 |
| X3 | A fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC7 |
| X4 | A value of `actionType` outside LOV-LEGAL-TYPE is sent | The document refuses it as an enumeration error at 422 and no row is written | MSG-GEN-001 | AC2 |
| X5 | The operation is called without the `Idempotency-Key` header | The document refuses the request at 400 and the fake answers the same; no stored answer exists | None | AC3 |
| X6 | A pack state is declared as a value of `status` | The document lint fails against LOV-LEGAL-STATUS and the review rejects it | None | AC5 |
| X7 | The index set of `legal_action` is guessed | The template carries the placeholder and the gap, and declares the primary key only | None | AC4 |
| X8 | A retired element reappears in the document | The absence test fails: no old monolith base, no second topic, no table of another schema, no pack table | None | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads TSD S4, the P5 and P3 documents and the platform envelopes, and consumes no service at build time |
| Negotiable | The index set, the two hand-over operation names and the pack-item composition rule are settled with their owners; the base, the operation IDs, the columns and the list codes are fixed by the target architecture |
| Valuable | Unblocks the app story on Day 1 and the sibling S4 stories that read the same legal action |
| Estimable | One OpenAPI document, one DDL template, four consumed or handed-over shapes, one fake set and eight contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the legal action that carries the litigation pack

  Background:
    Given the service naming rule of the platform library is in force
    Given the legal action of rwb-litigation is served on the base /api/recovery/litigation/v1
    Given the reference lists are LOV-LEGAL-TYPE and LOV-LEGAL-STATUS of TSD S4 T3.2, read with their version in force

  Scenario: AC1 The three legal-action operations are declared and no pack resource is added (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-litigation is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /cases/{caseId}/legal-actions as API-S4-002, GET /legal-actions/{legalActionId} as API-S4-003 and PATCH /legal-actions/{legalActionId} as API-S4-004, all under the base /api/recovery/litigation/v1 and owned by rwb-litigation
    Then the LegalAction schema carries id, caseId, lawFirmId, actionType, lawsuitNo, blackCaseNo, redCaseNo, courtName, claimAmount, filedDate, judgmentDate, judgmentAmount, litStatus and status
    Then the document declares no pack resource, no pack path and no second base, and it declares no operation of another service
    Then every operation ID of TSD S4 T-A.1 that this story publishes is kept and no operation is renumbered
    Then API-S4-001 and API-S4-005 are declared as other stories' and never as operations of this document (GAP-2755; ASM-4585)

  Scenario: AC2 The pack sub-shape of the read and the closed vocabularies are fixed (new, D-RCV-60)
    Given the LegalActionRequest, LegalAction and LegalActionUpdate schemas of the document
    When the pack sub-shape and the two list references are reviewed
    Then the read answer carries the pack item references, the checklist reference and the two case-state facts as read-only elements, and no element of them is declared as a column of legal_action
    Then actionType names LOV-LEGAL-TYPE and CIVIL_CASE is one of its values, and status names LOV-LEGAL-STATUS with its six values
    Then the document declares no seventh status value and it declares PACK_ASSEMBLY, PACK_VERIFIED, PACK_DEFECT_HOLD and NOTICE_BLOCKED as case-state facts only
    Then LegalActionRequest requires actionType and carries caseId from the path, claimAmount, courtName, lawFirmId, lawsuitNo and blackCaseNo as optional properties
    Then LegalActionUpdate carries filedDate, courtName, blackCaseNo, lawsuitNo and claimAmount
    Then a value of actionType outside LOV-LEGAL-TYPE is refused at 422 with MSG-GEN-001 naming the property
    Then a state fact sent in the body of a request is refused as an unknown property and changes nothing

  Scenario: AC3 The Idempotency-Key rule, the error envelope and the declared right of each operation are fixed (new, D-RCV-60)
    Given the operation table of the document
    When it is reviewed against TSD S4 T-A.1 and T-A.2
    Then API-S4-002 and API-S4-004 declare the Idempotency-Key header and a stored answer, and API-S4-003 declares no Idempotency-Key
    Then the error responses are 401, 403, 404, 409, 422 and 503 as the TSD rows give them, each with the platform problem document and one message ID per condition
    Then a body that cannot be parsed answers 400 with the same envelope, a code no S4 T-A row names and carried as a gap (GAP-2757; ASM-4587)
    Then the declared rights are Litigation C on the create, Litigation R on the read and Litigation U on the patch, with the scope applied and the role lists held by rwb-access
    Then a caller without the right is refused at 403 with MSG-P4-002 and changes nothing
    Then the document declares no right of its own invention and no role code as a constant

  Scenario: AC4 The legal_action columns are declared and the index set is carried as a gap (new, D-RCV-60)
    Given the legal_action DDL template of schema rwb_litigation
    When it is compared with TSD S4 T3.1 and T3.0
    Then the template declares DF-LEG-001 to DF-LEG-014 with their physical types, widths and required flags, and the seven standard columns
    Then case_id and law_firm_id are identifiers with no foreign key across schemas
    Then status is varchar(15) against LOV-LEGAL-STATUS and action_type is varchar(20) against LOV-LEGAL-TYPE, both closed by the list and not by a check constraint of their members
    Then the index set beyond the primary key on id is Not specified in the source documents (GAP-2757; ASM-4587) and the template declares the primary key only
    Then the template is applied by the service's own Flyway sequence and never edits an applied migration (DP-15)
    Then no pack table and no pack column is declared, and the holding of a written table is a new major version (GAP-2753; ASM-4583)

  Scenario: AC5 The case-state announcement handed to rwb-case is fixed and no pack state becomes a status (new, D-RCV-60)
    Given the case-state element of the document and the state rows of TSD S4 T4 and the Business Rules and Routing Logic
    When they are compared
    Then the announcement this service hands over carries the case reference, the legal action reference, the state fact, the rule ID and the version in force
    Then the state facts are NOTICE_BLOCKED from R-LIT-04, PACK_ASSEMBLY from R-LIT-15, PACK_VERIFIED from R-LIT-16, PACK_DEFECT_HOLD from R-LIT-17 and PACK_ASSEMBLY from R-LIT-21
    Then the answer shape carries the accepted or refused outcome and the state the case of record holds, and no case field is written here
    Then the operation name of the announcement and the field list of the answer are Not specified in the source documents (GAP-2751; ASM-4581)
    Then the 1, 2, 3 and 5 working days of the rules are declared as case-task service levels and not as timers of this service (GAP-2754; ASM-4584)

  Scenario: AC6 The task raise and the consumed document-index and case-facts shapes are fixed (new, D-RCV-60)
    Given the task element of the document and the P5 and P3 documents
    When the shapes are compared
    Then the task raise this service hands over carries the case reference, the task code, the capability area, the rule ID and its version
    Then the consumed read of the document index is GET /cases/{caseId}/documents as API-P5-002 and the checklist is GET /cases/{caseId}/document-checklist as API-P5-008, both described as consumed and never as provided
    Then the consumed read of the case facts is GET /cases/{caseId} as API-P3-002, described as consumed
    Then the operation name of the task raise and the field list of its answer are Not specified in the source documents (GAP-2751; ASM-4581)
    Then the document fixes no pack item list, no template status and no checklist item as a constant
    Then it declares no read of another service's table and no v_ace_ view

  Scenario: AC7 The contract fakes answer the document and the drift test blocks a drifted build (new, D-RCV-60)
    Given the fake set generated from the document
    When each fake is compared with the operation or the element it serves
    Then the legal-action fake answers the 201 create, the 200 read, the 200 patch, the 400, 401, 403, 404, 409, 422 and 503 refusals, and the repeated Idempotency-Key
    Then the document-index and case-facts fakes answer the complete, the incomplete, the out-of-scope and the delayed case
    Then the case-state fake answers the accepted state fact, the refusal from another state and a delayed answer
    Then the task fake answers the task created and a refusal
    Then the decision-record library stub answers a healthy chain and a stopped chain
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC8 The naming baseline and the boundary of the document are fixed (new, D-RCV-60)
    Given the naming and boundary section of the document
    When it is reviewed against the Template and Rules and the Ownership Map
    Then the base is /api/recovery/litigation/v1, the schema and the login are rwb_litigation, the topic is rwb.litigation.events.v1 with retry and .dlt topics, the event names are rwb.litigation.<Event>.v1, the task queue is rwb-litigation in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.litigation
    Then the document declares no event of its own and this story publishes none, because the service owns no event (GAP-2756; ASM-4586)
    Then the document declares no read of another service's table, no cross-schema join and no v_ace_ view, and it names recovery_case, task, document, notice, decision_log_entry and rule_row as other owners' consumed shapes only
    Then the old monolith base appears nowhere in the document, its examples or its fakes
    Then the document names no second topic, no second queue and no pack table
```

These eight criteria are new for the contract baseline and test the artefact only; they restate no business outcome of `RWB-S4-E5004-APP` and they copy no criterion of the legacy story. The wave 3 harness that consumes this baseline copies none of them.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/litigation/v1`; the document never declares another service's path as provided | DP-13; Template and Rules section R5.5 |
| BR2 | The three operations keep their TSD operation IDs API-S4-002, API-S4-003 and API-S4-004, and no pack operation and no fourth operation of this resource is declared | TSD S4 T-A.1; legacy Endpoints block |
| BR3 | `action_type` and `status` are declared as enumerations of LOV-LEGAL-TYPE and LOV-LEGAL-STATUS, and the code names the list and never a member list curated locally | TSD S4 T3.2; FSD S4 A2.4.3.1 (BR-S4-004) |
| BR4 | The pack states are case facts and never status values: the six members of LOV-LEGAL-STATUS are the whole list and no seventh is declared | TSD S4 T3.2 and T4; R-LIT-04, R-LIT-15, R-LIT-16, R-LIT-17, R-LIT-21 |
| BR5 | A read declares no `Idempotency-Key`; a write declares it and stores its answer | TSD S4 T-A.1 and T-A.2 |
| BR6 | Error responses use one envelope and one message ID per condition; the business message texts are copied unchanged from the legacy story | Template and Rules section R7.2 (s14); legacy Validation and messages block |
| BR7 | A schema change is additive within a major version; a breaking change is a new major version, and the holding of a written table is a breaking change | Architecture v5 slide 42 notes (backward compatibility) |
| BR8 | The document lists only operations owned by rwb-litigation; a consumed operation or shape is described as consumed, never as provided | Ownership Map v1 |
| BR9 | No business value is fixed in the contract: the pack item list, the template status, the checklist, the task code, the service levels and the index set stay data or reference data | Template and Rules section R7.2 (s17) |
| BR10 | The decision record is the local library's element on the shared topic, never a new event of this service, and its fields are the library's | DP-03; Template and Rules section R5.5 |
| BR11 | No personal data in a schema, an example or a fake: identifiers, document references, list values, dates and amounts only | TSD S4 T3.1; Architecture v5 slide 8 notes |
| BR12 | No ACE view and no ACE table is declared or read by this document | DP-05; Ownership Map v1 |

### 9. State transitions

The document's own lifecycle is the only state this story moves:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The three operations, the pack sub-shape, the template and the four shapes are described | In review |
| In review | Consumer sign-off | `RWB-S4-E5004-APP` and the sibling S4 stories accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1, for example a new court reference | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, a column of the template changes, or a list code changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |

Two vocabularies are declared and neither is moved here:

| Object | Values | Note |
|---|---|---|
| legal_action.action_type | `NOTICE`, `CIVIL_CASE`, `APPEAL`, `ENFORCEMENT`, `BANKRUPTCY_PETITION`, `LED_AUCTION` (LOV-LEGAL-TYPE) | Declared as the list reference; the pack's action is `CIVIL_CASE` |
| legal_action.status | `OPEN`, `FILED`, `JUDGMENT`, `ENFORCING`, `CLOSED`, `WITHDRAWN` (LOV-LEGAL-STATUS) | Declared as the list reference; the moves between the values are the app story's |
| The case's pack state | `NOTICE_BLOCKED`, `PACK_ASSEMBLY`, `PACK_VERIFIED`, `PACK_DEFECT_HOLD` | **Not** a value of either list; a state of the case of record, declared here only as the announcement shape (BR4) |

The pack state machine — which event moves the case and what a rejected pack leaves behind — belongs to `RWB-S4-E5004-APP` and appears nowhere in this document beyond the five rows of AC5, which name the rule that announces each state and not the transition itself.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-litigation | Owns the OpenAPI document, the DDL template and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes |
| Consuming teams (`RWB-S4-E5004-APP`, the sibling S4 stories, and the rwb-document and rwb-case owners whose shapes are consumed) | Review and sign off the parts they consume |
| Platform library owner | Owns the problem envelope, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an element, an example or a fake |
| Business analyst of S4 | Confirms that the two lists are named as list codes, that the pack states stay out of `status`, and that no member list is curated locally |

The login behind the document's security scheme is `rwb_litigation` by the naming rule of DP-02; the document names the scheme and not a credential, and no role, level or mask is defined here. Each operation's right is checked at its edge by the rwb-access authorise check of DP-08 before the operation runs; a caller whose role does not hold the right receives MSG-P4-002.

### 11. Data

The contract baseline declares shapes, not business values.
Reference data: the lists LOV-LEGAL-TYPE and LOV-LEGAL-STATUS are read through the reference-data contract of DP-06 and DP-07. The parameters, namely the pack item list, the template status, the checklist, the task code, the service levels and the index set, are read as data or reference data and are never declared here.

| BR Field ID | Element | Type and width | Required | List |
|---|---|---|---|---|
| DF-LEG-001 | id | uuid | Yes | None |
| DF-LEG-002 | caseId | varchar(255) | Yes | None |
| DF-LEG-003 | lawFirmId | uuid | No | None |
| DF-LEG-004 | actionType | varchar(20) | Yes | LOV-LEGAL-TYPE |
| DF-LEG-005 | lawsuitNo | varchar(30) | No | None |
| DF-LEG-006 | blackCaseNo | varchar(30) | No | None |
| DF-LEG-007 | redCaseNo | varchar(30) | No | None |
| DF-LEG-008 | courtName | varchar(120) | No | None |
| DF-LEG-009 | claimAmount | numeric(18,2) | No | None |
| DF-LEG-010 | filedDate | date | No | None |
| DF-LEG-011 | judgmentDate | date | No | None |
| DF-LEG-012 | judgmentAmount | numeric(18,2) | No | None |
| DF-LEG-013 | litStatus | varchar(200) | No | None |
| DF-LEG-014 | status | varchar(15) | Yes | LOV-LEGAL-STATUS |
| T3.0 standard columns | state, version, created_at, created_by, updated_at, updated_by, is_active | boolean, varchar(40), integer, timestamptz, uuid | n/a | None |

| Item | Content | BR Field ID |
|---|---|---|
| Pack sub-shape of the read | The pack item references, the checklist reference and the two case-state facts. Read-only elements of the answer, never columns of the row: the pack table does not exist (GAP-2753; ASM-4583). The pack is derived on every read from API-P5-002, API-P5-008 and API-P3-002; no pack, pack_item or pack_checklist table and no column of legal_action holds it | Not specified in the source documents (DOR-RWB-S4-E5004-CON-7) |
| Index set | Beyond the primary key on `id` the set is `Not specified in the source documents (GAP-2757; ASM-4587)`; the template declares the primary key only | Not specified in the source documents (DOR-RWB-S4-E5004-CON-7) |
| Decision record | The element the library writes: the decision code, the rule ID and version, the inputs reference, the final call, the decided time and the two hashes. The library owns the fields and the chain (DP-03) | Not specified in the source documents (DOR-RWB-S4-E5004-CON-7) |
| Case-state announcement | The shape handed to rwb-case and read back; its operation name is absent (GAP-2751; ASM-4581). The four pack states NOTICE_BLOCKED, PACK_ASSEMBLY, PACK_VERIFIED and PACK_DEFECT_HOLD are case states of rwb-case and never legal_action status (GAP-2754) | Not specified in the source documents (DOR-RWB-S4-E5004-CON-7) |
| Task raise | The shape handed to rwb-case for the pack hold of R-LIT-04; its operation name is absent (GAP-2751; ASM-4581) | Not specified in the source documents (DOR-RWB-S4-E5004-CON-7) |
| Document index and checklist | The consumed shapes of API-P5-002 and API-P5-008, described and never provided | Not specified in the source documents (DOR-RWB-S4-E5004-CON-7) |

**No new table, no new column and no migration.** `legal_action` is the TSD S4 T3.1 row and this document publishes its DDL template for the service's own Flyway sequence (DP-15); `decision_record` and `idempotency_key` are platform library objects created in `rwb_litigation` by the library's migration and are named here, not declared. `recovery_case` and `task` (P3), `document` (P5), `notice` (P6), `decision_log_entry` and `rule_row` (P7) and every `v_ace_*` view (P1) are other owners' and are named as consumed shapes only. `legal_action.case_id` and `law_firm_id` are identifiers, not foreign keys across schemas (DP-01).

**No personal data.** No element of this contract carries a name, an address, an identity number or an account number. The document references, the court references and the amounts are not personal data, and the borrower and the guarantor are reached by the services that need them through rwb-source-data.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13). This story publishes all three operations.

| ID | Method | Path | Request | Response | Access | Idempotency | Errors |
|---|---|---|---|---|---|---|---|
| API-S4-002 | POST | `/cases/{caseId}/legal-actions` | `LegalActionRequest`; `caseId` from the path | 201 with `LegalAction` in status `OPEN` | Litigation C, scope applied | `Idempotency-Key` required, answer stored | 401, 403, 404, 409, 422, 503 |
| API-S4-003 | GET | `/legal-actions/{legalActionId}` | None | 200 with `LegalAction` and the pack sub-shape | Litigation R, scope applied | Not applicable | 401, 403, 404, 503 |
| API-S4-004 | PATCH | `/legal-actions/{legalActionId}` | `LegalActionUpdate`; the court references and the filing date | 200 with `LegalAction` | Litigation U, scope applied | `Idempotency-Key` required, answer stored | 401, 403, 404, 409, 422, 503 |

The purpose, entities, rights, idempotency and error statuses are those of TSD S4 T-A.1 and T-A.2 for API-S4-002, API-S4-003 and API-S4-004, with the base renamed by DP-13. API-S4-001 `POST /notices/{noticeId}/approve` and API-S4-005 `POST /legal-actions/{legalActionId}/hearings` are not declared here: the notice approval is the notice stories' of this service and the hearing is `RWB-S4-E5011-APP`'s, and the legacy endpoint block of RWB-E5-004 names the first of them only because the notice precedes the pack (GAP-2755; ASM-4585).

#### 12.2 REST operations consumed

None: a contract document calls no service. The rows below are the shapes this service consumes and the shapes it **hands over**; the document declares them and the calls are `RWB-S4-E5004-APP`'s.

| Shape | Owner | Declared here | Open point |
|---|---|---|---|
| The document index | P5 rwb-document (`GET /api/recovery/document/v1/cases/{caseId}/documents`, API-P5-002) | The consumed request and the item list the pack is composed from | None: the operation is published by the P5 document, and no C row carries it (GAP-2751; ASM-4581) |
| The document checklist | P5 rwb-document (`GET /api/recovery/document/v1/cases/{caseId}/document-checklist`, API-P5-008) | The consumed request and the checklist rows the pack is measured against | None: published, and no C row carries it (GAP-2751) |
| The case facts | P3 rwb-case (`GET /api/recovery/case/v1/cases/{caseId}`, API-P3-002) | The consumed request and the case facts the pack's cover sheet needs | None: published, and no C row carries it (GAP-2751) |
| The case-state announcement and its answer | P3 rwb-case | The state fact, the legal action reference, the rule and its version, and the accepted or refused answer | The operation name and the field list of the answer are Not specified in the source documents (GAP-2751; ASM-4581) |
| The task raise for the pack hold | P3 rwb-case | The case reference, the task code, the capability area, the rule ID and its version | The operation name is Not specified in the source documents (GAP-2751; ASM-4581) |

Every call is one hop with a 2 s timeout in the app story's implementation (ADR-020). No operation of another service is declared as provided here (BR8).

#### 12.3 Events published

None. The service owns no event in the Ownership Map (Events: 0), DP-09 is not in either story's pattern set, and the pack assembly raises no business event. The service topic `rwb.litigation.events.v1` carries `LawsuitFiled`, `JudgmentRecorded` and `AuctionResult` in the event catalogue, and no source ties the assembly of a pack to any of them (GAP-2756; ASM-4586). The decision record is written through the local decision-record library of DP-03, which publishes `DecisionRecorded` on the shared `rwb.decision-record.v1`; that element is the library's and this document declares no payload of its own.

#### 12.4 Events consumed

None. The document index, the checklist, the case facts, the state facts and the task are synchronous answers of their contracts, so the document names no subscription and no inbox. `NoticeDelivered` and `PartnerResultSubmitted`, the two inputs the catalogue gives rwb-litigation, belong to the notice and firm-result stories and are not declared here.

#### 12.5 Workflows and activities

None. The document defines no workflow and no activity. `LitigationWorkflow` is the app story's, on task queue `rwb-litigation` in namespace `rwb-recovery`; this baseline fixes only the names the app and operations stories register, and the assembly activity's own type name and registration are Not specified in the source documents (GAP-2756; ASM-4586).

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job is declared; the 1, 2, 3 and 5 working days of the rules are case-task service levels on rwb-case and not timers or Schedules of this service.

#### 12.7 Tables owned

| Table | Schema | Owner | Note |
|---|---|---|---|
| legal_action | `rwb_litigation` | S4 | The DDL template of section 11: DF-LEG-001 to DF-LEG-014, the seven standard columns, the primary key on `id` and no cross-schema key (DP-01, DP-15) |
| decision_record | `rwb_litigation` | PLT library object applied in this schema | Named only: the shape is `RWB-PLT-E1027-CON`'s and the row is written in the caller's transaction (DP-03) |
| idempotency_key | `rwb_litigation` | PLT library object applied in this schema | Named only: the stored answer of the two write operations |

`hearing` is S4's and belongs to `RWB-S4-E5011-APP`; there is no pack table to declare (GAP-2753). `recovery_case` and `task` (P3), `document` (P5), `notice` (P6), `decision_log_entry` and `rule_row` (P7) are other owners' and appear only as consumed shapes. No table of another service is declared, read or keyed.

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Legal-action fake | The three operations of 12.1 | A 201 create in status `OPEN`, a 200 read with the pack sub-shape, a 200 patch to `FILED`, and the 400, 401, 403, 404, 409, 422 and 503 refusals |
| Repeated-key fake | The `Idempotency-Key` rule | The first answer returned again for the same key, with no second legal action |
| Document-index fake | API-P5-002 and API-P5-008 | A complete checklist, one item missing, an empty index, a 404 and a delayed answer |
| Case-facts fake | API-P3-002 | A case in `NOTICE_GENERATED`, one in `PACK_ASSEMBLY`, a 404 and a delayed answer |
| Case-state fake | The state announcement of 12.2 | The fact accepted, the refusal from another state, and a delayed answer |
| Task fake | The task raise of 12.2 | The task created with its identifier and a refusal |
| Decision-record library stub | DP-03 | A healthy chain with its outbox row, and a stopped chain |
| Template application | The `legal_action` DDL template | The table created twice in two throwaway schemas, with the standard columns, the primary key and no cross-schema reference |
| Drift test | Every fake against the document | A drifted fake fails the build |

The case-state and task fakes are stubbed from the P3 document and carry the placeholder until the two operation names are confirmed (GAP-2751).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 0 consumed by this document, 2 handed over | API-S4-002, API-S4-003 and API-S4-004 provided; the two hand-over shapes of 12.2 are declared for the app story and called by nobody here |
| Kafka | None | No event published and none consumed; `DecisionRecorded` is the library's element (12.3) |
| Temporal | None | No workflow, activity or Schedule (12.5) |
| File | None | No file element in this contract; the pack is composed from the index and no file is read here |

### 13. Solution plan

**Package.** Contract artefact of the service: the OpenAPI 3.1 document of the legal action resource, the `LegalActionRequest`, `LegalAction` and `LegalActionUpdate` schemas with the published types in `th.co.scb.ace.workbench.recovery.litigation.api`, the `legal_action` DDL template as a resource, and the fake set with the drift test. The implementation behind it is `RWB-S4-E5004-APP`.

**This document declares shapes and moves nothing.** It fixes the names, the types, the widths, the required set, the list references, the two write operations' `Idempotency-Key` rule, the pack sub-shape and the five shapes handed over or consumed. It writes no row, composes no pack, raises no task, announces no state and writes no decision record: every one of those acts is an application behaviour of `RWB-S4-E5004-APP`, and a contract that performed one would be a second implementation.

**Element surface**

| Element group | Elements | Required |
|---|---|---|
| Identity and case | `id`, `caseId`, `lawFirmId` | `id` and `caseId` yes; `lawFirmId` no |
| Type and status | `actionType`, `status` | both yes, each against its list |
| Court and claim | `lawsuitNo`, `blackCaseNo`, `redCaseNo`, `courtName`, `claimAmount` | none |
| Judgment and filing | `filedDate`, `judgmentDate`, `judgmentAmount`, `litStatus` | none |
| Pack, read only | the pack item references, the checklist reference and the two case-state facts | none in a request; they appear on the answer of API-S4-003 |
| Standard | `state`, `version`, `createdAt`, `createdBy`, `updatedAt`, `updatedBy`, `isActive` | none in the body; they are columns of the template |

The element names are the DF-LEG field names in camelCase; the mapping is one to one and is checked by the drift test. No element exists for a pack item beyond the document reference, because the pack is not a row (BR4, GAP-2753).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the document names the element and declares no record field of its own | referred to; the consuming story carries the dependency |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the base of this resource is `/api/recovery/litigation/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route; the resource is reached through it and the contract declares no composite route | referred to; the consuming story carries the dependency |

DP-13 is the pattern this story publishes. DP-03 is named and not declared: the record is the library's and the only trace on the resource is the decision element. DP-19 is the route the two screens use and is the platform edge story's. DP-01 and DP-15 stand behind the DDL template and add no dependency. DP-05 stands behind the boundary as a prohibition. DP-06, DP-07, DP-08 and DP-11 are not in this story's pattern set although the document names two list codes, a declared right and a consumed read; none adds a row (GAP-2751; ASM-4581).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| LegalActionOpenApi | Document | The base, the three operations, the schemas, the security, the error set and the versioning section (BR1 to BR7, BR11) |
| LegalActionSchema | Published schema | `LegalActionRequest`, `LegalAction` and `LegalActionUpdate` with the DF-LEG elements, the required set and the pack sub-shape (BR3, BR4) |
| LegalActionDdlTemplate | Resource | The `legal_action` DDL: columns, types, keys, the primary key and the standard columns (BR3, BR9) |
| PackView | Published schema | The read-only pack sub-shape of the answer, declared once and reused by the workspace (BR4) |
| ProblemEnvelope | Reused schema | The platform problem document with the `messageId` extension (BR6) |
| IdempotencyRule | Document | The `Idempotency-Key` header, the repeated-key answer and its counting (BR5) |
| HandOverShapes | Document | The case-state announcement and the task raise, with the placeholder on the two absent operation names (BR8) |
| ConsumedShapes | Document | The document index, the checklist and the case facts, described and never provided (BR8) |
| Fake set and fixtures | Test asset | The success, refusal, conflict, unavailable and repeated-key answers used by every consuming build (AC7) |
| DriftTest | Test asset | The comparison of a consuming build against sections 11 to 13 (AC7, AC8) |

**Database.** The template creates `legal_action` in `rwb_litigation` only, with the physical types of TSD S4 T3.1 and the standard columns of T3.0. `case_id` and `law_firm_id` are identifiers with no foreign key, and no other schema is named in the template. The template is applied by the service's own Flyway sequence and never edits an applied migration (DP-15). The index set is carried as a gap and the primary key on `id` is the only index declared.

**Configuration and reference data.** The list codes are named and their members are read as values in force with their version (BR3). The capability area and the rights are declared per operation and their role lists are rwb-access data. The problem envelope, its member names and its `messageId` extension are the platform style guide's and are reused, not redeclared.

**Build steps**

1. Write the document with the base and the three operations; lint the paths and the rights (AC1).
2. Write the three schemas with the element mapping, the required set, the enumeration rule and an example; validate the example (AC2).
3. Write the `legal_action` DDL template and apply it twice in two throwaway schemas; assert the columns, the keys, the widths and the absence of a cross-schema key and of a pack table (AC4).
4. Write the error section with the problem envelope and one message ID per condition, and the `Idempotency-Key` rule of the two write operations (AC3).
5. Write the pack sub-shape and the two hand-over shapes with their placeholders (AC2, AC5).
6. Write the three consumed shapes and the naming and boundary section, with the absence tests for the old base, the second topic and another service's table (AC6, AC8).
7. Generate the fake set and the drift test, and wire the drift test into the build of `RWB-S4-E5004-APP` and the sibling S4 stories (AC7).
8. Publish v1 and record the pinned version of this contract and of each consuming story (AC8).

**Feature flag.** `rwb.litigation.legal-action-contract`.

**Done when.** The document lints, the three schemas validate, the template applies twice, the fakes answer every status including the conflict and the repeated key, the drift test is green on the build of this story and of `RWB-S4-E5004-APP`, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Published as | Message |
|---|---|---|---|
| MSG-GEN-001 | A required property is missing, or a value is outside its list (X4) | 422, problem body with `messageId` MSG-GEN-001 and `field` | Enter {field}. |
| MSG-P4-002 | The caller's role does not hold the right of the operation | 403, problem body with `messageId` MSG-P4-002 | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written by the consuming story | 503 on the create, problem body with `messageId` MSG-P7-003 | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-S4-001 | Carried from the legacy message set of this key: a pack item is missing at filing | 409, problem body with `messageId` MSG-S4-001 and the item named | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | The claim expiry of the case falls inside the filing window, on the consuming story's screen | Not raised here: a warning, not an error | The claim on this case expires on {date}. File before then. |
| MSG-P1-001 | A consumed data product is stale after a late or failed ACE batch, on the consuming story's screen | Not raised here: a warning with the product and its date | {product} is from {date}. Today's ACE batch has not arrived. |

The six texts are the legacy wording of RWB-E5-004 plus the FSD S4 validation message of the same feature, and are copied unchanged; no message is reworded and no identifier is added. The 400, 401, 404 and 409 carry the platform problem document and no business message outside this set, and the 400 code is not named by any S4 T-A row (GAP-2757; ASM-4587). The 409's second cause — a state fact refused from another state — carries the case owner's message and is not reworded here.

### 15. Screens and states

No screen is built in this story. The contract serves two surfaces read through the gateway-bff composite route (DP-19), and it fixes the answer fields they read and nothing of their layout:

| Screen | State | What the contract serves |
|---|---|---|
| SCR-18 Notice approval | Generated | The legal action and the pack sub-shape next to the notice state |
| SCR-18 Notice approval | Approved, sent, delivered | The same legal action, read only |
| SCR-18 Notice approval | Unserved | The legal action as the notice story reads it |
| SCR-18 Notice approval | Empty | Not specified in the source documents (CG-ALL-9091) |
| SCR-18 Notice approval | Loading | Not specified in the source documents (CG-ALL-9091) |
| SCR-18 Notice approval | Error | Not specified in the source documents (CG-ALL-9091) |
| SCR-18 Notice approval | No access | Not specified in the source documents (CG-ALL-9091) |
| SCR-19 Litigation workspace | Pack | The legal action in status `OPEN` with the pack sub-shape and the case-state fact |
| SCR-19 Litigation workspace | Verified | The legal action with the pack sub-shape as the case of record holds `PACK_VERIFIED` |
| SCR-19 Litigation workspace | Instructed, filed, hearing, judgment | The legal action with `filedDate`, the court references, `litStatus`, `judgmentDate` and `judgmentAmount` |
| SCR-19 Litigation workspace | Refused or held | The 403 with MSG-P4-002, the 409 with MSG-S4-001, and the `NOTICE_BLOCKED` state fact |
| SCR-19 Litigation workspace | Empty | Not specified in the source documents (CG-ALL-9092) |
| SCR-19 Litigation workspace | Loading | Not specified in the source documents (CG-ALL-9092) |
| SCR-19 Litigation workspace | Error | Not specified in the source documents (CG-ALL-9092) |
| SCR-19 Litigation workspace | No access | Not specified in the source documents (CG-ALL-9092) |

The five SCR-18 states and the five SCR-19 states are the ones the legacy screen block of RWB-E5-004 gives, copied unchanged; the empty, loading, error and no access states of both screens are Not specified in the source documents (CG-ALL-9091, CG-ALL-9092). The route path, the screen-model field list and the merge order belong to `RWB-PLT-N001-CON`; the transition behind each state is the app story's, and the case state is rwb-case's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-004-01 | AC1, AC2 | Contract | The contract half of the assembly: the create in status `OPEN`, the read with the pack sub-shape, the patch with the court references, and `CIVIL_CASE` as a value of `actionType` |
| TC-E5-004-02 | AC1, AC5 | Contract | The contract half of R-LIT-04: the `NOTICE_BLOCKED` state fact, the rule ID and version, and the accepted or refused answer |
| TC-E5-004-03 | AC3, AC5 | Contract | The contract half of the not-recorded case: the library element, the 503 with MSG-P7-003 and the refused chain of the stub; the `PACK_VERIFIED` state fact |
| TC-E5-004-04 | AC3 | Contract | The contract half of the access case: Litigation C, R and U declared per operation, and the 403 with MSG-P4-002 |
| TC-E5-004-05 | AC5 | Contract | The four pack states named as case facts and refused as a value of `status`; the six members of LOV-LEGAL-STATUS and no seventh |
| TC-E5-004-06 | AC6 | Contract | The consumed document-index and case-facts shapes, the task raise with its placeholder, and the absence of a pack table |
| TC-S4-E5004-CON-01 | AC1, AC2, AC8 | Contract | The document linted: the base, the three operation IDs, the LegalAction elements, the pack sub-shape, the absence of the old base, of a second topic, of a pack resource and of another service's table |
| TC-S4-E5004-CON-02 | AC3 | Contract | One problem body per status on each operation, the six statuses of the TSD rows, the 400 carried as a gap, the rights per operation and the `Idempotency-Key` required on the two writes and refused absent |
| TC-S4-E5004-CON-03 | AC4 | Component | The template applied in two throwaway schemas; DF-LEG-001 to DF-LEG-014, the standard columns, the types, the widths, the primary key and the absence of a cross-schema key and of a pack table asserted |
| TC-S4-E5004-CON-04 | AC5, AC6, AC7 | Contract | The five hand-over and consumed shapes with their placeholders, the eight fakes against the document, and a drifted fake failing the build |
| TC-S4-E5004-CON-05 | AC4, AC6 | Component | Boundary of the section 12.7 tables: legal_action, decision_record and idempotency_key in rwb_litigation only; no table of another service declared, read or keyed; no pack table |

The six legacy identifiers of RWB-E5-004 are carried in their legacy order as the **contract half** of each case: they assert the shape each surface needs and not the business outcome, which `RWB-S4-E5004-APP` proves with the fakes. The four `TC-S4-E5004-CON-*` identifiers are new tests of the artefact. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the pack item list, the checklist, the template status, the task code, the service levels and the index set stay data or reference data, and no role code, list value or state member is written in code.
- No personal data in a schema, an example or a fake: identifiers, document references, list values, dates and amounts only.
- The contract names only `rwb_litigation` tables and only operations owned by rwb-litigation; the document index, the case facts, the state announcement and the task raise are consumed or handed over, never provided (DP-01, DP-08).
- One base, one topic and one queue per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- No pack resource, no pack table and no seventh status value; the pack states are case facts of rwb-case (BR4).
- No event, no workflow, no Schedule and no outbox row is declared by this document; the decision record is the library's element (12.3, 12.5, 12.6).
- No ACE view and no ACE table is declared or read (DP-05).
- An absent value is written as the placeholder with its gap and assumption pair and never guessed: the index set, the case-state operation name and the task operation name.
- Every example in the document is synthetic; no production payload and no production file is copied into a schema or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Contract element | Test cases |
|---|---|---|---|---|---|
| No requirement ID in the legacy master (GAP-2752; ASM-4582) | The pack is built from the document index and the case facts, ready for the officer to verify | FEAT-LIT-04 | 08 Litigate and enforce | The three operations, the pack sub-shape and the five shapes | TC-E5-004-01 to TC-E5-004-06, TC-S4-E5004-CON-01 to TC-S4-E5004-CON-04 |
| FEAT-LIT-04 | Assemble the litigation pack | FEAT-LIT-04 | 08 Litigate and enforce | The pack sub-shape and the `legal_action` template | TC-S4-E5004-CON-01, TC-S4-E5004-CON-03 |
| FEAT-DCM-02 | Index documents by case, type, date and extracted fields | FEAT-LIT-04 | 08 Litigate and enforce | The consumed shapes of API-P5-002 and API-P5-008 | TC-E5-004-06, TC-S4-E5004-CON-04 |
| R-LIT-04 | A withdrawn template moves the case to `NOTICE_BLOCKED` | FEAT-LIT-04 | 08 Litigate and enforce | The case-state announcement shape and the task raise shape | TC-E5-004-02, TC-S4-E5004-CON-04 |
| R-LIT-16 | A complete pack moves the case to `PACK_VERIFIED` | FEAT-LIT-04 | 08 Litigate and enforce | The case-state announcement shape and the pack sub-shape | TC-E5-004-03, TC-S4-E5004-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-004, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 of the legacy story, owned by RWB-S4-E5004-APP; this baseline copies none of them |
| Legacy test cases | TC-E5-004-01 to TC-E5-004-06, carried here as the contract half of each surface |
| Requirement | The legacy master and the Epics 3 to 8 specification carry no REQ identifier for this feature, so both stories trace to FEAT-LIT-04 until the Epics 3 to 8 PRD adds the identifiers (GAP-2752) |
| Screens | SCR-18 Notice approval and SCR-19 Litigation workspace, read through the gateway-bff composite route (DP-19) |
| Sibling slice | RWB-S4-E5004-APP: the composition, the two evaluations, the decision record, the task raise and the state announcement |
| Sibling stories of the service | `RWB-S4-E5005-APP` (defect list), `RWB-S4-E5006-APP` (lost document), `RWB-S4-E5007-APP` (verify and approve filing), `RWB-S4-E5011-APP` (hearings) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership), ADR-022 (local decision record plus central ledger) |

### 19. Out of scope

- The implementation behind the contract — the composer, the readers, the rule evaluations, the workflow, the activities, the row write and the two calls: `RWB-S4-E5004-APP`.
- The case-state machine, which event moves the case and what a rejected pack leaves behind: `RWB-S4-E5004-APP` section 9 and rwb-case (P3).
- The document index, the checklist and the documents themselves: rwb-document (P5).
- The case, its stage, its states, its tasks and its timers: rwb-case (P3).
- The demand notice, its dispatch, its delivery and its template: rwb-comms (P6) and the notice stories of this service.
- The check of the pack against the defect list and the recovery of a lost document: `RWB-S4-E5005-APP` and `RWB-S4-E5006-APP`.
- The verification of the pack and the approval of the filing: `RWB-S4-E5007-APP`; the panel and the instruction: `RWB-S4-E5008-APP` and `RWB-S4-E5009-APP`.
- The hearings of the legal action (API-S4-005, `hearing` DF-LEG-024 to DF-LEG-029): `RWB-S4-E5011-APP`.
- The decision-record library itself and its chain: `RWB-PLT-E1027-CON`; the central ledger and the rule packages: rwb-decision (P7).
- The roles, rights, scope and masking data themselves: rwb-access (P4).
- The gateway-bff composite route, the screen field list and the layout of SCR-18 and SCR-19: `RWB-PLT-N001-CON` and the edge stories.
- The deployment of this build, the chart values, the schema, the login and the flag: its own OPS story.
- The cross-service proof of the document against the live owners: the wave 3 integration harness.
