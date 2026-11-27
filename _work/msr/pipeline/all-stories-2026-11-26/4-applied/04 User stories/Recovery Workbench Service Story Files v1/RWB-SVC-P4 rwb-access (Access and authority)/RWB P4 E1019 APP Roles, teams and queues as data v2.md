# RWB-P4-E1019-APP Roles, teams and queues as data

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E1019-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-019 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP08, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P4-P |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E1019-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (FR-P4-004, FR-P4-007, FR-P4-033, FR-P4-037) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-019 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-E1019-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **security administrator (RW-SECADM) and a reference data administrator (RW-REFADM)**, I want **the Recovery roles, their permission rows and their conflicting pairs held as data in rwb-access at the matrix version in force, with the role catalogue and the caller's session answering from that version, and a conflicting pair refused at sign-in**, so that **a role change reaches every service that authorises without a code release, and no service has to hold a copy of the roles to know what a role may do**.

This is the rwb-access slice of legacy RWB-E1-019, and it is the role half of that legacy key. The legacy story held the queues, the members, the roles and the lists as one set of versioned tables in one schema; D-RCV-60 keeps the behaviour and separates the ownership:

- **This story, rwb-access (P4), schema `rwb_access`:** the tables `role`, `permission` and `role_conflict` (DF-REF-034 to DF-REF-044 and DF-REF-205 to DF-REF-211), the role and permission rows of the role version in force, the role-set checks, the role catalogue on `GET /api/recovery/access/v1/admin/roles`, the caller's session on `GET /api/recovery/access/v1/me/session`, and the conflict check that refuses a person holding both roles of a conflicting pair (DP-01).
- **Not this story, rwb-case (P3):** `queue`, `queue_member`, `queue_measure`, `capacity`, the assignment methods and the reference-load path with its approve and rollback operations. Those are RWB-P3-E1019-APP, RWB-P3-E1019-CON and RWB-P3-E1019-DB, and this story writes no queue, membership or capacity row and offers no assignment method.
- **Not this story, rwb-case reference data (P3):** `lov_value`, the lists and the evaluation of a list. `LOV-ROLE-CLASS`, `LOV-CAPABILITY` and `LOV-SCOPE` are read through the reference-data contract of rwb-case with the version in force (DP-07); no list value is copied into `rwb_access`.
- **Not this story, S9 and P7:** `partner_user` is rwb-partner's (S9), `decision_log_entry` and the `rule_package*` tables are rwb-decision's (P7).
- **Service naming:** base `/api/recovery/access/v1` (DP-13), schema `rwb_access`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1` (DP-14), Temporal task queue `rwb-access` in namespace `rwb-recovery` (not used here), Java package `th.co.scb.ace.workbench.recovery.access`.
- **Events:** this story publishes no event and consumes none. DP-09 is not in its pattern set, and the policy-change event `rwb.access.AccessPolicyChanged.v1` belongs to the story that loads a policy version, not to the catalogue read.
- **The refusal entry:** a conflict refusal and a refused call are recorded by the access-entry writer of RWB-P4-E1039-APP through the local decision-record library (DP-03); this story supplies the refusal and the reason and builds no record writer of its own, so DP-03 is not a pattern of this slice and no decision-record dependency is added here.
- **Database access:** through the per-service rwb-access login of the service baseline (DP-02). No statement in this story names a table in another schema, an ACE view or a table in `public`.

### 2. Business rationale

Access and rights live in documents and in people's heads today, and a change of rights needs a code change or a manual check. The legacy story made the whole organization structure data: queues, members, capacity, teams and roles in versioned tables, loaded from one template with an approver and a one-call rollback. That answer is still the right one, and the realignment makes it a smaller and a stronger answer by splitting it. The queue half describes who works which list, and it belongs with the case engines that read it, so it stays in rwb-case. The role half describes what a role may do in each capability area, and it is read by **every** service that authorises, so it belongs in rwb-access and it must be answerable in one hop.

That is what this story delivers. The role rows, the letters of each capability area and the pairs of roles one person may not hold together are rows of `rwb_access`, held at a matrix version, written from the approved role file by the service's own migration (DP-15), and answered by the catalogue and by the session. A queue row keeps only the role **code** it points at, and the loader that checks that code asks this service. Two consequences follow, and both are the point of the split: a role change is a new matrix version and reaches every reader without a deployment (REQ-ACA-002), and a person who is given two roles that may not be held together is stopped at the door instead of being discovered in an audit (legacy RWB-E1-019 BR9 and the separation-of-duty table, control CTL-08).

The story meets REQ-CWC-006 (roles, teams, queues, membership and capacity held as versioned reference data and changeable without a code release) for the role half, and REQ-ACA-002 (roles held as data, and a role change taking effect without a code release) in full. It pairs with the FSD P4 features FEAT-ACA-03 (hold roles as data) and FEAT-ACA-04 (hold the role to permission matrix as data), and it is the input to every service's authorise check, to scope by team and region, and to the access log. The rule that a version takes effect on its date and that open work keeps the version it was decided under is R-UNI-38, and it applies to the matrix exactly as it applies to a rule version.

Three things no source fixes are carried as placeholders in this story: how many roles a role version holds and what the approved role file looks like, including its conflict version label — Not specified in the source documents (GAP-0985; ASM-1728); the column that dates a matrix version, because `role` and `permission` carry no `valid_from` while the functional specification takes a matrix file into effect on a date — Not specified in the source documents (GAP-0985; ASM-1729); and the full list of conflicting pairs and the text of MSG-P4-006 — Not specified in the source documents (GAP-0985; ASM-1730).

### 3. Preconditions

- RWB-P4-E1037-CON is published: the OpenAPI 3.1 document for `/admin/roles` and `/me/session` on base `/api/recovery/access/v1`, the authorise contract this service answers, the RFC 9457 error envelope, and the exemptions of the guard library. This story adds no path.
- The `rwb_access` baseline is in place: `role` (DF-REF-034 to DF-REF-039), `permission` (DF-REF-040 to DF-REF-044) and `role_conflict` (DF-REF-205 to DF-REF-211) exist with their dictionary rows, and the authorise answer already resolves a caller's roles from `role` and `permission`.
- RWB-P3-E1019-CON is published (contract dependency, C): the queue contract carries the `role_code` a queue row points at, with its fake. This story builds against that fake from Day 1 and never against the rwb-case build (DP-11). The queue rows themselves are RWB-P3-E1019-APP's.
- RWB-PLT-E1043-CON and RWB-P3-E1043-CON are in place, so `LOV-ROLE-CLASS`, `LOV-CAPABILITY` and `LOV-SCOPE` are read with the version in force through the reference-data contract (DP-07). `LOV-ROLE-CLASS` holds BANK_USER, PARTNER_USER and NON_HUMAN_ACTOR; `LOV-SCOPE` holds OWN, TEAM, REGION and ALL; `LOV-CAPABILITY` holds the 14 areas, including CASE_RECORD, QUEUE_AND_ALLOCATION, DOCUMENTS, REFERENCE_DATA and PLATFORM_ADMINISTRATION (TSD P4 v3 T3.2).
- The approved role file for the version in force exists, prepared by RW-REFADM and approved by RW-SECADM. Its layout, its row counts and the conflict version label it carries are Not specified in the source documents (GAP-0985; ASM-1728).
- The roster the file must cover is the role list of TSD P4 v3 T6.1, with the three capability letters of each role: RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL, RW-FIELDCOL, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-GUARANT, RW-AGENCYMG, RW-CONDUCT, RW-CAPACITY, RW-PRODHEAD, RW-HEADLIT, RW-HEADNPA, RW-HEADASL, RW-CREDCOMM, RW-WOCOMM, RW-RISK, RW-COE, RW-DATASTEW, RW-FINANCE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-REFADM, RW-SECADM, RW-BIANAL, RW-TRIBE, SY-CASEWF, SY-RULES, SY-DATALOAD, SY-OCR and SY-AGENT. The number of roles a version holds is Not specified in the source documents (GAP-0985; ASM-1728).
- Matrix version PM-2026.11 is the version in force at go-live and PM-2026.12 is the version the functional specification takes into effect on 1 December 2026 with 756 permission rows (FSD P4 v3 A2.1, A2.4). The column that holds the effective date of a matrix version is Not specified in the source documents (GAP-0985; ASM-1729).
- The conflicting pairs the sources name are RW-SECADM with any business role (FSD P4 v3 AC-EXC-P4-001-03) and RW-RISK with RW-REFADM (legacy RWB-E1-019 section 10, separation of duty). The full list is Not specified in the source documents (GAP-0985; ASM-1730).
- The approved file, the test fixtures and every user in the tests are synthetic; no production role, person or entitlement is read, and no name is stored or logged anywhere.
- No approval is required to build against a Draft contract: the baseline is Draft (realignment v1) and the version is frozen when the consumers pass their contract tests.

### 4. Flow

1. RW-REFADM prepares the approved role file for matrix version PM-2026.11 — one row per role with its class and default scope, one row per role and capability area with its letters, and one row per conflicting pair — and RW-SECADM approves it. The file layout is Not specified in the source documents (GAP-0985; ASM-1728).
2. RoleSetChecks run over the file before any row is written: role class in `LOV-ROLE-CLASS`, role code unique, capability area in `LOV-CAPABILITY`, letters drawn from C, R, U, D, A or a dash, default scope in `LOV-SCOPE`, every conflict pair naming two role codes of the same file and no role with itself, and no required field empty (BR2).
3. The migration `V1019_1__role_matrix.sql` writes the rows of the approved file into `role`, `permission` and `role_conflict` in schema `rwb_access`, each permission row carrying `matrix_version` PM-2026.11 and each conflict row carrying the conflict version of the file and its `valid_from`; it copies no value from ACE and no value of a person (DP-15, DP-02).
4. The effective date of the version is read with the version, not with each row; the read path resolves the matrix version in force on the day asked (BR11, ASM-1729).
5. `GET /api/recovery/access/v1/admin/roles` answers the catalogue: for every role in force, its role code, name, class and default scope, its permission rows with the area and the letters, its conflict pairs, and the matrix version and conflict version they belong to (BR4, BR5).
6. `GET /api/recovery/access/v1/me/session` answers the caller's resolved roles from the sign-in claim and the `role` rows, the scope of those roles, the matrix version, and whether the caller holds a conflicting pair (BR5, BR6).
7. Sign-in: where the caller's roles include both halves of any `role_conflict` row at the conflict version in force, the session is refused with MSG-P4-006 naming the pair, an incident is raised to the security administrator queue, and the refusal is passed to the access-entry writer of RWB-P4-E1039-APP with reason ROLE_CONFLICT (BR3).
8. Every call is authorised at the door: the administration view needs the R letter of Platform administration, the role read a loader or a service identity makes needs the R letter of Reference data, a caller with no Workbench role is refused 401 with MSG-P4-001, and a caller without the needed letter is refused 403 with MSG-P4-002 and the refusal is passed to the access-entry writer of RWB-P4-E1039-APP as an AC-DENY (BR7, DP-08).
9. The answer is read only: no operation of this story writes a row of `role`, `permission` or `role_conflict` at run time, and the catalogue has no save, update or delete path.
10. The answer names no queue, no membership and no capacity value: a queue row keeps the role code, and the queue read, the capacity answer and the assignment methods are RWB-P3-E1019-APP's (BR8).
11. No statement of this story names a `v_ace_*` view, a table in `public` or a table of another service; the lists arrive through the reference-data contract and the boundary rule BND-6 of RWB-P4-E1069-APP stays green on the package (BR9, DP-01).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role row names a role class that is not a value of `LOV-ROLE-CLASS` | The whole version is refused, the row is named and no row is written | MSG-P1-002 | AC2 |
| X2 | The same role and capability area appear twice | The whole version is refused and the duplicate row is named | MSG-P1-002 | AC2 |
| X3 | The letters hold a character outside C, R, U, D, A and the dash | The whole version is refused and the row is named | MSG-P1-002 | AC2 |
| X4 | A role names a capability area that is not a value of `LOV-CAPABILITY`, or a default scope outside `LOV-SCOPE` | The whole version is refused and the field is named | MSG-GEN-001 | AC2 |
| X5 | A conflict pair names a role code the file does not hold, or names one role twice | The whole version is refused and the pair is named | MSG-P1-002 | AC2 |
| X6 | A required column is empty on a row | The whole version is refused and the field and row are named | MSG-GEN-001 | AC2 |
| X7 | A person holds both roles of a conflicting pair at the conflict version in force | The sign-in is refused, the pair is named, an incident is raised and the refusal is passed to the access-entry writer of RWB-P4-E1039-APP with reason ROLE_CONFLICT | MSG-P4-006 | AC3 |
| X8 | The caller holds no Workbench role | The call is refused before any role is answered | MSG-P4-001 | AC5 |
| X9 | The caller holds neither the Platform administration R nor the Reference data R letter the call needs | The call is refused and the refusal is passed to the access-entry writer of RWB-P4-E1039-APP as an AC-DENY | MSG-P4-002 | AC5 |
| X10 | A read arrives while a new matrix version is being applied | The read answers one version whole — either the old or the new — and never a mixture of two versions | None | AC7 |
| X11 | The migration is applied a second time | Flyway reports the version as already applied; no row is written twice and no version is edited in place | None | AC1 |
| X12 | A caller asks this service for a queue row, a member capacity or an assignment method | There is no such operation: the queue read and the capacity answer are RWB-P3-E1019-APP's, and the caller is answered 404 for a path this service does not publish | None | AC8 |

No exception path of this story changes a case, a task or a queue: this service answers roles, permissions and conflicts, and the case and queue state machines are rwb-case's.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the `rwb_access` baseline, the RWB-P3-E1019-CON fake and the reference-data fake; the queue rows, the capacity answer and the load path belong to RWB-P3-E1019-APP and are not prerequisites of this build |
| Negotiable | The role roster, the letters per area, the default scopes, the conflict pairs, the version labels and the effective dates are data rows of the approved file; the story fixes the checks, the catalogue shape and the read rule only |
| Valuable | One role change reaches every service that authorises without a code release, and a person given two incompatible roles is stopped at sign-in |
| Estimable | One migration, one check set, one catalogue read, one session read, one conflict check and one refusal path |
| Small | Fits one sprint with its tests, as a secondary slice of the legacy key |
| Testable | Every criterion in section 7 is one automated test over synthetic role rows; no ACE data and no production entitlement is needed |

### 7. Acceptance criteria

```gherkin
Feature: The Recovery roles, their permissions and their conflicts as data in rwb-access

  Background:
    Given the rwb-access base path is /api/recovery/access/v1 and the schema is rwb_access
    Given "LOV-ROLE-CLASS" holds "BANK_USER", "PARTNER_USER" and "NON_HUMAN_ACTOR"
    Given "LOV-SCOPE" holds "OWN", "TEAM", "REGION" and "ALL"
    Given "LOV-CAPABILITY" holds the 14 areas, including "CASE_RECORD", "QUEUE_AND_ALLOCATION", "DOCUMENTS", "REFERENCE_DATA" and "PLATFORM_ADMINISTRATION"
    Given matrix version "PM-2026.11" is in force from 30 November 2026
    Given every role row and every test user of this story is synthetic

  Scenario: AC1 The role version and its permission rows are in force (new, D-RCV-60)
    Given the approved role file for version "PM-2026.11" holds the role rows, their permission rows and their conflict pairs, and covers the role codes of TSD P4 T6.1, including "RW-CASEOWN", "RW-LITOFF", "RW-LEGAL", "RW-REFADM", "RW-SECADM" and "SY-CASEWF"
    When the migration "V1019_1__role_matrix.sql" is applied to schema "rwb_access"
    Then "role" holds one row per role of the file, each with its role code, role name, role class of "LOV-ROLE-CLASS" and default scope of "LOV-SCOPE"
    Then "permission" holds one row per role and capability area, each with the area of "LOV-CAPABILITY", the letters and matrix version "PM-2026.11"
    Then "role_conflict" holds the pairs of the file, each with the conflict version of the file and its valid from date
    Then "SY-CASEWF" is class "NON_HUMAN_ACTOR" and "RW-CASEOWN" is class "BANK_USER" with default scope "OWN"
    Then the row counts equal the counts the approved file holds, and no role code, area, scope or letter is a constant in code
    When the same migration version is applied a second time
    Then Flyway reports it as already applied and no row is written twice

  Scenario: AC2 An unknown role class, a duplicate role code or invalid letters refuses the whole version (new, D-RCV-60)
    Given the role row for "RW-CASEOWN" carries role class "BANK-USER", which is not a value of "LOV-ROLE-CLASS"
    When the role set checks run over the file
    Then the whole version is refused with MSG-P1-002 naming that row and the check "role class not in LOV-ROLE-CLASS"
    Then no row of the version is written to "role", "permission" or "role_conflict" and version "PM-2026.11" stays in force
    When the file lists "RW-CASEOWN" twice for capability area "CASE_RECORD"
    Then the whole version is refused with MSG-P1-002 naming the duplicate row and the check "role and area listed twice"
    When "RW-AUDIT" is given the letters "RX" in area "REPORTING"
    Then the whole version is refused with MSG-P1-002 naming that row and the check "letters outside CRUDA"
    When a role row names capability area "AUDIT_VIEW", which is not a value of "LOV-CAPABILITY"
    Then the whole version is refused with MSG-GEN-001 for field "capability_area"
    When a conflict pair names role code "RW-UNKNOWN"
    Then the whole version is refused with MSG-P1-002 and the check "conflicting pair names an unknown role code"
    When a role row carries no role name
    Then the whole version is refused with MSG-GEN-001 for field "role_name"

  Scenario: AC3 A conflicting pair is recorded and a person holding both is refused at sign-in (new, D-RCV-60)
    Given "role_conflict" holds a row that "RW-SECADM" may not be held with "RW-CASEOWN", and a row that "RW-RISK" may not be held with "RW-REFADM"
    When test user "U-1006" signs in with groups that give the roles "RW-SECADM" and "RW-CASEOWN"
    Then the session is refused with message MSG-P4-006 naming "RW-SECADM" and "RW-CASEOWN"
    Then an incident is raised to the security administrator queue
    Then the refusal carries the user reference, the pair and reason "ROLE_CONFLICT", and no name; the entry is written by RWB-P4-E1039-APP's access-entry writer and is not this story's deliverable
    And GET /api/recovery/access/v1/me/session for the same user answers the conflict state and grants no scope
    When a test user holding "RW-RISK" alone signs in and reads the session
    Then the session answers role "RW-RISK", its scope and the conflict state "clear"
    And a test user holding both "RW-RISK" and "RW-REFADM" is refused the same way

  Scenario: AC4 The role catalogue answers role, class, default scope, permissions and conflicts (new, D-RCV-60)
    Given a service identity holds the Reference data R letter and no Platform administration right
    Given the catalogue holds "RW-CASEOWN" with class "BANK_USER", default scope "OWN" and the letters of each area at "PM-2026.11"
    When the identity calls GET /api/recovery/access/v1/admin/roles to resolve a role code
    Then the response holds one entry per role in force, with role code, role name, role class, default scope, one permission row per capability area with its letters, its conflict pairs and matrix version "PM-2026.11"
    Then the entry for "RW-CASEOWN" answers class "BANK_USER", default scope "OWN" and the letters of each area
    Then the entry for "RW-SECADM" lists its conflict pairs with the conflict version of the file
    Then the response carries no person, no user identity, no e-mail address and no entitlement of a named individual
    And the matrix version answered is the one in force on the day of the call

  Scenario: AC5 A caller without the right is refused with MSG-P4-002 (new, D-RCV-60)
    Given test user "U-1002" holds only "RW-PHONECOL", whose Platform administration letter is "-" and whose Reference data letters are "R"
    When "U-1002" calls GET /api/recovery/access/v1/admin/roles as the administration view
    Then the call is refused with status 403 and message MSG-P4-002 with action "read roles"
    Then the refusal carries the user reference, area "PLATFORM_ADMINISTRATION", right "R" and result "REFUSED"; the entry is written by RWB-P4-E1039-APP's access-entry writer
    And the role catalogue itself is unchanged
    When a test user holding no Workbench role at all calls either operation
    Then the call returns status 401 with message MSG-P4-001
    And no entry is written with a role, a permission or a scope for that caller

  Scenario: AC6 The session names the resolved roles, scope, matrix version and conflict state (new, D-RCV-60)
    Given test user "U-1005" signs in with groups that give the roles "RW-LITOFF" and "RW-LEGAL"
    When the user calls GET /api/recovery/access/v1/me/session
    Then the session answers roles "RW-LITOFF" and "RW-LEGAL", the scope of each role from "LOV-SCOPE", matrix version "PM-2026.11" and conflict state "clear"
    Then the DOCUMENTS letters are "CRUA", the union of "CRU" and "CRUA"
    Then no permission comes from a role the user does not hold
    Then the session answers the scope of the roles only, and no case, queue or team scope derived from a queue row, because this story reads no queue row

  Scenario: AC7 A new matrix version takes effect on its date without a deployment (new, D-RCV-60)
    Given matrix version "PM-2026.11" is in force until 30 November 2026
    Given version "PM-2026.12" is applied with effective date 1 December 2026, carries the 756 permission rows of its file, and gives "RW-LEGAL" the letter "R" in area "QUEUE_AND_ALLOCATION", where "PM-2026.11" gave it none
    When the catalogue and the session are read on 30 November 2026
    Then both answer matrix version "PM-2026.11" and "RW-LEGAL" holds no R in "QUEUE_AND_ALLOCATION"
    When the same reads are made on 1 December 2026
    Then both answer matrix version "PM-2026.12" and "RW-LEGAL" holds "R" in "QUEUE_AND_ALLOCATION"
    Then no deployment, no restart and no code change was made
    And the rows of "PM-2026.11" stay readable with their effective end date

  Scenario: AC8 This slice writes no queue, membership or capacity row and reads no other schema (new, D-RCV-60)
    Given schema "rwb_access" holds "role", "permission" and "role_conflict"
    Given schema "rwb_case" holds "queue", "queue_member" and "queue_measure"
    When the role version of this story is applied and the catalogue and the session are read
    Then no row of "queue", "queue_member", "queue_measure", "assignment" or "task" is written or read by any statement of this story
    Then the only tables named by the migration and the read path are "role", "permission" and "role_conflict" in "rwb_access"
    Then no statement names a "v_ace_*" view, a table in schema "public" or a table of another service, and boundary rule BND-6 of RWB-P4-E1069-APP stays green on this package
    Then "LOV-ROLE-CLASS", "LOV-CAPABILITY" and "LOV-SCOPE" are read through the reference-data contract of rwb-case, and no list value is copied into "rwb_access"
    Then the story answers no capacity question and offers no assignment method, because those are RWB-P3-E1019-APP's
```

The eight criteria above are new and test only this deliverable: the role, permission and conflict rows of the role version, the role-set checks, the catalogue, the session and the conflict refusal. No legacy criterion of RWB-E1-019 is repeated here, because the legacy criteria of that key are the queue, membership, capacity, rollback and overflow criteria of RWB-P3-E1019-APP; the one legacy criterion that reaches this half is the access refusal, which is carried as TC-E1-019-13 in section 16.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The roles, the letters of each capability area and the pairs of roles one person may not hold together are data with a version. No role code, area, scope or letter is written in code | FSD P4 A2.3, A2.4; BR-P4-003, BR-P4-004; TSD P4 T3.1 |
| BR2 | A version with any failed row is refused in full: the class, the area, the scope, the letters, the duplicate row and the conflict pair are all checked before a row is written, and a failed version writes nothing | Legacy RWB-E1-019 BR2; MSG-P1-002; control CTL-08 |
| BR3 | A person may not hold both roles of a conflicting pair at the conflict version in force; the sign-in is refused with MSG-P4-006, an incident is raised and the refusal is passed to the access-entry writer of RWB-P4-E1039-APP with reason ROLE_CONFLICT | FSD P4 AC-EXC-P4-001-03; legacy RWB-E1-019 BR9 and section 10; separation of duty |
| BR4 | The catalogue answers every role in force with its class, its default scope, its permission rows and its conflict pairs, and names the matrix version and the conflict version they belong to | FSD P4 A2.3, A2.4; TSD P4 API-P4-007 |
| BR5 | The default deny rule holds on this surface: a caller with no Workbench role is refused 401, and a caller without the letter an operation needs is refused 403 with MSG-P4-002 and the refusal is passed to the access-entry writer of RWB-P4-E1039-APP | FSD P4 VR-P4-004-1; VR-P4-001-1; legacy MSG-P4-001 and MSG-P4-002 |
| BR6 | The session answers the caller's resolved roles, the scope of those roles, the matrix version and the conflict state; it answers no scope derived from a queue row, because a queue row is not read here | FSD P4 AC-P4-001-01, AC-ALT-P4-001-02; TSD P4 API-P4-012; DP-01 |
| BR7 | The administration view needs the R letter of Platform administration; the role read a loader or a service identity makes needs the R letter of Reference data; the guard library answers both in one hop inside 2 s | TSD P4 API-P4-007; DP-08; DP-11 |
| BR8 | This story writes no `queue`, `queue_member`, `queue_measure`, `assignment` or `task` row and answers no capacity or assignment question; those are rwb-case data and RWB-P3-E1019-APP's behaviour | Ownership map (`queue`, `queue_member` are P3); DP-01 |
| BR9 | No statement of this story names a `v_ace_*` view, a table in schema `public` or a table of another service; the lists arrive through the reference-data contract and no list value is copied | Architecture v5 slides 8, 9 and 41; DP-01; DP-05; DP-07 |
| BR10 | Every read is one hop on the caller's thread with a 2 s budget, and no read calls another service | ADR-020; DP-11 |
| BR11 | A matrix version takes effect on its effective date, and open work keeps the version it was decided under: the read answers one version whole and never a mixture | FSD P4 A2.4; R-UNI-38; TSD P4 T4 (LOV-VERSION-STATUS) |
| BR12 | The read path has no write method: no operation of this story creates, changes or deletes a `role`, `permission` or `role_conflict` row, and a new version is a new set of dated rows | FSD P4 A2.4; legacy RWB-E1-019 BR3; DP-15 |
| BR13 | The role rows, the permission rows and the conflict pairs carry no name and no personal field: a role is a code, an area is a code, a letter is a letter, and a conflict is a pair of codes | FSD P4 A2.3 field catalog; NFR-039; NFR-040 |

Where each rule sits in the target: BR1, BR4, BR6 and BR12 are answered from `rwb_access` only. BR7 is answered by the guard library and the permission rows of the caller's roles, in one hop. BR2 is the check set that runs before the migration writes anything, so a version that fails is never stored. BR3 is the sign-in path over `role_conflict` at the conflict version in force. BR9 is enforced by the module map and boundary rule BND-6 of RWB-P4-E1069-APP, and BR10 by the client budget of the service template.

### 9. State transitions

None for a case. This story holds no case, task, queue or approval state (TSD P4 v3 T4). The states it reads are the states of a role version, and the states it produces are the outcomes of a catalogue read, a session read and a conflict check.

| From | Event | Condition | To |
|---|---|---|---|
| No version of the role matrix | the approved role file is applied by this story's migration | Every role-set check passes | The version is in force from its effective date |
| A version in force | a later version is applied with a later effective date | The later version passes every check | The later version answers from its effective date; the older rows stay readable with their effective end date |
| A version in force | a read on a day inside two versions | None | Exactly one version answers, the one whose effective date is the latest not after the day asked |
| A version in force | a new version fails a check | Any failed row | The whole version is refused and the version in force is unchanged |
| Conflict rows of a version | a person signs in holding both halves of a pair | The pair is in force on the day of the sign-in | The session is refused with MSG-P4-006, an incident is raised and the refusal is passed to the access-entry writer of RWB-P4-E1039-APP |

The version status vocabulary is LOV-VERSION-STATUS (LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED) in TSD P4 v3 T3.2. This story writes the rows of an approved version and reads the version in force; the transitions of a load, its approval and its rollback on the reference-load path are rwb-case's and are not carried here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-access service identity (the per-service login, DP-02) | Answers the catalogue and the session, applies the role version by migration, runs the role-set checks and the conflict check, and passes the refusal to the access-entry writer of RWB-P4-E1039-APP |
| RW-SECADM, security administrator | Owns the role catalogue and the matrix; CRUDA in Platform administration (TSD P4 v3 T6.1); approves the role file |
| RW-REFADM, reference data administrator | Prepares the role file; Reference data CRUD (TSD P4 v3 T6.1); no approval and no sign-in exemption |
| RW-COE, center of excellence analyst | Reads the roles and the matrix (Rules and parameters CRUD, Platform administration R); may read the catalogue |
| RW-AUDIT, internal audit | Reads the role catalogue, the matrix version and the conflict pairs |
| RW-PLATADM, platform administrator | Reads the administration view (Platform administration CRUD); changes no role row in this story |
| Every other role, including RW-CASEOWN, RW-PHONECOL and RW-LITOFF | Is answered by the session for its own record; holds no write path here |
| Service identities and reference-data loaders of the other services | Read the catalogue to resolve a role code under the Reference data R letter, in one hop inside 2 s |
| SY-CASEWF, SY-RULES, SY-DATALOAD, SY-OCR and SY-AGENT | Are roles of class NON_HUMAN_ACTOR and are answered as roles, with no exemption from the conflict rule |
| No delegation of authority level applies | A role, a permission and a conflict are not a credit decision |

The catalogue answers two callers under two rights, exactly as the Work Package fixes: the administration view for a person needs the R letter of Platform administration (TSD P4 v3 API-P4-007), and the role read a loader or a service identity makes needs the R letter of Reference data. A caller holding neither is refused with MSG-P4-002, and a caller holding no Workbench role at all with MSG-P4-001. The database login is the per-service login of the service baseline (DP-02), and this story adds no grant.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 | `role` | id | Write by the migration; Read |
| DF-REF-035 | `role` | role_code | Write by the migration; Read |
| DF-REF-036 | `role` | role_name | Write by the migration; Read |
| DF-REF-037 | `role` | role_class (LOV-ROLE-CLASS) | Write by the migration; Read |
| DF-REF-038 | `role` | default_scope (LOV-SCOPE) | Write by the migration; Read |
| DF-REF-039 | `role` | entra_group | Read; the group-to-role mapping is ACE's `v_ace_iam_group`, read by the sign-in path and never copied here |
| DF-REF-040 | `permission` | id | Write by the migration; Read |
| DF-REF-041 | `permission` | role_id | Write by the migration; Read |
| DF-REF-042 | `permission` | capability_area (LOV-CAPABILITY) | Write by the migration; Read |
| DF-REF-043 | `permission` | letters | Write by the migration; Read |
| DF-REF-044 | `permission` | matrix_version | Write by the migration; Read |
| DF-REF-205 | `role_conflict` | id | Write by the migration; Read |
| DF-REF-206 | `role_conflict` | role_code | Write by the migration; Read |
| DF-REF-207 | `role_conflict` | conflicts_with | Write by the migration; Read |
| DF-REF-208 | `role_conflict` | reason | Write by the migration; Read; the reason text is the file's and is not a personal field |
| DF-REF-209 | `role_conflict` | conflict_version | Write by the migration; Read |
| DF-REF-210 | `role_conflict` | valid_from | Write by the migration; Read |
| DF-REF-211 | `role_conflict` | valid_to | Write by the migration; Read |
| DF-REF-027 to DF-REF-033 | `lov_value` of `rwb_case` | lov_code, value_code, label_en, sort_order, valid_from | Read through the reference-data contract (DP-07); never read from `rwb_access` |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the refusal entry of a sign-in conflict and of a refused call | Written by RWB-P4-E1039-APP's access-entry writer; this story writes no row of it |

Two values the sources do not fix are carried as placeholders. The effective date of a matrix version has no column on `role` or `permission` in TSD P4 v3 T3.1, while FSD P4 v3 A2.4 takes version PM-2026.12 into effect on 2026-12-01 — Not specified in the source documents (GAP-0985; ASM-1729). The number of role rows and permission rows a version holds, the role-file layout and the conflict version label are not stated by any source — Not specified in the source documents (GAP-0985; ASM-1728); the story seeds exactly the rows of the approved file, counts them against the file and never against a constant, and the file must cover the role codes of TSD P4 v3 T6.1. The full conflict list and the text of MSG-P4-006 are Not specified in the source documents (GAP-0985; ASM-1730). Field IDs are those in the Logical Data Model and Data Dictionary v9, and the legacy physical names `role`, `permission` and `role_conflict` are kept.

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/api/recovery/access/v1/admin/roles` | The role catalogue in force: for each role, its role code, role name, role class, default scope, one permission row per capability area with its letters, its conflict pairs, and the matrix version and conflict version they belong to | Platform administration R for the administration view of a person; Reference data R for the role read a loader or a service identity makes (TSD P4 API-P4-007; DP-08) | Not applicable, read only |
| GET | `/api/recovery/access/v1/me/session` | The caller's resolved session: the roles held, the scope of those roles, the matrix version and the conflict state | Any authenticated caller with a Workbench role, own record only, right R (TSD P4 API-P4-012) | Not applicable, read only |

Both paths sit on the base `/api/recovery/access/v1` of DP-13 and are the operations the ownership map gives to P4 (`GET /admin/roles`, `GET /me/session`). The catalogue answer is `Role[]`: the role code, the role name, the role class, the default scope, the permission rows of the role, the conflict pairs of the role and the matrix version; the conflict version travels with each pair. Request and answer field names are the dictionary names DF-REF-034 to DF-REF-044 and DF-REF-205 to DF-REF-211, and the response envelope is that of RWB-P4-E1037-CON. Errors: 401 no Workbench role (MSG-P4-001); 403 no letter for the operation (MSG-P4-002); 404 a path this service does not publish; 503 the role rows or the reference lists are unavailable (MSG-GEN-006).

This story adds no path, no query parameter and no response field to the contract baseline, and it publishes no load, approve or rollback operation: `/api/recovery/access/v1/admin/reference-loads*`, `/api/recovery/access/v1/admin/lists/{listCode}` and the reference version store are P3's under ASM-0041 and ASM-0071, and the queue, the membership and the capacity answer are P3's under the ownership map.

#### 12.2 REST operations consumed

None. At run time this service answers and calls no service: the caller's identity arrives in the session, the lists arrive through the reference-data client library of rwb-case (DP-07), and the queue code a queue row points at is read by rwb-case, not by this service. The one hop and the 2 s budget of DP-11 apply to the inbound call.

#### 12.3 Events published

None. DP-09 is not a pattern of this story, no outbox row is written and no topic is produced to. The topic `rwb.access.events.v1` and its event names `rwb.access.<Event>.v1` belong to the service, and `rwb.access.AccessPolicyChanged.v1` — the change of a role or a policy version — is published by the story that loads a policy version, not by this catalogue read. A refusal entry is written by the access-entry writer of RWB-P4-E1039-APP, not by this story, and it is not an event of this service.

#### 12.4 Events consumed

None. rwb-access is a reference-data owner in Architecture v5 slide 14 (events: none), and the version in force is read from `rwb_access` on each call. This story subscribes to no topic and writes no inbox row.

#### 12.5 Workflows and activities

None. The catalogue and the session are synchronous REST answers in the caller's thread. The six-monthly access review list (JOB-18, Architecture v5 slide 44) belongs to RWB-P4-AD008-APP; this story starts no workflow, signals none and registers no activity on the `rwb-access` queue.

#### 12.6 Schedules

None. No Temporal Schedule and no quartz job sits in this story, and nothing about a role version runs on a clock: the effective date is a value the read resolves.

#### 12.7 Tables owned

| Table | Schema | Owner (ownership map) | This story |
|---|---|---|---|
| `role` | `rwb_access` | P4 | Writes the rows of the role version by migration; reads them for the catalogue and the session |
| `permission` | `rwb_access` | P4 | Writes the rows of the role version by migration; reads them for the catalogue and the session |
| `role_conflict` | `rwb_access` | P4 | Writes the rows of the conflict version by migration; reads them for the catalogue and the conflict check |
| `outbox_event`, `processed_event`, `idempotency_key` | `rwb_access` | PLT library | Created by the service baseline (DP-09); this slice writes no row of them |
| `queue`, `queue_member`, `queue_measure`, `assignment`, `task` | `rwb_case` | P3 | **Never read and never written** (DP-01) |
| `lov_value`, `reference_row`, `reference_version` | `rwb_case` | P3 | **Never read by SQL**; the lists arrive through the reference-data contract (DP-07) |
| `partner_user` | `rwb_partner` | S9 | Not read and not written (ASM-0072) |
| `decision_log_entry`, `rule_package*` | `rwb_decision` | P7 | Not read and not written (ASM-0069) |

No foreign key crosses a schema and no statement in this story names a table outside `rwb_access`. The dictionary rows of the roles are the Workbench's own and stay with this service.

#### 12.8 Contract fakes

| Fake | Serves | Used for |
|---|---|---|
| Role-file fixture | This story's own approved role file | The role, permission and conflict rows of AC1, and the failing rows of AC2 |
| rwb-case queue fake (RWB-P3-E1019-CON) | The queue schema that carries the `role_code` a queue row points at | Every test that resolves a role code for a queue row, from Day 1 (DP-11) |
| rwb-case reference-data fake (RWB-P3-E1043-CON) | `LOV-ROLE-CLASS`, `LOV-CAPABILITY` and `LOV-SCOPE` with a version | AC1, AC2 and AC4, so no list value is a constant in the test |
| Sign-in fixture | The group-to-role answer of ACE common | AC3 and AC6: synthetic users with the roles of each case, and the conflicting pair |

The queue rows and the member rows are never seeded here: the queue fake answers only the role code a row would point at.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 operations under `/api/recovery/access/v1` | 0 | OpenAPI 3.1, one hop, 2 s timeout, read only |
| Kafka | None | None | DP-09 is not applied; this story writes no decision record and no event, and the refusal entry is RWB-P4-E1039-APP's |
| Temporal | None | None | No workflow, activity or Schedule in this story |
| File | None | None | The approved role file is read at build and migration time, not at run time |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access.roles`, module `roles`, in the service root `th.co.scb.ace.workbench.recovery.access`. Service base `/api/recovery/access/v1`, schema `rwb_access`, topic `rwb.access.events.v1` (not produced here), Temporal task queue `rwb-access` (not used here).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This is a secondary slice and it adds no build dependency of its own: the metadata rows "Depends on (build)" stay None, exactly as this Work Package fixes them. DP-06 (the parameters client) and DP-14 (the topic naming library) are carried by the service baseline and this story uses neither at run time; DP-08 is the authorise contract behind the catalogue read, whose rights come from the caller's `permission` rows; DP-11 is the inbound one-hop budget of the two read operations and of the fake this story builds against; DP-07 is how the three lists are read; DP-15 is the migration of this story; DP-19 is the route behind SCR-43, which this story does not build. DP-03 is not a pattern of this slice: the refusal entry is the access-entry writer of RWB-P4-E1039-APP's.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `V1019_1__role_matrix.sql` | Migration | Writes the rows of the approved role file into `role`, `permission` and `role_conflict` at matrix version PM-2026.11 and the conflict version of the file; copies no ACE value and no person |
| RoleSetChecks | Service | The checks of BR2 over the file: class, unique code, area, scope, letters, conflict pair and required field |
| RoleCatalogueRepository | Repository | Reads `role`, `permission` and `role_conflict` in schema `rwb_access` at the version in force; no write method |
| RoleCatalogueService | Service | Assembles `Role[]`: role, class, default scope, permission rows, conflict pairs, matrix version and conflict version |
| SessionResolver | Service | Resolves the caller's roles from the sign-in claim and the `role` rows, the scope of those roles, the matrix version and the conflict state |
| ConflictCheckService | Service | Compares the caller's roles with `role_conflict` at the conflict version in force and refuses the sign-in with MSG-P4-006 |
| ReferenceListCatalog | Service | `LOV-ROLE-CLASS`, `LOV-CAPABILITY` and `LOV-SCOPE` through the reference-data contract of DP-07; no Java enum of classes, areas or scopes |
| RefusalDecision | Service | The refusal of a conflict or of a refused call, with its reason, passed to the access-entry writer of RWB-P4-E1039-APP; this story holds no record writer |

**Database and migrations**

- Writes `role`, `permission` and `role_conflict` in `rwb_access` by the migration of this story; reads them at the version in force.
- Migration `V1019_1__role_matrix.sql` sits on the per-service Flyway sequence after the V0001 baseline (DP-15). It adds the index the catalogue read needs on `permission (role_id, matrix_version)` if the baseline does not already hold it, and no other object.
- The read predicates are the matrix version in force on the day asked and the conflict version in force on the same day; both are version values, never dates written in code.
- The repository exposes no save, update or delete, so a read can never change a role, a permission or a conflict.
- DB access uses the per-service rwb-access login of the service baseline (DP-02). No grant on `rwb_case`, on `recovery` or on `public` is added by this story.

**Configuration and reference data**

- The role roster, the letters per area, the default scopes, the conflict pairs, the matrix version, the conflict version and the effective date are rows of the approved role file and of the migration; none is a constant in code.
- `LOV-ROLE-CLASS`, `LOV-CAPABILITY` and `LOV-SCOPE` are read with the version in force through the reference-data contract (DP-07).
- The approved role file is prepared by RW-REFADM and approved by RW-SECADM; its layout and the conflict version label are Not specified in the source documents (GAP-0985; ASM-1728).
- The effective date of a matrix version is read with the version, not with each row, because `role` and `permission` carry no date column — Not specified in the source documents (GAP-0985; ASM-1729).

**Build steps**

1. `V1019_1__role_matrix.sql` with the rows of the approved file for PM-2026.11, plus a fixture that applies it twice; test AC1.
2. RoleSetChecks with one check per rule and a failing fixture for each: unknown class, duplicate role and area, the letters RX, an unknown area, an unknown conflict code, an empty role name; test AC2.
3. RoleCatalogueRepository and RoleCatalogueService, with the catalogue answer and its two rights through the guard; tests AC4 and AC5.
4. ConflictCheckService over `role_conflict` and the refusal with reason ROLE_CONFLICT, passed to RWB-P4-E1039-APP's access-entry writer; test AC3.
5. SessionResolver with the union of the caller's roles, the scope of each role and the conflict state; test AC6.
6. Version resolution on a fixed clock with two versions and their effective dates; test AC7.
7. ReferenceListCatalog over the reference-data fake, so a new role class or capability area is accepted as data with no build (BR1).
8. The boundary check of AC8 on the module map, and the proof that no statement names a queue, membership or capacity table; the boundary rule itself is RWB-P4-E1069-APP's and stays green.

**Feature switch.** None. The catalogue and the session are read paths and always answer the version in force; a version is changed by rows and by its effective date, not by a flag.

**Done when.** The tests in section 16 pass; `role`, `permission` and `role_conflict` hold the rows of the approved file at PM-2026.11; the catalogue answers role, class, default scope, permissions and conflicts with the matrix version; a caller holding a conflicting pair is refused at sign-in with MSG-P4-006; a caller without the right is refused with MSG-P4-002; the session answers roles, scope, matrix version and conflict state; a second version answers from its own date with no deployment; and no statement in the service names a table outside `rwb_access`.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P1-002 | A role-set check fails on a row: class, duplicate row, letters, conflict pair | The {source} load for {date} was refused: {check}. The previous load is still in use. | The role-set checks, as a 422 with the failing rows in the problem detail |
| MSG-GEN-001 | A required field is empty, or an area or a scope is not in its list | Enter {field}. | The role-set checks |
| MSG-P4-001 | The token holds no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. | The guard, on both operations |
| MSG-P4-002 | The caller holds no Platform administration R for the administration view, or no Reference data R for the role read | You cannot {action} here. Your role does not include it. | The guard, on both operations |
| MSG-P4-006 | The caller holds both roles of a conflicting pair | Not specified in the source documents (GAP-0985; ASM-1730); the message ID and the pair are fixed, the text is not | The sign-in path and the session |
| MSG-P7-003 | The refusal entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | RWB-P4-E1039-APP's access-entry writer, to which this story passes the refusal |

Every error is an RFC 9457 problem response with `messageId` set and `detail` carrying the text with its placeholders filled. For MSG-P4-002 the {action} value names the action the caller tried — for example "read roles" — and never a case fact, a field value or an entitlement of another person. For MSG-P1-002 the {check} value is the name of the failed check and the {source} and {date} values are the role version and its effective date.

### 15. Screens and states

No screen is built by this story. SCR-43 Roles and access shows the roles, their permissions, their default scope and their conflicting pairs, and the security administrator and internal audit read it there; it is served by the gateway-bff composite route (DP-19), which calls this service for the catalogue in one hop and renders the rows. The screen fields and the rendering of a letter per area are the screen owner's, and this story returns the rows and the versions only.

The states the operator sees on a version are the states of the role version: the version in force with its effective date, a later version applied with a later effective date, and the rows of the older version still readable with their effective end date. A person holding a conflicting pair sees the refusal of the session and the pair named by MSG-P4-006, and no scope.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-019-13 | AC5, BR5, BR7 | Component | RW-PHONECOL, whose Platform administration letter is "-", calls GET /admin/roles and is refused with MSG-P4-002; the same refusal at the reference-load path is RWB-P3-E1019-APP's and the -ITG copy is RWB-ITG-E1019-ITG's |
| TC-E1-019-01 | AC1, BR1, BR12 | End to end | The approved role file for PM-2026.11 with the role codes of TSD P4 T6.1 and one permission row per role and capability area; the 12 queues and 48 member rows of the same legacy case are RWB-P3-E1019-APP's |
| TC-E1-019-02 | Rollback of a queue version: owned by RWB-P3-E1019-APP | End to end | QUEUE versions 2 and 3 of the rwb-case slice; this story proves only that a queue rollback leaves `role`, `permission` and `role_conflict` unchanged |
| TC-E1-019-03 | Capacity of a member: owned by RWB-P3-E1019-APP | End to end | Member U-11 with capacity 40 and 40 open cases in the rwb-case slice; no capacity answer exists in this service |
| TC-E1-019-04 | Unknown team code on a queue row: owned by RWB-P3-E1019-APP | End to end | Queue with team code XYZ in the rwb-case slice |
| TC-E1-019-05 | Cap outside its range: owned by RWB-P3-E1019-APP | End to end | Cap 0 in the rwb-case slice; the cap range comes from the rwb-case parameter, not from this story |
| TC-E1-019-06 | The author cannot approve a load: owned by RWB-P3-E1019-APP | End to end | A queue version loaded and approved by the same test user in the rwb-case slice; this story has no load and no approval path |
| TC-E1-019-07 | Rollback with no earlier version: owned by RWB-P3-E1019-APP | End to end | Only one queue version in the rwb-case slice |
| TC-E1-019-08 | The same queue file loaded twice: owned by RWB-P3-E1019-APP | End to end | Same file twice for 2026-12-15 in the rwb-case slice |
| TC-E1-019-09 | AC7, BR11 | End to end | Matrix versions PM-2026.11 and PM-2026.12 with effective dates 30 November and 1 December 2026, read on a fixed clock; the future valid-from case of the queue version is RWB-P3-E1019-APP's and the cross-service case is RWB-ITG-E1019-ITG's |
| TC-E1-019-10 | AC1, BR1 | Component | A member row that names role code RW-LITOFF: the check resolves RW-LITOFF from this catalogue; the member-role check itself is RWB-P3-E1019-APP's |
| TC-E1-019-11 | Overflow loop between two queues: owned by RWB-P3-E1019-APP | End to end | DS-BKK-CO and DS-BKK-OVF in the rwb-case slice; this service holds no overflow queue |
| TC-E1-019-12 | A required queue column empty: owned by RWB-P3-E1019-APP | End to end | Row 3 with no assignment method in the rwb-case slice; the required-field case of this story is AC2 |

The thirteen legacy TC IDs are kept, and each row names either the criterion of this story that the case answers or the slice that owns the legacy case. The Level column follows Template and Rules section R7.2: the legacy level System maps to End to end and the legacy level Access maps to Component. Every legacy test case of this key is listed above with the slice of the behaviour this story answers: TC-E1-019-13 answers the access refusal, which is the one legacy criterion that reaches the role half, and it is tested here on the catalogue instead of the load path; TC-E1-019-01 answers the role, permission and conflict rows of the version, while its queues and members are RWB-P3-E1019-APP's; TC-E1-019-09 answers the version in force on its effective date for the matrix, while the queue version is P3's; and TC-E1-019-10 answers the role code a member row points at, while the member-role check is P3's. The queue, membership, capacity, rollback, overflow and required-column cases — TC-E1-019-02 to TC-E1-019-08, TC-E1-019-11 and TC-E1-019-12 — are owned by RWB-P3-E1019-APP, and their -ITG copies by RWB-ITG-E1019-ITG; no `-ITG` id is written here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: role codes, role classes, capability areas, letters, default scopes, conflict pairs, matrix versions and effective dates are rows of the approved file, of `role`, `permission` and `role_conflict`, and of the lists; a test proves that a new role, area or class needs no build (BR1).
- No personal data anywhere: a role is a code, a conflict is a pair of codes, the refusal carries a user reference and no name, the entry is RWB-P4-E1039-APP's, and no test row, log or prompt holds a name or an e-mail address.
- No read of another schema (DP-01): the queue, membership, capacity, list and reference tables are rwb-case's and are never read by SQL; the lists arrive through the reference-data contract, and `partner_user` and `decision_log_entry` are not read at all.
- ACE data only through the owner's contract or its own `v_ace_*` views — and this service reads neither: the field IDs, the lists and the group-to-role answer reach it as codes, and boundary rule BND-6 of RWB-P4-E1069-APP stays green on this package.
- One writer for a role version: only this story's migration writes `role`, `permission` and `role_conflict`, and the read path has no write method, so a catalogue read can never change a permission.
- Default deny on every call: a missing role resolves to 401 and a missing letter to 403 with MSG-P4-002, never to allow (BR5).
- A version answers whole or not at all: a read during an application answers the old version or the new one, never a mixture, and open work keeps the version it was decided under (BR11, R-UNI-38).
- One migration per story on the service's own Flyway sequence (DP-15); an applied version is never edited, and a change is a new version with its own effective date.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-006 | Roles, teams, queues, queue membership and capacity are held as versioned reference data and change without a code release — the role half is answered here | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-06 | All recovery processes | R-UNI-38; CTL-08 | TC-E1-019-01, TC-E1-019-10 |
| REQ-ACA-002 | Roles are held as data, and a role change takes effect without a code release | Epic 1, 3.4; Program, 5.4 | FEAT-ACA-03, FEAT-ACA-04 | All recovery processes | BR-P4-003; BR-P4-004; R-UNI-38 | TC-E1-019-01, TC-E1-019-09, TC-E1-019-13 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P3-E1019-CON | Contract | C: the queue contract that carries the role code a queue row points at, with its fake |
| RWB-P3-E1019-APP, RWB-P3-E1019-DB | App development, ACE DB | Sibling slice: the queues, the membership, the capacity, the reference-load path and the rollback |
| RWB-P4-E1037-CON, RWB-PLT-E1037-CON | Contract | The service baseline contract and the guard library that carry the two rights |
| RWB-P4-E1069-APP | App development | The boundary rule BND-6 this package must stay green against |
| RWB-P4-E2013-APP, RWB-P4-E1038-APP | App development | The delegation of authority table and its lookup, which are a different half of the access model |
| RWB-ITG-E1019-ITG | Integration | The cross-service proof that one version is in force for the queue read, the role read and the notice |

| Legacy reference | Where it is kept |
|---|---|
| Role and permission rows, their class, scope and letters (legacy sections 1, 8 BR1 and BR9, section 11) | Sections 1, 4, 8, 11, 12.7 |
| The role list of TSD P4 T6.1 with its three capability letters | Sections 3, 7, 11 |
| Matrix versions PM-2026.11 and PM-2026.12 with 756 permission rows | Sections 3, 7 (AC7), 14 |
| The conflict pairs RW-SECADM with any business role, and RW-RISK with RW-REFADM | Sections 3, 5 (X7), 7 (AC3), 8 (BR3) |
| MSG-P1-002, MSG-GEN-001, MSG-P4-001, MSG-P4-002, MSG-P4-006 | Section 14, exception paths |
| R-UNI-38, CTL-08 and the separation-of-duty table | Sections 2, 8, 9, 17 |
| Field IDs DF-REF-034 to DF-REF-044, DF-REF-205 to DF-REF-211 | Section 11 |

### 19. Out of scope

- The queues, the queue membership, the queue measures, the capacity answer, the assignment methods and the overflow queue: RWB-P3-E1019-APP, with RWB-P3-E1019-CON and RWB-P3-E1019-DB.
- The reference-load path with its approve and rollback operations, the reference version store and the list read: rwb-case (P3) under ASM-0041 and ASM-0071; `lov_value` and the evaluation of a list are P3's.
- `partner_user`: rwb-partner (S9) under ASM-0072.
- `decision_log_entry` and the `rule_package*` tables: rwb-decision (P7) under ASM-0055 and ASM-0069.
- The delegation of authority table and its lookup: RWB-P4-E1038-APP and RWB-P4-E2013-APP.
- The scope and masking evaluation per case, and the PDPA field masking rows: RWB-P4-E1037-APP and RWB-P4-E1069-APP.
- The access log search and export: RWB-P4-E1039-APP; break-glass grants: the break-glass story of the same service.
- The sign-in, the multi-factor check and the group-to-role mapping: ACE common and Entra ID (INT-21); this story reads the roles a sign-in already holds.
- The role matrix load and approval path that brings a later version: RWB-P4-AD002-APP and RWB-P4-AD004-APP; this story seeds the version in force by migration and reads it.
- The six-monthly access review list (JOB-18): RWB-P4-AD008-APP.
- The -ITG copies of the test cases: RWB-ITG-E1019-ITG.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
