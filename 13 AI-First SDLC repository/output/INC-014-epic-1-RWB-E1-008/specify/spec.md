# Technical Specification — RWB-E1-008 Decision log store v1, append only and hash chained

| Field | Value |
|---|---|
| Story | RWB-E1-008 — Decision log store v1, append only and hash chained |
| Epic / module | E1 / P7 Decision center and log |
| RUN_ID | `INC-014-epic-1-RWB-E1-008` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-017, BR-RWB-008); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 008 Decision log store v1 append only and hash chained v1.md` |
| Upstream IDs | BRD-RWB-007; FR-RWB-017; BR-RWB-008; REQ-DRI-001..003; US-RWB-E1-008; FEAT-DRI-01; ADR-009; CTL-06; NFR-033, NFR-035; API-P7-006, API-P7-007 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author / approval | Technical Specifier (agent run) / Product Owner (TBC); Compliance Reviewer |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen, component, route or label. SCR-38 Decision log query is RWB-E2-005; this story exposes two read endpoints only. |
| Logic In Scope | `YES` — append-only enforcement, chain sequencing, canonical form, SHA-256 hashing, corrections, range verification, break reporting and scoped reads. |
| API In Scope | `YES` — first implementation of `GET /api/recovery/v1/decision-log` (API-P7-006) and `GET /api/recovery/v1/decision-log/{entryId}` (API-P7-007), both first in E1 per TSD T-A. |
| API Impact Type | `NEW_API_REQUIRED` |
| Impacted Existing Nodes | `decision_log_entry`, trigger `tr_declog_append_only` and `refuse_change` (RWB-E1-001); ACE audit and SOC log; ACE incident and notification paths; P4 access check and scope. |
| New Nodes Required | `YES` — `DecisionCenterAndLogController`, `DecisionLogStore`, `CanonicalEntryForm`, `HashChainVerifier`, `ChainBreakNotifier`, `DecisionCenterAndLogRepository`, `DecisionLogEntry`; migration `V_E1_008__declog_chain.sql`. |
| Inherited Existing Behavior | Table and append-only trigger (RWB-E1-001); authentication, capability check and scope (P4); notification and incident paths (ACE); migrations (RWB-E1-044); job run records (RWB-TE-007). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Every decision writes one entry holding the seven field groups: inputs, versions, recommendation, approver, final call, actions and outcome. | SPEC-RWB-E1-008-004 | DIRECT | `DecisionLogEntry` maps DF-DEC-001..018; `append` inserts all groups. | COVERED |
| BR2 | A stored entry is never updated or deleted; a correction is a new entry naming the entry it corrects. | SPEC-RWB-E1-008-001, SPEC-RWB-E1-008-006, SPEC-RWB-E1-008-019 | DIRECT | Missing UPDATE/DELETE grants plus trigger; no update/delete method; `corrects_entry_id`. | COVERED |
| BR3 | Entries form one chain in `chain_seq` order; `prev_hash` is the previous `entry_hash`, 64 zeros for the first. | SPEC-RWB-E1-008-002, SPEC-RWB-E1-008-005, SPEC-RWB-E1-008-010 | DIRECT | Advisory chain lock; last-row read; genesis hash from configuration. | COVERED |
| BR4 | `entry_hash` is SHA-256 lower-case hex of the canonical form: all fields except `entry_hash` and standard columns, keys alphabetical, UTF-8, no spaces, ISO 8601 UTC microseconds, numbers as strings, empty as null. | SPEC-RWB-E1-008-003 | DIRECT | One `CanonicalEntryForm` shared by store and verifier; golden vectors. | COVERED |
| BR5 | The append is the last statement of the caller's transaction, so the action and its entry commit or roll back together. | SPEC-RWB-E1-008-007, SPEC-RWB-E1-008-018 | DIRECT | Append in caller's transaction; failure raises `DecisionLogUnavailableException`. | COVERED |
| BR6 | A break found by the verifier is reported to Compliance within 15 minutes and raises an incident. | SPEC-RWB-E1-008-011 | DIRECT | `ChainBreakNotifier`; MSG-P7-008. | COVERED |
| BR7 | Retention follows the bank retention schedule. | SPEC-RWB-E1-008-012 | DIRECT | Retention class is reference data per DL26; no period coded. | COVERED |
| AC1 | UPDATE and DELETE refused through service role and schema owner; entry unchanged; attempts in ACE audit with table, operation and entry ID. | SPEC-RWB-E1-008-001, SPEC-RWB-E1-008-019 | DIRECT | Grants refuse the service role; trigger raises "decision_log_entry is append only". | COVERED |
| AC2 | 100 entries verify: hashes match, `prev_hash` links, first is 64 zeros, result holds count 100, last seq 100 and hash. | SPEC-RWB-E1-008-003, SPEC-RWB-E1-008-005 | DIRECT | `verify(1, 100)` returns `ChainCheckResult`. | COVERED |
| AC3 | Reading an entry returns all seven groups plus `decidedAt`, `prevHash` and `entryHash`. | SPEC-RWB-E1-008-004, SPEC-RWB-E1-008-009 | DIRECT | API-P7-007 response `DecisionLogEntry`. | COVERED |
| AC4 | 10,000 entries with 7,412 changed: first break 7,412, incident, MSG-P7-008 within 15 minutes of run start. | SPEC-RWB-E1-008-005, SPEC-RWB-E1-008-011 | DIRECT | Batched range read; first failure retained; deadline from run start. | COVERED |
| AC5 | Parallel appends after 50 get 51 and 52, each `prev_hash` naming the entry before. | SPEC-RWB-E1-008-002, SPEC-RWB-E1-008-013 | DIRECT | PostgreSQL advisory lock on `decision_log_chain`. | COVERED |
| AC6 | A correction names `corrects_entry_id`; original unchanged; case read returns both in chain order. | SPEC-RWB-E1-008-006, SPEC-RWB-E1-008-020 | DIRECT | New row only; case query ordered by `chain_seq`. | COVERED |
| AC7 | Failed append leaves no entry, owner unchanged, `chain_seq` not consumed. | SPEC-RWB-E1-008-007, SPEC-RWB-E1-008-018 | DIRECT | Caller rollback; sequence assigned inside the transaction. | COVERED |
| AC8 | User without Decision log R gets 403 and MSG-P4-002. | SPEC-RWB-E1-008-008 | DIRECT | Method security; scope through the entry's case. | COVERED |
| X1 | UPDATE or DELETE on a stored entry. | SPEC-RWB-E1-008-001 | DIRECT | Refused; ACE audit and SOC log. | COVERED |
| X2 | Entry changed outside the service. | SPEC-RWB-E1-008-005, SPEC-RWB-E1-008-011 | DIRECT | First failing entry; incident; MSG-P7-008. | COVERED |
| X3 | Two writers append at once. | SPEC-RWB-E1-008-002, SPEC-RWB-E1-008-013 | DIRECT | Chain lock; consecutive `chain_seq`. | COVERED |
| X4 | A decided entry is wrong. | SPEC-RWB-E1-008-006 | DIRECT | Correction entry; original stays. | COVERED |
| X5 | Store cannot be written. | SPEC-RWB-E1-008-007 | DIRECT | Exception; caller rolls back. | COVERED |
| X6 | Role without Decision log R reads. | SPEC-RWB-E1-008-008 | DIRECT | 403; MSG-P4-002. | COVERED |

## User story intent interpretation

As a **center of excellence analyst (RW-COE)**, I want **an append-only decision log store holding the seven field groups of every decision, each entry hashed to the one before it**, so that **every Epic 1 decision is recorded once, cannot be changed or deleted, and any change is found by recomputing the chain**.

This is a backend data-store story. It builds the table extension, append path, hash chain and verifier that every later writer uses, plus the two read endpoints for auditors, Compliance and the centre of excellence. It adds no screen (the query screen is Epic 2) and is the evidence base for CTL-06.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | `DecisionLogStore.append` called by `DecisionLogWriter` (RWB-E1-027) inside the caller's transaction, as its last statement. Verification is on demand via `HashChainVerifier.verify`; the nightly schedule is RWB-TE-008. |
| Preconditions | RWB-E1-001 complete (`decision_log_entry`, `tr_declog_append_only`, `refuse_change`). Service role holds INSERT and SELECT and no UPDATE/DELETE. ACE notification to the Compliance group and the incident path are available. |
| Input / output | In: a validated `DecisionLogRecord`; for reads an `entryId` or `caseId` with page and size. Out: one row with `chain_seq`, `prev_hash`, `entry_hash`; `DecisionLogEntryRef`; `ChainCheckResult`; `DecisionLogEntry`/`DecisionLogPage`. |
| Feature flag | `rwb.decision.log-store`. Off: append path and endpoints disabled. |

## Field-level behaviour matrix

| Entity | Field | Source | Editable | Constraint |
|---|---|---|---|---|
| `decision_log_entry` | `id`, `case_id`, `decision_code` | Append / caller | No | uuid; case nullable only for `AC-%` (`ck_declog_case`); code from LOV-DECISION |
| `decision_log_entry` | `rule_id`, `rule_version`, `model_version`, `agent_version` | Caller | No | varchar(20)/(40); rule pair validated by the writer |
| `decision_log_entry` | `inputs_ref` | Caller | No | varchar(400), required |
| `decision_log_entry` | `recommendation`, `actions`, `outcome` | Caller | No | jsonb |
| `decision_log_entry` | `approver_user_id`, `approval_level` | Caller | No | uuid; LOV-APPROVAL-LEVEL |
| `decision_log_entry` | `final_call`, `override_reason`, `decided_at` | Caller | No | varchar(40) required; varchar(1000); timestamptz required |
| `decision_log_entry` | `chain_seq`, `prev_hash`, `entry_hash` | Last + 1; last hash or genesis; canonical hash | No | bigint unique; char(64) not null; char(64) not null |
| `decision_log_entry` | `corrects_entry_id`, `actor_user_id` | Caller | No | uuid; self-reference for corrections |

## Status-transition matrix

None. This story does not change a case status. A stored entry has no states; it exists from its append onward. The append either commits with the caller's action or leaves nothing behind.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | UPDATE or DELETE on a stored entry | Service role refused by missing grant; schema owner refused by trigger; attempt in ACE audit and SOC log | Database error, logged |
| X2 | Entry changed outside the service | First failing `chain_seq` and ID named; incident; Compliance told within 15 minutes | MSG-P7-008 |
| X3 | Two appends at once | Chain lock orders them; consecutive `chain_seq`; links correct | None |
| X4 | A decided entry is wrong | Correction with `corrects_entry_id`; original unchanged | None |
| X5 | Store cannot be written | `DecisionLogUnavailableException`; caller rolls back | MSG-P7-003 from the caller |
| X6 | Caller lacks Decision log R | 403; nothing read or changed | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` |
| New endpoints | `GET /api/recovery/v1/decision-log/{entryId}` (API-P7-007) and `GET /api/recovery/v1/decision-log` (API-P7-006), first in E1 per TSD T-A. |
| Contract delta | API-P7-007 returns `DecisionLogEntry` with all seven groups plus `decidedAt`, `prevHash`, `entryHash`. API-P7-006 returns `DecisionLogPage`, filtered by `caseId` in this story, ordered by `chain_seq`, with `page` and `size`. |
| Compatibility / versioning | New endpoints; no existing contract change; v1 unchanged. Other API-P7-006 filters come in RWB-E2-005. |
| Authorization | Decision log, right R; scope through the entry's case. An entry with no case has no case scope and is outside this read path (RWB-E1-039). |
| Errors | 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003 for unknown entry or out-of-scope case; 503 MSG-GEN-006. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label change; SCR-38 is RWB-E2-005. | Existing tests remain green; no new frontend test. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-017; BR-RWB-008; SPEC-RWB-E1-008-001..020 | New store, canonical form, verifier, notifier, repository, entity and controller; migration and grants. | Append/read; first and later entry; 100-entry chain; 10,000-entry break; parallel append; correction; failed append; missing right; out-of-scope case; golden vectors. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `DecisionCenterAndLogController` | Controller | Both read endpoints; validation; problem responses. |
| `DecisionLogStore` | Service | Chain lock, `chain_seq`/`prev_hash`, canonical form, hash, insert; no update or delete. |
| `CanonicalEntryForm` | Service | Canonical JSON per BR4; one implementation for store and verifier. |
| `HashChainVerifier` | Service | Recomputes a range in `chain_seq` order in batches of 1,000; first break and count. |
| `ChainBreakNotifier` | Service | Raises the incident and sends MSG-P7-008 to Compliance. |
| `DecisionCenterAndLogRepository` | Repository | Inserts and reads `decision_log_entry`; no update/delete method. |
| `DecisionLogEntry` | Entity | Maps the table; immutable. |

Package `recovery.decision.log`. The store is called only through `DecisionLogWriter` (RWB-E1-027); no other module writes the table. Case scope is resolved through the P3 published interface; no other module's table is read.

### Data and migration (SPEC-RWB-E1-008-014)

`V_E1_008__declog_chain.sql`: adds `chain_seq bigint not null unique`, `corrects_entry_id uuid references decision_log_entry(id)` and `actor_user_id uuid`; makes `case_id` nullable with `ck_declog_case (case_id IS NOT NULL OR decision_code LIKE 'AC-%')`; adds `ix_declog_actor_time (actor_user_id, decided_at)` and `ix_declog_rule (rule_id, rule_version)`; revokes UPDATE and DELETE from the service role. The trigger stays. Genesis hash and notification group are configuration.

### Append and chain algorithm

1. Take the PostgreSQL transaction advisory lock on key `decision_log_chain`.
2. Read the last entry's `chain_seq` and `entry_hash`.
3. Set `chain_seq` to last + 1 and `prev_hash` to the last `entry_hash`, or to `rwb.decision.chain.genesis-hash` (64 zeros) for the first entry.
4. Build the canonical form and set `entry_hash` to its SHA-256 in lower-case hexadecimal.
5. Insert. The caller commits the action and the entry together and releases the lock.
6. On failure raise `DecisionLogUnavailableException`; the caller rolls back and `chain_seq` is not consumed.

### Canonical form and reads

Canonical JSON: keys alphabetical, UTF-8, no spaces, timestamps ISO 8601 UTC with microseconds, numbers as strings, empty fields null. Golden vectors are checked into test resources and must match on the build server and a developer machine. Reads: by `entryId` (404 if unknown or out of scope) and by `caseId` ordered by `chain_seq` (`DecisionLogPage`, page and size). Scope is applied through the entry's case; access events are RWB-E1-039.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| SY-DECLOG; SY-CASEWF, SY-RULES, SY-DATALOAD, SY-OCR, SY-AGENT | Decision log C (service modules through the writer only) | All |
| RW-AUDIT, RW-COMPLY, RW-COE and every role with Decision log R | Decision log R | All or role scope |
| RW-PLATADM; no role | Receives incidents / may not update or delete an entry | All / — |

### Observability, performance and rollback (SPEC-RWB-E1-008-015, SPEC-RWB-E1-008-016, SPEC-RWB-E1-008-017)

Metrics: entries appended, append failures, verifications, first-break `chain_seq`, duration, notifications. Alerts: break, failed append, notification failure. Refused UPDATE/DELETE reach the ACE audit and SOC log with table, operation and entry ID. AC4's 10,000-entry check must finish inside the 15-minute window; reads use the unique `chain_seq` index in batches of 1,000. No other throughput NFR is stated; DL11 remains open. Flag `rwb.decision.log-store`; off disables append and reads. Rollback turns the flag off and redeploys the previous tag; the migration is forward-only, so nullable columns and indexes remain harmless.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-008-01 | AC1, BR2 | System | One entry; UPDATE and DELETE as service role and schema owner | Four statements refused; entry unchanged; four audit records |
| TC-E1-008-02 | AC2, BR3, BR4 | System | 100 entries | Hashes and links correct; first 64 zeros; count 100, last seq/hash |
| TC-E1-008-03 | AC3, BR1 | System | Entry with all seven groups | All groups plus `decidedAt`, `prevHash`, `entryHash` |
| TC-E1-008-04 | AC4, BR6 | System | 10,000 entries; 7,412 changed | First break 7,412; incident; MSG-P7-008 within 15 minutes |
| TC-E1-008-05 | AC5, BR3 | System | Two parallel appends after 50 | Seq 51 and 52; links correct |
| TC-E1-008-06 | AC6, BR2 | System | Entry E-1 and correction | E-1 unchanged; both in chain order; correction names E-1 |
| TC-E1-008-07 | AC7, BR5 | System | Closed connection | Exception; no entry; owner unchanged; seq not used |
| TC-E1-008-08 | AC8 | System | RW-PHONECOL user | 403; MSG-P4-002 |
| TC-E1-008-09 | Access | Access | Role without Decision log R | Refused; nothing read |
| TC-E1-008-10 | Principle 5 | Resilience | Append forced to fail inside a caller transaction | Caller change rolls back |
| TC-E1-008-11 | BR2, BR4 | Unit | Golden vectors; repository surface | Stable hashes; no update/delete method |

## Guardrails

- No business value in code: genesis hash, notification group and retention class are configuration or reference data. No personal data in logs, tests or prompts; entries hold references only.
- No read of another module's tables; other modules write only through the P7 writer. No update/delete method or grant; the verifier never repairs an entry. One canonical form implementation.

## Out of scope

- Entry validation and `DecisionRecorded` (RWB-E1-027); the nightly schedule and report (RWB-TE-008, JOB-14).
- Copy to the data lake (RWB-E1-014, JOB-13); audit queries and SCR-38 (RWB-E2-005); retention periods (DL26); access-event read scope (RWB-E1-039).

## Traceability

`REQ-DRI-001` → FEAT-DRI-01 → BR1 → SPEC-RWB-E1-008-004 → TC-E1-008-03, TC-E1-008-11. `REQ-DRI-002` → BR2, BR5 → SPEC-RWB-E1-008-001, SPEC-RWB-E1-008-006, SPEC-RWB-E1-008-007, SPEC-RWB-E1-008-018, SPEC-RWB-E1-008-019 → TC-E1-008-01, TC-E1-008-06, TC-E1-008-07, TC-E1-008-10. `REQ-DRI-003` → BR3, BR4, BR6 → SPEC-RWB-E1-008-002, SPEC-RWB-E1-008-003, SPEC-RWB-E1-008-005, SPEC-RWB-E1-008-011, SPEC-RWB-E1-008-013 → TC-E1-008-02, TC-E1-008-04, TC-E1-008-05. All map to BRD Epic 1, 3.7 and L3 process 17.

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | API assessment; SPEC-RWB-E1-008-009 | Are API-P7-006/007 in scope now? | Endpoints or store only. | Yes — story contract names both; TSD T-A marks them first in E1. | RESOLVED | SPEC-RWB-E1-008-009 |
| CLAR-002 | API-P7-006; SPEC-RWB-E1-008-009 | Are all list filters in scope? | Query surface and tests. | No — `caseId` only; the rest is RWB-E2-005 (story §12). | RESOLVED | SPEC-RWB-E1-008-009 |
| CLAR-003 | BR3; SPEC-RWB-E1-008-010 | Is the genesis hash fixed or configuration? | Code vs data. | 64 zeros via `rwb.decision.chain.genesis-hash`; no literal (story §13). | RESOLVED | SPEC-RWB-E1-008-010 |
| CLAR-004 | BR4; SPEC-RWB-E1-008-003 | What exactly is hashed? | Every hash. | The canonical JSON in BR4; golden vectors prove it. | RESOLVED | SPEC-RWB-E1-008-003 |
| CLAR-005 | BR7; SPEC-RWB-E1-008-012 | What retention period applies? | Deletion/archive. | DL26 sets the class; the period is reference data; no deletion here. | RESOLVED | SPEC-RWB-E1-008-012 |
| CLAR-006 | AC5; SPEC-RWB-E1-008-013 | How are concurrent appends serialised? | Chain integrity. | Advisory lock on `decision_log_chain` (story §4 step 2). | RESOLVED | SPEC-RWB-E1-008-013 |
| CLAR-007 | X1; SPEC-RWB-E1-008-001 | Which audit log gets refused attempts? | Evidence trail. | ACE audit and SOC log (story §4 step 7); FSD says ACE audit log; same path. | RESOLVED | SPEC-RWB-E1-008-001 |
| CLAR-008 | AC4; SPEC-RWB-E1-008-005 | Does the verifier stop at the first break? | Result shape. | This story returns the first; RWB-TE-008 counts all. | RESOLVED | SPEC-RWB-E1-008-005 |
| CLAR-009 | AC8; SPEC-RWB-E1-008-008 | Scope for an entry with no case? | Access-event reads. | Read is through the entry's case; no case means 404 here; RWB-E1-039 owns access events. | RESOLVED | SPEC-RWB-E1-008-008 |
| CLAR-010 | AC1; SPEC-RWB-E1-008-001 | Is the trigger owner the schema owner? | Refusal path tested. | AC1 tests both service role (grant) and schema owner (trigger). | RESOLVED | SPEC-RWB-E1-008-001 |

`CLARIFICATION_STATUS: RESOLVED` — all 10 items are answered from the story, TSD, FSD, rules or decision log. No item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend data-store story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New append-only hash-chained decision log store and two read endpoints; no UI.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: new store, verifier and API-P7-006/007 read contract]
REQUIREMENT_COVERAGE_SUMMARY: All 7 business rules, 8 acceptance criteria and 6 exception paths are mapped; no state transition exists.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
