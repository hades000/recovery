# RWB-P7-E2013-CON Approval routing with the delegation of authority table

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2013-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement |
| Patterns applied | DP01, DP03, DP06, DP07, DP08, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None (platform contracts of the DP table are delivery prerequisites, not per-story blockers) |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P4-E1037-CON (published contracts; platform contracts of the DP table are delivery prerequisites) |
| Contract version | v1 (base path `/api/recovery/decision/v1`) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (FR-P7-017, FR-P7-018, FR-P7-020, FR-P7-021, FR-P7-022, FR-P7-023, FR-P7-024, FR-P7-025, FR-P7-026, FR-P7-035) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the approval routing of RWB-E2-013 for rwb-decision, on base `/api/recovery/decision/v1`, with the delegation of authority read from rwb-access through its contract. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P7-E2013-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 24 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead of rwb-decision**, I want **the published contract baseline of the five approval operations — `GET /api/recovery/decision/v1/approvals`, `GET /approvals/{approvalId}`, `POST /approvals/{approvalId}/approve`, `/return` and `/refuse` on base `/api/recovery/decision/v1` — with the Approval resource and its authority element, the outcome enumerations, the escalation fields, the decision-record link, the error envelope with one message ID per condition, the two event envelopes, the nine contract tables and the six fakes**, so that **the app and OPS stories of this legacy key build against a fixed, testable contract on Day 1 and a field, a level, a status or a message code can never drift between rwb-decision, rwb-access, rwb-case, rwb-platform and the gateway without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). Approval routing shows why the baseline has to be fixed before the build: one routing decision reads the delegation rows and the authorise answer of rwb-access, the case and the parameters and lists of rwb-case, writes a local decision record and publishes two events, and one answer carries a level, a limit version, a status, a due time and an escalation level that three screens, one workflow and rwb-case read.

The baseline also fixes the naming the checks require: schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` for the service's own events, event names `rwb.decision.<Event>.v1`, task queue `rwb-decision` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.decision`. It records that the decision record leaves on the shared topic `rwb.decision-record.v1` through the local library and never through the service's own topic (DP-03, DP-09), and it records that the delegation of authority table is rwb-access's and is consumed and faked here and never joined (DP-01, DP-08).

It records too what the approval answer never carries: no customer name, no account number, no document body and no limit table. The answer holds IDs, codes, amounts, levels, versions and dates; the delegation facts are read at routing time from their owner and only the row reference, the level and the version are stamped on the approval.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so schema, topic, event and path names follow the platform rule rather than a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope and the retry and `.dlt` topic convention are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); where this document narrows them it does so explicitly.
- The operations and their owners are taken from the Ownership Map only; this document never declares another service's operation as provided.
- The delegation read of rwb-access is named by the target architecture as `GET /doa-limits` under P4, and the Ownership Map API catalogue has no row for it (GAP-1252; ASM-2216); the consumed row is written with the path the architecture names and the contract story of rwb-access fixes it.
- The contract baseline of the decision log of RWB-P7-E1008-CON is published, so the decision-record link this baseline carries points at one owner document.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).
- No production data is used in any example, schema or fake; every case number, user key, delegation row and amount is synthetic.

### 4. Flow

1. Draft the rwb-decision OpenAPI 3.1 fragment of the five approval operations, the Approval resource and the ApprovalAction request.
2. Fix the status enumeration, the level enumeration, the product enumeration and the override-reason reference list as enumerated elements of the answer, each read from reference data and not written in code.
3. Fix the authority element: the approval level or route role, the delegation row reference and the limit version, with the rule that the row is read from rwb-access and never joined.
4. Fix the escalation fields: the escalation level, the due time and the escalation role, so that an escalation is a change of level with an incremented counter and not a status.
5. Map every failure to the error envelope and one message ID, one condition per row.
6. Fix the `Idempotency-Key` rule on the three calls that change an approval, and the record-version rule behind 409.
7. Record the two published events with their schema elements, their key and their envelope, and the one consumed event.
8. Record that no workflow, no Schedule and no job element is created by the contract, and that the approval clock is the durable timer the app story implements.
9. Publish the nine contract tables of section 12 and the six contract fakes.
10. Add the contract tests: schema validation, the two enumerations, the authority element, the escalation fields, the error mapping, the idempotency replay, the event payload with no personal value, the drift between a fake and the document, and the absence of a retired element and of the delegation table.
11. Tag the baseline and hand it to RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP and the harness of the wave.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body or a request body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope, and a malformed request answers 422 | MSG-GEN-001 | AC1, AC5 |
| X2 | A field is renamed, removed or retyped within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A status value or a level value is added or removed | The enumeration test fails, and the change is a new major version of the answer | None | AC3 |
| X4 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC7 |
| X5 | A consumed path is not in the Ownership Map | The row carries its gap and its assumption, and the fake is derived from the owner's published document | None | AC4, AC7 |
| X6 | A retired element reappears in the document, a job or a topic | The absence test fails: no JOB-05 element, no Quartz row and no approval topic other than `rwb.decision.events.v1` | None | AC6, AC8 |
| X7 | A personal value appears in an example, a payload or a fake | The scanner fails the build and names the field and the sink | None | AC6 |
| X8 | The delegation table is declared as owned, joined or copied | The ownership test fails: `delegation_limit` is rwb-access's and the answer carries a reference only | None | AC2, AC4, AC8 |
| X9 | A field-level definition is missing from the source material | The field is marked with the placeholder and the combined gap row is carried | None | AC1, AC2, AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the decision-log contract of the same service and the Ownership Map only |
| Negotiable | Field-level detail is settled with the consumers; the five operations, the ten status and level values, the message IDs and the two event names are fixed by the target architecture and the legacy story |
| Valuable | Unblocks the app and OPS stories of this legacy key and every consumer of the approval answer on Day 1 |
| Estimable | One document fragment, five operations, one resource, nine contract tables, six fakes and nine contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of approval routing

  Background:
    Given the service naming rule of the platform library is in force
    Given the rwb-decision REST base is /api/recovery/decision/v1 and its topic is rwb.decision.events.v1
    Given no production data is used in any example, schema or fake

  Scenario: AC1 The OpenAPI document declares the five operations with their request and answer shapes (new, D-RCV-60)
    Given the OpenAPI 3.1 fragment of rwb-decision is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /approvals with the query parameters decision, product, page and size and the ApprovalPage answer, answering 200
    Then it declares GET /approvals/{approvalId} with no request body and the ApprovalDetail answer, answering 200
    Then it declares POST /approvals/{approvalId}/approve with the ApprovalAction body and the DecisionLogEntry answer, answering 200, with a required Idempotency-Key header
    Then it declares POST /approvals/{approvalId}/return with the ApprovalAction body and the Approval answer, answering 200, with a required Idempotency-Key header
    Then it declares POST /approvals/{approvalId}/refuse with the ApprovalAction body and the DecisionLogEntry answer, answering 200, with a required Idempotency-Key header
    Then all five sit under the base /api/recovery/decision/v1 and name rwb-decision as their owner
    Then the three POST operations declare the Idempotency-Key header as required and the two GET operations declare none
    Then each operation names the decision-log right A with the scope applied and the error responses 401, 403, 404, 409, 422 and 503 as section 12.1 lists them
    Then every property of the ApprovalAction is optional except the ones its condition needs, and every added property is optional, so a consumer of the previous version keeps working

  Scenario: AC2 The Approval resource fixes the approval, authority and source fields (new, D-RCV-60)
    Given the Approval resource declared in the document
    When its properties are compared with the approval table of the service
    Then it carries approvalId, caseId, decisionCode, regulationItem, capabilityArea, routeRoleCode, approvalLevel, delegationLimitId, limitVersion, productGroup, amount, terms, preparedBy, assignedUserId, status, dueAt, escalationLevel, sourceType, sourceRef, ruleId, ruleVersion and decisionLogId
    Then approvalId, caseId, decisionCode, capabilityArea, productGroup, preparedBy, status, sourceType and sourceRef are required, and the other thirteen are optional
    Then decisionCode is an element of the decision code list, capabilityArea of LOV-CAPABILITY and productGroup of LOV-PRODUCT, each read as reference data and never written in code
    Then approvalLevel is an element of LOV-APPROVAL-LEVEL and routeRoleCode names a role of the permission matrix; an item carries a level when it is limit-routed and a route role when it is role-routed
    Then delegationLimitId is an opaque reference to a row of rwb-access and not a foreign key, and limitVersion is the version in force on the routing date
    Then the resource carries no name, no e-mail address, no account number, no limit value and no customer fact

  Scenario: AC3 The status, level and outcome enumerations are fixed and the escalation is not a status (new, D-RCV-60)
    Given the status element of the Approval resource
    When its values are compared with the approval state machine
    Then status is one of WAITING, HELD_NO_LIMIT, APPROVED, REFUSED and RETURNED, copied from LOV-APPROVAL-STATUS
    Then approvalLevel is one of L1, L2, L3, L4, L5 and L6, copied from LOV-APPROVAL-LEVEL
    Then productGroup is one of MORTGAGE, HIRE_PURCHASE, SSME and UNSECURED, copied from LOV-PRODUCT
    Then escalationLevel is an integer that starts at 0 and increments by one on each escalation, and dueAt is the next due time after that escalation
    Then the document states that an escalation leaves the status WAITING, changes the level or the assigned role and writes a final call ESCALATED, and that ESCALATED is a decision-log final call and not a status value
    Then reasonCode names a row of LOV-OVERRIDE-REASON, read as reference data and never written in code

  Scenario: AC4 The authority element is read from rwb-access through its contract (new, D-RCV-60)
    Given the authority element of AC2 and the consumed row of section 12.2
    When the delegation read is reviewed against the Ownership Map
    Then the level, the holder, the substitute and the version are read on GET /api/recovery/access/v1/doa-limits, owned by P4 rwb-access, one hop with a 2 s timeout
    Then the authorise answer is read on POST /api/recovery/access/v1/authorise, owned by P4, and the A letter of the capability area is checked with the level or the route role
    Then the document states that delegation_limit is created, versioned and owned by rwb-access and that rwb-decision stores only delegationLimitId, approvalLevel and limitVersion
    Then the document declares no join, no view and no foreign key into rwb_access, and the contract test fails a document that names the delegation table as owned
    Then the DoA read has no row in the Ownership Map API catalogue, and the row carries its gap and its assumption (GAP-1252; ASM-2216)
    Then the DoA table stays with P4 while the routing rule and the approval sit with P7, and the split is recorded (GAP-1251; ASM-2215)

  Scenario: AC5 The error envelope maps one message ID per condition (new, D-RCV-60)
    Given the error responses declared for the five operations
    When each condition is compared with the message catalog
    Then the envelope is the platform error envelope with the status, the message ID and the message text, and no second envelope is introduced
    Then 401 answers with MSG-P4-001, 403 with MSG-P4-002 for a role without the A letter or the level, and 404 with MSG-P4-003 for an approval absent or outside the caller's scope
    Then 409 answers the preparer with MSG-P7-002, a change above the caller's level with MSG-P7-001, and a stale record version with MSG-GEN-004
    Then 422 answers a missing reason with MSG-GEN-001, a change from the recommendation without a coded reason with MSG-P7-005, and a committee approval without the resolution reference or the members present with MSG-GEN-001 naming the field
    Then 503 answers a decision record that cannot be written with MSG-P7-003 and a consumed call beyond the 2 s budget with MSG-GEN-006
    Then an item that no delegation row covers is answered as a status and a message in the body, with MSG-P7-010, and not as an error status
    Then no condition maps to two message IDs and no message ID is reworded

  Scenario: AC6 The ApprovalRequested and DecisionRecorded envelopes carry IDs and codes only (new, D-RCV-60)
    Given the event section of the document
    When it is reviewed against the event catalogue
    Then rwb.decision.ApprovalRequested.v1 is declared as event 09 on rwb.decision.events.v1, written to the outbox in the same transaction as the approval row
    Then its CloudEvents envelope names the type, the source service, the subject caseId and the key caseId
    Then its data carries approvalId, caseId, decisionCode, capabilityArea, approvalLevel or routeRoleCode, amount, limitVersion, ruleId, ruleVersion, dueAt and businessDate, and nothing else
    Then rwb.decision.DecisionRecorded.v1 is declared on rwb.decision-record.v1 through the local decision-record library with the decision code, the rule and the limit version
    Then the document states that no event carries a name, an account number, a document body or a limit value
    Then the document declares no ApprovalDecided event, because the catalogue has no row for it (GAP-1257; ASM-2221)

  Scenario: AC7 The nine contract tables are complete and the six fakes match them (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then 12.6 records None and states that the approval clock is a durable timer of the workflow and not a Schedule
    Then the rwb-access delegation and authorise fakes, the rwb-case case, parameter and reference-data fakes and the rwb-decision record fake answer the paths and payloads of 12.2 and the shapes of 12.1
    Then each fake answers the legacy values of section 7 of RWB-E2-013 and a delayed answer beyond 2 s
    Then the contract tests compare each fake with the document and fail on any drift

  Scenario: AC8 The owned tables, the naming and the migration are fixed by the baseline (new, D-RCV-60)
    Given the tables, the names and the migration declared in this story
    When they are compared with the service catalogue and the ownership map
    Then the service owns approval in schema rwb_decision, plus the library objects outbox_event, processed_event and idempotency_key created in that schema
    Then delegation_limit is named as rwb-access's, recovery_case, task, timer, parameter_catalog, parameter_value, reference_row and reference_version as rwb-case's, and decision_log_entry as this service's through the decision-log contract; none of them is declared as owned here except the decision entry
    Then the REST base is /api/recovery/decision/v1, the topic rwb.decision.events.v1, the queue rwb-decision in namespace rwb-recovery and the package th.co.scb.ace.workbench.recovery.decision
    Then the migration is a per-service Flyway script in the rwb-decision sequence and no script of another service is named
    Then the document states that the field-level types, lengths and optionality of the ApprovalAction and the page shape of the ApprovalPage are Not specified in the source documents (GAP-1255; ASM-2219)

  Scenario: AC9 A schema change stays additive within the major version and an event the catalogue does not carry is not declared (new, D-RCV-60)
    Given the OpenAPI fragment and the AsyncAPI fragment of this story
    When each schema change and each declared event is compared with the rules BR6 and BR14 and the event catalogue
    Then every schema change is additive within major version v1, and a breaking change is shown as a new major version, not as an edit of v1
    Then no event is declared that the event catalogue does not carry, whatever a service slide names
```

These nine criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by RWB-P7-E2013-APP. The fourteen legacy criteria of RWB-E2-013 are owned by RWB-P7-E2013-APP and copied there with their legacy tag; none of them is copied here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/decision/v1`; the document never declares another service's path as provided | DP-13; Architecture v5 slide 41 notes |
| BR2 | Event names are `rwb.<short>.<Event>.v1` on the topic `rwb.<short>.events.v1`, with retry and `.dlt` topics; the decision record leaves on the shared topic `rwb.decision-record.v1` | DP-03; DP-14; Template and Rules §R4 |
| BR3 | Every event carries the CloudEvents 1.0 envelope, is keyed by caseId, is written to the outbox in the same transaction as its state change and carries no personal data | Architecture v5 slides 42 and 43 notes; DP-09 |
| BR4 | A read declares no Idempotency-Key; a POST declares it and stores its answer | Architecture v5 slide 11; DP-09 |
| BR5 | Error responses use one envelope and one message ID per condition; the business message texts are copied unchanged from the legacy story | Architecture v5 platform baseline; Template and Rules §R7.2 s14 |
| BR6 | A schema change is additive within a major version; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR7 | The document lists only operations owned by rwb-decision; a consumed operation is described as consumed, never as provided; the case state, queues and tasks are rwb-case's, set by P3 on ApprovalRequested and never written by this service | Ownership Map v1; Architecture v5 slide 41 |
| BR8 | The delegation of authority table is rwb-access's and is read only through its contract, with no join, view or foreign key into rwb_access; the lookup is consumed from GET /api/recovery/access/v1/doa-limits and this service declares no path for it; the level lookup is a read with a 2 s budget; the service holds the delegation version in a local cache warmed before readiness and refreshed on DoaLimitChanged, with the effective date as the switch, no copy of the table, and an alert when the cached version is older than the version in force; the answer carries a row reference, a level and a version, never a limit value; the approval stores the delegation limit reference, the level and the version only; the lookup outcome is one of COVERED, NO_HOLDER, NOT_COVERED, NO_AMOUNT_LIMIT or RELATED_PARTY, and a refused authority decision carries requiredLevel; the request and response field set is frozen at the contract review | Architecture v5 slides 14 and 41; DP-01; DP-08; Ownership Map v1 |
| BR9 | The status, level, product and override-reason values are reference data of rwb-case, not contract constants written in code | TSD P7 T3.2; DP-07 |
| BR10 | An escalation is a change of level or role with an incremented escalation level and a new due time; it is not a status value | Legacy RWB-E2-013 AC2 and section 9; TSD P7 T3.1 and T3.2 |
| BR11 | The decision record is written locally through the decision-record library; it is never a new event of this service | Legacy RWB-E2-013 BR10; DP-03 |
| BR12 | The approval clock is a durable timer of the workflow; no Quartz row, no JOB-05 row and no Schedule belongs to this contract | Architecture v5 slides 42 and 44; DP-10 |
| BR13 | No business value is fixed in the contract: route roles, capability areas, levels, service levels and reason codes stay data or service configuration | Template and Rules §R7.2 s17 |
| BR14 | An event the catalogue does not carry is not declared by this baseline, whatever a service slide names | Architecture v5 slides 14 and 42; R-PREC |
| BR15 | The data lake copy of the decision record is retired: no INT-19 or INT-20 batch, lake partition, manifest or watermark belongs to this contract; reporting reads the DecisionRecorded event on rwb.decision-record.v1 | DP-17; ADR-018; Architecture v5 slide 37 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The five operations, the resource, the enumerations and the error mapping are described | In review |
| In review | Consumer sign-off | The app and OPS stories of this legacy key and the rwb-access, rwb-case and gateway-bff owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1, for example a new optional escalation field | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, or a status or level value is removed | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | Retired element reappears | The absence test of AC6 and AC8 fails | In review |

The approval state machine itself — WAITING, HELD_NO_LIMIT, APPROVED, REFUSED and RETURNED, with the escalation as a counter and a new due time — is declared by AC3 and written by RWB-P7-E2013-APP, not by this baseline.

### 10. Authority

The letters below are taken from the rwb-decision RBAC matrix of the module specification and from no other table.

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-decision | Owns the OpenAPI and AsyncAPI fragments and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of an Ownership Map row |
| Consuming teams (the app and OPS stories of this key, RWB-P7-E2014-APP, the harness, and the rwb-access, rwb-case and gateway-bff owners) | Review and sign off the parts they consume |
| RW-PRODHEAD, product head | Documents R on the decision log and A within the delegation table: the role the baseline names on the approve call |
| RW-LITOFF, litigation officer | Documents R: a reading role on an approval routed to the Litigation area |
| RW-HEADLIT, head of litigation | Documents R: the escalation role of a D7.x item |
| RW-RISK, risk and model risk officer | Documents R: the role that receives the no-limit incident, not an approval right |
| RW-AUDIT, internal audit | Documents R: a reading role on the decision log that the answer's decisionLogId points at |
| Platform library owner | Owns the CloudEvents envelope, the error envelope and the naming rule this document reuses |
| Data steward | Confirms that no personal data field is declared in an event or an answer |

The per-service login name behind the document's security scheme is not part of this baseline; the document names the scheme "the rwb-decision login (DP-02)". The authorisation decision itself is enforced at gateway-bff under RWB-PLT-N001-CON and RWB-P4-E1037-CON and is re-checked by the service on the decisive calls; it is not declared here.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | BR Field ID | Content |
|---|---|---|
| ApprovalAction | Not specified in the source documents (DOR-RWB-P7-E2013-CON-7) | `reason`, `resolutionReference`, `reasonCode`, `changes` and `membersPresent`, as the legacy story names them on the approve, refuse and return calls; which of them each call requires, and their types and lengths, are Not specified in the source documents (GAP-1255; ASM-2219) |
| Approval resource | DF-DEC-032 to DF-DEC-053 | The twenty-two properties of AC2, from approval DF-DEC-032 to DF-DEC-053; `delegationLimitId` and `limitVersion` are the authority element and are read from rwb-access, never derived from a limit table of this service |
| ApprovalDetail | Not specified in the source documents (DOR-RWB-P7-E2013-CON-7) | The Approval resource plus the routing detail the screen reads: the decision, the regulation item, the rule and its version, the due time, the escalation level, the source type and reference, the terms and the decision-log reference |
| ApprovalPage | Not specified in the source documents (DOR-RWB-P7-E2013-CON-7) | The Approval list with page metadata; the page shape, the default size and the maximum size are Not specified in the source documents (GAP-1255; ASM-2219) |
| DecisionLogEntry | Not specified in the source documents (DOR-RWB-P7-E2013-CON-7) | The reference returned by approve and refuse: the entry of the decision log of RWB-P7-E1008-CON, not a second resource of this service |
| Delegation read | Not specified in the source documents (DOR-RWB-P7-E2013-CON-7) | The delegation row reference, the level, the holder, the substitute, the version and the effective date, read from GET /api/recovery/access/v1/doa-limits with the decision, the regulation item, the product, the amounts and the on-date as the query; the field names behind the rwb-access contract are Not specified in the source documents (GAP-1252; ASM-2216) beyond the architecture naming of the operation |
| Event payloads | Not specified in the source documents (DOR-RWB-P7-E2013-CON-7) | IDs, codes, levels, amounts, versions, dates and the business date only; no name, account number, document body or limit value |
| Error body | Not specified in the source documents (DOR-RWB-P7-E2013-CON-7) | The status, the message ID and the message text of the platform envelope; no case fact and no approval fact beyond its ID |

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-decision (P7); base `/api/recovery/decision/v1`.

| ID | Method | Path | Documented shape | Access |
|---|---|---|---|---|
| API-P7-002 | GET | `/approvals` | Query decision, product, page, size; answer 200 with `ApprovalPage`; errors 401, 403, 503 | Decision log A, scope applied; no `Idempotency-Key` |
| API-P7-008 | GET | `/approvals/{approvalId}` | No body; answer 200 with `ApprovalDetail`; errors 401, 403, 404, 503 | Decision log A, scope applied; no `Idempotency-Key` |
| API-P7-003 | POST | `/approvals/{approvalId}/approve` | Body `ApprovalAction`; answer 200 with `DecisionLogEntry`; errors 401, 403, 404, 409, 422, 503 | Decision log A, scope applied; `Idempotency-Key` required |
| API-P7-004 | POST | `/approvals/{approvalId}/return` | Body `ApprovalAction`; answer 200 with `Approval`; errors 401, 403, 404, 409, 422, 503 | Decision log A, scope applied; `Idempotency-Key` required |
| API-P7-005 | POST | `/approvals/{approvalId}/refuse` | Body `ApprovalAction`; answer 200 with `DecisionLogEntry`; errors 401, 403, 404, 409, 422, 503 | Decision log A, scope applied; `Idempotency-Key` required |

The error codes of each condition and the enumerations are fixed by AC3 and AC5. Which property each `ApprovalAction` call requires, and whether a change above the caller's level is answered as 409 with the new level or as a stored `WAITING` item with a 200, are Not specified in the source documents (GAP-1255; ASM-2219); the legacy criterion AC7 answers MSG-P7-001 with the new level and approver, and this baseline carries that as the 409 body until the app story fixes the final shape.

#### 12.2 REST operations consumed

| Method and path | Owner | Contract | Use in the baseline |
|---|---|---|---|
| GET `/api/recovery/access/v1/doa-limits` | P4 rwb-access | RWB-P4-E1037-CON | The level, holder, substitute, row reference and version of the delegation table; the path is named by Architecture v5 slides 14 and 41 and has no Ownership Map API row (GAP-1252; ASM-2216) |
| POST `/api/recovery/access/v1/authorise` | P4 rwb-access | RWB-P4-E1037-CON | The A letter of the capability area and the caller's level or role (DP-08) |
| GET `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | RWB-P3-E1028-CON | The case, its status and the preparer; the case-status operation is not in the Ownership Map (GAP-1255; ASM-2219) |
| GET `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | RWB-P3-E1042-CON | The route, area and service-level parameters of DP-06 |
| GET `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | RWB-P3-E1043-CON | LOV-APPROVAL-LEVEL, LOV-APPROVAL-STATUS, LOV-CAPABILITY, LOV-PRODUCT and LOV-OVERRIDE-REASON of DP-07 |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (AC5, DP-11, ADR-020). The delegation table is consumed and faked, never joined and never declared as provided (BR8).

#### 12.3 Events published

| Event | Topic | Owner | Schema element |
|---|---|---|---|
| `rwb.decision.ApprovalRequested.v1` (event 09) | `rwb.decision.events.v1` | P7 rwb-decision | approvalId, caseId, decisionCode, capabilityArea, approvalLevel or routeRoleCode, amount, limitVersion, ruleId, ruleVersion, dueAt, businessDate; key caseId; written to the outbox in the same transaction as the approval row |
| `rwb.decision.DecisionRecorded.v1` (event 08) | `rwb.decision-record.v1` | P7 rwb-decision | decision code, rule ID and version, limit version, approval level, final call, approval ID, concluded at, record reference; published by the local decision-record library (DP-03) |

This story declares the two envelopes because the capability depends on them; the app story publishes them. `ApprovalDecided` is named in the service contract of Architecture v5 slide 14 and has no catalogue row, no event ID and no consumer, so it is not declared (GAP-1257; ASM-2221). The data-lake copy of the decision record of FEAT-DRI-06 and RWB-E1-014 is retired with the lake under DP-17; reporting reads the event on `rwb.decision-record.v1` (GAP-1254; ASM-2218).

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract element |
|---|---|---|---|
| `rwb.access.DoaLimitChanged.v1` | `rwb.access.events.v1` | P4 rwb-access | The delegation version that came into force and its effective date, so the cache of the routing is refreshed; declared so the version in force has one owner and one event |

This baseline fixes the shape and the key (no case key: the event is reference data, so the key is the delegation version); the approval read path subscribes to no event, and the consumer is RWB-P7-E2013-APP.

#### 12.5 Workflows and activities

None. The approval clock, its escalation and its restart are the durable timer of `ApprovalWorkflow`, which belongs to RWB-P7-E2013-APP; this baseline declares no workflow and no activity, and fixes only that the timer name, the task queue `rwb-decision` and the namespace `rwb-recovery` are the ones the app and OPS stories register (DP-10).

#### 12.6 Schedules

None. JOB-05, the legacy approval timer job, is retired and the approval clock is a workflow timer; the service's two Schedules, JOB-14 the hash-chain check at 02:00 and JOB-20 the rule promote at 00:01, belong to the decision-log and rule-version stories and are not declared here (Architecture v5 slides 42 and 44; DP-10).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| approval | P7 (rwb_decision) | The Approval resource, the authority element, the escalation fields and the status of AC2 and AC3 |
| decision_log_entry | P7 (rwb_decision) | The `DecisionLogEntry` answer of approve and refuse and the `decisionLogId` of the approval; the entry itself is the decision-log contract of RWB-P7-E1008-CON |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_decision` | The two published events, the one consumed event and the stored `Idempotency-Key` answer of BR4 |

`delegation_limit`, `role` and `permission` are P4 rwb-access's; `recovery_case`, `task`, `timer`, `parameter_catalog`, `parameter_value`, `reference_row` and `reference_version` are P3 rwb-case's; `notice` is P6's. None of them is declared as owned here and none is read directly (DP-01, BR8).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-access delegation WireMock | `DOA-2026.11` with L6 holder `U-9201`, L5 holder `U-9202`, L4 holder `U-9203` for MORTGAGE and the D6.4 row 2.1.1 at 2,400,000.00; no L6 holder for SSME; no row for HIRE_PURCHASE; the L3 committee row with recording holder `U-9204`; `U-9205` as the L6 substitute; `DOA-2027.01` from 1 January 2027; a delayed answer beyond 2 s | App story, contract tests, harness |
| rwb-access authorise WireMock | The A letter for `U-9201` in TREATMENT_AND_OFFER at L6, for `U-9213` in LITIGATION as RW-HEADLIT and for `U-9204` at L3; a refusal for a role without the area; a delayed answer beyond 2 s | App story, contract tests |
| rwb-case WireMock | Case `RW-2026-000123` at `In progress` with preparer `U-9211` and case `RW-2026-000124` at `In progress` with preparer `U-9210`; the status `Waiting approval` and the state of a refusal; the return task for `U-9210` | App story, contract tests, harness |
| rwb-case parameter WireMock | `rwb.approval.route.D7.1.area` = LITIGATION, `.role` = RW-LITOFF, `.escalation-role` = RW-HEADLIT and `.service-level` = 1 working day; `rwb.approval.service-level.default` = 3 working days; `rwb.approval.area.D6.4` = TREATMENT_AND_OFFER; a delayed answer beyond 2 s | App story, contract tests |
| rwb-case reference-data WireMock | LOV-APPROVAL-LEVEL with L1 to L6, LOV-APPROVAL-STATUS with the five values, LOV-CAPABILITY, LOV-PRODUCT with MORTGAGE, HIRE_PURCHASE, SSME and UNSECURED, and LOV-OVERRIDE-REASON with CUSTOMER_REVISED_OFFER; a delayed answer beyond 2 s | App story, contract tests |
| rwb-decision record WireMock | A healthy chain and outbox; a stopped chain for the fail-closed test; an entry with rule `R-LIT-03`, version `LIT-2026.12`, level L6 and final call `APPROVED` | App story, contract tests, harness |

The values are the legacy values of RWB-E2-013 section 7 and its background, kept unchanged so the component and integration assertions read the same fixtures.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 5 provided, 5 consumed | API-P7-002, API-P7-008, API-P7-003, API-P7-004 and API-P7-005 provided; the delegation read, the authorise call, the case read, the parameters and the lists consumed; one hop, 2 s |
| Kafka | 2 declared as published by their owners, 1 declared as consumed | `ApprovalRequested` and `DecisionRecorded`; `DoaLimitChanged` |
| Temporal | None | No workflow and no Schedule in this baseline; `ApprovalWorkflow` and its durable timer belong to RWB-P7-E2013-APP |
| File | None | No file element in this contract |

### 13. Solution plan

**Deliverables.** The additive change to the rwb-decision OpenAPI 3.1 document, the Approval, ApprovalDetail, ApprovalAction, ApprovalPage and DecisionLogEntry components, the AsyncAPI fragment of `rwb.decision.events.v1` that names `ApprovalRequested`, the contract README rows for the enumerations, the authority element, the escalation rule, the error mapping and the idempotency rule, and the six WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_decision`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

No pattern is claimed for DP-02, DP-04, DP-05, DP-12, DP-14, DP-16, DP-17, DP-18 or DP-20: this baseline declares no login value, no rule package, no ACE view, no case workflow, no renamed topic, no integration adapter, no data lake, no interaction ledger and no agent.

**Build steps**

1. Add the five operations and the five components to the OpenAPI document; validate the additive rule of AC1 in the pipeline.
2. Fix the three enumerations of AC3 as schema elements and add a test that a new status or level fails the build.
3. Write the authority element of AC2 and AC4, with the two consumed rows and the ownership test that fails a document naming `delegation_limit` as owned.
4. Write the error mapping of AC5 as one row per condition with its message ID, and assert that no condition carries two message IDs.
5. Fix the escalation fields and the rule of AC3, with a test that `ESCALATED` is not a status.
6. Record the two published and the one consumed event envelopes, with a scanner that fails on a personal value in any example or payload, and the absence test for `ApprovalDecided` and JOB-05.
7. Publish the six fakes and the nine contract tests; a drift between a fake and the document fails the build.
8. Baseline tag and the consumer sign-off note, including the app and OPS stories of this key, RWB-P7-E2014-APP, the harness and the rwb-access, rwb-case and gateway-bff owners.

**Done when.** The OpenAPI and AsyncAPI artefacts validate in the pipeline, the nine contract tests pass, the six fakes answer every consumed path and the drift test is green, no personal value appears in an example or a payload, the delegation table is named only as consumed, and the app and OPS stories of this legacy key have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-001 | A change is above the caller's level | This needs approval at level {level}. It has been sent to {approver}. |
| MSG-P7-002 | The caller prepared the item | You prepared this decision, so you cannot approve it. |
| MSG-P7-003 | The local decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-005 | A change from the recommendation carries no coded reason | Enter the reason you are not following the recommendation. |
| MSG-P7-010 | No delegation row covers the decision and product | No approval limit covers {decision} for {product}. The item is held and Risk has been told. |
| MSG-P7-011 | An item is escalated to a new approver | {decision} on case {caseNo} passed its service level and is now with you for approval. |
| MSG-GEN-001 | A required request field is missing or invalid | Enter {field}. |
| MSG-GEN-004 | The record changed under another approver | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-006 | A consumed call does not answer in time | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-001 | No Workbench role on the token | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | The role lacks the A letter or the level | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The approval is outside the caller's scope | This case is not in your scope. |

The message IDs are contract elements and the text is the agreed text: MSG-P7-001, MSG-P7-002, MSG-P7-003, MSG-P7-005, MSG-P7-010, MSG-P7-011, MSG-GEN-001, MSG-GEN-004 and MSG-P4-002 are copied from RWB-E2-013 section 14, and MSG-P4-001, MSG-P4-003 and MSG-GEN-006 from the platform message catalog. MSG-P4-003 and MSG-GEN-006 are named on the consumed rows of 12.2 as well, because the refusal and the timeout are raised by their owner and only relayed here.

### 15. Screens and states

The baseline serves the approval answer that SCR-10 Approval queue reads through the gateway-bff composite route (DP-19):

| Screen | What it reads from this contract | State |
|---|---|---|
| SCR-10 Approval queue | The page of approvals waiting on the caller, with decision, case, amount, level, limit version, age and due time | List, Loading; Empty, Error, No access: Not specified in the source documents (CG-ALL-7174) |
| SCR-10 Approval queue | The detail of one item before an action, with the routing detail of `ApprovalDetail` | Detail |
| SCR-11 Decision screen | The same detail, built in RWB-P7-E2014-APP for the D7.1 notices | Detail; Empty, Loading, Error, No access: Not specified in the source documents (CG-ALL-7175) |
| SCR-44 Interface and job monitor | Nothing from this contract directly; the timer and the escalation are workflow state, read by the OPS story | Escalated; Empty, Loading, Error, No access: Not specified in the source documents (CG-ALL-7176) |

The composite route, its field list, its masking rules and its timeout budget belong to RWB-PLT-N001-CON and are not fixed here. The Loading and Error states of the route are the platform route's, not this contract's. This baseline serves no notice approval: POST /api/recovery/v1/notices/{noticeId}/approve (Litigation A, API-S4-001) stays with the E2 notice story, the pack step approves no notice, and R-LIT-04 only blocks the generation.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P7-E2013-CON-01 | AC1, BR1, BR4, BR7 | Contract | The OpenAPI fragment with the five operations; a request missing the Idempotency-Key on a POST; an added optional property |
| TC-P7-E2013-CON-02 | AC2, BR5, BR8 | Contract | The Approval resource against approval DF-DEC-032 to DF-DEC-053; a resource carrying a name or a limit value |
| TC-P7-E2013-CON-03 | AC3, BR9, BR10 | Contract | The five status values and the six level values; an escalation from L6 to the escalation role with escalation level 1 and a new due time; a document declaring ESCALATED as a status |
| TC-P7-E2013-CON-04 | AC4, BR8, BR13 | Contract | The delegation and authorise fakes; a document naming delegation_limit as owned or joining rwb_access |
| TC-P7-E2013-CON-05 | AC5 | Contract | One call per condition: 401, 403, 404, the three 409s, the three 422s, the two 503s and the MSG-P7-010 body |
| TC-P7-E2013-CON-06 | AC6, BR2, BR3, BR11 | Contract | The ApprovalRequested and DecisionRecorded envelopes; a payload carrying an account number; an ApprovalDecided declaration |
| TC-P7-E2013-CON-07 | AC7, BR4, BR11 | Contract | The nine tables and the six fakes, with a drift between the fake and the document and a delayed answer beyond 2 s |
| TC-P7-E2013-CON-08 | AC8, BR1, BR2, BR12 | Contract | The owned and not-owned lists of 12.7, the naming of section 12, and the absence of a JOB-05 element and of a Schedule of this capability |
| TC-P7-E2013-CON-09 | AC8, BR8 | Contract | The boundary of the 12.7 tables: the last owned table idempotency_key and the first not-owned table delegation_limit |
| TC-P7-E2013-CON-10 | AC9, BR6, BR14 | Contract | The OpenAPI fragment and the AsyncAPI fragment against BR6 and BR14; the proposed test steps are Not specified in the source documents (NEWAC-RWB-P7-E2013-CON-AC9) |

These ten cases are new for the contract baseline and test the artefact only; no legacy test case of RWB-E2-013 is copied here, and TC-E2-013-01 to TC-E2-013-16 stay with RWB-P7-E2013-APP. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID once the contract tab is published.

### 17. Guardrails

- No business value in the contract: route roles, capability areas, levels, service levels, the escalation ceiling and the reason codes stay data, reference data or service configuration.
- No personal data in a schema, an example or a fake: IDs, codes, levels, amounts, versions and dates only; no name, e-mail address, account number or document body.
- The contract names only rwb-decision tables and only operations owned by rwb-decision; the delegation, the authorise answer, the case, the parameters and the lists are consumed and faked, never declared as provided (DP-01).
- The delegation of authority table is never declared as owned, joined, copied or read directly (BR8, AC4).
- One REST base, one topic and one decision-record topic: `/api/recovery/decision/v1`, `rwb.decision.events.v1` and `rwb.decision-record.v1`; a document that names another service's base or topic as its own fails the review (DP-03, DP-13).
- ACE data is reached only through the owner's contract; this document declares no ACE view and no cross-schema join.
- No retired element is reintroduced: the absence test fails a build that declares JOB-05, a Quartz row, a Schedule of this capability or an uncatalogued event.
- The error envelope, the CloudEvents envelope and the naming rule come from the platform library; this story narrows them but never redefines them.
- Every example is synthetic; no production payload is copied into a schema or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-APD-001 | Route to the approver the delegation table names | The authority element, the delegation consumed row and the level enumeration | TC-P7-E2013-CON-02, TC-P7-E2013-CON-04 |
| REQ-APD-003 | Accept, change, reject or return, each recorded | The three POST operations, `ApprovalAction` and the `DecisionLogEntry` answer | TC-P7-E2013-CON-01, TC-P7-E2013-CON-05 |
| REQ-APD-009 | The limit, the rule version and the approver are written | `limitVersion`, `approvalLevel`, `ruleId`, `ruleVersion` and `decisionLogId` on the resource | TC-P7-E2013-CON-02, TC-P7-E2013-CON-06 |
| REQ-APD-010 | Open items keep the version they were decided under | `limitVersion` as a stamped field and `DoaLimitChanged` as the only refresh | TC-P7-E2013-CON-03, TC-P7-E2013-CON-04 |
| RWB-E2-013 | The legacy key whose contract this baseline fixes | The nine criteria of section 7 | TC-P7-E2013-CON-01 to TC-P7-E2013-CON-10 |
| DP-01 | Owner's schema; no service reads another service's tables | The owned and not-owned lists of 12.7 | TC-P7-E2013-CON-04, TC-P7-E2013-CON-08, TC-P7-E2013-CON-09 |
| DP-03 | Local decision record and the shared topic | The `DecisionRecorded` row of 12.3 | TC-P7-E2013-CON-06 |
| DP-06 | Parameters through rwb-case's contract | The parameters row of 12.2 | TC-P7-E2013-CON-04, TC-P7-E2013-CON-07 |
| DP-07 | Reference data through rwb-case's contract | The lists row of 12.2 and the enumerations of AC3 | TC-P7-E2013-CON-03, TC-P7-E2013-CON-07 |
| DP-08 | Authorise contract of rwb-access | The authorise row of 12.2 and the 403 mapping of AC5 | TC-P7-E2013-CON-04, TC-P7-E2013-CON-05 |
| DP-09 | Outbox, inbox and CloudEvents | The two envelopes of AC6 and the consumed event of 12.4 | TC-P7-E2013-CON-06 |
| DP-10 | Temporal instead of Quartz | 12.5 and 12.6, and the absence test of AC8 | TC-P7-E2013-CON-08 |
| DP-11 | REST contract with mock, one hop, 2 s | The five consumed rows and the six fakes of 12.8 | TC-P7-E2013-CON-05, TC-P7-E2013-CON-07 |
| DP-13 | Per-service REST base | `/api/recovery/decision/v1` | TC-P7-E2013-CON-01 |
| DP-15 | Per-service Flyway | The migration of AC8 | TC-P7-E2013-CON-08 |
| DP-19 | Screen through gateway-bff | The screen reads of section 15 | TC-P7-E2013-CON-01 |
| ADR-020 | Contract-first REST, one hop, 2 s | The 2 s budget and the error mapping of AC5 | TC-P7-E2013-CON-05 |

### 19. Out of scope

- The implementation of the routing, the outcome checks, the escalation and the workflow (RWB-P7-E2013-APP).
- The deployment, the worker registration, the dashboards, the alerts and the run book (RWB-P7-E2013-OPS).
- The fourteen legacy criteria of RWB-E2-013, owned by RWB-P7-E2013-APP and tagged there.
- The decision screen SCR-11 and the D7.1 notice approval with release to dispatch (RWB-P7-E2014-APP).
- The delegation of authority table, its versions, its holders and its substitutes, owned by rwb-access and consumed here through RWB-P4-E1037-CON.
- The case, its status, the return task and the case-level timers, owned by rwb-case and consumed here.
- The parameters, the capability areas and the five lists as catalogues, owned by rwb-case (DP-06, DP-07).
- The decision-log contract, the hash chain, the daily seal and JOB-14 (RWB-P7-E1008-CON, RWB-P7-E1008-APP, RWB-P7-E2005-APP).
- The rule package registry and JOB-20, owned by the rule-version stories of this epic.
- The gateway-bff composite route, its masking and its timeout budget (RWB-PLT-N001-CON), and the screens themselves.
- The data lake: there is none (DP-17, ADR-018), and this baseline declares no lake element.
