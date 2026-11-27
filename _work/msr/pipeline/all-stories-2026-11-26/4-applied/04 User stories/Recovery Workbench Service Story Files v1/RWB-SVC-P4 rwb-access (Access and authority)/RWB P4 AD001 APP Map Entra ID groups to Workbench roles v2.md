# RWB-P4-AD001-APP Map Entra ID groups to Workbench roles

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-001 for rwb-access — the group-to-role mapping held as dated data rows in `rwb_access`, with its maintenance operations. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-AD001-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-AD001-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-001 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP13, DP19 |
| Parallel lane | L-P4-A |
| Ready to start | After RWB-P4-E1022-APP |
| Depends on (build) | RWB-P4-AD001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-N001-CON, RWB-P4-E1022-APP |
| Contract dependencies | RWB-P3-E1042-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **security administrator**, I want **each Entra ID group mapped to one Workbench role in each environment as a data row**, so that **a person gets their roles from the group the bank IAM grants, with no code change**.

This is the rwb-access slice of legacy RWB-AD-001, and it is the mapping half of that legacy key: the mapping rows as data, their version with a valid-from date, and their maintenance.

- **Service naming:** REST base `/api/recovery/access/v1` (DP-13), schema `rwb_access`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery` (not used here — this story starts no workflow), Java package `th.co.scb.ace.workbench.recovery.access`.
- **The mapping row:** the Entra ID group of a Workbench role for one environment is the `entra_group` column of the `role` row in `rwb_access` (DF-REF-039, varchar(120), optional, source Entra ID; TSD P4 v3 T3.1), one group per role per environment. The legacy example is the group `RWB-SIT-RW-CASEOWN` mapped to the role `RW-CASEOWN` in SIT. The final group names per environment are the bank IAM naming decision DL40.
- **The version and the dates:** the mapping rows carry the mapping version they belong to and the valid-from and valid-to dates of that version, so a new mapping is a new dated version and never an edit of the version in force (legacy RWB-AD-001 AC3). The columns and field IDs that carry the version label and the two dates are **Not specified in the source documents (GAP-0787; ASM-1444)**, because `role` carries no version or date column in TSD P4 v3 T3.1 while the legacy criterion needs one.
- **The three operations of this story:** the mapping read, the mapping change and the version read with its effective dates, at the paths the contract baseline RWB-P4-AD001-CON fixes on `/api/recovery/access/v1`. The paths have no row in the ownership map and no row in TSD P4 v3 appendix T-A, where the only role read is `GET /admin/roles` (API-P4-007) — **Not specified in the source documents (GAP-0787; ASM-1447)**.
- **The groups themselves:** the ACE view `v_ace_iam_group` (DF-ACE-301 to DF-ACE-304: `entra_group`, `role_code`, `source_system`, `data_as_of`) is read read-only through the ACE-view contract of RWB-P1-E1069-APP (DP-05), so the administrator picks a group the bank IAM holds and sees how fresh the answer is. No statement of this story names `public.iam_group`, `public.*` or a table of another service (DP-01). The Workbench mapping is `role.entra_group`, not the view's `role_code` column (ASM-1445).
- **The change is recorded:** every mapping change and every refusal is written as a local decision-record entry through the decision-record library of DP-03 and published on the shared topic `rwb.decision-record.v1`; the central ledger and its `GET /decision-log` stay P7 rwb-decision's (ASM-1450).
- **Screens:** SCR-43 Roles and access (list; access log) is served by the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON), which reads the mapping and the access log in parallel.
- **Not this story — the sign-in that consumes the mapping:** RWB-P4-E1022-APP (legacy RWB-E1-022) resolves the groups of a signed-in person at sign-in and turns them into roles. That story reads the mapping rows this story owns; this story neither reads a token nor resolves a session.
- **Not this story — reference data, parameters and the ledger:** `lov_value`, `reference_row` and `reference_version` are P3 rwb-case's under its reference-data contract, which this key does not apply, `parameter_catalog` and `parameter_value` are P3's under the parameters contract (DP-06), `decision_log_entry` and the central ledger are P7's, and `partner_user` is S9's. This story writes no row of any of them.
- **Not this story — the other administration stories of the same legacy module:** the permission-matrix load and its approval are RWB-P4-AD002-APP and RWB-P4-AD010-APP, the masking profiles are RWB-P4-AD004-APP, the separation-of-duty check at sign-in is RWB-P4-AD005-APP, and the access review list is RWB-P4-AD008-APP.

### 2. Business rationale

Access to recovery data is granted system by system today, and a change of who may see what needs a code change or a manual check. Legacy RWB-AD-001 answered that by holding the group-to-role mapping as a data row per environment, so that a person's Workbench roles follow the group the bank IAM already grants. The answer is still right, and the realignment makes it a service answer: the mapping is a column of the role rows of `rwb_access`, it carries the version and the effective dates of the version it belongs to, and the security administrator maintains it through a published operation instead of a deployment.

The distinction between this key and RWB-P4-E1022 is fixed and this story is the data half of it. **RWB-P4-E1022-APP resolves the groups of a signed-in person at sign-in; this story owns the mapping rows as data, their version with a valid-from date, and their maintenance, so a new mapping is a data change and never a code change.** RWB-P4-E1022-APP is the H dependency that consumes the mapping: it reads the rows this story writes, at the version in force at the moment of the sign-in, and owes this story nothing else. A mapping change therefore reaches a person at their next sign-in with no deployment, no restart and no ticket to a release train, which is REQ-ACA-002 taken to the group rather than to the role.

Two consequences are the point of the split. The first is that the mapping is P4's own data and not a read of the bank IAM: the ACE view is a reference for the group's name, source and freshness, and the Workbench decides which role a group gives. The second is that the mapping is versioned like every other business value of the service, so an audit can say which group gave which role on a given date, and a change is a dated version with a recorded decision — which is the control that FEAT-ACA-03 and FEAT-ADM-01 expect of the role administration of Epic 8.

The mapping change is published as `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1`, the one access-policy event the architecture gives this service (ASM-1448). No third event name is invented: a mapping change **is** an access-policy change, and the services that cache permission data need one signal, not two. The mapping has one consumer inside the estate — the sign-in of this same service — so a dedicated event would add a name and a contract without a consumer.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-AD001-CON (same service, its own contract story) | The published mapping contract: the three operations, the `RoleMapping`, `RoleMappingVersion` and `RoleMappingPage` schemas, the version-with-effective-date rule, the `rwb.access.AccessPolicyChanged.v1` declaration, the error envelope and the fakes this story builds against |
| RWB-P4-E1022-APP (same service, the H dependency) | Sign-on with Entra ID single sign-on, multi-factor authentication and the first roles (legacy RWB-E1-022): the sign-in that applies the mapping to the caller's groups. It is the consumer of the rows this story writes, and the two criteria AC1 and AC2 are observed through it |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the entry of every mapping change and of every refusal |
| RWB-PLT-E1042-CON and RWB-P3-E1042-CON | The parameters client library and the parameters contract of rwb-case (DP-06): the environment code of this deployment, read as data rather than written in code (ASM-1446) |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19), which serves SCR-43 and merges the mapping read with the access-log read |
| The `v_ace_iam_group` view and its SELECT grant | The group name, the source system and the data-as-of date of the groups the bank IAM holds (DF-ACE-301 to DF-ACE-304), read read-only through the ACE-view contract of RWB-P1-E1069-APP (DP-05). The view is never joined to a `public` table and no ACE table is read |
| The `role` and `permission` tables in `rwb_access` | The role rows that carry `entra_group` (DF-REF-034 to DF-REF-039) and the Platform administration letters of the caller (DF-REF-040 to DF-REF-044), from the service baseline of legacy RWB-E1-037 and RWB-P4-E1019-APP. This story adds the version and date columns through its own migration and changes no other column of them |
| The mapping version and its effective dates | The version label and the valid-from and valid-to dates of a mapping version. The columns and field IDs are **Not specified in the source documents (GAP-0787; ASM-1444)**; this story carries them with the role rows of the environment and creates no new table (ASM-1444) |
| The environment code | SIT is the environment of the legacy criterion. The parameter code that carries the environment, and the environment codes beyond SIT, are **Not specified in the source documents (GAP-0787; ASM-1446)** |
| The group names | The final Entra ID group names per environment are the bank IAM naming decision DL40, recorded in the legacy RWB-E1-022 preconditions; the legacy example `RWB-SIT-RW-CASEOWN` is the value used by the criteria and the tests |
| No approval step | No second approval of a mapping version is specified by any source: the legacy story names the security administrator as the actor and no approver (ASM-1449) |
| No human approval of this document | This story is born in Draft (realignment v1) under D-RCV-60 and builds against a Draft contract; the contract is frozen when its consumers pass their contract tests |

**Wave.** Wave 4 is taken from the W-MAP of business epic EP08 (Template and Rules §R5.6) and not from the Arch v5 wave 1 of the service, as the Work Package fixes; the release date is copied unchanged and marked tentative.

### 4. Flow

1. The security administrator opens SCR-43 Roles and access through the gateway-bff composite route of DP-19. The route calls the mapping read of this story and the access-log read in parallel, one hop each, and merges the answers.
2. The caller is authorised at the door: the mapping read needs the R letter of Platform administration, and the mapping change needs the C letter of Platform administration. RW-SECADM holds CRUDA there and RW-PLATADM holds CRUD (TSD P4 v3 T6.1); the legacy story names the security administrator as the actor. A caller with no Workbench role is refused 401 with MSG-P4-001 and a caller without the letter is refused 403 with MSG-P4-002; both refusals are written as a decision-record entry before the answer leaves the service (ASM-1450).
3. The deployment resolves its environment code as a parameter through the parameters contract (DP-06) and reads the mapping rows of that environment, so the same build serves SIT, user acceptance and production with no code change (ASM-1446).
4. The mapping read answers the rows in force on the date asked: for each row the group name `entra_group`, the role code, the role name, the role class and the default scope, the mapping version label, its valid-from and valid-to dates, and the data-as-of date of the group reference. A caller may filter by group name, by role code and by a date. The version answered is the one whose valid-from is the latest not after the date asked, and one version answers whole.
5. The security administrator changes a mapping: the page posts the group name, the role code and the valid-from date of the new version. The group is picked from the list the ACE view answers, with `source_system` and `data_as_of` shown, so an unknown or stale group is visible before the change is made (DP-05).
6. `RoleMappingChecks` run over the posted version before any row is written: the group name is present and within 120 characters (DF-REF-039), the role code exists as an active `role` row of this environment, no second row of the version maps the same group to a different role (one group to one role per environment), no second row of the version maps the same role to a second group, the valid-from date is present and not earlier than the day of the change, the version label is present, and no required field is empty (MSG-GEN-001).
7. The change is written as a new dated version: the mapping rows of the new version are written with its version label and valid-from, the valid-to of the version in force is closed on the day before the new valid-from, and the rows of the older version stay readable with their own dates. An applied version is never edited in place (DP-15; ASM-1444).
8. The decision-record entry is written in the same transaction through the library of DP-03: decision code `AC-CHG`, the environment, the mapping version, the rows changed, the acting user reference and the time, and no name and no e-mail address. The outbox row is written by the same library, so the entry is published on `rwb.decision-record.v1` with no second write. Where the entry cannot be written the change is not stored and the call fails with 503 and MSG-P7-003 (ASM-1450).
9. After the commit, one `rwb.access.AccessPolicyChanged.v1` is published on `rwb.access.events.v1` with change kind `MAPPING`, the environment, the mapping version, the role codes touched and the counts of rows added and closed — no group membership, no user reference and no personal data (ASM-1448).
10. The version read answers one mapping version by its label: its effective dates, its row count, its author reference, the decision-record entry reference of its change, and its rows. A version that is not in force is answered as a version, never as the mapping in force.
11. A caller asks for a role code the environment does not hold, a group the bank IAM does not hold, or a version label that does not exist: 404 with the envelope and no row. The service invents no group and no role.
12. Every read is one hop on the caller's thread inside the 2 s budget of DP-11; no read calls another service, and the group reference arrives from the ACE view of the same database through the P1 grant (DP-05).
13. The story writes no scope, no permission letter, no masking row and no delegation limit: the mapping says which role a group gives, and what that role may do is the permission matrix of RWB-P4-E1037-APP and RWB-P4-AD002-APP.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A required field of the change is empty | 422, no row is written and the version in force is unchanged | MSG-GEN-001 | AC2 |
| X2 | The group name is longer than 120 characters or names no group the ACE view holds | 422 with the field named; the reference answer is shown with its `data_as_of` | MSG-GEN-001 | AC2, AC3 |
| X3 | The role code is not an active `role` row of the environment | 422 naming the field and the value; nothing is written | MSG-GEN-001 | AC2 |
| X4 | The same group maps to a second role in the version, or the same role to a second group | 422 naming the duplicate rows; nothing is written, because one group gives one role per environment | MSG-P1-002 | AC2 |
| X5 | The valid-from date is earlier than the day of the change | 422 naming the field; nothing is written | MSG-GEN-001 | AC2 |
| X6 | The version label already exists | 409 with the envelope; the version in force is unchanged and the existing version is answered | MSG-GEN-004 | AC2 |
| X7 | The caller holds no Platform administration R for the read, or no C for the change | 403 before any row is read or written, one refusal entry | MSG-P4-002 | AC2 |
| X8 | The caller holds no Workbench role at all | 401 before any row is read or written, one refusal entry | MSG-P4-001 | AC2 |
| X9 | The decision-record entry cannot be written | 503, no mapping row is written and the version in force is unchanged | MSG-P7-003 | AC2 |
| X10 | The version label, the role code or the group asked for does not exist | 404 with the envelope; no row is answered and none is invented | MSG-GEN-004 (envelope `messageId`) | AC2 |
| X11 | A read arrives while a new version is being written | The read answers one version whole — the version in force or the new one — and never a mixture | None | AC3 |
| X12 | The ACE view cannot be read | The mapping read still answers the rows of `rwb_access`, and the group reference is answered as unavailable with its reason; the change is refused with 503 and nothing is written | MSG-GEN-006 | AC3 |
| X13 | A sign-in happens on the day a new version starts | The sign-in resolves the version whose valid-from is the latest not after that day; a session already open keeps the mapping it resolved until it ends | MSG-P4-001 for a person who is left with no role | AC1, AC3 |

No exception path of this story changes a case, a task, an approval or a session: this service holds the mapping, and the sign-in, the case state machine and the approval are other services'.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the mapping contract of RWB-P4-AD001-CON and its fakes, the decision-record library, the parameters contract and the gateway-bff route; it writes one service's own `role` rows and reads the service's own ACE view |
| Negotiable | The group names (DL40), the environment codes, the version labels and the dates are data rows; the story fixes the checks, the version rule and the read shape only |
| Valuable | A mapping change is a dated data row with a recorded decision and a published access-policy event, so no release is needed to change who a group makes a person |
| Estimable | One migration that adds the version and date columns and seeds the mapping, one check set, three operations, one record entry and one event |
| Small | Fits one sprint with its tests; the sign-in, the permission matrix and the screens are other stories' |
| Testable | Every criterion in section 7 is one automated test over synthetic role rows and a stubbed ACE view; no real group, person or entitlement is needed |

### 7. Acceptance criteria

```gherkin
Feature: Map Entra ID groups to Workbench roles

  Background:
    Given the rwb-access base path is /api/recovery/access/v1 and the schema is rwb_access
    Given a mapping is the "entra_group" column of a "role" row of one environment in "rwb_access"
    Given one group gives one role per environment

  Scenario: AC1 Group gives the role (legacy RWB-AD-001 AC1)
    Given the rwb-case contract mock returns the environment code "SIT" for this deployment
    Given the group RWB-SIT-RW-CASEOWN mapped to RW-CASEOWN
    When a member of the group signs in to SIT
    Then the session holds the role RW-CASEOWN

  Scenario: AC2 Unmapped group (legacy RWB-AD-001 AC2)
    Given the platform library contract mock returns the decision-record entry accepted on "rwb.decision-record.v1" for the refusal
    Given a person whose only group has no mapping
    When they sign in
    Then the system refuses they with MSG-P4-001 and the refusal is in the access log

  Scenario: AC3 Mapping change (legacy RWB-AD-001 AC3)
    Given a new mapping version with a valid from date
    When the date arrives
    Then sessions from that date use the new mapping
```

The three criteria are the legacy criteria of RWB-AD-001, copied word for word with the origin tag. Two Given lines are added and nothing else is changed: the first is the faked answer of the parameters contract (DP-06, the C dependency RWB-P3-E1042-CON) that names the environment `SIT`, and the second is the faked answer of the decision-record library (DP-03) for the refusal. Every legacy value is kept character for character: the group `RWB-SIT-RW-CASEOWN`, the role `RW-CASEOWN`, the environment `SIT`, `MSG-P4-001`, and the mapping-version valid-from rule of AC3.

AC1 and AC2 are answered by the mapping rows this story maintains and are observed through the sign-in of RWB-P4-E1022-APP, the H dependency that consumes the mapping; AC3 is answered by the version label and the valid-from date this story writes. The wording of AC2 is kept exactly as the legacy story has it, and the wording is noted once in section 14; the sentence is not corrected. The faked answer of the parameters contract in AC1 carries the legacy environment `SIT` unchanged.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A mapping is one data row per role per environment: the group name in `role.entra_group` of the role row of that environment. No group name, role code, environment code, version label or date is written in code | Legacy RWB-AD-001 story statement; TSD P4 v3 T3.1 (DF-REF-039); RWB-E1-022 section 2 |
| BR2 | A mapping version and its valid-from and valid-to dates travel with the mapping rows, and one version answers whole: the version whose valid-from is the latest not after the date asked | Legacy RWB-AD-001 AC3; TSD P4 v3 T4 (LOV-VERSION-STATUS) |
| BR3 | A new mapping is a new dated version written as data. An applied version is never edited, and the older rows stay readable with their own dates | Legacy RWB-AD-001 AC3; DP-15; Template and Rules §R5.5 |
| BR4 | The change is checked before a row is written: the group is present, the role is an active role row of the environment, one group gives one role and one role one group, the valid-from is present and not in the past, the version label is present, and no required field is empty | FSD P4 v3 VR-P4-003-1; legacy RWB-AD-001 Data table |
| BR5 | The mapping read and the version read need the R letter of Platform administration, and the mapping change needs the C letter. A caller with no Workbench role is 401 with MSG-P4-001 and a caller without the letter is 403 with MSG-P4-002, and both refusals are recorded | TSD P4 v3 T6.1 and API-P4-007; FSD P4 v3 VR-P4-001-1 and VR-P4-004-1 |
| BR6 | Every mapping change and every refusal writes one local decision-record entry through the library of DP-03 and is published on `rwb.decision-record.v1`; where the entry cannot be written the change is not stored | DP-03; FSD P4 v3 A2.3; MSG-P7-003 |
| BR7 | A mapping change is published as `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1` with change kind `MAPPING` and no personal data; no second event name exists for it | Architecture v5 slides 14 and 43; ASM-1448 |
| BR8 | The group reference is read read-only from `v_ace_iam_group` through the ACE-view contract of RWB-P1-E1069-APP with its `data_as_of`, and never from `public.iam_group`, a `public` table or another service's table; the mapping itself is P4's `role.entra_group` | TSD P4 v3 T3.1; DP-05; DP-01; ASM-1445 |
| BR9 | The environment code is read as a parameter through the parameters contract of rwb-case, so the same build serves every environment | DP-06; ASM-1446 |
| BR10 | A mapping version needs no second approval: the security administrator writes it under the C letter and the decision-record entry names the actor and the time | ASM-1449; legacy RWB-AD-001 Permission checks |
| BR11 | A person whose only group has no mapping, or whose group maps to no active role, gets no role and sees MSG-P4-001; the refusal is in the access log | Legacy RWB-AD-001 AC2; FSD P4 v3 AC-EXC-P4-001-04; VR-P4-001-1 |
| BR12 | A session resolves the mapping version in force at its sign-in and keeps it until the session ends; a change made after the sign-in reaches that person at the next sign-in | Legacy RWB-AD-001 AC3; ASM-1451 |

Where each rule sits in the target: BR1, BR2 and BR3 are answered from `rwb_access` only, with the version and the dates on the role rows (ASM-1444). BR4 is the check set that runs before the write, so a version that fails is never stored. BR5 and BR10 are the guard and the letters of the caller's own permission rows, answered in one hop. BR6 and BR7 are the decision-record library and the outbox of the service template. BR8 is enforced by the module map and by boundary rule BND-6 of RWB-P4-E1069-APP. BR9 is the parameters client of DP-06. BR11 and BR12 are the sign-in rule of RWB-P4-E1022-APP, which reads the rows this story owns.

### 9. State transitions

None for a case, a task or a session. The states of this story are the states of a mapping version.

| From | Event | Condition | To |
|---|---|---|---|
| No mapping version of an environment | the first mapping is written by this story's migration | Every check passes | The version is in force from its valid-from date |
| The version in force | a new version is written with a later valid-from | Every check passes and the decision-record entry is written | The new version is in force from its valid-from; the rows of the earlier version keep their own valid-to |
| The version in force | a new version fails a check or the entry cannot be written | Any failed row, or a 503 from the record library | The whole version is refused and the version in force is unchanged |
| The version in force | a read on a day inside two versions | None | Exactly one version answers, the one whose valid-from is the latest not after the day asked |
| The rows of a version | a mapping change is written | The change passes every check | The new rows carry the new version label; the earlier rows stay readable with their valid-to |
| A session | the sign-in resolves the version in force that day | A role is resolved | The session holds the roles of that version until it ends, whatever version later starts (ASM-1451) |

The version status vocabulary is LOV-VERSION-STATUS (LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED) in TSD P4 v3 T3.2. This story writes an approved version as data under the C letter and reads the version in force; the load, the approval and the rollback of a reference-data file on the reference-load path are rwb-case's and are not carried here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-access service identity (the per-service login, DP-02) | Answers the mapping read and the version read, writes a mapping version, runs the checks, writes the decision-record entry and publishes the access-policy event |
| RW-SECADM, security administrator | CRUDA in Platform administration (TSD P4 v3 T6.1): maintains the mapping, writes a mapping version and reads every version. The legacy story names this role as the actor |
| RW-PLATADM, platform administrator | CRUD in Platform administration (TSD P4 v3 T6.1): maintains the mapping as the security administrator does, and reads the versions |
| RW-AUDIT, internal audit | R in Platform administration: reads the mapping, the versions and the entries of the changes. Writes nothing |
| RW-COE, center of excellence analyst | CRUD in Rules and parameters and R in Platform administration: reads the mapping only. This story gives it no write path, because the mapping is not a rule or a parameter |
| RW-REFADM, reference data administrator | CRUD in Reference data and no right in Platform administration: does not maintain the mapping, which is not reference data (ASM-1445) |
| Every other role and every service identity | Reads the mapping through RWB-P4-E1022-APP's sign-in resolution and through no operation of this story |
| No delegation of authority level applies | A mapping is not a credit decision, and no limit of `delegation_limit` is read |

The mapping is role administration, not reference data: `role` and `permission` are P4's own tables under the ownership map, and the reference-data contract of rwb-case holds `lov_value`, `reference_row` and `reference_version` only (ownership map). The database login is the per-service login of the service baseline (DP-02), and this story adds no grant.

The legacy Permission checks table gives this story the Rules and parameters letters R and C, and the legacy Endpoints table gives it the rule-version paths. Neither is kept: the rule-version paths and their rights belong to the rule-version stories of this service and to P7 rwb-decision, while the mapping is role administration under Platform administration (GAP-0787; ASM-1447).

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 | `role` | id | Read; the mapping row is a role row |
| DF-REF-035 | `role` | role_code | Read and written by the mapping change |
| DF-REF-036 | `role` | role_name | Read, for the answer |
| DF-REF-037 | `role` | role_class (LOV-ROLE-CLASS) | Read, for the answer |
| DF-REF-038 | `role` | default_scope (LOV-SCOPE) | Read, for the answer |
| DF-REF-039 | `role` | entra_group | Read and written by the mapping change; the mapping itself |
| DF-REF-040 to DF-REF-044 | `permission` | role_id, capability_area, letters, matrix_version | Read, for the Platform administration letters of the caller. Never written here |
| Not specified in the source documents (GAP-0787; ASM-1444) | `role` | the mapping version label and the valid-from and valid-to dates of the version | Written by the mapping change; read by both reads |
| DF-ACE-301 | `v_ace_iam_group` | entra_group | Read read-only through the P1 ACE-view contract; the view is never written, and the mapping is the role column, not this one |
| DF-ACE-302 | `v_ace_iam_group` | role_code | Read only as the bank IAM's value; never the Workbench mapping (ASM-1445) |
| DF-ACE-303 | `v_ace_iam_group` | source_system | Read, for the answer |
| DF-ACE-304 | `v_ace_iam_group` | data_as_of | Read, for the freshness of the group reference |
| DF-REF-027 to DF-REF-033 | `lov_value` of `rwb_case` | lov_code, value_code, label_en, sort_order, valid_from | Not read by this story: a role class, a capability area and a scope travel as codes in `role` and `permission`, and the list values behind them are RWB-P4-E1019-APP's read through the reference-data contract |
| Not specified in the source documents (GAP-0787; ASM-1450) | the local decision record of DP-03 | the change entry and the refusal entry | Written through the decision-record library; no field is invented here |

Two values the sources do not fix are carried as placeholders. The mapping version label and the two effective dates have no column on `role` in TSD P4 v3 T3.1, while legacy AC3 needs a version with a valid-from — **Not specified in the source documents (GAP-0787; ASM-1444)**. The environment beyond SIT and the parameter that carries it are **Not specified in the source documents (GAP-0787; ASM-1446)**. Field IDs are those in the Logical Data Model and Data Dictionary v9, and the legacy physical names `role`, `permission` and `v_ace_iam_group` are kept.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-access` (P4); base `/api/recovery/access/v1`. The three paths are fixed by RWB-P4-AD001-CON and have no row in the ownership map and none in TSD P4 v3 appendix T-A — **Not specified in the source documents (GAP-0787; ASM-1447)**.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/api/recovery/access/v1/admin/role-mappings` | The mapping rows in force on the date asked for this environment: group name, role code and name, mapping version, valid-from and valid-to, and the `data_as_of` of the group reference. Query `entraGroup`, `roleCode`, `validOn`, `page`, `size` | Platform administration R (TSD P4 v3 T6.1) | Not applicable, read only |
| POST | `/api/recovery/access/v1/admin/role-mappings` | Write a new mapping version with its valid-from date and its rows; the answer is the version | Platform administration C | `Idempotency-Key` header; the same key returns the first answer |
| GET | `/api/recovery/access/v1/admin/role-mapping-versions/{versionId}` | One mapping version with its effective dates, its row count, its author reference, the decision-record entry reference and its rows | Platform administration R | Not applicable, read only |

The role catalogue read `GET /api/recovery/access/v1/admin/roles` (API-P4-007) and the session read `GET /api/recovery/access/v1/me/session` (API-P4-012) are the service's and are not restated or changed here; the roles, their permissions and their conflicts are the subject of RWB-P4-E1019-APP and RWB-P4-E1037-APP.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case`, published by RWB-P3-E1042-CON (DP-06) | The environment code of this deployment. The parameter code and the environment codes beyond SIT are **Not specified in the source documents (GAP-0787; ASM-1446)** |

The ACE view is a read-only SQL read and not a call to another service: `recovery.v_ace_iam_group` (SELECT) is granted and contracted by RWB-P1-E1069-APP (DP-05) and answers the group name, the source system and the `data_as_of` of the groups the bank IAM holds. It is never `public.iam_group` and never a `public` table.

The reference-data contract of rwb-case is not consumed: this story resolves no list value, because a role class, a capability area and a scope travel as codes in `role` and `permission`, and the list values behind them are RWB-P4-E1019-APP's read under the reference-data contract of rwb-case (ownership map).

#### 12.3 Events published

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 `rwb-access` | Change kind `MAPPING`, the environment, the mapping version, the role codes touched, the counts of rows added and closed and the time; no group membership, no user reference and no personal data |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | PLT library, consumed by P7 | Entry id, decision code (`AC-CHG` for a change, `AC-DENY` for a refusal), the environment, the mapping version and the time; written by the library of DP-03, not by this story's own writer |

Both messages use the CloudEvents 1.0 envelope with the attributes id, source, type, specversion, time, subject and datacontenttype. `rwb.access.DoaLimitChanged.v1` is not published here, and no second access event name is invented: a mapping change is an access-policy change (ASM-1448). Consumers refresh their cached permission data on `AccessPolicyChanged` (Architecture v5 slide 20), and the mapping's own consumer is the sign-in of RWB-P4-E1022-APP, which reads `rwb_access` in the same service.

#### 12.4 Events consumed

None. rwb-access is a reference-data owner in Architecture v5 slide 14 (events: none), the version in force is read from `rwb_access` on each call, and this story subscribes to no topic and writes no inbox row.

#### 12.5 Workflows and activities

None. The mapping read, the change and the version read are synchronous REST answers in the caller's thread. The six-monthly access review list (JOB-18, Architecture v5 slide 44) is RWB-P4-AD008-APP's; this story starts no workflow, signals none and registers no activity on the `rwb-access` queue.

#### 12.6 Schedules

None. No Temporal Schedule and no quartz job sits in this story, and nothing about a mapping runs on a clock: the valid-from date is a row value the read resolves.

#### 12.7 Tables owned

| Table | Schema | Owner (ownership map) | This story |
|---|---|---|---|
| `role` | `rwb_access` | P4 | Reads the rows; writes `entra_group` and the mapping version and dates by the mapping change and by the migration |
| `permission` | `rwb_access` | P4 | Reads the caller's Platform administration letters; never writes |
| `outbox_event`, `processed_event`, `idempotency_key` | `rwb_access` | PLT library | Created by the service baseline; the record library writes the outbox row of a change, and this story writes none by hand |
| `masking_rule`, `role_conflict`, `delegation_limit` | `rwb_access` | P4 | Not read and not written by this story |
| `v_ace_iam_group` | ACE database, read-only view | ACE / P1 `rwb-source-data` | Read read-only through the P1 ACE-view contract (DP-05) |
| `lov_value`, `reference_row`, `reference_version` | `rwb_case` | P3 | **Never read by SQL**; they are P3's reference data and this key applies no reference-data read |
| `parameter_catalog`, `parameter_value` | `rwb_case` | P3 | **Never read by SQL**; the environment code arrives through the parameters contract (DP-06) |
| `decision_log_entry` | `rwb_decision` | P7 | Not read and not written; the central ledger is P7's and the local entry is the library's |
| `partner_user` | `rwb_partner` | S9 | Not read and not written; the ownership map gives it to S9 |

No foreign key crosses a schema and no statement in this story names a table outside `rwb_access` except the read-only ACE view of the P1 contract. The mapping is the Workbench's own data and stays with this service.

#### 12.8 Contract fakes

| Fake | Serves | Used for |
|---|---|---|
| Mapping contract fake (RWB-P4-AD001-CON) | The three paths of 12.1 with a mapping version in force and a next version | AC1, AC2 and AC3, and every test that reads or writes a mapping |
| Parameters fake (RWB-P3-E1042-CON) | The environment code `SIT` and one later environment code | AC1 and AC3, so no environment is a constant in the test |
| ACE group fake | `v_ace_iam_group` with the group `RWB-SIT-RW-CASEOWN`, its source system and a `data_as_of`, plus one group the view no longer holds | AC2 and AC3 |
| Decision-record fake (RWB-PLT-E1027-CON) | The entry append, the hash-chain check and the 503 with MSG-P7-003 | AC2 and AC3 |

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 3 operations under `/api/recovery/access/v1` | 1 operation | OpenAPI 3.1, one hop, 2 s timeout; plus one read-only SQL read of the ACE view |
| Kafka | 2 published | 0 | `rwb.access.AccessPolicyChanged.v1` and the library's `rwb.decision-record.DecisionRecorded.v1` |
| Temporal | None | None | No workflow, activity or Schedule in this story |
| File | None | None | No file in this capability |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access.mapping`, module `mapping`, in the service root `th.co.scb.ace.workbench.recovery.access`. Service base `/api/recovery/access/v1`, schema `rwb_access`, topic `rwb.access.events.v1`, Temporal task queue `rwb-access` (not used here).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the decision-record entry of every change and every refusal and the outbox row that publishes it. DP-05 is the read-only ACE view that answers the group, its source and its `data_as_of`; the view and its SELECT grant come from RWB-P1-E1069-APP and this story adds no dependency for them. DP-06 is the environment code read as data, so one build serves every environment. DP-13 is the base of the three operations. DP-19 is the composite route that serves SCR-43 with the mapping read and the access-log read. The outbox relay and the inbox are the service template's own library objects and add no dependency to this story, which is why they are not in this key's pattern set.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `V4001_1__role_mapping_version.sql` | Migration | Adds the mapping version and effective-date columns to `role` in `rwb_access` and seeds the mapping rows of SIT, including the group `RWB-SIT-RW-CASEOWN` on the role `RW-CASEOWN`; copies no value of a person |
| `RoleMappingChecks` | Service | The checks of BR4 over a posted version: group, role, uniqueness both ways, the valid-from, the version label and the required fields |
| `RoleMappingRepository` | Repository | Reads the mapping rows at the version in force on a date and one version by its label; writes the rows of a new version |
| `RoleMappingService` | Service | Assembles the mapping answer and the version answer, resolves the environment through the parameters client and closes the earlier version on the day before the new valid-from |
| `AceGroupReader` | Client | Reads `v_ace_iam_group` read-only through the P1 ACE-view contract with `data_as_of`; no write and no join to a `public` table |
| `MappingChangeRecorder` | Service | Writes the decision-record entry of a change and of a refusal through the library of DP-03 and the outbox row that publishes `rwb.access.AccessPolicyChanged.v1` |
| `EnvironmentParameterClient` | Client | The environment code through the parameters contract of DP-06; no environment code in code or in a profile |

**Database and migrations**

- Writes `role` in `rwb_access` only: `entra_group` (DF-REF-039) and the mapping version and date columns this story adds (ASM-1444).
- Migration `V4001_1__role_mapping_version.sql` sits on the per-service Flyway sequence after the V0001 baseline (DP-15). It adds the version and date columns, one index on the version and the valid-from for the read, and the seed rows of the SIT mapping; it drops nothing and copies no ACE value.
- The read predicate is the version in force on the day asked; the version is a value, never a date written in code.
- A new version is written by insert and by closing the earlier version's valid-to; no update ever rewrites the rows of an applied version.
- DB access uses the per-service rwb-access login of the service baseline (DP-02). No grant on `rwb_case`, on `recovery` or on `public` is added by this story beyond the SELECT on the ACE view that RWB-P1-E1069-APP already grants.

**Configuration and reference data**

- The group names, the role codes, the version labels, the dates and the environment codes are data rows; none is a constant in code (BR1).
- The environment code arrives as a parameter through the parameters contract (DP-06); its parameter code is **Not specified in the source documents (GAP-0787; ASM-1446)**.
- The final group names per environment are the bank IAM decision DL40; the legacy example `RWB-SIT-RW-CASEOWN` is the value of the criteria and the tests.
- No feature switch: a mapping is changed by rows and by their dates, not by a flag.

**Build steps**

1. `V4001_1__role_mapping_version.sql` with the version and date columns and the SIT seed rows, plus a fixture that applies it twice; test AC1.
2. `RoleMappingChecks` with one check per rule and a failing fixture for each: an empty group, a group over 120 characters, an unknown role code, the same group twice, the same role twice, a valid-from in the past and an empty version label; test AC2.
3. `RoleMappingRepository` and `RoleMappingService` with the version-in-force resolution on a fixed clock and the closure of the earlier version; tests AC1 and AC3.
4. `MappingChangeRecorder` with the entry, the outbox row and the forced failure that answers 503 with MSG-P7-003; test AC2.
5. `AceGroupReader` over the ACE-view fake with `data_as_of`, and the 503 when the view cannot be read; test AC3.
6. `EnvironmentParameterClient` over the parameters fake, so a later environment needs no build (BR9).
7. The two read operations with the Platform administration R letter through the guard of RWB-P4-E1037-CON, and the change with the C letter; test AC2.
8. The boundary check: no statement names a `public` table, a `v_ace_*` view other than `v_ace_iam_group`, or a table of another service; BND-6 of RWB-P4-E1069-APP stays green on this package.

**Done when.** The tests in section 16 pass; `role` holds the mapping of SIT with the group `RWB-SIT-RW-CASEOWN` on the role `RW-CASEOWN`; a new mapping version with a valid-from date answers from that date with no deployment; a caller without the letter is refused with MSG-P4-002 and one refusal is recorded; a forced record failure leaves the version in force unchanged and answers 503 with MSG-P7-003; the change publishes `rwb.access.AccessPolicyChanged.v1`; and no statement in the service names a table outside `rwb_access` or a `public` table.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The caller holds no Workbench role, or a sign-in resolves no role from the mapping | You have no Recovery Workbench role. Ask your team manager to request one. | The guard of this story; the sign-in of RWB-P4-E1022-APP |
| MSG-P4-002 | The caller holds no Platform administration R for a read, or no C for a change | You cannot {action} here. Your role does not include it. | The guard, on all three operations |
| MSG-GEN-001 | A required field is empty, the group is longer than 120 characters, the role code is unknown or the valid-from is in the past | Enter {field}. | The checks of this story, as a 422 with the field and the row |
| MSG-P1-002 | The same group maps to a second role, or the same role to a second group, in one version | The {source} load for {date} was refused: {check}. The previous load is still in use. | The checks of this story, as a 422 with the duplicate rows |
| MSG-GEN-004 | The version label already exists, or the version, role or group asked for does not exist | Someone else changed this record. Reload it to see their change. | The change and the two reads |
| MSG-GEN-006 | The ACE group reference cannot be read | The reference data is not available. Try again later. | The mapping read and the change |
| MSG-P7-003 | The decision-record entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The change and the refusals, through the library of DP-03 |

Every error is an RFC 9457 problem response with `messageId` set and `detail` carrying the text with its placeholders filled. For MSG-P4-002 the {action} value names the action the caller tried — "read the group mapping", "change the group mapping" or "read a mapping version" — and never a case fact, a group membership or the entitlement of another person. For MSG-P1-002 the {check} value names the failed check and the {source} and {date} values are the mapping version and its valid-from date.

**Note on the legacy wording, carried once.** Legacy AC2 in RWB-AD-001 reads "the system refuses they with MSG-P4-001". The sentence is copied word for word in section 7 as the template requires; the criterion is not corrected here, and the message ID and the refusal it names are unchanged. The correction of the sentence, if the business wants one, is a change to the legacy story and not to this slice.

### 15. Screens and states

No screen is built by this story. SCR-43 Roles and access shows the roles, their permissions, the group mapping and the access log, and the security administrator and internal audit read it there; it is served by the gateway-bff composite route of DP-19, which calls the mapping read and the access-log read in parallel, one hop each, and renders the rows. The screen field list, the column order and the merge are the screen owner's, and this story returns the rows and the versions only.

| Screen | State | What the operator sees |
|---|---|---|
| SCR-43 Roles and access | List | The mapping rows in force for the environment: group, role code, role name, version and dates, and the `data_as_of` of the group reference |
| SCR-43 Roles and access | Change | The form of a new version: group picked from the ACE list, role code, valid-from, and the checks answered field by field |
| SCR-43 Roles and access | Changed | The new version with its commit time and the reference of the decision-record entry |
| SCR-43 Roles and access | Access log | The entries of the changes and of the refusals, read through the access-log operation of RWB-P4-AD007-APP on the same composite route |
| SCR-43 Roles and access | Refused | MSG-P4-002 or MSG-P4-001, with no row and no version |
| SCR-43 Roles and access | Not available | MSG-GEN-006 for the group reference, MSG-P7-003 for the record, each with the retry advice of the message |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-001-01 | AC1 | End to end | Legacy test "Group gives the role": the role `RW-CASEOWN` carries `entra_group` `RWB-SIT-RW-CASEOWN` in SIT; a synthetic member of that group signs in and the session holds `RW-CASEOWN`, with the mapping version and the environment of the sign-in |
| TC-AD-001-02 | AC2 | End to end | Legacy test "Unmapped group": a synthetic person whose only group is not mapped to an active role row; the sign-in answers MSG-P4-001 and one refusal entry is on `rwb.decision-record.v1` |
| TC-AD-001-03 | AC3 | End to end | Legacy test "Mapping change": two mapping versions with valid-from dates D and D2 on a fixed clock (synthetic fixture dates); a change written on the day before D answers from D, a session already open keeps the version it resolved, and the earlier rows stay readable with their valid-to |
| TC-AD-001-04 | Access | Component | Legacy test "A role without the right is refused with MSG-P4-002": `RW-PHONECOL` with no Platform administration letter calls the mapping read, the change and the version read; 403 with MSG-P4-002 on each, one refusal entry each, and no row written |
| TC-AD-001-05 | Principle 5 | NFR | Legacy test "A forced decision log write failure stops the action with MSG-P7-003": the decision-record write forced to fail on a change; 503 with MSG-P7-003, no mapping row written and the version in force unchanged |

The five legacy test cases are kept with their IDs and their legacy Covers values; the legacy test name is written in the Data column and the Level column follows Template and Rules §R7.2, where the legacy level Access maps to Component and the legacy level Resilience to the Principle 5 row at NFR. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The ITG copy of the set is RWB-ITG-AD001-ITG's and is not written here, so no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in code: group names, role codes, environment codes, version labels and dates are rows of `role` and of the parameters contract, and a test proves that a new mapping needs no build (BR1, BR9).
- No personal data anywhere: a mapping is a group name and a role code, an entry carries a user reference and no name, and no test row, log, event or prompt holds a name or an e-mail address.
- No read of another schema (DP-01): `lov_value`, the reference tables, the parameter tables, `decision_log_entry` and `partner_user` are never read by SQL, and the only external read is the read-only ACE view `v_ace_iam_group` of the P1 contract.
- ACE data only through the owner's contract or the service's own `v_ace_*` view (DP-05): no statement names `public.iam_group`, a `public` table or a table of another service, and boundary rule BND-6 of RWB-P4-E1069-APP stays green on this package.
- One writer for the mapping: only the migration and the change operation write `role.entra_group`, the applied version is never edited, and a change is a new dated version (BR3).
- Default deny on every call: a missing role resolves to 401 and a missing letter to 403 with MSG-P4-002, never to allow (BR5).
- A version answers whole or not at all, and a session keeps the version it resolved until it ends (BR2, BR12).
- One migration per story on the service's own Flyway sequence (DP-15); an applied version is never edited.
- One event name: `rwb.access.AccessPolicyChanged.v1`, with change kind `MAPPING`. No third event and no second name for a mapping change (BR7).

### 18. Traceability

No requirement ID is recorded for legacy RWB-AD-001 in TSD P4 v3 T8, and the Work Package carries the requirement list of this key as empty; the key serves the features FEAT-ACA-03 (hold roles as data) and FEAT-ADM-01 (run the full administration screens) of the FSD P4 v3, and the epic 8 requirement REQ-ACA-013 is recorded in that specification as written one epic ahead with its test with the story.

| Feature | Where this story answers it | Test cases |
|---|---|---|
| FEAT-ACA-03, hold roles as data | The mapping is a data row with a version and dates, changed without a code release (sections 4, 8, 11) | TC-AD-001-01, TC-AD-001-03 |
| FEAT-ADM-01, the full administration screens | The mapping read, the change and the version read behind SCR-43 and the composite route (sections 12.1, 15) | TC-AD-001-04 |
| The default deny rule and the recorded refusal | MSG-P4-001 and MSG-P4-002 with the decision-record entry (sections 8, 14) | TC-AD-001-02, TC-AD-001-04 |
| The record-before-change rule | The entry of DP-03 before the change stands (sections 4, 14) | TC-AD-001-05 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P4-AD001-CON | Contract | H: the mapping contract, its schemas, the version-with-effective-date rule and the fakes |
| RWB-P4-E1022-APP | App development | H: the sign-in that consumes the mapping at sign-in and holds the roles of the version it resolved |
| RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-N001-CON | Contract | H: the decision-record library, the parameters library and the gateway-bff composite route |
| RWB-P3-E1042-CON | Contract | C: the parameters contract of rwb-case that answers the environment code |
| RWB-P1-E1069-APP | App development | The ACE view `v_ace_iam_group` and its SELECT grant, read read-only; named as the reference, not on the build row |
| RWB-P4-E1019-APP, RWB-P4-E1037-APP | App development | The role catalogue, the permission matrix and the session of this service; this story changes neither |
| RWB-P4-AD002-APP, RWB-P4-AD004-APP, RWB-P4-AD008-APP | App development | Sibling administration slices of the same legacy module: the matrix load, the masking profiles and the access review |
| RWB-ITG-AD001-ITG | Integration | The cross-service proof that a mapping change reaches the sign-in and the caching services |

| Legacy reference | Where it is kept |
|---|---|
| The story statement (a group mapped to one role in each environment as a data row) | Sections 1, 2, 8 (BR1) |
| Legacy AC1, AC2 and AC3 with `RWB-SIT-RW-CASEOWN`, `RW-CASEOWN`, SIT, MSG-P4-001 and the valid-from rule | Section 7, section 14 (the wording note) |
| The Data table: `role` DF-REF-034 to DF-REF-039 and `v_ace_iam_group` DF-ACE-301 to DF-ACE-304 | Section 11 |
| The decision DL40 and the final group names | Sections 1, 3, 13 |
| The permission check Platform administration and the roles that hold it | Sections 10, 8 (BR5) |
| The validation and messages MSG-P4-001, MSG-P4-002, MSG-GEN-001, MSG-P1-002, MSG-P7-003 | Section 14, exception paths |
| Screen SCR-43 Roles and access | Section 15 |
| Legacy test cases TC-AD-001-01 to TC-AD-001-05 | Section 16 |

### 19. Out of scope

- The sign-in itself, the group claim of the token, the multi-factor check and the resolution of a person's roles from the mapping: RWB-P4-E1022-APP (legacy RWB-E1-022). This story owns the rows it reads.
- The permission matrix, its letters, the masking rows and the role conflicts: RWB-P4-E1037-APP, RWB-P4-E1037-CON and RWB-P4-E1019-APP.
- The matrix and masking loads with their approval and rollback, and the separation-of-duty check at sign-in: RWB-P4-AD002-APP, RWB-P4-AD004-APP, RWB-P4-AD010-APP and RWB-P4-AD005-APP.
- The access review list and the six-monthly Schedule (JOB-18): RWB-P4-AD008-APP.
- The access-log search, the export and the break-glass grant: RWB-P4-AD007-APP and the break-glass story of the same service.
- The reference data itself — `lov_value`, `reference_row` and `reference_version` — and the reference-load path: P3 rwb-case under the ownership map, with the reference-data contract it publishes.
- The parameter values of the estate, including the environment codes: P3 rwb-case under DP-06 and the ownership map; this story consumes the parameters contract and holds no parameter row.
- The central decision ledger and its query: P7 rwb-decision; this story writes the local entry only.
- `partner_user`: S9 rwb-partner under the ownership map, which gives partner users to S9.
- The bank IAM's own group administration and the naming decision DL40: Entra ID and the bank IAM (INT-21), recorded as the naming decision of the legacy preconditions.
- The Helm chart, the topic creation, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
- The integration harness and its evidence, and the `-ITG` copies of the test cases: RWB-ITG-AD001-ITG.
