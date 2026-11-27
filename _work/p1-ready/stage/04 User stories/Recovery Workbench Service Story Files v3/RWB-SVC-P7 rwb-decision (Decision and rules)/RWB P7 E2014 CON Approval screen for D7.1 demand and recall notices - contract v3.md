# RWB-P7-E2014-CON Approval screen for D7.1 demand and recall notices

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2014-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-014 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P7-E2014-CON-16) |
| Contract version | API Specification v5 (rwb-decision.yaml), base /api/recovery/decision/v1 |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P1-E1015-CON, RWB-P3-E1018-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (FR-P7-019, FR-P7-027, FR-P7-028) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-004, RD-P1-005, RD-P1-041, RD-P1-062 |

**Version 3 changes.**

- RD-P1-004, RD-P1-062: Align the Error and Message Standard v6 wording.
- RD-P1-062: Use prior bank business-day freshness fixtures and fail the age check when no stamp exists.
- RD-P1-005 and RD-P1-041: the consumed freshness row states the status values, the stamp in use and the never-stamped answer.
- A never-stamped product has no input age and the age check refuses approval (RD-P1-062).

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the approval screen for RWB-E2-014 in rwb-decision — the composite route of the screen, its panels, its field list and mask flags, the P7 operations it consumes, the screen state values, the notice summary shape, the paging and filter parameters, the error envelope, the fakes and the drift test. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (11 resolved, 23 cross-document, 11 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3 aligns the story with RD-P1-005, RD-P1-041. Tool: Claude Code / Claude Sonnet 5.5.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the D7.1 approval screen — the composite route served by gateway-bff with its panels, its field list and its mask flags; the five rwb-decision operations on `/api/recovery/decision/v1`; the screen state values; the notice summary shape; the paging and filter parameters; the error envelope and its message IDs; the nine contract tables and the four contract fakes** so that **the app story of this key builds against a frozen, testable contract on Day 1 and a field, a mask flag, a state value, a parameter or a message code can never drift between rwb-decision, rwb-comms, rwb-source-data, rwb-case and the platform route without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020), and a screen is the hardest place to keep it: the legacy story read the approval, the notice, its template version, the case number, the ACE balance and the contact value inside one process, in one transaction, and could change any of them without telling anybody. In the target the screen is composed at the edge and each of those facts has exactly one owner (Architecture v5 slides 14, 17, 20 and 41; DP-19).

The baseline fixes what the five parties have to agree before any of them builds. The route name, the two panels, the field list and the mask flags, because the browser renders one model and three owners produce it. The five P7 operations and their status codes, because the three decisions carry an `Idempotency-Key` and a refusal that is decided twice must not be written twice. The screen state values, because Ready, Stale input and Decided are what the officer acts on and they must mean the same thing in the route and in the service. The notice summary, because the notice body, its addressee and its account number stay in rwb-comms and only identifiers, codes and dates may cross the boundary. The paging and filter parameters, because the approval queue is read with a decision, a product and a page. The error envelope and its message IDs, because six of them are the business rules of the legacy story and their text is agreed.

It also fixes the naming the checks require: schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1`, event names `rwb.decision.<Event>.v1`, the shared record topic `rwb.decision-record.v1`, task queue `rwb-decision` in namespace `rwb-recovery`, and Java package `th.co.scb.ace.workbench.recovery.decision`. A screen composite adds the platform's public base `/api/recovery` with no service segment and no `/v1`, which is the edge's and not this service's (DP-13, DP-19).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the schema, topic, event and path names follow the platform rule rather than a local choice.
- The platform route contract is published (RWB-PLT-N001-CON): the public base `/api/recovery` with no service segment and no `/v1`, the opaque session cookie with a 15-minute idle, the coarse permission, the 2 s budget per downstream and the RFC 9457 problem envelope. This document narrows that baseline for one screen and never redefines it.
- The platform envelopes — the error envelope, the CloudEvents 1.0 envelope and the retry and `.dlt` topic convention — are the baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON).
- The notice contract of RWB-P6-E1052-CON is published, because the notice summary this baseline fixes is a narrowed view of that answer.
- The decision record library and its topic are published (RWB-PLT-E1027-CON), so the `DecisionRecorded` envelope of 12.3 is the library's and not a new design.
- The operations and their owners are taken from the Ownership Map only; this document never declares another service's operation as provided.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).
- No production data is used in any example, schema or fake; every notice, case, template, user and workspace key is synthetic.

### 4. Flow

1. Draft the OpenAPI 3.1 fragment of the screen composite: one public route, the two panels, the screen model and the field list.
2. Declare the mask flag of every field against the masking policy the route applies, and prove that no field can carry a raw personal value.
3. Declare the five P7 operations the screen consumes on base `/api/recovery/decision/v1`, with their bodies, answers, access rights and error statuses.
4. Fix the screen state values and the mapping from the approval status list of LOV-APPROVAL-STATUS and the notice state of the notice answer.
5. Fix the notice summary element list as identifiers, codes and dates only, and prove that no notice body, addressee, account number or merge value is declared.
6. Fix the paging and filter parameters of the queue read.
7. Map every failure to the error envelope and one message ID, one condition per row, and keep the owner's message identifier and detail through the route.
8. Record the one published event envelope and the four fakes; publish the nine contract tables.
9. Add the contract tests: schema validation, the mask rule, the state enumeration, the notice summary scan, the parameter shapes, the error mapping, the fake drift and the absence of a monolith path.
10. Tag the baseline and hand it to RWB-P7-E2014-APP, RWB-P7-E2014-OPS, the routing story RWB-P7-E2013-APP, the notice stories of RWB-P6-E1052-CON and the platform route story RWB-PLT-N001-APP.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response or request body fails schema validation | The build fails on the schema lint; a deployed route answers the problem envelope and a malformed request answers 422 | MSG-GEN-001 | AC1, AC7 |
| X2 | A field is renamed, removed or retyped within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC3 |
| X3 | A screen state value is added or removed | The enumeration test fails, and the change is a new major version of the screen model | None | AC4 |
| X4 | A field appears without a mask flag, or a raw personal value appears in an example | The mask test fails the build and names the field | None | AC2, AC5 |
| X5 | The notice summary declares a body, an addressee, an account number or a merge value | The scan fails the build and names the element | None | AC5 |
| X6 | A contract fake drifts from the document, or a fake answers a field the document does not declare | The drift test fails the build and the merge is blocked | None | AC8 |
| X7 | A retired element reappears: a monolith base, a data-lake extract or a second topic | The absence test fails | None | AC8 |
| X8 | A value is missing from the source material | The element carries the placeholder and one gap row | None | AC1, AC4, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform route and envelope contracts, the notice contract of the same wave and the Ownership Map only |
| Negotiable | Field-level detail and the mask policy keys are settled with the route owner and the consumers; the operations, the state values, the message IDs and the event name are fixed by the target architecture and the legacy story |
| Valuable | Unblocks the app and deployment stories of this key and the notice and route owners on Day 1 |
| Estimable | One document fragment, one public route, five operations, nine contract tables, four fakes and eight contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the D7.1 approval screen

  Background:
    Given the service naming rule of the platform library is in force
    Given the rwb-decision REST base is /api/recovery/decision/v1 and its topic is rwb.decision.events.v1
    Given the gateway-bff public base is /api/recovery with no service segment and no /v1
    Given no production data is used in any example, schema or fake

  Scenario: AC1 The composite route declares its route name, its two panels and its field list (new, D-RCV-60)
    Given the OpenAPI 3.1 fragment of the approval screen is published with this change
    When it is validated and linted
    Then it declares one public route for the screen on the public base /api/recovery, one hop to rwb-decision, rwb-comms and rwb-source-data and never a chain
    Then the route carries the name of the legacy screen pair SCR-11 and SCR-18, and the exact route name and path segment are Not specified in the source documents (GAP-1259; ASM-2223)
    Then it declares two panels, the decision panel for SCR-11 and the notice approval panel for SCR-18, each with its own field list
    Then the decision panel field list is approvalId, caseId, caseNo, decisionCode, approvalStatus, routeRoleCode, dueAt, escalationLevel, preparedBy, productGroup, ruleId, ruleVersion, noticeId, noticeType, noticeState, templateId, templateVersion, documentId, inputFacts and postalAddress
    Then every field names the operation it comes from and its owner, and no field is invented at the edge
    Then inputFacts is a list with inputCode, businessDate, ageDays, limitDays and stale, one element per input the notice was built from
    Then the route declares no field of its own beyond the two panels, and the route table, the document and the fake carry the same list

  Scenario: AC2 Every field carries a mask flag and no field can carry a raw personal value (new, D-RCV-60)
    Given the field list of the two panels
    When the mask flag of every field is compared with the masking policy of the route
    Then every field declares a mask flag of NONE, PARTIAL or FULL and a policy key, and no field declares no flag at all
    Then postalAddress declares PARTIAL with the postal-address policy key, and caseNo, preparedBy and noticeId declare NONE because they are identifiers and codes
    Then the document states that the masking itself is applied by the route with the policy of rwb-access and that this baseline fixes the flag, not the policy text
    Then the field list that carries a mask flag is itself Not specified in the source documents beyond the legacy screen (GAP-1269; ASM-2233)
    Then no example carries a name, an e-mail address, a full address, an account number or a national identifier
    Then a raw personal value in any example fails the build and names the field and the sink

  Scenario: AC3 The five P7 operations the screen consumes are declared (new, D-RCV-60)
    Given the fragment of the screen route and its consumed operations
    When each operation is compared with Appendix T-A of the module specification and the Ownership Map
    Then the screen consumes GET /approvals, GET /approvals/{approvalId}, POST /approvals/{approvalId}/approve, POST /approvals/{approvalId}/return and POST /approvals/{approvalId}/refuse on base /api/recovery/decision/v1
    Then the three decisions declare the Idempotency-Key header as required and the two reads declare none
    Then every operation declares right A of the decision log capability area with the scope applied and the error responses 401, 403, 404, 409, 422 and 503
    Then the decision body is ApprovalAction with reason, reasonCode and changes.templateCode, and the answer of the two approving operations is the decision log entry
    Then no other service's operation is declared as provided by rwb-decision

  Scenario: AC4 The screen state values are enumerated and mapped to the approval status and the notice state (new, D-RCV-60)
    Given the screen state element of both panels
    When its values are compared with the legacy screens and with LOV-APPROVAL-STATUS
    Then the decision panel declares READY, STALE_INPUT and DECIDED, and the notice approval panel declares GENERATED, APPROVED and HELD
    Then the document states that the legacy labels Ready, Stale input and Decided are the display names of the three shell states and that no other shell state is declared by this baseline
    Then the mapping states that approvalStatus carries WAITING, HELD_NO_LIMIT, APPROVED, REFUSED or RETURNED as reference data, and that a REFUSED outcome holds the notice with REFUSED_BY_APPROVER
    Then the route states loading, temporarily unavailable and session expired are declared as the platform route's and not as screen states of this baseline
    Then the two readings are reconciled in the document, because the legacy screens declare three shell states and the route declares its own (GAP-1267; ASM-2231)
    Then no state value is written in code: every one is read from reference data or from the route baseline

  Scenario: AC5 The notice summary carries identifiers, codes and dates only (new, D-RCV-60)
    Given the notice summary declared in the fragment of the notice approval panel
    When it is compared with the notice answer of RWB-P6-E1052-CON and with the legacy screen
    Then it carries noticeId, caseId, noticeType, noticeState, templateId, templateVersion, documentId and generatedAt, and nothing else
    Then it carries no notice body, no addressee, no account number, no merge value, no name and no postal address
    Then documentId is a reference and the PDF itself is served by rwb-document at the route and never carried in this summary
    Then the document states that the addressee role and the masked postal address the legacy screen shows are screen fields of the decision panel owned by rwb-source-data and not elements of the notice summary, because the notice answer carries no addressee (GAP-1268; ASM-2232)
    Then a scan of the summary schema and of every example finds no personal value

  Scenario: AC6 The paging and filter parameters of the queue read are fixed (new, D-RCV-60)
    Given the queue read of the decision panel
    When its query parameters are compared with the module specification
    Then it declares decision, product, page and size, and decision is fixed to D7.1 for this screen
    Then page and size are integers, size carries a maximum, and a request beyond the maximum or below zero answers 422 with MSG-GEN-001 naming the parameter
    Then the answer is a page of approvals with the total count and the page parameters echoed, and no full approval body in the list
    Then the page size default and maximum are Not specified in the source documents (GAP-1266; ASM-2230)
    Then the route adds no filter of its own and narrows no parameter

  Scenario: AC7 The error envelope maps one message ID per condition (new, D-RCV-60)
    Given the error responses declared for the route and for the five operations
    When each condition is compared with the message catalog
    Then every error is RFC 9457 problem details with the status, the message identifier and the detail, and no second envelope is introduced
    Then 401 answers a missing or expired session, 403 answers MSG-P4-002 when the role lacks the right, and 404 answers MSG-P4-003 when the approval is absent or out of the caller's scope
    Then 409 answers MSG-P7-002 for the preparer, MSG-P7-006 for a stale input, MSG-P6-003 for a withdrawn template and MSG-GEN-004 for a decision already taken
    Then 422 answers MSG-GEN-001 for a missing reason or a bad parameter and MSG-P7-005 for a change of variant without a coded reason
    Then 503 answers MSG-P7-003 for a record that cannot be written, MSG-GEN-006 for a consumed call beyond its budget, and the route's own temporarily-unavailable problem
    Then the owner's message identifier and detail pass through the route unchanged, and no condition maps to two message IDs

  Scenario: AC8 The nine contract tables are complete, the four fakes match them and the drift test is green (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed and the contract tests are run
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then 12.1 names the public route with owner PLT and the five operations with owner P7, and 12.7 records None because this baseline owns no table
    Then the rwb-comms, rwb-source-data, rwb-case and route fakes answer the paths and payloads of 12.2 and the shapes of 12.1, each with a delayed answer beyond 2 s
    Then the drift test compares each fake with the document and fails on any drift
    Then the absence test finds no monolith base, no data-lake extract and no topic other than rwb.decision.events.v1 and rwb.decision-record.v1
    Then the document states that schema rwb_decision, REST base /api/recovery/decision/v1, topic rwb.decision.events.v1, queue rwb-decision in namespace rwb-recovery and package th.co.scb.ace.workbench.recovery.decision are the names of this service, and that the public base belongs to the edge
```

These eight criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by RWB-P7-E2014-APP. The ten legacy criteria of RWB-E2-014 are owned by RWB-P7-E2014-APP and are not copied here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/decision/v1`; a public screen path is the edge's and carries no service segment and no `/v1` | DP-13; Architecture v5 slides 10 and 41 |
| BR2 | Event names are `rwb.<short>.<Event>.v1` on the topic `rwb.<short>.events.v1`, and the decision record leaves on `rwb.decision-record.v1` | DP-03, DP-14; Template and Rules §R4 |
| BR3 | Every event carries the CloudEvents 1.0 envelope, is keyed by caseId, is written to the outbox in the same transaction as its state change and carries no personal data | Architecture v5 slides 42 and 43 notes; DP-09 |
| BR4 | A read declares no Idempotency-Key; a POST declares it and stores its answer | Architecture v5 slide 11; DP-09 |
| BR5 | Error responses use one envelope and one message ID per condition, and the owner's identifier and detail pass through the route unchanged | Architecture v5 slides 10 and 11 |
| BR6 | A schema change is additive within a major version; a breaking change is a new major version | Architecture v5 slide 42 notes |
| BR7 | The document lists only operations owned by rwb-decision as provided; a consumed operation is described as consumed, never as provided | Ownership Map v1 |
| BR8 | The notice summary carries identifiers, codes and dates only: no notice body, no addressee, no account number and no merge value | RWB-P6-E1052-CON BR8; NFR-040; Template and Rules §R7.2 s17 |
| BR9 | Every field of the screen model declares a mask flag, and the mask is applied by the route with the policy of rwb-access; no raw personal value crosses the edge | Architecture v5 slide 35; DP-19 |
| BR10 | The screen state values and the approval status values are reference data or route baseline, never constants written in code | TSD P7 v2 T3.2; DP-07 |
| BR11 | The decision record is published by the local library on the shared topic and is never a new event of this service | DP-03; Architecture v5 slide 20 |
| BR12 | No workflow, no Schedule and no job element is declared by this baseline | DP-10; Architecture v5 slides 14 and 44 |
| BR13 | No business value is fixed in the contract: age limits, override reasons, template codes, route role codes, page sizes and timeouts stay data or service configuration | Template and Rules §R7.2 s17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The route, the two panels, the field list, the five operations, the states and the error mapping are described | In review |
| In review | Consumer sign-off | RWB-P7-E2014-APP, RWB-P7-E2014-OPS, RWB-P7-E2013-APP, the notice owner and the route owner accept the document and the fakes | Baselined |
| Baselined | Additive change | A field or an optional element is added within major version 1 | Baselined |
| Baselined | Breaking change | A field, a state value or a path is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | Retired element reappears | The absence test of AC8 fails | In review |

The screen state machine itself — READY, STALE_INPUT and DECIDED, and the panel states GENERATED, APPROVED and HELD — is declared by AC4 and is written by RWB-P7-E2014-APP and the route, not by this baseline.

### 10. Authority

The letters below are taken from the rwb-decision right of TSD P7 v2 T6.1, from Appendix T-A of the same specification and from the legacy authority table, and from no other table.

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-decision | Owns the OpenAPI fragment, the fakes and the baseline tag |
| Solution architect | Approves a breaking change, a new major version and the correction of an Ownership Map row |
| Platform route owner | Owns the public base, the session, the masking engine and the budget the fragment reuses; reviews the route and the mask flags |
| Notice owner (rwb-comms) | Reviews the notice summary and confirms that no body, addressee or merge value is carried |
| Source-data owner (rwb-source-data) | Reviews the account and contact fields and their mask flags |
| Case owner (rwb-case) | Reviews the case number field and the case-owner task row |
| RW-LITOFF, litigation officer | Approves, changes or refuses D7.1 notices they did not prepare: the role the baseline names on the five operations |
| RW-LEGAL, legal counsel | Holds the template approval the notice summary depends on, and decides D7.1 notices they did not prepare |
| RW-CASEOWN, case owner | Receives the refused notice task; reads the screen of the case with Litigation R |
| Data steward | Confirms that no personal data field is declared in the summary, the events or the examples |

The per-service login behind the operations is not part of this baseline; the document names the scheme "the rwb-decision login (DP-02)". The authorisation decision is enforced at the route and at the service under RWB-PLT-N001-CON and RWB-P4-E1037-CON and is not redeclared here.

### 11. Data

The contract baseline declares shapes, not business values. Until the baseline reviews publish the shapes, the case-facts projection, the two approval outcome event names, the redress task naming and the postal address business date are Not specified in the source documents (GAP-2216), and no behaviour is renamed if the published shapes differ.

| BR Field ID | Item | Content |
|---|---|---|
| Not specified in the source documents (DOR-RWB-P7-E2014-CON-7) | Decision panel model | approvalId, caseId, caseNo, decisionCode, approvalStatus, routeRoleCode, dueAt, escalationLevel, preparedBy, productGroup, ruleId, ruleVersion, noticeId, noticeType, noticeState, templateId, templateVersion, documentId, inputFacts, postalAddress; the exact type and order of each field beyond the names of the legacy screen are Not specified in the source documents (GAP-1266; ASM-2230) |
| Not specified in the source documents (DOR-RWB-P7-E2014-CON-7) | Notice approval panel model | noticeId, noticeState, noticeType, templateId, templateVersion, documentId, generatedAt and the input facts the notice was built from; no body and no addressee in the notice summary; the notice PDF is served at the route from documentId through rwb-document, and the addressee and the masked postal address come from the rwb-source-data fields of the decision panel |
| Not specified in the source documents (DOR-RWB-P7-E2014-CON-7) | inputFacts element | inputCode, businessDate, ageDays, limitDays and stale, one element per input; the input codes are the two the parameters name, TOTAL_BALANCE and POSTAL_ADDRESS, and no other code is declared |
| Not specified in the source documents (DOR-RWB-P7-E2014-CON-7) | Mask flags | NONE, PARTIAL and FULL with a policy key per field; the flag of every field is declared, the policy text is the route's |
| Not specified in the source documents (DOR-RWB-P7-E2014-CON-7) | Event payload | The decision record's elements only, with identifiers, codes and dates |
| Not specified in the source documents (DOR-RWB-P7-E2014-CON-7) | Error body | The status, the message identifier and the detail of the platform envelope; no case fact |

### 12. Contract

#### 12.1 REST operations provided

The public route is the platform's; the five operations are rwb-decision's. Base `/api/recovery/decision/v1` for the operations and `/api/recovery` for the public route.

| ID | Method | Path | Documented shape | Access |
|---|---|---|---|---|
| Route of the approval screen | GET | `/api/recovery/approvals/{approvalId}` | Composed answer with the two panels, the screen model and the states of AC4; errors 401, 403, 404, 503 | Session cookie; coarse permission at the edge; owner PLT |
| API-P7-002 | GET | `/approvals` | Query decision, product, page, size; answer a page of approvals with the total count; errors 401, 403, 503 | Decision log, right A, scope applied; no `Idempotency-Key` |
| API-P7-008 | GET | `/approvals/{approvalId}` | No body; answer the approval with its routing details; errors 401, 403, 404, 503 | Decision log, right A, scope applied; no `Idempotency-Key` |
| API-P7-003 | POST | `/approvals/{approvalId}/approve` | Body ApprovalAction; answer the decision log entry; errors 401, 403, 404, 409, 422, 503 | Decision log, right A, scope applied; `Idempotency-Key` required |
| API-P7-004 | POST | `/approvals/{approvalId}/return` | Body ApprovalAction; answer the approval; errors 401, 403, 404, 409, 422, 503 | Decision log, right A, scope applied; `Idempotency-Key` required |
| API-P7-005 | POST | `/approvals/{approvalId}/refuse` | Body ApprovalAction; answer the decision log entry; errors 401, 403, 404, 409, 422, 503 | Decision log, right A, scope applied; `Idempotency-Key` required |

The public route is `GET /api/recovery/approvals/{approvalId}` as the working read of AC1, and its exact path segment is Not specified in the source documents (GAP-1259; ASM-2223). The field-level types and the order of the model are Not specified either (GAP-1266; ASM-2230); the baseline carries the working read and is corrected by a new version when the register closes the point.

#### 12.2 REST operations consumed

| Method and path | Owner | Use in the baseline |
|---|---|---|
| GET `/api/recovery/comms/v1/notices/{noticeId}` | P6 rwb-comms, RWB-P6-E1052-CON | The notice summary of 12.1 and AC5 |
| POST `/api/recovery/decision/v1/approvals/{approvalId}/approve`, `/return`, `/refuse` | P7 rwb-decision | The three decisions of the decision panel; the baseline fixes their bodies and answers; `Idempotency-Key` required on each |
| GET `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data, DP-05 | The total balance and the postal contact value with `data_as_of`; no C row for this contract exists in this key (GAP-1266; ASM-2230) |
| GET `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data, DP-05 | The business date behind `inputFacts`; with the same gap (GAP-1266; ASM-2230). The answer is `DataProductFreshness` of rwb-source-data.yaml 5.1.0: `status` is `LOADED` or `STALE` and the row is the stamp in use (the latest stamped business date); a product never stamped answers `STALE` with `businessDate` null (RD-P1-005, RD-P1-041). A never-stamped product has null `staleSince` and no source timestamps. Omit `X-Data-As-Of`, show the stale banner, keep `data_as_of` and input age null, and fail the age check (RD-P1-062). |
| GET `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case number of the screen header, read at the route; no C row for this contract exists in this key (GAP-1266; ASM-2230) |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (AC7, DP-11, ADR-020). The baseline fixes no field name inside the owner answers beyond the elements listed in 12.1 and AC5.

#### 12.3 Events published

| Event | Topic | Owner | Schema element |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (event 08) | `rwb.decision-record.v1` | P7 rwb-decision | decision code D7.1, rule ID and version, template code and version, approver identifier, final call, inputs reference, decided at, record reference; key caseId; written to the outbox in the same transaction as the approval and the entry; published by the local decision-record library (DP-03) |

This baseline declares the envelope because the screen depends on it; the decision record is written by RWB-P7-E2014-APP through the library. `ApprovalRequested` (event 09) is published by RWB-P7-E2013-APP on routing and is not declared as an output of this screen. `ApprovalDecided` is named on the slide 14 contract line and has no row in the event catalogue of slides 42 and 43, so no envelope is declared for it here.

#### 12.4 Events consumed

None. The routing listener of `rwb.comms.NoticeGenerated.v1` is RWB-P7-E2013-APP's, and the screen reads the current state of the approval and the notice on the two reads of 12.2.

#### 12.5 Workflows and activities

None in this baseline. `ApprovalWorkflow` of the workflow kit is started by RWB-P7-E2013-APP and is signalled by RWB-P7-E2014-APP; the baseline declares no workflow element, no activity name and no timer, and its contract is fixed in RWB-P7-E2013-CON (DP-10).

#### 12.6 Schedules

None. The two Schedules of the service — the rule promote at 00:01 (JOB-20) and the hash-chain check at 02:00 (JOB-14) — belong to the rule registry story and the decision log store story, and this baseline declares no Schedule and reads no shared scheduler table (DP-10).

#### 12.7 Tables owned

None. This baseline owns no table: it declares the shapes of the screen and fixes the two the app story writes. `approval` and `decision_log_entry` are P7 rows in `rwb_decision` and are written by RWB-P7-E2013-APP and RWB-P7-E2014-APP; `notice`, `template` and `merge_field` are P6 rwb-comms'; `delegation_limit` is P4 rwb-access'; `parameter_catalog`, `reference_row` and `lov_value` are P3 rwb-case'; `recovery_case`, `task` and `timer` are P3 rwb-case'. None of them is declared as owned here and none is read directly (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| Route fake of the screen | The public route with both panels, the full field list and its mask flags, the three shell states and the three panel states, the 401, 403, 404 and 503 examples, and the temporarily-unavailable example | App story, deployment story, front end |
| rwb-comms notice fake (RWB-P6-E1052-CON) | Notice "N-0201" for case "RW-2026-000123" from template "DEMAND-MTG" "TH" version 2 in state Generated, under rule "R-LIT-03" version "LIT-2026.12", prepared by "U-9211"; the same notice Approved; the variant "DEMAND-MTG-B"; the withdrawn version 2; a delayed answer beyond 2 s | App story, contract tests |
| rwb-source-data fake | The total balance with `data_as_of` 2026-12-11 for LOADED, 2026-12-10 with `staleSince` 2026-12-11 for STALE, and null date and staleSince for never stamped, the postal address of the case masked, and the freshness row; a delayed answer beyond 2 s | App story, contract tests |
| rwb-case fake | Case "RW-2026-000123" with product group "MORTGAGE" and the case-owner task raise; a delayed answer beyond 2 s | App story, contract tests |

The values are the legacy values of RWB-E2-014 section 7, kept unchanged so the component and integration assertions read the same fixtures.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 public route and 5 operations provided, 5 consumed | The route under `/api/recovery` with owner PLT; API-P7-002, API-P7-003, API-P7-004, API-P7-005 and API-P7-008 with owner P7; the notice read, the two data-product reads and the case read consumed; one hop, 2 s |
| Kafka | 1 declared as published by its owner | `DecisionRecorded` on `rwb.decision-record.v1`; no event on `rwb.decision.events.v1` belongs to this screen |
| Temporal | None | `ApprovalWorkflow` belongs to RWB-P7-E2013-CON and is signalled by the app story |
| File | None | No file element; the notice PDF is a document reference served at the route |

### 13. Solution plan

**Deliverables.** The additive change to the gateway-bff route document for one screen, the OpenAPI fragment of the five rwb-decision operations, the decision panel and notice approval panel components with their field list and mask flags, the contract README rows for the state values, the parameter shapes, the error mapping and the mask rule, the four WireMock mapping sets, and the drift and absence tests.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_decision`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/decision/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-19 is the pattern this baseline exists for: the screen is the route, the route is the platform's, and the five operations and the notice summary behind it are the owners'. No pattern is claimed for DP-02, DP-04, DP-08, DP-12, DP-14, DP-15, DP-16, DP-17, DP-18 or DP-20: this baseline declares no login, no rule package, no authorise call, no case workflow, no renamed topic, no migration, no integration adapter, no lake extract, no ledger entry and no agent client.

**Build steps**

1. Write the route and the two panels with the field list of AC1, and the lint rule that the field list, the route table and the fake agree.
2. Add the mask flag of every field and the example scan of AC2; a field without a flag fails the build.
3. Declare the five operations with their bodies, answers, rights, `Idempotency-Key` and error statuses; test the enumeration of AC3.
4. Fix the screen states and the mapping of AC4, and the parameter shapes of AC6 with the 422 path.
5. Fix the notice summary of AC5 and add the scan that fails on a body, an addressee, an account number or a merge value.
6. Write the error mapping of AC7 as one row per condition with its message ID, and assert the pass-through of the owner's identifier and detail.
7. Publish the four fakes and the drift test of AC8; a drift between a fake and the document fails the build.
8. Add the absence test: no monolith base, no data-lake extract and no topic other than `rwb.decision.events.v1` and `rwb.decision-record.v1`.
9. Baseline tag and the consumer sign-off note, including the app and deployment stories of this key, the routing story, the notice owner and the route owner.

**Done when.** The documents validate in the pipeline, the eight contract tests pass, the four fakes answer every consumed path and every example, the drift and absence tests are green, no personal value appears in an example or a payload, and the app and deployment stories of this legacy key have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-002 | The preparer opens or acts on the item | You prepared this decision, so you cannot approve it. |
| MSG-P7-006 | An input is past its age limit | {input} is {days} days old, past its limit. Refresh it before you decide. |
| MSG-P6-003 | The template was withdrawn and the notice is held | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P7-005 | Change of variant without a coded reason | Enter the reason you are not following the recommendation. |
| MSG-GEN-001 | A required field or query parameter is missing or invalid | Enter {field}. |
| MSG-GEN-004 | Another approver decided first | Someone else changed this record. Reload it to see their change. |
| MSG-P7-004 | Approved | Approved. The case moves to {state}. |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The role lacks the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The approval is not on the case, or the case is outside the caller's scope | This case is not in your scope. |
| MSG-P4-001 | No Workbench role on the token | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-GEN-006 | A consumed call does not answer in time | {system} is not available. Try again in a few minutes. |

MSG-P7-002, MSG-P7-006, MSG-P6-003, MSG-P7-005, MSG-GEN-001, MSG-GEN-004, MSG-P7-004 and MSG-P7-003 are copied from RWB-E2-014 section 14 unchanged; MSG-P4-002, MSG-P4-003, MSG-P4-001 and MSG-GEN-006 are the platform message catalog's. The message IDs are contract elements and their text is the agreed text; the edge's own problem titles and details are the platform route's and are not fixed here.

### 15. Screens and states

The baseline serves the pair SCR-11 Decision screen and SCR-18 Notice approval, reached from SCR-10 Approval queue:

| Screen | What it reads from this contract | State |
|---|---|---|
| SCR-10 Approval queue | The page of approvals of API-P7-002 with the decision, product and page parameters | The route's loading and loaded states; empty, error and no access: Not specified in the source documents (CG-ALL-7204) |
| SCR-11 Decision screen | The decision panel of the route: the approval, the case number, the product group, the rule and its version, the preparer, the due time and the input facts with their ages | READY, STALE_INPUT, DECIDED; empty, loading, error and no access: Not specified in the source documents (CG-ALL-7205) |
| SCR-18 Notice approval | The notice approval panel: the notice, its type, its template code and version, its state and its document reference | GENERATED, APPROVED, HELD; empty, loading, error and no access: Not specified in the source documents (CG-ALL-7206) |

The field-level masking, the session states and the temporarily-unavailable state of the route belong to RWB-PLT-N001-CON and are declared as the route's in AC4; this baseline fixes the flags and the panel fields and nothing else. The route name, its path segment and the field list beyond the legacy screen are Not specified in the source documents (GAP-1259; ASM-2223).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P7-E2014-CON-01 | AC1 | Contract | The route document validated and linted; one public route, two panels, the field list, one hop per owner and no chain |
| TC-P7-E2014-CON-02 | AC2 | Contract | The mask flag of every field; the postal address PARTIAL; the example scan over both panels |
| TC-P7-E2014-CON-03 | AC3 | Contract | The five operations compared with Appendix T-A and the Ownership Map; the `Idempotency-Key` rule; the error statuses |
| TC-P7-E2014-CON-04 | AC4 | Contract | The state enumeration and the mapping to LOV-APPROVAL-STATUS and to the notice state; the legacy labels |
| TC-P7-E2014-CON-05 | AC5 | Contract | The notice summary schema and every example scanned for a body, an addressee, an account number and a merge value |
| TC-P7-E2014-CON-06 | AC6 | Contract | The four query parameters, the maximum and the 422 path for a bad page or size |
| TC-P7-E2014-CON-07 | AC7 | Contract | The problem schema and the 401, 403, 404, 409, 422 and 503 examples; the pass-through of the owner's identifier |
| TC-P7-E2014-CON-08 | AC8 | Component | The four fakes over the route and the owner answers; the drift test; the absence test for the monolith base and the lake |

### 17. Guardrails

- No business value in the contract: age limits, override reasons, template codes, route role codes, product groups, page sizes and timeouts stay data, reference data or service configuration.
- No personal data in a schema, an example or a fake: identifiers, codes, dates and a document reference only; no name, no address, no account number and no notice body.
- Every field of the screen model declares a mask flag, and the mask itself is the route's with the policy of rwb-access; no raw personal value crosses the edge.
- The contract names only operations owned by rwb-decision as provided and only the one public route as the edge's; every other operation is consumed and faked (DP-01, DP-07).
- One base, one topic and one queue for the service, and the public base without a service segment for the edge; a document that mixes the two fails the review (DP-13, DP-19).
- ACE data is reached only through the owner's contract; this document declares no ACE view and no cross-schema join.
- The decision record is a local record on the shared topic and never a new event of this service (DP-03).
- No retired element is reintroduced: the absence test fails a build that declares a monolith base, a data-lake extract or a third topic.
- Every example is synthetic; no production payload is copied into a schema or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-APD-002 | Recommendation, reasons, inputs and limit on one screen | The decision panel, its field list, the input facts and the mask flags | TC-P7-E2014-CON-01, TC-P7-E2014-CON-02, TC-P7-E2014-CON-05 |
| REQ-APD-006 | Demand and recall notices approved through approval routing | The five operations, the screen states and the error mapping | TC-P7-E2014-CON-03, TC-P7-E2014-CON-04, TC-P7-E2014-CON-07 |
| RWB-E2-014 | The legacy key whose contract this baseline fixes | The eight criteria of section 7 | TC-P7-E2014-CON-01 to TC-P7-E2014-CON-08 |
| DP-01 | Owner's schema; no service reads another service's tables | The owned and not-owned lists of 12.7 | TC-P7-E2014-CON-08 |
| DP-03 | Local decision record and the shared topic | The `DecisionRecorded` row of 12.3 | TC-P7-E2014-CON-08 |
| DP-05 | ACE data through rwb-source-data's contract | The two source-data rows of 12.2 | TC-P7-E2014-CON-01, TC-P7-E2014-CON-05 |
| DP-07 | Reference data through rwb-case's contract | The enumerated status values of AC4 | TC-P7-E2014-CON-04 |
| DP-11 | REST contract with mock, one hop, 2 s | The five consumed rows and the four fakes of 12.8 | TC-P7-E2014-CON-03, TC-P7-E2014-CON-07 |
| DP-13 | Per-service REST base | `/api/recovery/decision/v1` | TC-P7-E2014-CON-03 |
| DP-19 | Screen through the gateway-bff composite route | The public route and the two panels of 12.1 | TC-P7-E2014-CON-01, TC-P7-E2014-CON-02 |
| ADR-013 | 19 services inside ACE | The boundary of 12.7 | TC-P7-E2014-CON-08 |
| ADR-019 | Edge: gateway-bff and the partner gateway | The public route with no service segment | TC-P7-E2014-CON-01 |
| ADR-020 | Contract-first REST, one hop, 2 s | The 2 s budget and the error mapping of AC7 | TC-P7-E2014-CON-07 |

### 19. Out of scope

- The implementation of the screen, the checks, the notice calls and the record path: RWB-P7-E2014-APP.
- The deployment, the route registration, the dashboards, the alerts and the run book: RWB-P7-E2014-OPS.
- The routing of a generated notice, the approval level matrix and the DoA table read: RWB-P7-E2013-APP and RWB-P7-E2013-CON, with the DoA table owned by rwb-access (P4).
- The decision log store, the writer and the audit query: RWB-P7-E1008-CON, RWB-P7-E1027-CON and RWB-P7-E2005-CON.
- The gateway-bff route baseline itself, the session, the masking engine and the push: RWB-PLT-N001-CON and RWB-PLT-N001-APP.
- The notice, its template version and the three notice operations: RWB-P6-E1052-CON and its app story, consumed here.
- The ACE account and contact data products: RWB-P1-E1015-CON and its app story, consumed here.
- The case number, the case-owner task and the case scope: the rwb-case contract, consumed here.
- The legacy criteria themselves and the twelve legacy test cases: RWB-P7-E2014-APP.
- The Thai text of the messages, the screen layout and the component library: DL10 and the Workbench Design System.
