# Technical Specification — RWB-E1-027 Decision log writer v1

| Field | Value |
|---|---|
| Story | RWB-E1-027 — Decision log writer v1 |
| Epic / module | E1 / P7 Decision center and log |
| RUN_ID | `INC-025-epic-1-RWB-E1-027` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-017, BR-RWB-008); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 027 Decision log writer v1 v1.md` |
| Upstream IDs | BRD-RWB-007; FR-RWB-017; BR-RWB-008; REQ-DRI-004, REQ-DRI-005; US-RWB-E1-027; FEAT-DRI-02..05, 08; R-UNI-39, R-UNI-40; CTL-06; NFR-034; EV-08 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author / approval | Technical Specifier (agent run) / Product Owner (TBC); Compliance Reviewer |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen, component, route or label. Failed writes appear as incidents in job and service monitoring (RWB-E1-056). |
| Logic In Scope | `YES` — transaction check, field and version validation, idempotency, append, outbox publish and rollback. |
| API In Scope | `NO` — no HTTP endpoint is added or changed. The writer is a published Java interface; `DecisionRecorded` is an outbox event; reads reuse API-P7-006/007. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `decision_log_entry` and `DecisionLogStore` (RWB-E1-008); `LOV-DECISION` and parameter catalog (RWB-E1-042/043); ACE outbox (RWB-TE-006); ACE incident path; monitoring (RWB-E1-056); callers JOB-02, JOB-03, transfer engine (RWB-E1-021), document attach (RWB-E1-032). |
| New Nodes Required | `YES` — `DecisionLogWriter` (published interface), `DecisionLogWriterService`, `DecisionLogRecordValidator`, `Epic1DecisionRecords`, `DecisionRecordedPublisher`; migration `V_E1_027__declog_idempotency.sql`. |
| Inherited Existing Behavior | Hash chain and append-only store (RWB-E1-008); outbox and retry (RWB-TE-006); configuration and reference data (RWB-E1-042/043); monitoring and run book (RWB-E1-056); P4 capability check. |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Epic 1 writes entries for case created, owner assigned, case transferred and document attached. | SPEC-RWB-E1-027-011 | DIRECT | `Epic1DecisionRecords` builds the four records. | COVERED |
| BR2 | Required on every record: decision code from LOV-DECISION, inputs reference, final call, decided at, actor; the case unless the code is an access event. | SPEC-RWB-E1-027-003, SPEC-RWB-E1-027-006 | DIRECT | Validator checks presence, list membership and the case rule. | COVERED |
| BR3 | The version group needs at least one of rule, model or agent version, except access events; a rule ID needs its rule version. | SPEC-RWB-E1-027-004 | DIRECT | Validator names `versions` or `ruleVersion`. | COVERED |
| BR4 | An approver needs an approval level from LOV-APPROVAL-LEVEL on the same record. | SPEC-RWB-E1-027-005 | DIRECT | Rejects approver without level and unknown level. | COVERED |
| BR5 | The record is written in the caller's transaction; if it cannot be written, the action does not proceed. | SPEC-RWB-E1-027-001, SPEC-RWB-E1-027-008, SPEC-RWB-E1-027-010 | DIRECT | `MANDATORY`; append and outbox in one transaction; rollback on failure. | COVERED |
| BR6 | The same event with the same idempotency key gives one entry; the repeat is counted. | SPEC-RWB-E1-027-007 | DIRECT | Unique key lookup; first reference returned; `decision_log_repeats_total`. | COVERED |
| BR7 | Decision codes for Epic 1 events are parameters, not code. | SPEC-RWB-E1-027-011, SPEC-RWB-E1-027-012 | DIRECT | `rwb.decision.code.*` from the catalog. | COVERED |
| AC1 | Case created and owner assigned produce `CASE_CREATED` and `OWNER_ASSIGNED`; the second carries rule ID/version, actor `SY-CASEWF` and an inputs reference; both pass schema check; two `DecisionRecorded` events. | SPEC-RWB-E1-027-008, SPEC-RWB-E1-027-009, SPEC-RWB-E1-027-011 | DIRECT | One outbox row per accepted write. | COVERED |
| AC2 | Transfer with no rule, model or agent version is refused with MSG-P7-009 naming `versions`; error logged with case ID and field; transfer rolls back. | SPEC-RWB-E1-027-004, SPEC-RWB-E1-027-010 | DIRECT | Version-group check; PII-free log; caller rollback. | COVERED |
| AC3 | Rule ID with empty rule version refused, naming `ruleVersion`. | SPEC-RWB-E1-027-004 | DIRECT | Pair check. | COVERED |
| AC4 | Store unavailable: `DecisionLogUnavailableException`; owner empty, status `New`; incident to platform administrator. | SPEC-RWB-E1-027-010, SPEC-RWB-E1-027-015 | DIRECT | Append failure propagates; incident; no retry. | COVERED |
| AC5 | Repeated event gives one entry; first ID returned; repeat count +1 for R-UNI-40. | SPEC-RWB-E1-027-007 | DIRECT | Unique key; repeat metric. | COVERED |
| AC6 | Call outside a transaction refused with `IllegalTransactionStateException`; nothing written. | SPEC-RWB-E1-027-002 | DIRECT | `MANDATORY`. | COVERED |
| AC7 | Decision code `D99` refused, naming `decisionCode`. | SPEC-RWB-E1-027-006 | DIRECT | LOV-DECISION lookup. | COVERED |
| X1 | Missing version group, inputs reference, final call or case. | SPEC-RWB-E1-027-003, SPEC-RWB-E1-027-010 | DIRECT | Refused; field logged; caller rolls back. | COVERED |
| X2 | Rule ID with no rule version. | SPEC-RWB-E1-027-004 | DIRECT | Refused as X1. | COVERED |
| X3 | Store cannot be written. | SPEC-RWB-E1-027-010 | DIRECT | Rollback; incident; MSG-P7-003. | COVERED |
| X4 | Same event twice with the same key. | SPEC-RWB-E1-027-007 | DIRECT | One entry; repeat counted. | COVERED |
| X5 | Writer called outside a transaction. | SPEC-RWB-E1-027-002 | DIRECT | Refused; nothing written. | COVERED |
| X6 | Decision code not in LOV-DECISION. | SPEC-RWB-E1-027-006 | DIRECT | Refused; MSG-P7-009. | COVERED |

## User story intent interpretation

As the **case workflow module (SY-CASEWF)**, I want **one writer that validates and records case created, owner assigned, case transferred and document attached, with the rule ID and version used, in the same transaction as the action**, so that **the first decision records exist in Epic 1 and no action proceeds without its record**.

This is a backend integration story. It gives every module one published interface, one validator and one outbox event, so no module builds its own record and no action commits without one. It is the automated part of CTL-06 and adds no screen or HTTP contract.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | A calling module calls `DecisionLogWriter.write(record)` as the last step before commit, inside its own transaction. |
| Callers | SY-CASEWF for case created, owner assigned and case transferred; SY-OCR for document attached; SY-RULES, SY-DATALOAD and SY-AGENT for their own decisions. |
| Preconditions | RWB-E1-008 complete; RWB-E1-056 complete; LOV-DECISION and `rwb.decision.code.*` loaded; ACE outbox available in the same transaction. |
| Input / output | In: `DecisionLogRecord` (key, case, code, versions, inputs ref, recommendation, approver/level, final call, override, actions, outcome, decided at, actor, `correctsEntryId`). Out: `DecisionLogEntryRef` (ID, `chainSeq`, `entryHash`, `repeated`), one row, one outbox row. |
| Feature flag | `rwb.decision.log-writer`. Off: writer not wired; dependent Epic 1 actions stay disabled (no prior decision-log path exists). |

## Field-level behaviour matrix

| Entity | Field | Source | Editable | Constraint |
|---|---|---|---|---|
| `decision_log_entry` | `idempotency_key` | Calling module event ID | No | varchar(80), unique when present |
| `decision_log_entry` | `case_id`, `decision_code` | Calling module / parameter | No | Case required unless `AC-%`; code in LOV-DECISION |
| `decision_log_entry` | `rule_id`, `rule_version`, `model_version`, `agent_version` | Calling module | No | Rule ID requires its version; at least one version for non-access events |
| `decision_log_entry` | `inputs_ref`, `final_call`, `decided_at` | Calling module | No | Required; varchar(400), varchar(40), timestamptz |
| `decision_log_entry` | `actor_user_id` | Calling module service identity | No | Required uuid |
| `decision_log_entry` | `approver_user_id`, `approval_level` | Calling module | No | Approver requires a level from LOV-APPROVAL-LEVEL |
| `decision_log_entry` | `recommendation`, `actions`, `outcome`, `override_reason` | Calling module | No | jsonb; varchar(1000) |
| `outbox` | `DecisionRecorded` | Publisher | No | One row per accepted entry, same transaction |

## Status-transition matrix

None. This story does not change a case status. It makes a status change by another module depend on its entry: when the write fails, the case stays in its prior status (for example `New` in AC4). The writer has no state.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Missing version group, inputs ref, final call or case | Refused; field logged; caller rolls back | MSG-P7-009 |
| X2 | Rule ID with no rule version | Refused as X1 | MSG-P7-009 naming `ruleVersion` |
| X3 | Store cannot be written | `DecisionLogUnavailableException`; rollback; incident | MSG-P7-003 |
| X4 | Same event twice with the same key | One entry; first reference; repeat counted | None |
| X5 | Writer called outside a transaction | `IllegalTransactionStateException`; nothing written | None |
| X6 | Decision code not in LOV-DECISION | Refused as X1 | MSG-P7-009 naming `decisionCode` |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints reused | `GET /api/recovery/v1/decision-log/{entryId}` and `GET /api/recovery/v1/decision-log` (API-P7-006/007), built in RWB-E1-008, read the entries written here (SPEC-RWB-E1-027-013). |
| Contract delta | None. `DecisionLogWriter` is an internal published Java interface; `DecisionRecorded` (EV-08) is documented under detailed design as an outbox event. |
| Compatibility / authorization | Unchanged. The writer runs under the caller's service identity with Decision log C; reads require Decision log R. |
| Errors / versioning | MSG-P7-009 for validation; MSG-P7-003 for store failure; caller message such as MSG-P3-013. No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label change; failures appear in monitoring. | Existing tests remain green; no new frontend test. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-017; BR-RWB-008; SPEC-RWB-E1-027-001..020 | New interface, service, validator, builders, publisher and migration. | Valid write; each required field; version group; approver/level; unknown code; duplicate; no transaction; store failure; outbox rollback; architecture test. |

## Detailed design

### Components and package (SPEC-RWB-E1-027-016)

| Component | Type | Responsibility |
|---|---|---|
| `DecisionLogWriter` | Published interface | `write(DecisionLogRecord)`; the only write path. |
| `DecisionLogWriterService` | Service | Transaction check, idempotency, validation, append, outbox. |
| `DecisionLogRecordValidator` | Service | BR2 to BR4 checks; codes from LOV-DECISION. |
| `Epic1DecisionRecords` | Service | Builders for the four Epic 1 events. |
| `DecisionRecordedPublisher` | Service | Writes EV-08 to the ACE outbox. |
| `DecisionCenterAndLogRepository` | Repository | Idempotency lookup; append through `DecisionLogStore`. |

Package `recovery.decision.writer`. Callers depend on the interface only. No class outside `recovery.decision` writes `decision_log_entry`; an architecture test fails the build if one does. The writer calls the store and reads no other module's tables.

### Validation order

1. Check an open transaction (`MANDATORY`); otherwise `IllegalTransactionStateException`.
2. Check whether an entry with the idempotency key already exists; if so, return the first reference with `repeated = true`, increment the repeat metric, and stop.
3. Validate required fields (BR2): code in LOV-DECISION, inputs ref, final call, decided at, actor, and case unless `AC-%`.
4. Validate the version group (BR3): at least one of rule, model or agent version; rule ID needs its version.
5. Validate the approver group (BR4): approver requires a level from LOV-APPROVAL-LEVEL.
6. Append through `DecisionLogStore.append`, write `DecisionRecorded`, return the reference; the caller commits.

### Idempotency, transaction and outbox

The key is the calling module's event ID; `uk_declog_idempotency` enforces one entry per key. A duplicate returns the first ID and increments `decision_log_repeats_total`; it appends nothing and publishes no second event (R-UNI-40, "ignore the second event"). `DecisionRecorded` carries entryId, caseId, decisionCode and approver; consumers are the ledger and reporting. A record without a key skips the check; the four Epic 1 builders always supply one. `write` is `@Transactional(propagation = Propagation.MANDATORY)`; the entry and outbox row commit or roll back with the caller's action. The writer never retries. On refusal the caller rolls back; on append failure it sees `DecisionLogUnavailableException`, an incident goes to the platform administrator queue, and the caller shows MSG-P7-003 or MSG-P3-013.

### Epic 1 records and parameters

| Event | Final call | Parameter |
|---|---|---|
| Case created by JOB-02 | `CASE_CREATED` | `rwb.decision.code.CASE_CREATED` = D6 (assumed) |
| Owner assigned by JOB-03 | `OWNER_ASSIGNED` | `rwb.decision.code.OWNER_ASSIGNED` = D6 (assumed) |
| Case transferred | `CASE_TRANSFERRED` | `rwb.decision.code.CASE_TRANSFERRED` = D6 (assumed) |
| Document attached | `DOCUMENT_ATTACHED` | `rwb.decision.code.DOCUMENT_ATTACHED` = D6 (assumed) |

Values are parameters owned by RW-DATASTEW. Rule ID and version come from the action that fired the event (for example `ALLOC-MTG-BKK-01` / `ALLOC-2026.11`).

### Data, migration and security (SPEC-RWB-E1-027-012, SPEC-RWB-E1-027-014)

`V_E1_027__declog_idempotency.sql` adds `idempotency_key varchar(80)` with unique index `uk_declog_idempotency`; no other table. The column is nullable per TSD T3.1; the four builders always populate it. Authority: SY-DECLOG and the five calling service identities hold Decision log C (callers only through the writer); every role with Decision log R reads; RW-PLATADM receives failed-write incidents.

### Observability, performance and rollback (SPEC-RWB-E1-027-017)

Metrics: writes accepted, refusals by field, append failures, repeats, outbox failures. Alerts: append failure, repeated refusals, outbox backlog. Logs name case ID and field only, never values. The writer adds one insert and one outbox row to the caller's transaction; no separate throughput NFR is stated. Flag `rwb.decision.log-writer`; off leaves dependent actions disabled. Rollback turns the flag off and redeploys the previous tag; the nullable column and unique index remain harmless.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-027-01 | AC1, BR1, BR7 | System | Case created and allocated by `ALLOC-MTG-BKK-01` | Two entries with `CASE_CREATED`/`OWNER_ASSIGNED`; rule, version, actor, inputs; two outbox events |
| TC-E1-027-02 | AC2, BR3 | System | Transfer with no version | MSG-P7-009 `versions`; case ID and field logged; rollback |
| TC-E1-027-03 | AC3, BR3 | System | `R-UNI-14`, empty rule version | MSG-P7-009 `ruleVersion` |
| TC-E1-027-04 | AC4, BR5 | System | Store off during JOB-03 | Exception; owner empty; status `New`; incident |
| TC-E1-027-05 | AC5, BR6 | System | Document attached event sent twice | One entry; first ID; repeat count +1 |
| TC-E1-027-06 | AC6, BR5 | System | Writer outside a transaction | `IllegalTransactionStateException`; nothing written |
| TC-E1-027-07 | AC7, BR2 | System | Decision code `D99` | MSG-P7-009 `decisionCode` |
| TC-E1-027-08 | Access, Principle 5 | Access / Resilience | Role without Decision log C; write forced to fail | Refused; caller action rolls back; no entry, no event |
| TC-E1-027-09 | BR2, BR3 | Unit | Each required field; access-event shape | Correct field named; access event without case accepted |
| TC-E1-027-10 | BR4, guardrail | Unit | Approver without level; architecture scan | Refused `approvalLevel`; build fails on a second write path |

## Guardrails

- No business value in code: decision codes are parameters and list values. No personal data in logs, tests or prompts; refusals log case ID and field only.
- No read of another module's tables; callers pass values in the record. No write path to `decision_log_entry` other than this interface, checked by an architecture test.
- No retry inside the writer; the caller retries. The writer never repairs or rewrites an entry.

## Out of scope

- The store, hash chain and verifier (RWB-E1-008); approval records with the limit applied (RWB-E2-013).
- Access events (RWB-E1-039); the data lake copy (RWB-E1-014); the recommendation service (Epic 4, API-P7-001).

## Traceability

`REQ-DRI-004` → FEAT-DRI-02, 03, 08 → BR1, BR2, BR3, BR4, BR6, BR7 → SPEC-RWB-E1-027-003, SPEC-RWB-E1-027-004, SPEC-RWB-E1-027-005, SPEC-RWB-E1-027-006, SPEC-RWB-E1-027-007, SPEC-RWB-E1-027-008, SPEC-RWB-E1-027-009, SPEC-RWB-E1-027-011 → TC-E1-027-01, TC-E1-027-02, TC-E1-027-03, TC-E1-027-05, TC-E1-027-07, TC-E1-027-09, TC-E1-027-10. `REQ-DRI-005` → FEAT-DRI-04, 05 → BR5 → SPEC-RWB-E1-027-001, SPEC-RWB-E1-027-002, SPEC-RWB-E1-027-008, SPEC-RWB-E1-027-010 → TC-E1-027-04, TC-E1-027-06, TC-E1-027-08. All map to BRD Epic 1, 3.7 and L3 process 17.

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR7; SPEC-RWB-E1-027-011 | Are the four Epic 1 codes all D6? | Parameter values. | Assumed D6 for all four, owned by RW-DATASTEW; load as parameters and confirm before go-live (story §3). | RESOLVED | SPEC-RWB-E1-027-011 |
| CLAR-002 | BR6; SPEC-RWB-E1-027-007 | Is the idempotency key required? | Validation and dedupe. | The four builders always supply the event ID; the column is nullable per TSD T3.1. | RESOLVED | SPEC-RWB-E1-027-007 |
| CLAR-003 | AC5; SPEC-RWB-E1-027-007, SPEC-RWB-E1-027-009 | Does a repeat publish a second event? | Downstream consumers. | No — R-UNI-40 says ignore the second event; one entry, one event, repeat counted. | RESOLVED | SPEC-RWB-E1-027-007, SPEC-RWB-E1-027-009 |
| CLAR-004 | BR4; SPEC-RWB-E1-027-005 | Is a level required whenever an approver is present? | Refusal path. | Yes — BR4 requires it on the same record; LOV-APPROVAL-LEVEL applies. | RESOLVED | SPEC-RWB-E1-027-005 |
| CLAR-005 | BR2; SPEC-RWB-E1-027-003 | How are access events with no case handled? | Validator scope. | Null case allowed only for `AC-%`; the call path is RWB-E1-039 and out of scope. | RESOLVED | SPEC-RWB-E1-027-003, SPEC-RWB-E1-027-020 |
| CLAR-006 | X3; SPEC-RWB-E1-027-010, SPEC-RWB-E1-027-015 | Who receives a failed-write incident? | Alert routing. | Platform administrator queue (AC4); MSG-P7-003 to the caller. | RESOLVED | SPEC-RWB-E1-027-010, SPEC-RWB-E1-027-015 |
| CLAR-007 | X5; SPEC-RWB-E1-027-002 | What exception outside a transaction? | Caller handling. | `IllegalTransactionStateException` from `Propagation.MANDATORY` (story §12). | RESOLVED | SPEC-RWB-E1-027-002 |
| CLAR-008 | Guardrail; SPEC-RWB-E1-027-019 | Does the writer retry? | Duplicate risk. | No — the caller's job or request retries (story §17). | RESOLVED | SPEC-RWB-E1-027-019 |
| CLAR-009 | MSG-P7-009; SPEC-RWB-E1-027-018 | Is MSG-P7-009 customer-facing? | Message surface. | No — service log and incident only (story §14). | RESOLVED | SPEC-RWB-E1-027-018 |

`CLARIFICATION_STATUS: RESOLVED` — all 9 items are answered from the story, TSD, rules or decision log. No item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend integration story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New decision log writer published interface and outbox event; no UI or HTTP contract change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: internal published interface and EV-08 only; read endpoints reused]
REQUIREMENT_COVERAGE_SUMMARY: All 7 business rules, 7 acceptance criteria and 6 exception paths are mapped; no state transition exists.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
