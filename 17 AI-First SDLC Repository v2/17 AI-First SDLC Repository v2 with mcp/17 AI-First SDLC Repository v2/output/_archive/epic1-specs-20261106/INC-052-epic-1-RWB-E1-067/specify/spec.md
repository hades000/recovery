# Technical Specification — RWB-E1-067 Every Workbench action into the interaction ledger

| Field | Value |
|---|---|
| Story | RWB-E1-067 — Every Workbench action into the interaction ledger |
| Epic / module | E1 / P1 Recovery data engine |
| RUN_ID | `INC-052-epic-1-RWB-E1-067` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (REQ-ILG-002, 005, 007); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 067 Every Workbench action into the interaction ledger v1.md`; FSD P1 A2.18 context; TSD P1 T5.3 |
| Upstream IDs | BRD section: Business Requirements Epic 1, 3.1 and 4; REQ-ILG-002, REQ-ILG-005, REQ-ILG-007; FEAT-ILG-01, FEAT-ILG-04; US-RWB-E1-067; R-UNI-36, R-UNI-40; NFR-026 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen, component, route, label or state. The platform administrator sees failed events on SCR-09 through the existing exception queue; the case owner reads entries through RWB-E1-068. |
| Logic In Scope | `YES` — event subscription, event-to-entry mapping, schema-version check, duplicate rejection and hit count, ordering, retry and exception-queue routing. |
| API In Scope | `NO` — no endpoint or contract change. The listener consumes outbox events and calls the existing `InteractionLedgerWriter`. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `interaction` (write); `processed_event` (new); outbox consumer (RWB-TE-006); exception queue (P3); incident path (RWB-E1-027). |
| New Nodes Required | `YES` — `LedgerEventListener`, `LedgerEventMapper`, `LedgerDuplicateService`, `InteractionDuplicateRepository`, `InteractionDuplicate`. |
| Inherited Existing Behavior | Ledger writer, case sequence and `LOV-LEDGER-EVENT` (RWB-E1-066); outbox delivery and retry (RWB-TE-006); event publishers EV-01, EV-02, EV-04, EV-08, EV-16, EV-19. |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Case creation, allocation, transfer, escalation, document attachment and each decision write a ledger entry as they happen. | SPEC-RWB-E1-067-001, 002 | DIRECT | Six events mapped to six entry types. | COVERED |
| BR2 | Every entry names the system or person that produced it. | SPEC-RWB-E1-067-004 | DIRECT | Actor type and reference from the event header. | COVERED |
| BR3 | The same event with the same key produces one entry, and the repeat is counted. | SPEC-RWB-E1-067-005 | DIRECT | Unique `idempotency_key`; `processed_event.hit_count`. | COVERED |
| BR4 | Events for one case are processed in the order they were written. | SPEC-RWB-E1-067-006 | DIRECT | Outbox per-case ordering; `case_seq` follows delivery order. | COVERED |
| BR5 | A consumer failure retries, then goes to the exception queue with its owner. | SPEC-RWB-E1-067-007 | DIRECT | Three retries; owner RW-PLATADM; incident. | COVERED |
| BR6 | A consumer accepts the current and the previous schema version. | SPEC-RWB-E1-067-003 | DIRECT | Version check before mapping. | COVERED |
| BR7 | Event payloads carry references and codes, no personal data. | SPEC-RWB-E1-067-011 | DIRECT | Entry built from codes and IDs only; no summary. | COVERED |
| AC1 | Six actions produce six entries with `CASE_CREATED`, `CASE_ALLOCATED`, `CASE_TRANSFERRED`, `DOCUMENT_ATTACHED`, `CASE_ESCALATED`, `DECISION_TAKEN`. | SPEC-RWB-E1-067-001, 002 | DIRECT | One listener, one map. | COVERED |
| AC2 | `CASE_ALLOCATED` names source `WORKBENCH`, source reference `P3 case and workflow, EV-02 CaseAllocated` and actor `SY-RULES`; transfer names actor type `USER` and `u-teammgr-03`. | SPEC-RWB-E1-067-004 | DIRECT | Source reference composed from owning module and event. | COVERED |
| AC3 | A repeated `CaseAllocated` with the same key gives one entry and hit count 1. | SPEC-RWB-E1-067-005 | DIRECT | Unique clash caught; hit incremented in a new transaction. | COVERED |
| AC4 | A `CaseTransferred` at schema version 3 is not written; it goes to the exception queue with owner RW-PLATADM and reason. | SPEC-RWB-E1-067-003, 007 | DIRECT | Version 3 rejected when 2 is current and 1 previous. | COVERED |
| AC5 | Every ledger insert fails: four delivery attempts, then the exception queue and `LEDGER_WRITE_FAILED`. | SPEC-RWB-E1-067-007 | DIRECT | Initial attempt plus three retries. | COVERED |
| AC6 | `CASE_CREATED` then `CASE_ALLOCATED` produce `case_seq` 1 then 2. | SPEC-RWB-E1-067-006 | DIRECT | Per-case ordering preserved. | COVERED |
| AC7 | One event on two consumer threads gives one entry and hit count 1. | SPEC-RWB-E1-067-005 | DIRECT | Unique key; one transaction wins. | COVERED |
| AC8 | `DocumentStored` for an unknown case is not written; it goes to the exception queue with reason "case not found". | SPEC-RWB-E1-067-008 | DIRECT | Case existence check before append. | COVERED |
| X1 | The same event arrives twice with the same key. | SPEC-RWB-E1-067-005 | DIRECT | One entry; repeat counted. | COVERED |
| X2 | An event schema version is neither current nor previous. | SPEC-RWB-E1-067-003 | DIRECT | Exception queue; owner RW-PLATADM. | COVERED |
| X3 | The ledger write fails. | SPEC-RWB-E1-067-007 | DIRECT | Retry, exception queue, incident. | COVERED |
| X4 | Events for one case arrive in written order. | SPEC-RWB-E1-067-006 | DIRECT | Entries follow in `case_seq`. | COVERED |
| X5 | The same event reaches two consumer threads. | SPEC-RWB-E1-067-005 | DIRECT | One entry; one hit. | COVERED |
| X6 | An event names a case that does not exist. | SPEC-RWB-E1-067-008 | DIRECT | Exception queue; no entry. | COVERED |

## User story intent interpretation

As a **case owner (RW-CASEOWN)**, I want **every action the Workbench takes on my case written to the ledger when it is taken**, so that **I can read the history without assembling it from four systems**.

The Workbench acts without a person: it creates, allocates, transfers and escalates cases, attaches
documents and records decisions by rule. This story turns each of those events into a ledger entry. It
does not change the event publishers, the ledger writer or the read interface. Duplicate delivery is
expected at least once and is handled by the idempotency key.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | Outbox delivery of EV-01 `CaseCreated`, EV-02 `CaseAllocated`, EV-04 `CaseTransferred`, EV-08 `DecisionRecorded`, EV-16 `DocumentStored`, EV-19 `TimerBreached`. |
| Preconditions | RWB-E1-066 writer, case sequence and event list; RWB-TE-006 outbox with event ID, idempotency key, schema version, occurred time and actor; the six publishing stories exist. |
| Input | Event header and payload; event-to-entry map; current and previous schema version. |
| Output | One `interaction` row per event, or one `processed_event` hit; exception-queue item on failure. |
| Feature flag | `rwb.dataengine.ledger-events`. Off: the listener is not registered and no event is consumed. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `interaction` | `event_code` | Event map | Insert only | Must be in `LOV-LEDGER-EVENT` |
| `interaction` | `case_id` | Event payload | Insert only | Case must exist |
| `interaction` | `occurred_at` | Event header | Insert only | Required |
| `interaction` | `actor_type`, `actor_ref` | Event header | Insert only | `USER` or `SERVICE` |
| `interaction` | `source_system` | Listener | Insert only | `WORKBENCH` |
| `interaction` | `source_ref` | Owning module and event | Insert only | `<module>, <event ID> <event name>` |
| `interaction` | `idempotency_key` | Event header | Insert only | Unique; repeat returns the first entry |
| `interaction` | `decision_log_id` | Event payload for EV-08 | Insert only | Required for `DECISION_TAKEN` |
| `processed_event` | `idempotency_key` | Event header | Insert once | Primary key |
| `processed_event` | `first_interaction_id` | First entry | Insert once | References the first entry |
| `processed_event` | `hit_count` | Repeat count | Increment only | Starts at 1 on the repeat |
| `processed_event` | `last_hit_at` | Repeat time | Update on repeat | Required |

## Status-transition matrix

| Record | From | Event | To | Side effects |
|---|---|---|---|---|
| Event delivery | Pending | Listener accepts and writes | Processed | One `interaction` row; event marked processed for the ledger consumer |
| Event delivery | Pending | Duplicate key | Processed | No entry; `hit_count` incremented |
| Event delivery | Pending | Write fails | Retry | Retried up to three times |
| Event delivery | Retry exhausted | Third retry fails | Exception queue | Owner RW-PLATADM; incident `LEDGER_WRITE_FAILED` |
| Event delivery | Pending | Unknown case or schema version | Exception queue | No entry; reason recorded |

No case status changes. The exception queue state is `EXCEPTION_QUEUE` for the platform team (R-UNI-36).

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Same event twice with the same key | One entry; repeat counted | None |
| X2 | Schema version neither current nor previous | Not written; exception queue owner RW-PLATADM | None (queue item) |
| X3 | Ledger write fails | Three retries; exception queue; incident | MSG-P1-022 in incident detail |
| X4 | Events for one case in written order | Entries follow in `case_seq` | None |
| X5 | Same event on two consumer threads | One entry; one hit | None |
| X6 | Event names an unknown case | Not written; exception queue | None (queue item) |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing interfaces used | Outbox consumer (RWB-TE-006); `InteractionLedgerWriter.append` (RWB-E1-066). |
| Contract delta | None. |
| Backward compatibility | Unchanged; the listener is additive. |
| Authorization | Listener runs as `SY-CASEWF` with Case record C. |
| Error behaviour | 403 MSG-P4-002 if an identity without Case record C calls the writer; failures follow the outbox path. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label change; SCR-09 already shows exception-queue items. | Existing frontend tests remain green; no new frontend test required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-ILG-002, 005, 007; SPEC-RWB-E1-067-001..013 | New listener, mapper, duplicate service, repository and entity. | Positive, negative and error-path tests: six events; schema versions current/previous/unknown; duplicate key; two threads; ordering; retry exhaustion; unknown case; actor mapping; no PII. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `LedgerEventListener` | Listener | Outbox consumer for the six events; version check; calls mapper and writer. |
| `LedgerEventMapper` | Service | Event to `LedgerEntryCommand` using the configured map. |
| `LedgerDuplicateService` | Service | Catches the unique-key clash and increments the hit in a new transaction. |
| `InteractionDuplicateRepository` | Repository | Upserts `processed_event`. |
| `InteractionDuplicate` | Entity | One row per repeated idempotency key. |

Package `recovery.dataengine.ledger.events`. The listener never queries assignment, document or
decision tables; everything it needs is in the event payload.

### Data and migration

New table `processed_event`: `idempotency_key` varchar(120) primary key, `first_interaction_id` uuid not
null, `hit_count` integer not null, `last_hit_at` timestamptz not null, plus the standard columns. It
uses the `interaction` columns added by RWB-E1-066. Migration is forward-only.

### Event map

| Event | Ledger event |
|---|---|
| EV-01 `CaseCreated` | `CASE_CREATED` |
| EV-02 `CaseAllocated` | `CASE_ALLOCATED` |
| EV-04 `CaseTransferred` | `CASE_TRANSFERRED` |
| EV-08 `DecisionRecorded` | `DECISION_TAKEN` (with decision log entry ID) |
| EV-16 `DocumentStored` | `DOCUMENT_ATTACHED` |
| EV-19 `TimerBreached` | `CASE_ESCALATED` |

The map is configuration `rwb.dataengine.ledger.event-map`, not code. Source reference is composed as
`<owning module>, <event ID> <event name>`.

### Processing algorithm

1. Receive the event with its header and payload.
2. Reject a schema version that is neither current nor previous; move to the exception queue.
3. Map the event to `LedgerEntryCommand`; actor from the header; source `WORKBENCH`.
4. Call `InteractionLedgerWriter.append` in the listener transaction.
5. On a unique-key clash for `idempotency_key`, write no entry and increment `hit_count` in a new
   transaction.
6. On a missing case, move to the exception queue with reason "case not found".
7. On other failure, let the outbox retry; after three retries move to the exception queue and raise
   `LEDGER_WRITE_FAILED`.

**Transaction.** The entry insert uses the listener transaction; the duplicate hit is recorded in a new
transaction so it survives the original rollback. The listener publishes no event.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| SY-CASEWF | Case record C; runs the listener | All |
| SY-RULES, SY-OCR, SY-DECLOG | Appear as actors; do not call the writer | — |
| SY-AGENT | Case record R; may not append | — |
| RW-PLATADM | Owns exception-queue items; receives the incident | All |
| RW-CASEOWN | Reads entries through RWB-E1-068 | Own |

### Observability and operations

- Metrics: events consumed per type; entries written; duplicate hits; retries; exception-queue items.
- Alerts: `LEDGER_WRITE_FAILED`; exception-queue growth.
- Audit: `processed_event` records every repeat; the ledger records every action.
- Run book entry under RWB-E1-056.

### Performance

- Per-case ordered delivery; one insert per event.
- Duplicate detection is a primary-key lookup.
- No table scan of assignment, document or decision data.

### Feature flag and rollback

`rwb.dataengine.ledger-events`. Off: the listener is not registered; events remain in the outbox for
the other consumers. Rollback: turn the flag off; `processed_event` remains and is harmless.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-067-01 | AC1, BR1 | System | Six synthetic events for case RW-2026-000301 | Six entries with the six event codes; case, event, time, actor |
| TC-E1-067-02 | AC2, BR2 | System | `CASE_ALLOCATED`, `CASE_TRANSFERRED` | Source `WORKBENCH`; source ref P3/EV-02; actor `SY-RULES`; transfer actor type `USER` |
| TC-E1-067-03 | AC3, BR3 | System | `CaseAllocated` twice with key EV-02-RW-2026-000301-20261201 | One entry; hit count 1 |
| TC-E1-067-04 | AC4, BR6 | System | `CaseTransferred` schema version 3 | No entry; exception queue owner RW-PLATADM; reason recorded |
| TC-E1-067-05 | AC5, BR5 | System | Every insert fails | Four attempts; exception queue; incident |
| TC-E1-067-06 | AC6, BR4 | System | `CaseCreated` then `CaseAllocated` | `case_seq` 1 then 2 |
| TC-E1-067-07 | AC7, BR3 | System | One event on two threads | One entry; hit count 1 |
| TC-E1-067-08 | AC8 | System | `DocumentStored` for unknown case | No entry; exception queue "case not found" |
| TC-E1-067-09 | BR7 | Security | Event payload with a personal field | No personal field written; entry uses codes and IDs |
| TC-E1-067-10 | Access | Security | `SY-AGENT` calls `append()` | 403 MSG-P4-002 |
| TC-E1-067-11 | BR3 | Unit | First key, repeat key, concurrent key | Insert, increment, one winner |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR5; SPEC-007 | How many retries before the exception queue? | Determines the failure path. | Three retries from the outbox settings (NFR-026; DL11); AC5 counts four attempts in all. | RESOLVED | SPEC-007 |
| CLAR-002 | BR1; SPEC-002 | Is the event-to-entry map code or configuration? | Determines change control. | Configuration `rwb.dataengine.ledger.event-map`; story §13. | RESOLVED | SPEC-002 |
| CLAR-003 | BR6; SPEC-003 | Which schema versions are accepted? | Determines rejection. | Current and previous only; story BR6 and AC4. | RESOLVED | SPEC-003 |
| CLAR-004 | BR3; SPEC-005 | Where is the duplicate hit counted? | Determines the table. | `processed_event.hit_count`; story §13 and AC3. | RESOLVED | SPEC-005 |
| CLAR-005 | BR1; SPEC-001 | Are all six events available in E1? | Determines the listener scope. | Yes; the publishing stories are named in story §3. | RESOLVED | SPEC-001 |
| CLAR-006 | BR7; SPEC-011 | May the listener copy a summary from the event? | Determines PII exposure. | No; event payloads carry references and codes only. | RESOLVED | SPEC-011 |

`CLARIFICATION_STATUS: RESOLVED` — all 6 items are answered from the story, the event design or the
outbox settings. No item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New outbox listener and duplicate store; existing ledger writer and event contracts reused; no contract change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: event consumer with no endpoint or screen change]
REQUIREMENT_COVERAGE_SUMMARY: All 7 business rules, 8 acceptance criteria, 6 exception paths and 5 delivery transitions are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
