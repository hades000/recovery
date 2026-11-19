# Technical Specification — RWB-E1-066 Interaction ledger store and writer

| Field | Value |
|---|---|
| Story | RWB-E1-066 — Interaction ledger store and writer |
| Epic / module | E1 / P1 Recovery data engine |
| RUN_ID | `INC-046-epic-1-RWB-E1-066` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (REQ-ILG-001, 002, 004, 008); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 066 Interaction ledger store and writer v1.md`; FSD P1 A2.14/A2.18 context; TSD P1 T3.1, T5.2 |
| Upstream IDs | BRD section: Business Requirements Epic 1, 3.1 and 4; REQ-ILG-001, REQ-ILG-002, REQ-ILG-004, REQ-ILG-008; FEAT-ILG-01, FEAT-ILG-02, FEAT-ILG-05; US-RWB-E1-066; R-UNI-24; CTL-06; NFR-070, NFR-077 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — the story adds no screen, component, route, label or state. SCR-03 reads entries through RWB-E1-068; the failed-write message is displayed by the existing caller. |
| Logic In Scope | `YES` — validation, case sequencing, append-only insert, idempotency, transaction propagation, incident on failure. |
| API In Scope | `NO` — no new or changed contract. The story supplies the writer behind the existing `POST /api/recovery/v1/cases/{caseId}/interactions` (API-P3-015). |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `interaction` (extended); `recovery_case` (read); `decision_log_entry` (read by ID); `outbox`/incident path of RWB-E1-027 (existing). |
| New Nodes Required | `YES` — `InteractionLedgerWriter`, `LedgerWriteService`, `InteractionRepository`, `Interaction` entity; P3 `InteractionsHandler` delegates to the writer. |
| Inherited Existing Behavior | Case record and case numbers (RWB-E1-018); decision log writer and incident recorder (RWB-E1-027); `interaction` table and `tr_interaction_append_only` (RWB-E1-001); reference data list loader (RWB-E1-043). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | One ledger holds every interaction on a case; no other record is the authoritative history. | SPEC-RWB-E1-066-001, 002 | DIRECT | `interaction` is the store; all recording paths call `append()`. | COVERED |
| BR2 | Every entry carries case, event, time, actor and source. | SPEC-RWB-E1-066-003 | DIRECT | Required fields validated before insert. | COVERED |
| BR3 | An offer, promise, payment or hand-over is recorded on the interaction it was made in. | SPEC-RWB-E1-066-003, 008 | DIRECT | Promise fields on the entry; decision link where a decision. | COVERED |
| BR4 | Entries are append only; a correction is a new entry naming the original. | SPEC-RWB-E1-066-001, 011 | DIRECT | Trigger retained; `corrects_entry_id`; no update/delete method. | COVERED |
| BR5 | A ledger write that fails stops the action and raises an incident; no entry is discarded. | SPEC-RWB-E1-066-007 | DIRECT | Rollback; `LEDGER_WRITE_FAILED`; 503 MSG-P1-022. | COVERED |
| BR6 | The ledger records what happened; the decision log records why; a decision entry links the two. | SPEC-RWB-E1-066-008 | DIRECT | `decision_log_id`; no rule/version/inputs copied. | COVERED |
| BR7 | Entries of one case carry a gap-free sequence. | SPEC-RWB-E1-066-004 | DIRECT | Advisory lock + `max(case_seq) + 1`; unique (`case_id`, `case_seq`). | COVERED |
| AC1 | An outbound call writes case_seq 7 with event, time, actor, channel, direction, promise and source `WORKBENCH`. | SPEC-RWB-E1-066-002, 003, 004 | DIRECT | Writer maps the command; sequence from the case lock. | COVERED |
| AC2 | Six entries read in one sequence ordered by occurred time; case_seq 1–6 with no gap. | SPEC-RWB-E1-066-004, 009 | DIRECT | Sequence assignment and read index. | COVERED |
| AC3 | The decision log holds rule/version/inputs/approver; the ledger entry holds event, time, actor and decision ID only. | SPEC-RWB-E1-066-008 | DIRECT | Decision details stay in P7; only the ID is stored. | COVERED |
| AC4 | A failed insert returns 503 MSG-P1-022, leaves 6 entries, saves no contact and raises `LEDGER_WRITE_FAILED`. | SPEC-RWB-E1-066-006, 007 | DIRECT | `MANDATORY` propagation; incident recorder. | COVERED |
| AC5 | `append()` with no event code is refused with MSG-GEN-001 and writes nothing. | SPEC-RWB-E1-066-003 | DIRECT | Bean validation on the command. | COVERED |
| AC6 | Two simultaneous appends produce case_seq 7 and 8 with no gap or repeat. | SPEC-RWB-E1-066-004 | DIRECT | `pg_advisory_xact_lock`; retry once on unique clash. | COVERED |
| AC7 | An unknown case returns 404 MSG-P4-003 and writes no entry. | SPEC-RWB-E1-066-003 | DIRECT | Case existence check before insert. | COVERED |
| AC8 | UPDATE or DELETE is refused; a correction is a new `CORRECTION` entry naming case_seq 3. | SPEC-RWB-E1-066-001, 011 | DIRECT | Database trigger; `corrects_entry_id`. | COVERED |
| X1 | The ledger cannot be written. | SPEC-RWB-E1-066-007 | DIRECT | Rollback, 503, incident. | COVERED |
| X2 | A required value is missing. | SPEC-RWB-E1-066-003 | DIRECT | 422 MSG-GEN-001. | COVERED |
| X3 | Two entries for one case at the same moment. | SPEC-RWB-E1-066-004 | DIRECT | Consecutive case_seq. | COVERED |
| X4 | The case does not exist or is out of scope. | SPEC-RWB-E1-066-003 | DIRECT | 404 MSG-P4-003. | COVERED |
| X5 | Any change or delete of an entry. | SPEC-RWB-E1-066-001, 011 | DIRECT | Trigger refusal; correction entry. | COVERED |

## User story intent interpretation

As a **case owner (RW-CASEOWN)**, I want **every contact, letter, promise, payment and hand-over on the case written to one ledger when it is recorded**, so that **the history of the case is never assembled after the fact**.

This is the store and writer story. It makes the ledger the single authoritative history and gives every
recording path one published interface. It does not build the timeline view or the read filters; those
are RWB-E1-068. The decision log remains the record of why the system acted; the ledger records what
happened with the customer and points at the decision entry.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | A P3 handler records an interaction (`POST /cases/{caseId}/interactions`), or a load/notice path calls `append()` in its own transaction. |
| Preconditions | `recovery_case` exists (RWB-E1-018); decision log writer and incident path exist (RWB-E1-027); `interaction` table and `tr_interaction_append_only` exist (RWB-E1-001); `LOV-LEDGER-EVENT` loaded. |
| Input | `LedgerEntryCommand`: case ID, party ID, event code, occurred time, actor type and reference, source system and reference, channel, direction, action code, contact result, promise amount and date, summary, decision log entry ID, correction ID, idempotency key. |
| Output | `LedgerEntryRef` (entry ID, case_seq); one `interaction` row; incident on failure. |
| Feature flag | `rwb.dataengine.ledger-writer`. Off: the P3 handler keeps its prior path and no ledger entry is written. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `interaction` | `case_id` | Command | Insert only | Must exist in `recovery_case` |
| `interaction` | `event_code` | Command | Insert only | Required; must be in `LOV-LEDGER-EVENT` |
| `interaction` | `occurred_at` | Command | Insert only | Required; timestamptz with offset |
| `interaction` | `actor_type`, `actor_ref` | Command | Insert only | Required; `USER` or `SERVICE` with the identity reference |
| `interaction` | `source_system`, `source_ref` | Command | Insert only | Required; `WORKBENCH`, `EFS` or `ALS` and the source reference |
| `interaction` | `case_seq` | Assigned by writer | Insert only | Required; unique per case; gap-free |
| `interaction` | `idempotency_key` | Command | Insert only | Optional but unique when present; repeat returns the first entry |
| `interaction` | `channel`, `direction` | Command | Insert only | Nullable after this story; required for contact events |
| `interaction` | `promise_amount`, `promise_date` | Command | Insert only | Optional; recorded on the interaction where made |
| `interaction` | `decision_log_id` | Command | Insert only | Optional; set for `DECISION_TAKEN` |
| `interaction` | `corrects_entry_id` | Command | Insert only | Optional; set for `CORRECTION` |
| `interaction` | `summary` | Command | Insert only | Optional; personal field, masked on read |

## Status-transition matrix

| Record | From | Event | To | Side effects |
|---|---|---|---|---|
| Ledger entry | Does not exist | `append()` succeeds | Persisted | Row is immutable; `case_seq` assigned; outbox/action commits with it |
| Ledger entry | Does not exist | `append()` fails | Not persisted | Caller transaction rolls back; incident raised |
| Ledger entry | Persisted | UPDATE or DELETE attempted | Refused | Trigger raises; no change |
| Ledger entry | Persisted | Correction recorded | New entry | `CORRECTION` row names the original; original unchanged |

No case status changes. An entry has no status and is never changed.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Ledger cannot be written | Action and entry roll back; 503; incident `LEDGER_WRITE_FAILED` | MSG-P1-022 |
| X2 | Required value missing (event code, occurred time, actor) | 422; nothing written | MSG-GEN-001 |
| X3 | Two appends for one case at the same moment | Both written with consecutive `case_seq`; no gap or repeat | None |
| X4 | Case missing or out of scope | 404; nothing written | MSG-P4-003 |
| X5 | UPDATE or DELETE on an entry | Database refuses; correction is a new entry | None |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoint used | `POST /api/recovery/v1/cases/{caseId}/interactions` (API-P3-015). |
| Contract delta | None. The response fields already exist; the writer supplies the ledger semantics behind them. |
| Backward compatibility | Unchanged for callers; a failed ledger write now returns 503 MSG-P1-022 instead of a saved action. |
| Authorization | Case record C with scope; service identities `SY-CASEWF` and `SY-DATALOAD` hold Case record C. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 422 MSG-GEN-001; 503 MSG-P1-022. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label change; SCR-03 reads through RWB-E1-068. | Existing frontend tests remain green; no new frontend test required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-ILG-001, 002, 004, 008; SPEC-RWB-E1-066-001..014 | New writer, service, repository and entity; P3 handler delegation. | Positive, negative, boundary and error-path tests: every event code; missing required field; sequence under concurrency; unique key repeat; insert failure; correction; unknown case; trigger refusal; decision link. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `InteractionLedgerWriter` | Published interface | `append(LedgerEntryCommand)` for every recording path; `Propagation.MANDATORY`. |
| `LedgerWriteService` | Service | Validation, advisory lock, `case_seq`, insert, incident on failure. |
| `InteractionRepository` | Repository | Insert and read only; no update or delete method. |
| `Interaction` | Entity | Immutable mapping of `interaction`. |
| `InteractionsHandler` | Controller (P3) | Existing API-P3-015; delegates the write to the writer. |

Package `recovery.dataengine.ledger`. The architecture test forbids any class outside the ledger
package from using `InteractionRepository`.

### Data and migration

Migration adds to `interaction`: `event_code` varchar(40) not null, `actor_type` varchar(10) not null,
`actor_ref` varchar(64) not null, `source_ref` varchar(60) not null, `idempotency_key` varchar(120),
`case_seq` bigint not null, `decision_log_id` uuid, `corrects_entry_id` uuid. It drops NOT NULL on
`channel` and `direction` (Workbench events have no channel), adds unique (`case_id`, `case_seq`) and
unique (`idempotency_key`), and keeps `tr_interaction_append_only`. Index
`ix_interaction_case_time (case_id, occurred_at)` serves the read.

### Write algorithm

1. Validate the command: case exists, event code in `LOV-LEDGER-EVENT`, occurred time and actor present,
   source present, idempotency key length valid.
2. Take `pg_advisory_xact_lock` on the case ID.
3. Read `max(case_seq)` for the case and add 1.
4. Insert the row with all fields.
5. On a unique-key clash for `idempotency_key`, return the existing entry (repeat is handled by
   RWB-E1-067 for events; the direct write path returns the first entry).
6. On a unique-key clash for (`case_id`, `case_seq`), retry once.
7. On any other database error, translate to `LedgerWriteException`, raise `LEDGER_WRITE_FAILED` with
   the case ID and error class, and let the caller roll back.

### Transaction and events

The writer runs in the caller's transaction. The P3 handler commits the action and the entry together.
No event is published by this story. The incident path is `IncidentRecorder.raise` from RWB-E1-027; the
detail holds the error class and no personal data.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-CASEOWN | Case record C | Own |
| RW-TEAMMGR, RW-PHONECOL and other case roles | Case record R (read only in this story) | Team / own |
| SY-CASEWF | Case record C | All |
| SY-DATALOAD | Case record C | All |
| RW-AUDIT | Case record R; may not record | All |
| RW-PLATADM | Receives the incident | All |

The writer checks that the calling identity holds Case record C; a call without it throws
`AccessDeniedException`, mapped to MSG-P4-002.

### Observability and operations

- Metrics: entries written per event code; sequence retries; write failures; incident count.
- Alerts: `LEDGER_WRITE_FAILED`; sustained write failure.
- Audit: the ledger is the audit of what happened; the incident records the gap.
- Run book entry under RWB-E1-056.

### Performance

- One advisory lock per case; the lock is held for the insert only.
- Target: a single case history read under 2 seconds at 2031 size (NFR-070); the write path is a single
  indexed insert.
- No batch pre-allocation of `case_seq`; the lock prevents gaps.

### Feature flag and rollback

`rwb.dataengine.ledger-writer`. Off: the P3 handler keeps its prior path. Rollback: turn the flag off;
the added nullable columns remain and are harmless.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-066-01 | AC1, BR2, BR3 | System | Case with 6 entries; outbound call with promise | `case_seq` 7; event, time, actor, channel, direction, promise, source |
| TC-E1-066-02 | AC2, BR1, BR7 | System | 4 EFS entries, `CASE_CREATED`, `CASE_ALLOCATED` | 6 entries in one sequence; 1–6 with no gap |
| TC-E1-066-03 | AC3, BR6 | System | Reassignment under R-UNI-18 | Decision log holds rule/version/approver; ledger holds event, time, actor, decision ID |
| TC-E1-066-04 | AC4, BR5 | System | Insert forced to fail | 503 MSG-P1-022; 6 entries; no contact; incident |
| TC-E1-066-05 | AC5 | System | `append()` with no event code | MSG-GEN-001; no entry |
| TC-E1-066-06 | AC6, BR7 | System | Two concurrent appends | `case_seq` 7 and 8; no gap or repeat |
| TC-E1-066-07 | AC7 | System | Unknown case ID | 404 MSG-P4-003; no entry |
| TC-E1-066-08 | AC8, BR4 | System | UPDATE and DELETE on `case_seq` 3; correction | Statements refused; `CORRECTION` entry names 3 |
| TC-E1-066-09 | X1 | System | Incident recorder stub | Incident `LEDGER_WRITE_FAILED` with case ID and error class |
| TC-E1-066-10 | Access | Security | RW-AUDIT posts an interaction | 403 MSG-P4-002 |
| TC-E1-066-11 | BR7 | Unit | `max(case_seq)` null, 0, 6; retry on clash | Starts at 1; increments; retry succeeds once |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR7; SPEC-004 | How is `case_seq` made gap-free under concurrency? | Determines the locking strategy. | Transaction-level advisory lock on the case ID, then `max + 1`; story §13 step 3. | RESOLVED | SPEC-004 |
| CLAR-002 | BR5; SPEC-007 | Does a failed ledger write roll back the business action? | Determines transaction boundaries. | Yes; `Propagation.MANDATORY`, the action and entry commit together. | RESOLVED | SPEC-006, 007 |
| CLAR-003 | BR4; SPEC-001 | Is the append-only trigger kept? | Determines whether corrections overwrite. | Yes; `tr_interaction_append_only` stays; a correction is a new entry. | RESOLVED | SPEC-001, 011 |
| CLAR-004 | Contract; SPEC-002 | Is the endpoint new? | Determines API impact. | No; API-P3-015 exists; the writer is behind it. | RESOLVED | SPEC-002, 012 |
| CLAR-005 | BR1; SPEC-001 | Which recording paths must call `append()`? | Determines integration points. | P3 interactions, EFS history, ALS payment and notice dispatch; story §4 step 7. | RESOLVED | SPEC-001 |
| CLAR-006 | BR3; SPEC-003 | Where are promise amount and date stored? | Determines field placement. | On the interaction row where the promise was made; story BR3 and DF-INT-009/010. | RESOLVED | SPEC-003 |

`CLARIFICATION_STATUS: RESOLVED` — all 6 items are answered from the story and the data model. No item
changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New backend ledger store and writer; existing P3 interaction endpoint reused; no contract change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: new append-only store and published writer with no contract delta]
REQUIREMENT_COVERAGE_SUMMARY: All 7 business rules, 8 acceptance criteria, 5 exception paths and 4 state transitions are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
