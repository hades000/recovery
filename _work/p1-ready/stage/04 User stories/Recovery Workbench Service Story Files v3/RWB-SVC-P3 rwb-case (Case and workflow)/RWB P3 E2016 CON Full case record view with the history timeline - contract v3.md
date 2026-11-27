# RWB-P3-E2016-CON Full case record view with the history timeline

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- D-RCV-60 finishing pass: RD-P1-004, RD-P1-064; requests F12-affected-0186.

| Item | Value |
|---|---|
| Story key | RWB-P3-E2016-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-016 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Sizing | Fits within two weeks |
| Patterns applied | DP01, DP03, DP06, DP07, DP11, DP13, DP14, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-012, FR-P3-019, FR-P3-021, FR-P3-023, FR-P3-030) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-004, RD-P1-007, RD-P1-064 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-016 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (13 resolved, 20 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

### 1. Story

As a **tech lead of rwb-case**, I want **the published contract baseline for the case timeline: an OpenAPI 3.1 document for `GET /cases/{caseId}/timeline` with its query, its page and item shapes, its seven type values, its paging bounds and its error mapping, the consumed-operation list of the P7, P5, P6, P1 and P4 contracts with the one-hop 2-second rule, the event facts a timeline item reflects, the nine contract tables and the five contract fakes**, so that **the app story RWB-P3-E2016-APP, the deployment story and the wave 2 integration harness build on Day 1 against one fixed, testable contract instead of waiting for each other**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The timeline is the widest read in the workbench: it merges the records of five owners and it is the screen a new case owner opens first. If the item shape, the type list, the paging bounds and the partial-answer rule are agreed once and faked, the app story builds in parallel with rwb-decision, rwb-document, rwb-comms, rwb-source-data and rwb-access, and a change in any of those contracts is caught in a contract test rather than in an integration window.

The baseline also fixes the naming the checks require: schema `rwb_case`, REST base `/api/recovery/case/v1` (DP-13), task queue `rwb-case` in namespace `rwb-recovery` and Java package Not specified in the source documents (CG-ALL-4256). No topic is declared, because the timeline publishes nothing (DP-14 applies only as a prohibition here). The baseline states one operation and one named view of it, because queue history is the same operation filtered to ASSIGNMENT and TRANSFER, so a consumer cannot drift into a second path for the same answer.

The P1 case-scoped interaction-ledger read is published under RD-P1-007 and RD-P1-064. The rwb-comms case-scoped notice-list Ownership Map row remains open (GAP-0717; ASM-1264).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the schema, the queue and the Java package follow the platform rule rather than a local choice.
- The platform error envelope, the RFC 9457 problem details and the CloudEvents 1.0 envelope are the platform baseline; where this document narrows them it does so explicitly.
- The parameters contract and the reference-data contract of rwb-case are published (RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON), because the source timeout, the page size bounds and the type and reason labels are contracted as rows and not as constants.
- The operations and their owners come from the Ownership Map only; the document never declares another service's operation as provided by rwb-case.
- The legacy contract of RWB-E2-016 is read for the item fields, the error codes and the message texts; no business value is changed by this baseline.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the timeline operation, with the shared components that the other rwb-case reads reuse.
2. Fix the `TimelinePage` and `TimelineItem` components, the seven type values, the twelve item fields and the `unavailableSources[]` entry, with an example for each type.
3. Fix the query: `type`, `from`, `to`, `page` and `size`, with the default and the bounds read from the parameters contract, and document queue history as the same operation with a fixed type filter.
4. State the rights rule per item type, the silent omission rule and the three refusals, and map each HTTP status to its message ID.
5. Publish the consumed-operation list of 12.2 with the one-hop, 2 s and breaker rule, and name the two open points with their register rows.
6. Declare the event facts a timeline item reflects, and state that the timeline publishes no event and holds no projection.
7. Publish the nine contract tables of section 12 and the five contract fakes with their fixtures.
8. Add the contract tests: schema validation, paging bounds, type validation, error mapping, the rights filter and fake drift.
9. Tag the baseline and hand it to RWB-P3-E2016-APP, to RWB-P3-E2016-OPS and to RWB-ITG-E2016-ITG.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A query value is outside its bounds: `size` outside 1 to 200, `page` negative, `type` outside the seven | 422 with the error envelope naming the field and its bounds; no source is called | MSG-GEN-002 | AC2 |
| X2 | `to` is before `from` | 422 with the error envelope naming both fields; no source is called | MSG-GEN-003 | AC2 |
| X3 | The caller holds no Case record R | 403 with the error envelope; the answer is a refusal, never an empty page | MSG-P4-002 | AC3 |
| X4 | The case is unknown or outside the caller's scope | 404 with the error envelope; the two conditions are deliberately one answer | MSG-P4-003 | AC3 |
| X5 | A consumed operation has no agreed path | The document carries the placeholder and the register row; the fake serves the shape only, and the field-level path is settled with the owner before the app story's Done | None | AC5 |
| X6 | A fake drifts from the document | The contract test fails and the merge is blocked | None | AC5 |
| X7 | A field-level definition is missing from the source material | The field is marked with the placeholder and one gap row is carried, and no value is invented | None | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the legacy contract only |
| Negotiable | Item wording in the examples, the filter layout and the summary text are settled with the consumers; the operation, the item fields, the type list, the bounds and the rules are fixed by the target |
| Valuable | Unblocks the app story, the deployment story and the wave 2 harness on Day 1, and gives the five upstream owners one document to build their fakes from |
| Estimable | One document, one component set, one operation with a named view, nine contract tables, five fakes and six contract tests |
| Small | Fits one iteration with the contract tests |
| Testable | Every criterion is tested against the artefact and the fakes, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Case timeline contract baseline for rwb-case

  Background:
    Given the service naming rule of the platform library is in force
    Given the base of rwb-case is /api/recovery/case/v1 and its login is its own (DP-02)

  Scenario: AC1 The document describes the timeline operation and its shapes (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-case is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /cases/{caseId}/timeline on the base /api/recovery/case/v1 with the owner rwb-case
    Then the TimelinePage component declares items, page, size, total and unavailableSources
    Then the TimelineItem component declares at, type, summary, by, reference, reasonCode, fromQueueCode, toQueueCode and ruleId
    Then the document states that queue history is the same operation with type ASSIGNMENT and TRANSFER and declares no second path for it

  Scenario: AC2 The query, the type list and the bounds are in the contract (new, D-RCV-60)
    Given the document declares the query type, from, to, page and size
    When a consumer reads the parameter definitions
    Then type lists exactly DECISION, ASSIGNMENT, TRANSFER, INTERACTION, NOTICE, DOCUMENT and TIMER
    Then page defaults to 0 and size defaults to 50 with a minimum of 1 and a maximum of 200, and both defaults are named as parameter rows of the parameters contract
    Then a size outside 1 to 200, a negative page or an unknown type is refused with 422 and MSG-GEN-002
    Then a to date before the from date is refused with 422 and MSG-GEN-003
    Then no rule of the document fixes a page size or a timeout as a literal

  Scenario: AC3 The rights rule per item type and the refusals are stated (new, D-RCV-60)
    Given the document declares the operation under Case record R with the scope applied
    When a consumer reads the access section
    Then a decision item requires Decision log R, a document item requires Documents R and a notice item requires Litigation R
    Then an item type the caller has no right to read is left out of the answer, the answer is 200 and no other item is missing
    Then a caller without Case record R is refused with 403 and MSG-P4-002, and an unknown or out-of-scope case is 404 with MSG-P4-003
    Then the 401, 403, 404, 422 and 503 responses are declared for the operation

  Scenario: AC4 A slow or missing source is part of the answer, not an error (new, D-RCV-60)
    Given the document declares unavailableSources as a list of entries with system and messageId
    When a consumed source does not answer inside the 2 s budget or its breaker is open
    Then the operation still answers 200 with the remaining items and one entry per missing source carrying MSG-GEN-006
    Then the document states one hop, a 2 s timeout and a breaker per downstream for every consumed operation
    Then the document states that the timeline writes nothing, publishes nothing and holds no projection

  Scenario: AC5 The consumed operations and the five fakes match the document (new, D-RCV-60)
    Given the contract section of this story
    When the consumed operations of 12.2 are reviewed against the Ownership Map
    Then every consumed operation names its owner from the map and its one-hop 2 s budget
    Then the two operations without an agreed path carry their register rows and a fake that serves the shape only
    Then the five fakes answer the paths and payloads of 12.2 and the contract tests fail on any drift
    Then no operation of another service is declared as provided by rwb-case

  Scenario: AC6 The nine contract tables and the event facts are complete (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map
    Then 12.3 is None and no topic is declared for the timeline
    Then 12.4 names DecisionRecorded, DeviationRaised, DeviationCleared, PaymentMissed and TreatmentBooked as the facts that create timeline items
    Then 12.7 names recovery_case, assignment, queue and timer and never the interaction table
    Then the document states that a contact summary is masked by role before it is returned

  Scenario: AC7 Each business rule BR1 to BR13 is traced to a criterion or a guardrail test (new, D-RCV-60)
    Given the business rules of section 8
    When each rule is traced to the criterion or the test that holds it
    Then each of BR1 to BR13 names an AC and a test case, or is an architecture constraint held by TC-P3-E2016-CON-08
    Then no rule of section 8 is left without a criterion or a test
```

These six criteria test the artefact only. They restate no legacy criterion of RWB-E2-016: the eleven legacy criteria belong to RWB-P3-E2016-APP and their cross-service copies to RWB-ITG-E2016-ITG.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | One REST base per service: `/api/recovery/case/v1`; the document never declares another service's base | DP-13; Architecture v5 slide 41 | AC1; TC-P3-E2016-CON-01 |
| BR2 | The timeline publishes nothing, so no topic and no event name is declared for it; a legacy `rwb.p3.` or `rwb.casewf.` name never appears | DP-14; Architecture v5 slide 42 | AC6; TC-P3-E2016-CON-06 |
| BR3 | One operation serves the timeline and the queue history; the queue history is a named view with a fixed type filter, not a second path | Legacy contract; REQ-WKM-008 | AC1; TC-P3-E2016-CON-01 |
| BR4 | The item fields are fixed at twelve: `at`, `type`, `summary`, `by`, `reference`, `reasonCode`, `fromQueueCode`, `toQueueCode`, `ruleId`, and with `page`, `size` and `total` on the page | Legacy contract; RWB-P3-E2016-APP §12.1 | AC1; TC-P3-E2016-CON-01 |
| BR5 | The seven type values are a list value of the reference data with a version in force; they are never a Java enum and never a literal in the document | DP-07; LOV types | AC2; TC-P3-E2016-CON-02 |
| BR6 | `page` starts at 0, `size` starts at 50 and is limited to 1 to 200; the three numbers are parameter rows read through the parameters contract | DP-06; legacy contract | AC2; TC-P3-E2016-CON-02 |
| BR7 | The rights rule is per item type: Decision log R for a decision item, Documents R for a document item, Litigation R for a notice item, and Case record R for the operation itself | CTL-09; roles.txt Permissions | AC3; TC-P3-E2016-CON-03 |
| BR8 | An item type the caller may not read is omitted silently; the document states the omission so a consumer never reads an empty list as a failure | BR7; legacy AC5 | AC3; TC-P3-E2016-CON-03 |
| BR9 | A source that does not answer is an `unavailableSources[]` entry with MSG-GEN-006 on a 200 answer, never a 5xx of the timeline | NFR-008; MSG-GEN-006 | AC4; TC-P3-E2016-CON-04 |
| BR10 | Every consumed operation is one hop with a 2 s timeout and a breaker per downstream; a chain deeper than one is a contract defect | DP-11; ADR-020 | AC4, AC5; TC-P3-E2016-CON-04, TC-P3-E2016-CON-05 |
| BR11 | Error responses use one envelope and one message ID per condition; the business texts are copied unchanged from the legacy story | Architecture v5 platform baseline; Template and Rules §R7.2 s14 | AC3; TC-P3-E2016-CON-03 |
| BR12 | The contract names only rwb-case tables; `interaction` is another service's table and is documented as consumed, never as owned | DP-01; DP-18; ASM-0067 | AC5, AC6; TC-P3-E2016-CON-06, TC-P3-E2016-CON-07 |
| BR13 | The document fixes shapes and no business value: no threshold, no label text, no reason code and no timeout is written as a literal | Template and Rules §R7.2 s17 | AC6; TC-P3-E2016-CON-06 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operation, the two component shapes and the nine tables are described | In review |
| In review | Consumer sign-off | The app story, the deployment story and the harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1, for example a new item type | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, or an owner-side path changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | An open point closes | The interaction-ledger path or the notice-list row is agreed and published | Baselined, document amended within major version 1 |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-case | Owns the document, the component set and the five fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Consuming teams: the app story, the deployment story, the wave 2 harness and the owners of the P1, P4, P5, P6 and P7 contracts | Review and sign off the parts they consume, and publish the fakes from their own documents |
| Platform library owner | Owns the error envelope, the RFC 9457 shape and the naming rule this document reuses |
| Data steward | Confirms that no personal data field is declared in an item and that a contact summary is masked before it is returned |

The per-service login name behind the security scheme is Not specified in the source documents (GAP-0675; ASM-1222); the document names it "the rwb-case login (DP-02)".

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| TimelinePage | `items[]` of TimelineItem, `page` (integer), `size` (integer), `total` (integer), `unavailableSources[]` of `system` and `messageId` | Not specified in the source documents (DOR-RWB-P3-E2016-CON-7) |
| TimelineItem | `at` (date-time), `type` (one of the seven list values), `summary` (built from codes and labels, masked for a contact), `by` (the actor reference), `reference` (the ID of the source item), `reasonCode`, `fromQueueCode`, `toQueueCode`, `ruleId` | Not specified in the source documents (DOR-RWB-P3-E2016-CON-7) |
| Queue-history view | The same item with `type` in ASSIGNMENT and TRANSFER, carrying from and to queue, from and to owner, `reasonCode` and `ruleId` | Not specified in the source documents (DOR-RWB-P3-E2016-CON-7) |
| Case sources | `recovery_case` (DF-CAS-001, DF-CAS-011), `assignment` (DF-WRK-010, DF-WRK-012 to DF-WRK-016, DF-WRK-039, DF-WRK-040), `queue` (DF-WRK-002), `timer` (DF-WRK-030, DF-WRK-031, DF-WRK-035) | Not specified in the source documents (DOR-RWB-P3-E2016-CON-7) |
| Consumed sources | `decision_log_entry` (DF-DEC-001, DF-DEC-003, DF-DEC-004, DF-DEC-012, DF-DEC-016) through P7; `document` (DF-DOC-001, DF-DOC-004, DF-DOC-005) through P5; `notice` (DF-LEG-015, DF-LEG-018, DF-LEG-019, DF-LEG-022) through P6; `interaction` (DF-INT-002, DF-INT-004 to DF-INT-011) through P1 | Not specified in the source documents (DOR-RWB-P3-E2016-CON-7) |
| No personal data | No name, address, identity number or contact point is a property of an item; a contact summary is masked by role before it is returned (CTL-11, DL26) | Not specified in the source documents (DOR-RWB-P3-E2016-CON-7) |

The field names above are fixed by this baseline. The physical types and lengths of a `TimelineItem` property and the summary template per type are settled with the consumers at the baseline review; this story fixes no value and invents none. The summary wording of a document item is Not specified in the source documents (GAP-1061). The merged list is in occurred-time order with case sequence as the tie-break; the page order of the screen follows the case timeline contract (ASM-B2-P3-010-2).

The case status history is Not specified in the source documents (GAP-2210).

Open decisions apply to this baseline and stay open. DL10 (assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863) and DL26 (assumptions ASM-0247, ASM-0264, ASM-0275 and ASM-0355) are open; the baseline applies each assumption as stated and decides neither.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-case (P3); base `/api/recovery/case/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| GET | `/cases/{caseId}/timeline` | `TimelinePage`; query `type` (comma separated, the seven values), `from` (date), `to` (date), `page` (integer, default 0), `size` (integer, default 50, 1 to 200) | Case record R, scope applied; item types filtered by Decision log R, Documents R and Litigation R |

The queue history is documented as the same operation with `type=ASSIGNMENT,TRANSFER`; the document gives it a section of its own and no second path (BR3).

This contract provides the case timeline and consumes the P1 ledger read. rwb-source-data owns the ledger and applies masking to summary.

The interaction read the timeline consumes has the shape TSD P3 v3 gives API-P3-014: the query `from`, `to`, `page` and `size`, and per entry `occurredAt`, `channel`, `direction`, `contactResult` and `summary`, with the summary masked by role. That shape is declared as consumed in 12.2 with its budget, and it is superseded by the P1 contract wherever the two differ, because the ledger is P1's.

#### 12.2 REST operations consumed

| Method | Path | Owner | Documented use | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | The ledger entries of a case in the date range | One hop, 2 s, breaker |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | One ledger entry, the reference a decision item carries | One hop, 2 s, breaker |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document | The document metadata of a case in the date range | One hop, 2 s, breaker |
| GET | `/api/recovery/comms/v1/cases/{caseId}/notices` | P6 rwb-comms | The case-scoped notice list; Architecture v5 slide 17 names it and the Ownership Map has no row for it (GAP-0717; ASM-1264) | One hop, 2 s, breaker |
| GET | `/api/recovery/comms/v1/notices/{noticeId}` | P6 rwb-comms | One notice by ID | One hop, 2 s, breaker |
| GET | /api/recovery/source-data/v1/cases/{caseId}/interactions | P1 rwb-source-data, RWB-P1-E1066-CON 5.1.0 | Ledger entries for the contact items, using the case UUID and the provider’s paging and role-masked summary | One hop, 2 s, breaker |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Case record R, the scope and the item-type rights, cached | One hop, 2 s, breaker |
| GET | `/api/recovery/access/v1/masking-policies` | P4 rwb-access | The masking policy of the caller's role; the mask is applied by the ACE common masking path | One hop, 2 s, cached |

The masking path is the operation Architecture v5 slide 14 gives rwb-access (`/masking-policies`); the Ownership Map API section has no row for it, so the document takes the path from that slide and confirms it in the rwb-access contract baseline (RWB-P4-E1037-CON).

The contract version this story builds against is `/v1` (path version); the contract yaml version is Not specified in the source documents (DOR-RWB-P3-E2016-CON-23).

#### 12.3 Events published

None. The timeline writes no row and raises no event, so the contract declares no topic, no event type and no outbox row for it. A consumer must not expect a `rwb.case.*` type for a read of the history, and the six rwb-case event types of the service contract are unchanged by this baseline.

#### 12.4 Events consumed

| Event | Topic | Owner of the type | What it declares |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7; every service writes its own record | The ledger link a decision item carries: the record reference, the rule ID, the rule version, the final call and the decided time |
| `rwb.deviation.DeviationRaised.v1` (EV-06) | `rwb.deviation.events.v1` | S8 | A pause fact that becomes a timer item and a decision item on the case |
| `rwb.deviation.DeviationCleared.v1` (EV-07) | `rwb.deviation.events.v1` | S8 | The end of the pause, which becomes a later timer item |
| `rwb.payment.PaymentMissed.v1` (EV-12) | `rwb.payment.events.v1` | P8 | A missed payment that becomes an interaction item, a timer item and a decision item |
| `rwb.payment.TreatmentBooked.v1` (EV-11) | `rwb.payment.events.v1` | P8 | A booking that becomes an interaction item and a decision item |

These five types are the facts that create a timeline item; they reach rwb-case through the case router of the stories that move the case, and the timeline itself consumes none of them, because it reads the resulting state instead of a projection. The last four are declared here so that the harness and a consumer know which facts must appear as items; the first is the ledger link of every decision item.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| CaseWorkflow | Workflow, parent, one per case, workflow ID = case ID | `rwb-case` | No input or output schema is added by this baseline: the workflow writes the `assignment` and `timer` rows the timeline reads through its own activities, and the timeline starts no workflow and adds no activity |

#### 12.6 Schedules

None. The timeline is answered inside the request, and the legacy five-minute timer check (JOB-05) is retired in favour of durable timers inside the workflow (Architecture v5 slide 44), so the contract declares no Schedule and no Quartz row.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| recovery_case | P3 (rwb_case) | Case ID and team of the answer |
| assignment | P3 (rwb_case) | The assignment and transfer items with queue, reason, reason code and rule ID |
| queue | P3 (rwb_case) | The queue code of a move |
| timer | P3 (rwb_case) | The timer items with type, start and status |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | The library objects of the schema; the timeline writes none of them |

`interaction` is never named as a table of this contract: it is owned by rwb-source-data under ASM-0067 and DP-18 and is read through the P1 contract (BR12). No other table is named and no foreign key crosses a schema.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data WireMock | The case interaction-ledger entries with channel, direction, contact result and a summary that must come back masked; an empty answer; a delay beyond 2 s; the shape served without an agreed path | App story, harness, contract tests |
| rwb-document WireMock | The case document list with type and source; an empty answer; a delay beyond 2 s | App story, harness, contract tests |
| rwb-comms WireMock | The case notice list and the notice by ID, with type, sent date and delivery status; an empty answer | App story, harness, contract tests |
| rwb-decision WireMock | The ledger by case with entry IDs and decided times; one entry by ID; an empty answer | App story, harness, contract tests |
| rwb-access WireMock | `POST /authorise` with a granted answer for all four rights, a granted answer without Decision log R and without Litigation R, a refusal without Case record R, a refusal outside the scope; the masking policy of a role | App story, harness, contract tests |

Each fake is published from the same document and replaced by the real service as it lands, contract by contract; a drift between a fake and the document fails the build.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 8 consumed | The timeline operation provided with the queue-history view; the P7 ledger by case and by entry, the P5 document list, the P6 notice list and notice, the P1 ledger read and the P4 authorise and masking policy consumed; one hop, 2 s, breaker |
| Kafka | None published, five types declared as the facts of an item | `rwb.decision.DecisionRecorded.v1` for the ledger link and the four facts that create items; the timeline itself consumes none |
| Temporal | One workflow referenced, none added | CaseWorkflow writes the assignment and timer rows; the timeline starts nothing |
| File | None | No document content is part of the contract; the P5 metadata is the only document fact |

### 13. Solution plan

**Deliverables.** `openapi/rwb-case-v1-timeline.yaml` (the operation and components, merged into the service document), the queue-history section of the same file, the `contract/timeline-examples/` set with one example per type, the five WireMock mapping sets and the contract README with the paging, rights and partial-answer rules.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the item's reference is the record reference | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library; no topic for a read | H RWB-PLT-E1047-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform dependencies of this table are held by the platform CON stories and are not repeated in the metadata rows, which are all None by the Day-1 rule.

**Build steps**

1. OpenAPI skeleton with the base, the security scheme, the error responses and the shared components; schema lint in the pipeline.
2. `TimelinePage`, `TimelineItem` and the `unavailableSources[]` entry, with an example for each of the seven types and a masked contact example.
3. The query definitions, the default and bounds from the parameter rows, and the queue-history section.
4. The access section: the four rights, the silent omission rule, the 401, 403, 404, 422 and 503 mapping and the message IDs.
5. The consumed-operation list with the budget, the two register rows and the note on the masking path.
6. The five fakes and their fixtures, including the delayed and the empty answers.
7. The six contract tests, including a drift test that compares each fake with the document and a bounds test that reads the parameter defaults.
8. Baseline tag, the sign-off note of the app, deployment and harness stories, and the handover of the remaining notice-read point to the P6 owner.

**Done when.** The document validates in the pipeline, the six contract tests pass, the five fakes answer every consumed path or its placeholder, and the app, deployment and harness stories have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-019 | No item matches the filter (the screen text of an empty page with total 0) | Nothing on this case matches the filter. |
| MSG-GEN-006 | A source module does not answer in time | {system} is not available. Try again in a few minutes. |
| MSG-GEN-003 | Date to is before date from | {field} cannot be before {other}. |
| MSG-GEN-002 | Page size outside 1 to 200, a negative page, or an unknown type | {field} must be between {min} and {max}. |
| MSG-P4-002 | A role without Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the caller's scope or unknown | This case is not in your scope. |

The message IDs are contract elements; the text is the agreed text taken from the legacy story where the message already existed, and no new business message is invented by this baseline. For MSG-GEN-006 the {system} value is documented per source so a consumer can map it, and Thai text follows DL10.

### 15. Screens and states

The contract serves SCR-04 Case timeline in its Loading and Filtered states and the queue-history tab on the same screen, and it supplies the timeline section of SCR-03 Case record in its Loading state. The Empty, Error and No access states of SCR-03 and SCR-04 are Not specified in the source documents (CG-ALL-4258, CG-ALL-4259). All of them are served by the gateway-bff composite route (DP-19), owned by RWB-PLT-N001-CON, which calls rwb-case and the other owners in parallel and merges the answers; the document fixes the case side of that merge and no screen field list.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E2016-CON-01 | AC1 | Contract | The document validates; the operation, the two components and the queue-history section are present |
| TC-P3-E2016-CON-02 | AC2 | Contract | The seven types, the default page and size, and the 422 answers for size, page, type and the date pair |
| TC-P3-E2016-CON-03 | AC3 | Contract | The four rights, the silent omission rule and the 401, 403, 404, 422 and 503 responses |
| TC-P3-E2016-CON-04 | AC4 | Contract | The `unavailableSources[]` entry with MSG-GEN-006, the 200 answer, the one-hop 2 s rule and the no-write statement |
| TC-P3-E2016-CON-05 | AC5 | Component | The eight consumed rows against the map, the two placeholder rows and the five fakes |
| TC-P3-E2016-CON-06 | AC6 | Component | The nine tables, 12.3 None, the five event types of 12.4 and the table list of 12.7 without `interaction` |
| TC-P3-E2016-CON-07 | AC6 | Component | Boundary: only the five owned tables of 12.7, the library objects of the schema, and no foreign key across a schema |
| TC-P3-E2016-CON-08 | AC7 | Boundary | Guardrail: each rule BR1 to BR13 of section 8 names its criterion or test, or is held by this check |

The eight cases test the artefact and the fakes. The legacy test cases TC-E2-016-01 to TC-E2-016-12 stay with RWB-P3-E2016-APP, which owns the legacy criteria they cover, and their integration copies with RWB-ITG-E2016-ITG.

### 17. Guardrails

- No business value in the document: the type list, the labels, the reason codes, the timeout and the page size bounds are rows and parameters, and an example never fixes one.
- No personal data in a component, an example or a fake: IDs, codes, dates and amounts only, and a contact summary appears only in its masked form.
- The contract names only rwb-case tables and only operations owned by rwb-case; another service's operation is documented as consumed, never as provided (DP-01).
- One base per service and no topic for a read: a document that names another base, or a `rwb.p3.` or `rwb.casewf.` topic, fails the review (DP-13, DP-14).
- Every example is synthetic; no production payload is copied into a schema or a fake.
- The error envelope, the problem-details shape and the naming rule come from the platform library; this story narrows them but never redefines them.
- An open point is written as a register row and a placeholder, never guessed into a path.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-WKM-008 | Queue and transfer history visible on the case | The queue-history view of the operation, `reasonCode`, `fromQueueCode`, `toQueueCode`, `ruleId` | TC-P3-E2016-CON-01, TC-P3-E2016-CON-02 |
| REQ-OCC-008 | History timeline of every state change, transfer, contact, document and decision | The `type` list, the item fields and the four consumed contracts of 12.2 | TC-P3-E2016-CON-01, TC-P3-E2016-CON-05 |
| REQ-CWC-016 | Every allocation, assignment, transfer and timer event is logged with the rule ID and the rule version | `ruleId` on an assignment and a transfer item, and the rule ID of a `TimerBreached` fact | TC-P3-E2016-CON-01, TC-P3-E2016-CON-06 |
| REQ-DRI-002 | The decision log is append only; a correction is a new record | The `reference` of a decision item and the DecisionRecorded fact of 12.4 | TC-P3-E2016-CON-06 |
| REQ-WKM-014 | The next action is visible on the case record and in every queue view | None (out of scope, section 19) | None |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The budget column of 12.2 and BR10 | TC-P3-E2016-CON-04, TC-P3-E2016-CON-05 |

### 19. Out of scope

- The implementation of the timeline, the rights filter, the paging, the merge and the queue history (RWB-P3-E2016-APP).
- The deployment, the Helm values, the dashboards and the runbook (RWB-P3-E2016-OPS).
- The cross-service journey and its evidence (RWB-ITG-E2016-ITG).
- The contracts of rwb-decision, rwb-document, rwb-comms, rwb-source-data and rwb-access: consumed and faked here, never defined.
- The gateway-bff composite route and the screen model (RWB-PLT-N001-CON).
- The interaction-ledger API is provided by rwb-source-data (RD-P1-007, RD-P1-064).
- The document metadata itself and the document content (RWB-P5-E2016-APP and the P5 stories).
- The field-level types of a `TimelineItem` property and the summary template per type, settled with the consumers at the baseline review.
