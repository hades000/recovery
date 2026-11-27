# RWB-P4-E8011-APP Roll back a configuration version

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8011-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-011 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP06, DP13, DP19 |
| Parallel lane | L-P4-BE |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement; no size value in the story |
| Depends on (build) | RWB-P4-E8011-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON |
| Contract version | v1 (path prefix `/api/recovery/access/v1`); the build label of the contract is Not specified in the source documents (DOR-RWB-P4-E8011-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-011 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-P4-E8011-APP-L252, X20 RWB-P4-E8011-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (12 resolved, 12 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Not specified in the source documents (DOR-RWB-P4-E8011-APP-1)**, I want **one version of one versioned configuration table of `rwb-access` undone in a single action — every row of the version in force withdrawn and every row of the version before it put back in force, with each row keeping the identifier it already had — and the withdrawal and the restoration both written to the decision record with the caller, the time and the reason**, so that **a bad permission matrix, masking profile, role-conflict pair or delegation limit is out of force on the day it is found without a code release, open work keeps the queue and the role it was already given, and no configuration change is ever undone unlogged**.

Inside `rwb-access` this is the configuration-rollback capability of the legacy story RWB-E8-011:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- **Two deliverables, and nothing else.** The write `POST /api/recovery/access/v1/admin/config-rollbacks` undoes one version of one table and answers the rollback; the read `GET /api/recovery/access/v1/admin/config-rollbacks/{rollbackId}` answers the stored rollback and its record references.
- **"Any versioned table" is read as the four tables of this service that carry a version label of their own**: `permission.matrix_version` (DF-REF-044), `masking_rule.masking_version` (DF-REF-202), `role_conflict.conflict_version` (DF-REF-209) and `delegation_limit.limit_version` (DF-REF-055). A rollback is a state and date change on the rows already stored, never a copy: the withdrawn rows go to `ROLLED_BACK` and the restored rows to `IN_FORCE`, and every row keeps its `id`, so a case that holds a queue, a role or an approval level keeps it (FSD P4 v3 A2.3 AC-ALT-P4-003-01).
- **`role` is not moved by this story.** FEAT-ACA-03 calls the role list a versioned table, and TSD P4 v3 T3.1 gives `role` no version column; a role is added or retired by the matrix version that carries its permissions, so the rollback of a matrix version restores those permissions and leaves the `role` rows alone (GAP-2280; ASM-3769).
- **The boundary against the other rollback story.** Rule package versions belong to `rwb-decision` (P7) and reference-data versions to `rwb-case` (P3); the gate in front of those two owners is RWB-P4-AD013-APP, which is why this story holds none of their tables and calls neither owner. Both stories trace to the same feature FEAT-ADM-06, and the split is raised as the key's gap (GAP-2280; ASM-3769).
- Every rollback appends two entries to the local decision-record chain of the DP-03 library, in the same transaction as the row changes: one for the withdrawal and one for the restoration. The shared topic is `rwb.decision-record.v1`; the central ledger `decision_log_entry` stays in `rwb-decision` and is neither read nor written here.
- **No business event of its own.** The ownership map gives `rwb-access` zero events, so a rollback announces nothing on `rwb.access.events.v1`; the two record entries are the only messages it publishes, and a reader that needs the new state asks the tables' own reads.
- The panel sits on SCR-39 Rules and parameters and SCR-41 Delegation of authority through the gateway-bff composite route of DP-19; this story renders no screen, starts no workflow and owns no Schedule.

The label scheme of the three tables that are not the delegation table (`MTX-…`, `MSK-…`, `RCF-…`) is Not specified in the source documents (GAP-2280; ASM-3769): only `DOA-2026.11` and `DOA-2027.01` are named, and RWB-P4-E8011-CON fixes the pattern and the ordering rule before the endpoints are frozen.

### 2. Business rationale

Access configuration is the control that goes stale inside a day. A permission matrix with a wrong letter, a masking profile that unmasks a party identifier for the wrong role, a role-conflict pair that stops the wrong two roles being held, or a delegation limit that lets a level approve too much: each is a row set that a business person changes without a release, and each is found after it is in force. The FSD puts the target in one metric — rule and limit changes made without a code release, 100 percent, measured monthly on the decision log and the Workbench records (FSD P4 v3 A2.22.1) — and the Epics 3 to 8 BRD states it as a rule: every threshold, limit, timer, queue, role, template and route is a versioned data row, changed through a validated load without a code release, and rolled back by one call (RULE-001, BR-073).

The monolith could do that because the table, the screen and the decision log were one deployment. In the target the four tables are rows of `rwb_access`, the screen is composed at the edge, and the record is a library with a topic of its own. What has to survive the split is the property the legacy story asserts in one sentence: any versioned table returns to its previous version and the rollback is recorded. Undoing by deleting the bad version would break three things at once — a case would lose the queue row it was routed to, an audit would lose the evidence that the bad version was ever in force, and a reader would see a table version that no record mentions.

The restoration is therefore written as a second fact, not as an erasure. The withdrawn version's rows stay readable with their identifiers, their values and a closing date, and the previous version's rows are reopened with the identifiers they already carry. That is the FSD's alternate flow of the queue table, generalised to the four configuration tables of this service: version 2 in force for every queue row, each queue keeping its record ID, and the rollback recorded with the caller, the time and the reason (FSD P4 v3 A2.3 AC-ALT-P4-003-01).

This story meets REQ-CWC-013 (a validated load goes to production with a version stamp and no code release, and rolls back to the previous version by one call), REQ-DRI-010 (every threshold, limit and name is a versioned row, changed without a code release) and REQ-ACA-013 (administration screens for roles, permissions and delegation), and it carries FEAT-ADM-06. It applies R-UNI-38 at its edge — a version applies from its effective date — and R-UNI-39 in full: an action that cannot be recorded does not proceed, which here is the rule that a record failure leaves every row as it was and answers MSG-P7-003.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E8011-CON (same service, its own contract story) | The OpenAPI 3.1 document of the two operations, the `ConfigRollbackRequest` and `ConfigRollback` schemas, the target-kind set, the version-state set, the error envelope, the consumed-operation list and the contract fakes. This story implements that document and adds no path |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the withdrawal and the restoration entries, hash-linked, in the transaction that writes the rows |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the reason length bound and the rollback switch, as rows with the version in force |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) that serves SCR-39 and SCR-41 and calls the two operations, one hop each |
| The tables the rollback moves | `permission`, `masking_rule`, `role_conflict` and `delegation_limit` exist with their per-service Flyway sequence, created by RWB-P4-AD002-APP, RWB-P4-AD004-APP, RWB-P4-AD005-APP and RWB-P4-E1038-APP; this story adds no table and no column |

Business preconditions carried from RWB-E8-011 and the P4 specifications:

- A version is in force and is found wrong, and the version before it exists, is readable and carries its own values and dates.
- The version states are the values of LOV-VERSION-STATUS: LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED (TSD P4 v3 T3.2). This story produces `ROLLED_BACK` on the withdrawn rows and `IN_FORCE` on the restored ones.
- The right that opens the rollback is the U letter in the capability area of the target kind: PLATFORM_ADMINISTRATION for the permission matrix, the masking profile and the role-conflict table, and RULES_AND_PARAMETERS for the delegation limits (GAP-2280; ASM-3771).
- The effective moment is now: the withdrawn rows close at yesterday and the restored rows are open-ended, and no submitted date is accepted (GAP-2280; ASM-3770).
- The change checklist, the author-and-approver rule and the four-eyes refusal belong to the load and approval gates of the four tables (RWB-P4-AD002-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP) and are not repeated here; a rollback needs its reason and its caller.

### 4. Flow

1. The platform administrator opens SCR-39 Rules and parameters, panel versions, or SCR-41 Delegation of authority through the gateway-bff composite route (DP-19). Each panel lists the version labels it can see with the state of each version.
2. The administrator chooses the version in force that must go and submits it. The route calls `POST /api/recovery/access/v1/admin/config-rollbacks` on `rwb-access` with the body `targetKind`, `versionLabel` and `reason`, and the `Idempotency-Key` of the submission.
3. `ConfigRollbackController` validates the body: `targetKind` is one of `PERMISSION_MATRIX`, `MASKING_PROFILE`, `ROLE_CONFLICT`, `DELEGATION_LIMIT`; `versionLabel` and `reason` are present and the reason is inside the length read in step 5. An empty or malformed field is 422 with MSG-GEN-001 naming the field.
4. The controller calls its own `POST /api/recovery/access/v1/authorise`, one hop with a 2 s timeout and a cached answer, for U in the area that owns the target kind. A caller without U is refused with 403 and MSG-P4-002; no table is read for a write and no entry is written (BR4, AC3).
5. `ParameterReader` reads the reason length bound and the rollback switch through the parameters contract of DP-06, with the version in force. No length and no switch is a constant in code.
6. `ConfigVersionReader` reads the rows of the named version and the label of the version that was in force immediately before it, from the same table: by `valid_from` for `masking_rule`, `role_conflict` and `delegation_limit`, and by the label order the contract fixes for `permission`, which carries no date (GAP-2280; ASM-3769).
7. Three refusals happen before anything is written. A label with no row, or a label that is not the one in force, is 409 with MSG-GEN-004. A table whose named label is the only version it has is 409 with MSG-P3-015, which is the "rollback with no earlier version" refusal of the FSD (FSD P4 v3 A2.3 AC-EXC-P4-003-02). A rollback switch that is off in the parameters is 409 with MSG-GEN-004.
8. `ConfigRollbackService` executes one transaction. The rows of the withdrawn version get `valid_to` yesterday, `state` `ROLLED_BACK` and `is_active` false. The rows of the restored version get `valid_to` null, `state` `IN_FORCE` and `is_active` true. For `permission`, which has neither date column, the two statements move `is_active` and `state` only. No `id` is changed, no row is inserted and no row is deleted (BR1, BR2, BR3).
9. Both facts are appended to the local decision-record chain of DP-03 inside that transaction: a withdrawal entry and a restoration entry, each carrying the target kind, the two labels, the row counts, the caller reference, the reason and the time, and each with its outbox row (BR7).
10. The answer is 201 with `rollbackId`, `targetKind`, `withdrawnVersion`, `restoredVersion`, `effectiveFrom`, `rowsWithdrawn`, `rowsRestored`, `state` `ROLLED_BACK`, the two decision-record references and the `Location` of the read. `rollbackId` is minted here and is opaque to every consumer.
11. `GET /api/recovery/access/v1/admin/config-rollbacks/{rollbackId}` answers the stored rollback and the same two references, so an auditor can quote one identifier instead of a screen state (BR8).
12. Where an entry cannot be written, nothing changes and the call fails with 503 and MSG-P7-003: a configuration change that is not in the decision record cannot be defended, and a half-written pair of statements would leave a table with no version in force (BR7, BR9; legacy RWB-E8-011 AC2). A replay of the same `Idempotency-Key` answers the first answer and writes no second pair of entries (BR10).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | `targetKind`, `versionLabel` or `reason` is empty, or `targetKind` is not one of the four values | 422 naming the field, nothing read for a write and nothing written | MSG-GEN-001 | AC1 |
| X2 | The reason is longer than the bound the parameters hold | 422 naming `reason`, nothing written | MSG-GEN-001 | AC1 |
| X3 | The caller holds no U in the area of the target kind | 403, no table changes and no entry | MSG-P4-002 | AC3 |
| X4 | The caller has no session | 401, nothing written | MSG-P4-001 | AC3 |
| X5 | The label names no row, or is not the version in force | 409, nothing written; the screen reloads | MSG-GEN-004 | AC1 |
| X6 | The table has no version before the named one | 409, the named version stays in force and no entry is appended | MSG-P3-015 | AC5 |
| X7 | The rollback switch is off in the parameters | 409, nothing written | MSG-GEN-004 | AC1 |
| X8 | A record entry cannot be written | 503 and no row changes; the table keeps the version it had | MSG-P7-003 | AC2 |
| X9 | The same request arrives twice with the same `Idempotency-Key` | The first answer is replayed; no second pair of entries and no second change | None | AC4 |

No exception path of this story changes a role, a case or a task: this service moves states and dates of its own four tables and writes its own chain, and the role rows, the case and the task are not touched (section 12.7).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P4-E8011-CON and its fakes; the four tables and their migrations are other P4 stories' and the borrow of a version is a state change, so this story is two operations over four tables |
| Negotiable | The reason length, the rollback switch and the label scheme are parameters and contract values; the target-kind set and the state set are fixed by the contract and reviewed with the security administrator |
| Valuable | One version of one configuration table is undone in one action with the identifiers kept and the two facts recorded, without a release |
| Estimable | Two controllers, two services, one repository per table shape, one record appender, five fakes and six test cases |
| Small | Fits one sprint with its tests; no new table, no workflow, no schedule and no screen of its own |
| Testable | Each owned criterion has a test case in section 16, the identifier preservation is provable by comparing the row ids before and after, and the "no earlier version" refusal is provable on a table with one version |

### 7. Acceptance criteria

```gherkin
Feature: Roll back a configuration version

  Background:
    Given the environment is SIT
    Given permission matrix version "MTX-2026.11" is in force and "MTX-2026.05" was in force before it
    Given test user "U-8201" holds RW-CASEOWN with "R" in "RULES_AND_PARAMETERS" and no letter in "PLATFORM_ADMINISTRATION"
    Given test user "U-8202" holds RW-PLATADM with "CRUD" in "PLATFORM_ADMINISTRATION"
    Given test user "U-8203" holds RW-COE with "CRUD" in "RULES_AND_PARAMETERS"

  Scenario: AC1 Roll back a configuration version (legacy RWB-E8-011 AC1)
    Given the rwb-case contract mock returns parameter version "PAR-2026.11" in force with the rollback reason length and the rollback switch on
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then returns any versioned table to its previous version and records the rollback
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E8-011 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 A role without the right is refused (new, D-RCV-60)
    Given "U-8201" holds "R" in "RULES_AND_PARAMETERS" and no letter in "PLATFORM_ADMINISTRATION"
    When "U-8201" calls POST /api/recovery/access/v1/admin/config-rollbacks for targetKind "PERMISSION_MATRIX" and versionLabel "MTX-2026.11" with a reason
    Then the response is 403 with message MSG-P4-002
    Then no row of permission, masking_rule, role_conflict or delegation_limit changes state and no decision-record entry is appended

  Scenario: AC4 The previous version is restored and every row keeps its identifier (new, D-RCV-60)
    Given "MTX-2026.05" holds the permission rows of role "RW-CASEOWN" with the ids they carry
    When "U-8202" rolls back "MTX-2026.11" with a reason
    Then the response is 201 with targetKind "PERMISSION_MATRIX", withdrawnVersion "MTX-2026.11", restoredVersion "MTX-2026.05", state "ROLLED_BACK" and two decision-record references
    Then every permission row of "MTX-2026.05" is in force again with the same id it had before the rollback
    Then every permission row of "MTX-2026.11" carries is_active false and state "ROLLED_BACK" and is still readable
    Then exactly two decision-record entries carry the caller reference, the time and the reason, one for each fact
    When the same request is repeated with the same Idempotency-Key
    Then the first answer is replayed and no third entry is appended

  Scenario: AC5 A table with no earlier version is refused (new, D-RCV-60)
    Given the role-conflict table has one version "RCF-2026.11" and no version before it
    When a caller holding the right in "PLATFORM_ADMINISTRATION" rolls back "RCF-2026.11"
    Then the response is 409 with message MSG-P3-015
    Then "RCF-2026.11" stays in force and no decision-record entry is appended

  Scenario: AC6 A stored rollback is read back unchanged and its record holds references only (new, D-RCV-60)
    Given the rollback of "MTX-2026.11" is stored with its two decision-record references
    When the rollback is read after the permission tables change
    Then the stored answer and its two record references are returned unchanged and not recomputed
    Then the two record entries carry references, labels, counts and times only, with no name, e-mail address or personal field

  Scenario: AC7 A call with no credential or an unknown version is answered 401 or 404 (new, D-RCV-60)
    Given no credential is sent with POST /api/recovery/access/v1/admin/config-rollbacks
    When the call is made for targetKind "PERMISSION_MATRIX" and versionLabel "MTX-2026.11"
    Then the response is 401 and no row changes state and no decision-record entry is appended
    Given "U-8202" holds CRUD in "PLATFORM_ADMINISTRATION"
    When "U-8202" rolls back a versionLabel that is not in the permission matrix
    Then the response is 404 and no row changes state and no decision-record entry is appended

  Scenario: AC8 A consumed call that fails or does not answer changes nothing (new, D-RCV-60)
    Given the rwb-case contract mock fails or does not answer
    When "U-8202" rolls back "MTX-2026.11" with a reason
    Then no row changes state and no decision-record entry is appended
    Then the answer is Not specified in the source documents (NEWAC-RWB-P4-E8011-APP-AC8)
```

AC1 and AC2 are the two criteria of RWB-E8-011, copied with their text unchanged and their values kept; AC1 carries one added line at the top of its scenario, the parameters mock, so the rollback is provable while the parameters contract is still a fake. AC3 to AC8 are new under D-RCV-60 and test only what this story adds.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A rollback is a state and date change on the rows already stored: the withdrawn rows go to `ROLLED_BACK` with `valid_to` yesterday and `is_active` false, and the restored rows to `IN_FORCE` with `valid_to` null and `is_active` true | FSD P4 v3 A2.22; A2.3 AC-ALT-P4-003-01; ASM-3769 |
| BR2 | No row is inserted, no row is deleted and no `id` changes in a rollback; a superseded or withdrawn row stays readable with its values | FSD P4 v3 A2.3 AC-ALT-P4-003-01; TSD P4 v3 T3.1 |
| BR3 | The version before the named one is the label that was in force immediately before it in the same table, read by `valid_from` where the table carries dates and by the contract's label order for `permission` | ASM-3769; TSD P4 v3 T3.1 |
| BR4 | A rollback needs U in the capability area of the target kind: PLATFORM_ADMINISTRATION for the matrix, the masking profile and the role conflicts and RULES_AND_PARAMETERS for the delegation limits | TSD P4 v3 T6.1; ASM-3771 |
| BR5 | The effective moment is now: the withdrawn rows close at yesterday and the restored rows are open-ended, and no submitted date is accepted | ASM-3770; R-UNI-38 |
| BR6 | A table with no version before the named one refuses the rollback with MSG-P3-015 and the named version stays in force | FSD P4 v3 A2.3 AC-EXC-P4-003-02 |
| BR7 | Every rollback appends two entries to the local decision-record chain of DP-03 in the same transaction as the row changes, one for the withdrawal and one for the restoration; an action that cannot be recorded is not taken | R-UNI-39; legacy AC2; DP-03 |
| BR8 | The read of a rollback answers the stored answer and its two record references, and never recomputes them from the tables | ASM-3772; DP-03 |
| BR9 | No value a business person may change is written in code: the labels, the states, the reason bound and the switch are rows and values with a version | BR-P4-022; FSD P4 v3 A2.22.3.1; REQ-DRI-010 |
| BR10 | A request is idempotent by `Idempotency-Key`: a replay answers the first answer and appends no third entry | Architecture v5 slide 42; DP-09 |
| BR11 | The record of a rollback carries references, labels, counts and times only: no name, no e-mail address and no personal field | NFR-040; legacy guardrails |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 and BR2 are two update statements per table shape and no delete statement in the repository, so a withdrawn row cannot disappear.
- BR3 is one ordered read of the same table; where no earlier label exists the read returns nothing and BR6 answers instead.
- BR4 is one call to the own authorise operation with the area derived from the target kind; the letters come from `permission` rows and never from a role name in code.
- BR5 is the service clock: `valid_to` is the business date minus one day and the restored window is open-ended, so no caller can back-date a configuration change.
- BR7 is the record appender of DP-03 inside the transaction; a failure rolls the two statements back, which is why AC2 sees nothing change.
- BR10 is the `idempotency_key` row written in the transaction of the first answer; a replay returns the stored answer.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| A version `IN_FORCE`, an earlier version `SUPERSEDED` | A rollback is submitted | U held, the label is the one in force, an earlier version exists | The named version `ROLLED_BACK`; the earlier version `IN_FORCE` |
| A version `IN_FORCE` | A rollback is submitted | No U, or a field missing, or the label is not in force | Nothing changes; 403, 422 or 409 |
| A version `IN_FORCE`, no earlier version | A rollback is submitted | The table has one version only | Nothing changes; 409 with MSG-P3-015 |
| A version `IN_FORCE` | A record entry cannot be written | The chain write fails | Nothing changes; 503 with MSG-P7-003 |
| `ROLLED_BACK` | A later load of the same table | Another story loads a new version | `ROLLED_BACK` stays readable; the new version becomes the one in force |

| Chain | Event | Outcome |
|---|---|---|
| Append-only local chain | A rollback | Two entries appended with their `prev_hash` and `entry_hash`; no entry is ever updated or deleted |
| `rwb.access.events.v1` | A rollback | Nothing published: `rwb-access` owns no business event in the ownership map |

A withdrawn version is never deleted and never rewritten: it keeps its rows, its values and its label, so an audit can still prove what was in force and when it was undone.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Platform administrator (RW-PLATADM) | Roll back the permission matrix, a masking profile or a role-conflict version with CRUD in Platform administration (TSD P4 v3 T6.1); the actor of the legacy story |
| Center of excellence analyst (RW-COE) | Roll back a delegation limit version with CRUD in Rules and parameters, the "U … and roll back" refinement of T6.1; loads and approvals are other stories' |
| Risk and model risk officer (RW-RISK) | Holds RA in Rules and parameters and no U: a rollback submitted under that role is refused with MSG-P4-002 |
| Case owner (RW-CASEOWN) and every business role | R only in Rules and parameters and no letter in Platform administration: refused with 403 and MSG-P4-002 (AC3) |
| Internal audit (RW-AUDIT) and Compliance and PDPA officer (RW-COMPLY) | Read the two entries through the central ledger and the change report; they roll nothing back here |
| Security administrator (RW-SECADM) | Holds CRUDA in Platform administration and R in Rules and parameters; the right covers the matrix, the masking profile and the conflicts, and this story adds no path of its own for that role |
| The gateway-bff route | Calls the two operations on behalf of the signed-in user, one hop each, and passes the `Idempotency-Key` of the submission unchanged |
| `rwb-access` itself | Reads and writes its own four tables, reads `role` and `permission` for the authority answer, and writes its own chain and outbox |

The refusal shapes are 403 with an RFC 9457 problem response and `messageId` MSG-P4-002 for an absent right, 401 with MSG-P4-001 for no session, 409 with MSG-GEN-004 for a label that is not in force and MSG-P3-015 for no earlier version, 422 with MSG-GEN-001 for a field, and 503 with MSG-P7-003 for a record that cannot be written. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-E1037-CON.

### 11. Data

| BR Field ID | Table in `rwb_access` | Fields | Read or write |
|---|---|---|---|
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read: the rows of both labels. Write: `matrix_version` untouched; the standard columns of the rows of both labels |
| DF-REF-198 to DF-REF-204 | `masking_rule` | id, role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read: the rows of both labels. Write: `valid_to` on the withdrawn rows |
| DF-REF-205 to DF-REF-211 | `role_conflict` | id, role_code, conflicts_with, reason, conflict_version, valid_from, valid_to | Read: the rows of both labels. Write: `valid_to` on the withdrawn rows |
| DF-REF-016 to DF-REF-026, DF-REF-055 to DF-REF-062 | `delegation_limit` | id, decision_code, approval_level, product_group, the four amounts, holder_user_id, substitute_user_id, valid_from, valid_to, limit_version, regulation_item, applies_when, the four conditions | Read: the rows of both labels. Write: `valid_to` and the standard state of the rows of both labels |
| TSD P4 v3 T3.0 | all four tables | `is_active`, `state`, `version`, `updated_at`, `updated_by` | Write: `state` `ROLLED_BACK` and `IN_FORCE`, `is_active`, the optimistic lock, the caller reference in `updated_by` |
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read only: the caller's role and its class. A rollback moves no role row |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the withdrawal entry and the restoration entry: `decision_code` DF-DEC-003, `inputs_ref` DF-DEC-008 with the target kind, the two labels, the counts, the caller reference and the reason, `case_id` DF-DEC-002 empty, `decided_at` DF-DEC-016, `prev_hash` DF-DEC-017, `entry_hash` DF-DEC-018 | Write |
| (outbox) | `outbox_event` in `rwb_access` | the two record rows, with the stored answer of the idempotency row | Write |
| (idempotency) | `idempotency_key` in `rwb_access` | the key of the submission, with the stored answer | Write |
| (inbox) | `processed_event` | none: this story consumes no event | None |

No row of `decision_log_entry`, `rule_package_version`, `reference_version`, `lov_value`, `case` or `task` is read or written: the central ledger and the rule registry are `rwb-decision`'s (P7), reference data is `rwb-case`'s (P3), the list of values is P3 reference data under the ownership ruling, and no foreign key crosses a schema (DP-01). Field IDs are those of the Logical Data Model and Data Dictionary v9.

The names and types of the request and answer fields, the label scheme of the three tables that are not the delegation table, the ordering rule that decides the "version before", and the record codes of the two entries are Not specified in the source documents (GAP-2280; ASM-3769, ASM-3772): RWB-P4-E8011-CON fixes them and this story reads and writes them as that contract publishes them.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| POST | `/api/recovery/access/v1/admin/config-rollbacks` | P4 `rwb-access` | Body: `targetKind`, `versionLabel`, `reason` | `rollbackId`, `targetKind`, `withdrawnVersion`, `restoredVersion`, `effectiveFrom`, `rowsWithdrawn`, `rowsRestored`, `state` `ROLLED_BACK`, `decisionRecordRefs`, `Location` | 401 (MSG-P4-001); 403 (MSG-P4-002); 409 (MSG-GEN-004, MSG-P3-015); 422 (MSG-GEN-001); 503 (MSG-P7-003) | U in the area of the target kind, scope applied | `Idempotency-Key` required; a replay answers the first answer |
| GET | `/api/recovery/access/v1/admin/config-rollbacks/{rollbackId}` | P4 `rwb-access` | Path: `rollbackId` | The stored answer of the rollback and its two record references | 401 (MSG-P4-001); 403 (MSG-P4-002); 404 (MSG-GEN-004) | R in the area of the target kind | Read; no key |

Both operations sit on the base `/api/recovery/access/v1` of DP-13. The named table's version is the identity the rollback works on and the `rollbackId` is the identity the audit quotes; the read never recomputes the answer from the tables, so a later load cannot change the record of an earlier rollback. Neither path is in Recovery Workbench API Specification v5, which declares no rollback of a configuration version for this service; the paths and fields are fixed by RWB-P4-E8011-CON and confirmed at its contract review (GAP-2280; ASM-3769).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (own service) | The U check in the area of the target kind, cached for the session; MSG-P4-002 on a refusal |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case` | The reason length bound and the rollback switch, as parameter rows with the version in force (DP-06) |

One hop per call, 2 s timeout and a breaker per downstream (DP-11); the parameter read is cached for the life of the request. No operation of `rwb-decision`, `rwb-case`, `rwb-comms` or `rwb-document` beyond the parameters read is called, and the loads, approvals and the AD013 gate are not called.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | the hash-chained withdrawal entry and restoration entry of a rollback, each with the target kind, the two labels, the counts, the caller reference and the reason |

CloudEvents 1.0 envelope, from the outbox of the transaction that writes the rows. `rwb-access` owns no business event in the ownership map, so a rollback publishes nothing on `rwb.access.events.v1`; a reader that needs the new state reads the table through its own contract. The entry carries no name, no e-mail address and no personal field, and the `holder_user_id` and `substitute_user_id` of a delegation row are never carried (BR11).

#### 12.4 Events consumed

None. `rwb-access` is a configuration owner with no inbound event for this capability, and a rollback of its own tables needs no subscription. The `processed_event` table is written by no part of this story.

#### 12.5 Workflows and activities

None. A rollback is synchronous and immediate: this story starts no workflow, signals no workflow and registers no activity on the `rwb-access` queue. `ApprovalWorkflow` of the workflow kit is P7's and is not used for an administration change of this service.

#### 12.6 Schedules

None. A rollback takes effect at the moment of the call and needs no timer. The six-monthly access review list (JOB-18) is the only Schedule of `rwb-access` and belongs to RWB-P4-AD008-APP.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `permission` | P4 (`rwb_access`) | Read: the rows of both labels. Write: the standard state and `is_active` of both sets. Created by RWB-P4-AD002-APP |
| `masking_rule` | P4 (`rwb_access`) | Read: the rows of both labels. Write: `valid_to` and the state of both sets. Created by RWB-P4-AD004-APP |
| `role_conflict` | P4 (`rwb_access`) | Read: the rows of both labels. Write: `valid_to` and the state of both sets. Created by RWB-P4-AD005-APP |
| `delegation_limit` | P4 (`rwb_access`) | Read: the rows of both labels. Write: `valid_to` and the state of both sets. Created by RWB-P4-E1038-APP |
| `role` | P4 (`rwb_access`) | Read only: the caller's role and class. A rollback moves no role row (ASM-3769) |
| the local decision-record table of the DP-03 library | P4, in `rwb_access` | Write: the withdrawal entry and the restoration entry |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | The two record rows and the stored answer; no inbox row, because no event is consumed (DP-09) |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written: the central ledger entry is P7's and the local record travels on `rwb.decision-record.v1` |

`lov_value` and the `reference_version`/`reference_row` pair are reference data of P3 under the ownership ruling; this story's pattern list carries no DP-07 and its contract-dependency list no `RWB-P3-E1043-CON`, so the state values it writes are the contract's own and not a list read (GAP-2280; ASM-3769). No table of another service is read and no foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| authorise fake | RWB-P4-E1037-CON, RWB-P4-E8011-CON | Granted for RW-PLATADM with CRUD in Platform administration and for RW-COE with CRUD in Rules and parameters; refused with MSG-P4-002 for RW-CASEOWN with R only |
| parameters fake (rwb-case) | RWB-P3-E1042-CON | The reason length and the rollback switch, on and off, at version PAR-2026.11; library version Not specified in the source documents (DOR-RWB-P4-E8011-APP-22) |
| decision-record fake | RWB-PLT-E1027-CON | The append of a withdrawal and a restoration, the hash-link check, the replay of an `Idempotency-Key`, and the forced failure AC2 needs |
| configuration fixture | RWB-P4-E8011-CON, seeded from the tables' own stories | `MTX-2026.05` and `MTX-2026.11` with the same role rows and different letters, `MSK-2026.11`, `RCF-2026.11` as a single version, and the DoA versions `DOA-2026.11` and `DOA-2027.01` |
| gateway-bff fake | RWB-PLT-N001-CON | The composite route of SCR-39 and SCR-41 with the version panel, the rollback form with its reason, and the rolled-back state |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2 (the rollback and its read); consumed 2 | Base `/api/recovery/access/v1`; one hop, 2 s timeout |
| Kafka | Published 1 event type; consumed 0 | `rwb.decision-record.v1` through the DP-03 library; no `rwb.access.events.v1` message |
| Temporal | 0 workflows, 0 activities | The `rwb-access` queue carries the access review Schedule of RWB-P4-AD008-APP only |
| File | None | No file input and no file output; the loads of the four tables are other stories' |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/config`, Java package `th.co.scb.ace.workbench.recovery.access.config.rollback`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the in-process update of the single `recovery` schema and the ace-web screen that performed the rollback in process (DP-01 and DP-13: a state change on the service's own tables on the service's own base; DP-19: a gateway-bff composite route). DP-01, DP-02, DP-09 and DP-11 govern the service baseline and the one-hop budget of section 12.2; they add no dependency of their own, they are not in the pattern list the Work Package fixes for this story, and they are not claimed as patterns of it. The reference-list check of a restored row would need DP-07 and `RWB-P3-E1043-CON`, neither of which the metadata carries, so a restored row keeps the values it already held and the point is raised as the key's gap.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ConfigRollbackController | Controller | `POST /admin/config-rollbacks`: validation, the RFC 9457 problem responses, the `Idempotency-Key` read, the three 409 refusals |
| ConfigRollbackReadController | Controller | `GET /admin/config-rollbacks/{rollbackId}`: the stored answer and its two record references |
| ConfigRollbackService | Service | BR1, BR2 and BR5: the two updates per table shape in one transaction, and the answer |
| ConfigVersionReader | Service | BR3 and BR6: the rows of both labels, the label before the named one, and the no-earlier-version answer |
| ConfigRollbackRepository | Repository | The reads of both labels and the state and date updates for the four table shapes; no insert and no delete method |
| AreaRightResolver | Service | BR4: the capability area of the target kind and the U check through the own authorise call |
| PermissionReader | Service | The `role` and `permission` rows of the caller and the U letter of the area that owns the configuration data |
| ConfigRollbackRecordAppender | Service | The withdrawal entry and the restoration entry, with their outbox rows, in the transaction that moves the rows (DP-03) |
| CaseDataClient | Client | The parameters read of DP-06, one hop, 2 s timeout, cached |

**Database and migrations**

- This story adds no table and no column: the four tables and their per-service Flyway sequence belong to the stories that create them (DP-15), and this story moves their rows. If the SIT query plan needs an index for the version-in-force read of a table, the index is added to that table's story, not to a new migration here.
- No reader may see a table with no version in force between the two statements: both run in one transaction, and the withdrawal is written before the restoration so a partial commit cannot leave the tables open.
- There is no insert and no delete statement in the repository, so a withdrawn version can never be removed and a restored row keeps its `id`.
- The two record rows, their outbox rows and the idempotency row commit with the updates; a failure rolls all of them back and the call fails with MSG-P7-003.

**Configuration and reference data**

- The reason length bound and the rollback switch are parameter rows of `rwb-case` read through DP-06 with the version in force; neither is a constant in code (BR9).
- The target-kind set, the state set and the label pattern are contract constants of RWB-P4-E8011-CON, not values of this service's tables.
- No label, state, count or date is a constant in code or in a test fixture outside the seeded configuration fixture of section 12.8.

**Build steps**

1. `ConfigRollbackRepository` for the four shapes with the reads of both labels and the two updates; test that no insert and no delete exists and that a rollback leaves every `id` unchanged (AC4).
2. `ConfigVersionReader` and the label-before rule of BR3, including the tabular order for `permission`; test the single-version refusal of AC5.
3. `AreaRightResolver` and the U check of BR4; test the refusal of AC3 with nothing changed.
4. `ConfigRollbackService` with the one transaction of BR1, BR2 and BR5; test the withdrawn and restored states and dates on a fixed clock.
5. `ConfigRollbackRecordAppender` in the same transaction; test that exactly two entries leave the outbox per rollback and that neither carries a personal field.
6. The forced failure of AC2: 503, MSG-P7-003 and no row changed.
7. `CaseDataClient` over the parameters fake, so the story builds before `rwb-case` is in the environment; test that a changed reason bound is data and needs no build.
8. The replay test of X9 and the read of `rollbackId` after the fact, so the stored answer does not follow a later load.
9. The contract-fake run through the gateway-bff fake, so SCR-39 and SCR-41 can be demonstrated while the route is being built.

**Feature switch.** Both operations are switched by the service baseline of RWB-P4-E1037-CON and by the rollback switch parameter; the contract declares no 404 branch of its own and adds no second parameter.

**Done when.** The tests in section 16 pass; a rollback of `MTX-2026.11` answers `MTX-2026.05` with every `id` kept and two record references; the withdrawn rows are `ROLLED_BACK` and still readable; a table with one version is refused with MSG-P3-015; a caller without U is refused with MSG-P4-002; and a forced failure of the record leaves every row as it was with MSG-P7-003.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The caller has no session | You have no Recovery Workbench role. Ask your team manager to request one. | This story, on the rollback |
| MSG-P4-002 | The caller holds no U in the area of the target kind | You cannot {action} here. Your role does not include it. | This story, on the rollback |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. | This story, in the answer of the rollback |
| MSG-GEN-001 | A required field is empty, the reason is too long, or `targetKind` is not one of the four values | Enter {field}. | This story, on the rollback |
| MSG-GEN-004 | The label names no row, is not the version in force, the switch is off, or `rollbackId` is unknown | Someone else changed this record. Reload it to see their change. | This story, on both operations |
| MSG-P3-015 | The table has no version before the named one | Not specified in the source documents (GAP-2280; ASM-3772) | This story, on the rollback |
| MSG-P7-003 | A record entry cannot be written, or the outbox row cannot be staged | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the rollback |

Every error from this service is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. The business texts are copied unchanged from the legacy story where the message already existed: MSG-P4-001, MSG-P4-002, MSG-P4-004, MSG-GEN-001 and MSG-P7-003 are the legacy texts, and MSG-GEN-004 is the platform text. MSG-P3-015 is named by the FSD and its text is Not specified in the source documents (GAP-2280; ASM-3772); the message catalogue supplies it and the contract carries its `messageId` only.

### 15. Screens and states

The rollback is one panel serving SCR-39 Rules and parameters and SCR-41 Delegation of authority, reached through the gateway-bff composite route of DP-19, which lists the versions of a table and calls the two operations of this story, one hop each.

| Screen | State | What it shows |
|---|---|---|
| SCR-39 Rules and parameters | Versions, list | The version labels of the permission matrix, the masking profile and the role-conflict table with their state, the version in force marked |
| SCR-39 Rules and parameters | Rollback, form | The named version, the label that will be restored, the reason field with its bound, and the two record references the answer will carry |
| SCR-39 Rules and parameters | Rollback, done | The `rollbackId`, the withdrawn and restored labels, the counts and the two record references |
| SCR-39 Rules and parameters | Rollback, refused | The 403 of MSG-P4-002, the 409 of MSG-GEN-004 or MSG-P3-015, and the 422 of MSG-GEN-001 naming the field |
| SCR-39 Rules and parameters | Rollback, not recorded | The 503 of MSG-P7-003 with every row as it was |
| SCR-39 Rules and parameters | Empty | Not specified in the source documents (DOR-RWB-P4-E8011-APP-10; CG-ALL-5525) |
| SCR-39 Rules and parameters | Loading | Not specified in the source documents (DOR-RWB-P4-E8011-APP-10; CG-ALL-5525) |
| SCR-39 Rules and parameters | Error | Not specified in the source documents (DOR-RWB-P4-E8011-APP-10; CG-ALL-5525) |
| SCR-39 Rules and parameters | No access | Not specified in the source documents (DOR-RWB-P4-E8011-APP-10; CG-ALL-5525) |
| SCR-41 Delegation of authority | Versions, list | The DoA version labels with their state, the version in force marked, and the rollback action for a caller holding U in Rules and parameters |
| SCR-41 Delegation of authority | Rollback, done | The withdrawn and restored DoA versions, the counts and the two record references |
| SCR-41 Delegation of authority | Empty | Not specified in the source documents (DOR-RWB-P4-E8011-APP-10; CG-ALL-5526) |
| SCR-41 Delegation of authority | Loading | Not specified in the source documents (DOR-RWB-P4-E8011-APP-10; CG-ALL-5526) |
| SCR-41 Delegation of authority | Error | Not specified in the source documents (DOR-RWB-P4-E8011-APP-10; CG-ALL-5526) |
| SCR-41 Delegation of authority | No access | Not specified in the source documents (DOR-RWB-P4-E8011-APP-10; CG-ALL-5526) |

The legacy story named SCR-39 and SCR-41 for the same action; the legacy endpoints it carried are rule-version paths that belong to `rwb-decision` and to the load and approval stories of this service, and this story keeps the screen attribution and adds no panel of its own. The composite route specification and the screen field list belong to RWB-PLT-N001-CON and to the Epic 8 screen work.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-011-01 | AC1, BR1, BR2, BR5 | Contract | A rollback of `MTX-2026.11` with the parameters at version PAR-2026.11 and the switch on: the answer of the rollback, the restoration of `MTX-2026.05`, and the rows' state and dates |
| TC-E8-011-02 | AC2, BR7 | Component | The record store forced to fail during a rollback: 503, MSG-P7-003 and no row changed |
| TC-E8-011-03 | AC3, BR4 | Component | A caller holding RW-CASEOWN with R only: 403, MSG-P4-002, no state change and no entry |
| TC-E8-011-04 | AC2, BR7 | NFR | The two entries and their outbox rows inside the transaction of the updates, the idempotency row, and the rollback when an entry does not commit |
| TC-E8-011-05 | AC4, BR2, BR3, BR10 | Component | Two versions of the permission matrix: every restored `id` unchanged, the withdrawn rows `ROLLED_BACK` and readable, two entries with the caller, the time and the reason, and the replay of one `Idempotency-Key` |
| TC-E8-011-06 | AC5, BR6 | Component | A table with a single version: 409 with MSG-P3-015, the version still in force and no entry |
| TC-E8-011-07 | AC1, BR1, BR3, BR6 | Component | Boundary of each table of §12.7 (`permission`, `masking_rule`, `role_conflict`, `delegation_limit`) per ASM-3438: the first and last version of each table, and a table with one version |
| TC-E8-011-08 | BR8 | Component | The read of a rollback after the tables change: the stored answer and its two record references returned unchanged, not recomputed |
| TC-E8-011-09 | BR9 | Component | Changing a label, state, the reason bound or the switch row: the rollback follows the stored value with no code release |
| TC-E8-011-10 | BR11 | NFR | The two record entries inspected: references, labels, counts and times only, with no name, e-mail address or personal field |
| TC-E8-011-11 | AC6, BR8, BR9, BR11 | Component | The stored answer of a rollback read after the permission tables change and a label row changed: the answer and its two references returned unchanged, the rollback following the stored value, and the two entries with references, labels, counts and times only |
| TC-E8-011-12 | AC7 | Component | A call with no credential: 401 with no row changed and no entry; a rollback of a version not in the permission matrix: 404 with no row changed and no entry |
| TC-E8-011-13 | AC8 | Component | The rwb-case contract mock failing or not answering during a rollback: no row changed and no entry; the answer as Not specified in the source documents (NEWAC-RWB-P4-E8011-APP-AC8) |

The full test, with its Given, When and Then, is added to the next version of Recovery Workbench Test Cases, tab Story test cases, under the same test case ID. The four legacy rows are kept: TC-E8-011-01 for AC1, TC-E8-011-02 for AC2, TC-E8-011-03 for the access refusal of the legacy `Access` test and TC-E8-011-04 for the forced record failure of the legacy `Principle 5` test; two rows are added for AC4 and AC5. The legacy test table carries a Covers column and no Level column: `Access` is read as Component and `Principle 5` as NFR, and the Level of each row is this template's assignment under §R7.2 s16. No `-ITG` id appears here, because no integration story is split from this key.

### 17. Guardrails

- No business value in code: the labels, the states, the reason bound and the switch are rows and values with a version, and a test proves that a changed bound needs no build (BR9).
- No personal data anywhere: the rollback takes a caller reference, the answers carry labels, counts, states and times, and neither the entries nor the outbox rows carry a name, an e-mail address or a personal field (BR11).
- No read of another service's tables (DP-01): the central ledger and the rule registry are P7's, reference data and the list values are P3's, and no join crosses a schema.
- ACE data only through the owner's contract or the service's own `v_ace_*` views: this story reads no ACE data; the group-to-role mapping is the service baseline's.
- One writer per table: the rollback moves state and dates only through the two operations, and no other path of the service deletes a configuration row. The repository has no delete method, so a withdrawn version is never removed.
- No write without its record: the updates, the two entries and the outbox rows commit together, and the rollback is withheld with MSG-P7-003 when the record cannot be written (BR7, R-UNI-39).
- Identifiers are stable: a restored row keeps its `id`, so no case, queue membership or approval level is silently re-pointed by a rollback (BR2).
- One version in force: the two statements run in one transaction, withdrawal first, so no reader sees a table with no version in force.
- A refused caller learns nothing about the data: the refusal names the missing right or the missing earlier version and returns no row value.
- Idempotent by key: a retried submission answers the first answer and appends no third entry.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-013 | A rule change goes from a validated template load to production with a version stamp and no code release, and rolls back to the previous version by one call | Program 5.3; Epics 3 to 8 8.6 | FEAT-ADM-06 | 20 Administer access and audit | BR1, BR2, BR6 | TC-E8-011-01, TC-E8-011-06 |
| REQ-DRI-010 | A parameter catalog and a configuration service hold every threshold, limit and name, versioned, changed without a code release | Program 5.7; Epics 3 to 8 9 | FEAT-ADM-06 | 20 Administer access and audit | BR5, BR9 | TC-E8-011-01, TC-E8-011-05 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator | Program 5.4; Epics 3 to 8 8.6 | FEAT-ADM-06 | 20 Administer access and audit | BR4, BR7 | TC-E8-011-03, TC-E8-011-04 |

The requirement IDs are taken from the FSD feature table and the Program BRD under the fill order of Template and Rules §R7.3, which is the order the Work Package directs; the Work Package itself carries no requirement list for this key.

| Legacy reference | Where it is kept |
|---|---|
| AC1 any versioned table returned to its previous version and the rollback recorded, written to the decision log with the rule version | Sections 4, 7, 8, 12.1, 13 |
| AC2 not recorded: nothing changes and the user sees MSG-P7-003 | Sections 4, 5, 7, 8, 12.1, 16 |
| The permission check: Rules and parameters C for RW-COE and A for RW-RISK | Sections 3, 10, 12.1, 14 |
| The data table: `role` and `rule_row` fields | Sections 11, 12.7 |
| The endpoints of the legacy story: the rule-version paths that are P7's and not built here | Section 19 |
| Legacy screens SCR-39 and SCR-41 as the story named them | Section 15 |
| MSG-P4-002, MSG-P4-004, MSG-GEN-001, MSG-P7-003 and MSG-P3-015 | Section 14, exception paths |
| TC-E8-011-01 to TC-E8-011-04 | Section 16 |
| BR-P4-022, VR-P4-022-1, R-UNI-38, R-UNI-39 | Sections 2, 8, 14, 17 |
| Field IDs DF-REF-016 to DF-REF-026, DF-REF-034 to DF-REF-044, DF-REF-055 to DF-REF-062, DF-REF-198 to DF-REF-211, DF-DEC-001 to DF-DEC-018 | Section 11 |
| Legacy key RWB-E8-011, story RWB-P4-E8011-APP, contract RWB-P4-E8011-CON | Metadata, sections 3, 12 |
| The queue rollback example of version 3 to version 2 and the record-ID rule | Sections 1, 2, 7, 12.8 |

### 19. Out of scope

- The rule package versions of `rwb-decision` (P7) and the reference-data versions of `rwb-case` (P3), and the rollback gate in front of them: RWB-P4-AD013-APP. This story holds neither table and calls neither owner.
- The load, the approval and the four-eyes rule of the four tables: RWB-P4-AD002-APP, RWB-P4-AD004-APP, RWB-P4-AD005-APP and RWB-P4-E1038-APP. A rollback needs its reason and its caller, and no checklist.
- The tables' own migrations, columns and indexes, and the per-service Flyway sequence (DP-15).
- The role list itself: RWB-P4-AD001-APP and RWB-P4-E1019-APP; a rollback moves no `role` row.
- The lookup `GET /api/recovery/access/v1/doa-limits` and the authority decision behind `POST /authorise`: RWB-P4-E2013-APP and RWB-P4-E1037-APP.
- The decision log report of a configuration change, its monthly measure and the read of the central ledger: `rwb-decision` (P7) and RWB-P4-E2041-APP.
- The screens SCR-39 and SCR-41 themselves, their other panels and their composite route specification: RWB-PLT-N001-CON and the Epic 8 screen work.
- The integration harness and the `-ITG` copies of the test cases.
- The Helm chart, the Kafka values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
