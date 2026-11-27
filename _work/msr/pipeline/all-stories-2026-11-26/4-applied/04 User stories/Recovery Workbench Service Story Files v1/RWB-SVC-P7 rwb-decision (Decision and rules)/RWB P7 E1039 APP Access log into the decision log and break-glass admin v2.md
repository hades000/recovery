# RWB-P7-E1039-APP Access log into the decision log and break-glass admin

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: ledger slice of legacy RWB-E1-039 for rwb-decision — the access events of the six codes ingested into `rwb_decision.decision_log_entry`, the grant and the open incident marked on every entry written under a grant, the review due time of a grant, and the audit answer that names the emergency use. The ten legacy criteria stay with RWB-P4-E1039-APP; this slice carries new criteria and adds no legacy criterion. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P7-E1039-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P7-E1039-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-039 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP11, DP13, DP17, DP19 |
| Parallel lane | L-P7-L |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P4-E1039-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-ACA-006, REQ-ACA-008) |
| Status | Draft (realignment v1) |

### 1. Story

As **internal audit, and as the security administrator who reviews emergency access**, I want **every sign-in, refusal, read of a case or a document and export recorded as one entry in the central append-only, hash-chained decision ledger of rwb-decision, with the field IDs and their masking position and never a field value, and every entry written while a break-glass grant is active carrying the grant and the open incident**, so that **"who read this case, and under which emergency grant" is answered from one ledger, and each grant can be reviewed from the record it left**.

**The division of legacy RWB-E1-039 is fixed by this run.** The legacy story was one story in one process: it wrote an access event into the same `decision_log_entry` in the single `recovery` schema through a writer called in process, and it also owned the break-glass grant and the access-log read.

| Story | Owns |
|---|---|
| RWB-P4-E1039-CON | The published contract of the access log and of the grant: the entry shape, the operations, the refusal vocabulary and the fail-closed rule |
| RWB-P4-E1039-APP | The writer in the serving service, the break-glass grant with its time box, the access-log read of `rwb_access`, and the ten legacy acceptance criteria |
| RWB-P4-E1039-DB, RWB-P4-E1039-OPS | The schema of `rwb_access` and the deployment, alerts and run book |
| RWB-P5-E1039-APP | The access event of a document content read, where the document is served |
| **RWB-P7-E1039-APP (this story)** | The ledger's side: the ingest of the six access event codes into `decision_log_entry` in `rwb_decision`, the grant and incident marking, the review due time, and the access answer of the decision-log read |
| RWB-ITG-E1039-ITG | The end-to-end proof of the key across the services that serve the reads and the ledger |

This slice owns no legacy acceptance criterion: the ten criteria of the legacy story belong to RWB-P4-E1039-APP and are kept there word for word and tagged with their origin. The criteria of this story are new (`new, D-RCV-60`) and test only the ledger side named in the title. The store, the writer and the two reads are the other stories of this service and are named where they are relied on, never rebuilt here.

### 2. Business rationale

The bank cannot answer today who read a debtor's record on a given date, and administrators hold standing access to production data. Legacy RWB-E1-039 answered both with one append-only, hash-chained decision log and a break-glass grant that names an incident, ends on its own and marks every action. In the target the log is still one ledger, but it is no longer one table written by one process: every service writes its own decision record in its own schema and publishes it, and rwb-decision keeps the central ledger that audit reads (Architecture v5 slides 28 and 42; ADR-022; DP-03).

That move puts three things on this story. First, the ingest: the ledger has to recognise the six access event codes, keep the shape of an access entry, and apply the rule that an access entry is not a decision about a customer — so the case ID is empty for a sign-in, a refusal, an export and a grant, and no field value is ever carried (legacy section 11, DF-DEC-002; NFR-040). Second, the break-glass record: an activation is an `AC-BGON` entry, a refused activation leaves no `AC-BGON` behind and a refused admin call is an `AC-DENY` entry, and every entry written while a grant is active carries the grant and the incident, so the review of a use reads one entry and sees both (legacy BR4 to BR8; FEAT-ACA-09, FEAT-ACA-10). Third, the answer: the legacy criterion "who read this case over a period" is a query of the ledger with the case, the access code and a period, and its third line is that the entry under a grant names the incident — that query is what makes the whole slice auditable.

The negative side is fixed as tightly as the positive one. No service writes or reads another's tables, so the grant, its time box and the permission matrix stay with rwb-access and the ledger records only what the event carries (DP-01). No personal value in an entry, a log or an event: the field ID and the flag are the clearest facts an entry holds (NFR-040; §17). And the data-lake copy of the log is gone with the lake, so reporting builds its read model from the same events (DP-17; ADR-018).

It meets REQ-ACA-006 and REQ-ACA-008 and supports controls CTL-09 and CTL-11; the measure is unchanged, reads of the case store and the document store written to the access log at 100 percent (NFR-042). Every legacy value used by a criterion is carried unchanged into sections 7, 12.8 and 16, so the fixtures of this slice and of RWB-P4-E1039-APP read the same numbers and identifiers.

The element names the ledger adds to an access entry — the grant, the incident and the review due time — are named by no published schema, the use of the code AC-VERS is described nowhere, and the payload names inside `actions` beyond the legacy list are open; this story builds to the assumption in force and records it as Not specified in the source documents (GAP-2452; ASM-4061).

### 3. Preconditions

- RWB-P4-E1039-CON is published (the one contract dependency of this story, class C, never blocking the build): the `AccessLogEntry` shape, the six access event codes, the grant vocabulary, the refusal reason codes and the fail-closed rule, as an OpenAPI 3.1 document plus its fake.
- The `rwb_decision` schema and login are in place from the service-template work (DP-02), with the base `/api/recovery/decision/v1`, the topics `rwb.decision.events.v1` and `rwb.decision-record.v1`, the task queue `rwb-decision` and the inbox table `processed_event` (DP-09).
- RWB-P7-E1008-APP is in place: `decision_log_entry` in `rwb_decision` with its legacy field identifiers, `chain_seq`, `prev_hash`, `entry_hash`, the append-only trigger, the unique key on the idempotency key and the chain verifier behind the nightly check at 02:00. This story appends and reads those entries and adds no column of its own.
- RWB-P7-E1027-APP is in place: the writer and the `DecisionRecorded` contract of the service, so the payload this story consumes has one shape and no second record type exists.
- The decision-record library of RWB-PLT-E1027-CON is the published baseline, and the producer side of `rwb.decision-record.v1` is each serving service's own writer (RWB-P4-E1039-APP, RWB-P5-E1039-APP): DP-03 and DP-09 are the platform baseline of this slice, and the story record carries no build-order dependency of its own (metadata "Depends on (build)" = None, Template and Rules §R5.7 rules 2 and 3).
- The parameters client of RWB-PLT-E1042-CON and the reference-data client of RWB-PLT-E1043-CON are published, and RWB-P3-E1042-CON and RWB-P3-E1043-CON answer behind them (DP-06, DP-07). The value this story reads is `rwb.access.breakglass.review-days=1`, the legacy assumed value, kept as a parameter (DL38); the review due time is computed from it on the read and never stored (GAP-2452; ASM-4062).
- LOV-DECISION in the rwb-case reference lists holds AC-SIGN, AC-DENY, AC-READ, AC-EXPT, AC-BGON and AC-VERS with their version; the six codes are data and never a constant in code (DP-07).
- The gateway-bff composite route of RWB-PLT-N001-CON carries the decision-log read to the auditor's screen and renders a refusal in the route's problem-detail shape (DP-19).
- The readers hold Decision log R and the producing services hold Decision log C in the capability area; the authorisation decision is the cached permission decision the service template holds from rwb-access, and this story adds no guard of its own.
- Every fixture is synthetic: no production entry, case or grant is copied into a test or a fake.

### 4. Flow

1. A person signs in, or reads a case record, a document or a list, or exports a list. The service that serves the read builds the access event and writes its own decision record in its own schema, in the same transaction as the read answer (RWB-P4-E1039-APP, RWB-P5-E1039-APP).
2. The serving service's outbox relay publishes `DecisionRecorded` on `rwb.decision-record.v1`. The event carries the access event code, the actor reference, the case ID where there is one, the area, the right, the result, the field IDs with their flag, the filter and the row count of a list or export, the document ID, the reason code of a refusal, the grant ID and the incident reference where a grant is active.
3. rwb-decision: `AccessEntryListener` reads the message in the inbox and keeps it only when its decision code is one of the six access codes; every other record is left to the consumer of RWB-P7-E1027-APP. A record already processed is answered with the first entry's ID and counted as a repeat; nothing is appended.
4. `AccessEntryMapper` maps the record to the access shape: the case ID only where the event has a case, an empty case ID for a sign-in, a refusal, an export and a grant; the `actions` element with the area, the right, the result, the field IDs and their flag, the filter and the row count, the document ID, the reason code, the grant ID and the incident reference.
5. `EntryFieldGuard` refuses a record whose `actions` carries a value instead of a field ID, with `MSG-P7-009` naming the element, and nothing is appended; an unauditable read is never recorded as clear data.
6. `AccessEntryWriter` appends one row to `decision_log_entry` in `rwb_decision` through the store of RWB-P7-E1008-APP, with `decision_code`, `actor_user_id`, `case_id`, `decided_at`, `actions`, the idempotency key of the event and the chain link. An entry is never updated and never deleted.
7. For an `AC-BGON` entry, `BreakGlassReviewDue` adds the review due time: `decided_at` plus the parameter `rwb.access.breakglass.review-days`, one working day at the legacy assumed value. For an `AC-DENY` entry the reason code, the area and the right are carried, with no case ID.
8. Internal audit asks `GET /api/recovery/decision/v1/decision-log` with the case ID, decision "AC-READ", `from` and `to`. The read returns the entries in time order with the actor, the time, the field IDs and their flags, and, where the entry was written under a grant, the grant ID and the incident reference.
9. A read of the ledger that cannot be served answers nothing: 503 with `MSG-P7-003`, no item, and an incident to the platform administrator queue. A partial page is never returned.
10. The ingest break is alerted and the message stays on the topic: the retry cadence and the dead-letter topic are the platform's, so an entry either exists in full with its chain link or does not exist at all.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The `actions` of a record carries a field value instead of a field ID | Refused with `MSG-P7-009` naming the element; nothing is appended | MSG-P7-009 | AC1, AC7 |
| X2 | A record carries a decision code outside the six access codes | Not an access entry: it is left to the record consumer and no access entry is appended | None | AC1, AC5 |
| X3 | The same event arrives twice with the same idempotency key | One entry; the first entry ID is answered and the repeat is counted | None | AC7 |
| X4 | The ledger cannot be appended | The message is retried and then parked on the dead-letter topic with its headers; no partial row and no half-written chain link exists | None | AC8 |
| X5 | The ledger cannot be read | 503 with `MSG-P7-003`, no item, no partial page, and an incident to the platform administrator queue | MSG-P7-003 | AC8 |
| X6 | A caller without the Decision log right asks the read | Refused before the query, with no item | MSG-P4-002 | AC6 |
| X7 | A grant activation is refused for a missing field or a short reason | No `AC-BGON` entry exists; the access service owns the 422 and the field name | MSG-GEN-001, MSG-GEN-002 | AC5 |
| X8 | An `AC-BGON` record arrives with no incident reference | Refused with `MSG-P7-009` naming `incidentReference`; a grant entry without an incident is not auditable | MSG-P7-009 | AC4 |
| X9 | The reference list answers late or not at all | The record is retried; the code is never accepted on a guess, and no entry is appended from a failed list read | None | AC1 |

X8 and X9 are the paths this slice adds: the incident reference is the one element a grant entry cannot do without, and the six codes are data, so a list that cannot answer cannot validate a code.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P4-E1039-CON, the store of RWB-P7-E1008-APP, the writer of RWB-P7-E1027-APP and the platform contracts of the baseline |
| Negotiable | The element names inside `actions`, the grant and incident elements of the answer and the review due time are the open points of the assumption; the shape of the entry and the prohibition on values are fixed |
| Valuable | One ledger answers who saw what and when and names the emergency use, and each grant is reviewed from the entry it left |
| Estimable | One listener, one mapper, one guard, one review calculation, one query and one index |
| Small | Fits one week with its tests, as the ledger slice of the legacy key |
| Testable | Each criterion of section 7 is one test of section 16, run against the fakes of section 12.8 |

### 7. Acceptance criteria

```gherkin
Feature: Access log into the decision log and break-glass admin - the ledger of rwb-decision

  Background:
    Given the environment is SIT
    Given the ledger of rwb_decision is available

  Scenario: AC1 A case read is one entry with masked field IDs (new, D-RCV-60)
    Given the rwb-access contract mock returns the access event of test user "U-4101" holding RW-CASEOWN reading case "RW-2026-000123" at 10:15 on 3 December 2026, with field IDs DF-PTY-007 and DF-PTY-016 marked "masked"
    When the DecisionRecorded event of that read arrives on topic "rwb.decision-record.v1"
    Then one entry exists with decision code "AC-READ", actor "U-4101", the case ID and decided at 10:15
    Then its actions list the field IDs with DF-PTY-007 and DF-PTY-016 each flagged "masked", and no field value
    Then the entry carries chain_seq, prev_hash and entry_hash from the chain

  Scenario: AC2 An export is one entry with no case ID (new, D-RCV-60)
    Given the rwb-access contract mock returns the access event of test user "U-4103" holding RW-TEAMMGR exporting a case list filtered by status "ASSIGNED" and product "MORTGAGE" with 37 rows
    When the DecisionRecorded event of that export arrives on topic "rwb.decision-record.v1"
    Then one entry exists with decision code "AC-EXPT", actor "U-4103" and an empty case ID
    Then its actions carry the filter, the row count 37 and no field value

  Scenario: AC3 A document read names the case and the document (new, D-RCV-60)
    Given the rwb-access contract mock returns the access event of test user "U-4101" reading document "DOC-2026-0009981" on case "RW-2026-000123"
    When the DecisionRecorded event of that read arrives on topic "rwb.decision-record.v1"
    Then one entry exists with decision code "AC-READ", the case ID and document "DOC-2026-0009981" in its actions
    Then the entry is appended before the read answer is released, because the serving service commits it in the same transaction

  Scenario: AC4 A break-glass activation is one entry and marks every entry under the grant (new, D-RCV-60)
    Given incident "INC0004521" is open and test user "U-4102" holding RW-PLATADM activated break-glass at 10:30 for area "CASE_RECORD", right "U" and scope "ALL" under IAM request "IAM-778812", the grant ending at 14:30
    When the DecisionRecorded events of that activation and of two reads by "U-4102" at 14:20 and 14:25 arrive on topic "rwb.decision-record.v1"
    Then one entry exists with decision code "AC-BGON", actor "U-4102" and an empty case ID
    Then its actions carry incident "INC0004521" and the grant ID, and the entry carries a review due time of one working day after 10:30 from parameter "rwb.access.breakglass.review-days"
    Then the two read entries carry the same grant ID and incident "INC0004521"

  Scenario: AC5 A refused activation writes no AC-BGON entry and a refusal is an AC-DENY entry (new, D-RCV-60)
    Given test user "U-4104" holds RW-PLATADM and is not in group "RWB-SIT-BREAKGLASS"
    When the access service refuses the activation with MSG-P4-007 and publishes the refusal event
    Then no entry with decision code "AC-BGON" exists for "U-4104"
    Then one entry exists with decision code "AC-DENY", actor "U-4104", area "PLATFORM_ADMINISTRATION", right "R" and reason "NO_BREAKGLASS_GRANT" in its actions, with no case ID
    Then when an activation is refused with MSG-GEN-001 for field "incidentReference" or MSG-GEN-002 for field "reason", no entry of that activation is written at all

  Scenario: AC6 The audit answer names the break-glass use (new, D-RCV-60)
    Given three entries exist for case "RW-2026-000123" on 3 December 2026: a read by "U-4101" at 10:15, a read by "U-4102" at 11:02 under the grant of incident "INC0004521", and a read by "U-4101" at 16:40
    When test user "U-4105" holding RW-AUDIT calls GET /api/recovery/decision/v1/decision-log with the case ID, decision "AC-READ", from "2026-12-03" and to "2026-12-03"
    Then three items return in time order with actor, time, the field IDs and their flags
    Then the 11:02 item carries incident "INC0004521" and its grant ID
    Then a caller without the Decision log right is refused with MSG-P4-002 and no item

  Scenario: AC7 A repeated event gives one entry (new, D-RCV-60)
    Given the read entry of case "RW-2026-000123" at 10:15 exists with an entry ID and chain_seq 412
    When the same DecisionRecorded event arrives again with the same idempotency key
    Then one entry exists for that event
    Then the consumer answers the first entry's ID and adds one to the repeat count
    Then no second chain_seq and no second entry_hash is written

  Scenario: AC8 A ledger that cannot be read answers nothing (new, D-RCV-60)
    Given the ledger store is unavailable
    When test user "U-4105" holding RW-AUDIT calls GET /api/recovery/decision/v1/decision-log for case "RW-2026-000123"
    Then the call returns status 503 with message MSG-P7-003 and no item
    Then no partial page returns and an incident is raised to the platform administrator queue
    Then with the ingest stopped, every entry of the period either exists in full with its chain link or does not exist at all
```

The eight criteria are new: no line of them is a legacy criterion, and each one tests only the ledger side of the key. Where a criterion names a fact another owner holds — the read, the export, the document, the grant and its end time, the refusal — the line states the answer of that owner's contract mock and the legacy values are carried unchanged. The ten legacy criteria of RWB-E1-039 are delivered by RWB-P4-E1039-APP and the cross-service journey by RWB-ITG-E1039-ITG.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every access event of the six codes is one entry in the ledger, appended once, never updated and never deleted | REQ-ACA-006; NFR-042; FEAT-ACA-08; legacy BR1 |
| BR2 | The case ID is present only where the event has a case: it is empty for a sign-in, a refusal, an export and a grant activation | Legacy section 11, DF-DEC-002 |
| BR3 | An entry lists field IDs and their masking flag, never a field value; the clearest facts it may hold are the case ID, the document ID, the field ID, the flag, the filter, the row count, the grant ID and the incident | NFR-040; legacy BR3 |
| BR4 | Every entry written while a grant is active carries the grant ID and the incident reference in its `actions` | Admin and access model 5.3; legacy BR6; FEAT-ACA-09 |
| BR5 | An `AC-BGON` entry carries the incident, the grant, the area, the right, the scope and a review due time computed from the review-window parameter; the ledger records the grant and does not enforce it | Legacy BR4, BR5, BR7; FEAT-ACA-10 |
| BR6 | A refused admin call is an `AC-DENY` entry with the area, the right and the reason code, and no case ID | Legacy BR1, BR8; FEAT-ACA-07 |
| BR7 | The same event with the same idempotency key gives one entry, and the repeat is counted | R-UNI-40; DP-09 |
| BR8 | The ledger is append only and hash chained, and the chain is verified nightly at 02:00 by the store story | Principle 5; R-UNI-39; FEAT-DRI-01 |
| BR9 | An entry that cannot be appended is not partially stored: the message is retried and then parked with its headers | Principle 5; DP-09 |
| BR10 | An access entry arrives on `rwb.decision-record.v1`; no service writes `decision_log_entry` from outside rwb-decision and no field value crosses the topic | DP-01; DP-03; ADR-022 |
| BR11 | The six codes, the areas, the scopes and the roles are reference data with a version, and the review window is a parameter; neither is a constant in code | DP-06; DP-07; legacy section 17 |

### 9. State transitions

No case status changes in this story, and the ledger holds no grant state: the grant lives in rwb-access and the ledger records what each event says about it. The entry has the states below and no other.

| Object | From | Event | To | Result |
|---|---|---|---|---|
| Access entry | NONE | A `DecisionRecorded` of the period arrives | MAPPED | The code, the case, the actor and the `actions` are mapped; nothing is stored yet |
| Access entry | MAPPED | The `actions` carries a field ID and a flag | VALIDATED | The chain link is read and the append is prepared |
| Access entry | VALIDATED | The append commits | APPENDED | One row with `chain_seq`, `prev_hash` and `entry_hash`; never updated, never deleted |
| Access entry | MAPPED | The `actions` carries a value | REFUSED | `MSG-P7-009` names the element and nothing is appended |
| Access entry | APPENDED | The same event arrives again | REPEATED | The first entry ID is answered and the repeat is counted |
| Access entry | VALIDATED | The store cannot append | RETRIED | The message is retried and then parked on the dead-letter topic; no partial row exists |
| Grant entry | APPENDED | The review window after `decided_at` passes | DUE FOR REVIEW | The read answers the review due time; no state is written by the ledger |
| Read answer | REQUESTED | The store answers | RETURNED | Items in time order with the grant and the incident where the entry carries them |
| Read answer | REQUESTED | The store does not answer | REFUSED | 503 with `MSG-P7-003`, no item, one incident |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AUDIT Internal audit | Reads the ledger for a case, an access code and a period; changes nothing |
| RW-SECADM Security administrator | Reads the ledger and reviews each break-glass use from the `AC-BGON` entry and the entries it marks |
| RW-COMPLY Compliance and PDPA officer | Reads the ledger; receives an unreviewed use through the channel of Epic 8 |
| RW-COE, RW-DATASTEW | Read the access entries with the Decision log R right |
| The producing services of the workbench | Publish their own access records on `rwb.decision-record.v1`; they never read or write `decision_log_entry` (DP-01) |
| The rwb-decision service identity | Appends and reads the entries of `rwb_decision` (DP-02) |
| RW-PLATADM Platform administrator | Receives the incident of a failed ingest or a failed read; operates the run from the alerts of the OPS story |
| No delegation of authority level applies | An access entry records an access, not a credit decision; the ledger applies no limit |

No personal name, e-mail address or credential appears in this story, its examples or its fixtures; every actor is a role code or a test user reference.

### 11. Data

| BR Field ID | Entity in `rwb_decision` | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write, one entry per access event |
| DF-DEC-002 | decision_log_entry | case_id | Write; empty for a sign-in, a refusal, an export and a grant |
| DF-DEC-003 | decision_log_entry | decision_code | Write, read: the access code of the entry and the query filter |
| DF-DEC-014 | decision_log_entry | actions | Write, read: area, right, result, field IDs with the flag, filter, row count, document ID, reason code, grant ID, incident reference |
| DF-DEC-016 | decision_log_entry | decided_at | Write, read: the time order of the answer and the base of the review due time |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write, read |
| DF-REF-028, DF-REF-029 | lov_value, through the rwb-case contract | lov_code, value_code | Read: the six access codes of LOV-DECISION |
| Standard column | decision_log_entry | chain_seq, prev_hash, entry_hash | Write, through the store of RWB-P7-E1008-APP |
| Standard column | processed_event, idempotency_key | processed id, stored answer | Write, read, through the outbox and inbox library (DP-09) |

Field IDs are those in the Logical Data Model and Data Dictionary. The migration is one per-service Flyway step in the `rwb_decision` sequence (DP-15): `V1039_1__access_ledger.sql` adds the index on `(decision_code, decided_at)` and the index on `(case_id, decision_code, decided_at)` where the store does not already carry them, and it creates no table and no column.

The ledger holds no personal data: the actor is a role code or a user identifier, the subject is a case, document or entry identifier, and `actions` holds field IDs, flags, filters and counts. The review due time is computed and never stored, so the review window changes for tomorrow's entries without a data migration. The retention of the entries is the store story's and the access entries are not carved out of it.

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Status | Used for |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/decision-log` | Declared by API-P7-006; owner P7 | The access answer: `caseId`, `decision` "AC-READ", `from` and `to`, with `page` and `size` of the standard query, items in time order with actor, time, field IDs and flags, and the grant ID and incident reference where the entry carries them |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | Declared by API-P7-007; owner P7 | One access entry as it was appended, for the review of a single use |

This slice adds no path and no query parameter. It fixes what an access entry means on the read, and it answers three elements the published document does not name — `grantId`, `incidentReference` and the review due time of an `AC-BGON` item — which are taken from the assumption in force (GAP-2452; ASM-4061). Both paths answer 401 through the gateway-bff session envelope, 403 without Decision log R with `MSG-P4-002`, 422 for a period that ends before it starts and 503 when the store cannot be read.

#### 12.2 REST operations consumed

| Method and path | Owner | Use in this story | Contract |
|---|---|---|---|
| GET `/api/recovery/case/v1/admin/parameters/{code}` | P3 rwb-case | `rwb.access.breakglass.review-days` for the review due time of a grant entry | RWB-P3-E1042-CON (C) |
| GET `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-DECISION for the six access codes and their version | RWB-P3-E1043-CON (C) |

No operation of rwb-access, rwb-document or rwb-case's case read is consumed: the access facts arrive on the topic, and the grant, the matrix and the masking policy stay with their owners. RWB-P4-E1039-CON is consumed as the published record shape and its fake and not as a call. Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (DP-11, ADR-020). A missing list answer refuses the record rather than accepting a code on a guess (BR11). The parameter path and the element names inside the `actions` element are Not specified in the source documents beyond the legacy names (GAP-2452; ASM-4060).

#### 12.3 Events published

None. The ledger is the consumer of the record topic and does not republish what it stores. The service's own topic `rwb.decision.events.v1` carries the approval and rule events of RWB-P7-E2013-APP and RWB-P7-E1073-CON and nothing of this story, and nothing is forwarded to a lake or a file (DP-17).

#### 12.4 Events consumed

| Event | Topic | Producer | Handling |
|---|---|---|---|
| DecisionRecorded (EV-08) | `rwb.decision-record.v1` | All 19 services, through the decision-record library (RWB-PLT-E1027-CON, DP-03) | The six access codes are mapped and appended; every other record is left to the record consumer; idempotent on the event's key; a record that fails the access schema is retried and then parked on the dead-letter topic with its headers |

The envelope and the key are the library's (DP-09). The retry cadence and the dead-letter policy are the event platform's and this story configures no policy of its own.

#### 12.5 Workflows and activities

None. The ingest is a message consumer and the read is synchronous code in a REST handler. This story starts no workflow, registers no activity and holds no Quartz job; the task queue `rwb-decision` serves the other stories of the service (DP-10).

#### 12.6 Schedules

None. The nightly chain check at 02:00 is the store story's, and the review of a break-glass use is a person's act measured by a computed due time, not a scheduled job. The legacy Quartz rows are retired for this service (DP-10; Template and Rules §R6), so this story declares no cron entry and no shared scheduler row.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `decision_log_entry` | P7, in `rwb_decision` | The entry of every access event: the legacy field identifiers, the `actions` element, the chain columns and the decided-at time. Appended and read only |
| `processed_event` | PLT library, created in `rwb_decision` | The inbox that makes the ingest idempotent (DP-09) |
| `idempotency_key` | PLT library, created in `rwb_decision` | The stored answer of the event key and of a repeated read |
| `outbox_event` | PLT library, created in `rwb_decision` | Created with the schema; this story writes no row to it, because it publishes nothing |

No `rwb_access`, `rwb_case`, `rwb_document` or `rwb_reporting` table is read and no `v_ace_*` view is read (DP-01, DP-05). `role`, `permission`, `masking_rule` and `break_glass_grant` are P4's and this story holds no grant on them.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-access contract fake (RWB-P4-E1039-CON) | The shape of an access event and its refusal vocabulary | One read of case `RW-2026-000123` at 10:15 by `U-4101` with DF-PTY-007 and DF-PTY-016 masked; an export of 37 rows by `U-4103`; a document read of `DOC-2026-0009981`; an activation by `U-4102` with incident `INC0004521`, IAM request `IAM-778812`, area `CASE_RECORD`, right `U`, scope `ALL`, ending 14:30; two reads under the grant at 14:20 and 14:25; a refusal of `U-4104` with reason `NO_BREAKGLASS_GRANT`; a refusal of `U-4106` with area `PLATFORM_ADMINISTRATION` and right `R`; a field value in `actions`; a missing `incidentReference` |
| decision-record fixture (RWB-PLT-E1027-CON) | The `DecisionRecorded` payload and the key | The same events as records, one repeated with its key, one with a decision code outside the six codes, one with a slow delivery past the retry budget |
| Parameters fake (RWB-P3-E1042-CON) | The parameter read | `rwb.access.breakglass.review-days` = 1 with its version; an absent key; a slow answer past 2 s |
| Reference-data fake (RWB-P3-E1043-CON) | The list read | LOV-DECISION at version REF-2026.11 with the six codes and one code outside the list; a slow answer past 2 s |
| Ledger fixture (RWB-P7-E1008-APP) | `decision_log_entry` and its chain | Three entries of case `RW-2026-000123` on 3 December 2026 at 10:15, 11:02 and 16:40, the middle one carrying the grant and the incident; an entry at chain_seq 412 for the repeat; a store closed for the failed read |

The values are the legacy values of RWB-E1-039, kept unchanged so that the component, contract and integration assertions read the same fixtures; the fixtures carry no personal data. The element names inside the `actions` element and the three read elements of 12.1 are stubbed from the assumption and are Not specified in the source documents (GAP-2452; ASM-4061).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The decision-log read and the entry read on base `/api/recovery/decision/v1`; the parameter and list reads of rwb-case, one hop each within 2 s |
| Kafka | 0 published, 1 consumed | DecisionRecorded (EV-08) on `rwb.decision-record.v1`; nothing on `rwb.decision.events.v1` from this story |
| Temporal | None | No workflow, activity or Schedule; queue `rwb-decision` serves the other stories |
| File | None | No file is read or written, and the lake copy of the access log is removed (DP-17) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `accessledger`, Java package `th.co.scb.ace.workbench.recovery.decision.accessledger`; the artefact is the `rwb-decision` api deployment of the service template.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_decision`; never read another service's tables. The grant, the matrix and the masking policy stay with rwb-access and the document with rwb-document | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the ledger consumes what the serving services write | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library; the review window is a parameter row | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case; the six access codes arrive with their version | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout. The monolith's in-process call to the writer becomes the event on the topic, and the two data reads are one hop each | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/decision/v1`; every path of this story sits under the service base | none |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting. The lake copy of the access log and its read logging leave with the lake | none; no lake data is needed |
| DP-19 | Screen, ace-web | gateway-bff composite route for the decision-log read and the refusal shape | H RWB-PLT-N001-CON |

No pattern is claimed for DP-02, DP-04, DP-05, DP-08, DP-09, DP-10, DP-12, DP-14, DP-15, DP-16, DP-18 or DP-20: this story creates no login and no migration, evaluates no Drools package, reads no ACE view, declares no authorise call of its own, configures no topic name and no Schedule, runs no per-case workflow, calls no adapter, writes no ledger entry of the interaction ledger and calls no agent. The four H rows are platform contracts consumed as the published baseline: the story record carries no build-order dependency of its own (metadata "Depends on (build)" = None, §R5.7 rules 2 and 3).

**Hardware and software change.** The access log leaves one shared table in the single `recovery` schema, written in process by every module through one writer. Each serving service now writes its own record and publishes it, and the central ledger of rwb-decision keeps the auditable copy of every access event in `rwb_decision` with its chain. No new hardware is implied: the ingest runs in the existing `rwb-decision` pods, the entries live in the ACE PostgreSQL server under the `rwb_decision` schema and login, and the topic is the Kafka platform ACE already runs. The data-lake copy disappears with the lake.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `AccessEntryListener` | Inbox consumer | Consumes `DecisionRecorded`, keeps the six access codes, recognises a repeat by the event key and parks a record that fails the access schema |
| `AccessEntryMapper` | Service | The case-ID rule of BR2, the `actions` element of BR3, and the grant and incident marking of BR4 |
| `EntryFieldGuard` | Service | Refuses an `actions` element that carries a value instead of a field ID, with `MSG-P7-009` |
| `AccessEntryWriter` | Service | Appends one entry with its chain link through the store of RWB-P7-E1008-APP; never updates and never deletes |
| `BreakGlassReviewDue` | Service | Computes the review due time of a grant entry from `decided_at` and the review-window parameter (BR5) |
| `AccessLedgerQuery` | Service | The query behind the decision-log read for an access code and a period, with the grant and incident elements and the time order |
| `AccessCodeCatalog` | Service | Reads the six codes from LOV-DECISION with their version and refuses an unknown code (BR11) |

**Database and migrations.** One Flyway step in the `rwb_decision` sequence (DP-15), `V1039_1__access_ledger.sql`: the index on `(decision_code, decided_at)` for the period query and the index on `(case_id, decision_code, decided_at)` for the case answer, where the store does not already carry them. No column, no table and no seed: the six codes are reference data of rwb-case and the review window is a parameter.

**Configuration and reference data.** `rwb.access.breakglass.review-days=1` through the parameters client (DP-06), and LOV-DECISION through the reference client (DP-07), each with its version. Nothing else is configured: no retention value, no page size and no tolerance is set here.

**Build steps**

1. `AccessEntryListener` against the record fixture, with the six codes, one record outside them and one repeated key; tests for AC1 and AC7.
2. `AccessEntryMapper` with the case-ID rule and the `actions` element of a read, an export, a document read and a grant; tests for AC1, AC2, AC3 and AC4.
3. `EntryFieldGuard` and the refusal of a value in `actions`, with `MSG-P7-009` and nothing appended (X1).
4. `AccessEntryWriter` over the store of RWB-P7-E1008-APP, asserting the chain link on two consecutive entries and no update path.
5. `BreakGlassReviewDue` with a clock fixed at 10:30 and the parameter fake; test for AC4.
6. `AccessLedgerQuery` with the period validation, the time order and the grant and incident elements; tests for AC6.
7. The refused paths: no `AC-BGON` on a refused activation, the `AC-DENY` entry of a refusal, and the 422 case that writes nothing (AC5).
8. The failed store: the retry, the parked message and the 503 read with `MSG-P7-003` and no partial page (AC8).

**Done when.** The tests of section 16 pass, every access event of the period is in the ledger once with its chain link, the grant and the incident are on every entry written under a grant, the review due time is answered for a grant entry, the audit answer of a case names the emergency use, and the access entries of a business date reconcile one for one with the `DecisionRecorded` messages of the topic.

### 14. Validation and messages

| ID | When | Message | Raised as |
|---|---|---|---|
| MSG-P7-003 | The ledger cannot be read, or an entry cannot be appended | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The read answer 503, and the incident of the ingest |
| MSG-P7-009 | A record is refused for a missing or invalid element (written to the service log and the incident, never shown to a customer) | The decision record was refused: {field} is missing or not valid. | `DecisionRecordInvalidException`, with `field` |
| MSG-P4-002 | The caller lacks Decision log R on the read | You cannot {action} here. Your role does not include it. | The service guard, before the query |
| MSG-GEN-002 | Page size outside 1 to 500 on the read | {field} must be between {min} and {max}. | The read validation |

The ids and the texts are copied unchanged from legacy RWB-E1-039 and this story adds no message of its own. The field names of the refusals are `actions`, `incidentReference` and `decisionCode`. MSG-P4-004 and MSG-P4-007 belong to rwb-access and are named here only as the answers the fake returns. The published catalogue entry format of MSG-P7-009 is Not specified in the source documents (GAP-2452; ASM-4063). Thai text for each follows DL10.

### 15. Screens and states

No screen is built in this story. The entries are read through the two operations of 12.1 under `/api/recovery/decision/v1`, reached through the gateway-bff composite route (DP-19).

| Screen | What it shows from this story | State |
|---|---|---|
| SCR-38 Decision log query (Epic 2, RWB-P7-E2005-APP) | One access entry with actor, time, field IDs and flags, and the grant and incident where the entry carries them | Returned |
| SCR-38 Decision log query | The period answer of a case with the reads in time order and the emergency use named | Returned, empty |
| SCR-38 Decision log query | The refusal of a caller without Decision log R, and the 503 of an unreadable ledger | Refused, failed |
| SCR-43 Roles and access (Epic 8, rwb-access) | Not this story: the access log of `rwb_access` is P4's read | Out of scope here |

The screen's composition, its masking and its timeout budget belong to RWB-PLT-N001-CON and to RWB-P7-E2005-APP and are not fixed here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-039-01 | AC1, BR1, BR2, BR3: a case read is one entry with the field IDs masked and no field value | Integration | Synthetic case RW-2026-000123 read at 10:15 by U-4101 with DF-PTY-007 and DF-PTY-016 masked |
| TC-E1-039-02 | AC4, BR4, BR5: the activation is one AC-BGON entry, the review due time is answered and the two later reads carry the grant and the incident | Integration | Incident INC0004521, IAM request IAM-778812, grant ending 14:30, reads at 14:20 and 14:25, review-days 1 |
| TC-E1-039-03 | AC2, BR1, BR2: an export is one entry with the filter and 37 rows and no case ID | Integration | Case list filter by status ASSIGNED and product MORTGAGE returning 37 synthetic cases |
| TC-E1-039-04 | AC3, BR1: a document read names the case and the document and is appended before the answer is released | Contract | Synthetic document DOC-2026-0009981 on case RW-2026-000123 |
| TC-E1-039-05 | AC5, BR6: a refusal without a grant writes no AC-BGON entry and its AC-DENY entry carries the reason | Component | RW-PLATADM test user outside the break-glass group; refusal with MSG-P4-007 |
| TC-E1-039-06 | AC5, BR6: an activation refused for the incident field or the reason length writes no entry at all | Contract | Missing incident reference; 12-character reason |
| TC-E1-039-07 | AC8, BR3, BR9: a ledger that cannot be read answers 503 with no item, and an append that fails leaves no partial row | NFR | Store switched off in the test double, and the append forced to fail |
| TC-E1-039-08 | AC6, BR4: the three reads of one case return in time order and the 11:02 item carries the incident | Integration | Three reads of one case on 3 December 2026 |
| TC-E1-039-09 | AC5, BR6: a refusal of an admin call is an AC-DENY entry with the area, the right and no case ID | Component | RW-PHONECOL test user calling an admin operation |
| TC-E1-039-10 | AC7, BR7, BR8: a repeated event gives one entry and answers the first entry ID | Component | Two deliveries of one event with the same key; entry at chain_seq 412 |
| TC-E1-039-11 | AC6, BR1: a role without Decision log R reads nothing and is refused with MSG-P4-002 | Component | A role without the right calling the decision-log read |
| TC-E1-039-12 | AC8, BR9: the ingest is stopped for the period, so no entry exists half written and no partial answer returns | NFR | Store closed for the whole period; record parked with its headers |

The twelve ids are the legacy ids of this key, kept in the legacy order with their data unchanged; the covers are the criteria of this slice, because the legacy criteria are delivered by RWB-P4-E1039-APP. Legacy level System is answered at Integration or Contract for the slice this story owns, Access at Component and Resilience at NFR. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case id; the cross-service copy of the journey is RWB-ITG-E1039-ITG and sits there, not here.

### 17. Guardrails

- No business value in code: the six access codes, the areas, the scopes and the roles are list values with a version, and the review window is a parameter.
- No personal data in an entry, a log, an event, a test or a prompt: an entry carries the case ID, the document ID, the field ID and the flag, never a value, and the `actions` element is refused if a value appears in it.
- No read of another service's tables: the access facts arrive on the topic, the codes and the parameter arrive through the rwb-case contract, and a boundary test fails the build on a cross-schema reference.
- No write path to `decision_log_entry` other than the writer of this service, checked by an architecture test; the ledger has no update and no delete at all.
- No enforcement of the grant in the ledger: the time box, the group membership and the matrix are rwb-access's, and the ledger records what the event states.
- No personal data in the incident of a failed ingest: the incident carries the entry id, the message key and the field name only.
- No data-lake sink and no reporting copy: the legacy lake copy is retired and reporting follows the events (DP-17).
- The ingest is idempotent on the event key: a build that appends before checking the key fails the repeat test.
- Every example and fixture is synthetic; no production payload is copied into a test or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-006 | Every read of the case store and the document store written to the access log | Epic 1, 3.4 | FEAT-ACA-07, FEAT-ACA-08, FEAT-ACA-16 | 16 Manage risk, control and compliance; 17 Run the decision center | BR1, BR2, BR3, BR8, BR10, BR11 | TC-E1-039-01, TC-E1-039-03, TC-E1-039-04, TC-E1-039-07, TC-E1-039-12 |
| REQ-ACA-008 | Break-glass with its own approval, written to the access log | Epic 1, 3.4 | FEAT-ACA-09, FEAT-ACA-10 | 16 Manage risk, control and compliance; 17 Run the decision center | BR4, BR5, BR6, BR9 | TC-E1-039-02, TC-E1-039-05, TC-E1-039-06, TC-E1-039-08, TC-E1-039-09, TC-E1-039-10, TC-E1-039-11 |

| Element | Where it is fixed | Test cases |
|---|---|---|
| DP-01, DP-13 | The base of 12.1 and the owned and not-owned lists of 12.7 | TC-E1-039-01, TC-E1-039-11 |
| DP-03 | The consumed topic of 12.4 and BR10 | TC-E1-039-01, TC-E1-039-10 |
| DP-06 | The review due time of BR5 and the parameter row of 12.2 | TC-E1-039-02 |
| DP-07 | The list row of 12.2 and BR11 | TC-E1-039-01, TC-E1-039-09 |
| DP-11, DP-19 | The one-hop budget of 12.2 and the route of 15 | TC-E1-039-04, TC-E1-039-11 |
| DP-17 | BR1 and the retired lake copy | TC-E1-039-07 |
| ADR-014, ADR-020, ADR-022 | The schema and login, the one-hop budget and the local-record model | TC-E1-039-01, TC-E1-039-04 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P4-E1039-CON | Contract | C: the access entry shape and the refusal vocabulary, read as a fake and never blocking |
| RWB-P7-E1008-APP | App development | The store, the chain and the append-only rule this story appends to |
| RWB-P7-E1027-APP | App development | The writer and the `DecisionRecorded` shape of the service |
| RWB-P7-E2005-APP | App development | The two read operations of 12.1 that carry this story's answer |
| RWB-P4-E1039-APP, RWB-P5-E1039-APP | App development | The producers of the access events and the ten legacy criteria |
| RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-N001-CON | Contract | H: the library, the two clients and the route of the baseline |
| RWB-P3-E1042-CON, RWB-P3-E1043-CON | Contract | C: the parameter and the list behind the clients |
| RWB-ITG-E1039-ITG | Integration | The end-to-end proof across the producers and the ledger |

### 19. Out of scope

- The access writer and the fail-closed rule in the serving services, the break-glass grant with its time box and the access-log read of `rwb_access` (RWB-P4-E1039-APP).
- The published contract of the access log and of the grant, its fakes and its drift test (RWB-P4-E1039-CON).
- The tables, grants, retention and partitions of `rwb_access` (RWB-P4-E1039-DB) and the deployment, alerts and run book (RWB-P4-E1039-OPS).
- The access event of a document content read, where the document is served (RWB-P5-E1039-APP).
- The store, the append-only rule, the chain verifier and the nightly check at 02:00 (RWB-P7-E1008-APP), and the writer (RWB-P7-E1027-APP).
- The two read operations themselves and the screens that show them (RWB-P7-E2005-APP; SCR-38 is Epic 2).
- The permission matrix, the masking policy and the sign-in (RWB-P4-E1037-APP, RWB-P4-E1022-APP).
- The break-glass request, approval and review records, which the bank IAM holds, and the scheduled alert of an unreviewed use to the head of SCB IT security and Compliance (Epic 8, FEAT-ADM-12).
- The data-lake copy of the access log and its retention (retired under DP-17; no data lake in Arch v5).
- The Roles and access screen SCR-43 (Epic 8) and the gateway-bff composite route's composition, masking and timeout budget (RWB-PLT-N001-CON).
