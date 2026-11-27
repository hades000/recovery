# RWB-P4-E1008-APP Decision log store v1, append only and hash chained

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E1008-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP10, DP13, DP15, DP17, DP19 |
| Parallel lane | L-P4-M |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P7-E1008-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-DRI-001, REQ-DRI-002, REQ-DRI-003) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-008 for rwb-access. This is the second slice of the legacy key: the local append-only hash-chained decision-record store of this service and the Decision log right that every reader of it needs. The central ledger, the ingest, the 02:00 chain check and the two decision reads stay with `rwb-decision` (P7), and the access-event writers and break-glass stay with RWB-P4-E1039-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-E1008-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **center of excellence analyst (RW-COE), an internal auditor (RW-AUDIT) and a compliance and PDPA officer (RW-COMPLY)**, I want **every decision of `rwb-access`, including every access event, written once into the service's own `decision_record` store, each row chained to the row before it by a SHA-256 `entry_hash` and a `prev_hash` that starts at 64 zeros, append-only by grant and by trigger, correctable only by a new row that names the row it corrects, verified on every append and behind the local access-log read, and readable only under the `DECISION_LOG` capability-area right R inside the scope of the entry's case**, so that **no decision and no access of this service can be quietly changed or deleted, every reader can see whether the chain still holds, and only a role that holds the Decision log right sees the entries at all**.

Inside `rwb-access` this is the second slice of the legacy story RWB-E1-008:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- Three deliverables, and nothing else. First, the `decision_record` table in `rwb_access`, the local library object of DP-03, with `chain_seq`, `prev_hash`, `entry_hash`, `corrects_entry_id` and `actor_user_id`, its append-only trigger and its grants, and this service's own Flyway migration (DP-15). Second, the canonical form, the chain writer and the verifier that every rwb-access decision uses on write and that the `GET /api/recovery/access/v1/admin/access-log` read uses on read. Third, the `DECISION_LOG` capability-area right R on that read and on the authorise answer that `rwb-decision` takes before it returns an entry of the central ledger, with the scope applied through the entry's case, 403 MSG-P4-002 and 404 MSG-P4-003.
- A correction is a new row that names the corrected row. No update and no delete path exists anywhere: no repository method, no database grant, no endpoint.
- The shared topic is `rwb.decision-record.v1` with one event type `rwb.decision-record.DecisionRecorded.v1`, published by the local decision-record library for each append. This story adds no topic and publishes no `rwb.access.<Event>.v1` message of its own.
- The central `decision_log_entry` in `rwb_decision`, the ingest, the `ChainCheckWorkflow` at 02:00 as JOB-14 and the two decision-log read endpoints are P7's (RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-OPS). This story provides the local store and the right those readers and writers use, and it builds none of them.
- The access-event writers, the entry shape they write and the break-glass grant are RWB-P4-E1039-APP. This story supplies the store and the right that story writes through and reads under.
- The copy of the log to the data lake is retired: no job, topic, table, interface or file copies this store or its central ledger to a data lake (DP-17; legacy RWB-E1-014 retired).
- No Schedule is started here. DP-10 is carried by P7's JOB-14, and this slice starts no workflow.

The rest of the column set behind the five named columns, the canonical form, the genesis value and the per-service login name are Not specified in the source documents (GAP-0984; ASM-1725). The governing right of the local read is Not specified in the source documents (GAP-0984; ASM-1726). What the verifier does on a write and on a read is Not specified in the source documents (GAP-0984; ASM-1727).

### 2. Business rationale

Documentation and audit-trail findings (5 of 29 in the audit summary behind CTL-06) show that why a route was chosen, who approved it and on what figures is spread across e-mails and files. The legacy key RWB-E1-008 builds one decision log for the monolith: one record per decision with inputs, versions, recommendation, approver, final call, actions and outcome; every update and delete refused; one hash chain; and a verifier that finds a break. It meets REQ-DRI-001, REQ-DRI-002 and REQ-DRI-003, and the measure is every decision reproducible from the log (NFR-033).

In the target the log is recorded locally first and sealed centrally. Each service writes its decision record in its own schema in the same transaction as its state change, hash-linked to the record before it, and the local library publishes `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` (Architecture v5 slides 20, 28 and 42; ADR-022; DP-03). `rwb-decision` collects the record into the central ledger within 5 minutes and checks the chain at 02:00 as a Temporal Schedule (DP-10, JOB-14). Writing the central log synchronously inside every call would become a distributed transaction across 19 services, which is why the local record and the central ledger are two objects and not one.

`rwb-access` is the service where that split has a second consequence. Its own decision records are access events: who looked at which case, which document and which data product, and when (FSD P4 A2.7 and A2.8). If the local store is not append-only and not chained, an access entry can be edited after the fact, and the whole audit story of the service collapses. If the store is not readable under one explicit right, the access log either leaks to every role or is answerable only by the platform team. This slice therefore delivers the store, the verifier and the `DECISION_LOG` right together, because each one is worthless without the other two: a chain nobody verifies proves nothing, and a verified chain that any role can read is a privacy finding.

The split inside the legacy key is deliberate. RWB-P7-E1008-APP builds the central ledger, the ingest, the chain check and the two reads; RWB-P7-E1008-CON publishes the contract of the central read that asks this service for the right; RWB-P4-E1039-APP writes the access events and the break-glass grant; and this story builds the local store those writers depend on and the right every reader of both logs passes through. It supports REQ-ACA-006 (every read is written to the access log and the log is therefore readable) and REQ-DRI-012 (audit can query the record with its versions) on the access side, without taking either of those features away from the stories that own them.

### 3. Preconditions

- RWB-P4-E1037-APP delivered the `rwb_access` baseline: `role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit` exist with their dictionary rows (DF-REF-034 to DF-REF-044 and DF-REF-198 to DF-REF-211), and RWB-P4-E1037-CON published the authorise operation this story answers behind.
- The local decision-record library of DP-03 is available through RWB-PLT-E1027-CON: it fixes the library object names, the outbox row, the shared topic `rwb.decision-record.v1` and the one event type `rwb.decision-record.DecisionRecorded.v1`. That contract is a contract dependency of this story and its fake is used until it is published.
- The per-service Flyway sequence of DP-15 is in place through RWB-PLT-E1044-CON, so this story adds one migration to the `rwb-access` sequence and edits no applied version.
- The database login is the rwb-access login (DP-02). Its name is Not specified in the source documents (GAP-0984; ASM-1725), and the story names it "the rwb-access login (DP-02)" until the platform DB story fixes it.
- `LOV-CAPABILITY` in TSD P4 T3.2 names `DECISION_LOG` among the 14 capability areas, and it is read through the reference-data contract of `rwb-case` (DP-07) with the version in force. No area code is written in code.
- The letter each role holds in `DECISION_LOG` is a row of the permission matrix loaded by RWB-P4-AD002-APP, not a source value: the TSD P4 RBAC matrix of T6.1 tabulates Rules and parameters, Reference data and Platform administration only, so the `DECISION_LOG` letters of RW-AUDIT, RW-COMPLY, RW-COE and RW-PHONECOL are Not specified in the source documents (GAP-0984; ASM-1726).
- The chain lock is a PostgreSQL transaction advisory lock on the chain key of `rwb_access`, and the key is configuration; the same lock name as the central ledger is not used, because the two chains are separate.
- The access-event writers of RWB-P4-E1039-APP, the DoA lookup of RWB-P4-E2013-APP and the administrative changes of RWB-P4-E1037-APP write through the store this story builds. This story does not wait for them and builds none of them: it supplies the store, the verifier and the right.
- The 02:00 chain check, its Schedule, its 15-minute report to Compliance and the daily seal to write-once storage belong to `rwb-decision` (RWB-P7-E1008-APP, RWB-P7-E1008-OPS). No Schedule and no workflow of this story exists.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7), because every build dependency of its patterns arrives with the platform contract libraries and the baseline of this service.

### 4. Flow

1. Writer: any decision path of `rwb-access` — the access-event writers of RWB-P4-E1039-APP, the DoA lookup of RWB-P4-E2013-APP, an administrative change of RWB-P4-E1037-APP — calls `DecisionRecordStore.append(record)` inside its own transaction, as the last statement before the commit.
2. Store: takes the chain lock, a PostgreSQL transaction advisory lock on the chain key of `rwb_access`.
3. Store: reads the `chain_seq` and the `entry_hash` of the last row of `decision_record`.
4. Verifier on write: recomputes the canonical form and the `entry_hash` of that last row and compares the result with the stored `entry_hash`; on a mismatch the append is refused, nothing is written, an incident is raised and the break is reported to RW-COMPLY with MSG-P7-008.
5. Store: sets `chain_seq` to the last value plus 1 and `prev_hash` to the last `entry_hash`, or `chain_seq` 1 and `prev_hash` to 64 zeros where the store is empty (BR3).
6. Store: builds the canonical form of the new row (JSON with keys in alphabetical order, UTF-8, no spaces, timestamps in ISO 8601 UTC with microseconds, numbers as strings, empty fields as null) and sets `entry_hash` to its SHA-256 in lower-case hexadecimal (BR4).
7. Store: inserts the row with `actor_user_id` from the session and `corrects_entry_id` null; the caller's transaction commits the state change and the entry together, then the lock is released (BR5).
8. Store: on any failure raises `DecisionLogUnavailableException`; the caller's transaction rolls back, the action does not happen and the caller shows its own message (MSG-P7-003); the `chain_seq` that was read is not consumed (BR13).
9. Database: `tr_declog_append_only` refuses any UPDATE and any DELETE on `decision_record`, and the rwb-access login holds INSERT and SELECT only; a refused attempt is written to the ACE audit and SOC log with the table, the operation and the entry ID (BR2).
10. Correction: where a stored entry is found to be wrong, a new entry is appended with `corrects_entry_id` naming the corrected entry and with the correction's own `chain_seq`; the corrected entry is not touched (BR2).
11. Read: a caller holding `DECISION_LOG` R calls `GET /api/recovery/access/v1/admin/access-log`. The service resolves the caller's roles and the letters of the area from `permission` and `role` at the matrix version in force, applies default deny, and refuses a caller without R with 403 and MSG-P4-002 after writing one AC-DENY entry (BR9).
12. Read: the entries of the query are filtered by the scope of the caller through the case reference the entry carries; an entry of a case outside the caller's scope answers 404 with MSG-P4-003 and is never returned, and the refusal names neither the case nor the entry (BR9, BR10).
13. Read: the verifier runs over the answered range, recomputes each `entry_hash` and checks each `prev_hash` against the entry before it in `chain_seq` order, and the `chain` field of the answer states the head `chain_seq`, its `entry_hash`, the count verified and the first break when there is one; on a break an incident is raised and MSG-P7-008 is sent to RW-COMPLY, and no entry from the break onward is presented as verified (BR6).
14. Authorise answer: where `rwb-decision` reads an entry of the central ledger, it asks `POST /api/recovery/access/v1/authorise` for area `DECISION_LOG`, right R and the entry's case, and this service answers granted or 403 MSG-P4-002 by the same rule as step 11; a case outside the caller's scope answers 404 with MSG-P4-003 (BR9).
15. Guardrail: no job, topic, table, interface or file copies this store or the central ledger to a data lake; JOB-13 is continuous Kafka ingest in `rwb-decision` and JOB-14 is its chain check (DP-17, BR11).
16. Build: boundary rule BND-6 fails the build where a class of `th.co.scb.ace.workbench.recovery.access` names a `v_ace_*` view or a `public` table, and the rwb-access login holds no privilege on either (BR12).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | An UPDATE or a DELETE is attempted on a stored entry | The service login is refused for want of the grant and the schema owner is refused by the trigger; the attempt is written to the ACE audit and SOC log | None (database error, logged) | AC1 |
| X2 | A stored entry was changed outside the service, for example in DEV | The verifier names the first entry whose hash or link does not match, an incident is raised and the break is reported to RW-COMPLY | MSG-P7-008 | AC2 |
| X3 | Two writers append at the same moment | The chain lock orders them; the `chain_seq` values are consecutive and each `prev_hash` names the entry before | None | AC2 |
| X4 | A decided entry is wrong | A new entry is appended with `corrects_entry_id` naming it; the original keeps its value and its chain position | None | AC3 |
| X5 | The store cannot be written | The append fails, the caller's action rolls back, the `chain_seq` is not consumed and the caller shows its own message | MSG-P7-003 | AC1 |
| X6 | A caller without `DECISION_LOG` R reads the local access log, or is the reader of the central read | 403 and no entry; one AC-DENY entry is written before the refusal leaves the service | MSG-P4-002 | AC5 |
| X7 | The entry belongs to a case outside the caller's scope | 404 and no entry data; neither the case nor the entry is named | MSG-P4-003 | AC6 |
| X8 | A job, topic, table, interface or file that copies the log to a data lake is found | The guardrail test fails and the element is named; the store and the central ledger stay the only copies | None | AC7 |
| X9 | A class of the package names a `v_ace_*` view or a `public` table | The build fails with boundary rule BND-6 naming the class and the object; nothing merges | Build log | AC8 |
| X10 | The migration is applied a second time | Flyway reports the version as already applied; no row is written twice and no applied version is edited | None | AC1 |

No exception path of this story changes a case, a task, a role or a permission. This service reads its own store and its own permission rows, and the state machines of access and of the administrator surface stay with RWB-P4-E1037-APP and RWB-P4-E1039-APP.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the `rwb_access` baseline, the DP-03 library fake and the RWB-P7-E1008-CON fake; it waits for no other story and it builds no read of the central ledger |
| Negotiable | The chain key, the genesis value, the canonical form and the verifier's report shape are configuration and design choices fixed here; the column names, the message IDs and the decision codes are not |
| Valuable | Every decision and every access of this service is recorded once, cannot be changed, is verified by its own reader, and is readable only under the right |
| Estimable | One migration, one store, one canonical form, one verifier, one right resolver and one boundary rule, with eight criteria and ten test cases |
| Small | Fits one sprint with its tests, as the second slice of the legacy key |
| Testable | Every criterion is asserted on a row, a refusal, a build result or a chain report; every fixture is synthetic |

### 7. Acceptance criteria

```gherkin
Feature: Decision log store v1, append only and hash chained, in rwb-access

  Background:
    Given the environment is DEV with synthetic data
    Given the table "decision_record" exists in schema "rwb_access" with its trigger "tr_declog_append_only"
    Given the rwb-access login holds INSERT and SELECT on "decision_record"
    Given every access entry is a decision record written through the local decision-record library of DP-03

  Scenario: AC1 Append only by grant and by trigger (new, D-RCV-60)
    Given an entry with chain_seq 1 and decision code "AC-READ" is stored for case "RW-2026-000123"
    When an UPDATE of that entry and a DELETE of that entry are attempted through the rwb-access login
    Then both statements are refused with SQLSTATE 42501, because the login holds INSERT and SELECT only
    When the same UPDATE and the same DELETE are attempted as the schema owner
    Then both statements are refused by "tr_declog_append_only" with "decision_record is append only"
    Then the entry is unchanged in the store
    Then each refused attempt is written to the ACE audit and SOC log with the table, the operation and the entry ID
    And the repository of the service exposes no update method and no delete method, and no endpoint updates or deletes an entry

  Scenario: AC2 One SHA-256 chain with the 64-zero genesis and no gap (new, D-RCV-60)
    Given the store is empty
    When 100 entries are appended through the store and two further writers then append one entry each in parallel transactions
    Then chain_seq runs from 1 to 102 with no gap and no repetition
    Then the prev_hash of chain_seq 1 is 64 zeros and every later prev_hash equals the entry_hash of the entry before it
    Then every entry_hash is the lower-case hexadecimal SHA-256 of that entry's canonical form
    Then the verifier over the range 1 to 102 reports count 102, head chain_seq 102 and that entry's entry_hash with no break
    When the actions of the entry with chain_seq 51 are changed in the DEV database with the trigger disabled and the trigger is restored
    Then the verifier over 1 to 102 names chain_seq 51 and its entry ID as the first break
    Then an incident is raised and MSG-P7-008 is sent to the Compliance role RW-COMPLY
    And an append that would chain on a broken entry is refused, so no entry is written after a break

  Scenario: AC3 A correction is a new entry that names the corrected one (new, D-RCV-60)
    Given entry "E-1" records actor reference "U-6102" by mistake on case "RW-2026-000123"
    When a correction entry is appended with corrects_entry_id "E-1" and actor reference "U-6103"
    Then the store holds both entries, and entry "E-1" keeps its value, its chain_seq and its entry_hash
    Then the correction carries the next chain_seq and names "E-1"
    Then the local access-log read for case "RW-2026-000123" returns both entries in chain order, with the correction naming "E-1"
    And no path updates or deletes entry "E-1"

  Scenario: AC4 The DECISION_LOG R holder reads the local access log and the authorise answer grants the same right (new, D-RCV-60)
    Given test user "U-6104" holds RW-AUDIT, whose DECISION_LOG letter is "R" in the matrix version in force, with scope "ALL"
    When "U-6104" calls GET /api/recovery/access/v1/admin/access-log for a period that holds entries of case "RW-2026-000123"
    Then the answer is 200 and each entry carries chain_seq, prevHash, entryHash, the decision code, the actor reference and the decided time
    Then the chain field of the answer names the head chain_seq, its entry_hash and the count verified
    Given rwb-decision holds an entry of case "RW-2026-000123" in the central ledger
    When rwb-decision calls POST /api/recovery/access/v1/authorise with area "DECISION_LOG", right "R" and that case reference
    Then the answer is granted for "U-6104" and refused with 403 and MSG-P4-002 for a caller who holds no R in the area
    And this service reads no row of the central ledger and no schema of rwb-decision at any step

  Scenario: AC5 A role without the Decision log right is refused with MSG-P4-002 (new, D-RCV-60)
    Given test user "U-6105" holds only RW-PHONECOL, whose DECISION_LOG letter is "-" in the matrix version in force
    When "U-6105" calls GET /api/recovery/access/v1/admin/access-log for any period
    Then the answer is 403 with message MSG-P4-002 and no entry is returned
    Then exactly one entry is written with decision code "AC-DENY", capability area "DECISION_LOG" and right "R"
    And the same caller is refused with 403 and MSG-P4-002 on the authorise answer that rwb-decision takes
    And no entry of the store is changed by the refusal

  Scenario: AC6 An entry of a case outside the caller's scope is 404 with MSG-P4-003 (new, D-RCV-60)
    Given test user "U-6106" holds DECISION_LOG R with scope "OWN" and the entry belongs to case "RW-2026-000999" of another team
    When "U-6106" reads that entry through GET /api/recovery/access/v1/admin/access-log
    Then the answer is 404 with message MSG-P4-003 and no entry data
    Then the refusal names neither the case nor the entry
    And an entry that carries no case reference is answered only to a caller whose scope in the area is "ALL"

  Scenario: AC7 No lake copy of the store exists (new, D-RCV-60)
    Given the rwb-access build and the wave-1 environment run
    When the job map, the topic list, the schema list, the interface list and the file manifests are inspected
    Then no job, topic, table, interface or file copies the store or its central ledger to a data lake
    Then JOB-13 is continuous Kafka ingest in rwb-decision and no copy job of rwb-access exists
    Then no job of rwb-access checks the chain: the 02:00 check is JOB-14 in rwb-decision
    And the local store in rwb_access and the central ledger in rwb_decision are the only copies of a decision record

  Scenario: AC8 No ACE view and no public table is read by this service (new, D-RCV-60)
    Given a class "th.co.scb.ace.workbench.recovery.access.record.DecisionRecordReader" with a query on "recovery.v_ace_customer"
    When the pipeline runs the boundary rule of the rwb-access build
    Then the build fails with boundary rule BND-6, the class name and "recovery.v_ace_customer"
    When the same class names "public.customer" instead
    Then the build fails with boundary rule BND-6, the class name and "public.customer"
    When the same class reads "decision_record" in schema "rwb_access"
    Then the build passes
    And a statement by the rwb-access login against "recovery.v_ace_customer" and against "public.customer" fails with SQLSTATE 42501
```

The eight criteria above are new and test only this deliverable: the local append-only hash-chained store, the verifier and the `DECISION_LOG` right. The legacy criteria of RWB-E1-008 belong to the other slices: the central store and the response shape of the two decision reads to RWB-P7-E1008-APP, the schema objects and the grants of `rwb_decision` to RWB-P7-E1008-DB, the access-event writers, the entry shape and break-glass to RWB-P4-E1039-APP, and the run across services to RWB-ITG-E1008-ITG. No legacy criterion text is copied into this story.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every decision writes one entry holding the seven field groups: inputs, versions, recommendation, approver, final call, actions and outcome | REQ-DRI-001; DF-DEC-004 to DF-DEC-015 |
| BR2 | A stored entry is never updated and never deleted; a correction is a new entry that names the entry it corrects | REQ-DRI-002; R-UNI-24; `tr_declog_append_only`; ADR-009 |
| BR3 | Entries form one chain in `chain_seq` order; `prev_hash` is the `entry_hash` of the entry before, and 64 zeros for the first | REQ-DRI-003; DF-DEC-017, DF-DEC-018 |
| BR4 | `entry_hash` is the SHA-256, in lower-case hexadecimal, of the canonical form: the entry's fields except `entry_hash` and the standard columns, as JSON with keys in alphabetical order, UTF-8, no spaces, timestamps in ISO 8601 UTC with microseconds, numbers as strings and empty fields as null; one implementation serves the store and the verifier | Legacy RWB-E1-008 BR4; ADR-009 |
| BR5 | The append is the last statement of the caller's transaction, so the action and its entry commit or roll back together | Principle 5; R-UNI-39; CTL-06 |
| BR6 | The verifier runs on every append and behind the local access-log read, and a break raises an incident and is reported to Compliance with MSG-P7-008; the daily Schedule, its 15-minute bound and the daily seal stay with `rwb-decision` | NFR-035; REQ-DRI-003; DP-10 |
| BR7 | Retention of entries follows the bank retention schedule; this story deletes nothing | DL26 |
| BR8 | The store is the local library object of DP-03 in schema `rwb_access`, written by the owner and read by the owner only; no service reads another service's store | DP-01; DP-03; Architecture v5 slides 20 and 28 |
| BR9 | `DECISION_LOG` R is required on the local access-log read and on the authorise answer that `rwb-decision` takes before it returns a central entry; the scope is applied through the entry's case, a missing right answers 403 MSG-P4-002 and an out-of-scope entry answers 404 MSG-P4-003 | FSD P4 A2.26 VR-P4-026-1; TSD P4 T6.1 and T6.2; ASM-1726 |
| BR10 | The right is resolved from the `permission` and `role` rows at the matrix version in force, with default deny; no role code, area code, letter or matrix version is written in Java | FSD P4 A2.4; TSD P4 T3.1 (`permission`); DP-07 |
| BR11 | No job, topic, table, interface or file copies this store or the central ledger to a data lake; reporting reads the shared topic | DP-17; Architecture v5 slide 37 |
| BR12 | This service reads no ACE table and no `v_ace_*` view: boundary rule BND-6 fails the build on a view name or a `public` table, and the rwb-access login holds no privilege on either | ADR-010; DP-01; DP-05 |
| BR13 | A failed append leaves nothing behind: the caller's transaction rolls back, the state change does not happen, the `chain_seq` is not consumed and the caller shows MSG-P7-003 | Legacy RWB-E1-008 AC7; R-UNI-39 |
| BR14 | No Temporal Schedule and no workflow sits in this story: DP-10 is carried by the 02:00 chain check of `rwb-decision` (JOB-14) | DP-10; Architecture v5 slide 44 |

### 9. State transitions

`rwb-access` holds no case state machine of its own (TSD P4 T4). This story changes no case, task, role or permission status. The states it owns and observes are the states of a stored entry, of the chain and of a read.

| From | Event | Condition | To |
|---|---|---|---|
| No entry | An append by a decision path of this service | The chain lock is held and the last entry verifies | Entry appended with the next `chain_seq` and the last `entry_hash` as `prev_hash` |
| No entry | An append by a decision path of this service | The canonical form of the last entry does not verify | No entry; the append is refused, an incident is raised and MSG-P7-008 is sent |
| Entry appended | The caller's transaction commits | None | Entry and state change are durable together |
| Entry appended | The caller's transaction rolls back | None | No entry; the `chain_seq` is not consumed |
| A stored entry is wrong | A correction is appended | `corrects_entry_id` names the corrected entry | A second entry exists; the first keeps its value and its position |
| Chain | The verifier runs on a write or on a read | Every hash and every link match | Chain unbroken, head named |
| Chain | The verifier runs on a write or on a read | A hash or a link does not match | Chain broken at the first failing entry; incident raised, MSG-P7-008 sent |
| Read request | The caller's roles are resolved | `DECISION_LOG` R is held and the entry's case is in scope | Entries returned with the verified head |
| Read request | The caller's roles are resolved | R is absent | 403 with MSG-P4-002 and one AC-DENY entry |
| Read request | The caller's roles are resolved | R is held and the entry's case is out of scope | 404 with MSG-P4-003 |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-access service identity (the rwb-access login, DP-02) | Appends entries, holds the chain lock, runs the verifier, resolves the right and writes the refusal entry |
| Every decision path of `rwb-access` (access events of RWB-P4-E1039-APP, the DoA lookup of RWB-P4-E2013-APP, administrative changes of RWB-P4-E1037-APP) | Writes through the store only; no path writes `decision_record` directly |
| RW-AUDIT Internal audit | Reads the local entries under `DECISION_LOG` R (FSD P4 A2.26.3.3) |
| RW-COMPLY Compliance and PDPA officer | Reads the local entries; receives the break report MSG-P7-008 |
| RW-COE Center of excellence analyst | Reads the local entries under `DECISION_LOG` R |
| Every bank role holding `DECISION_LOG` R | Reads the entries inside its scope, and no entry outside it |
| RW-PLATADM Platform administrator | Receives the incident on a break or on a failed append |
| `rwb-decision` (P7) | Takes the authorise answer for area `DECISION_LOG` before returning a central entry; owns the ledger, the ingest and JOB-14 |
| No role | May update or delete an entry, and no role reads an entry outside its scope |

The letters each role holds in `DECISION_LOG` are rows of the permission matrix, not values of this story, and they are Not specified in the source documents (GAP-0984; ASM-1726). The refusal shape is 403 or 404 with an RFC 9457 problem response and `messageId` set; the unauthenticated shape is 401 with MSG-P4-001.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | `decision_record` | all entry fields, including decision code, case reference, inputs reference, recommendation, approver, approval level, final call, actions, outcome and decided at | Write (append), read |
| DF-DEC-028 | `decision_record` | `chain_seq` | Write, read |
| DF-DEC-029 | `decision_record` | `corrects_entry_id` | Write, read |
| DF-DEC-030 | `decision_record` | `actor_user_id` | Write, read |
| DF-DEC-017, DF-DEC-018 | `decision_record` | `prev_hash`, `entry_hash` | Write, read |
| DF-REF-040 to DF-REF-044 | `permission` | `role_id`, `capability_area`, `letters`, `matrix_version`; the `DECISION_LOG` R letter and the version in force | Read |
| DF-REF-034 to DF-REF-039 | `role` | `role_code`, `role_class`, `default_scope`; the scope of an entry's test | Read |
| DF-REF-159 to DF-REF-184 | `reference_version`, `reference_row` of `rwb-case` | `LOV-CAPABILITY` with `DECISION_LOG`, at the version in force | Read through the reference-data contract (DP-07) |
| (outbox) | outbox library table in `rwb_access` | the row of each appended entry, written by the library | Write through the library |
| (inbox) | `processed_event` | none: this story consumes no event | None |
| DF-DEC-001 to DF-DEC-018, DF-DEC-028 to DF-DEC-030 | `decision_log_entry` of `rwb_decision` | none | Not read and not written: the central ledger is P7's |

No row of `case`, `document`, `assignment` or `rule_package` is read, and no foreign key crosses a schema (DP-01). The case reference in an entry is a value the writer recorded, not a join, and it is used for the scope test only. No ACE row and no view column is read or copied: the store holds IDs, codes, references, hashes and times only (BR12).

The column set beyond the five columns this story names, their physical types and the canonical form of the entry are Not specified in the source documents (GAP-0984; ASM-1725); the story takes the entry fields from DF-DEC-001 to DF-DEC-018 of the Logical Data Model and Data Dictionary v9 and fixes the canonical form in BR4. Field IDs are those of the Logical Data Model and Data Dictionary v9.

### 12. Contract

#### 12.1 REST operations provided

None new. The two operations this slice serves the store and the right behind are the ones the Work Package fixes, and this story adds no path, no query parameter and no response field:

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/api/recovery/access/v1/admin/access-log` | The local access log of `rwb_access`, answered from the chain of this story and verified before it is returned | `DECISION_LOG` R, scope applied through the entry's case | Not applicable, read only |
| POST | `/api/recovery/access/v1/authorise` | The authorise answer for area `DECISION_LOG`, right R and a case reference, taken by `rwb-decision` before it returns a central entry | Any authenticated caller; the answer repeats the caller's own right | Idempotent by identity, area, right and case within the cache window |

Errors on both operations: 401 no Workbench role (MSG-P4-001), 403 no `DECISION_LOG` R (MSG-P4-002), 404 entry of a case outside the caller's scope (MSG-P4-003), 503 the store cannot be written or the chain does not verify (MSG-P7-003). The request and answer field names of both operations are published by RWB-P4-E1037-CON and RWB-P4-AD007-CON; this story changes neither schema. That `DECISION_LOG` R, rather than the `PLATFORM_ADMINISTRATION` R that TSD P4 API-P4-008 names for this path, governs the local read in this slice is Not specified in the source documents (GAP-0984; ASM-1726).

#### 12.2 REST operations consumed

None. The caller's identity arrives in the session, the right is resolved from the rows of this service, and the reference list reaches it through the client library of `rwb-case` (DP-07). The one hop and the 2 s budget of DP-11 apply to the inbound calls only.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library, published for each append; consumed by P7 and P9 | `entryId` | the hash-chained entry: entry ID, case reference, decision code, rule ID, rule version, inputs reference, recommendation, approver reference, approval level, final call, actions, outcome, decided at, `prev_hash`, `entry_hash` |

CloudEvents 1.0 envelope in binary mode, IDs and references only, no personal data. The library publishes it; this story adds no topic and no event type of its own, and it publishes no `rwb.access.<Event>.v1` message, because the events of this service are `AccessPolicyChanged` and `DoaLimitChanged` (Architecture v5 slides 14 and 43) and they belong to RWB-P4-E1037-APP.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 (events: none), and the chain of this story is read from its own schema.

#### 12.5 Workflows and activities

None. The append, the verifier and the right answer are synchronous work in the caller's thread. `rwb-access` registers no activity on queue `rwb-access` in this story, and the six-monthly access review list (JOB-18) belongs to RWB-P4-AD008-APP.

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job sits in this story: DP-10 is carried by `rwb-decision`, where the chain check of the central ledger runs at 02:00 as JOB-14 (RWB-P7-E1008-OPS). This slice starts no workflow and registers no Schedule.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `decision_record` | P4 (`rwb_access`) | The local library object of DP-03: the append-only hash-chained store of this service, created by this story's migration |
| `role` | P4 (`rwb_access`) | Read only: the role of the caller and its default scope |
| `permission` | P4 (`rwb_access`) | Read only: the `DECISION_LOG` R letter and the matrix version in force |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | The outbox row of each append (DP-09); no inbox row is written because no event is consumed |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written: the central ledger, its ingest and its chain check are P7's |

`lov_value`, `reference_version` and `reference_row` are reference data of P3 under the ownership ruling and are read through DP-07; no table of another service is read and no foreign key crosses a schema (DP-01). The trigger `tr_declog_append_only` and its function are created in `rwb_access` by this story, and the copy of the same objects in `rwb_decision` is RWB-P7-E1008-DB's.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| decision-record library stub | RWB-PLT-E1027-CON (DP-03) | An empty store, a healthy chain of 102 entries, a broken chain at `chain_seq` 51, a stop on the write path, and the event of one append |
| authorise and permission fake | RWB-P4-E1037-CON | The granted answer for RW-AUDIT with `DECISION_LOG` R and scope ALL, the refused answer for RW-PHONECOL with MSG-P4-002, and the out-of-scope answer with MSG-P4-003 |
| central decision read stub | RWB-P7-E1008-CON | One central entry of case "RW-2026-000123" and the authorise call it makes before it returns |
| reference-data fake | RWB-P3-E1043-CON | `LOV-CAPABILITY` with `DECISION_LOG`, at the version in force |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 0 new (2 served behind); consumed 0 | Base `/api/recovery/access/v1`; the store and the right sit behind the local read and behind the authorise answer; one hop, 2 s |
| Kafka | Published 1 event type; consumed 0 | `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`, through the DP-03 library |
| Temporal | 0 workflows, 0 activities, 0 Schedules | DP-10 is carried by P7's JOB-14; this slice starts no workflow |
| File | None | No file is read or written; no copy of the log leaves the database |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access.record`, module `record`, in the service root `th.co.scb.ace.workbench.recovery.access`. The migration sits in the per-service Flyway sequence of the service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; a gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This is a secondary slice: it adds no new build dependency of its own, and the metadata rows "Depends on (build)" and "Contract dependencies" stay exactly as this Work Package fixes them. The H dependencies of DP-03, DP-07, DP-15 and DP-19 arrive with the platform contract libraries and with the baseline of this service (RWB-P4-E1037-APP and its contract story), and DP-10 adds no dependency here at all because this story starts no Schedule: the only chain check of the estate is P7's JOB-14. DP-01 and DP-17 apply as prohibitions: this service reads no other schema, and no element of the build copies the store to a data lake.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `V1008_1__decision_record.sql` | Migration | Creates `decision_record` in `rwb_access` with the five named columns and the entry fields, the trigger `tr_declog_append_only`, the two indexes and the grants; no update and no delete grant is issued |
| `DecisionRecordRepository` | Repository | Inserts one row and reads a range in `chain_seq` order; the class exposes no update method and no delete method |
| `CanonicalEntryForm` | Service | Builds the canonical JSON of BR4; the one implementation used by the store and by the verifier |
| `DecisionRecordStore` | Service | Takes the chain lock, reads the head, sets `chain_seq` and `prev_hash`, hashes, inserts and releases the lock |
| `HashChainVerifier` | Service | Recomputes a range in `chain_seq` order in batches and reports count, head `chain_seq`, head `entry_hash` and the first break |
| `ChainBreakReporter` | Service | Raises the incident and sends MSG-P7-008 to RW-COMPLY on a break |
| `AccessLogChainReader` | Service | Answers the range of the local access-log read with the verified head in the `chain` field |
| `DecisionLogRightResolver` | Service | Resolves `DECISION_LOG` R from `permission` and `role` at the matrix version in force, applies the scope through the entry's case, and answers 403 or 404 |
| `DecisionRecordEntry` | Entity | Maps `decision_record`; immutable, with no setter |
| `record-modules.yaml` | Rule table | The package name and the allowed source object list of boundary rule BND-6, which is empty for this service |

**Database and migrations**

- Migration `V1008_1__decision_record.sql`, in the `rwb-access` sequence of DP-15, creates `decision_record` in schema `rwb_access` with the entry fields of DF-DEC-001 to DF-DEC-018 and the five named columns `chain_seq` (bigint, not null, unique), `prev_hash` (char(64), not null), `entry_hash` (char(64), not null), `corrects_entry_id` (uuid, references `decision_record` (id)) and `actor_user_id` (uuid); it adds the index `ix_declog_actor_time` on (`actor_user_id`, `decided_at`) and the index `ix_declog_chain` on (`chain_seq`).
- The same migration creates the function that refuses a change and the trigger `tr_declog_append_only` on UPDATE and DELETE, and it revokes UPDATE and DELETE on `decision_record` from the service role.
- The column set beyond the five named columns, their physical types and the choice of a database trigger over a rule are Not specified in the source documents (GAP-0984; ASM-1725); the types above follow the legacy physical schema of the key and are confirmed with the DB story of this service.
- No table of another service is created, altered or read, and no foreign key crosses a schema (DP-01). The copy of the same objects in `rwb_decision` is RWB-P7-E1008-DB's and is not touched here.
- An applied Flyway version is never edited; a change is a new version with a later number.

**Configuration and reference data**

- The chain key of the advisory lock is configuration, per service, and never the key of the central ledger.
- The genesis value is 64 zeros, held as configuration rather than as a literal in code; the canonical form of BR4 is the one implementation of `CanonicalEntryForm`.
- The capability area `DECISION_LOG` and the letters of each role are rows of `permission` and of `LOV-CAPABILITY`, read through DP-07 at the version in force; no area code, role code or letter is a constant (BR10).
- The feature switch is `rwb.access.decision-record`, read as a parameter; off means the append path is closed and the service answers its own message rather than writing an unrecorded decision.
- The login is the rwb-access login (DP-02): Not specified in the source documents (GAP-0984; ASM-1725).

**Build steps**

1. The migration with the table, the trigger, the indexes and the grants, and a fixture that attempts an UPDATE and a DELETE through the service login and as the schema owner; tests for AC1.
2. `CanonicalEntryForm` with golden vectors (a fixed entry to a fixed hash) checked into the test resources, and a fixture that changes one character of the canonical form.
3. `DecisionRecordStore` with the chain lock, the genesis case, the consecutive `chain_seq` and the parallel appends; tests for AC2.
4. `HashChainVerifier` on the write path and on the read path, with the break at `chain_seq` 51 and the refused append after a break; tests for AC2.
5. The correction path with `corrects_entry_id` and the read order; tests for AC3.
6. `DecisionLogRightResolver` and `AccessLogChainReader` behind the two operations, with the scope test through the entry's case; tests for AC4, AC5 and AC6.
7. `ChainBreakReporter` on the ACE incident and notification paths, with MSG-P7-008.
8. The lake-copy guardrail test and boundary rule BND-6 with two fixture classes; tests for AC7 and AC8.
9. A contract-fake run of the whole path, so the story builds before the library contract and the central read contract are published.

**Feature switch.** `rwb.access.decision-record`, read as a parameter. Off closes the append path and fails the guardrail tests; it never allows an unrecorded write.

**Done when.** The tests in section 16 pass, the golden hash vectors give the same result on the build server and on a developer machine, `decision_record` exists in `rwb_access` with the trigger and the grants and no update or delete path, the verifier names the first break on the tampered chain, the local read answers under `DECISION_LOG` R with 403 and 404 as specified, the lake-copy scan finds nothing, and the build is green and red on the two fixtures of the boundary rule.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The caller has no session | Your session has ended. Sign in again to continue. | This story, on both operations |
| MSG-P4-002 | The caller holds no `DECISION_LOG` R | You cannot {action} here. Your role does not include it. | This story, on both operations; one AC-DENY entry |
| MSG-P4-003 | The entry belongs to a case outside the caller's scope | This case is not in your scope. | This story, on both operations |
| MSG-P7-003 | The store cannot be written, or the chain does not verify | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on both operations |
| MSG-P7-008 | The verifier finds a break | The decision log check for {date} found a break at entry {entryId}. Entries from that entry on cannot be relied on until Compliance reviews them. | This story, on a break found on a write or on a read; P7 uses the same text on its 02:00 check |
| Build log | A class names a `v_ace_*` view or a `public` table | Boundary rule BND-6 broken: {class} names {object}. A recovery class names no ACE view and no public table. | This story, in the build |

For MSG-P4-002, {action} names the action the caller tried — "read the access log" or "read a decision record" — and never a case fact or an entry value. The five message texts are copied unchanged from RWB-E1-008 and from the P4 access messages of the legacy model; this story writes no new text. Every error is an RFC 9457 problem response with `messageId` set and `instance` naming the request.

### 15. Screens and states

No screen is built by this story. The local access log is one panel of SCR-43 Roles and access, served by the gateway-bff composite route of DP-19, which calls the read of this story; the central decision-log screen SCR-38 and its audit filters belong to RWB-E2-005 and to `rwb-decision`. This story renders nothing and returns the entries, the verified head and the refusals only.

| Surface | State | What it shows |
|---|---|---|
| SCR-43 Roles and access, access-log panel | List | The local entries under `DECISION_LOG` R, with `chain_seq`, the head and the count verified |
| SCR-43 Roles and access, access-log panel | Chain broken | The first failing entry is named and no entry from that point is shown as verified; the incident reference is with RW-COMPLY |
| SCR-43 Roles and access, access-log panel | Refused | 403 with MSG-P4-002 for a role without R; 404 with MSG-P4-003 for an entry outside the scope |

The field list of the composite route and the rendering of the panel belong to RWB-PLT-N001-CON and to the screen work of the epic, not here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-008-01 | AC1, BR2 | Component | One synthetic entry in `rwb_access`; an UPDATE and a DELETE through the service login and as the schema owner |
| TC-E1-008-02 | AC2, BR3, BR4 | Component | 100 synthetic entries plus two parallel appends, the golden canonical vectors and one entry changed in DEV |
| TC-E1-008-03 | AC2, BR1 | Component | One entry with all seven field groups filled, written and read back through the store |
| TC-E1-008-04 | AC2, BR6 | Component | A chain of 10,000 entries with `chain_seq` 7,412 changed, verified by the verifier on the read path |
| TC-E1-008-05 | AC2, BR3 | Component | Two parallel appends after `chain_seq` 50, asserting consecutive values and the links |
| TC-E1-008-06 | AC3, BR2 | Component | Entry "E-1" with the wrong actor reference and its correction naming "E-1" |
| TC-E1-008-07 | AC1, BR13 | Integration | The store forced to fail inside a transaction that also changes a row: rollback, MSG-P7-003 and no consumed `chain_seq` |
| TC-E1-008-08 | AC4, AC5, BR9 | Contract | RW-AUDIT with `DECISION_LOG` R and scope ALL, and RW-PHONECOL with the letter "-" |
| TC-E1-008-09 | AC5, BR9 | Component | A role without R refused with MSG-P4-002 and one AC-DENY entry |
| TC-E1-008-10 | AC1, BR5, BR13 | NFR | The append forced to fail while the caller's change rolls back; the chain is unchanged |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to Component or Contract as the row shows, Access to Component and Resilience to NFR. Every legacy test case of this key is kept above with the slice of the behaviour this story answers: TC-E1-008-01 answers the append-only rule of this service's store; TC-E1-008-02, TC-E1-008-03 and TC-E1-008-05 answer the chain, the field groups of the row and the parallel appends locally, while the response shape of the two central decision reads stays RWB-P7-E1008-APP; TC-E1-008-04 answers the verifier on the write and read path, while its 02:00 Schedule and the 15-minute report to Compliance are RWB-P7-E1008-APP and re-exercised by RWB-ITG-E1008-ITG; TC-E1-008-06 answers the correction, whose entry shape is also written by RWB-P4-E1039-APP for access events; TC-E1-008-07 and TC-E1-008-10 answer the failed append and the rollback; and TC-E1-008-08 and TC-E1-008-09 answer the right of this service, which RWB-ITG-E1008-ITG re-exercises across services. The `-ITG` copies are not written here: they belong to RWB-ITG-E1008-ITG.

### 17. Guardrails

- No business value in code: the chain key, the feature switch, the genesis value and the retention class are configuration; the capability area and the letters are rows of `permission` and of the reference list, read with the matrix version in force.
- No personal data in the store, in the event, in logs, in workflow inputs or in tests: the entry holds IDs, codes, references, hashes and times only, and every fixture is synthetic.
- One canonical form and one hash implementation for writing and verifying (BR4); a second implementation would make a real break indistinguishable from a hash mismatch.
- No update and no delete path: no repository method, no database grant, no endpoint and no trigger path exists for either, and the tests assert the refusal rather than rely on a review.
- A correction is a new entry and never an edit; the corrected entry keeps its value, its `chain_seq` and its `entry_hash`.
- The store is the owner's own schema object (DP-01, DP-03): no service reads another service's `decision_record`, and the central ledger is P7's.
- No ACE data and no `public` table: a class that names a view fails the build, and the login holds no privilege on either (BR12).
- No copy of the log leaves the database (BR11, DP-17); the lake-copy guardrail is a regression test, not a one-off check.
- No Schedule and no workflow in this story (BR14): DP-10 is P7's JOB-14, and an extra chain check in this service would double the incident path.
- One migration per story in the service's own Flyway sequence (DP-15); an applied version is never edited.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | One record per decision with the seven field groups | Business Requirements Epic 1, section 3.7; Business Requirements Program, section 5.7 | FEAT-DRI-01; FEAT-ACA-08 | 17 Run the decision center | BR1 | TC-E1-008-03 |
| REQ-DRI-002 | Append only; a correction is a new record naming the one it corrects | Business Requirements Epic 1, section 3.7; Business Requirements Program, section 5.7 | FEAT-DRI-01; FEAT-ACA-08 | 17 Run the decision center | BR2, BR5, BR8, BR13 | TC-E1-008-01, TC-E1-008-06, TC-E1-008-07, TC-E1-008-10 |
| REQ-DRI-003 | Hash chained, checked, a break reported to Compliance the same day | Business Requirements Epic 1, section 3.7; Business Requirements Program, section 5.7 | FEAT-DRI-01; FEAT-ADM-10 | 17 Run the decision center | BR3, BR4, BR6 | TC-E1-008-02, TC-E1-008-04, TC-E1-008-05 |

The supporting features of this slice are FEAT-DRI-01 (store decision log entries append-only and hash-chained) and FEAT-ACA-08 (write the access log into the decision log), with FEAT-ADM-10 (detect a broken hash chain) carried on the read side; this slice answers them for `rwb-access` only and changes neither the central ledger design nor the access-log writer design. The rights requirements of the read are carried by the P4 access stories (REQ-ACA-006 and REQ-ACA-007) and are exercised here only for area `DECISION_LOG`.

| Legacy reference | Where it is kept |
|---|---|
| AC1 append only, with the four refused statements | Section 7 AC1, section 4 step 9, section 16 |
| AC2 hash chain of 100 entries and the 64-zero genesis | Section 7 AC2, BR3 and BR4 |
| AC3 the seven field groups on the entry | Section 7 AC2, section 11, section 16 |
| AC4 a break found and reported | Section 7 AC2, BR6, X2 |
| AC5 two appends at the same moment | Section 7 AC2, section 4 step 2 |
| AC6 a correction is a new entry | Section 7 AC3, BR2 |
| AC7 a failed append leaves nothing behind | Section 7 AC1, BR13, X5 |
| AC8 reading an entry needs the Decision log right | Section 7 AC4 and AC5, BR9 and BR10 |
| BR1 to BR7 of the legacy story | Section 8 BR1 to BR7, with BR6 and BR7 narrowed to this service |
| TC-E1-008-01 to TC-E1-008-10 | Section 16 |
| The retired lake copy (legacy RWB-E1-014) | Section 7 AC7, BR11, section 19 |

### 19. Out of scope

- The central `decision_log_entry` of `rwb_decision`, its ingest, the `ingestDecisionRecord` activity, `ChainCheckWorkflow` and the two decision-log read endpoints: RWB-P7-E1008-APP and RWB-P7-E1008-DB.
- The contract and the AsyncAPI document of `rwb.decision-record.v1` and of `rwb.decision-record.DecisionRecorded.v1`: RWB-P7-E1008-CON.
- The 02:00 chain-check Schedule (JOB-14), its 15-minute report to Compliance and the daily ledger seal to write-once storage: RWB-P7-E1008-OPS; this slice starts no workflow and registers no Schedule.
- The access-event writers, the entry shape they write, the AC-READ, AC-DENY and AC-EXPT decision codes in their hands and the break-glass grant with its warning: RWB-P4-E1039-APP.
- The permission matrix as data, the role model, the masking policy and the authorise answer itself: RWB-P4-E1037-APP and RWB-P4-AD002-APP; this story reads the rows and answers for area `DECISION_LOG` only.
- The audit search filters, the paging and the CSV export over the local chain: RWB-P4-AD007-APP; this story supplies the store, the verifier and the right it reads under.
- The screen SCR-43 and its composite route: RWB-PLT-N001-CON and the screen work of the epic; the central screen SCR-38 belongs to RWB-E2-005.
- Retention periods and the deletion of an entry after its retention period: DL26, and no entry is deleted here.
- The end-to-end run across services, the `-ITG` copies of the test cases and the tamper step in a shared environment: RWB-ITG-E1008-ITG.
- The Helm chart, the topic subscription values, the metrics, the alerts and the runbook of this capability: an OPS story of this legacy key.
