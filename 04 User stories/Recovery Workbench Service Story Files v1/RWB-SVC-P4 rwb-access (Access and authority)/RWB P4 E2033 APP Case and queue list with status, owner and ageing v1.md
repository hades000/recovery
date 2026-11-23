# RWB-P4-E2033-APP Case and queue list with status, owner and ageing

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E2033-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-033 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP08, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P4-AT |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2033-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (FR-P4-023, FR-P4-024, FR-P4-025, FR-P4-026, FR-P4-027) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-033 and rewritten for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **team manager (RW-TEAMMGR), a case owner or an internal auditor who reads the case and queue list**, I want **rwb-access to answer, for that list and for its extract, which capability right my session holds, which scope predicate filters every row and every queue, which personal fields come back masked, and which filter set and row count the extract records**, so that **a manager sees every case of the team and no case of another team, the file leaves one record of who took what, and no answer tells anybody that a case outside their scope exists**.

Inside `rwb-access` this is the authority side of legacy RWB-E2-033:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- The capability is the answer behind the list and the extract, in three parts: the session answer of `GET /me/session`, extended here with the CASE_RECORD right, the scope predicate and the two policy versions in force; the per-object check for one case or one queue row, which is the CASE_RECORD branch of the authorise contract of DP-08 (`RWB-P4-E1037-CON`); and one access record per extract. No screen, no list query, no timer and no workflow is built here.
- The policy the answers come from is data in `rwb_access`: `role` with `default_scope`, `permission` with `capability_area`, `letters` and `matrix_version`, and `masking_rule` with `field_id`, `unmasked` and `masking_version`. No case, queue, timer, deviation or customer row is read (DP-01), and no parameter, list of values or queue code is copied into this schema.
- The row facts the object check needs — the case, its queue, its team, its owner and its region — arrive in the request from the caller, which holds them. The list itself, its twelve columns, the age in state, the breach flag and the two clocks stay in `rwb-case` (`RWB-P3-E2033-APP`, `RWB-P3-E2011-APP`), the composed page and the workbook stay in `rwb-integration` (`RWB-P2-E2033-APP`), and the extract writer stays in `RWB-P3-E1031-APP`.
- The legacy behaviour carried into the access service is unchanged: the same four scope values OWN, TEAM, REGION and ALL, the same refusal of a role with no Case record right, the same "not in your scope" answer that never confirms a case exists, the same masking default of a field with no rule, and the same single record per extract. The legacy story fixed the scope, the refusal and the entry; it fixed no element name for the answer, so the names of section 12.1 are Not specified in the source documents (GAP-2320; ASM-3849).

### 2. Business rationale

The legacy story exists because a team manager learns where work waits by asking each owner or by building a spreadsheet, and RWB-E1-031 with RWB-E2-011 puts the queue, the owner, the age and the service level state on the list. What none of those stories settles is who may see the page: the monolith answered a manager, a case owner and an auditor out of one in-process guard, with the scope applied inside the same query and the masking applied by whichever screen the reader happened to be on. Under Architecture v5 each service authorises its own object against cached permission data from `rwb-access`, with a 2 s timeout (slide 10), the case service reaches the access service by REST (slide 13), and the roles, permissions, scopes and masking rules are `rwb-access` rows (slide 41).

This story supplies that answer for the case and queue list and for its extract: the CASE_RECORD right, the scope predicate that filters every row and every queue, the masking markers of the fields the row asks about, and the record the extract leaves. It meets REQ-WKM-002 on the access side (the team's queues, filtered and exportable, and nothing of another team), carries REQ-DVH-006 (a deviation flag on a case in scope is never suppressed by this answer, so the flag is visible in every queue view), and meets REQ-ACA-006 on the extract side (one record of the user, the time, the filters and the row count before the file is made); REQ-ACA-006 also named a data-lake copy, which no longer exists. The measure of success is that every list read and every extract is granted or refused by the policy in force, that no role reaches a queue outside its scope, and that every extract leaves exactly one record with its filters and its row count.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| `RWB-P4-E1037-CON` | The service contract of `rwb-access` already in force from wave 1, under DP-08: the authorise contract, the guard library and the rule-to-permission matrix as data (legacy RWB-E1-037). This story implements the CASE_RECORD branch of that contract for the list, the queue row and the extract, and adds no operation to it |
| `RWB-P2-E2033-CON` | The published page and row shape of the composed case list on the integration base, whose element names and filter tokens this answer feeds and whose fake the story builds against. The contract is a build-against dependency only and never blocks. Architecture v5 slide 13 draws no P2 to P4 call, so the shape this answer must satisfy is taken from that contract (GAP-2320; ASM-3848) |
| `RWB-PLT-E1042-CON`, `RWB-P3-E1042-CON` | The parameters client library and the parameters contract of `rwb-case` (DP-06): `caselist.export.maxrows` 10,000, the legacy value under DL11, and the page-size bounds 1 to 200 that bound one batch of the authorise answer |
| `RWB-PLT-E1043-CON`, `RWB-P3-E1043-CON` | The reference-data client library and contract (DP-07): LOV-SCOPE with OWN, TEAM, REGION, ALL and LOV-CAPABILITY with CASE_RECORD and QUEUE_AND_ALLOCATION, with the version in force. No scope or capability string is written in code |
| `RWB-PLT-E1047-CON` | The naming library behind the topic and event names of DP-14 |
| `RWB-PLT-E1044-CON` | The per-service Flyway sequence in `rwb_access` (DP-15) |
| `RWB-PLT-N001-CON` | The gateway-bff composite route that serves SCR-02 (DP-19); the route and its merge order are that platform story's |

Business preconditions carried from RWB-E2-033, owned by other services where they say so:

- Matrix version `PM-2026.12` is in force and gives CASE_RECORD right R to RW-CASEOWN, RW-TEAMMGR, RW-SPECIAL and RW-AUDIT, with `default_scope` OWN for RW-CASEOWN, TEAM for RW-TEAMMGR and ALL for RW-AUDIT, and no CASE_RECORD right to RW-REFADM (TSD P4 T3.1 `role.default_scope`, LOV-SCOPE; legacy section 3). That the other reading roles of the legacy authority table keep the scope their own role row carries is assumed (ASM-3851).
- Masking version `MASK-SIT-01` is in force. That this is the masking version of the SIT environment is Not specified in the source documents (GAP-2320; ASM-3852).
- Queues `MTG-BKK-CO` and `MTG-BKK-LIT` belong to team `MTG-BKK`, the queue rows being `rwb-case`'s (legacy section 7). This story holds no queue row and reads none.
- The SERVICE_LEVEL and PRESCRIPTION timers, the breach flag and the deviation flag exist (RWB-P3-E1028-APP, RWB-S8); this story reads none of them.
- The caller signed in through Entra ID with a second factor and holds at least one Recovery role; with no role the answer is 401 MSG-P4-001.
- The service connects with the rwb-access login (DP-02). Its name is Not specified in the source documents (GAP-2320; ASM-3854); the story says "the rwb-access login" and never the shared monolith login.
- The platform contracts the DP rows name are in place behind `RWB-P4-E1037-CON` in wave 1, so this secondary slice adds no build dependency of its own (metadata H = None) and is Day 1.

### 4. Flow

1. Caller: a person opens SCR-02 Case list. gateway-bff resolves the session and calls the case list service, which asks `rwb-access` for the session answer.
2. `rwb-access`: reads the caller's roles from the session ACE Common resolved at sign-in, and the rights, scope and matrix version from `permission` and `role` for the versions in force.
3. `rwb-access`, right check: no CASE_RECORD R for any role the caller holds gives 403 with MSG-P4-002 naming the action, and an answer with no scope and no version (BR1).
4. `rwb-access`, scope predicate: the scope value comes from the `default_scope` of the caller's roles, read against LOV-SCOPE: OWN admits the cases the caller owns, TEAM the cases of `teamCode`, REGION the cases of `regionCode`, ALL any case (BR2). The answer carries the predicate and never a queue list, because the queue rows are the caller's.
5. `rwb-access`, masking: for the field IDs the caller names, the profile for the versions in force is read from `masking_rule`; a field with no covering row is marked masked (BR5). The answer marks each field `masked` or `clear` and carries no value.
6. `rwb-access`: caches the answer for the versions in force, writes nothing, and returns it inside the 2 s budget of DP-11.
7. Caller: builds the page, applies the predicate to the queue filter and to every row, and serves the twelve columns of the legacy list; a case outside the predicate is answered 404 with MSG-P4-003, never an empty row.
8. Caller, on a queue row or a case row: asks the authorise answer for that object with its team, owner and region. `rwb-access` answers from the same cached policy per object; one batch may carry at most the page size in force (BR6).
9. Team manager: chooses Extract. The caller sends the same filters, the export intent and the number of rows the scoped query returned.
10. `rwb-access`: checks the row count against `caselist.export.maxrows`, writes one access record (BR7) through the log path of `RWB-P4-E1039-APP`, and only then answers that the extract may be built; the workbook itself is `RWB-P3-E1031-APP`'s.
11. Policy change: a new matrix or masking version is loaded through the load path and is used from its `valid_from`; the next answer under the new version is computed afresh and no restart is needed (BR6).

Every answer is written before it is returned where it records a read; when the record cannot be written, the extract is refused with a 503 rather than served unrecorded (BR7).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No Recovery role in the session | 401 before the policy is read; no scope, no version and no row | MSG-P4-001 | BR1 |
| X2 | A role with no Case record right | 403 with the action named; no scope, no version and no row read | MSG-P4-002 | AC2 |
| X3 | A case or queue outside the predicate, whatever the request asks | 404 with no owner, no team and no field marker, so the answer never confirms the case exists | MSG-P4-003 | AC3 |
| X4 | A field has no masking row | The field is marked `masked` with the default marker; the answer is otherwise granted | None | AC11 |
| X5 | A filter token outside its list of values | 422 on the field; no access record and no case read | MSG-GEN-007 | AC7 |
| X6 | One batch of object checks above the page size in force | 422 naming the bound; no object is checked | MSG-GEN-002 | AC8 |
| X7 | The extract above `caselist.export.maxrows` | 422 naming the limit; no record and no file | MSG-P3-021 | AC6 |
| X8 | The access record cannot be written | The extract is refused with 503 and no file is made, and an incident is raised to the platform queue | MSG-P7-003 | BR7 |
| X9 | The parameters or reference contract does not answer inside its budget | No answer rather than a guessed one: 503, and the refusal is recorded | MSG-GEN-006 | BR9 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds and tests against the composed-page fake of `RWB-P2-E2033-CON` and the platform contracts already in force; reads `rwb_access` only and calls no other service at run time |
| Negotiable | The policy pack — roles, matrix, scope values, masking rows and their versions — is data; the story fixes the shape of the answer and the refusal behaviour only |
| Valuable | The list shows a manager the team's queues and hides another team's, the extract leaves one record, and no answer confirms that a case outside the scope exists |
| Estimable | One extended answer, one object check, one access record, one cache and no migration |
| Small | Fits one sprint with its tests; no screen, no query over case rows, no timer and no workflow |
| Testable | Every criterion in section 7 has a test case in section 16, on fixed synthetic data |

### 7. Acceptance criteria

```gherkin
Feature: Case and queue list with status, owner and ageing

  Background:
    Given today is 10 December 2026 at 09:00 Asia/Bangkok
    Given permission matrix version "PM-2026.12" is in force and gives CASE_RECORD right "R" to RW-CASEOWN, RW-TEAMMGR, RW-SPECIAL and RW-AUDIT and no CASE_RECORD right to RW-REFADM
    Given the default scope in force is "OWN" for RW-CASEOWN, "TEAM" for RW-TEAMMGR and "ALL" for RW-AUDIT
    Given masking version "MASK-SIT-01" is in force and holds unmasked "false" for DF-PTY-007 and DF-PTY-008 for RW-CASEOWN, RW-TEAMMGR and RW-AUDIT
    Given the rwb-integration contract mock returns the case-list rows of team "MTG-BKK": case "RW-2026-000101" in queue "MTG-BKK-CO" owned by "U-1001" status ASSIGNED, case "RW-2026-000102" in queue "MTG-BKK-LIT" owned by "U-1002" status IN_PROGRESS, and case "RW-2026-000103" in queue "MTG-BKK-CO" with no owner and status NEW

  Scenario: AC1 The session answer names the right, the scope and the versions (new, D-RCV-60)
    Given test user "U-1000" holds RW-TEAMMGR for team "MTG-BKK"
    When the caller reads GET /api/recovery/access/v1/me/session
    Then the answer carries caseRecordRight "R" for area "CASE_RECORD" under matrix version "PM-2026.12"
    Then the answer carries scope "TEAM" with team code "MTG-BKK" and no other team
    Then the answer names masking version "MASK-SIT-01"
    Then the scope predicate admits all three mock rows, including the unowned case "RW-2026-000103"
    Then one answer serves the request: a second read inside the same request reads no "permission" row twice

  Scenario: AC2 A role with no Case record right is refused before a row (new, D-RCV-60)
    Given test user "U-1401" holds RW-REFADM, which has no CASE_RECORD right in "PM-2026.12"
    When the caller asks for the session answer of the list
    Then the answer is 403 with message MSG-P4-002 naming the action "read the case list"
    Then the answer carries no scope, no team code, no version and no row
    Then the refusal is offered to the log path of RWB-P4-E1039-APP with no case data

  Scenario: AC3 The scope cannot be widened by the request (new, D-RCV-60)
    Given test user "U-1000" holds RW-TEAMMGR for team "MTG-BKK"
    Given the rwb-integration contract mock returns a row for case "RW-2026-000201" in queue "HP-NE-CO" of team "HP-NE"
    When the caller asks the authorise answer for case "RW-2026-000201" with scope "ALL" in the request
    Then the answer is 404 with message MSG-P4-003
    Then the answer carries no owner, no team and no field marker
    Then the requested scope "ALL" is ignored and the answer names scope "TEAM" with team "MTG-BKK"

  Scenario: AC4 The answer takes no view of the timer or the clock (new, D-RCV-60)
    Given case "RW-2026-000104" has deviation X1 open, its SERVICE_LEVEL timer paused and its PRESCRIPTION timer running to 30 June 2028
    Given the rwb-integration contract mock returns that row with service level state PAUSED and prescription clock RUNNING
    When the caller asks the session answer and the authorise answer for case "RW-2026-000104"
    Then both answers are granted with scope "TEAM" and the same two versions
    Then when the mock returns the same case with no SERVICE_LEVEL timer, and then with a timer due 10 December 2026 09:00 read at 09:00 and again at 09:01, the two answers are identical each time
    Then no rule of this story reads a timer row, a breach flag or a deviation flag

  Scenario: AC5 The extract leaves one entry with the filter set and the row count (new, D-RCV-60)
    Given the manager filters the list by queue "MTG-BKK-CO", product MORTGAGE and breached Yes and the scoped query returns 1 row
    When the caller asks the export answer with those three filters and row count 1
    Then the export is granted under scope "TEAM"
    Then one AC-EXPT entry is written with the actor, the time, the three filters, row count 1 and no case ID
    Then the entry is written before the workbook is asked for, and a refused entry serves no file

  Scenario: AC6 Above the row limit no entry and no file (new, D-RCV-60)
    Given 10,001 cases in the manager's scope match breached No and "caselist.export.maxrows" is 10,000
    When the caller asks the export answer with that row count
    Then the answer is 422 with message MSG-P3-021 naming 10,000 rows
    Then no AC-EXPT entry is written and no workbook is asked for

  Scenario: AC7 A filter token outside its list is refused and records nothing (new, D-RCV-60)
    When the caller asks the export answer with product "CAR", which is not in LOV-PRODUCT
    Then the answer is 422 with message MSG-GEN-007 for field product
    Then no AC-EXPT entry is written and no case is read

  Scenario: AC8 A batch above the page size in force is refused (new, D-RCV-60)
    Given the page size in force is minimum 1 and maximum 200
    When the guard asks the authorise answer for 500 case IDs at once
    Then the answer is 422 with message MSG-GEN-002 naming page size, minimum 1 and maximum 200
    Then when the maximum is changed to 100 by a parameter row, a batch of 100 is answered and a batch of 500 is still refused

  Scenario: AC9 No case matches (new, D-RCV-60)
    Given no case of team "MTG-BKK" has product SSME
    When the list is read and the extract asked with that filter
    Then the session answer is unchanged and admits no row
    Then one AC-EXPT entry is written with row count 0 and no case ID
    Then the workbook the writer builds holds the header row only

  Scenario: AC10 Paging under the scope is stable (new, D-RCV-60)
    Given 120 cases in scope with no breach and the same age in state
    When page 1 and page 2 of size 50 are read
    Then both reads are answered with scope "TEAM", team "MTG-BKK", matrix "PM-2026.12" and masking "MASK-SIT-01"
    Then page 1 admits the 50 lowest case numbers and page 2 the next 50, and no case appears on both pages

  Scenario: AC11 A field with no masking row is masked (new, D-RCV-60)
    Given no masking rule in "MASK-SIT-01" covers DF-PTY-008 for any role
    When the manager asks the answer for the field IDs of a list row, including DF-PTY-007 and DF-PTY-008
    Then DF-PTY-007 is marked "masked"
    Then DF-PTY-008 is marked "masked" with the default marker "XXXX-XX-XX"
    Then no field of the answer is marked "clear" and no value is returned

  Scenario: AC12 A change of version is used from the next answer (new, D-RCV-60)
    Given matrix version "PM-2026.13" is loaded with valid_from 11 December 2026 and gives RW-TEAMMGR default scope "REGION"
    When the manager reads the session answer on 10 December 2026 and again on 11 December 2026
    Then the first answer names "PM-2026.12" and scope "TEAM"
    Then the second answer names "PM-2026.13" and scope "REGION", with no deployment and no restart
    Then no cached answer survives the change
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The list and the extract need CASE_RECORD right R. A role without it is refused before any object is read, and the refusal carries no scope and no version | legacy BR1; CTL-09; TSD P4 T6.2 |
| BR2 | The scope value is the `default_scope` of the caller's roles, read against LOV-SCOPE: OWN, TEAM, REGION or ALL. Where a caller holds two roles the wider scope applies. The request never widens the answer | `role.default_scope`; LOV-SCOPE; legacy BR1 |
| BR3 | A case outside the predicate is answered as not in scope, 404 with no case fact, so the answer never confirms that a case exists | legacy section 5 X4; CTL-09 |
| BR4 | The answer takes no view of a timer, a breach, an escalation or a deviation: access depends on the object's team, owner and region and on the two versions in force only | legacy BR3, BR4 |
| BR5 | Masking: a field whose `masking_rule` row for the role and the version in force holds `unmasked` false is marked masked, and a field with no covering row is masked with the default marker. The answer marks fields and never carries a value | `masking_rule`; AC-EXC-P4-004-05; legacy BR7 |
| BR6 | Every answer names the matrix version and the masking version it used. A version is used from its `valid_from`, and one batch of object checks carries at most the page size in force | `matrix_version`, `masking_version`, `valid_from`; parameter row |
| BR7 | One access record per extract, with the actor, the time, the filter set, the row count and no case ID, written before the workbook is built; a refused record serves no file | legacy BR7; REQ-ACA-006; AC-ALT-P4-007-02 |
| BR8 | Only `role`, `permission` and `masking_rule` of `rwb_access` are read. No case, queue, timer, parameter, list or queue code is read here, and no other schema is named | DP-01, DP-05, DP-06, DP-07 |
| BR9 | A refusal is a refusal: 401, 403, 404, 422 or 503 with its message identifier and no data, never a thinner answer | legacy section 5 |

### 9. State transitions

None. This story changes no case status and no policy row. It reads `role`, `permission` and `masking_rule` and, on an extract, adds one access record through the log path of `RWB-P4-E1039-APP`, which is append only and belongs to that story. A policy version has its own load lifecycle (LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED), which the load stories own (RWB-P4-AD002-APP, RWB-P4-AD004-APP); this story only reads the version in force.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TEAMMGR, team manager | Reads and extracts under scope TEAM for the queues of the team |
| RW-CASEOWN, case owner | Reads and extracts under scope OWN |
| RW-AUDIT, internal audit | Reads and extracts under scope ALL, and still sees the masked fields |
| RW-REFADM, reference data administrator | No CASE_RECORD right; refused with MSG-P4-002 |
| A break-glass grant of CASE_RECORD R with scope ALL | Honoured for the incident window; every record written in it carries the grant ID and the incident (`RWB-P4-E1039-APP`) |
| No approval applies | The story takes no decision and approves nothing |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-034 | role | id | Read |
| DF-REF-035 | role | role_code | Read |
| DF-REF-037 | role | role_class | Read |
| DF-REF-038 | role | default_scope | Read |
| DF-REF-040 | permission | id | Read |
| DF-REF-041 | permission | role_id | Read |
| DF-REF-042 | permission | capability_area | Read |
| DF-REF-043 | permission | letters | Read |
| DF-REF-044 | permission | matrix_version | Read |
| DF-REF-198 | masking_rule | id | Read |
| DF-REF-199 | masking_rule | role_code | Read |
| DF-REF-200 | masking_rule | field_id | Read |
| DF-REF-201 | masking_rule | unmasked | Read |
| DF-REF-202 | masking_rule | masking_version | Read |
| DF-REF-203 | masking_rule | valid_from | Read |
| DF-REF-204 | masking_rule | valid_to | Read |
| Not specified in the source documents (GAP-2320; ASM-3853) | parameter row of the rwb-case catalog | the page-size bounds that bound one batch of object checks, and `caselist.export.maxrows`, with the version in force | Read, in process through the parameters contract |
| Not specified in the source documents (GAP-2320; ASM-3853) | reference_row of the rwb-case catalog | LOV-SCOPE and LOV-CAPABILITY rows with the version in force | Read, in process through the reference-data contract |

Field IDs are those of the Logical Data Model and Data Dictionary. Every row named here is a `rwb_access` row; the parameters and the reference rows are read through the contracts of `rwb-case` and never joined in SQL, and the access record of an extract is a row of the decision log written by `RWB-P4-E1039-APP`. No row of this story is written, so no field is marked Write.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/access/v1`; owner rwb-access (P4).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/me/session` | The caller's resolved session, extended by this story with `caseRecordRight` for area CASE_RECORD, the scope predicate (`effectiveScope` with `teamCode` or `regionCode`), `matrixVersion` and `maskingVersion`, and the masking markers of the field IDs the request names | None beyond a valid session; 401 with no Recovery role | Read only: the same request under the same versions returns the same answer |

The per-object check for one case or one queue row, and one batch of such checks, is the authorise contract published by `RWB-P4-E1037-CON` under DP-08; this story implements its CASE_RECORD branch, its scope rule and its batch bound of the page size in force, and adds no operation to it, so its path and its request and answer shapes are that contract's and are not restated here (GAP-2320; ASM-3849).

The element names `caseRecordRight`, `effectiveScope`, `teamCode`, `regionCode`, `matrixVersion`, `maskingVersion` and `fields` are proposed by this document and fixed at the baseline review of `RWB-P2-E2033-CON`, because the sources name the session response type and the four scope values but no element of this answer (GAP-2320; ASM-3849). Errors: 401 no session or no Recovery role (MSG-P4-001); 403 no Case record right (MSG-P4-002); 404 an object outside the scope (MSG-P4-003); 422 a token outside its list (MSG-GEN-007), a batch above its bound (MSG-GEN-002) or an extract above its row limit (MSG-P3-021); 503 a store or a contract that does not answer (MSG-GEN-006).

#### 12.2 REST operations consumed

One hop, no chaining; 2 s timeout and a breaker per downstream (ADR-020).

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | the path fixed in `RWB-P3-E1042-CON` (Not specified in the source documents (GAP-2320; ASM-3853)) | rwb-case (P3) | `caselist.export.maxrows` and the page-size bounds, with the version in force, cached by the parameters client | 2 s, cached |
| GET | the path fixed in `RWB-P3-E1043-CON` (Not specified in the source documents (GAP-2320; ASM-3853)) | rwb-case (P3) | LOV-SCOPE and LOV-CAPABILITY rows with the version in force, cached by the reference-data client | 2 s, cached |

No case, queue, timer or deviation read is made: the object facts arrive in the request from the caller, which holds them. The composed page of `RWB-P2-E2033-CON` is a build-against contract and never a run-time call.

#### 12.3 Events published

None. The topic `rwb.access.events.v1` carries no event from this story, and no outbox row is written. DP-14 has an instance here as the naming rule only: any event of this service is `rwb.access.<Event>.v1` on that topic, and this story adds none.

#### 12.4 Events consumed

None. The answer is computed from the rows per request, so a policy change is seen on the next answer under the new version rather than through a projection, and no inbox row is written. `rwb.deviation.DeviationRaised.v1` and `rwb.deviation.DeviationCleared.v1` are consumed by `RWB-P3-E1028-APP`; the deviation flag is not this story's subscription and is not read here.

#### 12.5 Workflows and activities

None. The answer is served inside the request: no workflow, no activity, no signal and no timer. The service has no workflow in the target, and the durable case timers live in `CaseWorkflow` on task queue `rwb-case`.

#### 12.6 Schedules

None. The session answer is computed per request and expires with the version in force, so no schedule refreshes it. JOB-18 belongs to this service but not to this story.

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| `role` | rwb_access | rwb-access (P4) | The caller's roles, their class and their `default_scope` |
| `permission` | rwb_access | rwb-access (P4) | The CASE_RECORD letters of a role under the matrix version in force |
| `masking_rule` | rwb_access | rwb-access (P4) | The `unmasked` marker of a field for a role under the masking version in force |
| `delegation_limit`, `role_conflict` | rwb_access | rwb-access (P4) | Not read by this story |
| `outbox_event`, `processed_event` | PLT library, created in rwb_access | Platform library | Not written by this read path |

No other table is named. `recovery_case`, `queue`, `timer`, `parameter_catalog`, `reference_row` and `lov_value` are `rwb_case`'s and are read through its contracts only (DP-01, DP-06, DP-07). The access record of an extract is a decision-log row and is written by `RWB-P4-E1039-APP`.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-integration WireMock | The composed page of `RWB-P2-E2033-CON` | The rows of team `MTG-BKK`, the filter tokens `queue`, `product` and `breached`, and one row of team `HP-NE` for the scope refusal |
| rwb-case parameter stub | `RWB-P3-E1042-CON` | `caselist.export.maxrows` 10,000, page-size bounds 1 and 200, a later maximum of 100 and a limit of 20,000 |
| rwb-case reference stub | `RWB-P3-E1043-CON` | LOV-SCOPE with its four values, LOV-CAPABILITY with CASE_RECORD and QUEUE_ALLOCATION, and LOV-PRODUCT without `CAR` |
| gateway-bff route stub | The edge route of `RWB-PLT-N001-CON` | The SCR-02 route and the merged screen model (DP-19) |
| rwb_access fixtures | This story's own test data | Matrix `PM-2026.12` and `PM-2026.13`, masking `MASK-SIT-01`, the four test users of section 7, and the AC-EXPT record reader |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, plus the CASE_RECORD branch of the authorise contract; 2 consumed | `GET /me/session` provided; the parameters and reference-data reads of `rwb-case` consumed; one hop, 2 s, breaker, cached per request |
| Kafka | None | No event published and none consumed (12.3, 12.4); the access record travels on the decision-record path of `RWB-P4-E1039-APP` |
| Temporal | None | No workflow and no activity (12.5) |
| File | None | The workbook is `RWB-P3-E1031-APP`'s; this story only gates it on the record |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `authority`; the answer is served inside the existing session endpoint of the service.

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_access`; only `role`, `permission` and `masking_rule` are read | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and its client library: `caselist.export.maxrows` and the page-size bound are parameter rows, never constants | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case: LOV-SCOPE and LOV-CAPABILITY with the version in force | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library: this story is the CASE_RECORD branch behind them, cached per request and per version | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/access/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.access.events.v1` and `rwb.access.<Event>.v1` as the naming rule; this story publishes nothing | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in `rwb_access`: the three tables exist from the wave 1 baseline, so this story adds no migration | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route for SCR-02: the list reads this answer through the route | H RWB-PLT-N001-CON |

DP-01 is the read of the three tables; DP-06 the two limits of AC6 and AC8; DP-07 the scope and capability values of AC1; DP-08 the answer of AC1, AC3 and AC4; DP-13 the base path; DP-19 the route the list is read through; DP-14 and DP-15 have an instance as conventions only, since nothing is published and no table is added. Metadata H is None because every platform contract these rows name is already in force behind `RWB-P4-E1037-CON` in wave 1, and `RWB-P2-E2033-CON` never blocks.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| SessionController | Controller | `GET /me/session`; the 401, 403 and 503 problem bodies with their message IDs |
| ScopeResolver | Service | BR2: the scope predicate from `role.default_scope` and LOV-SCOPE |
| PermissionSnapshotReader | Service | BR1: the CASE_RECORD letters of the caller's roles under the matrix version in force |
| MaskingMarkerReader | Service | BR5: the `masked` or `clear` marker of each named field, with the default marker |
| ObjectCheckService | Service | The CASE_RECORD branch of the authorise contract, per object and per batch (BR3, BR6) |
| PolicyVersionResolver | Service | BR6: the matrix and masking versions in force for the business date, and the cache key |
| ExportGateService | Service | BR7: the row count against the limit, the record built before the workbook, and the 503 of X8 |
| AccessRecordWriter | Client | The in-process call of the log path of `RWB-P4-E1039-APP`; this story supplies the values and the order |
| ParameterClient, ReferenceClient | Client | The cached reads of DP-06 and DP-07 |

**Database and migrations.** Reads `role`, `permission` and `masking_rule` of `rwb_access`; uses the primary keys and the `matrix_version` and `masking_version` columns the wave 1 baseline carries. No new table, column, index or migration (GAP-2320; ASM-3855). The service connects with the rwb-access login (DP-02), holding grants on `rwb_access` only.

**Configuration and reference data.** `caselist.export.maxrows` is 10,000, the legacy value under DL11, and the batch bound is the page size in force of 1 to 200, both read as parameter rows and never as constants. LOV-SCOPE and LOV-CAPABILITY are read with the version in force. The service holds no feature flag of its own: the switch `rwb.casewf.case-list-ageing` of the legacy story belongs to the case list stories and changes none of this answer.

**Build steps**

1. `SessionController` and the answer of 12.1 against the composed-page fake, with one test per refusal; AC1, AC2.
2. `ScopeResolver` and `PermissionSnapshotReader` with unit tests on the four scope values, two roles, the unowned case and the matrix version; AC1, AC3.
3. `ObjectCheckService` over the contract of DP-08, including the batch bound; AC3, AC8.
4. `MaskingMarkerReader` with the covering row, the missing row, the default marker and the version in force; AC11.
5. `PolicyVersionResolver` and the cache key, with the `valid_from` change of AC12 and the per-request reuse of AC1.
6. `ExportGateService` and `AccessRecordWriter`, with the entry order, the limit and the 503 of X8; AC5, AC6, AC7, AC9.
7. The parameter and reference clients with their budget, the 503 of X9 and their caches.
8. The contract test of `RWB-P2-E2033-CON` and the architecture test that no statement names a schema other than `rwb_access`; AC10.

**Done when.** The tests in section 16 pass; one session answer and one batch of 200 object checks return inside 2 s at the 95th percentile in SIT (NFR-008); every extract leaves exactly one AC-EXPT record with its filters and row count; the contract test of `RWB-P2-E2033-CON` is green; and no query of this story reaches a schema other than `rwb_access`.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | No valid session or no Recovery role | You have no Recovery Workbench role. Ask your team manager to request one. | This story, on the session answer |
| MSG-P4-002 | The role does not hold the Case record right | You cannot {action} here. Your role does not include it. | This story, before any object is read |
| MSG-P4-003 | The case or queue is outside the scope | This case is not in your scope. | This story, on the object check |
| MSG-GEN-007 | A filter token is not in its list | {value} is not a valid value for {field}. | This story, on the export answer |
| MSG-GEN-002 | One batch is above the page size in force | {field} must be between {min} and {max}. | This story, on the batch bound |
| MSG-P3-021 | The extract is above its row limit | The export holds at most {max} rows. Narrow the filters and try again. | This story, before the record and the workbook |
| MSG-P7-003 | The access record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on X8 |
| MSG-GEN-006 | A contract does not answer inside its budget | Not specified in the source documents (GAP-2320; ASM-3850) | This story, on the guards |

The message identifiers are the legacy ones and none is renumbered by the realignment. Thai text for each message follows decision DL10. The refusal order is fixed: session, then right, then the field list, then the filter tokens, then the batch bound or the row count, and only then is an answer given or a record written.

### 15. Screens and states

| Screen | State | What this story supplies |
|---|---|---|
| SCR-02 Case list | Loading | The session answer that the route asks for in parallel with the page |
| SCR-02 Case list | List | The scope predicate that decides which rows and queues appear, and the masking markers of the fields the row asks about |
| SCR-02 Case list | Filtered | The predicates and the versions, so a filter change is a new predicate request and never a new policy |
| SCR-02 Case list | Empty | The answer that admits no row, and the AC-EXPT record with row count 0 on an extract |
| SCR-02 Case list | Not permitted | The 403 of MSG-P4-002 and the 404 of MSG-P4-003, each with no row data |
| SCR-02 Case list | Extract | The gate: the limit check, one AC-EXPT record, then the workbook of `RWB-P3-E1031-APP` |
| SCR-02 Case list | Break-glass banner | The grant ID and the incident on each record written in the window (`RWB-P4-E1039-APP`) |

This story draws no screen. The layout, the columns and the "Breached" and "Paused" markers are `RWB-P3-E2033-APP`'s and the designer's (DL31), and the route path and the merge order are `RWB-PLT-N001-CON`'s (DP-19); the route and its screen-model field list are Not specified in the source documents (GAP-2320; ASM-3848).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-033-12 | AC2, BR1, BR9 | Component | RW-REFADM asks for the session answer; 403 MSG-P4-002, no scope and no row |
| TC-E2-033-01 | AC1, BR2, BR6 | Component | Manager of team MTG-BKK, three mock rows in two queues, matrix PM-2026.12 |
| TC-E2-033-02 | AC4, BR4 | Unit | Paused SERVICE_LEVEL timer, running PRESCRIPTION timer, deviation X1 open; identical answers |
| TC-E2-033-03 | AC5, BR7 | Contract | Four cases, filters queue, product and breached, row count 1, one AC-EXPT record and the workbook afterwards |
| TC-E2-033-04 | AC4, BR4 | Unit | Timer due 10 December 2026 09:00, read at 09:00 and 09:01; no change in the answer |
| TC-E2-033-05 | AC4, BR4 | Unit | NEW case with no SERVICE_LEVEL timer; granted under scope TEAM |
| TC-E2-033-06 | AC7, BR9 | Contract | Product filter CAR outside LOV-PRODUCT; 422 MSG-GEN-007 and no record |
| TC-E2-033-07 | AC8, BR6 | Contract | Batch of 500 against the bound 200; 422 MSG-GEN-002, then the maximum 100 and a batch of 100 |
| TC-E2-033-08 | AC9, BR7 | Component | Product SSME with no SSME case; no row admitted and one record with row count 0 |
| TC-E2-033-09 | AC3, BR2, BR3 | Component | Case of team HP-NE asked by the MTG-BKK manager with scope ALL in the request; 404 MSG-P4-003 |
| TC-E2-033-10 | AC6, BR7 | Contract | 10,001 matching rows against the limit 10,000; 422 MSG-P3-021, no record and no workbook |
| TC-E2-033-11 | AC10, BR2, BR6 | Component | 120 cases of equal age, pages of 50, page 1 and page 2 read in sequence |

The legacy level System maps to Component where the answer is asserted on the service's own operation against seeded `rwb_access` rows and the composed-page fake, to Contract where the assertion is the request and answer, and to Unit where the resolver is proved without a database. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The set is run here against this slice's assertions and by `RWB-P3-E2033-APP` and `RWB-P2-E2033-APP` against the page they serve; no identifier carries an `-ITG` suffix here, because the integration copy is `RWB-ITG-E2033-ITG`.

### 17. Guardrails

- No business value in code: the scope values, the capability areas, the two bounds and the two versions are rows and parameters read with the version in force; code holds behaviour only.
- No personal data in logs, tests, workflow history or prompts: the answer marks field IDs and never carries a value, a case row never enters this service, and test data is synthetic.
- No read of another service's tables: `role`, `permission` and `masking_rule` are `rwb_access` rows; the case, queue, timer, parameter and reference rows come through contracts (DP-01, DP-06, DP-07).
- No ACE view is read: this answer needs no account, customer, contact or collateral field.
- One hop only: the parameters and reference clients are cached and never chain to a further service (ADR-020).
- The answer is a read: nothing is written except the one access record of an extract, which belongs to `RWB-P4-E1039-APP`.
- A refusal is a refusal: no right, an object outside the scope and a token outside its list are answers with a status and a message identifier, never a thinner answer.
- The record comes first: an extract is gated on its record, so no file is ever served unrecorded.
- The cache is versioned, so a policy change takes effect from its `valid_from` and no answer outlives the version it names.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-002 | Team manager sees every team queue, filters by status, product and ageing, exports the view | Business Requirements Epic 2, section 3.2 | None in this module (the capability row is FEAT-ACA-07, FEAT-ACA-08) | All recovery processes | BR1, BR2, BR3, BR6, BR7 | TC-E2-033-01, TC-E2-033-03, TC-E2-033-06 to TC-E2-033-11 |
| REQ-DVH-006 | Deviation flag visible in every queue view | Business Requirements Epic 2, section 3.2 | None | All recovery processes | BR4 | TC-E2-033-02, TC-E2-033-04, TC-E2-033-05 |
| REQ-ACA-006 | Every read of the case store is written to the access log | Business Requirements Epic 2, section 3.2 | FEAT-ACA-08 | All recovery processes | BR7, BR9 | TC-E2-033-03, TC-E2-033-10 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | Not applicable to a business requirement | None | Not applicable | BR1, BR9 | TC-E2-033-01, TC-E2-033-12 |

REQ-DVH-006 is carried by BR4: a deviation flag on a case in the predicate is never suppressed by this answer, and a case outside it is not shown at all, so the flag is visible everywhere the case is. REQ-ACA-006 also named a data-lake copy; the data lake is removed (DP-17), so the requirement is carried by the extract record and its order alone. The per-case read entry of the case record view belongs to `RWB-P4-E1039-APP`.

| Legacy reference | Where it is kept |
|---|---|
| The purpose and the actors of the legacy story | Metadata, sections 1, 2, 10 |
| The scope of legacy BR1 and the four scope values | Sections 3, 7 AC1 to AC3, 8 BR2, 12.1 |
| The scope refusal of legacy X4 and MSG-P4-002, MSG-P4-003 | Sections 5, 7 AC2 and AC3, 14 |
| The breach and pause facts the legacy story shows | Sections 7 AC4, 8 BR4, 19 |
| The extract record of legacy BR7 and of AC-ALT-P4-007-02, with the row count and no case ID | Sections 7 AC5, AC6, AC9, 8 BR7, 12.1 |
| The masking default of AC-EXC-P4-004-05 | Sections 7 AC11, 8 BR5 |
| Legacy test set TC-E2-033-01 to TC-E2-033-12 and its integration copy | Section 16 |
| Legacy key RWB-E2-033, story RWB-P4-E2033-APP, contract RWB-P2-E2033-CON | Metadata, sections 1, 3, 12 |

### 19. Out of scope

- The list query, its twelve columns, the age in state, the breach flag and the two clocks: `RWB-P3-E2033-APP`, `RWB-P3-E2011-APP` and their contracts.
- The composed page on the integration base and the Excel workbook: `RWB-P2-E2033-APP`, `RWB-P2-E2033-CON`.
- The extract writer, its columns and its file: `RWB-P3-E1031-APP`.
- The access-log record's own story, its search operation and break-glass: `RWB-P4-E1039-APP`, `RWB-P4-E1039-CON`, `RWB-P4-AD007-APP`. This story supplies the values and the order only.
- Loading the permission matrix, the scope rows and the masking rows: `RWB-P4-AD002-APP`, `RWB-P4-AD003-APP`, `RWB-P4-AD004-APP` and their contracts.
- The rights and scope of every other capability area, the role-to-Entra mapping and the separation-of-duty check: `RWB-P4-AD001-APP`, `RWB-P4-AD005-APP`, `RWB-P4-E1037-APP`.
- The deviation record, its code, its owner and its clearance: rwb-deviation (S8).
- Next action columns, escalation, manual transfer and the service level values per state: `RWB-E2-035`, `RWB-E1-028`, `RWB-E2-015`, `RWB-E2-012`, DL22.
- The composite route path, its merge order and the screen field list: `RWB-PLT-N001-CON`; the layout belongs to the designer (DL31).
- The end-to-end journey with every service live and its `-ITG` copies: `RWB-ITG-E2033-ITG`.
