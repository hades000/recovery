# RWB-P4-E1065-APP Sandbox database with synthetic recovery data

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E1065-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-065 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP13, DP15, DP19 |
| Parallel lane | L-P4-AB |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P1-E1065-CON |
| Contract version | v1 (path /api/recovery/access/v1, section 7) |
| Contract fake library version | Not specified in the source documents (DOR-RWB-P4-E1065-APP-22) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (FR-P4-016, FR-P4-018, FR-P4-023) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-065 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E1065-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 30 cross-document, 9 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **security administrator (RW-SECADM), a reference data administrator (RW-REFADM) and a squad member with a Workbench role (RW-TRIBE)**, I want **the DEV sandbox to stand up the Recovery role list and the role to permission matrix in `rwb_access` from the same seed file on every rebuild, one synthetic test identity per role with no person name, the authorise answer and the resolved permission view those identities receive, and one local access entry per decision**, so that **every squad can build and test a role's read and action in DEV from the first day, before any role has a real user and with no production data**.

### 2. Business rationale

SIT reads the real ACE database and the real IAM groups; DEV has neither. Without a seeded role list and matrix, no squad can test a case read, a queue action or a refusal before a real user is mapped to a role, and every squad would ask the security administrator to create an identity by hand. The legacy story builds a sandbox database in DEV from the same DDL as SIT, fills both schemas with synthetic rows and, in step 8 of its flow, "loads the 54 roles, the permission matrix and one named test user per role"; legacy BR6 fixes the rule behind it (every role has a test user before it has real users, DL39) and legacy AC1 names the role and permission seeding in the same breath as the schema build.

This story is the rwb-access part of legacy RWB-E1-065. It carries the access seed and the access answers, not the database, the generator or the views: the DEV database `rwb_sandbox`, the ACE-shaped tables, the 92 recovery tables, the 30 `v_ace_*` views, the case volumes, the exception shapes, the dictionary-driven value factory, the verifier, the rename and the read-only grant on the sandbox belong to the rwb-source-data contract of this legacy key (RWB-P1-E1065-CON), the P1 and DB app stories of the same key, and the integration story RWB-ITG-E1065-ITG. What this slice owns is the part that answers for rwb-access: the `role` and `permission` rows the sandbox loads into `rwb_access`, one synthetic identity per role, and the two answers every other service and every screen gets from those rows at the matrix version in force.

rwb-access owns Recovery roles as data, scope, masking policy, the DoA table and the access log (Architecture v5 slide 41), and every other service asks it before a read or an action (slide 14: `POST /authorise`, cached). The seed is therefore the difference between a DEV environment where a role's rights exist only in a document and one where the authorise answer of every service is computed from rows. The seed writes role codes, capability areas, letters, a version label and synthetic identity keys only; it carries no person name, no account number and no identity number, so the sandbox keeps BR1 (no production data) and BR9 (no clear personal value outside the ACE-shaped tables) while giving DEV a usable policy pack.

The matrix this slice seeds is the access slice of the pack version in force: capability areas from LOV-CAPABILITY, letters C, R, U, D and A or a dash, scope from LOV-SCOPE, all rows at one matrix version. Loading and approving a pack in a running environment is the matrix story (RWB-P4-E1037-APP) and the pack load story (RWB-P4-AD002-APP); here the same file is written by a per-service migration so a fresh sandbox has the pack without a screen, and it meets REQ-RDF-001 (one owner per data product) and REQ-RDF-010 (access per data product by role, with personal data masked).

### 3. Preconditions

- The `rwb_access` baseline is in place: `role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit` exist at the platform migration version, and the local decision-record table is created by the decision-record library (DP-03).
- RWB-P4-E1037-CON is published — the authorise contract of rwb-access with `POST /authorise`, `GET /me/permissions` and the masking read — so this story answers an identity's rights behind a published shape. The request and answer field lists are Not specified in the source documents (GAP-0898; ASM-1619).
- RWB-P1-E1065-CON is published: the rwb-source-data contract of this legacy key, which fixes the DEV sandbox build, the database name `rwb_sandbox`, the seed value `20261128`, the order in which the per-service migrations run after the sandbox build, and the fixture the application tests run against (DP-11, C dependency).
- The access seed file — the legacy `roles.txt` and `Permissions` file of this key — is in the rwb-access repository as a migration resource. Its location, format, version label and row count are Not specified in the source documents (GAP-0895; ASM-1616); whether the DEV seed carries the SIT version label is also Not specified in the source documents (GAP-0895; ASM-1616).
- The matrix letters for the capability areas this seed fills are read from that file; the TSD P4 RBAC matrix tabulates only three of the 14 capability areas, so the letters of the other areas are Not specified in the source documents (GAP-0900; ASM-1621).
- The role count is the legacy 54; the TSD P4 RBAC matrix tabulates 42 role rows. The difference is Not specified in the source documents (GAP-0899; ASM-1620).
- The capability areas and scopes of the seed are the values of LOV-CAPABILITY (14 areas: CASE_RECORD, QUEUE_AND_ALLOCATION, TREATMENT_AND_OFFER, LITIGATION, ASSET_AND_DISPOSAL, DEBT_SALE, WRITE_OFF_AND_POSTING, DOCUMENTS, RULES_AND_PARAMETERS, REFERENCE_DATA, DECISION_LOG, PARTNER_PORTAL, REPORTING, PLATFORM_ADMINISTRATION) and LOV-SCOPE (OWN, TEAM, REGION, ALL), read through the reference-data contract of rwb-case (DP-07, C RWB-P3-E1043-CON).
- The DEV groups named in `role.entra_group` and one synthetic test identity per role are provisioned in the DEV directory by the sandbox build; who owns that list and when an identity is retired is Not specified in the source documents (GAP-0896; ASM-1617).
- The login is the rwb-access login (DP-02). The per-service login name and the DEV-only read-only role are Not specified in the source documents (GAP-0897; ASM-1618).
- The sign-in path that resolves directory groups to `role.entra_group` rows is RWB-P4-E1022-APP and RWB-P4-AD001-APP; this story neither serves nor changes it, and it reads no `v_ace_*` view and no `public` table (DP-05 applies here as a prohibition).

### 4. Flow

1. The sandbox build of RWB-P1-E1065-CON creates the DEV database `rwb_sandbox`, applies the ACE-shaped test double and the per-service migrations in order, and reaches the `rwb_access` migration step with an empty `role` and `permission`.
2. The rwb-access migration `Not specified in the source documents (CG-ALL-5116)` applies the access seed file in one transaction: the 54 `role` rows with role code, role name, role class, default scope and the DEV group name, then the `permission` rows with the role, the capability area, the letters and matrix version `PM-2026.12`.
3. The migration writes the same file on every rebuild, so the same seed value `20261128` and the same file give the same rows and the same counts; a row of the seed is never merged with a row of a different matrix version.
4. AccessSeedVerifier reads the written rows back: the role count, one matrix version on every permission row, every capability area against LOV-CAPABILITY and every scope against LOV-SCOPE through the reference-data contract, every letter in C, R, U, D, A or a dash, and every role with at least one permission row or an explicit dash.
5. TestIdentitySeeder records the DEV group of each role in `role.entra_group` and the sandbox build provisions one synthetic identity per role as a member of that group; the identity key carries the role code and a sequence and no person name.
6. A squad member signs in with the synthetic identity of the role being tested; the sign-in path of RWB-P4-E1022-APP resolves the directory groups to `role.entra_group` rows and holds the role set on the session.
7. rwb-access serves `GET /api/recovery/access/v1/me/permissions` for that identity: the role, its default scope, the matrix version in force and the letters per capability area, all read from `role` and `permission`.
8. rwb-access serves `POST /api/recovery/access/v1/authorise` for the read or the action the identity attempts: the letters of the area are unioned across the identity's roles, the scope test runs on the facts carried in the request, and the answer is `AC-READ` with matrix version `PM-2026.12` or a refusal with MSG-P4-002.
9. rwb-access writes one local access entry for the decision — decision code, actor, case ID when the decision is on a case, area, right, field IDs and the time — through the decision-record library, first in the transaction, and answers the caller.
10. The DEV sandbox has no Kafka, so no relay runs and no event leaves the sandbox; the entry stays in `rwb_access` and the DEV access-log read serves it. A squad that needs the entry in the central ledger uses the SIT environment built by RWB-ITG-E1065-ITG.
11. When the seed file changes, the next build writes the new rows at the new matrix version; the read-back of step 4 is the gate, and a role whose area has no row is refused by default, never allowed.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A seeded permission row names an area that is not in LOV-CAPABILITY, or a scope that is not in LOV-SCOPE | The sandbox build fails naming the row and the value; the previous sandbox stays in use | None (pipeline result) | AC1 |
| X2 | The same seed and the same file run twice | The same role rows and the same permission rows are written, with no duplicate and no row of another version | None | AC2 |
| X3 | A role has no permission row for an area, or the area holds a dash | The identity's action in that area is refused by default; nothing is allowed | MSG-P4-002 | AC5 |
| X4 | A test identity holds RW-REFADM and calls the case list | Refused before the case read, with one `AC-DENY` entry naming the area, the right and the result | MSG-P4-002 | AC5 |
| X5 | A seeded value matches a personal data pattern | The sandbox build fails naming the table and column; no sandbox is published from that build | None (pipeline result) | AC6 |
| X6 | The identity carries no Workbench role at all | Refused at the door of every endpoint; no case, queue or reference data is returned | MSG-P4-001 | AC3 |
| X7 | The local access entry cannot be written | The answer is 503 and no case data is returned; the decision is not taken on an unrecorded basis | MSG-P7-003 | AC7 |
| X8 | A reader holds the DEV read-only role and tries to change a seed row | The write is refused by the database; the row is unchanged | None (database error) | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the `rwb_access` baseline, the published authorise contract RWB-P4-E1037-CON and the RWB-P1-E1065-CON fixture. rwb-case's case list and reference data are contract fakes |
| Negotiable | Roles, areas, letters, scope, the matrix version and the seed file content are rows; the story fixes the migration, the verifier and the two answers, and names no role or letter in code |
| Valuable | Every role can be exercised in DEV from Day 1, with no person name and no production data, and every squad hears the same answer from rwb-access |
| Estimable | One migration, one seed file, one verifier, one identity seeder and two answers already on the contract |
| Small | Fits one sprint with its tests, as a secondary slice of the legacy key |
| Testable | Every criterion in section 7 is one automated test over the seeded schema, with every cross-service answer stubbed |

### 7. Acceptance criteria

```gherkin
Feature: Sandbox database with synthetic recovery data — the rwb-access seed and the access answers

  Background:
    Given the sandbox build uses seed 20261128
    Given the rwb-source-data contract mock returns the DEV sandbox build result for seed 20261128 with database "rwb_sandbox", schema "rwb_access" and the access seed file in the repository
    Given the rwb-case reference-data contract mock returns LOV-CAPABILITY with the 14 capability areas and LOV-SCOPE with "OWN", "TEAM", "REGION" and "ALL"

  Scenario: AC1 The access seed loads at one version (new, D-RCV-60)
    Given the access seed file holds 54 role rows and the role to permission matrix rows
    When the rwb-access migration runs in schema "rwb_access" after the baseline
    Then 54 rows are in "role", each with a role code, a role name, a role class from LOV-ROLE-CLASS, a default scope from LOV-SCOPE and a DEV group name
    And every permission row names a role of the seed, a capability area of LOV-CAPABILITY, its letters and matrix version "PM-2026.12"
    And every letter is "C", "R", "U", "D", "A" or a dash
    And the seed writes no person name, no account number and no identity number

  Scenario: AC2 The seed rebuild is idempotent (new, D-RCV-60)
    Given schema "rwb_access" holds the seed for seed 20261128 at matrix version "PM-2026.12"
    When the same migration and the same seed file run again in a rebuilt database
    Then the same 54 role rows and the same permission rows are present at "PM-2026.12"
    And no row is duplicated and no row of another matrix version is left in the schema
    And each role code, capability area and letter reads back character for character as in the seed file

  Scenario: AC3 One synthetic test identity per role (new, D-RCV-60)
    Given the sign-in path of RWB-P4-E1022-APP has resolved the groups of a synthetic identity to "role.entra_group" rows of "rwb_access"
    Given the seed names one DEV group per role in "role.entra_group" and the build provisions one synthetic identity per group
    When the identity "SYN-ID-RW-CASEOWN-01" calls GET /api/recovery/access/v1/me/permissions
    Then the answer names role "RW-CASEOWN", its default scope "OWN" and matrix version "PM-2026.12"
    And the same holds for each of the 54 roles, with one identity each and no role without an identity
    And no identity key carries a person name, an e-mail address or an identity number

  Scenario: AC4 The case list is granted to a role that holds the letter (new, D-RCV-60)
    Given the rwb-case contract mock returns the sandbox case list with case "RW-2026-000001"
    Given the identity "SYN-ID-RW-CASEOWN-01" holds role "RW-CASEOWN" with default scope "OWN" and owns case "RW-2026-000001"
    And the seed gives "RW-CASEOWN" the letter "R" in capability area "CASE_RECORD"
    When the caller asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R" and case "RW-2026-000001"
    Then the answer grants the read with decision code "AC-READ" and matrix version "PM-2026.12"
    And the case list is returned through the rwb-case contract
    And one local access entry is written with decision code "AC-READ", the actor, case "RW-2026-000001", area "CASE_RECORD", right "R" and the time

  Scenario: AC5 RW-REFADM is refused the case list (new, D-RCV-60)
    Given the rwb-case contract mock returns the sandbox case list
    Given the identity "SYN-ID-RW-REFADM-01" holds role "RW-REFADM" and matrix version "PM-2026.12" holds no CASE_RECORD row for it
    When the caller asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD" and right "R"
    Then the call is refused with status 403 and message MSG-P4-002 for action "open the case list"
    And no case row is returned and no account, party or document is read
    And one local access entry is written with decision code "AC-DENY", area "CASE_RECORD", right "R" and result "REFUSED"

  Scenario: AC6 No clear personal value in rwb_access (new, D-RCV-60)
    Given the seeded tables "role", "permission" and the local access entries
    When the verifier scans every column of schema "rwb_access" tagged is_personal, and every seeded text column, for the national ID, mobile number and e-mail patterns
    Then the build passes with no match, because the seed writes role codes, capability areas, letters, the matrix version, DEV group names and synthetic identity keys only
    And a clear identity number in the ACE-shaped tables is not a failure of this slice, because those tables are the ACE test double and belong to RWB-P1-E1065-CON
    And no sandbox is published from a build in which a seeded access value matches a personal data pattern

  Scenario: AC7 One local access entry per decision, with no relay (new, D-RCV-60)
    Given the DEV sandbox runs with no Kafka broker and no relay
    When two decisions are served for one identity, an "AC-READ" and an "AC-DENY"
    Then two entries are written through the decision-record library, each with its sequence number, its previous hash and its entry hash
    And the entry is written before the answer, and a failed write answers 503 with MSG-P7-003 and returns no case data
    And no topic is produced to and no consumer group is created by this schema in the sandbox

  Scenario: AC8 The DEV read-only role reads the seed and cannot change it (new, D-RCV-60)
    Given the DEV-only read-only role over the sandbox
    When a member of that role runs "SELECT role_code, default_scope FROM rwb_access.role" and then an UPDATE on the same row
    Then the read returns the 54 role rows
    And the UPDATE is refused by the database and the row is unchanged
    And the role holds no SELECT on the local access-entry table, so the access log cannot be read with it

  Scenario: AC10 The schema boundary holds and every role has a test identity (new, D-RCV-60)
    Given the rwb-access migration has run in schema "rwb_access" and the DEV sandbox runs with no Kafka broker
    When the boundary check lists every table and view that the access answers read and every object the sandbox creates
    Then every read and every created object is in schema "rwb_access" and no "v_ace_*" view, no "public" table and no table of another service appears
    And no Kafka broker is in the DEV profile and no topic is created by this schema
    And every role of the seed has one synthetic test identity whose key carries no person name

  Scenario: AC11 The provided operations answer 401 without an identity and 404 for a path not provided (new, D-RCV-60)
    Given the sign-in path of RWB-P4-E1022-APP and the provided operations POST /api/recovery/access/v1/authorise and GET /api/recovery/access/v1/me/permissions
    When the caller calls GET /api/recovery/access/v1/me/permissions with no identity
    Then the answer is status 401 and no role, permission or case row is returned
    And a call to a path under /api/recovery/access/v1 that is not provided is answered with status 404 and no role, permission or case row is returned
```

The ten criteria above are new and test only this deliverable: the access seed, the synthetic identities and the two answers rwb-access gives from the seeded rows, including the legacy access case TC-E1-065-10 (a test identity holding RW-REFADM is refused the case list with MSG-P4-002). The legacy criteria AC1 to AC9 of RWB-E1-065 are owned elsewhere: the schema, the dictionary, the case volumes, the exception shapes and the verifier by the rwb-source-data and DB stories of the same key (RWB-P1-E1065-CON and RWB-P1-E1065-APP); only legacy AC1's role and permission seeding sentence, legacy BR6 and legacy BR9 are answered here. No legacy criterion text is copied into this section.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | No production data in DEV: the DEV sandbox holds synthetic rows only, and the access seed holds role codes, letters and synthetic identity keys (legacy BR1) | NFR-045; CTL-11; legacy BR1 |
| BR2 | Every role has a test identity before it has real users, and the identity carries no person name (legacy BR6) | DL39 (ASM-1617, ASM-2705); legacy BR6 |
| BR3 | A clear identity number is allowed only in the ACE-shaped tables; `rwb_access` holds no clear personal value at all (legacy BR9) | D-RCV-35 U4; CTL-11; legacy BR9 |
| BR4 | Roles, capability areas, letters, scope and the matrix version are data rows with a version; no role code, area, letter or scope value is written in code | FSD P4 A2.3, A2.4; BR-P4-003, BR-P4-004; TSD P4 T3.2 |
| BR5 | The same seed and the same seed file give the same rows on every rebuild, and a rebuild never mixes two matrix versions | Legacy RWB-E1-065 AC5; TSD P4 T3.1 (matrix_version) |
| BR6 | The authorise answer is served only from `role` and `permission` at the matrix version in force; a capability area with no letter, and a role with no permission row, are refused (default deny) | FSD P4 A2.4; VR-P4-004-1; legacy TC-E1-065-10 |
| BR7 | rwb-access writes only its own schema: no `v_ace_*` view, no `public` table and no other service's table is read by this story, and the DEV groups reach it from the sign-in path of RWB-P4-E1022-APP | Architecture v5 slides 13, 14 and 41; DP-01, DP-05 |
| BR8 | The sandbox has no Kafka: the access entry is a local decision record written through the decision-record library, with no relay and no topic in the DEV profile (DP-09 is not a pattern of this story) | FSD P4 A2.8; DP-03; Architecture v5 slide 20 |
| BR9 | The DEV-only read-only role reads the seed and never changes it, and holds no read on the local access-entry table | Legacy RWB-E1-065 AC2, section 10; TSD P4 T6.2 |
| BR10 | The DEV matrix version is one label on every permission row of the seed; a row of a previous version is not carried into the sandbox | TSD P4 T3.1 (permission.matrix_version); FSD P4 A2.4 AC-P4-004-01 (version "PM-2026.12") |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| no `role` or `permission` row in `rwb_access` | the rwb-access migration runs | The sandbox build reaches the access step with the seed file present | 54 role rows and their permission rows at matrix version `PM-2026.12` |
| rows at `PM-2026.12` | the same migration and the same seed file run again | A rebuilt database with seed `20261128` | the same rows at `PM-2026.12`, no duplicate and no row of another version |
| a role with a letter in the area | an authorise request | The area and right are covered and the scope test passes | `AC-READ`, and one local entry written |
| a role with no letter in the area, or with a dash | an authorise request | The area or right is asked for | refused by default with MSG-P4-002, and one `AC-DENY` entry written |
| a synthetic identity of a role | the role receives its first real user | The release that gives the role a screen (DL39) | the identity is retired from the DEV group by its owner; the seeded role and permission rows do not change |

A `role` and a `permission` row have no lifecycle of their own: rwb-access holds no case state machine, and the module acts on events from rwb-case and writes through the decision log (TSD P4 T4). The pack version states LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED and ROLLED_BACK belong to the load path (TSD P4 T3.2 LOV-VERSION-STATUS, T4) and to the pack load story RWB-P4-AD002-APP; this story writes one label and reads it back, and never promotes a version.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-access service identity (the rwb-access login, DP-02) | Runs the seed migration, reads `role` and `permission`, serves the authorise answer and the resolved permission view, and writes the local access entry |
| Decision-record library identity | Writes the local access entry with its sequence and hash link; no relay runs in the sandbox (DP-03) |
| RW-SECADM, security administrator | Owns the role list and the matrix as data: approves a new version of the seed file, and reads the seeded rows and the access entries of the sandbox |
| RW-REFADM, reference data administrator | Prepares the seed file and the change checklist; no approval, and in the sandbox an identity holding RW-REFADM holds no CASE_RECORD letter, so the case list is refused with MSG-P4-002 |
| RW-TRIBE, tribe lead and squad members | Sign in with the synthetic identity of a role and exercise a read or an action in DEV against the seeded rows |
| RW-PLATADM, platform administrator | Owns the DEV identity list behind `role.entra_group` and the retirement of an identity when the role receives its first real user |
| RW-AUDIT, internal audit | Reads the local access entries of the sandbox with scope ALL; the read-only DEV role holds no access to them |

The per-service login name and the DEV-only read-only role are Not specified in the source documents (GAP-0897; ASM-1618); the story keeps the legacy name `rwb_sandbox_read` for the read-only role and "the rwb-access login (DP-02)" for the service. The roles, areas and letters above are rows of the seed and are not fixed in code; no role in this story may grant itself a letter.

### 11. Data

| BR Field ID | Entity in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-038 | role | id, role_code, role_name, role_class, default_scope | Write (seed), then Read |
| DF-REF-035 | role | role_code | Write (seed), then Read |
| DF-REF-038 | role | default_scope | Write (seed), then Read |
| DF-REF-039 | role | entra_group (the DEV group of the synthetic identity) | Write (seed), then Read |
| DF-REF-040 to DF-REF-044 | permission | id, role_id, capability_area, letters, matrix_version | Write (seed), then Read |
| DF-REF-042 | permission | capability_area | Write (seed), then Read |
| DF-REF-043 | permission | letters | Write (seed), then Read |
| DF-REF-044 | permission | matrix_version | Write (seed), then Read |
| DF-DEC-001 to DF-DEC-018 and DF-DEC-028 to DF-DEC-031 | local access entry (decision record) | decision code, actor, case ID, actions, decided at, chain sequence and hash link | Write |
| DF-DEC-002 | local access entry (decision record) | case_id (empty only for a decision with no case) | Write |
| DF-DEC-003 | local access entry (decision record) | decision_code | Write |
| DF-DEC-014 | local access entry (decision record) | actions (area, right, field IDs, result) | Write |
| DF-DEC-030 | local access entry (decision record) | actor_user_id (the synthetic identity key) | Write |
| LOV-CAPABILITY, LOV-SCOPE, LOV-ROLE-CLASS | reference data of rwb-case (not a `rwb_access` table) | the 14 capability areas, the four scopes, the three role classes | Read through the reference-data contract (DP-07); no `lov_value` row is written here |

The seed writes the 54 roles and their permission rows and nothing else: no case row, no ACE row, no `lov_value` row, no `masking_rule` row, no `delegation_limit` row and no `role_conflict` row is loaded by this story. The synthetic identities are not a `rwb_access` table — the seed records the DEV group of each role in `role.entra_group` (DF-REF-039) and the directory holds the identity, so no identity, person name or credential is stored in the schema. `delegation_limit` stays empty until its own load story runs (legacy section 11). Field IDs are those in the Logical Data Model and Data Dictionary v9.

### 12. Contract

#### 12.1 REST operations provided

None new. The two answers are served through the operations of RWB-P4-E1037-CON on base `/api/recovery/access/v1`; owner rwb-access (P4). This slice adds no path, no query parameter and no response field, and answers the following behind them:

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/authorise` | Decide a role's read or action for a capability area, a case and a field list, from the seeded matrix, with one local access entry | Any authenticated caller with a Workbench role | Idempotent by identity, area, right, case reference and field list within the cache window |
| GET | `/me/permissions` | The identity's resolved roles, default scope, matrix version and the letters per capability area | Authenticated caller, own record only | Not applicable |

Request for `/authorise`: the caller identity from the session, the capability area, the right, the case reference and the field IDs. Answer: the decision code (`AC-READ` or `AC-DENY`), the matrix version, the scope result and the access-entry reference. Errors: 401 no Workbench role (MSG-P4-001), 403 no letter for the area or right (MSG-P4-002), 404 a case outside the caller's scope (MSG-P4-003), 503 the access entry cannot be written (MSG-P7-003). The field names of the request and the answer are Not specified in the source documents (GAP-0898; ASM-1619).

The masking read, the DoA read, the role read `GET /admin/roles`, the access-log search `GET /admin/access-log`, the session read `GET /me/session` and the reference loads are P4 surface delivered by other P4 stories (RWB-P4-E1037-APP, RWB-P4-E1038-APP, RWB-P4-E1039-APP, RWB-P4-E1022-APP, RWB-P4-AD002-APP, RWB-P4-AD011-APP); this story adds none of them and changes no shape of any of them.

This story publishes no contract of its own; its contract dependency is RWB-P1-E1065-CON, and no contract story of this key is required.

#### 12.2 REST operations consumed

None at run time. This story answers from its own seeded rows, calls no service and reads no ACE view or ACE table (DP-01, DP-05 as a prohibition).

Two contracts are consumed as fixtures only. RWB-P1-E1065-CON fixes the DEV sandbox build this seed runs inside: database `rwb_sandbox`, seed `20261128`, the migration order and the fixture the application tests run against. The rwb-case case list and the rwb-case reference data are the mocks of AC4 and AC5 and of AC1, so the story builds and proves the grant and the refusal before rwb-case is live in DEV.

#### 12.3 Events published

None. The DEV sandbox has no Kafka broker, so nothing is produced and no outbox relay runs: the access entry of this story is a local decision record written through the decision-record library, and DP-09 is not a pattern of this story. In a running environment the access entry is relayed as `DecisionRecorded` (EV-08) on `rwb.decision-record.v1`, which is the behaviour of the authorise story RWB-P4-E2007-APP and of the P7 ledger story; here the entry stops in `rwb_access`. `AccessPolicyChanged` on `rwb.access.events.v1` is raised by the load path (RWB-P4-AD002-APP) when a pack version goes in force, not by this seed.

#### 12.4 Events consumed

None. A migration consumes no topic; the seed is the file, not a subscription, and the sandbox profile wires no consumer group into `rwb_access`.

#### 12.5 Workflows and activities

None. The seed is a migration and the two answers are synchronous REST calls in the caller's thread; this story runs no workflow, starts no activity and holds no Temporal worker of its own (Temporal and Drools design, this story runs no workflow).

DP-04 applies as a prohibition here: rwb-access evaluates no decision table for this story, the letters of a capability area are rows, and no DRL, workbook or rule package is written by the seed.

#### 12.6 Schedules

None. The only Schedule of rwb-access is the six-monthly access review list (JOB-18), which belongs to RWB-P4-AD008-APP (Architecture v5 slide 44). The sandbox build stage that calls this migration is a pipeline stage owned by RWB-P1-E1065-CON, not a Schedule of this service.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| role | P4 (`rwb_access`) | Recovery roles as data, with role class, default scope and the DEV group name |
| permission | P4 (`rwb_access`) | Capability area, letters and matrix version per role; the seeded matrix |
| local access entry (decision record) | P4 rows in `rwb_access`, written through the P7 decision-record library | One entry per decision in the DEV sandbox, with no relay |
| masking_rule, role_conflict, delegation_limit | P4 (`rwb_access`) | Same service, not written by this story; their load stories own the rows |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_access` | Present in the schema but not written by this story, because no event leaves the sandbox (DP-09 is not a pattern here) |

rwb-access reads no table of another service and holds no foreign key across services (DP-01); `lov_value` and the reference tables belong to rwb-case (P3) and reach this story only through the reference-data contract (DP-07); the central ledger copy of the access entries is written in `rwb_decision` from the topic by RWB-P7-E1027-CON and is out of this slice.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P1-E1065-CON fixture | The P1 contract of this legacy key | The DEV sandbox build result for seed `20261128`: database `rwb_sandbox`, schema `rwb_access` after the baseline, the migration order and the access seed file in the repository |
| rwb-case case-list mock | AC4 and AC5 | The sandbox case list with case `RW-2026-000001`, and a refusal path that returns no case row |
| reference-data fake (RWB-P3-E1043-CON) | DP-07 | LOV-CAPABILITY with the 14 areas, LOV-SCOPE with OWN, TEAM, REGION and ALL, LOV-ROLE-CLASS with BANK_USER, PARTNER_USER and NON_HUMAN_ACTOR |
| RWB-P4-E1037-CON fake | The P4 authorise and permission contract | `/authorise` and `/me/permissions`, with a granted identity and a refused identity |
| decision-record library stub | DP-03 | A local chain that accepts the entry, and a stopped chain for the 503 path (AC7) |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 0 consumed | Both operations are the published contract of RWB-P4-E1037-CON on `/api/recovery/access/v1`; no outbound call and one hop within 2 s on the inbound call |
| Kafka | None | No topic produced and none consumed in the DEV sandbox; the access entry is a local decision record with no relay (DP-03, and DP-09 is not a pattern of this story) |
| Temporal | None | No workflow, no activity and no Schedule in this story |
| File | None | The seed file is a migration resource of the repository, not a file interface; no claim-check file is read or written |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `seed`, Java package `th.co.scb.ace.workbench.recovery.access.seed`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This is a secondary slice: it adds no new build dependency of its own. Metadata "Depends on (build)" stays `None` and "Contract dependencies" stays `RWB-P1-E1065-CON` exactly as the Work Package fixes them, and the platform contract libraries of DP-03, DP-04, DP-07, DP-15 and DP-19 arrive with the baseline, not with this story. DP-05 applies as a prohibition (the seed reads no ACE view and no `public` table, and no ACE-shaped row is written), DP-04 as a prohibition (no decision table and no DRL in this service), DP-15 as the per-service Flyway sequence that carries the seed, DP-13 as the base of the two answers, and DP-19 as the route on which SCR-43 Roles and access will show the seeded rows when it arrives.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AccessSeedLoader | Service | Applies the seed file in one transaction: the 54 `role` rows and their `permission` rows at one matrix version; refuses a row whose area, scope, class or letters are outside their list |
| SeedFileReader | Service | Parses the access seed file (the legacy `roles.txt` and `Permissions` file); holds no role code, area or letter of its own |
| AccessSeedVerifier | Service | Reads the written rows back: role count, one version per permission row, area against LOV-CAPABILITY, scope against LOV-SCOPE, letters format, and the personal-data pattern scan of the seeded columns |
| TestIdentitySeeder | Service | Records the DEV group of each role in `role.entra_group` and asserts one synthetic identity per group, with an identity key that carries the role code and no person name |
| MePermissionReader | Service | Answers `GET /me/permissions` from `role` and `permission`: the role set, the default scope, the matrix version and the letters per area |
| AuthoriseAnswerReader | Service | Answers `POST /authorise` from the seeded rows: union of the letters across the identity's roles, the scope test on the request facts, and `AC-READ` or `AC-DENY` |
| AccessEntryWriter | Service | Writes the local access entry through the decision-record library, first in the transaction, with no relay |

**Database and migrations**

- Writes `role`, `permission` and the local access entry in schema `rwb_access`; writes no other table and reads no other schema (DP-01).
- Migration in this story: `V1065_1__access_seed.sql`, the versioned per-service Flyway migration that carries the seed file's rows into `role` and `permission`, run after the `rwb_access` baseline. Its companion `R__access_seed_rebuild.sql` is the repeatable migration that re-applies the same file, so a rebuild of the sandbox writes the same rows (AC2). No column, index or constraint is added for case, ACE or identity data; the synthetic identities live in the directory, not in the schema.
- The seed is idempotent by construction: the repeatable migration writes the rows of the file it is given, deletes nothing outside the matrix version it writes, and refuses a row that belongs to two versions of the same role and area.
- No row of `masking_rule`, `role_conflict` or `delegation_limit` is written by this story, and no `lov_value` row is written at all.

**Configuration and reference data**

- `rwb.access.seed-file` names the migration resource that holds the seed file; its path and format are Not specified in the source documents (GAP-0895; ASM-1616).
- `rwb.access.matrix-version` is the label written on every permission row; the value the sandbox loads is `PM-2026.12`, the version the access examples of FSD P4 A2.4 load, and whether the DEV seed must carry the same label as SIT is Not specified in the source documents (GAP-0895; ASM-1616).
- `rwb.access.seed.identity-prefix` is the prefix of the synthetic identity key; the key format follows the legacy synthetic convention `SYN-` and is Not specified in the source documents (GAP-0896; ASM-1617). The owner of the DEV identity list is Not specified in the source documents (GAP-0896).
- The roles, areas, letters and scopes are rows of the seed file; the area and scope values are compared with LOV-CAPABILITY and LOV-SCOPE read through the reference-data contract of rwb-case (DP-07), and a `rwb_access` copy of a list is never kept.
- The login is the rwb-access login (DP-02); the DEV-only read-only role name is Not specified in the source documents for the target schema (GAP-0897; ASM-1618), and its grants are those of the DEV grant script in build step 7, on `rwb_access` only.
- The feature switch is `rwb.access.sandbox-access-seed`, read as a parameter: on in the DEV profile only; off means the seed does not apply and every authorise request is refused closed with MSG-P4-002, never allowed by default.

**Build steps**

1. SeedFileReader and AccessSeedLoader over the seed file, with a test per list violation (an unknown area, an unknown scope, an invalid letter) and a test that no role code, area or letter appears in the Java source.
2. `V1065_1__access_seed.sql` and `R__access_seed_rebuild.sql`, with the read-back of AC1 and the same-seed test of AC2.
3. AccessSeedVerifier with the role count, the single matrix version, the area and scope comparison through the reference-data fake, and the personal-data pattern scan; tests for AC1 and AC6.
4. TestIdentitySeeder over `role.entra_group`, with one identity per role and the no-person-name check; tests for AC3.
5. MePermissionReader and AuthoriseAnswerReader over the seeded rows, with the granted path, the default-deny path and the missing-role path; tests for AC3, AC4 and AC5.
6. AccessEntryWriter with the entry before the answer, the `AC-READ` and `AC-DENY` codes, the local chain and the 503 when the record cannot be written; tests for AC4, AC5 and AC7.
7. The DEV grant script for the read-only role: SELECT on `role` and `permission` only, no UPDATE, no SELECT on the access-entry table; test for AC8.
8. Contract-fake run of RWB-P1-E1065-CON, the rwb-case case list and the reference data, so the story builds and proves every answer before rwb-case and rwb-source-data are live in DEV.

**Feature switch.** `rwb.access.sandbox-access-seed`, read as a parameter; off refuses closed and seeds nothing.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P4-E1037-CON and RWB-P1-E1065-CON stay green, a rebuilt DEV sandbox carries the same 54 role rows and permission rows at one matrix version, every role has one synthetic identity that carries no person name, an identity holding RW-REFADM is refused the case list with MSG-P4-002, and no column of `rwb_access` holds a clear personal value.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No Workbench role on the token | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | The area or the right is absent for the identity's roles | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is absent or outside the identity's scope | This case is not in your scope. |
| MSG-P7-003 | The local access entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

Seed failures are reported in the pipeline result with the table, the row and the value named; no user message applies. For MSG-P4-002 in this story, {action} names the action the identity tried — for example "open the case list" — and never a case fact or a role name.

### 15. Screens and states

No screen in this story. SCR-43 Roles and access — roles, permissions, scope and the group mapping, with the access log, first in E8 and by file load before (FSD P4 Screens) — will show the rows this seed writes, and the seeded identities make that screen demonstrable in DEV before a real user exists; the screen itself belongs to the administration stories and to RWB-P4-E1022-APP. The SCR-43 states are empty, loading, error and no access; Screen Specifications v1 gives no content for them, so their presentation is Not specified in the source documents (CG-ALL-5118).

Both answers reach a screen only through the gateway-bff composite route (DP-19), which calls rwb-access for the decision and each owner service for its own data, one hop each. The route specification and the field-level masking of the composite route are Not specified in the source documents (GAP-0898; ASM-1619).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-065-01 | AC1, AC3, BR4, BR5 | End to end | The access seed file; 54 roles; matrix version `PM-2026.12`; one synthetic identity per role; the seeded schema read back |
| TC-E1-065-02 | AC2, BR9 | End to end | The DEV read-only role: SELECT on `role` and `permission`, a refused UPDATE, and no SELECT on the access-entry table |
| TC-E1-065-03 | No criterion here; the dictionary-driven build belongs to RWB-P1-E1065-CON | End to end | A test migration adding `recovery_case.risk_tier` with its dictionary row and list LOV-RISK-TIER |
| TC-E1-065-04 | No criterion here; the build gate on a missing dictionary entry belongs to RWB-P1-E1065-CON | End to end | A dictionary fixture without the row for `recovery_case.closure_reason` |
| TC-E1-065-05 | AC5, BR5, BR10 | End to end | Two builds for commit `a1b2c3d` and seed `20261128`; the same 54 role rows and permission rows at `PM-2026.12` |
| TC-E1-065-06 | No criterion here; the empty-list failure belongs to RWB-P1-E1065-CON | End to end | An empty LOV-PRODUCT seed |
| TC-E1-065-07 | AC7, BR1, BR3 | End to end | A 13-digit value injected in an ACE-shaped table (allowed) and in a seeded `rwb_access` column (fails); the pattern scan of the seed |
| TC-E1-065-08 | No criterion here; the boundary accounts belong to RWB-P1-E1065-CON | End to end | Accounts at 89 and 90 days past due, set through the rwb-source-data contract fake (§12.8) |
| TC-E1-065-09 | AC9 for the same-seed result; the build lock itself belongs to RWB-P1-E1065-CON | End to end | Two builds started together |
| TC-E1-065-10 | AC4, AC5, BR6 | Component | The identity `SYN-ID-RW-REFADM-01` holding RW-REFADM calls the case list through the rwb-case mock; refused with MSG-P4-002 and one `AC-DENY` entry; `SYN-ID-RW-CASEOWN-01` is granted the same read |
| TC-E1-065-11 | AC7 | Component | The authorise call of AuthoriseAnswerReader: the access entry written before the answer with the `AC-READ` and `AC-DENY` codes and the local chain; a forced write failure answer is Not specified in the source documents (CG-ALL-5114) |
| TC-E1-065-12 | No criterion here; the operations of §12.1 | Component | The contract fakes of RWB-P4-E1037-CON and RWB-P1-E1065-CON; the `POST /authorise` and `GET /me/permissions` answers checked against the operation shapes |
| TC-E1-065-13 | No criterion here; the table boundaries of §12.7 (ASM-3438) | Component | The seed at 54 role rows; one row that belongs to two matrix versions of the same role and area, refused |
| TC-E1-065-14 | AC10, BR2, BR7, BR8 | Component | Not specified in the source documents (NEWAC-RWB-P4-E1065-APP-AC10) |
| TC-E1-065-15 | AC11 | Component | Not specified in the source documents (NEWAC-RWB-P4-E1065-APP-AC11) |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end, Access to Component and Resilience to NFR. Every legacy test case of this key is listed above with the slice of the behaviour this story answers — the access seed, the identities and the two answers for TC-E1-065-01, TC-E1-065-02, TC-E1-065-05, TC-E1-065-07, TC-E1-065-09 and TC-E1-065-10, and no criterion for the build-side cases; the -ITG copies of these cases are not here — they belong to RWB-ITG-E1065-ITG, which proves the same values across rwb-source-data, rwb-access, rwb-case and the DEV environment end to end.

### 17. Guardrails

- No business value in code: roles, capability areas, letters, scopes, the matrix version, the seed file path and the identity prefix are rows, parameters or the seed file itself. No role code, area or letter appears in Java, and the verifier fails a build whose seed names an area or scope outside its list.
- No personal data in events, logs, workflow inputs, tests or prompts. This story writes role codes, areas, letters, the version, DEV group names and synthetic identity keys only (`SYN-ID-RW-CASEOWN-01`, case `RW-2026-000001`); no person name, no address, no identity number and no account number is written, and the pattern scan blocks a value that looks real anywhere in `rwb_access`.
- ACE data only through the owner's contract or the owner's `v_ace_*` views — and this story reads neither: no `v_ace_*` view and no `public` table is read by the seed, the verifier or the two answers, and the ACE-shaped tables of the sandbox belong to RWB-P1-E1065-CON.
- No cross-schema read: `rwb_access` holds no foreign key into another schema and no copy of a case, a list value or an ACE row (DP-01); the reference lists arrive through the reference-data contract (DP-07) and the case facts arrive in the authorise request.
- No event leaves the sandbox: the access entry is a local decision record written through the decision-record library, with no relay and no topic in the DEV profile (DP-03, and DP-09 is not a pattern of this story); the entry is written before the answer, and a failed write means 503 and no data shown.
- One evaluator per concern: rwb-access writes no DRL, no workbook and no rule package for this story, and the capability letters are rows, not a decision table (DP-04 applies as a prohibition).
- The seed is a per-service Flyway migration in `rwb_access`, versioned and repeatable, and no migration of this service touches another service's schema or the shared baseline (DP-15).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-001 | 14 data products, each with one system of record and one owner, each reachable in DEV without a request to another team | Business Requirements Epic 1, sections 3.1 and 4 | None | All recovery processes | DL15 (ASM-5264), DL16 (ASM-1094, ASM-5264); D-RCV-35; legacy BR5, BR6 | TC-E1-065-02, TC-E1-065-03, TC-E1-065-06 |
| REQ-RDF-010 | Access per data product by role; personal data masked in line with PDPA | Business Requirements Epic 1, sections 3.1 and 4; Program section 6.7 (NFR-045) | FEAT-ACA-03, FEAT-ACA-04, FEAT-ACA-07 | All recovery processes | CTL-11; D-RCV-35 U4; DL39 (ASM-1617, ASM-2705); legacy BR1, BR6, BR9 | TC-E1-065-01, TC-E1-065-02, TC-E1-065-06, TC-E1-065-10 |

The supporting features of the access model are FEAT-ACA-03 (the role to permission matrix as data), FEAT-ACA-04 (roles as data) and FEAT-ACA-07 (every access event to the access log), which the FSD P4 module pairs with its own requirements in RWB-E1-037 and RWB-E1-039; this slice answers them only for the DEV sandbox seed and the two answers it serves, and changes neither matrix nor log design. The -ITG copies of the test cases are carried by RWB-ITG-E1065-ITG.

### 19. Out of scope

- The DEV database `rwb_sandbox`, the ACE-shaped test double for the 22 Tier 1 and 14 Tier 2 tables, the 92 recovery tables, the 30 `v_ace_*` views and their grants: the rwb-source-data contract and app stories of this key (RWB-P1-E1065-CON and RWB-P1-E1065-APP) and the DB story of the same key.
- The generator, the value factory, the data dictionary reads, the case volumes, the exception shapes, the verifier of the whole sandbox, the pipeline stage, the database rename and the read-only grant on schema `recovery`: RWB-P1-E1065-CON and RWB-P1-E1065-APP.
- The end-to-end proof of these values across the sandbox, rwb-access, rwb-case and the ACE views: RWB-ITG-E1065-ITG.
- Loading and approving a matrix version in a running environment, and the masking policy: RWB-P4-E1037-APP and RWB-P4-AD002-APP; the masking rules and their version: the masking design of RWB-P4-E1037-APP.
- The DoA table and its rows: RWB-P4-E1038-APP and RWB-P4-E2013-APP.
- The role, permission and group-mapping screen (SCR-43 Roles and access), the access-log search, the break-glass grant and the access review list: the administration stories, RWB-P4-E1022-APP, RWB-P4-E1039-APP, RWB-P4-AD006-APP, RWB-P4-AD007-APP and RWB-P4-AD008-APP.
- The sign-in path, the directory group mapping and the separation-of-duty check: RWB-P4-E1022-APP, RWB-P4-AD001-APP and RWB-P4-AD005-APP; the DEV directory accounts themselves are provisioned outside this story.
- The relay of the access entry to the central ledger and the SIT access log: RWB-P4-E2007-APP and RWB-P7-E1027-CON.
- The `rwb_access` schema baseline, the platform migration role, the `rwb.decision-record.v1` topic and consumer groups, the observability and the runbook of this service.
