# RWB-S9-E7018-CON Capture field work through the field app - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E7018-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the field work of rwb-partner, split from RWB-E7-018. It fixes the field-work element of `POST /partner/instructions/{instructionId}/results` (API-S9-005) on `/api/recovery/partner/v1` (DP-13) — the multipart `result` and `files` parts, the document references, the visit reference, the required flags, the four lists of TSD S9 T3.2 and the right U of the document — together with the three consumed rows (rwb-source-data's ledger, rwb-document's intake and rwb-decision's rule version), the EV-21 shape and envelope on `rwb.partner.events.v1`, the decision-record element of DP-03, the error envelope, the fakes and the absence tests. No source publishes a field-visit table in S9, a field-collector role, a result-code list, a document or interaction operation name, a partner route set or an interface ID for the field app, and TSD S9 T8 maps REQ-S9-009 to another feature (GAP-3136; ASM-5491, ASM-5492, ASM-5493, ASM-5494, ASM-5495, ASM-5496, ASM-5498, ASM-5499, ASM-5500, ASM-5501, ASM-5502). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S9-E7018-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the field work of rwb-partner — the field-work element of the result operation with its multipart parts and required flags, the document and visit references, the three consumed rows, the EV-21 shape, the decision-record element, the rights and the fakes**, so that **the app story, PRT-02 and the field application build against one fixed, testable contract on Day 1, and a result code, a document reference, a list value or an event shape can never drift between rwb-partner, rwb-document, rwb-source-data and rwb-decision without a failing build**.

This baseline declares shapes and moves nothing. It owns:

- the field-work element of `POST /partner/instructions/{instructionId}/results` (API-S9-005), declared additively inside the baseline RWB-S9-E6033-CON publishes for the same operation, with the `result` and `files` parts and the `Idempotency-Key`;
- the properties of the element over DF-PRT-008 to DF-PRT-016 and DF-REF-212 to DF-REF-217, with the required flags and the four lists of TSD S9 T3.2 published unchanged;
- the three consumed rows: the ledger entry of rwb-source-data, the document intake of rwb-document and the rule version of rwb-decision, each with a fake and a placeholder;
- the event EV-21 with its topic, name, envelope and payload;
- the decision-record element of DP-03 and the naming baseline of the service;
- the error envelope with 415 among the codes, the rights of the operation and the absence tests.

It does not own: the behaviour of the field-work step (RWB-S9-E7018-APP), the portal result intake (RWB-S9-E6033-APP), the instruction and acceptance operations (RWB-S9-E6031-APP, RWB-S9-E6034-APP), the invoice operation (RWB-S9-E6035-APP), the document hub (P5), the ledger (P1), the case (P3), the rule rows (P7) and the deployment of the service (the operations story of this legacy key).

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy feature crossed four boundaries at once — the instruction of the service, the case it belongs to, the evidence the collector brings and the rule version the record cites — and the legacy endpoint table named the result operation and the partner read without saying which fact belonged to whom. The target splits them: rwb-partner owns the instruction and its result, rwb-document owns the photograph and the bill, rwb-source-data owns the visit in its ledger, rwb-case owns the case and rwb-decision owns the rule and the central ledger. Each boundary is a contract another team builds against, so each is fixed before the app story starts.

The baseline also fixes the naming the checks require: schema and login `rwb_partner`, base `/api/recovery/partner/v1`, topic `rwb.partner.events.v1` with its retry and `.dlt` topics, task queue `rwb-partner` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.partner` (Template and Rules §R4; context pack). It records that this service holds no `v_ace_*` grant and no grant on `rwb_document`, `rwb_source_data`, `rwb_case` or `rwb_decision`.

Five points are carried as gaps and assumptions rather than decided quietly: the evidence and the visit are other services' rows and their operation names have no source (ASM-5491, ASM-5493); the field collector has no role row and `partner_user.role_code` reads LOV-ROLE, which publishes no list (ASM-5492); `result_code` has no list (ASM-5494); no partner route set exists, so the rule ID and version carry the placeholder (ASM-5496); and EV-21 is published in TSD S9 T5.3 and consumed in the event catalogue (ASM-5495).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the multipart rule, the pagination convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- Ownership is taken from the context pack and the Ownership Map only: `partner`, `partner_instruction` and `partner_user` are S9's, `document` is P5's, `interaction` is P1's, `recovery_case` and `timer` are P3's, `decision_log_entry` and `rule_row` are P7's, `notice` is P6's and every `v_ace_*` view is P1's. This document never declares another service's table or operation as its own.
- The result operation is published: TSD S9 T-A.1 gives API-S9-005 `POST /partner/instructions/{instructionId}/results` with partner portal right U and the `Idempotency-Key`, and T-A.2 gives its multipart request, its `PartnerInstruction` answer and the errors 401, 403, 404, 409, 415, 422 and 503.
- RWB-S9-E6033-CON is the baseline of the same operation for the portal intake. This document adds one element to it and re-declares nothing.
- The rwb-document, rwb-source-data and rwb-decision contracts are published with their fakes. Their operation names and the upload media types are Not specified in the source documents (GAP-3136; ASM-5491, ASM-5493, ASM-5496, ASM-5502).
- The `partner`, `partner_instruction` and `partner_user` tables arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 and sits in contract group `CG-W4` by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the field-work element of API-S9-005 inside the baseline of RWB-S9-E6033-CON, with its `result` part, its `files` part and its answer properties.
2. Fix the properties over DF-PRT-008 to DF-PRT-016 and DF-REF-212 to DF-REF-217, with the required flags of AC2 and the lists of TSD S9 T3.2 published unchanged.
3. Fix the document reference, the visit reference, the contact date and the rule ID with the version, and record which of them have no source.
4. Record the three consumed rows with their owners, their budgets, their fakes and their placeholders.
5. Record the decision-record element of DP-03, written before the answer, and record that no partner route set exists.
6. Record EV-21 with its topic, name, envelope, key, payload and consumers, and record the direction conflict.
7. Record the rights of the operation from TSD S9 T6.1 and T-A.1, the error envelope with 415, the naming baseline and the boundary rule.
8. Publish the contract tables of section 12 and the fakes of 12.8.
9. Add the contract tests: schema validation, the additive rule, the shapes, the lists, the multipart limits, the scope, the error envelope, the absence of a `v_ace_*` read and of a `document`, `interaction`, `recovery_case` or `rule_row` write, the drift between a fake and the document, and the absence of a new operation, table, Schedule or second topic.
10. Tag the baseline and hand it to RWB-S9-E7018-APP, to PRT-02 and the field application, and to the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request or a response body fails schema validation, or a part of the multipart body is unformed | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A property is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row or a field-work property has no name, list, media type or value in the sources | The row or the property carries the placeholder and the fake is derived from the published document | None | AC3, AC6 |
| X5 | A value of a list is declared as a code enumeration taken from no source, or the result vocabulary is invented | The vocabulary test fails the build: the list is the published LOV, and the result carries the placeholder | None | AC2 |
| X6 | The document declares another service's operation or table as provided, a `v_ace_*` view, a `document`, `interaction`, `recovery_case` or `rule_row` write, or a field-visit table | The review fails the baseline and the boundary test fails the build | None | AC3, AC7 |
| X7 | The document declares a second topic, a new operation, a Schedule, a Quartz row or a job | The absence test fails the build | None | AC4, AC7 |
| X8 | The rights of the operation are not the ones TSD S9 T6.1 and T-A.1 give it, or the 415 is dropped | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the FSD and TSD S9 appendices, the event catalogue, the LDM and the published owner contracts of rwb-document, rwb-source-data and rwb-decision only |
| Negotiable | The example values and the internal record shape are settled in the baseline review; the base, the operation, the rights, the lists, the topic, the queue and the schema are fixed by the architecture |
| Valuable | Unblocks RWB-S9-E7018-APP, PRT-02, the field application and the wave 4 harness on Day 1, and the rwb-document, rwb-source-data and rwb-decision teams on the same day |
| Estimable | One additive element on a published operation, nine contract tables, five fakes and ten contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the field work of rwb-partner

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of partner, partner_instruction and partner_user is S9, of document is P5, of interaction is P1, of recovery_case and timer is P3 and of decision_log_entry and rule_row is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The field-work element is declared on the published result operation (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-partner is published with this change
    When it is validated against the OpenAPI 3.1 schema and against the baseline of RWB-S9-E6033-CON
    Then it validates with no error
    Then POST /partner/instructions/{instructionId}/results is declared once as API-S9-005, with the base /api/recovery/partner/v1 owned by rwb-partner, the Idempotency-Key header and the errors 401, 403, 404, 409, 415, 422 and 503
    Then the request is declared as multipart with a result part of the FieldWorkResult element and a files part of one or more binary claims, and the answer is the PartnerInstruction element with the result, the status and the document references
    Then the change is additive within major version 1: no path, no operation ID, no error code and no existing property is renamed, removed or retyped by this baseline
    Then the document declares no second result operation, no visit path and no evidence path, and API-S9-001, API-S9-003, API-S9-004 and API-S9-006 are declared as they are without a change
    Then the upload media types, the size limits and the per-submission file count are Not specified in the source documents (GAP-3136; ASM-5502)

  Scenario: AC2 The field-work properties, their required flags and their lists are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S9 T3.0, T3.1, T3.2 and T-A.2 and with LDM v8
    Then FieldWorkResult declares instructionId, result, resultCode, status, visitedOn, documents and ruleVersion, drawn from DF-PRT-008, DF-PRT-014, DF-PRT-015, DF-REF-212 to DF-REF-217 and the documents of the answer
    Then the required properties are instructionId, result and visitedOn, with instructionId read-only, status read-only in the answer, and documents optional and repeatable
    Then the lists are LOV-INSTR-STATUS SENT, ACCEPTED, DECLINED, IN_PROGRESS, DONE and RECALLED, LOV-INSTRUCTION COLLECT, FILE_SUIT, ENFORCE, APPRAISE, REPOSSESS, LIST and SELL, LOV-PANEL ACTIVE, ON_NOTICE, SUSPENDED and EXITED, and LOV-PARTNER-TYPE AGENCY, LAW_FIRM, VALUER, AUCTION_VENDOR, BROKER, DEBT_BUYER, AMC and RAMC, copied from TSD S9 T3.2 and published unchanged
    Then resultCode is declared as a free value of varchar(40) with no enumeration, because DF-PRT-015 carries no list and the vocabulary is Not specified in the source documents (GAP-3136; ASM-5494)
    Then the element declares no property for a photograph, a bill, a document type, an index entry, a document body or a contact identity, and the document reference carries no field ID: Not specified in the source documents (GAP-3136; ASM-5491)
    Then the element declares no property of recovery_case, interaction, rule_row or a v_ace_* view

  Scenario: AC3 The visit, the evidence and the rule are declared as consumed and the boundary is fixed (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership of the context pack, with FSD S9 A2.15.2 and with LDM v8
    Then one interaction entry is declared as consumed from P1 rwb-source-data with channel VISIT and source FIELD_VISIT over DF-INT-001 to DF-INT-013, and its operation name and its reference field are Not specified in the source documents (GAP-3136; ASM-5493)
    Then the document intake is declared as consumed from P5 rwb-document as a claim-check claim per photograph and per bill, per REQ-DCM-013, and its operation name, its media types and its return element are Not specified in the source documents (GAP-3136; ASM-5491)
    Then the rule ID and the version in force are declared as consumed from P7 rwb-decision as values at their effective date under R-UNI-38, and no partner route set exists, so the pair is Not specified in the source documents (GAP-3136; ASM-5496)
    Then each consumed row is one hop with a 2 s budget and a breaker and declares no retry of its own (DP-11, ADR-020)
    Then the document declares no v_ace_* path or property, no document, interaction, recovery_case, timer or rule_row property, no field-visit table and no grant on any rwb_* schema of another owner

  Scenario: AC4 The event is declared with its direction and the conflict is recorded (new, D-RCV-60)
    Given the event section of the baseline
    When it is compared with Event and Messaging Design v5 and with TSD S9 T5.3
    Then the topic is rwb.partner.events.v1 with its retry and .dlt topics, and the event is rwb.partner.PartnerResultSubmitted.v1 (EV-21) in a CloudEvents 1.0 binary envelope with ce_source rwb-partner and the case ID as key and subject
    Then the payload is instructionId, result and documents with the submitted time, and it carries no personal data, no free text and no document content
    Then the event is declared published by this service on the field-app path, while the event catalogue reads EV-21 as consumed from the partner portal and TSD S9 T5.3 lists it as published; the conflict is recorded and one direction is declared (GAP-3136; ASM-5495)
    Then the document declares no second topic, no producer group of a step other than the result step and no consumed event of this step

  Scenario: AC5 The rights and the error envelope are fixed (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S9 T-A.1, T-A.2 and T6.1
    Then API-S9-005 declares Partner portal right U with the scope applied, and the 13 identities that hold U are RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT, RW-AGENCYMG and the six PT identities, which are the eight the legacy permission table names and its five more (ASM-5492)
    Then the 29 identities of the Partner portal column hold right R and are refused the submission, and they are the legacy table's eight roles and its twenty-one more
    Then a caller of another firm is declared as answered 404 by the scope, and a role without the right is refused with 403 and MSG-P4-002
    Then the error envelope carries one message ID per condition for 400, 401, 403, 404, 409, 415, 422 and 503, and the text of the 409 is Not specified in the source documents (GAP-3136; ASM-5500)
    Then no partner-identity element declares a credential, a token, a password or a personal contact value

  Scenario: AC6 The decision-record element and the five fakes answer the document (new, D-RCV-60)
    Given the record and the fakes of the baseline
    When each is compared with the library schema and with the operation or the element it serves
    Then one decision record is declared per submission with the instruction, the case, the firm, the result, the document count, the rule ID and the version in force
    Then the record is declared as written through the local library on the shared rwb.decision-record.v1 before the answer leaves the service, and the MSG-P7-003 path is declared
    Then the rwb-document fake answers a document reference and an index entry per claim, the rwb-source-data fake answers an accepted visit entry, the rwb-decision fake answers the rule and the version in force and a missing version, the decision-record stub answers a healthy and a stopped chain, and the partner-gateway fake answers the firm scope of the caller
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline, the tables and the boundary are fixed and no Schedule is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema is rwb_partner, the login is rwb_partner, the base is /api/recovery/partner/v1, the topic is rwb.partner.events.v1 with its retry and .dlt topics, the queue is rwb-partner in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.partner
    Then the tables named as owned are partner, partner_instruction and partner_user, with the library objects decision_record, idempotency_key, outbox_event and processed_event, and document, interaction, recovery_case, timer, decision_log_entry, rule_row, notice and payment are named as other owners' and consumed only through their contracts
    Then the properties of partner_instruction and partner_user are those of TSD S9 T3.1 and LDM v8 DF-PRT-008 to DF-PRT-016 and DF-REF-212 to DF-REF-217, and no visit table and no evidence column is declared (GAP-3136; ASM-5491, ASM-5493)
    Then the document declares no Schedule, no Quartz row and no job, because the ownership rows give the service none and the offline queue is the field application's
    Then the absence test fails a build that adds a new operation, a visit table, an evidence column, a second topic, a Schedule, a job, a v_ace_* read or a document, interaction or case write
```

These seven criteria are new for the contract baseline and test the artefact only. They copy no criterion of the legacy story, whose AC1 and AC2 stay with RWB-S9-E7018-APP word for word. The baseline fixes a surface; it records no visit, uploads no evidence and moves no instruction.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The field-work element is declared on the one published result operation and on no second operation, over the columns of DF-PRT-008 to DF-PRT-016 and DF-REF-212 to DF-REF-217 | TSD S9 T3.1, T-A.1, T-A.2; context pack ownership rows (tables `partner`, `partner_instruction`, `partner_user`; 6 REST operations) |
| BR2 | The visit is P1's interaction and the photographs and bills are P5's documents: the contract declares them as consumed rows with fakes and declares no visit table, no evidence column and no document body | DP-18; LDM v8 `interaction`, DF-INT-001 to DF-INT-013, LOV-CONTACT-SRC; REQ-DCM-013; ASM-5491, ASM-5493 |
| BR3 | The rule ID and the version are read as values at their effective date under R-UNI-38; no partner route set exists, so no rule row, package or rule ID set is declared and the pair carries the placeholder | Business Rules and Routing Logic v4 (no R-PRM rows; R-UNI-38 to R-UNI-40 nearest); ASM-5496 |
| BR4 | `result_code` is declared as a free varchar(40) value and never as an enumeration of the code, because DF-PRT-015 carries no list | TSD S9 T3.1; ASM-5494 |
| BR5 | The status vocabulary of the element is LOV-INSTR-STATUS and nothing else; `DECLINED` and `RECALLED` are values of the list and have no screen state of their own | TSD S9 T3.2; ASM-5497 |
| BR6 | EV-21 is one event on one topic with one envelope and one payload; the direction conflict is recorded and no second topic or producer group is declared | Event and Messaging Design v5; TSD S9 T5.3; ASM-5495 |
| BR7 | The operation declares the `Idempotency-Key` header and stores its answer, so the offline queue of the field application may resend one visit | TSD S9 T-A.2; NFR-062; ASM-5501 |
| BR8 | The multipart declaration follows the platform rule: the `result` part as JSON over the element and the `files` part as claim-check claims; the media types, the size limits and the file count carry the placeholder | ADR-020; FSD S9 A2.15.2; ASM-5502 |
| BR9 | No personal data in a schema, an example or a fake: identifiers, codes, list values, dates, a count of documents, a rule ID and a version only, and every example is synthetic | Template and Rules §R7.2 (s17); TSD S9 T6.2; NFR-053 |
| BR10 | One REST base, one topic, one queue, one schema and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR11 | A schema change is additive within major version 1; a breaking change is a new major version, and this baseline adds one element and changes no existing property | Platform API rule (ADR-020) |
| BR12 | The document lists only operations owned by rwb-partner; a consumed operation is described as consumed and faked, never as provided | DP-01, DP-11; context pack ownership rows (6 REST operations) |
| BR13 | The rights are the Partner portal rights of TSD S9 T6.1 and T-A.1: U on API-S9-005 for the 13 identities and R for the 29, and no partner-side identity holds right C | TSD S9 T6.1, T-A.1; legacy permission table of RWB-E7-018; ASM-5492 |

### 9. State transitions

The lifecycle of this document, not of an instruction:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The element, the properties, the three consumed rows, the event, the record element and the fakes are described | In review |
| In review | Consumer sign-off | The app story, PRT-02, the field application, the wave 4 harness and the owners of rwb-document, rwb-source-data and rwb-decision accept the document and the fakes | Baselined |
| Baselined | The three operation names are confirmed | The owners name the ledger entry, the intake and the rule read inside major version 1 | Baselined |
| Baselined | The result vocabulary is confirmed | The business lead publishes the result codes as a list inside major version 1 | Baselined |
| Baselined | Additive change | A property or an optional part is added within major version 1 | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a list value becomes an enumeration the list does not hold | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC1, AC3, AC4 and AC7 fail: a new operation, a visit table, an evidence column, a second topic, a Schedule, a job, a `v_ace_*` read or a document write | In review |

The state machine the document describes is the app story's: LOV-INSTR-STATUS is `SENT`, `ACCEPTED`, `DECLINED`, `IN_PROGRESS`, `DONE` and `RECALLED`, and the field-work step writes `DONE` only. This baseline fixes the vocabulary and the answer shape and moves no instruction.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-partner | Owns the element, the contract tables and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the confirmed operation names, the confirmed result vocabulary and the correction of the plan's C row |
| Business lead | Confirms the result vocabulary, the visit facts, the evidence types and the reading of `partner_user` |
| Consuming teams (the app story, PRT-02, the field application, the wave 4 harness and the owners of rwb-document, rwb-source-data and rwb-decision) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the multipart rule, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox and inbox library this document reuses |
| Data steward | Confirms that no personal data field is declared in an element, an example or a fake |

The per-service login behind the security scheme is "the rwb-partner login (DP-02)" and is not part of this baseline. The partner gateway of the DMZ (FAPI 2.0) fronts this service for the partner identities and the field application, and it is the edge's, not this baseline's.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Field-work element | `FieldWorkResult`: `instructionId` (DF-PRT-008), `result`, `resultCode` (DF-PRT-015) and `status` (DF-PRT-014), `visitedOn`, `documents` and `ruleVersion` |
| Identity elements | `partner_user` over DF-REF-212 to DF-REF-217: `id`, `identityRef`, `partnerId`, `roleCode` over LOV-ROLE, `validFrom` and `validTo` |
| Firm element | `Partner` over DF-PRT-001 to DF-PRT-007, published unchanged by the baseline of RWB-S9-E6033-CON |
| Required flags | `instructionId`, `result` and `visitedOn` required; `instructionId` read-only; `status` read-only in the answer; `documents` optional and repeatable; the other properties optional |
| Lists | LOV-INSTR-STATUS, LOV-INSTRUCTION, LOV-PANEL and LOV-PARTNER-TYPE, copied from TSD S9 T3.2; LOV-ROLE read from rwb-access |
| Event data | EV-21 `PartnerResultSubmitted`: `instructionId`, `result`, `documents` and the submitted time, with the case as key (§12.3, §12.4) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the answer, with the rule ID and the version in force (DP-03) |
| Consumed facts | DF-INT-001 to DF-INT-013 of `interaction` in P1 with channel `VISIT` and source `FIELD_VISIT`; the `document` of P5 with its type and its index; DF-REF-001 to DF-REF-015 of `rule_row` in P7 read as values |
| Case fact | DF-CAS-001 to DF-CAS-023 of `recovery_case` in P3: the case reference arrives on the instruction and leaves as the event key, and no property of it is declared |
| Consumed fields with no source | The three operation names, the document reference and its media types, the result vocabulary and the rule ID with its version: Not specified in the source documents (GAP-3136; ASM-5491, ASM-5493, ASM-5494, ASM-5496, ASM-5502) |
| Not declared here | `document` (P5), `interaction` (P1), `recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `notice` (P6), `payment` (P8) |

The field-level types, lengths and required flags of the declared properties are those of TSD S9 T3.1 and LDM v8; this story fixes the element name, the required flags of AC2, the free-value rule of BR4 and the optionality rule of BR11. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13). One operation and one element, declared additively inside the baseline of RWB-S9-E6033-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/partner/instructions/{instructionId}/results` (API-S9-005) | Multipart: `result` as a `FieldWorkResult` JSON part and `files` as one or more claims; `PartnerInstruction` out with the result, the status and the document references | Partner portal, right U, scope applied | `Idempotency-Key` header |
| GET | `/partners` (API-S9-001) | `Partner[]` out over the query type and status; declared here only as the read behind SCR-35 and not changed | Partner portal, right R, scope applied | Not applicable |

API-S9-005 and API-S9-001 keep the paths, the operation IDs, the answer element names, the rights and the error codes of TSD S9 T-A.1 and T-A.2; this baseline adds the `FieldWorkResult` part and changes no existing property, no error code and no right. The errors are 400, 401, 403 with MSG-P4-002, 404 for an instruction outside the caller's firm, 409 for a closed instruction, 415 for an undeclared media type, 422 with MSG-GEN-001 and 503, each with the envelope of section 14. What has no source is the result vocabulary, the document reference and the media types, and each carries the placeholder (GAP-3136; ASM-5491, ASM-5494, ASM-5502). API-S9-003, API-S9-004 and API-S9-006 belong to the instruction, acceptance and invoice stories and are neither built nor narrowed here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The interaction entry of the visit (operation name Not specified in the source documents (GAP-3136; ASM-5493)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | One ledger entry with channel `VISIT`, source `FIELD_VISIT`, the case, the firm and the contact date; answers its reference; faked |
| The document intake of the photographs and the bills (operation name Not specified in the source documents (GAP-3136; ASM-5491)) | `/api/recovery/document/v1` | P5 rwb-document | The claim-check intake and the index of each photograph and each bill; answers a document reference; faked |
| The rule in force (operation name Not specified in the source documents (GAP-3136; ASM-5496)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule ID and the version at their effective date, read as values; faked |

The three rows are one hop with a 2 s timeout, a breaker per downstream and a retry in the client's queue (ADR-020). They are contract dependencies of class C that the plan's C row does not carry, and DP-18, DP-05 and DP-09 are absent from the pattern set of the key; the absence is recorded (GAP-3136; ASM-5491, ASM-5493, ASM-5496).

#### 12.3 Events published

| Event | Topic and name | Key and envelope | Payload | Declared for |
|---|---|---|---|---|
| EV-21 `PartnerResultSubmitted` | `rwb.partner.events.v1`; `rwb.partner.PartnerResultSubmitted.v1`, CloudEvents 1.0 binary, schema `rwb_partner_partner_result_submitted` | Key and subject: the case ID; `ce_source` rwb-partner; `ce_id` and the W3C trace context | `instructionId`, `result`, `documents`, the submitted time | API-S9-005 on the field-app path, whose behaviour is RWB-S9-E7018-APP; rwb-case and rwb-reporting consume it |

The retry and `.dlt` topics are the platform's (DP-14), and the outbox that relays the event is the DP-09 dependency the plan does not carry. Event and Messaging Design v5 reads EV-21 as consumed from the partner portal while TSD S9 T5.3 lists it as published; the baseline declares one direction, records the conflict and declares no second topic and no event of the visit (GAP-3136; ASM-5495).

#### 12.4 Events consumed

None. A visit arrives by the REST operation and the client's queue, not on a topic, and the FSD declares no background event for the feature (FSD S9 A2.15.4.4). This baseline declares no consumer group, no subscription and no inbox row.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, one execution per partner instruction; the field-work step rides it | `rwb-partner` in namespace `rwb-recovery` | The `resultSubmitted` signal with the instruction and the submission reference; the stage outcome returns to `CaseWorkflow` |
| `recordFieldWorkResult` | Activity, declared and not registered by this story | `rwb-partner` | The instruction, the caller's binding, the result, the file claims and the rule version in; the result, the status, the document references and the record reference out |
| the stage outcome for the parent | Parent-child workflow edge to `CaseWorkflow` | `rwb-case` | The result and the document count as the stage result; no REST row is declared for the case move |

The service owns one workflow and no job in the context pack's ownership rows, and TSD S9 T4 gives it no case state machine of its own, so the case stage and its clock stay with rwb-case. The activity and signal names are a target design choice fixed by no source document.

#### 12.6 Schedules

None. The service owns no job in the context pack's ownership rows (Jobs: None), the submission is started by the collector's client, and the offline queue and the upload on reconnect of NFR-062 are the field application's. This baseline therefore declares no Temporal Schedule, no Quartz row, no shared job table and no batch table.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| partner | S9 (`rwb_partner`) | The firm, its code, its name, its type, its panel status, its contract end and its score; read by the element |
| partner_instruction | S9 (`rwb_partner`) | The work placed with a firm on a case with its type, its due date, its status, its result and its fee; the table the element is drawn from and the row the answer returns |
| partner_user | S9 (`rwb_partner`) | The firm's identities bound to one firm and one role over LOV-ROLE, with their validity (DF-REF-212 to DF-REF-217); read to scope the caller |
| decision_record | PLT library, created in `rwb_partner` | The local hash-linked record of the field work (DP-03) |
| idempotency_key | PLT library, created in `rwb_partner` | The key of API-S9-005 and the answer it holds |
| outbox_event, processed_event | PLT library, created in `rwb_partner` | The relay of EV-21 and the inbox guard |

`document` (P5), `interaction` (P1), `recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `notice` (P6) and `payment` (P8) are not owned by this baseline; it names them only as consumed answers or another story's data, and no foreign key leaves the schema (DP-01). No visit table and no evidence column is declared: neither exists in S9 (ASM-5491, ASM-5493).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-document intake fake | A document reference and an index entry per photograph and per bill claimed | AC3, AC6 |
| rwb-source-data ledger fake | An accepted visit entry with its reference, channel `VISIT` and source `FIELD_VISIT` | AC3, AC6 |
| rwb-decision rule fake | The rule ID and the version in force at the effective date, and a missing-version answer | AC2, AC3, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC6 |
| Partner gateway and gateway-bff fakes | The firm scope of the caller from `partner_user`, and the merged SCR-35 panel answer | AC5, AC6 |

The fakes are test-only and are replaced by the real services in SIT. The three operation names, the document reference, the media types, the result vocabulary and the rule pair carry the placeholder until their owners confirm them (GAP-3136; ASM-5491, ASM-5493, ASM-5494, ASM-5496, ASM-5502).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | API-S9-005 with its field-work element and API-S9-001 on `/api/recovery/partner/v1`; the ledger entry of rwb-source-data, the document intake of rwb-document and the rule read of rwb-decision; one hop, 2 s |
| Kafka | 1 published, 0 consumed | `rwb.partner.PartnerResultSubmitted.v1` on `rwb.partner.events.v1`, keyed by the case; no second topic; the decision record rides `rwb.decision-record.v1` |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `InstructionWorkflow` and `recordFieldWorkResult` on `rwb-partner`; the stage outcome to `CaseWorkflow` on `rwb-case`; no Schedule and no job |
| File | None built or delivered | The photographs and the bills are claim-check claims handed to rwb-document; the baseline declares no file path and no manifest of its own |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no instruction, no document and no ledger entry. What it publishes is one additive element, nine contract tables and five fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is declared as the element of the record written before the answer. DP-13 moves the base of the legacy `/api/recovery/v1` paths and gives the result operation its home. DP-19 sits behind SCR-35, whose screen model is the edge contract's and whose partner side is the partner gateway. DP-18, DP-05 and DP-09 are not in the pattern set: the ledger of rwb-source-data, the ACE data rule and the outbox are declared as consumed rows and an event shape rather than as pattern rows (GAP-3136; ASM-5491, ASM-5493, ASM-5495).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan carries for the app story and not for a CON story with no H row. The three consumed rows of §12.2 are class C dependencies in fact and the plan's C row is empty, so they are built against their documents and fakes on Day 1 with the placeholder.

**Deliverables and build steps**

1. Write the `FieldWorkResult` element on API-S9-005 and validate the additive rule of AC1 in the pipeline.
2. Write the properties, the required flags, the four lists and the free-value rule for `resultCode` of AC2.
3. Write the document and visit references and the rule pair, with their placeholders, and record the three consumed rows of AC3.
4. Record the event of AC4 with its envelope, its key, its payload and the direction conflict.
5. Record the rights and the error envelope of AC5, with 415 and the 13 holders of U.
6. Record the decision-record element of AC6 and validate it against the library schema.
7. Publish the five fakes of AC6 and the drift test.
8. Record the naming baseline, the tables owned and the absence tests of AC7, then tag the baseline and collect the consumer sign-off.

The deliverables are `openapi/rwb-partner-v1.yaml` with the added element, the contract README rows for the three consumed rows and their placeholders, and the five fakes of 12.8.

**Done when.** The OpenAPI document validates in the pipeline against the OpenAPI 3.1 schema and against the baseline of RWB-S9-E6033-CON, the ten contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, PRT-02, the field application and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required property of the element is absent or invalid, a part of the multipart body is unformed, or the rule version is not in force | Enter {field}. |
| MSG-P4-002 | The role lacks the Partner portal right U the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the answer leaves the service | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| the refusal of a closed instruction | The instruction is `DONE`, `DECLINED` or `RECALLED` and the operation answers 409 | Not specified in the source documents (GAP-3136; ASM-5500) |

The three IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. The fourth row is the 409 of the app story's X3 and has no message in any source, so it carries the placeholder.

### 15. Screens and states

The contract serves PRT-02 Instruction in its five legacy states — `New`, `accepted`, `in progress`, `result` and `closed` — through the partner gateway of the DMZ (FAPI 2.0) on the caller's firm scope, and SCR-35 Placement and allocation in its list state through the gateway-bff composite route (DP-19). The route calls rwb-partner for the firm, its panel status and its score and rwb-case for the case and its stage; this baseline fixes the rwb-partner answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The legacy screen table gives SCR-35 "Loading; list" and PRT-02 "New; accepted; in progress; result; closed", so PRT-02 is the instruction screen with a result state and neither screen is a visit form with a field list. The offline state, the form fields, the offline indicator and the words of the `result` and `closed` states are described by no source and carry the placeholder (GAP-3136; ASM-5497, ASM-5501). The refusal, the media-type, the bad-value and the not-recorded states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-018-01 | AC1, AC2 | Contract | The `FieldWorkResult` element over `INS-000318` of `PRT-0007`; the contract half answers the multipart rule, the required flags, the four lists and the free `resultCode` |
| TC-E7-018-02 | AC3, AC6 | Contract | The three consumed rows with their placeholders and fakes; the contract half answers the decision-record element and the MSG-P7-003 path |
| TC-E7-018-03 | AC5 | Contract | A role without right U, a caller of another firm and an undeclared media type; the contract half answers 403 with MSG-P4-002, 404 and 415 |
| TC-E7-018-04 | AC3, AC7 | Contract | The boundary and the absence of a new operation, of a visit table, of an evidence column, of a `v_ace_*` read, of a document write, of a Schedule and of a job |
| TC-S9-E7018-CON-01 | AC1 | Contract | The document validates; the one operation, its multipart parts, the `Idempotency-Key` and the eight error answers are present, and the change is additive |
| TC-S9-E7018-CON-02 | AC2 | Contract | The element validates with its seven properties, its three required properties, the four lists and the free `resultCode`; no evidence property |
| TC-S9-E7018-CON-03 | AC3 | Contract | The three consumed rows and their placeholders; the no-`v_ace_*`, no-document, no-interaction, no-case and no-rule-row boundary |
| TC-S9-E7018-CON-04 | AC4 | Contract | EV-21 with its topic, envelope, key and payload; the one declared direction and the recorded conflict; no second topic and no consumed event |
| TC-S9-E7018-CON-05 | AC5, AC6 | Contract | The rights, the 13 holders of U, the 29 holders of R, the eight error codes, the decision-record element and the five fakes against the library schema |
| TC-S9-E7018-CON-06 | AC6, AC7 | Contract | The drift test fails on a drifted fake; the naming baseline, the tables owned, the property sources against TSD S9 T3.1 and LDM v8, and the absence of a Schedule and a job |

The four legacy cases are those of RWB-E7-018 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S9-E7018-APP. The legacy level maps to `Contract` here because the artefact under test is the contract. The six cases `TC-S9-E7018-CON-01` to `-06` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the key has no integration slice.

### 17. Guardrails

- No business value in the contract: the instruction, panel, partner type and role lists, the result vocabulary, the rule ID and its version stay reference data, lists and rule values, never a schema default, a member taken from no source or a constant of the code.
- No personal data in a schema, an example or a fake: identifiers, codes, list values, dates, a count of documents, a rule ID and a version only, and every example is synthetic.
- ACE data only through the owner's contract: the document declares no `v_ace_*` path, no `v_ace_*` property and no ACE table, and this service holds no `v_ace_*` grant.
- The evidence stays with rwb-document: the document declares no document body, type, index entry or retention, and the reference carries no field ID (BR2).
- The visit stays with rwb-source-data: the document declares no visit table, no interaction property and no channel value of the code (BR2).
- The case stays with rwb-case: the document declares no `recovery_case` property, no case write and no Schedule.
- The rule rows stay with rwb-decision: the document declares no rule row, package or rule ID set (BR3).
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-partner; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence tests fail a build that adds a visit table, a second topic, a Schedule, a Quartz row or a job.
- The error envelope, the multipart rule, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S9-009 | Field work and its evidence reach the case through the field application (Should, E7) | The field-work element, the three consumed rows, the event and the record element | TC-E7-018-01, TC-S9-E7018-CON-01, TC-S9-E7018-CON-02 |
| REQ-DCM-013 | Field photographs and bills reach the same intake and index as scanned documents (Should, E2) | The document claim and the rwb-document fake | TC-S9-E7018-CON-03 |
| REQ-S9-008 | Partners exchange data through the partner portal and the external gateway, and not by email | The partner portal access of the operation and the partner gateway | TC-S9-E7018-CON-05 |
| NFR-062 | The field application captures evidence with no network connection and uploads when it reconnects | The `Idempotency-Key` rule of the operation and the repeat answer | TC-S9-E7018-CON-01 |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login | TC-S9-E7018-CON-06 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The envelope and the topic of EV-21 | TC-S9-E7018-CON-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows with their budget and breaker | TC-S9-E7018-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element | TC-S9-E7018-CON-05 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-018, disposition Split (rework); feature FEAT-PRM-15 |
| Legacy criteria | AC1 and AC2 are owned word for word by RWB-S9-E7018-APP; this baseline copies none of them |
| Wave and release | Wave 4 and release 31 May 2027 (tentative), copied unchanged from the plan; EP07 is wave 4 and the service's Arch v5 wave is 4, so the W-MAP wave is not earlier and no conflict is raised (ASM-5499) |
| Source text | Legacy RWB-E7-018; FSD S9 Partner management v3 A1.2, A1.4, A2.15, A2.15.2, A2.15.3.1 to A2.15.3.3, A2.15.4, the Screens table and Requirements served; TSD S9 Partner management v2 T1, T2, T3.0, T3.1, T3.2, T3.3, T4, T5.1, T5.2, T5.3, T6.1, T6.2 and T-A; Business Rules and Routing Logic v4 rows R-UNI-38 to R-UNI-40; LDM v8 `partner_user`, `interaction`, LOV-CHANNEL, LOV-CONTACT-SRC and LOV-ROLE; Event and Messaging Design v5 event EV-21; Program BRD v4 rows REQ-S9-009, REQ-DCM-013 and NFR-062 |
| Test cases | The four legacy cases as the contract half, and the six new contract cases TC-S9-E7018-CON-01 to -06 |
| Feature and screens | FEAT-PRM-15, PRT-02 Instruction and SCR-35 Placement and allocation |
| Rules | No partner route set exists; R-UNI-38 to R-UNI-40 are the nearest rows, and the rule ID and version carry the placeholder (ASM-5496) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the element, the scope, the state guard, the record and the three calls: RWB-S9-E7018-APP.
- The portal result intake of the same operation and its own element: RWB-S9-E6033-APP and RWB-S9-E6033-CON, whose baseline this document adds to and changes nothing of.
- The instruction, acceptance, override and invoice operations of the same base: RWB-S9-E6031-APP, RWB-S9-E6032-APP, RWB-S9-E6034-APP and RWB-S9-E6035-APP.
- The document hub, its types, its index, its retention and its OCR: rwb-document (P5), whose intake is declared as consumed and faked.
- The interaction ledger, its channel and source lists and its deduplication: rwb-source-data (P1), whose entry is declared as consumed and faked.
- The case of record and its clock: rwb-case (P3). The `decision_log_entry` ledger, the rule rows and the packages: rwb-decision (P7).
- The operation names, the document reference, the media types and the result vocabulary: their owners confirm them at the baseline review and the placeholder stands until then (GAP-3136; ASM-5491, ASM-5493, ASM-5494, ASM-5502).
- The direction of EV-21 beyond the one the baseline declares: the event catalogue and TSD S9 T5.3 disagree and the conflict is recorded (GAP-3136; ASM-5495).
- The offline behaviour, the devices and the non-functional targets of the field application, NFR-062 and NFR-063 being Proposed under DL11 (ASM-5501).
- The scorecard, the panel as reference data and the partner review: RWB-S9-E7011-APP, RWB-S9-E6030 and RWB-S9-E7013-APP. The contract end and the recall: RWB-S9-E7015-APP.
- The gateway-bff composite route, the partner gateway and the screen field lists of SCR-35 and PRT-02: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
