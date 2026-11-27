# RWB-P5-E1041-CON Retention classes and virus scan on intake

**Version 3 changes.**

- MSG-GEN-006 carries the English text of Error and Message Standard v6 (RD-P1-004).

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1041-CON |
| Readiness decisions | RD-P1-004 |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Contract version | v1 (base /api/recovery/document/v1, topic rwb.document.events.v1) |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-041 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Size | Set by the squad at refinement |
| Patterns applied | DP01, DP03, DP07, DP10, DP11, DP13, DP15, DP18, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | Not specified in the source documents (GAP-1026) |
| Integration dependencies | rwb-case case contract and rwb-case reference-data contract, published with their fakes (see Background) |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-022, FR-P5-023, FR-P5-024, FR-P5-025) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: the contract baseline of the retention and virus-scan API of `rwb-document` is split out of legacy RWB-E1-041 and published on base `/api/recovery/document/v1` with the topic `rwb.document.events.v1`, the class load, the rule and scan reads, the event schema and the fakes. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P5-E1041-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 19 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the retention and virus-scan API of `rwb-document` — the retention rule read and the class load and approve operations, the scan request and the two scan-status reads on base `/api/recovery/document/v1`, the `RetentionRule`, `RetentionLoad`, `RetentionAction` and `ScanStatus` shapes, the retention classes as reference data, the error envelope with every message ID and its HTTP status, the `Idempotency-Key` rule, the `rwb.document.RetentionApplied.v1` event schema with no personal data, and the fakes with their drift test**, so that **the app story of this legacy key, the upload path that scans before it stores, the intake pipeline, the screens SCR-44 and SCR-47 and the wave-1 harness build against a fixed, testable contract on Day 1, and a class code, a period, an end action, a scan value or an event field can never drift between the service that writes it and the callers that read it without a failing build**.

The service is `rwb-document` (P5): schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with event names `rwb.document.<Event>.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`. The legacy key is RWB-E1-041 and its ten acceptance criteria belong to `RWB-P5-E1041-APP`; this story owns no legacy criterion and writes eight new ones that test the artefact only.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). In the monolith the retention class of a type, the period and the end action of a class, the scan result of a file and the record of what the monthly job did were values passed in process between the store, the upload, the intake and the job, and the retention class table was loaded through a reference-data surface that no document contract described. Under the target architecture the store, the upload and the intake are three stories of the same service and a period, a scan value or an event field that changes without its consumers is a silent break. The shapes most likely to drift silently are exactly these:

- a class code or an end action renamed in the class load, so the run archives what Compliance meant to review;
- a period read differently by the load and the run, so the same class expires on two dates;
- a scan answer that says 200 with an empty body instead of CLEAN or INFECTED, so an uploader cannot tell "safe" from "not scanned";
- an `Idempotency-Key` honoured by the scan but not by the class load, so a repeated load creates a second version in force;
- an event payload that carries a customer value or a document name, so the retention decision leaks personal data to every consumer;
- an error returned with the wrong status or without a `messageId`, so a caller cannot tell a refused load from a missing class.

The baseline fixes the names the checks require and records what the sources leave open: no source names the paths or the field sets of the class load, the rule read or the scan operation (GAP-0996; ASM-1776); the legacy class table code RETENTION_CLASS and its columns are not the `retention_rule` shape the Ownership Map gives to P5 (GAP-0996; ASM-1778); the event `rwb.document.RetentionApplied.v1` is new, because the service catalogue names only two events (GAP-0996; ASM-1777); and the plan gives this story an empty Contract dependencies list while two P3 reads are consumed (GAP-0996; ASM-1776). Nothing else is guessed and no business value is fixed.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the event and the queue names follow the platform rule rather than a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope, the `Idempotency-Key` rule and the retry and `.dlt` topic convention are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); where this document narrows them it does so explicitly.
- TSD P5 T3.1 and T3.2 are in force for `retention_rule` (DF-REF-116 to DF-REF-127), `retention_action` (DF-DOC-091 to DF-DOC-095), the scan fields of `document_intake` (DF-DOC-058, DF-DOC-059) and the lists LOV-RETENTION, LOV-SCAN-RESULT (CLEAN, INFECTED), LOV-RETENTION-ACTION (ARCHIVED, LISTED, HELD, EXCEPTION) and LOV-RETENTION-END (ARCHIVE, REVIEW).
- The Ownership Map is the only source of owners: `retention_rule`, `retention_action`, `document`, `document_intake` and `document_type` are P5's in `rwb_document`; `recovery_case`, `lov_value` and `reference_row` are P3's; `decision_log_entry` is P7's; `interaction` is P1's.
- The `rwb-case` case contract and reference-data contract are published with their fakes, so the two consumed rows of 12.2 have one owner document each.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

The status and the release are the run defaults of D-RCV-60: the story is Draft (realignment v1) and the release is 30 November 2026 (tentative), with no approval recorded in the sources read (ASM-1775).

### 4. Flow

1. Draft the OpenAPI 3.1 document `openapi/rwb-document-retention-v1.yaml` with the eight operations of 12.1, the five resources of section 11 and the error responses of section 14, on the single base `/api/recovery/document/v1`.
2. Fix the `RetentionRule` shape and the class-in-force rule: one row per `record_class` in a `rule_version`, exactly one version in force on a business date, and a class that is not in force refused with 422 rather than answered with an invented class.
3. Fix the class load: the multipart request with `validFrom` and the table code RETENTION_CLASS, the `RetentionLoad` answer with the accepted and refused rows, the two rights (C to load, A to approve), the row checks of the legacy story and the whole-load refusal.
4. Fix the scan resource: the synchronous `POST /scans` request and its `ScanResult` answer, the declared budget, the 503 of an unavailable engine, and the two `ScanStatus` reads that answer a stored document and an intake item.
5. Fix `RetentionAction` and the action values, with the decision-record reference of a decided action and the empty-page rule.
6. Fix the `rwb.document.RetentionApplied.v1` schema: the topic, the key, the nine payload fields, the CloudEvents envelope, the no-personal-data rule and the count of the service's events.
7. Map every failure to the error envelope and a message ID, status by status, and record the two consumed P3 rows with their owner, their use, the 2 s budget and the missing C entries.
8. Record the `Idempotency-Key` rule on the three POSTs and the natural keys behind it, then publish the six fakes, the contract tests and the drift test, tag the baseline and hand it to RWB-P5-E1041-APP, RWB-P5-E1026-CON, RWB-P5-E1049-APP and the wave-1 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A property is renamed, removed or retyped within major version 1 | The contract test fails; the change needs a corrected document or a new major version | None | AC2, AC3 |
| X3 | The scan answer is a 200 with an empty or partial body | The contract test fails: `scanResult` is required and is CLEAN or INFECTED, never absent | MSG-GEN-001 | AC3, AC6 |
| X4 | The class load accepts a row it should refuse, or refuses one it should accept | The contract test fails on the row checks of AC4; the version in force is unchanged | MSG-P3-027 | AC4 |
| X5 | The event carries a personal value, a document name, a file byte or a tenth field | The AsyncAPI schema test and the no-personal-data test fail | None | AC5 |
| X6 | An operation returns a status or a `messageId` outside the mapping of AC6 | The contract test fails; the document states one status per condition | None | AC6 |
| X7 | A class load or a scan repeats a request with the same key and creates a second version or a second result | The contract test fails on the stored-answer rule of AC7 | MSG-GEN-004 | AC7 |
| X8 | A fake drifts from the document, or a scan event is declared besides the retention event | The drift test and the absence test fail the build | None | AC8 |

### 6. INVEST check

| Criterion | Verdict | Note |
|---|---|---|
| Independent | Pass | No build dependency; reads the platform envelopes, TSD P5 T3, the Ownership Map and the two `rwb-case` contracts only |
| Negotiable | Pass | The field-level names are settled with the consumers; the base, the eight operations, the two natural keys, the event schema and the error mapping are fixed by the target architecture and the legacy section 12 |
| Valuable | Pass | Unblocks the app story, the upload path, the intake pipeline and the harness on Day 1 |
| Estimable | Pass | One document, five resources, eight operations, two consumed rows, nine contract tables and six fakes |
| Small | Pass | Fits one sprint with its contract tests |
| Testable | Pass | Every criterion in section 7 is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the retention and virus-scan API of rwb-document

  Background:
    Given the service naming rule of the platform library is in force
    Given the retention_rule, retention_action and document_intake definitions of TSD P5 T3.1 are in force
    Given the lists LOV-RETENTION, LOV-SCAN-RESULT, LOV-RETENTION-ACTION and LOV-RETENTION-END of TSD P5 T3.2 are in force
    Given the rwb-case case contract and the rwb-case reference-data contract are published with their fakes

  Scenario: AC1 The eight operations are declared on the service base and validate (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-document is published with this baseline
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /api/recovery/document/v1/retention-rules and GET /api/recovery/document/v1/retention-rules/{classCode}
    Then it declares POST /api/recovery/document/v1/admin/retention-loads, POST /api/recovery/document/v1/admin/retention-loads/{loadId}/approve and GET /api/recovery/document/v1/admin/retention-loads/{loadId}
    Then it declares POST /api/recovery/document/v1/scans, GET /api/recovery/document/v1/documents/{documentId}/scan-status and GET /api/recovery/document/v1/intake-items/{intakeItemId}/scan-status
    Then every path sits under the base /api/recovery/document/v1 and no operation is declared on another service's base
    Then the rule reads declare the Documents right R, the load declares Reference data right C and the approve declares Reference data right A
    Then the document declares no run resource, no rerun operation and no class panel read, and names them as the operations of RWB-P5-E1017-APP and RWB-P5-AD021-CON

  Scenario: AC2 RetentionRule fixes the rule shape and the class-in-force rule (new, D-RCV-60)
    Given the RetentionRule and RetentionRulePage resources declared in the document
    When they are compared with retention_rule of TSD P5 T3.1 and the class field of document_type
    Then RetentionRule carries classCode, docTypeCode, productCode, tableName, retentionMonths, ageBasisField, endAction, ruleVersion, validFrom, validTo and approvedByRole
    Then classCode, docTypeCode, retentionMonths, ageBasisField, endAction and ruleVersion are required and the other properties are optional
    Then classCode, docTypeCode, retentionMonths, ageBasisField, endAction and ruleVersion are the identifiers of a class row and never a value of the contract
    Then endAction is one of the LOV-RETENTION-END values "ARCHIVE" and "REVIEW", and retentionMonths is an integer from 1 to 600
    Then exactly one ruleVersion is in force on a business date and a class that is not in force is answered 404, never invented
    Then the fixture in force is rule version "RET-2026.11" with class "LEGAL10Y" at 120 months and end action "REVIEW" and class "GENERAL05Y" at 60 months and end action "ARCHIVE"
    Then the document states that the class panel read of RWB-P5-AD021-CON is a projection of the same rows and is not re-declared here

  Scenario: AC3 The scan resource answers CLEAN or INFECTED and ScanStatus is fixed (new, D-RCV-60)
    Given the ScanRequest, ScanResult and ScanStatus resources declared in the document
    When they are compared with the scan fields of document_intake and the legacy published interface
    Then ScanRequest carries storageRef and sha256 as required, intakeId and source as optional, and no file name and no file byte
    Then ScanResult carries scanResult, scannedAt, threatFound and quarantineRef, with scanResult required and one of "CLEAN" and "INFECTED"
    Then a CLEAN answer carries threatFound false and no quarantineRef, and an INFECTED answer carries threatFound true, a quarantineRef and no stored document
    Then ScanStatus carries documentId or intakeItemId, scanResult, scannedAt, threatFound and quarantineRef, and null is never read as "safe"
    Then the document declares the budget of POST /scans as the property rwb.document.scan.timeout-seconds with the legacy value 30, and records it as the one declared exception to the 2 s one-hop rule
    Then an engine that does not answer maps to 503 with MSG-P5-022 and never to a CLEAN answer
    Then the scanning engine, its provider, its capacity and its queue are declared nowhere in the document

  Scenario: AC4 RetentionLoad fixes the class load, the row checks and the two rights (new, D-RCV-60)
    Given the RetentionLoad resource and the two admin operations declared in the document
    When they are compared with the legacy class load and the reference-load step of the story
    Then RetentionLoad carries loadId, table, ruleVersion, validFrom, rowCount, acceptedCount, refusedCount, refusedRows and status
    Then status is one of "LOADED", "APPROVED" and "REFUSED", and refusedRows carries row and error for every refused row
    Then the load request is multipart with a file and validFrom, and table is the legacy code "RETENTION_CLASS"
    Then the document states that the accepted rows are written to retention_rule and that the legacy template columns map onto record_class, retention_months, age_basis_field, end_action and rule_version
    Then a load with a period of 0 months, an end action other than ARCHIVE or REVIEW, or a repeated class code in one version is refused in full with 422 and MSG-P3-027
    Then a load for a version already in force answers 409 with MSG-P3-027 and leaves the version in force unchanged
    Then the load declares Reference data right C and the approve declares Reference data right A, and the same caller does not hold both rights for one load

  Scenario: AC5 RetentionAction and the RetentionApplied event are declared with no personal data (new, D-RCV-60)
    Given the RetentionAction resource and the AsyncAPI fragment of this baseline
    When they are compared with retention_action of TSD P5 T3.1 and the service catalogue
    Then RetentionAction carries documentId, runMonth, action, retentionClass, ruleVersion, decisionLogId and decidedAt
    Then documentId, runMonth, action and retentionClass are required, runMonth is "YYYY-MM" and action is one of "ARCHIVED", "LISTED", "HELD" and "EXCEPTION"
    Then rwb.document.RetentionApplied.v1 is declared on the topic rwb.document.events.v1, keyed by caseId, with the nine payload fields documentId, caseId, runMonth, action, retentionClass, ruleVersion, expiredAt and decisionLogRef and no tenth field
    Then the envelope is CloudEvents 1.0 in binary mode and the payload carries no customer name, no national identifier, no document name, no file byte and no decision-log row
    Then the document states that this key publishes one event and that the store, the extraction and the intake events belong to their own stories
    Then the document states that no scan event is declared, because the scan result is an attribute of the document and of the intake item

  Scenario: AC6 The error envelope and the message-to-status mapping are fixed (new, D-RCV-60)
    Given the error responses declared for the eight operations
    When each status is compared with the legacy section 14 and the platform envelope
    Then every error is an RFC 9457 problem response with messageId, detail and instance, and no partial page and no partial load
    Then 401 is declared for an unauthenticated caller and 403 for MSG-P4-002
    Then 404 is declared for a document, an intake item, a class or a load that does not exist
    Then 409 is declared for MSG-P3-027 on a version already in force and for MSG-GEN-004 on a concurrent request
    Then 422 is declared for MSG-P5-016, MSG-P3-027 and MSG-GEN-001
    Then 503 is declared for MSG-P5-022, MSG-P7-003 and MSG-GEN-006
    Then the text of every message is copied unchanged from the legacy story or marked as not specified in the source documents

  Scenario: AC7 The Idempotency-Key rule and the natural keys are fixed (new, D-RCV-60)
    Given the Idempotency-Key rule of the three POST operations
    When it is compared with the legacy idempotency rows of the two jobs and the family
    Then POST /scans requires the header, keyed by storageRef and sha256, and a repeat inside the window answers the first stored result with no second scan and no second audit entry
    Then POST /admin/retention-loads requires the header, keyed by table and ruleVersion, and a repeat answers the first load rather than a second version
    Then the approve operation requires the header and is keyed by loadId, and a second approve answers 409
    Then the five GET operations declare no Idempotency-Key and store no answer
    Then a repeat inside the window creates no second version in force, no second scan result and no second event
    Then a concurrent request is answered 409 with MSG-GEN-004 and never by a second stored set

  Scenario: AC8 The six fakes match the document and no scan event is declared (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed and the fakes are run against the document
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the six fakes of 12.8 answer the eight operations of 12.1 and the two consumed rows of 12.2 with the legacy values, including class "LEGAL10Y" at 120 months, class "GENERAL05Y" at 60 months, rule version "RET-2026.11", run month "2026-12" and the run date 2026-12-06
    Then the drift test compares each fake with the document and fails on any mismatch of a path, a status, a field name or a required flag
    Then the absence test fails a build that declares a scan event, a second retention event or an operation on another service's base

  Scenario: AC9 The naming, topic, versioning, personal-data, ledger and idempotency rules of section 8 hold on the artefact (new, D-RCV-60)
    Given the base, the topic, the schemas, the examples and the POST operations of this baseline
    When they are compared with the business rules BR1, BR2, BR3, BR8, BR9, BR11 and BR12 of section 8
    Then every path sits under /api/recovery/document/v1 and the topic is rwb.document.events.v1 with its retry and .dlt topics
    Then a change inside major version 1 is additive and no property is removed, renamed, retyped or newly required
    Then no schema, example or fake carries a customer name, a national identifier, a document name or a custody holder
    Then no ledger table, ledger row or ledger operation is declared, each POST declares Idempotency-Key and each GET declares none
    Then the document declares exactly one event, rwb.document.RetentionApplied.v1, and no scan event
```

The eight criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by `RWB-P5-E1041-APP`, whose AC1 to AC10 are the legacy criteria of RWB-E1-041. No criterion fixes a business value beyond the legacy examples: the class codes, the periods, the rule version, the run month and the decision code are fixtures and data rows, not constants of the contract.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/document/v1` on every declared operation | DP-13; Template and Rules §R4 |
| BR2 | One topic per service: `rwb.document.events.v1`, with the retry and `.dlt` topics of the platform convention | DP-09; Architecture v5 slides 16 and 42 |
| BR3 | A change inside major version 1 is additive; a removed, renamed or retyped property and a narrowed required set are a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR4 | The document declares only tables of `rwb_document` and only operations owned by `rwb-document`; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-01 |
| BR5 | The class of a type is answered only from the rule version in force on the business date, and a class not in force is refused, never invented | NFR-028; FSD P5 AC-EXC-P5-017-02; DL26 |
| BR6 | The scan answer is CLEAN or INFECTED and nothing else; an unavailable engine is a refusal and never a safe answer | REQ-DCM-010; FEAT-DCM-18; legacy section 5 X2 |
| BR7 | No business value is fixed in the contract: the class codes, the periods, the age bases, the end actions, the rule version, the run month, the scan timeout and the decision code stay data rows, parameters or properties | Template and Rules §R7.2 s17; RWB-E1-041 section 17 |
| BR8 | No personal data in a schema, an example or a fake: identifiers, codes, versions, dates and counts only, and no customer name, national identifier, document name or custody holder | PDPA minimisation; RWB-E1-041 section 17 |
| BR9 | The interaction ledger is `rwb-source-data`'s: the contract declares no ledger row, no ledger read and no ledger table, and the audit entry of a blocked file stays an audit entry | DP-18; default ruling of R-PREC |
| BR10 | Every consumed row states one hop, a 2 s timeout, a GET retry once with jitter and a breaker per downstream, and a failed read maps to MSG-GEN-006 naming the system that failed | DP-11, ADR-020; Architecture v5 slide 11 |
| BR11 | A POST requires `Idempotency-Key` and stores its answer, and its natural key makes the second answer the same as the first; a GET declares none | Architecture v5 slide 11 |
| BR12 | This key publishes one event, `rwb.document.RetentionApplied.v1`, and declares no scan event: the scan result is an attribute of the document and of the intake item | TSD P5 T5.3; WP B-P5-01; ASM-1777 |

### 9. State transitions

| Baseline state | Event | Condition | Next state |
|---|---|---|---|
| Draft | Review opened | The eight operations, the five resources and the two consumed rows are described | In review |
| In review | Consumer sign-off | RWB-P5-E1041-APP, RWB-P5-E1026-CON, RWB-P5-E1049-APP and the wave-1 harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional label on `RetentionRule` | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, a status changes or the event payload gains a field | New major version drafted |
| Baselined | Drift in a fake, or a retired element returns | A contract test fails | In review |

This baseline declares no document state machine and no case state machine. The four values it does fix as answers, not as transitions:

| Field value in the baseline | Meaning declared by this document |
|---|---|
| `scanResult` = "CLEAN" | The file may be stored; the value is written by the scan activity, never by a caller |
| `scanResult` = "INFECTED" | The file is in quarantine and no document row exists; a caller never overrides it |
| `status` = "APPROVED" | The rows of a load are the rule version in force from their `validFrom`; the earlier rows stay readable |
| `action` = "LISTED" | The run listed a due document for a recorded decision and changed nothing else |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of `rwb-document` | Owns the OpenAPI document, the AsyncAPI fragment and the six fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the naming of the new retention event and the correction of the plan's Contract dependencies list for the two P3 reads |
| Consuming teams (RWB-P5-E1041-APP, RWB-P5-E1026-CON, RWB-P5-E1049-APP, the SCR-44 and SCR-47 route, the wave-1 harness) | Review and sign off the parts they consume |
| RW-COMPLY, Compliance and PDPA officer | Confirms that the class, the period and the end action answer is the retention authority the legacy story gives the role, and that the load needs the second right |
| RW-REFADM, reference data administrator | Confirms the load template of table RETENTION_CLASS and the row checks that refuse a load in full |
| P3 owner (`rwb-case`) | Confirms the case, the hold and the reference-list rows: the owner of `recovery_case`, `lov_value` and `reference_row` |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the `Idempotency-Key` rule and the naming rule this document reuses |
| Data steward | Confirms that no personal value is declared in an answer, an example or a fake |

The per-service login behind the document's security scheme is not part of this baseline: the document names the scheme "the rwb-document login (DP-02)" and the name is Not specified in the source documents (GAP-0996; ASM-1776). The declared area and right of each operation are enforced at gateway-bff (DP-19); no `rwb-access` contract is declared here.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | BR Field ID | Content |
|---|---|---|
| RetentionRule | Not specified in the source documents (DOR-RWB-P5-E1041-CON-7) | classCode, docTypeCode, productCode, tableName, retentionMonths, ageBasisField, endAction, ruleVersion, validFrom, validTo, approvedByRole; from `retention_rule` DF-REF-116 to DF-REF-127 and `document_type` DF-REF-223 |
| RetentionRulePage | Not specified in the source documents (DOR-RWB-P5-E1041-CON-7) | The page items as `RetentionRule` with page, size and total; the page field names are the platform convention, and the legacy source fixes none (GAP-0996; ASM-1776) |
| RetentionLoad | Not specified in the source documents (DOR-RWB-P5-E1041-CON-7) | loadId, table, ruleVersion, validFrom, rowCount, acceptedCount, refusedCount, refusedRows (row, error), status (LOADED, APPROVED, REFUSED) |
| RetentionAction | Not specified in the source documents (DOR-RWB-P5-E1041-CON-7) | documentId, runMonth, action, retentionClass, ruleVersion, decisionLogId, decidedAt; from `retention_action` DF-DOC-091 to DF-DOC-095 and the standard columns |
| RetentionClassPage | Not specified in the source documents (GAP-1026) | Not specified in the source documents (GAP-1026) |
| RetentionActionPage | Not specified in the source documents (GAP-1026) | Not specified in the source documents (GAP-1026) |
| RetentionLoadResult | Not specified in the source documents (GAP-1026) | Not specified in the source documents (GAP-1026) |
| RetentionRun | Not specified in the source documents (GAP-1026) | Not specified in the source documents (GAP-1026) |
| RetentionRunPage | Not specified in the source documents (GAP-1026) | Not specified in the source documents (GAP-1026) |
| ScanRequest | Not specified in the source documents (DOR-RWB-P5-E1041-CON-7) | storageRef (required), sha256 (required), intakeId (optional), source (optional); no file name, no file byte |
| ScanResult | Not specified in the source documents (DOR-RWB-P5-E1041-CON-7) | scanResult (CLEAN or INFECTED, required), scannedAt, threatFound, quarantineRef |
| ScanOperation | Not specified in the source documents (GAP-1034) | Not specified in the source documents (GAP-1034) |
| ScanStatus | Not specified in the source documents (DOR-RWB-P5-E1041-CON-7) | documentId or intakeItemId, scanResult, scannedAt, threatFound, quarantineRef; from `document_intake` DF-DOC-058 and DF-DOC-059 and the two scan columns of `document` |
| RetentionApplied | Not specified in the source documents (DOR-RWB-P5-E1041-CON-7) | documentId, caseId, runMonth, action, retentionClass, ruleVersion, expiredAt, decisionLogRef; the CloudEvents envelope carries the rest |
| DecisionRecord | Not specified in the source documents (DOR-RWB-P5-E1041-CON-7) | decisionCode, finalCall, inputsRef, decidedAt and the chain fields of the library; decision code DOCRET, final call ARCHIVED, LISTED, HELD or EXCEPTION |
| Error envelope | Not specified in the source documents (DOR-RWB-P5-E1041-CON-7) | RFC 9457 problem details with `messageId`, `detail`, `instance` and the status of section 14 |
| List values | Not specified in the source documents (DOR-RWB-P5-E1041-CON-7) | LOV-RETENTION, LOV-SCAN-RESULT (CLEAN, INFECTED), LOV-RETENTION-ACTION (ARCHIVED, LISTED, HELD, EXCEPTION) and LOV-RETENTION-END (ARCHIVE, REVIEW), read through the `rwb-case` reference-data contract and never copied |

Every example in the document is synthetic and uses the legacy values: class "LEGAL10Y" at 120 months with end action "REVIEW", class "GENERAL05Y" at 60 months with end action "ARCHIVE", rule version "RET-2026.11", run month "2026-12", the stored date 1 November 2021, the expiry date 1 November 2026, the run date 2026-12-06 and the decision code "DOCRET". No example carries a real customer value and none carries a document name. The set of LOV-RETENTION values is not enumerated in the source documents; the two class codes above are the ones the legacy criteria use, and the periods are the legacy fixtures under DL26 (GAP-0996; ASM-1778). Open decisions DL10 (ASM-2250, ASM-2357, ASM-2377, ASM-2863) and DL26 (ASM-0247, ASM-0264, ASM-0275, ASM-0355) remain open; each assumption is Not specified in the source documents (DOR-RWB-P5-E1041-CON-18).

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-document` (P5); base `/api/recovery/document/v1`.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/retention-rules` | Query ruleVersion, docTypeCode, productCode, page, size; answer `RetentionRulePage` | Documents R | Not applicable |
| GET | `/retention-rules/{classCode}` | Answer `RetentionRule` in the rule version in force; 404 when the class is not in force | Documents R | Not applicable |
| POST | `/admin/retention-loads` | multipart file and `validFrom`, table RETENTION_CLASS; 201 `RetentionLoad` | Reference data C | `Idempotency-Key` header, keyed by table and ruleVersion |
| POST | `/admin/retention-loads/{loadId}/approve` | 200 `RetentionLoad` with status APPROVED; 409 when already approved or in force | Reference data A | `Idempotency-Key` header, keyed by loadId |
| GET | `/admin/retention-loads/{loadId}` | Answer `RetentionLoad` with the accepted and refused rows and their reasons | Reference data R | Not applicable |
| POST | `/scans` | Request `ScanRequest`; answer `ScanResult` with CLEAN or INFECTED; 503 when the engine does not answer | Documents C, service identity for the intake and the upload | `Idempotency-Key` header, keyed by storageRef and sha256 |
| GET | `/documents/{documentId}/scan-status` | Answer `ScanStatus` of a stored document | Documents R | Not applicable |
| GET | `/intake-items/{intakeItemId}/scan-status` | Answer `ScanStatus` of an intake item | Documents R | Not applicable |

The eight paths and their field names are this baseline's design: no source names them (GAP-0996; ASM-1776). The class panel reads of SCR-31 and SCR-32 are declared by RWB-P5-AD021-CON on the same base as a projection of the same `retention_rule` rows, so exactly one baseline owns each path; the run resource, its read and the rerun are RWB-P5-E1017-APP's and are named nowhere here. Error statuses are those of section 14.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 `rwb-case` | The case and `legal_hold` (DF-CAS-020), faked (RWB-P3-E1018-CON); the plan lists no C row for it (ASM-1776) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 `rwb-case` | LOV-RETENTION, LOV-SCAN-RESULT, LOV-RETENTION-ACTION and LOV-RETENTION-END at the version in force, faked (RWB-P3-E1043-CON) |

Every row is one hop with a 2 s timeout, a GET retry once with jitter and a breaker per downstream (DP-11, ADR-020). A failed read maps to 503 with MSG-GEN-006 naming the system that failed and never to an accepted class or a safe scan answer. No P1 ledger operation is consumed: the ledger is `rwb-source-data`'s and this contract declares no ledger row (DP-18).

#### 12.3 Events published

| Event | Topic | Owner | Declared schema |
|---|---|---|---|
| `rwb.document.RetentionApplied.v1` | `rwb.document.events.v1` | P5 `rwb-document` | Key caseId; payload documentId, caseId, runMonth, action, retentionClass, ruleVersion, expiredAt, decisionLogRef; CloudEvents 1.0 binary mode; no personal data, no document name, no file byte |
| decision record | `rwb.decision-record.v1` | PLT library, consumed by P7 | The hash-chained record with decision code DOCRET and final call ARCHIVED, LISTED, HELD or EXCEPTION, with `inputsRef` naming the class row and the run |

This baseline declares the event schema and the record declaration because the service owns the topic; the row itself is written by the run of RWB-P5-E1041-APP in its own transaction, and this key publishes nothing at run time. The event is new: the service catalogue names `rwb.document.DocumentStored.v1` and `rwb.document.DocumentFieldsExtracted.v1` only, and this baseline adds the third event of the service and records it in the Kafka Topic and Event Catalog (GAP-0996; ASM-1777). No scan event is declared: the scan result is an attribute of the document and of the intake item, and the `MALWARE_BLOCKED` audit entry is an audit-log entry.

#### 12.4 Events consumed

None. The retention and scan paths subscribe to no topic: the hold and the four lists are synchronous reads and the trigger is the Schedule or the HTTP request. A hold placed a minute ago is visible on the next run.

#### 12.5 Workflows and activities

| Name | Kind | Queue | Contracted use |
|---|---|---|---|
| `RetentionWorkflow` | Workflow contract, from the L3 workflow kit template "Scheduled job" | `rwb-document` | One typed workflow with the run month in and the run counts out, started by the `retention-monthly` Schedule; owned by RWB-P5-E1041-APP |
| `scanIntakeItem` | Activity contract | `rwb-document` | One typed activity with the intake item ID in and `ScanStatus` out, idempotent by the item and its scan result; contributed to `DocumentIntakeWorkflow` of RWB-P5-E1049-APP |

This baseline declares the two contracts and the queue, not their implementation: the workflow body, the six activities of the run and the retry values are RWB-P5-E1041-APP's, and the intake workflow is RWB-P5-E1049-APP's.

#### 12.6 Schedules

| Schedule | Job | Owner | Contracted use |
|---|---|---|---|
| `retention-monthly` | JOB-17 Retention | RWB-P5-E1041-APP | Temporal Schedule on queue `rwb-document`, monthly on the first Sunday at 02:30 Asia/Bangkok, with the run month as its input; the baseline fixes the Schedule name, the queue and the input, not the cron of an environment |
| document intake, every 15 minutes in business hours | JOB-12 Document intake | RWB-P5-E1049-APP | Named because the scan answer exists only after this Schedule runs; this baseline creates no Schedule for it |

No Quartz row and no shared job table survives either Schedule (DP-10); both are Schedules of the workflow kit, and this baseline registers neither.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `retention_rule` | P5 (`rwb_document`) | The class rows behind `RetentionRule` and the class load: record class, period, age basis, end action, rule version, validity, approver |
| `retention_action` | P5 (`rwb_document`) | The action of a month behind `RetentionAction`, with the decision-record reference |
| `document` | P5 (`rwb_document`) | The class, the stored date and the two scan attributes the `ScanStatus` read answers |
| `document_intake` | P5 (`rwb_document`) | `scan_result` (DF-DOC-058) and `scanned_at` (DF-DOC-059) behind `ScanStatus` |
| `document_type` | P5 (`rwb_document`) | The class of a type, read to resolve the rule of a document |
| decision-record library table | PLT library, created in `rwb_document` | The DOCRET record the run writes |
| outbox and idempotency library tables | PLT library, created in `rwb_document` | The RetentionApplied row and the idempotency rows of the three POSTs |

`recovery_case`, `lov_value` and `reference_row` are P3's, `decision_log_entry` is P7's and `interaction` is P1's; they are named only as consumed answers and never declared as this service's tables (DP-01, DP-18). No ACE view is read.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| retention contract stub | `GET /retention-rules` in rule version "RET-2026.11" with class "LEGAL10Y" at 120 months and end action REVIEW and class "GENERAL05Y" at 60 months and end action ARCHIVE; a class not in force answering 404; an empty page for an unknown type | App story, contract tests |
| class load fake | A load of table RETENTION_CLASS that is accepted and approved; a load refused whole with two refused rows, one at a period of 0 months and one with end action DELETE; a repeated version answering 409 | App story, contract tests, the reference-data administrator's test |
| scan fake | CLEAN on a synthetic file; INFECTED with a `quarantineRef` on the EICAR signature; no answer beyond the declared budget (503, MSG-P5-022); a repeated key answering the first result | App story, upload story, intake story, contract tests |
| scan-status fake | A stored document with CLEAN and its time; an intake item with INFECTED and its quarantine reference; the two fields absent, answering 404 | App story, screens, contract tests |
| rwb-case case WireMock | `GET /cases/{caseId}` for case "RW-2026-000123" with `legal_hold` false and case "RW-2026-000789" with `legal_hold` true; a delayed answer beyond 2 s | App story, contract tests |
| rwb-case reference-data WireMock | The four lists with the values of section 11; a delayed answer beyond 2 s | App story, contract tests |
| decision-record and central ledger fake | The local DOCRET record with one of the four final calls and a ledger reference; a refusing write | App story, contract tests |

A drifted fake fails the drift test of AC8. The exact response field names of the page metadata of `RetentionRulePage` and of the refused rows of `RetentionLoad` beyond what section 11 names are Not specified in the source documents (GAP-0996; ASM-1776).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 8 provided, 2 consumed | The two rule reads, the three class-load operations, the scan request and the two scan-status reads; the case read and the list read of P3; one hop and 2 s on every consumed call, and the declared 30 s budget of the scan |
| Kafka | 1 event schema and 1 record declared, 0 consumed | `rwb.document.RetentionApplied.v1` on `rwb.document.events.v1` and the record on `rwb.decision-record.v1`; no scan event |
| Temporal | 1 workflow contract, 1 activity contract, 1 Schedule named | `RetentionWorkflow` and `scanIntakeItem` on queue `rwb-document`, and the `retention-monthly` Schedule |
| File | 1 reference | `storageRef` points at the blob the store owns; the review-list file of the run is a File call of the app story; this baseline carries no byte and no body |

### 13. Solution plan

**Deliverables.** The OpenAPI 3.1 document `openapi/rwb-document-retention-v1.yaml` with the eight operations and the five resources; the AsyncAPI 3.0 fragment for `rwb.document.RetentionApplied.v1` and the record declaration; the contract README rows for the class-in-force rule, the load checks, the scan budget, the idempotency keys and the event count; and the seven WireMock mapping sets of section 12.8.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H, C, I and X lists of the metadata table are empty: this baseline adds no build dependency of its own (it is Day 1 by rule), and the platform and service contracts it names are the ones the app story declares. DP-01 appears because the contract names only `rwb_document` tables and consumes the case and the lists through their owners; DP-03 because the DOCRET record is a declared part of the retention answer; DP-07 because the four lists are the reference data of the class and the scan values; DP-10 because the retention Schedule and the scan activity are the Temporal surface the contract declares; DP-11 because both consumed rows are one hop with a fake; DP-13 because the base is the service's own; DP-15 because the migration position is recorded here for the app story; DP-18 because the ledger is P1's and no ledger row is declared; DP-19 because the two screen reads reach SCR-44 and SCR-47 through the composite route.

**Build steps**

1. Write the eight operations with their paths, parameters, resources and error responses; validate the document in the pipeline.
2. Fix the required and optional sets of AC2 to AC5 as schema constraints and README rows, with the class-in-force rule as a written rule.
3. Declare the class load with its multipart request, the row checks, the whole-load refusal and the two rights of AC4.
4. Declare the scan resource with the synchronous answer, the declared budget and the 503 of an unavailable engine, and the two scan-status reads of AC3.
5. Map every status and message ID of AC6 and record the RFC 9457 envelope.
6. Declare the `RetentionApplied` schema and the record of AC5, with the no-personal-data test and the absence test for a scan event.
7. Record the `Idempotency-Key` rule and the three natural keys of AC7.
8. Publish the seven fakes and the eight contract tests, including the drift test; tag the baseline and collect the consumer sign-off of the upload and intake stories, RWB-P5-E1041-APP, RWB-P5-E1049-APP and the wave-1 harness.

**Done when.** The OpenAPI artefact and the AsyncAPI fragment validate in the pipeline, the eight contract tests pass, the seven fakes answer every operation of 12.1 and both consumed rows of 12.2, the drift test is green, and RWB-P5-E1041-APP and the upload and intake stories have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-016 | Malware found | This file was not stored because the malware scan found a threat. It is held in quarantine. |
| MSG-P3-027 | Retention class load fails a check | The {table} load was refused: {error} at row {row}. The version in force is unchanged. |
| MSG-P5-022 | The scanning service is unavailable | The malware scan is not available, so the file was not stored. Try again in a few minutes. |
| MSG-P7-003 | Decision record write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field is empty, or a body fails its schema | Enter {field}. |
| MSG-GEN-004 | A concurrent request for the same load or the same scan | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-006 | A consumed P3 read does not answer, or the breaker is open | {system} is not available. Try again in a few minutes. |

The message IDs and the wording are contract elements copied unchanged from RWB-E1-041 section 14; MSG-GEN-001, MSG-GEN-004 and MSG-GEN-006 are the platform messages the envelope adds, and their text is the platform baseline text. Thai text for each follows decision DL10.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The status mapping is fixed by AC6: 401 unauthenticated, 403 with MSG-P4-002, 404 for a document, an intake item, a class or a load that does not exist, 409 with MSG-P3-027 or MSG-GEN-004, 422 with MSG-P5-016, MSG-P3-027 or MSG-GEN-001, and 503 with MSG-P5-022, MSG-P7-003 or MSG-GEN-006. A refusal returns no partial page, no partial load and no partial scan result. For MSG-P3-027 the {table} value is RETENTION_CLASS. For MSG-GEN-006 the {system} value is fixed by the consumed row that failed.

### 15. Screens and states

SCR-44 Interface and job monitor and SCR-47 Personal data are the two screens the legacy story names, and the states they render are the scan and run states of `RWB-P5-E1041-APP`. SCR-44 empty, loading, error and no access states are Not specified in the source documents (CG-ALL-5901); SCR-47 empty, error and no access states are Not specified in the source documents (CG-ALL-5902). The contract serves them through the gateway-bff composite route of DP-19 (`RWB-PLT-N001-CON`), which calls this service once for the scan status, the rule of a class and the last action of a document and merges the answers into the screen model. This baseline fixes the answer shapes only: the screen field list, the route specification, the merge order and the read-only projection belong to `RWB-PLT-N001-CON`.

The three answers the screens depend on are fixed here: `ScanStatus` with `scanResult` CLEAN or INFECTED and `scannedAt`, `RetentionRule` with the period and the end action in the version in force, and `RetentionAction` with the action of the month. A screen that shows an unscanned item as safe is a drift of the answer, and the drift test of AC8 fails it.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-041-12 | AC1, AC4, AC5, BR7 | NFR | Decision record write forced to fail during an archive; the answer carries no archived state and MSG-P7-003 (the legacy Resilience case, answered against the artefact) |
| TC-E1-041-11 | AC1, AC6, BR4 | Component | Caller with Reference data R only calls the load and the approve; refused with MSG-P4-002 (the legacy Access case) |
| TC-E1-041-01 | AC3, BR6 | End to end | EICAR test file through `POST /scans`; an INFECTED answer with a quarantine reference and no stored document |
| TC-E1-041-02 | AC2, AC5, BR5 | End to end | Class "LEGAL10Y" and type "DEMAND_LETTER" in rule version "RET-2026.11" |
| TC-E1-041-03 | AC2, AC5, BR5 | End to end | Appraisal report stored 1 November 2021, run 6 December 2026; action ARCHIVED with its DOCRET reference |
| TC-E1-041-04 | AC2, AC5, BR5 | End to end | Court notice stored 1 November 2016; action LISTED with its DOCRET reference |
| TC-E1-041-05 | AC2, AC5, BR10 | End to end | Case RW-2026-000789 with legal_hold true; action HELD and the case read from the fake |
| TC-E1-041-06 | AC3, AC6, BR6 | End to end | Scan fake with no answer; 503 with MSG-P5-022 and no CLEAN answer |
| TC-E1-041-07 | AC2, AC5, BR5 | End to end | Class OLD03Y not in version RET-2026.11; action EXCEPTION and a 404 on the class read |
| TC-E1-041-08 | AC7, AC8 | End to end | The same scan key and the same load key twice on 7 December 2026 |
| TC-E1-041-09 | AC4, AC6 | End to end | Load with period 0 and end action DELETE; refused whole with MSG-P3-027 naming both rows |
| TC-E1-041-10 | AC2, AC7, BR5 | End to end | Appraisal report stored 6 December 2021; the expiry equals the run date and the rule answers it |
| TC-E1-041-13 | AC8 | Component | The six fakes of 12.8 run against the document; the drift test compares each fake with the document and the absence test fails a build that declares a scan event or a second retention event |
| TC-E1-041-14 | AC1, AC5 | Component | Contract test of the eight operations of 12.1 and the RetentionApplied event of 12.9 against rwb-document-retention-v1.yaml and the AsyncAPI fragment |
| TC-E1-041-15 | AC1, AC8 | Component | Boundary test of the tables of 12.7: each table is owned by P5 or named as consumed only, and no ACE view is read |
| TC-E1-041-16 | AC9, BR1, BR2, BR3, BR8, BR9, BR11, BR12 | Component | Not specified in the source documents (NEWAC-RWB-P5-E1041-CON-AC11) |

The twelve legacy test cases of RWB-E1-041 are listed in the order of the WP and the legacy story; each is answered here at contract level against the artefact and the fakes, and its business outcome is proved by `RWB-P5-E1041-APP`. The legacy level System maps to End to end, Access to Component and Resilience to NFR. No integration harness story exists for this key, so no test case is copied with the `-ITG` suffix. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the class codes, the periods, the age bases, the end actions, the rule version, the run month and the scan timeout stay data rows, fixtures or properties of the app story.
- No personal data in a schema, an example or a fake: identifiers, codes, versions, dates and counts only; no customer name, national identifier, document name and no custody holder.
- No file byte, no file body and no document content in any payload, example or fake; `storageRef` and `sha256` are the only file identifiers declared.
- No ledger row, no ledger read and no ledger table (DP-18): the interaction ledger is `rwb-source-data`'s.
- No decision-log row: the contract answers a `decisionLogRef` or a `decisionLogId` reference and never a decision-log row.
- The contract names only `rwb_document` tables and only operations owned by `rwb-document`; the two P3 reads are consumed and faked, never declared as provided (DP-01).
- One REST base and one topic per service; a document that names another service's base or topic as its own fails the review (DP-13).
- One event is added by this baseline and no scan event exists; the absence test of AC8 fails a build that declares one.
- The scanning engine, its provider and its capacity are named nowhere in the contract.
- Every example is synthetic and the legacy values are examples only; no production payload is copied into a schema or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DCM-010 | Every document carries a retention class; intake runs a virus scan before storage | The `RetentionRule` shape and the class-in-force rule, the class load of 12.1, the `ScanRequest`, `ScanResult` and `ScanStatus` shapes and MSG-P5-016 with MSG-P5-022 | TC-E1-041-01, TC-E1-041-02, TC-E1-041-06, TC-E1-041-09, TC-E1-041-10, TC-E1-041-13, TC-E1-041-14, TC-E1-041-15 |
| REQ-DCM-016 | A legal hold stops deletion and expiry while it is in place, overriding the class | The case row of 12.2, its fake and the `action` value HELD of `RetentionAction` | TC-E1-041-05 |
| REQ-DCM-019 | Records retention runs by class, and a disposal or an extension is a recorded decision, never silent | `RetentionAction`, the four action values, the DOCRET reference and the `RetentionApplied` schema | TC-E1-041-03, TC-E1-041-04, TC-E1-041-12 |

The legacy story RWB-E1-041 carries the three requirement IDs above; NFR-028 (a class per type, periods not set), NFR-029, NFR-072 and NFR-074 are the non-functional statements behind the same shapes.

| Decision or pattern | Where it sits in this story |
|---|---|
| DP-01 | Only `rwb_document` tables declared; the case and the lists consumed and faked |
| DP-03 | The DOCRET record declaration of 12.3 and the decision-record fake |
| DP-07 | The reference-list row of 12.2, the four lists and their fake |
| DP-10 | The `RetentionWorkflow`, the `scanIntakeItem` contract and the `retention-monthly` Schedule |
| DP-11 | Both consumed rows with one hop, a 2 s timeout and a fake |
| DP-13 | Base `/api/recovery/document/v1` on all eight operations |
| DP-15 | The migration position recorded for `retention_rule` and `retention_action` |
| DP-18 | No ledger table, no ledger row and no ledger operation |
| DP-19 | SCR-44 and SCR-47 behind gateway-bff |
| ADR-013 | The service owns its schema inside ACE PostgreSQL |
| ADR-014 | The `rwb_document` schema and the rwb-document login (name not specified) |
| ADR-020 | Contract-first REST, one hop, 2 s timeout |

The legacy key is RWB-E1-041; its AC1 to AC10 are owned by `RWB-P5-E1041-APP`, and the cross-service proof of the same values is the wave-1 harness of RWB-E1-049 plus the contract tests of this baseline.

### 19. Out of scope

- The build of the class load, the rule reads, the scan client, the run and the review list: `RWB-P5-E1041-APP`.
- The document store, its containers and the storage product: `RWB-P5-E1024-APP`.
- The upload dialog and its refusal surface: `RWB-P5-E1026-APP` and `RWB-P5-E1026-CON`.
- The intake record, the 15-minute Schedule and the OCR, classification and extraction steps: `RWB-P5-E1049-APP` and the stories after it.
- The run resource, its read and its rerun as a REST operation: `RWB-P5-E1017-APP`; the class panel reads of SCR-31 and SCR-32: `RWB-P5-AD021-CON` and `RWB-P5-AD021-APP`.
- Placing or lifting a legal hold: `rwb-case`.
- The scanning engine, its provider, its licences and its own operations: only the answer and the quarantine reference are declared here.
- The gateway-bff composite route, the screen field list and the merge order of SCR-44 and SCR-47: `RWB-PLT-N001-CON`.
- The Helm chart, the retry policy values, the topic and DLT provisioning, the metrics, the alerts and the runbook.
