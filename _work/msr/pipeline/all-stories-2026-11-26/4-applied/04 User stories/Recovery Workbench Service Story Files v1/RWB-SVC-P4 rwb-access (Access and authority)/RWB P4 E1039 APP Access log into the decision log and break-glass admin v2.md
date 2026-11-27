# RWB-P4-E1039-APP Access log into the decision log and break-glass admin

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: app slice of legacy RWB-E1-039 for rwb-access — the access event writer, the break-glass grant and the access-log read, with every entry written through the local decision-record library. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-E1039-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-E1039-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-039 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP11, DP13, DP17, DP19 |
| Parallel lane | L-P4-A |
| Ready to start | After RWB-P4-E1022-APP |
| Depends on (build) | RWB-P4-E1039-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-N001-CON, RWB-P4-E1022-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P7-E1008-CON, RWB-P7-E1027-CON |
| Integration dependencies | None |
| External dependencies | RWB-P4-E1039-DB, RWB-P4-E1039-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (FR-P4-023, FR-P4-024, FR-P4-025, FR-P4-026, FR-P4-027, FR-P4-028, FR-P4-029, FR-P4-030, FR-P4-031) |
| Status | Draft (realignment v1) |

### 1. Story

As a **security administrator (RW-SECADM)**, I want **every sign-in, refusal, read of a case record or document and export written to the decision record of the service that served it and published to the decision topic, and emergency access taken only under a break-glass grant approved in the bank IAM against an open incident, for a limited time, with every action marked**, so that **every access can be audited from one log and emergency access is controlled and reviewed**.

This is the application slice of legacy key RWB-E1-039 under epic RWB-SVC-P4. It delivers, in `rwb-access`:

- the **access event writer**: one entry per access event, written through the local decision-record library of DP-03 in the same transaction as the read response and never after it, with the case id where there is one, the field ids and their masking position, or the filter and the row count for a list or an export, and never a field value;
- the **published writer interface** that the guard and masker library of RWB-PLT-E1037 binds, so that a service that serves a read writes its own entry in its own chain and no service reads another service's schema (DP-01);
- the **break-glass grant**: activation against an approved IAM request and an open incident, the time box, the marking of every entry written while the grant is active, and the end of the grant with no action by anyone;
- the **access-log read** behind the gateway-bff route, and the refusal record of every admin call that the matrix denies;
- the **fail-closed rule**: a read whose access event cannot be written returns no data, because an unaudited read of a personal record is not allowed.

**The division of this legacy key is fixed and is the same in all four stories.** This story owns all ten legacy acceptance criteria of section 7 and the writer, the grant and the read above. **RWB-P4-E1039-CON** owns the published contract: the `GET /api/recovery/access/v1/admin/access-log` read, the break-glass grant, end and read operations, the record shape of one access-log entry, the two-person rule, the time box, the refusal vocabulary and the fail-closed rule. **RWB-P4-E1039-DB** owns the ACE DB slice in `rwb_access`: the Flyway sequence, the four tables this key needs, the grants to the `rwb-access` login, and the retention and partitioning of the log as data. **RWB-P4-E1039-OPS** owns the DevOps slice: the Helm values, the Kafka ACLs, the secrets, the alerting of a failed or refused access-log write, the break-glass alert route and the run book.

**The end-to-end proof of the key is RWB-ITG-E1039-ITG**, which runs the same journey across the services that serve the reads and against the central ledger. The same legacy key has two neighbours, neither of which is this story: **RWB-P5-E1039-APP** on the document side writes the entry of a document content read where the document is served, and **RWB-P7-E1039-APP** on the ledger side owns the central `decision_log_entry` table, the `GET /decision-log` query and the chain verification. P4 writes no P7 table and reads none.

### 2. Business rationale

The bank cannot answer today who read a debtor's record on a given date, and administrators have standing access to production data. The legacy story wrote each access event into one append-only, hash-chained decision log inside a single process and a single schema, with an in-process publisher called by every module. That shape does not survive the split: nineteen services own nineteen schemas, one login each, and no service may read another's tables (DP-01), so an access log written by one process on behalf of all of them would be a shared table in disguise.

**The division is fixed and is the same in all four stories.** The permission matrix, the masking policy and the scope rule stay with RWB-P4-E1037-APP; the access log, the break-glass grant and the entries' record shape stay with **RWB-P4-E1039-APP**; the contract of the two reads and of the grant is **RWB-P4-E1039-CON**; the schema, the grants, the retention and the partitions are **RWB-P4-E1039-DB**; the deployment, the topic ACLs, the alerts and the run book are **RWB-P4-E1039-OPS**; and the end-to-end proof across the wave 1 services is **RWB-ITG-E1039-ITG**. The same legacy key also has two neighbours whose stories are not part of this division: **RWB-P5-E1039-APP**, which records the access event of a document content read where the document is served, and **RWB-P7-E1039-APP**, which owns the central ledger and the workbench-wide query. Neither story copies a legacy acceptance criterion of this key: the ten criteria of section 7 belong to this story, verbatim, each tagged with its origin.

**The access log is written locally, and this is the decision the whole slice turns on.** Every service writes its decision records in its own schema through the local decision-record library of DP-03 and publishes `rwb.decision-record.DecisionRecorded.v1` to the shared topic `rwb.decision-record.v1` from its own outbox; the central ledger of P7 consumes that topic and answers the workbench-wide query within five minutes (Architecture v5 slides 28 and 42; ADR-022). The access entry follows the same rule: it is written in the schema of the service that served the read, in the same transaction as the read response, and the library publishes it. So `decision_log_entry` and the central ledger stay with P7 rwb-decision, and **P4 writes no P7 table** — not `decision_log_entry`, not `approval`, not the chain state of the ledger. What P4 owns is the writer, the grant and the read of the entries in `rwb_access`, and the workbench-wide answer to "who read this case" is the P7 query `GET /decision-log` that legacy AC8 already names.

The split follows the architecture and not a preference. Each service authorises the object itself against cached permission data with a 2 s timeout and a breaker per downstream (slide 10); the access owner publishes `POST /authorise`, `GET /me/permissions`, `GET /doa-limits` and `/masking-policies` (slide 14); personal data stays in the owning service and the masking rules are enforced there (slide 35); and one service's release must never block another's, which a shared log table would do. Writing the entry where the access happened keeps the transaction local, keeps the fail-closed rule enforceable inside the caller, and leaves the ledger as a consumer and never as a dependency of a read.

The negative side is fixed as tightly as the positive one. Deny by default and fail closed (slides 29 and 35); no personal value in an entry, a log, an event or a payload — only the case id, the field id and the flag (NFR-040); no token store (ADR-010); no cross-schema read (DP-01); no data lake (DP-17: the lake copy and its read logging are removed, and reporting reads events into rwb-reporting). The values the criteria use are the legacy values unchanged: test users U-4101, U-4102, U-4103, U-4104, U-4105 and U-4106; case RW-2026-000123; document DOC-2026-0009981; incident INC0004521; IAM request IAM-778812; group RWB-SIT-BREAKGLASS; the 37 synthetic cases of the filtered list; the 10:30 to 14:31 window of the test clock; the 12-character reason; Idempotency-Key k-001 and k-002; field ids DF-PTY-007 and DF-PTY-016; the access event codes AC-SIGN, AC-DENY, AC-READ, AC-EXPT, AC-BGON and AC-VERS; and the messages MSG-P4-002, MSG-P4-004, MSG-P4-007, MSG-GEN-001 to MSG-GEN-004 and MSG-P7-003.

It meets REQ-ACA-006 and REQ-ACA-008 and supports controls CTL-09 and CTL-11. The measure is unchanged: reads of the case store and the document store written to the access log, target 100 percent (NFR-042). Where the sources do not fix the local table name, the legacy path `/admin/break-glass` against the target `/admin/break-glass-grants`, or the composition of the `actions` field for a refusal and an export, this story builds to the assumption in force and records the open point as Not specified in the source documents (GAP-0780; ASM-1423), (GAP-0780; ASM-1424) and (GAP-0780; ASM-1425).

### 3. Preconditions

- RWB-P4-E1039-CON is published (this story's contract deliverable): the access-log read, the break-glass grant, end and read operations, the record shape of one entry, the two-person rule, the time box, the refusal vocabulary and the fail-closed rule, with its fakes.
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1`, which writes the entry, hash-links it to the previous record and publishes `rwb.decision-record.DecisionRecorded.v1` from the outbox in the caller's transaction (DP-03).
- RWB-PLT-E1042-CON and RWB-PLT-E1043-CON are published, and RWB-P3-E1042-CON and RWB-P3-E1043-CON publish the contracts behind them (DP-06, DP-07): the break-glass parameters and the reference lists arrive as data, never as code.
- RWB-PLT-N001-CON is published: the gateway-bff composite route that carries the access-log read and the break-glass banner to the screen in the route's problem-detail shape (DP-19).
- RWB-P4-E1022-APP is done: sign-in, the session and `GET /api/recovery/access/v1/me/session` exist, and the session answer carries the resolved roles, the matrix version and the masking version.
- The parameters are in force in the rwb-case parameter catalogue: `rwb.access.breakglass.window-hours=4`, `rwb.access.breakglass.incident-pattern=^INC[0-9]{7}$`, `rwb.access.breakglass.reason-min=20`, `rwb.access.breakglass.review-days=1` (assumed values; DL38). The reason maximum is 1000 characters, as the legacy validation message states.
- The reference list LOV-DECISION holds the access event codes AC-SIGN, AC-DENY, AC-READ, AC-EXPT, AC-BGON and AC-VERS, and LOV-CAPABILITY, LOV-SCOPE and LOV-ROLE hold the areas, scopes and roles the entry and the grant carry; they are P3 rwb-case reference data (DP-07) and are read with their version, not copied into code.
- The Entra ID break-glass group for each environment exists, granted only through the bank IAM with an end time (name per DL40; RWB-SIT-BREAKGLASS assumed in SIT), and the ACE Common PII and SOC logging path of Architecture v5 slide 30 is available for the second copy of an access event.
- No table of another service is read: `decision_log_entry` and `approval` are P7's, `lov_value` and the reference tables are P3's, and the local decision-record table, `outbox_event`, `processed_event`, `idempotency_key` and `break_glass_grant` are created in `rwb_access` by RWB-P4-E1039-DB (DP-01).
- No build dependency blocks the start beyond the contract and the session: every H dependency is a CON story of this service or of the platform, plus RWB-P4-E1022-APP for the session, so the story starts after the sign-on slice and builds against the published contracts and their fakes.

### 4. Flow

1. A person signs in, or reads a case record, a document, a list, or exports a list. The service that serves the read asks the guard library of RWB-PLT-E1037 for the right, and the guard answers from the cached policy of the access owner.
2. The serving service builds the access event: the event code, the actor reference, the case id where there is one, the capability area and the right, the result, the field ids with the masked flag of each, the filter and the row count for a list or an export, the document id, the grant id and the incident reference where a grant is active, and a reason code where the event is a refusal.
3. The writer calls the local decision-record library with the event, in the same transaction as the read response. The library writes one entry in the serving service's own schema, hash-links it to the previous record of that chain, and appends `rwb.decision-record.DecisionRecorded.v1` to the outbox of that transaction.
4. The read response is returned only after the entry is committed. If the write fails, the read returns nothing: status 503 with MSG-P7-003, no business data in the body, and an incident to the platform administrator queue (AC7).
5. The outbox relay publishes the event to `rwb.decision-record.v1`; P7 rwb-decision consumes it into the central ledger within five minutes, and P9 rwb-reporting reads it for its projection. P4 neither consumes nor acknowledges that topic.
6. A platform administrator (RW-PLATADM) raises a break-glass request in the bank IAM naming the open incident, the capability area, the scope and the reason. The security administrator approves it there, and the IAM adds the administrator to the break-glass group until the window ends. This is the two-person rule: the person who asks and the person who approves are never the same person.
7. RW-PLATADM calls `POST /api/recovery/access/v1/admin/break-glass-grants` with the incident reference, the IAM request id, the capability area, the right, the scope and the reason, and an `Idempotency-Key`.
8. `BreakGlassService` checks the caller's membership of the break-glass group, the incident reference against the parameter pattern, the reason against the parameter length, and that no grant of the caller is active. It writes the AC-BGON entry through the same writer, then records the grant with its start and its end.
9. The grant ends at the earlier of the parameter window and the IAM group end, and it is enforced on every request rather than by a job: after the end time the guard ignores the grant and the role's own letters apply, with no action by anyone (AC2).
10. Every entry written while the grant is active carries the grant id and the incident reference, in the `actions` element of the entry. The ACE front end shows the MSG-P4-004 banner with the end time from `GET /api/recovery/access/v1/me/session`.
11. `GET /api/recovery/access/v1/admin/access-log` returns the entries of `rwb_access` for a user and a period, with `matrixVersion` and `maskingVersion`, and answers the security administrator's review of each use. The workbench-wide question "who read this case" is answered by `GET /decision-log` of P7, which is the query of legacy AC8.
12. After the end time, or on an explicit end, the grant moves to Ended and is never reopened; a second activation needs a new IAM approval, a new incident reference and a new idempotency key.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The access log entry cannot be written | The read or export returns no data; status 503; an incident is raised to the platform administrator queue | MSG-P7-003 | AC7 |
| X2 | Break-glass is requested by a person not in the break-glass group | Refused with 403; the refusal is written as an AC-DENY entry with the reason NO_BREAKGLASS_GRANT | MSG-P4-007 | AC5 |
| X3 | Break-glass is requested with no incident reference, a reference that fails the pattern, or a reason under the minimum length | Refused with 422 naming the field; no grant is created and no AC-BGON entry is written | MSG-GEN-001, MSG-GEN-002 | AC6 |
| X4 | An action is attempted after the grant has ended | The grant is ignored; the role's own letters apply; a refusal is written | MSG-P4-002 | AC2 |
| X5 | A second activation is sent while a grant is active | With the same Idempotency-Key the first response returns and no new entry is written; with a new key the call returns 409 | MSG-GEN-004 | AC10 |
| X6 | A role without Platform administration R calls an admin endpoint, such as the access log or the roles list | Refused with 403; an AC-DENY entry is written with the area, the right and no case id | MSG-P4-002 | AC9 |
| X7 | The decision-record library answers a malformed or partial write | The read fails closed with 503; nothing is served and no partial entry is left in the chain | None | AC7 |
| X8 | The break-glass group answers late or not at all | The activation is refused, never allowed on an unverified membership | MSG-P4-007 | AC5 |
| X9 | The access event names a field id that no list and no masking rule knows | The entry is written with the field id as given and the flag `masked`; the anomaly is counted, and a read is never served with an unknown field in clear | None | AC1 |
| X10 | The outbox relay lags behind the write | The entry is already committed and the read is already answered; the relay retries from the outbox with its retry cadence and the ledger records the delay | None | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the contract of this service, the DP-03 library, the two P3 contracts and the session of RWB-P4-E1022-APP; no other story has to be finished first |
| Negotiable | The table name of the grant, the partition granularity and the retention period are open until the DB story freezes them; the entry shape, the time box and the fail-closed rule are fixed by the contract |
| Valuable | One log answers who saw what and when, and standing administrator access ends with a time box and a record |
| Estimable | One writer, one grant service and check, one read service, the session extension and the banner element |
| Small | Fits one sprint with the tests of section 16 |
| Testable | Each criterion below is one end-to-end, component, contract or NFR test in section 16, against the fakes of section 12.8 |

### 7. Acceptance criteria

```gherkin
Feature: Access log into the decision log and break-glass admin

  Background:
    Given the environment is SIT
    Given the decision-record library is available

  Scenario: AC1 Read logged (legacy RWB-E1-039 AC1)
    Given the case contract mock returns case "RW-2026-000123" opened at 10:15 on 3 December 2026 by test user "U-4101" holding RW-CASEOWN
    When the case record view loads
    Then the system writes one decision log entry with decision code "AC-READ", actor "U-4101", the case ID and decided at 10:15
    Then its actions list the field IDs returned, with DF-PTY-007 and DF-PTY-016 marked "masked"

  Scenario: AC2 Break-glass granted (legacy RWB-E1-039 AC2)
    Given incident "INC0004521" is open
    Given the security administrator approved IAM request "IAM-778812" and the IAM added test user "U-4102" holding RW-PLATADM to group "RWB-SIT-BREAKGLASS" until 18:00
    When "U-4102" calls POST /admin/break-glass at 10:30 with incident "INC0004521", request "IAM-778812", area "CASE_RECORD", right "U", scope "ALL" and a reason of 46 characters
    Then the grant is active until 14:30, the earlier of 4 hours and the group end
    Then the banner shows MSG-P4-004 with time "14:30"
    Then every entry written for "U-4102" until 14:30 carries the grant ID and incident "INC0004521"
    Then the system allows at 14:20 PATCH /tasks/{taskId} on case "RW-2026-000123" by "U-4102" and marked with the grant
    Then the system refuses at 14:31 the same call with MSG-P4-002, because RW-PLATADM holds only "R" in Case record, with no action by anyone

  Scenario: AC3 Export logged (legacy RWB-E1-039 AC3)
    Given the case contract mock returns 37 rows to test user "U-4103" holding RW-TEAMMGR for the case list filtered by status "ASSIGNED" and product "MORTGAGE"
    When the user exports the list
    Then the system writes one decision log entry with decision code "AC-EXPT", actor "U-4103", the filter, row count 37 and no case ID

  Scenario: AC4 Document read logged (legacy RWB-E1-039 AC4)
    Given the document contract mock returns document "DOC-2026-0009981" on case "RW-2026-000123" to test user "U-4101" holding RW-CASEOWN
    When GET /documents/{documentId}/content returns the file
    Then one entry with decision code "AC-READ", the case ID and the document ID is written before the file is returned

  Scenario: AC5 Break-glass without an IAM grant is refused (legacy RWB-E1-039 AC5)
    Given test user "U-4104" holds RW-PLATADM and is not in group "RWB-SIT-BREAKGLASS"
    When the user calls POST /admin/break-glass with incident "INC0004521"
    Then the system refuses the call with status 403 and message MSG-P4-007
    Then one entry with decision code "AC-DENY" and reason "NO_BREAKGLASS_GRANT" is written

  Scenario: AC6 Break-glass with a missing incident or a short reason is refused (legacy RWB-E1-039 AC6)
    Given test user "U-4102" is in group "RWB-SIT-BREAKGLASS"
    When the user calls POST /admin/break-glass with no incident reference
    Then the system refuses the call with status 422 and message MSG-GEN-001 for field "incidentReference"
    Then when the user calls it with incident "INC0004521" and a reason of 12 characters
    Then the system refuses the call with status 422 and message MSG-GEN-002 for field "reason" with min 20 and max 1000

  Scenario: AC7 A read that cannot be logged returns nothing (legacy RWB-E1-039 AC7)
    Given the decision log store is unavailable
    When test user "U-4101" opens case "RW-2026-000123"
    Then the call returns status 503 with message MSG-P7-003 and no case data
    Then the system raises an incident to the platform administrator queue

  Scenario: AC8 Access audit query (legacy RWB-E1-039 AC8)
    Given case "RW-2026-000123" was read by "U-4101" at 10:15, by "U-4102" at 11:02 under break-glass, and by "U-4101" at 16:40 on 3 December 2026
    When test user "U-4105" holding RW-AUDIT calls GET /decision-log with that case ID, decision "AC-READ", from "2026-12-03" and to "2026-12-03"
    Then three entries return in time order with actor, time and fields shown
    Then the 11:02 entry carries incident "INC0004521"

  Scenario: AC9 Refusals are written to the decision log (legacy RWB-E1-039 AC9)
    Given test user "U-4106" holds only RW-PHONECOL
    When the user calls GET /admin/roles
    Then the system refuses the call with MSG-P4-002
    Then one entry with decision code "AC-DENY", area "PLATFORM_ADMINISTRATION", right "R" and no case ID is written

  Scenario: AC10 A repeated activation does not open a second grant (legacy RWB-E1-039 AC10)
    Given "U-4102" activated break-glass at 10:30 with Idempotency-Key "k-001"
    When the user sends the same request again with key "k-001" at 10:31
    Then the first response returns and no new entry is written
    Then when the user sends a request with key "k-002" at 10:32
    Then the call returns status 409 with message MSG-GEN-004
```

These ten criteria are the legacy criteria of RWB-E1-039, copied with their values unchanged and tagged with their origin. Two things are read in the target shape and not in the monolith's: the path `POST /admin/break-glass` of AC2, AC5 and AC6 is the published operation `POST /api/recovery/access/v1/admin/break-glass-grants` (the criterion keeps the legacy spelling), and the decision log of AC1, AC3, AC4, AC7, AC8 and AC9 is the local decision record of DP-03 in the serving service's own schema, with the central ledger of P7 behind `GET /decision-log` for the workbench-wide query of AC8 (GAP-0780; ASM-1425).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every sign-in, refusal, read of the case store or the document store, and export writes one access event to the decision record: one entry, in the same transaction as the response, hash-linked to the previous record of that chain | REQ-ACA-006; NFR-042; FEAT-ACA-08 |
| BR2 | A read or export whose access event cannot be written returns no data; the answer is 503 with MSG-P7-003 and an incident to the platform administrator queue | Principle 5; R-UNI-39; RB1 |
| BR3 | An access event lists field ids and their masking position, never field values; the clearest fact an entry may carry is the case id, the document id, the field id and the flag `clear` or `masked` | NFR-040; guardrail on personal data; RB7 |
| BR4 | Break-glass needs a grant approved by the security administrator in the bank IAM, an open incident reference and a reason of at least 20 characters; the requester and the approver are never the same person | Admin and access model, section 5.3; Access flow sheet, roles.txt; REQ-ACA-008 |
| BR5 | A grant ends at the earlier of the window (4 hours, assumed) and the IAM group end, with no action by anyone, and the end is enforced on every request rather than by a job | rwb.access.breakglass.window-hours; DL38; RB5 |
| BR6 | Every action under break-glass is marked with the grant id and the incident reference, in the `actions` element of the entry | Admin and access model, section 5.3; RB10 |
| BR7 | The security administrator reviews each use inside the review window (one working day, assumed); an unreviewed use goes to the head of SCB IT security and to Compliance | DL38; Access flow sheet, roles.txt |
| BR8 | A platform administrator holds only the letters of RW-PLATADM in the matrix version in force; any right beyond them comes only from an active break-glass grant | Admin and access model, section 3.2; permission matrix |
| BR9 | A person may not review their own break-glass use, and the reviewer is not the requester and not the approver | Admin and access model, section 6.2 |
| BR10 | The entry is written in the schema of the service that served the read and published to `rwb.decision-record.v1` from that service's outbox; P4 reads and writes no table of rwb-decision | DP-01; DP-03; Architecture v5 slide 28 |
| BR11 | The event codes, the areas, the scopes and the roles are reference data with a version, and the window, the incident pattern, the reason bounds and the review window are parameters; neither is a constant in code | DP-06; DP-07; BR-P4-007 |

### 9. State transitions

No case status changes in this story. A break-glass grant and a decision-record entry have states of their own:

| Object | From | Event | To | Result |
|---|---|---|---|---|
| Break-glass grant | NONE | `POST /admin/break-glass-grants` with a verified group membership, a valid incident and a valid reason | ACTIVE | The AC-BGON entry is written; `startsAt` and `endsAt` are set to the earlier of the window and the group end |
| Break-glass grant | ACTIVE | The end time is reached | ENDED | The guard ignores the grant on every request with no action by anyone; the role's own letters apply |
| Break-glass grant | ACTIVE | An explicit end request from the requester or the security administrator | ENDED | Closed before the end time; the close is written as an entry and the grant is never reopened |
| Break-glass grant | ACTIVE | A second activation with the same Idempotency-Key | ACTIVE | The first answer returns and no second entry is written |
| Break-glass grant | ACTIVE | A second activation with a new Idempotency-Key | ACTIVE | Refused with 409 and MSG-GEN-004 |
| Access entry | NONE | An access event of the service | APPENDED | One entry, hash-linked; an entry is never updated or deleted |
| Access entry | APPENDED | The event is a refused call | APPENDED | An AC-DENY entry with the area, the right and the reason code |
| Access entry | APPENDED | The outbox relay publishes it | PUBLISHED | `DecisionRecorded` on `rwb.decision-record.v1`; the local entry is unchanged |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM Platform administrator | Requests break-glass in the bank IAM and activates an approved grant with the grant operation (Platform administration C) |
| RW-SECADM Security administrator | Approves break-glass in the bank IAM, reviews each use and reads the access log (Platform administration R) |
| RW-COMPLY Compliance and PDPA officer | Reads the access log and receives the unreviewed uses |
| RW-AUDIT Internal audit | Reads the access log and queries access to a case through the central ledger; changes nothing |
| RW-COE, RW-DATASTEW | Read the access log (Platform administration R) |
| Every bank role | Generates access events by signing in, reading and exporting |
| The serving services of the workbench | Call the published writer through the guard and masker library; each writes in its own schema |
| SY-DECLOG Decision record writer | The DP-03 library identity that writes the entry and the outbox row in the caller's transaction |
| Head of SCB IT security | Receives a break-glass use that is not reviewed inside the window |

No person is named in this story; every actor is a role code or a test user reference.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | the local decision record of DP-03, in `rwb_access` | all fields | Write (one entry per access event) |
| DF-DEC-002 | the local decision record of DP-03 | case_id | Write; empty for sign-in, refusal, export and break-glass events (change recorded in the additions file) |
| DF-DEC-030 | the local decision record of DP-03 | actor_user_id | Write, read |
| DF-DEC-003 | the local decision record of DP-03 | decision_code | Read (query by access event code) |
| DF-DEC-014 | the local decision record of DP-03 | actions | Read (area, right, fields, filter, row count, grant, incident) |
| DF-DEC-016 | the local decision record of DP-03 | decided_at | Read; the partition key of the log |
| DF-REF-035 | role (P4 rwb_access) | role_code | Read (the role whose letters the grant extends) |
| DF-REF-043 | permission (P4 rwb_access) | letters | Read (the letters of RW-PLATADM that the grant adds to) |

Field ids are those in the Logical Data Model and Data Dictionary. The entry is the decision record of the DP-03 library: it carries the field ids above, its `prev_hash` and `entry_hash`, and no personal value — the case id, the document id, the field id and the mask flag are the clearest facts it holds (BR3). **The access log is written through the local decision-record library of DP-03 to the shared topic `rwb.decision-record.v1`**: the library commits the entry in the serving service's own schema and in the same transaction as the read, and publishes it from that service's outbox as `rwb.decision-record.DecisionRecorded.v1`. `decision_log_entry` in `rwb_decision` and the central ledger are P7 rwb-decision's and are not written, read or named as this service's table; `GET /decision-log` is P7's operation. The local decision-record table of the DP-03 library has no table name in the Ownership Map, so it is named by its contract and never by an invented table name (GAP-0780; ASM-1423). The break-glass grant is a row of `break_glass_grant` in `rwb_access`, created by RWB-P4-E1039-DB; this story reads the grant through the contract of RWB-P4-E1039-CON, whose seven legacy fields — the grant id, the incident reference, the IAM request id, the capability area, the right, the scope and the reason with its start and end — are the only grant values it names, and it adds no column of its own.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-access (P4); base `/api/recovery/access/v1`. The shapes are fixed by RWB-P4-E1039-CON; this story implements them.

| Method | Path | Shape | Access |
|---|---|---|---|
| GET | `/api/recovery/access/v1/admin/access-log` | AccessLogPage over the entries of `rwb_access`: query `user`, `from`, `to`, `event`, `capabilityArea`, `page`, `size`; items with `at`, `user`, `event`, `capability`, `result`, `grantId`, `incidentReference`, `matrixVersion`, `maskingVersion` | Platform administration R, scope applied |
| POST | `/api/recovery/access/v1/admin/break-glass-grants` | BreakGlassActivation in, BreakGlassGrant out: `grantId`, `incidentReference`, `capabilityArea`, `right`, `scope`, `startsAt`, `endsAt`; `Idempotency-Key` required | Platform administration C, plus membership of the break-glass group |
| POST | `/api/recovery/access/v1/admin/break-glass-grants/{grantId}/end` | Closes an active grant before its end time and writes the close as an entry; `Idempotency-Key` required | Platform administration C, or the requester of the grant |
| GET | `/api/recovery/access/v1/admin/break-glass-grants/{grantId}` | BreakGlassGrant with its state ACTIVE or ENDED, `startsAt`, `endsAt` and the IAM request id | Platform administration R |

Errors for the four: 401 the gateway-bff session envelope; 403 no right (MSG-P4-002), or no membership of the break-glass group on the grant operation (MSG-P4-007); 409 a grant is already active (MSG-GEN-004); 422 a field missing or invalid (MSG-GEN-001, MSG-GEN-002) or a period that ends before it starts (MSG-GEN-003); 503 the entry could not be written (MSG-P7-003). The end and read paths follow the base rule of DP-13 and the assumption in force, because no source names them (GAP-0780; ASM-1425).

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access (RWB-P4-E1022-APP) | The caller's roles, matrix and masking versions, and the break-glass state with the end time that the MSG-P4-004 banner shows |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The window of 4 hours, the incident pattern, the reason minimum of 20 and the review window of one working day (DP-06) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-DECISION with AC-SIGN, AC-DENY, AC-READ, AC-EXPT, AC-BGON and AC-VERS, and LOV-CAPABILITY, LOV-SCOPE and LOV-ROLE, each with its version (DP-07) |

No operation of rwb-decision, rwb-document or rwb-case's case read appears here: the caller of the writer already holds the case id, the document id and the field ids it passes, so P4 calls no service to build an entry.

#### 12.3 Events published

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | The DP-03 library of PLT, in this service's outbox | One message per access entry, with the entry id, the case id, the decision code, the actor reference, the grant id, the incident reference, `prev_hash` and `entry_hash`, in the CloudEvents 1.0 envelope |

This story publishes no business event on `rwb.access.events.v1`: the two policy events of the service, `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoALimitChanged.v1`, belong to RWB-P4-E1037-APP and the delegation story, and an access entry is not a policy change.

#### 12.4 Events consumed

None. P4 rwb-access is the reference-data owner of Architecture v5 slide 14, whose contract line records no consumed event; the access entry needs no subscription, and the break-glass state is read from the session, not from a topic.

#### 12.5 Workflows and activities

None. The writer, the grant and the read are synchronous code in a REST handler; no workflow is started and no activity is registered for this key.

#### 12.6 Schedules

None. The six-monthly access review list (JOB-18) is a Schedule of rwb-access but belongs to RWB-P4-AD008-APP; this story registers none.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (rwb_access) | Read: the role code of the actor and the letters the grant extends (DF-REF-035) |
| `permission` | P4 (rwb_access) | Read: the Platform administration R letter and the matrix version (DF-REF-043) |
| `masking_rule` | P4 (rwb_access) | Read: the masking version an entry states |
| the local decision-record table of the DP-03 library | P4, in `rwb_access` | Written through the library; the access entries and their chain |
| `break_glass_grant` | P4, in `rwb_access` | Written and read; created by RWB-P4-E1039-DB, whose name for it is an assumption (GAP-0780; ASM-1423) |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library objects, created in `rwb_access` | The outbox row of each entry, the inbox the service does not use for this key, and the stored answer of the two POST operations |

**`decision_log_entry` and the central ledger are P7 rwb-decision's, and P4 writes no P7 table.** The ledger consumes `rwb.decision-record.v1` and answers `GET /decision-log`; this service publishes to the topic and never reads the ledger's tables, and it holds no copy of them. The grant table is a P4 table of this key: no source names it, so its name is the assumption in force and not a copied value.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| Case fake | The case read the access event is written for | Case RW-2026-000123 opened at 10:15 on 3 December 2026; the 37 rows of the filtered list (AC1, AC3) |
| Document fake | The document content read | Document DOC-2026-0009981 on case RW-2026-000123, returned only after the entry (AC4) |
| Decision-record fake | The DP-03 library write and the chain | An append that commits, an append that fails, a seeded chain of a week with AC-READ, AC-DENY and AC-EXPT entries and one grant entry with incident INC0004521 (AC1, AC2, AC7, AC8) |
| Ledger fake | `GET /decision-log` of P7 | Three reads of case RW-2026-000123 on 3 December 2026, the 11:02 one carrying incident INC0004521 (AC8) |
| Parameters fake | `GET /admin/parameters` | window-hours 4, incident-pattern `^INC[0-9]{7}$`, reason-min 20, review-days 1 (AC2, AC5, AC6) |
| Reference-data fake | `GET /admin/lists/{listCode}` | LOV-DECISION at version REF-2026.11, LOV-CAPABILITY, LOV-SCOPE and LOV-ROLE (AC2, AC6, AC9) |
| IAM group fake | The break-glass group and the IAM request | Member until 18:00, not a member, request IAM-778812 approved and unapproved (AC2, AC5) |

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 4 | 3 | The access-log read and the three grant operations provided; the session, parameters and reference-data reads consumed; one hop, 2 s timeout |
| Kafka | 1 published | 0 consumed | `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` through the DP-03 outbox; no event on `rwb.access.events.v1` from this key |
| Temporal | 0 | 0 | No workflow, activity or Schedule |
| File | 0 | 0 | No file is read or written; the list export of AC3 is a response of the case list, not a file of this service |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.access` for the implementation, with the writer interface published in `th.co.scb.ace.workbench.recovery.access.api` so that the guard and masker library of RWB-PLT-E1037 binds one implementation rather than nineteen copies.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The entry is written in the serving service's own chain, and `decision_log_entry` is never read here | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library. The window, the incident pattern, the reason bounds and the review window are parameter rows | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case. The event codes, the areas, the scopes and the roles arrive with their version | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout. The writer call of the monolith becomes a contract call of the serving service to its own library, and the two P3 reads are one hop each | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/access/v1`; every path of this story sits under the service base | none |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting. The lake copy of the access log and its read logging leave with the lake, and P9 reads `DecisionRecorded` | none; no lake data is needed |
| DP-19 | Screen, ace-web | gateway-bff composite route. The access-log read and the banner reach the screen through the route, and SCR-43 is not built here | H RWB-PLT-N001-CON |

**Hardware and software change.** The `recovery.access.accesslog` package of the monolith is replaced by a writer that every service binds and a grant service in `rwb-access`. The entry leaves the monolith's single `decision_log_entry` and is written in each service's own schema through the DP-03 library; the central ledger of P7 collects it from `rwb.decision-record.v1` and answers the workbench-wide query. The ACE audit and PII path to the SOC is unchanged: every service still sends the audit fact through ACE Common (Architecture v5 slide 30), and the decision record is the second, durable copy. No new hardware is implied: the writer runs inside each service's existing pods, the grant service inside the `rwb-access` pods, and the only new objects are the four tables of RWB-P4-E1039-DB in `rwb_access`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `AccessEventWriter` | Published interface | Turns an access event into one decision-record entry and appends it through the DP-03 library in the caller's transaction (BR1, BR10) |
| `AccessEventPublisher` | Service | Builds the event from the request context — code, actor, case, area, right, result, field ids with the flag, filter, row count, document id, grant and incident — and raises the fail-closed error when the write fails (BR2) |
| `BreakGlassService` | Service | Verifies the group membership, the incident pattern, the reason bounds and the absence of an active grant; writes the AC-BGON entry; records the grant with `startsAt` and `endsAt` (BR4, BR5) |
| `BreakGlassGrantCheck` | Service | Adds the grant's right in its area and scope to the guard answer until `endsAt`, marks every entry with the grant and the incident, and ignores an ended grant on every request (BR5, BR6) |
| `GrantEndService` | Service | Ends a grant early, writes the close as an entry and refuses to reopen it (BR5) |
| `AccessLogQueryService` | Service | Maps the access-log read onto the entries of `rwb_access`, with the subject scope and the two version fields |
| `RefusalRecorder` | Service | Writes an AC-DENY entry for an admin call the matrix refuses, with the area, the right and no case id (BR1, AC9) |
| `BreakGlassBanner` contract element | Screen element | Shows MSG-P4-004 with the end time from the session answer, through the gateway-bff route (DP-19) |

**Configuration.** The four break-glass parameters come from the rwb-case catalogue through the parameters client (DP-06). The event codes, the areas, the scopes and the roles come from the reference lists with their version (DP-07). Nothing of either is a constant in code, and no environment value is read outside the parameter contract.

**Build steps**

1. Bind the DP-03 library and implement `AccessEventWriter` over it; prove one entry committed in the caller's transaction and one outbox row, with the `prev_hash` chain intact (AC1).
2. Extend `AccessEventPublisher` with the field ids and the mask flag, the filter and the row count, the document id, the grant id and the incident reference; test the case read, the export and the document read (AC1, AC3, AC4).
3. Make the read fail closed when the write fails, with 503, MSG-P7-003, no business data and the incident to the platform administrator queue (AC7).
4. Build `BreakGlassService` and the grant operation with the group check, the incident pattern, the reason bounds, the time box and the idempotency rule; test the granted case, the missing membership and the two validation refusals (AC2, AC5, AC6, AC10).
5. Build `BreakGlassGrantCheck` with the end time enforced on every request, a clock fixed at 10:30 and moved to 14:20 and 14:31, and the marking of every entry (AC2).
6. Build `AccessLogQueryService` and the read, with the subject scope, the period validation and the two version fields (AC8).
7. Build `RefusalRecorder` on the admin surface, so a refused admin call writes its AC-DENY entry with the area and the right (AC9).
8. Extend the session answer with the break-glass state and the end time, and hand the banner element to the gateway-bff route (AC2).
9. Run the ten criteria against the fakes of section 12.8 and hand the shapes to RWB-ITG-E1039-ITG for the cross-service proof.

**Feature flag.** `rwb.access.access-log`, read as a parameter per environment. Off, the writer still refuses a read it cannot record, so a switch-off never opens an unaudited path; it only stops the grant operation and leaves the matrix letters in force.

**Done when.** The tests in section 16 pass, the entry of every access event is committed in the serving service's transaction and appears once on `rwb.decision-record.v1`, the grant ends at the earlier of the window and the group end with no action by anyone, a refused admin call writes its AC-DENY entry, the fail-closed path returns no data, and the break-glass test of the access test set (one request with an open incident, one without) passes in SIT and is signed by the security administrator.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-004 | Break-glass access is active; the banner shows the end time | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-007 | Break-glass requested with no approved IAM grant, or with no verified group membership | Emergency access needs an approved break-glass request in the bank IAM with an open incident. |
| MSG-P4-002 | An action after the grant has ended, or an access log query without the right | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | Incident reference empty, or a required field empty | Enter {field}. |
| MSG-GEN-002 | Reason shorter than 20 characters or longer than 1000, or page size outside 1 to 500 | {field} must be between {min} and {max}. |
| MSG-GEN-003 | Query from date after to date | {field} cannot be before {other}. |
| MSG-GEN-004 | A second activation while a grant is active | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | The access event cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The ids and the texts are copied unchanged from RWB-E1-039; the story adds no message of its own. Thai text for each follows DL10, and the proposed Thai for MSG-P4-007 is the one recorded in the additions file. The 503 of the fail-closed path carries MSG-P7-003 and no personal data; the 401 of an expired session carries the gateway-bff session envelope, whose business message id is Not specified in the source documents (GAP-0780; ASM-1425).

### 15. Screens and states

| Screen | State | What the story supplies |
|---|---|---|
| The ACE front-end shell | Break-glass active | The MSG-P4-004 banner with the end time from the session answer, over every screen while the grant is active |
| SCR-43 Roles and access | Access log, list | The access-log read with the entries, `matrixVersion` and `maskingVersion`, paged at 50 and at most 200 |
| SCR-43 Roles and access | Access log, filtered | The same read narrowed by `user`, `from`, `to`, `event` and `capabilityArea` |
| SCR-43 Roles and access | Refused | The 403 with MSG-P4-002 and no list, plus the AC-DENY entry the refusal writes |
| SCR-38 Decision log query | Case access | The workbench-wide answer of P7's `GET /decision-log`, which is out of scope here and named for the audit journey only |

No screen is built in this story. SCR-43 belongs to Epic 8 and SCR-38 to Epic 2 (RWB-E2-005); the gateway-bff composite route of RWB-PLT-N001-CON merges the access-log read and the session read, one hop each, and renders the problem-detail shape of a refusal (DP-19).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-039-01 | AC1, BR1, BR3 | Component | Synthetic case RW-2026-000123 with masked personal fields |
| TC-E1-039-02 | AC2, BR4, BR5, BR6, BR8 | Component | Incident INC0004521, IAM request IAM-778812, test clock 10:30 to 14:31 |
| TC-E1-039-03 | AC3, BR1 | Component | Case list filter returning 37 synthetic cases |
| TC-E1-039-04 | AC4, BR1 | Contract | Synthetic document on the case |
| TC-E1-039-05 | AC5, BR4 | Component | RW-PLATADM test user outside the break-glass group |
| TC-E1-039-06 | AC6, BR4 | Contract | Missing incident reference; 12-character reason |
| TC-E1-039-07 | AC7, BR2 | NFR | Decision log store switched off in the test double |
| TC-E1-039-08 | AC8, BR6 | Integration | Three reads of one case on one day |
| TC-E1-039-09 | AC9, BR1 | Component | RW-PHONECOL test user calling the admin API |
| TC-E1-039-10 | AC10 | Component | Two keys for one active grant |
| TC-E1-039-11 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E1-039-12 | Principle 5 | NFR | The decision log write forced to fail during a case read |

The twelve ids, their Covers and their Data are the legacy ones, with the Level column added for the target. TC-E1-039-11 stays the Access row of the test pack at Component level and TC-E1-039-12 the Resilience row at NFR level. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case id; the cross-service copy of the journey is RWB-ITG-E1039-ITG and is not written here.

### 17. Guardrails

- No business value in code: the window, the incident pattern, the reason bounds, the review window, the event codes, the areas, the scopes and the roles are parameters and reference data with a version.
- No personal data in an entry, a log, an event, a test or a prompt: an entry carries the case id, the document id, the field id and the mask flag, never a value; the reason text is free text written by the administrator and must not hold customer data.
- No read of another module's tables: the entry is written in the serving service's own schema through the DP-03 library, `decision_log_entry` is P7's, and the access log is read through the owner's operation (DP-01).
- No right beyond the letters of RW-PLATADM without an active grant, and the grant end is enforced on every request rather than by a job.
- The read fails closed: an access event that cannot be written returns no data, with MSG-P7-003 and no business payload.
- No token store and no session table: the session is gateway-bff's, and P4 holds the roles, the policy and the access log only (ADR-010).
- The chain is append only: an entry is never updated or deleted, and its hash link is written in the same transaction as the entry.
- The central ledger is consumed by P7 and P9 and never by P4; a P4 path that reads `rwb_decision` fails the review.
- Every example and fixture is synthetic; no production payload is copied into a test or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-006 | Every read of the case store and the document store written to the access log | Epic 1, 3.4 | FEAT-ACA-07, FEAT-ACA-08, FEAT-ACA-16 | 16 Manage risk, control and compliance | BR1, BR2, BR3, BR10, BR11 | TC-E1-039-01, TC-E1-039-03, TC-E1-039-04, TC-E1-039-07, TC-E1-039-08, TC-E1-039-09, TC-E1-039-12 |
| REQ-ACA-008 | Break-glass with its own approval, written to the access log | Epic 1, 3.4 | FEAT-ACA-09, FEAT-ACA-10 | 16 Manage risk, control and compliance | BR4, BR5, BR6, BR7, BR8, BR9 | TC-E1-039-02, TC-E1-039-05, TC-E1-039-06, TC-E1-039-10 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P4-E1039-CON | Contract | Sibling: the published contract this story implements, and the owner of the entry shape and the refusal vocabulary |
| RWB-P4-E1039-DB | ACE DB | X dependency tracked: the four tables of the key in `rwb_access`, their grants and the retention of the log |
| RWB-P4-E1039-OPS | DevOps | X dependency tracked: the Helm values, the topic ACLs, the alerts and the run book |
| RWB-P4-E1022-APP | App development | H dependency: the session, the guard answer and the caller identity |
| RWB-P4-E1037-APP | App development | C dependency through its contract: the matrix and the masking policy the entry states |
| RWB-P5-E1039-APP | App development | Neighbour of the same legacy key on the document side: writes the entry of a content read where the document is served |
| RWB-P7-E1039-APP | App development | Neighbour of the same legacy key on the ledger side: the central `decision_log_entry`, the `GET /decision-log` query and the chain verification |
| RWB-ITG-E1039-ITG | Integration | The end-to-end proof of the key across the wave 1 services and the ledger |

The requirement ids are the two the Work Package gives for this key, and they are the two the legacy story traces; no requirement is added by this story.

### 19. Out of scope

- The published contract documents and the fakes as artefacts: RWB-P4-E1039-CON.
- The Flyway sequence, the four tables, the grants, the retention and the partitioning: RWB-P4-E1039-DB.
- The Helm values, the Kafka ACLs, the secrets, the alerts and the run book: RWB-P4-E1039-OPS.
- Logging reads of the data lake copy: the lake is removed by DP-17, so no such read exists and no lake entry is written.
- The break-glass request, approval and review records, which are held in the bank IAM and are referenced by id only.
- The scheduled alert for an unreviewed break-glass use to the head of SCB IT security and to Compliance (Epic 8, FEAT-ADM-12 Manage an incident).
- The central ledger, the `GET /decision-log` implementation and the hash-chain verification (P7 rwb-decision; RWB-P7-E1039-APP), which this story uses through its contract only.
- The document content read and the entry it writes where the document is served (P5 rwb-document; RWB-P5-E1039-APP).
- The screen SCR-38 Decision log query (RWB-E2-005), the screen SCR-43 Roles and access (Epic 8) and the gateway-bff composite route (RWB-PLT-N001-CON).
- The cross-service journey harness and its recorded evidence (RWB-ITG-E1039-ITG).
