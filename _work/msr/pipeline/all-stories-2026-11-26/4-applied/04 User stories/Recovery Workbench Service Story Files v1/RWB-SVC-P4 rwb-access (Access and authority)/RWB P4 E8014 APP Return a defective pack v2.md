# RWB-P4-E8014-APP Return a defective pack

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8014-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-014 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP06, DP13, DP19 |
| Parallel lane | L-P4-BH |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P4-E8014-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-014 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-E8014-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer whose role owns a pack**, I want **every candidate access pack to be checked before it is released, and a pack that fails to be sent back to the role that owns it with each defect named — the row, the field and the rule it breaks — and the verdict recorded against the pack version and the rule version in force**, so that **an access change that would break the matrix, the scope or the masking is corrected by its owner before it can reach the service, and a code release is not needed to change a role, a letter or a masking profile**.

Inside `rwb-access` this is the pack check and return gate of the legacy story RWB-E8-014:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1`, task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- A **pack** is a candidate version of this service's own access model: an ordered set of `PERMISSION`, `SCOPE` and `MASKING` rows that a centre of excellence analyst prepares for a role set, with its `packVersion`, its `ownerRole` and the `capabilityArea` it covers. It is a document of rows, not a file and not a set of documents.
- Two deliverables: the write `POST /api/recovery/access/v1/admin/pack-checks`, which authorises, checks every row, decides the verdict and records it; and the read `GET /api/recovery/access/v1/admin/pack-checks`, which answers the checks of one owner role with their verdicts and defect lists.
- The checks are this service's, because the rows they read are its own: `role`, `permission` and `masking_rule` (DP-01). No row of another service is read, and the pack's own content is nothing but rows of these three tables.
- The verdict is one of `ACCEPTED` and `RETURNED`. A `RETURNED` pack is not applied, is not stored as a version, and is answered with its defect list; the owner role corrects it and submits a new `packVersion`. The load and the approval of the version that follows are the matrix and reference-data stories of this service, and are not part of this one.
- The result is recorded as one entry of the local decision-record chain of the DP-03 library, in the transaction that answers the verdict, with the pack version, the owner role, the capability area, the verdict, the rule version in force and the defect list (AC1, AC2).
- The screen is SCR-39 Rules and parameters through the gateway-bff composite route of DP-19, which shows the returned packs of the caller's owner role and their defects; this story renders no screen of its own.
- This story starts no workflow, owns no Schedule and publishes no message on `rwb.access.events.v1`: the check is request-driven, and the only message it produces is `rwb.decision-record.DecisionRecorded.v1` on the shared decision-record topic.
- The separation-of-duty check at sign-in (RWB-P4-AD005-APP), the load of a permission matrix version (RWB-P4-AD002-APP), the scope table (RWB-P4-AD003-APP), the masking profile load (RWB-P4-AD004-APP) and the delegation of authority table (RWB-P4-AD016-APP) are other stories of this service; this story reads their rows and writes none of them.

### 2. Business rationale

REQ-ACA-003 makes the role to permission matrix the only source of what a role may see and do, REQ-ACA-005 requires personal data to be masked by role on every screen, REQ-ACA-007 requires access requested outside the authority matrix to be refused **and the refusal recorded**, and REQ-ACA-009 requires a user to see only what the role and scope allow. All four are Must and all four are E1. The legacy story carried them as one administration journey (FEAT-ADM-09, RWB-E8-014): the pack, the check and the decision log were rows of one schema and the check was a step of a screen.

The target splits the act in two. The owner of an access change prepares a pack; the service that owns the matrix checks it and either accepts it or returns it with the defects named. Nothing is applied by the check, and nothing is applied without it. That is what makes REQ-ACA-007 provable: a refusal is a recorded verdict with a defect list, not a message on a screen, and the record names the rule version it was decided under.

The gate exists because the three ways an access pack goes wrong are all silent if nobody looks. A row that names a capability area the matrix does not hold quietly widens the authority of a role. A row that names a role twice quietly leaves two scopes in force for one role. A `PERMISSION` row that gives a role access to a personal area with no masking row quietly exports personal data to a screen that has no profile. Each is cheap to detect at submission and expensive to detect in production, and each is detectable only where the rows live — here.

Fixing the verdict and its defect list once, in a published contract and a faked consumer set, is what lets the screen story, the gateway route and the matrix work build in parallel, and lets a drift between the fake and the document fail a build rather than an integration window.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E8014-CON (same service, its own contract story) | The OpenAPI 3.1 document of the two operations, the `PackCheck`, `PackRow`, `DefectItem`, `PackCheckAnswer` and `PackCheckSummary` schemas, the three check codes, the verdict set, the error envelope, the consumed-operation list and the contract fakes. This story implements that document and adds no path |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the entry of a verdict, hash-linked, written in the transaction that answers it |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the personal capability areas of PC-MSK, the pack row limit and the page bounds, as rows and not as code |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) that serves SCR-39 and calls the two operations, one hop each |
| The `role`, `permission` and `masking_rule` rows of the service | Created and loaded by RWB-P4-AD002-APP, RWB-P4-AD003-APP and RWB-P4-AD004-APP; this story reads them and writes none of them |

Business preconditions carried from RWB-E8-014, from the feature specification and from the technical specification:

- The rights in force are those of TSD P4 v3 T6.1: RW-COE holds `CRUD` in Rules and parameters, RW-LITOFF holds `R`, RW-PHONECOL holds a dash, RW-AUDIT holds `R` and RW-SECADM holds `R`. The submit authorises Rules and parameters C; the read authorises Rules and parameters R (BR3).
- The FSD P4 v3 A2.25.3.3 role table names the litigation officer as a user of the feature and the check itself as unattended; in the target the pack is submitted by the role that prepares it and read by the role that owns it, and the difference is carried as a conflict row of the key (GAP-2290; ASM-3792).
- The three letters of the permission model are those of TSD P4 v3 T3.1 `permission.letters` (DF-REF-043, `varchar(5)`): C, R, U, D and A. A row that names a letter outside that set is a defect of PC-ENT.
- A role's default scope is TSD P4 v3 T3.1 `role.default_scope` (DF-REF-038, list LOV-SCOPE: OWN, TEAM, REGION, ALL) and its class is DF-REF-037. The role code and the scope are read; neither the role nor the scope is changed here.
- The masking profile of a role and field is a `masking_rule` row, DF-REF-198 to DF-REF-204, with `unmasked` and `masking_version`. A `PERMISSION` row for a personal capability area of a role that holds no masking row in the pack is a defect of PC-MSK.
- The personal capability areas, the pack row limit and the page bounds are parameter rows of `rwb-case` read through DP-06 with the version in force; no value is a constant in code (BR-P4-025, BR10). Their names and their values are Not specified in the source documents (GAP-2288; ASM-3791).
- The rule version a verdict is recorded under is the version label the parameters contract answers plus the `matrix_version` of the `permission` rows in force (DF-REF-044), read at the moment of the check (BR8).

### 4. Flow

1. The owner role opens SCR-39 Rules and parameters through the gateway-bff composite route (DP-19), which shows the packs of that owner role in state `RETURNED` with their defect lists and calls this service for the read.
2. The centre of excellence analyst prepares a pack and submits it for check: `POST /api/recovery/access/v1/admin/pack-checks` with `packVersion`, `ownerRole`, `capabilityArea`, `rows[]` of `PERMISSION`, `SCOPE` and `MASKING` rows, and an `Idempotency-Key` header.
3. `PackCheckController` validates the request: every field is required; `packVersion` matches the label shape in force; `ownerRole` is an existing `role.role_code`; `rows` is not empty and not above the pack row limit. An empty field or a value outside its range is refused with 422 and MSG-GEN-001 or MSG-GEN-002 naming the field, and no row is checked and nothing is recorded (BR11).
4. The controller looks the `Idempotency-Key` up in the idempotency table of the platform library in `rwb_access`. A key already answered replays that first answer and checks nothing and records nothing (BR12, AC6).
5. The controller calls `POST /api/recovery/access/v1/authorise` on its own service, one hop with a 2 s timeout and a cached answer, for Rules and parameters C. A caller without the C letter is refused with 403 and MSG-P4-002, and no row is read and nothing is recorded (BR3, AC3).
6. `RuleVersionReader` reads the parameters contract for the personal capability areas, the pack row limit and the page bounds, and takes the `matrix_version` of the `permission` rows in force; the pair is the rule version the verdict is recorded under (BR8).
7. `PackChecker` runs the three checks over every row, in the fixed order PC-ENT, PC-SCP, PC-MSK, and does not stop at the first defect:
   - PC-ENT: the row names a `role_code` of `role` and a `capability_area` that the `permission` rows in force hold; a letter outside C, R, U, D and A, or an area the matrix does not hold, is a defect (BR4, REQ-ACA-003, REQ-ACA-007).
   - PC-SCP: the pack holds at most one `SCOPE` row per role, and every scope row names a role of `role`; a second row for one role, or a role that does not exist, is a defect (BR5, REQ-ACA-009).
   - PC-MSK: every `PERMISSION` row for a capability area named in the personal-area parameter row has at least one `MASKING` row for the same role in the pack; a personal area with no masking row for that role is a defect (BR6, REQ-ACA-005).
8. Each failing row appends one `DefectItem` with its `checkCode`, its `rowRef` (row type, row number and role code), its `field` and its `ruleRef` (the row in force or the parameter row the defect breaks), in the order the checks run and then in the order of the rows (BR7, AC5).
9. `PackCheckService` decides the verdict: no defect is `ACCEPTED`; one defect or more is `RETURNED`. A returned pack is not applied, no version is written to `permission`, `role` or `masking_rule`, and the pack itself is not stored as a row (BR9, AC1, AC4).
10. In one local transaction the service appends one entry to the decision-record chain of DP-03 with the record code of a pack check, the pack version, the owner role, the capability area, the verdict, the rule version, the defect count and the defect list; writes the idempotency row; and stages the outbox row of the entry (BR8, BR10, BR12).
11. The answer is 201 with `packCheckId`, `packVersion`, `ownerRole`, `capabilityArea`, `state`, `ruleVersion`, `defectCount`, `defects[]`, `decidedAt` and the `Location` of the read (BR1).
12. Where the entry, the idempotency row or the outbox row cannot be written, the verdict is withheld with 503 and MSG-P7-003: nothing is answered, nothing is applied and the pack stays undecided, so a check that cannot be recorded is not a check (BR10, AC2).
13. Where the same `packVersion` of the same owner role has already been decided, the call answers 409 with MSG-GEN-004 and no second entry; the owner corrects the pack and submits a new `packVersion`, which is a new check and leaves the earlier verdict in the chain (BR13, AC7).
14. `GET /api/recovery/access/v1/admin/pack-checks?ownerRole=&state=&page=&size=` answers the checks of one owner role with their `packVersion`, `capabilityArea`, `state`, `ruleVersion`, `decidedAt`, `defectCount` and `defects[]`, newest first and then by entry id, with the page bounds read through DP-06; an owner role with no check answers 200 with an empty `items` and total 0, never a 404 (BR14).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A required field is empty, or `rows` is empty | 422 naming the field; no row checked, no entry | MSG-GEN-001 | AC1 |
| X2 | `packVersion` does not match the label shape in force | 422 naming `packVersion`; no row checked, no entry | MSG-GEN-001 | AC1 |
| X3 | `rows` exceeds the pack row limit of the parameter row in force | 422 naming `rows` with its bounds; no row checked, no entry | MSG-GEN-002 | AC1 |
| X4 | The caller holds no Rules and parameters C | 403; no row read, no verdict, no entry | MSG-P4-002 | AC3 |
| X5 | The caller's session has ended | 401; no row read, no verdict, no entry | MSG-P4-001 | AC3 |
| X6 | The same `packVersion` of the same owner role is already decided | 409 and no second entry; the earlier verdict stands | MSG-GEN-004 | AC7 |
| X7 | The parameters contract does not answer inside 2 s | 503 and no verdict; a check without the rule version in force is not decided | MSG-P7-003 | AC4 |
| X8 | The decision-record entry, the idempotency row or the outbox row cannot be written | 503 and no verdict; nothing is applied and the pack stays undecided | MSG-P7-003 | AC2 |
| X9 | The same request arrives twice with the same `Idempotency-Key` | The first answer is replayed; one entry, no second check | None | AC6 |
| X10 | A break-glass grant is active for the caller | The check proceeds and the answer carries the warning with the end time of the grant; the entry carries the grant id | MSG-P4-004 | AC3 |
| X11 | A row names a role code that no `role` row holds | One `DefectItem` with check code PC-ENT, the row and the field; the verdict is `RETURNED` | None | AC5 |

No exception path of this story writes a `role`, a `permission`, a `masking_rule` or a `delegation_limit` row, and none changes a case, a task or a pack's content: the only row this story writes of its own is the entry of its own chain plus the platform library rows of the request.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P4-E8014-CON and its fakes; reads only its own three tables and one parameter read, so no other service blocks it |
| Negotiable | The personal-area parameter, the pack row limit, the page bounds and the label shape are rows; the three check codes and the verdict set are fixed by the target architecture and reviewed with the security administrator |
| Valuable | A pack that would break the matrix, the scope or the masking is returned with its defects named, and the refusal is recorded with the rule version — REQ-ACA-003, 005, 007 and 009 |
| Estimable | One controller, one checker, one rule-version reader, one query service, one record appender, one idempotency store, four fakes and nine test cases |
| Small | Fits one sprint with its tests; no new table, no workflow, no Schedule, no screen and no event of its own |
| Testable | Each criterion has a test case in section 16; a defect list is provable against a seeded pack, and the record-before-answer rule is provable with a forced failure |

### 7. Acceptance criteria

```gherkin
Feature: Return a defective pack

  Background:
    Given the environment is SIT
    Given the access model of rwb-access is in force at matrix version "MAT-2027.02"
    Given test user "U-5101" holds RW-COE with "CRUD" in "RULES_AND_PARAMETERS" and submits packs
    Given test user "U-5102" holds RW-LITOFF with "R" in "RULES_AND_PARAMETERS" and is the owner role of the packs of this feature
    Given test user "U-5104" holds RW-PHONECOL with "-" in "RULES_AND_PARAMETERS"
    Given test user "U-5105" holds RW-AUDIT with "R" in "RULES_AND_PARAMETERS"

  Scenario: AC1 Return a defective pack (legacy RWB-E8-014 AC1)
    Given the rwb-case contract mock returns the pack-check parameter rows in force
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then sends a pack that fails the check back to its owner with the defects named
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E8-014 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 A caller without the right is refused and nothing is checked (new, D-RCV-60)
    Given a pack "AP-2027.03" for ownerRole "RW-LITOFF" with four PERMISSION rows for "LITIGATION" and one MASKING row for "RW-LITOFF"
    When "U-5104" calls POST /api/recovery/access/v1/admin/pack-checks with Idempotency-Key "k-014-3"
    Then the response is 403 with message MSG-P4-002 and no verdict is answered
    Then no row of role, permission or masking_rule is read for the check
    Then no pack-check entry is appended and GET /api/recovery/access/v1/admin/pack-checks?ownerRole=RW-LITOFF answers an empty list
    When a caller with no session sends the same request
    Then the response is 401 with message MSG-P4-001 and nothing is recorded

  Scenario: AC4 A pack with no defect is accepted and returned to nobody (new, D-RCV-60)
    Given a pack "AP-2027.04" for ownerRole "RW-LITOFF" of one PERMISSION row for "LITIGATION" and one MASKING row for the same role, both inside the matrix in force
    When "U-5101" calls POST /api/recovery/access/v1/admin/pack-checks with Idempotency-Key "k-014-4"
    Then the response is 201 with state "ACCEPTED" and defectCount 0 and an empty defects list
    Then the answer carries ruleVersion "MAT-2027.02" with the check rule-set label in force
    Then no row of permission, role or masking_rule is written by the check

  Scenario: AC5 Every defect is named once with its row, its field and its rule (new, D-RCV-60)
    Given the parameters in force name "CASE_RECORD" and "LITIGATION" as personal capability areas
    Given a pack "AP-2027.05" for ownerRole "RW-LITOFF" holding a PERMISSION row for capability area "CLOSING" with letters "U", a PERMISSION row for "LITIGATION" with letters "X", two SCOPE rows for role "RW-LITOFF", and a PERMISSION row for "CASE_RECORD" with no MASKING row for that role
    When "U-5101" calls POST /api/recovery/access/v1/admin/pack-checks with Idempotency-Key "k-014-5"
    Then the response is 201 with state "RETURNED"
    Then the defects list carries one item for the unknown capability area with checkCode "PC-ENT" and its rowRef and field
    Then it carries one item for the letter outside C, R, U, D and A with checkCode "PC-ENT"
    Then it carries one item for the second SCOPE row of role "RW-LITOFF" with checkCode "PC-SCP"
    Then it carries one item for the personal area with no masking row with checkCode "PC-MSK"
    Then the defectCount is 4 and the items are ordered by check and then by row
    Then no item carries a name, an e-mail address or a user reference

  Scenario: AC6 One verdict, one entry, and a repeated key replays it (new, D-RCV-60)
    Given a pack "AP-2027.06" for ownerRole "RW-LITOFF" with one defect
    When "U-5101" calls POST /api/recovery/access/v1/admin/pack-checks with Idempotency-Key "k-014-6"
    Then the response is 201 with state "RETURNED" and the defect list
    Then exactly one entry of the local decision-record chain is appended with the pack version, the verdict and the rule version in force
    When the same request is sent again with Idempotency-Key "k-014-6"
    Then the first answer is replayed with the same packCheckId and no second entry is appended

  Scenario: AC7 A decided pack version is never decided twice and an earlier verdict is kept (new, D-RCV-60)
    Given pack "AP-2027.06" of ownerRole "RW-LITOFF" was decided "RETURNED" under Idempotency-Key "k-014-6"
    When "U-5101" submits the same pack "AP-2027.06" again with Idempotency-Key "k-014-7"
    Then the response is 409 with message MSG-GEN-004 and no second entry is appended
    When the owner corrects the pack and "U-5101" submits it as "AP-2027.07" with Idempotency-Key "k-014-8"
    Then a second entry is appended with the verdict of the corrected pack and the rule version in force
    Then the verdict of "AP-2027.06" is unchanged and is still answered by the read
    When "U-5102" calls GET /api/recovery/access/v1/admin/pack-checks?ownerRole=RW-LITOFF&state=RETURNED
    Then the answer carries the returned pack "AP-2027.06" with its defects and not the accepted one
```

AC1 and AC2 are the two criteria of RWB-E8-014, copied with their text unchanged and their values kept: "the data and the rule version this feature needs", "its trigger arrives" and "the defects named" read in this story as the pack check and its defect list. AC1 carries one added line at the top of its scenario, the parameters mock, so the rule version is provable while `rwb-case` is still a fake. AC3 to AC7 are new under D-RCV-60 and test only what this story adds: the right, an accepted pack, the complete defect list, the record and the replay, and the version rule.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One verdict per pack version: `ACCEPTED` when no row fails a check, `RETURNED` when one row or more does, and the answer names the pack version, the owner role, the capability area and the rule version | RWB-E8-014 AC1; FSD P4 v3 A2.25; ASM-3789 |
| BR2 | The pack is checked against this service's own rows only: `role`, `permission` and `masking_rule`; no row of another service is read and the pack's content is stored nowhere | DP-01; Ownership Map v1; REQ-ACA-003 |
| BR3 | The submit needs Rules and parameters C and the read needs Rules and parameters R; a caller without the letter is refused with 403 and MSG-P4-002 and nothing is read and nothing is recorded | TSD P4 v3 T6.1; legacy RWB-E8-014 permission checks |
| BR4 | PC-ENT: every `PERMISSION` row names a role of `role`, a capability area the `permission` rows in force hold, and letters drawn from C, R, U, D and A; anything else is a defect and is refused rather than applied | REQ-ACA-003, REQ-ACA-007; TSD P4 v3 T3.1 DF-REF-042 and DF-REF-043 |
| BR5 | PC-SCP: the pack holds at most one `SCOPE` row per role and every scope row names a role of `role`; a duplicate row for one role or an unknown role is a defect | REQ-ACA-009; TSD P4 v3 T3.1 DF-REF-038; ASM-3790 |
| BR6 | PC-MSK: a `PERMISSION` row for a capability area named in the personal-area parameter row needs at least one `MASKING` row for the same role in the pack; a personal area with no masking row is a defect | REQ-ACA-005; TSD P4 v3 T3.1 DF-REF-198 to DF-REF-204; ASM-3791 |
| BR7 | The defect list is complete and ordered: one item per failing row and check with its check code, its row reference, its field and the rule it breaks; the checker never stops at the first defect | FSD P4 v3 A2.25.2; RWB-E8-014 AC1 |
| BR8 | The verdict is recorded in one entry of the local chain with the pack version, the owner role, the capability area, the verdict, the rule version in force, the defect count and the defect list | RWB-E8-014 AC1; R-UNI-39; DP-03 |
| BR9 | A check applies nothing: no `permission`, `role` or `masking_rule` row is written, and a returned pack is not a version of the matrix | FSD P4 v3 A2.25; ASM-3789 |
| BR10 | An answer that cannot be recorded is withheld with 503 and MSG-P7-003, so no verdict exists without its record | RWB-E8-014 AC2; DP-03 |
| BR11 | The pack version label, the personal areas, the pack row limit and the page bounds are parameter rows read through DP-06 with the version in force; no value is a constant in code | BR-P4-025; DP-06; ASM-3791 |
| BR12 | One `Idempotency-Key` answers one check: a replay answers the first answer, appends no second entry and checks nothing again | Architecture v5 slide 42; DP-09 |
| BR13 | A decided `packVersion` of an owner role is never decided twice: a repeat answers 409 with MSG-GEN-004, and a corrected pack is submitted under a new version whose verdict sits beside the earlier one | RWB-E8-014 AC1; ASM-3789 |
| BR14 | The read answers the checks of one owner role, newest first and then by entry id, and an owner role with no check answers an empty list with total 0; it never answers a 404 | DP-03; ASM-3794 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1, BR4, BR5 and BR6 are one ordered pass in `PackChecker`: entitlement, scope, masking, over every row, collecting defects instead of returning at the first one.
- BR2 is the absence of a repository for anything else: the module has no table, view or join for a case, a document, a rule package or a delegation limit, and the pack's rows are the three tables it reads.
- BR3 is the authorise call of the service's own contract, cached for the session; the read is filtered by the owner role the caller may see.
- BR7 and BR8 are one payload: the defect list is part of the entry, so the read is a projection of the chain and not a second store.
- BR9 is a rule about what is missing: the service has no write method on `permission`, `role` or `masking_rule`, so a check cannot apply even by mistake.
- BR10 is the transaction order: entry, idempotency row and outbox row commit together, and a failure rolls all three back.
- BR11 is the parameter reader at request time; a changed limit or a changed personal area is data and needs no build.
- BR12 and BR13 are the `idempotency_key` row of the platform library and the decided-version lookup in front of the checker.
- BR14 is the read: it filters by the owner role, orders on `decidedAt` then entry id, and has no 404 branch.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| No check | A pack is submitted | C held, the pack is valid, no row fails a check | `ACCEPTED`, one entry, answer 201 |
| No check | A pack is submitted | C held, the pack is valid, one row or more fails | `RETURNED`, one entry with the defect list, answer 201 |
| No check | A pack is submitted | No C letter | Refused 403 with MSG-P4-002; nothing read, no entry |
| No check | A pack is submitted | The session has ended | Refused 401 with MSG-P4-001; no entry |
| No check | A pack is submitted | A field is empty, outside its range, or `rows` is above the limit | Refused 422 with MSG-GEN-001 or MSG-GEN-002; no check, no entry |
| No check | A pack is submitted | The parameters contract does not answer | Refused 503 with MSG-P7-003; no verdict |
| No check | A pack is submitted | The entry cannot be written | Refused 503 with MSG-P7-003; nothing answered, nothing applied |
| `RETURNED` | The owner submits a corrected pack | A new `packVersion` for the same owner role | A new check, `ACCEPTED` or `RETURNED`; the earlier entry stays |
| `RETURNED` or `ACCEPTED` | The same `packVersion` is submitted again | None | Refused 409 with MSG-GEN-004; one verdict per version |
| `RETURNED` or `ACCEPTED` | The same request is sent again with its key | The key is stored | The first answer is replayed; no second entry |

| Chain | Event | Outcome |
|---|---|---|
| Append-only local chain of DP-03 | A check is decided | One entry appended with the pack version, the verdict, the rule version and the defect list, with its `prev_hash` and `entry_hash`; no entry is updated or deleted |
| `permission`, `role`, `masking_rule` | A check is decided | No change: the check applies nothing (BR9) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Center of excellence analyst (RW-COE, `CRUD` in Rules and parameters) | Submit a pack for check with Rules and parameters C; receives the verdict and the defect list (TSD P4 v3 T6.1) |
| Litigation officer (RW-LITOFF, `R` in Rules and parameters) | The owner role a pack is returned to: reads the returned packs and their defects with Rules and parameters R |
| Internal audit (RW-AUDIT, `R`) | Reads the verdicts of the owner roles in scope; checks nothing and applies nothing |
| Security administrator (RW-SECADM, `R`) | Reads the verdicts and the defect lists; the load and approval of a matrix version are other stories of this service |
| A role with a dash in Rules and parameters (RW-PHONECOL) | Refused with 403 and MSG-P4-002; nothing is read and nothing is recorded |
| The gateway-bff route | Calls the two operations on behalf of the signed-in user, one hop each, and passes the `Idempotency-Key` unchanged |
| `rwb-access` itself | Reads `role`, `permission` and `masking_rule` in its own schema and writes only its own chain and the platform library rows of the request |
| `rwb-case` (P3) | Owns the parameters and reference data under the default ruling; answers the one parameters read of DP-06 |
| `rwb-decision` (P7) | Owns the central ledger; this story calls it not at all |

The refusal shapes are 403 with an RFC 9457 problem response and `messageId` MSG-P4-002 for an absent right, 401 with MSG-P4-001 for no session, 409 with MSG-GEN-004 for a decided pack version, 422 with MSG-GEN-001 or MSG-GEN-002 for a pack that cannot be read, and 503 with MSG-P7-003 for a parameters read or a record that cannot be completed. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-E8014-CON.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | `id`, `role_code`, `role_name`, `role_class`, `default_scope`, `entra_group` | Read: the role code of every row, its class and its default scope |
| DF-REF-040 to DF-REF-044 | `permission` | `id`, `role_id`, `capability_area`, `letters`, `matrix_version` | Read: the areas and letters in force and the `matrix_version` of the verdict |
| DF-REF-198 to DF-REF-204 | `masking_rule` | `id`, `role_code`, `field_id`, `unmasked`, `masking_version`, `valid_from`, `valid_to` | Read: the masking profile in force per role and field |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the verdict entry: `decision_code` DF-DEC-003, `case_id` DF-DEC-002 empty, `inputs_ref` DF-DEC-008 with the pack version, the owner role, the capability area, the verdict, the rule version and the defect list, `decided_at` DF-DEC-016, `prev_hash` DF-DEC-017 and `entry_hash` DF-DEC-018 | Write; and read for the list |
| (idempotency) | `idempotency_key` (platform library table in `rwb_access`) | the request and the stored answer of a check | Write and read (DP-09; ASM-0074) |
| (outbox) | `outbox_event` | the record row of the verdict entry | Write |
| (inbox) | `processed_event` | none: this story consumes no event | None |
| DF-REF-016 to DF-REF-026, DF-REF-055 to DF-REF-062 | `delegation_limit` | none | Not read: the delegation table is RWB-P4-AD016-APP's |
| DF-REF-205 to DF-REF-211 | `role_conflict` | none | Not read: the sign-in conflict check is RWB-P4-AD005-APP's |

No row of another service is read: a pack names no case, no document and no rule package, and the parameters the check needs arrive in the one contract answer of section 12.2 (DP-01). The name and the shape of the pack version label, the personal capability areas and the pack row limit are Not specified in the source documents (GAP-2288; ASM-3791): they are parameter rows, their names are fixed by RWB-P4-E8014-CON, and the check fails closed without them (BR11).

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| POST | `/api/recovery/access/v1/admin/pack-checks` | P4 `rwb-access` | Body: `packVersion`, `ownerRole`, `capabilityArea`, `rows` of `rowType`, `rowNo`, `roleCode`, `capabilityArea`, `letters`, `scope`, `fieldId`, `unmasked` | `packCheckId`, `packVersion`, `ownerRole`, `capabilityArea`, `state` `ACCEPTED` or `RETURNED`, `ruleVersion`, `defectCount`, `defects` of `checkCode`, `rowRef`, `field`, `ruleRef`, `decidedAt`, with `Location` of the read | 401 (MSG-P4-001); 403 (MSG-P4-002); 409 (MSG-GEN-004); 422 (MSG-GEN-001, MSG-GEN-002); 503 (MSG-P7-003) | Rules and parameters C | `Idempotency-Key` required; a replay answers the first answer and appends no second entry |
| GET | `/api/recovery/access/v1/admin/pack-checks` | P4 `rwb-access` | Query: `ownerRole`, `state`, `page`, `size` | `PackCheckSummary`: `items` of `packCheckId`, `packVersion`, `capabilityArea`, `state`, `ruleVersion`, `decidedAt`, `defectCount`, `defects`, and `page`, `size`, `total` | 401 (MSG-P4-001); 403 (MSG-P4-002); 422 (MSG-GEN-001); 503 (MSG-P7-003) | Rules and parameters R, filtered by the owner role the caller may see | Not applicable, read only |

Both operations sit on the base `/api/recovery/access/v1` of DP-13. `page` defaults to the value of its parameter row and `size` is capped by it, both read through DP-06 and never from code (BR11).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (own service) | The Rules and parameters C check behind the submit and the R check behind the read, cached for the session; MSG-P4-002 on a refusal |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case` | The personal capability areas of PC-MSK, the pack row limit, the page bounds and the check rule-set label, with the version in force (DP-06) |

One hop per call, 2 s timeout and a breaker per downstream (DP-11). No operation of `rwb-comms`, `rwb-decision`, `rwb-document`, `rwb-litigation` or `rwb-integration` is called by this story.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | the hash-chained entry of a verdict: the pack version, the owner role, the capability area, the verdict, the rule version and the defect list |

CloudEvents 1.0 envelope, from the outbox of the transaction that answers the verdict. The payload carries codes, a version label and row references and no name, no e-mail address and no personal field. This story publishes no message on `rwb.access.events.v1`: the ownership row of `rwb-access` carries no event of its own for this capability, and the two events of the service named in Architecture v5 slide 14 belong to RWB-P4-E1037-APP and RWB-P4-E8008-APP.

#### 12.4 Events consumed

None. The check is request-driven and reads its own rows and one parameters answer; no inbox row is written and no consumer group is declared.

#### 12.5 Workflows and activities

None. The check is synchronous and short; it starts no workflow, signals none and registers no activity on the `rwb-access` queue. The raising of a task where a person is needed, which FSD P4 v3 A2.25.2 names, is the returned-packs list of the screen and not a workflow task (GAP-2289; ASM-3793).

#### 12.6 Schedules

None. The check runs when a pack is submitted; the six-monthly access review list (JOB-18) is the only Schedule of `rwb-access` and belongs to RWB-P4-AD008-APP.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | Read only: the role code, the role class and the default scope of every row the pack names |
| `permission` | P4 (`rwb_access`) | Read only: the capability areas and letters in force, and the `matrix_version` the verdict is recorded under |
| `masking_rule` | P4 (`rwb_access`) | Read only: the masking profile in force per role and field |
| the local decision-record table of the DP-03 library | P4, in `rwb_access` | Write: the verdict entry. Read: the list of checks |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | The outbox row of the entry and the idempotency row of the request; no inbox row, because no event is consumed (DP-09; ASM-0074) |
| `delegation_limit`, `role_conflict` | P4 (`rwb_access`) | Not read: the delegation table is RWB-P4-AD016-APP's and the conflict table is RWB-P4-AD005-APP's |

No table of another service is named as this service's and none is created here (DP-01). `lov_value`, `reference_version` and `reference_row` are reference data of P3 under the ownership ruling; this story's pattern list carries no DP-07 and its contract-dependency list no `RWB-P3-E1043-CON`, so the check reads no list of values and the letter set of BR4 is the model constant of the `permission.letters` column, not a reference row (GAP-2288; ASM-3791).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| authorise fake | RWB-P4-E8014-CON, RWB-P4-E1037-CON | A granted answer for RW-COE with C and for RW-AUDIT and RW-LITOFF with R in Rules and parameters, and a refused answer with MSG-P4-002 for RW-PHONECOL with a dash |
| parameters fake | RWB-P3-E1042-CON | The personal capability areas, the pack row limit, the page bounds and the check rule-set label, with the version in force, and a 503 for X7 |
| decision-record fake | RWB-PLT-E1027-CON | The append of a verdict, the hash-link check, a seeded chain of packs "AP-2027.03" and "AP-2027.06", the replay of a stored key and the forced failure AC2 needs |
| gateway-bff fake | RWB-PLT-N001-CON | The composite route of SCR-39 with the returned packs of the owner role, the pack form and the defect panel |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2 (the check and the list); consumed 2 | Base `/api/recovery/access/v1`; the own authorise operation and the `rwb-case` parameters read, one hop and 2 s each |
| Kafka | Published 1 event type; consumed 0 | `rwb.decision-record.v1` through the DP-03 library |
| Temporal | 0 workflows, 0 activities | The `rwb-access` queue carries the access review Schedule of RWB-P4-AD008-APP only |
| File | None | A pack is a JSON body of rows; no file is uploaded and no file is produced |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/packcheck`, Java package `th.co.scb.ace.workbench.recovery.access.packcheck`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the in-module check and the in-module decision-log write of the monolith (DP-03 and DP-13: the record on the shared topic and the operations on this service's own base), and the ace-web screen that checked a pack in process (DP-19: a gateway-bff composite route on SCR-39). DP-01, DP-02, DP-09 and DP-11 govern the service baseline and the one-hop budget of section 12.2; they add no dependency of their own and are not claimed as patterns of this story.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| PackCheckController | Controller | The two operations: validation, the `Idempotency-Key` lookup, the RFC 9457 problem responses, `Location` on a decided check |
| PackCheckService | Service | The verdict of BR1 and BR9, the answer and the record call of BR8; applies nothing |
| PackChecker | Service | The three checks of BR4, BR5 and BR6 over every row, collecting defects in the order of BR7 |
| RuleVersionReader | Service | The parameters read of DP-06 and the `matrix_version` of the rows in force; the rule version of BR8 |
| PackCheckQueryService | Service | The read of BR14: the checks of one owner role, the order, the paging and the empty answer |
| PackCheckRepository | Repository | Read-only queries over `role`, `permission`, `masking_rule` and the local chain; no write method on any of the three tables |
| PermissionReader | Service | The caller's letters from its own `permission` and `role` rows, and the authorise call |
| DecisionRecordAppender | Service | The verdict entry with its outbox row, in the transaction that answers the check (DP-03, DP-09) |
| IdempotencyStore | Service | The `Idempotency-Key` lookup and store of the platform library, written with the answer |

**Database and migrations**

- This story creates no table of its own. `role`, `permission` and `masking_rule` are created by RWB-P4-AD002-APP, RWB-P4-AD003-APP and RWB-P4-AD004-APP, the local decision-record table by RWB-P4-E1039-APP and the platform library tables by the service's own DB story, all in the per-service Flyway sequence of DP-15; this story reads them.
- No write statement touches `role`, `permission` or `masking_rule`, so a check can never apply itself even if the verdict is wrong (BR9).
- The entry, the idempotency row and the outbox row commit in one transaction; a failure rolls all three back and the verdict is withheld with MSG-P7-003 (BR10).

**Configuration and reference data**

- The personal capability areas, the pack row limit, the page default and maximum and the pack version label shape are parameter rows of `rwb-case` read through DP-06 with the version in force; no value is a constant in code (BR11). Their names are fixed by RWB-P4-E8014-CON.
- The letter set C, R, U, D and A is the domain of the `permission.letters` column and is a model constant of the contract, not a reference list of this service (section 12.7).
- The scope codes the pack may name are read from the matrix and not fixed here; the check of PC-SCP is the one-row-per-role rule and the role code, and no scope code is a constant of this story (BR5).

**Build steps**

1. `PackCheckController` and its validation; tests for X1, X2 and X3 with no row read.
2. `PermissionReader` and the authorise call; test the AC3 refusal of a caller with a dash, with no row read and an empty list afterwards.
3. `RuleVersionReader` over the parameters fake; test that a changed limit or area is data and needs no build, and the 503 of X7.
4. `PackChecker` and PC-ENT; tests for an unknown capability area, an unknown role code and a letter outside C, R, U, D and A.
5. `PackChecker` and PC-SCP and PC-MSK; tests for a duplicate scope row and for a personal area with no masking row, including the ordering of the defect list of AC5.
6. `DecisionRecordAppender` and `IdempotencyStore` in one transaction; tests for the replay of AC6 and the forced failure of AC2 with no verdict.
7. The decided-version lookup of BR13; tests for the 409 of AC7 and for the corrected version that leaves the earlier entry in place.
8. `PackCheckQueryService` over a seeded chain of packs "AP-2027.03" and "AP-2027.06"; tests for the order, the paging, the state filter and the empty answer of BR14.
9. The contract-fake run of both operations through the gateway-bff fake, so SCR-39 can be demonstrated while the route and the matrix stories are being built.

**Feature switch.** The two operations are switched by the service baseline of RWB-P4-E1037-CON, not by a flag of their own. A pack check that is switched off would let an unchecked pack be loaded by the matrix story, which is the state the gate exists to prevent, so this story adds no flag and removes nothing.

**Done when.** The tests in section 16 pass; a pack with a row outside the matrix, a duplicate scope row and a personal area with no masking row is answered `RETURNED` with four ordered defects and one entry that carries the rule version; a clean pack is answered `ACCEPTED` with no defect and writes no access row; a caller with a dash is refused with MSG-P4-002 and nothing is read; a forced record failure withholds the verdict with MSG-P7-003; the same key replays one answer with one entry; and a decided pack version is refused with MSG-GEN-004 while a corrected version is decided beside it.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The caller has no session | You have no Recovery Workbench role. Ask your team manager to request one. | This story, on both operations |
| MSG-P4-002 | The caller holds no Rules and parameters C on the submit, or no R on the read | You cannot {action} here. Your role does not include it. | This story, on both operations |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. | This story, as a warning on the answer |
| MSG-GEN-001 | A required field is empty, or `packVersion` is not of the shape in force | Enter {field}. | This story, on the submit and on the read query |
| MSG-GEN-002 | `rows` is above the pack row limit, or `size` is above the page maximum | Not specified in the source documents (GAP-2291; ASM-3795) | This story, on the submit and on the read query |
| MSG-GEN-004 | The pack version of the owner role is already decided | Not specified in the source documents (GAP-2291; ASM-3795) | This story, on the submit |
| MSG-P7-003 | The parameters read fails, or the verdict entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the submit |

The message IDs are contract elements; the text is the agreed text taken from the legacy story where the message already existed. MSG-GEN-002 and MSG-GEN-004 carry an identifier and no text here, because no source read for this work package gives their wording; the message catalogue supplies it before the operations are frozen. The defect items of section 12.1 are not catalogue messages: each names a check code, a row, a field and the rule it breaks, and its wording is not specified either (GAP-2288; ASM-3789).

### 15. Screens and states

| Screen | State | What the screen consumes |
|---|---|---|
| SCR-39 Rules and parameters | Returned packs, list | The read of `state=RETURNED` for the caller's owner role, with the pack version and the defect count |
| SCR-39 Rules and parameters | Returned pack, defects | The `defects` of one check: check code, row reference, field and rule |
| SCR-39 Rules and parameters | Accepted pack, list | The read of `state=ACCEPTED`, with the verdict and the rule version |
| SCR-39 Rules and parameters | Pack, form | `PackCheck` with `packVersion`, `ownerRole`, `capabilityArea` and the three row types |
| SCR-39 Rules and parameters | Pack, refused | The 403 of the envelope with MSG-P4-002, the pack unchanged |
| SCR-39 Rules and parameters | Pack, malformed | The 422 of the envelope with MSG-GEN-001 or MSG-GEN-002 naming the field |
| SCR-39 Rules and parameters | Pack, already decided | The 409 of the envelope with MSG-GEN-004 and a reload action |
| SCR-39 Rules and parameters | Not recorded | The 503 of the envelope with MSG-P7-003 and a retry that reuses the same `Idempotency-Key` |
| SCR-39 Rules and parameters | List, empty | An empty `items` with total 0 and no error |

The screens are served by the gateway-bff composite route (DP-19), which shows the returned packs of the caller's owner role and calls the two operations of this story, one hop each. The route specification, the panel split and the screen field list belong to RWB-PLT-N001-CON; the load, the approval and the rollback of a matrix version are the administration stories of this service and are not part of this document.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-014-01 | AC1, BR1, BR4, BR7, BR8 | Contract | Pack "AP-2027.03" of ownerRole "RW-LITOFF" with 24 rows; a PERMISSION row for capability area "CLOSING", a row with letters "X", a second SCOPE row for "RW-LITOFF" and a "CASE_RECORD" row with no masking row; the answer `RETURNED` with four defects and one entry with rule version "MAT-2027.02" |
| TC-E8-014-02 | AC2, BR10 | Component | The decision-record append forced to fail: 503 with MSG-P7-003, no verdict, no entry, the pack undecided and no access row written |
| TC-E8-014-03 | AC3, BR3 | Component | "U-5104" holding a dash in Rules and parameters is refused 403 with MSG-P4-002 and no row is read; a caller with no session is refused 401 with MSG-P4-001; "U-5105" holding R may read and may not submit |
| TC-E8-014-04 | AC2, BR10 | NFR | The record failure repeated under the wave 4 load: every call answers 503 with MSG-P7-003 and the chain, the access rows and the idempotency table are unchanged |
| TC-E8-014-05 | AC4, BR1, BR9 | Contract | Pack "AP-2027.04" inside the matrix in force: state `ACCEPTED`, defectCount 0, empty defects, ruleVersion "MAT-2027.02", and no `permission`, `role` or `masking_rule` row written |
| TC-E8-014-06 | AC5, BR7 | Component | A pack with two PC-ENT defects, one PC-SCP and one PC-MSK: four items, ordered by check then row, each with its rowRef and field, and no name or user reference |
| TC-E8-014-07 | AC6, BR12 | Component | The same request under key "k-014-6" twice: the first answer replayed with its packCheckId, one entry, one check |
| TC-E8-014-08 | AC7, BR13 | Component | Pack "AP-2027.06" decided `RETURNED` and resubmitted: 409 with MSG-GEN-004 and no second entry; "AP-2027.07" decided beside it and the earlier verdict unchanged |
| TC-E8-014-09 | AC7, BR14 | Component | The read for "RW-LITOFF" with `state=RETURNED`: one item with its defects, paging from the parameter row, newest first; an owner role with no check answers an empty list with total 0 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to Contract, Access to Component and Principle 5 to NFR. TC-E8-014-01 to TC-E8-014-04 are the four cases of RWB-E8-014 and are kept: 01 and 02 cover the two legacy criteria, 03 the access refusal and 04 the forced record failure. TC-E8-014-05 to TC-E8-014-09 are new under D-RCV-60 and test only what this story adds. The integration copy of the set is not written here, so no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in code: the personal capability areas, the pack row limit, the page bounds and the version label shape stay parameter rows behind DP-06, and the role codes stay rows of `role` (BR11).
- No personal data: a pack row, a defect item, an entry and a log line carry role codes, capability areas, letters, scopes, field ids and references only — never a name, an e-mail address or a user reference (BR7, NFR-040).
- The service names only its own tables and only operations it owns; `lov_value`, `case`, `document`, `rule_package_version` and `delegation_limit` are named as other stories' and are never read here (BR2).
- One REST base and one topic per service; a change that names another service's base or topic fails the review (DP-13).
- A check applies nothing: there is no write method on `role`, `permission` or `masking_rule`, so a verdict can never become a change by accident (BR9).
- The verdict is written before it is answered, and an answer that cannot be recorded is withheld (BR10).
- Every example is synthetic; no pack, no matrix version and no production row is copied into a test, a fixture or a log.
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.
- A submit without its `Idempotency-Key` is refused, and a replay never decides a second time.

### 18. Traceability

| Requirement ID | Requirement (short) | Where this story meets it | Test cases |
|---|---|---|---|
| REQ-ACA-003 | The role to permission matrix is held as data and is the only source of what a role may see and do | PC-ENT checks every row against the `permission` rows in force and records the `matrix_version` of the verdict | TC-E8-014-01, TC-E8-014-05 |
| REQ-ACA-005 | Personal data is masked by role on every screen | PC-MSK returns a pack that gives a role access to a personal capability area with no masking row for that role | TC-E8-014-01, TC-E8-014-06 |
| REQ-ACA-007 | Access requested outside the authority matrix is refused and the refusal is recorded | The `RETURNED` verdict with its defect list and the entry that carries it, written before the answer | TC-E8-014-01, TC-E8-014-02 |
| REQ-ACA-009 | A user sees only the cases and queues their role and scope allow | PC-SCP returns a pack that names one role with two scopes or a role that does not exist | TC-E8-014-01, TC-E8-014-06 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator | The two operations as the SCR-39 route consumes them, with the defect panel and the refusal shapes | TC-E8-014-03, TC-E8-014-09 |
| REQ-DRI-010 | A parameter catalog and a configuration service hold every threshold, limit and name, versioned, changed without a code release | The one parameters read of DP-06 and the rule version every verdict is recorded under | TC-E8-014-04, TC-E8-014-05 |

The requirement IDs are those this key serves, and their text is taken from the Program BRD under the fill order of Template and Rules §R7.3; the Work Package carries no requirement list for this key.

| Legacy reference | Where it is kept |
|---|---|
| AC1 return a defective pack, the check and the record of the result with its rule version | Sections 4, 7 (AC1), 8, 12.1, 12.3 |
| AC2 not recorded: nothing changes and the user sees MSG-P7-003 | Sections 5 (X8), 7 (AC2), 11, 14 |
| The permission check: Rules and parameters C for RW-COE and A for RW-RISK | Sections 7 (AC3), 10, 12.1, 14 |
| The legacy data rows `assignment`, `decision_log_entry`, `rule_row` and `role` of the legacy table | Section 11, with `role` DF-REF-034 to DF-REF-039 kept and the others named as their owners' |
| The legacy screens SCR-39 Rules and parameters and SCR-41 Delegation of authority | Section 15, carried to SCR-39 with the returned-packs panel |
| Test cases TC-E8-014-01 to TC-E8-014-04 | Section 16 |
| Legacy key RWB-E8-014, story RWB-P4-E8014-APP, contract RWB-P4-E8014-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The implementation of the contract baseline itself (RWB-P4-E8014-CON): the document, the schemas, the check codes and the fakes.
- The load, the approval and the rollback of a permission matrix version (RWB-P4-AD002-APP, RWB-P4-AD010-APP, RWB-P4-AD013-APP): this story checks and returns a pack and applies nothing.
- The scope of a role as data (RWB-P4-AD003-APP), the masking profile load (RWB-P4-AD004-APP) and the separation-of-duty check at sign-in (RWB-P4-AD005-APP).
- The delegation of authority table, its load and its lookup (RWB-P4-AD016-APP and the delegation stories).
- The rule package store, the rule-version load and approval (RWB-P4-AD011-APP, RWB-P4-AD012-APP) and the change checklist of TSD P4 v3 T6.3.
- The screen SCR-39 Rules and parameters, its other panels and its composite route specification (RWB-PLT-N001-CON).
- The central decision ledger, its query API and the chain verification (P7 `rwb-decision`).
- The deployment, the Helm chart, the topic subscription, the dashboards and the runbook.
- The pack's own content and the litigation pack of FEAT-LIT-05, its documents and its release (P4 litigation and P5 `rwb-document`).
- The cross-service journey harness and its evidence, and the `-ITG` copies of the test cases.
