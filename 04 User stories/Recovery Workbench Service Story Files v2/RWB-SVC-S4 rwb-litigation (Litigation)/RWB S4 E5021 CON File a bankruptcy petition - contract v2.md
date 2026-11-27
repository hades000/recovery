# RWB-S4-E5021-CON File a bankruptcy petition - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5021-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-021 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Size | Not set in this story; the squad sizes it at refinement |
| Contract version | v1 (major version in the base path /api/recovery/litigation/v1) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E5-021 for rwb-litigation (S4). The legal action is published on Day 1 on base `/api/recovery/litigation/v1` with the three operations API-S4-002, API-S4-003 and API-S4-004, the petition as a value of `action_type`, the `legal_action` DDL template, the decision-record element, the two consumed answer shapes and the fakes; the three legacy acceptance criteria stay with RWB-S4-E5021-APP and every criterion here is new. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S4-E5021-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (7 resolved, 13 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **contract owner of rwb-litigation (S4)**, I want **the published contract of the legal action as it carries the bankruptcy petition — the base `/api/recovery/litigation/v1` with API-S4-002 create, API-S4-003 read and API-S4-004 patch, the `LegalActionRequest`, `LegalAction` and `LegalActionUpdate` schemas with the petition sub-shape and the value `BANKRUPTCY_PETITION` of `action_type`, the `legal_action` DDL template with DF-LEG-001 to DF-LEG-014, the `Idempotency-Key` rule, the error envelope, the declared right of each operation, the decision-record element, the approval-request shape handed to rwb-decision, the case-move answer shape handed to rwb-case, the fakes and the drift test** instead of the monolith's in-process controller and its one `recovery.legal_action` table, so that **RWB-S4-E5021-APP and every later litigation story build against one frozen, testable shape from Day 1, and a court field, a status value, an action type or an error status can never drift between rwb-litigation, rwb-decision, rwb-case and rwb-partner without a failing build**.

This story owns the contract and nothing else:

- the OpenAPI 3.1 document of the legal action resource: the base, the three operations, the three object schemas, the problem schema, the security and the error set;
- the petition sub-shape: `action_type` closed on LOV-LEGAL-TYPE with `BANKRUPTCY_PETITION` among its values, the required set of a petition and the filing fields;
- the `legal_action` DDL template with the columns and types of TSD S4 T3.1 and the standard columns of T3.0, applied in this service's own schema, with no cross-schema key;
- the element naming rule (camelCase after the DF-LEG field identifiers), the required set and the enumeration rule that names a list code and no member;
- the `Idempotency-Key` rule on the two write operations, the compatibility rule and the pinning rule;
- the shapes this service hands to rwb-decision, rwb-case and rwb-partner, and the shapes of the answers it reads back;
- the fake set generated from the document, and the drift test every consuming build runs.

It does not build the petition. The evaluation of R-LIT-58, the row write, the approval call, the case announcement, the firm instruction and the filing step are `RWB-S4-E5021-APP`'s; the case route state `BANKRUPTCY_PETITION` is rwb-case's; the approval item and its clock are rwb-decision's; and the firm instruction is rwb-partner's and `RWB-S4-E5009-APP`'s. The document declares shapes and moves nothing.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020), and the litigation service has one base and one document for its legal actions. The legacy key RWB-E5-021 opened the action, took the petition to the approver and filed it through the firm against one `recovery` schema, with the legal action, the case, the approval and the panel all in reach. Four of those are now other services' rows and every one of them is reached on a published shape, so each shape has to be fixed before the app story starts: the three operations and their request and answer bodies, the value of `action_type` that makes a legal action a bankruptcy petition, the columns a petition writes, the decision record the service writes in its own transaction, and the two answers it hands over.

The petition is not a resource of its own. TSD S4 gives one `legal_action` table, one action type list with six values of which `BANKRUPTCY_PETITION` is one, and one status list with six values; the petition is a legal action of that type, so a second resource or a second table would fork the vocabulary. This document therefore fixes the type, its required fields and its states inside the one existing resource — which is also why no new table and no new column is invented here, and why the index set of `legal_action` has to be carried as a gap rather than guessed (GAP-1890; ASM-3105).

The baseline also fixes the naming the checks require: schema `rwb_litigation`, login `rwb_litigation`, base `/api/recovery/litigation/v1`, topic `rwb.litigation.events.v1` with retry and `.dlt` topics, event names `rwb.litigation.<Event>.v1`, task queue `rwb-litigation` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.litigation`. It keeps the operation IDs the TSD allocates, API-S4-002 create, API-S4-003 read and API-S4-004 patch, of which the legacy endpoint block names only the create and the read.

Two contested points are carried as gaps rather than decided quietly. The approval contract publishes reads and the three decisions but no operation that raises an approval item, so the petition's "take it to the approver" has no published operation and no field set (GAP-1889; ASM-4688). And the case contract and the partner contract are named by Architecture v5 in prose only — "Partner: issueInstruction (law firm)" and the case-facts move — so their operation names are absent (GAP-1885; ASM-4687).

It serves FEAT-LIT-21 "File a bankruptcy petition" through the shape of its legal action, and it traces to that feature until the Epics 3 to 8 PRD adds requirement identifiers, because the legacy master and the Epics 3 to 8 specification carry none for this key (GAP-1886; ASM-3101).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the event names and the package follow the platform rule and not a local choice.
- The platform error envelope and its `messageId` extension are the platform baseline; where this document narrows them it does so explicitly. The envelope, its member names and its extension are reused and never redeclared.
- The reference lists of the legal action are the data of rwb-case and are read with their version: LOV-LEGAL-TYPE (`NOTICE`, `CIVIL_CASE`, `APPEAL`, `ENFORCEMENT`, `BANKRUPTCY_PETITION`, `LED_AUCTION`) and LOV-LEGAL-STATUS (`OPEN`, `FILED`, `JUDGMENT`, `ENFORCING`, `CLOSED`, `WITHDRAWN`) of TSD S4 T3.2. The document names the list codes and their members as the TSD enumerates them, and the version in force is read at run time.
- The `legal_action` row and its columns are the TSD S4 T3.1 row, DF-LEG-001 to DF-LEG-014, plus the seven standard columns of T3.0. No field outside that row is declared, because no source gives one for a petition.
- The decision record is the local decision-record library's, `RWB-PLT-E1027-CON`, and its shape is not fixed here: this document names the element it needs and points to the library.
- The approval contract `RWB-P7-E2013-CON` is the P7 document this baseline reads for the shape it hands over; the case contract and the partner contract are read for the answer shapes and their operation names are absent (GAP-1885; ASM-4687; GAP-1889; ASM-4688).
- No build dependency: this story is Day 1 by rule (Template and Rules section R5.7 rule 1), and every consuming story of the service builds against it and its fake.
- The FSD S4 v3 and the TSD S4 v2 this baseline reads are In review with an empty sign-off table, and this document is not signed off either. The run of D-RCV-60 has no human approval step, so both slices of the key carry Status Draft (realignment v1) and the missing approval is recorded rather than waited for (GAP-2834; ASM-4658).

### 4. Flow

1. Draft the OpenAPI 3.1 document of the legal action resource on base `/api/recovery/litigation/v1`: API-S4-002, API-S4-003 and API-S4-004 with their request and answer bodies, their rights and their error sets.
2. Fix the `LegalAction` element set from DF-LEG-001 to DF-LEG-014 in camelCase, with the required set of TSD S4 T3.1 and the two list references of T3.2.
3. Fix the petition sub-shape: `actionType = BANKRUPTCY_PETITION` required on the create, `claimAmount`, `courtName`, `lawFirmId`, `lawsuitNo` and `blackCaseNo` optional on the create, and the filing fields on the patch.
4. Write the `legal_action` DDL template with the columns, the physical types, the widths, the keys and the standard columns; carry the index set as a gap.
5. Write the decision-record element and the two answer shapes this service hands over: the approval request to rwb-decision, the case-move answer to rwb-case, and the firm instruction request to rwb-partner.
6. Write the `Idempotency-Key` rule on the two write operations, the versioning rule, the compatibility rule and the pinning rule.
7. Generate the fake set from the document and wire the drift test into the build of this story and of `RWB-S4-E5021-APP`.
8. Publish v1 and record the pinned version of each consuming story.
9. Hand the baseline to `RWB-S4-E5021-APP`, to the sibling S4 stories that read the same resource, and to the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | None | AC1 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC8 |
| X3 | A fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC7 |
| X4 | A value of `actionType` outside LOV-LEGAL-TYPE is sent | The document refuses it as an enumeration error at 422 and no row is written | MSG-GEN-001 | AC2 |
| X5 | The operation is called without the `Idempotency-Key` header | The document refuses the request at 400 and the fake answers the same; no stored answer exists | None | AC3 |
| X6 | The document declares an operation of another service or a second base | The review fails the baseline; a consumed shape is described as consumed, never as provided | None | AC8 |
| X7 | The index set of `legal_action` is guessed | The row carries the placeholder and the gap, and the template declares only the primary key | None | AC4 |
| X8 | A retired element reappears in the document | The absence test fails: no old monolith base, no second topic and no table of another schema | None | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the TSD S4 and the platform envelopes only, and consumes no service |
| Negotiable | The index set, the approval-raise shape and the two absent operation names are settled with their owners; the base, the operation IDs, the columns and the list codes are fixed by the target architecture |
| Valuable | Unblocks the app story on Day 1 and the sibling S4 stories that read the same legal action |
| Estimable | One OpenAPI document, one DDL template, three consumed shapes, one fake set and eight contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the legal action that carries a bankruptcy petition

  Background:
    Given the service naming rule of the platform library is in force
    Given the legal action of rwb-litigation is served on the base /api/recovery/litigation/v1
    Given the reference lists are LOV-LEGAL-TYPE and LOV-LEGAL-STATUS of TSD S4 T3.2, read with their version in force

  Scenario: AC1 The three legal-action operations are declared with the petition fields and the action type (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-litigation is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /cases/{caseId}/legal-actions as API-S4-002, GET /legal-actions/{legalActionId} as API-S4-003 and PATCH /legal-actions/{legalActionId} as API-S4-004, all under the base /api/recovery/litigation/v1 and owned by rwb-litigation
    Then the LegalAction schema carries id, caseId, lawFirmId, actionType, lawsuitNo, blackCaseNo, redCaseNo, courtName, claimAmount, filedDate, judgmentDate, judgmentAmount, litStatus and status
    Then actionType names LOV-LEGAL-TYPE and BANKRUPTCY_PETITION is one of its values, and status names LOV-LEGAL-STATUS with its six values
    Then the document declares no second base, no second resource and no operation of another service
    Then every legacy operation ID of TSD S4 T-A.1 is kept and no operation is renumbered

  Scenario: AC2 The petition create, its answer and the filing patch are fixed as shapes (new, D-RCV-60)
    Given the LegalActionRequest, LegalAction and LegalActionUpdate schemas of the document
    When the petition sub-shape is reviewed
    Then LegalActionRequest requires actionType with the value BANKRUPTCY_PETITION, and carries caseId from the path, claimAmount, courtName, lawFirmId, lawsuitNo and blackCaseNo as optional properties
    Then the create answers 201 with LegalAction in status OPEN, and the answer carries the identifiers, the court fields and the status of the row it wrote
    Then LegalActionUpdate carries filedDate, courtName, blackCaseNo, lawsuitNo and claimAmount, and the filing sets filedDate and status FILED
    Then no element of the request or the answer names a table, a column or a value outside TSD S4 T3.1 and T3.2, and no separate petition resource is declared
    Then a value of actionType outside LOV-LEGAL-TYPE is refused at 422 with MSG-GEN-001 naming the property
    Then the request and answer of the approval raise and of the case move are declared as consumed shapes and never as operations of this service (GAP-1889; ASM-4688)

  Scenario: AC3 The Idempotency-Key rule, the error envelope and the declared right of each operation are fixed (new, D-RCV-60)
    Given the operation table of the document
    When it is reviewed against TSD S4 T-A.1 and T-A.2
    Then API-S4-002 and API-S4-004 declare the Idempotency-Key header and a stored answer, and API-S4-003 declares no Idempotency-Key
    Then the error responses are 401, 403, 404, 409, 422 and 503 as the TSD rows give them, each with the platform problem document and one message ID per condition
    Then a body that cannot be parsed answers 400 with the same envelope, a code no S4 T-A row names and carried as a gap (GAP-1890; ASM-3105)
    Then the declared rights are Litigation C on the create, Litigation R on the read and Litigation U on the patch, with the scope applied and the role lists held by rwb-access
    Then a caller without the right is refused at 403 with MSG-P4-002 and changes nothing
    Then the document declares no right of its own invention and no role code as a constant

  Scenario: AC4 The legal_action columns and their indexes are declared and no column is added (new, D-RCV-60)
    Given the legal_action DDL template of schema rwb_litigation
    When it is compared with TSD S4 T3.1 and T3.0
    Then the template declares DF-LEG-001 to DF-LEG-014 with their physical types, widths and required flags, and the seven standard columns
    Then case_id, law_firm_id and the court references are identifiers with no foreign key across schemas
    Then status is varchar(15) against LOV-LEGAL-STATUS and action_type is varchar(20) against LOV-LEGAL-TYPE, both closed by the list and not by a check constraint of their members
    Then the index set beyond the primary key on id is Not specified in the source documents (GAP-1890; ASM-3105) and the template declares the primary key only
    Then the template is applied by the service's own Flyway sequence and never edits an applied migration (DP-15)
    Then no table and no column outside this row is declared, and the holding of a written table is a new major version

  Scenario: AC5 The decision-record element and the approval-request shape handed to rwb-decision are fixed (new, D-RCV-60)
    Given the decision element of the document and the approval shape of RWB-P7-E2013-CON
    When they are compared with DP-03 and with the P7 approval document
    Then the document names the decision record as the local library's element on rwb.decision-record.v1 with the decision code, the rule ID, the rule version, the inputs reference, the final call, the decided time and the two hashes, and fixes none of the library's own fields
    Then the approval request this service hands over carries the case reference, the legal action reference, the decision code, the capability area, the product group, the amount, the source type and reference, the rule ID and its version, and the Idempotency-Key
    Then the operation that raises the approval item and the field set of its answer are Not specified in the source documents (GAP-1889; ASM-4688)
    Then the 5 working days of R-LIT-58 is declared as the approval workflow's clock on rwb-decision and not as a timer of this service (GAP-1888; ASM-3103)
    Then no field of decision_log_entry of rwb-decision and no rule row is declared or written by this service

  Scenario: AC6 The case-move answer handed to rwb-case is fixed (new, D-RCV-60)
    Given the case element of the document
    When it is compared with R-LIT-58 and with the case of record
    Then the document declares the route fact BANKRUPTCY_PETITION as a route state of rwb-case and never as a status of legal_action
    Then the announcement this service hands over carries the case reference, the legal action reference, the route fact, the rule ID R-LIT-58 and the version in force
    Then the answer shape carries the accepted or refused outcome and the case state the case of record holds, and no case field is written here
    Then the operation name of the announcement and the field list of the answer are Not specified in the source documents (GAP-1885; ASM-4687)
    Then the document declares no read of recovery_case and no case rule, and it fixes no transition of the case route

  Scenario: AC7 The contract fakes answer the document and the drift test blocks a drifted build (new, D-RCV-60)
    Given the fake set generated from the document
    When each fake is compared with the operation or the element it serves
    Then the legal-action fake answers the 201 create, the 200 read, the 200 patch, the 400, 401, 403, 404, 409, 422 and 503 refusals, and the repeated Idempotency-Key
    Then the approval fake answers the granted, the refused and the delayed D7.5 answer of RWB-P7-E2013-CON
    Then the case fake answers the accepted route fact, the refusal from another state and a delayed answer
    Then the partner fake answers the accepted instruction and a refusal outside the panel
    Then the decision-record library stub answers a healthy chain and a stopped chain
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC8 The naming baseline and the boundary of the document are fixed (new, D-RCV-60)
    Given the naming and boundary section of the document
    When it is reviewed against the Template and Rules and the Ownership Map
    Then the base is /api/recovery/litigation/v1, the schema and the login are rwb_litigation, the topic is rwb.litigation.events.v1 with retry and .dlt topics, the event names are rwb.litigation.<Event>.v1, the task queue is rwb-litigation in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.litigation
    Then the document declares no event of its own: LawsuitFiled, JudgmentRecorded and AuctionResult are the catalogue's and this story publishes none (GAP-1887; ASM-3102)
    Then the document declares no read of another service's table, no cross-schema join and no v_ace_ view, and it names recovery_case, document, decision_log_entry, rule_row, partner and notice as other owners' consumed shapes only
    Then the old monolith base appears nowhere in the document, its examples or its fakes
    Then the document names no second topic, no second queue and no batch table
```

These eight criteria are new for the contract baseline and test the artefact only; they restate no business outcome of `RWB-S4-E5021-APP` and they copy no criterion of the legacy story. The wave 3 harness that consumes this baseline copies none of them.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | One REST base per service: `/api/recovery/litigation/v1`; the document never declares another service's path as provided | DP-13; Architecture v5 slide 41 notes | TC-S4-E5021-CON-01 |
| BR2 | The three operations keep their TSD operation IDs API-S4-002, API-S4-003 and API-S4-004, and no fourth operation of this resource is declared | TSD S4 T-A.1; legacy Endpoints block | TC-S4-E5021-CON-01 |
| BR3 | `action_type` and `status` are declared as enumerations of LOV-LEGAL-TYPE and LOV-LEGAL-STATUS and the code names the list, never a member list curated locally | TSD S4 T3.2; FSD S4 A2.21.3.1 (BR-S4-021) | TC-S4-E5021-CON-01 |
| BR4 | A read declares no `Idempotency-Key`; a write declares it and stores its answer | Architecture v5 slide 11; TSD S4 T-A.1 | TC-S4-E5021-CON-02 |
| BR5 | Error responses use one envelope and one message ID per condition; the business message texts are copied unchanged from the legacy story | Architecture v5 platform baseline; Template and Rules section R7.2 (s14) | TC-S4-E5021-CON-02 |
| BR6 | A schema change is additive within a major version; a breaking change is a new major version, and the holding of a written table is a breaking change | Architecture v5 slide 42 notes (BACKWARD compatibility) | TC-S4-E5021-CON-01 |
| BR7 | The document lists only operations owned by rwb-litigation; a consumed operation or shape is described as consumed, never as provided | Ownership Map v1 | TC-S4-E5021-CON-01 |
| BR8 | The case route state `BANKRUPTCY_PETITION` is rwb-case's and the status of the legal action is this service's; the document never uses one for the other | R-LIT-58; `ownership.json` (`recovery_case` owner P3) | TC-E5-021-02 |
| BR9 | No business value is fixed in the contract: the list members, the filing window, the bankruptcy test, the index set and the approver route stay data or reference data | TSD S4 T3.2; Template and Rules section R7.2 (s17) | TC-S4-E5021-CON-01 |
| BR10 | The decision record is the local library's element on the shared topic, never a new event of this service, and its fields are the library's | DP-03; Architecture v5 slide 42 (event 08) | TC-S4-E5021-CON-04 |
| BR11 | No personal data in a schema, an example or a fake: identifiers, list values, court references, dates and amounts only | TSD S4 T3.1; Architecture v5 slides 42 and 43 notes | TC-S4-E5021-CON-01 |
| BR12 | No ACE view and no ACE table is declared or read by this document; the lit_status field arrives from LIT through COLLINS and rwb-source-data | DP-05; TSD S4 T3.1 (DF-LEG-013) | TC-S4-E5021-CON-01 |
| BR13 | Reference data read: the lists are LOV-LEGAL-TYPE and LOV-LEGAL-STATUS; the parameters read are Not specified in the source documents (DOR-RWB-S4-E5021-CON-20) | DP-06; DP-07 | TC-S4-E5021-CON-01 |

### 9. State transitions

The document's own lifecycle is the only state this story moves:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The three operations, the petition shape, the template and the consumed shapes are described | In review |
| In review | Consumer sign-off | `RWB-S4-E5021-APP` and the sibling S4 stories accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1, for example a new court reference | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, a column of the template changes, or a list code changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |

Two vocabularies are declared and neither is moved here:

| Object | Values | Note |
|---|---|---|
| legal_action.action_type | `NOTICE`, `CIVIL_CASE`, `APPEAL`, `ENFORCEMENT`, `BANKRUPTCY_PETITION`, `LED_AUCTION` (LOV-LEGAL-TYPE) | Declared as the list reference; the petition is the value `BANKRUPTCY_PETITION` |
| legal_action.status | `OPEN`, `FILED`, `JUDGMENT`, `ENFORCING`, `CLOSED`, `WITHDRAWN` (LOV-LEGAL-STATUS) | Declared as the list reference; the moves between the values are the app story's |

The petition state machine — which event moves a legal action from `OPEN` to `FILED` and what a refused approval leaves behind — belongs to `RWB-S4-E5021-APP` and appears nowhere in this document. The case route state `BANKRUPTCY_PETITION` is rwb-case's and the document fixes only the shape of the announcement (BR8).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-litigation | Owns the OpenAPI document, the DDL template and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes |
| Consuming teams (RWB-S4-E5021-APP, the sibling S4 stories, and the rwb-decision, rwb-case and rwb-partner owners whose answer shapes are declared) | Review and sign off the parts they consume |
| Platform library owner | Owns the problem envelope, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an element, an example or a fake |
| Business analyst of S4 | Confirms that LOV-LEGAL-TYPE and LOV-LEGAL-STATUS are named as list codes and that no member list is curated locally |
| rwb-access authorise check | Each operation of this resource is checked by the rwb-access authorise check against the rights declared per operation in section 12; the check's role codes are Not specified in the source documents (DOR-RWB-S4-E5021-CON-6) |

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

| Item | BR Field ID | Content |
|---|---|---|
| Petition sub-shape | Not specified in the source documents (DOR-RWB-S4-E5021-CON-7) | `actionType = BANKRUPTCY_PETITION` required on the create; `claimAmount`, `courtName`, `lawFirmId`, `lawsuitNo` and `blackCaseNo` optional; the filing fields `filedDate`, `courtName`, `blackCaseNo`, `lawsuitNo` and `claimAmount` on the patch |
| Index set | Not specified in the source documents (DOR-RWB-S4-E5021-CON-7) | Beyond the primary key on `id` the set is `Not specified in the source documents (GAP-1890; ASM-3105)`; the template declares the primary key only and the app story's two lookups are named there |
| Decision record | Not specified in the source documents (DOR-RWB-S4-E5021-CON-7) | The element the library writes: the decision code, the rule ID and version, the inputs reference, the final call, the decided time and the two hashes. The library owns the fields and the chain (DP-03) |
| Approval request | Not specified in the source documents (DOR-RWB-S4-E5021-CON-7) | The shape handed to rwb-decision; its raise operation is absent from the P7 contract (GAP-1889; ASM-4688) |
| Case-move answer | Not specified in the source documents (DOR-RWB-S4-E5021-CON-7) | The shape handed to rwb-case and read back; its operation name is absent (GAP-1885; ASM-4687) |
| Firm instruction request | Not specified in the source documents (DOR-RWB-S4-E5021-CON-7) | The shape handed to rwb-partner; the instruction is `RWB-S4-E5009-APP`'s and its operation name is absent (GAP-1885; ASM-4687) |

**No new table, no new column and no migration.** `legal_action` is the TSD S4 T3.1 row and this document publishes its DDL template for the service's own Flyway sequence (DP-15); `decision_record` and `idempotency_key` are platform library objects created in `rwb_litigation` by the library's migration and are named here, not declared. `recovery_case` (P3), `document` (P5), `decision_log_entry` and `rule_row` (P7), `partner` (S9), `notice` (P6) and every `v_ace_*` view (P1) are other owners' and are named as consumed shapes only. `legal_action.case_id` and `law_firm_id` are identifiers, not foreign keys across schemas (DP-01).

**No personal data.** No element of this contract carries a name, an address, an identity number or an account number. The court references and the amounts are not personal data, and the borrower and the guarantor are reached by the services that need them through rwb-source-data and never through this resource.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13). This story publishes all three operations.

| ID | Method | Path | Request | Response | Access | Idempotency | Errors |
|---|---|---|---|---|---|---|---|
| API-S4-002 | POST | `/cases/{caseId}/legal-actions` | `LegalActionRequest`; `caseId` from the path; `actionType = BANKRUPTCY_PETITION` for a petition | 201 with `LegalAction` in status `OPEN` | Litigation C, scope applied | `Idempotency-Key` required, answer stored | 401, 403, 404, 409, 422, 503 |
| API-S4-003 | GET | `/legal-actions/{legalActionId}` | None | 200 with `LegalAction` | Litigation R, scope applied | Not applicable | 401, 403, 404, 503 |
| API-S4-004 | PATCH | `/legal-actions/{legalActionId}` | `LegalActionUpdate`, for example the filing of a petition | 200 with `LegalAction` | Litigation U, scope applied | `Idempotency-Key` required, answer stored | 401, 403, 404, 409, 422, 503 |

The purpose, request and response entities, rights, idempotency and error statuses are those of TSD S4 T-A.1 and T-A.2 for API-S4-002, API-S4-003 and API-S4-004, with the base renamed by DP-13. The hearing operation API-S4-005 and the notice approval API-S4-001 are not declared here, because they belong to the hearing and notice stories of this service.

#### 12.2 REST operations consumed

None: a contract document calls no service. The three rows below are the shapes this service **hands over** and the answers it reads back; the document declares them, and the calls are `RWB-S4-E5021-APP`'s.

| Shape | Owner | Declared here | Open point |
|---|---|---|---|
| The approval request and its answer | P7 rwb-decision (`RWB-P7-E2013-CON`) | The request elements of the petition item and the granted, refused or delayed answer | The operation that raises an item and the field set of its answer are Not specified in the source documents (GAP-1889; ASM-4688) |
| The case-move announcement and its answer | P3 rwb-case | The route fact `BANKRUPTCY_PETITION`, the rule and its version, and the accepted or refused answer | The operation name and the field list of the answer are Not specified in the source documents (GAP-1885; ASM-4687) |
| The firm instruction request | S9 rwb-partner | The case reference, the legal action reference, the petition type and the pack reference the instruction needs | The operation name is Not specified in the source documents (GAP-1885; ASM-4687); the instruction itself is `RWB-S4-E5009-APP`'s |

Every one of them is one hop with a 2 s timeout in the app story's implementation (ADR-020). No operation of another service is declared as provided here (BR7).

#### 12.3 Events published

None. The service topic `rwb.litigation.events.v1` carries `LawsuitFiled`, `JudgmentRecorded` and `AuctionResult` in the event catalogue (Architecture v5 slides 19 and 43); this document publishes none of them, because DP-09 is not in this story's pattern set and the catalogue assigns no story to `LawsuitFiled`, so the filing of a bankruptcy petition is not tied to that event by any source read here (GAP-1887; ASM-3102). The decision record is written through the local decision-record library of DP-03, which publishes `DecisionRecorded` (event 08) on the shared `rwb.decision-record.v1`; that element is the library's and this document declares no payload of its own.

#### 12.4 Events consumed

None. The approval answer, the case answer and the partner answer are synchronous answers of their contracts, not topics, so the document names no subscription and no inbox. `NoticeDelivered` and `PartnerResultSubmitted`, the two events Architecture v5 slide 19 gives rwb-litigation as input, belong to the demand-notice and firm-result stories and are not declared here.

#### 12.5 Workflows and activities

None. The document defines no workflow and no activity. `LitigationWorkflow` is the app story's, on task queue `rwb-litigation` in namespace `rwb-recovery`, and the approval child workflow runs on `rwb-decision`; this baseline fixes only the names the app and operations stories register, and the child's own type name, workflow ID and queue registration are Not specified in the source documents (GAP-1888; ASM-3103).

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job is declared; the 5 working days of R-LIT-58 is the approval workflow's durable timer on `rwb-decision` and not a Schedule of this service.

#### 12.7 Tables owned

| Table | Schema | Owner | Note |
|---|---|---|---|
| legal_action | `rwb_litigation` | S4 | The DDL template of section 11: DF-LEG-001 to DF-LEG-014, the seven standard columns, the primary key on `id` and no cross-schema key (DP-01, DP-15) |
| decision_record | `rwb_litigation` | PLT library object applied in this schema | Named only: the shape is `RWB-PLT-E1027-CON`'s and the row is written in the caller's transaction (DP-03) |
| idempotency_key | `rwb_litigation` | PLT library object applied in this schema | Named only: the stored answer of the two write operations |

`hearing` is S4's and belongs to the hearing story; `recovery_case` (P3), `document` (P5), `decision_log_entry` and `rule_row` (P7), `partner` (S9) and `notice` (P6) are other owners' and appear only as consumed shapes. No table of another service is declared, read or keyed.

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Legal-action fake | The three operations of 12.1 | A 201 create in status `OPEN`, a 200 read of the same legal action, a 200 patch to `FILED`, and the 400, 401, 403, 404, 409, 422 and 503 refusals |
| Repeated-key fake | The `Idempotency-Key` rule | The first answer returned again for the same key, with no second legal action |
| Approval fake | The approval shape of 12.2 | The D7.5 item granted, refused with a reason, and delayed beyond 2 s |
| Case fake | The case-move shape of 12.2 | The route fact `BANKRUPTCY_PETITION` accepted, the refusal from another state, and a delayed answer |
| Partner fake | The firm instruction shape of 12.2 | The instruction accepted with the firm reference, and a refusal outside the panel |
| Decision-record library stub | DP-03 | A healthy chain with its outbox row, and a stopped chain |
| Template application | The `legal_action` DDL template | The table created twice in two throwaway schemas, with the standard columns, the primary key and no cross-schema reference |
| Drift test | Every fake against the document | A drifted fake fails the build |

The approval, case and partner fakes are stubbed from the published documents of their owners and carry the placeholder until the missing operation names are confirmed (GAP-1885; ASM-4687; GAP-1889; ASM-4688).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 0 consumed by this document | API-S4-002, API-S4-003 and API-S4-004 provided; the three consumed shapes of 12.2 are declared for the app story and called by nobody here |
| Kafka | None | No event published and none consumed; `DecisionRecorded` is the library's element (12.3) |
| Temporal | None | No workflow, activity or Schedule; `LitigationWorkflow` and the approval child are the app story's (12.5) |
| File | None | No file element in this contract |

### 13. Solution plan

**Package.** Contract artefact of the service: the OpenAPI 3.1 document of the legal action resource, the `LegalActionRequest`, `LegalAction` and `LegalActionUpdate` schemas with the published types in `th.co.scb.ace.workbench.recovery.litigation.api`, the `legal_action` DDL template as a resource, and the fake set with the drift test. The implementation behind it is `RWB-S4-E5021-APP`.

**This document declares shapes and moves nothing.** It fixes the names, the types, the widths, the required set, the list references, the two write operations' `Idempotency-Key` rule and the answers this service hands over. It writes no row, opens no petition, requests no approval, announces no case route and files nothing: every one of those acts is an application behaviour of `RWB-S4-E5021-APP`, and a contract that performed one would be a second implementation of the story. The petition state machine — which event moves `legal_action.status` from `OPEN` to `FILED`, what a refused approval leaves on the row, and when the filing fact is written — is the app story's and is described in its section 9 only; this document states the vocabulary and the shapes and fixes no transition. The case route state `BANKRUPTCY_PETITION` is rwb-case's and is declared here as an announcement shape only.

**Element surface**

| Element group | Elements | Required |
|---|---|---|
| Identity and case | `id`, `caseId`, `lawFirmId` | `id` and `caseId` yes; `lawFirmId` no |
| Type and status | `actionType`, `status` | both yes, each against its list |
| Court and claim | `lawsuitNo`, `blackCaseNo`, `redCaseNo`, `courtName`, `claimAmount` | none |
| Judgment and enforcement | `judgmentDate`, `judgmentAmount`, `litStatus` | none |
| Standard | `state`, `version`, `createdAt`, `createdBy`, `updatedAt`, `updatedBy`, `isActive` | none in the body; they are columns of the template |

The element names are the DF-LEG field names in camelCase; the mapping is one to one and is checked by the drift test. No element exists for a petition beyond this row, because no source gives one.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the document names the element and declares no record field of its own | referred to; the consuming story carries the dependency |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the base of this resource is `/api/recovery/litigation/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route; the resource is reached through it and the contract declares no composite route | referred to; the consuming story carries the dependency |

DP-13 is the pattern this story publishes. DP-03 is named and not declared: the record is the library's and the only trace on the resource is the decision element. DP-19 is the route the two screens use and is the platform edge story's. DP-01 and DP-15 stand behind the DDL template as the schema and migration rules and add no dependency. DP-07 is not in this story's pattern set although two list codes are named; the lists are read as values in force through the reference data of rwb-case, and that read carries no dependency row (GAP-1885; ASM-4687).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| LegalActionOpenApi | Document | The base, the three operations, the schemas, the security, the error set and the versioning section (BR1 to BR6, BR11) |
| LegalActionSchema | Published schema | `LegalActionRequest`, `LegalAction` and `LegalActionUpdate` with the DF-LEG elements, the required set and the petition sub-shape (BR3, BR8) |
| LegalActionDdlTemplate | Resource | The `legal_action` DDL: columns, types, keys, the primary key and the standard columns (BR3, BR9) |
| PetitionElementSet | Published schema | The petition sub-shape and its filing fields, declared once and reused by the create and the patch (BR8) |
| ProblemEnvelope | Reused schema | The platform problem document with the `messageId` extension (BR5) |
| IdempotencyRule | Document | The `Idempotency-Key` header, the repeated-key answer and its counting (BR4) |
| HandOverShapes | Document | The approval request, the case-move announcement and the firm instruction request with the placeholder on the three absent operation names (BR7) |
| Fake set and fixtures | Test asset | The success, refusal, conflict, unavailable and repeated-key answers used by every consuming build (AC7) |
| DriftTest | Test asset | The comparison of a consuming build against sections 11 to 13 (AC7, AC8) |

**Database.** The template creates `legal_action` in `rwb_litigation` only, with the physical types of TSD S4 T3.1 and the standard columns of T3.0. `case_id` and `law_firm_id` are identifiers with no foreign key, and no other schema is named in the template. The template is applied by the service's own Flyway sequence and never edits an applied migration (DP-15). The index set is carried as a gap and the primary key on `id` is the only index declared.

**Configuration and reference data.** The list codes are named and their members are read as values in force with their version (BR3). The capability area and the rights are declared per operation and their role lists are rwb-access data. The problem envelope, its member names and its `messageId` extension are the platform style guide's and are reused, not redeclared.

**Build steps**

1. Write the document with the base and the three operations; lint the paths and the rights (AC1).
2. Write the three schemas with the element mapping, the required set, the enumeration rule and an example; validate the example (AC2).
3. Write the `legal_action` DDL template and apply it twice in two throwaway schemas; assert the columns, the keys, the widths and the absence of a cross-schema key (AC4).
4. Write the error section with the problem envelope and one message ID per condition, and the `Idempotency-Key` rule of the two write operations (AC3).
5. Write the decision element and the three hand-over shapes with their placeholders (AC5, AC6).
6. Write the naming and boundary section and the absence tests for the old base, the second topic and another service's table (AC8).
7. Generate the fake set and the drift test, and wire the drift test into the build of `RWB-S4-E5021-APP` and the sibling S4 stories (AC7).
8. Publish v1 and record the pinned version of this contract and of each consuming story (AC8).

**Feature flag.** `rwb.litigation.legal-action-contract`.

**Done when.** The document lints, the three schemas validate, the template applies twice, the fakes answer every status including the conflict and the repeated key, the drift test is green on the build of this story and of `RWB-S4-E5021-APP`, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Published as | Message |
|---|---|---|---|
| MSG-GEN-001 | A required property is missing, or a value is outside its list (X4) | 422, problem body with `messageId` MSG-GEN-001 and `field` | Enter {field}. |
| MSG-P4-002 | The caller's role does not hold the right of the operation | 403, problem body with `messageId` MSG-P4-002 | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written by the consuming story | 503 on the create, problem body with `messageId` MSG-P7-003 | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the pack, which the pack stories of this service raise, so no path of this document raises it | Not raised here | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | The claim expiry of the case falls inside the filing window, on the consuming story's screen | Not raised here | The claim on this case expires on {date}. File before then. |

The five texts are the legacy wording of RWB-E5-021 section 14 and are copied unchanged; no message is reworded and no message identifier is added. `MSG-GEN-001` is displayed with the property it names. The 400, 401, 404, 409 and the platform 503 carry the platform problem document and no business message of this set, and the 400 code is not named by any S4 T-A row (GAP-1890; ASM-3105). The 409's message text is not stated in any source read for this key, so the document fixes only its status, its cause and its `messageId` slot.

### 15. Screens and states

No screen is built in this story. The contract serves two surfaces read through the gateway-bff composite route (DP-19), and it fixes the answer fields they read and nothing of their layout:

| Screen | State | What the contract serves |
|---|---|---|
| SCR-19 Litigation workspace | Pack | The legal action with `actionType`, `claimAmount`, `courtName` and `status` `OPEN` |
| SCR-19 Litigation workspace | Instructed | The same legal action with the approval reference of the answer and the status `OPEN` |
| SCR-19 Litigation workspace | Filed | The legal action with `filedDate`, `courtName`, `blackCaseNo` and `status` `FILED` |
| SCR-19 Litigation workspace | Hearing | The legal action as the hearing story reads it, with `litStatus` |
| SCR-19 Litigation workspace | Judgment | The legal action with `judgmentDate` and `judgmentAmount` |
| SCR-19 Litigation workspace | Refused | The 403 with MSG-P4-002, and the 409 or 422 of a refused request |
| SCR-19 Litigation workspace | Empty | Not specified in the source documents (CG-ALL-9553) |
| SCR-19 Litigation workspace | Loading | Not specified in the source documents (CG-ALL-9553) |
| SCR-19 Litigation workspace | Error | Not specified in the source documents (CG-ALL-9553) |
| SCR-19 Litigation workspace | No access | Not specified in the source documents (CG-ALL-9553) |
| SCR-20 Enforcement workspace | Requested | The legal action proposed from the enforcement decision of the case |
| SCR-20 Enforcement workspace | Seized | The legal action of the enforcement step, read only |
| SCR-20 Enforcement workspace | Auctioned | The legal action of the auction step, read only |
| SCR-20 Enforcement workspace | Closed | The legal action with `status` `CLOSED` or `WITHDRAWN` |
| SCR-20 Enforcement workspace | Empty | Not specified in the source documents (CG-ALL-9554) |
| SCR-20 Enforcement workspace | Loading | Not specified in the source documents (CG-ALL-9554) |
| SCR-20 Enforcement workspace | Error | Not specified in the source documents (CG-ALL-9554) |
| SCR-20 Enforcement workspace | No access | Not specified in the source documents (CG-ALL-9554) |

The five SCR-19 states and the four SCR-20 states are the ones the legacy screen block of RWB-E5-021 gives, copied unchanged. The empty, loading, error and no access states of both screens are not in the screen specification and are Not specified in the source documents (CG-ALL-9553; CG-ALL-9554). The route path, the screen-model field list and the merge order belong to `RWB-PLT-N001-CON`; the transition behind each state is the app story's, and the case route state that SCR-20 shows is rwb-case's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-021-01 | AC1, AC2 | Contract | The contract half of the petition filing: the create in status `OPEN`, the answer fields, the patch to `FILED` and the `BANKRUPTCY_PETITION` value of `actionType` |
| TC-E5-021-02 | AC1, AC6 | Contract | The contract half of R-LIT-58: the route fact shape of `BANKRUPTCY_PETITION`, the rule ID and version, and the accepted or refused answer |
| TC-E5-021-03 | AC3, AC5 | Contract | The contract half of the not-recorded case: the library element, the 503 with MSG-P7-003 and the refused chain of the stub |
| TC-E5-021-04 | AC3 | Contract | The contract half of the access case: Litigation C, R and U declared per operation, and the 403 with MSG-P4-002 |
| TC-E5-021-05 | AC5, AC7 | Contract | The contract half of the forced-failure case: the stopped chain of the library stub and the drift test on a consuming build |
| TC-S4-E5021-CON-01 | AC1, AC2, AC8 | Contract | The document linted: the base, the three operation IDs, the LegalAction elements, the petition sub-shape, the absence of the old base, of a second topic and of another service's table |
| TC-S4-E5021-CON-02 | AC3 | Contract | One problem body per status on each operation, the six statuses of the TSD rows, the 400 carried as a gap, the rights per operation and the `Idempotency-Key` required on the two writes and refused absent |
| TC-S4-E5021-CON-03 | AC4 | Component | The template applied in two throwaway schemas; DF-LEG-001 to DF-LEG-014, the standard columns, the types, the widths, the primary key and the absence of a cross-schema key asserted; a drifted hand-written table refused |
| TC-S4-E5021-CON-04 | AC5, AC6, AC7 | Contract | The decision element, the approval request and case-move answer shapes with their placeholders, the eight fakes against the document, and a drifted fake failing the build |
| TC-S4-E5021-CON-05 | AC4 | Component | Boundary test of the tables of section 12.7: legal_action with DF-LEG-001 to DF-LEG-014 and the seven standard columns, decision_record and idempotency_key named only, no table of another service declared, read or keyed |

The first five identifiers are the legacy identifiers of RWB-E5-021 in their legacy order, carried here as the **contract half** of each case: they assert the shape each surface needs and not the business outcome, which `RWB-S4-E5021-APP` proves end to end. The four `TC-S4-E5021-CON-*` identifiers are new tests of the artefact. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the list members, the filing window, the bankruptcy test, the index set and the approver route stay data or reference data, and no role code, list value or state member is written in code.
- No personal data in a schema, an example or a fake: identifiers, court references, list values, dates and amounts only.
- The contract names only `rwb_litigation` tables and only operations owned by rwb-litigation; the approval, the case move and the firm instruction are consumed shapes, never provided operations (DP-01, DP-07).
- One base, one topic and one queue per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- No ACE view and no ACE table is declared or read; the court status arrives from LIT through COLLINS and rwb-source-data (DP-05).
- No event, no workflow, no Schedule and no outbox row is declared by this document; the decision record is the library's element (12.3, 12.5, 12.6).
- An absent value is written as the placeholder with its gap and assumption pair and never guessed: the index set, the approval raise operation, the case operation name and the partner operation name.
- Every example in the document is synthetic; no production payload and no production file is copied into a schema or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Contract element | Test cases |
|---|---|---|---|---|---|
| No requirement ID in the legacy master (GAP-1886; ASM-3101) | The petition is recorded as a legal action, taken to the approver and filed through the firm | FEAT-LIT-21 | 08 Litigate and enforce | The three operations, the petition sub-shape, the `legal_action` template and the hand-over shapes | TC-E5-021-01 to TC-E5-021-05, TC-S4-E5021-CON-01 to TC-S4-E5021-CON-04 |
| FEAT-LIT-21 | File a bankruptcy petition | FEAT-LIT-21 | 08 Litigate and enforce | `actionType = BANKRUPTCY_PETITION`, the filing fields and the route fact `BANKRUPTCY_PETITION` | TC-S4-E5021-CON-01, TC-S4-E5021-CON-04 |
| R-LIT-58 | The petition is routed to the approver at D7.5 when enforcement is exhausted and the bankruptcy test is met | FEAT-LIT-21 | 08 Litigate and enforce | The approval request shape and the case-move answer shape | TC-E5-021-02, TC-S4-E5021-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-021, disposition Split (rework) |
| Legacy criteria | AC1, AC2 and AC3 of the legacy story, owned by RWB-S4-E5021-APP; this baseline copies none of them |
| Legacy test cases | TC-E5-021-01 to TC-E5-021-05, carried here as the contract half of each surface |
| Requirement | The legacy master and the Epics 3 to 8 specification carry no REQ identifier for this feature, so both stories trace to FEAT-LIT-21 until the Epics 3 to 8 PRD adds the identifiers (GAP-1886) |
| Screens | SCR-19 Litigation workspace and SCR-20 Enforcement workspace, read through the gateway-bff composite route (DP-19) |
| Sibling slice | RWB-S4-E5021-APP: the evaluation, the row, the approval call, the case announcement, the instruction and the filing |
| Sibling slices of the service | The hearing story (API-S4-005), the notice approval story (API-S4-001), `RWB-S4-E5009-APP` for the firm instruction and `RWB-S4-E5022-APP` for the enforcement proceeds |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership), ADR-022 (local decision record plus central ledger) |

### 19. Out of scope

- The implementation behind the contract — the handlers, the repository, the rule evaluation, the workflow, the activities, the row write and the three calls: `RWB-S4-E5021-APP`.
- The petition state machine, which event moves the legal action and what a refused approval leaves on the row: `RWB-S4-E5021-APP` section 9.
- The approval item, the delegation of authority table and its clock: rwb-decision (P7), `RWB-P7-E2013-CON` and `RWB-P7-E2013-APP`; the operation that raises an item is not published there (GAP-1889).
- The case of record, its route state and its transitions: rwb-case (P3).
- The firm instruction itself, its pack, its lifecycle and the firm's result: `RWB-S4-E5009-APP` and rwb-partner (S9).
- The pack documents and their checklist: rwb-document (P5) and the pack stories of this service, which raise MSG-S4-001.
- The demand and recall notice and its approval (API-S4-001): rwb-comms (P6) and the notice story of this service.
- The hearings of the legal action (API-S4-005, `hearing` DF-LEG-024 to DF-LEG-029): the hearing story of this service.
- The court status that arrives from LIT through COLLINS and rwb-source-data: rwb-source-data (P1) and rwb-integration (P2).
- The decision-record library itself and its chain: `RWB-PLT-E1027-CON`; the central ledger and the rule packages: rwb-decision (P7).
- The roles, rights, scope and masking data themselves: rwb-access (P4).
- The gateway-bff composite route, the screen field list and the layout of SCR-19 and SCR-20: `RWB-PLT-N001-CON` and the edge stories.
- The deployment of this build, the chart values, the schema, the login and the flag: its own OPS story.
- The cross-service proof of the document against the live owners: the wave 3 integration harness.
