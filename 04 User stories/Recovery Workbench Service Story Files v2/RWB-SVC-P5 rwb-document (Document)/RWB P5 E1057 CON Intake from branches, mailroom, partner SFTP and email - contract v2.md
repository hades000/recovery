# RWB-P5-E1057-CON Intake from branches, mailroom, partner SFTP and email

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1057-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-057 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Size | Not sized in this story; the squad sizes it at refinement (DOR-RWB-P5-E1057-CON-16) |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | v1 on base `/api/recovery/document/v1` |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-020, FR-P5-022, FR-P5-023) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the contract baseline of the channel-intake API of `rwb-document` is split out of legacy RWB-E1-057 and published on base `/api/recovery/document/v1` with the three admin operations, the two run shapes, the channel and result enumerations, the error envelope, the event position, the fakes and the drift test. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P5-E1057-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (14 resolved, 15 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the channel-intake API of `rwb-document` — the run list, the run read and the rerun operation on base `/api/recovery/document/v1` with the `IntakeRun` and `IntakeRunPage` shapes, the channel code rule, the source, scan-result and OCR-status enumerations, the run states and the refusal reason codes, the error envelope with every message ID of section 14 and its HTTP status, the `Idempotency-Key` rule, the event position of the path and the fakes with their drift test**, so that **the app story of this legacy key, the operator screen of Epic 2, the partner slice of the same key and the wave 1 integration harness build against a fixed, testable contract on Day 1, and a renamed count, a channel code that the run record cannot carry or a rerun answered with the wrong status can never drift between two builds without a failing test**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). Legacy RWB-E1-057 carries its one endpoint in a section 12 of prose, with an in-process `PartnerDirectory` and a `JobRecord` row beside it, and it leaves the consumer to infer the exact shapes of a run. Under the target architecture the parts most likely to drift silently are exactly the ones this baseline fixes:

- a count renamed in `IntakeRun` or `IntakeRunPage`, so the operator reads a channel column that carries nothing;
- a channel code widened to a free string, so a branch, a mailroom, a partner code and a mailbox code become indistinguishable in the run record and the per-channel alert of MSG-P5-008 names nothing;
- a result or a refusal reason outside the declared set, so a refused file is counted as taken in and the duplicate rule of R-UNI-40 stops being visible;
- a rerun answered 200 where the legacy contract answers a job, or a rerun of a run still in progress answered without MSG-GEN-004;
- an event invented for the path, so a consumer subscribes to a name the catalogue never publishes;
- an `Idempotency-Key` that is not the channel-code, source-reference and hash rule, so a repeat run takes the same file in twice.

The baseline fixes the names the checks require: schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with its retry and `.dlt` topics, task queue `rwb-document` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.document`. It makes the C dependencies of the app story explicit — the P3 parameters contract `RWB-P3-E1042-CON` and the P3 reference-data contract `RWB-P3-E1043-CON` — and it records that the partner-by-code read of `rwb-partner` is consumed and faked although the plan lists it in no C row (ASM-1839).

It also records the boundary the sibling baselines already occupy. `POST /api/recovery/document/v1/intake-items` and the intake item read are declared by RWB-P5-E1049-CON, the review list and the resolve operation by RWB-P5-E1032-CON, and the content read by both; this baseline therefore declares the three operations of the run record and the rerun and nothing else, so no operation is declared twice for `rwb-document` (ASM-1838). Nothing else is guessed: the names this key does not settle carry the placeholder `Not specified in the source documents (GAP-1013; ASM-1837)`.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the operation, topic, event and queue names follow the platform rule rather than a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope, the `Idempotency-Key` rule and the retry and `.dlt` topic convention are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); where this document narrows them it does so explicitly.
- TSD P5 appendix T-A.1 and T-A.2 are in force for the intake operations API-P5-010 to API-P5-013, and TSD P5 T3.1 and T3.2 are in force for the `document_intake` field definitions and the three lists LOV-DOC-SOURCE, LOV-SCAN-RESULT and LOV-OCR-STATUS.
- The Ownership Map is the only source of owners: `document_intake`, `document_hub_parameter` and `document` are P5's in `rwb_document`; `partner` is S9's in `rwb_partner`; `parameter_catalog`, `reference_row` and `lov_value` are P3's; the ACE views are P1's.
- The sibling baselines are published: RWB-P5-E1049-CON for the intake item submit and read, RWB-P5-E1032-CON for the review list and the resolve, and RWB-P5-E1041-CON for the scan result and the quarantine rule; none of their operations is re-declared here.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7), so its four H, C, I and X columns are empty and every dependant builds against the published baseline and its fakes.
- The release date 30 November 2026 is the legacy one and is tentative (ASM-1826), and the story carries Status Draft (realignment v1) because no approval of the realigned story is recorded (ASM-1836).

### 4. Flow

1. Draft the OpenAPI 3.1 document of `rwb-document` with the three admin operations, the two run resources of section 11 and the error responses of section 14, on the single base `/api/recovery/document/v1`.
2. Fix the run list and the run read: the paging default, the newest-first order, the per-channel counts and the per-result counts of one 15-minute window.
3. Fix the `IntakeRun`, `IntakeRunPage` and `IntakeRunChannel` shapes, so the operator reads one answer with the run, its channels and its reason counts, and the page carries its own paging fields.
4. Fix the channel code rule: a channel code is the branch code of a scanner folder, the literal MAILROOM, the partner code of an SFTP subfolder or the mailbox code, and it is a 40-character uppercase token rather than a free string.
5. Fix the enumerations: the three values of LOV-DOC-SOURCE on the run rows, the two values of LOV-SCAN-RESULT, the four values of LOV-OCR-STATUS, the three run states and the four result and refusal classes.
6. Map every failure to the error envelope and a message ID, status by status, and carry the missing names and the missing C row as a gap and an assumption.
7. Record the `Idempotency-Key` rule of the rerun operation and the channel-code, source-reference and hash key of a pickup, and declare that the two are different keys for different operations.
8. Declare the event position: this path publishes nothing, `DocumentStored` and `DocumentFieldsExtracted` are the catalogue's two events of the service, and a third name fails the absence test.
9. Publish the six fakes, the drift test and the baseline tag, then hand the baseline to RWB-P5-E1057-APP, RWB-S9-E1057-APP and the wave 1 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | MSG-GEN-001 | AC1 |
| X2 | A count, a channel row or a page field is renamed, removed or retyped within major version 1 | The contract test fails; the change needs a corrected document or a new major version | None | AC2 |
| X3 | A channel code is declared as a free string, or a run row carries a code the rule cannot produce | The contract test fails on the pattern and on the enum of the code | None | AC3 |
| X4 | A value outside LOV-DOC-SOURCE, LOV-SCAN-RESULT or LOV-OCR-STATUS appears on a run row, or an unknown run state is answered | The contract test fails on the enum | None | AC3, AC4 |
| X5 | A refusal is answered without its message ID, or a message ID with the wrong status | The contract test fails on the error envelope and on the status mapping of section 14 | MSG-GEN-004 | AC5 |
| X6 | A repeat of the same `Idempotency-Key` starts a second run, or a rerun of a live run is accepted | The contract test fails: one 202 and one 409 with MSG-GEN-004 | MSG-GEN-004 | AC5 |
| X7 | An event is declared for the pickup, or a fourth event name appears for the service | The absence test fails the build | None | AC6 |
| X8 | A fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC7, AC8 |

### 6. INVEST check

| Criterion | Verdict | Note |
|---|---|---|
| Independent | Pass | No build dependency; reads the platform envelopes, TSD P5 T-A and T3, the Ownership Map and the three sibling baselines only |
| Negotiable | Pass | The field-level names are settled with the consumers; the operations, the channel code rule, the enumerations, the status mapping, the idempotency rules and the event position are fixed by the target architecture and the legacy section 12 |
| Valuable | Pass | Unblocks RWB-P5-E1057-APP, the operator screen of Epic 2, the partner slice RWB-S9-E1057-APP and the wave 1 harness on Day 1 |
| Estimable | Pass | One document, three resources, three operations, three consumed rows, nine contract tables and six fakes |
| Small | Pass | Fits one sprint with its contract tests |
| Testable | Pass | Every criterion in section 7 is tested against the artefact, not against a business outcome |

INVEST result per criterion: independent Pass, negotiable Pass, valuable Pass, estimable Pass, small Pass and testable Pass, as the verdicts of the table above.

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the channel-intake API of rwb-document

  Background:
    Given the service naming rule of the platform library is in force
    Given the document_intake definitions of TSD P5 T3.1 and the operations API-P5-010 to API-P5-013 of TSD P5 T-A are in force
    Given the sibling baselines RWB-P5-E1049-CON, RWB-P5-E1032-CON and RWB-P5-E1041-CON are published

  Scenario: AC1 The three admin operations are declared and the document validates (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-document is published with this baseline
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /api/recovery/document/v1/admin/jobs as the intake run list and GET /api/recovery/document/v1/admin/jobs/{jobId} as the run read
    Then it declares POST /api/recovery/document/v1/admin/jobs/{jobId}/rerun as the rerun of a failed run, rebased by DP-13 from the legacy `/admin/jobs/{jobId}/rerun` of the monolith base
    Then every operation carries the Platform administration area, its right, and the statuses 200, 202, 401, 403, 404, 409 and 503 as section 14 fixes them
    Then the document states that no intake submit, intake item read, review list or resolve operation is declared here, because RWB-P5-E1049-CON and RWB-P5-E1032-CON declare them
    Then no operation of another service's base is declared as provided

  Scenario: AC2 The IntakeRun and IntakeRunPage shapes are fixed (new, D-RCV-60)
    Given the IntakeRun, IntakeRunPage and IntakeRunChannel resources declared in the document
    When they are compared with the legacy job record of section 12 and the document_intake fields of TSD P5 T3.1
    Then IntakeRun carries runId, businessDate, scheduleId, state, startedAt, endedAt, channels, takenIn, refused, duplicate and version
    Then IntakeRunChannel carries channelCode, takenIn, refused, duplicate and the reason counts as an array of reasonCode and count
    Then IntakeRunPage carries items, page, size and total and lists the runs newest first
    Then the list query declares businessDate, state, page and size with a default of 50
    Then runId and scheduleId are uuids, version is an integer and the three counts are integers and never negative
    Then the example carries run "RUN-2026-000123", business date 30 November 2026, state "complete", channel "BR-0123" with 1 taken in and channel "MAILROOM" with 0
    Then a null channel list answers an empty array and never a missing property

  Scenario: AC3 The channel code rule and the three list enumerations are fixed (new, D-RCV-60)
    Given the channel code declaration and the enumeration declarations of the document
    When they are compared with the legacy section 8 BR1 and the three lists of TSD P5 T3.2
    Then channelCode is a string of 1 to 40 characters matching the uppercase token pattern, and the document states its four producers: a branch code, the literal MAILROOM, a partner code and a mailbox code
    Then source carries the five values of LOV-DOC-SOURCE: SCAN, UPLOAD, GENERATED, PARTNER and EMAIL
    Then the run rows declare source "SCAN" for branch and mailroom files, "PARTNER" for the SFTP subfolders and "EMAIL" for mailbox attachments
    Then scanResult carries the two values of LOV-SCAN-RESULT and ocrStatus the four values of LOV-OCR-STATUS, and neither is repeated as a literal in the document
    Then the document states that no list value is fixed in code and that all three lists are read through the reference-data contract RWB-P3-E1043-CON
    Then a run row carrying a source outside the five values fails the schema and the contract test

  Scenario: AC4 The run states, the result values and the refusal reason codes are fixed (new, D-RCV-60)
    Given the state and result declarations of the document
    When they are compared with the legacy exception paths X1 to X12 and the counts of section 4
    Then state carries three values: running, failed and complete, and no fourth value
    Then the result classes are taken in, refused and duplicate, and the three counts of IntakeRunChannel are the counts of those three classes
    Then the refusal reason codes are declared as references to a message ID or to a fixed code, and they carry MSG-P5-001, MSG-P5-017, PARTNER_UNKNOWN and PARTNER_NOT_ACTIVE with no other value in this baseline
    Then a refused file with no reason code fails the schema, and a duplicate is never counted as refused
    Then the document states that the reason codes of the partner panel are produced by the partner slice RWB-S9-E1057-APP and carried as values of the same field
    Then the run state is derived from the Schedule execution and is never written by a client

  Scenario: AC5 The error envelope, every message ID with its status and the two idempotency rules are fixed (new, D-RCV-60)
    Given the error responses and the idempotency rules declared for the three operations
    When each status is compared with the legacy section 12 errors and section 14
    Then 401 answers MSG-P4-001, 403 answers MSG-P4-002, and 404 answers the not-found message whose ID is Not specified in the source documents (GAP-1013; ASM-1840)
    Then 409 answers MSG-GEN-004 for a run still in progress and 503 answers MSG-GEN-006 naming the system that failed
    Then the rerun is answered 202 with the IntakeRun of the started run and never 200 and never 201
    Then the rerun declares the Idempotency-Key header, and a repeat with the same key returns the first answer and starts no second run
    Then the document states the separate pickup key of channel code, source reference and file hash, held by the idempotency library of RWB-PLT-TE006-CON, with its exact storage window Not specified in the source documents (GAP-1013; ASM-1842)
    Then the two GET operations declare no Idempotency-Key and no side effect
    Then every error is an RFC 9457 problem response with messageId, detail and instance, and MSG-P5-001, MSG-P5-017, MSG-P5-007 and MSG-P5-008 are declared as refusal and alert texts and never as error statuses

  Scenario: AC6 The event position is declared and no event of this key is invented (new, D-RCV-60)
    Given the AsyncAPI position of this baseline and the catalogue row of the service
    When they are compared with Arch v5 slides 16 and 42 and TSD P5 T5.3
    Then the document states that the pickup publishes no event and holds no outbox row of its own
    Then it states that rwb.document.events.v1 with its retry topics at 1 min, 10 min and 1 h and its .dlt topic carries DocumentStored and DocumentFieldsExtracted, and that both are published by the store and by extraction and not by this path
    Then the service naming rule of rwb.document.<Event>.v1 is recorded, and a declared pickup event fails the absence test
    Then the document states that the only Kafka dependency of this path is the idempotency and inbox library of RWB-PLT-TE006-CON
    Then the decision-record topic rwb.decision-record.v1 is declared as not used by this path

  Scenario: AC7 The six fakes answer the document (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed and the fakes are run against the document
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the six fakes of 12.8 answer the three operations of 12.1 and the three reads of 12.2 with the values of the legacy examples, including branch "BR-0123", channel "MAILROOM", partner "LF-007", mailbox "MBX-RECOVERY-01" and the 25.0 and 25.1 MB boundary
    Then the run fake answers one run in each of the three states and one run per refusal reason code
    Then no fake carries a real customer value, a file name of a real document or a sender address in clear

  Scenario: AC8 The drift test and the absence test fail on any mismatch (new, D-RCV-60)
    Given the contract section of this story and the six fakes
    When the drift test compares each fake with the document
    Then it fails on any mismatch of a path, a status, a field name, a required flag or an enum value
    Then it fails a build that declares a fourth admin operation on this base, an intake submit declared a second time, or an event name outside rwb.document.<Event>.v1
    Then it fails a build in which a list value is typed in the document instead of named as a list
    Then it passes when the document, the six fakes and the three sibling baselines agree
```

The eight criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by RWB-P5-E1057-APP. The legacy AC1 to AC16 are owned by RWB-P5-E1057-APP (eleven) and RWB-S9-E1057-APP (five), and the wave 1 harness RWB-ITG-E1057-ITG consumes this baseline and copies none of these criteria.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/document/v1` on every declared operation | DP-01; Template and Rules §R4; Arch v5 slide 41 notes |
| BR2 | One topic per service: `rwb.document.events.v1`, with the retry and `.dlt` topics of the platform convention | DP-09; Arch v5 slides 16 and 42 |
| BR3 | A change inside major version 1 is additive; a removed, renamed or retyped property and a narrowed required set are a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR4 | The document declares only tables of `rwb_document` and only operations owned by `rwb-document`; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-01 |
| BR5 | No operation of this base is declared twice: the intake submit and the intake item read are RWB-P5-E1049-CON's and the review list and the resolve are RWB-P5-E1032-CON's | Ownership Map; the three sibling baselines |
| BR6 | No business value is fixed in the contract: the type list, the size limit, the duplicate window, the alert threshold, the channel values and the paging default are parameters, reference rows or document defaults | Template and Rules §R7.2 s17; RWB-E1-057 section 17 |
| BR7 | No personal data in a schema, an example or a fake: identifiers, channel codes, counts, states and business dates only, and no sender address, no file name and no email subject in any payload | Arch v5 slide 11; RWB-E1-057 section 17 |
| BR8 | A channel code is a token of at most 40 characters and never a path, an address or a URL; the folder and the mailbox behind it stay in the property set of the deployment | RWB-E1-057 section 8 BR8; DP-15 |
| BR9 | The pickup publishes no event and the contract invents none: the two catalogued events of the service belong to the store and to extraction | Arch v5 slide 42; ASM-1841 |
| BR10 | Every error uses one envelope and one message ID per condition; the message texts are copied unchanged from legacy RWB-E1-057 section 14 | Architecture v5 platform baseline; Template and Rules §R7.2 s14 |
| BR11 | A POST requires `Idempotency-Key` and stores its answer; a GET declares none; the rerun answers 202 and never 200 or 201 | Architecture v5 slide 11; DP-09; legacy section 12 |
| BR12 | The contract declares no channel and no run state machine beyond the values the fields may take; a transition belongs to the app story that performs it | RWB-E1-057 section 9; RWB-P5-E1057-APP owns the run and item transitions |

### 9. State transitions

| Baseline state | Event | Condition | Next state |
|---|---|---|---|
| Draft | Review opened | The three operations, the three resources, the three consumed rows and the event position are described | In review |
| In review | Consumer sign-off | RWB-P5-E1057-APP, RWB-S9-E1057-APP, the operator screen of Epic 2 and the wave 1 harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional `reasonCode` on a channel row | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a required set is narrowed | New major version drafted |
| Baselined | Drift in a fake, or a retired element returns | A contract test fails | In review |

This baseline declares no channel state machine and no run state machine of its own. The three run states are values of a field, and the transitions between them belong to RWB-P5-E1057-APP.

| Field value in the baseline | Meaning declared by this document |
|---|---|
| `state` = "running" | The Schedule has started the run and the channels are being read |
| `state` = "failed" | The run stopped on a channel; a rerun may start one run for the same window |
| `state` = "complete" | Every channel was read and the counts were written, whether or not any file was taken in |
| `source` = "SCAN" | A branch scanner folder or the mailroom folder |
| `source` = "PARTNER" | A partner SFTP subfolder named by the partner code |
| `source` = "EMAIL" | A recovery mailbox attachment |
| `scanResult` empty | The item was taken in and not yet scanned; the scan step sets the value |
| `ocrStatus` = "PENDING" | The item was taken in and not yet read; the OCR step moves it |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-document | Owns the OpenAPI document, the AsyncAPI position and the six fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version and the resolution of `GAP-1013` |
| Consuming teams (RWB-P5-E1057-APP, RWB-S9-E1057-APP, the operator screen of Epic 2, the wave 1 harness) | Review and sign off the parts they consume |
| RW-PLATADM, the platform administrator | Confirms that the run record and the rerun carry what the operator needs (Platform administration CRUD) |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the `Idempotency-Key` rule and the naming rule this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an example or a fake |

The per-service login behind the document's security scheme is not part of this baseline; the document names the scheme "the rwb-document login (DP-02)" and the name is Not specified in the source documents (GAP-1013; ASM-1837). The declared area and right are enforced at gateway-bff (DP-19); no `rwb-access` contract is declared here. The authorise check of the operations is the DP-08 check, performed at gateway-bff (DP-19); its rwb-access name is Not specified in the source documents (DOR-RWB-P5-E1057-CON-6).

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| IntakeRun | runId (uuid), businessDate, scheduleId (uuid), state (running, failed, complete), startedAt, endedAt, channels (array of IntakeRunChannel), takenIn, refused, duplicate, version, from the `document_intake` fields DF-DOC-045 to DF-DOC-063 grouped by `run_id` and `channel_code` | Not specified in the source documents (DOR-RWB-P5-E1057-CON-7) |
| IntakeRunChannel | channelCode, takenIn, refused, duplicate, reasons (array of reasonCode and count); the channel code rule of AC3 | Not specified in the source documents (DOR-RWB-P5-E1057-CON-7) |
| IntakeRunPage | items (array of IntakeRun), page, size, total; the list is newest first by businessDate and startedAt | Not specified in the source documents (DOR-RWB-P5-E1057-CON-7) |
| Run state set | running, failed, complete | Not specified in the source documents (DOR-RWB-P5-E1057-CON-7) |
| Result classes | taken in, refused, duplicate | Not specified in the source documents (DOR-RWB-P5-E1057-CON-7) |
| Refusal reason codes | MSG-P5-001 for a type not allowed, MSG-P5-017 for a size above the limit, PARTNER_UNKNOWN and PARTNER_NOT_ACTIVE for the partner panel | Not specified in the source documents (DOR-RWB-P5-E1057-CON-7) |
| Channel code | A token of 1 to 40 uppercase characters: a branch code, the literal MAILROOM, a partner code or a mailbox code | Not specified in the source documents (DOR-RWB-P5-E1057-CON-7) |
| Error envelope | RFC 9457 problem details with `messageId`, `detail`, `instance` and the status of section 14 | Not specified in the source documents (DOR-RWB-P5-E1057-CON-7) |

Every example in the document is synthetic and uses the legacy values: branch "BR-0123", branch "BR-0077", channel "MAILROOM", partner "LF-007", mailbox "MBX-RECOVERY-01", the file "scan-0001.pdf" of 1.2 MB, the 25.0 and 25.1 MB boundary and the 6 KB signature image. No example carries a real customer value, a real sender address or a real file name; the legacy values are examples only. The field-level names of `IntakeRun`, `IntakeRunChannel` and `IntakeRunPage` are Not specified in the source documents (GAP-1013; ASM-1837), and the baseline fixes them as the smallest superset of the legacy job record.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-document (P5); base `/api/recovery/document/v1`.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/admin/jobs` | 200 `IntakeRunPage`; query `businessDate`, `state`, `page`, `size` 50, newest first | Platform administration R | None |
| GET | `/admin/jobs/{jobId}` | 200 `IntakeRun` with its channels and its reason counts | Platform administration R | None |
| POST | `/admin/jobs/{jobId}/rerun` | 202 `IntakeRun` of the started run | Platform administration U | `Idempotency-Key` header |

Error statuses 401, 403, 404, 409 and 503 are those of section 14. The legacy path `POST /admin/jobs/{jobId}/rerun` is rebased by DP-13 and the names of the three operations and of the two resources are the baseline's own (GAP-1013; ASM-1837). No intake submit, intake item read, review list, resolve or content operation is declared here, because RWB-P5-E1049-CON and RWB-P5-E1032-CON declare them (ASM-1838). The run record and the three admin operations are published by this baseline; the channel property layout and the channel inventory are environment values of RWB-P5-E1057-INF and RWB-P5-E1057-OPS; the target hold container is rwb-quarantine; the partner read is consumed through the rwb-partner contract with a fake and no C row (GAP-0367; GAP-1012; GAP-1014).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/parameters/{paramCode}` | P3 rwb-case | `INTAKE_ALLOWED_TYPES`, `INTAKE_MAX_FILE_MB`, `INTAKE_DUPLICATE_WINDOW_DAYS`, `INTAKE_MIN_IMAGE_KB` and `INTAKE_ALERT_AFTER_FAILURES` (C `RWB-P3-E1042-CON`) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-DOC-SOURCE, LOV-SCAN-RESULT and LOV-OCR-STATUS (C `RWB-P3-E1043-CON`) |
| GET | the partner-by-code read of rwb-partner | S9 rwb-partner | The partner ID, code and panel status behind a PARTNER channel code; one hop, 2 s, faked; the exact path is Not specified in the source documents (GAP-1013; ASM-1839) and no C row of the plan carries it |

Every row is one hop with a 2 s timeout, a GET retry once with jitter and a breaker per downstream (DP-11, ADR-020). A failed read maps to 503 with MSG-GEN-006 naming the system that failed and never to a run answered as complete.

#### 12.3 Events published

| Event | Topic | Owner | Declared position |
|---|---|---|---|
| None | — | — | This path publishes no event and holds no outbox row of its own. `rwb.document.events.v1` with its retry topics at 1 min, 10 min and 1 h and its `.dlt` topic carries `DocumentStored` and `DocumentFieldsExtracted`, published by the store of RWB-P5-E1024-APP and by the extraction of RWB-P5-E1053-APP (ASM-1841) |

The baseline declares the service topic and the two catalogue events because the service owns the topic, and it declares no third name. The absence test of AC6 and AC8 fails a build that declares a pickup event; the event catalogue owner confirms the position before the wave 1 release.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| None | — | — | The path is started by the intake Schedule, not by an event. `DocumentStored` with source UPLOAD is consumed by the `ingest` activity of RWB-P5-E1049-APP and not by this baseline, and `rwb.decision-record.v1` is not used by this path |

#### 12.5 Workflows and activities

| Name | Kind | Queue | Contracted use |
|---|---|---|---|
| `pickup` | Activity contract | `rwb-document` | One typed activity interface with the run slot in and the run counts out, idempotent by channel code, source reference and file hash; called by `DocumentIntakeWorkflow`; no workflow is declared here |
| `DocumentIntakeWorkflow` | Workflow, from the L3 "Document intake" template | `rwb-document` | Owned by RWB-P5-E1049-APP; this baseline names only the activity it contributes and the run record the activity writes |

#### 12.6 Schedules

| Schedule | Workflow | Queue | Interval | Note |
|---|---|---|---|---|
| None | `DocumentIntakeWorkflow` | `rwb-document` | Every 15 minutes in business hours (JOB-12) | This baseline declares no Schedule and no cron entry; the Schedule is registered from the values of RWB-P5-E1057-OPS and its ID is the `scheduleId` of the run record |

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `document_intake` | P5 (`rwb_document`) | The rows behind every count of the run record: `run_id`, `channel_code`, `source`, `source_ref`, `file_sha256`, `scan_result` and `ocr_status` |
| `document_hub_parameter` | P5 (`rwb_document`) | Contracted use only: the rows behind the five parameters |
| idempotency library table | PLT library, created in `rwb_document` | The `Idempotency-Key` row of the rerun and the channel-code, source-reference and hash key of a pickup |
| outbox, inbox library tables | PLT library, created in `rwb_document` | Created by the library migration; this path writes no outbox row of its own |

`partner` is S9's in `rwb_partner`, `parameter_catalog`, `reference_row` and `lov_value` are P3's, and the ACE views are P1's and are named as consumed answers and never declared as this service's tables (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| run fake | One run in each of the running, failed and complete states with the channel rows of branch "BR-0123", channel "MAILROOM", partner "LF-007" and mailbox "MBX-RECOVERY-01" | App story, operator screen, contract tests |
| refusal fake | One run per reason code, MSG-P5-001 for a DOCX, MSG-P5-017 for 25.1 MB, PARTNER_UNKNOWN and PARTNER_NOT_ACTIVE, with the 25.0 MB row taken in | App story, partner slice, contract tests |
| parameters and reference-data WireMock | The five parameters with `INTAKE_MAX_FILE_MB` 25 and `INTAKE_DUPLICATE_WINDOW_DAYS` 30; the three lists with the five DOC-SOURCE, two SCAN-RESULT and four OCR-STATUS values | App story, contract tests |
| rwb-partner WireMock | Partner "LF-007" ACTIVE, a code that resolves to no partner, a partner SUSPENDED and a delayed answer beyond 2 s | App story, partner slice, contract tests |
| rerun fake | A 202 with the started run, a 409 with MSG-GEN-004 for a live run, a 404 with the not-found message and a 503 with MSG-GEN-006 | App story, operator screen, contract tests |
| error envelope fake | One answer per message ID of section 14 with its status and its `detail` text | Contract tests, operator screen |

A drifted fake fails the drift test of AC8. The exact response field names of the partner-by-code read are Not specified in the source documents (GAP-1013; ASM-1839).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 3 consumed | The run list, the run read and the rerun; the parameters read, the lists read and the partner-by-code read; one hop and 2 s on every consumed call |
| Kafka | 0 published, 0 consumed; 1 topic position declared | `rwb.document.events.v1` carries the two catalogue events of the service and this path publishes neither; the idempotency library of RWB-PLT-TE006-CON is the only Kafka dependency |
| Temporal | 1 activity contract, 1 workflow named | `pickup` on queue `rwb-document`, called by `DocumentIntakeWorkflow`, which is owned by RWB-P5-E1049-APP; no Schedule |
| File | 0 byte carried | The run counts are counts of files the channels handed over; no file name, no path and no container reference is part of an answer |

### 13. Solution plan

**Deliverables.** The OpenAPI 3.1 document `openapi/rwb-document-v1.yaml` with the three admin operations and the three resources; the contract README rows for the channel code rule, the enumerations, the state and result sets, the error mapping, the two idempotency rules, the event position and the operation-ownership boundary; and the six WireMock mapping sets of section 12.8.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/document/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H, C, I and X lists of the metadata table are empty: this baseline adds no build dependency of its own (it is Day 1 by rule), and the platform and service contracts it names are the ones the app story declares. DP-01 is applied because every shape derives from rows of `rwb_document` and no other schema is declared. DP-06 and DP-07 are the two C rows: the five parameters and the three lists are read through the `rwb-case` contracts and never typed into the document. DP-09 fixes the topic position, the absence of a pickup event and the idempotency rules. DP-10 names the `pickup` activity contract and the workflow that calls it, without declaring a Schedule. DP-11 fixes the three consumed rows to one hop with 2 s and a fake each, including the partner read that carries no C row. DP-13 rebases the only legacy path on the service base. DP-15 records that the table behind the counts belongs to this service's own migration sequence. DP-19 records that the run record and the rerun are reached through the gateway-bff composite route; this baseline fixes the answer shapes only and no route specification.

**Build steps**

1. Write the three operations with their paths, queries, resources and error responses; validate the document in the pipeline.
2. Fix the required and optional sets of AC2 and the paging default as schema constraints and README rows.
3. Declare the channel code pattern, the three lists and the state and result sets of AC3 and AC4, with every list value named as a list and never typed.
4. Map every status and message ID of AC5 and record the RFC 9457 envelope, the 202 rerun and the two idempotency rules, including the not-found placeholder.
5. Record the event position of AC6 and the absence test for a pickup event.
6. Publish the six fakes and the eight contract tests, including the drift test; tag the baseline and collect the consumer sign-off of RWB-P5-E1057-APP, RWB-S9-E1057-APP, the operator screen of Epic 2 and the wave 1 harness.

**Done when.** The OpenAPI artefact validates in the pipeline, the eight contract tests pass, the six fakes answer every operation and read of sections 12.1 and 12.2, the drift test is green, and RWB-P5-E1057-APP, RWB-S9-E1057-APP and RWB-ITG-E1057-ITG have accepted the baseline.

### 14. Validation and messages

| ID | When | Message | HTTP status |
|---|---|---|---|
| MSG-P5-001 | A file type is not allowed (a refusal reason code, not an error) | This file type cannot be stored. Use PDF, JPG or PNG. | 200 |
| MSG-P5-017 | A file is above the size limit (a refusal reason code) | This file is larger than {size} MB and cannot be stored. | 200 |
| MSG-P5-007 | A file is refused at intake (a refusal text) | {source} file {file} was not taken in: {reason}. It is in the {folder} folder. | 200 |
| MSG-P5-008 | Two runs in a row fail on one channel (an alert text) | Document intake failed twice in a row for {channel}. Check the interface and job monitor. | 200 |
| MSG-GEN-006 | A dependency is not available or the storage refuses the write | {system} is not available. Your request is queued and will be retried. | 503 |
| MSG-GEN-004 | The run is still in progress or the idempotency key changed the record | Someone else changed this record. Reload it to see their change. | 409 |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. | 403 |
| MSG-P4-001 | No authenticated caller | Not specified in the source documents (GAP-1013; ASM-1837) | 401 |
| not-found message | A run that does not exist | Not specified in the source documents (GAP-1013; ASM-1840) | 404 |

The message IDs and the wording are contract elements copied unchanged from RWB-E1-057 section 14; Thai text for each follows open decision DL10, which carries its recorded assumptions. MSG-P4-001 and the not-found message are named by the target error envelope and are copied from the platform set, and their exact texts are recorded as the placeholder above.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The status mapping is the legacy one plus the two platform rows: 202 for an accepted rerun, 401 with MSG-P4-001, 403 with MSG-P4-002, 404 with the not-found message, 409 with MSG-GEN-004 and 503 with MSG-GEN-006. The four refusal and alert texts of the run record are never answered as an error status.

Screen states of SCR-44 (empty, loading, error and no access) are owned by the operator screen of Epic 2. The no access state is answered with 403 and MSG-P4-002, and the error state with the statuses 503 and 409 of section 14; the empty and loading states are Not specified in the source documents (DOR-RWB-P5-E1057-CON-10).

### 15. Screens and states

SCR-44 Interface and job monitor of Epic 2 is the screen these operations serve, reached through the gateway-bff composite route (DP-19), which calls the owner once and merges the answer into the screen model; the screen itself belongs to Epic 2 and the run record is published by RWB-P5-E1057-APP. This baseline fixes the answer shapes only and declares no screen field list and no route specification. The states its shapes imply are: a run in each of the three states, a channel row per channel read, a refusal count per reason code, a duplicate count, and a rerun that is refused because the run is still in progress. The screen states empty and loading are Not specified in the source documents (CG-ALL-6080); the error and no access states follow section 14.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P5-E1057-CON-01 | AC1, BR1, BR4, BR5 | Contract | The OpenAPI 3.1 document validates; the three operations and their statuses are declared; no sibling operation is redeclared and no foreign base is provided |
| TC-P5-E1057-CON-02 | AC2, BR3 | Contract | A run in each state with its channels; a renamed count fails the lint; a null channel list answers an empty array |
| TC-P5-E1057-CON-03 | AC3, BR6, BR8 | Contract | The channel code pattern with "BR-0123", "MAILROOM", "LF-007" and "MBX-RECOVERY-01"; a lower-case or over-long code fails the schema; a source outside the five values fails the enum |
| TC-P5-E1057-CON-04 | AC4, BR12 | Contract | One run per refusal reason code; a duplicate counted as refused fails the test; a fourth state fails the enum |
| TC-P5-E1057-CON-05 | AC5, BR10, BR11 | Contract | One answer per message ID of section 14 with its status; a rerun answered 200 fails the test; the same key twice starts one run; a live run answers 409 |
| TC-P5-E1057-CON-06 | AC6, BR9 | Contract | The event position and the absence test; a declared pickup event fails the build; a fourth event name fails the test |
| TC-P5-E1057-CON-07 | AC7, BR7 | Contract | The six fakes run against the document; every example is synthetic and no fake carries a sender address or a real file name |
| TC-P5-E1057-CON-08 | AC8, BR2, BR5 | Contract | The drift test over the document and the six fakes; a drifted path, status, field name, required flag or enum fails it |
| TC-P5-E1057-CON-09 | BR4, BR5 | Contract | Boundary of the four section 12.7 table rows: the two `rwb_document` tables are the only declared tables; a table outside `rwb_document` or outside those rows fails the test |
| TC-E1-057-17 | X12, BR7 (legacy Access) | Contract | The rerun fake answers 403 with MSG-P4-002 for a caller without Platform administration U |
| TC-E1-057-01 | AC1, BR1 | Contract | A run row with source "SCAN", channel "BR-0123" and one taken in |
| TC-E1-057-02 | AC2, BR1, BR4 | Contract | A run row with source "PARTNER" and channel "LF-007" |
| TC-E1-057-03 | AC3, BR1, BR9 | Contract | A run row with source "EMAIL" and channel "MBX-RECOVERY-01", and no sender address in any answer |
| TC-E1-057-04 | AC4, BR1 | Contract | A run row with source "SCAN" and channel "MAILROOM" |
| TC-E1-057-05 | AC5, BR2 | Contract | One refusal counted under MSG-P5-001 on channel "BR-0123" |
| TC-E1-057-06 | AC6, BR2 | Contract | One refusal under MSG-P5-017 for 25.1 MB and one taken in for 25.0 MB |
| TC-E1-057-07 | AC7, BR4 | Contract | Two refusals under PARTNER_UNKNOWN and PARTNER_NOT_ACTIVE |
| TC-E1-057-08 | AC8, BR5 | Contract | A duplicate counted once and taken in once |
| TC-E1-057-09 | AC9 (run by RWB-S9-E1057-APP) | Contract | A complete run with zero on every channel |
| TC-E1-057-10 | AC10 (run by RWB-P5-E1057-APP) | Contract | A failed run with MSG-GEN-006 naming the storage and no count |
| TC-E1-057-11 | AC11 (run by RWB-P5-E1057-APP), BR7 | Contract | Two failed runs in a row on channel "PARTNER_SFTP" and the alert text MSG-P5-008 |
| TC-E1-057-12 | AC12 (run by RWB-P5-E1057-APP), BR7 | Contract | One run for the 09:15 slot and no second run record |
| TC-E1-057-13 | AC13 (run by RWB-S9-E1057-APP) | Contract | A run with no taken-in attachment and the emails archived |
| TC-E1-057-14 | AC14 (run by RWB-P5-E1057-APP), BR6 | Contract | A duplicate counted on the run after a failed move |
| TC-E1-057-15 | AC15 (run by RWB-P5-E1057-APP), BR7 | Contract | A run at 18:15 produces no run record until 08:00 the next working day |
| TC-E1-057-16 | AC16 (run by RWB-P5-E1057-APP), BR3 | Contract | A taken-in row with an empty scanResult and ocrStatus PENDING, answered unchanged by the two GET operations |

The seventeen legacy test cases of RWB-E1-057 are listed in the order of the work package and the legacy story; each is answered here at contract level against the artefact and the fakes, and its business outcome is proved by RWB-P5-E1057-APP or, for AC2, AC3, AC7, AC9 and AC13, by RWB-S9-E1057-APP. TC-E1-057-17 keeps the legacy level Access and maps to Component in the app story and to Contract here, and the System level of the others maps to Contract because the artefact under test is the contract. The integration harness copies end in `-ITG` and belong to RWB-ITG-E1057-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the type list, the size limit, the duplicate window, the alert threshold, the channel values and the paging default stay parameters, reference rows or document defaults of the app story.
- No personal data in a schema, an example or a fake: identifiers, channel codes, counts, states and business dates only, and no sender address, no file name and no email subject.
- The channel code is a token and never a path, an address or a URL; the folder and the mailbox behind it stay in the property set of the deployment (BR8).
- No operation of this base is declared twice: the intake submit and read, the review list, the resolve and the content read belong to the sibling baselines (BR5).
- ACE data is reached only through the owner's contract or a `v_ace_*` view; this document declares no ACE view and no cross-schema join (DP-01).
- The contract names only `rwb_document` tables and only operations owned by `rwb-document`; a foreign base or a foreign table fails the review (DP-01).
- One REST base and one topic per service; a document that names another service's base or topic as its own fails the review.
- The path publishes no event and the contract invents none; a pickup event name fails the absence test (BR9).
- Every example in the document is synthetic and the legacy values are examples only; no production payload is copied into a schema or a fake.
- The contract declares no channel state and no run state machine beyond the values the fields may take; a transition belongs to RWB-P5-E1057-APP.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DCM-009 | Documents arrive from branches, mailroom, partner file transfer and email through the same intake | The run record, the channel code rule, the source enumeration and the three result counts | TC-P5-E1057-CON-02, TC-P5-E1057-CON-03, TC-E1-057-01, TC-E1-057-02, TC-E1-057-04 |
| REQ-DCM-010 | Every document carries a retention class, and intake runs a virus scan before the document is stored | The `scanResult` field, its empty state on insert and the declaration that the scan step owns it | TC-P5-E1057-CON-03, TC-E1-057-16 |

| Decision or pattern | Where it sits in this story |
|---|---|
| DP-01 | Only `rwb_document` tables declared; the partner read consumed and faked |
| DP-06 | The parameters row of 12.2 and the five parameter names |
| DP-07 | The reference-list row of 12.2 and the three lists |
| DP-09 | The idempotency rules, the topic position and the absence of a pickup event |
| DP-10 | The `pickup` activity contract and the workflow that calls it |
| DP-11 | All three consumed rows with one hop, a 2 s timeout and a fake |
| DP-13 | The rerun path rebased on the service base |
| DP-15 | The migration position recorded for the table behind the counts |
| DP-19 | The run record and the rerun behind gateway-bff, and the SCR-44 reference |
| ADR-013 | The service owns its schema inside ACE PostgreSQL |
| ADR-014 | The `rwb_document` schema and the rwb-document login |
| ADR-020 | Contract-first REST, one hop, 2 s timeout |
| ADR-021 | Per-service Flyway and migration ownership |

The legacy key is RWB-E1-057; its AC1, AC4, AC5, AC6, AC8, AC10, AC11, AC12, AC14, AC15 and AC16 are owned by RWB-P5-E1057-APP, its AC2, AC3, AC7, AC9 and AC13 by RWB-S9-E1057-APP, and the cross-service proof of the same values is RWB-ITG-E1057-ITG.

### 19. Out of scope

- The build of the pickup activity, the channel readers, the intake service, the alert service, the run record and the rerun: RWB-P5-E1057-APP.
- The partner panel and the mailbox channel criteria AC2, AC3, AC7, AC9 and AC13: RWB-S9-E1057-APP.
- The intake submit and the intake item read: RWB-P5-E1049-CON.
- The review list, the resolve operation and the content read: RWB-P5-E1032-CON.
- The scan result, the quarantine rule and the scan failure answers: RWB-P5-E1041-CON.
- The store, the write-once container and the version history: RWB-P5-E1024-APP.
- The channels, the hold container, the topic and the ACL provisioning: RWB-P5-E1057-INF.
- The chart, the Schedule registration, the flag values, the dashboards, the alerts and the runbook: RWB-P5-E1057-OPS.
- The parameters and reference-data catalogues themselves and their admin operations: P3 rwb-case.
- The partner panel, its statuses and its admin operations: S9 rwb-partner.
- The cross-service proof of these values: RWB-ITG-E1057-ITG.
