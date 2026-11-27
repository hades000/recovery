# RWB-P5-AD021-CON Retention classes and legal hold

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-AD021-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-021 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-021 for `rwb-document`; this is the contract baseline of the retention-class and legal-hold surface of `rwb-document` on base `/api/recovery/document/v1`. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P5-AD021-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the retention-class and legal-hold surface of `rwb-document` — the four resources of the class and the document retention state with their pages, the four reads this baseline claims, the four admin operations of the same surface that it names and does not claim, the error envelope with its message IDs, the three consumed P3 rows with their owner and their 2 s budget, the no-event position, the no-workflow position and the four fakes**, so that **the app story of this key, the retention run of `RWB-P5-E1017-APP`, the class and virus-scan story of `RWB-P5-E1041-APP` and the screens SCR-31 and SCR-32 build against one fixed, testable contract on Day 1, and a class value, a hold flag, a proposed disposal or a decision-log reference can never drift between the service, the run, the screens and the tests without a failing build**.

The service is `rwb-document` (P5): schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with event names `rwb.document.<Event>.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`. The legacy key is RWB-AD-021 and its two acceptance criteria belong to `RWB-P5-AD021-APP`; this story owns no legacy criterion and writes new ones that test the artefact only.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). In the monolith the retention class of a type, the hold flag of a case and the record of what the monthly job did were three values read in process by whichever module needed them, and the retention job wrote a row nobody's contract described. Those are exactly the values most likely to drift silently: a class renamed in one place and not the other, a hold flag lost on the way to the screen so a held document looks disposable, a proposed disposal answered 200 with an empty body so a reader cannot tell "nothing to do" from "not read", or an archive action recorded without its decision record so a disposal is not provable.

The baseline fixes the names the checks require and records what the sources leave open. It fixes the base, the four reads, the four resources and their pages, the class-in-force rule, the projection of the case hold onto a document, the action values, the decision code, the error envelope and the fakes. It records as a gap that no source names these paths or these field sets (GAP-1026; ASM-1944), that the plan gives this story a Contract dependencies list of None while three P3 rows are consumed (GAP-1026; ASM-1946), and that the admin load and the run are other stories' operations (GAP-1026; ASM-1945). The legal hold is the case attribute `recovery_case.legal_hold` (DF-CAS-020) in P3, read through the P3 case contract and projected: the Ownership Map has no document-level hold table, so the contract carries a projected flag and a reference, and no hold write (ASM-1936; ASM-0076 for the retention tables' owner).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the event and the queue names follow the platform rule rather than a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope, the `Idempotency-Key` rule and the retry and `.dlt` topic convention are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); where this document narrows them it does so explicitly.
- TSD P5 T3.1 and T3.2 are in force for the shapes and the list values: `document` (DF-DOC-001 to DF-DOC-011, DF-DOC-025 and DF-DOC-026), `retention_action` (DF-DOC-091 to DF-DOC-095), `document_type` (DF-REF-219, DF-REF-223, DF-REF-229) and the lists LOV-RETENTION, LOV-RETENTION-ACTION and LOV-RETENTION-END.
- TSD P1 T3.1 is in force for `retention_rule` (DF-REF-116 to DF-REF-126), which the Ownership Map and Architecture v5 slides 16, 41 and 44 JOB-17 place with P5 (ASM-0076).
- The Ownership Map is the only source of owners: `document`, `document_type`, `retention_rule` and `retention_action` are P5's in `rwb_document`; `recovery_case`, `lov_value` and `reference_row` are P3's; `decision_log_entry` is P7's; `delegation_limit` is P4's.
- No build dependency: this story is Day 1 by rule and has no H dependency (Template and Rules §R5.7).
- The rwb-case case contract and reference-data contract are published with their fakes, so the consumed rows of 12.2 have one owner document each.

### 4. Flow

1. Draft the OpenAPI 3.1 document of `rwb-document` with the four claimed reads, the four resources and their pages, and the error responses of section 14.
2. Fix the class-in-force rule: one class row in force per class code and rule version on a business date, `classCode` unique within a `ruleVersion`, and a type whose class is not in force refused with 422 and MSG-GEN-002 rather than answered with an invented class.
3. Fix the four resources and the optionality rule, with the legacy values as fixtures: LEGAL10Y for DEMAND_LETTER, GENERAL05Y for APPRAISAL_REPORT, rule version RET-2026.11.
4. Fix the projection of the hold onto `DocumentRetention`: `legalHold` and `legalHoldRef` are read from the P3 case answer on each read, and the answer carries no personal value.
5. Fix the action resource and its values: LOV-RETENTION-ACTION with ARCHIVED, LISTED, HELD and EXCEPTION, and the DOCRET decision-log reference on every action the run decided.
6. Record the three consumed P3 rows with their owner, their use, the 2 s budget and the fakes, and carry the plan's missing C entries as a gap row rather than adding rows to the plan.
7. Record the negative positions: no event of this key, no workflow and no activity of this story, and no Schedule — JOB-17 is `RWB-P5-E1017-APP`'s — and name the four admin operations of the same surface as other stories' operations.
8. Publish the nine contract tables of section 12 and the four fakes of 12.8, add the contract tests of section 7 with the drift test between each fake and the document, and tag the baseline for the app story, the run, the class load and the composite route.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A property is renamed, removed or retyped within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC7 |
| X3 | A class code exists in two rule versions at once with the same valid-from date | The class-in-force rule fails the load check and the contract test fails; no read answers an ambiguous class | None | AC2 |
| X4 | A `DocumentRetention` answer carries a personal value, or a fake returns a customer field | The privacy test fails the build; the answer carries the case number, the type code and the class only | None | AC3 |
| X5 | An action is answered without its LOV-RETENTION-ACTION value, or a decided disposal without its DOCRET reference | The contract test fails; the document states that the run writes both or neither | MSG-P7-003 (in the run, not in this read) | AC4 |
| X6 | A consumed P3 row is declared without its owner, or a fake drifts from the document | The drift test fails and the merge is blocked | None | AC6, AC7 |
| X7 | An event, a workflow or a Schedule is declared by this baseline | The absence test fails: no `rwb.document.DocumentStored.v1`, no `rwb.document.DocumentFieldsExtracted.v1`, no workflow on `rwb-document` and no Schedule in this key | None | AC7 |

### 6. INVEST check

| Criterion | Verdict | Note |
|---|---|---|
| Independent | Pass | No build dependency; reads the platform envelopes, the TSD P5 and TSD P1 shapes, the Ownership Map and the two rwb-case contracts only |
| Negotiable | Pass | The field-level names are settled with the consumers; the base, the four reads, the class rule, the action values and the consumed rows are fixed by the target architecture |
| Valuable | Pass | Unblocks the app story of this key, the retention run and the class load on Day 1, and gives SCR-31 and SCR-32 one shape to render |
| Estimable | Pass | One document, four resources, four claimed reads, three consumed rows, nine contract tables and four fakes |
| Small | Pass | Fits one sprint with the contract tests |
| Testable | Pass | Every criterion in section 7 is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the retention-class and legal-hold surface of rwb-document

  Background:
    Given the service naming rule of the platform library is in force
    Given the document, document_type, retention_action and retention_rule definitions of TSD P5 T3.1 and TSD P1 T3.1 are in force
    Given the lists LOV-RETENTION, LOV-RETENTION-ACTION and LOV-RETENTION-END of TSD P5 T3.2 are in force
    Given the rwb-case case contract and the rwb-case reference-data contract are published with their fakes

  Scenario: AC1 The four reads are declared on the service base and validate (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-document is published with this baseline
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /api/recovery/document/v1/retention-classes, GET /api/recovery/document/v1/retention-classes/{classCode}, GET /api/recovery/document/v1/documents/{documentId}/retention and GET /api/recovery/document/v1/documents/{documentId}/retention-actions
    Then every path sits under the base /api/recovery/document/v1 and no operation is declared on another service's base
    Then the class list answers RetentionClassPage and the class read answers RetentionClass
    Then the document retention read answers DocumentRetention and the action read answers RetentionActionPage
    Then each read names its Documents right R and its error statuses of section 14
    Then the four reads declare no Idempotency-Key, and no write operation of this surface is declared as provided by this baseline
    Then POST /api/recovery/document/v1/admin/retention-loads, POST /api/recovery/document/v1/admin/retention-loads/{loadId}/approve, GET /api/recovery/document/v1/admin/retention-runs and POST /api/recovery/document/v1/admin/retention-runs/{runId}/rerun are declared as the operations of RWB-P5-E1041-CON and RWB-P5-E1017-APP and not as part of this baseline

  Scenario: AC2 The RetentionClass resource and the version-in-force rule (new, D-RCV-60)
    Given the RetentionClass resource declared in the document
    When it is compared with the retention_rule fields of TSD P1 T3.1 and the class field of TSD P5 T3.1
    Then it carries classCode, labelEn, labelTh, productCode, docTypeCode, retentionMonths, ageBasisField, endAction, ruleVersion, validFrom and validTo
    Then classCode, productCode, docTypeCode, retentionMonths, ageBasisField, endAction and ruleVersion are required and labelEn, labelTh, validFrom and validTo are optional
    Then classCode is unique within one ruleVersion and exactly one row is in force on a business date
    Then the fixture in force is rule version "RET-2026.11" with class "LEGAL10Y" for type "DEMAND_LETTER" and class "GENERAL05Y" for type "APPRAISAL_REPORT"
    Then a class that is not in the rule version in force is refused with 422 and MSG-GEN-002 and never answered with an invented class
    Then endAction is one of the LOV-RETENTION-END values "ARCHIVE" and "REVIEW", and no period, age basis or end action is fixed in the document

  Scenario: AC3 DocumentRetention exposes the class and the projected hold and no personal value (new, D-RCV-60)
    Given the DocumentRetention resource declared in the document
    When it is compared with the document and retention_action fields of TSD P5 T3.1 and the case hold of TSD P3 T3.1
    Then it carries documentId, retentionClass, expiryDate, state, legalHold, legalHoldRef and lastAction
    Then documentId, retentionClass and state are required and legalHold is always present, so a missing answer is never read as "no hold"
    Then legalHold and legalHoldRef are the projection of recovery_case.legal_hold (DF-CAS-020) read through the P3 case contract, and the document states that rwb-document owns no hold row
    Then state is one of "ACTIVE", "LISTED", "HELD", "ARCHIVED" and "EXCEPTION", and the document states that these are the values of LOV-RETENTION-ACTION
    Then the resource carries no customer name, no national identifier, no address and no other personal value, and no example or fake carries one
    Then a P3 case contract that does not answer within 2 s answers MSG-GEN-006 and never a DocumentRetention with legalHold false

  Scenario: AC4 RetentionAction, the action values and the DOCRET reference (new, D-RCV-60)
    Given the RetentionAction resource and the RetentionActionPage declared in the document
    When they are compared with retention_action of TSD P5 T3.1 and T3.2
    Then RetentionAction carries documentId, runMonth, action, decisionLogId and recordedAt
    Then documentId, runMonth and action are required and decisionLogId and recordedAt are optional
    Then action is one of "ARCHIVED", "LISTED", "HELD" and "EXCEPTION" and no other value is accepted
    Then decisionLogId names the decision record of decision code "DOCRET" and the document states that a decided action without its record is refused by the run, not answered by this read
    Then runMonth is "YYYY-MM" and a document with no action yet answers an empty page, not an error
    Then the page carries no decision-log row beyond the identifier of the record

  Scenario: AC5 The error envelope and the status mapping (new, D-RCV-60)
    Given the error responses declared for the four reads
    When each status is compared with section 14
    Then every error is an RFC 9457 problem response carrying messageId, detail and instance
    Then 401 is declared for an unauthenticated caller and 403 for MSG-P4-002 and MSG-P4-003
    Then 404 is declared for a document or a class that does not exist
    Then 409 is declared for a read that meets a run in progress on the same document, with MSG-P2-006
    Then 422 is declared for MSG-GEN-001 and MSG-GEN-002, and 503 for MSG-GEN-006 and for a P3 timeout
    Then MSG-P1-002 is declared as the refusal of a class or a rule load and MSG-P1-020 as the run summary the read displays, each with its text copied from its source or marked as not specified in the source documents
    Then a refusal returns no partial page, no class and no document state

  Scenario: AC6 The three consumed P3 rows carry their owner, the 2 s budget and a fake (new, D-RCV-60)
    Given the consumed operations of the document
    When they are compared with the Ownership Map and the plan
    Then GET /api/recovery/case/v1/cases/{caseId} names P3 rwb-case as its owner, for the case and its legal_hold
    Then POST /api/recovery/case/v1/cases/{caseId}/legal-hold names P3 rwb-case as its owner and the document states that this service never calls it
    Then GET /api/recovery/case/v1/admin/lists/{listCode} names P3 rwb-case as its owner, for LOV-RETENTION, LOV-RETENTION-ACTION and LOV-RETENTION-END
    Then every consumed row states one hop, the 2 s timeout, the GET retry once with jitter and the breaker per downstream
    Then every failure of a consumed call maps to MSG-GEN-006 naming the system that failed and never to an accepted class or a hold state
    Then the missing C entries of these three rows are recorded as the gap of the key and no row is added to the metadata table
    Then the document names no other service's operation as consumed

  Scenario: AC7 No event, no workflow and no Schedule is declared, and the fakes match the document (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then 12.3 records None and states that rwb.document.DocumentStored.v1 and rwb.document.DocumentFieldsExtracted.v1 are the service's only two events and are published by other stories, never by this key
    Then 12.4 records None and 12.5 records None, and 12.6 names JOB-17 with RWB-P5-E1017-APP as its owner
    Then the four fakes of 12.8 answer the four reads of 12.1 with the fixtures of AC2 and AC4 and the hold of AC3
    Then the contract tests compare each fake with the document and fail on any drift
```

The seven criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by `RWB-P5-AD021-APP`, whose AC1 and AC2 are the legacy criteria of RWB-AD-021. No criterion fixes a business value beyond the legacy examples: the class codes, the rule version, the run month and the decision code are fixtures and data rows, not constants of the contract.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/document/v1`; the document never declares another service's path as provided | DP-13; Architecture v5 slide 41 notes |
| BR2 | The class of a type is answered only in the rule version in force on the business date, and a class not in force is refused, never invented | NFR-028; FSD P5 AC-EXC-P5-017-02; DL26 |
| BR3 | `classCode` is unique within one `ruleVersion`, and exactly one row is in force for a class code on a business date | TSD P1 T3.1 (`rule_version`, `valid_from`, `valid_to`); refdata change process |
| BR4 | A document's retention state is one of the LOV-RETENTION-ACTION values, and the contract fixes no other spelling | TSD P5 T3.2; section 9 |
| BR5 | The legal hold is the case attribute `recovery_case.legal_hold` projected onto the document; the contract carries no hold write and the service owns no hold row | REQ-DCM-016; NFR-072; Ownership Map (ASM-1936) |
| BR6 | A decided action carries its DOCRET decision-log reference, and the contract answers the identifier only, never a decision-log row | REQ-DCM-019; NFR-074; Ownership Map (`decision_log_entry` is P7's) |
| BR7 | Error responses use one envelope and one message ID per condition; the business message texts are copied unchanged from the legacy story | Architecture v5 platform baseline; Template and Rules §R7.2 s14 |
| BR8 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR9 | The document lists only operations owned by `rwb-document`; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-01 |
| BR10 | This key publishes no event and declares no workflow and no Schedule: the two `rwb.document` events, `RetentionRunWorkflow` and JOB-17 belong to other stories | Architecture v5 slides 41, 42, 43 and 44; TSD P5 T5.3 and T4 |
| BR11 | A GET declares no `Idempotency-Key`; the four reads of this baseline are GETs and store no answer | Architecture v5 slide 11 |
| BR12 | No personal value is declared in a resource, an example or a fake: the answers carry the case number, the type code, the class, the dates and the counts | PDPA minimisation; TSD P5 T3.1 |
| BR13 | The admin load and the run of the same surface are other stories' operations; naming them here does not claim them | WP B-P5-03 (`RWB-P5-E1041-CON`, `RWB-P5-E1017-APP`); ASM-1945 |

### 9. State transitions

| Baseline state | Event | Condition | Next state |
|---|---|---|---|
| Draft | Review opened | The four reads, the four resources and the three consumed rows are described | In review |
| In review | Consumer sign-off | The app story, the retention run, the class load and the composite route accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional label | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a status changes | New major version drafted |
| Baselined | Drift in a fake or a retired element returns | A contract test fails | In review |

This baseline declares **no document state machine and no case state machine**. The retention state of a document (section 9 of `RWB-P5-AD021-APP`) and the case status are read and reported, never driven, from this contract: `state` on `DocumentRetention` is the value of the last `retention_action` row of the month, written by the run, and this contract has no operation that writes it. A class row moves only when a class load is accepted (`RWB-P5-E1041-APP`): the accepted rows become the version in force from their `valid_from`, the earlier rows stay readable, and a refused or repeated load leaves the version in force unchanged.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of `rwb-document` | Owns the OpenAPI document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the plan's Contract dependencies list for the three P3 rows |
| Consuming teams (the app story of this key, `RWB-P5-E1017-APP`, `RWB-P5-E1041-APP`, the SCR-31 and SCR-32 route) | Review and sign off the parts they consume |
| RW-COMPLY, Compliance and PDPA officer | Confirms that the class, the period and the end action answer is the retention authority the legacy story gives the role |
| P3 owner (`rwb-case`) | Confirms the case and hold row and the reference-list row: the owner of `legal_hold`, `lov_value` and `reference_row` |
| P4 and P7 owners | Confirm that no DoA value and no decision-log row is declared here (`delegation_limit` is P4's, `decision_log_entry` is P7's) |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the `Idempotency-Key` rule and the naming rule this document reuses |
| Data steward | Confirms that no personal value is declared in an answer, an example or a fake |

The per-service login behind the document's security scheme is not part of this baseline: the document names the scheme "the rwb-document login (DP-02)" and the name is Not specified in the source documents (GAP-1026; ASM-1950). No delegation-of-authority level is declared or read: a retention class, a disposal and a legal hold carry no DoA value. The declared area and right of each read are enforced at gateway-bff (DP-19); no `rwb-access` contract is declared here.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| RetentionClass | classCode, labelEn, labelTh, productCode, docTypeCode, retentionMonths, ageBasisField, endAction, ruleVersion, validFrom, validTo; from `retention_rule` DF-REF-116 to DF-REF-126 and `document_type` DF-REF-219 and DF-REF-223 |
| RetentionClassPage | The paged answer of the class list: the page items as `RetentionClass` and the page metadata the platform convention fixes; the page field names are Not specified in the source documents (GAP-1026; ASM-1944) |
| DocumentRetention | documentId, retentionClass, expiryDate, state, legalHold, legalHoldRef, lastAction; the class and the expiry date from `document` DF-DOC-001 to DF-DOC-011 and the class row, the hold from the P3 case answer DF-CAS-020 |
| RetentionAction | documentId, runMonth, action, decisionLogId, recordedAt; from `retention_action` DF-DOC-091 to DF-DOC-095, with `recorded_at` from the standard columns |
| RetentionActionPage | The paged answer of the action read: the page items as `RetentionAction` and the page metadata; the page field names are Not specified in the source documents (GAP-1026; ASM-1944) |
| RetentionLoad | The load request of `RWB-P5-E1041-CON`: ruleVersion, validFrom and the class rows; declared as a shape and not claimed by this baseline |
| RetentionLoadResult | The load answer of `RWB-P5-E1041-CON`: the accepted and refused row counts and their reasons; declared as a shape and not claimed |
| RetentionRun | The run resource of `RWB-P5-E1017-APP`: runId, runMonth, ruleVersion, status, archivedCount, heldCount, exceptionCount, startedAt, finishedAt, archiveLocation; declared as a shape and not claimed |
| RetentionRunPage | The paged answer of the run read of `RWB-P5-E1017-APP`; declared as a shape and not claimed |
| error envelope | The platform RFC 9457 problem response with `messageId`, `detail` and `instance` |
| List values | LOV-RETENTION, LOV-RETENTION-ACTION (ARCHIVED, LISTED, HELD, EXCEPTION) and LOV-RETENTION-END (ARCHIVE, REVIEW), read through the rwb-case reference-data contract and never copied |

Every example in the document is synthetic and uses the legacy values: class "LEGAL10Y" for type "DEMAND_LETTER", class "GENERAL05Y" for type "APPRAISAL_REPORT", rule version "RET-2026.11", run month "2026-12", decision code "DOCRET", the stored date 1 November 2021, the expiry date 1 November 2026 and the run date 2026-12-06. The holder and the document name in MSG-P5-004 remain placeholders. The set of LOV-RETENTION values is not enumerated in the source documents; the two class codes above are the ones the legacy criteria use (GAP-1026; ASM-1949).

### 12. Contract

#### 12.1 REST operations provided

Owner P5 (`rwb-document`); base `/api/recovery/document/v1`.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/api/recovery/document/v1/retention-classes` | Query: productCode, docTypeCode, page, size; answer `RetentionClassPage` | Documents R | Not applicable |
| GET | `/api/recovery/document/v1/retention-classes/{classCode}` | Answer `RetentionClass` in the rule version in force | Documents R | Not applicable |
| GET | `/api/recovery/document/v1/documents/{documentId}/retention` | Answer `DocumentRetention` | Documents R | Not applicable |
| GET | `/api/recovery/document/v1/documents/{documentId}/retention-actions` | Answer `RetentionActionPage` | Documents R | Not applicable |

The four reads are this baseline's design: no source names these paths, their query parameters or their answer shapes (GAP-1026; ASM-1944). Error statuses are those of section 14.

The same surface carries four admin operations that this baseline **names and does not claim**:

| Method | Path | Owner story | Position of this baseline |
|---|---|---|---|
| POST | `/api/recovery/document/v1/admin/retention-loads` | RWB-P5-E1041-CON and RWB-P5-E1041-APP | Declares `RetentionLoad` and `RetentionLoadResult` as shapes; the operation and its `Idempotency-Key` belong to the class load |
| POST | `/api/recovery/document/v1/admin/retention-loads/{loadId}/approve` | RWB-P5-E1041-CON and RWB-P5-E1041-APP | Not claimed; the approval authority is the reference-data holder's |
| GET | `/api/recovery/document/v1/admin/retention-runs` | RWB-P5-E1017-APP | Declares `RetentionRunPage` as a shape; the read belongs to the run |
| POST | `/api/recovery/document/v1/admin/retention-runs/{runId}/rerun` | RWB-P5-E1017-APP | Not claimed; answers 409 while a run is in progress, in the run's own contract |

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 `rwb-case` | The case, its scope and `legal_hold` (DF-CAS-020), projected onto `DocumentRetention`, faked (RWB-P3-E1018-CON) |
| POST | `/api/recovery/case/v1/cases/{caseId}/legal-hold` | P3 `rwb-case` | The hold is placed and lifted by `rwb-case`; this service never calls it, and it is listed so the baseline shows that no hold write exists here |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 `rwb-case` | LOV-RETENTION, LOV-RETENTION-ACTION and LOV-RETENTION-END at the version in force, faked (RWB-P3-E1043-CON) |

Every row is one hop with a 2 s timeout, a GET retry once with jitter and a breaker per downstream (DP-11, ADR-020). A failed read maps to MSG-GEN-006 naming the system that failed and never to an accepted class or a hold state. The plan's Contract dependencies list for this story is **None**, so the three rows are consumed and faked without a C entry; that is recorded as the gap of the key and no row is added to the metadata table (GAP-1026; ASM-1946).

#### 12.3 Events published

None. `rwb-document` publishes exactly two events, `rwb.document.DocumentStored.v1` and `rwb.document.DocumentFieldsExtracted.v1`, on `rwb.document.events.v1` (Architecture v5 slides 41, 42 and 43); a class read, a document retention read, an action read and a class load publish neither, and this key publishes no event at all. The decision record of a run is published by the decision-record library of `RWB-P5-E1017-APP` on the shared decision-record topic, not by this baseline.

#### 12.4 Events consumed

None. The hold is read synchronously through the P3 case contract on the flight of each read, so the contract needs no inbox, no projection and no topic subscription; a hold placed a minute ago is already visible on the next read.

#### 12.5 Workflows and activities

None. The run is the `RetentionRunWorkflow` of `RWB-P5-E1017-APP` on task queue `rwb-document`; this baseline declares no workflow, no activity and nothing on the queue.

#### 12.6 Schedules

| Schedule | Job | Owner | Position of this baseline |
|---|---|---|---|
| Retention | JOB-17, monthly, first Sunday 02:30 Asia/Bangkok | RWB-P5-E1017-APP | Named because the `runMonth` of `RetentionAction` and the states of `DocumentRetention` exist only after this Schedule runs; this baseline creates no Schedule and changes none |

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `document` | P5 (`rwb_document`) | The class, the type, the case and the state of a document, and its stored date, as read by `DocumentRetention` |
| `document_type` | P5 (`rwb_document`) | The class of a type and the type table version, read to resolve `RetentionClass` |
| `retention_rule` | P5 (`rwb_document`) | The class rows, their period, age basis, end action and rule version, read in the version in force (ASM-0076) |
| `retention_action` | P5 (`rwb_document`) | The action, run month and decision-log reference of each month, read by `RetentionAction` |
| outbox, inbox and idempotency library tables | PLT library, created in `rwb_document` | Declared by the service template; this baseline writes no row and stores no answer |

`recovery_case` and `lov_value` / `reference_row` are P3's, `decision_log_entry` is P7's and `delegation_limit` is P4's; they are named only as consumed answers and never declared as this service's tables (DP-01). No ACE view is read (DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case WireMock | `GET /cases/{caseId}` answers case "RW-2026-000123" with `legal_hold` true, and case "RW-2026-000124" with `legal_hold` false; a case outside the scope answers 403; a delayed answer beyond 2 s | App story, contract tests, run tests |
| rwb-case reference-data WireMock | `GET /admin/lists/{listCode}` answers LOV-RETENTION with "LEGAL10Y" and "GENERAL05Y"; LOV-RETENTION-ACTION with "ARCHIVED", "LISTED", "HELD" and "EXCEPTION"; LOV-RETENTION-END with "ARCHIVE" and "REVIEW"; a delayed answer beyond 2 s | App story, contract tests |
| retention contract stub | The four reads: class "LEGAL10Y" for "DEMAND_LETTER" and "GENERAL05Y" for "APPRAISAL_REPORT" in rule version "RET-2026.11"; a class not in force (422, MSG-GEN-002); a document past its period (LISTED with a DOCRET reference); a document under hold (HELD); an empty action page; a read meeting a run in progress (409, MSG-P2-006) | App story, run tests, contract tests |
| class and rule fixture | Rule version "RET-2026.11" with its valid-from date, the two class rows above and their end actions; the periods are fixture placeholders and not business values (ASM-1939) | App story, contract tests |

A drifted fake fails the drift test of AC7. The four admin operations of 12.1 have their own fakes in the contracts that own them and are not declared here.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 3 consumed | The class list, the class read, the document retention read and the action read; the case read, the hold read and the reference-list read of P3; one hop and 2 s on the consumed calls |
| Kafka | 0 published by this key, 0 consumed | The service's two events are declared and belong to other stories |
| Temporal | None | `RetentionRunWorkflow` and JOB-17 are `RWB-P5-E1017-APP`'s |
| File | None | No blob is named, read or written by this contract; the archive location of a run is the run's answer and `RWB-PLT-TE012-APP`'s storage |

### 13. Solution plan

**Deliverables.** The OpenAPI 3.1 document `openapi/rwb-document-retention-v1.yaml` with the four reads and the four resources; the contract README rows for the class-in-force rule, the hold projection, the action values, the decision code and the positions of 12.3 to 12.6; and the four WireMock mapping sets of section 12.8.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/document/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H, C, I and X lists of the metadata table are empty: this baseline adds no build dependency of its own (it is Day 1 by rule), and the platform and rwb-case contracts it names are the ones the app story declares. DP-05 is applied as the negative: no resource of this contract carries an ACE view, an `account_ext` row or a customer attribute, and where a screen needs a customer value it is requested through the owner's contract. DP-13 fixes the base of the four reads. DP-19 places SCR-31 and SCR-32 behind the composite route, which this contract serves with its four answers.

**Build steps**

1. Write the four reads with their paths, query parameters, resources and error responses; validate the document in the pipeline.
2. Fix the class-in-force rule, the uniqueness of `classCode` within a `ruleVersion` and the optionality rule of AC2 as schema constraints and README rows.
3. Fix `DocumentRetention` and the hold projection of AC3, with `legalHold` always present and the fail-closed rule of AC3's last line.
4. Fix `RetentionAction` and the LOV-RETENTION-ACTION values of AC4, with the DOCRET reference and the empty-page rule.
5. Record the three consumed rows with their owner, their use, the 2 s budget and the gap of the missing C entries.
6. Record the positions of 12.3 to 12.6 and the four admin operations that this baseline names and does not claim.
7. Publish the four fakes and the contract tests of section 7; a drift between a fake and the document fails the build.
8. Baseline tag and the consumer sign-off note, with the app story, the run, the class load and the composite route.

**Done when.** The OpenAPI artefact validates in the pipeline, the seven contract tests pass, the four fakes answer every read of 12.1 and every consumed row of 12.2, the drift test is green, and `RWB-P5-AD021-APP`, `RWB-P5-E1017-APP` and `RWB-P5-E1041-APP` have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-002 | A change to a write-once legal document is attempted (the legacy refusal of this key) | Legal documents cannot be changed. Add a new version instead. |
| MSG-P5-003 | A document is in the review queue and its class is not yet confirmed | Some fields need checking. The document is in the review queue. |
| MSG-P5-004 | An original document is overdue back from its holder | {document} is due back from {holder} since {date}. |
| MSG-GEN-001 | A required query field of a read is empty | Enter {field}. |
| MSG-GEN-002 | A value is outside its range, or a class is not in the rule version in force | The message text of MSG-GEN-002 is Not specified in the source documents (GAP-1026; ASM-1947); its ID and its 422 status are fixed by the baseline |
| MSG-P4-002 | The caller holds no Documents right R for the read | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. |
| MSG-P1-002 | A class or a rule load fails a check, or repeats a load | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P1-020 | The run summary alert of the month names the cases kept on legal hold | The run summary text is Not specified in the source documents (GAP-1026; ASM-1947); the ID and the count it carries are the run's |
| MSG-P2-006 | A read meets a run in progress on the same document | The message text of MSG-P2-006 is Not specified in the source documents (GAP-1026; ASM-1947); its ID and its 409 status are fixed by the baseline |
| MSG-GEN-006 | A consumed P3 read does not answer in time, or the breaker is open | {system} is not available. Your request is queued and will be retried. |
| MSG-P7-003 | The decision record of a run cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs and wording are contract elements. The five business messages are copied unchanged from RWB-AD-021 section 14 and keep their legacy types; MSG-P4-003, MSG-P2-006, MSG-P1-002, MSG-P1-020, MSG-GEN-002 and MSG-GEN-006 are the platform and cross-service messages whose text is either copied from its own source or marked as not specified; MSG-P7-003 is the decision-record refusal the run raises and this read never raises. Thai text for each message follows decision DL10.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled and `instance` naming the request. The status mapping is 401 unauthenticated, 403 for MSG-P4-002 and MSG-P4-003, 404 for a document or a class that does not exist, 409 for MSG-P2-006, 422 for MSG-GEN-001 and MSG-GEN-002, and 503 for MSG-GEN-006 and a P3 timeout. The four reads are GETs and declare no `Idempotency-Key`.

### 15. Screens and states

SCR-31 Document review queue and SCR-32 Document custody are the two screens the legacy story names, and their legacy states are Loading; list; reviewed for SCR-31 and Out; overdue; returned for SCR-32. The contract serves them through the gateway-bff composite route of DP-19 (`RWB-PLT-N001-CON`), which calls this service once for the panel and the badge and merges the answers into the screen model. This baseline fixes the operation answers only: the screen field list, the route specification, the merge order and the read-only projection belong to `RWB-PLT-N001-CON`, and the badge states that render these answers are those of section 15 of `RWB-P5-AD021-APP`.

The two answers the screens depend on are fixed here: `DocumentRetention` with `state` in ACTIVE, LISTED, HELD, ARCHIVED and EXCEPTION, and `RetentionActionPage` with one row per month. A screen that shows a held document as disposable is a drift of the answer, and the drift test of AC7 fails it.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-021-01 | AC2, AC3, AC4, BR2, BR3, BR5, BR6 | Contract | Appraisal report of class GENERAL05Y stored on 1 November 2021 on case RW-2026-000123 with no hold; JOB-17 runs on 6 December 2026; the document is listed with its DOCRET record (the legacy Expiry case, answered against the contract) |
| TC-AD-021-02 | AC2, AC3, BR5 | Contract | The same appraisal report with case RW-2026-000123 under legal hold; `legalHold` true with its reference and `state` HELD (the legacy Hold case, answered against the contract) |
| TC-AD-021-03 | AC1, AC5, BR7 | Component | A role without the Documents right R calls the four reads; refused with MSG-P4-002 and the problem envelope, and nothing returned |

The three legacy test cases of RWB-AD-021 are listed in the order of the legacy story; each is answered here at contract level against the artefact and the fakes, and its business outcome is proved by `RWB-P5-AD021-APP`. The legacy `Test` column ("Expiry", "Hold", "A role without the right is refused with MSG-P4-002") is kept in the Data column. Legacy levels map System to End to end and Access to Component; the end-to-end copies of TC-AD-021-01 and TC-AD-021-02 sit in `RWB-P5-AD021-APP`, and no integration harness copy is named because no `RWB-ITG-AD021-ITG` story exists in the plan. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the class codes, the periods, the age bases, the end actions, the rule version, the run month, the list values and the decision code stay data rows, fixture values or list values.
- No personal value in a schema, an example or a fake: the case number, the type code, the class, the dates and the counts only; MSG-P5-004 keeps its placeholders.
- ACE data is reached only through the owner's contract or a `v_ace_*` view; this document declares no ACE view, no `account_ext` row and no cross-schema join.
- The contract names only `rwb-document` tables and only operations owned by `rwb-document`; the rwb-case rows are consumed and faked, never declared as provided (DP-01).
- The hold is projected and never owned: no hold write, no hold column and no hold state is declared.
- The decision log is P7's: the contract answers a `decisionLogId` reference and never a decision-log row, and it disposes of nothing.
- One REST base per service; a document that names another service's base or topic as its own fails the review (DP-13).
- No event, no workflow and no Schedule is declared by this baseline, and the absence test of AC7 fails a build that declares one.
- Every example is synthetic; no production payload is copied into a schema or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DCM-016 | A legal hold stops deletion and expiry while it is in place, overriding the retention class | The `legalHold` and `legalHoldRef` of `DocumentRetention`, the P3 case row of 12.2 and the projected-hold rule of BR5 | TC-AD-021-02 |
| REQ-DCM-019 | Records retention runs by class, and a disposal or an extension is a recorded decision, never silent | `RetentionAction`, the LOV-RETENTION-ACTION values, the DOCRET reference of BR6 and the class-in-force rule of BR2 | TC-AD-021-01 |
| REQ-DCM-020 | The hub carries a records management position signed by Compliance and Legal | The `RetentionClass` and `RetentionAction` answers that the position's storage, hold and disposal statements are read against | TC-AD-021-01, TC-AD-021-02 (the position itself is outside this service) |

The legacy story RWB-AD-021 carries **no requirement ID of its own**; the three IDs above are the FSD P5 requirements the surface serves. NFR-028 (a class per type, periods not set), NFR-029 (write-once inside the period), NFR-072 and NFR-074 are the non-functional statements behind the same shapes.

| Decision or pattern | Where it sits in this story |
|---|---|
| DP-01 | Only `rwb-document` tables declared; the three P3 rows consumed and faked |
| DP-05 | No ACE view and no customer attribute in any resource |
| DP-11 | The three consumed rows with one hop, a 2 s timeout, a fake and a fail-closed refusal |
| DP-13 | Base `/api/recovery/document/v1` on all four reads |
| DP-19 | SCR-31 and SCR-32 behind gateway-bff, served by the four answers |
| ADR-013 | The service owns its schema inside ACE PostgreSQL |
| ADR-014 | The `rwb_document` schema and the rwb-document login (name not specified) |
| ADR-020 | Contract-first REST, one hop, 2 s timeout |
| ASM-0076 | `retention_rule` is P5's, so the class rows are read locally and not through another service |

The legacy key is RWB-AD-021; its AC1 and AC2 are owned by `RWB-P5-AD021-APP`, its class load and virus-scan part by `RWB-P5-E1041-APP`, and its run by `RWB-P5-E1017-APP`.

### 19. Out of scope

- The build of the four reads, the panel, the badge and the action panel: `RWB-P5-AD021-APP`.
- The retention run, JOB-17, the archive action, the run answer and the re-run: `RWB-P5-E1017-APP`.
- The class load, its approval and the virus scan on intake: `RWB-P5-E1041-CON` and `RWB-P5-E1041-APP`.
- The personal data screen SCR-47 and the PDPA data-subject paths (Epic 8).
- The gateway-bff composite route, the screen field list and the merge order of SCR-31 and SCR-32: `RWB-PLT-N001-CON`.
- The case and hold contract of P3, the reference-data contract of P3, the decision ledger of P7 and the DoA table of P4: consumed or named, never defined here.
- The Helm chart, the retry policy values, the topic and DLT provisioning, the metrics, the alerts and the runbook.
