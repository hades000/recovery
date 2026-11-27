# RWB-S4-E5014-CON Decide and manage an appeal - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5014-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-014 |
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

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E5-014 for rwb-litigation (S4). The legal action is published on Day 1 on base `/api/recovery/litigation/v1` with the three operations API-S4-002, API-S4-003 and API-S4-004, the appeal as a value of `action_type`, the `legal_action` DDL template, the decision-record element, the approval-request shape, the four case route facts, the fakes and the drift test. The two legacy acceptance criteria stay with RWB-S4-E5014-APP and every criterion here is new. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S4-E5014-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **contract owner of rwb-litigation (S4)**, I want **the published contract of the legal action as it carries an appeal — the base `/api/recovery/litigation/v1` with API-S4-002 create, API-S4-003 read and API-S4-004 patch, the `LegalActionRequest`, `LegalAction` and `LegalActionUpdate` schemas with the appeal sub-shape and the value `APPEAL` of `action_type`, the `legal_action` DDL template with DF-LEG-001 to DF-LEG-014, the `Idempotency-Key` rule, the error envelope, the declared right of each operation, the decision-record element, the D7.4 approval-request shape, the four case route facts, the fakes and the drift test** instead of the monolith's in-process controller and its one `recovery.legal_action` table, so that **RWB-S4-E5014-APP and every later appeal story build against one frozen, testable shape from Day 1, and a court reference, a case number, a status value or an error status can never drift between rwb-litigation, rwb-decision, rwb-case and rwb-partner without a failing build**.

This story owns the contract and nothing else:

- the OpenAPI 3.1 document of the legal action resource: the base, the three operations, the three object schemas, the problem schema, the security and the error set;
- the appeal sub-shape: `action_type` closed on LOV-LEGAL-TYPE with `APPEAL` among its values, the required set of an appeal, the court references and the filing fields;
- the `legal_action` DDL template with the columns and types of TSD S4 T3.1 and the standard columns of T3.0, applied in this service's own schema, with no cross-schema key;
- the element naming rule (camelCase after the DF-LEG field identifiers), the required set and the enumeration rule that names a list code and no member;
- the `Idempotency-Key` rule on the two write operations, the compatibility rule and the pinning rule;
- the shapes this service hands to rwb-decision, rwb-case and rwb-partner, and the shapes of the answers it reads back;
- the fake set generated from the document, and the drift test every consuming build runs.

It does not build the appeal. The evaluation of R-LIT-45 to R-LIT-49, the row write, the approval call, the case announcements, the firm instruction, the filing step and the durable timers are `RWB-S4-E5014-APP`'s; the case route states are rwb-case's; the approval item and its limit are rwb-decision's; the firm is rwb-partner's and `RWB-S4-E5009-APP`'s. The document declares shapes and moves nothing.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020), and the litigation service has one base and one document for its legal actions. The legacy key RWB-E5-014 recorded the appeal decision, its grounds and its approval against one `recovery` schema, with the legal action, the case, the decision log and the panel all in reach. Four of those are now other services' rows and every one of them is reached on a published shape, so each shape has to be fixed before the app story starts: the three operations and their request and answer bodies, the value of `action_type` that makes a legal action an appeal, the columns an appeal writes, the decision record the service writes in its own transaction, the approval request it hands to the decision centre and the four route facts it announces to the case of record.

The appeal is not a resource of its own. TSD S4 gives one `legal_action` table, one action type list with six values of which `APPEAL` is one, and one status list with six values; the appeal is a legal action of that type, so a second resource or a second table would fork the vocabulary. This document therefore fixes the type, its required fields and its court references inside the one existing resource — which is also why no new table and no new column is invented here, and why the two values the legacy criterion names but no source stores, the appeal grounds and the appeal window end, are carried as gaps rather than guessed (GAP-2802; ASM-4642; GAP-2805; ASM-4645).

The baseline also fixes the naming the checks require: schema `rwb_litigation`, login `rwb_litigation`, base `/api/recovery/litigation/v1`, topic `rwb.litigation.events.v1` with retry and `.dlt` topics, event names `rwb.litigation.<Event>.v1`, task queue `rwb-litigation` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.litigation`. It keeps the operation IDs the TSD allocates, API-S4-002 create, API-S4-003 read and API-S4-004 patch, of which the legacy endpoint block names only the create and the read.

Two contested points are carried as gaps rather than decided quietly. The approval contract publishes reads and the three decisions but no operation that raises an approval item, so the appeal's "take it to the approver at D7.4" has no published operation and no field set (GAP-2801; ASM-4641). And the case contract and the partner contract are named by the Architecture in prose only, so their operation names are absent and are carried as the placeholder (GAP-2801; ASM-4641).

It serves FEAT-LIT-14 "Decide and manage an appeal" through the shape of its legal action, and it traces to that feature until the Epics 3 to 8 PRD adds requirement identifiers, because the legacy master and the Epics 3 to 8 specification carry none for this key (GAP-2803; ASM-4643).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the event names and the package follow the platform rule and not a local choice.
- The platform error envelope and its `messageId` extension are the platform baseline; where this document narrows them it does so explicitly. The envelope, its member names and its extension are reused and never redeclared.
- The reference lists of the legal action are the data of rwb-case and are read with their version: LOV-LEGAL-TYPE (`NOTICE`, `CIVIL_CASE`, `APPEAL`, `ENFORCEMENT`, `BANKRUPTCY_PETITION`, `LED_AUCTION`) and LOV-LEGAL-STATUS (`OPEN`, `FILED`, `JUDGMENT`, `ENFORCING`, `CLOSED`, `WITHDRAWN`) of TSD S4 T3.2. The document names the list codes and their members as the TSD enumerates them, and the version in force is read at run time.
- The `legal_action` row and its columns are the TSD S4 T3.1 row, DF-LEG-001 to DF-LEG-014, plus the seven standard columns of T3.0. No field outside that row is declared, because no source gives one for an appeal: the grounds and the window end are absent from the row and from the FSD field catalog (GAP-2802; ASM-4642).
- The decision record is the local decision-record library's, `RWB-PLT-E1027-CON`, and its shape is not fixed here: this document names the element it needs and points to the library.
- The approval contract is the P7 document this baseline reads for the shape it hands over; the case contract and the partner contract are read for the answer shapes and their operation names are absent (GAP-2801; ASM-4641).
- No build dependency: this story is Day 1 by rule (Template and Rules section R5.7 rule 1), and every consuming story of the service builds against it and its fake.

### 4. Flow

1. Draft the OpenAPI 3.1 document of the legal action resource on base `/api/recovery/litigation/v1`: API-S4-002, API-S4-003 and API-S4-004 with their request and answer bodies, their rights and their error sets.
2. Fix the `LegalAction` element set from DF-LEG-001 to DF-LEG-014 in camelCase, with the required set of TSD S4 T3.1 and the two list references of T3.2.
3. Fix the appeal sub-shape: `actionType = APPEAL` required on the create, `courtName`, `claimAmount`, `lawFirmId`, `lawsuitNo` and `blackCaseNo` optional on the create, and the filing fields and the court numbers on the patch.
4. Write the `legal_action` DDL template with the columns, the physical types, the widths, the keys and the standard columns; carry the index set as a gap and add no column for the grounds or the window end.
5. Write the decision-record element and the three hand-over shapes: the D7.4 approval request to rwb-decision, the four case route facts to rwb-case, and the firm instruction request to rwb-partner.
6. Write the `Idempotency-Key` rule on the two write operations, the versioning rule, the compatibility rule and the pinning rule.
7. Generate the fake set from the document and wire the drift test into the build of this story and of `RWB-S4-E5014-APP`.
8. Publish v1 and record the pinned version of each consuming story.
9. Hand the baseline to `RWB-S4-E5014-APP`, to the sibling S4 stories that read the same resource, and to the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | None | AC1 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC8 |
| X3 | A fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC7 |
| X4 | A value of `actionType` outside LOV-LEGAL-TYPE is sent | The document refuses it as an enumeration error at 422 and no row is written | MSG-GEN-001 | AC2 |
| X5 | The operation is called without the `Idempotency-Key` header | The document refuses the request at 400 and the fake answers the same; no stored answer exists | None | AC3 |
| X6 | The document declares an operation of another service or a second base | The review fails the baseline; a consumed shape is described as consumed, never as provided | None | AC8 |
| X7 | A column is proposed for the appeal grounds or the appeal window end | The review refuses it: no source gives the column, and adding one is a new major version of the template | None | AC4 |
| X8 | A retired element reappears in the document | The absence test fails: no old monolith base, no second topic and no table of another schema | None | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the TSD S4 and the platform envelopes only, and consumes no service |
| Negotiable | The index set, the approval-raise shape and the absent operation names are settled with their owners; the base, the operation IDs, the columns and the list codes are fixed by the target architecture |
| Valuable | Unblocks the app story on Day 1 and the sibling S4 stories that read the same legal action |
| Estimable | One OpenAPI document, one DDL template, three hand-over shapes, one fake set and eight contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the legal action that carries an appeal

  Background:
    Given the service naming rule of the platform library is in force
    Given the legal action of rwb-litigation is served on the base /api/recovery/litigation/v1
    Given the reference lists are LOV-LEGAL-TYPE and LOV-LEGAL-STATUS of TSD S4 T3.2, read with their version in force

  Scenario: AC1 The three legal-action operations are declared with the appeal fields and the action type (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-litigation is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /cases/{caseId}/legal-actions as API-S4-002, GET /legal-actions/{legalActionId} as API-S4-003 and PATCH /legal-actions/{legalActionId} as API-S4-004, all under the base /api/recovery/litigation/v1 and owned by rwb-litigation
    Then the LegalAction schema carries id, caseId, lawFirmId, actionType, lawsuitNo, blackCaseNo, redCaseNo, courtName, claimAmount, filedDate, judgmentDate, judgmentAmount, litStatus and status
    Then actionType names LOV-LEGAL-TYPE and APPEAL is one of its values, and status names LOV-LEGAL-STATUS with its six values
    Then the document declares no second base, no second resource and no operation of another service
    Then every legacy operation ID of TSD S4 T-A.1 is kept and no operation is renumbered

  Scenario: AC2 The appeal create, its answer and the filing patch are fixed as shapes (new, D-RCV-60)
    Given the LegalActionRequest, LegalAction and LegalActionUpdate schemas of the document
    When the appeal sub-shape is reviewed
    Then LegalActionRequest requires actionType with the value APPEAL, and carries caseId from the path, courtName, claimAmount, lawFirmId, lawsuitNo and blackCaseNo as optional properties
    Then the create answers 201 with LegalAction in status OPEN, and the answer carries the identifiers, the court references and the status of the row it wrote
    Then LegalActionUpdate carries filedDate, courtName, blackCaseNo, lawsuitNo and judgmentDate, and the filing sets filedDate and status FILED
    Then no element of the request or the answer names a table, a column or a value outside TSD S4 T3.1 and T3.2, and no separate appeal resource is declared
    Then no element carries the appeal grounds or the appeal window end, because no column of the row or field of the catalog holds them (GAP-2802; ASM-4642)
    Then a value of actionType outside LOV-LEGAL-TYPE is refused at 422 with MSG-GEN-001 naming the property
    Then the approval request, the case route facts and the firm instruction are declared as consumed shapes and never as operations of this service (GAP-2801; ASM-4641)

  Scenario: AC3 The Idempotency-Key rule, the error envelope and the declared right of each operation are fixed (new, D-RCV-60)
    Given the operation table of the document
    When it is reviewed against TSD S4 T-A.1 and T-A.2
    Then API-S4-002 and API-S4-004 declare the Idempotency-Key header and a stored answer, and API-S4-003 declares no Idempotency-Key
    Then the error responses are 401, 403, 404, 409, 422 and 503 as the TSD rows give them, each with the platform problem document and one message ID per condition
    Then a body that cannot be parsed answers 400 with the same envelope, a code no S4 T-A row names and carried as a gap (GAP-2801; ASM-4641)
    Then the declared rights are Litigation C on the create, Litigation R on the read and Litigation U on the patch, with the scope applied and the role lists held by rwb-access
    Then a caller without the right is refused at 403 with MSG-P4-002 and changes nothing
    Then the document declares no right of its own invention and no role code as a constant

  Scenario: AC4 The legal_action columns and their indexes are declared and no column is added (new, D-RCV-60)
    Given the legal_action DDL template of schema rwb_litigation
    When it is compared with TSD S4 T3.1 and T3.0
    Then the template declares DF-LEG-001 to DF-LEG-014 with their physical types, widths and required flags, and the seven standard columns
    Then case_id, law_firm_id and the court numbers are identifiers with no foreign key across schemas
    Then status is varchar(15) against LOV-LEGAL-STATUS and action_type is varchar(20) against LOV-LEGAL-TYPE, both closed by the list and not by a check constraint of their members
    Then the template declares no column for the appeal grounds and none for the appeal window end (GAP-2802; ASM-4642)
    Then the index set beyond the primary key on id is Not specified in the source documents (GAP-2801; ASM-4641) and the template declares the primary key only
    Then the template is applied by the service's own Flyway sequence and never edits an applied migration (DP-15)
    Then no table and no column outside this row is declared, and the holding of a written table is a new major version

  Scenario: AC5 The decision-record element and the D7.4 approval-request shape handed to rwb-decision are fixed (new, D-RCV-60)
    Given the decision element of the document and the approval shape of the rwb-decision approval contract
    When they are compared with DP-03 and with that approval document
    Then the document names the decision record as the local library's element on rwb.decision-record.v1 with the decision code, the rule ID, the rule version, the inputs reference, the final call, the decided time and the two hashes, and fixes none of the library's own fields
    Then the approval request this service hands over carries the case reference, the legal action reference, the decision code, the capability area, the product group, the amount, the source type and reference, the rule ID and its version, and the Idempotency-Key
    Then the level is declared as D7.4 and the above-limit approval of the Head of Litigation as the approver route of R-LIT-47, both held by rwb-decision and neither re-implemented here
    Then the operation that raises the approval item and the field set of its answer are Not specified in the source documents (GAP-2801; ASM-4641)
    Then no field of decision_log_entry of rwb-decision and no rule row is declared or written by this service

  Scenario: AC6 The four case route facts handed to rwb-case are fixed as shapes (new, D-RCV-60)
    Given the case element of the document
    When it is compared with R-LIT-45 to R-LIT-49 and with the case of record
    Then the document declares JUDGMENT_DISMISSED, APPEAL_DECISION, APPEAL_FILED, IN_HEARING and TO_WRITE_OFF as route states of rwb-case and never as status values of legal_action (GAP-2804; ASM-4644)
    Then each announcement this service hands over carries the case reference, the legal action reference, the route fact, the rule ID and the version in force
    Then the answer shape carries the accepted or refused outcome and the case state the case of record holds, and no case field is written here
    Then the operation name of the announcement and the field list of the answer are Not specified in the source documents (GAP-2801; ASM-4641)
    Then the document declares no read of recovery_case and no case rule, and it fixes no transition of the case route

  Scenario: AC7 The contract fakes answer the document and the drift test blocks a drifted build (new, D-RCV-60)
    Given the fake set generated from the document
    When each fake is compared with the operation or the element it serves
    Then the legal-action fake answers the 201 create, the 200 read, the 200 patch, the 400, 401, 403, 404, 409, 422 and 503 refusals, and the repeated Idempotency-Key
    Then the approval fake answers the D7.4 grant, the above-limit grant, the refusal with a reason and the delayed answer
    Then the case fake answers each of the four route facts accepted, the refusal from another state and a delayed answer
    Then the partner fake answers the appeal instruction accepted and a refusal outside the panel
    Then the decision-record library stub answers a healthy chain and a stopped chain
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC8 The naming baseline and the boundary of the document are fixed (new, D-RCV-60)
    Given the naming and boundary section of the document
    When it is reviewed against the Template and Rules and the ownership rows of the service
    Then the base is /api/recovery/litigation/v1, the schema and the login are rwb_litigation, the topic is rwb.litigation.events.v1 with retry and .dlt topics, the event names are rwb.litigation.<Event>.v1, the task queue is rwb-litigation in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.litigation
    Then the document declares no event of its own: the service's ownership rows carry no event and this baseline publishes none
    Then the document declares no read of another service's table, no cross-schema join and no v_ace_ view, and it names recovery_case, decision_log_entry, rule_row, document, partner, notice and hearing as other owners' consumed shapes only
    Then the old monolith base appears nowhere in the document, its examples or its fakes
    Then the document names no second topic, no second queue and no batch table
```

These eight criteria are new for the contract baseline and test the artefact only; they restate no business outcome of `RWB-S4-E5014-APP` and they copy no criterion of the legacy story. The wave 3 harness that consumes this baseline copies none of them.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/litigation/v1`; the document never declares another service's path as provided | DP-13; context pack S4 naming rules |
| BR2 | The three operations keep their TSD operation IDs API-S4-002, API-S4-003 and API-S4-004, and no fourth operation of this resource is declared | TSD S4 T-A.1; legacy Endpoints block |
| BR3 | `action_type` and `status` are declared as enumerations of LOV-LEGAL-TYPE and LOV-LEGAL-STATUS and the code names the list, never a member list curated locally | TSD S4 T3.2; FSD S4 A2.14.3.1 (BR-S4-014) |
| BR4 | A read declares no `Idempotency-Key`; a write declares it and stores its answer | TSD S4 T-A.1; ADR-020 |
| BR5 | Error responses use one envelope and one message ID per condition; the business message texts are copied unchanged from the legacy story | Template and Rules section R7.2 (s14); legacy Validation and messages block |
| BR6 | A schema change is additive within a major version; a breaking change is a new major version, and the holding of a written table is a breaking change | ADR-020; ADR-021 |
| BR7 | The document lists only operations owned by rwb-litigation; a consumed operation or shape is described as consumed, never as provided | context pack, ownership rows owned by S4 |
| BR8 | The case route states of the appeal are rwb-case's and the status of the legal action is this service's; the document never uses one for the other | R-LIT-45 to R-LIT-49; TSD S4 T3.2 |
| BR9 | No business value is fixed in the contract: the list members, the appeal window, the filing deadline, the D7.4 limit and the grounds stay data or reference data | TSD S4 T3.2; Template and Rules section R7.2 (s17) |
| BR10 | The decision record is the local library's element on the shared topic, never a new event of this service, and its fields are the library's | DP-03; ADR-022 |
| BR11 | No personal data in a schema, an example or a fake: identifiers, list values, court references, dates and amounts only | TSD S4 T3.1; FSD S4 A2.14.3.2 |
| BR12 | No ACE view and no ACE table is declared or read by this document; the court status arrives from LIT through COLLINS and rwb-source-data | DP-05; TSD S4 T3.1 (DF-LEG-013) |

### 9. State transitions

The document's own lifecycle is the only state this story moves:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The three operations, the appeal shape, the template and the hand-over shapes are described | In review |
| In review | Consumer sign-off | `RWB-S4-E5014-APP` and the sibling S4 stories accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1, for example a new court reference | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, a column of the template changes, or a list code changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |

Two vocabularies are declared and neither is moved here:

| Object | Values | Note |
|---|---|---|
| legal_action.action_type | `NOTICE`, `CIVIL_CASE`, `APPEAL`, `ENFORCEMENT`, `BANKRUPTCY_PETITION`, `LED_AUCTION` (LOV-LEGAL-TYPE) | Declared as the list reference; the appeal is the value `APPEAL` |
| legal_action.status | `OPEN`, `FILED`, `JUDGMENT`, `ENFORCING`, `CLOSED`, `WITHDRAWN` (LOV-LEGAL-STATUS) | Declared as the list reference; the moves between the values are the app story's |

The appeal state machine — which event moves a legal action from `OPEN` to `FILED`, and what a declined appeal leaves on the row — belongs to `RWB-S4-E5014-APP` and appears nowhere in this document. The five case route states `JUDGMENT_DISMISSED`, `APPEAL_DECISION`, `APPEAL_FILED`, `IN_HEARING` and `TO_WRITE_OFF` are rwb-case's, and the document fixes only the shapes of their announcements (BR8). No value of LOV-LEGAL-STATUS names an appeal decision, which is why the ruling on the row's status is carried as (GAP-2804; ASM-4644).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-litigation | Owns the OpenAPI document, the DDL template and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the ownership rows the baseline consumes |
| Consuming teams (RWB-S4-E5014-APP, the sibling S4 stories, and the rwb-decision, rwb-case and rwb-partner owners whose answer shapes are declared) | Review and sign off the parts they consume |
| Platform library owner | Owns the problem envelope, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an element, an example or a fake, and that no column is invented for the grounds or the window end |
| Business analyst of S4 | Confirms that LOV-LEGAL-TYPE and LOV-LEGAL-STATUS are named as list codes and that no member list is curated locally |

The login name behind the document's security scheme is `rwb_litigation` by the naming rule of DP-02; the document names the scheme and not a credential, and no role, level or mask is defined here.

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

| Item | Content |
|---|---|
| Appeal sub-shape | `actionType = APPEAL` required on the create; `courtName`, `claimAmount`, `lawFirmId`, `lawsuitNo` and `blackCaseNo` optional; the filing fields `filedDate`, `courtName`, `blackCaseNo`, `lawsuitNo` and the judgment fields on the patch |
| Index set | Beyond the primary key on `id` the set is `Not specified in the source documents (GAP-2801; ASM-4641)`; the template declares the primary key only and the app story's two lookups are named there |
| Appeal grounds | No column and no field; carried as `Not specified in the source documents (GAP-2802; ASM-4642)` and held in the decision record's inputs reference by the app story |
| Appeal window end and filing deadline | No column and no field; carried as `Not specified in the source documents (GAP-2805; ASM-4645)` and held as durable timers of `LitigationWorkflow` |
| Decision record | The element the library writes: the decision code, the rule ID and version, the inputs reference, the final call, the decided time and the two hashes. The library owns the fields and the chain (DP-03) |
| Approval request | The shape handed to rwb-decision at D7.4; its raise operation is absent from the approval contract (GAP-2801; ASM-4641) |
| Case route facts | The shapes handed to rwb-case and read back; their operation names are absent (GAP-2801; ASM-4641) |
| Firm instruction request | The shape handed to rwb-partner; the instruction is `RWB-S4-E5009-APP`'s and its operation name is absent (GAP-2801; ASM-4641) |

**No new table, no new column and no migration.** `legal_action` is the TSD S4 T3.1 row and this document publishes its DDL template for the service's own Flyway sequence (DP-15); `decision_record` and `idempotency_key` are platform library objects created in `rwb_litigation` by the library's migration and are named here, not declared. `recovery_case` (P3), `decision_log_entry` and `rule_row` (P7), `document` (P5), `partner` (S9), `notice` (P6), `hearing` (S4, the hearing story's) and every `v_ace_*` view (P1) are other owners' and are named as consumed shapes only. `legal_action.case_id`, `law_firm_id` and the court numbers are identifiers, not foreign keys across schemas (DP-01).

**No personal data.** No element of this contract carries a name, an address, an identity number or an account number. The court references and the amounts are not personal data, and the borrower and the guarantor are reached by the services that need them through rwb-source-data and never through this resource.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13). This story publishes all three operations.

| ID | Method | Path | Request | Response | Access | Idempotency | Errors |
|---|---|---|---|---|---|---|---|
| API-S4-002 | POST | `/cases/{caseId}/legal-actions` | `LegalActionRequest`; `caseId` from the path; `actionType = APPEAL` for an appeal | 201 with `LegalAction` in status `OPEN` | Litigation C, scope applied | `Idempotency-Key` required, answer stored | 401, 403, 404, 409, 422, 503 |
| API-S4-003 | GET | `/legal-actions/{legalActionId}` | None | 200 with `LegalAction` | Litigation R, scope applied | Not applicable | 401, 403, 404, 503 |
| API-S4-004 | PATCH | `/legal-actions/{legalActionId}` | `LegalActionUpdate`, for example the filing of an appeal | 200 with `LegalAction` | Litigation U, scope applied | `Idempotency-Key` required, answer stored | 401, 403, 404, 409, 422, 503 |

The purpose, request and response entities, rights, idempotency and error statuses are those of TSD S4 T-A.1 and T-A.2 for API-S4-002, API-S4-003 and API-S4-004, with the base renamed by DP-13. The hearing operation API-S4-005 and the notice approval API-S4-001 are not declared here, because they belong to the hearing and notice stories of this service.

#### 12.2 REST operations consumed

None: a contract document calls no service. The three rows below are the shapes this service **hands over** and the answers it reads back; the document declares them, and the calls are `RWB-S4-E5014-APP`'s.

| Shape | Owner | Declared here | Open point |
|---|---|---|---|
| The approval request and its answer | P7 rwb-decision | The request elements of the appeal item at D7.4 and the granted, refused or delayed answer | The operation that raises an item and the field set of its answer are Not specified in the source documents (GAP-2801; ASM-4641) |
| The four case route facts and their answer | P3 rwb-case | `APPEAL_DECISION`, `APPEAL_FILED`, `IN_HEARING` and `TO_WRITE_OFF`, the rule and its version, and the accepted or refused answer | The operation name and the field list of the answer are Not specified in the source documents (GAP-2801; ASM-4641) |
| The firm instruction request | S9 rwb-partner | The case reference, the legal action reference, the appeal type and the pack reference the instruction needs | The operation name is Not specified in the source documents (GAP-2801; ASM-4641); the instruction itself is `RWB-S4-E5009-APP`'s |

Every one of them is one hop with a 2 s timeout in the app story's implementation (ADR-020). No operation of another service is declared as provided here (BR7).

#### 12.3 Events published

None. The ownership rows of rwb-litigation carry no event, so this document publishes none and declares no payload of its own; the service topic `rwb.litigation.events.v1` with its retry and `.dlt` topics is reserved by the naming rule and stays unpublished by this baseline. The decision record is written through the local decision-record library of DP-03, which publishes `DecisionRecorded` on the shared `rwb.decision-record.v1`; that element is the library's.

#### 12.4 Events consumed

None. The approval answer, the case answer and the partner answer are synchronous answers of their contracts, not topics, so the document names no subscription and no inbox. The rule events of the appeal (`JUDGMENT_AGAINST_THE_BANK`, `APPEAL_WINDOW_OPEN`, `APPEAL_APPROVED`, `APPEAL_HEARING_SET`, `APPEAL_DECLINED`) are evaluated in the service from its own facts and the case read, and are not topics either.

#### 12.5 Workflows and activities

None. The document defines no workflow and no activity. `LitigationWorkflow` is the app story's, on task queue `rwb-litigation` in namespace `rwb-recovery`, and the approval child workflow runs on `rwb-decision`; this baseline fixes only the names the app and operations stories register, and the child's own type name, workflow ID and queue registration are Not specified in the source documents (GAP-2801; ASM-4641).

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job is declared; the appeal window and the filing deadline are durable timers of the app story's workflow, and their lengths are the reference rows of GAP-2805.

#### 12.7 Tables owned

| Table | Schema | Owner | Note |
|---|---|---|---|
| legal_action | `rwb_litigation` | S4 | The DDL template of section 11: DF-LEG-001 to DF-LEG-014, the seven standard columns, the primary key on `id` and no cross-schema key (DP-01, DP-15) |
| decision_record | `rwb_litigation` | PLT library object applied in this schema | Named only: the shape is `RWB-PLT-E1027-CON`'s and the row is written in the caller's transaction (DP-03) |
| idempotency_key | `rwb_litigation` | PLT library object applied in this schema | Named only: the stored answer of the two write operations |

`hearing` is S4's and belongs to the hearing story; `recovery_case` (P3), `decision_log_entry` and `rule_row` (P7), `document` (P5), `partner` (S9) and `notice` (P6) are other owners' and appear only as consumed shapes. No table of another service is declared, read or keyed.

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Legal-action fake | The three operations of 12.1 | A 201 create in status `OPEN`, a 200 read of the same legal action, a 200 patch to `FILED`, and the 400, 401, 403, 404, 409, 422 and 503 refusals |
| Repeated-key fake | The `Idempotency-Key` rule | The first answer returned again for the same key, with no second legal action |
| Approval fake | The approval shape of 12.2 | The D7.4 item granted, the above-limit grant of the Head of Litigation, the refusal with a reason, and a delayed answer |
| Case fake | The case shapes of 12.2 | Each of the four route facts accepted, the refusal from another state, and a delayed answer |
| Partner fake | The firm instruction shape of 12.2 | The appeal instruction accepted with the firm reference, and a refusal outside the panel |
| Decision-record library stub | DP-03 | A healthy chain with its outbox row, and a stopped chain |
| Template application | The `legal_action` DDL template | The table created twice in two throwaway schemas, with the standard columns, the primary key and no cross-schema reference |
| Drift test | Every fake against the document | A drifted fake fails the build |

The approval, case and partner fakes are stubbed from the published documents of their owners and carry the placeholder until the missing operation names are confirmed (GAP-2801; ASM-4641).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 0 consumed by this document | API-S4-002, API-S4-003 and API-S4-004 provided; the three consumed shapes of 12.2 are declared for the app story and called by nobody here |
| Kafka | None | No event published and none consumed; `DecisionRecorded` is the library's element (12.3) |
| Temporal | None | No workflow, activity or Schedule; `LitigationWorkflow` and the approval child are the app story's (12.5) |
| File | None | No file element in this contract |

### 13. Solution plan

**Package.** Contract artefact of the service: the OpenAPI 3.1 document of the legal action resource, the `LegalActionRequest`, `LegalAction` and `LegalActionUpdate` schemas with the published types in `th.co.scb.ace.workbench.recovery.litigation.api`, the `legal_action` DDL template as a resource, and the fake set with the drift test. The implementation behind it is `RWB-S4-E5014-APP`.

**This document declares shapes and moves nothing.** It fixes the names, the types, the widths, the required set, the list references, the two write operations' `Idempotency-Key` rule and the answers this service hands over. It writes no row, opens no appeal, requests no approval, announces no case route, instructs no firm and files nothing: every one of those acts is an application behaviour of `RWB-S4-E5014-APP`, and a contract that performed one would be a second implementation of the story. The appeal state machine — which event moves `legal_action.status` from `OPEN` to `FILED`, what a declined appeal leaves on the row, and when the filing fact is written — is the app story's and is described in its section 9 only; this document states the vocabulary and the shapes and fixes no transition. The five case route states are rwb-case's and are declared here as announcement shapes only.

**Element surface**

| Element group | Elements | Required |
|---|---|---|
| Identity and case | `id`, `caseId`, `lawFirmId` | `id` and `caseId` yes; `lawFirmId` no |
| Type and status | `actionType`, `status` | both yes, each against its list |
| Court and claim | `lawsuitNo`, `blackCaseNo`, `redCaseNo`, `courtName`, `claimAmount` | none |
| Judgment and enforcement | `judgmentDate`, `judgmentAmount`, `litStatus` | none |
| Standard | `state`, `version`, `createdAt`, `createdBy`, `updatedAt`, `updatedBy`, `isActive` | none in the body; they are columns of the template |

The element names are the DF-LEG field names in camelCase; the mapping is one to one and is checked by the drift test. No element exists for an appeal beyond this row, because no source gives one: the grounds and the window end are absent and stay absent (GAP-2802; GAP-2805).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the document names the element and declares no record field of its own | referred to; the consuming story carries the dependency |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the base of this resource is `/api/recovery/litigation/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route; the resource is reached through it and the contract declares no composite route | referred to; the consuming story carries the dependency |

DP-13 is the pattern this story publishes. DP-03 is named and not declared: the record is the library's and the only trace on the resource is the decision element. DP-19 is the route the two screens use and is the platform edge story's. DP-01 and DP-15 stand behind the DDL template as the schema and migration rules and add no dependency. DP-07 is not in this story's pattern set although two list codes are named; the lists are read as values in force through the reference data of rwb-case, and that read carries no dependency row (GAP-2801; ASM-4641).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| LegalActionOpenApi | Document | The base, the three operations, the schemas, the security, the error set and the versioning section (BR1 to BR6, BR11) |
| LegalActionSchema | Published schema | `LegalActionRequest`, `LegalAction` and `LegalActionUpdate` with the DF-LEG elements, the required set and the appeal sub-shape (BR3, BR8) |
| LegalActionDdlTemplate | Resource | The `legal_action` DDL: columns, types, keys, the primary key and the standard columns (BR3, BR9) |
| AppealElementSet | Published schema | The appeal sub-shape, its court references and its filing fields, declared once and reused by the create and the patch (BR8) |
| ProblemEnvelope | Reused schema | The platform problem document with the `messageId` extension (BR5) |
| IdempotencyRule | Document | The `Idempotency-Key` header, the repeated-key answer and its counting (BR4) |
| HandOverShapes | Document | The approval request, the four case route facts and the firm instruction request, with the placeholder on the three absent operation names (BR7) |
| Fake set and fixtures | Test asset | The success, refusal, conflict, unavailable and repeated-key answers used by every consuming build (AC7) |
| DriftTest | Test asset | The comparison of a consuming build against sections 11 to 13 (AC7, AC8) |

**Database.** The template creates `legal_action` in `rwb_litigation` only, with the physical types of TSD S4 T3.1 and the standard columns of T3.0. `case_id`, `law_firm_id` and the court numbers are identifiers with no foreign key, and no other schema is named in the template. The template is applied by the service's own Flyway sequence and never edits an applied migration (DP-15). The index set is carried as a gap and the primary key on `id` is the only index declared.

**Configuration and reference data.** The list codes are named and their members are read as values in force with their version (BR3). The capability area and the rights are declared per operation and their role lists are rwb-access data. The problem envelope, its member names and its `messageId` extension are the platform style guide's and are reused, not redeclared.

**Build steps**

1. Write the document with the base and the three operations; lint the paths and the rights (AC1).
2. Write the three schemas with the element mapping, the required set, the enumeration rule and an example; validate the example (AC2).
3. Write the `legal_action` DDL template and apply it twice in two throwaway schemas; assert the columns, the keys, the widths and the absence of a cross-schema key (AC4).
4. Write the error section with the problem envelope and one message ID per condition, and the `Idempotency-Key` rule of the two write operations (AC3).
5. Write the decision element and the three hand-over shapes with their placeholders (AC5, AC6).
6. Write the naming and boundary section and the absence tests for the old base, the second topic and another service's table (AC8).
7. Generate the fake set and the drift test, and wire the drift test into the build of `RWB-S4-E5014-APP` and the sibling S4 stories (AC7).
8. Publish v1 and record the pinned version of this contract and of each consuming story (AC8).

**Feature flag.** `rwb.litigation.legal-action-contract`, shared with the legal-action resource of the service.

**Done when.** The document lints, the three schemas validate, the template applies twice, the fakes answer every status including the conflict and the repeated key, the drift test is green on the build of this story and of `RWB-S4-E5014-APP`, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Published as | Message |
|---|---|---|---|
| MSG-GEN-001 | A required property is missing, or a value is outside its list (X4) | 422, problem body with `messageId` MSG-GEN-001 and `field` | Enter {field}. |
| MSG-P4-002 | The caller's role does not hold the right of the operation | 403, problem body with `messageId` MSG-P4-002 | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written by the consuming story | 503 on the create, problem body with `messageId` MSG-P7-003 | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the pack, which the pack stories of this service raise, so no path of this document raises it | Not raised here | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | The claim expiry of the case falls inside the filing window, on the consuming story's screen | Not raised here | The claim on this case expires on {date}. File before then. |

The five texts are the legacy wording of RWB-E5-014 section 14 and are copied unchanged; no message is reworded and no message identifier is added. `MSG-GEN-001` is displayed with the property it names. The 400, 401, 404, 409 and the platform 503 carry the platform problem document and no business message of this set, and the 400 code is not named by any S4 T-A row (GAP-2801; ASM-4641). The 409's message text is not stated in any source read for this key, so the document fixes only its status, its cause and its `messageId` slot.

### 15. Screens and states

No screen is built in this story. The contract serves two surfaces read through the gateway-bff composite route (DP-19), and it fixes the answer fields they read and nothing of their layout:

| Screen | State | What the contract serves |
|---|---|---|
| SCR-18 Notice approval | Generated | The notices of the case as the notice stories serve them; no appeal element |
| SCR-18 Notice approval | Approved, Sent, Delivered, Unserved | The notice states as the notice stories serve them; no appeal element |
| SCR-19 Litigation workspace | Pack | The legal action with `actionType`, `courtName`, `claimAmount` and `status` `OPEN` |
| SCR-19 Litigation workspace | Instructed | The same legal action with the approval reference of the answer and the status `OPEN` |
| SCR-19 Litigation workspace | Filed | The legal action with `filedDate`, `courtName`, `blackCaseNo`, `redCaseNo` and `status` `FILED` |
| SCR-19 Litigation workspace | Hearing | The legal action as the hearing story reads it, with `litStatus` |
| SCR-19 Litigation workspace | Judgment | The legal action with `judgmentDate` and `judgmentAmount` |
| SCR-19 Litigation workspace | Refused | The 403 with MSG-P4-002, and the 409 or 422 of a refused request |

The three SCR-18 states and the five SCR-19 states are the ones the legacy screen block of RWB-E5-014 gives, copied unchanged. The route path, the screen-model field list and the merge order belong to `RWB-PLT-N001-CON`; the transition behind each state is the app story's, and the case route states SCR-19 shows are rwb-case's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-014-01 | AC1, AC2 | Contract | The contract half of the appeal decision and filing: the create in status `OPEN`, the answer fields, the patch to `FILED` and the `APPEAL` value of `actionType` |
| TC-E5-014-02 | AC5 | Contract | The contract half of the not-recorded case: the library element, the 503 with MSG-P7-003 and the stopped chain of the stub |
| TC-E5-014-03 | AC3 | Contract | The contract half of the access case: Litigation C, R and U declared per operation, and the 403 with MSG-P4-002 |
| TC-E5-014-04 | AC5, AC7 | Contract | The contract half of the forced-failure case: the stopped chain of the library stub and the drift test on a consuming build |
| TC-S4-E5014-CON-01 | AC1, AC2, AC8 | Contract | The document linted: the base, the three operation IDs, the LegalAction elements, the appeal sub-shape, the absence of the old base, of a second topic and of another service's table |
| TC-S4-E5014-CON-02 | AC3 | Contract | One problem body per status on each operation, the six statuses of the TSD rows, the 400 carried as a gap, the rights per operation and the `Idempotency-Key` required on the two writes and refused absent |
| TC-S4-E5014-CON-03 | AC4 | Component | The template applied in two throwaway schemas; DF-LEG-001 to DF-LEG-014, the standard columns, the types, the widths, the primary key, the absence of a cross-schema key and the absence of a grounds column asserted; a drifted hand-written table refused |
| TC-S4-E5014-CON-04 | AC5, AC6, AC7 | Contract | The decision element, the approval request, the four case route facts and the instruction shapes with their placeholders, the eight fakes against the document, and a drifted fake failing the build |

The first four identifiers are the legacy identifiers of RWB-E5-014 in their legacy order, carried here as the **contract half** of each case: they assert the shape each surface needs and not the business outcome, which `RWB-S4-E5014-APP` proves end to end. The four `TC-S4-E5014-CON-*` identifiers are new tests of the artefact. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the list members, the appeal window, the filing deadline, the D7.4 limit and the grounds stay data or reference data, and no role code, list value or state member is written in code.
- No personal data in a schema, an example or a fake: identifiers, court references, list values, dates and amounts only.
- The contract names only `rwb_litigation` tables and only operations owned by rwb-litigation; the approval, the case facts and the firm instruction are consumed shapes, never provided operations (DP-01).
- One base, one topic and one queue per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- No ACE view and no ACE table is declared or read; the court status arrives from LIT through COLLINS and rwb-source-data (DP-05).
- No event, no workflow, no Schedule and no outbox row is declared by this document; the decision record is the library's element (12.3, 12.5, 12.6).
- An absent value is written as the placeholder with its gap and assumption pair and never guessed: the index set, the grounds, the window end and the filing deadline, the approval raise operation, the case operation name and the partner operation name.
- Every example in the document is synthetic; no production payload and no production file is copied into a schema or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Contract element | Test cases |
|---|---|---|---|---|---|
| No requirement ID in the legacy master (GAP-2803; ASM-4643) | The appeal decision, its grounds and its approval are recorded as a legal action and tracked to its end | FEAT-LIT-14 | 08 Litigate and enforce | The three operations, the appeal sub-shape, the `legal_action` template and the hand-over shapes | TC-E5-014-01 to TC-E5-014-04, TC-S4-E5014-CON-01 to TC-S4-E5014-CON-04 |
| FEAT-LIT-14 | Decide and manage an appeal | FEAT-LIT-14 | 08 Litigate and enforce | `actionType = APPEAL`, the court references, the filing fields and the four case route facts | TC-S4-E5014-CON-01, TC-S4-E5014-CON-04 |
| R-LIT-46, R-LIT-47, R-LIT-49 | The appeal is decided at D7.4, filed on approval and routed to write-off on refusal | FEAT-LIT-14 | 08 Litigate and enforce | The approval request shape, the case route facts and the decision element | TC-E5-014-01, TC-S4-E5014-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-014, disposition Split (rework) |
| Legacy criteria | AC1 and AC2 of the legacy story, owned by RWB-S4-E5014-APP; this baseline copies none of them |
| Legacy test cases | TC-E5-014-01 to TC-E5-014-04, carried here as the contract half of each surface |
| Requirement | The legacy master and the Epics 3 to 8 specification carry no REQ identifier for this feature, so both stories trace to FEAT-LIT-14 until the PRD adds the identifiers (GAP-2803) |
| Screens | SCR-18 Notice approval and SCR-19 Litigation workspace, read through the gateway-bff composite route (DP-19) |
| Sibling slice | RWB-S4-E5014-APP: the evaluation, the row, the approval call, the case announcements, the instruction, the filing and the timers |
| Sibling slices of the service | `RWB-S4-E5016-APP` (judgment and dismissal), `RWB-S4-E5011-APP` (hearings, API-S4-005), `RWB-S4-E5012-APP` (next-step proposal), `RWB-S4-E5009-APP` (firm instruction) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership), ADR-022 (local decision record plus central ledger) |

### 19. Out of scope

- The implementation behind the contract — the handlers, the repository, the rule evaluation, the workflow, the activities, the row write, the three calls and the timers: `RWB-S4-E5014-APP`.
- The appeal state machine, which event moves the legal action and what a declined appeal leaves on the row: `RWB-S4-E5014-APP` section 9.
- The approval item, the D7.4 limit and its clock: rwb-decision (P7) and its approval contract story; the operation that raises an item is not published there (GAP-2801).
- The case of record, its route states and their transitions: rwb-case (P3).
- The firm instruction itself, its pack, its lifecycle and the firm's result: `RWB-S4-E5009-APP` and rwb-partner (S9).
- The dismissal and the judgment that open the appeal window: `RWB-S4-E5016-APP`.
- The hearings of the appeal and the `hearing` table (API-S4-005): `RWB-S4-E5011-APP`.
- The pack documents, their checklist and the document that would carry the appeal grounds: rwb-document (P5) and the pack stories of this service, which raise MSG-S4-001.
- The notices and their approval (API-S4-001): rwb-comms (P6) and the notice story of this service.
- The court status that arrives from LIT through COLLINS and rwb-source-data: rwb-source-data (P1) and rwb-integration (P2).
- The decision-record library itself and its chain: `RWB-PLT-E1027-CON`; the central ledger and the rule packages: rwb-decision (P7).
- The roles, rights, scope and masking data themselves: rwb-access (P4).
- The gateway-bff composite route, the screen field list and the layout of SCR-18 and SCR-19: `RWB-PLT-N001-CON` and the edge stories.
- The deployment of this build, the chart values, the schema, the login and the flag: its own OPS story.
- The cross-service proof of the document against the live owners: the wave 3 integration harness.
