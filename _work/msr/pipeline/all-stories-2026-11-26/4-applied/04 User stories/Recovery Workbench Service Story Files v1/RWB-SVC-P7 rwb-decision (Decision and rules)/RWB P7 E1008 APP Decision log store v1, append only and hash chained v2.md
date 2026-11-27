# RWB-P7-E1008-APP Decision log store v1, append only and hash chained

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: app slice of RWB-E1-008 for rwb-decision — the central decision ledger in `rwb_decision`, the continuous ingest of `rwb.decision-record.v1`, the single hash chain and its verifier, the two decision-log reads and the daily chain check as a Temporal Schedule. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P7-E1008-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P7-E1008-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP10, DP13, DP15, DP17, DP19 |
| Parallel lane | L-P7-B |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P7-E1008-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | RWB-P7-E1008-DB, RWB-P7-E1008-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (FR-P7-001, FR-P7-003, FR-P7-004, FR-P7-005, FR-P7-006, FR-P7-009, FR-P7-010, FR-P7-011, FR-P7-012, FR-P7-013, FR-P7-029, FR-P7-036) |
| Status | Draft (realignment v1) |

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **an append-only decision ledger in `rwb_decision` holding the seven field groups of every decision, collected from the nineteen services off `rwb.decision-record.v1`, chained entry to entry and verified in one range**, so that **every decision of the programme is recorded once and in one place, cannot be changed or deleted, and any change to a stored entry is found by recomputing the chain**.

This is the app slice of legacy RWB-E1-008 for `rwb-decision`. It delivers, in the service and in schema `rwb_decision`:

- the **ingest** of `rwb.decision-record.v1` — the JOB-13 work of the target, continuous and event-driven rather than a 01:00 batch (Architecture v5 slides 20, 28 and 44; DP-03) — which validates each `DecisionRecorded` envelope and appends one `decision_log_entry` with its chain position;
- the **single chain**: `chain_seq`, `prev_hash` (the `entry_hash` of the entry before, 64 zeros for the first) and `entry_hash` (the SHA-256, lower-case hexadecimal, of the canonical form of BR4), with the chain lock of the legacy store so that two appends at the same moment get consecutive positions;
- the **verifier**: a range recomputed in `chain_seq` order in batches of 1,000, reporting the first break with its `chain_seq` and entry ID, raising an incident and sending MSG-P7-008 to the Compliance and PDPA officer group within 15 minutes;
- the **daily chain check** as a Temporal Schedule at 02:00 on the `rwb-decision` queue — the JOB-14 of the target — replacing the legacy Quartz job and its nightly copy (DP-10);
- the **two reads** of the ledger under `/api/recovery/decision/v1` — `GET /decision-log` and `GET /decision-log/{entryId}` — under the Decision log right, with the case scope applied through the case read of rwb-case;
- the **sealed-entry announcement** on the shared topic `rwb.decision-record.v1` and the **daily WORM seal** of the ledger hash to immutable storage (Architecture v5 slide 14 OUT line `FILE Immutable storage: daily ledger seal (WORM)`).

The eight legacy acceptance criteria stay with this story and are copied verbatim in section 7. The published contract, the schema and the deployment are separate stories of the same key: `RWB-P7-E1008-CON`, `RWB-P7-E1008-DB` and `RWB-P7-E1008-OPS`.

### 2. Business rationale

Documentation and audit trail findings (5 of 29 in the audit summary behind CTL-06) show that why a route was chosen, who approved it and on what figures is spread across e-mails and files. The legacy story met that with one table in the single `recovery` schema, written by one published interface inside the monolith, and it was right about the two things that matter: a stored entry is never changed, and the entries form one chain that a verifier can re-walk.

Architecture v5 changes where the record is written, not why. Slide 20 gives every service its own schema with `outbox + inbox + decision_record`, so each service writes its decision where the decision is taken and publishes `DecisionRecorded` to `rwb.decision-record.v1`; slide 28 adds that the change and its record commit together and that "rwb-decision reads rwb.decision-record.v1 into the ledger within 5 minutes", with "alerts for missing records" and "the chain checked every day"; ADR-022 records the decision as *local decision record plus central ledger*; slide 41 makes P7 the owner of "approvals, central decision ledger, DMN model registry" in `rwb_decision`; and slide 44 makes JOB-13 continuous Kafka ingest and JOB-14 a Schedule at 02:00.

So this story keeps the legacy guarantees and moves them one level up:

- **The chain is now over the central ledger.** Nineteen services write local records in nineteen schemas; the ledger is the one place where a single chain can be recomputed, because only there are all the entries of all the decisions in one sequence. `chain_seq` and the two hashes survive unchanged as columns and as the algorithm of BR4; what changes is that the row arrives as an event rather than as an in-process call.
- **Append-only is enforced twice and checked a third time.** The trigger `tr_declog_append_only` refuses an update and a delete for the schema owner, the service login has no UPDATE or DELETE grant (both are the DB story's), and the verifier finds a change made with the trigger disabled (the legacy AC4 case). All three are needed: AC1 tests the first two, AC4 tests the third.
- **The copy to the data lake is gone.** The legacy 01:00 copy (RWB-E1-014, JOB-13) has no target: there is no data lake (DP-17, ADR-018), reporting reads events, and the same JOB-13 id now names the continuous ingest (Architecture v5 slide 44). The ledger keeps its chain and its daily seal instead of shipping partitions.
- **The record is read where the reader is.** `GET /decision-log` and `GET /decision-log/{entryId}` stay as they were under the decision base of DP-13, so Audit and the center of excellence read one place, one hop from gateway-bff (DP-19).

It meets REQ-DRI-001, REQ-DRI-002 and REQ-DRI-003, carries CTL-06 and the 15-minute break report of NFR-035, and gives the FSD P7 measure "decisions within the delegation of authority, 100 percent" its service-side evidence: every decision reproducible from the log (NFR-033). Retention follows DL26.

Where no source fixes a value this story depends on, it carries the placeholder and a gap: the append path into the ledger is not a published operation of the Ownership Map (GAP-1224; ASM-2188); the construction of one central chain out of nineteen local chains is not specified (GAP-1225; ASM-2189); and the FSD still describes a data-lake stream that the architecture removes (GAP-1226; ASM-2190).

### 3. Preconditions

- `RWB-P7-E1008-CON` is published: the two read operations on base `/api/recovery/decision/v1`, the `DecisionLogEntry` and `DecisionLogPage` shapes, the error envelope, the `DecisionRecorded` envelope the ingest consumes, the tables the ledger owns and the fakes, so this story builds against a fixed contract on Day 1.
- `RWB-P7-E1008-DB` is applied: schema `rwb_decision`, the `decision_log_entry` table of section 12.7 with its keys, indexes, the trigger `tr_declog_append_only` and the function `refuse_change`, the grants of the `rwb-decision` login, and the library objects `outbox_event`, `processed_event` and `idempotency_key` in that schema.
- The local decision-record library of RWB-PLT-E1027-CON is live, with the `DecisionRecorded` envelope on the shared topic `rwb.decision-record.v1` in CloudEvents 1.0 binary mode (DP-03); every one of the 19 services publishes to it and the topic exists with its retry and `.dlt` topics.
- The workflow kit and the `rwb-recovery` namespace are live with RWB-PLT-E1071-CON, so the chain check can be a Schedule at 02:00 on the `rwb-decision` queue (DP-10).
- The per-service Flyway sequence runs in `rwb_decision` under RWB-PLT-E1044-CON (DP-15); this story adds no migration of its own.
- The reference-data contract of rwb-case is live with RWB-P3-E1043-CON and the platform client of RWB-PLT-E1043-CON (DP-07) for `LOV-DECISION` and `LOV-APPROVAL-LEVEL`; the ledger stores the codes it receives and validates none of them against a list of its own.
- The gateway-bff route of RWB-PLT-N001-CON exists, so the two reads are reachable from a screen through the composite route (DP-19), and the decision-log screen itself stays RWB-P7-E2005-APP.
- The `rwb-decision` service login and the schema owner are the only principals that touch the table; their names are Not specified in the source documents (GAP-1224; ASM-2188).
- The ingest is the only writer of `decision_log_entry`: the Ownership Map publishes `GET /decision-log` and `GET /decision-log/{entryId}` for P7 and no append operation, so this story declares no write path and records the point as a gap (GAP-1224; ASM-2188).
- The order in which the entries of 19 independent local chains become one central `chain_seq` is Not specified in the source documents (GAP-1225; ASM-2189).
- No approval stop: the story is released at status Draft (realignment v1) and starts on Day 1 with only contract dependencies (Template and Rules §R5.7).

### 4. Flow

1. A service commits a decision with its state change; its local record is written in its own schema in the same transaction and `DecisionRecorded` is written to its own outbox (DP-03; Architecture v5 slides 20 and 28). This story does not do that write; it receives the result.
2. The outbox relay of that service publishes `rwb.decision.DecisionRecorded.v1` on the shared topic `rwb.decision-record.v1`, keyed by `caseId` where there is a case and by the entry id where there is not.
3. The ingest of `rwb-decision` reads the envelope, checks the envelope (mode, `ce_type`, `ce_specversion`, key, traceparent) and looks the `ce_id` up in `processed_event`; a repeat is counted and answered with the first entry, and no second row is written (R-UNI-40).
4. The ingest validates the payload: the decision code is present, `inputsRef` is present, the final call is present, and at least one of rule version, model version and agent version is present, with a rule ID requiring its rule version (DF-DEC-001 to DF-DEC-031). A missing field is refused with MSG-P7-009 and the field name on the dead-letter record and nothing is chained; the same refusal the writer of RWB-E1-027 makes on the caller's side.
5. The ingest takes the chain lock — one PostgreSQL transaction advisory lock on the key `decision_log_chain` — and reads the `chain_seq` and `entry_hash` of the last entry.
6. The ingest sets `chain_seq` to last plus 1 and `prev_hash` to the last `entry_hash`, or to 64 zeros for the first entry.
7. The ingest builds the canonical form of the entry (BR4) and sets `entry_hash` to its SHA-256 in lower-case hexadecimal, then inserts the row, writes the outbox row of the sealed-entry announcement, and commits; the lock is released with the commit.
8. On any failure the transaction rolls back, no `chain_seq` is consumed, the consume offset is not committed, and the ingest retries from the retry topic; after the last retry the envelope goes to the dead-letter topic with its failure reason and an alert is raised.
9. At 02:00 the Schedule of section 12.6 starts `DecisionChainCheckWorkflow` on the `rwb-decision` queue with the business date as its input and no personal data in it.
10. The workflow runs `verifyChainRange` in batches of 1,000 from `chain_seq` 1 to the last entry: each `entry_hash` is recomputed from the canonical form and each `prev_hash` is compared with the entry before it.
11. A clean run returns the count checked, the last `chain_seq` and its `entry_hash`; the workflow writes one ledger-seal record for the business date and hands the range to the WORM seal step, which writes the file `ledger-seal-<businessDate>.json` with the count, the last `chain_seq` and the last `entry_hash` to immutable storage (Architecture v5 slide 14, `FILE Immutable storage: daily ledger seal (WORM)`).
12. A run that finds a break ends at the first failing entry: the result names its `chain_seq` and entry ID, `raiseChainBreak` raises an incident to the platform administrator queue, `sendComplianceNotice` sends MSG-P7-008 to the Compliance and PDPA officer group within 15 minutes of the run start, and the seal is not written for that date.
13. A reader with Decision log R reads `GET /api/recovery/decision/v1/decision-log?caseId=…` one page at a time in `chain_seq` order, and one entry with `GET /api/recovery/decision/v1/decision-log/{entryId}`; the scope comes from the authorise answer and the case read, and an entry of a case outside the scope answers 404 with MSG-P4-003.
14. A step at a point of no return (debt transfer, write-off posting, auction sale, title transfer) waits for the ledger to confirm its record in strict mode: it reads the entry back with `GET /decision-log/{entryId}` and proceeds only when the entry is present with its `entry_hash`; the exact confirmation mechanism is Not specified in the source documents (GAP-1227; ASM-2191).
15. A correction is a new entry: the ingest accepts a payload whose `correctsEntryId` names an earlier entry, appends it in chain order and leaves the corrected entry untouched.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | An UPDATE or DELETE is attempted on a stored entry | The login has no grant for it and the trigger `tr_declog_append_only` raises for the schema owner; the attempt is written to the ACE audit and SOC log | None (database error, logged) | AC1 |
| X2 | A stored entry was changed outside the service, for example in a test environment | The verifier names the first entry whose hash does not match, raises an incident and tells Compliance within 15 minutes | MSG-P7-008 | AC4 |
| X3 | Two appends arrive at the same moment | The chain lock orders them; `chain_seq` values are consecutive and each `prev_hash` names the entry before | None | AC5 |
| X4 | A decided entry is wrong | A new entry is written that names the corrected entry in `corrects_entry_id`; the original stays | None | AC6 |
| X5 | The ledger cannot be written | The ingest transaction rolls back, no `chain_seq` is consumed, the offset is not committed and the ingest retries; after the last retry the envelope is dead-lettered and an incident is raised | MSG-P7-003 | AC7 |
| X6 | A role without Decision log R reads an entry | Refused with 403 | MSG-P4-002 | AC8 |
| X7 | An envelope arrives twice with the same `ce_id` | The repeat is counted and the first entry reference is answered; no second row is written | None | AC3, AC5 |
| X8 | A break is found by the chain check | The break is reported with its `chain_seq` and entry ID; the seal of that date is not written | MSG-P7-008 | AC4 |
| X9 | An envelope names a decision code the reference list does not know | The entry is refused with the field named and the envelope is dead-lettered; nothing is chained | MSG-P7-009 (the writer's; this story does not re-check the list) | AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against its own contract, the platform decision-record library, the workflow kit, the Flyway sequence, the reference-data client and the gateway route; every other service is a published envelope on the shared topic |
| Negotiable | The ingestion batch size, the retry policy and the seal file layout are settled at build time; the chain algorithm, the two reads and the 15-minute break report are fixed |
| Valuable | Every decision of the programme is recorded once in one place, cannot be altered, and a break is found and reported the same day |
| Estimable | One ingest consumer, one chain service, one verifier, one workflow with three activities and one Schedule, two read operations |
| Small | Fits one sprint with its ten legacy tests, as the app slice of the key |
| Testable | Each criterion below is one test in section 16, at end-to-end level against the fakes and the seeded ledger |

### 7. Acceptance criteria

```gherkin
Feature: Decision log store v1, append only and hash chained

  Background:
    Given the environment is DEV with synthetic data
    Given the decision log store is empty

  Scenario: AC1 Append only (legacy RWB-E1-008 AC1)
    Given an entry with chain_seq 1 and final call "OWNER_ASSIGNED" is stored for case "RW-2026-000123"
    When an UPDATE setting final_call to "CASE_TRANSFERRED" and a DELETE of the entry are attempted through the ACE service's database role and again through the schema owner role
    Then the system refuses all four statements : by the missing grant for the service role, and with "decision_log_entry is append only" from tr_declog_append_only for the schema owner
    Then the entry is unchanged
    Then the system writes the refused attempts to the ACE audit log with the table, the operation and the entry ID

  Scenario: AC2 Hash chain (legacy RWB-E1-008 AC2)
    Given 100 entries are appended
    When the chain verifier runs from chain_seq 1 to 100
    Then every entry_hash equals the SHA-256 of the entry's canonical form
    Then every prev_hash equals the entry_hash of the entry before it, and the first prev_hash is 64 zeros
    Then the result holds count 100, last chain_seq 100 and that entry's entry_hash

  Scenario: AC3 Seven field groups (legacy RWB-E1-008 AC3)
    Given an entry is appended for decision "D6" on case "RW-2026-000123" with rule "R-UNI-14", rule version "UNI-2026.11", inputs reference "inputs/2026-12-03/7f3a", recommendation, approver "U-6101", approval level "L6", final call "APPROVED", actions and outcome
    When it is read with GET /decision-log/{entryId}
    Then the response holds inputsRef, ruleId and ruleVersion, recommendation, approverUserId and approvalLevel, finalCall, actions and outcome
    Then decidedAt, prevHash and entryHash are present

  Scenario: AC4 Hash chain verified daily (legacy RWB-E1-008 AC4)
    Given the store holds 10,000 entries
    Given the actions of the entry with chain_seq 7,412 were changed in the DEV database with the trigger disabled
    When the chain verifier runs from chain_seq 1 to 10,000
    Then the result names chain_seq 7,412 and its entry ID as the first break
    Then the system raises an incident and MSG-P7-008 is sent to the Compliance group within 15 minutes of the run start

  Scenario: AC5 Two appends at the same moment form one chain (legacy RWB-E1-008 AC5)
    Given entries up to chain_seq 50 are stored
    When two writers append one entry each in parallel transactions
    Then the entries get chain_seq 51 and 52
    Then the prev_hash of 52 equals the entry_hash of 51, and the prev_hash of 51 equals the entry_hash of 50

  Scenario: AC6 A correction is a new entry (legacy RWB-E1-008 AC6)
    Given entry "E-1" records owner "U-6102" by mistake
    When a correction entry is appended with corrects_entry_id "E-1" and the right owner "U-6103"
    Then entry "E-1" is unchanged
    Then GET /decision-log for case "RW-2026-000123" returns both entries in chain order with the correction naming "E-1"

  Scenario: AC7 A failed append leaves nothing behind (legacy RWB-E1-008 AC7)
    Given the rwb-case contract mock returns the case owner of "RW-2026-000123" as still the old owner while the ledger entry is unconfirmed (strict mode)
    Given the database connection for the store is closed in the test double
    When a writer appends an entry inside a transaction that also changes the case owner
    Then the system raises decisionLogUnavailableException
    Then the system stores no entry , the case owner is unchanged and chain_seq is not used

  Scenario: AC8 Reading an entry needs the Decision log right (legacy RWB-E1-008 AC8)
    Given the rwb-access contract mock returns the authorise answer REFUSED with MSG-P4-002 for a caller without Decision log R
    Given test user "U-6104" holds only RW-PHONECOL, whose Decision log letter is "-"
    When the user calls GET /decision-log/{entryId}
    Then the system refuses the call with status 403 and message MSG-P4-002
```

The eight criteria are the legacy criteria word for word, with two mock statements added in AC7 and AC8 where the cross-service part is stubbed: the owner change of rwb-case is a contract fake and the authorise answer is RWB-P4-E1037-CON's fake. No value — case ID, decision code, rule ID, rule version, inputs reference, user reference, approval level, final call, `chain_seq`, hash rule — was changed.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every decision writes one entry holding the seven field groups: inputs, versions, recommendation, approver, final call, actions and outcome | REQ-DRI-001; DF-DEC-004 to DF-DEC-015 |
| BR2 | A stored entry is never updated or deleted; a correction is a new entry naming the entry it corrects | REQ-DRI-002; R-UNI-24; `tr_declog_append_only`; ADR-009, ADR-022 |
| BR3 | Entries form one chain in `chain_seq` order; `prev_hash` is the `entry_hash` of the entry before, and 64 zeros for the first | REQ-DRI-003; DF-DEC-017, DF-DEC-018 |
| BR4 | `entry_hash` is the SHA-256, in lower-case hexadecimal, of the canonical form: the entry's fields except `entry_hash` and the standard columns, as JSON with keys in alphabetical order, UTF-8, no spaces, timestamps in ISO 8601 UTC with microseconds, numbers as strings and empty fields as null | RWB-E1-008 BR4; ADR-009 |
| BR5 | The ledger row and its sealed-entry announcement commit together in one transaction; a failed write leaves no entry, no chain position and no event | Principle 5; R-UNI-39; CTL-06 |
| BR6 | A break found by the verifier is reported to Compliance within 15 minutes and raises an incident; the daily seal of that date is not written | NFR-035; REQ-DRI-003; Architecture v5 slide 28 |
| BR7 | Retention of entries follows the bank retention schedule, and the daily seal is kept in immutable storage | DL26; Architecture v5 slide 14 (`FILE Immutable storage: daily ledger seal (WORM)`) |
| BR8 | The ledger is written by the ingest of `rwb.decision-record.v1` only: no service writes a `rwb_decision` row, and the two published operations are read only | DP-01; DP-03; Ownership Map (`decision_log_entry`, P7) |
| BR9 | The ledger keeps no data-lake copy and no reporting copy; reporting reads the events, and the legacy lake copy RWB-E1-014 is retired | DP-17; ADR-018; Template and Rules §R6 |
| BR10 | The record of a service reaches the ledger within 5 minutes of its commit, and a gap is alerted | Architecture v5 slide 28 |

### 9. State transitions

None in the case sense: this story changes no case status. A stored entry has no states; it exists from its append onward. The states below are the ingest and the chain, and they leave no business row:

| From | Event | Condition | To |
|---|---|---|---|
| Received | Envelope validated | `ce_type`, key and payload fields pass | Chained |
| Chained | Row inserted, outbox row written, commit | The chain lock was held and the insert succeeded | Sealed |
| Received | Envelope refused | A required field is missing, or the `ce_id` is known | Refused or Repeated (nothing chained) |
| Chained | Rollback | The insert, the lock or the commit fails | Received (offset not committed, retried) |
| Received | Retries exhausted | The envelope fails on the last retry | Dead-lettered (alert raised) |
| Sealed | Chain check over a range | Every hash and link matches | Verified for that range |
| Sealed | Chain check over a range | The first mismatch is found | Broken (incident, MSG-P7-008, no seal) |
| Verified | Daily seal written | The range was verified to the last entry | Sealed for the business date |
| Broken | Correction appended | A new entry names the broken one in `corrects_entry_id` | Sealed (the original still stored and still broken) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DECLOG Decision log writer | Publishes records to the shared topic (Decision log C, on its own service's side) |
| SY-CASEWF, SY-RULES, SY-DATALOAD, SY-OCR, SY-AGENT | Write through their own service's writer only (Decision log C) |
| The `rwb-decision` service identity | Reads the shared topic, appends ledger rows, runs the chain check and the seal (its own login, DP-02) |
| RW-AUDIT Internal audit | Reads entries (Decision log R) |
| RW-COMPLY Compliance and PDPA officer | Reads entries; receives break reports |
| RW-COE Center of excellence analyst | Reads entries |
| Every bank role holding Decision log R | Reads entries inside its scope |
| RW-PLATADM Platform administrator | Receives the incident on a break, a dead-lettered envelope or a failed run |
| No role | May update or delete an entry |

No personal name and no credential appears in the code, the configuration or a test fixture: a caller is a role code or a user reference only.

### 11. Data

| BR Field ID | Entity in `rwb_decision` | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | `decision_log_entry` | `id` | Write, then read |
| DF-DEC-002 | `decision_log_entry` | `case_id` | Write, then read; empty for an access event |
| DF-DEC-003 | `decision_log_entry` | `decision_code` | Write, then read |
| DF-DEC-004, DF-DEC-005 | `decision_log_entry` | `rule_id`, `rule_version` | Write, then read |
| DF-DEC-006, DF-DEC-007 | `decision_log_entry` | `model_version`, `agent_version` | Write, then read |
| DF-DEC-008 | `decision_log_entry` | `inputs_ref` | Write, then read |
| DF-DEC-009 to DF-DEC-015 | `decision_log_entry` | `recommendation`, `approver_user_id`, `approval_level`, `final_call`, `override_reason`, `actions`, `outcome` | Write, then read |
| DF-DEC-016 | `decision_log_entry` | `decided_at` | Write, then read |
| DF-DEC-017, DF-DEC-018 | `decision_log_entry` | `prev_hash`, `entry_hash` | Write, then read |
| DF-DEC-028 | `decision_log_entry` | `chain_seq` | Write, then read |
| DF-DEC-029 | `decision_log_entry` | `corrects_entry_id` | Write, then read |
| DF-DEC-030 | `decision_log_entry` | `actor_user_id` | Write, then read |
| DF-DEC-031 | `decision_log_entry` | `idempotency_key` | Write from `ce_id`, then read for the repeat |
| Library object | `processed_event` in `rwb_decision` | `event_id`, consumer, processed time | Write on every accepted envelope; read for the repeat |
| Library object | `outbox_event` in `rwb_decision` | the sealed-entry row | Write in the same transaction as the ledger row |
| No row copied | `recovery_case`, `task`, `timer`, `queue`, `approval`, `rule_*`, `delegation_limit`, `parameter_catalog`, `reference_row` | — | None: no row of another owner is copied into `rwb_decision`; the case, the rule version and the limits are identifiers received on the envelope or read over a contract |

Field IDs are those in the Logical Data Model and Data Dictionary. A fee or a balance never enters this table: the ledger holds references, codes and facts.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-decision`, base `/api/recovery/decision/v1`. Only the operations the Ownership Map gives to P7 are declared; there is no write path into the ledger (GAP-1224; ASM-2188).

| Method | Path | Purpose | Authorisation | Notes |
|---|---|---|---|---|
| GET | `/decision-log` | API-P7-006: search the ledger, in this story by `caseId` only and in `chain_seq` order, one page at a time | Decision log, right R; scope applied through the authorise answer and the case read of rwb-case | Filters by decision, rule version and approver and the screen belong to RWB-P7-E2005-APP |
| GET | `/decision-log/{entryId}` | API-P7-007: read one entry with its inputs, its versions, its final call, its reason and its two hashes | Decision log, right R; scope applied through the entry's case | 404 for an unknown entry or a case out of scope (MSG-P4-003) |

Errors follow the envelope of `RWB-P7-E1008-CON`: 401, 403 with MSG-P4-002, 404 with MSG-P4-003, 503 with MSG-GEN-006 when the ledger cannot be read.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/lists/LOV-DECISION` | P3 rwb-case (RWB-P3-E1043-CON) | Reads the decision codes in force for validation of an envelope against the list, never as a list of its own |
| GET | `/api/recovery/case/v1/admin/lists/LOV-APPROVAL-LEVEL` | P3 rwb-case (RWB-P3-E1043-CON) | Reads the approval levels in force (`L1` to `L6`) for the same check |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Reads the case of an entry for the scope filter and for the case timeline reference of the read |

All three are one hop with a 2 s budget, through the platform client libraries of RWB-PLT-E1043-CON and the case contract (DP-07): a failure of any of them never blocks the ingest — the code is stored as received and the check is repeated on the next read (see X9).

#### 12.3 Events published

| Event | Topic | Key | Payload carries | Purpose |
|---|---|---|---|---|
| rwb.decision.DecisionRecorded.v1 | rwb.decision-record.v1 (shared topic) | `caseId` where the entry has a case; the entry id where it does not | entry id, case ID where there is one, decision code, final call, rule ID, rule version, `chain_seq`, `entry_hash`, actor reference, decided time | Announces the sealed ledger entry to the strict-mode waiters and to rwb-reporting; written to the outbox of `rwb_decision` in the same transaction as the ledger row |

| Envelope element | Value |
|---|---|
| Mode | CloudEvents 1.0, binary mode |
| ce_specversion | 1.0 |
| ce_type | rwb.decision.DecisionRecorded.v1 |
| ce_source | `rwb-decision` (the ledger's own identity) |
| ce_subject | The case ID where there is one, the entry id where there is not |
| ce_id and traceparent | A new event identifier, and the trace context of the ingest |
| Payload | Identifiers and facts only; no personal data and no free text beyond the legacy fields |

The service topic `rwb.decision.events.v1` (with its retry topic and its `.dlt`) carries the approvals and the rule registry of this service — `ApprovalRequested`, `ApprovalDecided`, `RulePackageInForce` (Architecture v5 slides 14 and 42) — and this story publishes none of them. The re-announcement on the shared topic is deduplicated by `ce_id` and by `ce_source`, so the ledger ignores its own announcement. The catalogue names `rwb-decision` as a consumer of `rwb.decision-record.v1` and not as a producer; the announcement is the working read of the strict-mode confirmation (GAP-1227; ASM-2191).

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| rwb.decision.DecisionRecorded.v1 | rwb.decision-record.v1 (shared topic) | all 19 services, including `rwb-decision` itself (filtered out by `ce_source`) | The one input of the ledger: validated, deduplicated in `processed_event`, then chained (JOB-13, continuous; Architecture v5 slides 28, 42 and 44) |

The consumer group is `rwb-decision-ledger`, the retry topic and the `.dlt` are the platform's, and an envelope that fails on the last retry is dead-lettered with its reason and alerted (X5, X9). A consumer lag above the 5-minute completeness target raises the missing-record alert of BR10.

#### 12.5 Workflows and activities

| Workflow or activity | Type | Runs on | Use |
|---|---|---|---|
| `DecisionChainCheckWorkflow` | Workflow | queue `rwb-decision` | One run per business date: the range from the first to the last entry, the batch loop and the seal (JOB-14) |
| `verifyChainRange(fromSeq, toSeq)` | Activity | queue `rwb-decision` | Recomputes the range in batches of 1,000 and returns count, last `chain_seq`, last `entry_hash`, first break `chain_seq` and entry ID |
| `raiseChainBreak(breakSeq, entryId)` | Activity | queue `rwb-decision` | Raises the incident to the platform administrator queue |
| `sendComplianceNotice(businessDate, breakSeq, entryId)` | Activity | queue `rwb-decision` | Sends MSG-P7-008 to the Compliance and PDPA officer group |
| `writeLedgerSeal(businessDate, count, lastSeq, lastHash)` | Activity | queue `rwb-decision` | Writes the daily seal file to immutable storage (WORM) |

The ingest itself is a Kafka consumer and not a workflow; it is idempotent through `processed_event`, it holds no state between envelopes, and a workflow class never calls it.

#### 12.6 Schedules

| Schedule | Cron | Queue | Job | Overlap and catch-up |
|---|---|---|---|---|
| `decision-log-chain-check` | 02:00 daily | `rwb-decision` | JOB-14 Hash-chain check (Architecture v5 slide 44) | Overlap policy SKIP; catch-up window of one day; a missed run is visible as a missing seal |

The legacy Quartz job and its nightly copy are retired: the schedule is a Temporal Schedule in this service (DP-10) and the ingest is continuous rather than a 01:00 batch (GAP-1226; ASM-2190).

#### 12.7 Tables owned

| Table | Owner | Read or write here |
|---|---|---|
| `decision_log_entry` | P7 (`rwb_decision`) | Write by the ingest, read by the two operations and by the verifier |
| `outbox_event` | PLT library, created in `rwb_decision` by RWB-P7-E1008-DB | Write: the sealed-entry announcement |
| `processed_event` | PLT library, created in `rwb_decision` by RWB-P7-E1008-DB | Write and read: the dedupe of the ingest |
| `idempotency_key` | PLT library, created in `rwb_decision` by RWB-P7-E1008-DB | Write: the stored answer of a repeated read request where the edge requires it |

**Not owned and not touched.** `delegation_limit` is P4 rwb-access (Ownership Map ruling; Architecture v5 slides 14 and 41) and is read through the access contract by the approval stories, never here. `parameter_catalog`, `parameter_value`, `reference_row`, `reference_version` and `lov_value` are P3 rwb-case and are read over RWB-P3-E1043-CON (DP-07). `approval`, `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are P7 but belong to other stories of this service and are not created, read or written here. `recovery_case`, `task`, `timer` and `queue` are P3's. No foreign key, view or grant of `rwb_decision` names another schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Ledger read fake | `GET /decision-log` and `GET /decision-log/{entryId}` | A page in `chain_seq` order; one entry with the seven field groups; 403 with MSG-P4-002; 404 with MSG-P4-003; 503 with MSG-GEN-006 |
| DecisionRecorded fake | The shared topic of RWB-PLT-E1027-CON | One valid envelope with `ce_type` `rwb.decision.DecisionRecorded.v1`; one repeated `ce_id`; one refused body; one envelope with no case |
| Reference fake | RWB-P3-E1043-CON | `LOV-DECISION` with `D6` and `LOV-APPROVAL-LEVEL` with `L1` to `L6` |
| Authorise fake | RWB-P4-E1037-CON | An allowed answer, and a refusal with MSG-P4-002 for a caller without Decision log R |
| Case fake | The case read of rwb-case | Case `RW-2026-000123` in scope, and a case out of scope for MSG-P4-003 |
| Seal target fake | Immutable storage | An accepted seal file, and a refused write that fails the run |

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 read operations under `/api/recovery/decision/v1` | 3: two reference lists of P3 and the case read of P3 | One hop, 2 s timeout; the reads are behind gateway-bff |
| Kafka | 1 event type re-announced on the shared topic `rwb.decision-record.v1` | 1 event type on the same shared topic, plus the service topic `rwb.decision.events.v1` for other slices | CloudEvents 1.0 binary mode; key `caseId` or entry id; retry and `.dlt` topics |
| Temporal | 1 workflow, 4 activities, 1 Schedule (02:00) | 0 | Namespace `rwb-recovery`, queue `rwb-decision` |
| File | 1 out: the daily ledger seal | 0 | Immutable (WORM) storage, one file per business date |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, with the ledger in `decision.log` and the ingest in `decision.ingest`. The service is built from the platform template (Spring Boot, outbox relay, inbox, Temporal worker, codec, OpenTelemetry, contract tests) on its own Helm chart and pipeline, deployed as an API deployment and a worker deployment on the same task queue.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DecisionLogController` | Controller | The two reads, their validation and the RFC 9457 error envelope |
| `DecisionRecordIngestListener` | Consumer | Reads `rwb.decision-record.v1`, validates the envelope, dedupes in `processed_event`, calls the chain writer and the outbox |
| `DecisionLogStore` | Service | The chain lock, `chain_seq` and `prev_hash`, the canonical form, the hash, the insert |
| `CanonicalEntryForm` | Service | Builds the canonical JSON of BR4; one implementation shared by the store and the verifier |
| `HashChainVerifier` | Service | Recomputes a range in `chain_seq` order in batches of 1,000 and reports the first break |
| `ChainBreakNotifier` | Service | Raises the incident and sends MSG-P7-008 to the Compliance group |
| `DecisionLogRepository` | Repository | Inserts and reads `decision_log_entry`; no update and no delete method exists |
| `DecisionLogEntry` | Entity | Maps `decision_log_entry`; immutable |
| `LedgerSealWriter` | Activity client | Writes the daily seal file and records its result |
| `DecisionChainCheckWorkflow` | Workflow | The 02:00 run, the batch loop and the seal |

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The patterns **not claimed** by this story are DP-02 (one login per service, delivered by the platform DB work and the DB story), DP-04 (embedded Drools, the rule registry's own story), DP-05 (ACE views, never read here), DP-06 (parameters, the approval stories' read), DP-08 (the access guard, consumed through the authorise contract of RWB-P4-E1037-CON without a build dependency), DP-09 (outbox and inbox library — the objects are created by RWB-P7-E1008-DB under the X row and `RWB-PLT-TE006-CON` is not in this story's H row, recorded as GAP-1228; ASM-2192), DP-11 (in-process call — replaced by the event), DP-12 (case workflow), DP-14 (topic naming library), DP-16 (integration adapter), DP-18 (interaction ledger) and DP-20 (agent client).

**Build steps**

1. Consume `rwb.decision-record.v1` with the retry and `.dlt` topics; test the envelope check, the repeat and the dead-letter path (AC3, X7).
2. Build `CanonicalEntryForm` with golden vectors (a fixed entry to a fixed hash) checked into the test resources.
3. Build the chain writer with the advisory lock and the insert; test 100 entries, two parallel appends and the rollback (AC2, AC5, AC7).
4. Build the correction path (`corrects_entry_id`) and the read order; test AC6.
5. Build `HashChainVerifier` in batches; test the 10,000-entry break at `chain_seq` 7,412 (AC4).
6. Build `DecisionChainCheckWorkflow`, the incident and the Compliance notice, and the seal writer (AC4, BR6, BR7).
7. Build the two reads under `/api/recovery/decision/v1` with the guard and the scope; test AC3 and AC8.
8. Prove the append-only pair on a real schema: the login refused for want of a grant and the schema owner refused by `tr_declog_append_only` (AC1).

**Configuration.** `rwb.decision.chain.genesis-hash` (64 zeros), the consumer group `rwb-decision-ledger`, the batch size of the verifier (1,000), the 15-minute notice budget, the Compliance notification group and the seal target. The feature flag `rwb.decision.log-store` keeps its name; the seal path and the retention class are Not specified in the source documents (GAP-1226; ASM-2190).

**Done when.** The ten tests of section 16 pass, the golden hash vectors give the same result on the build server and on a developer machine, the append-only pair is proven on the service schema, and the 02:00 run writes one seal per business date and reports a break within 15 minutes.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | A caller's action fails because the ledger append failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-008 | The verifier finds a break | The decision log check for {date} found a break at entry {entryId}. Entries from that entry on cannot be relied on until Compliance reviews them. |
| MSG-P7-009 | An envelope is refused for a missing or invalid field (the writer's message, reused on the dead-letter record) | The decision record was refused: {field} is missing or not valid. |
| MSG-P4-002 | Read without Decision log R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Entry of a case outside the caller's scope | This case is not in your scope. |
| MSG-GEN-006 | The ledger cannot be read | {system} is not available. Try again in a few minutes. |

The texts of MSG-P7-003, MSG-P7-008, MSG-P4-002 and MSG-P4-003 are copied unchanged from RWB-E1-008; Thai text for each message follows DL10.

### 15. Screens and states

No new screen in this story. Entries are read through the two operations and behind gateway-bff (DP-19); the Decision log query screen SCR-38 and the filters come in RWB-P7-E2005-APP, and the case timeline that shows the entries is P3's. What an operator sees here is the chain-check run and its seal: Verified, Broken or Sealed for a business date, with the count, the last `chain_seq` and the last `entry_hash`.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-008-01 | AC1, BR2 | End to end | One synthetic entry; update and delete statements through the service login and the schema owner |
| TC-E1-008-02 | AC2, BR3, BR4 | End to end | 100 synthetic entries and the golden canonical vectors |
| TC-E1-008-03 | AC3, BR1 | End to end | One entry with all seven field groups filled, read on the decision base |
| TC-E1-008-04 | AC4, BR6 | End to end | 10,000 synthetic entries with `chain_seq` 7,412 changed with the trigger disabled |
| TC-E1-008-05 | AC5, BR3 | End to end | Two parallel ingests after `chain_seq` 50 |
| TC-E1-008-06 | AC6, BR2 | End to end | Entry "E-1" and its correction |
| TC-E1-008-07 | AC7, BR5 | End to end | Closed connection in the test double, and the strict-mode fake of rwb-case |
| TC-E1-008-08 | AC8 | End to end | The RW-PHONECOL test user and the authorise fake |
| TC-E1-008-09 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E1-008-10 | Principle 5 | NFR | The ledger append forced to fail; nothing stored, no `chain_seq` consumed, the offset not committed |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the end-to-end proof across real services is RWB-ITG-E1008-ITG.

### 17. Guardrails

- No business value in code: the genesis hash, the batch size, the notice budget and the notification group are configuration; the decision codes and approval levels are rows of the P3 reference contract.
- No personal data in the ledger, an event, a log or a test fixture: an entry holds references (`inputs_ref`, case ID, user references, rule ID), never a customer name, an account number or an identity number.
- No read of another service's table; the only cross-service inputs are the shared topic, the reference contract and the case read, one hop with a 2 s budget (DP-01, DP-07).
- No update or delete grant and no update or delete method in the repository; the trigger stays installed and the chain check proves it a third way (BR2).
- One canonical form implementation for writing and verifying, with golden vectors in the build (BR4).
- No data-lake copy and no reporting copy: reporting reads the events (DP-17, BR9).
- The seal is written only for a range that verified end to end; a broken date is never sealed (BR6).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | One record per decision with the seven field groups | Epic 1, 3.7; Program, 5.7 | FEAT-DRI-01 | 17 Run the decision center | BR1 | TC-E1-008-03 |
| REQ-DRI-002 | Append only; a correction is a new record naming the one it corrects | Epic 1, 3.7; Program, 5.7 | FEAT-DRI-01 | 17 Run the decision center | BR2, BR5 | TC-E1-008-01, TC-E1-008-06, TC-E1-008-07, TC-E1-008-10 |
| REQ-DRI-003 | Hash chained, checked, break reported to Compliance the same day | Epic 1, 3.7; Program, 5.7 | FEAT-DRI-01 | 17 Run the decision center | BR3, BR4, BR6, BR7 | TC-E1-008-02, TC-E1-008-04, TC-E1-008-05, TC-E1-008-09 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P7-E1008-CON | Contract | H: the two read operations, the shapes, the error envelope and the envelope the ingest consumes |
| RWB-P7-E1008-DB | Database | X: the schema, the table, the keys, the indexes, the trigger, the grants, the login and the library objects |
| RWB-P7-E1008-OPS | DevOps | X: the pipeline, the Flyway run at start, the configuration and secrets, the chain-check job, the alerts, the seal and the restore run book |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library and the `DecisionRecorded` envelope on the shared topic |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | Contract | H and C: the reference-data client and the two lists it reads |
| RWB-PLT-E1071-CON | Contract | H: the workflow kit, the namespace and the Schedule |
| RWB-PLT-E1044-CON | Contract | H: the per-service Flyway sequence |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff route the two reads use |
| RWB-PLT-TE006-CON | Contract | Referred to only: the outbox and inbox library whose objects the DB story creates (GAP-1228) |
| RWB-ITG-E1008-ITG | Integration | I: the end-to-end proof of the shared topic, the ledger and the strict-mode confirmation |
| RWB-P7-E2005-APP | App development | The query API with the filters and SCR-38, on the same table and the same base |
| RWB-P7-E1027-APP | App development | The writer side of this service's own decisions, on the same chain |

### 19. Out of scope

- The contract document, the shapes, the envelope specification and the fakes: RWB-P7-E1008-CON.
- The schema, the table, the trigger, the grants, the login and the library objects: RWB-P7-E1008-DB.
- The pipeline, the Flyway run at start, the configuration, the alerts, the seal job in the pipeline and the restore run book: RWB-P7-E1008-OPS.
- The local record and its writer in each of the 19 services: RWB-PLT-E1027-CON and RWB-PLT-E1027-APP, and the writer story of this service RWB-P7-E1027-APP.
- The query filters by approver, rule version and date, and the query screen SCR-38: RWB-P7-E2005-APP.
- The copy of the log to the data lake (RWB-E1-014) and its partitions and watermarks: no target path, retired under DP-17 and ADR-018.
- The legacy nightly schedule of RWB-TE-008 as a Quartz row: replaced by the 02:00 Temporal Schedule of section 12.6 (DP-10).
- Approvals, the delegation of authority limits and the approval screen: RWB-P7-E2013-APP and RWB-P7-E2014-APP.
- The rule registry and the rule version packages: the rule stories of this service, RWB-P7-E1073-APP and its siblings.
- Retention periods and their configuration (DL26), beyond the seal of BR7.
