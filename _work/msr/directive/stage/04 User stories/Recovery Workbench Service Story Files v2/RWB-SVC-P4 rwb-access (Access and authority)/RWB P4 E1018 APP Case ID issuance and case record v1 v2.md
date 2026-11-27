# RWB-P4-E1018-APP Case ID issuance and case record v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E1018-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Size | Not specified in the source documents (DOR-RWB-P4-E1018-APP-16); the squad sizes it at refinement |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P4-O |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E1018-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-CWC-001, REQ-CWC-002, REQ-CWC-003, REQ-CWC-004, REQ-CWC-005, REQ-CWC-016, REQ-CHO-004) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the case-authority slice of RWB-E1-018 for rwb-access, split from the case service that issues the case number, so that whether a caller may cause a case to be created, read the case record or allocate and transfer the case is answered only from the role-to-permission matrix, the scope and the masking rows of this service. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E1018-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 29 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **security administrator (RW-SECADM), a case owner (RW-CASEOWN), a team manager (RW-TEAMMGR), a compliance and PDPA officer (RW-COMPLY) and rwb-case itself**, I want **the case-record authority of rwb-access answered behind the two existing operations `POST /api/recovery/access/v1/authorise` and `GET /api/recovery/access/v1/me/permissions` — whether a caller may cause a case to be created (Case record C), read the case record (Case record R) or allocate and transfer it (Queue and allocation R/U), with default deny, the letters read from the role-to-permission matrix at the version in force, the scope OWN, TEAM, REGION or ALL applied to the case facts the caller presents one hop from rwb-case, 403 MSG-P4-002 and 404 MSG-P4-003, and a `masked` or `clear` marker per personal field ID of the case record under the masking version in force — recorded as an access entry through the local decision-record library**, so that **every creation, read, allocation and transfer of a case is decided from data by the service that owns the policy, the case number grants nothing of itself, and rwb-access holds no case row and no ACE row to decide it with**.

Inside `rwb-access` this is the case-authority slice:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access`, Java package `th.co.scb.ace.workbench.recovery.access`.
- The case number RW-YYYY-NNNNNN is issued by rwb-case (RWB-P3-E1018-APP) and formatted, sequenced and validated there. This service never issues it, never formats it, never validates it and never parses it, and it is never an authority token: a request that carries a plausible case number and nothing else is refused exactly as a request with no number is.
- The case facts arrive in the request from rwb-case, one hop, inside the 2 s budget (DP-11): the case reference, the owner reference, the queue, the team, the region and the field IDs whose masking the caller asks about. This service reads no case table, no `v_ace_*` view and no `public` table at any step (DP-01, DP-05).
- The policy it reads is its own: `role`, `permission` and `masking_rule` in `rwb_access` (DP-07 applies through the reference-data contract but no list value is written in this story's code), and the answer is written as an access entry through the local decision-record library (DP-03).
- The database login used by the capability is the per-service login of DP-02. Its name is Not specified in the source documents (GAP-0982; ASM-1719); the story names it "the rwb-access login (DP-02)" and never the shared monolith login.

The legacy facts this slice keeps are the authority facts of RWB-E1-018: a role without Case record R is refused with 403 and MSG-P4-002 (legacy AC14), and a case outside the reader's scope answers 404 with MSG-P4-003 (legacy §14). Everything that creates, numbers, excludes, groups or cancels a case is another slice of the same legacy key.

### 2. Business rationale

Legacy RWB-E1-018 built one case per customer and product, gave it a number in the form RW-YYYY-NNNNNN issued once and never reused, and let every role with Case record R read it inside its scope (REQ-CWC-001 to REQ-CWC-005, REQ-CWC-016, REQ-CHO-004). The authority half of that story is the half that survives the move to 19 services unchanged in intent but not in shape: in the monolith the read endpoints of `recovery.casewf` called the access check in process, and the case record, the permission matrix and the masking rows all sat in one schema. In the target, rwb-case owns the case, the sequence, the entry and exclusion rules, the case tables and the case endpoints, and rwb-access owns the policy: roles, the role-to-permission matrix, scope, the masking rows and the delegation of authority table (Architecture v5 slides 14 and 41).

Three things follow, and this story is all three:

1. **The decision moves to the policy owner and stays one hop.** rwb-case presents the case facts it holds and asks `POST /authorise` for the area and the right; the answer is a decision, the right, the scope applied, the matrix version, the masking version and a marker per field ID. Nothing of the case is copied into `rwb_access` and nothing of the policy is copied into `rwb_case`.
2. **The case number is a name, not a permission.** The number is the identity of the case and the thing every letter and document carries; it cannot also be an authority token, or a caller who can guess or read a number would hold authority over the case. This slice therefore treats the number as an opaque string it neither parses nor validates: the creation, read, allocation and transfer answers depend on the letters, the scope and the case facts only.
3. **A policy change needs no release.** The letters, the scope rule and the masking rows are data with versions; the matrix version and the masking version in force are read on every call, so a change approved on the load path takes effect on the next call with no deployment (REQ-ACA-002, REQ-ACA-003, REQ-ACA-005, REQ-ACA-007, REQ-ACA-009; FSD P4 A2.4, A2.11, A2.14 and A2.30).

This story is the rwb-access part of legacy RWB-E1-018 and a secondary slice of it. The case, its numbering, the sequence, the yearly range, the entry and exclusion rules and the case tables stay with rwb-case (RWB-P3-E1018-APP and RWB-P3-E1018-CON); the ACE read behind the entry and exclusion decisions stays with rwb-source-data; the document binding of the case stays with rwb-document (RWB-P5-E1018-APP); the decision record of a case creation and the central ledger stay with rwb-decision (RWB-P7-E1018-APP); and the end-to-end proof across the four services is RWB-ITG-E1018-ITG. This slice delivers the authority question behind the two existing operations, its refusals, its scope and its masking markers, and nothing else.

The request and answer field names of the authorise operation, the source of the caller's team and region membership and the roster of case-record personal field IDs are Not specified in the source documents (GAP-0982; ASM-1719), (GAP-0982; ASM-1720) and (GAP-0982; ASM-1721). The story fixes the shape, the membership source and the two field IDs of the case record it answers for, and leaves every business value in a data row.

### 3. Preconditions

- RWB-P4-E1037-APP delivered the `rwb_access` baseline: the tables `role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit` exist with their dictionary rows (DF-REF-034 to DF-REF-044, DF-REF-198 to DF-REF-204), and RWB-P4-E1037-CON published the authorise operation this story answers behind.
- RWB-P3-E1018-CON is published: the rwb-case contract with its case read and its case facts, the error envelope, the not-found and out-of-scope answers and the fake (DP-11). This service consumes none of it at run time; the shape of the case facts a caller presents is stubbed from it, so the two services agree before either is live.
- The permission matrix version `PM-2026.12` is in force in `permission`, with a `CASE_RECORD` row and a `QUEUE_AND_ALLOCATION` row for every role the tests use (FSD P4 AC-P4-004-01). Whether `PM-2026.12` is the label in force at the release date is Not specified in the source documents (GAP-0982; ASM-1719); the story reads the version in force and names the label its tests use.
- The masking version `MASK-SIT-01` is in force in `masking_rule`, with rows for the case-record personal field IDs `DF-PTY-007` and `DF-PTY-016` (FSD P4 A2.5 AC-ALT-P4-005-01 and A2.7 AC-P4-007-01). That `MASK-SIT-01` is the masking version of the environment is Not specified in the source documents (GAP-0982; ASM-1721).
- The load path of this service that prepares, approves and verifies a policy pack is RWB-P4-AD002-APP and RWB-P4-AD004-APP; this story reads the versions in force and writes no policy row of its own.
- The caller's teams and regions are resolved at sign-in and carried with the call (RWB-P4-E1022-APP). Where that membership is held is Not specified in the source documents (GAP-0982; ASM-1720); this service holds no team table and no region table, because `queue` and `queue_member` are rwb-case's.
- The local decision-record library and the shared topic `rwb.decision-record.v1` are live (DP-03, EV-08), so the access entry of an answer is written before the answer leaves.
- The login is the rwb-access login (DP-02). The per-service login name is Not specified in the source documents (GAP-0982; ASM-1719).
- The 30 `recovery.v_ace_*` views and the `public` schema exist and are owned by ACE; this service holds no privilege on either (DP-02, DP-05), which RWB-P4-E1069-APP asserts for its own login and this story asserts again for the two schemas it must not reach.

### 4. Flow

1. rwb-case is about to create a case, read a case record, place a case on a queue or transfer one, and calls `POST /api/recovery/access/v1/authorise` with the caller identity from the session, the capability area (`CASE_RECORD` or `QUEUE_AND_ALLOCATION`), the right (`C`, `R` or `U`), the case reference, the case facts it holds (owner, queue, team, region) and the field IDs whose masking a screen or an agent needs (DP-08, DP-11, one hop, 2 s).
2. rwb-access: resolves the caller's roles from the session and reads the permission rows of that area for those roles at the matrix version in force from `permission`, with the role rows from `role` for the default scope; no role code, area or letter is written in code (BR1, BR2, BR11).
3. rwb-access: unions the letters of every role the caller holds. An empty union, a missing role or a missing row is a refusal: nothing is allowed by default and nothing is allowed because a row is absent (BR1).
4. rwb-access: where the right is absent from the union, answers 403 with MSG-P4-002 before any case fact is examined, and writes the refusal entry (BR2, BR12).
5. rwb-access: applies the scope. `OWN` allows the case whose owner is the caller; `TEAM` allows the case whose team is one of the caller's teams; `REGION` allows the case whose region is one of the caller's regions; `ALL` allows any case; a case that no scope of the caller covers is answered 404 with MSG-P4-003, which is the same answer as a case that does not exist (BR3, BR4).
6. rwb-access: resolves the masking marker of each field ID of the request from `masking_rule` at the masking version in force: `clear` only where a row for a role the caller holds, that field ID and that version says `unmasked` true, and `masked` otherwise, including where no row exists (BR5).
7. rwb-access: composes the answer — the decision code (`AC-READ` or `AC-DENY`), the area, the right, the roles that carry the letter, the scope that was applied, the matrix version, the masking version, a marker per field ID and the `messageId` of a refusal. The answer carries no case fact of its own, no value, clear or masked, and no part of the case number (BR7, BR8).
8. rwb-access: writes the access entry through the local decision-record library first, in the same transaction as the answer: decision code, actor, case reference, area, right, scope applied, matrix version, masking version, the field IDs and their markers, and the time. The entry carries no name, no identity number, no address and no case fact (BR6, BR9).
9. rwb-access: the library publishes `rwb.decision-record.DecisionRecorded.v1` (EV-08) on `rwb.decision-record.v1` through its outbox; this story adds no event and no topic of its own (BR9).
10. rwb-case: acts on the answer — creates the case only on an allowed `C`, returns the case only on an allowed `R`, runs the transfer only on an allowed `U` — and keeps every case row itself.
11. rwb-access: a policy pack load commits a later matrix version or a later masking version, and the load path publishes `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1`; the cached decision of the previous version is not served after the change, and the next call answers under the version now in force without a deployment (BR8).
12. A screen or an agent that needs the markers of a case-record read asks `GET /api/recovery/access/v1/me/permissions` for the caller's roles, default scope, matrix version and masking version, and the per-field markers come back inside the authorise answer of the read.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The caller holds no Workbench role at all | Refused before any matrix row is read; no case fact examined | MSG-P4-001 | AC1 |
| X2 | The area or the right is absent for every role of the caller, or the role has no row for the area | 403 before any case fact is examined; one refusal entry written | MSG-P4-002 | AC1, AC4 |
| X3 | The case exists but no scope of the caller covers it | 404, the same answer as a case that does not exist; no owner, queue, team, region or status is answered | MSG-P4-003 | AC2, AC3 |
| X4 | The case reference in the request is unknown to rwb-case | 404 with MSG-P4-003; the answer is indistinguishable from X3, so a caller cannot probe for the existence of a case | MSG-P4-003 | AC2 |
| X5 | The request carries no case reference for a right that needs one | 422 with the required field named; no matrix row is read and no entry is written | MSG-GEN-001 | AC2 |
| X6 | The case number in the request is well formed but the caller has no letter | 403 with MSG-P4-002: the number grants nothing, and the refusal is the same as with any other number | MSG-P4-002 | AC8 |
| X7 | The case number is malformed, re-used or belongs to a closed case | Treated as an opaque string: the decision depends on the letters, the scope and the case facts, never on the number | None | AC8 |
| X8 | No `masking_rule` row covers a personal field ID at the version in force | The field is answered `masked` and a pack gap is raised; the decision itself is unchanged | None | AC6 |
| X9 | The access entry cannot be written | 503 and no answer: no decision, no scope, no marker and no version is returned; an incident is raised | MSG-P7-003 | AC1, AC8 |
| X10 | A class of the package or a statement of the authorise path names `rwb_case.recovery_case`, another service's schema, a `v_ace_*` view or a `public` table | The build fails on the fixture class and the container test fails on the statement; nothing merges | Build log | AC7 |
| X11 | A later matrix or masking version is committed on the load path | The cached answer of the earlier version is dropped; the next call answers under the version now in force | None | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the `rwb_access` baseline and the RWB-P4-E1037-CON fake, with the case facts stubbed from RWB-P3-E1018-CON; the policy pack load, the session and the case service are other stories |
| Negotiable | The letters, the default scope, the masking rows and the version labels are data rows; the story fixes the decision rule, the scope rule and the answer shape only |
| Valuable | One place answers whether a case may be created, read, allocated or transferred, from data, with the case number powerless and the policy changeable without a release |
| Estimable | One resolver for the letters, one for the scope, one for the markers, one repository, one controller contribution and one entry writer |
| Small | Fits one sprint with its tests, as a secondary slice of the legacy key |
| Testable | Every criterion in section 7 is one automated test over the policy fixture; no ACE data and no case row is needed |

### 7. Acceptance criteria

```gherkin
Feature: Case ID issuance and case record v1 — the case authority of rwb-access

  Background:
    Given permission matrix version "PM-2026.12" is in force in "permission"
    Given masking version "MASK-SIT-01" is in force in "masking_rule"
    Given case "RW-2026-000123" is owned by "CO-0201", sits on queue "TDR-BKK-CO" with team "TDR-BKK" and region "BKK"
    Given the case number is an opaque string that this service neither formats, validates nor parses

  Scenario: AC1 Case record C allows the creation request and no C refuses it (new, D-RCV-60)
    Given permission matrix version "PM-2026.12" holds CASE_RECORD letters "CRU" for role "RW-CASEOWN" and "-" for role "RW-REFADM"
    When rwb-case asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "C" and the case facts of a new case for borrower "P-0101" and product group "HIRE_PURCHASE"
    Then the answer is allowed, with area "CASE_RECORD", right "C", the role "RW-CASEOWN", the scope applied and matrix version "PM-2026.12"
    Then one access entry is written with decision code "AC-READ", area "CASE_RECORD", right "C" and matrix version "PM-2026.12"
    When a caller holding only "RW-REFADM" asks for the same creation
    Then the answer is refused with status 403 and message MSG-P4-002, before any case fact is examined
    Then no case fact is answered and one access entry holds decision code "AC-DENY", area "CASE_RECORD", right "C" and result "REFUSED"

  Scenario: AC2 Case record R with scope OWN returns the owned case and 404 for another's (new, D-RCV-60)
    Given role "RW-CASEOWN" holds CASE_RECORD letters "R" and default scope "OWN"
    When the caller whose actor is "CO-0201" asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R" and the case facts of "RW-2026-000123"
    Then the answer is allowed with right "R", the scope applied "OWN" and matrix version "PM-2026.12"
    When the same caller asks for the case facts of "RW-2026-000456", owned by "CO-0299"
    Then the answer is status 404 with message MSG-P4-003
    Then the answer carries no owner, no queue, no team, no region, no status and no case number
    Then a case reference rwb-case does not return answers the same 404 with MSG-P4-003
    Then one access entry is written for the refused read with the area, the right, the scope applied and result "REFUSED"

  Scenario: AC3 TEAM, REGION and ALL scopes are applied to the case facts of the request (new, D-RCV-60)
    Given role "RW-TEAMMGR" holds CASE_RECORD letters "R" and default scope "TEAM", and the caller's teams are "TDR-BKK" and regions are "BKK"
    When the caller asks for area "CASE_RECORD", right "R" and the case facts of "RW-2026-000123" with team "TDR-BKK"
    Then the answer is allowed with the scope applied "TEAM"
    When the caller asks for the case facts of a case with team "TDR-NE"
    Then the answer is status 404 with message MSG-P4-003
    Given a caller whose roles carry default scope "REGION"
    When the caller asks for a case whose region is "BKK"
    Then the answer is allowed with the scope applied "REGION"
    When the caller asks for a case whose region is "NE"
    Then the answer is status 404 with message MSG-P4-003
    Given a caller whose roles carry default scope "ALL"
    When the caller asks for the case facts of "RW-2026-000123", which another owner and another team hold
    Then the answer is allowed with the scope applied "ALL"
    Then the scope value comes from "role" and never from the request, so a caller cannot widen its own scope

  Scenario: AC4 Queue and allocation U allows a transfer and an R-only role is refused (new, D-RCV-60)
    Given role "RW-TEAMMGR" holds QUEUE_AND_ALLOCATION letters "RU" and role "RW-CASEOWN" holds "R" under "PM-2026.12"
    When the team manager asks POST /api/recovery/access/v1/authorise for area "QUEUE_AND_ALLOCATION", right "U" and the case facts of "RW-2026-000123"
    Then the answer is allowed with area "QUEUE_AND_ALLOCATION", right "U" and matrix version "PM-2026.12"
    When the case owner asks for the same transfer
    Then the answer is refused with status 403 and message MSG-P4-002
    Then the transfer is refused before the handler runs, so the owner and the queue of the case are unchanged
    Then one access entry is written with decision code "AC-DENY", area "QUEUE_AND_ALLOCATION" and right "U"
    When the case owner asks for right "R" of the same area
    Then the answer is allowed with right "R", because the read of the allocation and the change of it are different letters

  Scenario: AC5 A matrix version change takes effect without a deployment (new, D-RCV-60)
    Given matrix version "PM-2026.11" is in force and holds letter "-" for role "RW-LEGAL" in "QUEUE_AND_ALLOCATION"
    When the load path approves matrix version "PM-2026.12" with letter "R" for "RW-LEGAL" in "QUEUE_AND_ALLOCATION", valid from "2026-12-01", and publishes rwb.access.AccessPolicyChanged.v1
    Then the next authorise by a caller holding "RW-LEGAL" for area "QUEUE_AND_ALLOCATION", right "R" is allowed and names matrix version "PM-2026.12"
    Then the service is not restarted and no deployment is made
    Then no answer taken under "PM-2026.11" is served after the change, and the entry of the new answer names "PM-2026.12"

  Scenario: AC6 The masking markers for the personal fields of the case record (new, D-RCV-60)
    Given masking version "MASK-SIT-01" holds unmasked "false" for "DF-PTY-007" and "DF-PTY-016" for roles "RW-CASEOWN", "RW-TEAMMGR" and "RW-AUDIT"
    Given masking version "MASK-SIT-01" holds unmasked "true" for "DF-PTY-016" for role "RW-COMPLY"
    When a caller holding "RW-CASEOWN" asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R" and field IDs "DF-PTY-007" and "DF-PTY-016"
    Then the answer marks "DF-PTY-007" and "DF-PTY-016" "masked" under masking version "MASK-SIT-01"
    Then the answer carries no name, no identity number, no address and no rendering of either field
    When a caller holding "RW-COMPLY" asks for the same two field IDs
    Then the answer marks "DF-PTY-016" "clear" and "DF-PTY-007" "masked", and still carries no value
    Given no "masking_rule" row covers field "DF-PTY-008" at "MASK-SIT-01" for any role
    When any caller asks for field "DF-PTY-008"
    Then the answer marks it "masked" and raises a pack gap naming the field and the version

  Scenario: AC7 No case-table read, no ACE view and no public read (new, D-RCV-60)
    Given the case facts of a request arrive from rwb-case and rwb-access holds its rows in schema "rwb_access" only
    When a session as the rwb-access login selects from "rwb_case.recovery_case"
    Then the statement fails with SQLSTATE 42501 "permission denied for schema rwb_case"
    When the same session selects from "recovery.v_ace_account" or from "public.customer"
    Then each statement fails with SQLSTATE 42501, and has_table_privilege is false for every view name and for "public"
    Then the authorise path issues statements against "role", "permission" and "masking_rule" in "rwb_access" and writes its access entry, and against nothing else
    When a fixture class of the package names "rwb_case.recovery_case"
    Then the build fails with boundary rule BND-6, the rule RWB-P4-E1069-APP applies to the import boundary of this service
    Then the owner, the queue, the team, the region and the case number reach the decision only through the request

  Scenario: AC8 The case number carries no authority and every answer names the right and the version (new, D-RCV-60)
    Given two authorise requests are identical except that one carries case number "RW-2026-000123" and the other "RW-2026-999999"
    When both are asked for area "CASE_RECORD", right "R" and the same case facts
    Then both answers are identical in decision, scope applied, matrix version and masking version
    Then no prefix "RW-", no year and no six-digit rule appears in the code, and the number is passed through unread
    When the case facts are outside every scope of the caller and the case number is "RW-2026-999999"
    Then the answer is status 404 with message MSG-P4-003, because the letters and the scope decide and the number does not
    Then every answer names the area, the right, the scope applied and matrix version "PM-2026.12", and a refusal names its messageId
    When the access entry cannot be written
    Then the call answers 503 with message MSG-P7-003 and no decision, no scope and no version is returned

  Scenario: AC16 Every business rule of section 8 is held by a criterion or a test case (new, D-RCV-60)
    Given the business rules BR1 to BR12 of section 8
    When the rules are traced to the criteria of section 7 and the test cases of section 16
    Then each rule BR1 to BR12 is named by at least one criterion or one test case
    Then a rule with no criterion and no test case fails the traceability review before the build

  Scenario: AC17 A request with no valid session is answered 401 with no decision (new, D-RCV-60)
    Given a request reaches POST /api/recovery/access/v1/authorise with no session or with an expired session
    When the caller asks for area "CASE_RECORD", right "R" and the case facts of "RW-2026-000123"
    Then the answer is status 401
    Then no decision, no scope applied and no matrix version is returned

  Scenario: AC18 A replay of a write with the same idempotency key returns the first answer and writes no second entry (new, D-RCV-60)
    Given a write request to POST /api/recovery/access/v1/authorise carries an idempotency key and the case facts of "RW-2026-000123"
    When the same request is replayed with the same idempotency key
    Then the replay returns the answer of the first request, with the same decision, the same scope applied and matrix version "PM-2026.12"
    Then no second access entry is written for that idempotency key, and no second decision is taken
```

The eleven criteria above are new and test only this deliverable: the case-record and queue-and-allocation decisions of rwb-access, its scope, its masking markers, its boundary and its powerlessness of the case number. The legacy criteria of RWB-E1-018 are owned elsewhere: AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC11, AC12 and AC15 are the creation, numbering, exclusion and state criteria of rwb-case (RWB-P3-E1018-APP); AC9 and AC13 and the batch gate are the integration slice (RWB-ITG-E1018-ITG); AC10 and the decision-record write are rwb-decision's (RWB-P7-E1018-APP); and AC14, the refusal with MSG-P4-002, is answered here, by AC1 and AC4, and proved end to end in RWB-ITG-E1018-ITG. No legacy criterion text is copied into this story.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The answer is a refusal unless a `permission` row for a role the caller holds, the requested area and the version in force carries the requested letter. A missing role, a missing row, an empty letter set and a `-` letter all refuse; nothing is allowed by default and nothing is allowed because a row is absent | FSD P4 A2.4 VR-P4-004-1; TSD P4 T6.2; REQ-ACA-003; REQ-ACA-007 |
| BR2 | The letters are data: `C`, `R`, `U`, `D` and `A`, or `-` for none, read per role and per capability area at the matrix version in force; the union of the caller's roles applies, and no role code, area or letter is written in Java | FSD P4 A2.4 field catalog; TSD P4 T3.1 (`permission.letters`); TSD P4 T3.2 LOV-CAPABILITY |
| BR3 | The scope is data and comes from `role.default_scope` at the version in force: `OWN` matches the owner of the case, `TEAM` the caller's teams, `REGION` the caller's regions, `ALL` any case. A caller cannot widen its scope in the request, and the widest scope of the roles held applies | FSD P4 A2.14; TSD P4 T3.2 LOV-SCOPE; REQ-ACA-009 |
| BR4 | A case that no scope of the caller covers answers 404 with MSG-P4-003, and an unknown case reference answers the same 404, so the answer reveals neither the existence nor an attribute of a case outside the scope | FSD P4 VR-P4-014-1; AC-EXC-P4-004-01; MSG-P4-003 |
| BR5 | A personal field ID is `clear` only where a `masking_rule` row for a role the caller holds, that field ID and the masking version in force says `unmasked` true; otherwise it is `masked`, including where no row exists, and a missing row raises a pack gap and never opens a field | FSD P4 A2.5; AC-EXC-P4-004-05; NFR-039; REQ-ACA-005 |
| BR6 | The access entry is written first, in the same transaction as the answer, through the local decision-record library, with the area, the right, the scope applied, the versions, the field IDs and the markers only; a failed write answers 503 and no answer is given | FSD P4 A2.7; AC-P4-007-01; AC-EXC-P4-007-03; DP-03 |
| BR7 | The case number is never issued, formatted, validated or parsed here, and it is never an authority token: the decision depends on the letters, the scope and the case facts only, and a well-formed number with no letter is refused | REQ-CWC-002; legacy AC4 and AC11 (the number is rwb-case's); AC8 |
| BR8 | The matrix version and the masking version in force are read on every call from `permission` and `masking_rule`; a version change approved on the load path takes effect on the next call with no deployment, and no answer of the superseded version is served after the change | FSD P4 AC-P4-004-01; TSD P4 T3.2 LOV-VERSION-STATUS; REQ-ACA-002 |
| BR9 | This story adds no event and no topic: the access entry is a library write whose payload is EV-08 on `rwb.decision-record.v1`, published by the library through the outbox, and no topic name is typed in code (the naming library supplies the name) | DP-03; DP-09; DP-14; FSD P4 A2.8 |
| BR10 | rwb-access reads no case table, no `v_ace_*` view, no table in schema `public` and no schema but `rwb_access`; the case facts arrive in the request and the ACE data stays with rwb-source-data | Architecture v5 slides 8, 9 and 41; DP-01; DP-05; ADR-010 |
| BR11 | No business value is written in code: the areas, the letters, the scope values, the field IDs, the role codes and the version labels are data rows read with the version in force | FSD P4 BR-P4-004; TSD P4 T3.2; principle 1 |
| BR12 | The refusal comes before the handler it protects and before any case fact is examined; the caller is told the action and the role, never a case fact, an owner or a number | FSD P4 A2.4 AC-ALT-P4-004-02; MSG-P4-002 |

How the rules hold in `rwb-access`:

- BR1, BR2 and BR11 are executed by `MatrixResolver` and `LetterUnion`: one statement over `permission` and `role` at the version in force, and the union of the letters of the roles the session holds.
- BR3 and BR4 are executed by `ScopeResolver`: it compares the case facts of the request with the caller's own teams and regions and with the actor, and answers the scope applied or the out-of-scope refusal.
- BR5 is executed by `FieldMarkerResolver`: one statement over `masking_rule` per field ID and version, with the no-row default and the pack-gap alert.
- BR6 and BR9 are executed by `AccessEntryWriter`, which writes through the decision-record library before the answer is composed.
- BR7 is executed by the request model itself: the case number is a string field that no class reads, formats or matches.
- BR8 is executed by reading the versions per call and by dropping the cached answer when the load path commits a later version (AC5).
- BR10 is executed by the schema boundary and by the build rule of AC7, and BR12 by the order of the checks in the controller contribution.

Rule coverage by criterion and test case: BR1 by AC1, AC4, TC-E1-018-02 and TC-E1-018-13; BR2 by AC1, AC5 and TC-E1-018-05; BR3 by AC2, AC3, TC-E1-018-03 and TC-E1-018-12; BR4 by AC2, AC3, AC8 and TC-E1-018-15; BR5 by AC6 and TC-E1-018-16; BR6 by AC1, AC8 and TC-E1-018-10; BR7 by AC8 and TC-E1-018-11; BR8 by AC5 and TC-E1-018-14; BR9 by AC1 and TC-E1-018-08; BR10 by AC7, TC-E1-018-17 and TC-E1-018-18; BR11 by AC1, AC5 and TC-E1-018-05; BR12 by AC1, AC4 and TC-E1-018-13.

### 9. State transitions

rwb-access holds no case state machine of its own (TSD P4 T4): the case, its stage, its queue and its owner move in rwb-case, and this story neither reads nor writes them. What moves here is the policy version and, with it, the answer.

| From | Event | Condition | To |
|---|---|---|---|
| a matrix version in force | the load path approves a later version with a later `valid_from` | The pack is approved and carries a later valid-from date | The later version is in force; the previous rows stay readable with their `valid_to`, and the cached answer of the earlier version is dropped |
| a masking version in force | the load path approves a later masking version | The pack is approved and carries a later valid-from date | The later masking version answers the markers; no answer of the earlier version is served after the change |
| a decision made under a version | a later version comes into force | The caller calls again | The answer is taken under the version now in force, and the access entry names it |
| a refusal, a grant, a scope applied | the access entry written | The entry commits | The answer is returned; a failed write leaves no answer at all |

The policy version moves from LOADED to APPROVED to IN_FORCE to SUPERSEDED or ROLLED_BACK on the load path (TSD P4 T3.2 LOV-VERSION-STATUS); this story reads the version in force and writes no policy row.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-access service identity (the rwb-access login, DP-02) | Reads `role`, `permission` and `masking_rule`, answers the case-record and queue-and-allocation decisions and writes the access entry; holds no privilege in `rwb_case`, in `recovery` or in `public` |
| RW-SECADM, security administrator | Approves a matrix version or a masking version on the load path; holds CRUDA in Platform administration (TSD P4 T6.1) |
| RW-REFADM, reference data administrator | Prepares a policy pack file; no approval, no rollback, and no Case record letter of its own, so it is refused on every case right (legacy AC14) |
| RW-COMPLY, Compliance and PDPA officer | Reads which masking version is in force and which field IDs it covers; receives the pack-gap alert |
| RW-AUDIT, internal audit | Reads the access entries and the versions in force |
| RW-CASEOWN, case owner; RW-TEAMMGR, team manager; and every role with Case record R | Read a case record in their scope; the team manager may transfer a case with Queue and allocation U; the case owner may not |
| rwb-case (P3) | Owns the case, the case number, the sequence, the entry and exclusion rules and the case tables; presents the case facts and receives the answer, and copies no policy of this service |
| No approval level from the delegation of authority applies | The story takes no amount-based business decision; the DoA lookup is RWB-P4-E2013-APP |

The per-service login name is Not specified in the source documents (GAP-0982; ASM-1719); the story names it "the rwb-access login (DP-02)" until the platform DB story fixes it. The caller's teams and regions are carried with the call and are not held here; where that membership is held is Not specified in the source documents (GAP-0982; ASM-1720). The roles and areas above are rows of `role` and `permission`; no role grants itself a letter and no role code is fixed in code.

### 11. Data

| BR Field ID | Table in rwb_access | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | `role_code`, `role_name`, `role_class`, `default_scope` | Read (the scope and the role roster) |
| DF-REF-040 to DF-REF-044 | `permission` | `role_id`, `capability_area`, `letters`, `matrix_version` | Read (the letters of the area at the version in force) |
| DF-REF-198 to DF-REF-204 | `masking_rule` | `role_code`, `field_id`, `unmasked`, `masking_version`, `valid_from`, `valid_to` | Read (the marker per field ID and version) |
| DF-DEC-001 to DF-DEC-018 | access entry (local decision record) | decision code, actor, case reference, actions, decided at, hash chain, idempotency key | Write |
| DF-DEC-014 | access entry (local decision record) | actions (area, right, scope applied, roles, matrix version, masking version, field IDs, marker per field ID) | Write |
| DF-DEC-028 to DF-DEC-031 | access entry (local decision record) | the standard record columns of the library entry | Write |
| DF-CAS-001 and DF-CAS-002 | case, through the request of rwb-case (RWB-P3-E1018-CON) | `id`, `case_no` | Received in the request, never read and never written; the number is passed through unread |
| DF-CAS-001 to DF-CAS-023 | case, through the request of rwb-case | the owner, queue, team, region and status facts the scope test needs | Received in the request, never read and never written |

No case row, no ACE row and no other service's row is copied into `rwb_access`: the case facts of a request are held for that request only, are compared with the caller's own teams and regions, and are not persisted. The request and answer field names of the authorise operation, the source of the caller's team and region membership and the roster of case-record personal field IDs are Not specified in the source documents (GAP-0982; ASM-1719), (GAP-0982; ASM-1720) and (GAP-0982; ASM-1721); the story answers for `DF-PTY-007` and `DF-PTY-016` under the masking version in force and holds no dictionary row. Field IDs are those in the Logical Data Model and Data Dictionary v9. DF-REF-039 is kept as a business rule reference only; its Logical Data Model entry is Not specified in the source documents (DOR-RWB-P4-E1018-APP-7).

### 12. Contract

#### 12.1 REST operations provided

None new. The two operations of RWB-P4-E1037-CON on base `/api/recovery/access/v1` are served by this service, and this slice delivers the case-authority part behind them. It adds no path, no query parameter and no response field. The contract that publishes them is RWB-P4-E1037-CON; this story has no contract story of its own and publishes none.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/authorise` | Decide a caller's creation, read, allocation or transfer of a case for a capability area and a right, with the scope applied, the matrix version, the masking version and a marker per field ID | Any authenticated caller with a Workbench role | Idempotent by actor, area, right, case reference, case facts and field list within the cache window |
| GET | `/me/permissions` | The caller's resolved roles, default scope, matrix version and masking version | Authenticated caller, own record only | Not applicable |

Request of `/authorise`: the caller identity from the session, the capability area (`CASE_RECORD` or `QUEUE_AND_ALLOCATION`), the right (`C`, `R` or `U`), the case reference, the case facts (owner, queue, team, region), the field IDs whose masking is asked for and the request key. Answer: the decision code (`AC-READ` or `AC-DENY`), the area, the right, the roles that carry the letter, the scope applied (`OWN`, `TEAM`, `REGION` or `ALL`), the matrix version, the masking version, one marker per field ID (`masked` or `clear`) and the `messageId` of a refusal. The request and answer field names are Not specified in the source documents (GAP-0982; ASM-1719). Errors: 401 no Workbench role (MSG-P4-001), 403 no letter for the area or the right (MSG-P4-002), 404 case absent or out of scope (MSG-P4-003), 422 a required request field missing (MSG-GEN-001), 503 access entry unwritable (MSG-P7-003).

The authorise decision answers no case fact of its own: it answers a decision, a scope, two versions and the markers. The role read, the session read, the access-log search, the DoA read and the policy load paths are P4 surface delivered by other P4 stories (RWB-P4-E1022-APP, RWB-P4-E1039-APP, RWB-P4-E2013-APP, RWB-P4-AD002-APP); this story adds none of them.

#### 12.2 REST operations consumed

None at run time. rwb-access calls no service to decide a case right: the caller's identity and roles arrive in the session, the case facts arrive in the request from rwb-case, and the policy arrives from its own tables. The one-hop and 2 s budget of DP-11 apply to the inbound call. The shape of the case facts is stubbed from RWB-P3-E1018-CON so that rwb-case and rwb-access agree before either is live; that contract is a build dependency, not a run-time call.

#### 12.3 Events published

None. This slice publishes no event of its own and holds no topic of its own: the access entry is a decision-record entry written through the local decision-record library (DP-03), whose payload is EV-08 on `rwb.decision-record.v1` and which the library publishes. The policy events of the service, `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoALimitChanged.v1`, belong to the load path and the DoA story (RWB-P4-AD002-APP, RWB-P4-E2013-APP) and are published there; this slice neither publishes nor consumes them, and its cache is dropped when the load path commits a later version.

#### 12.4 Events consumed

None at run time. The matrix version and the masking version in force are read from `rwb_access` on each call; no topic is consumed here. The cache is dropped when the load path commits a later version, which is the load path's own event (AC5).

#### 12.5 Workflows and activities

None. The decision is a synchronous REST answer in the caller's thread; this story starts no workflow, runs no activity and holds no child workflow. The case lifecycle and its child workflows are rwb-case's.

#### 12.6 Schedules

None. No Temporal Schedule and no job sits in this story. The six-monthly access review list (JOB-18) is RWB-P4-AD008-APP (Architecture v5 slide 44).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `role` | P4 (`rwb_access`) | Recovery roles as data; the default scope and the role roster are read here, no row is written |
| `permission` | P4 (`rwb_access`) | Capability area, letters and matrix version; read here, no row is written |
| `masking_rule` | P4 (`rwb_access`) | Which role sees which personal field unmasked, by masking version; read here, no row is written |
| access entry (local decision record) | P4 rows in `rwb_access`, written through the P7 decision-record library | The `AC-READ` and `AC-DENY` entries with the area, the right, the scope, the versions and the markers (DP-03) |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | Outbox, inbox and idempotency objects (DP-09), written by the library for the decision record |

No table of another service, no `v_ace_*` view and no `public` table is read, and no foreign key crosses a schema (DP-01). `rwb_case.recovery_case`, `case_account`, `case_party` and `case_entry_exclusion` are P3's and are reached only as request facts; `decision_log_entry` is P7's and is reached only through the library and its ledger; `data_product*` and `sys_*` are P1's and are not read.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P4-E1037-CON fake | The authorise and permission operations of this service | A granted creation, a granted read in each scope, a refused letter, an out-of-scope case, an unknown case and a field list with and without rows |
| RWB-P3-E1018-CON fake (build only) | The case facts a caller presents | Case `RW-2026-000123` owned by `CO-0201`, queue `TDR-BKK-CO`, team `TDR-BKK`, region `BKK`; a case of another owner and team; an out-of-scope case; an unknown case |
| policy pack fixture | This story's own test data | The `PM-2026.12` and `PM-2026.11` matrix rows of the roles in the background, the `MASK-SIT-01` rows of `DF-PTY-007`, `DF-PTY-016` and the no-row field `DF-PTY-008` |
| decision-record library stub | DP-03 | A healthy chain and a stopped chain for the 503 path |

The request and answer field names of `/authorise` are stubbed from the published fixture of RWB-P4-E1037-CON; their list is Not specified in the source documents (GAP-0982; ASM-1719).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 new provided, 0 consumed | The case authority is served on the two RWB-P4-E1037-CON operations on `/api/recovery/access/v1`; no path is added and no outbound call is made |
| Kafka | 0 published, 0 consumed | This slice adds no topic; the access entry is a library write whose payload is EV-08 on `rwb.decision-record.v1` |
| Temporal | None | No workflow and no activity |
| File | None | This story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `caseauthority`, Java package `th.co.scb.ace.workbench.recovery.access.caseauthority`. The build rule of AC7 lives in the test source tree of the same service, beside the harness of RWB-P4-E1069-APP.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; no P7 contract, as this slice calls no rule package |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This is a secondary slice and it adds no H dependency of its own: the metadata rows "Depends on (build)" and "Contract dependencies" stay exactly as this Work Package fixes them, and every platform contract library above arrives with the `rwb_access` baseline and the service template. Read one by one:

- DP-01, DP-02 and DP-13 are the target shape itself: schema `rwb_access`, the rwb-access login and the base `/api/recovery/access/v1` replace the shared recovery schema, the shared login and the monolith base, with no new dependency. DP-01 also carries the prohibition: no case table and no other schema is read here.
- DP-03 applies to the access entry: it is a library write first in the transaction, and the library publishes EV-08 on `rwb.decision-record.v1`. The library H dependency is carried by the baseline; this slice adds none.
- DP-04 is carried by the P3 primary slice of this legacy key: rwb-case evaluates the ENTRY and EXCLUSION packages and fetches the versions from rwb-decision. rwb-access evaluates no Drools rule in this slice, holds no KieBase and calls no rule package; the row is listed because the legacy story carries the evaluator and because the primary slice takes the dependency.
- DP-05 applies as a prohibition: no ACE view is read here, and the case facts a decision needs arrive from their owner in the request. The views stay with rwb-source-data.
- DP-06 is carried by the P3 primary slice: the entry threshold `case.entry.dpd` and the other parameters are read by rwb-case. This slice reads no parameter; its own feature switch is the only parameter it takes, and the client library arrives with the baseline.
- DP-07 is the reference-data contract for the capability areas and the scope values; the rows are read as data in `permission` and `role` and the lists arrive through the baseline, so this slice adds no dependency.
- DP-09 is the local library's outbox and adds no topic of its own: the access entry leaves through the library's outbox on `rwb.decision-record.v1`, and this story creates no topic, no producer and no consumer.
- DP-10 is carried by the baseline and the P3 primary slice: rwb-case runs DailyCaseRun on a Schedule and by event, and this story starts no workflow and holds no Schedule.
- DP-11 is the inbound budget: one hop from rwb-case with a 2 s timeout, and the answer in the caller's thread.
- DP-14 is the naming library with no event of its own: no topic name is typed in code, and this slice publishes nothing.
- DP-15 is carried by the baseline: the tables arrive with `rwb_access` and its Flyway sequence, and this story adds no migration and no column, because every value it answers is a data row of the pack.
- DP-19 is the gateway-bff composite route behind SCR-03 Case record and SCR-43 Roles and access; this story builds no screen and adds no route. The empty, error and no-access states of SCR-03 and the empty, loading, error and no-access states of SCR-43 are Not specified in the source documents (DOR-RWB-P4-E1018-APP-10).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `CaseAuthorityControllerPart` | Controller contribution | Wires the resolvers behind `POST /authorise` and `GET /me/permissions` of RWB-P4-E1037-CON; adds no path; orders the refusal before any case fact is examined |
| `MatrixResolver` | Service | Reads the permission rows of the area for the caller's roles at the matrix version in force and returns the role roster with the letters; reads no other schema |
| `LetterUnion` | Service | Unions the letters of every role the caller holds and answers the letter present or absent; `-` and no row mean absent |
| `ScopeResolver` | Service | Compares the case facts of the request with the actor, the caller's teams and the caller's regions, widest scope first, and answers the scope applied or the out-of-scope refusal |
| `FieldMarkerResolver` | Service | Resolves `masked` or `clear` per field ID from `masking_rule` at the masking version in force, with the no-row default |
| `PackGapAlerter` | Service | Raises the pack gap to RW-COMPLY for a personal field ID with no covering row |
| `AccessEntryWriter` | Service | Writes the access entry, first in the transaction, through the decision-record library, with the area, the right, the scope, the versions and the markers |
| `PolicyRepository` | Repository | Reads `role`, `permission` and `masking_rule` in `rwb_access` only; holds the version-in-force queries |
| `AccessModulesRule` | Build rule (test source) | BND-6 over the module map: a class of the package names no case table, no `v_ace_*` view and no `public` table |

**Database and migrations**

- Reads `role`, `permission` and `masking_rule` in schema `rwb_access`; writes the access entry of the decision-record library.
- No migration in this story: the tables and their indexes arrive with the `rwb_access` baseline (RWB-P4-E1037-APP, DP-15) and the rows arrive with the policy pack load (RWB-P4-AD002-APP, RWB-P4-AD004-APP). This story adds no table, no column, no index and no row.
- The version-in-force reads are covered by the baseline indexes on `permission (role_id, capability_area, matrix_version)` and `masking_rule (role_code, field_id, masking_version)`; a missing index is a baseline change and not this story's.
- No case table, no `v_ace_*` object and no `public` object is created, altered, granted or read (DP-01, DP-05, DP-02).
- Schema `rwb_case` is owned by rwb-case (DP-01) and the ACE views by rwb-source-data (ADR-010); both are named in this section only as prohibitions, and this story holds no grant on either.

**Configuration and reference data**

- The matrix version in force: read from `permission` per call; the tests use `PM-2026.12` after `PM-2026.11`. That these are the labels in force at the release date is Not specified in the source documents (GAP-0982; ASM-1719).
- The masking version in force: read from `masking_rule` per call; the tests use `MASK-SIT-01`. The label is Not specified in the source documents (GAP-0982; ASM-1721).
- The capability areas `CASE_RECORD` and `QUEUE_AND_ALLOCATION` and the scope values `OWN`, `TEAM`, `REGION` and `ALL` are list values of LOV-CAPABILITY and LOV-SCOPE; no list value is written in code.
- The authorise request and answer field names are fixed by the fixture until the contract story publishes them (GAP-0982; ASM-1719).
- The caller's teams and regions arrive with the call; this service holds no team table and no region table, because `queue` and `queue_member` are rwb-case's (GAP-0982; ASM-1720).
- The login is the rwb-access login (DP-02): Not specified in the source documents (GAP-0982; ASM-1719).
- The contract fake library version of RWB-P4-E1037-CON: Not specified in the source documents (DOR-RWB-P4-E1018-APP-22).
- The contract version of RWB-P4-E1037-CON that this story builds against: Not specified in the source documents (DOR-RWB-P4-E1018-APP-23); only the `/api/recovery/access/v1` path is fixed here.

**Build steps**

1. `PolicyRepository` and `MatrixResolver` with the version-in-force query and the role roster; tests for AC1 and AC5.
2. `LetterUnion` with the union, the `-` letter and the no-row default, and the refusal ordered before any case fact is read; tests for AC1 and AC4.
3. `ScopeResolver` with `OWN`, `TEAM`, `REGION` and `ALL`, the widest-scope rule, and the same 404 for an out-of-scope and an unknown case; tests for AC2 and AC3.
4. `FieldMarkerResolver` with the per-field marker, the no-row default and the pack-gap alert; test for AC6.
5. `AccessEntryWriter` with the entry first in the transaction and the 503 when the library fails; tests for AC1 and AC8.
6. The request model with the case number as an unread string, and the answer composer with the area, the right, the scope applied, both versions and the messageId; test for AC8.
7. `AccessModulesRule` and the container test over `rwb_case.recovery_case`, a view name and `public.customer`; test for AC7.
8. A contract-fake run of the whole path against the RWB-P3-E1018-CON case facts, so the story builds before rwb-case and the load path are live.

**Feature switch.** `rwb.access.case-authority`, read as a parameter through the parameters contract (DP-06). Off: every case right is refused and every field is answered masked, and the refusal is MSG-P4-002; the switch never opens a right and never widens a scope.

**Done when.** The tests in section 16 pass; the matrix version and the masking version in force are read per call and named in every answer and every entry; a matrix change from `PM-2026.11` to `PM-2026.12` changes the answer with no deployment; a case number alone never changes an answer; a session as the rwb-access login holds no privilege in `rwb_case`, in `recovery` or in `public`; and the contract tests of RWB-P3-E1018-CON and RWB-P4-E1037-CON stay green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | The token holds no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | The area or the right is absent for every role of the caller | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside every scope of the caller, or the case reference is unknown | This case is not in your scope. |
| MSG-GEN-001 | A required request field is missing, for example the case reference | Enter {field}. |
| MSG-P7-003 | The access entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

For MSG-P4-002 the {action} value names the action the caller tried — "create this case", "read this case record", "transfer this case" — and never a case fact, an owner, a queue or a case number. For MSG-GEN-001 the {field} value is "a case reference". Every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The operation answers 401 for no role, 403 for a missing letter, 404 for a case out of scope or unknown, 422 for a missing request field and 503 when the entry cannot be written. The wording of the 422 and the 503 is fixed by the shared error envelope; the two refusal texts above are the ones of FSD P4.

### 15. Screens and states

No screen is built by this story. SCR-03 Case record shows the case header and its tabs, and its personal fields are rendered from the markers this story answers under the masking version in force: the borrower's identity number and address fields read `masked` or `clear` per role, and the screen never receives a value from this service. SCR-43 Roles and access shows the roles, the permissions, the scope and the masking rows, and is served by RWB-P4-AD008-APP and the admin stories. Both screens are served by the gateway-bff composite route (DP-19), which calls rwb-access for the decision and the markers and rwb-case for the case facts, one hop each, and merges the answers.

The states this story makes visible are the refusal states of the two decisions: the 403 of a role without the letter, the 404 of a case outside the scope, and the masked or clear marker of a personal field. The screen fields, the field-level rendering of a masked value and the composite route specification are Not specified in the source documents (GAP-0982; ASM-1719).

The states of SCR-03 Case record and SCR-43 Roles and access are those in Screen Specifications v1. Where that specification gives none, the states are Not specified in the source documents (CG-ALL-4898; CG-ALL-4899): empty, error and no-access for SCR-03, and empty, loading, error and no-access for SCR-43.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-018-02 | AC2: the creation of a case is refused before any case fact is examined when the caller holds no Case record C; the exclusion decision itself is rwb-case's | Component | Caller holding only `RW-REFADM`; case facts of a new case for `P-0101` with product group `HIRE_PURCHASE`; matrix `PM-2026.12` |
| TC-E1-018-01 | AC1, AC8: the creation decision is allowed on the letter C and answers the right and the matrix version; the case, its number and its rows are created by rwb-case (RWB-P3-E1018-APP) | Component | Caller holding `RW-CASEOWN` with `CASE_RECORD` letters `CRU`; case number `RW-2026-000123`; last number issued `RW-2026-000122` |
| TC-E1-018-03 | AC3: one case per customer and product means one case reference to decide, so the read decision answers that one case and no other; the grouping is rwb-case's | Component | Borrower `P-0102`; case facts of one case with two linked accounts; caller `CO-0201` with scope `OWN` |
| TC-E1-018-04 | AC4: a closed case keeps its number and the number decides nothing; a closed case and an open case answer the same way for the same letters and scope; numbering is rwb-case's | Component | Closed case `RW-2026-000123`, next case `RW-2026-000124`, caller `CO-0201` with scope `OWN` |
| TC-E1-018-05 | AC5: a matrix version change is data and takes effect with no deployment; the status list itself is rwb-case's | Contract | Matrix `PM-2026.11` then `PM-2026.12`; role `RW-LEGAL`; area `QUEUE_AND_ALLOCATION`; valid from `2026-12-01` |
| TC-E1-018-06 | AC6: an excluded account has no case, so the creation decision is never asked for it; the exclusion rule is rwb-case's | Component | Account `A-5005` with `dispute_open` true; reason `OPEN_DISPUTE`; no creation request raised |
| TC-E1-018-07 | AC7: the entry threshold boundary decides whether a creation happens at all, and the authority decision answers the request it is given; the threshold is rwb-case's | Component | Accounts `A-5006` at 89 days and `A-5007` at 90 days past due; one creation request only |
| TC-E1-018-08 | AC8: a repeated creation request for the same case facts answers the same decision and writes no second entry for the same request key; the repeat of the run is rwb-case's | Component | Same case facts and the same request key twice; one access entry |
| TC-E1-018-09 | AC9: no case exists before the ALS batch completes, so no creation decision is asked; the batch gate is rwb-source-data's and rwb-case's (RWB-ITG-E1018-ITG) | Component | ALS batch for `2026-12-02` at status `RUNNING`; no creation request raised |
| TC-E1-018-10 | AC10: when the access entry cannot be written the answer is 503 with MSG-P7-003 and no decision is returned; the case creation record is rwb-decision's and rwb-case's | NFR | Decision-record library forced to fail; no answer, no scope, no version |
| TC-E1-018-11 | AC11: a number at the top of the yearly range changes no answer, because the number is opaque here; the range and MSG-P3-025 are rwb-case's | Component | Case number `RW-2026-999999` and `RW-2026-000123`, all other facts equal |
| TC-E1-018-12 | AC12: two products give two cases, and each case reference is decided on its own facts and scope; the split is rwb-case's | Component | Borrower `P-0103`; two case references, one mortgage and one hire purchase; scopes `OWN` and `TEAM` |
| TC-E1-018-13 | AC1, AC4: a role without the right is refused with MSG-P4-002 on the read and on the transfer, and one refusal entry is written | Component | `RW-REFADM` asking for Case record R and for Queue and allocation U on `RW-2026-000123`; MSG-P4-002 both times |
| TC-E1-018-14 | AC5, AC8: a failure of the policy read or of the entry leaves no answer, and no stale version is served; the decision-record resilience of the creation is rwb-decision's | NFR | Library down for one call; a later matrix version committed during the call |
| TC-E1-018-15 | AC2, AC3: a case whose key has no source row still has an owner and a team, and the decision follows the facts presented; the REC-05 listing is rwb-source-data's and rwb-case's | Component | Case facts of `RW-2026-000126` with accounts `A-5013` and party `P-0105`; scope `OWN` and then `TEAM` |
| TC-E1-018-16 | AC6: a field with no masking row is masked, and the version is named even when the pack has a gap; the EXCLUSION package check is rwb-case's | Component | Masking version `MASK-SIT-01` with no row for `DF-PTY-008`; roles `RW-CASEOWN` and `RW-AUDIT` |
| TC-E1-018-17 | AC7: the build rule refuses any class of the access module that names a case table, a `v_ace_*` view or a `public` table | Component | Module map of `th.co.scb.ace.workbench.recovery.access.caseauthority` with one class naming `rwb_case.recovery_case`, one view name and `public.customer`; the build fails on each |
| TC-E1-018-18 | AC7: the boundary of the tables of section 12.7 holds, so only `role`, `permission`, `masking_rule` and the decision-record objects are read or written | Component | Container test over schema `rwb_access`; a statement against `rwb_case.recovery_case` fails with SQLSTATE 42501 |
| TC-E1-018-19 | AC16: every rule BR1 to BR12 of section 8 is named by a criterion of section 7 or a test case of section 16 | Component | Section 8 rule table and section 16 test case table of this story |
| TC-E1-018-20 | AC17: a request to POST /api/recovery/access/v1/authorise with no valid session answers 401 and no decision | Component | Request with no session and with an expired session; area `CASE_RECORD`, right `R`; case number `RW-2026-000123` |
| TC-E1-018-21 | AC18: a replay of a write with the same idempotency key returns the first answer and writes no second entry; the repeat of the run is rwb-case's | Component | Not specified in the source documents (NEWAC-RWB-P4-E1018-APP-AC18) |
| TC-E1-018-22 | AC1, AC15: the creation publishes rwb.case.CaseCreated.v1 on rwb.case.events.v1 and records DecisionRecorded on rwb.decision-record.v1 through P7 (DP-03); the AC15 rollback is the P7 admin rollback; the publish is rwb-case's and the ledger entry is rwb-decision's | Component | ALS batch seeded through the W1J01 harness; exact synthetic case set Not specified in the source documents (GAP-0343) |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end, Access to Component and Resilience to NFR; the cases this story owns are tested at Component and Contract level over the policy fixture, and the cases whose behaviour belongs to another slice are listed above with that slice named. Every legacy test case of RWB-E1-018 appears once with the slice of the behaviour this story answers: the creation, exclusion, grouping, numbering, state and threshold cases (TC-E1-018-01 to TC-E1-018-08, TC-E1-018-11, TC-E1-018-12, TC-E1-018-16) are created and held by rwb-case and appear here for the authority decision that precedes or accompanies them; TC-E1-018-09 and TC-E1-018-15 are the batch gate and the missing-key case of RWB-ITG-E1018-ITG; TC-E1-018-10 and TC-E1-018-14 carry the decision-record behaviour of RWB-P7-E1018-APP; and TC-E1-018-13, the refusal with MSG-P4-002, is this story's own. The -ITG copies of these cases are not here — they belong to the integration slice RWB-ITG-E1018-ITG, which proves the same values across rwb-case, rwb-source-data, rwb-access and rwb-document end to end.

### 17. Guardrails

- No business value in code: the capability areas, the letters, the scope values, the field IDs, the role codes and the version labels are data rows read with the version in force; no role code, area, letter or field-ID list appears in Java, and the build rule reads its allowed object list from the module map.
- No personal data in events, logs, workflow inputs, tests or prompts: the answer carries a marker and a version only, the access entry carries IDs, the scope and the field markers only, and every test row is synthetic (`DF-PTY-007` and `DF-PTY-016` are named, never rendered).
- ACE data only through the owner's contract or `v_ace_*` views — and this service reads neither: the case facts arrive in the request, the account and customer facts stay with rwb-source-data, and a class that names a view fails the build (DP-01, DP-05).
- No cross-schema read and no cross-schema key: `rwb_access` holds no foreign key into another schema and no copy of a case, a customer or an ACE row; `rwb_case` is reached only through the request, and `decision_log_entry` only through the library.
- The case number is never an authority token and is never parsed: no prefix, no year and no six-digit rule appears in this service, and the number is passed through as an opaque string (BR7).
- Default deny on every path: a missing role, a missing permission row, a missing letter, a missing masking row and a missing case fact all resolve to refused or masked, never to allowed and never to clear (BR1, BR5).
- The refusal comes before the handler and before any case fact is examined, and the refusal names the action, the area and the right, never a case fact or a number (BR12).
- The access entry is written first, in the same transaction as the answer, through the decision-record library; a failed write means 503 and no answer (BR6).
- One login per service (DP-02), one schema (`rwb_access`), one base (`/api/recovery/access/v1`), one naming library (DP-14) and no event or topic of this slice's own (DP-09).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-001 | One case for every non-excluded account at 90 days past due, created only where the caller may create it | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-04; FEAT-ACA-04 | 6.1 Take over the case at 90 days past due | BR1; BR2; CTL-09 | TC-E1-018-01, TC-E1-018-02, TC-E1-018-11 |
| REQ-CWC-002 | Case ID RW-YYYY-NNNNNN, issued once and never reused, printed on every document and never an authority token | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-01; FEAT-ACA-14 | 6.1 | BR7; BR8 | TC-E1-018-01, TC-E1-018-04, TC-E1-018-11 |
| REQ-CWC-003 | One case per customer and product, linked by business key with no foreign key | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-02; FEAT-ACA-14 | 6.1 | BR3; R-UNI-17 | TC-E1-018-01, TC-E1-018-03, TC-E1-018-12 |
| REQ-CWC-004 | Exclusion rules held as data and applied at creation | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-05 | 6.1 | BR1 | TC-E1-018-01, TC-E1-018-02, TC-E1-018-06 |
| REQ-CWC-005 | One case state at a time, from the state model and the lists | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-03 | 6.1 | BR8 | TC-E1-018-01, TC-E1-018-02, TC-E1-018-05 |
| REQ-CWC-016 | Every workflow event logged with its rule ID and version, and every read of the case store logged | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-21; FEAT-ACA-07 | 6.1 | BR6; R-UNI-39 | TC-E1-018-01, TC-E1-018-02, TC-E1-018-03 |
| REQ-CHO-004 | One agreed hand-over point in days past due for every rule and report, read from the case facts the caller presents | Business Requirements Epic 1, section 3.3 | FEAT-CWC-01; FEAT-CWC-02; FEAT-CWC-04; FEAT-ACA-11 | 6.1 | BR3; BR10 | TC-E1-018-01, TC-E1-018-04, TC-E1-018-08 |

The P4 requirements this slice serves are REQ-ACA-003 (the matrix is the only source of what a role may see and do), REQ-ACA-005 (personal data masked by role on every screen and in every agent call), REQ-ACA-007 (access outside the matrix refused and the refusal recorded) and REQ-ACA-009 (a user sees only the cases and queues their role and scope allow); they reach the table above through the same test cases and through the features FEAT-ACA-04, FEAT-ACA-05, FEAT-ACA-07, FEAT-ACA-11 and FEAT-ACA-14 of the FSD P4 module. The features FEAT-CWC-20 (the workflow admin API) and FEAT-CWC-21 (log every workflow event) are carried by the case service; this slice answers them only for the authority decision each event and each read needs. The -ITG copies of the test cases are carried by RWB-ITG-E1018-ITG.

| Legacy reference | Where it is kept |
|---|---|
| Legacy key RWB-E1-018; story RWB-P4-E1018-APP; contract RWB-P3-E1018-CON; baseline `rwb_access` | Metadata; sections 1, 3, 12 |
| Case number form RW-YYYY-NNNNNN, issued once and never reused | Sections 2, 8 (BR7), 11, 17 — held by rwb-case and never by this service |
| Legacy §14 messages MSG-P4-002 and MSG-P4-003, and legacy AC14 | Sections 5, 7 (AC1, AC2, AC4), 14 |
| Legacy §10 authority roles RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL, RW-REFADM, RW-COE | Sections 7, 10, 16 |
| BR11 of the legacy story (business key, no foreign key); D-RCV-35 U4; ADR-010 | Sections 8, 11, 12.7, 17 |
| Synthetic values: case `RW-2026-000123`, last number `RW-2026-000122`, accounts `A-5001` to `A-5013`, person keys `P-0101` to `P-0105`, queues `TDR-BKK-CO` and `TDR-BKK`, matrix `PM-2026.11` and `PM-2026.12`, mask `MASK-SIT-01`, field IDs `DF-PTY-007`, `DF-PTY-016`, `DF-PTY-008` | Sections 3, 7, 12.8, 16 |
| Field IDs DF-REF-034 to DF-REF-044, DF-REF-198 to DF-REF-204, DF-DEC-001 to DF-DEC-018, DF-DEC-028 to DF-DEC-031, DF-CAS-001 and DF-CAS-002 | Section 11 |
| Legacy test cases TC-E1-018-01 to TC-E1-018-16 | Section 16 |
| The other slices of RWB-E1-018 (rwb-case, rwb-source-data, rwb-document, rwb-decision, the integration harness) | Sections 2, 16, 19 |

### 19. Out of scope

- Case creation, the entry and exclusion rules, the grouping, the numbering sequence, the yearly range and the case tables: rwb-case (RWB-P3-E1018-APP and RWB-P3-E1018-CON).
- The ACE read behind the entry and exclusion decisions: rwb-source-data (RWB-P1-E1018-APP); this service reads no view.
- The document binding of the case: rwb-document (RWB-P5-E1018-APP).
- The decision record of a case creation and the central decision ledger: rwb-decision (RWB-P7-E1018-APP); this slice writes only its own access entry through the library.
- The policy pack load path — the reference loads, their approval, verification and rollback, and the rows of the matrix and the masking versions themselves: RWB-P4-AD002-APP and RWB-P4-AD004-APP.
- The sign-in, the session, the Entra group mapping and the caller's resolved teams and regions: RWB-P4-E1022-APP.
- Roles, teams and queues as data: RWB-P4-E1019-APP for the role model, and rwb-case (`queue`, `queue_member`) for the queue and team rows.
- The delegation of authority table and its lookup: RWB-P4-E2013-APP.
- The access log search screen and the six-monthly access review list (JOB-18): RWB-P4-E1039-APP and RWB-P4-AD008-APP.
- The ACE-sourced masking rows of `v_ace_customer` and the import boundary of this service as a whole: RWB-P4-E1069-APP.
- SCR-03 Case record and SCR-43 Roles and access as screens, with their states and filters: their screen stories and the gateway-bff composite route (DP-19).
- The end-to-end proof of these decisions across rwb-case, rwb-source-data, rwb-access and rwb-document: RWB-ITG-E1018-ITG.
- The contract document, its fakes and its versioning (RWB-P3-E1018-CON and RWB-P4-E1037-CON); the `rwb_access` schema baseline, the login, the topic and queue provisioning, the chart, the dashboards and the runbook of this service.
