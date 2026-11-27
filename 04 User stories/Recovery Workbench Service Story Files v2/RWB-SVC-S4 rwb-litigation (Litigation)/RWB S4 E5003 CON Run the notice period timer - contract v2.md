# RWB-S4-E5003-CON Run the notice period timer - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5003-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-003 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S4-E5003-CON-16) |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-S4-E5003-CON-14) |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | 1 (major version from base path /api/recovery/litigation/v1) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E5-003 for rwb-litigation (S4). The notice and its period are published on Day 1 on base `/api/recovery/litigation/v1` with API-S4-001, API-S4-002 and API-S4-003, the notice sub-shape of the legal action, the timer element of the workflow signal, the `legal_action` DDL template, the decision-record element, the four consumed answer shapes and the fakes. The four legacy acceptance criteria stay with `RWB-S4-E5003-APP` and every criterion here is new. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S4-E5003-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (12 resolved, 10 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **contract owner of rwb-litigation (S4)**, I want **the published contract as it carries a statutory notice and its period — the base `/api/recovery/litigation/v1` with API-S4-001 approve, API-S4-002 create and API-S4-003 read, the notice sub-shape of `LegalAction` with `actionType = NOTICE`, the `noticeDeliveryResult` signal and its timer element, the `legal_action` DDL template with DF-LEG-001 to DF-LEG-014, the `Idempotency-Key` rule, the error envelope, the declared right of each operation, the decision-record element, the notice, proof, case and approval answer shapes, the fakes and the drift test** instead of the monolith's in-process controller, its one `recovery.legal_action` table and its `timer` row, so that **RWB-S4-E5003-APP and the notice stories of the service build against one frozen, testable shape from Day 1, and a notice state, a period date, a list value or an error status can never drift between rwb-litigation, rwb-comms, rwb-document, rwb-case and rwb-decision without a failing build**.

This story owns the contract and nothing else:

- the OpenAPI 3.1 document of the legal action resource as the notice uses it: the base, the three operations, the request and answer schemas, the problem schema, the security and the error set;
- the notice sub-shape: `actionType = NOTICE` of LOV-LEGAL-TYPE, the required set of a notice action and its optional court and firm references;
- the `noticeDeliveryResult` signal element and its timer element — `started_at`, `expires_at`, the period length reference and the rule ID and version — which are workflow elements and not columns;
- the `legal_action` DDL template with the columns and types of TSD S4 T3.1 and the standard columns of T3.0, applied in this service's own schema, with no cross-schema key;
- the element naming rule (camelCase after the DF-LEG field identifiers), the required set and the enumeration rule that names a list code and no member;
- the `Idempotency-Key` rule on the two write operations, the compatibility rule and the pinning rule;
- the shapes this service hands to rwb-comms, rwb-document, rwb-case and rwb-decision, and the shapes of the answers it reads back;
- the fake set generated from the document, and the drift test every consuming build runs.

It does not run any period. The three rule evaluations, the proof attach, the timer of the stage, the row write, the route announcements and the decision records are `RWB-S4-E5003-APP`'s; the notice and its served result are rwb-comms's; the case state is rwb-case's; and the approval is rwb-decision's. The document declares shapes and moves nothing.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020), and the litigation service has one base and one document for its legal actions. The legacy key RWB-E5-003 moved a case through a period that started on a WIN delivery result and ended on a rule, with the notice, the proof, the timer row, the case status and the decision log entry all in reach of one transaction. Four of those are now other services' records and every one of them is reached on a published shape, so each shape has to be fixed before the app story starts: the three operations and their bodies, the value of `actionType` that makes a legal action a notice action, the columns a notice action writes, the delivery result the workflow is signalled with, the period element, the decision record the service writes in its own transaction, and the four answers it hands over.

The notice period is not a resource. TSD S4 gives one `legal_action` table with a six-value action list of which `NOTICE` is one, and one six-value status list; the notice is a legal action of that type, so a second resource, a second table or a separate period table would fork the vocabulary and would put a clock in a schema. The period is therefore published as an element of the workflow signal and of the read answer, and the row keeps only what the TSD defines — which is why no new column is invented here and why the index set of `legal_action` has to be carried as a gap (GAP-2750; ASM-4579).

The baseline also fixes the naming the checks require: schema `rwb_litigation`, login `rwb_litigation`, base `/api/recovery/litigation/v1`, topic `rwb.litigation.events.v1` with retry and `.dlt` topics, event names `rwb.litigation.<Event>.v1`, task queue `rwb-litigation` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.litigation`. It keeps the operation IDs the TSD allocates — API-S4-001 approve, API-S4-002 create and API-S4-003 read — of which the legacy endpoint block of RWB-E5-003 names the first two.

Two contested points are carried as gaps rather than decided quietly. The FSD S4 A2.2 says the proof of delivery is written "onto the notice" while the Ownership Map gives S4 no `notice` table and Architecture v5 gives notices to rwb-comms, so the notice row and its served result are another owner's and this document declares only the shape of the announcement (GAP-2750; ASM-4573). And the four operations this service calls — the notice read, the proof attach, the case route fact and the approval route — are named by no source read for this key, so their shapes carry the placeholder (GAP-2750; ASM-4577).

It serves FEAT-LIT-03 "Run the notice period timer" through the shapes it publishes, and it traces to that feature until the Epics 3 to 8 PRD adds requirement identifiers, because the legacy master and the Epics 3 to 8 specification carry none for this key (GAP-2750; ASM-4580).

### 3. Preconditions

- The service template and the naming library are available (`RWB-PLT-TPL`, `RWB-PLT-E1047-CON`), so the base, the topic, the event names and the package follow the platform rule and not a local choice.
- The platform error envelope and its `messageId` extension are the platform baseline; where this document narrows them it does so explicitly. The envelope, its member names and its extension are reused and never redeclared.
- The reference lists of the legal action are the data of rwb-case and are read with their version: LOV-LEGAL-TYPE (`NOTICE`, `CIVIL_CASE`, `APPEAL`, `ENFORCEMENT`, `BANKRUPTCY_PETITION`, `LED_AUCTION`) and LOV-LEGAL-STATUS (`OPEN`, `FILED`, `JUDGMENT`, `ENFORCING`, `CLOSED`, `WITHDRAWN`) of TSD S4 T3.2. The document names the list codes and their members as the TSD enumerates them, and the version in force is read at run time.
- The `legal_action` row and its columns are the TSD S4 T3.1 row, DF-LEG-001 to DF-LEG-014, plus the seven standard columns of T3.0. No field outside that row is declared, because no source gives one for a notice action.
- The decision record is the local decision-record library's, `RWB-PLT-E1027-CON`, and its shape is not fixed here: this document names the element it needs and points to the library.
- The notice, proof, case and approval contracts are the documents this baseline reads for the shapes it hands over; their operation names are absent (GAP-2750; ASM-4577).
- No build dependency: this story is Day 1 by rule (Template and Rules section R5.7 rule 1), and every consuming story of the service builds against it and its fake.

### 4. Flow

1. Draft the OpenAPI 3.1 document of the legal action resource on base `/api/recovery/litigation/v1`: API-S4-001, API-S4-002 and API-S4-003 with their request and answer bodies, their rights and their error sets.
2. Fix the `LegalAction` element set from DF-LEG-001 to DF-LEG-014 in camelCase, with the required set of TSD S4 T3.1 and the two list references of T3.2.
3. Fix the notice sub-shape: `actionType = NOTICE` required on the create, `courtName` and `lawFirmId` optional, and no period element on the row.
4. Write the `noticeDeliveryResult` signal element with `noticeRef`, `caseRef`, `servedResult`, `deliveredAt`, `proofRef` and the timer element `startedAt`, `expiresAt`, `periodLengthRef`, `ruleId` and `ruleVersion`; carry the read answer's period element from the same definition.
5. Write the `legal_action` DDL template with the columns, the physical types, the widths, the keys and the standard columns; carry the index set as a gap.
6. Write the decision-record element and the four answer shapes this service hands over: the notice read and the unserved announcement, the proof attach, the case route fact and the approval route.
7. Write the `Idempotency-Key` rule on the two write operations, the versioning rule, the compatibility rule and the pinning rule.
8. Generate the fake set from the document and wire the drift test into the build of this story and of `RWB-S4-E5003-APP`.
9. Publish v1 and record the pinned version of each consuming story.
10. Hand the baseline to `RWB-S4-E5003-APP`, to the notice stories of the service and to the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | None | AC1 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC7 |
| X3 | A fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A value of `actionType` outside LOV-LEGAL-TYPE, or a `servedResult` outside its reference set, is sent | The document refuses it as an enumeration error at 422 and nothing is written | MSG-GEN-001 | AC2 |
| X5 | The operation is called without the `Idempotency-Key` header | The document refuses the request at 400 and the fake answers the same; no stored answer exists | None | AC3 |
| X6 | The document declares an operation of another service or a second base | The review fails the baseline; a consumed shape is described as consumed, never as provided | None | AC7 |
| X7 | The index set of `legal_action` is guessed, or a period column is added to the row | The review fails the baseline: the template declares the primary key only and the period stays an element of the signal | None | AC4 |
| X8 | A retired element reappears in the document | The absence test fails: no old monolith base, no second topic, no timer table and no table of another schema | None | AC7 |
| X9 | The period element is published as a column or as a Schedule | The review fails the baseline; the element belongs to the workflow signal and to the read answer (ASM-4578) | None | AC4, AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the TSD S4, the naming rules and the platform envelopes only, and consumes no service |
| Negotiable | The index set, the four absent operation names, the period element and the notice-ownership conflict are settled with their owners; the base, the operation IDs, the columns and the list codes are fixed by the target architecture |
| Valuable | Unblocks the app story on Day 1 and the notice, proof and pack stories that read the same resource |
| Estimable | One OpenAPI document, one signal definition, one DDL template, four consumed shapes, one fake set and eight contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the legal action that carries a statutory notice and its period

  Background:
    Given the service naming rule of the platform library is in force
    Given the legal action of rwb-litigation is served on the base /api/recovery/litigation/v1
    Given the reference lists are LOV-LEGAL-TYPE and LOV-LEGAL-STATUS of TSD S4 T3.2, read with their version in force

  Scenario: AC1 The three operations are declared with the notice sub-shape and the action type (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-litigation is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /notices/{noticeId}/approve as API-S4-001, POST /cases/{caseId}/legal-actions as API-S4-002 and GET /legal-actions/{legalActionId} as API-S4-003, all under the base /api/recovery/litigation/v1 and owned by rwb-litigation
    Then the LegalAction schema carries id, caseId, lawFirmId, actionType, lawsuitNo, blackCaseNo, redCaseNo, courtName, claimAmount, filedDate, judgmentDate, judgmentAmount, litStatus and status
    Then actionType names LOV-LEGAL-TYPE and NOTICE is one of its values, and status names LOV-LEGAL-STATUS with its six values
    Then the document declares no second base, no second resource and no operation of another service
    Then every legacy operation ID of TSD S4 T-A.1 is kept and no operation is renumbered

  Scenario: AC2 The notice create, its answer and the read answer are fixed as shapes (new, D-RCV-60)
    Given the LegalActionRequest and LegalAction schemas of the document
    When the notice sub-shape is reviewed
    Then LegalActionRequest requires actionType with the value NOTICE, and carries caseId from the path, courtName and lawFirmId as optional properties
    Then the create answers 201 with LegalAction in status OPEN, and the answer carries the identifiers, the court fields and the status of the row it wrote
    Then the read answer carries the period element startedAt, expiresAt, periodLengthRef, ruleId and ruleVersion as workflow facts and not as columns of the row
    Then no element of the request or the answer names a table, a column or a value outside TSD S4 T3.1 and T3.2, and no separate notice resource and no period resource is declared
    Then a value of actionType outside LOV-LEGAL-TYPE or a servedResult outside its reference set is refused at 422 with MSG-GEN-001 naming the property
    Then the notice record, its served result and its template are declared as consumed shapes of rwb-comms and never as data of this service (GAP-2750; ASM-4573)

  Scenario: AC3 The Idempotency-Key rule, the error envelope and the declared right of each operation are fixed (new, D-RCV-60)
    Given the operation table of the document
    When it is reviewed against TSD S4 T-A.1 and T-A.2 and the legacy permission block of RWB-E5-003
    Then API-S4-001 and API-S4-002 declare the Idempotency-Key header and a stored answer, and API-S4-003 declares no Idempotency-Key
    Then the error responses are 401, 403, 404, 409, 422 and 503 as the TSD rows give them, each with the platform problem document and one message ID per condition
    Then a body that cannot be parsed answers 400 with the same envelope, and the 400 code is not named by any S4 T-A row (GAP-2750; ASM-4580)
    Then the declared rights are Litigation A on the approval, Litigation C on the create and Litigation R on the read, with the scope applied and the role lists held by rwb-access
    Then a caller without the right is refused at 403 with MSG-P4-002 and changes nothing
    Then the document declares no right of its own invention and no role code as a constant

  Scenario: AC4 The legal_action columns are declared and no period column is added (new, D-RCV-60)
    Given the legal_action DDL template of schema rwb_litigation
    When it is compared with TSD S4 T3.1 and T3.0
    Then the template declares DF-LEG-001 to DF-LEG-014 with their physical types, widths and required flags, and the seven standard columns
    Then case_id and law_firm_id are identifiers with no foreign key across schemas
    Then status is varchar(15) against LOV-LEGAL-STATUS and action_type is varchar(20) against LOV-LEGAL-TYPE, both closed by the list and not by a check constraint of their members
    Then the template declares no timer table, no notice table, no period column and no delivered_at column, because the period is an element of the signal and the notice is rwb-comms's
    Then the index set beyond the primary key on id is Not specified in the source documents (GAP-2750; ASM-4579) and the template declares the primary key only
    Then the template is applied by the service's own Flyway sequence and never edits an applied migration (DP-15)

  Scenario: AC5 The delivery signal, its timer element and the decision-record element are fixed (new, D-RCV-60)
    Given the noticeDeliveryResult signal definition and the decision element of the document
    When they are compared with R-LIT-07, R-LIT-08 and DP-03
    Then the signal carries noticeRef, caseRef, servedResult, deliveredAt, proofRef and the idempotency key of the delivery, and it declares no personal field
    Then the timer element carries startedAt, expiresAt, periodLengthRef, ruleId and ruleVersion, and it is a workflow element with no column behind it
    Then the period length is declared as a reference to a versioned reference row and no value is fixed in the document
    Then the decision record is declared as the local library's element on rwb.decision-record.v1 with the decision code, the rule ID, the rule version, the inputs reference, the final call, the decided time and the two hashes, and none of the library's own fields is fixed here
    Then the document declares no Schedule, no Quartz job and no durable-timer name of the implementation, and no timer table (GAP-2750; ASM-4578)

  Scenario: AC6 The four hand-over shapes and the fakes answer the document (new, D-RCV-60)
    Given the notice read and unserved announcement, the proof attach, the case route fact and the approval route shapes of the document
    When each is compared with its owner's document and with the fake that serves it
    Then the notice shape carries the notice reference, its type, its sent date, its served result and its proof reference, and the announcement carries the not-served result with the rule ID and version
    Then the proof attach carries the notice reference, the proof reference and the idempotency key, and answers the attached proof reference or a refusal
    Then the case route fact carries WITH_CUSTOMER_NOTICE_PERIOD, NOTICE_UNSERVED or PACK_ASSEMBLY with the rule ID and version, and the answer carries the accepted or refused outcome and the case state
    Then the approval route carries the case reference, the legal action reference, the decision code, the capability area, the product group, the notice reference and the Idempotency-Key
    Then the operation name of each of the four is Not specified in the source documents (GAP-2750; ASM-4578)
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The versioning rule, the naming baseline and the boundary of the document are fixed (new, D-RCV-60)
    Given the versioning and boundary section of the document
    When it is reviewed against the Template and Rules and the Ownership Map
    Then the base is /api/recovery/litigation/v1, the schema and the login are rwb_litigation, the topic is rwb.litigation.events.v1 with retry and .dlt topics, the event names are rwb.litigation.<Event>.v1, the task queue is rwb-litigation in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.litigation
    Then the document declares no event of its own: it publishes none and consumes none, and the delivery result is declared as a signal (GAP-2750; ASM-4578)
    Then the document declares no read of another service's table, no cross-schema join and no v_ace_ view, and it names recovery_case, timer, notice, document, decision_log_entry and rule_row as other owners' consumed shapes only
    Then the old monolith base appears nowhere in the document, its examples or its fakes
    Then the document names no second topic, no second queue, no batch table and no Schedule
    Then a breaking change is a new major version and an additive change stays within major version 1

  Scenario: AC8 Each rule BR1 to BR13 of section 8 is asserted against the document (new, D-RCV-60)
    Given the business rules of section 8
    When the document is reviewed against each rule
    Then each rule is met by the document and its check is named in TC-S4-E5003-CON-06
    Then the base, the operation IDs, the list codes, the Idempotency-Key rule, the error envelope, the compatibility rule, the consumed operations and the personal-data check are each asserted against the document
```

These eight criteria are new for the contract baseline and test the artefact only; they restate no business outcome of `RWB-S4-E5003-APP` and they copy no criterion of the legacy story. The wave 3 harness that consumes this baseline copies none of them.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/litigation/v1`; the document never declares another service's path as provided | DP-13; Architecture v5 slide 41 notes |
| BR2 | The three operations keep their TSD operation IDs API-S4-001, API-S4-002 and API-S4-003, and no fourth operation of this resource is declared | TSD S4 T-A.1; legacy Endpoints block of RWB-E5-003 |
| BR3 | `action_type` and `status` are declared as enumerations of LOV-LEGAL-TYPE and LOV-LEGAL-STATUS and the code names the list, never a member list curated locally | TSD S4 T3.2; FSD S4 A2.3.3.1 (BR-S4-003) |
| BR4 | A read declares no `Idempotency-Key`; a write declares it and stores its answer | Architecture v5 slide 11; TSD S4 T-A.1 |
| BR5 | Error responses use one envelope and one message ID per condition; the business message texts are copied unchanged from the legacy story | Architecture v5 platform baseline; Template and Rules section R7.2 (s14) |
| BR6 | A schema change is additive within a major version; a breaking change is a new major version, and the holding of a written table is a breaking change | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR7 | The document lists only operations owned by rwb-litigation; a consumed operation or shape is described as consumed, never as provided | Ownership Map v1 |
| BR8 | The period and its dates are elements of the workflow signal and of the read answer, never columns of `legal_action` and never a Schedule | TSD S4 T3.1 (no period column); R-LIT-07 timing column; ASM-4578 |
| BR9 | The notice record, its served result and its template are rwb-comms's; the document declares the approve operation it owns and the announcement shape, never a notice table | Architecture v5 slide 10 ("Notices rwb-comms"); Ownership Map (S4 owns `hearing` and `legal_action`) |
| BR10 | No business value is fixed in the contract: the list members, the period length, the proof window, the warning window and the approver route stay data or reference data | TSD S4 T3.2; Template and Rules section R7.2 (s17) |
| BR11 | The decision record is the local library's element on the shared topic, never a new event of this service, and its fields are the library's | DP-03; Architecture v5 slide 42 (event 08) |
| BR12 | No personal data in a schema, an example or a fake: identifiers, list values, dates, court references and amounts only | TSD S4 T3.1; Architecture v5 slides 42 and 43 notes |
| BR13 | No ACE view and no ACE table is declared or read by this document; the WIN delivery facts arrive through rwb-comms, never from `v_ace_pod` here | DP-05; Architecture v5 slide 29 |

### 9. State transitions

The document's own lifecycle is the only state this story moves:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The three operations, the notice shape, the signal, the template and the four hand-over shapes are described | In review |
| In review | Consumer sign-off | `RWB-S4-E5003-APP` and the notice stories accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1, for example a court reference on the notice | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, a column of the template changes, a period element moves to a column, or a list code changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |

Two vocabularies are declared and neither is moved here:

| Object | Values | Note |
|---|---|---|
| legal_action.action_type | `NOTICE`, `CIVIL_CASE`, `APPEAL`, `ENFORCEMENT`, `BANKRUPTCY_PETITION`, `LED_AUCTION` (LOV-LEGAL-TYPE) | Declared as the list reference; the notice is the value `NOTICE` |
| legal_action.status | `OPEN`, `FILED`, `JUDGMENT`, `ENFORCING`, `CLOSED`, `WITHDRAWN` (LOV-LEGAL-STATUS) | Declared as the list reference; the moves between the values are the app story's |

The notice-period state — running, fired, stopped, never started — is declared as the timer element and as the case state the app story announces, and no value of LOV-LEGAL-STATUS names it. Which event moves the period, and what an unserved notice leaves on the row, belong to `RWB-S4-E5003-APP` and appear nowhere in this document (ASM-4578).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-litigation | Owns the OpenAPI document, the signal definition, the DDL template and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes |
| Consuming teams (`RWB-S4-E5003-APP`, the notice stories of the service, and the rwb-comms, rwb-document, rwb-case and rwb-decision owners whose answer shapes are declared) | Review and sign off the parts they consume |
| Platform library owner | Owns the problem envelope, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an element, an example or a fake |
| Business analyst of S4 | Confirms that LOV-LEGAL-TYPE and LOV-LEGAL-STATUS are named as list codes and that no member list, period length or window value is curated locally |

The login behind the document's security scheme is `rwb_litigation` by the naming rule of DP-02; the document names the scheme and not a credential, and no role, level or mask is defined here.

Each of the three operations is authorised through the rwb-access authorise check (DP-08) before its body runs; the check names no role, level or mask here.

### 11. Data

The contract baseline declares shapes, not business values.

| BR Field ID | Element | Type and width | Required | List |
|---|---|---|---|---|
| DF-LEG-001 | id | uuid | Yes | None |
| DF-LEG-002 | caseId | uuid | Yes | None |
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

The six rows below name elements and not fields, so they carry no BR Field ID; their BR Field ID is `Not specified in the source documents (DOR-RWB-S4-E5003-CON-7)`.

| Item | Content |
|---|---|
| Notice sub-shape | `actionType = NOTICE` required on the create; `courtName` and `lawFirmId` optional; no period element, no `delivered_at`, no served result and no notice column on the row, and no separate notice resource: the row is found by `caseId` and action type, and the notice reference stays with rwb-comms (ASM-4573) |
| Delivery signal | `noticeRef`, `caseRef`, `servedResult`, `deliveredAt`, `proofRef` and the idempotency key; `servedResult` names a reference set at its version and no member is curated here |
| Timer element | `startedAt`, `expiresAt`, `periodLengthRef`, `ruleId`, `ruleVersion`; a workflow element of the signal and of the read answer, with no column behind it (BR8) |
| Period home | The period starts at `delivered_at` and its length is a versioned reference row by product group and notice type, whose value waits for the business; the period is a durable timer of the LitigationWorkflow stage on queue rwb-litigation; the timer ledger is rwb-case's, so no timer table exists in rwb_litigation |
| Index set | Beyond the primary key on `id` the set is `Not specified in the source documents (GAP-2750; ASM-4579)`; the template declares the primary key only |
| Decision record | The element the library writes: the decision code, the rule ID and version, the inputs reference, the final call, the decided time and the two hashes. The library owns the fields and the chain (DP-03) |
| Four hand-over shapes | The notice read and the unserved announcement, the proof attach, the case route fact and the approval route; their operation names are `Not specified in the source documents (GAP-2750; ASM-4578)` |
| Reference data | The lists LOV-LEGAL-TYPE and LOV-LEGAL-STATUS and the period length reference are read through the reference-data contract (DP-06) and the parameter contract (DP-07); no parameter key is named here |

**No new table, no new column and no migration.** `legal_action` is the TSD S4 T3.1 row and this document publishes its DDL template for the service's own Flyway sequence (DP-15); `decision_record` and `idempotency_key` are platform library objects created in `rwb_litigation` by the library's migration and are named here, not declared. `recovery_case` and `timer` (P3), `notice` (P6), `document` (P5), `decision_log_entry` and `rule_row` (P7) and every `v_ace_*` view (P1) are other owners' and are named as consumed shapes only. `legal_action.case_id`, `law_firm_id` and the notice, proof and approval references are values, not foreign keys across schemas (DP-01).

**No personal data.** No element of this contract carries a name, an address, an identity number or an account number. The court references, the amounts and the dates are not personal data, and the borrower and the guarantor are reached by the services that need them through rwb-source-data and never through this resource.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13). This story publishes all three operations.

| ID | Method | Path | Request | Response | Access | Idempotency | Errors |
|---|---|---|---|---|---|---|---|
| API-S4-001 | POST | `/notices/{noticeId}/approve` | None; `noticeId` from the path | 200 with the notice answer, carrying the approval state and the notice reference | Litigation A, scope applied | `Idempotency-Key` required, answer stored | 401, 403, 404, 409, 503 |
| API-S4-002 | POST | `/cases/{caseId}/legal-actions` | `LegalActionRequest`; `caseId` from the path; `actionType = NOTICE` | 201 with `LegalAction` in status `OPEN` | Litigation C, scope applied | `Idempotency-Key` required, answer stored | 401, 403, 404, 409, 422, 503 |
| API-S4-003 | GET | `/legal-actions/{legalActionId}` | None | 200 with `LegalAction` and its period element | Litigation R, scope applied | Not applicable | 401, 403, 404, 503 |

The purpose, response entities, rights, idempotency and error statuses are those of TSD S4 T-A.1 and T-A.2 for API-S4-001, API-S4-002 and API-S4-003, with the base renamed by DP-13. The hearing operation API-S4-005 and the legal-action patch API-S4-004 are not declared here, because they belong to the hearing, filing and enforcement stories of this service; the create of a notice action is the one write this key needs.

#### 12.2 REST operations consumed

None: a contract document calls no service. The four rows below are the shapes this service **hands over** and the answers it reads back; the document declares them, and the calls are `RWB-S4-E5003-APP`'s.

| Shape | Owner | Declared here | Open point |
|---|---|---|---|
| The notice read and the unserved announcement | P6 rwb-comms | The notice reference, its type, its sent date, its served result and its proof reference; the not-served result with the rule ID and version | The operation names and the field list of the answer are `Not specified in the source documents (GAP-2750; ASM-4577)`; the notice record is never provided here (BR9) |
| The proof attach | P5 rwb-document | The notice reference, the proof reference and the idempotency key; the attached proof reference or a refusal | The operation name is `Not specified in the source documents (GAP-2750; ASM-4577)` |
| The case route fact and its answer | P3 rwb-case | `WITH_CUSTOMER_NOTICE_PERIOD`, `NOTICE_UNSERVED` or `PACK_ASSEMBLY` with the rule ID and version; the accepted or refused answer with the case state | The operation name and the answer field list are `Not specified in the source documents (GAP-2750; ASM-4577)` |
| The approval route | P7 rwb-decision | The case reference, the legal action reference, the decision code, the capability area, the product group, the notice reference and the `Idempotency-Key` | The operation name is `Not specified in the source documents (GAP-2750; ASM-4577)` |

Every one of them is one hop with a 2 s timeout in the app story's implementation (ADR-020). No operation of another service is declared as provided here (BR7).

#### 12.3 Events published

None. `rwb.litigation.events.v1` is this service's topic and the Ownership Map gives S4 zero events, so this document publishes none of the catalogue's `LawsuitFiled`, `JudgmentRecorded` or `AuctionResult`, and no notice-period event exists: the period is a timer of the workflow and its result leaves on the case contract. The decision record is the local library's element of DP-03, which publishes `DecisionRecorded` (event 08) on the shared `rwb.decision-record.v1`; that element is the library's and this document declares no payload of its own.

#### 12.4 Events consumed

None. The delivery result is declared as the `noticeDeliveryResult` signal of the litigation stage and not as a subscription, so the document names no topic, no consumer and no inbox. Architecture v5 slide 19 shows `NoticeDelivered` among the inputs of rwb-litigation while the Ownership Map gives S4 no event: whether that event exists and who consumes it is left open by the sources and is carried with the app story's gap (GAP-2749; ASM-4575).

#### 12.5 Workflows and activities

None. The document defines no workflow and no activity. `LitigationWorkflow` is the app story's, on task queue `rwb-litigation` in namespace `rwb-recovery`; this baseline fixes the name of the signal element and the shape of the timer it carries, and names no activity, no workflow ID and no timer name of the implementation.

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job is declared. The notice period belongs to one case and one notice, not to a calendar, so it is a durable timer inside a workflow run and not a Schedule; the Quartz marker of FSD S4 A2.3.2 is not carried as a job and DP-10 adds no dependency row here.

#### 12.7 Tables owned

| Table | Schema | Owner | Note |
|---|---|---|---|
| legal_action | `rwb_litigation` | S4 | The DDL template of section 11: DF-LEG-001 to DF-LEG-014, the seven standard columns, the primary key on `id` and no cross-schema key (DP-01, DP-15) |
| decision_record | `rwb_litigation` | PLT library object applied in this schema | Named only: the shape is `RWB-PLT-E1027-CON`'s and the row is written in the caller's transaction (DP-03) |
| idempotency_key | `rwb_litigation` | PLT library object applied in this schema | Named only: the stored answer of the two write operations |

`hearing` is S4's and belongs to the hearing story; `recovery_case` and `timer` (P3), `notice` (P6), `document` (P5), `decision_log_entry` and `rule_row` (P7) are other owners' and appear only as consumed shapes. No timer table, no notice table and no period column is declared, read or keyed.

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Legal-action fake | The three operations of 12.1 | A 200 approval of the notice, a 201 create in status `OPEN` with `actionType NOTICE`, a 200 read with the period element, and the 400, 401, 403, 404, 409, 422 and 503 refusals |
| Repeated-key fake | The `Idempotency-Key` rule | The first answer returned again for the same key, with no second legal action and no second approval |
| Signal fake | The `noticeDeliveryResult` element of 12.5 | A delivered result, a refused result, an absent result and a delivered result without `deliveredAt` |
| Notice fake | The notice shape of 12.2 | The notice in state `NOTICE_DISPATCHED` with its served result, a 404, and the not-served announcement accepted |
| Document fake | The proof attach of 12.2 | The proof reference attached, and a 503 |
| Case fake | The three route facts of 12.2 | Each fact accepted with the case state, a refusal from another state, and a delayed answer |
| Approval fake | The approval route of 12.2 | The item granted, and refused with a reason |
| Decision-record library stub | DP-03 | A healthy chain with its outbox row, and a stopped chain |
| Template application | The `legal_action` DDL template | The table created twice in two throwaway schemas, with the standard columns, the primary key and no cross-schema reference |
| Drift test | Every fake against the document | A drifted fake fails the build |

The notice, document, case and approval fakes are stubbed from the published documents of their owners and carry the placeholder until the missing operation names are confirmed (GAP-2750; ASM-4577).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 0 consumed by this document | API-S4-001, API-S4-002 and API-S4-003 provided; the four consumed shapes of 12.2 are declared for the app story and called by nobody here |
| Kafka | None | No event published and none consumed; `DecisionRecorded` is the library's element (12.3, 12.4) |
| Temporal | None | No workflow, activity or Schedule declared; the signal element is the app story's `LitigationWorkflow` (12.5) |
| File | None | No file element in this contract |

### 13. Solution plan

**Package.** Contract artefact of the service: the OpenAPI 3.1 document of the legal action resource, the `LegalActionRequest` and `LegalAction` schemas with the published types in `th.co.scb.ace.workbench.recovery.litigation.api`, the `noticeDeliveryResult` and timer definitions, the `legal_action` DDL template as a resource, and the fake set with the drift test. The implementation behind it is `RWB-S4-E5003-APP`.

**This document declares shapes and moves nothing.** It fixes the names, the types, the widths, the required set, the list references, the two write operations' `Idempotency-Key` rule and the four answers this service hands over. It writes no row, approves no notice, attaches no proof, starts no timer and announces no case state: every one of those acts is an application behaviour of `RWB-S4-E5003-APP`. The period element is declared as a workflow element, because a column for it would put a clock in a schema that the TSD does not give this service, and a Schedule for it would detach the period from the case it belongs to.

**Element surface**

| Element group | Elements | Required |
|---|---|---|
| Identity and case | `id`, `caseId`, `lawFirmId` | `id` and `caseId` yes; `lawFirmId` no |
| Type and status | `actionType`, `status` | both yes, each against its list |
| Court and claim | `lawsuitNo`, `blackCaseNo`, `redCaseNo`, `courtName`, `claimAmount` | none |
| Period | `period.startedAt`, `period.expiresAt`, `period.periodLengthRef`, `period.ruleId`, `period.ruleVersion` | read answer only; never a property of the create |
| Standard | `state`, `version`, `createdAt`, `createdBy`, `updatedAt`, `updatedBy`, `isActive` | none in the body; they are columns of the template |

The element names are the DF-LEG field names in camelCase; the mapping is one to one and is checked by the drift test. No element exists for a notice beyond this row and the period, because no source gives one.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the document names the element and declares no record field of its own | referred to; the consuming story carries the dependency |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | ACE data through the owner's contract or the service's own views; applied as a prohibition: the WIN delivery facts are declared as a consumed notice shape | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the base of this resource is `/api/recovery/litigation/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route; the resource is reached through it and the contract declares no composite route | referred to; the consuming story carries the dependency |

DP-13 is the pattern this story publishes. DP-03 is named and not declared: the record is the library's and the only trace on the resource is the decision element. DP-05 is negative here, as in the app story: no `v_ace_pod` read is declared. DP-19 is the route the two screens use and is the platform edge story's. DP-01 and DP-15 stand behind the DDL template as the schema and migration rules and add no dependency. DP-07 is not in this story's pattern set although two list codes are named; the lists are read as values in force through the reference data of rwb-case and that read carries no dependency row (GAP-2750; ASM-4580). DP-10 is not applied: no Schedule and no Quartz job is declared.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| LegalActionOpenApi | Document | The base, the three operations, the schemas, the security, the error set and the versioning section (BR1 to BR6, BR12) |
| LegalActionSchema | Published schema | `LegalActionRequest` and `LegalAction` with the DF-LEG elements, the required set and the notice sub-shape (BR3, BR8, BR9) |
| LegalActionDdlTemplate | Resource | The `legal_action` DDL: columns, types, keys, the primary key and the standard columns, with no period column (BR8) |
| NoticeSubShape | Published schema | The notice sub-shape and its identifiers, declared once and reused by the create and the read (BR9) |
| DeliverySignalSchema | Published schema | The `noticeDeliveryResult` element and its period element with the reference to the versioned length (BR8, BR10) |
| ProblemEnvelope | Reused schema | The platform problem document with the `messageId` extension (BR5) |
| IdempotencyRule | Document | The `Idempotency-Key` header, the repeated-key answer and its counting (BR4) |
| HandOverShapes | Document | The notice read and announcement, the proof attach, the case route fact and the approval route with the placeholder on the four absent operation names (BR7) |
| Fake set and fixtures | Test asset | The success, refusal, conflict, unavailable and repeated-key answers used by every consuming build (AC6) |
| DriftTest | Test asset | The comparison of a consuming build against sections 11 to 13 (AC6, AC7) |

**Database.** The template creates `legal_action` in `rwb_litigation` only, with the physical types of TSD S4 T3.1 and the standard columns of T3.0. `case_id` and `law_firm_id` are identifiers with no foreign key, and no other schema is named in the template. The template is applied by the service's own Flyway sequence and never edits an applied migration (DP-15). The index set is carried as a gap and the primary key on `id` is the only index declared.

**Configuration and reference data.** The list codes are named and their members are read as values in force with their version (BR3). The period length and the proof window are named as references to versioned reference rows and no value is written here. The capability area and the rights are declared per operation and their role lists are rwb-access data. The problem envelope, its member names and its `messageId` extension are the platform style guide's and are reused, not redeclared.

**Build steps**

1. Write the document with the base and the three operations; lint the paths and the rights (AC1).
2. Write the three schemas with the element mapping, the required set, the enumeration rule and an example; validate the example (AC2).
3. Write the `legal_action` DDL template and apply it twice in two throwaway schemas; assert the columns, the keys, the widths, the absence of a cross-schema key and the absence of a period column (AC4).
4. Write the error section with the problem envelope and one message ID per condition, and the `Idempotency-Key` rule of the two write operations (AC3).
5. Write the delivery signal, its timer element and the decision element with their references (AC5).
6. Write the four hand-over shapes with their placeholders (AC6).
7. Generate the fake set and the drift test, and wire the drift test into the build of `RWB-S4-E5003-APP` and the notice stories (AC6).
8. Write the versioning and boundary section and the absence tests for the old base, the second topic, the timer table and another service's table (AC7).
9. Publish v1 and record the pinned version of this contract and of each consuming story.

**Feature flag.** `rwb.litigation.notice-period-contract`.

**Done when.** The document lints, the three schemas validate, the template applies twice with no period column, the fakes answer every status including the conflict and the repeated key, the drift test is green on the build of this story and of `RWB-S4-E5003-APP`, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Published as | Message |
|---|---|---|---|
| MSG-GEN-001 | A required property is missing, or a value is outside its list (X4) | 422, problem body with `messageId` MSG-GEN-001 and `field` | Enter {field}. |
| MSG-P4-002 | The caller's role does not hold the right of the operation | 403, problem body with `messageId` MSG-P4-002 | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written by the consuming story | 503 on the approval and the create, problem body with `messageId` MSG-P7-003 | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-S4-002 | The prescription date of the case falls inside the warning window, on the consuming story's screen | Not raised here | The claim on this case expires on {date}. File before then. |
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the pack, which the pack stories raise, so no path of this document raises it | Not raised here | The pack is missing {item}. Add it before filing. |

The five texts are the legacy wording of RWB-E5-003 section 14 and are copied unchanged; no message is reworded and no message identifier is added. `MSG-GEN-001` is displayed with the property it names. The 400, 401, 404 and 409 carry the platform problem document and no business message of this set, and the 400 code is not named by any S4 T-A row (GAP-2750; ASM-4580). The 409's message text is not stated in any source read for this key, so the document fixes only its status, its causes — a notice that is not `NOTICE_DISPATCHED`, an action that is not `OPEN`, a period already started — and its `messageId` slot.

### 15. Screens and states

No screen is built in this story. The contract serves two surfaces read through the gateway-bff composite route (DP-19), and it fixes the answer fields they read and nothing of their layout:

| Screen | State | What the contract serves |
|---|---|---|
| SCR-18 Notice approval | Generated | The notice reference, its type and the approval answer of API-S4-001 |
| SCR-18 Notice approval | Approved | The approval state on the notice answer and the legal action of the notice in status `OPEN` |
| SCR-18 Notice approval | Sent | The legal action with `actionType` `NOTICE` and the notice reference |
| SCR-18 Notice approval | Delivered | The period element `startedAt`, `expiresAt`, `ruleId` and `ruleVersion` of the read answer |
| SCR-18 Notice approval | Unserved | The 200 read of a notice action whose period was never started, and the announcement shape's rule |
| SCR-19 Litigation workspace | Pack | The legal action of the notice after the case announced `PACK_ASSEMBLY` |
| SCR-19 Litigation workspace | Instructed | The legal action with `lawFirmId` and the status `OPEN` |
| SCR-19 Litigation workspace | Filed | The legal action with `filedDate`, `courtName` and `blackCaseNo` |
| SCR-19 Litigation workspace | Hearing | The legal action as the hearing story reads it, with `litStatus` |
| SCR-19 Litigation workspace | Judgment | The legal action with `judgmentDate` and `judgmentAmount` |
| SCR-19 Litigation workspace | Empty | Not specified in the source documents (CG-ALL-9070) |
| SCR-19 Litigation workspace | Loading | Not specified in the source documents (CG-ALL-9070) |
| SCR-19 Litigation workspace | Error | Not specified in the source documents (CG-ALL-9070) |
| SCR-19 Litigation workspace | No access | Not specified in the source documents (CG-ALL-9070) |
| SCR-18 Notice approval | Refused | The 403 with MSG-P4-002, and the 409 or 422 of a refused request |
| SCR-18 Notice approval | Failed | The 503 of a stopped decision-record chain or an absent downstream |
| SCR-18 Notice approval | Empty | Not specified in the source documents (CG-ALL-9069) |
| SCR-18 Notice approval | Loading | Not specified in the source documents (CG-ALL-9069) |
| SCR-18 Notice approval | Error | Not specified in the source documents (CG-ALL-9069) |
| SCR-18 Notice approval | No access | Not specified in the source documents (CG-ALL-9069) |

The five SCR-18 states and the five SCR-19 states are the ones the legacy screen block of RWB-E5-003 gives, copied unchanged. The route path, the screen-model field list and the merge order belong to `RWB-PLT-N001-CON`; the transitions behind each state are the app story's, and the case state that SCR-19 shows is rwb-case's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-003-01 | AC1, AC2, AC5 | Contract | The contract half of the period: the create in status `OPEN` with `actionType NOTICE`, the read answer with `startedAt` and `expiresAt`, the signal element and the rule ID and version |
| TC-E5-003-02 | AC1, AC2 | Contract | The contract half of R-LIT-07: the notice sub-shape, the proof reference on the signal and the case route fact `WITH_CUSTOMER_NOTICE_PERIOD` |
| TC-E5-003-03 | AC1, AC2 | Contract | The contract half of R-LIT-08: an absent proof on the signal, the announcement shape and the case route fact `NOTICE_UNSERVED` |
| TC-E5-003-04 | AC3, AC5 | Contract | The contract half of the not-recorded case: the library element, the 503 with MSG-P7-003 and the stopped chain of the stub |
| TC-E5-003-05 | AC3 | Contract | The contract half of the access case: Litigation A, C and R declared per operation, and the 403 with MSG-P4-002 |
| TC-E5-003-06 | AC5, AC6 | Contract | The contract half of the forced-failure case: the stopped chain of the library stub and the drift test on a consuming build |
| TC-S4-E5003-CON-01 | AC1, AC2, AC7 | Contract | The document linted: the base, the three operation IDs, the LegalAction elements, the notice sub-shape, the period element, the absence of the old base, of a second topic and of another service's table |
| TC-S4-E5003-CON-02 | AC3 | Contract | One problem body per status on each operation, the six statuses of the TSD rows, the 400 carried as a gap, the rights per operation and the `Idempotency-Key` required on the two writes and refused absent |
| TC-S4-E5003-CON-03 | AC4 | Component | The template applied in two throwaway schemas; DF-LEG-001 to DF-LEG-014, the standard columns, the types, the widths, the primary key, the absence of a cross-schema key and the absence of a period or timer column asserted; a drifted hand-written table refused |
| TC-S4-E5003-CON-04 | AC5, AC6 | Contract | The delivery signal and its timer element, the decision element, the four hand-over shapes with their placeholders, the ten fakes against the document, and a drifted fake failing the build |
| TC-S4-E5003-CON-05 | AC4 | Component | Boundary of the §12.7 tables: `legal_action` the only table applied; `decision_record` and `idempotency_key` named and not declared; no timer, notice or period table or column in `rwb_litigation`, asserted on the applied template |
| TC-S4-E5003-CON-06 | AC8, BR1 to BR13 | Contract | Each rule of section 8 asserted against the document: the base, the operation IDs, the list codes, the Idempotency-Key rule, the error envelope, the compatibility rule, the consumed operations and the personal-data check |

The first six identifiers are the legacy identifiers of RWB-E5-003 in their legacy order, carried here as the **contract half** of each case: they assert the shape each surface needs and not the business outcome, which `RWB-S4-E5003-APP` proves end to end. The four `TC-S4-E5003-CON-*` identifiers are new tests of the artefact. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the list members, the period length, the proof window, the warning window and the approver route stay data or reference data, and no role code, list value, state member or number of days is written in code.
- No personal data in a schema, an example or a fake: identifiers, notice references, list values, dates and amounts only.
- The contract names only `rwb_litigation` tables and only operations owned by rwb-litigation; the notice, the proof, the case state and the approval are consumed shapes, never provided operations (DP-01, DP-05, BR9).
- One base, one topic and one queue per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- No ACE view and no ACE table is declared or read; the WIN delivery facts arrive through rwb-comms (BR13).
- No event, no workflow, no Schedule and no outbox row is declared by this document; the decision record is the library's element and the period is a timer of the workflow (12.3, 12.5, 12.6).
- No period column and no timer table: the period is an element of the signal and of the read answer, and a breaking change is the only route by which it could become a column (BR8).
- An absent value is written as the placeholder with its gap and assumption pair and never guessed: the index set, the four operation names and the 409 text.
- Every example in the document is synthetic; no production payload and no production file is copied into a schema or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Contract element | Test cases |
|---|---|---|---|---|---|
| No requirement ID in the legacy master (GAP-2750; ASM-4580) | The notice period is started on proof of delivery and tracked to its expiry, and an unserved notice starts no period | FEAT-LIT-03 | 08 Litigate and enforce | The three operations, the notice sub-shape, the delivery signal, the period element and the `legal_action` template | TC-E5-003-01 to TC-E5-003-06, TC-S4-E5003-CON-01 to TC-S4-E5003-CON-04 |
| FEAT-LIT-03 | Run the notice period timer | FEAT-LIT-03 | 08 Litigate and enforce | `actionType = NOTICE`, the period element and the three route facts | TC-S4-E5003-CON-01, TC-S4-E5003-CON-04 |
| R-LIT-07, R-LIT-08, R-LIT-15 | The period starts from `delivered_at`, is not started on an unserved notice, and opens pack assembly at expiry | FEAT-LIT-03 | 08 Litigate and enforce | The delivery signal, the timer element and the case route fact shapes | TC-E5-003-02, TC-E5-003-03, TC-S4-E5003-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-003, disposition Split (rework) |
| Legacy criteria | AC1, AC2, AC3 and AC4 of the legacy story, owned by RWB-S4-E5003-APP; this baseline copies none of them |
| Legacy test cases | TC-E5-003-01 to TC-E5-003-06, carried here as the contract half of each surface |
| Requirement | The legacy master and the Epics 3 to 8 specification carry no REQ identifier for this feature, so both stories trace to FEAT-LIT-03 until the Epics 3 to 8 PRD adds the identifiers (GAP-2750) |
| Screens | SCR-18 Notice approval and SCR-19 Litigation workspace, read through the gateway-bff composite route (DP-19) |
| Sibling slice | RWB-S4-E5003-APP: the validation, the three rule answers, the proof attach, the timer, the row and the announcements |
| Sibling slices of the service | RWB-S4-E5001-APP for the issue of the notices, RWB-S4-E5002-APP for the proof of delivery, RWB-S4-E5004-APP for the pack and the hearing story for API-S4-005 |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-016 (reusable Temporal layer, Schedules replace Quartz), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership), ADR-022 (local decision record plus central ledger) |

### 19. Out of scope

- The implementation behind the contract — the handlers, the repository, the rule evaluations, the workflow, the activities, the timer, the row write, the proof attach and the announcements: `RWB-S4-E5003-APP`.
- The period state machine, which event moves the period and what an unserved notice leaves on the row: `RWB-S4-E5003-APP` section 9.
- The notice record, its template, its dispatch and its served result: rwb-comms (P6) and the notice stories of this service; the approve operation is published here as the TSD and the Ownership Map give it, and the record is not.
- The proof of delivery and its custody in DMS: rwb-document (P5).
- The case of record, its state and the `timer` ledger: rwb-case (P3).
- The approval item, the delegation of authority table and the central ledger: rwb-decision (P7), `RWB-P7-E2013-CON` and `RWB-P7-E2013-APP`; the operation that raises an item is not published there (GAP-2750).
- The legal-action patch (API-S4-004) and the hearings (API-S4-005): the filing, enforcement and hearing stories of this service.
- The pack assembly that R-LIT-15 opens, and R-LIT-05, R-LIT-09, R-LIT-10 and R-LIT-11: `RWB-S4-E5004-APP`, the notice stories and rwb-document.
- The decision-record library itself and its chain: `RWB-PLT-E1027-CON`; the rule packages: rwb-decision (P7).
- The roles, rights, scope and masking data themselves: rwb-access (P4).
- The gateway-bff composite route, the screen field list and the layout of SCR-18 and SCR-19: `RWB-PLT-N001-CON` and the edge stories.
- The deployment of this build, the chart values, the schema, the login and the flag: its own OPS story.
- The cross-service proof of the document against the live owners: the wave 3 integration harness.
