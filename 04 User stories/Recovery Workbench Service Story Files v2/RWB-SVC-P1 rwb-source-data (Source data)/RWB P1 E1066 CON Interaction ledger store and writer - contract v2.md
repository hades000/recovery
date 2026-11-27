# RWB-P1-E1066-CON Interaction ledger store and writer

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1066-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-066 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP09, DP11, DP13, DP15, DP18, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Size | Sized by the squad at refinement |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | v1 on base `/api/recovery/source-data/v1` (OpenAPI 3.1 baseline of this story) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-029, FR-P1-030) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-066 for rwb-source-data. The published Java interface `InteractionLedgerWriter` of the monolith becomes the contract baseline of a REST resource on base `/api/recovery/source-data/v1` (DP-11, DP-13), with the ledger owned by P1 in schema `rwb_source_data` (DP-01, DP-18; the R-PREC default ruling) and with the rwb-case timeline named as a consumer of this contract and never as a second ledger. The error envelope, the Idempotency-Key rule and the versioning rule follow the platform baseline; the two consumed contracts, the case read of rwb-case and the decision-log read of rwb-decision, are documented and faked and never defined here. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1066-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 21 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the interaction-ledger resource of rwb-source-data: an OpenAPI 3.1 document with the append, the list and the read of one entry, the `Interaction`, `InteractionRequest` and `InteractionPage` schemas, one error envelope with the agreed message IDs, the Idempotency-Key rule, the correction rule, the versioning rule, the nine contract tables of section 12 and the contract fakes for the rwb-case case read and the rwb-decision decision-log read**, so that **the writer, the operations and the test stories of this legacy key, the rwb-case recording screens and the case timeline can build against a fixed, testable contract on Day 1 without waiting for rwb-source-data to be built**.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). In the monolith the ledger was written through an in-process interface, so the caller and the writer shared a transaction and a type; in the target the callers are the recording screens of rwb-case, the event paths of rwb-integration and the case timeline, and none of them may share a table with rwb-source-data (DP-01, DP-18; Architecture v5 slides 29 and 41).

The field set is the part that has to be agreed once. The API specification already carries an `Interaction` schema with twenty-nine properties, and the ledger columns of the legacy story are exactly the ones that schema names: `eventCode`, `caseSeq`, `actorType`, `actorRef`, `sourceRef`, `idempotencyKey`, `decisionLogId`, `correctsEntryId` and `retentionClass` are in the schema and in the table. If the contract fixes them once, the app story builds the writer in parallel with the operations story, rwb-case builds its screens and its timeline against the same document, and a change in either is caught in a contract test instead of an integration window.

The baseline also settles the one ownership question this legacy key raises. The API specification declares `/cases/{caseId}/interactions` with x-module P3, because the case timeline belongs to rwb-case; the ledger itself belongs to rwb-source-data by the R-PREC default ruling and DP-18. The contract therefore names P1 as the owner of the ledger resource and names the P3 path as a consumer that reads this contract: one ledger, one append, one read of an entry, and a timeline that composes them. It fixes the naming the checks require: schema `rwb_source_data`, REST base `/api/recovery/source-data/v1`, topic `rwb.source-data.events.v1`, event names `rwb.source-data.<Event>.v1`, task queue `rwb-source-data` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.sourcedata`.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, the topic and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the RFC 9457 problem details and the message catalogue are in force, so every status maps to one envelope and one message ID (Architecture v5 slide 11).
- The outbox, inbox and idempotency library is available as a reference for the stored-response behaviour and the table names (RWB-PLT-TE006-CON, DP-09).
- The API specification is the source of the `Interaction`, `InteractionRequest` and `InteractionPage` schemas, and its field list is carried into this baseline without a rename (Template and Rules §R7.3; R-PREC level 6).
- The operations and their owners are taken from the Ownership Map only: the ledger resource is P1's, the case read is P3's and the decision-log read is P7's; this document never declares another service's operation as its own (DP-01).
- The reference list LOV-LEDGER-EVENT is reference data of rwb-case and its values are carried in the document as an enumeration only, never as a business rule (DP-07; RWB-P3-E1043-CON).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the interaction-ledger resource on base `/api/recovery/source-data/v1`: the append, the list with its filters, and the read of one entry, with the shared components of the service.
2. Carry the `Interaction` schema field for field from the API specification, mark `summary` as personal data, and add `InteractionRequest` and `InteractionPage`.
3. Agree the error envelope and map every status of the resource to its message ID, reusing the business texts of the legacy story unchanged.
4. State the Idempotency-Key rule on the append, its stored-response behaviour, and the correction rule: no update operation exists, so a correction is a second append naming the entry it corrects.
5. State the versioning rule for the REST surface, and the rule that the ledger has one owner and that the rwb-case timeline reads it.
6. Publish the nine contract tables of section 12 and the two consumed fakes with the ledger fixture.
7. Add the contract tests: schema validation, the field-set test against the API specification, the error mapping, the idempotency replay and the version negotiation.
8. Tag the baseline and hand it to RWB-P1-E1066-APP, RWB-P1-E1066-OPS, the rwb-case timeline story and every consuming service.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request body or a query parameter fails schema validation | 400 with the error envelope and the failing pointer | MSG-GEN-004 | AC3 |
| X2 | A required value of the append is missing | 422 with the error envelope naming the field | MSG-GEN-001 | AC3 |
| X3 | The same Idempotency-Key is replayed with a different body | 409 with the error envelope; the stored entry is not overwritten | MSG-GEN-004 | AC4 |
| X4 | The append omits the Idempotency-Key header | 400 with the error envelope naming the header | MSG-GEN-004 | AC4 |
| X5 | The caller asks for a major version the service does not serve | 404 with the error envelope and the served major version | MSG-GEN-004 | AC5 |
| X6 | A field of the API specification is missing from the document, or a fake drifts from the document | The contract test fails and the merge is blocked | None | AC2, AC6 |
| X7 | The rwb-case or rwb-decision contract has no published fake | The baseline cannot be tagged, because a consumed contract is faked before it is built | None | AC6 |

X1 to X5 are the contract-level refusals of this baseline; the business texts MSG-P1-022, MSG-GEN-001, MSG-P4-002 and MSG-P4-003 are carried unchanged from the legacy story and are mapped in the same envelope.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes and the Ownership Map only |
| Negotiable | Field-level descriptions, examples and the order of the query parameters are settled with the consumers; the operations, the owner, the envelope and the rules are fixed by the target architecture |
| Valuable | Unblocks the writer, the operations story, the recording screens and the case timeline on Day 1 |
| Estimable | One document, three schemas, one error envelope, three rules, nine contract tables and four fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Interaction-ledger resource contract baseline for rwb-source-data

  Background:
    Given the service naming rule of the platform library is in force
    Given the API specification is the source of the Interaction, InteractionRequest and InteractionPage schemas

  Scenario: AC1 The OpenAPI 3.1 document describes the ledger operations (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-source-data is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/source-data/v1
    Then it declares POST /cases/{caseId}/interactions with the owner rwb-source-data
    Then it declares GET /cases/{caseId}/interactions with the query parameters from, to, channel, actor, page and size
    Then it declares GET /cases/{caseId}/interactions/{entryId}
    Then every operation names its security right and its error responses 400, 401, 403, 404, 409, 422 and 503

  Scenario: AC2 The Interaction schema carries every field of the API specification (new, D-RCV-60)
    Given the Interaction schema of the published document
    When it is compared field for field with the Interaction schema of the API specification
    Then it carries every property of the specification, among them eventCode, caseSeq, actorType, actorRef, sourceRef, idempotencyKey, decisionLogId, correctsEntryId and retentionClass
    Then no property returns a personal value in clear text
    Then the summary property is marked as personal data and returns the mask Not specified in the source documents (ACR-RWB-P1-E1066-CON-AC2) to a caller whose role may not see it
    Then every example in the document is synthetic and carries no production value
    Then each property marked required in the API specification as settled at the baseline review is marked required in the document

  Scenario: AC3 One error envelope and one message mapping (new, D-RCV-60)
    Given the error envelope component of the document
    When a 400, 401, 403, 404, 409, 422 or 503 response is produced
    Then the body carries the code, the message, the messageId, the traceId and the field list
    Then the response carries the problem media type and the trace identifier
    Then the messageId is one of MSG-P1-022, MSG-GEN-001, MSG-P4-002, MSG-P4-003 or MSG-GEN-004, with the agreed text
    Then a refused write maps to 503 with MSG-P1-022, a missing field to 422 with MSG-GEN-001, a missing right to 403 with MSG-P4-002 and a case outside the scope to 404 with MSG-P4-003
    Then a refusal of the case contract for a case the caller may not see maps to 404 with MSG-P4-003, and 403 with MSG-P4-002 only for a role without Case record R

  Scenario: AC4 The append is idempotent and a correction is a new append (new, D-RCV-60)
    Given the POST /cases/{caseId}/interactions operation and its Idempotency-Key header
    When the request omits the header
    Then the service answers 400 with the error envelope and MSG-GEN-004
    When the first call with a key is accepted
    Then it answers 201 with the entry identifier and caseSeq
    When the same key is sent twice with the same body
    Then the second call returns the stored entry with the same caseSeq and writes no second row
    When the same key is sent with a different body
    Then the service answers 409 with the error envelope
    Then a caller treats any non-2xx answer as a failed action and keeps no action without its entry
    Then the document declares no PATCH and no PUT on an entry and no If-Match, because an entry is never updated
    Then a correction is a second POST carrying correctsEntryId with the entry it corrects

  Scenario: AC5 The ledger has one owner beside the rwb-case timeline (new, D-RCV-60)
    Given the published document and the ownership statement in it
    When the resource owners are reviewed against the Ownership Map
    Then the interaction ledger is owned by rwb-source-data and no other service declares an append
    Then the timeline operation GET /cases/{caseId}/interactions of rwb-case is named as a consumer that reads this contract through the ledger read interface
    Then the document states that the timeline composes this contract and never keeps a second ledger
    Then the document declares major version 1 in the path, and an unsupported major version is answered 404 with the error envelope

  Scenario: AC6 The nine contract tables are complete and the fakes match them (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map
    Then the rwb-case fake answers GET /api/recovery/case/v1/cases/{caseId} with a case in scope, a case out of scope and a 404
    Then the rwb-decision fake answers GET /api/recovery/decision/v1/decision-log/{entryId} with a decision entry and a missing entry
    Then the ledger fixture carries the table, the two unique keys and the append-only trigger
    Then the contract tests compare the fakes with the document and fail on any drift

  Scenario: AC9 The schema changes only additively within version 1 and carries only list values (new, D-RCV-60)
    Given the published version 1 document of the interaction-ledger resource
    When a schema change is checked against it
    Then an additive change is accepted within major version 1
    Then a breaking change is refused within major version 1 and needs a new major version
    Then every eventCode value of the enumeration is a value of the closed list LOV-LEDGER-EVENT of the reference data
    Then the channels, the directions and the results are list values of the reference data
```

**Target reading.** Two criteria above need a word on where the boundary sits, because the sources disagree. The API specification declares `/cases/{caseId}/interactions` with x-module P3 and `GET /decision-log/{entryId}` with x-module P7; the ledger resource of this contract is P1's, because the R-PREC default ruling gives the interaction ledger to rwb-source-data and DP-18 repeats it (Architecture v5 slides 29 and 41). This contract therefore fixes P1 as the owner of the append and of the read that serves it, and names the P3 timeline as a consumer of the ledger read interface. What the timeline does with the entries — ordering by `occurredAt` and `caseSeq`, the case header, the screen states — stays with rwb-case and is not described here. The P1 ledger resource path is `/cases/{caseId}/interactions` on the service base `/api/recovery/source-data/v1`, because the legacy writer had no path at all (GAP-0505; ASM-0697). This service is the only writer of the ledger tables, and rwb-integration writes intake outcomes through the same append contract (GAP-1511). The DP02 contact-and-consent row, its consent vocabulary, the LETTER append members and the UNSERVED value are not yet published; until they are, the shapes of 12.1 and the mapping of section 13 hold and the point closes against the reference-data contract of DP-07 (GAP-2181).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/source-data/v1`; a document never declares another service's path as its own | DP-13; Architecture v5 slide 41 notes |
| BR2 | The interaction ledger is owned by rwb-source-data and is one table in `rwb_source_data`; no other service keeps a copy and no consumer writes it | DP-01, DP-18; R-PREC default ruling; Architecture v5 slides 29 and 41 |
| BR3 | Every entry carries case, event, time, actor and source, and the schema carries them as required | REQ-ILG-002; legacy RWB-E1-066 BR2 |
| BR4 | Every POST declares the Idempotency-Key and stores its response; a replay with the same body returns the stored entry and the same caseSeq | Architecture v5 slide 11; DP-09; REQ-ILG-007 |
| BR5 | Entries are append only: the contract declares no update and no delete on an entry, so a correction is a new append naming the original | REQ-ILG-001; R-UNI-24; legacy RWB-E1-066 BR4 |
| BR6 | Error responses use one envelope and one message ID per condition; the business texts are copied unchanged from the legacy story | Architecture v5 slide 11; Template and Rules §R7.2 s14 |
| BR7 | The ledger records what happened and the decision log records why: the entry carries `decisionLogId` and never the rule, the version or the inputs | FEAT-ILG-02; ADR-009; legacy RWB-E1-066 BR6 |
| BR8 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 11 (BACKWARD compatibility) |
| BR9 | The contract fixes no business value of its own: `eventCode` is an enumeration of the values of LOV-LEDGER-EVENT, a closed list of the reference data, and the channels, the directions and the results are list values of the reference data | Template and Rules §R7.2 s17; DP-07; Reference Data and Lists of Values v5, LOV-LEDGER-EVENT |

**Where each rule lives in the target.** BR1 and BR8 are properties of the document and are tested by the schema linter and the version-negotiation test. BR2 is the ownership statement the document carries and the reason the P3 path is named as a consumer; the table itself is created in `rwb_source_data` by the migration of RWB-P1-E1066-APP and deployed by RWB-P1-E1066-OPS. BR3 and BR7 are schema requirements and are asserted field for field against the API specification (AC2). BR4 is the Idempotency-Key rule and the stored-response behaviour of the platform library, and its runtime proof is the app story's test. BR5 is an absence: the document declares no PATCH, no PUT and no DELETE, and the append carries `correctsEntryId`, so the rule is enforced by what the contract does not offer. BR6 is the envelope mapping of section 14. BR9 is the closed list declared as an enumeration with its owner named, so a value that is not in the enumeration fails schema validation.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The three operations, the three schemas and the two consumed contracts are described | In review |
| In review | Consumer sign-off | The app and operations stories, the rwb-case timeline story and the test stories accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, or an operation is withdrawn | New major version drafted |
| Baselined | Drift in a fake, or a missing field against the API specification | A contract test fails | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-source-data | Owns the document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Consuming teams (app, operations, test, the rwb-case timeline and the rwb-integration event paths) | Review and sign off the parts they consume |
| Data steward | Confirms that `summary` is marked as personal data and that no event or example carries a clear personal value |
| rwb-case (P3) | Owns the case, its scope and the timeline; agrees the consumer statement of the ledger read |
| rwb-decision (P7) | Owns the decision-log contract this document consumes and fakes |

The per-service login name behind the document's security scheme and the exact resource path of the ledger are Not specified in the source documents (GAP-0505; ASM-0697); the document names the login as "the `rwb_source_data` login (DP-02)" and fixes the path as `/cases/{caseId}/interactions` on the service base. Every operation of this contract is authorised through the rwb-access authorise check (DP-08), which this story does not define.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Interaction resource | Every property of the `Interaction` schema of the API specification: `id`, `caseId`, `personKey`, `occurredAt`, `channel`, `direction`, `actionCode`, `contactResult`, `promiseAmount`, `promiseDate`, `summary`, `conductCheck`, `sourceSystem`, `eventCode`, `actorType`, `actorRef`, `sourceRef`, `idempotencyKey`, `caseSeq`, `decisionLogId`, `correctsEntryId`, `contactKey`, `fromHolderRef`, `toHolderRef`, `treatmentId`, `proceedsId`, `retentionClass`, `deliveryStatus` and `externalRef`, from `interaction` fields DF-INT-001 to DF-INT-021 and the channel-ledger fields the specification adds | DF-INT-001 to DF-INT-021 |
| Append request | `InteractionRequest` of the API specification: `channel`, `direction`, `result`, `summary`, plus the ledger values the append needs, carried as one schema and never as free text | Not specified in the source documents (DOR-RWB-P1-E1066-CON-7) |
| Page resource | `InteractionPage` of the API specification: `items`, `page`, `size`, `total` | Not specified in the source documents (DOR-RWB-P1-E1066-CON-7) |
| Personal data | `summary` is marked `x-personal-data: true` and is masked by role; `personKey` and `contactKey` are references and never a name, a number or an address; no other field is classed as personal data | Not specified in the source documents (DOR-RWB-P1-E1066-CON-7) |
| Decision-log reference | `decisionLogId` only; the code, rule, version and inputs stay in rwb-decision | Not specified in the source documents (DOR-RWB-P1-E1066-CON-7) |

The field-level detail of the append request — which ledger values are required, which are nullable for a Workbench event, and the exact length of each — is Not specified in the source documents (GAP-0505; ASM-0697); this baseline fixes the property names from the API specification and leaves the required flags to the review.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-source-data (P1); base `/api/recovery/source-data/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| POST | `/cases/{caseId}/interactions` | `InteractionRequest` in; 201 with `Interaction`; `Idempotency-Key` header required, a repeat with the same key replays the stored response (Flow step 4) | Case record C on the case |
| GET | `/cases/{caseId}/interactions` | `InteractionPage`; query parameters `from`, `to`, `channel`, `actor`, `page`, `size` | Case record R on the case |
| GET | `/cases/{caseId}/interactions/{entryId}` | `Interaction` of one entry | Case record R on the entry's case |

The error responses are 400 for a body or a query that fails validation, 401 without a session, 403 without Case record C or R, 404 for a case or an entry that does not exist or is out of scope, 409 for an `Idempotency-Key` already used with a different body, 422 for a missing or invalid field, and 503 when the ledger cannot be written or a consumed contract does not answer inside 2 s. `GET /cases/{caseId}/interactions` is the list the ledger read interface serves with its filters; RWB-P1-E1068-APP implements that read interface and records the path it serves, and this document fixes the shape and the parameters of the page. The ledger resource path is `/cases/{caseId}/interactions` on the service base, with the single-entry read at `/cases/{caseId}/interactions/{entryId}`, the split of the error statuses above is fixed here, the ledger is written under the rwb_source_data login, and the authorisation of the append needs Case record C (GAP-0505; GAP-0504; ASM-0697).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline | Fake |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case check of the append: the case exists and the caller holds Case record C and the case scope; a 404 is passed on as 404 with MSG-P4-003 | RWB-P3-E1018-CON fake |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | Confirms the decision-log reference of a `DECISION_TAKEN` entry; the identifier alone is stored | RWB-P7-E1027-CON fake |

Both are one hop with a 2 s timeout and a breaker per downstream (DP-11). The reference list LOV-LEDGER-EVENT is consumed through the rwb-case reference-data contract and its client library (DP-07; RWB-P3-E1043-CON), so it appears in the document as an enumeration with its owner named and not as a third operation.

#### 12.3 Events published

None of its own. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1013-APP (Architecture v5 slides 15 and 41). The decision-record library publishes `rwb.decision-record.DecisionRecorded.v1` on the shared topic `rwb.decision-record.v1` when a decision entry is appended, under the CloudEvents 1.0 envelope (DP-03, DP-09); that is the library's event, it is not declared in this document, and this baseline adds no message schema.

#### 12.4 Events consumed

None. The append arrives over REST from the recording screens and from the event paths of rwb-integration, and Architecture v5 slide 15 gives this service no consumed event. The outbox rebuild of one entry from a business event is RWB-P1-E1067-APP and is out of this baseline.

#### 12.5 Workflows and activities

None. No workflow, activity or Schedule is part of this contract; the append is synchronous. The task queue `rwb-source-data` in namespace `rwb-recovery` and its activities belong to the other P1 stories.

#### 12.6 Schedules

None.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `interaction` | P1 (rwb_source_data) | The ledger resource: the append, the list and the read of one entry |
| `processed_event` | PLT library, created in rwb_source_data | The inbox of DP-09 (the event paths of rwb-integration) |
| `idempotency_key` | PLT library, created in rwb_source_data | The stored response of the append |
| `outbox_event` | PLT library, created in rwb_source_data | The outbox the decision-record library writes through |

No other table is named in the contract, and no table of another service is read (DP-01). `recovery_case` stays in `rwb_case` and `decision_log_entry` stays in `rwb_decision`; both are reached over the consumed operations of 12.2 only.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case WireMock | `GET /cases/{caseId}` with a case in scope and Case record C, a case out of scope, a 404 and a timeout | App story, contract tests |
| rwb-decision WireMock | `GET /decision-log/{entryId}` with one decision entry and a missing entry | App story, contract tests |
| Ledger fixture | The `interaction` table at the baseline plus the ledger migration, with the two unique keys and the append-only trigger | App story, operations smoke run, contract tests |
| rwb-case reference-data fake | The twelve values of LOV-LEDGER-EVENT with their Thai labels | Contract tests |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 2 consumed | The append, the list and the read of one entry; the case read and the decision-log read; one hop, 2 s timeout |
| Kafka | None of its own | `DecisionRecorded` is published by the local decision-record library on `rwb.decision-record.v1` |
| Temporal | None | No workflow, activity or Schedule in this contract |
| File | None | No file in this contract |

### 13. Solution plan

**Deliverables.** `openapi/rwb-source-data-interactions-v1.yaml` (OpenAPI 3.1), `contract/error-envelope.yaml`, the idempotency, correction and versioning rules in the contract README, and the four fakes of 12.8 with their stub fixtures. The optional actor filter of the read is backed by an index whose name, columns and migration are Not specified in the source documents (GAP-0585).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | ACE data only through this service's own contract or views; the ledger contract names no ACE object | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case and the client library | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox, inbox and idempotency library; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/source-data/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the error responses and the shared components; schema lint in the pipeline.
2. The three operations and the three schemas, with the `Interaction` field set compared against the API specification by a test (AC1, AC2).
3. The error envelope and the message-ID mapping, with the business texts copied unchanged (AC3).
4. The Idempotency-Key rule, the stored-response behaviour and the correction rule, and the statement that no update operation exists (AC4).
5. The versioning rule and the ownership statement that names the rwb-case timeline as a consumer (AC5).
6. The nine contract tables and the four fakes of 12.8.
7. The six contract tests; a drift between a fake and the document, or a missing field against the API specification, fails the build (AC6).
8. Baseline tag and the consumer sign-off note.

**Done when.** The document validates in the pipeline, the field-set test against the API specification passes with no missing property, the six contract tests pass, and the four fakes answer every provided and consumed path of sections 12.1 and 12.2.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-022 | The ledger write failed (new, see additions) | The entry was not saved because the interaction ledger could not be written. Try again in a few minutes. |
| MSG-GEN-001 | A required value is missing | Enter {field}. |
| MSG-P4-002 | Role without Case record C or R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case missing or out of scope | This case is not in your scope. |
| MSG-GEN-004 | The request body, a query parameter or a required header fails validation, or an unsupported major version is requested | The request could not be read: {detail}. |

Thai text for each message follows decision DL10, which is still open; its assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 are confirmed by the programme directive (D-RCV-60). MSG-P1-022, MSG-GEN-001, MSG-P4-002 and MSG-P4-003 keep their legacy text unchanged; MSG-GEN-004 is the general validation and version message and its text is the platform text carried as above.

### 15. Screens and states

The contract serves the recording screens of the rwb-case slice and the case timeline, both of which arrive through the gateway-bff composite route (DP-19; RWB-PLT-N001-CON). The timeline shows the entries of one case ordered by `occurredAt` and `caseSeq` and renders `summary` masked by role; the states of that screen (loading, empty, list, error) belong to rwb-case and to the screen owners. This baseline fixes the ledger side of the merge only. This story owns no screen and no screen state; the recording screens and the case timeline are built by RWB-P3-E1018-APP. The composite route specification and the screen field list are Not specified in the source documents (GAP-0505; ASM-0697).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P1-E1066-CON-01 | AC1 | Contract | The document validates; the three operations, the six query parameters with the case in the path, and the seven error statuses are present |
| TC-P1-E1066-CON-02 | AC2 | Contract | The `Interaction` field set compared with the API specification; `summary` marked personal data; every property free of a clear personal value |
| TC-P1-E1066-CON-03 | AC3 | Contract | 400, 401, 403, 404, 409, 422 and 503 responses carry one envelope and a valid message ID |
| TC-P1-E1066-CON-04 | AC4 | Contract | A POST without the header; a replay with the same body; a replay with a different body; a correction with `correctsEntryId`; no PATCH, PUT or If-Match in the document |
| TC-P1-E1066-CON-05 | AC5 | Component | The ownership statement, the consumer statement of the P3 timeline, and an unsupported major version refused |
| TC-P1-E1066-CON-06 | AC6 | Component | The nine contract tables complete and the four fakes matching their provided and consumed paths |
| TC-P1-E1066-CON-07 | AC9, BR8, BR9 | Contract | A schema change additive within version 1 accepted; a breaking change refused within version 1; every enumerated value a list value of the reference data, with no business value of the contract's own |
| TC-P1-E1066-CON-08 | AC6 | Contract | The four tables of 12.7 each with its owner; no other table named; no table of another service read |
| TC-E1-066-01 | AC1, BR2, BR3 — regression evidence: AC1 is owned by the rwb-case and rwb-integration slices of this key | End to end | Case RW-2026-000201 with 6 entries; outbound call with promise 25,000.00 |
| TC-E1-066-02 | AC2, BR1, BR7 — regression evidence: AC2 is owned by the recovery slices and the cross-service proof | End to end | 4 EFS entries, CASE_CREATED and CASE_ALLOCATED |
| TC-E1-066-03 | AC3, BR6 — regression evidence: AC3 is owned by the rwb-case slice and the rwb-decision contract | End to end | Reassignment under R-UNI-18 version 2026.11 |
| TC-E1-066-04 | AC4, BR5 — regression evidence: AC4 is owned by the rwb-integration slice and the cross-service proof | End to end | Insert forced to fail |
| TC-E1-066-05 | AC5 — regression evidence: AC5 is owned by RWB-P1-E1066-APP over this contract | End to end | append() with no event code |
| TC-E1-066-06 | AC6, BR7 — regression evidence: AC6 is owned by RWB-P1-E1066-APP over this contract | End to end | Two concurrent appends on one case |
| TC-E1-066-07 | AC7 — regression evidence: run by RWB-P1-E1066-APP over the case fake (AC7 is not owned by this story) | End to end | Unknown case ID |
| TC-E1-066-08 | AC8, BR4 — regression evidence: run by the owner story of AC8 (the migration trigger of this key and the cross-service proof; AC8 is not owned by this story) | End to end | UPDATE and DELETE on entry case_seq 3; CORRECTION entry |
| TC-E1-066-09 | Access — regression evidence: the access path belongs to the rwb-case slice | Component | RW-AUDIT posts an interaction; refused with MSG-P4-002 |

The six contract test cases are this story's and run against the artefacts. The nine legacy test case IDs are kept in order and their Covers and Data are carried onto the split, with the legacy level "System" mapped to "End to end" and "Access" to "Component"; they are regression rows here because the criteria they cover are owned by the slices named in each Covers cell, and they run again on the contract in RWB-ITG-E1066-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the event codes, the channels, the directions and the results stay list values of the reference data, and the document names their owner.
- No personal data in an event schema, an example or a fake: `summary` is marked and masked, `personKey` and `contactKey` are references, and every example is synthetic.
- The contract names only rwb-source-data's ledger table and the platform library objects; no other service's table is read or documented as provided (DP-01).
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13, DP-14).
- One ledger and one append: the document declares no second append, and the P3 timeline is named as a consumer and never as an owner (DP-18).
- Every POST declares the Idempotency-Key, and no entry is ever updated or deleted by a contract operation (DP-09; R-UNI-24).
- The error envelope, the problem media type, the CloudEvents envelope and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-ILG-001 | One ledger holds every interaction on a case | The ledger resource, the ownership statement, the no-update rule | TC-P1-E1066-CON-01, TC-P1-E1066-CON-05 |
| REQ-ILG-002 | Every entry carries case, event, time, actor and source | The required properties of `Interaction` and `InteractionRequest` | TC-P1-E1066-CON-02 |
| REQ-ILG-004 | Offer, promise, payment or hand-over recorded on its interaction | `promiseAmount` and `promiseDate` on the entry, `treatmentId`, `proceedsId` | TC-P1-E1066-CON-02 |
| REQ-ILG-008 | A failed ledger write loses no entry and is reported | 503 with MSG-P1-022 in the envelope mapping | TC-P1-E1066-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three provided operations and the two consumed operations with their client budget | TC-P1-E1066-CON-06 |
| ASM-0697 | The ledger is P1's and the P3 timeline consumes it | The ownership statement and the consumer statement of AC5 | TC-P1-E1066-CON-05 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1066-APP | App development | H consumer: implements the three operations of 12.1 and writes the ledger |
| RWB-P1-E1066-OPS | DevOps | Consumer: deploys the resource, the migration and the alerts of the writer |
| RWB-P1-E1067-APP | App development | Sibling of the same legacy key: the outbox path that appends from a business event, on this contract |
| RWB-P1-E1068-APP | App development | Sibling of the same legacy key: the read interface and its filters, whose shape this contract fixes in `GET /cases/{caseId}/interactions` |
| RWB-P3-E1018-APP | App development | Consumer: the recording screens and the case timeline of rwb-case |
| RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON | Contract | H: the decision-record library, the reference-data client library, the outbox and inbox library, the per-service Flyway sequence and the gateway-bff composite route |
| RWB-P3-E1043-CON, RWB-P3-E1018-CON, RWB-P7-E1027-CON | Contract | C: the reference-data contract, the case contract and the decision-log contract, each documented as consumed and faked |

### 19. Out of scope

- The writer, the controller, the repository and the migration as code (RWB-P1-E1066-APP).
- The chart, the migration step, the flag, the five series, the three alerts and the smoke run (RWB-P1-E1066-OPS).
- The case timeline of rwb-case, its ordering, its screen and its states (RWB-P3-E1018-APP); this contract names it as a consumer and fixes the ledger side only.
- The ledger read interface and its filter behaviour beyond the shape fixed in `GET /interactions` (RWB-P1-E1068-APP).
- The outbox path from a business event to an entry, and the duplicate rule across event keys (RWB-P1-E1067-APP).
- The case contract of rwb-case and the decision-log contract of rwb-decision: consumed and faked here, never defined (RWB-P3-E1018-CON, RWB-P7-E1027-CON).
- The central decision ledger, its entries and its versions (the P7 stories).
- The values of LOV-LEDGER-EVENT and their Thai labels (rwb-case, RWB-P3-E1043-CON); the document carries them as an enumeration with their owner.
- The gateway-bff composite route and the screen field list (RWB-PLT-N001-CON and the screen owners).
- The field-level required flags and the exact length of each append property (GAP-0505; ASM-0697).
