# RWB-P6-E1046-CON Template and merge field catalog as data

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E1046-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Contract version | v1 (base `/api/recovery/comms/v1`, OpenAPI 3.1) |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-046 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP07, DP11, DP13, DP15, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement (DOR-RWB-P6-E1046-CON-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E1043-CON (DP-07, rwb-case reference-data contract); RWB-PLT-N001-CON (DP-19); DP-15 platform contract story: Not specified in the source documents (GAP-2344) |
| Integration dependencies | None |
| External dependencies | None |
| Open decisions | DL10 (ASM-2250, ASM-2357, ASM-2377, ASM-2863); DL28 (ASM-1861, ASM-1925, ASM-2093, ASM-2727); both still open |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (FR-P6-001, FR-P6-002, FR-P6-003, FR-P6-004, FR-P6-005, FR-P6-006, FR-P6-007, FR-P6-008, FR-P6-009, FR-P6-010, FR-P6-011, FR-P6-012, FR-P6-013, FR-P6-014) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-046 for rwb-comms. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P6-E1046-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 17 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the template and merge field catalog of `rwb-comms` — the five admin template operations on base `/api/recovery/comms/v1` with their `Template`, `TemplatePage`, `TemplateApproval` and `TemplateWithdrawal` shapes, the template and merge-field state rules, the merge-field catalog version in force, the error envelope with its message IDs, the `Idempotency-Key` rule, the two consumed reads with their owner and the contract fakes**, so that **the app, test and integration stories of this legacy key build against a fixed, testable contract on Day 1 and a version state, an approval field or a catalog version can never drift between rwb-comms, rwb-case and rwb-source-data without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). Legacy RWB-E1-046 exposes its catalog as an in-process `TemplateCatalog` interface inside one module, with the load path owned by another module, and its state, its approval columns and its catalog version are read by the letter engine of RWB-P6-E1052, by the dispatch stories of wave 2 and by the integration harness of wave 1. Those are exactly the values most likely to drift silently: an approval field renamed, a state spelled differently in an answer than in a check, a catalog version that a load silently replaces, or a refusal that returns 200 with an empty page.

The baseline fixes the names the checks require: schema `rwb_comms`, REST base `/api/recovery/comms/v1`, topic `rwb.comms.events.v1`, task queue `rwb-comms` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.comms`. It records that this key publishes none of the service's three notice events, because a template load, an approval or a withdrawal is a synchronous answer and never a notice. It also records what the sources leave open: the exact request and answer field names of the five operations, the approver identity type on the file, where the body object lives, and the data-dictionary read of rwb-source-data, which has no contract dependency in the plan. Each of those is a placeholder and a gap row, never a guess `Not specified in the source documents (GAP-1067; ASM-2015)`.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, topic, event and queue names follow the platform rule rather than a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope, the `Idempotency-Key` rule and the retry and `.dlt` topic convention are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); where this document narrows them it does so explicitly.
- The rwb-case reference-data contract RWB-P3-E1043-CON is published, so the LOV read this catalog consumes has one owner document and one fake.
- The TSD P6 appendix T-A.1 and T-A.2 are in force for API-P6-003 to API-P6-007, and the template and merge_field definitions of TSD P6 T3.1 and the lists of T3.2 are in force for the shapes and the values.
- The Ownership Map is the only source of owners: `template` and `merge_field` are P6's in `rwb_comms`, `lov_value` is P3's, `sys_fields` is P1's, `signature_request` and `document` are P5's and `decision_log_entry` is P7's.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of `rwb-comms` with the five admin template operations, the four resources of section 11 and the error responses of T-A.2.
2. Fix the state spelling and the state rules: Draft is created by upload, Approved and Withdrawn are reached only through the approve and the withdraw operation, and a version is current only when it is Approved and its valid-from date has arrived.
3. Fix the merge-field catalog shape and the meaning of the version in force, so two consumers never read a different catalog for the same business date.
4. Record the two consumed reads with their owner, their use and the 2 s budget, and map every failure to the error envelope and a message ID; carry the missing contract dependency of the data-dictionary read as a gap row.
5. Record the `Idempotency-Key` rule on the three POSTs and state the stored-answer behaviour of a repeat.
6. Record the event position: this key publishes none of `rwb.comms.NoticeGenerated.v1`, `rwb.comms.NoticeDispatched.v1` and `rwb.comms.NoticeDelivered.v1`, and consumes no topic.
7. Publish the nine contract tables of section 12 and the contract fakes of section 12.8.
8. Add the contract tests: schema validation, the state values, the catalog version, the error mapping, the idempotency rule, the drift between a fake and the document, and the absence of a notice event in this key.
9. Tag the baseline and hand it to RWB-P6-E1046-APP, the dispatch stories of wave 2 and the wave 1 harness RWB-ITG-E1046-ITG.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | MSG-GEN-001 | AC1 |
| X2 | A state value is spelled differently in the document and in a check | The contract test fails; the change needs a corrected document, not a new spelling | None | AC2, AC7 |
| X3 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X4 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC8 |
| X5 | The data-dictionary read path has no contract dependency in the plan | The row carries the gap and the assumption, and the fake is derived from the published data-dictionary document | None | AC6 |
| X6 | A notice event is declared as published by this key | The absence test fails: no `rwb.comms.NoticeGenerated.v1`, `NoticeDispatched.v1` or `NoticeDelivered.v1` on a template load or an approval | None | AC8 |
| X7 | A field-level definition is missing from the source material | The field is marked with the placeholder and one gap row is carried | None | AC2, AC3, AC5 |

### 6. INVEST check

| Criterion | Verdict | Note |
|---|---|---|
| Independent | Pass | No build dependency; reads the platform envelopes, the TSD P6 appendix, the Ownership Map and the rwb-case reference-data contract only |
| Negotiable | Pass | The field-level names are settled with the consumers; the five operations, the state values, the catalog version and the two consumed reads are fixed by the target architecture |
| Valuable | Pass | Unblocks the app story of this legacy key, the notice story of wave 1 and the wave 1 harness on Day 1 |
| Estimable | Pass | One document, four resources, five operations, two consumed reads, nine contract tables and four fakes |
| Small | Pass | Fits one sprint with the contract tests |
| Testable | Pass | Every criterion in section 7 is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the template and merge field catalog of rwb-comms

  Background:
    Given the service naming rule of the platform library is in force
    Given the template and merge_field definitions of TSD P6 T3.1 and the lists of TSD P6 T3.2 are in force
    Given the rwb-case reference-data contract RWB-P3-E1043-CON is published with its fake

  Scenario: AC1 The five admin operations are declared with their request and answer shapes (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-comms is published with this baseline
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /admin/templates, POST /admin/templates, GET /admin/templates/{templateId}/content, POST /admin/templates/{templateId}/approve and POST /admin/templates/{templateId}/withdraw, all under the base /api/recovery/comms/v1 and owned by rwb-comms
    Then the list operation answers TemplatePage and the upload operation answers Template
    Then the approve operation takes TemplateApproval and answers Template, and the withdraw operation takes TemplateWithdrawal and answers Template
    Then the content operation answers the binary named by bodyRef
    Then each operation names its Documents right of T6.1 and its error statuses of T-A.2
    Then the three POSTs declare the Idempotency-Key header and the two GETs declare none
    Then POST /cases/{caseId}/notices and GET /notices/{noticeId} are declared as the operations of RWB-P6-E1052-CON and not as part of this baseline

  Scenario: AC2 The Template resource fixes the version, the state and the approval fields (new, D-RCV-60)
    Given the Template resource declared in the document
    When it is compared with the template fields of TSD P6 T3.1
    Then it carries id, templateCode, templateVersion, language, productGroup, bodyRef, approvedByLegal, approvedBy, approvedAt, validFrom, channel, noticeType, signatureBasis, mergeCodes and state
    Then id, templateCode, templateVersion, language, bodyRef and approvedByLegal are required and every other property is optional, so a consumer of the previous version keeps working
    Then state is one of "Draft", "Approved" and "Withdrawn", and the document states that the stored values are DRAFT, APPROVED and WITHDRAWN
    Then approvedBy, approvedAt and validFrom are present when state is "Approved" and the document states that a version with an incomplete approval is refused
    Then the resource carries no template body and no merge value

  Scenario: AC3 The MergeField resource and the catalog version in force (new, D-RCV-60)
    Given the MergeField resource and the catalog-version element of the document
    When they are compared with the merge_field fields of TSD P6 T3.1
    Then MergeField carries id, mergeCode, sourceEntity, sourceField, fieldId, isRequired, personalData, catalogVersion and validFrom
    Then mergeCode is unique within one catalogVersion and catalogVersion with validFrom names the version in force on a business date
    Then exactly one catalogVersion is in force on a business date, and a refused or repeated load leaves the version already in force unchanged
    Then the fixture in force is "MF-2026.11" with merge codes "CASE_NO", "CUSTOMER_NAME", "POSTAL_ADDRESS", "TOTAL_OUTSTANDING" and "NOTICE_DATE"
    Then fieldId names a BR Field ID and the document states that every fieldId is checked through the rwb-source-data data-dictionary contract

  Scenario: AC4 The error envelope and the message mapping (new, D-RCV-60)
    Given the error responses declared for the five operations
    When each status is compared with T-A.2 and section 14
    Then the two GETs answer 401, 403 and 503, and the content operation also answers 404
    Then the upload answers 401, 403, 413, 415, 422 and 503
    Then the approve and the withdraw answer 401, 403, 404, 409, 422 and 503
    Then every error carries the platform envelope with the message ID of the condition: MSG-GEN-001 for a missing required field, MSG-P6-006 for an unknown merge code, MSG-P1-002 for a failed catalog check or a repeated load, MSG-P6-005 for a template with no Approved version and MSG-P6-003 for a withdrawn version
    Then a refusal returns no partial page, no version and no body

  Scenario: AC5 The Idempotency-Key rule on the three POSTs (new, D-RCV-60)
    Given the upload, the approve and the withdraw operation of the document
    When the rule of each is reviewed
    Then each requires the Idempotency-Key header and answers the first stored answer to a repeat with the same key
    Then a repeat with the same key creates no second version, no second approval and no second withdrawal
    Then the two GETs declare no Idempotency-Key and are answered from the version in force

  Scenario: AC6 The two consumed reads carry their owner, the 2 s budget and the fake (new, D-RCV-60)
    Given the consumed operations of the document
    When they are compared with the Ownership Map
    Then GET /api/recovery/case/v1/admin/lists/{listCode} names P3 rwb-case as its owner, for LOV-LANG, LOV-PRODUCT, LOV-NOTICE and LOV-CHANNEL
    Then GET /api/recovery/source-data/v1/admin/data-dictionary/fields names P1 rwb-source-data as its owner, for the BR Field ID check
    Then the data-dictionary row carries the missing-dependency gap of the plan (GAP-1064; ASM-2012)
    Then every consumed row states one hop, the 2 s timeout, the GET retry once with jitter and the breaker per downstream
    Then every failure of a consumed call maps to MSG-GEN-006 naming the system that failed and never to an accepted load

  Scenario: AC7 The state rules of a template version are fixed by the contract (new, D-RCV-60)
    Given the state rules declared in the document
    When they are compared with the operations of AC1
    Then a version created by the upload is "Draft" and is never a current version
    Then "Approved" is reached only through the approve operation, which records approvedBy, approvedAt and validFrom
    Then "Withdrawn" is reached only through the withdraw operation, which records a reason and leaves the version readable
    Then a version whose validFrom is in the future leaves the earlier Approved version current until that date
    Then a template whose only Approved version is Withdrawn has no current version, and the refusal names MSG-P6-003
    Then no notice state and no case state is declared by this contract

  Scenario: AC8 The four fakes match the document and no notice event is declared (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then 12.3 and 12.4 record None and state that rwb.comms.NoticeGenerated.v1, NoticeDispatched.v1 and NoticeDelivered.v1 are published by the notice path of RWB-P6-E1052 and not by this key
    Then the four fakes of 12.8 answer the operations of 12.1 and the two reads of 12.2 with the values of the fixtures
    Then the contract tests compare each fake with the document and fail on any drift
```

The eight criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by RWB-P6-E1046-APP. The legacy AC1 to AC8 of RWB-E1-046 are owned by RWB-P6-E1046-APP; the wave 1 harness RWB-ITG-E1046-ITG consumes this baseline and copies none of these criteria.

Scenario: AC9 The contract meets rules BR7, BR8, BR9, BR10, BR12, BR13 and BR14 (new, D-RCV-60)

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A template version is used only when its state is Approved and it carries the Legal approver and approval date | RWB-E1-046 BR1; REQ-OCC-002; CTL-14 |
| BR2 | The current version for a template code and language on a date is the Approved version with the highest version number whose valid from is on or before that date | RWB-E1-046 BR2; R-LIT-03 (template_status = current) |
| BR3 | A withdrawn version has no current version, and generation holds until Legal approves a new one | RWB-E1-046 BR3; R-LIT-04, R-LIT-06 |
| BR4 | Every merge code a template uses exists in the catalog version in force, and every catalog row names a BR Field ID in the data dictionary | RWB-E1-046 BR4; REQ-OCC-001; Principle 1 |
| BR5 | A load with any refused row is refused in full and the previous version, or the previous catalog version, stays in force | RWB-E1-046 BR5; refdata change process, step 3 |
| BR6 | Earlier versions are never changed or deleted; open cases keep the version they were generated under | RWB-E1-046 BR6; refdata change process, step 6; R-UNI-38 |
| BR7 | Templates are owned by Legal counsel as reference data, and the approver named on a version is that authority | RWB-E1-046 BR7; DL28 |
| BR8 | One REST base per service: `/api/recovery/comms/v1`; the document never declares another service's path as provided | DP-13; Architecture v5 slide 41 notes |
| BR9 | Error responses use one envelope and one message ID per condition; the business message texts are copied unchanged from the legacy story | Architecture v5 platform baseline; Template and Rules §R7.2 s14 |
| BR10 | A schema change is additive within a major version; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR11 | A GET declares no Idempotency-Key; a POST declares it and stores its answer, so a repeat with the same key creates nothing | Architecture v5 slide 11; DP-09 |
| BR12 | The document lists only operations owned by rwb-comms; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-01 |
| BR13 | This key publishes no notice event: `rwb.comms.NoticeGenerated.v1`, `rwb.comms.NoticeDispatched.v1` and `rwb.comms.NoticeDelivered.v1` belong to the notice path and the dispatch stories | TSD P6 T5.3; Architecture v5 slides 17 and 42; section 7 AC8 |
| BR14 | No business value is fixed in the contract: template codes, merge codes, languages, field IDs, dates and the catalog version stay data rows of the load files | Template and Rules §R7.2 s17; RWB-E1-046 section 17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| (none) | `POST /admin/templates` | The upload carries template code, language, bodyRef and every merge code exists in the catalog version in force | Draft, with the next version number for the code and language |
| Draft | `POST /admin/templates/{templateId}/approve` | `TemplateApproval` carries the approver and a valid-from date | Approved, with approvedBy, approvedAt and validFrom recorded |
| Draft | `POST /admin/templates/{templateId}/withdraw` | A draft version is withdrawn before it was ever current | Withdrawn, readable, never a current version |
| Approved | `POST /admin/templates/{templateId}/withdraw` | `TemplateWithdrawal` carries a reason | Withdrawn; no current version remains while no later Approved version exists, and the refusal names MSG-P6-003 |
| Approved | a later version is approved with a validFrom on or before the business date | The later version has the higher version number | Approved, readable, no longer current |
| Withdrawn | (no transition) | A withdrawn version is never returned to Draft or Approved; Legal approves a new version instead | Withdrawn, readable |

| Baseline state | Event | Condition | Next state |
|---|---|---|---|
| Draft | Review opened | The five operations, the four resources and the two consumed reads are described | In review |
| In review | Consumer sign-off | The app story, the notice story and the wave 1 harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new optional catalog field | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake or a retired element returns | A contract test fails | In review |

The merge-field catalog version moves only when a catalog load is accepted: the accepted catalogVersion becomes the version in force from its validFrom, the earlier one stays readable, and a refused or repeated load leaves the version in force unchanged (BR5). No notice state and no case state is declared or changed by this contract.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-comms | Owns the OpenAPI document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the plan's contract-dependency list for the data-dictionary read |
| Consuming teams (the app story, the notice story of wave 1, the dispatch stories of wave 2, the wave 1 harness, and the rwb-case and rwb-source-data owners) | Review and sign off the parts they consume |
| RW-LEGAL, Legal counsel | Confirms that the approve and the withdraw operation carry the Legal authority the legacy story gives them (Documents A) |
| RW-REFADM, reference data administrator | Confirms that the upload carries the reference-data authority the legacy story gives it (Documents C) |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the `Idempotency-Key` rule and the naming rule this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer and no merge value is carried |

The per-service login name behind the document's security scheme is not part of this baseline; the document names the scheme "the rwb-comms login (DP-02)" and the name is Not specified in the source documents (GAP-1068; ASM-2016). The declared area and right of each operation are enforced at gateway-bff (DP-19); the service itself refuses a request whose declared right is absent with the status and message Not specified in the source documents (GAP-1068) from its own operation configuration; no rwb-access contract is declared here.

### 11. Data

The contract baseline declares shapes, not business values. The catalogue is owned by rwb-comms (P6) and other stories read it only through these operations, never as a table. The field-ID check is answered by the P1 rwb-source-data data-dictionary contract. bodyRef is an opaque reference that this contract does not resolve; the body location rule is Not specified in the source documents (GAP-1065).

| Item | Content | BR Field ID |
|---|---|---|
| Template | id, templateCode, templateVersion, language, productGroup, bodyRef, approvedByLegal, approvedBy, approvedAt, validFrom, channel, noticeType, signatureBasis, mergeCodes, state, from template DF-REF-045 to DF-REF-051 and DF-REF-063 to DF-REF-069 | DF-REF-045 to DF-REF-051 and DF-REF-063 to DF-REF-069 |
| TemplatePage | The paged answer of the list operation: the page items as Template and the page metadata the platform convention fixes; the page field names are Not specified in the source documents (GAP-1067; ASM-2015) | Not specified in the source documents (DOR-RWB-P6-E1046-CON-7) |
| TemplateApproval | The request of the approve operation: approvedBy, approvedAt and validFrom, and the reason when a consumer asks for one; the exact field set is Not specified in the source documents (GAP-1066; ASM-2014) | Not specified in the source documents (DOR-RWB-P6-E1046-CON-7) |
| TemplateWithdrawal | The request of the withdraw operation: the reason of the withdrawal; the field name and the allowed reasons are Not specified in the source documents (GAP-1067; ASM-2015) | Not specified in the source documents (DOR-RWB-P6-E1046-CON-7) |
| MergeField | id, mergeCode, sourceEntity, sourceField, fieldId, isRequired, personalData, catalogVersion, validFrom, from merge_field DF-REF-252 to DF-REF-260 | DF-REF-252 to DF-REF-260 |
| Entity and field registry answer | The BR Field ID set of rwb-source-data, read through its contract and never copied | Not specified in the source documents (DOR-RWB-P6-E1046-CON-7) |
| List values | LOV-LANG, LOV-PRODUCT, LOV-NOTICE, LOV-CHANNEL and LOV-SIGNATURE-BASIS, read through the rwb-case reference-data contract and never copied | Not specified in the source documents (DOR-RWB-P6-E1046-CON-7) |

Every example in the document is synthetic and uses the legacy values: template "DEMAND-MTG", language "TH", versions 1 and 2, the dates 2026-10-01, 2026-11-10, 2026-11-20, 2026-11-30 and 2026-12-01, and the catalog version "MF-2026.11". The approver identifier on a file is a staff identifier such as "LEG-0001"; the field is a USER_REF of type uuid in TSD P6 T3.1 and the conversion of the file value to the uuid is Not specified in the source documents (GAP-1066; ASM-2014).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`.

| Method | Path | API ID | Documented shape | Access | Idempotency |
|---|---|---|---|---|---|
| GET | `/admin/templates` | API-P6-003 | Query: code, language, state, page, size, and the current-version filter by code, language and on-date (parameter name Not specified in the source documents (GAP-1067)); answer `TemplatePage` | Documents R | Not applicable |
| POST | `/admin/templates` | API-P6-004 | Multipart: file, templateCode, language, productGroup, channel, noticeType, signatureBasis, mergeCodes; answer `Template` in state Draft | Documents C | `Idempotency-Key` header |
| GET | `/admin/templates/{templateId}/content` | API-P6-005 | Answer: the binary named by `bodyRef` | Documents R | Not applicable |
| POST | `/admin/templates/{templateId}/approve` | API-P6-006 | Request `TemplateApproval`; answer `Template` in state Approved | Documents A | `Idempotency-Key` header |
| POST | `/admin/templates/{templateId}/withdraw` | API-P6-007 | Request `TemplateWithdrawal`; answer `Template` in state Withdrawn | Documents A | `Idempotency-Key` header |

Error statuses per operation are those of T-A.2 (section 7, AC4). The exact request and answer field names of `TemplatePage`, `TemplateApproval` and `TemplateWithdrawal` are Not specified in the source documents (GAP-1066; ASM-2014); this baseline fixes the resource names, the state values, the optionality rule of AC2 and the idempotency rule of AC5.

`POST /cases/{caseId}/notices` (API-P6-001) and `GET /notices/{noticeId}` (API-P6-002) are this service's operations but belong to the contract of RWB-P6-E1052-CON; this baseline references them and claims neither.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-LANG, LOV-PRODUCT, LOV-NOTICE and LOV-CHANNEL at the version in force, faked (DP-07, RWB-P3-E1043-CON) |
| GET | `/api/recovery/source-data/v1/admin/data-dictionary/fields` | P1 rwb-source-data | The BR Field ID check of every catalog row, faked; the plan carries no C dependency for this read (GAP-1064; ASM-2012) |

Every row is one hop with a 2 s timeout, a GET retry once with jitter and a breaker per downstream (DP-11, ADR-020). A failed read maps to MSG-GEN-006 naming the system that failed and never to an accepted load.

#### 12.3 Events published

| Event | Topic | Owner | Position of this baseline |
|---|---|---|---|
| `rwb.comms.NoticeGenerated.v1` | `rwb.comms.events.v1` | P6 rwb-comms | Declared as the service's event; published by the notice path of RWB-P6-E1052-APP, never by a template load or an approval |
| `rwb.comms.NoticeDispatched.v1` | `rwb.comms.events.v1` | P6 rwb-comms | Declared as the service's event; published by the dispatch stories of wave 2, never by this key |
| `rwb.comms.NoticeDelivered.v1` | `rwb.comms.events.v1` | P6 rwb-comms | Declared as the service's event; published by the proof-of-delivery story of wave 2, never by this key |

This baseline declares the three events because the service owns the topic; this legacy key publishes none of them (BR13), and a template load, an approval or a withdrawal is audited in the service log and the audit entry instead. The event names follow `rwb.<short>.<Event>.v1` on `rwb.<short>.events.v1` with the CloudEvents 1.0 envelope, keyed by the template or catalog identifier, and carry IDs, codes, versions and dates only.

#### 12.4 Events consumed

None. The catalog is read on demand by its callers and subscribes to no topic; the list values and the data-dictionary answer of section 12.2 are synchronous reads, and a change of either reaches this service on its next load.

#### 12.5 Workflows and activities

None. The five operations are synchronous REST calls in the caller's thread; this baseline declares no workflow, no activity and nothing on task queue `rwb-comms` in namespace `rwb-recovery`.

#### 12.6 Schedules

None. No Schedule, no cron entry and no job name is declared; JOB-10 WIN notices and JOB-11 the outbox relay belong to other stories, and this key holds no Schedule of its own.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| template | P6 (`rwb_comms`) | The versions, their state and their approval record, with the keys of RWB-P6-E1046-APP section 11 |
| merge_field | P6 (`rwb_comms`) | The merge codes and their BR Field ID by catalog version |
| notice | P6 (`rwb_comms`) | Contracted use only: `template_id` names the version a notice was generated from; this baseline and this key write no notice row |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_comms` | The idempotency row behind `Idempotency-Key` and the service's event envelope objects |

`signature_request` and `document` are P5's, `interaction` is P1's, `recovery_case` is P3's, `lov_value` is P3's reference data and `decision_log_entry` is P7's; they are named only as consumed answers and never declared as this service's tables (DP-01). `sys_fields` is P1's and is reached through the data-dictionary contract.

The P5 stamp `document.template_id` is a soft reference, not a foreign key, because the template and merge_field tables are held in `rwb_comms` and not in P5; a reconciliation check compares the stamped identifier with the template identifier of this service. The identifier property of the version answer is Not specified in the source documents (GAP-2343), and the rwb-document login name is Not specified in the source documents (GAP-2343).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case reference-data WireMock | `GET /admin/lists/{listCode}` answers LOV-LANG "TH" and "EN"; LOV-PRODUCT "MORTGAGE", "HIRE_PURCHASE", "SSME" and "UNSECURED"; LOV-NOTICE "DEMAND", "RECALL", "STATUTORY_SALE_NOTICE" and "GUARANTOR_NOTICE"; LOV-CHANNEL "LETTER", "SMS" and "LINE", and a delayed answer beyond 2 s | App story, contract tests, wave 1 harness |
| rwb-source-data data-dictionary WireMock | `GET /admin/data-dictionary/fields` answers DF-REF-045 to DF-REF-051 and DF-REF-252 to DF-REF-260 as known BR Field IDs, answers no field for `"XX-CAS-999"`, and offers a delayed answer beyond 2 s | App story, contract tests, wave 1 harness |
| catalog fixture "MF-2026.11" | The five merge codes "CASE_NO", "CUSTOMER_NAME", "POSTAL_ADDRESS", "TOTAL_OUTSTANDING" and "NOTICE_DATE" with their BR Field IDs and the valid-from date of the catalog version | App story, contract tests |
| template fixture pack | DEMAND-MTG "TH" version 1 Approved by "LEG-0001" on 2026-10-01; version 2 approved 2026-11-10 with valid from 2026-11-10; version 3 with valid from 2026-12-01; RECALL-HP "TH" with one Draft version; a withdrawn version 2; a file with an unknown merge code and a file with no `bodyRef` | App story, contract tests, wave 1 harness |

A drifted fake fails the drift test of AC8. The exact response field names of the data-dictionary read are Not specified in the source documents (GAP-1067; ASM-2015).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 5 provided, 2 consumed | The five admin template operations; the reference-data read and the data-dictionary read; one hop, 2 s on the consumed calls |
| Kafka | 0 published by this key, 0 consumed | The three notice events are the service's and belong to the notice path and the dispatch stories |
| Temporal | None | No workflow, no activity and no Schedule |
| File | 1 | The template body as a claim-check file behind `bodyRef`, read on the content operation |

### 13. Solution plan

**Deliverables.** The OpenAPI 3.1 document `openapi/rwb-comms-v1.yaml` with the five admin operations and the four resources; the contract README rows for the state values, the catalog version, the idempotency rule and the events this key does not publish; and the four WireMock mapping sets of section 12.8.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H, C, I and X lists of the metadata table are empty: this baseline adds no build dependency of its own (it is Day 1 by rule), and the platform and rwb-case contracts it names are the ones the app story declares. DP-08 is not among the patterns: no rwb-access contract is declared, and the declared area and right are enforced at gateway-bff (DP-19, GAP-1068).

**Build steps**

1. Write the five operations with their paths, parameters, resources and error responses; validate the document in the pipeline.
2. Fix the state values and the optionality rule of AC2, and the catalog-version rule of AC3, as schema constraints and README rows.
3. Record the two consumed rows with their owner, their budget and the missing-dependency gap of the data-dictionary read.
4. Record the `Idempotency-Key` rule on the three POSTs and the stored-answer behaviour.
5. Record the three notice events as the service's and the statement that this key publishes none of them, with an absence test.
6. Publish the four fakes and the eight contract tests; a drift between a fake and the document fails the build.
7. Baseline tag and the consumer sign-off note, including the app story, the notice story, the dispatch stories and the wave 1 harness.

**Done when.** The OpenAPI artefact validates in the pipeline, the eight contract tests pass, the four fakes answer every operation and read of sections 12.1 and 12.2, the drift test is green, and RWB-P6-E1046-APP and RWB-ITG-E1046-ITG have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-005 | A template has no Approved version | {template} version {version} has no Legal approval. It cannot be used. |
| MSG-P6-006 | A template uses a merge code not in the catalog | {template} uses the merge field {field}, which is not in the merge field catalog. The load was refused. |
| MSG-P6-003 | The current version is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P1-002 | A catalog load fails a check, or repeats a load | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | A required field is empty in a load row, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | A caller holds no Documents right for the operation | You cannot {action} here. Your role does not include it. |
| MSG-GEN-006 | A consumed read does not answer in time | {system} is not available. Your request is queued and will be retried. |

The message IDs and wording are contract elements: the five business messages are copied unchanged from RWB-E1-046 section 14, MSG-P4-002 is the reference-data refusal of the legacy load path, and MSG-GEN-006 is the platform unavailable message whose {system} value is fixed by the consumed row that failed. Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-33 Template catalog admin and SCR-40 Reference data are the two screens the legacy story names. The contract serves them in their states — Loading, Read only, Draft, Approved and Withdrawn for the catalog; Versions and load for the reference data record — through the gateway-bff composite route (DP-19), which calls the five admin operations and merges the answers into the screen model. This baseline fixes the operation answers only; the screen field list, the route specification and the read-only projection belong to RWB-PLT-N001-CON, and the delivered template screen of legacy RWB-E1-034 is outside this baseline. SCR-33 empty, error and no access states: Not specified in the source documents (CG-ALL-6371). SCR-40 empty, loading, error and no access states: Not specified in the source documents (CG-ALL-6372).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-046-01 | AC1, BR1, BR2, BR6 | End to end | Catalog MF-2026.11; DEMAND-MTG TH version 1 Approved; load of version 2 |
| TC-E1-046-02 | AC2, BR1, BR2 | End to end | RECALL-HP TH with one Draft version |
| TC-E1-046-03 | AC3, BR4 | End to end | GUARANTOR-SSME body using GUARANTOR_EMAIL |
| TC-E1-046-04 | AC3, AC4, BR4, BR5 | End to end | Catalog file of 12 rows, row 7 with an unknown field ID |
| TC-E1-046-05 | AC5, BR5 | End to end | Template row with empty body_ref |
| TC-E1-046-06 | AC6, BR11 | End to end | The AC1 file loaded twice |
| TC-E1-046-07 | AC7, BR3 | End to end | DEMAND-MTG TH version 2 withdrawn |
| TC-E1-046-08 | AC8, BR2 | End to end | DEMAND-MTG TH version 3 valid from 2026-12-01 |
| TC-E1-046-09 | AC4, AC6 | Component | RW-LITOFF calls POST /admin/reference-loads; refused with MSG-P4-002 |
| TC-E1-046-10 | AC1, BR8, BR12 | Component | Contract test: the five operations declared under /api/recovery/comms/v1 and no other service path |
| TC-E1-046-11 | AC8, BR13 | Component | Contract test: no notice event declared; 12.3 and 12.4 record None |
| TC-E1-046-12 | AC8, BR12 | Component | Boundary test: each table of 12.7 with its owner and contracted use |
| TC-E1-046-13 | AC4, BR9 | Component | Error responses: one envelope and one message ID per condition |
| TC-E1-046-14 | AC2, BR10 | Component | Additive optional property passes; a breaking change requires a new major version |
| TC-E1-046-15 | AC2, BR7 | Component | Approved version names the Legal approver authority in approvedBy |
| TC-E1-046-16 | AC3, BR14 | Component | Contract scan: no business value fixed beyond the fixture of MF-2026.11 |
| TC-E1-046-17 | AC1, AC7, AC8 | Component | Current-version read by code, language and on-date at 2026-11-30 and at 2026-12-01 (AC8 boundary) |
| TC-E1-046-18 | AC9, BR7, BR8, BR9, BR10, BR12, BR13, BR14 | Component | Not specified in the source documents (NEWAC-RWB-P6-E1046-CON-AC9) |

The nine legacy test cases of RWB-E1-046 are listed in the order of the legacy story; each is answered here at contract level against the artefact and the fakes, and its business outcome is proved by RWB-P6-E1046-APP. TC-E1-046-09 keeps its legacy load path `POST /admin/reference-loads` in its Data column; the operation this baseline puts in its place is the upload of section 12.1, and the mapping is the gap GAP-1063. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end and Access to Component.

### 17. Guardrails

- No business value in the contract: template codes, merge codes, languages, field IDs, list values, dates and the catalog version stay data rows of the load files or values of the fakes.
- No personal data in a schema, an example or a fake: IDs, codes, versions, dates and counts only; the approver on a version is a staff identifier and no customer field is declared.
- No template body and no merge value in a payload, an example, a fake or a log; the body is a claim-check reference behind `bodyRef`, and a merge field marked `personalData` is resolved only at generation time.
- ACE data is reached only through the owner's contract or the `v_ace_*` views; this document declares no ACE view and no cross-schema join.
- The contract names only rwb-comms tables and only operations owned by rwb-comms; the rwb-case and rwb-source-data reads are consumed and faked, never declared as provided (DP-01).
- One REST base and one topic per service; a document that names another service's base or topic as its own fails the review (DP-13).
- No notice event is published by this key, and the absence test of AC8 fails a build that declares one on a template load or an approval.
- Every example in the document is synthetic; no production payload is copied into a schema or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-OCC-001 | Notices from Legal-approved templates with merge fields from case data | The `MergeField` resource, the BR Field ID check through rwb-source-data, MSG-P6-006 and MSG-P1-002 | TC-E1-046-03, TC-E1-046-04, TC-E1-046-13 |
| REQ-OCC-002 | Templates versioned, Legal approval recorded against the version | The `Template` resource, its state values and approval fields, `TemplateApproval`, `TemplateWithdrawal`, MSG-P6-005 and MSG-P6-003 | TC-E1-046-01, TC-E1-046-02, TC-E1-046-05, TC-E1-046-07, TC-E1-046-08, TC-E1-046-10, TC-E1-046-14, TC-E1-046-15 |

| Decision or pattern | Where it sits in this story |
|---|---|
| DP-01 | Only rwb-comms tables declared; the two reads consumed and faked |
| DP-07 | The reference-data row of 12.2 and its fake |
| DP-11 | The two consumed rows with one hop, a 2 s timeout and a fake |
| DP-13 | Base `/api/recovery/comms/v1` on all five operations |
| DP-15 | The migration position recorded for the two tables in the service's own sequence |
| DP-19 | SCR-33 and SCR-40 behind gateway-bff |
| ADR-013 | The service owns its schema inside ACE PostgreSQL |
| ADR-014 | The `rwb_comms` schema and the rwb-comms login |
| ADR-020 | Contract-first REST, one hop, 2 s timeout |
| ADR-021 | Per-service Flyway and migration ownership |

The legacy key is RWB-E1-046; its AC1 to AC8 are owned by RWB-P6-E1046-APP, and the cross-service proof of the same values is RWB-ITG-E1046-ITG.

### 19. Out of scope

- The build of the five operations, the checks and the current-version selection: RWB-P6-E1046-APP.
- Notice generation from an approved version: RWB-P6-E1052-APP and RWB-P6-E1052-CON.
- Dispatch and proof of delivery: RWB-P6-E2021, RWB-P6-E2022 and RWB-P6-E1055.
- The cross-service proof of these values: RWB-ITG-E1046-ITG.
- The rwb-case reference-data contract and the rwb-source-data data-dictionary contract themselves: consumed and faked, never defined here.
- The gateway-bff composite route and the screen field list: RWB-PLT-N001-CON.
- The delivered template screen with upload, approval and withdrawal (legacy RWB-E1-034) and the Compliance approval path for a template (FEAT-ADM-05, Epic 8).
