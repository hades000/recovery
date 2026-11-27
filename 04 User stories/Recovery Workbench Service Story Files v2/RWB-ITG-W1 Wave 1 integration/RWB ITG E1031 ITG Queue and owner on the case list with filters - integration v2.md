# RWB-ITG-E1031-ITG Queue and owner on the case list with filters

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1031-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-031 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP08, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None; integration dependencies RWB-P3-E1031-APP and RWB-P4-E1039-APP are not done |
| Contract dependencies | None |
| Integration dependencies | RWB-P4-E1039-APP, RWB-P3-E1031-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-008, FR-PLT-019, FR-PLT-026, FR-PLT-033) |
| Status | Draft (directive resolutions) |
| Size | Not specified in the source documents (DOR-RWB-ITG-E1031-ITG-16) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-031 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E1031-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (12 resolved, 7 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof of the RWB-E1-031 case list with queue and owner, the queue, team and status filters and the Excel export across P3 rwb-case (the list, export and row limit) and P4 rwb-access (the right, the masking and the export access entry)**, so that **scope, masking and the export audit are proved on the real wave 1 services before the wave exits**.

### 2. Business rationale

The legacy story adds the queue and owner columns to SCR-02 Case list, filters the list by queue, team and status inside the caller's scope, and writes the export to the access log through the P4 `AccessEventPublisher` before the file is made. In the 19-service target the same behaviour is served from the owning services: the list and the export stay on P3 rwb-case under `/api/recovery/case/v1` (DP-13); the row limit, the queues and the status lists are data read through the P3 parameters and reference-data contracts (DP-06, DP-07); the access guard and the access log are P4 rwb-access's (DP-08), and the masking rules are P4's, applied over the P1 rwb-source-data masked view columns before any value reaches a response or a file; the screen itself is reached through gateway-bff (DP-19) but is not built or tested here.

The target split for the legacy key is therefore: P3 rwb-case owns the case list query, the queue, team and status filters, the export endpoint and the row limit, and reads the case and queue rows from its own schema (DP-01); P4 rwb-access owns the right check on Case record R, the masking policy for the role and the export access entry with its read path. This story is the integration proof across those two owners. This ITG story owns no legacy acceptance criterion: legacy AC1 to AC8 sit at component level with RWB-P3-E1031-APP, and the access criterion sits with RWB-P3-E1031-APP and RWB-P4-E1039-APP. The eleven scenarios of section 7 are the integration proof, and they are all new in D-RCV-60.

No service contract is faked: the suite exercises the published wave 1 contracts of P3 and P4 through gateway-bff. Where the sources do not name the exact access entry and its read path, the masking source used for the export columns, or the home of the row limit and the list rows, the suite asserts through the owners' contracts and records the open point as Not specified in the source documents (GAP-0355; ASM-0451), with its two companions ASM-0452 for the masking source and ASM-0453 for the parameter and list home.

The measure is unchanged from the legacy story: a user sees only the cases their scope allows (REQ-ACA-009), every case carries a queue and an owner visible on the list (REQ-CWC-007), the export holds at most the configured rows, and the list answers in under 2 seconds (NFR-008). The story meets REQ-ACA-005, REQ-ACA-006 and REQ-ACA-009 and supports controls CTL-09 and CTL-11.

### 3. Preconditions

- RWB-P3-E1031-APP is done: the case list, the queue, team and status filters, the export endpoint and the row limit are in SIT on P3 rwb-case.
- RWB-P4-E1039-APP is done: the right check on Case record R, the masking policy for the role and the access log with its write and read are in SIT on P4 rwb-access.
- The published contracts of P3 rwb-case and P4 rwb-access are deployed under their own per-service bases behind gateway-bff.
- The harness RWB-ITG-W1J01-ITG is available with synthetic cases, teams, queues and users.
- The parameter `caselist.export.maxrows` is 10,000 (assumed; DL11), loaded as a data row through the P3 parameters contract.
- The queues and the status lists are loaded as data rows: queue "DIL-BKK-CO", "DIL-BKK-OVF" and "LIT-BKK-OFF", and status "ASSIGNED" and "WAITING_PARTNER".
- The test users U-71 holding RW-TEAMMGR with scope Team, U-7102 holding RW-REFADM, and the scope All users of AC4 and AC8 exist in SIT.
- No production data is used, and no production connection is opened.
- The release date 30 November 2026 is tentative; a date is not a condition of this story.
- This story has no build dependency, so it is ready on Day 1.

### 4. Flow

1. QA integration engineer: seeds 64 cases in queue "DIL-BKK-CO", 20 in queue "DIL-BKK-OVF" and one case in queue "LIT-BKK-OFF" of team "LIT-BKK" through the harness RWB-ITG-W1J01-ITG; no production data is used.
2. Harness: signs in as test user U-71 holding RW-TEAMMGR with scope Team and reads the session through GET /api/recovery/access/v1/me/permissions.
3. Harness: calls GET /api/recovery/case/v1/cases with page 0 and size 50 and checks each row for case number, product, status, stage, queue, owner and entry date.
4. Harness: filters by queue "DIL-BKK-CO", then by team "DIL-BKK" and status "ASSIGNED", and records the total of each filtered list.
5. Harness: reads GET /api/recovery/case/v1/queues and asserts the three queues with their team codes.
6. Harness: calls GET /api/recovery/case/v1/cases/export on the filtered list and reads the xlsx row count and its header row.
7. Harness: reads GET /api/recovery/access/v1/admin/access-log and finds the export entry with user U-71, the time, the filters and the row count, and asserts that its write time precedes the file time.
8. Harness: runs the negative cases — no match, 10,001 rows, the access log switched to fail, the out-of-scope queue "LIT-BKK-OFF", the case with no owner, exactly 10,000 rows and the role without Case record R — and records every status, message and entry.
9. Harness: reads GET /api/recovery/case/v1/admin/parameters and asserts `caselist.export.maxrows` is 10000.
10. Harness: proves the 2 s budget over 20 calls of GET /api/recovery/case/v1/cases with page 0 and size 50 on 26,500 synthetic cases in scope, writes the evidence report and removes the fixtures.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No case meets the filters | The list returns an empty page with total 0 and the empty state is shown | MSG-P3-020 | AC3, AC6 |
| X2 | The filtered list holds more rows than the export limit | The export is refused with 422 and no file is made; the user narrows the filter | MSG-P3-021 | AC4 |
| X3 | The access entry cannot be written | The export returns no file; the refusal is raised before the xlsx is built | MSG-P7-003 | AC5 |
| X4 | A filter names a queue outside the caller's scope | Only in-scope cases return; the out-of-scope queue returns none | MSG-P3-020 | AC6 |
| X5 | A case has no owner | The owner cell is blank and the case is still listed | None | AC7 |
| X6 | The filtered list holds exactly 10,000 rows | The export is allowed and the file holds 10,000 rows | None | AC8 |
| X7 | A role without Case record R calls the list | The call is refused with 403 and no row returns | MSG-P4-002 | AC9 |
| X8 | The list exceeds the 2 s budget | The call is recorded as a breach against NFR-008; the suite reports the percentile and asserts nothing about the data | None | AC10 |
| X9 | A consumed call exceeds its 2 s timeout or returns a server error | The call is retried once under the suite policy; the evidence report records the call and the response; no assertion is made on unverified data | None | AC1, AC2, AC10 |
| X10 | The fixture set does not match the harness RWB-ITG-W1J01-ITG expectations | The suite fails as a harness fault and names the missing element; no service defect is raised | None | AC1, AC10 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is its own module and reuses the harness RWB-ITG-W1J01-ITG; it needs the two APP stories and the published contracts of P3 and P4, not their source code |
| Negotiable | The row limit, the queues, the status lists, the fixture sizes and the exact fault-switch mechanism are data rows or harness properties; the story fixes the assertions and the call set |
| Valuable | Scope, masking and the export audit are proved on the real wave 1 services, and the 2 s budget is measured rather than assumed, before the wave exits |
| Estimable | One suite module, one fixture pack of 26,500 cases, one export reader, one access-log assertion, one 2 s sampler and one evidence report |
| Small | Eleven scenarios over two services; no service code and no schema change |
| Testable | Every scenario asserts a contract response, a row count, a status or a message; all data is synthetic |

### 7. Acceptance criteria

```gherkin
Feature: Queue and owner on the case list with filters, end-to-end across wave 1 services

  Background:
    Given the wave 1 services rwb-case and rwb-access are deployed in SIT with their published contracts behind gateway-bff
    Given the RWB-ITG-W1J01-ITG synthetic cases, teams, queues and users are loaded and no production data is used
    Given team "DIL-BKK" has 64 cases in queue "DIL-BKK-CO" and 20 in "DIL-BKK-OVF"

  Scenario: AC1 Filter by queue (new, D-RCV-60)
    Given test user "U-71" of team "DIL-BKK" with scope Team
    When "U-71" filters by queue "DIL-BKK-CO"
    Then 64 cases return through GET /api/recovery/case/v1/cases, each with its owner and status
    Then no case from another queue shows

  Scenario: AC2 Export with its access entry (new, D-RCV-60)
    Given the list filtered by queue "DIL-BKK-CO" and status "ASSIGNED" holds 51 cases
    When "U-71" calls GET /api/recovery/case/v1/cases/export
    Then an Excel file with 51 rows downloads
    Then GET /api/recovery/access/v1/admin/access-log holds one export entry with user "U-71", the time, the filters and 51 rows, written before the file

  Scenario: AC3 No case meets the filters (new, D-RCV-60)
    Given test user "U-71" of team "DIL-BKK" with scope Team
    When "U-71" filters by queue "DIL-BKK-CO" and status "WAITING_PARTNER" and no case matches
    Then the list shows the empty state with MSG-P3-020

  Scenario: AC4 Export above the limit (new, D-RCV-60)
    Given parameter "caselist.export.maxrows" is 10000
    Given a filtered list holds 10,001 cases for a user with scope All
    When the user exports
    Then no file is made
    Then MSG-P3-021 shows with maximum 10000

  Scenario: AC5 The access log is unavailable (new, D-RCV-60)
    Given the P4 access-log write is switched to fail by the agreed test-only fault switch
    When "U-71" exports a list of 51 cases
    Then the call returns no file and MSG-P7-003
    Then no export entry is written

  Scenario: AC6 Queue outside the scope (new, D-RCV-60)
    Given test user "U-71" of team "DIL-BKK" with scope Team
    When "U-71" filters by queue "LIT-BKK-OFF" of team "LIT-BKK"
    Then no case shows
    Then the list shows the empty state with MSG-P3-020

  Scenario: AC7 A case with no owner (new, D-RCV-60)
    Given case "RW-2026-000601" is in queue "DIL-BKK-OVF" with no owner
    When "U-71" filters by that queue
    Then the case shows with a blank owner value

  Scenario: AC8 Export at the limit (new, D-RCV-60)
    Given a filtered list of exactly 10,000 cases for a user with scope All
    When the user exports
    Then a file with 10,000 rows downloads

  Scenario: AC9 A role without Case record R is refused (new, D-RCV-60)
    Given test user "U-7102" holds RW-REFADM
    When the user calls GET /api/recovery/case/v1/cases
    Then the call returns status 403 with MSG-P4-002

  Scenario: AC10 The list meets the 2 second budget (new, D-RCV-60)
    Given 26,500 synthetic cases in scope
    When the suite calls GET /api/recovery/case/v1/cases with page 0 and size 50 twenty times
    Then the 95th percentile response time is under 2 seconds (NFR-008)

  Scenario: AC11 The architecture constraints of BR6 to BR9 hold on the consumed contracts (new, D-RCV-60)
    Given 26,500 synthetic cases in scope and a filtered list of 51 cases for test user "U-71"
    When the suite reads the list, the queues, the parameters and the export through gateway-bff
    Then the list meets the 2 second budget of NFR-008 (BR6)
    Then the row limit and the queues come back as data rows from GET /api/recovery/case/v1/admin/parameters and GET /api/recovery/case/v1/queues, and the status lists are read as data rows through the P3 reference-data contract (BR8)
    Then the export carries only the masked columns of the caller's role (BR7)
    Then every owner display name is synthetic in SIT and comes from the ACE user directory in the common module, and every call is one hop with a 2 s timeout (BR9, ADR-020, DP-11)
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The list holds only cases inside the caller's scope (Own, Team, Region, All) | RWB-E1-031 BR1; REQ-ACA-009; CTL-09; LOV-SCOPE |
| BR2 | Filters combine with AND; the team filter is Not specified in the source documents (GAP-2208) | RWB-E1-031 BR2; FSD A2.19 |
| BR3 | Every export is written to the access log before the file is made; the export access entry and its read-back path are Not specified in the source documents (GAP-0355) | RWB-E1-031 BR3; REQ-ACA-006; CTL-11 |
| BR4 | Export columns follow the masking rules for the caller's role | RWB-E1-031 BR4; REQ-ACA-005; DL26 |
| BR5 | An export holds at most the configured number of rows | RWB-E1-031 BR5; parameter caselist.export.maxrows = 10,000 (assumed; DL11) |
| BR6 | A screen responds in under 2 seconds | RWB-E1-031 BR6; NFR-008 |
| BR7 | Masking is applied from the P4 rules over the P1 masked view columns before any value reaches a response or the file; how the P4 rules reach rwb-case is Not specified in the source documents (GAP-0355) | REQ-ACA-005; DL26; DP-08 |
| BR8 | The row limit, the queues and the status lists are data rows read through the P3 contracts | DP-06; DP-07 |
| BR9 | Owner display names come from the ACE user directory in the common module and are synthetic in SIT; the owner display name path is Not specified in the source documents (GAP-0355), and every call is one hop with a 2 s timeout | ADR-020; DP-11 |

Open decisions that apply to this section: DL10 (assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863); DL11 (assumptions ASM-0553, ASM-0703, ASM-1051, ASM-1104); DL26 (assumptions ASM-0247, ASM-0264, ASM-0275, ASM-0355).

### 9. State transitions

None. This story changes no case status; it reads queue, owner and status only. The screen's Loading, empty, list and filtered states are observations of one read, not transitions.

| Observation | Meaning |
|---|---|
| Loading | The screen waits for the page of GET /api/recovery/case/v1/cases; the suite reads the same page and adds nothing |
| Empty | The page holds no item and total 0, and MSG-P3-020 is shown; AC3 and AC6 read this state |
| List | Rows carry case number, product, status, stage, queue, owner and entry date; AC1 and AC7 read this state |
| Filtered | The chosen queue, team and status are applied and the total reflects them; AC1, AC2 and AC8 read this state |

The suite reads these observations through the owner's contract; it changes none of them directly.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TEAMMGR | Lists, filters and exports cases in team scope (Case record R) |
| RW-CASEOWN | Lists and exports their own cases (Case record R, scope Own) |
| Every role with Case record R | Lists cases in its scope |
| RW-REFADM, RW-SECADM | No Case record right; refused |
| RW-COMPLY | Reads the access log entries for exports |
| QA integration engineer | Runs the suite, seeds the synthetic fixtures, reads the evidence report |

No other role is in scope for this story.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case (P3 rwb-case) | id | Read |
| DF-CAS-002 | recovery_case (P3 rwb-case) | case_no | Read |
| DF-CAS-003 | recovery_case (P3 rwb-case) | product_group | Read |
| DF-CAS-005 | recovery_case (P3 rwb-case) | status | Read |
| DF-CAS-006 | recovery_case (P3 rwb-case) | stage_code | Read |
| DF-CAS-009 | recovery_case (P3 rwb-case) | owner_user_id | Read |
| DF-CAS-010 | recovery_case (P3 rwb-case) | queue_id | Read |
| DF-CAS-011 | recovery_case (P3 rwb-case) | team_code | Read |
| DF-CAS-012 | recovery_case (P3 rwb-case) | region_code | Read |
| DF-CAS-013 | recovery_case (P3 rwb-case) | entry_date | Read |
| DF-WRK-001 | queue (P3 rwb-case) | id | Read |
| DF-WRK-002 | queue (P3 rwb-case) | queue_code | Read |
| DF-WRK-003 | queue (P3 rwb-case) | queue_name | Read |
| DF-WRK-004 | queue (P3 rwb-case) | team_code | Read |
| Access entry, its read path, the masking source and the parameter and list home | P4 rwb-access access log and masking policy; P3 rwb-case parameters and reference data | Test-only names and read paths | Not specified in the source documents (GAP-0355; ASM-0451) |

Every field in the table is read through the contracts of section 12.2, never from a schema (DP-01). The export carries the masked columns only: it holds no customer name and no identity number. Field IDs are those in the Logical Data Model and Data Dictionary. Every row in the suite is synthetic, loaded by the harness RWB-ITG-W1J01-ITG.

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The names reserved for P2 rwb-integration — `/api/recovery/integration/v1`, `rwb.integration.events.v1`, `rwb-integration` and `rwb_integration` — are not used, and no rwb_integration table is written.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| GET /api/recovery/case/v1/cases | P3 rwb-case | The scoped and filtered list with queue and owner; AC1, AC3, AC6, AC7, AC9, AC10 |
| GET /api/recovery/case/v1/cases/export | P3 rwb-case | The xlsx of the filtered list; AC2, AC4, AC5, AC8 |
| GET /api/recovery/case/v1/queues | P3 rwb-case | The queue rows used by the queue filter |
| GET /api/recovery/case/v1/cases/{caseId} | P3 rwb-case | One case row, to confirm the blank owner of case RW-2026-000601 |
| GET /api/recovery/case/v1/admin/parameters | P3 rwb-case | The row limit caselist.export.maxrows as a data row |
| GET /api/recovery/access/v1/admin/access-log | P4 rwb-access | The export entry with user, time, filters and row count; AC2, AC5 |
| GET /api/recovery/access/v1/me/permissions | P4 rwb-access | The right and the masking position of the caller's role |

The contract version of each consumed operation is the v1 carried by its /v1 path in the table above; no other contract version is named in the story or the source documents (DOR-RWB-ITG-E1031-ITG-23).

Every call is one hop with a 2 s timeout (ADR-020, DP-11).

#### 12.3 Events published

None. The suite publishes no event.

#### 12.4 Events consumed

None. The suite consumes no topic in this story: the list and the export are synchronous REST reads. No legacy `rwb.p3.` or `rwb.casewf.` topic name appears anywhere in the run (DP-14).

#### 12.5 Workflows and activities

None. No workflow, activity or Nexus operation is started or awaited by this story.

#### 12.6 Schedules

None. The list and the export are on demand; no Schedule, workflow or activity runs for them.

#### 12.7 Tables owned

None. The suite owns no table and never reads another service's schema (DP-01). The rows behind the assertions are recovery_case and queue in rwb_case (P3), and role and masking_rule in rwb_access (P4); each is read only through its owner's contract.

#### 12.8 Contract fakes

None. Every call in section 12.2 goes to the real SIT service; no service contract is faked. No contract fake library version for rwb-access or rwb-case is recorded as published: Not specified in the source documents (DOR-RWB-ITG-E1031-ITG-22). AC5 uses the agreed test-only fault switch on the P4 access-log write, and it is the only intervention in a running service. The synthetic xlsx is checked by row count and header row only, and its masked columns are checked through the header names.

#### 12.9 Call-type summary

| Call type | Provided by the suite | Consumed by the suite |
|---|---|---|
| REST | 0 | 7 |
| Kafka | 0 | 0 |
| Temporal | 0 | 0 |
| File | 0 | 0 |

The xlsx arrives in the body of the export response; it is not a claim-check file call, so the file column stays at zero.

### 13. Solution plan

| Component | Type | Responsibility |
|---|---|---|
| Suite module for RWB-ITG-W1, reusing harness RWB-ITG-W1J01-ITG | Integration suite | Runs the eleven scenarios against SIT and holds no service code |
| Fixture pack | Test data | 26,500 synthetic cases across teams and queues, the queues and status lists, and the test users U-71, U-7102 and the scope All users |
| Export reader | Assertion | Opens the xlsx of the response, reads the header row and the row count, and asserts the masked columns and the absence of a customer name and an identity number |
| Access-log assertion | Assertion | Reads GET /api/recovery/access/v1/admin/access-log and matches the export entry on user, time, filters and row count, and on its write time preceding the file |
| 2 s sampler | Assertion | Calls GET /api/recovery/case/v1/cases with page 0 and size 50 twenty times and reports the 95th percentile against 2 seconds |
| Evidence report | Report | Records per scenario the total, the file row count, the access entry, the statuses, the messages and the percentile |

Decoupling patterns applied (Template and Rules v1 §R5.5):

| DP | Legacy marker | Microservice pattern | Dependency added | Where it sits |
|---|---|---|---|---|
| DP-01 | recovery.<table>, "recovery schema" | Owner's schema rwb_<name>; never read another service's tables | none | P3 rwb-case owns schema rwb_case with recovery_case and queue; the suite reads no table in any schema and asserts through contracts only |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON | On RWB-P3-E1031-APP for the row limit; the suite reads the same row as data through GET /api/recovery/case/v1/admin/parameters |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | On RWB-P3-E1031-APP for the queues and the status lists; the suite sends the codes as data |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON | On RWB-P3-E1031-APP for the right check and on RWB-P4-E1039-APP for the masking and the access log; the suite asserts the refusal of AC9 and the entry of AC2 |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | The seven consumed REST operations of section 12.2 |
| DP-13 | /api/recovery/v1 | /api/recovery/<short>/v1 | none | Every consumed path in section 12.2 |
| DP-14 | rwb.p<n>. or rwb.casewf. topic names | rwb.<short>.events.v1; naming library | H RWB-PLT-E1047-CON | The suite consumes no topic, and no legacy topic name appears in the run |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | On RWB-P3-E1031-APP for the case and queue rows; the suite owns no table and runs no migration |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The suite enters through gateway-bff; no screen is in scope and none is tested |

The dependency-added column records the build dependency of the owning story. The H, C, I and X lists of this story are exactly those of the metadata table: no H, no C, no X, and the two I dependencies RWB-P4-E1039-APP and RWB-P3-E1031-APP. An ITG story waits on no build of its own. The row and envelope names of the case list, the page-token name and the 401 message text are Not specified in the source documents (GAP-2209).

Build steps:

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the SIT endpoints of P3 rwb-case and P4 rwb-access through gateway-bff.
2. Build the fixture pack: 26,500 synthetic cases across teams and queues, the queues "DIL-BKK-CO", "DIL-BKK-OVF" and "LIT-BKK-OFF", the status lists, and the users U-71, U-7102 and the scope All users, with `caselist.export.maxrows` read as a data row.
3. Implement AC1, AC3, AC6 and AC7: the scoped and filtered list, the empty state, the out-of-scope queue and the blank owner.
4. Implement AC2, AC4, AC5 and AC8 with the export reader and the access-log assertion: the 51-row file and its entry, the refusal above 10,001 rows, the fault-switch refusal with no entry, and the 10,000-row file.
5. Implement AC9: the refused call of the RW-REFADM user with status 403 and MSG-P4-002.
6. Implement AC10: the 2 s sampler over 20 calls on 26,500 synthetic cases and the 95th percentile report.
7. Prove BR4 and BR7 over the header row and a value read of the export, write the evidence report, run the suite in SIT against the wave 1 release candidate and remove the fixtures.

Done when: all eleven test cases pass in SIT against the published wave 1 contracts of P3 and P4, the export entry is found for every successful export and for none of the refused ones, the 95th percentile of the list is under 2 seconds on 26,500 cases, and no service code or schema was changed by this story apart from the agreed test-only fault switch.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-020 | No case meets the filters | No cases match these filters. Change a filter to see more. |
| MSG-P3-021 | Export above the row limit | The export holds at most {max} rows. Narrow the filters and try again. |
| MSG-P7-003 | Access log unavailable at export | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

A successful export carries no message: the response is the file itself, and its proof is the access entry of AC2.

The message IDs and wording are copied from RWB-E1-031 section 14. No new message ID is added by this story. Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-02 Case list, reached through gateway-bff. Loading: skeleton rows. Empty: MSG-P3-020. Error: Not specified in the source documents (CG-ALL-310). No access: Not specified in the source documents (CG-ALL-310). List: columns case number, product, status, stage, queue, owner, entry date. Filtered: the chosen queue, team and status show above the list with a clear control, and Export uses the filters shown.

The suite does not build or test the screen; it reads the same rows through GET /api/recovery/case/v1/cases and the same file through GET /api/recovery/case/v1/cases/export. The export file name is "Case list 20261202 1.xlsx".

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-031-01-ITG | AC1, BR1, BR2 | Integration | Synthetic 64 cases in queue DIL-BKK-CO of team DIL-BKK; end-to-end: real services on the wave 1 contracts |
| TC-E1-031-02-ITG | AC2, BR3, BR4 | Integration | Synthetic 51 cases filtered by queue and status, one export entry; end-to-end: real services on the wave 1 contracts |
| TC-E1-031-03-ITG | AC3 | Integration | Synthetic filter with no match in queue DIL-BKK-CO; end-to-end: real services on the wave 1 contracts |
| TC-E1-031-04-ITG | AC4, BR5 | Integration | Synthetic 10,001 cases with scope All against the limit 10000; end-to-end: real services on the wave 1 contracts |
| TC-E1-031-05-ITG | AC5, BR3 | NFR | P4 access-log write switched to fail over a synthetic list of 51 cases; end-to-end: real services on the wave 1 contracts |
| TC-E1-031-06-ITG | AC6, BR1 | Integration | Synthetic queue LIT-BKK-OFF of team LIT-BKK; end-to-end: real services on the wave 1 contracts |
| TC-E1-031-07-ITG | AC7 | Integration | Synthetic case RW-2026-000601 in queue DIL-BKK-OVF with no owner; end-to-end: real services on the wave 1 contracts |
| TC-E1-031-08-ITG | AC8, BR5 | Integration | Synthetic exactly 10,000 cases with scope All; end-to-end: real services on the wave 1 contracts |
| TC-E1-031-09-ITG | AC9 | Component | Test user U-7102 holding RW-REFADM; end-to-end: real services on the wave 1 contracts |
| TC-ITG-E1031-ITG-10 | AC10, NFR | NFR | 20 calls on 26,500 synthetic cases with page 0 and size 50; end-to-end: real services on the wave 1 contracts |
| TC-ITG-E1031-ITG-11 | AC11, BR6, BR7, BR8, BR9 | Integration | 26,500 synthetic cases in scope, a filtered list of 51 cases, the parameter and queue data rows and the masked export; end-to-end: real services on the wave 1 contracts |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the legacy test case id.

### 17. Guardrails

- No business value in code: the row limit, the queues and the status lists are data rows read through the P3 contracts.
- No personal data in logs, tests, evidence or prompts: the export applies masking by role and holds no customer name and no identity number; only field IDs and masking positions are asserted.
- No cross-service table read: every assertion goes through the owner's contract, and the suite owns no table. Owner display names come from the ACE user directory interface.
- One hop and a 2 s timeout on every call (ADR-020).
- The export is never made when its access entry cannot be written; the refusal is raised before the file is built.
- Synthetic data only, loaded by the harness RWB-ITG-W1J01-ITG; the scope All users of AC4 and AC8 hold no production right.
- No production access of any kind from the suite or its configuration.

### 18. Traceability

| Requirement or decision | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-CWC-007 | Every case has a queue and an owner by rule, visible on the case list | GET /api/recovery/case/v1/cases with the queue and owner columns, GET /api/recovery/case/v1/queues | TC-E1-031-01-ITG, TC-E1-031-03-ITG, TC-E1-031-07-ITG |
| REQ-ACA-009 | A user sees only the cases their scope allows | GET /api/recovery/case/v1/cases with the scope of the caller, GET /api/recovery/access/v1/me/permissions, MSG-P4-002 | TC-E1-031-02-ITG, TC-E1-031-04-ITG, TC-E1-031-05-ITG, TC-E1-031-06-ITG, TC-E1-031-08-ITG, TC-E1-031-09-ITG |
| NFR-008 | A screen responds in under 2 seconds | GET /api/recovery/case/v1/cases with page 0 and size 50 on 26,500 cases | TC-ITG-E1031-ITG-10 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The seven consumed REST operations of section 12.2 | TC-E1-031-02-ITG, TC-E1-031-04-ITG, TC-E1-031-08-ITG |
| DP-08 | Authorise contract of rwb-access and the guard library | The right check behind GET /api/recovery/case/v1/cases, the masking of the export columns and the export entry read through GET /api/recovery/access/v1/admin/access-log | TC-E1-031-02-ITG, TC-E1-031-05-ITG, TC-E1-031-09-ITG |
| DP-06 | Parameters contract of rwb-case | GET /api/recovery/case/v1/admin/parameters for caselist.export.maxrows | TC-E1-031-04-ITG, TC-E1-031-08-ITG |
| ASM-0451 | The access entry and its read path have target names on their owner | GET /api/recovery/access/v1/admin/access-log and the export endpoint of section 12.2 | TC-E1-031-02-ITG, TC-E1-031-05-ITG |
| ASM-0452 | The masking source for the export columns is P4 rules over the P1 masked view columns | The header row and the value read of the export in AC2 and AC8 | TC-E1-031-02-ITG, TC-E1-031-08-ITG |
| ASM-0453 | The row limit and the lists are P3 data rows | GET /api/recovery/case/v1/admin/parameters and GET /api/recovery/case/v1/queues | TC-E1-031-04-ITG, TC-E1-031-08-ITG |

The legacy AC1 to AC8 at component level belong to RWB-P3-E1031-APP, and the access test at component level belongs to RWB-P3-E1031-APP and RWB-P4-E1039-APP, not to this story.

### 19. Out of scope

- The P3 rwb-case and P4 rwb-access APP builds and their unit and component tests.
- The CON, DB and OPS stories of the two services.
- The legacy AC1 to AC8 at component level and the access test at component level, which the sibling APP stories own.
- SCR-07 My queue and team queue (Epic 2).
- The base case list filters by product, stage, age and deviation (RWB-E1-002, FEAT-RDF-18).
- The masking rules themselves (RWB-E1-037, DL26).
- The build of the harness RWB-ITG-W1J01-ITG.
- NFR load and performance testing.
