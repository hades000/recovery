# RWB-P1-E1066-CON Interaction ledger store and writer

SCB Collections and Recovery. Henka Group, 27 November 2026.
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
| Ready to start | After the dependency contracts and fakes are published |
| Size | Not specified; pending squad refinement |
| Depends on (build) | RWB-PLT-N009-CON, RWB-P3-E1018-CON, RWB-P7-E1027-CON, RWB-P3-E1043-CON, RWB-PLT-TE006-CON |
| Contract dependencies | None |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7), OpenAPI 3.1, base `/api/recovery/source-data/v1` |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v2.md (FR-P1-029, FR-P1-030) |
| Readiness decisions | RD-P1-001, RD-P1-003, RD-P1-004, RD-P1-005, RD-P1-007, RD-P1-008, RD-P1-011, RD-P1-022, RD-P1-023, RD-P1-064 |
| Status | Draft (directive resolutions) |

**Version 3 changes**

- Contract rebased on rwb-source-data.yaml 5.1.0: full InteractionRequest, required lists, types, case-scoped paths and the entry read (RD-P1-005, RD-P1-007).
- Shared `Problem` body, status table and idempotency rules replace the old envelope and MSG-GEN-004 (RD-P1-001, RD-P1-004); provided and consumed fakes named and versioned (RD-P1-011).
- Acceptance criteria rewritten and AC10 to AC16 added; AC7 and AC8 stay with RWB-P1-E1066-APP.
- Findings RWB-P1-E1066-CON#1 to #22 fixed or carried as pending with a gap ID (GAP-3487, S8-4, S8-5, S8-12, GAP-3352, GAP-3353, GAP-1475).
- Batch D: the dispatch and delivery values of a LETTER entry are ruled (RD-P1-064; GAP-3352 and GAP-3353 closed, superseding the fourth bullet); test case IDs TC-P1-E1066-CON-09 to -15 cited.

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register); applied RD-P1-001, RD-P1-003, RD-P1-004, RD-P1-005, RD-P1-007, RD-P1-008, RD-P1-011, RD-P1-022 and RD-P1-023; findings RWB-P1-E1066-CON#1 to #22.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-066 for rwb-source-data. The published Java interface `InteractionLedgerWriter` of the monolith becomes the contract baseline of a REST resource on base `/api/recovery/source-data/v1` (DP-11, DP-13), with the ledger owned by P1 in schema `rwb_source_data` (DP-01, DP-18; the R-PREC default ruling) and with the rwb-case timeline named as a consumer of this contract and never as a second ledger. The error envelope, the Idempotency-Key rule and the versioning rule follow the platform baseline; the two consumed contracts, the case read of rwb-case and the decision-log read of rwb-decision, are documented and faked and never defined here. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1066-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 21 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the interaction-ledger resource of rwb-source-data: an OpenAPI 3.1 document with the append, the list and the read of one entry, the `Interaction`, `InteractionRequest` and `InteractionPage` schemas, one error envelope with the agreed message IDs, the Idempotency-Key rule, the correction rule, the versioning rule, the nine contract tables of section 12 and the contract fakes for the provided ledger operations, the rwb-case case read and the rwb-decision decision-log read**, so that **the writer, the operations and the test stories of this legacy key, the rwb-case recording screens and the case timeline can build against a fixed, testable contract on Day 1 without waiting for rwb-source-data to be built**.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). In the monolith the ledger was written through an in-process interface, so the caller and the writer shared a transaction and a type; in the target the callers are the recording screens of rwb-case, the event paths of rwb-integration and the case timeline, and none of them may share a table with rwb-source-data (DP-01, DP-18; Architecture v5 slides 29 and 41).

The field set is the part that has to be agreed once. The API specification carries the `Interaction` schema (rwb-source-data.yaml 5.1.0), and the ledger columns of the legacy story are exactly the ones that schema names: `eventCode`, `caseSeq`, `actorType`, `actorRef`, `sourceRef`, `idempotencyKey`, `decisionLogId`, `correctsEntryId` and `retentionClass` are in the schema and in the table. If the contract fixes them once, the app story builds the writer in parallel with the operations story, rwb-case builds its screens and its timeline against the same document, and a change in either is caught in a contract test instead of an integration window.

The baseline also settles the one ownership question this legacy key raises. The API specification declares `/cases/{caseId}/interactions` with x-module P3, because the case timeline belongs to rwb-case; the ledger itself belongs to rwb-source-data by the R-PREC default ruling and DP-18. The contract therefore names P1 as the owner of the ledger resource and names the P3 path as a consumer that reads this contract: one ledger, one append, one read of an entry, and a timeline that composes them. It fixes the naming the checks require: schema `rwb_source_data`, REST base `/api/recovery/source-data/v1`, topic `rwb.source-data.events.v1`, event names `rwb.source-data.<Event>.v1`, task queue `rwb-source-data` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.sourcedata`.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, the topic and the event names follow the platform rule rather than a local choice.
- The published `Problem` component (`application/problem+json`) and the Error and Message Standard v6 are in force, so every status maps to one body and one message ID (Architecture v5 slide 11; RD-P1-004).
- The outbox, inbox and idempotency library is available as a reference for the stored-response behaviour and the table names (RWB-PLT-TE006-CON, DP-09).
- The API specification is the source of the `Interaction`, `InteractionRequest` and `InteractionPage` schemas, and its field list is carried into this baseline without a rename (Template and Rules §R7.3; R-PREC level 6).
- The operations and their owners are taken from the Ownership Map only: the ledger resource is P1's, the case read is P3's and the decision-log read is P7's; this document never declares another service's operation as its own (DP-01).
- The reference list LOV-LEDGER-EVENT is reference data of rwb-case and its values are carried in the document as an enumeration only, never as a business rule (DP-07; RWB-P3-E1043-CON).
- The build dependencies of the header are published before this contract is tagged.

### 4. Flow

1. Add the interaction-ledger resource to `rwb-source-data.yaml` 5.1.0 (OpenAPI 3.1) on base `/api/recovery/source-data/v1`: the append, the list with its filters, and the read of one entry, with the shared components of the service. No story-local yaml file is created (RD-P1-005 rule 1).
2. Carry the `Interaction` schema field for field from the API specification, mark `summary` as personal data, and add `InteractionRequest` and `InteractionPage`.
3. Use the published `Problem` body and the status table of 12.1; the business texts of the legacy story are unchanged.
4. State the header replay rule (RD-P1-001), the business-key rule (RD-P1-007 rule 4) and the correction rule: no update operation exists, so a correction is a second append naming the entry it corrects.
5. State the versioning rule for the REST surface, and the rule that the ledger has one owner and that the rwb-case timeline reads it.
6. Publish the nine contract tables of section 12, the provider fake, the consumed fakes and the ledger fixture.
7. Add the contract tests: schema validation, the field-set test against the API specification, the error mapping, the idempotency replay and the version negotiation.
8. Tag the baseline and hand it to RWB-P1-E1066-APP, RWB-P1-E1066-OPS, the rwb-case timeline story and every consuming service.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A body or query cannot be parsed, or a value is outside its list | 400 (unreadable body; list value in a query) or 422 (list value in a body), with `Problem` and `field` | MSG-GEN-001, MSG-GEN-007 | AC3, AC10, AC11 |
| X2 | A required value of the append is missing | 422 naming the field | MSG-GEN-001 | AC3, AC10 |
| X3 | The same header key with a different request or path, or while the first is in flight; a stored business key with a different request | 409; the stored entry is not overwritten | MSG-PLT-N009-05 | AC4 |
| X4 | The append omits the Idempotency-Key header or it is not a UUID | 400 naming the header | MSG-PLT-N009-03 | AC4 |
| X5 | The caller asks for a major version the service does not serve | 404 with `type` ending `/unknown-version` | MSG-GEN-007 | AC5 |
| X6 | A property or operation of rwb-source-data.yaml 5.1.0 is missing, or a fake drifts from it | The contract test fails and the merge is blocked | None | AC2, AC6, AC16 |
| X7 | The rwb-case or rwb-decision contract has no published fake | The baseline cannot be tagged, because a consumed contract is faked before it is built | None | AC6 |

X1 to X5 are the contract-level refusals of this baseline; MSG-P1-022, MSG-GEN-001, MSG-P4-002 and MSG-P4-003 keep their texts and are carried in the `Problem` body.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes and the Ownership Map only |
| Negotiable | Field-level descriptions, examples and the order of the query parameters are settled with the consumers; the operations, the owner, the envelope and the rules are fixed by the target architecture |
| Valuable | Unblocks the writer, the operations story, the recording screens and the case timeline on Day 1 |
| Estimable | One yaml fragment, three schemas, the shared `Problem`, three rules, nine contract tables and the fakes of 12.8 |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Interaction-ledger resource contract baseline for rwb-source-data

  Background:
    Given the service naming rule of the platform library is in force
    Given rwb-source-data.yaml 5.1.0 is the source of the Interaction, InteractionRequest, InteractionPage and Problem schemas

  Scenario: AC1 The OpenAPI 3.1 document describes the ledger operations (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-source-data is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/source-data/v1
    Then it declares POST /cases/{caseId}/interactions with the owner rwb-source-data
    Then it declares GET /cases/{caseId}/interactions with the query parameters from, to, channel, actor (string, at most 64), page (integer, minimum 0, default 0) and size (integer 1 to 200, default 50)
    Then it declares GET /cases/{caseId}/interactions/{entryId}
    Then POST needs Case record C, the two reads Case record R, and each operation declares exactly the statuses of the table in 12.1

  Scenario: AC2 The Interaction schema carries every field of the API specification (new, D-RCV-60)
    Given the Interaction schema of the published document
    When it is compared field for field with the Interaction schema of the API specification
    Then it carries every property of rwb-source-data.yaml 5.1.0, among them eventCode, caseSeq (integer int64, readOnly), actorType, actorRef, sourceRef, idempotencyKey, decisionLogId, correctsEntryId, documentId and retentionClass (at most 10 characters)
    Then `Interaction` requires id, caseId, occurredAt and sourceSystem
    Then `InteractionRequest` requires eventCode, occurredAt, actorType, actorRef, sourceRef and idempotencyKey
    Then `summary` is marked x-personal-data, and a caller with no unmasking rule reads it as "MASKED"
    Then every example in the document is synthetic and carries no production value

  Scenario: AC3 One problem body and one message mapping (new, D-RCV-60)
    Given the Problem component of the document
    When a 400, 401, 403, 404, 409, 422 or 503 response is produced
    Then the body is application/problem+json with type, title, status, messageCode and traceId, and detail, instance, messageTh, field or errors where they apply, and no other member
    Then each status carries the messageCode of the status table of 12.1
    Then no session answers 401 MSG-P4-001, a role without Case record C answers 403 MSG-P4-002 on POST, a case out of scope or unknown answers 404 MSG-P4-003 and a failed write answers 503 MSG-P1-022
    Then a 403 from the case contract maps to 404 MSG-P4-003

  Scenario: AC4 The append is idempotent and a correction is a new append (new, D-RCV-60)
    Given the POST /cases/{caseId}/interactions operation and its Idempotency-Key header
    When the request omits the header or sends a value that is not a UUID
    Then the service answers 400 MSG-PLT-N009-03
    When the first call with a key is accepted
    Then it answers 201 with the entry identifier and caseSeq
    When the same key is sent again with the same body within 24 hours
    Then the stored 201 and body are returned with the same id and caseSeq and no second row is written
    When the same key is sent with a different body, or while the first call is in flight
    Then the service answers 409 MSG-PLT-N009-05
    When a new header key carries a business idempotencyKey already stored, with the same request
    Then it answers 200 with the existing entry and no new caseSeq
    When a new header key carries that business key with a different request
    Then it answers 409 MSG-PLT-N009-05
    Then a caller treats any non-2xx answer as a failed action and keeps no action without its entry
    Then the document declares no PATCH and no PUT on an entry and no If-Match, because an entry is never updated
    Then a correction is a second POST carrying correctsEntryId with the entry it corrects

  Scenario: AC5 The ledger has one owner beside the rwb-case timeline (new, D-RCV-60)
    Given the published document and the ownership statement in it
    When the resource owners are reviewed against the Ownership Map
    Then the interaction ledger is owned by rwb-source-data and no other service declares an append
    Then the timeline operation GET /cases/{caseId}/interactions of rwb-case is named as a consumer that reads this contract through the ledger read interface
    Then the document states that the timeline composes this contract and never keeps a second ledger
    Then the document declares major version 1 in the path
    Then a call to /v2 answers 404 with messageCode MSG-GEN-007 naming the version as the value

  Scenario: AC6 The nine contract tables are complete and the fakes match them (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map
    Then the rwb-source-data provider fake at fakes/rwb-source-data/5.1.0/ answers every declared status of the three operations
    Then the rwb-case fake answers GET /api/recovery/case/v1/cases/{caseId} with a case in scope, a case out of scope, a 404, a 503 and a delay over 2 s
    Then the rwb-decision fake answers GET /api/recovery/decision/v1/decision-log/{entryId} with a decision entry and a missing entry
    Then the ledger fixture carries `interaction` with `uk_interaction` (idempotency key), `uk_interaction_case_seq` (case_id, case_seq) and the trigger `tr_interaction_append_only`
    Then the contract tests compare the fakes with the document and fail on any drift

  Scenario: AC9 The schema changes only additively within version 1 and carries only list values (new, D-RCV-60)
    Given the published version 1 document of the interaction-ledger resource
    When a schema change is checked against it
    Then, against baseline tag rwb-source-data 5.1.0, adding an optional property or operation passes the compatibility job
    Then removing, renaming or retyping a property, making a property required, removing an enum value or tightening a maxLength fails the job and needs a new major version
    Then the eventCode enumeration equals the 14 values of LOV-LEDGER-EVENT
    Then channel, direction and contactResult are values of LOV-CHANNEL, LOV-DIRECTION and LOV-CONTACT-RESULT

  # AC7 and AC8 belong to RWB-P1-E1066-APP (legacy RWB-E1-066 AC7, AC8)

  Scenario: AC10 The append request carries every ledger property (new, RD-P1-007)
    Given a valid CONTACT, DECISION_TAKEN and CORRECTION request
    When each is validated against InteractionRequest
    Then each passes
    When a required property is removed
    Then the fake answers 422 MSG-GEN-001 naming the field

  Scenario: AC11 Limits and list values are enforced (new, RD-P1-004)
    Given a summary of 2000 characters, a summary of 2001 characters and eventCode "FAX"
    When each is sent to the fake in an otherwise valid append
    Then 2000 characters are accepted
    Then 2001 characters answer 422 MSG-GEN-002 and "FAX" answers 422 MSG-GEN-007

  Scenario: AC12 The list parameters are bounded as the read story applies them (new)
    Given the list operation of RWB-P1-E1068-APP
    When it is called with size 200, then size 201, then page -1, then a channel outside LOV-CHANNEL, then from after to
    Then size 200 answers 200
    Then size 201 and page -1 answer 422 MSG-GEN-002, the channel answers 400 MSG-GEN-007 and the dates answer 422 MSG-GEN-003
    Then entries are ordered by occurredAt then caseSeq, and an empty ledger answers 200 with items [] and total 0

  Scenario: AC13 An entry of another case is not returned (new, RD-P1-005)
    Given an entry of case B
    When it is read under case A
    Then the answer is 404 MSG-P4-003 with no entry value

  Scenario: AC14 Authentication and rights on the append (new)
    Given no token, and then a token without Case record C
    When POST is called
    Then the answers are 401 MSG-P4-001 and 403 MSG-P4-002 and no entry is written

  Scenario: AC15 A slow case read refuses the append (new)
    Given the case fake delays more than 2 s
    When a user token posts a valid append
    Then the answer is 503 MSG-P1-022 and no entry is written

  Scenario: AC16 Consumers run against the same fake version (new, RD-P1-011)
    Given the consumer expectations of RWB-P1-E1067-APP, RWB-P3-E1066-APP and RWB-P2-E2001-APP
    When they run against the provider fake of version 5.1.0
    Then each uses the case-scoped path and every call validates against the yaml
```

**Target reading.** Two criteria above need a word on where the boundary sits, because the sources disagree. The API specification marks `/cases/{caseId}/interactions` x-module P3 with owner P1, and `GET /decision-log/{entryId}` x-module P7; the ledger resource of this contract is P1's, because the R-PREC default ruling gives the interaction ledger to rwb-source-data and DP-18 repeats it (Architecture v5 slides 29 and 41). This contract therefore fixes P1 as the owner of the append and of the read that serves it, and names the P3 timeline as a consumer of the ledger read interface. What the timeline does with the entries — ordering by `occurredAt` and `caseSeq`, the case header, the screen states — stays with rwb-case and is not described here. The ledger path is the case-scoped `/cases/{caseId}/interactions` on `/api/recovery/source-data/v1` (RD-P1-007 rule 2; ASM-3528, ASM-3542); the flat `/interactions` family and ASM-0696 and ASM-0697 are superseded. This service is the only writer of the ledger table, and rwb-integration writes intake outcomes through the same append contract (GAP-1511). The DP02 contact-and-consent row, its consent vocabulary and the UNSERVED value are not part of this contract and close against the reference-data contract of DP-07 (GAP-2181).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/source-data/v1`; a document never declares another service's path as its own | DP-13; Architecture v5 slide 41 notes |
| BR2 | The interaction ledger is owned by rwb-source-data and is one table in `rwb_source_data`; no other service keeps a copy and no consumer writes it | DP-01, DP-18; R-PREC default ruling; Architecture v5 slides 29 and 41 |
| BR3 | Every entry carries case, event, time, actor and source: `InteractionRequest` requires eventCode, occurredAt, actorType, actorRef, sourceRef and idempotencyKey, the case comes from the path and the source system is server-set | REQ-ILG-002; legacy RWB-E1-066 BR2; RD-P1-007 |
| BR4 | Every POST declares the Idempotency-Key header (UUID, 24 hours); a replay returns the stored status and body; the body idempotencyKey is a separate, permanent business key | Architecture v5 slide 11; DP-09; REQ-ILG-007; RD-P1-001; RD-P1-007 |
| BR5 | Entries are append only: the contract declares no update and no delete on an entry, so a correction is a new append naming the original | REQ-ILG-001; R-UNI-24; legacy RWB-E1-066 BR4 |
| BR6 | Error responses use the shared `Problem` body and one message ID per condition; the business texts are unchanged | Architecture v5 slide 11; RD-P1-004 |
| BR7 | The ledger records what happened and the decision log records why: the entry carries `decisionLogId` and never the rule, the version or the inputs | FEAT-ILG-02; ADR-009; legacy RWB-E1-066 BR6 |
| BR8 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 11 (BACKWARD compatibility) |
| BR9 | The contract fixes no business value of its own: `eventCode` is an enumeration of the values of LOV-LEDGER-EVENT, a closed list of the reference data, and the channels, the directions and the results are list values of the reference data | Template and Rules §R7.2 s17; DP-07; Reference Data and Lists of Values v5, LOV-LEDGER-EVENT |

**Where each rule lives in the target.** BR1 and BR8 are properties of the document and are tested by the schema linter, the compatibility job against baseline tag rwb-source-data 5.1.0 and the unknown-version test. BR2 is the ownership statement the document carries and the reason the P3 path is named as a consumer; the table itself is created in `rwb_source_data` by the migration of RWB-P1-E1066-APP and deployed by RWB-P1-E1066-OPS. BR3 and BR7 are schema requirements and are asserted field for field against the API specification (AC2). BR4 is the Idempotency-Key rule and the stored-response behaviour of the platform library, and its runtime proof is the app story's test. BR5 is an absence: the document declares no PATCH, no PUT and no DELETE, and the append carries `correctsEntryId`, so the rule is enforced by what the contract does not offer. BR6 is the envelope mapping of section 14. BR9 is the closed list declared as an enumeration with its owner named, so a value that is not in the enumeration fails schema validation.

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

The security scheme names the `rwb_source_data` service identity (DP-02). POST is authorised by Case record C from the caller's token plus the case read (RD-P1-007 rule 5); the rwb-case workload identity skips the case read for its pre-commit appends; no rwb-access authorise call is made by the append. The two reads follow RWB-P1-E1068-APP (rwb-access authorise and masking, exact fields GAP-0983).

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Interaction resource | Every property of the `Interaction` schema of rwb-source-data.yaml 5.1.0. Required: `id`, `caseId`, `occurredAt`, `sourceSystem`. Types: `caseSeq` integer int64 readOnly; `promiseAmount` number held as numeric(18,2); `retentionClass` at most 10 (ASM-3541 states 20 and is settled by RWB-P1-E2034-APP); `documentId` uuid | DF-INT-001 to DF-INT-029; `documentId` has no field ID (GAP-3497) |
| Append request | Required: `eventCode`, `occurredAt`, `actorType` (USER, SERVICE, PARTNER), `actorRef` (at most 64), `sourceRef` (at most 60), `idempotencyKey` (at most 120). Optional: `channel`, `direction`, `contactResult`, `actionCode` (10), `summary` (2000), `promiseAmount`, `promiseDate`, `contactKey` (255), `conductCheck`, `decisionLogId`, `correctsEntryId`, `fromHolderRef` (60), `toHolderRef` (60), `treatmentId`, `proceedsId`, `documentId`, `deliveryStatus`, `externalRef` (60). Server-set and never sent: `id`, path `caseId`, `caseSeq`, `sourceSystem`, `retentionClass` | DF-INT-014 to DF-INT-029 |
| Conditional rules | `correctsEntryId` for CORRECTION names an entry of the same case. For eventCode LETTER (RWB-P1-E2021-APP): `conductCheck` required when `deliveryStatus` is SENT or absent; `externalRef` required when `deliveryStatus` is present. Caller values (RD-P1-064): a dispatch entry carries `conductCheck` PASSED and `externalRef` = the WIN barcode; a letter refused by the conduct check carries `conductCheck` BLOCKED with no `deliveryStatus` and no `externalRef`; a delivery entry carries `externalRef` = barcode, else notice reference, so the two pair | RD-P1-064 |
| Page resource | `InteractionPage`: `items`, `page`, `size`, `total` | None; not stored |
| Personal data | `summary` is Restricted (Data Classification v5 R229) and `actorRef` Confidential (R234). `summary` reads as "MASKED" with no unmasking rule; `personKey` and `contactKey` are references and never a name, number or address; masking rows by role and record class are GAP-1475 | DF-INT-016 |
| Decision-log reference | `decisionLogId` only; the code, rule, version and inputs stay in rwb-decision | DF-INT-020 |

Entries for Workbench events (CASE_CREATED and the other intake codes) carry empty `channel` and `direction`; EFS history entries carry `sourceSystem` EFS, set by the writer when the key starts `EFS:` (RD-P1-007 rule 8).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/source-data/v1` (DP-13). InteractionLedgerWriter is the only component that writes the ledger, and it appends only. Inside rwb-source-data it is called in process (RWB-P1-E1067-APP, RWB-P1-E2034-APP and the RWB-P1-DM005-APP cutover); every other service uses REST.

| Method | Path | Purpose and contract | Access |
|---|---|---|---|
| POST | `/cases/{caseId}/interactions` (`postCasesCaseidInteractions`) | `InteractionRequest` in; new business key 201 `Interaction`; stored business key 200 with the existing entry. Header `Idempotency-Key` (UUID) required. Statuses 200, 201, 400, 401, 403, 404, 409, 422, 503 | Case record C |
| GET | `/cases/{caseId}/interactions` (`getCasesCaseidInteractions`) | `InteractionPage`; query `channel` (LOV-CHANNEL), `actor` (string at most 64, matches `actorRef`), `from`, `to`, `page` (minimum 0, default 0), `size` (1 to 200, default 50); ordered by `occurredAt` then `caseSeq`; empty ledger gives an empty page, and the screen shows MSG-P3-024. Statuses 200, 400, 401, 403, 404, 422, 503 | Case record R |
| GET | `/cases/{caseId}/interactions/{entryId}` (`getCasesCaseidInteractionsEntryid`) | One `Interaction`; 404 MSG-P4-003 when the entry is not on that case. Statuses 200, 400, 401, 403, 404, 503 | Case record R |

**Header and business keys.** Same header key and same request: the stored status and body are replayed for 24 hours. Same header key with another request or path, or in flight: 409 MSG-PLT-N009-05. Missing or non-UUID header: 400 MSG-PLT-N009-03. Key store unavailable: 503 MSG-PLT-N009-06 (RD-P1-001). The body `idempotencyKey` (form `<code>-<caseNo>-<yyyyMMdd>-<actionId>`; EFS history `EFS:<efs_record_key>`) is unique permanently: a new header key with a stored business key answers 200 with the existing entry, or 409 MSG-PLT-N009-05 when the request differs. A producer sends the same value in `ce_idempotencykey`. The append writes no decision record. No PATCH, PUT or DELETE exists; a correction is a new POST with `correctsEntryId`.

**Status table** (published `Problem` body, RD-P1-004):

| Condition | Status | messageCode |
|---|---|---|
| Body not parseable | 400 | MSG-GEN-001 |
| Required value missing in a body | 422 | MSG-GEN-001 |
| Value over its length or out of range | 422 | MSG-GEN-002 |
| `from` after `to` | 422 | MSG-GEN-003 |
| Value not in its list: query; body | 400; 422 | MSG-GEN-007 |
| `Idempotency-Key` missing or not a UUID | 400 | MSG-PLT-N009-03 |
| Header or business key conflict | 409 | MSG-PLT-N009-05 |
| Idempotency store unavailable | 503 | MSG-PLT-N009-06 |
| No session or no Workbench role | 401 | MSG-P4-001 |
| Role lacks the right | 403 | MSG-P4-002 |
| Case or entry missing or outside scope | 404 | MSG-P4-003 |
| Ledger cannot be written, or the case read of the append fails or exceeds 2 s | 503 | MSG-P1-022 |
| Case read of a GET fails or exceeds 2 s | 503 | MSG-GEN-006 |
| Unsupported major version | 404 | MSG-GEN-007 |

Pending: the refusal answers for a `DECISION_TAKEN` reference that is missing, unknown or not answered (GAP-3487), and the messageCode for a `correctsEntryId` outside the case with the rule for a future `occurredAt` (GAP-3489).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline | Fake |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case check of the three operations: existence and scope; a 404 or 403 answers 404 MSG-P4-003 to a user caller; the append skips it for the rwb-case workload identity | RWB-P3-E1018-CON fake |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | Confirms the decision-log reference of a `DECISION_TAKEN` entry; the identifier alone is stored | RWB-P7-E1027-CON fake |
| POST | `/api/recovery/access/v1/authorise` and the rwb-access masking read | P4 rwb-access | The two GET operations only: Case record R and the `summary` masking answer (RWB-P1-E1068-APP); field names pending (GAP-0983) | RWB-P4-E1037-CON fake |

Each is one hop with a 2 s timeout and a breaker per downstream (DP-11). The reference list LOV-LEDGER-EVENT is consumed through the rwb-case reference-data contract and its client library (DP-07; RWB-P3-E1043-CON), so it appears in the document as an enumeration with its owner named and not as a third operation.

#### 12.3 Events published

None of its own. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP and are published in RWB-P1-E1015-CON (RD-P1-022). The ledger append publishes no decision record. Each acting service records its own decision through the decision-record library; the shared event type is `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` (RD-P1-008). This contract publishes no event.

#### 12.4 Events consumed

None for this resource. The append arrives over REST or in process; the ledger intake that consumes business events is published in RWB-P1-E1067-CON.

#### 12.5 Workflows and activities

None. No workflow, activity or Schedule is part of this contract; the append is synchronous. The task queue `rwb-source-data` in namespace `rwb-recovery` and its activities belong to the other P1 stories.

#### 12.6 Schedules

None.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `interaction` | P1 (rwb_source_data) | The ledger resource: the append, the list and the read of one entry; keys `uk_interaction` and `uk_interaction_case_seq`, trigger `tr_interaction_append_only`; migration owner RWB-P1-E1066-APP |
| `processed_event` | PLT library, created in rwb_source_data | Used by the ledger intake of RWB-P1-E1067-APP only, not by this resource |
| `idempotency_key` | PLT library, created in rwb_source_data | The stored response of the append |
| `outbox_event` | PLT library, created in rwb_source_data | Not used: the append writes no decision record |

No other table is named in the contract, and no table of another service is read (DP-01). `recovery_case` stays in `rwb_case` and `decision_log_entry` stays in `rwb_decision`; both are reached over the consumed operations of 12.2 only.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case WireMock | `GET /cases/{caseId}`: case in scope, out of scope, 404, 503 and delay over 2 s | App story, contract tests |
| rwb-decision WireMock | `GET /decision-log/{entryId}` with one decision entry and a missing entry | App story, contract tests |
| Ledger fixture | `interaction` at the baseline plus the RWB-P1-E1066-APP migration, with `uk_interaction`, `uk_interaction_case_seq` and `tr_interaction_append_only` | App story, operations smoke run, contract tests |
| rwb-case reference-data fake | The 14 values of LOV-LEDGER-EVENT with their Thai labels | Contract tests |
| **Provider fake** rwb-source-data 5.1.0, `fakes/rwb-source-data/5.1.0/` (WireMock generated from the yaml) | `postCasesCaseidInteractions`, `getCasesCaseidInteractions`, `getCasesCaseidInteractionsEntryid`: one mapping per declared status, including 201, header replay, 200 business repeat, 400, 401, 403, 404, 409 MSG-PLT-N009-05, 422, 503, delay over 2 s, list with entries and empty page; fixtures with the 14 event codes | RWB-P1-E1067-APP, RWB-P3-E1066-APP, RWB-P2-E2001-APP and every other REST appender |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 3 consumed | The append, the list and the read of one entry; the case read, the decision-log read and the rwb-access authorise and masking read; one hop, 2 s timeout |
| Kafka | None of its own | The append publishes no decision record; acting services record their decisions through the library |
| Temporal | None | No workflow, activity or Schedule in this contract |
| File | None | No file in this contract |

### 13. Solution plan

**Deliverables.** The ledger fragment of `rwb-source-data.yaml` 5.1.0 (API Specification v7) with the shared `Problem` and `IdempotencyKey` components, the idempotency, correction and versioning rules in the contract README, the provider fake and the consumed fakes of 12.8. The actor filter is backed by `ix_interaction_case_actor` (Physical Schema v9).

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

1. The paths, security rights, error responses and shared components in `rwb-source-data.yaml`; schema lint and the compatibility job against tag rwb-source-data 5.1.0.
2. The three operations and the three schemas, with the `Interaction` field set compared against the API specification by a test (AC1, AC2).
3. The `Problem` body and the status table of 12.1 (AC3, AC11, AC14).
4. The Idempotency-Key rule, the stored-response behaviour and the correction rule, and the statement that no update operation exists (AC4).
5. The versioning rule and the ownership statement that names the rwb-case timeline as a consumer (AC5).
6. The nine contract tables and the four fakes of 12.8.
7. The contract tests of section 16; a drift between a fake and the document fails both the provider and the consumer build (AC6, AC16).
8. Baseline tag and the consumer sign-off note.

**Done when.** The yaml validates in the pipeline, the field-set test passes with no missing property, the contract tests of section 16 pass, and the fakes of 12.8 answer every provided and consumed path of 12.1 and 12.2.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-022 | The ledger write failed, or the append's case read failed | The entry was not saved because the interaction ledger could not be written. Try again in a few minutes. |
| MSG-GEN-001 | A required value is missing, or the body cannot be parsed | Enter {field}. |
| MSG-GEN-002 | A value is outside its length or range | {field} must be between {min} and {max}. |
| MSG-GEN-003 | `from` is after `to` | {field} cannot be before {other}. |
| MSG-GEN-006 | The case read of a GET does not complete | {system} is not available. Try again in a few minutes. |
| MSG-GEN-007 | A value is not in its list, or the major version is not served | {value} is not a valid value for {field}. Choose a value from the list. |
| MSG-PLT-N009-03, -05, -06 | Header key missing or invalid; conflict; store unavailable | Platform texts (Error and Message Standard v6) |
| MSG-P4-001 | No valid session or no Workbench role | Platform text (Error and Message Standard v6) |
| MSG-P4-002 | Role without Case record C or R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case or entry missing or out of scope | This case is not in your scope. |
| MSG-P3-024 | Screen text for an empty ledger | Nothing is recorded in {section} yet. |

Thai text follows DL10 (recommended option A: the business lead drafts per module and Legal and Compliance approve). MSG-GEN-004 is the concurrent-change message and is not used by this resource.

### 15. Screens and states

The contract serves the recording screens of the rwb-case slice and the case timeline, both of which arrive through the gateway-bff composite route (DP-19; RWB-PLT-N001-CON). The timeline shows the entries of one case ordered by `occurredAt` and `caseSeq` and renders `summary` as "MASKED" where the role may not see it; the states of that screen (loading, empty, list, error) belong to rwb-case and to the screen owners. This baseline fixes the ledger side of the merge only. This story owns no screen and no screen state; the recording screens and the case timeline are built by RWB-P3-E1018-APP. The composite route specification and the screen field list are outside this contract and belong to the screen owners.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P1-E1066-CON-01 | AC1 | Contract | The yaml validates; three operations, parameters, rights and statuses |
| TC-P1-E1066-CON-02 | AC2 | Contract | Field set, required lists, types and `summary` mark |
| TC-P1-E1066-CON-03 | AC3 | Contract | `Problem` body and messageCode per status |
| TC-P1-E1066-CON-04 | AC4 | Contract | Header replay and conflict, missing header, business repeat, no PATCH or PUT |
| TC-P1-E1066-CON-05 | AC5 | Component | Ownership statement, P3 consumer statement, /v2 refused |
| TC-P1-E1066-CON-06 | AC6 | Component | Nine contract tables and fakes |
| TC-P1-E1066-CON-07 | AC9, BR8, BR9 | Contract | Compatibility job against tag 5.1.0; list values |
| TC-P1-E1066-CON-08 | AC6 | Contract | Table ownership of 12.7 |
| TC-P1-E1066-CON-09 to TC-P1-E1066-CON-15 | AC10 to AC16 | Contract | Request properties, limits, list parameters, entry of another case, 401 and 403, slow case read, consumer fake run |

Test Cases v9 holds TC-P1-E1066-CON-01 to -15 for the criteria of this story. Legacy TC-P1-E1066-APP-15 to TC-P1-E1066-APP-17 are run by RWB-P1-E1066-APP; the other legacy cases belong to the slices that own those criteria.

### 17. Guardrails

- No business value in the contract: the event codes, the channels, the directions and the results stay list values of the reference data, and the document names their owner.
- No personal data in an event schema, an example or a fake: `summary` is marked and masked, `personKey` and `contactKey` are references, and every example is synthetic.
- The contract names only rwb-source-data's ledger table and the platform library objects; no other service's table is read or documented as provided (DP-01).
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13, DP-14).
- One ledger and one append: the document declares no second append, and the P3 timeline is named as a consumer and never as an owner (DP-18).
- Every POST declares the Idempotency-Key, and no entry is ever updated or deleted by a contract operation (DP-09; R-UNI-24).
- The `Problem` body, the idempotency helper and the naming rule come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-ILG-001 | One ledger holds every interaction on a case | The ledger resource, the ownership statement, the no-update rule | TC-P1-E1066-CON-01, TC-P1-E1066-CON-05 |
| REQ-ILG-002 | Every entry carries case, event, time, actor and source | The required properties of `Interaction` and `InteractionRequest` | TC-P1-E1066-CON-02 |
| REQ-ILG-004 | Offer, promise, payment or hand-over recorded on its interaction | `promiseAmount` and `promiseDate` on the entry, `treatmentId`, `proceedsId` | TC-P1-E1066-CON-02 |
| REQ-ILG-008 | A failed ledger write loses no entry and is reported | 503 MSG-P1-022 in the status table; the incident is raised by the calling service or by the intake | TC-P1-E1066-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three provided operations and the two consumed operations with their client budget | TC-P1-E1066-CON-06 |
| ASM-3542 | The ledger is P1's on the case-scoped path and the P3 timeline consumes it | The ownership statement and the consumer statement of AC5 | TC-P1-E1066-CON-05 |

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
- The ledger read behaviour beyond the contract shape of 12.1 (RWB-P1-E1068-APP).
- The outbox path from a business event to an entry, and the duplicate rule across event keys (RWB-P1-E1067-APP).
- The case contract of rwb-case and the decision-log contract of rwb-decision: consumed and faked here, never defined (RWB-P3-E1018-CON, RWB-P7-E1027-CON).
- The central decision ledger, its entries and its versions (the P7 stories).
- The values of LOV-LEDGER-EVENT and their Thai labels (rwb-case, RWB-P3-E1043-CON); the document carries them as an enumeration with their owner.
- The gateway-bff composite route and the screen field list (RWB-PLT-N001-CON and the screen owners).
- The flat `/interactions` paths and `GET /interactions?externalRef=` named by older consumer stories: withdrawn; consumers repoint to the case-scoped read (RD-P1-007 rule 2).
- The contact-point read and the failed-contact record, and DP07 records and freshness: not operations of this resource (records and freshness are RWB-P1-E1015-CON; contact points GAP-1070, GAP-1097).
- The LETTER entry business rules (RWB-P1-E2021-APP) and the retention class resolution (RWB-P1-E2034-APP).

### Remaining delivery steps

- Size the story at refinement; owner: squad.
- Obtain epic design sign-off; owner: product owner.
- Publish the contract at the tag rwb-source-data 5.1.0; owner contract owner.
- Add or update story tests in Test Cases v9 (W2-tests); owner: test writer.
- Run the required test data in DEV after implementation; owner: delivery team.
- Rule the masking rows by role and record class; owner data steward; GAP-1475.
- Rule the decision-log reference refusals; owner solution architect; GAP-3487.
- Rule the future-date rule and the correction messageCode; owner solution architect; GAP-3489.
- Add the `document_id` column or withdraw `documentId`; owner data architect; GAP-3497.
- Publish the provider fake of version 5.1.0; owner contract owner.
