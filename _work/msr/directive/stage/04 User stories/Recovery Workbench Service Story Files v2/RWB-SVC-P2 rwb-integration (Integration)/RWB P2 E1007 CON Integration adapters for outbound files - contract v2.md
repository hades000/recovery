# RWB-P2-E1007-CON Integration adapters for outbound files

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P2-E1007-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Contract version | v1, on `/api/recovery/integration/v1` |
| Patterns applied | DP01, DP02, DP03, DP05, DP07, DP09, DP10, DP11, DP16, DP17, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Size | Sized by the squad at refinement; not sized in this story (DOR-RWB-P2-E1007-CON-16) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| Fakes until publish (DP-03, DP-07, DP-09, DP-10, DP-19) | RWB-PLT-E1027-CON; RWB-PLT-E1043-CON; RWB-P3-E1043-CON; RWB-PLT-TE006-CON; RWB-PLT-E1071-CON; RWB-PLT-N001-CON, built against fakes until publish |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (FR-P2-001, FR-P2-002, FR-P2-003, FR-P2-004, FR-P2-005, FR-P2-006, FR-P2-007, FR-P2-008, FR-P2-009, FR-P2-010, FR-P2-011, FR-P2-012, FR-P2-013, FR-P2-014, FR-P2-015, FR-P2-016, FR-P2-017, FR-P2-018, FR-P2-020, FR-P2-021, FR-P2-022) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-007 for rwb-integration. The legacy story had no published contract: one module held the adapter, the scheduler, the tables and the exception queue, its "published interfaces" were three Java interfaces in one package and its two endpoints sat under the monolith base. This story fixes the contract of the outbound-file capability of rwb-integration on `/api/recovery/integration/v1`, the AsyncAPI document of `rwb.integration.events.v1` with `FileDelivered` and `FileFailed`, the `deliverFile(manifest)` and `receiveFile` activity contract on queue `rwb-integration`, one error envelope, the Idempotency-Key rule, the versioning rule and the contract fakes, so that the app, infrastructure, operations and test stories of this key can start on Day 1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (25 resolved, 47 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the rwb-integration outbound-file capability fixed as a contract: the four admin operations of the exception queue on the service base, the two events `FileDelivered` and `FileFailed` on `rwb.integration.events.v1` with the CloudEvents 1.0 envelope, the `deliverFile(manifest)` and `receiveFile` activities on queue `rwb-integration` with the manifest of a claim-check file, one error envelope, the Idempotency-Key rule on every POST, the versioning and compatibility rule, the nine contract tables and the fakes of every consumed service**, so that **every team of this key builds on Day 1 against one agreed, testable shape and no team waits for another service, or for the app story, to exist**.

The legacy story described a pattern in prose and three Java interfaces inside one package. That was enough while one module owned the adapter, the retry schedule, the tables and the screen. Across a service boundary it is not: the requesting service has to know what `deliverFile` accepts and returns, the operations team has to know what the exception queue reads, the app story has to know what a delivery row means, the test stories have to know what a fake may answer, and the debt-sale team has to know that its files travel on the same contract. This document is that answer, and it is deliberately narrow: it declares the four admin operations, two events, two provided activities, one manifest, one envelope and nine fakes, and it declares nothing that belongs to another service.

The contract also fixes the seams the split creates, and says so where a source is silent. The manifest of `deliverFile` is the claim-check manifest of Architecture v5 slide 11 — fileId, batchId, sha256, record count — widened with the interface, the business date, the case IDs, the idempotency key, the claim-check link and the requesting service; its exact payload is Not specified in the source documents, so it is fixed here and carried as a gap row (GAP-0648; ASM-1078). Whether `deliverFile` returns when the item is PENDING or when the file is acknowledged is fixed the same way: it returns the item reference and the status, and the requesting service learns the outcome from `FileDelivered` or `FileFailed`. Both are the kind of seam that costs a week per team if it stays unwritten.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling rule (DP-11, ADR-020) and the event contract is the platform rule (DP-09, DP-14). Both only pay off if the seams are written once. Here the seams are small and load-bearing: four admin operations, two events, two activities, one manifest, five consumed services and nine fakes. The business values behind them are already fixed by the legacy story — the retry intervals, the attempt limit, the exception queue, the owner task, the resend — so what is left is shape, and shape is what unblocks parallel work.

If the shape is agreed and faked on Day 1, four teams move at once. The app story builds the builder, the sender, the retry policy, the inbox and the four operations against the fakes; the infrastructure story provisions the endpoints, the keys and the staging area to the manifest and the budgets of this document; the operations story provisions the topic, the queue, the windows and the alerts against the events and the states declared here; the test and integration stories read one event shape and one state list. Without it, each team invents its own manifest, the delivery states diverge between the sender and the screen, and the one property the business asked for — that a failed file is found on the day it fails and reaches a named owner — depends on which service was written first.

The contract also states what this service does not own and does not do. Only rwb-source-data reads the thirty `recovery.v_ace_*` views, so no element of this contract is an ACE read (DP-05; ASM-1071). `debt_sale_account` is rwb-debtsale's, so the INT-25 tape rows travel in the manifest and are never read here (DP-01; ASM-1072). There is no data lake, so no element names a lake target (DP-17; ASM-1073). There is no inbound adapter, so `receiveFile` is published for completeness and called by no wave-1 flow (BR9). And the two Airflow windows are not Schedules of this service (ASM-1074).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the REST base, the topic, the event names and the task queue follow the platform rule and not a local choice (DP-13, DP-14).
- The CloudEvents 1.0 envelope, the JSON Schema registry with BACKWARD compatibility, the platform error envelope and the message catalogue are the platform baseline (DP-09); this document narrows them where it must and says so.
- The outbox and inbox library contract is available (RWB-PLT-TE006-CON): `outbox_event`, `processed_event`, `outbox_delivery`, `idempotency_key`, the retry topics and the `.dlt` topic are its elements and are reused, not redefined.
- The Temporal workflow kit contract is available (RWB-PLT-E1071-CON): the typed activity and workflow interfaces, the task queue naming, the retry and heartbeat policy, the codec and the build ID rule (DP-10).
- The owners' contracts are as published: the rwb-source-data freshness, customer and account operations (RWB-P1-E1015-CON and the P1 stories), the rwb-comms notice read (RWB-P6-E1007-APP), the rwb-document store and read (RWB-P5-E1007-APP), the rwb-case case action (RWB-P3-E1007-APP) and the rwb-access authorise operation (RWB-P4-E1037-CON). This story consumes them and fakes them; it defines none of them.
- The reference-data contract of rwb-case carries the lists this contract names (RWB-PLT-E1043-CON, RWB-P3-E1043-CON; DP-07).
- The decision-record library contract is available (RWB-PLT-E1027-CON; DP-03).
- The gateway-bff composite route that serves SCR-09 is published (RWB-PLT-N001-CON; DP-19).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the provided operations: the four admin paths on `/api/recovery/integration/v1`, their query parameters, their response types, their rights and their idempotency.
2. Draft the error envelope: one RFC 9457 problem-details body, the status codes of the four operations, and the message identifier each code carries.
3. Draft the AsyncAPI document of `rwb.integration.events.v1`: `FileDelivered` and `FileFailed`, their CloudEvents attributes, their key, their payload elements and the rule that neither carries personal data or file content.
4. Draft the activity contract: `deliverFile(manifest)` and `receiveFile` on queue `rwb-integration`, the manifest element list, the return element, the typed failures and the retry classification.
5. Draft the consumed contracts as this service sees them: the five owner operations, their placeholders where no source names a path or a field, and the degradation rule for a 4xx and a 5xx.
6. State the tables and their ownership, including that the outbox, inbox and idempotency objects are library objects created in `rwb_integration` and that no ACE view and no other service's table is named.
7. State the versioning and compatibility rule: `/v1` in the path, additive change only within a version, a breaking change in a new version, BACKWARD compatibility in the registry.
8. Publish the nine fakes and the drift test that compares each fake with this document.
9. Tag the baseline and hand it to the app, infrastructure, operations and test stories of this key.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A provided operation is called without a session or without a Recovery role | The envelope answers 401 before any read | MSG-P4-001 | AC1 |
| X2 | A provided operation is called by a role without the Platform administration right | The envelope answers 403 and nothing changes | MSG-P4-002 | AC1 |
| X3 | A resend names an unknown item or delivery | The envelope answers 404 | MSG-P4-003 | AC1 |
| X4 | A resend names an item or delivery that is not in EXCEPTION, or whose version changed | The envelope answers 409 and nothing changes | MSG-GEN-004 | AC1 |
| X5 | A message on `rwb.integration.events.v1` misses a CloudEvents attribute or carries a type other than the two | The contract test fails the producer, and at run time the consumer routes the message to `.dlt` with an alert | None | AC2 |
| X6 | An event payload would carry a name, an address, an identity number or file content | The schema refuses the field and the contract test fails the build | None | AC2 |
| X7 | A fake drifts from this document, or the app calls a path this document does not declare | The contract test fails and the merge is blocked | None | AC5 |
| X8 | A consumed contract removes, renames or retypes an element this document declares | The contract returns to review with the owner of that operation and the stories of this key are re-baselined | None | AC4 |
| X9 | A field-level detail of a consumed operation is missing from the source material | The element carries the placeholder of §R9, one gap row and one assumption row, and the fake is written to the assumed shape | None | AC4, AC5 |
| X10 | A code path or a migration of this service reaches another schema, an ACE view or a foreign key | The architecture boundary test fails the build | None | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; uses the platform envelopes, the library contracts and the owners' published operations, and declares none of theirs as its own |
| Negotiable | Field-level detail of the consumed operations is settled with their owners; the manifest, the two events, the four operations and the state list are fixed by this realignment |
| Valuable | Unblocks the app, infrastructure, operations and test stories of this key on Day 1 and gives rwb-comms, rwb-payment and rwb-debtsale one file contract to call |
| Estimable | Four provided operations, two events, two activities, five consumed services, nine tables and nine fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact — the OpenAPI document, the AsyncAPI document, the activity contract, the fake, this file — and never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the outbound-file capability for rwb-integration

  Background:
    Given the service naming rule and the CloudEvents 1.0 envelope of the platform library are in force
    Given the outbox, inbox and idempotency library contract of RWB-PLT-TE006-CON is in force
    Given the service base is /api/recovery/integration/v1, the topic is rwb.integration.events.v1 and the task queue is rwb-integration

  Scenario: AC1 The four admin operations and the one error envelope are published (new, D-RCV-60)
    Given the OpenAPI 3.1 document of this contract
    When the four operations are reviewed
    Then the operations are GET /admin/outbound-items, POST /admin/outbound-items/{itemId}/resend, GET /admin/outbox/deliveries and POST /admin/outbox/deliveries/{deliveryId}/resend on the base
    Then each operation names its right as Platform administration R or U and states that the scope is applied
    Then both POST operations require the Idempotency-Key header and answer 409 on an item or delivery not in EXCEPTION
    Then every error is one RFC 9457 problem-details body carrying the status, the code, the message identifier and the trace id
    Then the document declares no fifth path, no other base and no path of another service

  Scenario: AC2 The topic carries FileDelivered and FileFailed and nothing else (new, D-RCV-60)
    Given the AsyncAPI document of rwb.integration.events.v1
    When the two event types are validated
    Then the types are rwb.integration.FileDelivered.v1 and rwb.integration.FileFailed.v1
    Then each message carries the CloudEvents 1.0 attributes id, source, type, specversion, time, subject and datacontenttype in binary mode
    Then each message is keyed by the case ID and its payload carries fileId, interfaceId, businessDate and the facts of the event only
    Then no payload element can carry a name, an address, an identity number or file content
    Then an eighth type and a message without the envelope are refused by the contract test and routed to .dlt at run time

  Scenario: AC3 The deliverFile and receiveFile activity contract carries the claim-check manifest (new, D-RCV-60)
    Given the activity contract of this document
    When deliverFile and receiveFile are reviewed
    Then both are activities on the task queue rwb-integration and on no other queue
    Then the deliverFile input carries fileId, batchId, sha256, recordCount, interfaceId, businessDate, caseIds, idempotencyKey, the claim-check link and the requesting service
    Then the deliverFile output carries the item reference and the item status, and the outcome arrives as FileDelivered or FileFailed
    Then receiveFile is published for completeness and no wave-1 flow calls it
    Then a typed failure distinguishes a non-retryable refusal from a retryable failure, and no activity input carries file content
    Then the exact manifest payload is the assumed shape of GAP-0648 and is re-confirmed at the contract review

  Scenario: AC4 The nine contract tables are complete and attributed (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map
    Then 12.7 names interface_config, outbound_item and job_catalog as P2 tables and the four library objects created in rwb_integration
    Then no ACE view, no recovery schema table and no other service's table is named as an object of this service
    Then 12.2 names the five consumed services and no operation of theirs appears as provided
    Then 12.6 registers no Temporal Schedule for the two file windows

  Scenario: AC5 The nine fakes answer every declared path and drift fails the build (new, D-RCV-60)
    Given the nine fakes of 12.8
    When each fake is compared with the element it serves
    Then every consumed path and payload is answered with the shape of this document
    Then every error answer named in this document, 401, 403, 404, 409, 422, 503, is reachable in a fake
    Then the withheld file, the failed transfer and the duplicate event are reproducible from the fakes alone
    Then a drift between a fake and this document fails the contract test and blocks the merge

  Scenario: AC6 Versioning, compatibility and the boundary are fixed (new, D-RCV-60)
    Given the published contract and the code and migrations of this key
    When the compatibility and boundary checks run
    Then the version is in the path as /v1 and a breaking change requires a new version
    Then an additive change within the version keeps the schema subject BACKWARD compatible
    Then the boundary test finds no statement on an ACE view, no cross-schema read, no foreign key out of rwb_integration and no SFTP call outside the transport component
    Then no element of this contract names a data lake, a lake file or a lake delivery
    Then INT-19, INT-20, JOB-13 and JOB-15 are removed with no target in this service

  Scenario: AC7 Every business rule of section 8 is traced to its contract element (new, D-RCV-60)
    Given the business rules of section 8 and the published contract of this document
    When each rule is reviewed against its contract element
    Then the contract declares only /api/recovery/integration/v1 and rwb.integration.events.v1 as its own base and topic (BR1)
    Then only FileDelivered and FileFailed are published, keyed by case ID with the CloudEvents 1.0 envelope (BR2)
    Then the four admin operations are the exception queue surface and no /interface-runs path is declared (BR3)
    Then every POST requires the Idempotency-Key header and a repeat within 24 hours returns the stored response and changes nothing (BR4)
    Then every error is one RFC 9457 body and a resend of an item or delivery not in EXCEPTION, or of a changed version, answers 409 (BR5)
    Then deliverFile and receiveFile are on queue rwb-integration in namespace rwb-recovery with the claim-check manifest (BR6)
    Then no element is an ACE read and rwb_integration holds no grant on the recovery schema (BR7)
    Then debt_sale_account is never read and the INT-25 tape rows travel in the deliverFile manifest (BR8)
    Then no wave-1 flow calls receiveFile and interface_config holds outbound rows only (BR9)
    Then no element names a lake target and INT-19, INT-20, JOB-13 and JOB-15 have no target in this service (BR10)
    Then retry counts, intervals, owner role, alert role and lists are versioned rows and no contract element fixes a value (BR11)
    Then no event, command, activity input or fake carries personal data or file content (BR12)
    Then the version is in the path, an additive change stays within it, a breaking change needs a new version and the registry subject is BACKWARD compatible (BR13)
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base and one topic per service: this contract declares `/api/recovery/integration/v1` and `rwb.integration.events.v1` and never declares another service's path or topic as its own | DP-13; DP-14; Arch v5 slide 41 |
| BR2 | The two events are `rwb.integration.FileDelivered.v1` and `rwb.integration.FileFailed.v1` on `rwb.integration.events.v1`, keyed by case ID and carried with the CloudEvents 1.0 envelope; no other type is published | Arch v5 slides 16, 41 and 43; DP-09 |
| BR3 | The four admin operations are the exception queue surface of this service, on the paths of the TSD P2 v3 appendix and the Ownership Map; the naming of Architecture v5 slide 16 (`/interface-runs`) is superseded | TSD P2 v3 T-A.1 API-P2-001 to API-P2-004; Ownership Map; GAP-0648; ASM-1076 |
| BR4 | Every POST carries the Idempotency-Key header and stores its response for 24 hours; a repeat returns the stored response and changes nothing | Arch v5 slide 11; TSD P2 v3 T3.1 `idempotency_key` |
| BR5 | Every error is one RFC 9457 problem-details body; a resend of an item or delivery not in EXCEPTION, or a changed version, is 409 | Arch v5 slide 11; TSD P2 v3 T-A.2 |
| BR6 | `deliverFile(manifest)` and `receiveFile` are activities on queue `rwb-integration` in namespace `rwb-recovery`; the manifest is a claim-check manifest with fileId, batchId, sha256 and the record count, widened with the interface, the business date, the case IDs, the idempotency key, the claim-check link and the requesting service | Arch v5 slides 11 and 16; DP-10; GAP-0648; ASM-1078 |
| BR7 | Only rwb-source-data reads the `recovery.v_ace_*` views; no element of this contract is an ACE read and `rwb_integration` holds no grant on the recovery schema | Arch v5 slides 8, 9 and 29; ADR-010; DP-05; ASM-1071 |
| BR8 | `debt_sale_account` is rwb-debtsale's and is never read by this service: the INT-25 tape rows travel in the `deliverFile` manifest | Ownership Map; DP-01; FSD P2 v3 A1.5; ASM-1072 |
| BR9 | There is no inbound adapter: `receiveFile` is published for completeness, no wave-1 flow calls it, and `interface_config` holds outbound rows only | D-RCV-35 U1; ADR-010; FSD P2 v3 A1.6 |
| BR10 | There is no data lake: no element names a lake target; INT-19, INT-20, JOB-13 and JOB-15 are removed with no target in this service, and no lake file, lake copy or lake delivery row is created; the reporting projection is rwb-reporting's from the business events, and the decision ledger is fed from the shared decision-record topic | DP-17; Arch v5 slides 2, 8, 37 and 44; GAP-1163; ASM-1073 |
| BR11 | The retry counts, intervals, owner role, alert role and lists are `interface_config` rows and reference-data rows with the version in force; no element of the contract fixes a value | DP-07; DP-09; TSD P2 v3 T3.1 and T3.2 |
| BR12 | No personal data in an event, a command, an activity input or a fake: identifiers, codes, counts and hashes only, and the claim-check link instead of the file | Arch v5 slide 11; CTL-11; DP-09 |
| BR13 | The version is in the path, an additive change is allowed within it and a breaking change needs a new version; the registry subject is BACKWARD compatible, and the subject name and the compatibility level are platform values | Arch v5 slide 11; DP-13; DP-14; ASM-1080 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The four operations, the two events, the two activities, the nine sub-tables and the nine fakes are described | In review |
| In review | Consumer sign-off | The app, infrastructure, operations and test stories accept the document and the fakes | Baselined |
| Baselined | Additive change | A field, an error code or a fake is added without removing one | Baselined |
| Baselined | Breaking change to a provided operation or an event | A path, an element or a type is removed, renamed or retyped | New version |
| Baselined | Breaking change to a consumed operation | An owner removes, renames or retypes an element this contract declares | In review, with that owner |
| Baselined | Drift in a fake | A contract test fails | In review |

The runtime states the contract fixes for the item are PENDING, SENT, RETRY, EXCEPTION and ACKNOWLEDGED, and for the delivery PENDING, RETRYING, DELIVERED and EXCEPTION; they are declared in 12.1 and 12.7 and are not states of this document (TSD P2 v3 T3.2 and T4).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-integration | Owns this document and the nine fakes; tags the baseline |
| Solution architect | Approves a breaking change to a provided operation, to an event or to the manifest |
| The rwb-source-data owner | Owns the freshness, customer and account operations and signs off the shapes this contract consumes |
| The rwb-comms owner | Owns the notice facts behind INT-14 and signs off the shape taken from its document |
| The rwb-document owner | Owns the store and the claim-check read behind the file |
| The rwb-case owner | Owns the route state and the owner task this contract raises |
| The rwb-access owner | Owns the right check behind the four admin operations |
| The rwb-integration app, infrastructure, operations and test stories | Review and accept the parts they consume |
| Data steward | Confirms that no personal data element is declared in an event, a command or an activity input |

The deployment identity that calls the owners' contracts is Not specified in the source documents (GAP-0648; ASM-1070); the document names it "the rwb-integration login (DP-02)" and leaves the name to the operations story.

### 11. Data

The contract declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Outbound item | id, interfaceId, idempotencyKey, payloadRef, caseIds, attemptCount, nextAttemptAt, status, lastError, ownerRole (`outbound_item`) | DF-OPS-168 to DF-OPS-177 |
| Interface row | interfaceId, direction, transport, inboundPath (outbound folder), filePattern, dataProduct, maxAttempts, retryIntervalsMin, ownerRole, alertRole, validFrom, validTo (`interface_config`) | DF-OPS-137 to DF-OPS-148 |
| Delivery record | eventId, consumer, status, attemptCount, nextAttemptAt, lastErrorCode, deliveredAt, taskId (`outbox_delivery`) | DF-OPS-199 to DF-OPS-206 |
| Outbox event | eventType, schemaVersion, caseId, caseSeq, idempotencyKey, payload, actorRef, occurredAt (`outbox_event`) | DF-OPS-190 to DF-OPS-197 |
| Inbox record | consumer, idempotencyKey, eventId, hitCount, lastSeenAt (`processed_event`) | DF-OPS-179 to DF-OPS-183 |
| Idempotency record | idempotencyKey, endpoint, requestHash, response (`idempotency_key`) | DF-OPS-185 to DF-OPS-188 |
| File manifest | fileId, batchId, sha256, recordCount, interfaceId, businessDate, caseIds, idempotencyKey, claim-check link, requesting service | Not specified in the source documents (DOR-RWB-P2-E1007-CON-7) |
| Item status list | PENDING, SENT, RETRY, EXCEPTION, ACKNOWLEDGED (LOV-OUTBOUND-STATUS) | DF-OPS-175 |
| Delivery status list | PENDING, RETRYING, DELIVERED, EXCEPTION (LOV-OUTBOX-DELIVERY) | DF-OPS-201 |
| Decision-record element | decision code, the action (deliver, exception, resend), the item or delivery reference and the freshness, written by the library on `rwb.decision-record.v1` | Not specified in the source documents (DOR-RWB-P2-E1007-CON-7) |

The physical names, lengths and required flags are those of the TSD P2 Integration v3 T3.1 and the BR field IDs DF-OPS-136 to DF-OPS-148 and DF-OPS-168 to DF-OPS-206. The JSON field names of the four responses and the shape of the problem body are Not specified in the source documents (GAP-0648; ASM-1082) and are fixed here; the query parameters of the two list operations are those of TSD P2 v3 T-A.2.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/integration/v1`; owner rwb-integration (P2). Four operations.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/admin/outbound-items` | Lists outbound items by status, interface, from and to; response `OutboundItem[]` of id, interfaceId, status, attemptCount, lastError, caseCount, ownerRole, updatedAt | Platform administration R, scope applied | Not applicable |
| POST | `/admin/outbound-items/{itemId}/resend` | Sends an item in EXCEPTION again: status PENDING, attempt count 0, written to the ACE audit log with the user and the time; response `OutboundItem` | Platform administration U, scope applied | `Idempotency-Key` header; 409 when not in EXCEPTION or the version changed |
| GET | `/admin/outbox/deliveries` | Lists outbox deliveries by status, consumer, eventType, from, to, page and size; response `OutboxDeliveryPage` | Platform administration R, scope applied | Not applicable |
| POST | `/admin/outbox/deliveries/{deliveryId}/resend` | Sends a delivery in EXCEPTION again: status PENDING, attempt count 0; response `OutboxDelivery` | Platform administration U, scope applied | `Idempotency-Key` header; 409 when not in EXCEPTION |

Errors, one RFC 9457 body for all four: 401 no session or no Recovery role (MSG-P4-001); 403 no Platform administration right (MSG-P4-002); 404 unknown item or delivery (MSG-P4-003); 409 not in EXCEPTION or a changed version (MSG-GEN-004); 422 a malformed query; 503 the store or a consumed contract is unavailable (MSG-GEN-006). The four paths are API-P2-001 to API-P2-004 of TSD P2 Integration v3 T-A.1 and the Ownership Map rows owned by P2, re-based on the service base by DP-13. Architecture v5 slide 16 names `GET /interface-runs` and `POST /interface-runs/{id}/retry` instead; that naming is superseded and recorded (GAP-0648; ASM-1076). A later slice narrows the consumer filter of the delivery read and does not re-declare these paths.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the contract |
|---|---|---|---|
| GET | `/api/recovery/source-data/v1/freshness` | P1 rwb-source-data | Whether the ACE batch of the business date is complete; faked with COMPLETE, FAILED at 05:20 and one slow answer |
| GET | `/api/recovery/source-data/v1/customers/{id}` | P1 rwb-source-data | The addressee facts by person key and contact key; faked with one hit, one miss and masking applied by the owner |
| GET | `/api/recovery/source-data/v1/accounts/{id}` | P1 rwb-source-data | The account facts of the INT-25 tape; faked with the 120 synthetic keys of the request |
| GET | Not specified in the source documents (GAP-0648; ASM-1081) | P6 rwb-comms | The notice facts behind INT-14: notice ID, sent date, person key and document ID; faked with 85 notices and one 404 |
| POST | `/api/recovery/document/v1/documents` | P5 rwb-document | Stores the built file and returns the upload link and the document ID |
| GET | `/api/recovery/document/v1/documents/{id}` | P5 rwb-document | Follows the claim-check link of a stored file; faked with one hit and one 404 |
| POST | `/api/recovery/case/v1/cases/{caseId}/actions` | P3 rwb-case | The route-state change and the one owner task; faked with the two route states and the task |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Platform administration R and U check, cached per session |
| POST (ACE Common path) | INT-22 audit and PII logging | ACE Common | The resend record and the personal-data access events |

Every operation is one hop with a 2 s client budget and a breaker per downstream, one GET retry with jitter and no retry on a 4xx (DP-11, ADR-020). The notice read is named by its legacy purpose only — `notice.sent_date` and `notice.person_key` (DF-LEG-019, DF-LEG-030) and `document.storage_ref` (DF-DOC-006) — because Architecture v5 slide 14 gives no notice-fact read to P6 and the legacy story built the file from the notice table in process; its path, query and field names are fixed in the rwb-comms contract (GAP-0648; ASM-1081). `debt_sale_account` appears in no consumed operation: the INT-25 rows travel in the manifest (BR8).

#### 12.3 Events published

| Event type | Topic | Key | Payload elements |
|---|---|---|---|
| `rwb.integration.FileDelivered.v1` | `rwb.integration.events.v1` | caseId | fileId, interfaceId, businessDate, documentId, sha256, recordCount, requesting service |
| `rwb.integration.FileFailed.v1` | `rwb.integration.events.v1` | caseId | fileId, interfaceId, businessDate, attemptCount, lastError code, caseIds, ownerRole |

Both are written to `outbox_event` in the same transaction as the item state change and relayed with the CloudEvents 1.0 envelope in binary mode, retry topics 1 minute, 10 minutes and 1 hour, then `.dlt` with an alert (DP-09; Arch v5 slides 9 and 11). The schema version is carried in `outbox_event.schema_version`; the registry subject is BACKWARD compatible. The shared event `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` is published by the local decision-record library when an item moves to EXCEPTION or is resent; its schema belongs to RWB-P7-E1027-CON and is not restated here (DP-03).

#### 12.4 Events consumed

| Event type | Topic | Owner | Consumer contract |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 | CloudEvents 1.0, key the source and the business date; releases a held request after a failed batch; inbox dedupe on the key; no outbox delivery of its own |

This service is called as a task and not as an event listener for its work (Arch v5 slide 16, "events (none: called as a task)"), so `AceDataReady` is the only subscription. `AceDataLate` is P1's alert to the platform and to the gateway banner and is not consumed here. The requesting flows — a notice, a posting file, a buyer tape — arrive through `deliverFile` and never as an event of this service.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `deliverFile(manifest)` | Activity, provided by P2, called by the requesting services | `rwb-integration` | Input: the manifest of BR6. Output: the item reference and the item status. Typed failures: `FreshnessHold`, `ManifestRefused`, `TargetUnavailable` |
| `receiveFile` | Activity, provided by P2 | `rwb-integration` | The published inbound counterpart; input and output are declared for completeness and no wave-1 flow calls it (BR9) |
| `OutboundFileWorkflow` | Workflow, one execution per interface and business date, workflow ID `<interfaceId>:<businessDate>` | `rwb-integration` | Input: the manifest and the item reference. Output: the last item status |
| `buildOutboundFile` | Activity | `rwb-integration` | Input: the manifest and the item. Output: the file reference, the record count and the sha256 |
| `storeOutboundFile` | Activity | `rwb-integration` | Input: the file reference and the manifest. Output: the document ID and the claim-check link |
| `sendFileOverMft` | Activity | `rwb-integration` | Input: the document ID, the interface and the endpoint reference. Output: the attempt result; idempotent on the fileId |
| `parkItemInException` | Activity | `rwb-integration` | Input: the item, the failure class and the attempt count. Output: status EXCEPTION, `FileFailed` in the outbox and the owner task reference |

The retry policy is the workflow kit's: initial interval 1 s, back-off 2, maximum 3 attempts per activity, with a 4xx of a consumed contract classified as non-retryable and a 5xx or a timeout as retryable (DP-10). The file-level retry ladder is not the activity retry: it is the `max_attempts` and `retry_intervals_min` of the interface row, applied by `OutboundFileWorkflow` as timers (BR11). That `deliverFile` returns at PENDING and lets the workflow carry the ladder is Not specified in the source documents (GAP-0648; ASM-1078).

**Claim-check handoff (GAP-0334).** The built file is stored through `POST /api/recovery/document/v1/documents`: rwb-document creates the document ID and returns the upload link, and the bytes reach Blob through that link. rwb-document issues the claim-check link, a SAS link for one file valid 15 minutes (Arch v5 slide 11). The manifest and the activities carry references and the link, never the bytes. The manifest schema of BR6 is published in the activity contract jar and the AsyncAPI document before the first SIT run of this path.

**File-window trigger (GAP-0334).** The bank Airflow opens the WIN window at 16:00 and the debt-buyer window per lot by calling the requesting service, which calls `deliverFile`. The window is identified by the interface and the business date, and a repeated window call builds no second file. A window that does not start fails the window check of the smoke run, and the runbook entry names the Airflow DAG and the requesting service (RWB-P2-E1007-OPS). The operation Airflow calls on the requesting service and its field names are Not specified in the source documents (GAP-0334).

#### 12.6 Schedules

None. This contract registers no Temporal Schedule. The WIN window at 16:00 and the debt-buyer window per lot are opened by the bank's Airflow, which calls the requesting services and never a `rwb_*` schema (Arch v5 slides 16, 32 and 44; ASM-1074). The outbox relay runs every minute as a platform interval of the library and is not a Schedule of this contract (DP-09). The retry ladder is a workflow timer, not a Schedule (BR11). The window trigger rule is stated in 12.5; its deployment checks belong to RWB-P2-E1007-OPS.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `interface_config` | P2 (rwb_integration) | The outbound interface rows, by version, with direction OUTBOUND only |
| `outbound_item` | P2 (rwb_integration) | One outbound file, its status, attempt count, next attempt, last error, case IDs and manifest reference |
| `job_catalog` | P2 (rwb_integration) | The job catalog read; this contract writes no row in it and the loading of the JOB-10 and JOB-11 rows is Not specified in the source documents (GAP-0648; ASM-1079) |
| `outbox_event` | PLT library, created in `rwb_integration` | The event written in the same transaction as the state change |
| `outbox_delivery` | PLT library, created in `rwb_integration` | One delivery per event and consumer, its attempts and its task |
| `processed_event` | PLT library, created in `rwb_integration` | The inbox: consumer, key, CloudEvents id, hit count |
| `idempotency_key` | PLT library, created in `rwb_integration` | The stored response of the two POST operations, kept 24 hours |
| `decision_record` | PLT library table, created in `rwb_integration` (not an LDM v9 entity) | The local decision record of an exception and of a resend (DP-03) |

No other table is named. `notice` is rwb-comms's, `document` is rwb-document's, `debt_sale_account` is rwb-debtsale's, `recovery_case` and `task` are rwb-case's and `role` is rwb-access's; none appears here as an object of this service (DP-01). The thirty `recovery.v_ace_*` views are rwb-source-data's read surface and this schema holds no grant on `recovery` (BR7). `interface_run` and `interface_signoff` do not exist in the target (FSD P2 v3 A1.6; TSD P2 v3 T3.1).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data WireMock | Freshness COMPLETE and FAILED at 05:20 for 2026-11-10, one slow answer; addressee and address for the 85 synthetic notices; account facts for the 120 synthetic keys | App story, contract tests |
| rwb-comms WireMock | The 85 approved notices of 2026-11-10 with person key, sent date and document ID; one 404 | App story, AC5 |
| rwb-document WireMock | 201 with a document ID and an upload link; the claim-check read by ID; one 404 for the withheld file | App story, AC5 |
| rwb-case WireMock | The route state RETRY_QUEUE and EXCEPTION_QUEUE and one open task for RW-PLATADM; one 404 | App story, AC5 |
| rwb-access WireMock | Authorise granted to RW-PLATADM and refused to RW-CASEOWN with MSG-P4-002 | App story, contract tests |
| rwb-debtsale caller stub | The INT-25 request with 120 synthetic account keys for an awarded lot | App story, AC3 |
| ACE Common audit and PII stub | The resend record accepted, and one refusal for the 503 answer | App story |
| MFT/SFTP edge stub | A receiver that accepts and one that fails three times | App story, AC5 |
| Kafka stubs | One `AceDataReady` for 2026-11-10, a duplicate of it, the event key `EV-10:TRT-0001:v1` twice, one malformed envelope and one eighth type | Contract tests, AC2 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 9 consumed | The four admin operations provided; the P1 freshness, customer and account reads, the P6 notice read, the P5 store and read, the P3 case action, the P4 authorise and the ACE Common audit path consumed; one hop, 2 s timeout |
| Kafka | 2 published, 1 consumed | `FileDelivered` and `FileFailed` on `rwb.integration.events.v1`; `AceDataReady` consumed with inbox dedupe; `DecisionRecorded` published by the library |
| Temporal | 1 workflow, 6 activities | `OutboundFileWorkflow` with four step activities and the provided `deliverFile` and `receiveFile` on queue `rwb-integration` |
| File | 2 party interfaces | INT-14 WIN and INT-25 buyer tape over MFT/SFTP with PGP; INT-19 and INT-20 removed with no target in this service; no data lake and no lake element anywhere in the contract |

### 13. Solution plan

**Deliverables.** `contract/outbound-admin.yaml` (OpenAPI 3.1 of the four admin operations, the problem envelope and the idempotency rule), `contract/integration-events.yaml` (AsyncAPI 3 of `rwb.integration.events.v1` with the CloudEvents envelope, the two types and their payloads), `contract/outbound-activities.yaml` (the `deliverFile` and `receiveFile` activity contract, the manifest, the return and the typed failures), `contract/outbound-consumed.yaml` (the five owner operations as consumed, with the notice-read placeholder), `contract/outbound-tables.md` (the ownership statement of 12.7), and the nine WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_integration`; no other schema is read | none |
| DP-02 | `recovery_svc` login | One login per service, named by the operations story | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | ACE facts through the rwb-source-data contract; no view is read here | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case; the lists stay rows | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library, CloudEvents, the service topic, retry and `.dlt` | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Typed activity and workflow contract on the service queue; timers instead of a scheduler | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with a fake; one hop; 2 s timeout | none |
| DP-16 | `recovery.integration.adapter` | The rwb-integration contract: activities, events, admin operations, manifest | C RWB-P2-E1007-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed; no lake element in any document | none |
| DP-19 | Screen, ace-web | gateway-bff composite route for SCR-09 | H RWB-PLT-N001-CON |

**Build steps**

1. Write the OpenAPI document: the four operations, their query parameters, their response types, their rights, the Idempotency-Key rule, the 409 and the one problem body.
2. Write the AsyncAPI document: the two types, the envelope, the key, the payloads, the retry topics, the `.dlt` rule and the schema subject.
3. Write the activity contract: the two activities, the manifest of BR6, the return element, the typed failures and the retry classification.
4. Write the consumed contracts: the five owner operations, the notice-read placeholder and the 4xx and 5xx degradation rule.
5. Write the table ownership statement and the explicit absence of any ACE view, recovery table, lake element and inbound adapter.
6. Write the versioning and compatibility rule and the drift test between each fake and this document.
7. Build the nine fakes and their fixtures with synthetic keys only.
8. Add the six contract tests of section 16.
9. Tag the baseline and collect the sign-off of the app, infrastructure, operations and test stories.

**Done when.** The five contract files validate in the pipeline, the six contract tests pass, the nine fakes answer every consumed path and every declared error, and the stories of this key have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | An outbound file is held because the ACE batch is not complete | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-004 | A resend on an item or delivery not in EXCEPTION, or on a changed version | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-005 | A resend is accepted | Saved. |
| MSG-GEN-006 | A consumed contract is unavailable, so the attempt is retried | {system} is not available. Your request is queued and will be retried. |
| MSG-P2-001 | An outbound file or an outbox delivery moves to the exception queue after the retry limit | {item} was not delivered to {interface} after {count} attempts. It is in the exception queue. |
| MSG-P4-001 | A call without a session | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A role without the Platform administration right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A resend or a list names an unknown item or delivery | This case is not in your scope. |

The texts are copied unchanged from the legacy story, except MSG-P1-001, MSG-P2-001 and MSG-P4-003, which use the Error and Message Standard v4 wording (CG-ALL-2981; CG-ALL-2982; DOR-RWB-P2-E1007-CON-9). The contract adds no message of its own; a message identifier is carried on every error of the envelope, and a code without an identifier in the source set keeps the §R9 placeholder until the Error and Message Standard names it.

### 15. Screens and states

None in this story. The four provided operations serve SCR-09 Exception queue, whose fields, states and masking belong to RWB-P2-E1007-APP and whose route is RWB-PLT-N001-CON. The contract fixes only the states a screen may show — PENDING, SENT, RETRY, EXCEPTION and ACKNOWLEDGED for an item, PENDING, RETRYING, DELIVERED and EXCEPTION for a delivery — and the resend action with its 409. The held-file and failed-file alerts are alert rules over the held-item series and over `FileFailed`, owned by RWB-P2-E1007-OPS; the legacy alert names `rwb.integration.outbound.held` and `rwb.integration.outbound.failed` are not event names of the target (GAP-0648; ASM-1077). Loading state of SCR-09: as Screen Specifications v1 SCR-09. Empty, error and no-access states of SCR-09: Not specified in the source documents (CG-ALL-2986).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P2-E1007-CON-01 | AC1 | Contract | The four operations on the base with their rights, the Idempotency-Key rule, the 409 and the one problem body; a fifth path or another base fails the review |
| TC-P2-E1007-CON-02 | AC2 | Contract | One message of each of the two types validated against the AsyncAPI document; a malformed envelope, an eighth type and a payload with a personal-data field are refused |
| TC-P2-E1007-CON-03 | AC3 | Component | The manifest of `deliverFile` round-tripped through the contract; the return element; the three typed failures; `receiveFile` called by no flow |
| TC-P2-E1007-CON-04 | AC4 | Contract | The nine sub-tables present; 12.7 names only the P2 tables and the four library objects; no ACE view, no lake element and no Schedule |
| TC-P2-E1007-CON-05 | AC5 | Contract | Each of the nine fakes compared with its element; every declared error answer reachable; one injected drift fails the test |
| TC-P2-E1007-CON-06 | AC6 | NFR | The boundary test finds no cross-schema statement, no ACE view, no foreign key out of `rwb_integration` and no SFTP call outside the transport component; the compatibility check passes on an additive change |
| TC-P2-E1007-CON-07 | AC4 | Contract | Boundary test: each table of 12.7 with its owner and the four library objects; a read or write outside the 12.7 tables fails |
| TC-P2-E1007-CON-08 | AC7, BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13 | Contract | The contract files reviewed rule by rule against the AC7 outcomes; one rule broken on purpose, a lake target or a fifth path, fails the review |
| TC-E1-007-05 | BR9 | NFR | Legacy case "file missing at the cut-off", retired: the contract declares no inbound adapter, no inbound folder listing, no check DQ-057 and no run table `interface_run`; the behaviour is ACE ingestion and the EV-27 AceDataLate alert; the row closes when the ACE ingestion story RWB-ACE-001 publishes its checks |
| TC-E1-007-06 | BR9 | NFR | Legacy case "same file delivered twice", retired: the contract declares no inbound adapter, no inbound folder listing, no check DQ-059 and no run table `interface_run`; the behaviour is ACE ingestion; the row closes when the ACE ingestion story RWB-ACE-001 publishes its checks |

### 17. Guardrails

- No business value in the contract: the attempts, the intervals, the owner role, the alert role and the lists are `interface_config` rows and reference-data rows with the version in force.
- No personal data in an event, a command, an activity input or a fake: identifiers, codes, counts and hashes only, and the claim-check link instead of the file.
- The contract names only rwb-integration's own operations, events and activities as provided; the five consumed services are consumed and are never restated as this service's.
- One REST base, one topic and one task queue per service; a document that names another service's base as provided, or a topic outside `rwb.<short>.events.v1`, fails the review (DP-13, DP-14).
- No ACE view, no recovery table and no lake element appears as an object of this service, and `rwb_integration` holds no grant on `recovery` (DP-01, DP-05, DP-17).
- The envelope, the registry, the inbox, the retry topics and the `.dlt` rule come from the platform library; this story narrows them and never redefines them.
- Every example and fixture is synthetic; no production payload, address or event is copied into a schema or a fake.
- The version stays in the path and a breaking change needs a new version; the compatibility check runs in every build.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-006 | No component calls a system of record directly; source data is read through ACE's views and leaves through ACE's paths and the Workbench outbound adapters | The five consumed services, the manifest and the two events | TC-P2-E1007-CON-02, TC-P2-E1007-CON-03 |
| REQ-DRI-007 | Every outbound file is logged, retried on a defined schedule and raised to a named owner in an exception queue | The four admin operations, the item and delivery states, the exception path of the delivery row | TC-P2-E1007-CON-01, TC-P2-E1007-CON-04 |
| REQ-DRI-008 | Data from other systems reaches the Workbench only through ACE ingestion and the ACE views; the Workbench runs no file load | The absence of any ACE read and the `receiveFile` rule of BR9 | TC-P2-E1007-CON-03, TC-P2-E1007-CON-06 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The outbox and inbox objects of 12.7, the envelope of 12.3 and the `.dlt` rule | TC-P2-E1007-CON-02 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout, claim-check for files | The nine consumed operations with the 2 s budget and the manifest | TC-P2-E1007-CON-03, TC-P2-E1007-CON-06 |

### 19. Out of scope

- The implementation of the builder, the sender, the retry policy, the inbox, the four operations and the workflow (RWB-P2-E1007-APP).
- INT-19, INT-20, JOB-13 and JOB-15: removed with no target in this service; the reporting projection belongs to rwb-reporting and the decision ledger is fed from the shared decision-record topic (DP-17; GAP-1163).
- The MFT/SFTP endpoints, the PGP keys, the key store, the network rules, the staging area and the budgets (RWB-P2-E1007-INF).
- The Helm chart, the values, the topic and queue provisioning, the two Airflow windows, the alerts, the dashboards and the runbook (RWB-P2-E1007-OPS).
- The real cross-service journey of the path against the live owners (RWB-ITG-E1007-ITG).
- The freshness, customer and account operations of rwb-source-data, their columns and their views (RWB-P1-E1015-CON and the P1 stories).
- The notice facts and the WIN letter content (RWB-P6-E1007-APP and RWB-E2-021).
- The document store, its custody and its retention (RWB-P5-E1007-APP and the P5 stories).
- The route state, the owner task and the case action implementation (RWB-P3-E1007-APP).
- The right, the scope and the masking rule implementation (RWB-P4-E1037-CON).
- The field-level completeness of any consumed contract (GAP-0648).
