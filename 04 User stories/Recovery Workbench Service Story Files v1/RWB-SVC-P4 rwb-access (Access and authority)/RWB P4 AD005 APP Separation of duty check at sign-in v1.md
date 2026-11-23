# RWB-P4-AD005-APP Separation of duty check at sign-in

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-005 for rwb-access — the separation-of-duty table held as dated rows in `rwb_access`, the check the sign-in calls after it resolves a person's roles, the refusal of the whole session with its incident and its recorded decision, and the conflict version the session read answers. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-AD005-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-005 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP13, DP19 |
| Parallel lane | L-P4-A |
| Ready to start | After RWB-P4-E1022-APP |
| Depends on (build) | RWB-P4-AD005-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-N001-CON, RWB-P4-E1022-APP |
| Contract dependencies | RWB-P3-E1042-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **security administrator**, I want **the session of a person refused when the roles they hold form a pair that the separation-of-duty table forbids at the conflict version in force**, so that **no one holds two roles the table forbids, and every refusal is recorded and brought to me**.

This is the rwb-access slice of legacy RWB-AD-005, and it is the separation-of-duty half of that legacy key: the pairs as dated data with their conflict version, the check that decides whether a resolved role set holds both halves of a pair, the refusal of the whole session, the incident to the security administrator, the decision-record entry of the refusal, and the conflict version the session read answers.

- **Service naming:** REST base `/api/recovery/access/v1` (DP-13), schema `rwb_access`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery` (not used here — this story starts no workflow), Java package `th.co.scb.ace.workbench.recovery.access`.
- **The table:** a pair one person may not hold together is a `role_conflict` row in `rwb_access` (TSD P4 v3 T3.1, NEW): `id` (DF-REF-205, uuid), `role_code` (DF-REF-206, LOV-ROLE), `conflicts_with` (DF-REF-207, varchar(30)), `reason` (DF-REF-208, varchar(200)), `conflict_version` (DF-REF-209, varchar(20)), `valid_from` (DF-REF-210, date) and `valid_to` (DF-REF-211, date, optional). The legacy story's actor is the security administrator and the legacy key needs both halves of a pair named when a session is refused, so the pair is stored as two role codes and the reason is stored as text.
- **The version and the dates:** every row carries the `conflict_version` it belongs to and that version's `valid_from` and `valid_to`, so the table in force on a date is a version and never the latest row (legacy RWB-AD-005 AC2). One version answers whole, and a pair is read only from the version in force on the day of the sign-in.
- **The rule the sources name:** the legacy criterion names the pair `RW-WRITEOFF` and `RW-WOCOMM` — the person is on the write-off team and on the write-off committee — and the FSD P4 v3 names the pair `RW-SECADM` with any business role (`RW-CASEOWN` in its example). `conflicts_with` holds one role code of varchar(30), so a pair that forbids one role "with any business role" is one row per business role at the same `conflict_version`, not a wildcard the schema cannot carry (ASM-1490).
- **The check operation:** the check runs after RWB-P4-E1022-APP has resolved a person's role codes and before the session is answered, on `POST /api/recovery/access/v1/authorise/separation-of-duty` — the request is the resolved role codes, the answer is allowed or the conflicting pair with its conflict version and reason. Architecture v5 slide 14 names `POST /authorise` on this service and gives it no separation-of-duty path; the ownership map has no row for it and TSD P4 v3 appendix T-A has none either, so the path, the request and the answer are this revision's own decision on the base of §R4 — **Not specified in the source documents (GAP-0795; ASM-1483)**.
- **The refusal of the whole session:** where the resolved set holds both halves of a pair at the conflict version in force, the whole session is refused — no role, no scope, no partial session — with MSG-P4-006 naming both role codes (FSD P4 v3 AC-EXC-P4-001-03 names the message and the pair). The message text itself is **Not specified in the source documents (GAP-0795; ASM-1489)**.
- **The incident:** the criterion and the FSD both require an incident to the security administrator. No source names an incident queue, an incident operation or a target service, and Architecture v5 slide 14 gives this service no event and no incident path, so the addressee and the channel are **Not specified in the source documents (GAP-0795; ASM-1487)**; the recorded refusal, whose addressee is the security administrator, is the channel that exists.
- **The decision record:** every refusal is one local decision-record entry through the library of DP-03 — decision code `AC-DENY`, reason code `ROLE_CONFLICT`, the two role codes, the conflict version, the environment, the subject reference and the time, and no name and no e-mail address — and the library's outbox row publishes it on `rwb.decision-record.v1`. The FSD's "one refusal event is written with reason ROLE_CONFLICT" is this entry, because the service publishes no event of its own for a refusal.
- **The conflict version on the session read:** the session read of this service (`GET /api/recovery/access/v1/me/session`, API-P4-012, whose purpose in TSD P4 v3 T-A.2 is "roles, scope, matrix and conflict versions, partner and break-glass state") answers the `conflictVersion` the session was checked against. The operation is declared by RWB-P4-E1037-CON; this story supplies the value and adds no field to that contract.
- **The groups behind a pair:** the groups a person holds are read read-only from `v_ace_iam_group` (DF-ACE-301 to DF-ACE-304) through the ACE-view contract of RWB-P1-E1069-APP (DP-05), so the refusal and its entry can name the group of each role code without reading a `public` table. No statement of this story names `public.*` or a table of another service (DP-01).
- **The environment:** the code of this deployment is read as a parameter through the parameters contract of rwb-case (DP-06) and recorded on the entry, so one build serves every environment. The parameter code is **Not specified in the source documents (GAP-0795; ASM-1485)**.
- **Screens:** SCR-43 Roles and access (list; access log) is served by the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON), which reads the separation-of-duty table and the access log in parallel. The screen shows the pairs and their version; it shows no refusal of one person to another.
- **Not this story — the sign-in, the token and the role resolution:** RWB-P4-E1022-APP (legacy RWB-E1-022) holds the session, checks the second factor, resolves the groups into role codes and calls this story's check between the resolution and the session answer. **This story owns the rule, its version and the refusal fact; that story owns when the check is called and what a session is.**
- **Not this story — the matrix, the masking, the role catalogue and the mapping:** the permission matrix, its letters and the PDPA masking are RWB-P4-E1037-APP and RWB-P4-E1037-CON, the role rows and their catalogue are RWB-P4-E1019-APP, and the group-to-role mapping is RWB-P4-AD001-APP. This story reads `role` and `permission` for a role code and a letter and writes neither.
- **Not this story — the load and the approval of a new version, the rule versions and the ledger:** the load and approval path of a separation-of-duty version is the load path of RWB-P4-E1037-CON, the two rule-version paths of the legacy Endpoints table are the rule-version stories of this service and P7 rwb-decision's, `decision_log_entry` and the central ledger are P7's, and `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are P7's under the ownership map.

### 2. Business rationale

Separation of duty is the oldest control in a recovery operation and the one a write-off fails first: the person who proposes a write-off may not be the person who approves it, and the bank's audit expects that to be a rule of the system rather than a habit of the team. Legacy RWB-AD-005 answered it with a table of forbidden role pairs read at sign-in. The answer is still right, and the realignment makes it a service answer: the pairs are rows of `rwb_access` with a conflict version and effective dates, and one operation answers whether a resolved role set holds both halves of a pair.

The split is fixed and this story is the rule half of it. **RWB-P4-E1022-APP owns the sign-in, the token, the group claim and the resolution of a person's roles; this story owns the pair as data, the conflict version in force on the day, the check that the sign-in calls after the resolution, the refusal of the whole session, the incident, the recorded decision and the conflict version the session read answers.** Neither story can be built alone — a check with no resolved roles has nothing to check and a resolution with no check has no negative answer — and the two meet at one published operation, which is what lets each be tested against a fake from Day 1 (DP-11). The refusal is the whole session and never a part of it: a person left holding one of the two roles would be told their access is fine while the pair that made it unsafe is still held, so the negative answer is total and the person asks for a role to be removed rather than for a case to be opened.

The rule is also the reason the version matters more than the row. A pair that forbade two roles last quarter may be harmless this quarter, and a new pair may be exactly what a reorganisation needs; so a version with a valid-from date governs the next sign-in with no deployment and no restart (legacy AC2), and the session keeps the version it was checked against until it ends, so a person is never refused by a version that started in the middle of their working day. That is the same rule the matrix, the masking rows and the mapping of this service follow, and it gives the audit one answer to "which pair was in force when this person signed in".

Two consequences are the point of the slice. The first is that the refusal is evidenced twice over: a message to the person naming the pair, and a decision-record entry that names the same pair, the conflict version and the environment, so the security administrator can act without reading a log by hand and internal audit can reconstruct the refusal after the fact. The second is that the incident required by the criterion has no home in the target architecture: no source names a queue, an operation or a target for it, and the service publishes no event of its own for a refusal. The story therefore records the refusal as the incident — one entry with its addressee — rather than inventing a queue or an event name, and the open point is raised (GAP-0795; ASM-1487).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-AD005-CON (same service, its own contract story) | The published separation-of-duty contract: the check operation, the conflict-table read and the version read, the `RoleConflict`, `RoleConflictVersion`, `SodCheckRequest` and `SodCheckResult` schemas, the refusal rule, the `conflictVersion` field of the session read, the decision-record type, the error envelope and the fakes |
| RWB-P4-E1022-APP (same service, the H dependency) | Sign-on with Entra ID single sign-on, multi-factor authentication and the first roles (legacy RWB-E1-022): the sign-in that resolves a person's role codes and calls this story's check before it answers a session. Both criteria are observed through it |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the entry of every refusal, written in the same transaction as the refusal decision |
| RWB-PLT-E1042-CON and RWB-P3-E1042-CON | The parameters client library and the parameters contract of rwb-case (DP-06): the environment code recorded on the entry, read as data rather than written in code (ASM-1485) |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19), which serves SCR-43 and merges the conflict-table read with the access-log read |
| The `role_conflict`, `role` and `permission` tables in `rwb_access` | The pairs with their conflict version and dates (DF-REF-205 to DF-REF-211), the role rows a pair points at (DF-REF-034 to DF-REF-039) and the Platform administration letters of the caller (DF-REF-040 to DF-REF-044), from the service baseline of legacy RWB-E1-037 and the role matrix of RWB-P4-E1019-APP. This story seeds the pairs of its own migration and changes no column of them |
| The `v_ace_iam_group` view and its SELECT grant | The group name of a role code, its source system and its `data_as_of` (DF-ACE-301 to DF-ACE-304), read read-only through the ACE-view contract of RWB-P1-E1069-APP (DP-05). The view is never joined to a `public` table and no ACE table is read |
| A conflict version in force | The pairs the check reads, with their `valid_from` and `valid_to`. The version labels are data rows of the table and of the load path, and no source fixes the labels of the estate — **Not specified in the source documents (GAP-0795; ASM-1484)**. The tests use synthetic labels and dates |
| The environment code | SIT is the environment of the legacy story's module; the parameter code that carries the environment, and the environment codes beyond it, are **Not specified in the source documents (GAP-0795; ASM-1485)** |
| No approval step of this story's own | The approval of a new conflict version is the approval of the load path of RWB-P4-E1037-CON, which takes its approver role from the parameter; this story neither writes nor approves a version at run time (ASM-1488) |
| No human approval of this document | This story is born in Draft (realignment v1) under D-RCV-60 and builds against a Draft contract; the contract is frozen when its consumers pass their contract tests |

**Wave.** Wave 4 is taken from the W-MAP of business epic EP08 (Template and Rules §R5.6) and not from the Arch v5 wave 1 of the service, as the Work Package fixes; the release date is copied unchanged and marked tentative.

### 4. Flow

1. RWB-P4-E1022-APP has verified the token and the second factor and has resolved the person's groups into role codes on the active `role` rows. It calls `POST /api/recovery/access/v1/authorise/separation-of-duty` with the resolved role codes, the subject reference and the time of the sign-in, before it answers a session (ASM-1483).
2. The check resolves the conflict version in force: the `conflict_version` whose `valid_from` is the latest not after the date of the sign-in, and one version answers whole (legacy AC2; ASM-1484).
3. The check reads the pairs of that version from `role_conflict` and compares them with the resolved set as an unordered pair — `role_code` with `conflicts_with` and `conflicts_with` with `role_code` are the same pair, so the row is written one way and read both ways.
4. Where no pair of the version is held, the answer is allowed, with the conflict version applied and no role code echoed; the sign-in proceeds and the session carries that `conflictVersion`.
5. Where one or more pairs are held, the answer is refused, naming the two role codes of the first pair found, the conflict version and the `reason` of the row. The whole set is refused: the answer carries no partial role list, no scope and no session token (legacy AC1).
6. The refusal is written as one local decision-record entry through the library of DP-03 in the same transaction: decision code `AC-DENY`, reason code `ROLE_CONFLICT`, the two role codes, the conflict version, the environment, the subject reference and the time; no name, no e-mail address and no group membership of a person.
7. The incident goes to the security administrator through that entry: the entry names the addressee role `RW-SECADM` and the pair, so the security administrator's working list is the refusal record. A dedicated incident queue or operation does not exist and is not invented (ASM-1487).
8. The sign-in of RWB-P4-E1022-APP answers MSG-P4-006 to the person, naming both role codes, and answers no session. An existing session of the same person is not extended by the refusal and is not signed out by it; the rule is applied at the next sign-in.
9. The group of each role code is read read-only from `v_ace_iam_group` through the P1 ACE-view contract (DP-05) when the entry or the administrator's list needs to say which group gave the role, with its `data_as_of`; where the view cannot be read the refusal still stands and only the group of the entry is answered as unavailable (MSG-GEN-006).
10. The conflict-table read answers the pairs in force on a date asked — role code, conflicting role code, reason, conflict version and the two dates — and the version read answers one version by its label with its effective dates, its row count, its author reference and the decision-record entry reference of its load. Both are Platform administration R.
11. A new version reaches the next sign-in with no deployment: it is loaded and approved through the load path of RWB-P4-E1037-CON, its rows carry its `conflict_version` and `valid_from`, and the check reads the version in force on the day of the sign-in (legacy AC2; ASM-1488).
12. Every call is one hop on the caller's thread inside the 2 s budget of DP-11; the check reads `rwb_access` in its own schema and the group reference of the same database through the P1 grant, and calls no other service.
13. The story writes no role, no letter, no masking row, no delegation limit and no session: a pair says which two roles may not be held together, and what a role may do is the permission matrix of RWB-P4-E1037-APP.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The resolved role set holds both halves of a pair at the conflict version in force | The whole session is refused, the pair is named, the entry is written with reason `ROLE_CONFLICT` and the incident goes to the security administrator | MSG-P4-006 | AC1 |
| X2 | The resolved role set holds two pairs at once | The refusal names the first pair of the version by the order of the rows, and the entry names every pair held; the session is refused once, not twice | MSG-P4-006 | AC1 |
| X3 | The check is called with no subject reference or no role code list | 401 with MSG-P4-001 and no entry beyond the refusal of the call, because a call with no subject is not a sign-in | MSG-P4-001 | AC1 |
| X4 | The resolved set is empty | The answer is allowed with no pair, and the sign-in of RWB-P4-E1022-APP answers MSG-P4-001 to a person left with no role; this story invents no role | MSG-P4-001 (raised by the sign-in) | AC1 |
| X5 | No conflict version is in force on the date of the sign-in | The check fails closed: the session is refused, the pair is not guessed and the entry names the missing version; 503 to the caller | MSG-GEN-004 in the answer; the entry in the library | AC2 |
| X6 | Two versions are in force on the same date | Exactly one answers — the one whose `valid_from` is the latest not after the date — and the read never mixes two versions | None | AC2 |
| X7 | The decision-record entry cannot be written | 503 with MSG-P7-003, no session is answered and the refusal is not reported as complete | MSG-P7-003 | AC1 |
| X8 | The ACE group reference cannot be read | The refusal stands and the group is answered as unavailable with its reason; no refusal is withdrawn for want of a group name | MSG-GEN-006 | AC1 |
| X9 | The caller of the conflict-table read or of the version read holds no Platform administration R | 403 before any row is read, one refusal entry | MSG-P4-002 | AC2 |
| X10 | The version label, the role code or the pair asked for does not exist | 404 with the envelope; no row is answered and none is invented | MSG-GEN-004 (envelope `messageId`) | AC2 |
| X11 | A sign-in happens on the day a new version starts | The check applies the version whose `valid_from` is the latest not after that day; a session already open keeps the version it was checked against until it ends | None | AC2 |

No exception path of this story changes a case, a task, an approval or a queue: this service holds the pairs, and the case state machine and the approval are other services'.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the separation-of-duty contract of RWB-P4-AD005-CON and its fakes, the decision-record library, the parameters contract and the gateway-bff route; it reads and writes `role_conflict` in its own schema and reads no table of another service |
| Negotiable | The pairs, the reasons, the version labels and the dates are data rows loaded through the load path of this service; the story fixes the check, the refusal rule and the read shape only |
| Valuable | A forbidden pair is refused at the door with one message to the person and one recorded decision to the security administrator, and a new pair reaches the next sign-in with no release |
| Estimable | One migration that seeds the pairs the sources name, one check, two reads, one refusal record and its entry, and the `conflictVersion` value of the session |
| Small | Fits one sprint with its tests; the sign-in, the session, the permission matrix and the screens are other stories' |
| Testable | Every criterion in section 7 is one automated test over synthetic conflict rows and a fixed clock; no real group, person or entitlement is needed |

### 7. Acceptance criteria

```gherkin
Feature: Separation of duty check at sign-in

  Background:
    Given the rwb-access base path is /api/recovery/access/v1 and the schema is rwb_access
    Given a pair is a "role_conflict" row of one conflict version in "rwb_access"
    Given a conflict version answers whole and the version in force is the one whose valid from is the latest not after the date of the sign-in

  Scenario: AC1 Conflict refused (legacy RWB-AD-005 AC1)
    Given the platform library contract mock returns the decision-record entry accepted on "rwb.decision-record.v1" for the refusal
    Given a person in the groups for RW-WRITEOFF and RW-WOCOMM
    When they sign in
    Then the system refuses the session and an incident goes to the security administrator

  Scenario: AC2 Table as data (legacy RWB-AD-005 AC2)
    Given a new separation of duty version
    When it is approved
    Then the next sign-in checks against it
```

The two criteria are the legacy criteria of RWB-AD-005, copied word for word with the origin tag. One Given line is added and nothing else is changed: the faked answer of the decision-record library (DP-03) for the refusal, which is what makes AC1 observable without a live library. Every legacy value is kept character for character: the two role codes `RW-WRITEOFF` and `RW-WOCOMM`, the sign-in, the refused session, the incident to the security administrator, and the new version that the next sign-in checks against.

AC1 is answered by the check over the version in force and is observed through the sign-in of RWB-P4-E1022-APP, the H dependency that calls the check; AC2 is answered by the version rule of the check — the version whose `valid_from` is the latest not after the date of the sign-in — while the approval of the version is the load path of RWB-P4-E1037-CON and not this story's, so the criterion is tested from this side with the version arriving as data (ASM-1488). The incident of AC1 has no queue and no operation in any source: it is carried by the recorded refusal, whose addressee is the security administrator (ASM-1487).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A pair one person may not hold together is one `role_conflict` row of two role codes with its reason, its conflict version and its two dates. No pair, reason, version label or date is written in code | Legacy RWB-AD-005 story statement and Data table; TSD P4 v3 T3.1 (DF-REF-205 to DF-REF-211); RWB-P4-E1022-APP section 3 |
| BR2 | A conflict version answers whole, and the version in force is the one whose `valid_from` is the latest not after the date of the sign-in; a version's rows stay readable with their own `valid_to` | Legacy RWB-AD-005 AC2; TSD P4 v3 T3.1; T4 (LOV-VERSION-STATUS) |
| BR3 | Where the resolved role set holds both halves of a pair at the version in force, the whole session is refused: no role, no scope and no partial session is answered | Legacy RWB-AD-005 AC1; FSD P4 v3 AC-EXC-P4-001-03 |
| BR4 | The refusal names both role codes of the pair and the conflict version, and it carries MSG-P4-006. The message ID is fixed; its text is not fixed by any source and is not invented here | FSD P4 v3 AC-EXC-P4-001-03; GAP-0795; ASM-1489 |
| BR5 | Every refusal writes one local decision-record entry through the library of DP-03 — decision code `AC-DENY`, reason code `ROLE_CONFLICT`, the pair, the conflict version, the environment and the subject reference — and no name and no e-mail address. Where the entry cannot be written the session is not answered | DP-03; FSD P4 v3 AC-EXC-P4-001-06; MSG-P7-003; ASM-1486 |
| BR6 | The incident the criterion requires goes to the security administrator through the recorded refusal, because no source names an incident queue, an incident operation or a target service; no event name is invented for it | Legacy RWB-AD-005 AC1; FSD P4 v3 AC-EXC-P4-001-03; Architecture v5 slide 14; ASM-1487 |
| BR7 | A session keeps the conflict version it was checked against until it ends, and a version that starts after a sign-in reaches that person at the next sign-in | Legacy RWB-AD-005 AC2; ASM-1484 |
| BR8 | A pair that forbids one role with any business role is carried as one row per business role at the same conflict version, because `conflicts_with` holds one role code of varchar(30) | FSD P4 v3 AC-EXC-P4-001-03; TSD P4 v3 T3.1 (DF-REF-207); ASM-1490 |
| BR9 | The conflict-table read and the version read need the Platform administration R letter; the check is called by the sign-in of this service with a subject reference, and a call with no subject is 401 with MSG-P4-001. Default deny applies to both | TSD P4 v3 T6.1 and API-P4-007; TSD P4 v3 API-P4-012; FSD P4 v3 VR-P4-004-1 |
| BR10 | The group of a role code is read read-only from `v_ace_iam_group` through the P1 ACE-view contract with its `data_as_of`, and never from `public.iam_group`, a `public` table or another service's table | TSD P4 v3 T3.1; DP-05; DP-01 |
| BR11 | The environment code is read as a parameter through the parameters contract of rwb-case and recorded on the entry, so the same build serves every environment | DP-06; ASM-1485 |
| BR12 | A new conflict version is approved through the load path of RWB-P4-E1037-CON; this story reads the version in force and neither writes nor approves a version at run time, so a new pair needs no deployment and no code change | ASM-1488; DP-15; Template and Rules §R5.5 |

Where each rule sits in the target: BR1, BR2, BR8 and BR12 are answered from `rwb_access` only, with the version and the dates on the pair rows. BR3 and BR4 are the check and its negative answer. BR5 is the decision-record library and the outbox of the service template. BR6 is the open point of the key and is carried as a gap. BR7 is the value the sign-in keeps. BR9 is the guard and the letters of the caller's own permission rows, answered in one hop. BR10 is enforced by the module map and by boundary rule BND-6 of RWB-P4-E1069-APP. BR11 is the parameters client of DP-06.

### 9. State transitions

None for a case, a task or an approval. The states of this story are the states of a conflict version and the outcomes of one sign-in.

| From | Event | Condition | To |
|---|---|---|---|
| No conflict version of an environment | The first version is seeded by this story's migration | Every row passes the checks of the load path | The version is in force from its `valid_from` |
| The version in force | A new version is approved through the load path of RWB-P4-E1037-CON | The approval passes | The new version is in force from its `valid_from`; the rows of the earlier version keep their own `valid_to` (ASM-1488) |
| The version in force | A read on a day inside two versions | None | Exactly one version answers, the one whose `valid_from` is the latest not after the day asked |
| A resolved role set | the check of this story runs | No pair of the version is held | ALLOWED; the session carries the `conflictVersion` applied |
| A resolved role set | the check of this story runs | Both halves of a pair are held | REFUSED (`ROLE_CONFLICT`): no role, no scope, MSG-P4-006, one entry, the incident to the security administrator |
| A resolved role set | the decision-record entry cannot be written | The library answers 503 | The session is not answered and the outcome is not a refusal: the check fails closed with MSG-P7-003 |
| A session already open | A new version starts | None | The session keeps the version it was checked against until it ends |
| A refused person | Their roles are changed and they sign in again | No pair is held at the version in force | ALLOWED; the session carries the new `conflictVersion` |

The version status vocabulary is LOV-VERSION-STATUS (LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED) in TSD P4 v3 T3.2. This story reads the version in force; the load, the approval and the rollback of a version of the table are the load path of RWB-P4-E1037-CON and are not carried here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-access service identity (the per-service login, DP-02) | Answers the check, the conflict-table read and the version read, resolves the version in force, writes the decision-record entry of a refusal and reads the group of a role code read-only |
| The sign-in of RWB-P4-E1022-APP | Calls the check with the resolved role codes and the subject reference of the person signing in, after the resolution and before the session answer. It holds no letter of this story: it is the same service |
| RW-SECADM, security administrator | CRUDA in Platform administration (TSD P4 v3 T6.1): reads the pairs and their versions and is the addressee of every refusal. The legacy story names this role as the actor |
| RW-PLATADM, platform administrator | CRUD in Platform administration (TSD P4 v3 T6.1): reads the pairs and their versions as the security administrator does |
| RW-AUDIT, internal audit | R in Platform administration: reads the pairs, the versions and the entries of the refusals. Writes nothing |
| RW-COE, center of excellence analyst | CRUD in Rules and parameters and R in Platform administration: reads the pairs only. A pair is not a rule, so this story gives it no write path |
| RW-WRITEOFF and RW-WOCOMM | Hold R in Rules and parameters and R in Reference data and no Platform administration right (TSD P4 v3 T6.1): they are subject to the pair of AC1 and read nothing of this story |
| Every other role and every service identity | Is subject to the check at its own sign-in and reads nothing of this story's operations |
| No delegation of authority level applies | A pair is not a credit decision, and no limit of `delegation_limit` is read |

The pair table is role administration and not reference data: `role_conflict` is P4's own table under the ownership map, and the reference-data contract of rwb-case holds `lov_value`, `reference_row` and `reference_version` only. The database login is the per-service login of the service baseline (DP-02), and this story adds no grant beyond the SELECT on the ACE view that RWB-P1-E1069-APP already grants.

The legacy Permission checks table gives this story the Rules and parameters letters C and A through RW-COE and RW-RISK, and the legacy Endpoints table gives it the two rule-version paths. Neither is kept: the rule-version paths and their rights belong to the rule-version stories of this service and to P7 rwb-decision, and the separation-of-duty table is Platform administration data read under R (GAP-0795; ASM-1488).

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-205 | `role_conflict` | id | Written by the migration seed; read by both reads |
| DF-REF-206 | `role_conflict` | role_code (LOV-ROLE) | Written by the migration seed; read by the check and both reads |
| DF-REF-207 | `role_conflict` | conflicts_with | Written by the migration seed; read by the check and both reads |
| DF-REF-208 | `role_conflict` | reason | Written by the migration seed; read, and answered on a refusal |
| DF-REF-209 | `role_conflict` | conflict_version | Written by the migration seed; read, to resolve the version in force |
| DF-REF-210 | `role_conflict` | valid_from | Written by the migration seed; read, to resolve the version in force |
| DF-REF-211 | `role_conflict` | valid_to | Written by the migration seed and by the load path of RWB-P4-E1037-CON; read, to resolve the version in force |
| DF-REF-034 to DF-REF-038 | `role` | id, role_code, role_name, role_class, default_scope | Read, to confirm that a role code of a pair is an active role row and to answer its name. Never written here |
| DF-REF-039 | `role` | entra_group | Read only as the group that gave a role code to the person; the mapping is RWB-P4-AD001-APP's and is not written here |
| DF-REF-040 to DF-REF-044 | `permission` | role_id, capability_area, letters, matrix_version | Read, for the Platform administration letters of the caller. Never written here |
| DF-ACE-301 to DF-ACE-304 | `v_ace_iam_group` | entra_group, role_code, source_system, data_as_of | Read read-only through the P1 ACE-view contract; the view is never written |
| Not specified in the source documents (GAP-0795; ASM-1486) | the local decision record of DP-03 | the refusal entry: decision code, reason code, the pair, the conflict version, the environment, the subject reference and the time | Written through the decision-record library; no field is invented here |
| DF-REF-027 to DF-REF-033 | `lov_value` of `rwb_case` | lov_code, value_code, label_en, sort_order, valid_from | Not read by this story: a role code and a capability area travel as codes, and the list values behind them are RWB-P4-E1019-APP's read through the reference-data contract |
| Not specified in the source documents (GAP-0795; ASM-1485) | the parameters of the estate | the environment code of this deployment | Read through the parameters contract of rwb-case; no parameter row is held here |

Two values the sources do not fix are carried as placeholders. The parameter that carries the environment code, and the codes beyond the legacy module's environment, are **Not specified in the source documents (GAP-0795; ASM-1485)**. The fields of the local decision-record entry are the library's and are **Not specified in the source documents (GAP-0795; ASM-1486)**; the decision code `AC-DENY` and the reason code `ROLE_CONFLICT` are the values the functional specification and the sibling slices use, and they are copied. The conflict version labels of the estate are data rows and no source fixes them, so the tests use synthetic labels and dates. Field IDs are those in the Logical Data Model and Data Dictionary v8, and the legacy physical names `role`, `permission` and `role_conflict` are kept.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-access` (P4); base `/api/recovery/access/v1`. The check path is this revision's decision and has no row in the ownership map and none in TSD P4 v3 appendix T-A — **Not specified in the source documents (GAP-0795; ASM-1483)**.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise/separation-of-duty` | The check: the resolved role codes in, and allowed out, or the conflicting pair with its conflict version and reason | The sign-in of this service with the subject reference of the person signing in; no capability letter | Not applicable, no state is written by the check; the refusal entry is keyed by the sign-in |
| GET | `/api/recovery/access/v1/admin/role-conflicts` | The pairs in force on the date asked: role code, conflicting role code, reason, conflict version, valid-from and valid-to. Query `roleCode`, `validOn`, `conflictVersion`, `page`, `size` | Platform administration R (TSD P4 v3 T6.1) | Not applicable, read only |
| GET | `/api/recovery/access/v1/admin/role-conflict-versions/{versionId}` | One conflict version with its effective dates, its row count, its author reference and the decision-record entry reference of its load | Platform administration R | Not applicable, read only |

The session read `GET /api/recovery/access/v1/me/session` (API-P4-012) belongs to RWB-P4-E1037-CON; this story supplies the `conflictVersion` value that read answers and adds no operation and no field of its own. The route the three operations sit on is the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON).

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case`, published by RWB-P3-E1042-CON (DP-06) | The environment code recorded on a refusal entry. The parameter code is **Not specified in the source documents (GAP-0795; ASM-1485)** |

The ACE group reference is a read-only SQL read and not a call to another service: `recovery.v_ace_iam_group` (DF-ACE-301 to DF-ACE-304) is granted and contracted by RWB-P1-E1069-APP (DP-05) and answers the group name, the source system and the `data_as_of` of a role code. It is never `public.iam_group` and never a `public` table. The reference-data contract of rwb-case is not consumed: this story resolves no list value, because a role code and a conflict version travel as codes in `role_conflict`.

#### 12.3 Events published

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | PLT library, consumed by P7 | Entry id, decision code `AC-DENY`, reason code `ROLE_CONFLICT`, the two role codes, the conflict version, the environment and the time; written by the library of DP-03, not by this story's own writer |

The message uses the CloudEvents 1.0 envelope with the attributes id, source, type, specversion, time, subject and datacontenttype. No access event is published by this story: a new conflict version is loaded through the load path of RWB-P4-E1037-CON, which publishes `rwb.access.AccessPolicyChanged.v1` with its own change kind, and `rwb.access.DoaLimitChanged.v1` belongs to the delegation table. No third event name is invented for a refusal, because a refusal is a decision record and not a policy change (ASM-1487).

#### 12.4 Events consumed

None. rwb-access is a reference-data owner in Architecture v5 slide 14 (events: none), the version in force is read from `rwb_access` on each call, and this story subscribes to no topic and writes no inbox row.

#### 12.5 Workflows and activities

None. The check and the two reads are synchronous REST answers in the caller's thread. The six-monthly access review list (JOB-18, Architecture v5 slide 44) is RWB-P4-AD008-APP's; this story starts no workflow, signals none and registers no activity on the `rwb-access` queue.

#### 12.6 Schedules

None. No Temporal Schedule and no quartz job sits in this story: the `valid_from` date of a version is a row value the check resolves, and nothing about a pair runs on a clock.

#### 12.7 Tables owned

| Table | Schema | Owner (ownership map) | This story |
|---|---|---|---|
| `role_conflict` | `rwb_access` | P4 | Writes the pairs of its own migration seed; reads the version in force; the load path of RWB-P4-E1037-CON writes a new version and this story writes none at run time |
| `role` | `rwb_access` | P4 | Reads an active role row and its name and group; never writes |
| `permission` | `rwb_access` | P4 | Reads the caller's Platform administration letters; never writes |
| `outbox_event`, `processed_event`, `idempotency_key` | `rwb_access` | PLT library | Created by the service baseline; the record library writes the outbox row of a refusal, and this story writes none by hand |
| `masking_rule`, `delegation_limit`, `access_log` | `rwb_access` | P4 | Not read and not written by this story; the access log is RWB-P4-AD007-APP's and RWB-P4-E1039-APP's |
| `v_ace_iam_group` | ACE database, read-only view | ACE / P1 `rwb-source-data` | Read read-only through the P1 ACE-view contract (DP-05) |
| `lov_value`, `reference_row`, `reference_version` | `rwb_case` | P3 | **Never read by SQL**; they are P3's reference data and this story applies no reference-data read |
| `parameter_catalog`, `parameter_value` | `rwb_case` | P3 | **Never read by SQL**; the environment code arrives through the parameters contract (DP-06) |
| `decision_log_entry` | `rwb_decision` | P7 | Not read and not written; the central ledger is P7's and the local entry is the library's |
| `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` | `rwb_decision` | P7 | Not read and not written; the ownership map keeps the rule registry with P7 despite TSD P4 v3 declaring the tables |
| `partner_user` | `rwb_partner` | S9 | Not read and not written; the ownership map gives it to S9 |

No foreign key crosses a schema and no statement in this story names a table outside `rwb_access` except the read-only ACE view of the P1 contract. `role_conflict` is the Workbench's own data and stays with this service.

#### 12.8 Contract fakes

| Fake | Serves | Used for |
|---|---|---|
| Separation-of-duty contract fake (RWB-P4-AD005-CON) | The three paths of 12.1: a version in force with a held pair, a version in force with no pair, a next version with a later `valid_from`, the conflict-table read and the version read | AC1 and AC2, and every test that checks a role set or reads a pair |
| Sign-in fake (RWB-P4-E1022-CON) | A resolved role set for a person, with the two role codes `RW-WRITEOFF` and `RW-WOCOMM`, and a set with one of them only | AC1, so no live sign-in is needed |
| Parameters fake (RWB-P3-E1042-CON) | The environment code of the deployment | AC1, so no environment is a constant in the test |
| ACE group fake | `v_ace_iam_group` with the group of each role code and its `data_as_of`, plus a role code the view no longer holds | AC1 |
| Decision-record fake (RWB-PLT-E1027-CON) | The entry append, the hash-chain check and the 503 with MSG-P7-003 | AC1 |

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 3 operations under `/api/recovery/access/v1` | 1 operation | OpenAPI 3.1, one hop, 2 s timeout; plus one read-only SQL read of the ACE view |
| Kafka | 1 published | 0 | `rwb.decision-record.DecisionRecorded.v1`; no access event of this story |
| Temporal | None | None | No workflow, activity or Schedule in this story |
| File | None | None | No file in this capability |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access.sod`, module `sod`, in the service root `th.co.scb.ace.workbench.recovery.access`. Service base `/api/recovery/access/v1`, schema `rwb_access`, topic `rwb.access.events.v1`, Temporal task queue `rwb-access` (not used here).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the entry of every refusal and the outbox row that publishes it. DP-05 is the read-only ACE view that answers the group of a role code with its `data_as_of`; the view and its SELECT grant come from RWB-P1-E1069-APP and this story adds no dependency for them. DP-06 is the environment code read as data, so one build serves every environment. DP-13 is the base of the three operations. DP-19 is the composite route that serves SCR-43 with the conflict-table read and the access-log read. The outbox relay and the inbox are the service template's own library objects and add no dependency to this story, which is why they are not in this key's pattern set.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `V4005_1__role_conflict_seed.sql` | Migration | Creates the pairs the sources name in `rwb_access` — `RW-WRITEOFF` with `RW-WOCOMM`, and `RW-SECADM` with each business role of the matrix — each with its conflict version, its reason and its `valid_from`; one index on the conflict version and `valid_from` for the read; copies no ACE value and no value of a person |
| `SodCheckService` | Service | The check of BR1 to BR4 over a resolved role set at the version in force: allowed, or the pair with its version and reason; refuse the whole set, never a part of it |
| `ConflictVersionResolver` | Service | The version in force on the date of the sign-in, one version whole (BR2) |
| `RoleConflictRepository` | Repository | Reads the pairs of a version, one version by its label and the version in force on a date; writes no row at run time |
| `SodRefusalRecorder` | Service | Writes the decision-record entry of a refusal through the library of DP-03 and the outbox row that publishes it (BR5) |
| `AceGroupReferenceClient` | Client | Reads the group of a role code read-only through the P1 ACE-view contract with `data_as_of`; no write and no join to a `public` table |
| `EnvironmentParameterClient` | Client | The environment code through the parameters contract of DP-06; no environment code in code or in a profile |

**Database and migrations**

- Writes `role_conflict` in `rwb_access` by the migration seed only: the pairs of AC1 and of the FSD example, with their `conflict_version`, `valid_from`, `valid_to` and `reason`.
- Migration `V4005_1__role_conflict_seed.sql` sits on the per-service Flyway sequence after the V0001 baseline (DP-15). It creates the pairs, one index on the version and the `valid_from` for the read, and no column, because `role_conflict` carries its version and dates already (TSD P4 v3 T3.1); it drops nothing and copies no ACE value.
- The read predicate is the version in force on the date of the sign-in; the version is a value, never a date written in code.
- A new version is written by the load path of RWB-P4-E1037-CON and by no statement of this story; the read path of this story has no write method.
- DB access uses the per-service rwb-access login of the service baseline (DP-02). No grant on `rwb_case`, on `recovery` or on `public` is added by this story beyond the SELECT on the ACE view that RWB-P1-E1069-APP already grants.

**Configuration and reference data**

- The pairs, the reasons, the conflict version labels and the dates are data rows; none is a constant in code (BR1).
- The environment code arrives as a parameter through the parameters contract (DP-06); its parameter code is **Not specified in the source documents (GAP-0795; ASM-1485)**.
- The message ID MSG-P4-006 is fixed; its text is **Not specified in the source documents (GAP-0795; ASM-1489)** and is not written by this story.
- No feature switch: a pair is changed by rows and by their dates, not by a flag, and the check is always on for a session that resolves at least one role.

**Build steps**

1. `V4005_1__role_conflict_seed.sql` with the pairs of AC1 and of the FSD example, their version and dates, plus a fixture that applies it twice; test AC1.
2. `ConflictVersionResolver` on a fixed clock with two versions and a gap between them, so exactly one answers and a missing version fails closed (BR2); test AC2.
3. `SodCheckService` with one case per shape: a held pair, an unheld pair, a pair written in the reverse order, two pairs held at once and an empty set (BR3, BR8); test AC1 and AC2.
4. `SodRefusalRecorder` with the entry, the outbox row and the forced failure that answers 503 with MSG-P7-003; test AC1.
5. `AceGroupReferenceClient` over the ACE-view fake with `data_as_of`, and the 503 when the view cannot be read; test AC1.
6. `EnvironmentParameterClient` over the parameters fake, so a later environment needs no build (BR11).
7. The conflict-table read and the version read with the Platform administration R letter through the guard of RWB-P4-E1037-CON, and the 403 with MSG-P4-002; test AC2.
8. The `conflictVersion` value handed to the session read of RWB-P4-E1037-CON, so a session states the version it was checked against (BR7); test AC2.
9. The boundary check: no statement names a `public` table, a `v_ace_*` view other than `v_ace_iam_group`, a table of another service or a rule package table; BND-6 of RWB-P4-E1069-APP stays green on this package.

**Done when.** The tests in section 16 pass; `role_conflict` holds the pair `RW-WRITEOFF` with `RW-WOCOMM` at a version with a `valid_from`; a resolved set holding both codes is refused with MSG-P4-006, no role and no scope, and one entry with reason `ROLE_CONFLICT` is on `rwb.decision-record.v1`; a set holding one of the two is allowed; a new version with a later `valid_from` answers from that date with no deployment; a forced record failure leaves the session unanswered and answers 503 with MSG-P7-003; and no statement in the service names a table outside `rwb_access` or a `public` table.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The check is called with no subject reference or with no role code list, or a sign-in resolves no role at all | You have no Recovery Workbench role. Ask your team manager to request one. | The check of this story; the sign-in of RWB-P4-E1022-APP for the empty set |
| MSG-P4-002 | The caller of a read holds no Platform administration R | You cannot {action} here. Your role does not include it. | The guard, on both reads |
| MSG-P4-003 | A path this service does not publish, or a record outside the caller's scope | This case is not in your scope. | The reads, as a 404 |
| MSG-P4-006 | The resolved role set holds both halves of a pair at the conflict version in force | Not specified in the source documents (GAP-0795; ASM-1489); the message ID and the two role codes are fixed, the text is not | The check, and the sign-in that answers the person |
| MSG-GEN-001 | A required field of a read is empty or malformed, or a role code of a pair is not an active role row | Enter {field}. | The reads, as a 422 with the field named |
| MSG-GEN-004 | The version label, the role code or the pair asked for does not exist, or no version is in force on the date asked | Someone else changed this record. Reload it to see their change. | The reads and the check |
| MSG-GEN-006 | The ACE group reference cannot be read | The reference data is not available. Try again later. | The check and the entry of a refusal |
| MSG-P7-003 | The decision-record entry of a refusal cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The check, through the library of DP-03 |

Every error is an RFC 9457 problem response with `messageId` set and `detail` carrying the text with its placeholders filled. For MSG-P4-002 the {action} value names the action the caller tried — "read the separation-of-duty table" or "read a conflict version" — and never a case fact, a role code of another person or a group membership. MSG-P4-006 names the two role codes of the pair and the conflict version applied, and never a person, a group membership or a case.

### 15. Screens and states

No screen is built by this story. SCR-43 Roles and access shows the roles, their permissions, the conflicting pairs and the access log, and the security administrator and internal audit read it there; it is served by the gateway-bff composite route of DP-19, which calls the conflict-table read and the access-log read in parallel, one hop each, and renders the rows. The screen field list, the column order and the merge are the screen owner's, and this story returns the pairs and the versions only.

| Screen | State | What the operator sees |
|---|---|---|
| SCR-43 Roles and access | List | The pairs in force for the environment: role code, conflicting role code, reason, conflict version and the two dates |
| SCR-43 Roles and access | Version | One conflict version with its effective dates, its row count and the reference of the decision-record entry of its load |
| SCR-43 Roles and access | Access log | The entries of the refusals with reason `ROLE_CONFLICT`, the pair and the time, read through the access-log operation of RWB-P4-AD007-APP on the same composite route |
| SCR-43 Roles and access | Refused | MSG-P4-002 or MSG-P4-001, with no pair and no version |
| SCR-43 Roles and access | Not available | MSG-GEN-006 for the group reference and MSG-P7-003 for the record, each with the retry advice of the message |

A person refused at sign-in sees MSG-P4-006 through the sign-in screen of RWB-P4-E1022-APP and no screen of this story: the refusal carries the two role codes and the way to ask for a role to be removed.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-005-01 | AC1 | End to end | Legacy test "Conflict refused": a synthetic person whose resolved set holds `RW-WRITEOFF` and `RW-WOCOMM` at the version in force signs in; the session is refused with MSG-P4-006 naming both codes, one entry with reason `ROLE_CONFLICT` is on `rwb.decision-record.v1`, and the incident is addressed to the security administrator |
| TC-AD-005-02 | AC2 | End to end | Legacy test "Table as data": two conflict versions with `valid_from` dates D and D2 on a fixed clock (synthetic labels and dates); a version approved through the load path answers from D, the next sign-in is checked against it, a session already open keeps the version it was checked against, and the earlier rows stay readable with their `valid_to` |
| TC-AD-005-03 | Access | Component | Legacy test "A role without the right is refused with MSG-P4-002": `RW-PHONECOL` with no Platform administration letter calls the conflict-table read and the version read; 403 with MSG-P4-002 on each, one refusal entry each, and no row answered |
| TC-AD-005-04 | Principle 5 | NFR | Legacy test "A forced decision log write failure stops the action with MSG-P7-003": the decision-record write forced to fail on a refusal; 503 with MSG-P7-003, no session answered and no refusal reported as recorded |

The four legacy test cases are kept with their IDs and their legacy Covers values; the legacy test name is written in the Data column and the Level column follows Template and Rules §R7.2, where the legacy level Access maps to Component and the legacy level Resilience to the Principle 5 row at NFR. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The ITG copy of the set is RWB-ITG-AD005-ITG's and is not written here, so no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in code: the pairs, the reasons, the conflict version labels and the dates are rows of `role_conflict`, and the environment is a parameter; a test proves that a new pair needs no build (BR1, BR11).
- No personal data anywhere: a pair is two role codes, a refusal carries a subject reference and no name, and no test row, log, event or prompt holds a name or an e-mail address (BR5).
- No read of another schema (DP-01): `lov_value`, the reference tables, the parameter tables, `decision_log_entry`, the rule package tables and `partner_user` are never read by SQL, and the only external read is the read-only ACE view `v_ace_iam_group` of the P1 contract.
- ACE data only through the owner's contract or the service's own `v_ace_*` view (DP-05): no statement names `public.iam_group`, a `public` table or a table of another service, and boundary rule BND-6 of RWB-P4-E1069-APP stays green on this package.
- One writer per row set: this story's migration seeds the pairs it names, the load path of RWB-P4-E1037-CON writes a new version, and the read path of this story has no write method, so a read can never change a pair (BR12).
- Default deny on every call: a call with no subject is 401 and a missing letter is 403 with MSG-P4-002, never an allow (BR9).
- Fail closed on a refusal: a refusal whose entry cannot be written is not a refusal and no session is answered (BR5); a missing conflict version refuses the session rather than allowing it (X5).
- A version answers whole or not at all, and a session keeps the version it was checked against until it ends (BR2, BR7).
- One event name for the record, `rwb.decision-record.DecisionRecorded.v1`, and no invented access event for a refusal; a new version publishes the access-policy event of its own load path (BR6).

### 18. Traceability

No requirement ID is recorded for legacy RWB-AD-005 in TSD P4 v3 T8, the legacy story's Feature row reads None, and the Work Package carries the requirement list of this key as empty. The control the key serves is named by the FSD P4 v3 exception row AC-EXC-P4-001-03, "A conflicting role pair is refused", which fixes the message MSG-P4-006, the two role codes of its example, the incident to the security administrator and the refusal reason `ROLE_CONFLICT`.

| Reference | Where this story answers it | Test cases |
|---|---|---|
| FSD P4 v3 AC-EXC-P4-001-03, a conflicting role pair is refused | The check over the version in force, the whole-session refusal and the message naming the pair (sections 4, 7, 8) | TC-AD-005-01 |
| The role conflict table as data with a version | `role_conflict` with `conflict_version`, `valid_from` and `valid_to`, and the version rule of the check (sections 8, 11, 12.7) | TC-AD-005-02 |
| The incident to the security administrator | The recorded refusal with its addressee role, and the open point carried as a gap (sections 4, 8, 14) | TC-AD-005-01 |
| The record-before-refusal rule | The entry of DP-03 before the refusal stands (sections 4, 14) | TC-AD-005-04 |
| The permission check of the administration reads | The Platform administration R letter and MSG-P4-002 on both reads (sections 8, 12.1) | TC-AD-005-03 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P4-AD005-CON | Contract | H: the separation-of-duty contract, its four schemas, the refusal rule, the `conflictVersion` field and the fakes |
| RWB-P4-E1022-APP | App development | H: the sign-in that resolves the role codes and calls the check before it answers a session |
| RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-N001-CON | Contract | H: the decision-record library, the parameters library and the gateway-bff composite route |
| RWB-P3-E1042-CON | Contract | C: the parameters contract of rwb-case that answers the environment code |
| RWB-P1-E1069-APP | App development | The ACE view `v_ace_iam_group` and its SELECT grant, read read-only; named as the reference, not on the build row |
| RWB-P4-E1019-APP, RWB-P4-E1037-APP | App development | The role catalogue, the permission matrix, the masking and the session of this service; this story changes none of them |
| RWB-P4-AD001-APP | App development | Sibling slice of the same legacy module: the group-to-role mapping that gives a role code its group |
| RWB-ITG-AD005-ITG | Integration | The cross-service proof that a refused session stops at the door and that the refusal reaches the security administrator |

| Legacy reference | Where it is kept |
|---|---|
| The story statement (a session refused when a person's groups hold a conflicting role pair) | Sections 1, 2, 8 (BR1, BR3) |
| Legacy AC1 and AC2 with `RW-WRITEOFF`, `RW-WOCOMM`, the incident and the new version | Section 7, section 14 |
| The Data table: `role` DF-REF-034 to DF-REF-038 | Section 11 |
| The permission checks Rules and parameters C and A | Section 10 (not kept; the rule-version rights are other stories') |
| The validation and messages MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-GEN-001, MSG-P7-003 | Section 14, exception paths |
| The message MSG-P4-006 of the FSD | Section 14, and the open point of its text |
| Screen SCR-43 Roles and access | Section 15 |
| Legacy test cases TC-AD-005-01 to TC-AD-005-04 | Section 16 |

### 19. Out of scope

- The sign-in itself, the token, the second factor, the group claim and the resolution of a person's roles: RWB-P4-E1022-CON and RWB-P4-E1022-APP (legacy RWB-E1-022). This story owns the rule the sign-in calls and the refusal fact; it owns no session.
- The permission matrix, its letters, the masking rows and the session read itself: RWB-P4-E1037-CON and RWB-P4-E1037-APP; `GET /me/session` (API-P4-012) is theirs, and this story supplies one value only.
- The role rows, the role catalogue and the groups of the roles: RWB-P4-E1019-APP.
- The group-to-role mapping and its maintenance: RWB-P4-AD001-APP.
- The load, the approval and the rollback of a separation-of-duty version, and the matrix and masking loads of the same module: the load path of RWB-P4-E1037-CON with RWB-P4-AD002-APP, RWB-P4-AD004-APP and RWB-P4-AD010-APP.
- The two rule-version paths of the legacy Endpoints table, a load and an approval: the rule-version stories of this service and P7 rwb-decision under the ownership map. They are listed here as the legacy rows they are and are not restated as paths of this story.
- The rule package registry and its tables (`rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`): P7 rwb-decision under the ownership map, despite TSD P4 v3 declaring them.
- The access review list and the six-monthly Schedule (JOB-18): RWB-P4-AD008-APP. The access-log search and the export: RWB-P4-AD007-APP; the access log itself is RWB-P4-E1039-APP's. The break-glass grant: RWB-P4-AD006-APP.
- The central decision ledger and its query: P7 rwb-decision; this story writes the local entry only.
- The reference data — `lov_value`, `reference_row` and `reference_version` — and the parameter values of the estate: P3 rwb-case under the ownership map; this story consumes the parameters contract and holds no parameter row.
- `partner_user`: S9 rwb-partner under the ownership map.
- The incident queue, the incident operation and the target service of the incident the criterion requires: named by no source, carried as a gap and an assumption, and not created by this story (GAP-0795; ASM-1487).
- The bank IAM's own group administration: Entra ID and the bank IAM (INT-21).
- The Helm chart, the topic creation, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
- The integration harness and its evidence, and the `-ITG` copies of the test cases: RWB-ITG-AD005-ITG.
