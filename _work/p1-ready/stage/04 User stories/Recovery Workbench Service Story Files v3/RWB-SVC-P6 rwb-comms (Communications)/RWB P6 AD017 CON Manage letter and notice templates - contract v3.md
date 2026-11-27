# RWB-P6-AD017-CON Manage letter and notice templates

**Version 3 changes.**

- MSG-GEN-006 carries the English text of Error and Message Standard v6 (RD-P1-004).

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-AD017-CON |
| Readiness decisions | RD-P1-004 |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Contract version | /v1 (path `/api/recovery/comms/v1`); document version Not specified in the source documents (DOR-RWB-P6-AD017-CON-23) |
| Service epic | RWB-SVC-P6 |
| Wave | 4 |
| Size | Not specified in the source documents (DOR-RWB-P6-AD017-CON-16); the squad sizes it at refinement |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP07, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON (reference lists, DP07; plan row to be added at the next plan revision) |
| Integration dependencies | None |
| External dependencies | None |
| Open decisions | DL28 (open); assumptions ASM-1861, ASM-1925, ASM-2093, ASM-2727 |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-017 for rwb-comms; the published contract baseline of the template administration surface of the service. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P6-AD017-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (14 resolved, 8 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Tribe lead and squad members (RW-TRIBE)**, I want **the published contract baseline of template administration in rwb-comms — the five template operations on `/api/recovery/comms/v1` as TSD appendix T-A.1 names them, the Template resource with its state vocabulary and its current-version rule, the approval and withdrawal rules, the reference-data and body-reference rows, the two consumed rows with their owners, the nine contract tables and the four fakes**, so that **the app story of this legacy key, the Epic 1 story it extends, the screen story behind the composite route and the test stories build against one fixed, testable contract on Day 1, and a path, a field, a state value or a right can never drift between rwb-comms, rwb-case and the services the screen calls without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and the platform's 2 s budget is the decoupling decision (ADR-020). The legacy story RWB-AD-017 describes a screen with three states and two criteria but publishes no contract at all: its endpoint table names the notice request and the notice read of the communications module, its data table mixes four entities of four owners, and its permission table names the Litigation right while the TSD puts the template operations on the Documents right (GAP-1146; ASM-2093). The target needs the opposite: one published baseline that fixes the five operations of API-P6-003 to API-P6-007, the shape of the template version, the three state values, the rule that makes a version current, the two consumed rows and the fakes, before the app story starts. This story is that baseline, and it publishes no business behaviour of its own.

The baseline also fixes the naming the checks require: schema `rwb_comms`, REST base `/api/recovery/comms/v1`, task queue `rwb-comms` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.comms`. It records that the template operations are API-P6-003 to API-P6-007 of the TSD appendix T-A.1 and of the Ownership Map under P6, that `template` and `merge_field` are P6's own tables on Architecture v5 slide 41, that the task of the litigation officer and the reference lists are rwb-case's, that the physical document of any kind is rwb-document's, that the decision record is the local library's on `rwb.decision-record.v1`, and that no template event exists in the service event catalogue (Architecture v5 slides 41 and 42). Where a source is silent — the withdrawal reason, the decision code and rule id of an approval, the task code and queue, the reference-data dependency of this key — the document carries the placeholder of the gap and not an invented value.

The ownership of templates itself is a disagreement that the baseline records and does not follow quietly: the legacy story cites DL28, which reads "the document module owns templates and fields; Legal approves wording", while the catalogue of Architecture v5 and the Ownership Map give `template` and `merge_field` to P6 rwb-comms. Under the precedence rule the catalogue wins and DL28 is the loser, so the row is a conflict with its assumption (GAP-1146; ASM-2093), and rwb-comms owns the wording while the physical documents and any generated file stay with rwb-document.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the paths, the topic, the queue and the package follow the platform rule rather than a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope and the retry and `.dlt` topic convention are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); where this document narrows them it does so explicitly.
- The Epic 1 contract of RWB-P6-E1034-APP is published, so the five template operations, the Template shape and the state column this baseline fixes have one owner document and this baseline is an additive change to it, not a second version of it.
- The template and merge field catalogue contract RWB-P6-E1046-CON is published, so `template`, `merge_field`, the version numbering and the merge code check are fixed by the story that owns them and are read here.
- The operations and their owners are taken from the Ownership Map only; this document never declares another service's operation as provided. The reference lists and the task are P3 rwb-case, the physical document is P5 rwb-document, the decision ledger is P7 rwb-decision and the body container is the one RWB-P6-E1034-APP fixed.
- The document is Day 1 by rule: a CON story has no build dependency and sits in the contract group of its wave (Template and Rules §R5.7).
- The split of the surface between RWB-P6-E1034-APP and the Epic 8 administration surface of this legacy key is Not specified in the source documents (GAP-1146; ASM-2093); this baseline fixes only what the five operations answer and restates none of the Epic 1 rules it inherits.
- The reference-data dependency of this key is not in its pattern set and not in its dependency rows, so the read of LOV-PRODUCT, LOV-CHANNEL, LOV-NOTICE and LOV-SIGNATURE-BASIS is declared as consumed with the placeholder and not as a C row (GAP-1147; ASM-2094).
- The withdrawal reason, its length, its field and the decision code and rule id of an approval or a withdrawal are Not specified in the source documents (GAP-1148; ASM-2095); this document fixes where the reason is recorded and no rule it does not have.
- The task raised on a withdrawn version has no operation, task code or queue in any source (GAP-1149; ASM-2096), and no template event exists in the catalogue (GAP-1150; ASM-2097).

### 4. Flow

1. Draft the additive change to the rwb-comms OpenAPI 3.1 document: the five template operations of API-P6-003 to API-P6-007 under the base `/api/recovery/comms/v1`, the Template and TemplatePage resources, the approval and withdrawal request bodies, the error responses and the Idempotency-Key on the three POST operations.
2. Fix the template resource and its state vocabulary: Draft, Approved and Withdrawn, the current-version rule, the merge codes, the body reference and the record version of the optimistic lock.
3. Fix the approval and the withdrawal rules as contract conditions: the Documents right, the self-approval refusal, the valid from date, the non-empty reason, the state conflict, the record before the change and the task of R-LIT-04.
4. Record the two consumed rows with their owner and their placeholder: the reference lists of rwb-case and the litigation officer task of rwb-case.
5. Record the body reference and the container it points at, so that no second container is declared and no P5 table is read.
6. Record the decision-record element as declared through the local library, and record that no template event exists and none is invented.
7. Publish the nine contract tables of section 12 and the four contract fakes of 12.8.
8. Add the contract tests: schema validation, the additive rule, the closed state vocabulary, the error envelope and one message ID per condition, the absence of a cross-schema read, the absence of a retired element and of an invented event, and the drift between a fake and the document.
9. Tag the baseline and hand it to RWB-P6-AD017-APP, to RWB-P6-E1034-APP for the additive review, and to the screen story behind RWB-PLT-N001-CON.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | MSG-P3-030 | AC1 |
| X2 | A field is renamed, removed or retyped within major version 1 | The additive test fails; the change needs a new major version | None | AC2 |
| X3 | A state value outside Draft, Approved and Withdrawn appears in the document or in a fake | The vocabulary test fails the build | None | AC2 |
| X4 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC5 |
| X5 | The document declares another service's operation as provided, or a path outside the base | The review fails the baseline; the row is described as consumed and faked | None | AC1 |
| X6 | A retired element reappears — a second base, a second container, a Quartz row or a template event that the catalogue does not hold | The absence test fails the build | None | AC6 |
| X7 | A row whose operation no source names is filled with an invented path | The placeholder test fails the build: the row keeps the placeholder and the gap | None | AC4 |
| X8 | The decision record cannot be written | The state does not change and the answer is 503 with MSG-P7-003, as the app story applies it | MSG-P7-003 | AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Epic 1 contract it extends and the Ownership Map only |
| Negotiable | The two consumed rows, the withdrawal reason and the task code are settled with the rwb-case owner and the business owner; the operations, the paths, the state values and the base are fixed by the target architecture |
| Valuable | Unblocks the app story of this key, the additive review of the Epic 1 story and the screen story on Day 1 |
| Estimable | One document, one additive change, two consumed rows, nine contract tables, four fakes and seven contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of template administration in rwb-comms

  Background:
    Given the service naming rule of the platform library is in force
    Given the five template operations of TSD P6 appendix T-A.1 are API-P6-003 to API-P6-007
    Given the Epic 1 contract RWB-P6-E1034-APP is published with the Template shape and the three state values

  Scenario: AC1 The five template operations are declared on the service base (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-comms is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /admin/templates, POST /admin/templates, GET /admin/templates/{templateId}/content, POST /admin/templates/{templateId}/approve and POST /admin/templates/{templateId}/withdraw, all under the base /api/recovery/comms/v1 and owned by rwb-comms
    Then each operation declares its purpose, its request and answer, its capability area and right from the Documents column of TSD P6 T6.1, and its error responses 401, 403, 404 and 503, with 409, 413, 415 and 422 on the operations that can raise them
    Then the list declares the query code, language, state, page and size and answers a page; the body operation answers a binary stream
    Then the three POST operations declare the Idempotency-Key header and the stored answer, and the two GET operations declare none
    Then the document declares no path outside the base and no operation owned by another service as provided
    Then every path and field name is the one TSD P6 appendix T-A.1 and the Epic 1 contract use, and the document records that the legacy endpoint table of RWB-AD-017 names the notice request and the notice read and no template operation (GAP-1146; ASM-2093)

  Scenario: AC2 The template resource and its state vocabulary are fixed (new, D-RCV-60)
    Given the Template and TemplatePage schemas of the document
    When they are compared with TSD P6 T3.1 and with the Epic 1 contract
    Then Template carries id, templateCode, templateVersion, language, productGroup, channel, noticeType, signatureBasis, mergeCodes, state, approvedBy, approvedAt, validFrom, createdBy, createdAt and version
    Then the field identifiers are DF-REF-045 to DF-REF-051 and DF-REF-063 to DF-REF-069 of TSD P6 T3.1, and mergeCodes is the list of merge codes the body uses
    Then state is a closed set of DRAFT, APPROVED and WITHDRAWN, and no other value appears in the document, in an example or in a fake
    Then the document states the current-version rule — the current version of a code and language is the Approved version with the latest valid from date on or before today — and declares no set-current operation
    Then bodyRef points at the write-once container that RWB-P6-E1034-APP fixed, the document declares no second container and no file path of a shared disk, and where that container is the document hub of rwb-document the value is a document reference read through the owner's contract and never a row of another schema
    Then every added property is optional in the schema, so a consumer of the Epic 1 version keeps working (GAP-1148; ASM-2095)

  Scenario: AC3 The approval and withdrawal rules are fixed as contract conditions (new, D-RCV-60)
    Given the approve and the withdraw operations of the document
    When their conditions are compared with the rules of the legacy story and of the Epic 1 story
    Then the approve declares Documents right A, the refusal of an approver who is the uploader, the state guard Draft, the valid from date as today or later and the record version of the optimistic lock, with 409 for a wrong state, a changed record or a self-approval and 422 for a valid from date before today
    Then the withdraw declares Documents right A, the state guard Approved, a non-empty reason and the record version, with 409 for a wrong state or a changed record and 422 for an empty reason
    Then the document declares that the decision record is written through the local decision-record library before the state change and that a failed write changes nothing and answers 503 with MSG-P7-003
    Then the document declares that a withdrawal moves the version to Withdrawn, that generation holds under R-LIT-04, that no earlier version becomes current again, and that a new approved version of the code and language resumes generation under R-LIT-06
    Then the document declares the litigation officer task of a withdrawal as a consumed row of rwb-case with the template code, the version, the language, the case and MSG-P6-003, and its operation, its task code and its queue are Not specified in the source documents (GAP-1149; ASM-2096)
    Then the decision code and the rule id that an approval or a withdrawal records are Not specified in the source documents and the document holds them unset rather than inventing them (GAP-1148; ASM-2095)

  Scenario: AC4 The reference-data and body-reference rows are declared with their owner (new, D-RCV-60)
    Given the consumed rows and the data rows of the document
    When each is compared with the Ownership Map
    Then LOV-PRODUCT, LOV-CHANNEL, LOV-NOTICE and LOV-SIGNATURE-BASIS of TSD P6 T3.2 are declared as reference data of rwb-case read with the version in force, and the read is declared as consumed and faked
    Then the document records that this key carries no DP-07 and no C row for that read, so the row carries the placeholder (GAP-1147; ASM-2094)
    Then the withdrawal reason is declared as recorded in the local decision record and not in a column of template, and no field of the document invents one
    Then bodyRef is declared as a reference into the write-once container of RWB-P6-E1034-APP, and the document declares no second container and no P5 table read
    Then the reference lists are declared as values read with a version and never as constants of the document (BR-P6-001)

  Scenario: AC5 The four contract fakes answer the document (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-case reference-list fake answers LOV-PRODUCT, LOV-CHANNEL, LOV-NOTICE and LOV-SIGNATURE-BASIS with a version, a list without a value, and a delayed answer beyond 2 s
    Then the rwb-case task fake answers an accepted task for one case with the template code, the version, the language and MSG-P6-003, a refused raise and a delayed answer beyond 2 s
    Then the decision-record library stub answers a healthy chain and outbox and a stopped chain
    Then the body container stub answers a stored body for one version and a missing body for a stale reference
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC6 The nine tables are complete and no cross-schema read or retired element is declared (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the tables named as owned are template, merge_field, the read of notice and the library objects, and recovery_case, task, timer, reference_row, document, decision_log_entry, role, interaction, outbound_item and legal_action are named as other owners' and consumed only through their contracts
    Then the document declares no read of a v_ace_ view of this service and no cross-schema join (DP-01, DP-05)
    Then the document declares no second REST base, no second topic, no second body container, no Quartz row and no shared job table
    Then the document declares no template event, because the event catalogue holds NoticeGenerated, NoticeDispatched and NoticeDelivered on rwb.comms.events.v1 and nothing else of this service (GAP-1150; ASM-2097)

  Scenario: AC7 The baseline records what it serves and copies none of it (new, D-RCV-60)
    Given the acceptance criteria of the legacy story and the four legacy test cases of the key
    When the baseline is reviewed against them
    Then the document records that AC1 Approve and AC2 Withdraw of RWB-AD-017 are served by the five operations and the rules of this baseline, that their wording stays with RWB-P6-AD017-APP, and that this baseline copies neither criterion
    Then the document records that TC-AD-017-01 to TC-AD-017-04 stay with RWB-P6-AD017-APP and that the contract cases of this story test the artefact only
    Then the document records that the Epic 1 cases TC-E1-034-01 to TC-E1-034-11 stay with RWB-P6-E1034-APP and that this baseline re-plans none of them
    Then every example in the document is synthetic and carries a template code, a version, a language, a state and a date, and no name, address or account number

  Scenario: AC8 The rules of section 8 that no other criterion tests are checked in the document (new, D-RCV-60)
    Given the business rules BR1, BR3, BR4, BR6, BR8, BR11, BR12 and BR13 of section 8
    When each is compared with the document and with the sources named in section 8
    Then BR1 holds: the document declares one REST base, /api/recovery/comms/v1, and no path of another service as provided
    Then BR3 holds: the state set is the closed set of three values, and the current version is a derived rule with no state and no operation of its own
    Then BR4 holds: the two GET operations declare no Idempotency-Key, and the three POST operations declare it and the stored answer
    Then BR6 holds: every change is additive within /v1, and a breaking change is declared as a new major version
    Then BR8 holds: the template, its merge codes and its body reference are rows of this service, and the document repoints no notice and closes no task
    Then BR11 holds: every value that no source names carries the placeholder and a gap ID, and no path is invented
    Then BR12 holds: the document declares no view of its own and no cross-schema read
    Then BR13 holds: the partner instruction is S9 InstructionWorkflow, the internal alert is a P3 task, and rwb-comms keeps no record of the internal alert
```

These eight criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-P6-AD017-APP, they copy neither criterion of the legacy story, and they re-plan nothing of RWB-P6-E1034-APP.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/comms/v1`; the document never declares another service's path as provided | DP-13; Architecture v5 slide 41 notes |
| BR2 | The five template operations of this baseline are API-P6-003 to API-P6-007 of TSD appendix T-A.1 and are P6's in the Ownership Map | TSD P6 T-A.1; Ownership Map v1 |
| BR3 | The state vocabulary is a closed set of three values and the current version is a derived fact, never a state and never an operation | TSD P6 T3.1; RWB-P6-E1034-APP |
| BR4 | A read declares no Idempotency-Key; a POST declares it and stores its answer | Architecture v5 slide 11; DP-09 platform baseline |
| BR5 | Error responses use one envelope and one message ID per condition; the business texts are copied unchanged from the Epic 1 story where the message already exists | Architecture v5 platform baseline; Template and Rules §R7.2 s14 |
| BR6 | A schema change is additive within a major version; a breaking change is a new major version | Architecture v5 slide 42 notes |
| BR7 | The document lists only operations owned by rwb-comms; a consumed operation is described as consumed, with its owner and its fake | Ownership Map v1 |
| BR8 | The template, its merge codes and its body reference are this service's rows; the task and the reference lists are rwb-case's, the physical document is rwb-document's, and this story neither repoints a notice nor closes a task (the resumption of held generation is Not specified in the source documents (GAP-1149)) | DP-01; Architecture v5 slide 41 |
| BR9 | The decision record is the local library's entry on the shared topic, never a new event of this service, and no template event is declared | DP-03; Architecture v5 slide 42 |
| BR10 | No business value is fixed in the contract: the value sets, the page size, the allowed body types, the size limit, the withdrawal reason rule, the decision code and the task code stay data, reference data or gaps | Template and Rules §R7.2 s17 |
| BR11 | Where no source names a value or an operation the row carries the placeholder and the gap, and no path is invented | Template and Rules §R9 |
| BR12 | ACE data is reached only through the owner's contract or the owner's `v_ace_*` views; this document declares no view of its own and no cross-schema read | DP-05 |
| BR13 | The partner instruction is S9 InstructionWorkflow; the internal alert is a P3 task; rwb-comms keeps the template of the partner instruction only and no record of the internal alert | Architecture v5 slide 17; slide 41 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The five operations, the resource, the vocabulary, the consumed rows and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the Epic 1 story for the additive review and the screen story accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1, for example a new optional property of Template | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, or a state value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A retired element or an invented event appears | The absence test of AC6 fails | In review |
| Baselined | A placeholder row is filled without a source | The placeholder test of AC4 fails | In review |

The template version state machine — Draft to Approved, Approved to Withdrawn — is the app story's and this baseline fixes its vocabulary and its guards and moves no version.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-comms | Owns the OpenAPI document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes, including the conflict of DL28 |
| Consuming teams (the app story of this key, the Epic 1 story RWB-P6-E1034-APP, the screen story behind the composite route, and the rwb-case, rwb-document, rwb-decision and rwb-access owners) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the CloudEvents envelope, the naming rule and the idempotency store this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an example or a fake |

The per-service login name behind the document's security scheme is not part of this baseline; the document names the scheme "the rwb-comms login (DP-02)".

### 11. Data

The contract baseline declares shapes, not business values.

| Item | BR Field ID | Content |
|---|---|---|
| Template resource | DF-REF-045 to DF-REF-051 and DF-REF-063 to DF-REF-069 | The Template of RWB-P6-E1034-APP with its sixteen properties and its `version`; the fields of TSD P6 T3.1 DF-REF-045 to DF-REF-051 and DF-REF-063 to DF-REF-069 |
| TemplatePage | Not specified in the source documents (DOR-RWB-P6-AD017-CON-7) | `items` of Template with the paging facts of the `page` and `size` query of API-P6-003; the exact field list beyond `items` is Not specified in the source documents (GAP-1148; ASM-2095) |
| State vocabulary | Not specified in the source documents (DOR-RWB-P6-AD017-CON-7) | DRAFT, APPROVED and WITHDRAWN as a closed set, with the current-version rule of AC2 |
| Approval request | DF-REF-065 (valid_from) | `validFrom`; the rest of the body is Not specified in the source documents (DOR-RWB-P6-AD017-CON-7) beyond the purpose of API-P6-006 (GAP-1148; ASM-2095) |
| Withdrawal request | Not specified in the source documents (DOR-RWB-P6-AD017-CON-7) | `reason`, recorded in the local decision record and not in a column of template; its length and content rule are Not specified in the source documents (GAP-1148; ASM-2095) |
| Body reference | DF-REF-050 | `body_ref` DF-REF-050 pointing at the write-once container of RWB-P6-E1034-APP |
| Reference lists | DF-REF-049 (product_group), DF-REF-068 (signature_basis); the others Not specified in the source documents (DOR-RWB-P6-AD017-CON-7) | LOV-PRODUCT, LOV-CHANNEL, LOV-NOTICE and LOV-SIGNATURE-BASIS of TSD P6 T3.2, consumed from rwb-case with the version in force (GAP-1147; ASM-2094) |
| Decision record element | Not specified in the source documents (DOR-RWB-P6-AD017-CON-7) | IDs, codes, dates and the state after the change only; no name, address, identity number or account number |

The field-level types, lengths and required flags of the added properties are settled in the baseline review; this story fixes the names, the optionality rule of AC2 and the closed vocabulary of AC2.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/admin/templates` | Query `code`, `language`, `state`, `page`, `size` in; a page of Template out with status 200 | Documents, right R, scope applied | Not applicable |
| POST | `/admin/templates` | Multipart `file` with `templateCode`, `language`, `productGroup`, `channel`, `noticeType`, `signatureBasis` and `mergeCodes` in; Template of status 201 out, in state DRAFT | Documents, right C, scope applied | Idempotency-Key header, answer stored for 24 hours |
| GET | `/admin/templates/{templateId}/content` | No body in; the binary body of the version out with status 200 | Documents, right R, scope applied | Not applicable |
| POST | `/admin/templates/{templateId}/approve` | TemplateApproval with `validFrom` in; Template of status 200 out, in state APPROVED | Documents, right A, scope applied | Idempotency-Key header, answer stored for 24 hours |
| POST | `/admin/templates/{templateId}/withdraw` | TemplateWithdrawal with `reason` in; Template of status 200 out, in state WITHDRAWN | Documents, right A, scope applied | Idempotency-Key header, answer stored for 24 hours |

All five answer 401, 403, 404 and 503; the approve and the withdraw also answer 409 and 422; the upload also answers 409, 413, 415 and 422. Each condition answers one message ID of section 14. The five paths are the operations API-P6-003 to API-P6-007 of the TSD appendix T-A.1 and are P6's in the Ownership Map; the legacy endpoint table of RWB-AD-017 names the notice request and the notice read and no template operation, which is the conflict of GAP-1146.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | the list read of RWB-P3-E1043-CON, `GET /api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-PRODUCT, LOV-CHANNEL, LOV-NOTICE and LOV-SIGNATURE-BASIS with the version in force, faked. This key carries no DP-07 and no C row for the read, and the row is Not specified in the source documents as a dependency of this key (GAP-1147; ASM-2094) |
| POST | the task raise of a withdrawn version | P3 rwb-case | One task per case to the litigation officer team under R-LIT-04 with the template code, the version, the language, the case and MSG-P6-003, faked. The operation, the task code, the target queue and the task fields are Not specified in the source documents (GAP-1149; ASM-2096) |

Two rows and no third. The notice rows a withdrawal looks at are this service's own; the body is the container RWB-P6-E1034-APP fixed; the authorise answer is asked by gateway-bff; and no row reads a table or a `v_ace_*` view (DP-01, DP-05). Every row is one hop with the platform's 2 s budget and a breaker per downstream, and a missing answer never approves, never withdraws and never marks a task as raised (ADR-020).

#### 12.3 Events published

| Event | Topic | Owner | Schema element |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (event 08) | `rwb.decision-record.v1` | P7 rwb-decision | decision record reference, decision code, rule id, template code, template version, language, state after the change, decidedAt; the local decision-record library publishes it (DP-03) |

This story declares the one element and publishes none itself. No template event is declared, because the catalogue of Architecture v5 slide 42 holds NoticeGenerated, NoticeDispatched and NoticeDelivered on `rwb.comms.events.v1` and nothing for a template (GAP-1150; ASM-2097).

#### 12.4 Events consumed

None. The five operations are user actions and the baseline consumes no event.

#### 12.5 Workflows and activities

None. No workflow, no activity and no durable timer is declared: the five operations are synchronous request and answer calls, and the task raise and the decision record are calls inside the transaction of the state change.

#### 12.6 Schedules

None. No Schedule, no Quartz row and no shared job table is declared by this baseline (Architecture v5 slide 44).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| template | P6 (rwb_comms) | The version, its language, product group, channel, notice type, signature basis, merge codes, body reference, approver, approval time, valid from date and state; the table the five operations read and write |
| merge_field | P6 (rwb_comms) | The merge catalogue checked against the version in force; read only |
| notice | P6 (rwb_comms) | Read only, to find the held notices of a withdrawn version |
| decision record (local) | P6 rows in `rwb_comms`, written through the P7 library | The record of an approval and of a withdrawal, with the withdrawal reason (DP-03) |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_comms` | The envelope of the decision record and the idempotency of the three POST operations |

`recovery_case`, `task`, `timer`, `queue`, `assignment`, `reference_row`, `reference_version` and `lov_value` are P3's, `document`, `document_custody` and `signature_request` are P5's, `decision_log_entry`, `approval` and `rule_row` are P7's, `role` and `permission` are P4's, `interaction` is P1's, `outbound_item` and `interface_config` are P2's, `deviation` is S8's and `legal_action` is S4's; the contract names them only as consumed answers and never as read tables (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case reference-list WireMock | LOV-PRODUCT, LOV-CHANNEL, LOV-NOTICE and LOV-SIGNATURE-BASIS with a version, a list without a value the body uses, and a delayed answer beyond 2 s | App story, contract tests |
| rwb-case task WireMock | A task accepted for case `RC-2026-000321` with template `DEMAND-MTG` TH version 3 and MSG-P6-003, a refused raise and a delayed answer beyond 2 s | App story, contract tests |
| decision-record library stub | A healthy chain and outbox, and a stopped chain | App story, contract tests |
| body container stub | A stored DOCX body for `DEMAND-MTG` TH version 3 and a missing body for a stale reference | App story, contract tests |

The two fakes of rwb-case stand behind rows whose operation no source names and carry the placeholder until the rwb-case owner publishes them (GAP-1147; GAP-1149).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 5 provided, 2 consumed | The five template operations provided; the reference lists and the task raise consumed; one hop, 2 s |
| Kafka | 1 declared as published by its owner, none consumed | `rwb.decision.DecisionRecorded.v1`; no template event |
| Temporal | None | No workflow, no activity, no Schedule |
| File | None | The body is streamed through a reference and no file is produced or consumed |

### 13. Solution plan

**Deliverables.** The additive change to `openapi/rwb-comms-v1.yaml` for the five template operations and the Template and TemplatePage resources, the contract README rows for the state vocabulary, the current-version rule, the withdrawal reason and the placeholders, and the four WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies as a prohibition: the document declares no ACE view and no ACE row of this service, and the account and party facts of a generated notice are not part of this contract at all. DP-08 is not in the pattern set of this key: the capability area and the right are declared per operation and enforced at gateway-bff, which asks rwb-access.

**Build steps**

1. Add the five paths and the Template, TemplatePage, TemplateApproval and TemplateWithdrawal schemas to the document, and validate the additive rule of AC2 in the pipeline.
2. Close the state vocabulary of AC2 and add the vocabulary test that fails on a fourth value in the document, an example or a fake.
3. Record the current-version rule and the absence of a set-current operation in the document and in the contract README.
4. Record the approval and withdrawal conditions of AC3, with the error set and one message ID per condition.
5. Record the two consumed rows of 12.2 with their owner, their fake and the placeholder of the two gaps of this key.
6. Record the body-reference row of AC4 and the decision-record element of 12.3, and add the absence test for a second container, a second base, a Quartz row and a template event.
7. Publish the four fakes and the seven contract tests; a drift between a fake and the document fails the build.
8. Baseline tag and the consumer sign-off note, including the app story of this key, the Epic 1 story for the additive review and the screen story behind the composite route.

**Done when.** The OpenAPI artefact validates in the pipeline, the seven contract tests pass, the four fakes answer every consumed row and the drift test is green, and the app story, the Epic 1 story and the screen story have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-030 | A response body or a query fails schema validation | The request could not be read: {detail}. |
| MSG-GEN-006 | A consumed call does not answer in time | {system} is not available. Try again in a few minutes. |
| MSG-GEN-001 | A required field is empty, including the withdrawal reason | Enter {field}. |
| MSG-GEN-003 | The valid from date is before today | {field} cannot be before {other}. |
| MSG-GEN-004 | Another person changed the version first | Someone else changed this record. Reload it to see their change. |
| MSG-P6-003 | A withdrawn version is asked for, and on the task of a withdrawal | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P6-005 | A version with no Legal approval is asked to become current | {template} version {version} has no Legal approval. It cannot be used. |
| MSG-P6-006 | A merge code of the uploaded body is not in the catalogue in force | {template} uses the merge field {field}, which is not in the merge field catalog. The load was refused. |
| MSG-P6-010 | The body file type is not allowed | This template file type cannot be loaded. Use {types}. |
| MSG-P7-002 | The uploader approves their own version | You prepared this decision, so you cannot approve it. |
| MSG-P7-003 | The decision record of an approval or a withdrawal cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-005 | Approve on a version that is not Draft, or withdraw on one that is not Approved | This case cannot move to {state} from {current}. |
| MSG-P4-002 | The role lacks the Documents right of the operation | You cannot {action} here. Your role does not include it. |

The message IDs are contract elements; every text is the agreed text the Epic 1 story RWB-E1-034 and its contract already carry, copied unchanged, and MSG-P3-030 and MSG-GEN-006 are the platform messages of a schema failure and of a call that does not answer in time.

### 15. Screens and states

The contract serves SCR-33 Template approval in its Draft, Approved and Withdrawn states through the gateway-bff composite route (DP-19): the paged list with the filters on template code, language and state, the version detail with the body download, the approve dialog with its valid from date and the withdraw dialog with its reason. The route calls rwb-comms for the five operations and rwb-access for the right; this baseline fixes the rwb-comms answers only, and the composite route specification, the screen field list and the masking belong to RWB-PLT-N001-CON. The empty, loading, error and no access states of SCR-33 are Not specified in the source documents (CG-ALL-6287).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-017-01 | legacy AC1, BR2, BR10 | End to end | DEMAND-MTG TH version 2 Approved; version 3 Draft; approval by LEG-0001 with valid from 2026-11-20; the contract half answers the approve operation, the Template fields and the state vocabulary |
| TC-AD-017-02 | legacy AC2, BR2, BR7 | End to end | DEMAND-MTG TH version 3 Approved and current, withdrawn with a reason; a notice of that template held with TEMPLATE_WITHDRAWN; the contract half answers the withdraw operation, the task row of 12.2 and the state vocabulary |
| TC-AD-017-03 | Access, BR2 | Component | RW-LITOFF holds Documents CRU; the contract half answers the 403 of the approve operation and the right declared for it |
| TC-AD-017-04 | Principle 5, BR5, BR9 | NFR | The decision-record library stopped on 10 approvals and 10 withdrawals; the contract half answers the stopped chain of the library stub and the 503 of the two operations |
| TC-P6-AD017-CON-01 | AC1 | Contract | The document validates; the five operations, the base, the rights, the Idempotency-Key rule and the error set are present; no foreign path |
| TC-P6-AD017-CON-02 | AC2 | Contract | The Template properties and field IDs, the closed state set, the current-version rule, the optionality rule and the body reference |
| TC-P6-AD017-CON-03 | AC3 | Contract | The approve and withdraw conditions, the decision record before the change, R-LIT-04, R-LIT-06 and the placeholder of the unset decision code |
| TC-P6-AD017-CON-04 | AC4 | Contract | The four reference lists with their owner and version, the placeholder of the missing C row, and the withdrawal reason in the decision record |
| TC-P6-AD017-CON-05 | AC5 | Component | The four fakes match the document; a drifted fake fails the build |
| TC-P6-AD017-CON-06 | AC6 | Contract | The nine sub-tables present with owners; no cross-schema read; the absence test for a second base, a second container, a Quartz row and a template event |
| TC-P6-AD017-CON-07 | AC7 | Contract | The legacy criteria and the four legacy cases recorded as served by this baseline and copied nowhere; the Epic 1 cases untouched |
| TC-P6-AD017-CON-08 | AC8 | Contract | The one REST base and no foreign path (BR1); the closed state set and the derived current version (BR3); Idempotency-Key on the POST operations only (BR4); additive change within /v1 (BR6); the rows of this service only (BR8); the placeholder and gap ID for unnamed values (BR11); no view and no cross-schema read (BR12); the partner instruction and the internal alert, with no record of the alert (BR13) |

The four legacy cases keep their legacy IDs, their legacy order and their legacy data and are the evidence the contract serves; they are tested by RWB-P6-AD017-APP. The seven contract cases are new and test the artefact only. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the value sets, the page size, the allowed body types, the size limit, the withdrawal reason rule, the decision code and the task code stay data, reference data or gaps.
- No personal data in a schema, an example or a fake: template codes, versions, languages, states, dates and synthetic user IDs only.
- The contract names only rwb-comms tables and only operations owned by rwb-comms; the reference lists and the task are consumed and faked, never declared as provided (DP-01, DP-03).
- One base, one topic and one queue per service; a document that names another service's base or topic as its own fails the review (DP-13).
- No retired element and no invented event: the absence test of AC6 fails a build that declares a second base, a second body container, a Quartz row, a shared job table or a template event.
- ACE data is reached only through the owner's contract or the owner's `v_ace_*` views; this document declares no ACE view and no cross-schema join (DP-05).
- A placeholder row is never filled without a source: the test of AC4 fails a build that replaces a gap with a value.
- Every example in the document is synthetic; no production payload and no production template body is copied into a schema or a fake.
- The error envelope, the CloudEvents envelope and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Trace item | Value |
|---|---|
| Legacy key | RWB-AD-017, disposition Split (rework) |
| Legacy criteria | AC1 (Approve) and AC2 (Withdraw) of the legacy story, owned by RWB-P6-AD017-APP and copied nowhere in this baseline; this baseline records that it serves them |
| Test cases | The four legacy cases as the evidence the contract serves, and the seven new contract cases TC-P6-AD017-CON-01 to TC-P6-AD017-CON-07 |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership) |
| Rules | R-LIT-04, R-LIT-06, R-UNI-39 |
| Operations | API-P6-003 to API-P6-007 of TSD P6 appendix T-A.1, on the base `/api/recovery/comms/v1` |
| Gaps and assumptions of this key | GAP-1146 to -5 with ASM-2093 to -5 |

The legacy story carries no requirement ID of its own: its metadata row names the decision DL28 and no feature. The requirement that the wording be versioned with the Legal approval recorded against the version is REQ-OCC-002, it is held by RWB-P6-E1034-APP, and this baseline restates none of it. DL28 itself is the loser of the ownership conflict of this key and is recorded as such (GAP-1146; ASM-2093).

### 19. Out of scope

- The implementation of the five operations, the list, the body download, the approve, the withdraw and the task (RWB-P6-AD017-APP).
- The Epic 1 upload-and-approve core of RWB-P6-E1034-APP: this baseline is an additive change to its contract, restates none of its rules and re-plans none of its cases (rule U2, Template and Rules §R6).
- The template and merge field catalogue contract RWB-P6-E1046-CON; this baseline reads it.
- Notice generation and its contract RWB-P6-E1052-CON. Notice generation only reads the state this contract describes.
- The task row, the queue, the assignment and the timer of rwb-case; the reference lists and their versions; consumed and faked, never defined here (GAP-1147; GAP-1149).
- The physical document, its custody, its retention and its signature: rwb-document. The body reference of this contract points into the container RWB-P6-E1034-APP fixed.
- The central decision ledger, the approvals and the rule packages of rwb-decision; the local record goes through its library.
- A template event and the catalogue change it would need (GAP-1150; ASM-2097).
- The gateway-bff composite route, the screen field list and the masking: RWB-PLT-N001-CON.
- The deployment, the consumer groups, the dashboards, the alerts and the runbook of this capability.
