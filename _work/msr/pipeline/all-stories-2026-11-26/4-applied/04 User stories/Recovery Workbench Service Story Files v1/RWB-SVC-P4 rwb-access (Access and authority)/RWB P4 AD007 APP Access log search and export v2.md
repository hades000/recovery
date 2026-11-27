# RWB-P4-AD007-APP Access log search and export

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-AD007-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP07, DP13, DP19 |
| Parallel lane | L-P4-A |
| Ready to start | After RWB-P4-E1039-APP |
| Depends on (build) | RWB-P4-AD007-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-N001-CON, RWB-P4-E1039-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-007 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-AD007-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **internal auditor**, I want **the access log of `rwb-access` searched by person reference, date, event and capability area, with the role and the matrix and masking versions in force shown on every entry, and the result exported with the same masking as the screen**, so that **I can show who accessed what without asking IT, and every answer says which version of the permission matrix and of the masking policy its entries were read under**.

Inside `rwb-access` this is the access-log search and export capability of the legacy story RWB-AD-007:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- Two deliverables, and nothing else: the read `GET /api/recovery/access/v1/admin/access-log`, which answers an `AccessLogPage` of decision records with the decision code AC-READ, AC-DENY or AC-EXPT, the actor reference, the capability area, the right, the case or document or data-product reference, the role code, the matrix version, the masking version, the grant id, the incident reference and the decided time; and the read `GET /api/recovery/access/v1/admin/access-log/export`, which answers the same rows as `text/csv` with the same masking.
- `rwb_access` holds no separate access-log table. An access event is a decision-record entry of the local library of DP-03, written by RWB-P4-E1039-APP (legacy RWB-E1-039) in the same transaction as the action it records, hash-linked to the entry before it and published as `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`. The central ledger for the whole estate is P7's `decision_log_entry` in `rwb_decision`; this story reads the local chain and never `rwb_decision`.
- RWB-P4-E1039-APP owns the access event writer, the entry shape, the break-glass grant and the first read of the chain. This story adds the audit search over that chain — the four filters, the ordering, the paging and the versions in the answer — and the export operation over it.
- The screen SCR-43 Roles and access is served through the gateway-bff composite route of DP-19; this story renders no screen of its own.
- The central decision-log view for the whole estate, the query API over `rwb_decision`, the chain verification and the daily ledger seal stay in `rwb-decision` (P7). This story runs no workflow, opens no case state and writes no business row.

Whether the audit search must span the whole central ledger and not only the local chain of `rwb_access` is Not specified in the source documents (GAP-0801; ASM-1502).

### 2. Business rationale

Access to a case, a document or a data product is only defensible if somebody can show, after the fact, who looked at what, under which role and under which version of the permission matrix and of the masking policy. Today that question is a request to IT: the legacy key records the access event through `DecisionLogWriter` into a single decision log table inside the monolith (FEAT-ACA-07, FEAT-ACA-08) and the search is a SQL screen nobody outside IT can run (FEAT-ACA-16, RWB-AD-007). In the target, the record is written by its owner in the owner's own schema, hash-linked, and collected centrally within five minutes (Architecture v5 slide 28; ADR-022), so the local chain is the first and complete answer for the events `rwb-access` itself produced, and it is answerable without a call to another service.

This story therefore builds the one read an internal auditor needs — search by staff user reference, period, event and capability area, with the role and the versions that were in force — and the export that carries the same masking, so an audit request is answered by the auditor and not by the platform team. It meets REQ-ACA-006 (every read is written to the access log, and the log is therefore readable) and supports REQ-DRI-012 (audit can query the record of what happened, with the versions) on the access side, REQ-ACA-007 (a refusal is recorded, so the refusal must also be findable) and NFR-042 (every read of the case store and the document store is logged and reviewable). The export is the evidence for the internal audit and the compliance and PDPA officer, and it is the input to FEAT-ACA-16.

The one rule that makes the read trustworthy is R-UNI-39: no action proceeds unlogged. This story carries the same rule on the read side — a search and an export are themselves access events, and neither is answered when its own entry cannot be written, so the log can never be missing the question that produced an answer.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E1039-APP (same service, its own story) | The access event writer, the entry shape inside the local decision-record chain of DP-03, the break-glass grant and its warning MSG-P4-004, and the first read of the chain. This story searches and exports what that story writes |
| RWB-P4-AD007-CON (same service, its own contract story) | The published OpenAPI 3.1 document of the two reads, the `AccessLogEntry` and `AccessLogPage` schemas, the CSV column order, the error envelope and the contract fakes. This story builds against it and changes no schema |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the read over the chain and the entry this story appends for its own search and its own export |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the page default, the page maximum and the export cap, as rows and not as code |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the reference-data contract of `rwb-case` (DP-07): LOV-CAPABILITY, LOV-EVENT and LOV-SCOPE with the version in force |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) that serves SCR-43 and calls the two reads, one hop each |

Business preconditions carried from RWB-AD-007:

- The permission row of a role in the capability area is data: `permission` holds the letters C, R, U, D and A or a dash for none, with the matrix version. The roles that hold Platform administration R are RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM and RW-SECADM (legacy permission checks; TSD P4 v3 T6.1).
- The access events of a week exist in the chain before the read is demonstrated: the sign-ins and the refusals of the SIT users, written by RWB-P4-E1039-APP, with the sealed synthetic data of RWB-P4-E1065-APP.
- The matrix and the masking policy in force in SIT are the ones RWB-P4-E1037-APP loaded; the entries carry the version they were written under, so a later version does not rewrite history.
- The event list LOV-EVENT and the capability-area list LOV-CAPABILITY are reference data of `rwb-case` under the R-PREC default ruling and the ownership map (ASM-0071). This story reads them through DP-07 and holds no copy of them.
- The retention of an access entry is Not specified in the source documents (GAP-0805; ASM-1506).

### 4. Flow

1. The internal auditor opens SCR-43 Roles and access, panel access log, through the gateway-bff composite route (DP-19), which calls `GET /api/recovery/access/v1/admin/access-log` on `rwb-access` with `user` (a staff user reference), `from`, `to`, `event`, `capabilityArea`, `page` and `size`.
2. `AccessLogController` validates the query. `from` and `to` are required and a period that ends before it starts is refused; `user`, `event` and `capabilityArea` are optional filters; a value that is not a staff user reference is refused. No read is made and no entry is written when the query is refused.
3. The controller resolves the caller's session and calls `POST /api/recovery/access/v1/authorise` on its own service, one hop with a 2 s timeout and a cached answer, for Platform administration R. A caller without the right is refused with 403 and MSG-P4-002, and exactly one entry with decision code AC-DENY is written for the refusal before the refusal leaves the service.
4. `AccessLogSearchService` reads the local decision-record chain of `rwb_access` over the period, filtered by the actor reference, the event and the capability area, ordered by `decided_at` then by entry id so the paging is stable, and paged with the page default and the page maximum read through DP-06.
5. The actor reference of each entry is resolved through the service's own `v_ace_iam_group` ACE view (DP-05) for the group the role is bound to. No name, no e-mail address and no personal field is read, returned or logged: the search takes a staff user reference only (BR3).
6. Scope filters the answer: a caller whose scope does not cover an entry does not see it, and an out-of-scope search returns an empty page with total 0. It never answers 404 and never names a case, so the read cannot be used to probe for the existence of a case.
7. The answer is an `AccessLogPage`: `items`, `page`, `size`, `total`, `matrixVersion`, `maskingVersion`, `chain`, `coveredFrom` and `coveredTo`. The two version fields state the version the returned entries were read under, and `chain` with the period names the chain and the period the answer covers.
8. Where a break-glass grant is active for the caller, the answer carries the warning MSG-P4-004 with the end time of the grant, the gateway shows the banner, and every entry written under the grant carries the grant id and the incident reference.
9. The export is the same query at `GET /api/recovery/access/v1/admin/access-log/export`: `text/csv` in UTF-8, one header row in the order of section 12.1, the same rows in the same order and the same masking as the screen. The cap is 10,000 rows; above it the answer is 422 and no file and no entry are produced.
10. Every search appends one entry with decision code AC-READ, and every successful export appends one entry with decision code AC-EXPT carrying the filter of the query, the row count and no case id. Both appends are decision-record entries of the local library (DP-03) written in the same transaction as the answer, with their outbox row.
11. Where the record cannot be written, the answer is not returned: the call fails with 503 and MSG-P7-003, because an access event that is missing cannot be reconstructed later (R-UNI-39; legacy RWB-E1-039).
12. The chain is hash-linked entry to entry (`prev_hash`, `entry_hash`). This story reads the links of the period it answers and shows the head it read; the verification of the whole chain and the daily seal are `rwb-decision`'s (P7) and are not built here.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | `from` or `to` is empty | 422, no read, no entry | MSG-GEN-001 | AC1 |
| X2 | The period ends before it starts | 422 naming `to` and `from`, no read, no entry | MSG-GEN-003 | AC1 |
| X3 | An event code or a capability area is not in its list in force | 422 naming the field, no read, no entry | MSG-GEN-001 | AC1 |
| X4 | A `user` value is not a staff user reference | 422 naming `user`; no name is accepted in its place | MSG-GEN-001 | AC1 |
| X5 | The caller holds no Platform administration R | 403 and one entry with decision code AC-DENY, actor reference, area and right R | MSG-P4-002 | AC3 |
| X6 | The caller's session has ended | 401, no read and no entry | MSG-P4-001 | AC3 |
| X7 | The search matches nothing, or lies outside the caller's scope | 200 with an empty `items` and total 0; never a 404 and never a named case | None | AC1 |
| X8 | The export matches more than the cap | 422, no file, no AC-EXPT entry; the count is named in the response | Not specified in the source documents (GAP-0802; ASM-1503) | AC4 |
| X9 | The entry for the search or for the export cannot be written | 503 and no answer; the search and the file are not given | MSG-P7-003 | AC4 |
| X10 | A break-glass grant is active for the caller | The warning is returned with the answer and every entry written under the grant carries the grant id and the incident reference | MSG-P4-004 | AC5 |

No exception path of this story changes a case, a task, a role or a permission: this service reads its own chain and appends its own entries, and the state machine of access is RWB-P4-E1039-APP's and RWB-P4-E1037-APP's.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the contract of RWB-P4-AD007-CON and its fakes; the access events it reads are written by RWB-P4-E1039-APP and the filters read the row tables of its own schema only |
| Negotiable | The page bounds, the export cap, the event list and the capability areas are rows and reference data; the CSV column order is fixed by the contract and reviewed with audit |
| Valuable | One search and one export replace an IT request and a screen only the platform team can run, and every answer states the versions it was read under |
| Estimable | One controller, one search service, one export writer, three read repositories, one record appender, one contract-fake run and six test cases |
| Small | Fits one sprint with its tests; no new table, no workflow, no schedule and no screen of its own |
| Testable | Each owned criterion has a test case in section 16; the search is provable against a seeded chain and the refusal against a role without the right |

### 7. Acceptance criteria

```gherkin
Feature: Access log search and export

  Background:
    Given the environment is SIT
    Given test user "U-4101" holds RW-AUDIT with Platform administration R
    Given test user "U-4106" holds only RW-PHONECOL and holds no right in the capability area "PLATFORM_ADMINISTRATION"
    Given the access log of rwb-access holds the read, refusal and export entries of a week

  Scenario: AC1 Search (legacy RWB-AD-007 AC1)
    Given the rwb-case contract mock returns reference version "REF-2026.11" in force with LOV-CAPABILITY, LOV-EVENT and LOV-SCOPE
    Given sign-ins and refusals for a week
    When I search by person and date
    Then the matching entries show with the role and versions in force

  Scenario: AC2 Export (legacy RWB-AD-007 AC2)
    Given a search result
    When I export it
    Then the file carries the same masking as the screen

  Scenario: AC3 A caller without the Platform administration right is refused (new, D-RCV-60)
    Given test user "U-4106" holds only RW-PHONECOL
    When "U-4106" calls GET /api/recovery/access/v1/admin/access-log with from 2026-11-16 and to 2026-11-22
    Then the response is 403 with message MSG-P4-002 and no entry is returned
    Then exactly one entry is written with decision code "AC-DENY", actor reference "U-4106", capability area "PLATFORM_ADMINISTRATION" and right "R"

  Scenario: AC4 The export cap and the export entry (new, D-RCV-60)
    Given a search with from 2026-11-16 and to 2026-11-22 matches 10,001 entries
    When the same query is exported
    Then the response is 422 with no file and no entry is written
    When the same query is exported over 37 of those entries
    Then the response is 200 with media type text/csv, one header row and 37 rows
    Then exactly one entry is written with decision code "AC-EXPT", the filter of the query, the row count 37 and no case id

  Scenario: AC5 Every answer names the versions its entries were read under (new, D-RCV-60)
    Given the entries of the week were read under matrix version "MAT-2026.11" and masking version "MSK-2026.11"
    When the search is answered for test user "U-4101"
    Then the answer states matrixVersion "MAT-2026.11" and maskingVersion "MSK-2026.11"
    Then the answer names the chain it read and the period the chain covers
    Given break-glass grant "BG-2026-000412" for incident "INC0004521" is active until 14:30
    Then the answer carries the warning MSG-P4-004 with the time "14:30"
    Then every entry written under the grant carries grant id "BG-2026-000412" and incident reference "INC0004521"
    Then an entry written under masking version "MSK-2026.10" keeps "MSK-2026.10" in the answer
```

AC1 and AC2 are the legacy criteria of RWB-AD-007, copied with their text unchanged and their values kept; AC1 carries one added line at the top of its scenario, the reference-data mock, so the search is provable while the reference-data contract is still a fake. AC3 to AC5 are new under D-RCV-60 and test only what this story adds.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The access log is searched by staff user reference, period, event and capability area, and every entry shows the role and the versions in force | RWB-AD-007 AC1; FEAT-ACA-16; FSD P4 v3 A2.16 |
| BR2 | An access entry carries the decision code AC-READ, AC-DENY or AC-EXPT, the actor reference, the capability area, the right, the case or document or data-product reference, the role code, the matrix version, the masking version, the grant id, the incident reference and the decided time | FSD P4 v3 A2.7; REQ-ACA-006; LDM v8 DF-DEC-001 to DF-DEC-018 |
| BR3 | The search takes a staff user reference only: no name is accepted, returned or logged, and no personal field leaves the service | FSD P4 v3 A2.16.3.2; NFR-040; ASM-1505 |
| BR4 | A caller must hold Platform administration R; a caller without it is refused with MSG-P4-002 and the refusal is recorded as one AC-DENY entry | REQ-ACA-007; TSD P4 v3 T6.1 and API-P4-008 |
| BR5 | A search outside the caller's scope returns nothing; it is never a 404 and never names a case | TSD P4 v3 T6.2; FSD P4 v3 A2.16.3.3 |
| BR6 | The export carries the same rows, the same order and the same masking as the screen, one header row, and it is capped at 10,000 rows with 422 above the cap | RWB-AD-007 AC2; ASM-1503 |
| BR7 | Every search appends one AC-READ entry and every successful export one AC-EXPT entry, in the same transaction as the answer; an answer that cannot be recorded is not returned | R-UNI-39; FEAT-ACA-07; MSG-P7-003 |
| BR8 | The masking version recorded on an entry is the version that masks it in the answer and in the export; a later masking version does not rewrite an old entry | ASM-1504; NFR-039 |
| BR9 | Every answer states the matrix version and the masking version its entries were read under, and names the chain and the period it covers | FSD P4 v3 A2.16; Architecture v5 slide 28 |
| BR10 | While a break-glass grant is active the warning MSG-P4-004 is returned, and every entry written under the grant carries the grant id and the incident reference | FSD P4 v3 A2.9; VR-P4-007-1 |
| BR11 | The page default, the page maximum and the export cap are parameter rows read through DP-06; no bound is a constant in code | DP-06; BR-P4-016 |
| BR12 | The capability areas, the events and the scopes are reference lists read through DP-07 with the version in force; no value is copied into code | DP-07; BR-P4-016 |
| BR13 | The retention of an access entry follows the decision log's retention rule; no separate rule is built for the access log | NFR-030; ASM-1506 |
| BR14 | The local chain is the source of the search; the central ledger of `rwb_decision` is never read, and the end-to-end ledger view belongs to the integration story | DP-01; ASM-1502 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 and BR9 are one query over the chain with the four filters and the period as predicates, plus two version fields in the answer: the version is a column of each entry, so the answer cannot name a version the entry was not written under.
- BR2 is the shape of the entry the writer of RWB-P4-E1039-APP produced; this story adds no field to it and reads it as it stands.
- BR3 is the absence of a name in the request and in the answer: the filter is a reference, the ACE view is read for the group of that reference, and no personal column is selected.
- BR4 is the authorise call in step 3 of section 4; the refusal is one entry and not a silent 403.
- BR6 is the same select for both operations plus a writer that emits the header row once and counts the rows before it streams; the cap is checked before the first byte leaves.
- BR7 is the record appender of DP-03 inside the transaction that produces the answer, for both operations.
- BR8 is the absence of a re-mask on read: the masking version and the masked field list of the entry decide the rendering, and no current rule is applied to an old entry. Which masking version applies to an old entry in an export is Not specified in the source documents (GAP-0803; ASM-1504); the version recorded on the entry applies and is shown in its `masking_version` column.
- BR11 and BR12 are reads through the client libraries of DP-06 and DP-07 at request time, with the version in force; a changed bound or a new list value is data.
- BR14 is a repository that has no connection to `rwb_decision` and no join across a schema.

### 9. State transitions

This story holds no case, task, role or permission state. The states it answers are the states of a query, and the chain it reads is append-only.

| From | Event | Condition | To |
|---|---|---|---|
| No query | A search is asked | `from` and `to` present and ordered, filters valid | Query validated |
| Query validated | Authorise answers granted | Platform administration R held | Read issued |
| Query validated | Authorise answers refused | Platform administration R absent | Refused, one AC-DENY entry |
| Read issued | The chain answers | The period holds entries | Answered with items and the two versions |
| Read issued | The chain answers | No entry matches or none is in scope | Answered with an empty page and total 0 |
| Answered | The record is appended | The append commits | Answer returned |
| Answered | The record cannot be appended | The append fails | 503 with MSG-P7-003, no answer |
| Export requested | The match count is over the cap | None | 422, no file, no entry |
| Export requested | The match count is within the cap | None | CSV streamed, one AC-EXPT entry |

| Chain | Event | Outcome |
|---|---|---|
| Append-only local chain | A search, a refusal or an export | One entry appended with its `prev_hash` and `entry_hash`; no entry is ever updated or deleted |
| Append-only local chain | A masking policy or matrix version changes | New entries carry the new version; old entries keep theirs and are read under it |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Internal auditor (RW-AUDIT) | Search the local access chain and export the result; the primary reader (FSD P4 v3 A2.16.3.3) |
| RW-COE, RW-DATASTEW, RW-COMPLY, RW-PLATADM, RW-SECADM | Hold Platform administration R and may therefore read the same search and the same export; the export is the evidence they attach |
| A role without Platform administration R | Is refused with 403 and MSG-P4-002, and the refusal is written as one AC-DENY entry |
| The gateway-bff route | Calls the two reads on behalf of the signed-in user, one hop each, and never caches an answer across users |
| `rwb-access` itself | Reads `role`, `permission` and `masking_rule` in its own schema, its own ACE view and its own chain; it writes only entries of its own chain |
| `rwb-decision` (P7) | Owns the central ledger, the chain verification and the daily seal; this story calls it not at all |

The refusal shape is 403 with an RFC 9457 problem response and `messageId` set to MSG-P4-002, and the unauthenticated shape is 401 with MSG-P4-001. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-E1037-CON.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read: the Platform administration R letter and the matrix version |
| DF-REF-198 to DF-REF-204 | `masking_rule` | id, role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read: the masking version that applies to an entry |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the access entry: `decision_code` DF-DEC-003 (AC-READ, AC-DENY, AC-EXPT), `case_id` DF-DEC-002 empty for an access event, `inputs_ref` DF-DEC-008 with the actor reference, the area, the right, the references, the role code, the matrix version, the masking version, the grant id and the incident reference, `actions` DF-DEC-014, `decided_at` DF-DEC-016, `prev_hash` DF-DEC-017 and `entry_hash` DF-DEC-018 | Read; and write for the entry this story appends for its own search and its own export |
| `v_ace_iam_group.entra_group` | the service's own ACE view (DP-05) | the Entra group of the actor reference, and nothing else | Read |
| DF-REF-159 to DF-REF-184 | `reference_version`, `reference_row` of `rwb-case` | LOV-CAPABILITY, LOV-EVENT and LOV-SCOPE with the version in force | Read through the reference-data contract |
| (outbox) | outbox library table in `rwb_access` | the record row of a search and of an export | Write |
| (inbox) | `processed_event` | none: this story consumes no event | None |

No row of `case`, `document`, `assignment` or `rule_package` is read: the case is `rwb-case`'s (P3), the document is `rwb-document`'s (P5), the assignment is `rwb-case`'s and the rule registry is `rwb-decision`'s (P7), and no foreign key crosses a schema (DP-01). No row of `decision_log_entry` is read or written: the central ledger is P7's and the local record goes on `rwb.decision-record.v1`. The case, document and data-product references in an entry are references the writer recorded, not joins.

The field-level placement of the access facts inside `inputs_ref` is fixed by the entry of RWB-P4-E1039-APP and by the schema of RWB-P4-AD007-CON; this story reads it and adds no field. Whether a person may be searched by name is Not specified in the source documents (GAP-0804; ASM-1505): the search takes a staff user reference only, and no name is accepted, displayed or logged. Field IDs are those of the Logical Data Model and Data Dictionary v9.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| GET | `/api/recovery/access/v1/admin/access-log` | P4 `rwb-access` | Query: `user` (staff user reference), `from`, `to`, `event`, `capabilityArea`, `page`, `size` | `AccessLogPage`: `items` of the entry of section 11, `page`, `size`, `total`, `matrixVersion`, `maskingVersion`, `chain`, `coveredFrom`, `coveredTo` | 401 (MSG-P4-001); 403 (MSG-P4-002); 422 (MSG-GEN-001, MSG-GEN-003); 503 (MSG-P7-003) | Platform administration R, scope applied | Not applicable, read only; no Idempotency-Key |
| GET | `/api/recovery/access/v1/admin/access-log/export` | P4 `rwb-access` | The same query | `text/csv`, UTF-8, one header row, the rows of the query in the same order and with the same masking as the screen; 10,000 rows maximum | 401; 403; 422 (the cap, and the two validation messages); 503 | Platform administration R, scope applied | Not applicable, read only |

`page` defaults to 50 and `size` to a maximum of 200, both read from the parameters contract (DP-06) and never from code. The CSV column order is `decided_at, decision_code, actor_reference, capability_area, right, case_reference, document_reference, data_product_reference, role_code, matrix_version, masking_version, grant_id, incident_reference`; the screen shows the same columns in the same order, so the file carries the same values and the same masking as the screen (AC2).

The export format, its columns and its cap are Not specified in the source documents (GAP-0802; ASM-1503): the shape above is the one this story and its contract fix, and the review confirms it with audit before the endpoint is frozen. The operation `GET /admin/access-log` is the one API-P4-008 names on the base `/api/recovery/access/v1` of DP-13; this story adds the export path beside it and changes no other operation of the service.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (own service) | The Platform administration R check behind both reads, cached for the session; MSG-P4-002 on a refusal |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case` | The page default 50, the page maximum 200 and the export cap 10,000, with the version in force (DP-06) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 `rwb-case` | LOV-CAPABILITY, LOV-EVENT and LOV-SCOPE in force (DP-07) |

One hop per call, 2 s timeout and a breaker per downstream (DP-11); the answers are cached for the session or for the life of the request. No operation of `rwb-decision`, `rwb-document` or `rwb-case` beyond the parameters and reference lists is called.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | the hash-chained entry of a search (AC-READ), of a refusal (AC-DENY) and of an export (AC-EXPT) |

CloudEvents 1.0 envelope; the payload carries references, codes, versions and times and no name, no e-mail address and no personal field. This story publishes no `rwb.access.<Event>.v1` message: the access policy is changed by RWB-P4-E1037-APP and the access event itself is written by RWB-P4-E1039-APP.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 (events: none), and a read of the local chain needs no subscription.

#### 12.5 Workflows and activities

None. This story starts no workflow, signals no workflow and registers no activity on the `rwb-access` queue. The six-monthly access review list (JOB-18) is a Schedule of `rwb-access` and belongs to RWB-P4-AD008-APP.

#### 12.6 Schedules

None. The search and the export are request-driven.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | Read only: the role code and class of an entry's role |
| `permission` | P4 (`rwb_access`) | Read only: the Platform administration R letter and the matrix version |
| `masking_rule` | P4 (`rwb_access`) | Read only: the masking version and the field list that apply to an entry |
| the local decision-record table of the DP-03 library | P4, in `rwb_access` | Read: the access entries of the period. Write: the entry of the search and of the export |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | The outbox row of each appended entry; no inbox row is written because no event is consumed (DP-09) |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written: the central ledger is P7's |

`lov_value`, `reference_version` and `reference_row` are reference data of P3 under the ownership ruling and are read through DP-07; no table of another service is read and no foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| authorise fake | RWB-P4-E1037-CON, RWB-P4-AD007-CON | The granted answer for RW-AUDIT, RW-COE and RW-PLATADM with Platform administration R, and the refused answer with MSG-P4-002 for RW-PHONECOL |
| decision-record fake | RWB-PLT-E1027-CON | A seeded chain of a week with AC-READ, AC-DENY and AC-EXPT entries under matrix version MAT-2026.11, masking versions MSK-2026.11 and MSK-2026.10, one grant entry with grant id BG-2026-000412 and incident INC0004521; the append, the hash-link check and the forced failure of AC4 |
| parameters fake | RWB-P3-E1042-CON | The page default 50, the page maximum 200 and the export cap 10,000 |
| reference-data fake | RWB-P3-E1043-CON | LOV-CAPABILITY, LOV-EVENT and LOV-SCOPE at version REF-2026.11 |
| gateway-bff fake | RWB-PLT-N001-CON | The composite route of SCR-43 with the access-log panel and the export state |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2 (the search and the export); consumed 3 | Base `/api/recovery/access/v1`; one hop, 2 s timeout |
| Kafka | Published 1 event type; consumed 0 | `rwb.decision-record.v1` through the DP-03 library |
| Temporal | 0 workflows, 0 activities | The `rwb-access` queue carries the access review Schedule of RWB-P4-AD008-APP only |
| File | 1 CSV answer | The export response; no file input and no file store |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/accesslog`, Java package `th.co.scb.ace.workbench.recovery.access.accesslog`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none: the group of the actor reference is read through the service's own `v_ace_iam_group` |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the in-process read of the single decision log table (DP-01 and DP-03: a local hash-linked chain in `rwb_access`, read by its owner) and the ace-web screen that ran the query in process (DP-19: a gateway-bff composite route). DP-01, DP-02, DP-09 and DP-11 are applied as constraints of the service baseline and add no dependency of their own; they are not in the pattern list the Work Package fixes for this story and are not claimed.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AccessLogController | Controller | The two reads: query validation, paging, the RFC 9457 problem responses, the cap check before the first byte |
| AccessLogSearchService | Service | The period, actor, event and capability-area predicates over the chain, the scope filter, the ordering, the two version fields and the chain name |
| AccessLogExportWriter | Service | The CSV rows and header in the column order of section 12.1, the same masking as the screen, the row count and the cap |
| AccessLogRepository | Repository | Read-only queries over the local decision-record table of DP-03 in `rwb_access`, with the period window and the filters; no write method |
| PermissionReader | Service | The `permission` and `role` rows of the caller and the Platform administration R letter with its matrix version |
| MaskingReader | Service | The `masking_rule` row that applies to an entry by role and masking version |
| ActorGroupReader | Service | The `v_ace_iam_group` read of the actor reference (DP-05); no personal column |
| AccessEventAppender | Service | The AC-READ, AC-DENY and AC-EXPT entry with its outbox row, in the transaction that produces the answer (DP-03, DP-09) |
| CaseDataClient | Client | The parameters and reference lists through DP-06 and DP-07, one hop, 2 s timeout, cached |

**Database and migrations**

- This story creates no table and owns no Flyway version of its own. `role`, `permission` and `masking_rule` are created by RWB-P4-E1037-APP and the local decision-record table by RWB-P4-E1039-APP in the per-service sequence of DP-15; this story reads them.
- The read predicates are the period window, the actor reference, `decision_code`, the capability area and the right; if the SIT query plan needs an index that the creating story does not have, the index is added to that story's migration, not to a new one here.
- No write statement exists in the repository: the class exposes no save, update or delete, so a search can never change an entry. The only write of this story is the append through the DP-03 library.
- The append and its outbox row commit in one transaction; a failure rolls them back and the answer is not returned (MSG-P7-003).

**Configuration and reference data**

- The page default 50, the page maximum 200 and the export cap 10,000 are parameter rows of `rwb-case` read through DP-06 with the version in force; no bound is a constant in code (BR11). Their names are fixed by the contract of RWB-P4-AD007-CON.
- LOV-CAPABILITY (14 areas), LOV-EVENT and LOV-SCOPE are read through DP-07 at the version in force (RWB-P3-E1043-CON); no capability area, event or scope is a constant in code (BR12).
- The matrix version and the masking version are columns of the entry and of the permission and masking rows; the read never computes a current version and applies it to an old entry (BR8).

**Build steps**

1. `AccessLogRepository` with the read-only queries, the period window and the stable ordering; test that a second page never repeats or skips an entry.
2. `AccessLogSearchService` with the four filters, the scope filter and the empty answer of X7; tests for AC1 and for the period and list refusals of X1 to X4.
3. `PermissionReader` and the authorise call of step 3; tests for AC3, including the single AC-DENY entry.
4. `MaskingReader` and the version of an entry; test that an entry under MSK-2026.10 keeps its version while MSK-2026.11 is in force (AC5, BR8).
5. `AccessLogExportWriter` with the header row, the column order and the cap; tests for AC4, including the 422 above the cap and the AC-EXPT entry of the successful export.
6. `AccessEventAppender` and the 503 when the record cannot be written; test for X9 (TC-AD-007-04).
7. `CaseDataClient` over the parameters and reference-data fakes, so the story builds before `rwb-case` is in the environment; test that a changed bound is data and needs no build (BR11).
8. The contract-fake run of both reads through the gateway-bff fake, so the screen can be demonstrated while SCR-43 is being built.
9. The denial test through the guard for a role without Platform administration R, and the service-identity test of section 10.

**Feature switch.** The search and the export are read paths and carry no switch of their own. The panel is shown on SCR-43 by the gateway-bff route when the service baseline is on (RWB-P4-E1037-CON); this story adds no flag and removes nothing.

**Done when.** The tests in section 16 pass; a search by staff user reference and period answers the entries with their role and the two versions in SIT; a caller without Platform administration R is refused with MSG-P4-002 and leaves one AC-DENY entry; an export over the cap answers 422 with no entry and an export of 37 rows answers the CSV and one AC-EXPT entry; every answer states the matrix version and the masking version it was read under; and a break-glass entry carries its grant id and incident reference.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The caller has no session | Your session has ended. Sign in again to continue. | This story, on both reads |
| MSG-P4-002 | The caller holds no Platform administration R | You cannot {action} here. Your role does not include it. | This story, on both reads; one AC-DENY entry |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. | This story, in the answer of both reads |
| MSG-GEN-001 | A required field is empty, a user value is not a staff user reference, or a code is not in its list | Enter {field}. | This story, on both reads |
| MSG-GEN-003 | The period ends before it starts | {field} cannot be before {other}. | This story, on both reads |
| MSG-P7-003 | The entry of the search or of the export cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on both reads |
| the export cap message | The export matches more than the cap | Not specified in the source documents (GAP-0802; ASM-1503) | This story, before the first byte of the file |

Every error from this service is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. The business texts are copied unchanged from the legacy story where the message already existed.

### 15. Screens and states

The access log is one panel of SCR-43 Roles and access, served by the gateway-bff composite route of DP-19, which calls the search of this story and the session read of `rwb-access` in parallel, one hop each.

| Screen | State | What it shows |
|---|---|---|
| SCR-43 Roles and access | Access log, list | The entries of the query with the actor reference, the capability area, the right, the case or document or data-product reference, the role code, the matrix version and the masking version, paged |
| SCR-43 Roles and access | Access log, filtered | The same list narrowed by person reference, period, event and capability area, with the filters valid against the reference lists in force |
| SCR-43 Roles and access | Access log, empty | An empty list with total 0 and no error, also when the entries exist outside the caller's scope |
| SCR-43 Roles and access | Export | The CSV answer with one header row and the same columns, the same order and the same masking as the screen; the row count of the file is the row count of the entry |
| SCR-43 Roles and access | Export over the cap | The refusal of X8 with the match count and no file |
| SCR-43 Roles and access | Break-glass warning | The banner with MSG-P4-004 and the end time of the grant, over the list, with the grant id and the incident reference on each entry written under it |
| SCR-43 Roles and access | Refused | The MSG-P4-002 refusal for a role without Platform administration R; no list is shown |

The legacy story named SCR-39 Rules and parameters and SCR-40 Reference data in its screen table although the access-log read sits on neither; the target screen is SCR-43 Roles and access, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON and to the Epic 8 screen work. This story renders no screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-007-01 | AC1, BR1, BR2 | Contract | The search by staff user reference and period over the seeded chain, with the reference lists at version REF-2026.11 and the role and versions on every entry |
| TC-AD-007-02 | AC2, BR6 | Component | An export of a search result: the same rows, the same order, the same masking and one header row |
| TC-AD-007-03 | AC3, BR4 | Component | A caller with RW-PHONECOL and no Platform administration R: 403, MSG-P4-002 and one AC-DENY entry |
| TC-AD-007-04 | AC4, BR7 | NFR | The record store forced to fail during a search and during an export: 503, MSG-P7-003 and no answer |
| TC-AD-007-05 | AC4, BR6 | Component | A match of 10,001 entries answered 422 with no entry, and a match of 37 entries answered as CSV with one AC-EXPT entry, the filter and the row count |
| TC-AD-007-06 | AC5, BR8, BR9, BR10 | Component | Entries under MSK-2026.11 and MSK-2026.10, and one entry written under grant BG-2026-000412 with incident INC0004521 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The four legacy rows are kept: TC-AD-007-01 and TC-AD-007-02 for AC1 and AC2, TC-AD-007-03 for the access refusal and TC-AD-007-04 for the forced record failure; two rows are added for the new criteria of this story. The legacy level System maps to Component or Contract as the row shows, Access to Component and Resilience to NFR. The ITG copy of the set is the integration story's and is not written here, so no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in code: the page bounds and the export cap are parameter rows (BR11), the capability areas, events and scopes are reference lists with a version (BR12), and a test proves that a new list value or a changed bound needs no build.
- No personal data anywhere: the search takes a staff user reference, the answer carries references, codes, versions and times, and no name, e-mail address or personal field appears in the answer, the CSV, the entries or the tests (BR3, NFR-040).
- No read of another service's tables (DP-01): `case`, `document` and `assignment` are their owners', `decision_log_entry` is P7's, and no join crosses a schema. The references in an entry are values, not foreign keys.
- ACE data only through the owner's contract or the service's own `v_ace_*` view: this story reads `v_ace_iam_group` for the group of an actor reference and nothing else (DP-05).
- One writer for an entry: only the append of DP-03 writes the chain, and the repository of this story has no write method, so a search can never change history.
- No answer without its record: the entry of a search and of an export commits with the answer, and the answer is withheld with MSG-P7-003 when it cannot be written (BR7, R-UNI-39).
- The read is idempotent and ordered: the same query answers the same page, and the ordering is total, so a retry never repeats or skips an entry.
- A refused caller learns nothing about the data: the refusal names the missing right and nothing else, and an out-of-scope search is empty and never a 404 that would confirm a case.
- Masking is a property of the entry: the version recorded on the entry decides the rendering, and the export can never be less masked than the screen.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-006 | Every read is written to the access log, and the log is readable | Program, Access and audit | FEAT-ACA-07, FEAT-ACA-16 | 20 Administer access and audit | BR2, BR7 | TC-AD-007-01, TC-AD-007-04 |
| REQ-ACA-007 | An access outside the matrix is refused and the refusal is recorded | Program, Access and audit | FEAT-ACA-07 | 20 Administer access and audit | BR4 | TC-AD-007-03, TC-AD-007-06 |
| REQ-DRI-012 | Audit can query the record for a population and receive it with versions and the final call | Program, Data and reporting | FEAT-ACA-16 | 20 Administer access and audit | BR1, BR8, BR9 | TC-AD-007-01, TC-AD-007-05, TC-AD-007-06 |
| REQ-ACA-013 | The administration screens for roles, permissions and delegation are available to the security administrator | Epic 8 BRD | FEAT-ACA-16 | 20 Administer access and audit | BR5, BR9 | TC-AD-007-02, TC-AD-007-06 |

The requirement IDs are taken from the FSD feature table and the Program BRD under the fill order of Template and Rules §R7.3, because the Work Package carries the requirement list of this story empty; the set is fixed by the FSD "Requirements served" rows and does not change.

| Legacy reference | Where it is kept |
|---|---|
| AC1 search by person and date, with the role and the versions in force | Sections 4, 7, 8, 12.1, 13 |
| AC2 export with the same masking as the screen | Sections 4, 7, 8, 12.1, 16 |
| MSG-P4-004, MSG-P4-001, MSG-P4-002, MSG-GEN-001, MSG-P7-003 | Section 14, exception paths |
| The permission check on Platform administration R for the six roles | Sections 3, 10, 12.1 |
| TC-AD-007-01 to TC-AD-007-04 | Section 16 |
| Rule IDs R-UNI-38, R-UNI-39 and R-UNI-40 | Sections 2, 8, 17 |
| Field IDs DF-REF-034 to DF-REF-044, DF-REF-198 to DF-REF-204, DF-DEC-001 to DF-DEC-018 | Section 11 |
| Legacy screens SCR-39 and SCR-40 as the story named them | Section 15, carried to SCR-43 Roles and access |
| Legacy key RWB-AD-007, story RWB-P4-AD007-APP, contract RWB-P4-AD007-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The access event writer, the entry shape, the break-glass grant and its warning: RWB-P4-E1039-APP. This story reads what that story writes.
- The central decision ledger, the query API over `rwb_decision`, the chain verification and the daily seal: `rwb-decision` (P7), and the end-to-end ledger view is the integration story's.
- The permission matrix, the masking policy and the role administration: RWB-P4-E1037-APP and the Epic 8 administration stories.
- The access review list (JOB-18) and the six-monthly Schedule: RWB-P4-AD008-APP.
- The screen SCR-43 Roles and access itself, its panels beyond the access log and its composite route specification: RWB-PLT-N001-CON and the Epic 8 screen work.
- The report of access events in `rwb-reporting` and the monthly measure of refusals.
- The retention job of the chain and the deletion of an entry after its retention period: no entry is deleted here, and the retention rule is the decision log's (BR13).
- The integration harness and the `-ITG` copies of the test cases.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
