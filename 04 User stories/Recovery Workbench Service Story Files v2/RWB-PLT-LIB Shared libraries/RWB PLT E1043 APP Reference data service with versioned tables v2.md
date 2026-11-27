# RWB-PLT-E1043-APP Reference data service with versioned tables

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: delta slice split from RWB-E1-043 for the platform library RWB-PLT-LIB — the reference-data client library that every service binds. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 25 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-PLT-E1043-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-LIB |
| Wave | 0 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-043 |
| Legacy disposition | Preserved + delta |
| Build status | In build |
| Patterns applied | DP01, DP04, DP05, DP06, DP07, DP08, DP09, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-PLT-LIB-G |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1043-CON, RWB-PLT-E1042-CON, RWB-PLT-E1072-CON, RWB-PLT-E1037-CON, RWB-PLT-TE006-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P3-E1042-CON, RWB-P7-E1073-CON, RWB-P4-E1037-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-016, FR-PLT-017, FR-PLT-018, FR-PLT-020) |
| Status | Draft (directive resolutions) |
| Size | To be sized by the squad at refinement |
| Contract version | Not specified in the source documents (DOR-RWB-PLT-E1043-APP-23); consumed paths are under /api/recovery/case/v1 |

### 1. Story

As a **service developer**, I want **the reference-data client implemented in the platform library — the typed read of a table code for a business date that returns the approved version in force with its rows, a cache whose time to live is a catalog entry, one log line per table read with the table code and the version, a typed exception when no approved version applies so that an engine never runs on a missing or stale value, and the exclusions proved in code (no rule table is served, the holiday calendar is not served)** — so that **every engine reads a dated, approved value through one contract and can say which version it used, with no service reading another service's tables** (Template and Rules §R6, DP-07, DP-01).

This is the delta slice of legacy RWB-E1-043 for the platform shared libraries. The legacy story built the two versioned tables, the registry, the read service and the load and approve operations inside one module; this story keeps none of that and delivers only the client library that every service binds against the rwb-case owner contract. The conformance points of the legacy story are kept unchanged: the approved version with the latest valid from on or before the business date, the one log line per table read, no run on a missing or stale value, and no rule table in the reference set.

### 2. Business rationale

Today the values that drive allocation, timers and approval limits live in team spreadsheets and in procedure documents, so nobody can say which value applied to a case on a given day. The reference data service answers that question, and after the realignment the answer has to cross a service boundary: the tables, the registry, the read service, the load and approve operations and the cache stay with rwb-case (P3), and each of the 19 services reads a value through a library instead of a shared schema.

**The division is fixed.** The two versioned tables `reference_version` and `reference_row`, the `ReferenceVersionRegistry` and its load and approve operations, the reference read service and its cache stay with **RWB-P3-E1043-APP** and **RWB-P3-E1043-CON**, and the legacy acceptance criteria AC1 to AC10 of RWB-E1-043 stay with RWB-P3-E1043-APP. This story and its contract **RWB-PLT-E1043-CON** deliver the reference-data client library that every service binds, so that a service reads a dated, approved version through one published contract and never reads another service's table (DP-01, DP-07; Architecture v5 slides 14, 20, 27 and 29).

That split is what makes the reference promise auditable across 19 services. "Every engine can say which version it used" only holds if the value arrives with its version number attached, if the version in force is derived from a business date the caller passes rather than from the system clock, and if a missing version is a refusal rather than a default. Writing that down once, in the client, is cheaper and safer than 19 readings of the same table.

The client also carries the two exclusions the target architecture depends on. Rule packages are Drools packages governed in rwb-decision (P7, DP-04) and are not reference tables, so the client refuses a rule package code; the Bank of Thailand holiday calendar is ACE data read through `v_ace_holiday` by rwb-source-data (P1, DP-05) and is not served here at all. The acceptance criteria below are new, tagged `(new, D-RCV-60)`, and test only this library deliverable: no legacy acceptance criterion is copied into this story.

It supports REQ-DRI-011 and REQ-CWC-006, and the logging rule REQ-CWC-016 that the legacy story cites: every engine logs the table code and the version of every table it reads.

### 3. Preconditions

- RWB-PLT-E1043-CON is published: the `ReferenceDataClient` interface, the `ReferenceVersion`, `VersionedRows` and `NoVersionInForceException` types, the two consumed operations, the twelve-code set and the fakes.
- RWB-PLT-E1042-CON is published: the parameters client library that reads the cache time to live from the catalog (DP-06).
- RWB-PLT-E1072-CON is published: the embedded rules kit contract, so the boundary between this client and the kit is a published contract and not a verbal agreement (DP-04).
- RWB-PLT-E1037-CON is published: the access guard library, so a permission failure on the consumed read is surfaced by the caller's guard and not by this client (DP-08).
- RWB-PLT-TE006-CON is published: the outbox and inbox library, which carries no reference event because the legacy design publishes none (DP-09).
- RWB-PLT-E1047-CON and RWB-PLT-E1044-CON are published: the naming library and the per-service Flyway baseline the library artefact follows (DP-14, DP-15).
- RWB-PLT-N001-CON is published: the gateway-bff composite route under which the reference data screens read the tables; no screen is built here (DP-19).
- RWB-P3-E1043-CON is published: the rwb-case reference-data contract behind the read operation; RWB-P3-E1042-CON publishes the parameters operation behind the time to live.
- The list LOV-REF-TABLE is loaded with the twelve reference table codes of section 8 BR1. No rule table has a code in it, and the holiday calendar has no code in it.
- The business date of the calling service is set from the ACE batch record for the day (`v_ace_batch_status`) through the P1 contract; the client never reads the system clock for the business date.
- The cache time to live is the value the legacy story carries, `refdata.cache.ttl-seconds` = 300 (assumed; DL11), published as a named entry of the rwb-case parameter catalog with 300 as its documented default. The catalog entry identifier is Not specified in the source documents (GAP-1409; ASM-2458).
- The artefact coordinates of the library — the group and the artefact name it is published under — are Not specified in the source documents (GAP-1409; ASM-2458) and come from the platform library baseline, not from this story.
- The three tests build against the contract fakes of section 12.8; no rwb-case instance has to be running.

### 4. Flow

1. A service adds the library dependency and calls `ReferenceDataClient.rows(tableCode, businessDate)` in its engine start-up hook, passing the business date it received through the rwb-source-data (P1) contract.
2. The client checks the table code against the eleven codes it serves (BR1), read through `GET /api/recovery/case/v1/admin/lists/{listCode}` on rwb-case. A code outside the eleven is refused and never reaches the owner.
3. The client resolves the version in force: the APPROVED version of that table with the latest `valid_from` on or before the business date, taken from the version projection of the same list operation on rwb-case. The client reads no `reference_version` and no `reference_row` row of its own.
4. The client looks up its cache by table code and business date. A hit inside the time to live answers without a call to rwb-case.
5. On a miss the client reads the version with its rows, stores the entry with the time to live read from the parameters catalog through `GET /api/recovery/case/v1/admin/parameters`, and answers.
6. The client writes one `ReferenceVersionLogger` line per table read: the table code, the version number and the business date. The line carries no customer identifier and no row content.
7. If no approved version applies, the client throws `NoVersionInForceException(tableCode, businessDate)` carrying MSG-P3-027. The calling engine does not start its run and raises its own alert through its own story.
8. The caller receives rows only: a rule package code is refused as not a reference table (the kit owns rule packages), and the holiday calendar is not served at all — the working-day calculator reads `v_ace_holiday` through the P1 query.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The table code is not one of the twelve reference table codes | The client refuses the read before any call to rwb-case; nothing is cached and nothing is logged as a table read | MSG-P3-027 | AC6 |
| X2 | The code is a rule package code | The client refuses it as not a reference table and names the kit as the owner of rule packages; no rule table is read | MSG-P3-027 | AC6 |
| X3 | No approved version applies to the business date | `NoVersionInForceException` is thrown with the table code, the business date and MSG-P3-027; the caller's engine does not run | MSG-P3-027 | AC4 |
| X4 | Only a VALIDATED or a ROLLED_BACK version exists for the date | It is never served; the read resolves to the previous APPROVED version or refuses with the exception | MSG-P3-027 | AC8 |
| X5 | The cache entry passes its time to live while a new version is approved | The next read reloads from rwb-case and serves the new approved version; the stale entry is dropped | None | AC3 |
| X6 | A caller asks the client for the holiday calendar | The read is refused: the calendar is ACE data and is read through the rwb-source-data (P1) contract | MSG-P3-027 | AC7 |
| X7 | The consumed list or parameters read answers 403 for the caller | The read fails closed with the caller's own permission refusal; no cached value is served in place of the answer | MSG-P4-002 | AC3 |
| X8 | A version is rolled back after the cache was filled | The rolled-back version is never returned; the entry is dropped and the previous approved version is served | MSG-P3-027 | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the library contract story and the platform contract stories; rwb-case is reached through its contract fake, so no other service has to be built first |
| Negotiable | The cache size, the log format around the three fixed fields and the fixture set are open; the read rule, the refusal, the code set and the log fields are fixed by the contract |
| Valuable | Gives all 19 services one dated, approved read of reference data on Day 1 and removes every private copy of a reference table from the service plans |
| Estimable | One published interface, three types, one cache, one logger, one code catalog, one fake |
| Small | Fits two weeks with its tests |
| Testable | Each criterion below is one test against the contract fakes of section 12.8 |

### 7. Acceptance criteria

```gherkin
Feature: Reference-data client library

  Background:
    Given the business date is 2026-11-25
    Given the table "EXPOSURE_BAND" has version 3 approved with valid from 2026-11-30 and bands "E1" to "E4"
    Given user "U-REF-01" holds RW-REFADM and user "U-RSK-01" holds the approve right in Reference data

  Scenario: AC1 The read answers the version in force for the business date (new, D-RCV-60)
    Given "EXPOSURE_BAND" version 4 with bands "E1" to "E5" is approved with valid from 2026-12-01
    When the client reads rows("EXPOSURE_BAND", 2026-11-30)
    Then it returns version 3 with its 4 rows and version 4 is not served
    When the client reads rows("EXPOSURE_BAND", 2026-12-01)
    Then it returns version 4 with its 5 rows

  Scenario: AC2 A superseded version stays readable with its valid to (new, D-RCV-60)
    Given version 4 of "EXPOSURE_BAND" is approved with valid from 2026-12-01
    When the client reads versionInForce("EXPOSURE_BAND", 2026-11-30)
    Then the version 3 record carries its 4 rows, status APPROVED and valid to 2026-11-30
    When the client reads versions("EXPOSURE_BAND")
    Then both version 3 and version 4 are listed with their own valid from and valid to

  Scenario: AC3 The cache serves the approved version for its time to live (new, D-RCV-60)
    Given approved "QUEUE" version 7 is in force on the business date and the cache time to live is 300 seconds
    When the client reads "QUEUE" for 2026-11-30, again inside the time to live, and once more after it
    Then the second read answers from the cache with no call to rwb-case
    Then the third read reloads from rwb-case and serves the approved version in force at that moment
    Then a further approved version is picked up at the next expiry and not before

  Scenario: AC4 No version in force refuses the read and the caller does not run (new, D-RCV-60)
    Given the table "TEAM" has no approved version with valid from on or before 2026-11-30
    When the client reads rows("TEAM", 2026-11-30)
    Then it throws NoVersionInForceException naming table "TEAM" and business date 2026-11-30
    Then the exception carries MSG-P3-027
    Then the calling engine does not start its run and raises its own alert

  Scenario: AC5 One log line per table read with the table code and the version (new, D-RCV-60)
    Given approved "QUEUE" version 7 is in force for business date 2026-11-30
    When the client reads "QUEUE" for 2026-11-30 twice inside the time to live
    Then exactly one ReferenceVersionLogger line is written for that table read
    Then the line carries the table code "QUEUE", the version number 7 and the business date 2026-11-30
    Then the line carries no customer identifier and no row content

  Scenario: AC6 A rule package code is refused as not a reference table (new, D-RCV-60)
    Given a code that is a rule package code and not one of the twelve reference table codes
    When the client is asked to read it for 2026-11-30
    Then the read is refused with MSG-P3-027 and the code is named as a rule package code
    Then the client states that rule packages are governed by rwb-decision and served by the rules kit
    Then no rule table is read and no reference table is cached

  Scenario: AC7 The holiday calendar is not served by the client (new, D-RCV-60)
    Given the working-day calculator needs the Bank of Thailand holiday calendar for business date 2026-11-30
    When the client is asked for the holiday calendar
    Then it is refused as not a reference table, because the calendar is ACE data
    Then the working-day calculator reads the holiday calendar through the rwb-source-data (P1) contract instead
    Then no holiday row is cached and no holiday table code exists in LOV-REF-TABLE

  Scenario: AC8 Only a version that is APPROVED is ever served (new, D-RCV-60)
    Given a "LEGAL_PERIOD" version with status "VALIDATED" and valid from 2026-12-01
    And a "REGION" version 5 with status "ROLLED_BACK"
    When the client reads "LEGAL_PERIOD" for 2026-12-01 and "REGION" for 2026-11-30
    Then the VALIDATED version is not served and the approved version in force is returned
    Then the ROLLED_BACK version 5 is never returned and the previous approved version is served
    Then the cache holds no entry for a version that is not APPROVED

  Scenario: AC9 The client serves only the eleven table codes and adds no code, status or message of its own (new, D-RCV-60)
    Given the reference table codes held in LOV-REF-TABLE
    When the client is asked for the table codes it serves
    Then the eleven codes PRODUCT, REGION, EXPOSURE_BAND, ROLE, TEAM, QUEUE, SERVICE_LEVEL, DOCUMENT_TYPE, TEMPLATE, LEGAL_PERIOD and PRODUCT_PARAMETER are returned and no other code is
    Then the status vocabulary and the messages are those of RWB-PLT-E1043-CON, and the client holds no table, writes no row and reads no other service's schema

  Scenario: AC10 A consumed call that fails or does not answer stops the caller and serves no default (new, D-RCV-60)
    Given the rwb-case call for "QUEUE" fails or does not answer
    When the client reads "QUEUE" for 2026-11-30
    Then it throws naming table "QUEUE" and business date 2026-11-30
    Then the calling engine does not run and no default row, older version or empty list is served
```

These criteria are new and test only the library deliverable in the title. No legacy acceptance criterion is repeated here: AC1 to AC10 of RWB-E1-043 stay with RWB-P3-E1043-APP, which owns the two tables, the registry, the read service and the load and approve operations. Every number and identifier in the criteria above is the one the legacy story carries, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The client serves the eleven reference table codes only: PRODUCT, REGION, EXPOSURE_BAND, ROLE, TEAM, QUEUE, SERVICE_LEVEL, DOCUMENT_TYPE, TEMPLATE, LEGAL_PERIOD and PRODUCT_PARAMETER. A delegation limit is not served here: it is read from the rwb-access operation GET /doa-limits declared in RWB-P3-E1043-CON section 12.2. The list is data and changes by a load of LOV-REF-TABLE | RWB-E1-043 section 8 BR1; REQ-DRI-011; GAP-0696 |
| BR2 | The version in force on a business date is the APPROVED version with the latest valid from on or before that date, and the business date comes from the caller, never from the system clock | RWB-E1-043 section 8 BR3 (R-UNI-38) |
| BR3 | A version that is not APPROVED is never served, and a version that is ROLLED_BACK is never returned | RWB-E1-043 section 17 (the cache never serves a version that is not APPROVED) |
| BR4 | Every engine logs the table code and the version of every table it reads, one line per table read, with the business date and no customer identifier | RWB-E1-043 section 8 BR7; REQ-CWC-016 |
| BR5 | An engine that finds no version in force for a table it needs does not run on stale or missing values: the client throws and the caller stops; a dated read with no version in force answers 404 with MSG-P3-027 naming the table code and the business date, and never an older version, a default row or an empty list | RWB-E1-043 section 8 BR9; Principle 5; NFR-033; GAP-0698 |
| BR6 | The cache time to live is a catalog entry read through the parameters client, never a code constant; the value the legacy story carries is 300 (assumed; DL11) | DP-06; RWB-E1-043 section 13 |
| BR7 | A rule package is not a reference table: the client refuses a rule package code, and rule packages are governed in rwb-decision and evaluated through the rules kit | RWB-E1-043 section 12 and section 17; DP-04 |
| BR8 | The holiday calendar is not reference data: it is ACE data read from `v_ace_holiday` through the P1 query, and the client serves none of it | RWB-E1-043 section 2 and section 12; DP-05 |
| BR9 | The client reads only the rwb-case contract: it holds no table, writes no row and reads no other service's schema | DP-01; Ownership Map (`reference_version`, `reference_row` and `lov_value` are P3) |
| BR10 | The codes, the status vocabulary and the messages are those of the owner contract: the client adds no code, no status and no message of its own | RWB-PLT-E1043-CON; RWB-E1-043 sections 9 and 14 |

### 9. State transitions

No reference version changes its status in this story: VALIDATED, APPROVED and ROLLED_BACK are the owner's states and move only through the load and approve operations of RWB-P3-E1043-APP. The client holds one state per cache entry.

| From | Event | Condition | To |
|---|---|---|---|
| ABSENT | A read for a table code and business date | The owner answers an APPROVED version | CACHED |
| ABSENT | A read for a table code and business date | The owner answers no approved version | ABSENT; `NoVersionInForceException` thrown |
| CACHED | A read inside the time to live | None | CACHED, answered without a call |
| CACHED | The time to live elapses | None | EXPIRED |
| EXPIRED | The next read | The owner answers an APPROVED version | CACHED, replaced in place |
| CACHED or EXPIRED | The owner reports the version rolled back | None | EVICTED; the previous approved version is resolved |
| ANY | A code outside the twelve | None | ABSENT; the read is refused before any call |

The statuses of the reference version itself — VALIDATED, APPROVED, ROLLED_BACK — are named here so that the two documents agree on the vocabulary; the transitions among them are the business of RWB-P3-E1043-APP section 9.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The service developer of any of the 19 services | Binds the library, calls the read with its own business date and its own table codes, and reads the version it was given |
| The platform library team, owning the artefact | Publishes the interface and the types, changes them only through RWB-PLT-E1043-CON, and owns the cache, the logger and the code catalog |
| The rwb-case owner (P3) | Owns the two tables, the registry, the read service and the load and approve operations behind the consumed operations |
| The rwb-decision owner (P7) | Owns the rule packages and the registry the client refuses to serve |
| RW-COE, RW-REFADM | Load and approve the values in rwb-case; have no right in the library |
| RW-PLATADM | Receives the incident a caller raises when no version is in force |
| No delegation of authority level applies | The library takes no business decision and approves nothing |

No personal name, no email address and no credential appears in a document, a fixture or a log line. Where a caller must be named, the example uses the user identifier `U-REF-01` or a role code only.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-160 | reference_version | table_code | Read, through the rwb-case contract |
| DF-REF-161 | reference_version | version_no | Read, through the rwb-case contract |
| DF-REF-163 | reference_version | valid_from | Read, through the rwb-case contract |
| DF-REF-164 | reference_version | valid_to | Read, through the rwb-case contract |
| DF-REF-165 | reference_version | status | Read, through the rwb-case contract |
| DF-REF-169 | reference_version | row_count | Read, through the rwb-case contract |
| DF-REF-183 | reference_row | row_key | Read, through the rwb-case contract |
| DF-REF-184 | reference_row | row_data | Read, through the rwb-case contract |
| DF-REF-028 | lov_value | lov_code | Read, through the rwb-case list operation, for LOV-REF-TABLE |
| DF-REF-029 | lov_value | value_code | Read, through the rwb-case list operation, for LOV-REF-TABLE |

Field IDs are those in the Logical Data Model and Data Dictionary. The client writes no reference field and holds no table: `reference_version`, `reference_row` and `lov_value` are rwb-case's under the Ownership Map, and the load and approve fields DF-REF-159, DF-REF-166, DF-REF-167, DF-REF-168, DF-REF-170, DF-REF-171, DF-REF-181 and DF-REF-182 are written by RWB-P3-E1043-APP and not read here beyond the projection above. This story reads and writes no rule table and no rule field: `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are rwb-decision's and belong to RWB-P7-E1073 and the kit contract RWB-PLT-E1072-CON. The per-code column definitions and the column types are Not specified in the source documents (GAP-0697), and this story names no column beyond the fields above.

### 12. Contract

#### 12.1 REST operations provided

None — the library publishes Java types, not operations. The reference read, the list read, the parameters read, the reference-load and the approve operations belong to rwb-case (P3) in the Ownership Map, and the library adds no path, no topic and no task queue of its own.

#### 12.2 REST operations consumed

| Operation | Provider | Why the client needs it | Pattern |
|---|---|---|---|
| GET /api/recovery/case/v1/admin/lists/{listCode} | rwb-case (P3) | The LOV-REF-TABLE code set, so the twelve table codes are data and a rule package code is never in the set | DP-07, DP-11 |
| GET /api/recovery/case/v1/admin/parameters | rwb-case (P3) | The cache time to live as a catalog entry, so the bound is data and not a code constant | DP-06, DP-11 |

Two consumption rows, both one hop with a 2 s timeout and a breaker per provider (Architecture v5 slide 11). The list operation reads a list with its versions, as the legacy contract states, so the approved version in force and its rows arrive in that answer and the client makes no third call. The catalog key that carries the time to live is Not specified in the source documents (GAP-1409; ASM-2458); the legacy value 300 (assumed; DL11) is read through this operation and never hard-coded.

#### 12.3 Events published

None — the legacy design publishes no event for a version change and this story adds none. No message is written to the outbox by the client, and the outbox library of RWB-PLT-TE006-CON carries no reference event.

#### 12.4 Events consumed

None — no event is published for a version change, so none is consumed. A new approved version reaches a consumer at its next cache expiry, which is the read behaviour the legacy story carried; a later owner event would be consumed through the inbox library of RWB-PLT-TE006-CON.

#### 12.5 Workflows and activities

None — the client runs inside the caller's own activity or start-up hook, on the caller's own queue `rwb-<short>`. It starts no workflow, owns no task queue and is never called from workflow code, so a replay reuses the recorded answer.

#### 12.6 Schedules

None — the client owns no Schedule and no job. The refresh is the cache expiry of section 9, not a Temporal Schedule, and no job of the legacy design belongs to the library.

#### 12.7 Tables owned

None. `reference_version`, `reference_row` and `lov_value` stay with rwb-case (P3) under the Ownership Map default ruling and are named here only as the source of the read; `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` stay with rwb-decision (P7) and are not read at all. The library holds no table, no migration and no schema of its own, and the boundary test of section 13 fails the build on any read of those tables from the library (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| Reference-data client fake (RWB-PLT-E1043-CON) | `ReferenceDataClient.rows`, `versionInForce` and `versions` | A version-in-force answer with EXPOSURE_BAND version 3 and version 4, and a no-version answer for TEAM on 2026-11-30 (AC1, AC2, AC4, AC8) |
| rwb-case reference-data fake (RWB-P3-E1043-CON) | The version-and-rows read behind the client | QUEUE version 7 in force, a clock the test moves past the time to live, and a rollback of REGION version 5 (AC3, AC5, AC8) |
| rwb-case list fake (RWB-P3-E1043-CON) | `GET /api/recovery/case/v1/admin/lists/{listCode}` | The twelve LOV-REF-TABLE codes, a rule package code that is absent from the list, and a 403 for a role without Reference data R (AC6, X7) |
| rwb-case parameter fake (RWB-P3-E1042-CON) | `GET /api/recovery/case/v1/admin/parameters` | The cache time to live at 300, raised and missing (AC3) |
| Rules kit boundary fake (RWB-PLT-E1072-CON) | The kit's `RuleEvaluator` boundary | A call proving that no rule package code and no rule row reaches the client (AC6) |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None provided; two consumed operations over one provider | OpenAPI 3.1 at rwb-case, one hop, 2 s timeout, breaker per provider, GET only |
| Kafka | None published and none consumed | No event exists for a version change; the refresh is the cache expiry |
| Temporal | None | The client runs inside the caller's activity; it owns no queue, no workflow and no Schedule |
| File | None | A reference load file is handled by rwb-case and the reference data administrator; the library reads no file |

### 13. Solution plan

**Package.** Shared library artefact of the platform, Java package `th.co.scb.ace.workbench.recovery.platform.refdata`, with the published interface and the three types in `th.co.scb.ace.workbench.recovery.platform.refdata.api`. The library is not one of the 19 services: it has no schema, no topic, no task queue and no REST base.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The client reads the two reference tables only through the rwb-case contract and holds none of them | none |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision. The rule registry stays with rwb-decision (P7) and this client serves no rule table, so a rule package code is refused | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views. The ACE views are read by rwb-source-data (P1) and never by this library, so the holiday calendar reaches a caller through the P1 query and not through the client | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library. The cache time to live is a catalog entry read through the parameters client | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case. This story is that client library, so the row adds no dependency beyond the owner contract it is built against | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library. A permission failure on the consumed read is surfaced by the caller's guard, and the client fails closed | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents. The client publishes no event for a version change and uses the library for nothing | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout. The legacy in-process `ReferenceDataService` becomes the rwb-case REST contract and its fake | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`. The library adds no path; the two consumed paths are rwb-case's under `/api/recovery/case/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library. The library has no topic of its own and follows the naming rule for the caller's queue name only | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema. The library carries no migration; the consuming service applies its own baseline through the sequence | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route. The reference data screens read the tables through gateway-bff and Epic 8; the client adds no route | H RWB-PLT-N001-CON |

**Hardware and software change.** The client moves the reference read from an in-process service call against a shared schema to a library call against the rwb-case contract, compiled into 19 services on the existing AKS cluster. No new hardware is implied: the tables stay in the existing ACE PostgreSQL server, in the schema owned by rwb-case and the cache lives in each service's own heap. The software change is the loss of every private copy of a reference table from the service plans, the loss of any read of `reference_version` or `reference_row` outside rwb-case, and one log line per table read in place of an untraceable value.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `ReferenceDataClient` | Published interface | `rows`, `versionInForce` and `versions`; the only way a service reads a reference table (BR2) |
| ReferenceDataClientImpl | Service | Checks the table code, resolves the version in force through the owner contract, answers from the cache, throws the refusal (BR1, BR2, BR5) |
| ReferenceVersionCache | Service | Cache keyed by table code and business date; the time to live is read through the parameters client (BR6) |
| ReferenceVersionLogger | Service | One line per table read with the table code, the version number and the business date, and no customer identifier (BR4) |
| ReferenceTableCatalog | Service | The twelve reference table codes from LOV-REF-TABLE; refuses any other code, including a rule package code (BR1, BR7) |
| `ReferenceVersion`, `VersionedRows`, `NoVersionInForceException` | Published type | The records and the typed refusal the contract publishes; the exception carries MSG-P3-027 |
| Client fake and fixtures | Test asset | Version-in-force, no-version, cache-expiry and rollback answers used by every consuming service's tests (AC1 to AC8) |

**Configuration and reference data.** The cache time to live is the catalog entry the legacy story names, `refdata.cache.ttl-seconds`, with 300 as the legacy value and documented default (confirmed by the programme directive; DL11), published as a named entry of the rwb-case parameter catalog; the catalogue entry identifier itself is Not specified in the source documents (GAP-1409; ASM-2458). LOV-REF-TABLE carries the twelve codes and is loaded by the reference data administrator through RWB-P3-E1043-APP. The first approved version of each of the twelve tables is loaded by the reference data administrator and approved by RW-RISK before SIT, as legacy section 13 states. The library itself is configured with no business value. The model version in force for each decision step and the champion and challenger shares are reference data owned by rwb-case (P3) and reached through RWB-P3-E1043-CON (DP-07); the rule package registry stays with rwb-decision (P7); the table name is the R9 placeholder.

**Build steps**

1. Publish the interface and the three types from RWB-PLT-E1043-CON and compile a sample service against them; assert that no method opens a transaction and no method writes a row.
2. Write `ReferenceTableCatalog` over the list operation; assert the twelve codes, the absence of a rule package code and the refusal (AC6).
3. Write the version-resolution read through the owner contract with a fixed business date parameter; assert version 3 for 2026-11-30 and version 4 for 2026-12-01 (AC1, AC2).
4. Write `ReferenceVersionCache` with the time to live read through the parameters client; assert the hit, the expiry and the refresh (AC3).
5. Write the refusal path: `NoVersionInForceException` with the table code, the business date and MSG-P3-027, and the caller's contract test proving the engine does not start (AC4).
6. Write `ReferenceVersionLogger` and call it once per table read; assert the three fields and the absence of a customer identifier (AC5).
7. Prove the two exclusions in code: the holiday calendar is refused and read from `v_ace_holiday` through the P1 query, and the kit boundary shows no rule row reaching the client (AC6, AC7).
8. Prove the status filter: a VALIDATED version is not served and a ROLLED_BACK version is never returned (AC8).
9. Wire the fakes into a contract test and run it in the build of every consuming service, failing on any drift from RWB-PLT-E1043-CON.

**Screens and states.** This story builds no screen. SCR-39, SCR-40 and SCR-42 read the tables through the gateway-bff route (DP-19), and their empty, loading, error and no access states are each Not specified in the source documents (CG-ALL-1363; CG-ALL-1364; CG-ALL-1365).

**Feature flag.** One flag per consuming service, read as a parameter; off, the engine reads the value the service used before the library existed, and the library itself is always built.

**Done when.** The seven criteria pass, the contract tests of RWB-PLT-E1043-CON pass against the fakes, the boundary test shows no read of `reference_version`, `reference_row` or `lov_value` from outside rwb-case, a smoke run shows one log line for each of the twelve table codes, and no rule table and no holiday row is served. The artefact is published under the coordinates of the platform library baseline (GAP-1409; ASM-2458).

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-P3-027 | No approved version applies to the table and the business date, or the code is not a reference table | The {table} load was refused: {check}. Version {version} stays in force. | `NoVersionInForceException`, messageId MSG-P3-027, non-retryable in the caller |
| MSG-P4-002 | A caller without Reference data R reads the list or the parameters catalog | You cannot {action} here. Your role does not include it. | The caller's own 403; the client fails closed and serves no cached value |

The two texts are the legacy ones, character for character, and Thai text for each follows decision DL10. The refusal keeps the message identifier MSG-P3-027 although the tables now sit with rwb-case and the governance of a value is the owner's; no source renumbers it, and renumbering would break every log line and every decision record that cites it. In MSG-P3-027 the {table} placeholder carries the table code and, for the refusal this client raises, {check} names the check that failed and {version} names the version that stays in force.

### 15. Screens and states

No screen in this story, and the client adds no route to any screen (DP-19). The reference data screens SCR-39, SCR-40 and SCR-42 come in Epic 8 and read the tables through gateway-bff against the rwb-case contract; the loader holds RW-REFADM and the approver holds the approve right in Reference data, unchanged from legacy section 10. The client shows nothing to a user: it either answers the version in force with its rows, or refuses with a checked exception carrying MSG-P3-027, the table code and the business date, which is non-retryable, and leaves the caller to raise its own alert. The empty, loading, error and no access states of SCR-39, SCR-40 and SCR-42 are each Not specified in the source documents (CG-ALL-1363; CG-ALL-1364; CG-ALL-1365).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-E1043-APP-01 | AC1 | Component | EXPOSURE_BAND versions 3 and 4; reads for 2026-11-30 and 2026-12-01 against the client fake and the rwb-case reference-data fake |
| TC-PLT-E1043-APP-02 | AC2 | Component | versionInForce and versions for EXPOSURE_BAND after version 4 is approved; version 3 keeps its 4 rows and valid to 2026-11-30 |
| TC-PLT-E1043-APP-03 | AC3 | Component | QUEUE version 7, time to live 300 from the parameters fake, a moved clock and a second approved version |
| TC-PLT-E1043-APP-04 | AC4 | Component | TEAM with no approved version on 2026-11-30; the exception fields and MSG-P3-027; the caller's engine does not start |
| TC-PLT-E1043-APP-05 | AC5 | NFR | Two reads of QUEUE version 7 inside the time to live; the captured log line holds the table code, the version and the date and no customer identifier |
| TC-PLT-E1043-APP-06 | AC6, AC7 | Contract | A rule package code refused; the holiday calendar refused; the kit boundary fake and the rwb-source-data (P1) contract fake holiday read asserted |
| TC-PLT-E1043-APP-07 | AC8 | Component | A VALIDATED LEGAL_PERIOD version and a ROLLED_BACK REGION version 5; neither is served and no such cache entry exists |
| TC-PLT-E1043-APP-08 | AC9 | Contract | The eleven table codes read from LOV-REF-TABLE; the client's code list asserted against them; the RWB-PLT-E1043-CON status and message fakes |
| TC-PLT-E1043-APP-09 | AC10 | Component | rwb-case reference-data fake failing or not answering for QUEUE on 2026-11-30; the calling engine stub asserted not to run |

The full test, with its Given, When and Then, is carried into the next Test Cases version under the same id. The legacy set TC-E1-043-01 to TC-E1-043-11 is executed by RWB-P3-E1043-APP and is not copied here.

### 17. Guardrails

- No business value in code: table codes, versions, bands, limits and periods are rows, and the code holds only the versioning and read behaviour.
- No personal data in logs, fixtures, tests or prompts: a log line carries the table code, the version number and the business date, and nothing else.
- No read of another service's tables: `reference_version`, `reference_row` and `lov_value` are read through the rwb-case contract only, and the boundary test fails the build otherwise (DP-01).
- The cache never serves a version that is not APPROVED, and a rolled-back version is never returned.
- A missing version is a refusal with MSG-P3-027, never a default value and never a silent fallback to an older version.
- No rule table is read, loaded or versioned by the library, and no rule package code is accepted; rule packages are Drools packages of rwb-decision and the rules kit (DP-04).
- No holiday row is read or cached by the library: the calendar is ACE data under `v_ace_holiday` and reaches a caller through rwb-source-data (DP-05).
- The time to live is a catalog entry read through the parameters client, never a constant in the code.
- The library writes no row, opens no transaction and starts no workflow; a replay of the caller's activity reuses the recorded answer.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-011 | Reference data service with versioned tables, valid from and to, author and approver | Business Requirements Epic 1, section 4; Program, section 5.7 | FEAT-CWC-23 | 14 Set strategy, policy and decision rules | R-UNI-38; CTL-08 | TC-PLT-E1043-APP-01 to TC-PLT-E1043-APP-07 |
| REQ-CWC-006 | Roles, teams, queues and capacity as versioned reference data | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-23 | 14 Set strategy, policy and decision rules | R-UNI-38 | TC-PLT-E1043-APP-01, TC-PLT-E1043-APP-03, TC-PLT-E1043-APP-04 |
| REQ-CWC-016 | Every engine logs the table code and version of every table it reads | Cited in RWB-E1-043 section 8 BR7; Not specified in the source documents (GAP-1409; ASM-2458) | FEAT-CWC-23 | 14 Set strategy, policy and decision rules | R-UNI-38 | TC-PLT-E1043-APP-05 |
| TC-E1-043-01, TC-E1-043-02, TC-E1-043-03, TC-E1-043-04, TC-E1-043-05, TC-E1-043-06, TC-E1-043-07, TC-E1-043-08, TC-E1-043-09, TC-E1-043-10, TC-E1-043-11 | The whole legacy test set of RWB-E1-043, executed by RWB-P3-E1043-APP | RWB-E1-043 section 16 | FEAT-CWC-23 | 14 Set strategy, policy and decision rules | R-UNI-38; CTL-08 | Executed by RWB-P3-E1043-APP |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1043-CON | Contract | H: publishes the interface, the three types, the two consumed operations, the twelve-code set, the refusal and the fakes this story implements |
| RWB-P3-E1043-APP, RWB-P3-E1043-CON | App development, Contract | The owning-service pair: keeps the two tables, the registry, the read service, the load and approve operations and the cache, and owns the legacy acceptance criteria AC1 to AC10 |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | Contract | H and C: the parameters client and the catalog entry that carries the cache time to live (DP-06) |
| RWB-PLT-E1072-CON, RWB-P7-E1073-CON | Contract | H and C: the rules kit contract and the rwb-decision governance contract that own rule packages, so this client serves none (DP-04) |
| RWB-PLT-E1037-CON, RWB-P4-E1037-CON | Contract | H and C: the access guard library and the authorise contract behind a permission failure on the consumed read (DP-08) |
| RWB-PLT-TE006-CON | Contract | H: the outbox and inbox library; no reference event exists, so nothing is published (DP-09) |
| RWB-PLT-E1047-CON, RWB-PLT-E1044-CON | Contract | H: the naming library and the per-service Flyway baseline the artefact and its consumers follow (DP-14, DP-15) |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route under which the reference data screens will read the tables; no screen is built here (DP-19) |

### 19. Out of scope

- The two versioned tables `reference_version` and `reference_row`, the reference version registry, the read service, the load and approve operations and the cache: RWB-P3-E1043-APP and RWB-P3-E1043-CON.
- The rule packages and the rule registry — their load, validation, approval and rollback: rwb-decision (P7), RWB-P7-E1073 and the kit contract RWB-PLT-E1072-CON.
- The holiday calendar: ACE data under `v_ace_holiday`, read by rwb-source-data (P1); the client serves none of it.
- The reference data screens SCR-39, SCR-40 and SCR-42: Epic 8.
- The permission matrix and its masking rules: RWB-E1-037 and the access guard library (P4).
- The delegation of authority content: RWB-E1-038.
- The product parameter completeness checks (RWB-E1-045) and the rule change audit report (RWB-E2-041).
- The platform library artefact coordinates, its publication channel and its deployment pipeline: the platform library baseline and RWB-PLT-TPL, recorded in GAP-1409 with ASM-2457.
