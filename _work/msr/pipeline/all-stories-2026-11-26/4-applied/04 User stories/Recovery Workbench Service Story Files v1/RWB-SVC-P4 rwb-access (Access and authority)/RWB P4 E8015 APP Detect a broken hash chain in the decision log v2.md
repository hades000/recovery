# RWB-P4-E8015-APP Detect a broken hash chain in the decision log

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8015-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP06, DP13, DP19 |
| Parallel lane | L-P4-BI |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P4-E8015-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: app slice of RWB-E8-015 for rwb-access: the daily chain check of this service's own decision-record chain, the on-demand run of internal audit, the breach record and the two reads. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-E8015-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **internal audit (RW-AUDIT)**, I want **the Workbench to walk the hash chain of its own decision-record entries every day, to stop at the first entry that does not verify, to record the run with its outcome and the version in force, and to answer the runs and their breaches**, so that **a changed, missing or reordered record is found by the control itself instead of by a reader, and the finding reaches Compliance on the same business day**.

Inside `rwb-access` this is the control half of the legacy story RWB-E8-015:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- The chain this story walks is **this service's own** local decision-record chain in `rwb_access`, written through the library of DP-03. Each of the 19 services writes its local record where the decision is taken, and the one central chain over `rwb.decision-record.v1` is `rwb-decision`'s. The archive therefore carries two controls, not one: the owner verifies what it wrote, and P7 verifies the ledger (ADR-022; ASM-3798).
- Three deliverables and nothing else: the Schedule `chain-check-daily` on the `rwb-access` queue, which runs `AccessChainCheckWorkflow`; the write `POST /api/recovery/access/v1/admin/chain-checks`, which is the same workflow started by internal audit outside the schedule; and the read `GET /api/recovery/access/v1/admin/chain-checks`, which answers the runs this service recorded and filters to the breaches.
- The run row is not a new table. The result is one append to the local chain, and the read is a projection over the entries that carry the check's record code, so the record of a run is as untouchable as the record of an approval (BR2, BR8).
- The check is read-only on the chain it walks: it writes one entry of its own and moves a checkpoint, and it never repairs, rewrites, deletes or re-sequences an entry it found or did not find.
- The two paths are not ownership-map rows: no source names a chain-check endpoint. They are fixed on the DP-13 base by the contract of RWB-P4-E8015-CON and the point is carried in GAP-2293 and ASM-3799.
- A daily unattended run needs the workflow kit and a Schedule (the platform story RWB-PLT-E1071-CON). That dependency is not in this story's metadata build list, so the Schedule is built against the platform Schedule API and the missing H is raised at D1 (GAP-2296; ASM-3804). The metadata is not changed here.
- This story publishes no `rwb.access.<Event>.v1` message: the only message is `rwb.decision-record.DecisionRecorded.v1` (EV-08) on `rwb.decision-record.v1`, from the outbox of the run that records the result.

The legacy story's two endpoints (`/admin/rule-versions` and its approve path) and its data table (`decision_log_entry`, `rule_row`, `role`) belong to other keys and other services; they are read as the legacy copy of the generic administration template and are carried in GAP-2295, not implemented here.

### 2. Business rationale

REQ-DRI-002 (Must) says the decision log is append only, and REQ-DRI-003 (Must) says it is hash chained **and the chain integrity is checked every day, with a break reported to Compliance the same day**; NFR-035 repeats the target as a daily check with a same-day report. A chain that is never walked proves nothing: the hash link only becomes evidence when a control recomputes it on a schedule and records that it did.

The legacy story carried the feature inside the monolith (FEAT-ADM-10, RWB-E8-015), where the decision log was a table of the one recovery schema and one administration module could read it end to end. In the target there is no single table an administration module may read: every service writes its record into its own schema and P7 keeps the central ledger (Architecture v5 slides 20 and 28; DP-01; ADR-022). The control therefore splits by owner. `rwb-access` is the service that already holds the access log, the break-glass grants and the audit surface, and it holds the check for the entries it wrote; the central ledger and its 02:00 Schedule belong to RWB-P7-E1008-APP, which this story neither calls nor duplicates.

The split is what makes the control finishable in wave 4: no cross-service read, no C dependency on `rwb-decision`, and a check that runs on its own queue over its own rows. The evidence a reader needs is unchanged from the legacy intent: which window was checked, how many entries verified, where the walk stopped, when, and under which parameter and algorithm version. The three questions behind an audit finding, in order, are answered by one row and one written record, and a breach cannot be quietened because the next run walks the same window again until the chain verifies.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E8015-CON (same service, its own contract story) | The OpenAPI 3.1 document of the two operations, the `ChainCheck` and `ChainCheckPage` schemas, the outcome set, the error envelope, the consumed-operation list, the Schedule and workflow declarations and the five fakes. This story implements that document and adds no path |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the entry shape, the canonical form of a hash, the append, the hash-link check and the record codes |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the cadence, the start time, the batch size and the page bounds, as rows and not as code |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) that serves SCR-43 Roles and access and calls the two operations, one hop each |
| The platform workflow kit and Schedule API | The daily run and the on-demand run are one workflow started from a Schedule and from a request. The kit's own contract story is RWB-PLT-E1071-CON, which this story's metadata does **not** carry (GAP-2296; ASM-3804) |

Business preconditions carried from RWB-E8-015, from the feature specification and from the technical specification:

- The cadence is daily and the report to Compliance is same-day (REQ-DRI-003; NFR-035). The cadence itself is a parameter row read through DP-06, with the version in force written on the run; no interval is a constant in code (BR4).
- The rights in force are those of TSD P4 v3 T6.1: RW-AUDIT holds `R` in Platform administration, RW-PLATADM holds `CRUD`, RW-SECADM holds `CRUDA`, and the case roles hold a dash. Both operations authorise Platform administration R (BR3, ASM-3802). The legacy permission table's Rules and parameters `C` and `A` describes the rule-version feature of RWB-E8-007 and is carried in GAP-2295.
- The FSD P4 v3 A2.26.3.3 role table names the feature as one that runs unattended, with internal audit as the role that also uses it; that is the reading this story implements.
- The chain this service may walk is the one its own login owns: the local decision-record table of the DP-03 library in `rwb_access`. `decision_log_entry` is P7's and is not read (DP-01).
- The entry a run appends is the library's entry, not a new shape: `decision_code`, `case_id` empty, `inputs_ref`, the version, `decided_at`, `prev_hash` and `entry_hash` (DF-DEC-001 to DF-DEC-018).
- The record code, the order and batch of the walk, the start time of the Schedule and the same-day channel to Compliance are library codes and parameter rows; where a value is missing, section 11 carries the placeholder and its citation (GAP-2294; ASM-3801).

### 4. Flow

1. The Schedule `chain-check-daily` on the `rwb-access` queue starts `AccessChainCheckWorkflow` with the business date as its input and no personal data in it. The cadence and the start time are parameter rows read through DP-06 with the version in force (REQ-DRI-003).
2. `readCheckWindow` reads the checkpoint from the run store of the service (the `verifiedThrough` entry id of the last `CLEAN` run) and the head of the local chain from the DP-03 library, and fixes the window: the entries after the checkpoint up to the head, or none when the checkpoint is the head (BR5).
3. `recomputeChainRange` walks the window in the library's chain order in batches whose size is a parameter row. For each entry it recomputes the entry hash from the canonical form the library publishes and compares the `prev_hash` of the entry with the `entry_hash` of the entry before it (BR6).
4. A link that verifies moves the position on and counts one entry checked.
5. The first link that does not verify ends the walk: `outcome` is `BROKEN`, `firstBrokenEntryId` is that entry, `verifiedThrough` is the entry before it, and no entry after it is checked (BR6, AC4).
6. A walk that reaches the head with every link verified answers `outcome` `CLEAN`, `verifiedThrough` the head and `firstBrokenEntryId` null (BR6, AC1).
7. `recordCheckResult` appends exactly one entry to the local chain of DP-03 with the library's record code for a chain check, `case_id` empty, `inputs_ref` carrying the run row (window, counts, outcome, first broken entry, trigger, parameter version and the library's algorithm version), `decided_at` and the `prev_hash` and `entry_hash` the library computes (BR2, BR7, AC1).
8. The same transaction stages the outbox row, so `rwb.decision-record.DecisionRecorded.v1` is published from the outbox and never from the workflow (BR8).
9. A `CLEAN` run moves the checkpoint to `verifiedThrough`. A `BROKEN` run leaves the checkpoint where it was, so the next run walks the same window and re-raises the breach until the chain verifies or the owning team takes the incident path (BR7, BR9).
10. A `BROKEN` outcome **is** the control breach: the result entry plus the run row answered with `outcome` `BROKEN`, readable on SCR-43 Roles and access and on the read of step 12 on the same business day by the Compliance and PDPA officer and internal audit (REQ-DRI-003; ASM-3803).
11. Where the result entry, the checkpoint row or the outbox row cannot be written the transaction rolls back: no outcome is answered, no checkpoint moves and the Schedule's failure is alerted by the platform; the retry walks the same window and records one result (BR10, AC2).
12. `GET /api/recovery/access/v1/admin/chain-checks` answers the runs this service recorded: one item per run in `checkedAt` order then entry id, with `outcome`, `entriesChecked`, `verifiedThrough`, `firstBrokenEntryId`, `windowFrom`, `windowTo`, `trigger`, `checkedAt`, `entryId`, and `page`, `size`, `total` and the checkpoint entry id; `outcome=BROKEN` filters to the breaches, and page and size come from parameter rows (BR11, AC5).
13. `POST /api/recovery/access/v1/admin/chain-checks` starts the same workflow with `trigger` `ON_DEMAND` under an `Idempotency-Key`, under the same checkpoint rule, and answers 201 with the run row and the `Location` of the read (BR12, AC3).
14. Both operations authorise first: Platform administration R through the authorise operation of this service, one hop and cached for the session. A caller without it is refused with 403 and MSG-P4-002, no run is started, nothing is appended and no parameters row is read (BR3, AC3).
15. The service reads no row of `decision_log_entry`, no `rule_row` and no `case`: the central ledger and its own check are P7's, the rule registry is P7's, and a chain check addresses no case (BR5, DP-01).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The caller holds no Platform administration R | 403, no run started, no entry, no parameters read | MSG-P4-002 | AC3 |
| X2 | The caller's session has ended | 401, no run started and nothing appended | MSG-P4-001 | AC3 |
| X3 | The parameters read answers no cadence, no batch size or no page bound | The run is not started and the read answers 503; nothing is appended | MSG-P7-003 | AC2 |
| X4 | The checkpoint names an entry that no longer exists in the local chain | The walk starts from the chain head instead, the run row states the window it actually walked, and the finding is carried as a breach of type `WINDOW_RESET` | None | AC4 |
| X5 | The first link that does not verify is found | The walk stops, `outcome` `BROKEN`, `firstBrokenEntryId` set, `verifiedThrough` the entry before it, one entry appended | None | AC4 |
| X6 | The window is empty because the checkpoint is the chain head | The run answers `CLEAN` with `entriesChecked` 0 and `verifiedThrough` the checkpoint; one entry is appended so the control still shows a run | None | AC1 |
| X7 | The result entry, the checkpoint row or the outbox row cannot be written | The transaction rolls back, no outcome is answered, no checkpoint moves; the platform alerts the failed Schedule | MSG-P7-003 | AC2 |
| X8 | A second `POST` arrives with the same `Idempotency-Key` | The first result is replayed; one entry, one walk | None | AC3 |
| X9 | `page` or `size` is outside the bounds in force | 422 naming the field, no run row answered | MSG-GEN-001 | AC5 |
| X10 | A break-glass grant is active for the caller | The run proceeds and the answer carries the warning with the end time of the grant and the grant id in the entry | MSG-P4-004 | AC3 |

No exception path of this story changes a chain entry, a case, a task, a role, a permission or a rule: the walk is read-only on everything it inspects, and the only row it writes of its own is the entry of its own chain plus the platform library rows of the run.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P4-E8015-CON and its fakes; walks only its own chain, so no `rwb-decision` dependency and no cross-service read |
| Negotiable | The record code, the batch size, the start time and the page bounds are parameter rows and library codes; the outcome field names are settled with the contract story and with Internal audit |
| Valuable | Makes REQ-DRI-003 and NFR-035 provable for the entries this service wrote, and leaves a record that a changed record was found and when |
| Estimable | One workflow with three activities, one Schedule, two controllers, one chain walker, one result appender, one read projection, five fakes and six test cases |
| Small | Fits one sprint; no new table, no screen of its own and no event of its own |
| Testable | Each owned criterion has a test case in section 16; a break is provable against a seeded chain and the record failure against the library fake |

### 7. Acceptance criteria

```gherkin
Feature: Detect a broken hash chain in the decision log

  Background:
    Given the environment is SIT
    Given the chain walked is the local decision-record chain of rwb-access in schema rwb_access, and decision_log_entry of rwb_decision is not read
    Given test user "U-8101" holds RW-AUDIT, whose Platform administration letter is "R" in the SIT matrix
    Given test user "U-8110" holds RW-PHONECOL, whose Platform administration letter is a dash in the SIT matrix

  Scenario: AC1 Detect a broken hash chain in the decision log (legacy RWB-E8-015 AC1)
    Given the rwb-case contract mock returns the chain-check cadence, the start time, the batch size and their version in force
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then tests the log chain and raises a control breach if a record does not verify
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E8-015 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 A caller without Platform administration R is refused (new, D-RCV-60)
    Given "U-8110" holds RW-PHONECOL with a dash in Platform administration
    When "U-8110" calls POST /api/recovery/access/v1/admin/chain-checks with Idempotency-Key "k-015-3"
    Then the response is 403 with message MSG-P4-002 and no run is answered
    Then no chain-check entry is appended and the rwb-case contract fake records no parameters read
    When "U-8101" calls GET /api/recovery/access/v1/admin/chain-checks
    Then the response is 200 and the breach list is unchanged by the refusal

  Scenario: AC4 The walk stops at the first entry that does not verify (new, D-RCV-60)
    Given the local chain holds 5 entries and the entry_hash of entry "E-4" was changed after it was written, so its prev_hash no longer matches the entry_hash of entry "E-3"
    When the daily run walks the window from the checkpoint to the chain head
    Then the run answers outcome "BROKEN", firstBrokenEntryId "E-4", verifiedThrough "E-3" and entriesChecked 3
    Then entries "E-4" and "E-5" are not checked and no entry of the chain is repaired, rewritten or re-sequenced
    Then exactly one chain-check entry is appended with the run row and the parameter version in force
    When the next daily run starts
    Then it walks the same window again and answers outcome "BROKEN" with firstBrokenEntryId "E-4", because the checkpoint did not move

  Scenario: AC5 The run report answers one row per run and role codes only (new, D-RCV-60)
    Given a "CLEAN" run verified through entry "E-9" and a later "BROKEN" run stopped at entry "E-11"
    When "U-8101" calls GET /api/recovery/access/v1/admin/chain-checks
    Then the answer carries one item per run, each with outcome, entriesChecked, verifiedThrough, firstBrokenEntryId, windowFrom, windowTo, trigger, checkedAt and entryId
    Then the answer carries the checkpoint entry id "E-9" and the page, size and total it answered with
    Then no item carries a name, an e-mail address, a user reference or a case id
    When "U-8101" calls the same read with outcome "BROKEN"
    Then the answer carries the broken run only
```

AC1 and AC2 are the two criteria of RWB-E8-015, copied with their text unchanged; AC1 carries one added line at the top of its scenario, the parameters mock, so the run is provable while the `rwb-case` contract is still a fake. AC3 to AC5 are new under D-RCV-60 and test only what this service adds: the right, the stop at the first break and the run report.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The chain is walked every day and a break is reported the same business day; the daily check is the Schedule `chain-check-daily` of this service | REQ-DRI-003; NFR-035 |
| BR2 | The chain walked is this service's own local decision-record chain, and the record of a run is one append to it with the library's record code; a run is never a new table | ADR-022; DP-03; ASM-3798 |
| BR3 | Both operations need Platform administration R, authorised through the authorise operation of this service; a caller without it is refused with 403 and MSG-P4-002 and nothing is walked or written | TSD P4 v3 T6.1; FSD P4 v3 A2.26.3.3; ASM-3802 |
| BR4 | The cadence, the start time, the batch size and the page bounds are parameter rows read through DP-06 with the version in force, and the version is written on the run; no interval and no batch size is a constant in code | DP-06; BR-P4-026 |
| BR5 | The service walks only the rows its own login owns; `decision_log_entry`, `rule_row` and `case` are other services' and are never read | DP-01; Ownership Map v1 |
| BR6 | The walk recomputes the entry hash from the library's canonical form and compares each `prev_hash` with the `entry_hash` before it, in chain order, in batches; it stops at the first link that does not verify and checks no entry after it | RWB-E8-015 AC1; DP-03 |
| BR7 | Exactly one result entry is appended per run, inside the transaction that moves the checkpoint; a `CLEAN` run moves the checkpoint and a `BROKEN` run does not, so a break is re-raised until it is resolved | R-UNI-39; DP-03; ASM-3800 |
| BR8 | `rwb.decision-record.DecisionRecorded.v1` is published from the outbox of that transaction, with references, counts, versions and times and no case id and no personal field | DP-09; EV-08; NFR-040 |
| BR9 | The walk is read-only on the chain it inspects: no entry is repaired, rewritten, deleted or re-sequenced, and a break is a finding and not a write | REQ-DRI-002; DP-03 |
| BR10 | An answer that cannot be recorded is withheld: the transaction rolls back, no checkpoint moves, no outcome is answered and the failed Schedule is alerted | RWB-E8-015 AC2; REQ-DRI-005; DP-03 |
| BR11 | The read answers this service's own runs only, in `checkedAt` order then entry id, with `outcome=BROKEN` as its filter, and it never answers a name, an e-mail address, a user reference or a case id | DP-01; NFR-040; ASM-3800 |
| BR12 | An on-demand run and a scheduled run are one workflow under one checkpoint rule, and one `Idempotency-Key` answers one run and makes no second walk | Architecture v5 slide 42; DP-09 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 and BR12 are one Schedule and one request path onto the same workflow definition; the only difference is the `trigger` value on the run row.
- BR2 is the absence of a run table: the projection of section 12.7 reads the entries whose record code is the library's chain-check code, so the report inherits the append-only guarantee of the chain.
- BR5 is the absence of a foreign repository: the module has no view, no join and no synonym for `decision_log_entry`, `rule_row` or `case`.
- BR6 is the walker: the canonical form and the hash come from the library, and this service supplies the order, the batch and the comparison, never a second hash algorithm.
- BR7 is the checkpoint: `verifiedThrough` and the checkpoint row commit with the entry, and the two are never written apart.
- BR9 is the absence of a repair path: there is no update, no delete and no re-chain method on the chain, and a break is answered only by the incident path of the owning team.
- BR10 is the rollback and the alert on the failed Schedule; the retry is the platform's and it walks the same window.
- BR11 is the page shape of the read and the filter, with role codes and entry ids only.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Idle | The Schedule fires, or internal audit posts a run | The right is held and the parameters are in force | Window fixed |
| Window fixed | The walk starts | The checkpoint is before the chain head | Walking |
| Walking | A link verifies | `prev_hash` equals the `entry_hash` before it | Walking, one entry further |
| Walking | A link does not verify | `prev_hash` differs, or an entry hash cannot be recomputed | Stopped, outcome `BROKEN` |
| Walking | The head is reached | Every link verified | Stopped, outcome `CLEAN` |
| Stopped | The result is appended | The entry, the checkpoint and the outbox row commit | Recorded |
| Stopped | The result cannot be appended | The transaction fails | Idle, nothing recorded, the Schedule alerted |
| Recorded | `CLEAN` | None | Checkpoint moves to `verifiedThrough` |
| Recorded | `BROKEN` | None | Checkpoint unchanged; the breach stays open |

| Chain | Event | Outcome |
|---|---|---|
| Local decision-record chain | A run is recorded, a decision is taken, an approval is given | One entry appended with its `prev_hash` and `entry_hash`; no entry is ever updated or deleted |
| Checkpoint | `CLEAN` and `BROKEN` runs | One row per service, moved only by a `CLEAN` run |
| Central ledger | None | Not touched by this story; P7's chain is verified by RWB-P7-E1008-APP |

A breach is closed by a decision of the owning team, recorded as its own entry; this story neither closes nor annotates a breach, and the next run states whether the chain verifies again (BR7, BR9).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Internal audit (RW-AUDIT) | Reads the runs and the breaches, and starts an on-demand run: Platform administration `R` in TSD P4 v3 T6.1 |
| Compliance and PDPA officer (RW-COMPLY) | Reads the breach list on the same business day; starts no run unless a Platform administration right is granted |
| Platform administrator (RW-PLATADM) | Holds Platform administration `CRUD`; may start a run and operate the Schedule |
| Security administrator (RW-SECADM) | Holds Platform administration `CRUDA`; may start a run |
| A case role without a Platform administration letter (RW-CASEOWN, RW-PHONECOL) | Refused with 403 and MSG-P4-002; nothing is walked and nothing is recorded |
| The gateway-bff route | Calls the two operations on behalf of the signed-in user, one hop each, and passes the `Idempotency-Key` unchanged |
| The platform workflow kit | Starts the workflow from the Schedule and from the request, and records the failed run as an alert |
| `rwb-access` itself | Reads its own chain and its own checkpoint, appends one entry, and writes only its own rows |
| `rwb-decision` (P7) | Owns the central ledger, its chain and its 02:00 check; this story calls it not at all |
| `rwb-case` (P3) | Owns the parameters read; consumed one hop, never a table read |

The refusal shapes are 403 with an RFC 9457 problem response and `messageId` MSG-P4-002 for an absent right, 401 with MSG-P4-001 for no session, 422 with MSG-GEN-001 for a page bound, and 503 with MSG-P7-003 for a record or a parameters read that cannot be completed. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-E8015-CON.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the run entry: `decision_code` DF-DEC-003 with the library's chain-check code, `case_id` DF-DEC-002 empty, `inputs_ref` DF-DEC-008 with the window, the counts, the outcome, the first broken entry, the trigger, the parameter version and the algorithm version, `decided_at` DF-DEC-016, `prev_hash` DF-DEC-017 and `entry_hash` DF-DEC-018 | Write; and read for the walk and the report |
| DF-DEC-017, DF-DEC-018 | decision record (local library, DP-03) | `prev_hash` and `entry_hash` of every entry in the window | Read: the two values the walk compares |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read by the authorise operation of this service only, for Platform administration R |
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read by the authorise operation only; the answer carries role codes |
| (idempotency) | `idempotency_key` (platform library table in `rwb_access`) | the request and the stored answer of an on-demand run | Write and read (DP-09) |
| (outbox) | `outbox_event` | the record row of the run entry | Write |
| (checkpoint) | the service checkpoint row | the last verified entry id and the time it was set | Write on a `CLEAN` run; read at the start of every run |
| (inbox) | `processed_event` | none: this story consumes no event | None |
| parameters | `rwb_case` parameters | the cadence, the start time, the batch size and the page bounds, with the version in force | Returned through the P3 contract; not read |

No row of `decision_log_entry` is read or written: the central ledger is P7's, and this story writes and walks only its own chain in `rwb_access` (DP-01, BR5). No row of `case`, `task` or `rule_row` is read: a chain check addresses no case and evaluates no rule. The placeholder for a field the sources do not fix is carried where it is used: the record code of a chain check, the order and batch of the walk, the start time of the Schedule and the same-day channel to Compliance are Not specified in the source documents (GAP-2294; ASM-3801), and the name and shape of the checkpoint and the run-row fields are fixed by RWB-P4-E8015-CON (GAP-2293; ASM-3800). Field ids are those of the Logical Data Model and Data Dictionary v9 and of TSD P4 v3 T3.1.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| POST | `/api/recovery/access/v1/admin/chain-checks` | P4 `rwb-access` | No body; header `Idempotency-Key` required | `checkId`, `outcome` (`CLEAN` or `BROKEN`), `entriesChecked`, `verifiedThrough`, `firstBrokenEntryId`, `windowFrom`, `windowTo`, `trigger` `ON_DEMAND`, `checkedAt`, `entryId`, with `Location` of the read | 401 (MSG-P4-001); 403 (MSG-P4-002); 503 (MSG-P7-003) | Platform administration R | Required; a replay answers the first result and makes no second walk |
| GET | `/api/recovery/access/v1/admin/chain-checks` | P4 `rwb-access` | Query `outcome`, `page`, `size` | `ChainCheckPage`: `items[]` of the run row, `checkpointEntryId`, `page`, `size`, `total` | 401 (MSG-P4-001); 403 (MSG-P4-002); 422 (MSG-GEN-001); 503 (MSG-P7-003) | Platform administration R, scope applied | Not applicable, read only |

Both operations sit on the base `/api/recovery/access/v1` of DP-13. Asynchronous work never answers 202: the on-demand run completes inside the request budget and answers the run row, or it answers 503 and records nothing (BR10). `page` defaults to its parameter row and `size` is capped by it, both read through DP-06 and never from code (BR4). `GET /admin/chain-checks` is not an ownership-map row; the path, the outcome set and the field names are fixed by RWB-P4-E8015-CON (GAP-2293; ASM-3799).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (own service) | The Platform administration R check behind both operations, cached for the session; MSG-P4-002 on a refusal |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case` | The cadence, the start time, the batch size and the page bounds, with the version in force (DP-06) |

One hop per call, 2 s timeout and a breaker per downstream (DP-11). No operation of `rwb-decision`, `rwb-case` (other than the parameters read) or any other service is called: the central ledger and its check are P7's and the chain walked is this service's own.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | the hash-chained entry of a chain check: the window, the counts, the outcome, the first broken entry, the trigger, the parameter version and the algorithm version |

CloudEvents 1.0 envelope, from the outbox of the transaction that appends the entry and moves the checkpoint. The payload carries identifiers, counts, versions and times, and no case id, no name, no e-mail address and no personal field. This story publishes no `rwb.access.<Event>.v1` message: the administration events of `rwb-access` belong to RWB-P4-E1037-APP and RWB-P4-E8008-APP, and a chain check adds neither.

#### 12.4 Events consumed

None. `rwb-access` subscribes to no topic for this capability; the run is started by its own Schedule or by its own request, and no `processed_event` row is written.

#### 12.5 Workflows and activities

| Element | Kind | Queue | Use |
|---|---|---|---|
| `AccessChainCheckWorkflow` | Workflow | `rwb-access` | One run: window, walk, result, checkpoint |
| `readCheckWindow` | Activity | `rwb-access` | Reads the checkpoint and the chain head through the DP-03 library and fixes the window |
| `recomputeChainRange` | Activity | `rwb-access` | Recomputes the hashes and compares the links in batches, stopping at the first break |
| `recordCheckResult` | Activity | `rwb-access` | Appends the result entry, moves the checkpoint on a `CLEAN` run and stages the outbox row |

Namespace `rwb-recovery`; one workflow and three activities with no personal data in any input or output (NFR-040). The workflow is started by the Schedule of section 12.6 and by the on-demand operation of section 12.1.

#### 12.6 Schedules

| Schedule | Queue | Cadence | Input | Use |
|---|---|---|---|---|
| `chain-check-daily` | `rwb-access` | Daily, from the parameter row in force with its version; the start time is a parameter row | The business date | The daily check of REQ-DRI-003 and NFR-035, replacing the legacy in-process trigger |

No other Schedule belongs to this story. The access review Schedule (JOB-18) is RWB-P4-AD008-APP's.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| the local decision-record table of the DP-03 library | P4, in `rwb_access` | The result entry of a run, the walk over the window and the report projection |
| `permission` | P4 (rwb_access) | The Platform administration letters, read by the authorise operation only |
| `role` | P4 (rwb_access) | The role codes the authorise answer carries |
| the checkpoint row of this service | P4, in `rwb_access` | The last verified entry id, moved only by a `CLEAN` run |
| `idempotency_key`, `outbox_event` | Platform library, in `rwb_access` | The on-demand request row and the record row of the entry |

No table of another service is named (DP-01): `decision_log_entry` is P7 `rwb_decision`'s, the parameters are P3's, and `case`, `task` and `rule_row` are not touched.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| authorise fake | `POST /authorise` granting Platform administration R to RW-AUDIT, RW-PLATADM, RW-SECADM, RW-DATASTEW, RW-COE and RW-COMPLY, and refusing RW-PHONECOL with MSG-P4-002 | This story, contract tests, harness |
| parameters fake | `GET /admin/parameters` with the cadence, the start time, the batch size and the page bounds as rows, with the version in force | This story, contract tests |
| decision-record fake | The append with its `prev_hash` and `entry_hash`, the hash-link check, the canonical form, a forced failure and a seeded chain of any length | This story, contract tests, harness |
| chain fixture | A seeded five-entry chain, one variant with the `entry_hash` of entry "E-4" changed after it was written and one clean variant | Tests of AC1 and AC4 |
| gateway-bff fake | The SCR-43 Roles and access route: the breach list of this read merged with the access log of RWB-P4-AD007-APP, one hop each | Screen route, harness |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The run and the report provided; the authorise and the parameters reads consumed; one hop, 2 s timeout |
| Kafka | 1 published, 0 consumed | `rwb.decision-record.DecisionRecorded.v1` through the DP-03 outbox |
| Temporal | 1 workflow, 3 activities, 1 Schedule | `AccessChainCheckWorkflow` on queue `rwb-access`; `chain-check-daily` |
| File | 0 | No file input and no file answer |

### 13. Solution plan

**Deliverables.** `ChainCheckController` (POST and GET), `ChainCheckService`, `ChainCheckpointRepository`, `ChainWalker` (canonical form, hash comparison, first-break stop), `ChainCheckResultAppender` (the DP-03 append, the checkpoint and the outbox in one transaction), `AccessChainCheckWorkflow` with its three activities, the `chain-check-daily` Schedule, the authorise and parameters clients, the read projection with its filter and paging, and the six test cases of section 16.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/access/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependency-added column records the build dependency of the owning story. The workflow kit and its Schedule API are a platform prerequisite of the daily run and are not in this story's metadata list (GAP-2296; ASM-3804).

**Build steps**

1. The controller pair on the DP-13 base with the contract's schema, the problem responses and the `Idempotency-Key`.
2. The parameters reader and the authorise client, with the session cache and the 2 s budget.
3. `readCheckWindow`: the checkpoint, the head, the window rule and the empty-window case.
4. `recomputeChainRange`: the library's canonical form, the batch loop, the comparison per link and the first-break stop.
5. `recordCheckResult`: one transaction for the entry, the checkpoint and the outbox row, and the rollback that withholds the answer.
6. The workflow and its three activities on queue `rwb-access`, and the `chain-check-daily` Schedule started from the parameter rows.
7. The read projection with the `outcome` filter, the ordering, the paging and the checkpoint entry id.
8. The five fakes and the two chain fixtures.
9. The six test cases; a break is proved against the seeded chain and the withheld answer against the forced failure.

**Feature switch.** The run is switched by the service baseline of RWB-P4-E8015-CON and by the cadence parameter row; the document of the contract declares no 404 branch and this story adds no flag of its own.

**Done when.** The daily Schedule records one `CLEAN` or `BROKEN` run per day on a seeded chain, an on-demand run answers one row, the report answers the runs and the breaches without personal data, a forced record failure leaves no outcome and no checkpoint move, and the harness of the wave 4 audit journey has accepted the evidence.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A caller without Platform administration R calls either operation | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | `page` or `size` is outside the bounds in force | Enter {field}. |
| MSG-P7-003 | The result entry, the checkpoint or the outbox row cannot be written, or a parameters row the run needs is missing | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. |

The texts are copied unchanged from the legacy story RWB-E8-015; MSG-GEN-001 is the general field message of the FSD. The message IDs are contract elements of RWB-P4-E8015-CON, and this story answers no sixth message and no business text of its own.

### 15. Screens and states

| Screen | State | What the screen consumes |
|---|---|---|
| SCR-43 Roles and access, audit panel | Day clean | The latest run row with outcome `CLEAN`, `entriesChecked`, `verifiedThrough` and `checkedAt` |
| SCR-43 Roles and access, audit panel | Breach | The latest run row with outcome `BROKEN`, `firstBrokenEntryId`, `verifiedThrough` and the time, and the list filtered to `outcome=BROKEN` |
| SCR-43 Roles and access, audit panel | Running | The run in flight with the trigger `ON_DEMAND` and the checkpoint it started from |
| SCR-43 Roles and access, audit panel | Refused | The 403 of the envelope with MSG-P4-002 and no row |
| SCR-43 Roles and access, audit panel | Not recorded | The 503 of the envelope with MSG-P7-003 and no row |
| SCR-43 Roles and access, audit panel | Break-glass warning | The warning of the session read, shown as the MSG-P4-004 banner over the panel |

The panel is served by the gateway-bff composite route (DP-19), which calls this read and the access log of RWB-P4-AD007-APP in parallel, one hop each, and merges them. This story renders no screen of its own; the screen field list belongs to the Epic 8 screen work and to RWB-PLT-N001-CON. The legacy screens SCR-39 Rules and parameters and SCR-41 Delegation of authority are the rule-version and limit screens and are not part of this feature (GAP-2295).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-015-01 | AC1 | Integration | A seeded 8-entry chain with every link verifying; the daily Schedule fires; one entry appended with outcome `CLEAN`, the window, the counts and the parameter version in force |
| TC-E8-015-02 | AC2 | Component | The DP-03 append answers a forced failure; the transaction rolls back, no outcome is answered and MSG-P7-003 is returned; the checkpoint is unchanged |
| TC-E8-015-03 | AC3 (Access) | Component | "U-8110" holds RW-PHONECOL with a dash in Platform administration; both operations answer 403 with MSG-P4-002, no entry is appended and no parameters row is read |
| TC-E8-015-04 | AC2 (Principle 5) | Integration | A forced decision-record write failure stops the action with MSG-P7-003; the failed Schedule is alerted and the retry records one result |
| TC-E8-015-05 | AC4 | Component | A five-entry chain with the `entry_hash` of "E-4" changed; outcome `BROKEN`, `firstBrokenEntryId` "E-4", `verifiedThrough` "E-3", `entriesChecked` 3; the next run re-raises it |
| TC-E8-015-06 | AC5 | Component | One `CLEAN` and one `BROKEN` run; the report answers one item per run, the checkpoint entry id and the paging; no name, e-mail address, user reference or case id; the `outcome=BROKEN` filter |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. TC-E8-015-01 to TC-E8-015-04 are the four legacy rows of RWB-E8-015 and keep their Covers values as the legacy story states them: AC1, AC2, the access refusal and Principle 5. No `-ITG` copy appears in this table, because no integration slice is split from this key in this Work Package.

### 17. Guardrails

- No business value in code: the cadence, the start time, the batch size, the page bounds and the record code are parameter rows or library codes (BR4).
- No personal data in events, workflow inputs, logs or the report: entry ids, counts, versions, outcome codes, role codes and times only (BR8, BR11, NFR-040).
- The chain walked is this service's own; `decision_log_entry`, `rule_row` and `case` are never read, joined or viewed (DP-01, BR5).
- The walk is read-only: no entry is repaired, rewritten, deleted or re-sequenced, and a break is a finding that only the owning team's decision can close (REQ-DRI-002, BR9).
- One REST base and one topic per service; the paths of this story sit on `/api/recovery/access/v1` and it declares no `rwb.access.<Event>.v1` message (DP-13).
- Every fixture is synthetic: no production entry, no production hash and no personal field is copied into a test or a fake.
- The error and CloudEvents envelopes come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Element in this story | Test cases |
|---|---|---|---|
| REQ-DRI-002 | The decision log is append only; a record cannot be changed or deleted | The result is one append to the DP-03 chain; no update, delete or re-chain path exists; the report is a projection (BR2, BR9) | TC-E8-015-01, TC-E8-015-05 |
| REQ-DRI-003 | The decision log is hash chained and the chain integrity is checked every day, with a break reported to Compliance the same day | The `chain-check-daily` Schedule, the walk, the `BROKEN` outcome and the same-day breach row (BR1, BR6, BR7) | TC-E8-015-01, TC-E8-015-05, TC-E8-015-06 |
| NFR-035 | The decision log hash chain is checked daily, and a break is reported to Compliance the same day | The daily run and the breach list the Compliance role reads; a failed run is alerted (BR1, BR10) | TC-E8-015-04, TC-E8-015-06 |
| REQ-ACA-007 | Access requested outside the authority matrix is refused and the refusal is recorded | Platform administration R on both operations, 403 with MSG-P4-002, and no run, no entry and no parameters read on a refusal (BR3) | TC-E8-015-03 |

The requirement IDs are taken from the Program BRD under the fill order of Template and Rules §R7.3, because the Work Package carries no requirement list for this story; the FSD P4 v3 requirements table serves the same module.

### 19. Out of scope

- The central decision ledger, its chain and its 02:00 chain check with the 15-minute break report (RWB-P7-E1008-APP); this story neither calls nor repeats it.
- The decision log query API for audit (RWB-P7-E2005-APP) and the write side of the ledger (`rwb.decision-record.v1` ingest, P7).
- The access log writer, the break-glass grant and the access event (RWB-P4-E1039-APP, RWB-P4-AD006-APP, RWB-P4-AD007-APP); the audit panel merges this read with the access log and consumes its rows.
- The rule-version operations and the data table of the legacy story: the rule package registry is P7's (RWB-P4-E8007-APP, RWB-P4-AD011-APP, RWB-P4-AD012-APP), and the legacy endpoints are carried in GAP-2295.
- The reference-data and parameter administration of the same module (RWB-P4-AD009-APP, RWB-P4-AD010-APP) and the access review Schedule JOB-18 (RWB-P4-AD008-APP).
- A notification channel to Compliance through `rwb-comms`; the same-day report of this story is the breach row and the report read (ASM-3803).
- The workflow kit, the namespace and the Schedule API (RWB-PLT-E1071-CON), the parameters client (RWB-PLT-E1042-CON) and the composite route (RWB-PLT-N001-CON).
- The schema migration, the indexes, the grants, the deployment, the Helm chart, the dashboards and the runbook: the DB, OPS and INF slices of the same key outside this Work Package.
- The cross-service journey harness and its evidence (the wave 4 integration epic).
