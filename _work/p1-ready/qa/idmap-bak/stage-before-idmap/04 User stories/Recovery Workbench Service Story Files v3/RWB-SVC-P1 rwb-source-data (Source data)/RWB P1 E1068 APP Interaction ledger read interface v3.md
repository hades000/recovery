# RWB-P1-E1068-APP Interaction ledger read interface

**Version 3 changes.**
- Full `Interaction` response, shared Problem body, query status codes, UUID `caseId`, read order and ledger resource of the contract 5.1.0 (RD-P1-004, 005, 007, 009, 023).
- Parameters read through `GET /api/recovery/case/v1/parameters/{key}` (RD-P1-028); flag off answers 404 (RD-P1-045); access-log record fields from GAP-0586.
- DEF-052: RWB-P3-E1018-CON and RWB-P1-E1066-CON added as contract dependencies; closure requested.
- AC rewrites and AC14 to AC24 from the review; test case IDs of Test Cases v9.
- Review findings fixed: 1 to 4, 6 to 12, 14, 18, 19, 23, 25 to 29. Left pending with an owner: 5, 13, 15, 16, 17, 21, 22, 24. Finding 20 needs no change (GAP-0587 resolved by directive).
- Batch D: rwb-asset is named as a service reader of the case ledger for the delivery state of a notice (RD-P1-064); its permission row is Pending (NEW-GAP-G2-finish-2).

**Version and date.** v3, 27 November 2026.

**Change log.** D-RCV-60, 27 November 2026: applied RD-P1-004, RD-P1-005, RD-P1-007, RD-P1-009, RD-P1-023, RD-P1-028 and RD-P1-045; resolved dependency finding DEF-052 in the story header and recorded a request to close the defect row. Agent: S6-stories.

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1068-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-068 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P1-E1068-APP-16); the squad sizes it at refinement |
| Patterns applied | DP01, DP06, DP07, DP08, DP11, DP15, DP18, DP19 |
| Parallel lane | L-P1-P |
| Ready to start | After RWB-P1-E1066-APP |
| Depends on (build) | RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1066-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P4-E1037-CON, RWB-P3-E1018-CON, RWB-P1-E1066-CON |
| Contract version | 5.1.0 (Recovery Workbench API Specification v7, rwb-source-data.yaml; Interaction resource) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-029, FR-P1-030) |
| Readiness decisions | RD-P1-004, RD-P1-005, RD-P1-007, RD-P1-009, RD-P1-023, RD-P1-028, RD-P1-045, RD-P1-064 |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: moved from RWB-E1-068 for rwb-source-data. The in-process `InteractionLedgerReader.read()` of the monolith and the P3 interactions handler over it become one REST read operation of this service, `GET /cases/{caseId}/interactions` on base `/api/recovery/source-data/v1` (DP-11), so rwb-case and every other consumer read the ledger through this contract and no longer through an in-process interface or the table; the `interaction` table stays P1's own table in schema `rwb_source_data` and the read stays a local query on it with no join across a schema (DP-01, DP-18; ownership ruling of R-PREC, the Ledger owned by rwb-source-data); the `CaseScopeQuery` local check becomes one call of the rwb-case case contract with a 2 s budget and no cached scope, and masking plus the PII access-log write become calls of the rwb-access authorise and masking contract (DP-08, DP-11); the page-size default and maximum become parameters of the rwb-case parameters contract and the channel filter becomes LOV-CHANNEL of the rwb-case reference-data contract (DP-06, DP-07); the `(case_id, actor_ref)` index for the actor filter is added on the per-service Flyway sequence and `ix_interaction_case_time` is kept (DP-15); the screens that read the ledger arrive through gateway-bff (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1068-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 18 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **to read a case's ledger in one ordered sequence, filtered by channel, actor or date range**, so that **I can see what has happened to it before I decide anything**.

This is the read slice of legacy RWB-E1-068, and it owns the whole legacy key: **AC1** to **AC8**. AC1 (the ledger reads in one ordered sequence), AC2 (it can be filtered), AC3 (it is available to the case record and no class outside the ledger package queries the table), AC4 (a date range in the wrong order is refused), AC5 (a case outside the caller's scope is refused), AC6 (the summary is masked when no masking rule allows it), AC7 (page size at and above the limit) and AC8 (a case with no entries) are all proved here, and this key has exactly one slice.

It delivers: the read operation `GET /cases/{caseId}/interactions` with the filters `channel`, `actor`, `from`, `to` and the paging `page`, `size`, answering an `InteractionPage` of entries ordered by `occurred_at` and then `case_seq`; the ordered, filtered and paged query on this service's own `interaction` table with the actor index that serves the actor filter; the scope check as one call of the rwb-case case contract, a case that does not exist and a case outside the caller's scope answering the same 404 with MSG-P4-003 as the legacy story says; the masking of `interaction.summary` through the rwb-access masking contract and the PII access-log write when a personal field is returned unmasked; the page-size default and maximum and the channel list read as data through the rwb-case parameters and reference-data contracts; and the route the screens arrive through, the gateway-bff composite route of DP-19.

It builds no ledger row, no append and no intake map: those are RWB-P1-E1066-APP and RWB-P1-E1067-APP. It writes no row of its own table and changes nothing in the ledger. It builds no screen: SCR-03 and SCR-04 arrive through gateway-bff and are the screen owners'.

### 2. Business rationale

A case owner who decides a route, a settlement or a legal step must first know what was said, promised, sent and done on the case. One read interface returns the ledger in order with the source of each entry, filters it by channel, actor and date range, and masks personal content by role on the same rules as the case record. The case record view and every other consumer read through this interface, so there is one ordering and one masking rule for the history. Serves REQ-ILG-006, REQ-ILG-003 and REQ-ILG-014; NFR-070 (one case history read in under 2 seconds at its 2031 size; DL11).

In the target the read is a service operation instead of an in-process interface of the monolith. The ledger is P1's table in `rwb_source_data` (DP-01, DP-18; the R-PREC default ruling that the ledger belongs to rwb-source-data), so the read is served by the service that owns the rows and not by a P3 handler that borrowed them. rwb-case keeps its case record and its timeline, and reads this ledger through this contract, one hop, 2 s, with a breaker; no other service queries `interaction` and nothing is joined across a schema.

Two of the three things the monolith did in one method call now cross a boundary. The scope of the case is answered by rwb-case over the case contract and is never a local join and never a cached answer, because a stale scope answer is a scope leak. The masking decision and the PII access-log write are answered by rwb-access, so that one masking policy covers the ledger and the case record alike, and a personal field with no unmasking rule for the caller's role comes back masked rather than missing (BR-P1-015-2). The third, the order, stays local: one table, one index on `(case_id, occurred_at)` and the tie-break on `case_seq`, so the whole history of a case reads in under 2 seconds at its 2031 size.

### 3. Preconditions

- RWB-P1-E1066-APP is done: the `interaction` table exists in `rwb_source_data` with its ledger columns, its two unique keys and the index `ix_interaction_case_time` on `(case_id, occurred_at)`, and entries can be appended and read.
- RWB-P1-E1001-APP is done: schema `rwb_source_data` exists with the base `interaction` table, its standard record columns and the dictionary rows of P1 (legacy RWB-E1-001 in the target).
- The per-service Flyway sequence of rwb-source-data exists with its own history table in schema `rwb_source_data`, and the baseline version has been applied on it (DP-15; RWB-PLT-E1044-CON).
- The interaction-ledger contract of RWB-P1-E1066-CON is published: the `Interaction` and `InteractionPage` schemas, the error envelope and the contract fakes. The read operation of section 12.1 is added to that resource document and is never a second draft of it.
- RWB-PLT-E1042-CON is on the classpath and RWB-P3-E1042-CON is published with its fake, so the parameters `rwb.dataengine.ledger.page-size-default` (50) and `rwb.dataengine.ledger.page-size-max` (200) are read through `GET /api/recovery/case/v1/parameters/{key}` and never written in code (DP-06; RD-P1-028). Their catalog rows are not yet in Recovery Workbench Parameter Catalog v1 and are requested from its owner.
- RWB-PLT-E1043-CON is on the classpath and RWB-P3-E1043-CON is published with its fake, so the list **LOV-CHANNEL** is served as data: MOBILE, HOME_PHONE, WORK_PHONE, LINE, EMAIL, POSTAL_ADDRESS, CALL, VISIT, SMS, LETTER, PORTAL, BRANCH (DP-07).
- RWB-PLT-E1037-CON is on the classpath and RWB-P4-E1037-CON is published with its fake, so the authorise answer and the masking rows for `interaction.summary` are read through the rwb-access contract (DP-08).
- RWB-PLT-N001-CON exists: the gateway-bff composite route through which SCR-03 and SCR-04 arrive; this story serves the data behind it and adds no screen of its own (DP-19).
- The caller holds Case record R on the case, and the roles `rwb_source_data` and the login of this service exist in DEV and SIT with the credential held by the platform and never written in code, a test or a runbook (DP-02; Architecture v5 slides 11 and 29).
- The final ruling maps a case outside the caller's scope to the same 404 MSG-P4-003 as a missing case; 403 MSG-P4-002 remains for a caller whose role has no Case record R. RWB-P3-E1018-CON owns the case-contract response (ASM-0825).
- Open decisions DL10, DL11 and DL26 are still open; this story builds on their assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 (DL10), ASM-0553, ASM-0703, ASM-1051 and ASM-1104 (DL11), and ASM-0247, ASM-0264, ASM-0275 and ASM-0355 (DL26).

### 4. Flow

1. The history panel of SCR-03, or the timeline of SCR-04, calls `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` through gateway-bff with `channel`, `actor`, `from`, `to`, `page` and `size` (DP-11, DP-19).
2. `InteractionReadController` binds the path and the query parameters and refuses a request that does not match the published operation (12.1).
3. `ParameterClient` reads the page-size default 50 and the page-size maximum 200 through `GET /api/recovery/case/v1/parameters/{key}`, and `ReferenceDataClient` reads **LOV-CHANNEL** from the rwb-case reference-data contract, so both are data and never constants (DP-06, DP-07).
4. `LedgerFilterValidator` checks the filter after the right is confirmed: `channel` is a value of LOV-CHANNEL, `from` is not after `to`, `size` is between 1 and 200, `page` is 0 or more; a malformed value or a channel outside the list answers 400 with MSG-GEN-001 or MSG-GEN-007; an out-of-range value or an inverted date range answers 422 with MSG-GEN-002 or MSG-GEN-003 and the field name (RD-P1-004) (AC4, AC7).
5. `CaseScopeClient` calls `GET /api/recovery/case/v1/cases/{caseId}` once with the caller's token, one hop, 2 s budget: 200 means in scope; 404 becomes 404 MSG-P4-003 (missing and out of scope alike); any other status or a timeout becomes 503 MSG-GEN-006 (AC5, AC9). The outcomes apply in the order 401, 403 (no right), 400 or 422, 404 (scope), 503, so a caller without the right learns nothing about the case (AC11).
6. `MaskingClient` calls the rwb-access masking contract once for the caller's roles and the field `interaction.summary`, 2 s timeout and a breaker; with no unmasking rule, every summary is returned as `MASKED` (DP-08; AC6).
7. `AuthoriseClient` confirms Case record R for the caller on the case through the rwb-access authorise contract; a role without the right is refused with 403 and MSG-P4-002 and the refusal is logged; no answer, a 5xx or an open breaker is 503 MSG-GEN-006 (DP-08; AC11, AC15).
8. `InteractionQueryRepository` runs one read-only query on `rwb_source_data.interaction`: `case_id` equal, the optional `channel`, `actor_ref` and `occurred_at` range, ordered by `occurred_at` and then `case_seq`, with `limit` and `offset`; the date window and the order use `ix_interaction_case_time` and the actor filter uses `ix_interaction_case_actor` (12.7). No other table is joined and no other schema is touched (DP-01).
9. `LedgerReadService` masks the summary of each entry that the masking answer does not unmask, and returns the channel, direction, result, promise amount and promise date in full (AC6).
10. When a personal field is returned unmasked, `PiiAccessLogClient` writes the read to the rwb-access access log with user, role, case ID, data product, field ID and time, and never a value (GAP-0586; ASM-0828); when that write fails, the read is refused with 503 MSG-GEN-006 rather than returned unmasked (BR-P1-015-4). The operation and payload of the write are not published in rwb-access.yaml (Pending, NEW-GAP-S6-12).
11. `InteractionReadController` answers 200 with an `InteractionPage`: `items` of `Interaction`, each with its event code, time, actor type and reference, channel, direction, result, promise amount and date, source system and source reference, plus `page`, `size` and `total` (AC1, AC2).
12. A case with no matching entry answers 200 with 0 items and total 0, and the panel shows the Empty state with MSG-P3-024 (AC8).
13. The call changes nothing: no row of the ledger is written, updated or deleted, and the read takes no lock (AC3, §17).
14. Screen states of SCR-03 and SCR-04 for this read: Loading (skeleton rows); Empty is the state of AC8; Error shows the message of section 14, MSG-GEN-006 among them; No access is the refusal of steps 5 and 7 (MSG-P4-003 and MSG-P4-002).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | `from` is after `to` | 422; nothing returned | MSG-GEN-003 | AC4 |
| X2 | The case is outside the caller's scope, or does not exist | 404; nothing returned | MSG-P4-003 | AC5 |
| X3 | No masking rule allows the caller to see the summary | Summary returned as "MASKED" | None | AC6 |
| X4 | Page size outside 1 to 200, or channel outside LOV-CHANNEL | Size: 422 and no items; channel: 400 and no items | MSG-GEN-002; MSG-GEN-007 | AC7, AC17 |
| X5 | The case has no matching entries | 200 with items=[] and total=0; the consuming screen shows its Empty state with MSG-P3-024 | MSG-P3-024 (screen) | AC8 |
| X6 | The rwb-case case contract does not answer inside 2 s, or answers 503 | The read is refused with 503 and MSG-GEN-006; no scope answer is guessed from a cache and no entry is returned | MSG-GEN-006 | AC9 |
| X7 | The rwb-access masking contract is open-circuit or does not answer inside 2 s | Every summary is returned as "MASKED" and no unmasked field is returned; the read is not refused | None | AC6 |
| X8 | The PII access-log write fails while an unmasked personal field would be returned | The read is refused with 503 and MSG-GEN-006; no unmasked field is returned | MSG-GEN-006 | AC10 |
| X9 | No session | 401; no downstream call | MSG-P4-001 | AC16 |
| X10 | The caller's role has no Case record R | 403; the refusal is logged | MSG-P4-002 | AC11 |
| X11 | The authorise call does not answer, answers 5xx or its breaker is open | 503; no entry | MSG-GEN-006 | AC15 |
| X12 | The parameters or list contract is down and no cached version exists | 503; no default assumed | MSG-GEN-006 | AC20 |

X1 to X5 are the legacy exception paths of RWB-E1-068, carried unchanged. X6, X7 and X8 are the paths the two contract hops add: in the monolith the scope was a local check and the masking a local call, so neither could time out, and the PII access log was written in the same process.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published ledger contract, the rwb-case case, parameters and reference-data contracts and the rwb-access contract with their fakes from Day 1, and needs the `interaction` table of RWB-P1-E1066-APP |
| Negotiable | The internal class split, the number of queries for items and total, and the cache of the reference lists are the squad's choice behind the contract; the order, the filters, the page limits and the masked field are fixed |
| Valuable | One ordered, filterable and masked history per case, and one place where every consumer reads it |
| Estimable | One migration for the index, one controller, one service, one repository, four clients and one architecture test |
| Small | Fits one sprint with its tests, as the read slice of the legacy key |
| Testable | Every criterion in section 7 is one API call on a synthetic ledger, apart from the architecture test of AC3 |

### 7. Acceptance criteria

```gherkin
Feature: Interaction ledger read interface

  Background:
    Given caseId "00000000-0000-4000-8000-000000000401" (caseNo "RW-2026-000401") has 9 ledger entries from 2026-08-04 to 2026-12-06
    Given 3 entries come from EFS with channel CALL between 2026-08-04 and 2026-10-15
    Given 2 entries come from user "u-owner-04" with channel VISIT on 2026-11-10 and 2026-11-20
    Given 4 entries come from the Workbench with no channel between 2026-12-01 and 2026-12-06
    Given user "u-owner-04" holds RW-CASEOWN and owns the case
    Given the rwb-case contract mock answers 200 for caseId "00000000-0000-4000-8000-000000000401" with the token of user "u-owner-04"
    Given the rwb-access masking contract mock returns the summary of each entry masked for the roles of user "u-owner-04"

  Scenario: AC1 The ledger reads in ledger order
    Given caseId "00000000-0000-4000-8000-000000000401" (caseNo "RW-2026-000401") has 9 entries, including two entries with the same occurredAt and caseSeq values 4 and 5
    When u-owner-04 reads the case ledger
    Then 9 Interaction records are returned ordered by occurredAt ascending and caseSeq ascending
    And every Interaction property declared by the v5.1.0 contract is returned with its fixture value
    And sourceSystem is EFS only for EFS history and WORKBENCH for the other entries

  Scenario: AC2 Filters are applied together
    Given the 9-entry ledger of the Background
    When the case is read with channel=CALL
    Then the 3 EFS call entries are returned and total is 3
    When it is read with actor=u-owner-04
    Then the 2 VISIT entries are returned and total is 2
    When it is read with channel=CALL and actor=u-owner-04
    Then the response is 200 with total 0 and no items
    When it is read with from=2026-12-01 and to=2026-12-06
    Then the 4 Workbench entries dated from 2026-12-01 to 2026-12-06 are returned and total is 4
    And the time zone and the inclusivity of entries at the day boundaries are Pending (NEW-GAP-S6-10)

  Scenario: AC3 Only ledger package classes query the ledger
    Given the rwb-source-data build
    When the architecture test runs
    Then only classes in the sourcedata.ledger package reference interaction
    And the repository exposes no write method

  Scenario: AC4 An inverted date range is refused
    Given from=2026-12-06 and to=2026-12-01
    When the reader calls the operation
    Then the response is 422 Problem with messageCode MSG-GEN-003, field=to and other=from
    And no ledger query runs

  Scenario: AC5 A missing or out-of-scope case is concealed
    Given the case contract answers 404 for the caller and the caseId is a UUID
    When the caller reads the ledger
    Then the response is 404 Problem with messageCode MSG-P4-003 and no items
    And a missing case and an out-of-scope case have the same response body

  Scenario: AC6 Summary masking preserves null values
    Given a non-null summary and a null summary are in the ledger
    And the masking contract returns no unmasking row for the caller
    When the caller reads the ledger
    Then each non-null summary is MASKED and the null summary stays null
    And no PII access-log call is made

  Scenario: AC7 Paging bounds and defaults
    Given 201 entries match the filters and parameter values are default 50 and maximum 200
    When the reader omits size, then reads size=200, size=201, size=0 and page=-1
    Then the first page has 50 items and total 201, and size=200 returns 200 items
    And size=201, size=0 and page=-1 return 422 Problem with MSG-GEN-002 and the offending field, min 1 and max 200 for size
    When the parameter version gives a maximum of 100
    Then size=101 returns 422 MSG-GEN-002

  Scenario: AC8 Empty ledger
    Given the case has no matching entries
    When its owner reads the ledger
    Then the service returns 200 with items=[] and total=0
    And the consuming screen displays MSG-P3-024 with the text "Nothing is recorded in interactions yet."

  Scenario: AC9 Case dependency failure
    Given the case contract answers 503, does not answer after one retry within its 2 s budget, or its breaker is open
    When the caller reads the ledger
    Then the response is 503 Problem with messageCode MSG-GEN-006 and no entries

  Scenario: AC10 PII access-log failure
    Given an unmasking row applies and the access-log write returns 503
    When the caller reads the ledger
    Then the response is 503 Problem with messageCode MSG-GEN-006 and no body items
    And no summary value is logged

  Scenario: AC11 Authorisation precedes case disclosure
    Given authorise denies Case record R and the case contract answers 404
    When RW-REFADM reads the UUID caseId
    Then the response is 403 Problem with messageCode MSG-P4-002, the refusal is logged and no case answer is disclosed

  Scenario: AC12 Masking dependency failure fails closed
    Given the masking contract returns non-2xx, does not answer within its 2 s budget or its breaker is open
    When the caller reads the ledger
    Then the response is 200 and every non-null summary is MASKED
    And no PII access-log call is made

  Scenario: AC13 The read writes no ledger or case data
    Given the ledger row count and checksum are recorded before the read
    When the caller reads the ledger
    Then the row count and checksum are unchanged
    And no POST, PUT or PATCH is sent to rwb-case

  Scenario: AC14 An unmasked read is logged
    Given the masking contract allows a non-null summary for the caller
    When the caller reads the ledger
    Then the summary is returned in full
    And an access-log record holds user, role, caseId, data product, field ID DF-INT-011 and time, and no summary value
    And the operation and payload of the write are Pending (NEW-GAP-S6-12)

  Scenario: AC15 Authorise failure
    Given the authorise contract times out, returns 5xx or its breaker is open
    When the caller reads the ledger
    Then the response is 503 Problem with messageCode MSG-GEN-006 and no items

  Scenario: AC16 No session
    Given the request has no token
    When the ledger is read
    Then the response is 401 Problem with messageCode MSG-P4-001
    And no downstream call is made

  Scenario: AC17 Channel outside LOV-CHANNEL
    Given channel=FAX is not in LOV-CHANNEL
    When the ledger is read
    Then the response is 400 Problem with messageCode MSG-GEN-007 and field=channel

  Scenario: AC18 Paging boundaries
    Given 9 entries and page size 4
    When pages 0, 1, 2 and 3 are read
    Then item counts are 4, 4, 1 and 0 and total is 9 on every page
    And size=0 and page=-1 return 422 MSG-GEN-002

  Scenario: AC19 One-sided and same-day date ranges
    Given the 9-entry ledger of the Background
    When it is read with only from=2026-12-01, then only to=2026-10-15
    Then the first returns the 4 entries from 2026-12-01 and the second the 3 entries up to 2026-10-15
    When it is read with from=to=2026-11-10
    Then the 1 VISIT entry of that day is returned
    And the date format, time zone and the answer to a malformed date are Pending, owner API contract owner (NEW-GAP-S6-10)

  Scenario: AC20 Parameters or list unavailable with no cache
    Given the cache is cold and the parameters or list contract returns 503
    When the ledger is read
    Then the response is 503 Problem with messageCode MSG-GEN-006 and no default is assumed

  Scenario: AC21 Correction entries are identifiable
    Given a ledger entry and a later correction referencing its entry ID
    When the ledger is read
    Then both Interaction records are returned and the correction carries correctsEntryId of the first entry

  Scenario: AC22 Team and audit readers are scoped
    Given RW-TEAMMGR and RW-AUDIT are each authorized for the fixture case
    When each reads the ledger
    Then each receives 200 with the 9 entries
    And each non-null summary is MASKED where the masking contract returns no unmasking row for that role

  Scenario: AC23 Timed read
    Given one case has 5,000 entries and the ledger holds the agreed 2031 volume
    When the first page of 50 is read repeatedly
    Then the response time at the 95th percentile is under 2 seconds (NFR-070; Non Functional Specification v5 section 3.2)
    And the total 2031 ledger volume, the environment and the measurement point are Pending under DL11, owner solution architect and QA

  Scenario: AC24 Feature flag off
    Given rwb.dataengine.ledger-read is off
    When the ledger read is called
    Then the service answers 404 and queries no ledger row
    And the history panel shows its Error state with MSG-GEN-006
    And the messageCode of the 404 is Pending (NEW-GAP-S6-9)

```

**Target reading.** The criteria are read against rwb-source-data.yaml 5.1.0 and the decision register; what changes against the legacy story is where they run. `GET /cases/{caseId}/interactions` is no longer a path of rwb-case served by a P3 handler over an in-process `InteractionLedgerReader`, but the read operation of rwb-source-data on its base `/api/recovery/source-data/v1`, and rwb-case reaches the ledger only through this contract (DP-11, DP-18). The query runs on P1's own table `interaction` in schema `rwb_source_data`: one filtered, ordered and paged SELECT on `case_id` with the optional `channel`, `actor_ref` and `occurred_at` range, ordered by `occurred_at` and then `case_seq`, using `ix_interaction_case_time` on `(case_id, occurred_at)` and `ix_interaction_case_actor` on `(case_id, actor_ref)` (DP-01, DP-15). The scope of AC5 comes from the rwb-case case contract and is never cached, and the masking of AC6 comes from the rwb-access masking contract (DP-08). The page limits of AC7 are rwb-case parameters and the channel list is rwb-case reference data (DP-06, DP-07). The screens arrive through the gateway-bff composite route (DP-19). The architecture test proves that only classes in `...sourcedata.ledger` query `interaction`.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The ledger reads back in one ordered sequence, by occurred time and then case sequence | REQ-ILG-006; interaction.occurred_at; interaction.case_seq |
| BR2 | The ledger can be filtered by channel, actor and date range through one interface | REQ-ILG-006 |
| BR3 | Entries carry channel, who or what was reached, and the outcome where the interaction had one | REQ-ILG-003; interaction.contact_result |
| BR4 | Personal data in the ledger is masked by role on the same rules as the case record | REQ-ILG-014; CTL-11; DL26 |
| BR5 | A case outside the caller's scope is refused | CTL-09 |
| BR6 | No consumer queries the interaction table directly | ADR-002; DT08 |

**Where each rule lives in the target.** BR1 is the `ORDER BY occurred_at, case_seq` of the one query and the index that serves it, `ix_interaction_case_time` on `(case_id, occurred_at)`; the order is the same one the writer allocated `case_seq` in, so a tie on the time is broken by the write order and never by the primary key (DP-01, DP-15). `case_seq` is unique per case but nullable in Physical Schema v9; the order of entries that share a time when one has no sequence is Pending (NEW-GAP-S6-11). BR2 is the four filters of the published operation: `channel` is validated against LOV-CHANNEL of the rwb-case reference-data contract, `actor` against `actor_ref` on the new index, and `from` and `to` against the half-open business-date window of `occurred_at`; the pagination is the parameter pair of the parameters contract, so a limit change is a parameter version and not a release (DP-06, DP-07). BR3 is the field set of the answer: the channel, the direction, the contact result, the promise amount and date, and the source system and source reference of each entry; an entry that had no contact still answers its event code and its source. BR4 moves from an in-process masking call to the rwb-access masking contract, evaluated for the caller's roles against the field `interaction.summary`: no row means masked, which is the safe default of DL26, and the channel, result and promise fields are returned unmasked; whether any of them also needs the access log is Pending (NEW-GAP-S6-13). BR5 is the one scope call of the case contract, made for the caller and not for the service, with the 404 of MSG-P4-003 preserved; the case service does not disclose whether the case is missing or merely out of scope, and this read does not either (DP-11). BR6 becomes a schema boundary as well as a rule: `interaction` exists once, in `rwb_source_data`, and the other eighteen services reach it only through this contract, which the architecture test of AC3 enforces for this service and the Ownership Map enforces for the rest (DP-01, DP-18).

### 9. State transitions

None. This story does not change a case status. It reads the ledger and changes nothing.

| From | Event | Condition | To |
|---|---|---|---|
| an empty result page | a read of a case whose entries do not match the filter | The channel, actor or date window excludes every entry | Still an empty result page; the panel shows the Empty state |
| a valid filter | a read with a page size above the maximum | The parameter contract answers a maximum of 200 | The read is refused with 422 and no page is returned |
| an applied migration version | a change to the actor index | The index needs a different column order | A new Flyway version is merged; the applied version is never edited |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Reads the ledger of own cases (Case record R, scope Own) |
| RW-TEAMMGR, team manager | Reads the ledger of team cases (Case record R, scope Team) |
| RW-CONDUCT, RW-AUDIT and other roles with Case record R | Read the ledger of cases in their scope |
| RW-REFADM, reference data administrator | May not read (no Case record right); refused with 403 and MSG-P4-002 |
| RW-COMPLY, Compliance and PDPA officer | Owns the masking rules that decide who sees the summary (DL26) |
| rwb-case (P3) | Owns the case, its scope and the case record; answers the scope check and serves the parameters and the lists this read consumes (C RWB-P3-E1018-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON) |
| rwb-access (P4) | Owns the roles, the scope model, the masking policy and the access log; answers the authorise, masking and access-log calls (C RWB-P4-E1037-CON) |
| rwb-asset (service identity) | Reads the delivery state of a notice from `latestDeliveryStatus` of the LETTER entry (RD-P1-064). Pending: its service-identity row Case record R and the masking answer for a service caller, owner solution architect with the rwb-access owner (NEW-GAP-G2-finish-2) |

The read runs as the service identity of rwb-source-data (DP-02; Architecture v5 slides 11 and 29), and the caller's identity travels in the token so that the scope and the masking answer are made for the caller and not for the service.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-INT-001 | interaction | id | Read |
| DF-INT-002 | interaction | case_id | Read |
| DF-INT-003 | interaction | person_key | Read |
| DF-INT-004 | interaction | occurred_at | Read |
| DF-INT-005 | interaction | channel | Read |
| DF-INT-006 | interaction | direction | Read |
| DF-INT-007 | interaction | action_code | Read |
| DF-INT-008 | interaction | contact_result | Read |
| DF-INT-009 | interaction | promise_amount | Read |
| DF-INT-010 | interaction | promise_date | Read |
| DF-INT-011 | interaction | summary | Read, masked by role |
| DF-INT-012 | interaction | conduct_check | Read |
| DF-INT-013 | interaction | source_system | Read |
| DF-INT-014 | interaction | event_code | Read |
| DF-INT-015 | interaction | actor_type | Read |
| DF-INT-016 | interaction | actor_ref | Read, and filtered on |
| DF-INT-017 | interaction | source_ref | Read |
| DF-INT-018 | interaction | idempotency_key | Read |
| DF-INT-019 | interaction | case_seq | Read, as the order tie-break |
| DF-INT-020 | interaction | decision_log_id | Read, as a reference only |
| DF-INT-021 | interaction | corrects_entry_id | Read |
| DF-INT-022 | interaction | contact_key | Read |
| DF-INT-023 | interaction | from_holder_ref | Read |
| DF-INT-024 | interaction | to_holder_ref | Read |
| DF-INT-025 | interaction | treatment_id | Read |
| DF-INT-026 | interaction | proceeds_id | Read |
| DF-INT-027 | interaction | retention_class | Read |
| DF-INT-028 | interaction | delivery_status | Read |
| DF-INT-029 | interaction | external_ref | Read |
| DF-CAS-001 | recovery_case | id | Read through the rwb-case case contract, not from the table |

Field IDs are those in the Logical Data Model and Data Dictionary.

**Which side is this story's.** `DF-INT-001` to `DF-INT-029` are this service's own rows in `rwb_source_data`: the query reads them and writes none of them, and the story adds one index and no column (DP-01, DP-18). The read returns the complete `Interaction` representation published by RWB-P1-E1066-CON (contract 5.1.0), including `idempotencyKey`, `correctsEntryId`, `contactKey`, holder references, treatment/proceeds/document references, `deliveryStatus`, `externalRef` and `retentionClass`; `sourceSystem` is `EFS` only for EFS history and `WORKBENCH` for other entries (RD-P1-007). `DF-CAS-001` is rwb-case's own key, read through the case contract and never joined locally; the answer carries the case ID it was asked for and no case field (DP-11). The field names in section 12 are those of the `Interaction` and `InteractionPage` schemas of the API specification; the physical column names are RWB-P1-E1066-CON's.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/source-data/v1`. One operation, the read of a case's ledger, on the interaction-ledger resource of this legacy key, published with the `Interaction` and `InteractionPage` schemas of RWB-P1-E1066-CON. The path keeps the legacy relative form with the case in the path, exactly as the acceptance criteria write it.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases/{caseId}/interactions` | Reads a case's ledger in one ordered sequence, filtered by channel, actor and date range and paged, and returns an `InteractionPage` | Any authenticated caller with Case record R on the case, the scope applied (DP-08); refused with 401 without a session and 403 without the right | None: a read changes nothing |

**Query.** `channel`, `actor`, `from`, `to`, `page`, `size`. `channel` is a value of LOV-CHANNEL read through the rwb-case reference-data contract; `actor` is the `actor_ref` of the entries; `from` and `to` filter `occurred_at`; format, timezone and inclusive boundaries remain Pending under NEW-GAP-S6-10; `page` is 0 or more; `size` defaults to 50 and is between 1 and its maximum of 200, both read through the rwb-case parameters contract (DP-06, DP-07). `actor` is a typed query parameter of at most 64 characters matching `actorRef` (RD-P1-005 rule 8); a longer value is 422 MSG-GEN-002. The actor index is `ix_interaction_case_actor` on `(case_id, actor_ref)`.

**Response.** `InteractionPage`: `items` of the complete `Interaction` schema, `page`, `size` and `total`. `total` is the count after all filters. Entries sort by `occurredAt` ascending, then `caseSeq` ascending; `caseSeq` is the ledger arrival sequence (RD-P1-009). A page beyond the last page returns 200 with `items=[]`. A null summary remains null; a non-null summary is returned as `MASKED` unless the masking contract allows it. Pending: how a null `caseSeq` participates when two entries share `occurredAt`, owner data architect, tracked as NEW-GAP-S6-11.

**Properties of `Interaction`** (every one is returned; one without a value is null or absent, as the yaml marks only four as required).

| Properties | Type | Required | Masking |
|---|---|---|---|
| `id`, `caseId` | uuid | Yes | None |
| `occurredAt` | date-time | Yes | None |
| `sourceSystem` (EFS or WORKBENCH) | string | Yes | None |
| `summary` (up to 2000) | string | No | `MASKED` unless the masking contract allows it |
| `personKey`, `contactKey` (up to 255) | string | No | Reference only; access-log rule Pending (NEW-GAP-S6-13) |
| `actorType`, `actorRef`, `sourceRef`, `eventCode`, `channel`, `direction`, `actionCode`, `contactResult`, `conductCheck`, `idempotencyKey`, `fromHolderRef`, `toHolderRef`, `retentionClass`, `deliveryStatus`, `externalRef`, `barcodeStatus` | string, lengths and enums as in the yaml | No | None; access-log rule Pending (NEW-GAP-S6-13) |
| `promiseAmount`, `promiseDate` | number, date | No | None; access-log rule Pending (NEW-GAP-S6-13) |
| `caseSeq` | integer | No | None |
| `decisionLogId`, `correctsEntryId`, `treatmentId`, `proceedsId`, `documentId` | uuid | No | None |

`documentId` and `barcodeStatus` have no column in Physical Schema v9 and no DF-INT field; their source is Pending, owner data architect (NEW-GAP-S6-15).

**Errors.** Every error uses `application/problem+json` and the shared `Problem` schema: required `type`, `title`, `status`, `messageCode` and `traceId`; `detail`, `instance`, Thai `messageTh`, `field` and `errors` as defined by RD-P1-004; no other members. A malformed or missing query value, an invalid list value, or a non-UUID `caseId` returns 400; a non-UUID `caseId` uses MSG-GEN-001 before any read. A channel outside LOV-CHANNEL returns 400 MSG-GEN-007. A value outside its range returns 422 MSG-GEN-002; a date range in the wrong order returns 422 MSG-GEN-003. Missing session is 401; lack of Case record R is 403; a case absent or outside scope is 404 MSG-P4-003; unavailable store/dependency is 503 MSG-GEN-006. These status/code mappings follow RD-P1-004.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Pattern |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Once per read: the case exists, and the caller's scope covers it; a refusal becomes the 404 of MSG-P4-003 and no scope answer is cached | DP-11; faked (the case contract of RWB-P3-E1018-CON) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Once per read: Case record R for the caller on the case, role and scope | DP-08; C RWB-P4-E1037-CON; faked |
| GET | `/api/recovery/access/v1/masking-policies` | P4 rwb-access | Once per read: the unmasking answer for `interaction.summary` for the caller's roles; no row means masked | DP-08; C RWB-P4-E1037-CON; faked |
| GET | `/api/recovery/case/v1/parameters/{key}` | P3 rwb-case | The page-size default 50 and the page-size maximum 200, read as data and cached per parameter version | DP-06; C RWB-P3-E1042-CON; faked |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | The list **LOV-CHANNEL**, read as data for the channel filter and the channel validation | DP-07; C RWB-P3-E1043-CON; faked |

Every call is one hop with a 2 s total budget per downstream. A GET retries once with jitter inside that budget; the POST authorise call is not retried; each downstream has its own breaker and bulkhead (Error Handling and Resilience Standard v4). The caller's token is forwarded to the case and authorise calls; parameters and list reads use the rwb-source-data service identity; the identity of the masking and access-log calls is Pending (NEW-GAP-S6-14). Any answer from the case or authorise call other than those of section 4 gives 503 MSG-GEN-006, with `{system}` naming the dependency; any non-2xx from masking masks every non-null summary. The parameters and the list are cached against their version and never defaulted to a constant; the scope and masking answers are never cached across calls. The authorise, masking-policy and access-log operations and their payloads are not in rwb-access.yaml 5.1.0: Pending, owner rwb-access contract owner (NEW-GAP-S6-12; GAP-0925, GAP-1404, GAP-0586). Whether a service identity or a partner role (PT-AGENCY, PT-LAWFIRM) may call this read, and with what masking and logging, is Pending, owner solution architect and product owner (NEW-GAP-S6-14; GAP-2102). No other service is called and no table of another service is read (DP-01).

#### 12.3 Events published

None. A read publishes no event; the topic and its events are owned by RWB-P1-E1015-APP (Architecture v5 slides 15 and 41). A read publishes nothing, writes no outbox row and adds no message schema.

#### 12.4 Events consumed

None. Architecture v5 slide 15 gives this service no consumed event, and a read is a synchronous step. The ledger rows the query returns arrive through the writer and the intake of this legacy key, not through a subscription of this story (RWB-P1-E1066-APP, RWB-P1-E1067-APP).

#### 12.5 Workflows and activities

None. The read is a synchronous REST step and one query; it starts no workflow and no activity. The task queue of this service is `rwb-source-data` in namespace `rwb-recovery`, and the workflows `AceIngestCheck` and `reconciliation` and the activities `listEligibleAccounts` and `snapshot(page)` of Architecture v5 slide 15 are other P1 stories.

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job sits in this story: the read is driven by the screen.

#### 12.7 Tables owned

| Object | Schema | Owner | This story |
|---|---|---|---|
| `interaction` | `rwb_source_data` | P1 rwb-source-data (DP-01, DP-18) | Read only: the filtered, ordered and paged SELECT on `case_id`, plus the count for `total`; the migration adds the index `ix_interaction_case_actor` on `(case_id, actor_ref)` and keeps `ix_interaction_case_time` on `(case_id, occurred_at)`; no column, no key and no trigger is changed |
| `processed_event`, `idempotency_key`, `outbox_event` | `rwb_source_data` | PLT library, created in this service's schema | Not used: a read writes no inbox row, no idempotency row and no outbox row |

The PII access log is not a table of this story: it is the access log of rwb-access, written through the rwb-access contract, and this story owns no row of it (12.2). No table of another service is read and no foreign key crosses a schema (DP-01, DP-18). The case of AC5 is answered by the case contract and never by a local join to `rwb_case`.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| Case contract fake (RWB-P3-E1018-CON) | `GET /api/recovery/case/v1/cases/{caseId}` | 200 for a case in scope, 404 for a case missing or out of scope, 503 and a timeout (AC5, AC9, X6) |
| rwb-access authorise fake | `POST /api/recovery/access/v1/authorise` | Case record R granted for RW-CASEOWN, RW-TEAMMGR, RW-CONDUCT and RW-AUDIT, refused for RW-REFADM (TC-E1-068-09), a timeout and a 503 (TC-P1-E1068-APP-02) |
| rwb-access masking fake | `GET /api/recovery/access/v1/masking-policies` | No unmasking rule for `interaction.summary` (AC6), an unmasking rule for a notice role, and an open breaker (X7) |
| Parameters fake | `GET /api/recovery/case/v1/parameters/{key}` | Page-size default 50 and maximum 200, a version with maximum 100, and a 503 with a cold cache (AC7, AC20) |
| Reference-data fake | `GET /api/recovery/case/v1/admin/lists/{listCode}` | The twelve values of LOV-CHANNEL with their Thai labels, and a channel outside the list (AC2, AC4, X4) |
| Ledger fixture | `rwb_source_data` | A container at the baseline plus the writer's and this story's migrations, with the 9 entries of the Background, the empty case of AC8, and 5,000 entries for the timed read (AC1, AC2, AC8) |

Every fixture is synthetic, and no production ledger row and no production summary is copied into one. The contract fakes of the table are the ones published with RWB-P3-E1018-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P4-E1037-CON; the fake library version recorded as published is Not specified in the source documents (DOR-RWB-P1-E1068-APP-22).

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 1 operation on `/api/recovery/source-data/v1` | 5 operations (`/api/recovery/case/v1/cases/{caseId}`, `/api/recovery/access/v1/authorise`, `/api/recovery/access/v1/masking-policies`, `/api/recovery/case/v1/parameters/{key}`, `/api/recovery/case/v1/admin/lists/{listCode}`) | OpenAPI 3.1, one hop, 2 s timeout, breaker per downstream (DP-11, DP-08) |
| Kafka | None | None | The topic belongs to RWB-P1-E1015-APP; a read publishes nothing |
| Temporal | None | None | No workflow, activity or Schedule in this story |
| File | None | None | No file is read or written |
| SQL | None | `interaction` in `rwb_source_data`, read only | One query for the page and one for the total; no read of another service's table (DP-01) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata`, module `ledger`, package `...sourcedata.ledger.read`, with the published types in `...sourcedata.api`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, topic `rwb.source-data.events.v1` (not published here), Temporal task queue `rwb-source-data` in namespace `rwb-recovery` (not used here).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 and DP-18 are this story's own patterns: the ledger the monolith held in the shared `recovery` schema is P1's table in `rwb_source_data`, and the read is a local query on it with no join across a schema. DP-11 is used for the read itself, which replaces the in-process `InteractionLedgerReader` with a contract, and again for the scope hop that replaces `CaseScopeQuery`. DP-08 replaces the in-process masking of `MaskingPolicy` with the rwb-access contract, so the masking decision and the access log are one policy and one contract. DP-06 moves the two page-size properties of the legacy configuration into the parameters contract, and DP-07 moves LOV-CHANNEL into the reference data, so neither is a constant. DP-15 is the per-service sequence on which the actor index arrives. DP-19 applies to the case record and the timeline, which this story serves and does not build.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `V<next>__rwb_e1_068_interaction_actor_index.sql` (the next version on the service sequence) | Migration | Creates `ix_interaction_case_actor` on `(case_id, actor_ref)`, keeps `ix_interaction_case_time` on `(case_id, occurred_at)`, and changes no column |
| `InteractionReadController` | Controller | The one operation of 12.1 on `/api/recovery/source-data/v1`; RFC 9457 problem details; the query parameters and the paging |
| `LedgerReadService` | Service | Filter validation, scope, masking, the PII access-log rule, the page and the total |
| `LedgerFilterValidator` | Service | `channel` in LOV-CHANNEL, `from` not after `to`, `size` 1 to the parameter maximum, `page` 0 or more; 400 MSG-GEN-001 / MSG-GEN-007 and 422 MSG-GEN-002 / MSG-GEN-003 with the field names |
| `InteractionQueryRepository` | Repository | The read-only query and the count; no insert, no update and no delete method exists |
| `InteractionView` | Entity | Read-only mapping of the interaction table for the answer |
| `CaseScopeClient` | Client | The rwb-case case contract: one hop, 2 s timeout, the refusal passed on as 404 with MSG-P4-003, no cache (DP-11) |
| `AuthoriseClient` | Client | The rwb-access authorise contract, through the guard library (DP-08) |
| `MaskingClient` | Client | The rwb-access masking contract for `interaction.summary`; no row means masked; an open breaker means masked (DP-08) |
| `ParameterClient` | Client library use | Page-size default and maximum as data, cached per parameter version (DP-06) |
| `ReferenceDataClient` | Client library use | LOV-CHANNEL as data for the filter and its validation (DP-07) |
| `PiiAccessLogClient` | Client | Writes the read when a personal field is returned unmasked, and refuses the read when the write fails (12.2) |

**Migrations and sequence (DP-15).** One version on rwb-source-data's own Flyway sequence, after the writer's: it creates `ix_interaction_case_actor` on `(case_id, actor_ref)` in schema `rwb_source_data` and leaves `ix_interaction_case_time` as the writer's migration created it. The legacy story asked for the actor index in a Flyway migration for the actor filter; the target puts it on the service's own sequence, so the table and its indexes version together. The exact version number is assigned by the sequence owner at build time, no monolith version number is reused, and an applied version is never edited.

**Masking authority.** The unmasking answer for `interaction.summary` comes from the rwb-access masking contract alone, under DP-08 and rank R3 of Architecture v5: one contract answers for the caller's roles, and this story keeps no masking row of its own. `data_product_access` is P1's data product access catalogue and not the masking authority; the alignment of FSD P1 A2.15 and TSD P1 T3.6 is outside this story.

**Database.** This story owns no table and one index: `interaction` in `rwb_source_data`. It creates no table of another service, adds no foreign key across a schema, and reads `recovery_case` over the case contract only (DP-01, DP-18). The query for a page and the query for its total both fall on the same two indexes; the timed read of one case with 5,000 entries is the evidence for NFR-070.

**Configuration and reference data**

- The page-size default 50 and the page-size maximum 200 are parameters of rwb-case, read through the parameters contract and never written in code or in a property file; the legacy keys `rwb.dataengine.ledger.page-size-default` and `rwb.dataengine.ledger.page-size-max` name the parameter rows and nothing else (DP-06); both rows are to be added to the parameter catalog with value, unit, bounds, owner and test case.
- The list LOV-CHANNEL with its twelve values and its Thai labels is reference data of rwb-case, read through the reference-data contract; a channel outside it is refused with MSG-GEN-007 for a channel outside LOV-CHANNEL (RD-P1-004).
- The masking rule for `interaction.summary` is policy of rwb-access: no row for the caller's roles means masked, and an unmasking row writes the read to the access log (DP-08).
- Open values of the masking and access-log rules: the masking version label, the personal field IDs the masking rows cover, the AC-READ granularity of the access log, the parameter names and defaults of the access-log page and of the field-ID batch limit, and the database login name are Not specified in the source documents (GAP-2321). They are settled at the wave-2 policy load and change no rule, criterion or test; the authorise element is confirmed at contract review.
- The 2 s budget, the breaker and the bulkhead of each consumed call are configuration of the clients (DP-11).
- The flag `rwb.dataengine.ledger-read` gates the operation at deployment.
- The scope answer and the masking answer are never cached: a stale scope answer is a scope leak, a stale masking answer can disclose a summary, and a call that does not answer inside 2 s either refuses the read (scope) or masks it (masking).
- The read is one call from gateway-bff to this service. Its three calls (the scope of the rwb-case contract, and the authorise and the masking of rwb-access) run concurrently, each one hop with a 2 s budget and a breaker, and none nests a further call; the parameters and the channel list come from their versioned cache. The chain is recorded for the architecture review list of the edge decision (GAP-0587).

**Build steps**

1. The migration for `ix_interaction_case_actor`, with a repeated run that changes nothing and `ix_interaction_case_time` untouched.
2. `InteractionReadController` and the query binding of 12.1, with RFC 9457 problem details.
3. `LedgerFilterValidator`: `channel` against LOV-CHANNEL, `from` not after `to`, `size` 1 to the parameter maximum, `page` 0 or more, with MSG-GEN-001, MSG-GEN-002 and MSG-GEN-003 naming the field (AC4, AC7).
4. `ParameterClient` and `ReferenceDataClient` against their fakes, so the default, the maximum and the list are data and the timed read is deterministic (AC2, AC7).
5. `InteractionQueryRepository`: the filtered, ordered and paged query and the count, with `ORDER BY occurred_at, case_seq` and the indexes of step 1; an explain-plan test asserts that the actor filter uses the new index and the date window the writer's (AC1, AC2).
6. `CaseScopeClient` and the 404 of MSG-P4-003 for a missing case and for an out-of-scope case, with no cache and the timeout path (AC5, X6).
7. `AuthoriseClient` through the guard library: Case record R granted for the reading roles and refused for RW-REFADM with MSG-P4-002 (TC-E1-068-09).
8. `MaskingClient` and the masking of `interaction.summary`: no rule or an open breaker means `MASKED`, and the other fields stay in full (AC6, X7).
9. `PiiAccessLogClient`: the write when a personal field is returned unmasked, and the refusal of the read when the write fails (X8).
10. The empty answer of a case with no entries: 0 items, total 0, 200 (AC8).
11. The architecture test: no class outside `...sourcedata.ledger` queries `interaction`, and the repository has no write method (AC3).
12. Tests for AC1 to AC24 and the access test of section 16, and the timed read of AC23.

**Feature flag.** `rwb.dataengine.ledger-read`. Off, the operation answers 404 and no query runs (RD-P1-045 item 4); the history panel shows the Error state with MSG-GEN-006; the ledger and the writer are unaffected (AC24).

**Done when.** The tests in section 16 pass, the actor index is applied on the service sequence beside the writer's index, the read answers the 9 entries of the Background in order and filters them three ways against the fakes, a summary with no masking rule comes back `MASKED`, size 201 is refused with MSG-GEN-002, a case with no entries answers 0 items and total 0, and a timed read of one case with 5,000 entries completes inside 2 seconds.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No valid session or no Workbench role | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | Role lacks Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case missing or outside caller scope | This case is not in your scope. |
| MSG-GEN-001 | Malformed query value or non-UUID caseId | Enter {field}. |
| MSG-GEN-002 | size outside 1 to 200 | {field} must be between {min} and {max}. |
| MSG-GEN-003 | from is after to | {field} cannot be before {other}; field=to, other=from. |
| MSG-GEN-006 | Store or dependency unavailable | {system} is not available. Try again in a few minutes. |
| MSG-GEN-007 | Query value not in its list of values | {value} is not a valid value for {field}. Choose a value from the list. |
| MSG-P3-024 | The interaction ledger has no matching entries | Nothing is recorded in {section} yet. |

MSG-P3-024 is informational, not a Problem error: the service returns the empty 200 page and the consuming case screen displays "Nothing is recorded in interactions yet." Thai text follows DL10. Query validation follows RD-P1-004: malformed input and a non-UUID caseId answer 400 MSG-GEN-001; channel outside LOV-CHANNEL answers 400 MSG-GEN-007; size or page outside range answers 422 MSG-GEN-002; inverted dates answer 422 MSG-GEN-003. The screen, not this service, raises MSG-P3-024.

### 15. Screens and states

No screen in this story, and no route of its own. SCR-03 Case record (Epic 1, Read only) shows the ledger in its history panel through this operation; its states in Screen Specifications v1 are Loading, read only, editable and on hold. SCR-04, the full timeline, arrives in Epic 2 (RWB-E2-034) with the states Loading and filtered; its Empty, Error and No access states are Not specified in the source documents (CG-ALL-2330). Both arrive through the gateway-bff composite route and are the screen owners' (DP-19; RWB-PLT-N001-CON). The panel lists entries earliest first, filters by channel, actor and date range and pages through the list. For this read it shows Loading (skeleton rows), Empty (MSG-P3-024: "Nothing is recorded in interactions yet."), Error (the message of section 14 above the panel) and No access (steps 5 and 7); a masked summary shows as `MASKED`. This story serves the data and renders no state.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-068-01 | AC1, BR1, BR3 | End to end | The 9-entry fixture with two entries sharing one time |
| TC-E1-068-02 | AC2, BR2 | End to end | Filters by channel CALL, actor u-owner-04, 2026-12-01 to 2026-12-06 |
| TC-E1-068-03 | AC3, BR6 | End to end | Architecture test |
| TC-E1-068-04 | AC4 | End to end | from 2026-12-06, to 2026-12-01 |
| TC-E1-068-05 | AC5, BR5 | End to end | Case contract answers 404 |
| TC-E1-068-06 | AC6, BR4 | End to end | No masking rule; one null summary |
| TC-E1-068-07 | AC7 | End to end | 201 entries; no size, 200, 201, 0, page -1 |
| TC-E1-068-08 | AC8 | End to end | Case with no entries |
| TC-E1-068-09 | Access | Component | RW-REFADM reads the ledger; refused with MSG-P4-002 |
| TC-E1-068-10 | Operation of section 12.1 | Contract | InteractionPage schema and the contract fake |
| TC-E1-068-11 | Section 12.7 | Component | Explain plan: actor filter and date window use their indexes |
| TC-E1-068-12 | AC9, X6 | End to end | Case contract 503 and timeout |
| TC-E1-068-13 | AC10, X8 | End to end | Access-log write fails for an unmasked summary |
| TC-E1-068-14 | AC11, X10 | Component | Authorise denies while the case answers 404 |
| TC-E1-068-15 | AC12, X7 | End to end | Masking timeout, non-2xx and open breaker |
| TC-E1-068-16 | AC13 | End to end | Ledger count and checksum before and after |
| TC-P1-E1068-APP-01 | AC14 | Component | Unmasked read and its access-log record |
| TC-P1-E1068-APP-02 | AC15 | Component | Authorise timeout, 5xx, open breaker |
| TC-P1-E1068-APP-03 | AC16 | Component | No token |
| TC-P1-E1068-APP-04 | AC17 | Component | channel=FAX |
| TC-P1-E1068-APP-05 | AC18 | Component | Pages of 4 over 9 entries; size 0, page -1 |
| TC-P1-E1068-APP-06 | AC19 | Component | One-sided and same-day ranges |
| TC-P1-E1068-APP-07 | AC20 | Component | Cold cache, parameters 503 |
| TC-P1-E1068-APP-08 | AC21 | Component | Entry and its correction |
| TC-P1-E1068-APP-09 | AC22 | Component | RW-TEAMMGR and RW-AUDIT |
| TC-P1-E1068-APP-10 | AC23 | Component | 5,000 entries, first page of 50 |
| TC-P1-E1068-APP-11 | AC24 | Component | Flag off |

The test case IDs are those of Test Cases v9, tab Story test cases. The legacy level "System" maps to "End to end" and "Access" to "Component".

### 17. Guardrails

- No business value in code: the page-size default and maximum are parameters of rwb-case, the channels are list values of LOV-CHANNEL, the masking rule is policy of rwb-access, and the 2 s budgets are configuration.
- No personal data in logs, tests, events or prompts: a summary is never logged and never written to a trace; the PII access log records the user, role, case ID, data product, field ID and time of the read and never the value; test summaries are synthetic.
- `interaction.summary` (`DF-INT-011`) is masked as specified. Data Classification marks further fields of this table as Confidential or personal (`actor_ref`, `person_key`, `contact_key` and the promise values among them); which returned fields need the access log and masking in UAT is Pending, owner Compliance and PDPA officer (NEW-GAP-S6-13).
- No read of another service's tables: the case is answered by the case contract, the masking and the authorise answers by the access contract, the parameters and the lists by their contracts, and `interaction` is read only in this service (DP-01, DP-06, DP-07, DP-08, DP-11).
- ACE data only through the owner's contract or `v_ace_*` views: this story reads no ACE data at all; the ledger holds what the writer recorded and the read adds nothing.
- The read changes nothing: no insert, no update and no delete on the ledger, no advisory lock, and the repository has no write method.
- The scope answer and the masking answer are never cached; a scope call that does not answer inside 2 s refuses the read, and a masking call that does not answer masks the summary (DP-08, DP-11).
- A personal field with no unmasking rule is never returned; a personal field is not returned unmasked when the PII access log cannot be written (BR-P1-015-2, BR-P1-015-4).
- One login, one schema and one sequence: the release carries the `rwb_source_data` login, migrates `rwb_source_data` only, and an applied migration version is never edited (DP-02, DP-15).
- No screen is served here: SCR-03 and SCR-04 arrive through the gateway-bff composite route and are the screen owners' (DP-19).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ILG-006 | Ledger reads in one ordered sequence, filterable by channel, actor and date range | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-03 | All recovery processes | CTL-09 | TC-E1-068-01, TC-E1-068-02, TC-E1-068-03, TC-E1-068-04, TC-E1-068-05, TC-E1-068-07, TC-E1-068-08 |
| REQ-ILG-003 | Entries carry channel, who was reached and the outcome | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-03 | All recovery processes | None | TC-E1-068-01 |
| REQ-ILG-014 | Personal data in the ledger masked by role as on the case record | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-03 | All recovery processes | CTL-11; DL26 | TC-E1-068-06, TC-P1-E1068-APP-01 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1066-APP | App development | H build dependency: the `interaction` table, its `case_seq`, its keys and the index this read queries, and the writer whose entries it returns |
| RWB-P1-E1066-CON | Contract | C dependency: publishes the Interaction resource and `InteractionPage` schema this read uses; build against its v5.1.0 contract |
| RWB-P1-E1067-APP | App development | Sibling of the same legacy key: the intake that writes the Workbench facts this read returns |
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON | Contract | H: the parameters client library and the reference-data client library (DP-06, DP-07) |
| RWB-PLT-E1037-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON | Contract | H: the authorise and masking guard library, the per-service Flyway sequence and the gateway-bff composite route (DP-08, DP-15, DP-19) |
| RWB-P3-E1042-CON, RWB-P3-E1043-CON | Contract | C: the parameters contract and the reference-data contract of rwb-case, each with its fake |
| RWB-P4-E1037-CON | Contract | C: the authorise, masking and access-log contract of rwb-access, with its fake |
| RWB-P3-E1018-APP | App development | Sibling: the case record and timeline that read the ledger through this contract |
| RWB-P3-E1018-CON | Contract | C dependency: case read and scope contract fake used by this story |
| RWB-E2-034 in the legacy set | App development | The full timeline SCR-04 and the ledger as a timeline on the case, which consume this read in Epic 2 |

### 19. Out of scope

- The full case timeline screen SCR-04 and the ledger as a timeline on the case (FEAT-ILG-09, RWB-E2-034); this story serves the read they use and builds neither screen.
- The case record view SCR-03 and its history panel, which arrive through gateway-bff and belong to the screen owner (DP-19; RWB-PLT-N001-CON).
- Recording entries: the append, the ledger table, the case sequence, the keys and the append-only trigger (RWB-P1-E1066-APP and RWB-P1-E1066-CON), and the Workbench intake (RWB-P1-E1067-APP).
- The PII access-log values, the access log table and the PII logging path of the platform (rwb-access and the platform library); this story calls the contract and owns no row of it.
- Masking rule values (DL26, Compliance) and the masking mechanism (RWB-P4-E1037-CON and the P4 stories); this story reads the decision and applies it.
- The scope model, the case record and the case status of rwb-case (RWB-P3-E1018-CON and the P3 stories); this story asks and passes the answer on.
- The parameters and reference data themselves, their values, their versions and their Thai labels (RWB-P3-E1042-CON, RWB-P3-E1043-CON).
- The gateway-bff composite route and the rendering of a masked summary (RWB-PLT-N001-CON and the screen owners).
- The retention class resolution and the archive of ledger rows (RWB-E1-017 in the legacy set); this read returns live rows only and resolves nothing.

### 20. Remaining delivery steps

- Size: Not specified; owner delivery squad.
- Epic design sign-off: Pending; owner product owner and solution architect.
- Contract Done (RWB-P1-E1066-CON, RWB-P3-E1018-CON, RWB-P3-E1042-CON, RWB-P4-E1037-CON): Pending; owner contract owners.
- Fake published: Pending; owner contract owners.
- rwb-access authorise, masking and access-log payloads (NEW-GAP-S6-12): Pending; owner rwb-access contract owner.
- Page-size parameter rows: Pending; owner centre of excellence.
- Synthetic test data in DEV: Pending; owner QA lead.
