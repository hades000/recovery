# RWB-P4-E2034-APP Interaction ledger on the case and from every channel

**Version 3 changes.**

- MSG-GEN-006 and MSG-P4-001 carry the English text of Error and Message Standard v6 (RD-P1-004).

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E2034-APP |
| Readiness decisions | RD-P1-004 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-034 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement; no size value in the source documents (DOR-RWB-P4-E2034-APP-16) |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP08, DP09, DP10, DP11, DP13, DP15, DP18, DP19 |
| Parallel lane | L-P4-AU |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2034-CON, RWB-P4-E1037-CON (path `/api/recovery/access/v1`; contract version Not specified in the source documents (DOR-RWB-P4-E2034-APP-23)) |
| Integration dependencies | Interaction ledger on rwb-source-data; IDs Not specified in the source documents (GAP-1612) |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-ILG-009, REQ-ILG-010, REQ-ILG-011, REQ-ILG-012, REQ-ILG-013, REQ-ILG-014, REQ-ILG-007, REQ-ILG-008, REQ-ILG-006) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-034 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E2034-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (25 resolved, 21 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **holder of RW-CASEOWN, RW-TEAMMGR, RW-CONDUCT or RW-AUDIT who reads the interaction ledger of a case — and as an agent that reads it on their behalf**, I want **one access answer for that ledger: whether my role may read it, which scope admits the case, and which fields of an entry come back masked — the same on every channel the entry came from and on every screen that shows it — with each ledger read written into the access log**, so that **the ledger is read where the case is read, the contact point of an entry is never shown to a role that may not see it, and any audit question about who read which ledger can be answered from one log**.

Inside `rwb-access` this is the access-side slice of legacy RWB-E2-034: service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, service topic `rwb.access.events.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`, one schema and one login per service (DP-01, DP-02, DP-13).

- **The answer this story builds:** for one case and the field IDs of its ledger entries, the area `CASE_RECORD` right `R`, the scope that admits the case (OWN, TEAM, REGION or ALL), and a `masked` or `clear` marker per field ID under the masking version in force. The answer carries markers and identifiers, never a value.
- **Owned here:** the mask of an entry's personal fields by role, the right and scope refusal of the ledger read, and the access-log entry of every ledger read and every refusal (FEAT-ACA-05, FEAT-ACA-07, FEAT-ACA-08, FEAT-ACA-16).
- **Not this slice:** the ledger table, the append, the case-scoped interaction read, the EFS intake rule, the outcome list and the retention class are `rwb-source-data`'s (DP-18, R-PREC default ruling on `interaction`); the channel consumer and the exception queue are `RWB-P2-E2034-APP`; the timeline and the case record section are `RWB-P3-E2034-APP`; the partner portal is the S9 slice. This story builds no screen, no consumer, no workflow and no ledger table.
- **Unchanged from the legacy story:** the 404 `MSG-P4-003` of a case outside the reader's scope (legacy AC11), the 403 `MSG-P4-002` of a role without Case record R (legacy exception X8), the contact point kept as a reference and masked by role (BR5, REQ-ILG-014), the mask holding whatever the screen (FEAT-ACA-05), and the access log written as a decision record (FEAT-ACA-07, FEAT-ACA-08).
- **Data, not code:** the roles, the permission matrix, the masking rows and the role conflicts are rows of `rwb_access`; LOV-SCOPE and LOV-CAPABILITY come through the reference-data contract (DP-07). No role code, scope name, capability area, field ID or version string is a constant.

### 2. Business rationale

Contact outcomes from collections, letters sent through WIN and work held by partners sit in different systems today, so a case owner who picks up a case does not know which number answered or who held it last; the measure of the whole legacy key is the share of open cases whose last right-party contact is visible on the case, today zero for cases that came from EFS. The ledger and its channels answer the "what happened" half of that measure. This story answers the half that decides whether the ledger may be read at all and in what form: the right, the scope and the mask (REQ-ILG-012, REQ-ILG-014), and the record of who read it (FEAT-ACA-07, FEAT-ACA-08).

The risk it removes is concrete. A ledger entry carries a contact point — the reference behind which a phone number or an address sits — and CTL-11 and REQ-ILG-014 require that reference and never the value, masked by role. Without one owner of that decision, each screen that shows the ledger masks by its own rule, an export masks nothing, an agent reads whatever its prompt happens to include, and no log can say who looked at which entry: NFR-039 and NFR-040 ask for masking at rest and in use and for the minimum data per screen and per agent, NFR-042 for every read to be logged, and NFR-051 for an agent to pass the same role checks as a person.

The measure is the one the module reports — rule and limit changes made without a code release, at 100 percent, because the roles, the matrix version and the masking rows are data — plus two facts an audit can check: every ledger read is answered with a mask the policy in force names, and every read of it leaves one `AC-READ` entry naming the case and the masked field IDs.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E1037-CON, in force from wave 1 | The service contract on `/api/recovery/access/v1`: the authorise decision element, the caller's resolved session and the access-log read, with `role`, `permission` and `masking_rule` already in `rwb_access`. This story implements the decision behind the element for the ledger and adds no operation |
| RWB-P2-E2034-CON is baselined | The shape of one ledger entry as the channel intake publishes it: `eventCode`, `channel`, `direction`, `sourceSystem`, `contactKey`, `fromHolderRef`, `toHolderRef`, the field IDs behind them and the fakes. This is the only cross-service shape the answer is asked about |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03), written in the same transaction as the answer |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and contract carrying LOV-SCOPE and LOV-CAPABILITY with the version in force (DP-07); `lov_value` stays P3's |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and contract (DP-06): the access-log page default and maximum and the batch limit of field IDs per answer are parameter rows, whose names are Not specified in the source documents (GAP-2321; ASM-3860) |
| RWB-PLT-TE006-CON | The outbox and inbox library that publishes the access event of DP-09 in the answer's transaction |
| RWB-PLT-E1044-CON | The per-service Flyway sequence in `rwb_access` (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route that serves SCR-03 and SCR-04 (DP-19); the route and the screens are P3's |

Business preconditions carried from the legacy story:

- Permission matrix version `PM-2026.12` is in force and gives CASE_RECORD right R to RW-CASEOWN, RW-TEAMMGR, RW-CONDUCT and RW-AUDIT, and no CASE_RECORD right to RW-REFADM (FSD P4 A2.4; TSD P4 T6.1). The default scope of each role is the `role.default_scope` row in force.
- Masking version `MASK-SIT-01` is in force. That this label is the masking version of SIT is Not specified in the source documents (GAP-2321; ASM-3856).
- The personal fields of a ledger entry that the mask covers are `DF-INT-011` summary and `DF-INT-022` contact point, with `DF-ACE-076` and `DF-ACE-077` behind them. Which field IDs of the entry the policy covers is Not specified in the source documents (GAP-2321; ASM-3857).
- The ledger of the case holds its entries (rwb-source-data); a case with no entry is normal and shows the empty state of RWB-P3-E2034-APP, not an error here.
- The caller signed in through Entra ID with multi-factor authentication and holds at least one Recovery role; with no role the answer is 401 `MSG-P4-001` (FSD P4 A2.1, A2.2).
- The database login is the rwb-access login (DP-02); its name is Not specified in the source documents (GAP-2321; ASM-3861).
- Assumption (GAP-2184): every event code takes retention class ILG-STD, the two link columns are uuid, and an append whose event code has no class row is refused with 422; these hold until reference data of DP-07 publishes the class list (sections 7, 11, 12.1).
- Assumption (GAP-2225): the element names, paths and field shapes of the interaction item, the append command and the intake result follow RWB-P2-E2034-CON and the Logical Data Model field IDs, to be confirmed at contract review.
- The platform contracts named above are pulled by the wave-1 access stories, so this secondary slice adds no build dependency of its own (metadata H = None) and builds on Day 1 against `RWB-P2-E2034-CON` and the fixtures of section 12.8.

### 4. Flow

1. Caller: a person opens SCR-03 Case record or SCR-04 Case timeline; gateway-bff resolves the session and `rwb-case` asks `rwb-access` for the ledger of the case, naming the case, the area `CASE_RECORD`, the right `R` and the field IDs of the entries on the page.
2. `rwb-access`: resolves the caller's roles from the session and the rights from `permission` for the matrix version in force, `PM-2026.12`; reads `role`, `permission`, `masking_rule` and `role_conflict` from `rwb_access` only (BR9).
3. `rwb-access`, right check: no CASE_RECORD R for any role of the caller gives 403 with `MSG-P4-002` naming the action and no case data (BR1), and one `AC-DENY` entry.
4. `rwb-access`, scope check: the case is admitted when its attributes satisfy the caller's `default_scope` in force read through DP-07 — OWN for a case the caller owns, TEAM for a case of the caller's team, REGION for its region, ALL for any case (BR2). A case outside it is answered 404 with `MSG-P4-003` and no case data, so the answer never confirms that the case exists, and one `AC-DENY` entry is written.
5. `rwb-access`, mask: for each field ID asked, the profile is read from `masking_rule` for the roles the caller holds and the masking version in force; with no covering row the field is `masked` (BR4). The channel of the entry is not an input: an entry from EFS, from the Workbench and from the partner portal is answered with the same markers (BR3).
6. `rwb-access`: writes one `AC-READ` decision record through the library of DP-03 with the case ID, the field IDs asked and their markers under the version used, then returns the answer — granted, with the scope and the version — inside the 2 s budget of DP-11 (BR5). Nothing is returned before the record commits; a failure answers 503 `MSG-P7-003` and raises an incident.
7. Caller: `rwb-case` applies the markers to each entry of the page and renders it; a field marked `masked` is rendered masked whatever the screen, the export or the agent call (BR3).
8. Agent: a service identity reads the same ledger for the same case and is answered by the same decision under its own roles; the `AC-READ` entry carries the agent's actor reference (BR8).
9. Repeat: the same ask under the same policy versions is answered from the cached decision, and that read still writes its own `AC-READ` entry (BR7).
10. Policy change: a new matrix or masking version is approved on the load path, the rows are written by that path, and the cache is dropped on the commit that writes them; the next ask is answered under the new version with no deployment (BR7).
11. Audit: `RW-PLATADM` calls `GET /api/recovery/access/v1/admin/access-log` with the user, the event `AC-READ`, from and to, and reads one row per ledger read with the case ID, the field IDs and their markers (BR6).

Screen states of SCR-03 Case record and SCR-04 Case timeline that this service answers: granted, with the markers under the version used. The no access, error, empty and loading states are Not specified in the source documents (CG-ALL-5371; CG-ALL-5372); the empty state of the ledger is the screen's and is carried by RWB-P3-E2034-APP.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The case is outside the caller's scope | 404 with no case data; one `AC-DENY` entry naming the area and the right and no case ID | MSG-P4-003 | AC4, TC-E2-034-11 |
| X2 | No role of the caller holds Case record R | Refused before any case fact is read: 403, no field marker | MSG-P4-002 | AC5, TC-E2-034-12 |
| X3 | No masking row covers a field ID | The field is marked `masked` with the default marker; the read is otherwise granted | None | AC1, AC3 |
| X4 | The reference list of scope or capability is not available | No answer rather than a guessed one: 503; the refusal is recorded | MSG-GEN-006 | AC10, AC13, TC-E2-034-16, TC-E2-034-19 |
| X5 | The decision record cannot be written | Nothing is returned: 503 with no case data, and an incident is raised to the platform administrator queue | MSG-P7-003 | AC8, TC-E2-034-07 |
| X6 | The token carries no Recovery role, or no second factor | No answer is given: 401 before the policy is read; one refusal entry with the reason | MSG-P4-001 | BR1, AC7 |
| X7 | Two roles of the caller conflict, for example RW-SECADM with a business role | The session is refused at sign-in from the `role_conflict` rows; no ledger ask is made | MSG-P4-006 | AC11, TC-E2-034-17 |
| X8 | An agent or service identity holds no role | Refused 401; no ledger data and no marker | MSG-P4-001 | AC7 |
| X9 | The page size of the access-log read is out of bounded range | 422 naming the field and its bounds, before any row is read | MSG-GEN-002 | AC12, AC14, TC-E2-034-18, TC-E2-034-21 |

A masking version that changes mid-day for the same case, and the version the answer then names, are Not specified in the source documents (GAP-2321; ASM-3856); until they are, the answer uses the version whose `valid_from` is the latest on or before the business date and names it, so a caller can never mistake a stale marker for a current one.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds and tests against `RWB-P2-E2034-CON` and the wave-1 access contract; reads its own schema only and calls no other service at run time |
| Negotiable | The policy pack — roles, matrix version, masking rows and their versions — is data; the story fixes the shape of the answer and the refusal behaviour only |
| Valuable | The ledger is readable by the roles entitled to it, masked by role on every channel and every screen, and every read is in the access log |
| Estimable | One decision behind an existing operation, one cache, one decision-record path, one admin read and one index |
| Small | Fits one sprint with its tests; no screen, no consumer, no ledger table and no workflow |
| Testable | Every owned criterion has a test case in section 16; the entry shape is a published fake |

### 7. Acceptance criteria

```gherkin
Feature: Interaction ledger on the case and from every channel

  Background:
    Given open case "RW-2026-000301" with account "ACC-SYN-0301", held by "U-2001" in team "MTG-BKK"
    Given permission matrix version "PM-2026.12" is in force and gives CASE_RECORD right "R" to RW-CASEOWN, RW-TEAMMGR, RW-CONDUCT and RW-AUDIT, and no CASE_RECORD right to RW-REFADM
    Given the default scope in force is "OWN" for RW-CASEOWN, "TEAM" for RW-TEAMMGR and "ALL" for RW-AUDIT
    Given masking version "MASK-SIT-01" is in force and holds unmasked "false" for DF-INT-011 and DF-INT-022 for RW-CASEOWN, RW-TEAMMGR, RW-CONDUCT and RW-AUDIT
    Given the rwb-integration contract mock returns the ledger entry shape of "RW-2026-000301" with field IDs DF-INT-011 and DF-INT-022 and the three entries of 14, 15 and 18 December 2026

  Scenario: AC1 A granted ledger read answers with the field markers (new, D-RCV-60)
    Given test user "U-2001" holds RW-CASEOWN and owns case "RW-2026-000301"
    When the caller asks POST /api/recovery/access/v1/authorise for case "RW-2026-000301", area "CASE_RECORD", right "R" and field IDs DF-INT-011 and DF-INT-022
    Then the answer is granted with scope "OWN" under matrix version "PM-2026.12"
    Then DF-INT-011 and DF-INT-022 are marked "masked" under masking version "MASK-SIT-01"
    Then one AC-READ decision record is written with the case ID and the two field IDs marked "masked"
    Then the answer carries no contact key value, no summary text, no number and no address

  Scenario: AC2 Every channel of one case gets one answer (new, D-RCV-60)
    Given the ledger of "RW-2026-000301" holds a CONTACT entry with source EFS and channel CALL of 14 December 2026 10:15, a CONTACT entry with source WORKBENCH and channel CALL of 15 December 2026 09:30, and a PARTNER_RESULT entry with source WORKBENCH and channel PORTAL of 18 December 2026 16:00
    Given test user "U-2001" holds RW-CASEOWN and owns case "RW-2026-000301"
    When the caller asks once for the case, the area "CASE_RECORD", the right "R" and the field IDs of the three entries
    Then one answer is returned with the same markers for the three entries
    Then the channel EFS, CALL, PORTAL and the source of an entry change no marker, and the answer names the masking version it used
    Then the contact point of the entry of 15 December 2026 stays the reference "PHONE:CP-SYN-0301-M" and no number and no address appears in the answer

  Scenario: AC3 A field with an unmasked row comes back clear and the rest stays masked (new, D-RCV-60)
    Given masking version "MASK-SIT-01" holds unmasked "true" for DF-INT-011 for RW-AUDIT and no row for DF-INT-022 for RW-AUDIT
    Given test user "U-3005" holds RW-AUDIT with default scope "ALL"
    When "U-3005" asks for case "RW-2026-000301", area "CASE_RECORD", right "R" and field IDs DF-INT-011 and DF-INT-022
    Then the answer is granted with scope "ALL"
    Then DF-INT-011 is marked "clear" and DF-INT-022 is marked "masked"
    Then one AC-READ entry names DF-INT-011 as "clear" and DF-INT-022 as "masked" under "MASK-SIT-01"

  Scenario: AC4 A case outside the reader's scope is not found (new, D-RCV-60)
    Given case "RW-2026-000301" is owned by "U-2002" in team "MTG-BKK"
    Given test user "U-3001" holds RW-CASEOWN with default scope "OWN" in team "HP-NE"
    When "U-3001" reads the ledger of case "RW-2026-000301"
    Then the response is 404 with message MSG-P4-003
    Then no entry, no case number and no contact reference is returned, and no marker is named
    Then one AC-DENY entry is written with area "CASE_RECORD" and right "R" and it carries no case ID

  Scenario: AC5 A role without Case record R is refused (new, D-RCV-60)
    Given test user "U-3002" holds only RW-REFADM, whose Case record letter is "-" in "PM-2026.12"
    When "U-3002" reads the ledger of case "RW-2026-000301"
    Then the response is 403 with message MSG-P4-002 with action "read the ledger of this case"
    Then no entry and no field marker is returned
    Then one AC-DENY entry is written with area "CASE_RECORD" and right "R" and it carries no case ID

  Scenario: AC6 The access log answers who read which ledger (new, D-RCV-60)
    Given two granted ledger reads of case "RW-2026-000301" by "U-2001" on 15 December 2026 at 09:30 and 10:00
    Given test user "U-4001" holds RW-PLATADM with Platform administration right "R"
    When "U-4001" calls GET /api/recovery/access/v1/admin/access-log with user "U-2001", event "AC-READ", from 15 December 2026 00:00 and to 15 December 2026 23:59
    Then the page holds one row per read with the case ID DF-INT-011 and DF-INT-022 and their markers
    Then no row holds a contact key value, a summary text, a number or an address
    When test user "U-3002" holding only RW-REFADM calls the same read
    Then the call is refused with status 403 and message MSG-P4-002 with action "read the access log"

  Scenario: AC7 An agent reads the ledger under the same decision (new, D-RCV-60)
    Given the service identity SY-AGENT holds RW-CASEOWN for case "RW-2026-000301"
    When SY-AGENT asks for the ledger of case "RW-2026-000301", area "CASE_RECORD", right "R" and field IDs DF-INT-011 and DF-INT-022
    Then the answer carries the same markers as the answer to "U-2001" under the same versions
    Then one AC-READ entry names the agent's actor reference instead of a person
    When a service identity with no Recovery role asks for the same ledger
    Then the answer is 401 with message MSG-P4-001 and no entry and no marker is returned

  Scenario: AC8 An answer that cannot be recorded is not given (new, D-RCV-60)
    Given the decision-record library is unavailable
    When "U-2001" reads the ledger of case "RW-2026-000301"
    Then the response is 503 with message MSG-P7-003
    Then no marker, no scope and no case data is returned
    Then an incident is raised to the platform administrator queue and no AC-READ entry exists for that read

  Scenario: AC9 A new masking version changes the answer with no deployment (new, D-RCV-60)
    Given test user "U-2001" holds RW-CASEOWN and DF-INT-022 is marked "masked" for it under "MASK-SIT-01"
    When masking version "MASK-SIT-02" is approved on the load path and holds unmasked "true" for DF-INT-022 for RW-CASEOWN
    Then the next ask for case "RW-2026-000301" marks DF-INT-022 "clear" under "MASK-SIT-02" with no deployment
    Then the AC-READ entries written before the change still name "MASK-SIT-01"
    Then a mask that no row of the new version covers comes back "masked"

  Scenario: AC10 A ledger read is refused when a reference list is not available (new, D-RCV-60)
    Given the reference-data contract of DP-07 cannot return the scope list of LOV-SCOPE
    When "U-2001" reads the ledger of case "RW-2026-000301" with area "CASE_RECORD", right "R" and field IDs DF-INT-011 and DF-INT-022
    Then the response is 503 with message MSG-GEN-006
    Then no marker, no scope and no case data is returned
    Then one AC-DENY entry is written with area "CASE_RECORD" and right "R" and it carries no case ID

  Scenario: AC11 Two conflicting roles of one caller are refused at sign-in (new, D-RCV-60)
    Given the role_conflict rows of rwb_access hold a conflict between RW-SECADM and RW-CASEOWN
    Given test user "U-2001" holds RW-CASEOWN and additionally RW-SECADM
    When "U-2001" signs in with both roles
    Then the session is refused at sign-in with message MSG-P4-006 naming both roles
    Then no ledger ask is made and no AC-READ entry exists

  Scenario: AC12 A page size out of bounds is refused before any row is read (new, D-RCV-60)
    Given test user "U-4001" holds RW-PLATADM with Platform administration right "R"
    When "U-4001" calls GET /api/recovery/access/v1/admin/access-log with a page size outside its bounds
    Then the response is 422 with message MSG-GEN-002 naming the field and its bounds
    Then no row is read

  Scenario: AC13 A ledger read is refused when the capability reference list is not available (new, D-RCV-60)
    Given the reference-data contract of DP-07 cannot return the capability reference list
    When "U-2001" reads the ledger of case "RW-2026-000301" with area "CASE_RECORD", right "R" and field IDs DF-INT-011 and DF-INT-022
    Then the response is 503 with message MSG-GEN-006
    Then no marker, no scope and no case data is returned
    Then one AC-DENY entry is written with area "CASE_RECORD" and right "R" and it carries no case ID

  Scenario: AC14 A page size at its bound is answered and one just outside it is refused (new, D-RCV-60)
    Given test user "U-4001" holds RW-PLATADM with Platform administration right "R"
    When "U-4001" calls GET /api/recovery/access/v1/admin/access-log with a page size at its lower bound
    Then the page is answered with rows within the bound
    When "U-4001" calls GET /api/recovery/access/v1/admin/access-log with a page size one above its upper bound
    Then the response is 422 with message MSG-GEN-002 naming the field and its bounds
    Then no row is read

  Scenario: AC15 A role scope or version change in rwb_access takes effect with no deployment (new, D-RCV-60)
    Given test user "U-3005" holds RW-AUDIT with default scope "ALL" under matrix version "PM-2026.12"
    When the permission data of rwb_access changes the default scope of RW-AUDIT under a new matrix version and "U-3005" asks for case "RW-2026-000301" with area "CASE_RECORD", right "R" and field IDs DF-INT-011 and DF-INT-022
    Then the answer is given under the new matrix version with no deployment
```

AC1 to AC15 are the criteria this story owns; it owns no legacy criterion. The legacy AC1 to AC11 and the access row TC-E2-034-12 are carried by the slices named in section 19, and AC11 — a case outside the reader's scope is refused with `MSG-P4-003` — is stated here as AC4 with the legacy values unchanged, because the scope answer of the ledger read is this slice's. In AC1 and AC2 the assertions that belong to this service are the markers and the version they come from; the entries, their order and their text are P1's and P3's. AC2 proves that neither the channel nor the source of an entry is an input to the mask: the role is. AC3 proves that a covering row is what makes a field clear, not the screen. AC4 and AC5 prove the two refusals of the legacy story, each also as the entry the audit reads. AC6 turns the access log into an answer, which is what makes FEAT-ACA-16 real for this key. AC7 proves NFR-051 for the ledger, AC8 that a read is never unlogged, and AC9 that the mask follows the version in force without a release.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The right comes from the permission matrix version in force; a caller whose roles hold no Case record R is refused 403 `MSG-P4-002` with no case data and one `AC-DENY` entry | FSD P4 A2.4 VR-P4-004-1; TSD P4 T6.1; FEAT-ACA-04 |
| BR2 | A case is admitted when its attributes satisfy the caller's `default_scope` in force — OWN, TEAM, REGION or ALL; a case outside it is answered 404 `MSG-P4-003` with no case data and one `AC-DENY` entry | FSD P4 A2.14; LOV-SCOPE; legacy AC11 |
| BR3 | The mask depends on the role, the field ID and the masking version only: the channel, the source and the screen of an entry change no marker, so the same field is masked on SCR-03, SCR-04, an export and an agent call | FEAT-ACA-05; NFR-040; legacy BR5 |
| BR4 | A field is marked `masked` unless a `masking_rule` row for a role the caller holds and that field says unmasked true for the masking version in force; with no covering row the field is masked | FSD P4 A2.5 AC-EXC-P4-004-05; NFR-039; legacy BR6 |
| BR5 | Every granted ledger read writes one `AC-READ` decision record with the case ID, the field IDs and their markers under the version used, before the answer is returned; one read is one entry (GAP-2321; ASM-3858) | FSD P4 A2.7 AC-P4-007-01; FEAT-ACA-07; FEAT-ACA-08 |
| BR6 | Every refusal writes one `AC-DENY` decision record with the area and the right and no case ID, and the access-log read returns both codes to a role holding Platform administration R, within its page bounds | FSD P4 A2.7 AC-EXC-P4-007-04, A2.16; FEAT-ACA-16 |
| BR7 | The answer is cached per policy version and the cache is dropped on the commit that writes a new matrix or masking version, so a policy change takes effect with no deployment; the answer names the version it used, so a stale marker is detectable | FSD P4 AC-P4-004-01; DP-11; TSD P4 T3.2 |
| BR8 | Role codes, scope values, capability areas, field IDs and every version are data read from `rwb_access` and the reference lists; an agent or service identity is decided by the same checks as a person and its read is logged with its actor reference (GAP-2321; ASM-3862) | FSD P4 BR-P4-004, BR-P4-005; NFR-051; principle 1 |
| BR9 | The answer is built from the request and from `rwb_access`: no `interaction`, `recovery_case`, notice, instruction, treatment or proceeds row and no `v_ace_*` view is read, and the entry's values never enter this service | DP-01; DP-05; DP-18 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 is a read of `permission` for the caller's roles and the `matrix_version` in force; the letters C, R, U, D and A are the five-character field of TSD P4 T3.1, and the answer names the version it used.
- BR2 is `ScopeRule`, comparing the attributes of the request with the `default_scope` value read through DP-07; the four scope names are list values, never Java constants, and the attribute set of the request is Not specified in the source documents (GAP-2321; ASM-3859).
- BR3 is the reason the request carries no channel and no source as decision inputs: they travel with the entry for display, and a marker that differed by channel would be a defect of this answer, not of the screen.
- BR4 is a read of `masking_rule` by `field_id`, `role_code` and `masking_version`; the answer carries markers, never values, so no personal data crosses the boundary in either direction (NFR-039).
- BR5 and BR6 are one transaction as the answer: the record is written first, the answer is returned after it commits, and a failure answers 503 with `MSG-P7-003` and changes nothing.
- BR7 is a cache keyed by the matrix and masking versions; the load path writes the new rows and drops it, and no answer is served under a version it does not name.
- BR8 is visible in the code review: no role code, scope name, capability area, field ID or version string appears in a constant.
- BR9 is the reason there is no ledger repository here: the service holds `role`, `permission`, `masking_rule`, `role_conflict`, the decision record and the outbox, and nothing else.

### 9. State transitions

None. This story changes no case status and no ledger entry: the ledger is append-only and belongs to `rwb-source-data`, the timeline and the case are `rwb-case`'s, and the story runs no workflow of its own. The only states it has are the states of its answer:

| Answer state | When | What the caller gets | Record written |
|---|---|---|---|
| Granted | The caller holds Case record R and the case is in scope | The scope, the masking version and a `masked` or `clear` marker per field ID | `AC-READ` |
| Refused, no right | No role of the caller holds Case record R | 403 `MSG-P4-002`, no case data | `AC-DENY` |
| Not found | The caller holds the right and the case is outside the scope | 404 `MSG-P4-003`, no case data | `AC-DENY` |
| Not answered | The record cannot be written, or a list the answer needs is unavailable | 503, no case data | None; the failure is raised as an incident |

The policy versions are not states of this story: a version is loaded, approved and put in force by the load path, and this story only reads the version in force.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Case record R with default scope OWN: reads the ledger of a case it owns, with the personal fields masked |
| RW-TEAMMGR, team manager | Case record R with default scope TEAM: reads the ledger of a case of its team |
| RW-CONDUCT, conduct and QA officer | Case record R with the role default scope: reads the ledger within that scope |
| RW-AUDIT, internal audit | Case record R with default scope ALL: reads any ledger; a field is clear only where a masking row says so |
| RW-REFADM and every role with no Case record R | Refused with `MSG-P4-002`; no entry and no marker is returned |
| RW-PLATADM, platform administrator | Reads the access log through `GET /admin/access-log` with Platform administration R, scope applied |
| RW-SECADM, security administrator | Approves the permission matrix and masking versions through the load path stories; this story reads the versions in force |
| RW-COMPLY, Compliance and PDPA officer | Reads which masking version is in force and which fields it covers; this story writes no value on their behalf |
| SY-AGENT and the other service identities | Ask the same question for their own reads; the roles of a service identity are checked as a person's are and its read is logged |

Reading is the whole of this story: it grants or refuses a read and writes the record of it. It changes no case, no entry and no policy row; a policy row changes only through the load path stories of this service, and the break-glass grant, its incident reference and its four-hour ceiling stay with the wave-1 stories of the access service.

### 11. Data

| BR Field ID | Table in rwb_access | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read |
| DF-REF-198 to DF-REF-204 | `masking_rule` | id, role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read |
| DF-REF-205 to DF-REF-211 | `role_conflict` | id, role_code, conflicts_with, reason, conflict_version, valid_from, valid_to | Read (the sign-in check, X7) |
| DF-REF-027 to DF-REF-033 | `lov_value` | LOV-SCOPE and LOV-CAPABILITY values, read through the reference-data contract of DP-07 | Read through the contract; the table is P3's |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the `AC-READ` and `AC-DENY` entries: code, actor, area, right, case ID, actions, decided at | Write |
| (outbox) | outbox table in `rwb_access` | the decision-record row of the answer | Write |
| (inbox) | `processed_event` | present in the schema; this story consumes no event and writes none | Not used |

The field IDs the answer marks — `DF-INT-011` summary and `DF-INT-022` contact point, with `DF-ACE-076` and `DF-ACE-077` behind them — appear in `masking_rule.field_id` and in the answer as identifiers only. The entry itself, its contact key, its summary, its holder references and the values of the ACE views stay with their owners and are never copied, read or logged here: the answer is markers, identifiers and version labels (NFR-039, NFR-040, DP-18). Field IDs are those of the Logical Data Model and Data Dictionary v9.

Which field IDs of an entry the policy covers, and whether the mask applies to the summary as it does to the contact point, are Not specified in the source documents (GAP-2321; ASM-3857).

### 12. Contract

#### 12.1 REST operations provided

None new in this story. The operations are those of the service contract in force from wave 1 (RWB-P4-E1037-CON) on base `/api/recovery/access/v1`, owner rwb-access (P4), unchanged in path, request, response and error shape:

| Method | Path | What this story decides or serves | Access |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | The right, the scope and the `masked`/`clear` marker per field ID for the ledger of one case; 401 (MSG-P4-001), 403 (MSG-P4-002), 404 (MSG-P4-003), 503 (MSG-P7-003) | The session's roles; the answer is the check |
| GET | `/api/recovery/access/v1/admin/access-log` | The `AC-READ` and `AC-DENY` rows of ledger reads by user, event, from, to, page and size | Platform administration R, scope applied |

The Ownership Map rows of this service are the four administration operations — `GET /admin/access-log`, `GET /admin/roles`, `GET /me/session` and `POST /admin/break-glass-grants`; the authorise element is the guard contract of RWB-P4-E1037-CON on the same base and the sibling stories of this run consume it at the path above (GAP-2321; ASM-3859). `GET /admin/roles`, `GET /me/session` and `POST /admin/break-glass-grants` are other stories' and are not used here.

#### 12.2 REST operations consumed

None. The entry shape arrives in the request — the field IDs, the case and the identifiers — so this story calls no service at run time and holds no ledger read. The shape it expects is the one `RWB-P2-E2034-CON` declares; that contract is used as a fake in the tests (12.8) and as the alignment reference in the build.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | PLT library; consumed by P7 | case ID where there is one, else the actor reference | the hash-chained `AC-READ` or `AC-DENY` record: code, actor, area, right, case ID, field IDs with markers, decided at |

CloudEvents 1.0 envelope, published by the library of DP-03 in the transaction of the answer. The payload carries no personal value: the `AC-READ` record carries field IDs and markers, the `AC-DENY` record the area and the right only. No event is published on `rwb.access.events.v1`: the ownership row of this service lists no event of its own, so the policy change is a commit in this service and not an event of this slice.

#### 12.4 Events consumed

None. The policy versions are written by this service's load path and read from `rwb_access`; the story holds no inbox row and subscribes to no topic.

#### 12.5 Workflows and activities

None. The answer is served inside the request and the record is written in the same transaction; this story registers no workflow and no activity on `rwb-access`.

#### 12.6 Schedules

None. No Schedule and no Quartz row. JOB-18, the six-monthly access review list, is a Temporal Schedule of this service and its story is RWB-P4-AD008-APP.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | The caller's roles, their class and their `default_scope` |
| `permission` | P4 (`rwb_access`) | The CASE_RECORD right and the `matrix_version` in force |
| `masking_rule` | P4 (`rwb_access`) | The `masked` or `clear` marker per role, field and masking version |
| `role_conflict` | P4 (`rwb_access`) | The conflicting role pairs the sign-in check reads |
| `delegation_limit` | P4 (`rwb_access`) | Not read here; it is the delegation slice's |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | The outbox row of the access event; no inbox row and no stored answer in this story |
| `lov_value`, `reference_row`, `reference_version` | P3 (`rwb_case`) | LOV-SCOPE and LOV-CAPABILITY read through the contract; not owned here |

`interaction`, its append-only trigger and its indexes are `rwb-source-data`'s and appear nowhere as an object of this contract (DP-18); `recovery_case`, `notice`, `instruction`, `treatment` and `proceeds` are never read (DP-01), and no foreign key crosses a schema.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-integration contract fake | RWB-P2-E2034-CON | The entry shape of "RW-2026-000301": field IDs DF-INT-011 and DF-INT-022, the three entries of 14, 15 and 18 December 2026, contact key "PHONE:CP-SYN-0301-M", and the six event and channel codes |
| decision-record fake | RWB-PLT-E1027-CON | The `AC-READ` and `AC-DENY` write and the publish on `rwb.decision-record.v1`, including the forced failure of X5 |
| policy pack fixture | RWB-P4-E1037-CON | Matrix PM-2026.12 and masking versions MASK-SIT-01 and MASK-SIT-02 with the roles, scopes and masking rows of the background and of AC3 and AC9, and the role conflict of X7 |
| reference-data fake | RWB-P3-E1043-CON | LOV-SCOPE and LOV-CAPABILITY with the version in force, and the unavailable list of X4 |
| parameters fake | RWB-P3-E1042-CON | The access-log page default and maximum and the batch limit of field IDs |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 0 new (1 existing decision operation implemented and 1 existing admin read served), consumed 0 | Base `/api/recovery/access/v1`; the entry shape arrives in the request |
| Kafka | Published 1 decision record; consumed 0 | `rwb.decision-record.v1`; no event on `rwb.access.events.v1` |
| Temporal | None | No workflow, activity or Schedule on `rwb-access` |
| File | None | No file input or output, and no export here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/ledgeraccess`, Java package `th.co.scb.ace.workbench.recovery.access.ledgeraccess`, extending the authorise module behind RWB-P4-E1037-CON.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | ACE data through rwb-source-data or the owner's views; this slice reads neither and answers with markers | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library — this service is its owner | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library, CloudEvents, the owner's topic | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/access/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in `rwb_access` | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data; the answer is asked about its entry shape | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 is the shape of the answer: `interaction` and every case, notice, instruction, treatment and proceeds row belong to their owners, so the decision is built from identifiers in the request and from `rwb_access`, never from a joined query. DP-03 is the access log: an `AC-READ` and an `AC-DENY` are decision records on `rwb.decision-record.v1`, so an access question and a decision question are answered from one log. DP-05 is a statement: the contact value and the ACE view behind it stay with `rwb-source-data`, so this service answers with field IDs and markers. DP-06 supplies the page bounds of the access-log read and the batch limit of field IDs, whose names are Not specified in the source documents (GAP-2321; ASM-3860); DP-07 supplies LOV-SCOPE and LOV-CAPABILITY with the version in force, because `lov_value` stays with P3. DP-08 is the contract this story implements: the guard library of the callers and the decision of this service are one contract, so a caller and an owner cannot disagree about a marker. DP-09 is the outbox row of the access event and nothing else, since the ownership row of this service lists no event; DP-10 is a statement that no job of this key runs from a shared Quartz table and JOB-18 is RWB-P4-AD008-APP. DP-11 is the caller-facing boundary — one hop, 2 s, cached — and DP-13, DP-15 and DP-18 are the naming, migration and ownership conventions of the service. DP-19 is the route the screens arrive through; the screens are P3's.

The platform contracts the DP rows name are preconditions of the service lane already in place behind RWB-P4-E1037-CON in wave 1, so metadata H is None and this secondary slice is Day 1 (ASM-3859).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| LedgerAccessController | Controller | The authorise element and the access-log read on the existing base; validation and problem responses |
| LedgerAccessDecisionService | Service | Right, scope and marker per field, in that order; one answer, one record |
| PermissionResolver | Service | Reads `permission` for the caller's roles and the `matrix_version` in force |
| ScopeRule | Service | Compares the case attributes of the request with the `default_scope` in force |
| LedgerMaskService | Service | The `masked` or `clear` marker per field ID for the caller's roles and the masking version in force; default masked |
| AccessRecordWriter | Service | The `AC-READ` and `AC-DENY` entries through DP-03, written before the answer commits |
| AccessLogQuery | Service | The paged `AC-READ` and `AC-DENY` rows by user, event, from and to, bounded by the parameter rows |
| PolicyCache | Service | The cached answer per policy version, dropped on the commit that writes a new version |
| AccessRepository | Repository | `role`, `permission`, `masking_rule`, `role_conflict` and the outbox in `rwb_access`; no foreign table |

**Database and migrations.** No new table: `role`, `permission`, `masking_rule` and `role_conflict` exist from the wave-1 stories behind RWB-P4-E1037-CON, and the policy rows are loaded by the load path. One migration in the per-service Flyway sequence of DP-15: `V2034_1__ledger_access_read_path.sql` adds `ix_masking_rule_role_field` on `masking_rule (role_code, field_id, masking_version)` and `ix_permission_role_area` on `permission (role_id, capability_area, matrix_version)`, so the two reads of an answer are index reads inside the 2 s budget. No ledger table, column or index is created here (DP-18).

**Configuration and reference data.** The matrix version and the masking version in force are data: the latest `valid_from` on or before the business date. The access-log page default and maximum and the batch limit of field IDs per answer are parameter rows through DP-06 (GAP-2321; ASM-3860). LOV-SCOPE and LOV-CAPABILITY come through DP-07. No role code, scope name, capability area, field ID, version string or timeout constant sits in code; the 2 s is the platform standard of the guard client.

**Build steps**

1. `PermissionResolver` and `ScopeRule` over `permission`, `role` and the reference lists, with the matrix version named in the answer; tests for AC1, AC4 and AC5.
2. `LedgerMaskService` with the covering-row lookup, the default masked and the channel-independent answer; tests for AC1, AC2 and AC3.
3. `AccessRecordWriter` with the `AC-READ` and `AC-DENY` entries written before the answer, and the forced failure of X5; tests for AC4, AC5 and AC8.
4. `AccessLogQuery` and the admin read with the page bounds and the refusal of X9; tests for AC6.
5. The agent and service-identity path with its own actor reference and the 401 of X8; test AC7.
6. `PolicyCache` and the drop on the commit that writes a new version; test AC9 against the MASK-SIT-02 fixture.
7. The migration of the two indexes, and a timing test that one answer stays inside the 2 s budget on a policy pack of the loaded size.
8. The contract-fake run of the whole capability against the `RWB-P2-E2034-CON` entry shape and the decision-record fake, so the story builds before the ledger side exists in the environment.

**Feature switch.** `rwb.p4.ledger-access`, read from the platform feature-flag library under the R-PREC default ruling. Off: the ledger read is answered by the case record answer alone (the matrix right, the scope and the mask of the case fields), the ledger field IDs are answered `masked` for every role and the access-log write is unchanged — so nothing becomes readable that a policy did not already allow, and the story's other behaviour is untouched. The switch needs no schema rollback.

**Done when.** The tests in section 16 pass; a case owned by the caller is answered with its field markers and the version used; a case outside the scope is answered 404 with no case data; a role without Case record R is answered 403; an entry from EFS, from the Workbench and from the portal gets the same markers; a field with no covering row comes back masked; every granted and every refused read leaves its record; the access log answers who read which ledger; and a newly approved masking version changes the answer with no deployment.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The token carries no Recovery role, or no second factor | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. | The access check before this story's answer (X6, X8) |
| MSG-P4-002 | No role of the caller holds the right in the capability area | You cannot {action} here. Your role does not include it. | This story, on the refusal of BR1 and on the access-log read of BR6 (X2, AC6) |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. | This story, on the refusal of BR2 (X1) |
| MSG-P4-006 | Two roles of the caller conflict | {role} may not be held together with {role}. | The access check, from this service's `role_conflict` rows (X7) |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on every answer (X5) |
| MSG-GEN-006 | A list the answer needs is not available | {system} is not available. Try again in a few minutes. | This story, on a reference-list failure (X4) |
| MSG-GEN-002 | The page size of the access-log read is out of bounds | {field} must be between {min} and {max}. | This story, on the admin read (X9) |

For `MSG-P4-002` the {action} value is the action the caller attempted, for example "read the ledger of this case" or "read the access log"; for `MSG-P4-003` no case fact is echoed, because the message must not confirm that a case exists. Every error is an RFC 9457 problem response with `messageId`, the text with its placeholders filled and the instance of the request; the Thai text follows DL10 (open decision; assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863). `MSG-P3-024`, the empty state of the ledger, is the screen's and is carried by RWB-P3-E2034-APP.

### 15. Screens and states

This story builds no screen. SCR-03 Case record and SCR-04 Case timeline, with their ledger section, filters and empty state, are RWB-P3-E2034-APP's through the gateway-bff composite route of DP-19; the access-log read serves the platform administration view of RWB-P4-E1039-APP, whose fields and layout are that story's.

What this story decides for those screens is what each state may show:

| Screen | State | What the answer decides |
|---|---|---|
| SCR-03 Case record, SCR-04 Case timeline | Granted | The ledger entries of the page are rendered; a field this story marks `masked` is rendered masked and a field marked `clear` is the only one shown in full, whatever the screen |
| SCR-03, SCR-04 | Entry from EFS, WORKBENCH or PORTAL | The same markers: the channel and the source of an entry change nothing on the screen |
| SCR-03, SCR-04 | Refused | The page shows `MSG-P4-002` and no entry and no case fact, and one `AC-DENY` entry exists |
| SCR-03, SCR-04 | Not found | The page shows `MSG-P4-003` and no entry and no case fact, and one `AC-DENY` entry exists |
| SCR-03, SCR-04 | Not available | The page shows `MSG-P7-003` where the record could not be written, and no entry |
| SCR-03 Case record | Empty, loading, error, no access | Not specified in the source documents (CG-ALL-5371) |
| SCR-04 Case timeline | Empty, loading, error, no access | Not specified in the source documents (CG-ALL-5372) |

A screen that renders a field clear because a client cached it is a defect of the screen, not of the answer: the answer always names the masking version it used, and a field is clear only where a row of that version says so.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-034-12 | AC5, BR1 | Component | RW-REFADM reads the ledger of "RW-2026-000301"; refused 403 with MSG-P4-002, no marker returned, one AC-DENY |
| TC-E2-034-01 | AC1, AC2, BR3, BR4, BR5 | Component | One EFS action row with a promise of 12,500.00 for 20 December 2026 and one Workbench call of 15 December 2026 09:30 to "PHONE:CP-SYN-0301-M" with NO_ANSWER; the answer for their field IDs |
| TC-E2-034-02 | AC2, BR3 | Component | One transfer from "U-2001" to "U-2002" on 16 December 2026 11:00 and one instruction "INS-SYN-0301" to partner "LF-SYN-01" of 17 December 2026 14:00: the holder change and the PORTAL entry carry the same markers as the CALL entries |
| TC-E2-034-03 | AC2, AC6, BR3, BR6 | Component | From EFS, WORKBENCH and the partner portal on 14, 15 and 18 December 2026: one answer, then one access-log row per read naming the case and the markers |
| TC-E2-034-04 | AC2, BR3 | Component | Notice "NT-SYN-0301" with barcode "EV000000001TH", treatment "TRT-SYN-0301" and proceeds "PRC-SYN-0301" of 5,000.00: the LETTER, OFFER and PAYMENT entries carry the same markers |
| TC-E2-034-05 | AC1, AC6, BR7 | Contract | Two identical asks under "PM-2026.12" and "MASK-SIT-01": the same answer from the cached decision and one AC-READ row per read |
| TC-E2-034-06 | AC1, BR9 | Component | Three EFS rows of 14 December 2026, listed, unlisted and on no open case: the answer for the listed entry is the same as for any other and this service reads no EFS row |
| TC-E2-034-07 | AC8, BR5 | NFR | The decision-record write forced to fail during a granted read: 503 with MSG-P7-003, no marker, no AC-READ, incident raised |
| TC-E2-034-08 | AC4, BR2 | Component | InstructionIssued for a case that does not exist, and a case outside the scope: 404 with MSG-P4-003 and one AC-DENY with no case ID |
| TC-E2-034-09 | AC1, AC2, BR3 | Component | The EFS row of contact time 14 December 2026 10:15 written on 15 December 2026 at 10:00 after the call of 09:30: both entries are decided the same and neither gains a marker of its own |
| TC-E2-034-10 | AC1, BR6 | Component | Case "RW-2026-000302" with no entry: the ask for the case alone is granted and one AC-READ names the case and no field; the empty state is the screen's |
| TC-E2-034-11 | AC4, AC7 | End to end | Case "RW-2026-000301" owned by "U-2002" in team "MTG-BKK" read by "U-3001" of "HP-NE" with Own scope: 404 and MSG-P4-003, no ledger read; then the same case read by SY-AGENT in scope, with the same markers |
| TC-E2-034-13 | AC3 | Component | U-3005 holds RW-AUDIT with scope ALL; MASK-SIT-01 holds unmasked true for DF-INT-011 for RW-AUDIT and no row for DF-INT-022 for RW-AUDIT; ask for case "RW-2026-000301" with DF-INT-011 and DF-INT-022: granted, DF-INT-011 clear, DF-INT-022 masked, one AC-READ naming both |
| TC-E2-034-14 | AC9 | Component | U-2001 holds RW-CASEOWN and DF-INT-022 is masked under MASK-SIT-01; MASK-SIT-02 is approved on the load path with unmasked true for DF-INT-022 for RW-CASEOWN; the next ask for "RW-2026-000301" marks DF-INT-022 clear under MASK-SIT-02 with no deployment, and earlier AC-READ rows still name MASK-SIT-01 |
| TC-E2-034-15 | Not specified in the source documents (DOR-RWB-P4-E2034-APP-12) | Component | Not specified in the source documents (DOR-RWB-P4-E2034-APP-12) |
| TC-E2-034-16 | AC10, BR8 | Component | Scope list of LOV-SCOPE not available through DP-07 for "U-2001" reading case "RW-2026-000301": 503 with MSG-GEN-006, no marker, one AC-DENY with no case ID |
| TC-E2-034-17 | AC11, BR8 | Component | U-2001 holds RW-CASEOWN and RW-SECADM, a conflict in role_conflict: refused at sign-in with MSG-P4-006 naming both roles, no ledger read, no AC-READ |
| TC-E2-034-18 | AC12, BR6 | Component | U-4001 holds RW-PLATADM and calls the access-log read with a page size outside its bounds: 422 with MSG-GEN-002, no row read |
| TC-E2-034-19 | AC13, BR8 | Component | Capability reference list not available through DP-07 for "U-2001" reading case "RW-2026-000301": 503 with MSG-GEN-006, no marker, one AC-DENY with no case ID |
| TC-E2-034-21 | AC14, BR6 | Component | U-4001 holds RW-PLATADM: access-log read at the lower page bound is answered; one above the upper bound: 422 with MSG-GEN-002, no row read |
| TC-E2-034-22 | AC15, BR8 | Component | RW-AUDIT default scope changed in rwb_access under a new matrix version: the next ask for RW-2026-000301 is answered under that version with no deployment |

The legacy level System maps to Component where the ledger side is stubbed by `RWB-P2-E2034-CON` and to End to end where the composite route is exercised; Access maps to Component. All twelve legacy test case IDs are kept in the legacy order, with the leg each row runs named in its Covers; the rows whose ledger, transport or partner assertion belongs to another slice are kept as regression evidence and are proved end to end by RWB-ITG-E2034-ITG, so no `-ITG` copy sits in this story. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: role codes, scope values, capability areas, field IDs, the matrix version, the masking version and the page bounds are data rows in `rwb_access` and list values read through DP-07; the switch is a platform flag (BR8).
- No personal data in logs, events, the record or the tests: the answer carries markers, the `AC-READ` entry carries field IDs and markers, the `AC-DENY` entry carries the area and the right, and the event carries version labels; test data is synthetic and staff appear as user references.
- ACE data only through its owner: the contact value and the `v_ace_*` views stay with `rwb-source-data`, and this service stores and returns no customer value (DP-05, DP-18, NFR-039, NFR-040).
- No cross-schema read (DP-01): `interaction`, `recovery_case`, `notice`, `instruction`, `treatment`, `proceeds` and the ACE views are never queried; the case arrives as attributes of the request and the policy is the service's own.
- The record is written before the answer: a failure answers 503 with no case data and raises an incident, so no ledger read is unlogged (BR5, BR6).
- One writer for the policy: only the load path stories of this service write a role, a permission or a masking row; this story reads them, so an answer and the policy it names cannot disagree.
- The answer is idempotent for a policy version and the mask never widens with the channel: the same question under the same versions returns the same markers, and the cache is dropped on the commit that writes a new version.
- The feature switch changes one rule and no schema, and it never widens a mask: off answers the ledger field IDs masked for every role and leaves every other decision as it was.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ILG-009 | Contact outcomes from collections reach the ledger | Business Requirements Epic 2, section 3.2 | FEAT-ILG-06 | 06 to 10 Recovery case processes | BR3, BR9 | TC-E2-034-01, TC-E2-034-06 |
| REQ-ILG-010 | Dispatched letters write their result, including proof of delivery | Business Requirements Epic 2, section 3.2 | FEAT-ILG-07 | 06 to 10 Recovery case processes | BR3 | TC-E2-034-04 |
| REQ-ILG-011 | A hand-over names who held the case, who holds it now and when | Business Requirements Epic 2, section 3.2 | FEAT-ILG-08 | 06 to 10 Recovery case processes | BR3 | TC-E2-034-02 |
| REQ-ILG-012 | The case record view shows the ledger as an ordered timeline | Business Requirements Epic 2, section 3.2 | FEAT-ILG-09 | 06 to 10 Recovery case processes | BR1, BR2, BR3 | TC-E2-034-03, TC-E2-034-10, TC-E2-034-11 |
| REQ-ILG-013 | Ledger entries carry their own retention class | Business Requirements Epic 2, section 3.2 | FEAT-ILG-10 | All recovery processes | BR9 | TC-E2-034-01 |
| REQ-ILG-014 | Personal data in the ledger is masked by role on the case record rules | Business Requirements Epic 2, section 3.2 | FEAT-ILG-06 | 06 to 10 Recovery case processes | BR3, BR4 | TC-E2-034-01, TC-E2-034-11, TC-E2-034-12, TC-E2-034-13, TC-E2-034-15 |
| REQ-ILG-007 | One entry per key; a repeat is ignored and counted | Business Requirements Epic 2, section 3.2 | FEAT-ILG-06 | 06 to 10 Recovery case processes | BR5, BR7 | TC-E2-034-05 |
| REQ-ILG-008 | A failed ledger write loses no entry and the delivery is retried | Business Requirements Epic 2, section 3.2 | FEAT-ILG-07 | 06 to 10 Recovery case processes | BR5 | TC-E2-034-07 |
| REQ-ILG-006 | The timeline orders entries by occurred time and case sequence | Business Requirements Epic 2, section 3.2 | FEAT-ILG-09 | 06 to 10 Recovery case processes | BR3, BR7 | TC-E2-034-03, TC-E2-034-09 |

| Legacy reference | Where it is kept |
|---|---|
| The refusal of a role without Case record R and the not-in-scope answer (legacy exception X8, AC11) | Sections 4, 5, 7, 14 (AC4, AC5) |
| The contact point as a reference, never a number or an address (legacy BR5, REQ-ILG-014) | Sections 7, 8, 11, 17 |
| The mask holding whatever the screen, and the default masked (FSD P4 A2.5) | Sections 4, 7, 8, 15 (AC2, AC3) |
| The access log of a read and of a refusal (FEAT-ACA-07, FEAT-ACA-08, FEAT-ACA-16) | Sections 4, 7, 8, 12.3 (AC6, AC8) |
| Rules R-UNI-40, CTL-11, NFR-039, NFR-040, NFR-042, NFR-051 | Sections 2, 8, 17, 18 |
| Matrix version PM-2026.12, masking versions MASK-SIT-01 and MASK-SIT-02, roles RW-CASEOWN, RW-TEAMMGR, RW-CONDUCT, RW-AUDIT, RW-REFADM, RW-PLATADM | Background, AC1 to AC9, sections 3 and 10 |
| Legacy key RWB-E2-034, story RWB-P4-E2034-APP, contract RWB-P2-E2034-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The `interaction` table, its columns, its append-only trigger, its indexes, the append, the case-scoped interaction read, the EFS intake rule, the outcome list, the retention classes and the intake summary: the rwb-source-data stories of this legacy key (DP-18).
- The channel consumer, the mapper, the delivery states, the retry, the three-attempt exception rule and SCR-09: RWB-P2-E2034-APP, RWB-P2-E2034-CON and its deployment story.
- The timeline, the case-scoped read composition, the ledger section of SCR-03, the filters and empty state of SCR-04: RWB-P3-E2034-APP and RWB-P3-E2016-APP.
- The partner portal, the partner result and the instruction: the S9 slice of this key; the notice, the payment and the offer: the P6, P8 and S2 stories.
- Loading, approving and rolling back the policy pack: the reference-load and approval path of RWB-P4-AD002-APP, RWB-P4-AD004-APP and RWB-P4-AD010-APP, and the administration screens of Epic 8.
- Break-glass access, its incident reference, its ceiling and its review; the access review list of JOB-18 (RWB-P4-AD008-APP); the role list and session operations `GET /admin/roles` and `GET /me/session`.
- The delegation of authority table and its lookup (RWB-P4-E2013-APP), the case record view (RWB-P4-E1023-APP) and the other access decisions of the case record view (RWB-P4-E2015-APP).
- The gateway-bff composite route itself, the Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (RWB-PLT-N001-CON and an OPS story of this key).
- The real cross-service proof of the whole legacy key: RWB-ITG-E2034-ITG.
